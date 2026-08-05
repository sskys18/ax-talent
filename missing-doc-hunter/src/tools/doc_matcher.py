#!/usr/bin/env python3
"""Interpret PBC requests and match them against a local evidence manifest.

Standard library only. No pandas, no external APIs. The matcher is deliberately
conservative: when sufficiency cannot be determined safely it classifies the
request as "Needs human review" rather than asserting readiness.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Request type configuration
# ---------------------------------------------------------------------------

# Sources that are too weak to stand alone as submission evidence.
WEAK_SOURCES = {"email", "chat", "screenshot", "placeholder", "unknown", "manual note", "verbal"}

# Approval-status values that count as acceptable.
APPROVED_STATUSES = {"approved", "signed", "final"}

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

TYPE_CONFIG: Dict[str, Dict[str, object]] = {
    "receivables": {
        "match_tokens": ["receivable", "receipt", "collectab", "customer term"],
        "purpose": "Support existence, valuation, and collectability of accounts receivable at period end.",
        "required_keys": ["customer_id", "invoice_id", "due_date", "amount", "receipt_date"],
        "required_evidence": [
            {"label": "Receivables aging report", "tokens": ["aging"]},
            {"label": "90+ day collectability assessment", "tokens": ["collectab"]},
            {"label": "Customer contract terms", "tokens": ["customer term", "contract term", "terms"]},
            {"label": "Subsequent cash receipts", "tokens": ["receipt", "subsequent"]},
        ],
        "requires_approval": False,
        "tb_account": "Accounts receivable",
    },
    "cutoff": {
        "match_tokens": ["cutoff", "revenue", "sales invoice", "delivery", "shipment", "tax invoice"],
        "purpose": "Test that revenue is recognized in the correct period (cutoff).",
        "required_keys": ["invoice_id", "contract_id", "shipment_date", "revenue_recognition_date"],
        "required_evidence": [
            {"label": "Signed contracts for sampled transactions", "tokens": ["contract"]},
            {"label": "Tax invoices", "tokens": ["invoice"]},
            {"label": "Delivery / shipment evidence", "tokens": ["delivery", "shipment"]},
        ],
        "requires_approval": False,
        "tb_account": "Revenue",
    },
    "journal entry": {
        "match_tokens": ["journal", "preparer", "reviewer", "approval"],
        "purpose": "Test manual journal entries for appropriate preparation, review, and approval.",
        "required_keys": ["journal_id", "preparer", "reviewer", "approval_date"],
        "required_evidence": [
            {"label": "Manual journal entry list", "tokens": ["journal", "manual"]},
            {"label": "Preparer information", "tokens": ["preparer"]},
            {"label": "Reviewer approval logs and approval dates", "tokens": ["approval", "reviewer"]},
        ],
        "requires_approval": True,
        "tb_account": "Manual journal entries",
    },
    "inventory": {
        "match_tokens": ["inventory", "slow moving", "nrv", "allowance", "valuation"],
        "purpose": "Support inventory valuation and the slow-moving/obsolescence allowance.",
        "required_keys": ["item_id", "aging_days", "nrv", "allowance_amount"],
        "required_evidence": [
            {"label": "Valuation allowance calculation support", "tokens": ["allowance", "valuation"]},
            {"label": "Slow-moving inventory list", "tokens": ["slow moving", "aging"]},
        ],
        "requires_approval": False,
        "tb_account": "Inventory",
    },
    "related party": {
        "match_tokens": ["related party", "counterparty", "settlement"],
        "purpose": "Support completeness and terms of related-party transactions and settlements.",
        "required_keys": ["counterparty", "contract_id", "transaction_amount", "terms"],
        "required_evidence": [
            {"label": "Related-party transaction listing", "tokens": ["related party", "transaction"]},
            {"label": "Contract terms", "tokens": ["contract", "terms"]},
            {"label": "Settlement evidence", "tokens": ["settlement"]},
        ],
        "requires_approval": False,
        "tb_account": "Related-party receivables",
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def normalize(value: object) -> str:
    """Lowercase and collapse punctuation so tokens can be substring-matched."""
    text = str(value or "").lower()
    return re.sub(r"[^a-z0-9가-힣]+", " ", text).strip()


def read_csv_rows(path: str) -> List[Dict[str, str]]:
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def classify_request_type(request_text: str) -> Optional[str]:
    text = normalize(request_text)
    if "cutoff" in text:
        return "cutoff"
    if "journal" in text:
        return "journal entry"
    if "inventory" in text:
        return "inventory"
    if "related party" in text:
        return "related party"
    if "receivable" in text:
        return "receivables"
    return None

def display_path(path: Optional[str]) -> Optional[str]:
    """Return a submission-safe relative path for manifest metadata."""
    if not path:
        return None
    absolute = os.path.abspath(path)
    try:
        return os.path.relpath(absolute, PROJECT_ROOT)
    except ValueError:
        return os.path.basename(path)


def file_search_text(row: Dict[str, str]) -> str:
    parts = [
        row.get("file_name", ""),
        row.get("keywords", ""),
        row.get("columns", ""),
        row.get("notes", ""),
        row.get("source", ""),
        row.get("file_type", ""),
    ]
    return normalize(" ".join(parts))


def file_columns(row: Dict[str, str]) -> List[str]:
    raw = row.get("columns", "") or ""
    return [normalize(c) for c in raw.split(";") if c.strip()]


def is_placeholder(row: Dict[str, str]) -> bool:
    text = file_search_text(row)
    if "placeholder" in text:
        return True
    if normalize(row.get("file_type", "")) == "txt":
        return True
    if normalize(row.get("source", "")) == "placeholder":
        return True
    return False


def entity_matches(row: Dict[str, str], request_entity: str) -> bool:
    fe = normalize(row.get("entity", ""))
    re_ = normalize(request_entity)
    if not fe or not re_:
        return True  # cannot assess -> do not hard-fail on entity
    return fe == re_


def tokens_present(tokens: List[str], text: str) -> bool:
    return any(normalize(tok) in text for tok in tokens)


def is_subsequent_receipt(row: Dict[str, str]) -> bool:
    text = file_search_text(row)
    return "receipt" in text or "subsequent" in text


# ---------------------------------------------------------------------------
# Core evaluation
# ---------------------------------------------------------------------------

def evaluate_request(
    request: Dict[str, str],
    evidence: List[Dict[str, str]],
    tb_index: Dict[str, List[Dict[str, str]]],
) -> Dict[str, object]:
    request_id = request.get("request_id", "").strip()
    request_text = request.get("request_text", "").strip()
    period = request.get("period", "").strip()
    entity = request.get("entity", "").strip()

    request_type = classify_request_type(request_text)

    issues: List[Dict[str, str]] = []
    missing_items: List[str] = []
    next_actions: List[str] = []

    def add_issue(kind: str, detail: str) -> None:
        issues.append({"type": kind, "detail": detail})

    if request_type is None:
        # Cannot infer purpose safely.
        return {
            "request_id": request_id,
            "request_text": request_text,
            "period": period,
            "entity": entity,
            "inferred_purpose": "Unclassified request - purpose could not be inferred.",
            "request_type": "unknown",
            "required_evidence": [],
            "required_keys": [],
            "matched_files": [],
            "missing_items": ["Unable to determine required evidence"],
            "issues": [{"type": "needs_manual_judgment", "detail": "Request type could not be inferred from the text."}],
            "status": "Needs human review",
            "next_actions": ["Manually review the request wording and confirm the intended evidence."],
            "trial_balance_refs": [],
        }

    cfg = TYPE_CONFIG[request_type]
    required_keys: List[str] = list(cfg["required_keys"])  # type: ignore[arg-type]
    required_evidence_cfg: List[Dict[str, object]] = cfg["required_evidence"]  # type: ignore[assignment]
    required_evidence_labels = [ev["label"] for ev in required_evidence_cfg]

    # ----- match files by request-type tokens -----
    matched: List[Dict[str, str]] = []
    for row in evidence:
        text = file_search_text(row)
        if tokens_present(cfg["match_tokens"], text):  # type: ignore[arg-type]
            matched.append(row)

    matched_names = [r.get("file_name", "") for r in matched]

    # ----- entity / placeholder / weak-source screening -----
    meaningful: List[Dict[str, str]] = []
    for row in matched:
        name = row.get("file_name", "")
        if not entity_matches(row, entity):
            add_issue("entity_mismatch", f"{name} belongs to entity '{row.get('entity','')}', expected '{entity}'.")
            continue
        if is_placeholder(row):
            add_issue("weak_source", f"{name} is a placeholder, not real evidence.")
            add_issue("needs_manual_judgment", f"{name} cannot be relied upon; confirm with the client.")
            continue
        if normalize(row.get("source", "")) in WEAK_SOURCES:
            add_issue("weak_source", f"{name} comes from a weak source ('{row.get('source','')}').")
            add_issue("needs_manual_judgment", f"{name} source is weak; corroborate before submission.")
        meaningful.append(row)

    # ----- trial-balance context -----
    tb_refs: List[Dict[str, str]] = []
    tb_account = cfg.get("tb_account")
    if tb_account:
        for tb in tb_index.get(normalize(tb_account), []):
            if not tb.get("entity") or normalize(tb.get("entity", "")) == normalize(entity):
                tb_refs.append({
                    "account": tb.get("account", ""),
                    "period": tb.get("period", ""),
                    "amount": tb.get("amount", ""),
                })

    # ----- no meaningful evidence -> Missing -----
    if not meaningful:
        add_issue("missing_document", "No meaningful evidence matched to this request.")
        missing_items.extend(required_evidence_labels)
        next_actions.append(f"Request all evidence for {request_id}: {', '.join(required_evidence_labels)}.")
        if matched:
            next_actions.append("Confirm entity/placeholder problems with the client for the files that were provided.")
        return {
            "request_id": request_id,
            "request_text": request_text,
            "period": period,
            "entity": entity,
            "inferred_purpose": cfg["purpose"],
            "request_type": request_type,
            "required_evidence": required_evidence_labels,
            "required_keys": required_keys,
            "matched_files": matched_names,
            "missing_items": missing_items,
            "issues": issues,
            "status": "Missing",
            "next_actions": next_actions,
            "trial_balance_refs": tb_refs,
        }

    # ----- required linking keys (columns) -----
    available_columns = set()
    for row in meaningful:
        available_columns.update(file_columns(row))
    missing_keys = [k for k in required_keys if normalize(k) not in available_columns]
    if missing_keys:
        add_issue("missing_required_columns", f"Missing linking keys: {', '.join(missing_keys)}.")
        missing_items.append(f"Linking keys not evidenced: {', '.join(missing_keys)}")

    # ----- required evidence coverage -----
    combined_text = " ".join(file_search_text(r) for r in meaningful)
    for ev in required_evidence_cfg:
        if not tokens_present(ev["tokens"], combined_text):  # type: ignore[arg-type]
            add_issue("missing_document", f"No document covers: {ev['label']}.")
            missing_items.append(str(ev["label"]))

    # ----- period checks -----
    for row in meaningful:
        fp = normalize(row.get("period", ""))
        rp = normalize(period)
        if fp and rp and fp != rp and not is_subsequent_receipt(row):
            add_issue(
                "partial_period_mismatch",
                f"{row.get('file_name','')} covers period '{row.get('period','')}', expected '{period}'.",
            )

    # ----- approval checks -----
    if cfg.get("requires_approval"):
        for row in meaningful:
            status = normalize(row.get("approval_status", ""))
            if status not in APPROVED_STATUSES:
                add_issue(
                    "missing_approval",
                    f"{row.get('file_name','')} approval status is '{row.get('approval_status','')}'.",
                )

    # ----- decide status -----
    issue_types = {i["type"] for i in issues}
    if issue_types & {"missing_approval", "weak_source", "needs_manual_judgment"}:
        status = "Needs human review"
    elif issue_types & {"missing_document", "missing_required_columns", "partial_period_mismatch"} or missing_items:
        status = "Partially ready"
    else:
        status = "Ready"

    # ----- next actions -----
    if status == "Ready":
        next_actions.append("No obvious manifest-level gap found. Perform final human review before relying on the evidence.")
    else:
        if missing_keys:
            next_actions.append(f"Ask client to provide linking keys: {', '.join(missing_keys)}.")
        for ev in required_evidence_cfg:
            if ev["label"] in missing_items:
                next_actions.append(f"Request document for: {ev['label']}.")
        if "partial_period_mismatch" in issue_types:
            next_actions.append(f"Confirm the correct reporting period ({period}) for mismatched files.")
        if "missing_approval" in issue_types:
            next_actions.append("Obtain reviewer approval logs and approval dates.")
        if "weak_source" in issue_types or "needs_manual_judgment" in issue_types:
            next_actions.append("Manually assess weak/placeholder items before relying on them.")

    return {
        "request_id": request_id,
        "request_text": request_text,
        "period": period,
        "entity": entity,
        "inferred_purpose": cfg["purpose"],
        "request_type": request_type,
        "required_evidence": required_evidence_labels,
        "required_keys": required_keys,
        "matched_files": matched_names,
        "missing_items": missing_items,
        "issues": issues,
        "status": status,
        "next_actions": next_actions,
        "trial_balance_refs": tb_refs,
    }


def build_manifest(
    requests_path: str,
    evidence_path: str,
    trial_balance_path: Optional[str],
) -> Dict[str, object]:
    requests = read_csv_rows(requests_path)
    evidence = read_csv_rows(evidence_path)

    tb_index: Dict[str, List[Dict[str, str]]] = {}
    tb_rows: List[Dict[str, str]] = []
    if trial_balance_path and os.path.exists(trial_balance_path):
        tb_rows = read_csv_rows(trial_balance_path)
        for row in tb_rows:
            tb_index.setdefault(normalize(row.get("account", "")), []).append(row)

    results = [evaluate_request(req, evidence, tb_index) for req in requests]

    status_summary: Dict[str, int] = {}
    for r in results:
        status_summary[r["status"]] = status_summary.get(r["status"], 0) + 1

    return {
        "generated_by": "missing-doc-hunter/doc_matcher.py",
        "inputs": {
            "requests": display_path(requests_path),
            "evidence": display_path(evidence_path),
            "trial_balance": display_path(trial_balance_path) if trial_balance_path and os.path.exists(trial_balance_path) else None,
        },
        "trial_balance_available": bool(tb_rows),
        "status_summary": status_summary,
        "requests": results,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Match PBC requests against a local evidence manifest.")
    parser.add_argument("--requests", required=True, help="Path to pbc_requests.csv")
    parser.add_argument("--evidence", required=True, help="Path to evidence_manifest.csv")
    parser.add_argument("--trial-balance", default=None, help="Optional path to trial_balance.csv")
    parser.add_argument("--out", required=True, help="Output path for submission_package_manifest.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = build_manifest(args.requests, args.evidence, args.trial_balance)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
    print(f"Wrote {args.out}")
    print("Status summary:", json.dumps(manifest["status_summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
