#!/usr/bin/env python3
"""Render human-readable reports from submission_package_manifest.json.

Standard library only. Produces:
- missing_doc_hunter_report.md
- missing_items.md
- followup_email_draft.md
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Dict, List


def load_manifest(path: str) -> Dict[str, object]:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _bullets(items: List[str]) -> str:
    if not items:
        return "- (none)\n"
    return "".join(f"- {item}\n" for item in items)


def _issue_lines(issues: List[Dict[str, str]]) -> str:
    if not issues:
        return "- (none)\n"
    return "".join(f"- `{i.get('type','')}`: {i.get('detail','')}\n" for i in issues)


def render_report(manifest: Dict[str, object]) -> str:
    requests: List[Dict[str, object]] = manifest.get("requests", [])  # type: ignore[assignment]
    status_summary: Dict[str, int] = manifest.get("status_summary", {})  # type: ignore[assignment]

    out: List[str] = []
    out.append("# Missing Doc Hunter Report\n")

    out.append("## Summary\n")
    out.append(f"Total requests evaluated: **{len(requests)}**\n\n")
    for status in ("Ready", "Partially ready", "Missing", "Needs human review"):
        out.append(f"- {status}: {status_summary.get(status, 0)}\n")
    out.append(f"\nTrial balance available: {'yes' if manifest.get('trial_balance_available') else 'no'}\n")

    out.append("\n## Request-by-Request Review\n")
    for r in requests:
        out.append(f"### {r.get('request_id','')} - {r.get('status','')}\n")
        out.append(f"- **Request text**: {r.get('request_text','')}\n")
        out.append(f"- **Inferred purpose**: {r.get('inferred_purpose','')}\n")
        out.append(f"- **Request type**: {r.get('request_type','')}\n")
        out.append(f"- **Period / Entity**: {r.get('period','')} / {r.get('entity','')}\n")
        out.append("- **Required evidence**:\n")
        for ev in r.get("required_evidence", []):  # type: ignore[union-attr]
            out.append(f"  - {ev}\n")
        out.append(f"- **Required keys**: {', '.join(r.get('required_keys', []))}\n")  # type: ignore[arg-type]
        out.append(f"- **Matched files**: {', '.join(r.get('matched_files', [])) or '(none)'}\n")  # type: ignore[arg-type]
        tb_refs = r.get("trial_balance_refs", [])
        if tb_refs:
            refs = "; ".join(f"{t.get('account','')}={t.get('amount','')}" for t in tb_refs)  # type: ignore[union-attr]
            out.append(f"- **Trial balance reference**: {refs}\n")
        out.append("- **Issues**:\n")
        out.append("".join("  " + line for line in _issue_lines(r.get("issues", [])).splitlines(keepends=True)))  # type: ignore[arg-type]
        out.append("- **Missing items**:\n")
        for mi in r.get("missing_items", []):  # type: ignore[union-attr]
            out.append(f"  - {mi}\n")
        if not r.get("missing_items"):
            out.append("  - (none)\n")
        out.append("- **Next actions**:\n")
        for na in r.get("next_actions", []):  # type: ignore[union-attr]
            out.append(f"  - {na}\n")
        out.append("\n")

    out.append("## Missing or Insufficient Documents\n")
    any_missing = False
    for r in requests:
        if r.get("status") in ("Missing", "Partially ready") and r.get("missing_items"):
            any_missing = True
            out.append(f"- **{r.get('request_id','')}** ({r.get('status','')}): {', '.join(r.get('missing_items', []))}\n")  # type: ignore[arg-type]
    if not any_missing:
        out.append("- (none)\n")

    out.append("\n## Human Review Notes\n")
    any_review = False
    for r in requests:
        review_issues = [i for i in r.get("issues", []) if i.get("type") in ("needs_manual_judgment", "weak_source", "entity_mismatch")]  # type: ignore[union-attr]
        if r.get("status") == "Needs human review" or review_issues:
            any_review = True
            details = "; ".join(i.get("detail", "") for i in review_issues) or "Requires manual assessment."
            out.append(f"- **{r.get('request_id','')}**: {details}\n")
    if not any_review:
        out.append("- (none)\n")
    out.append("\nThis tool uses heuristic metadata matching only. It does not open or verify the")
    out.append(" contents of source documents. Do not treat these results as an assurance conclusion.\n")

    out.append("\n## Submission Readiness\n")
    ready = [r.get("request_id", "") for r in requests if r.get("status") == "Ready"]
    not_ready = [r.get("request_id", "") for r in requests if r.get("status") != "Ready"]
    out.append(f"- Screened as ready for human review: {', '.join(ready) or '(none)'}\n")
    out.append(f"- Needs follow-up before human review: {', '.join(not_ready) or '(none)'}\n")
    pct = round(100 * len(ready) / len(requests)) if requests else 0
    out.append(f"- Manifest screening readiness: {len(ready)}/{len(requests)} ({pct}%)\n")

    return "".join(out)


def render_missing_items(manifest: Dict[str, object]) -> str:
    requests: List[Dict[str, object]] = manifest.get("requests", [])  # type: ignore[assignment]

    missing_docs: List[str] = []
    weak_docs: List[str] = []
    ambiguous_docs: List[str] = []
    review_docs: List[str] = []

    for r in requests:
        rid = r.get("request_id", "")
        for i in r.get("issues", []):  # type: ignore[union-attr]
            t = i.get("type", "")
            detail = i.get("detail", "")
            line = f"{rid}: {detail}"
            if t == "missing_document":
                missing_docs.append(line)
            elif t == "weak_source":
                weak_docs.append(line)
            elif t in ("entity_mismatch", "partial_period_mismatch", "missing_required_columns", "missing_approval"):
                ambiguous_docs.append(f"{rid} ({t}): {detail}")
            elif t == "needs_manual_judgment":
                review_docs.append(line)
        if r.get("status") == "Needs human review" and rid not in " ".join(review_docs):
            review_docs.append(f"{rid}: status is Needs human review.")

    out: List[str] = []
    out.append("# Missing and Insufficient Items\n\n")
    out.append("## Missing documents\n")
    out.append(_bullets(missing_docs))
    out.append("\n## Weak documents\n")
    out.append(_bullets(weak_docs))
    out.append("\n## Ambiguous / incomplete documents\n")
    out.append(_bullets(ambiguous_docs))
    out.append("\n## Documents requiring human review\n")
    out.append(_bullets(review_docs))
    return "".join(out)


def render_followup_email(manifest: Dict[str, object]) -> str:
    requests: List[Dict[str, object]] = manifest.get("requests", [])  # type: ignore[assignment]
    outstanding = [r for r in requests if r.get("status") != "Ready"]

    out: List[str] = []
    out.append("Subject: PBC follow-up - outstanding / insufficient evidence\n\n")
    out.append("Hi team,\n\n")
    out.append("Thanks for the documents provided so far. After screening the submission ")
    out.append("against our PBC request list, the following items still need attention ")
    out.append("before human review can proceed efficiently. Please help close these gaps.\n\n")

    if not outstanding:
        out.append("All requests currently have no obvious manifest-level gaps. Final human review is still required.\n\n")
    else:
        for r in outstanding:
            out.append(f"{r.get('request_id','')} - {r.get('status','')}\n")
            out.append(f"  Request: {r.get('request_text','')}\n")
            missing = r.get("missing_items", [])
            if missing:
                out.append("  Still needed:\n")
                for mi in missing:  # type: ignore[union-attr]
                    out.append(f"    - {mi}\n")
            actions = r.get("next_actions", [])
            if actions:
                out.append("  Requested actions:\n")
                for na in actions:  # type: ignore[union-attr]
                    out.append(f"    - {na}\n")
            out.append("\n")

    out.append("Where a document was provided but could not be relied upon (wrong entity, ")
    out.append("wrong period, placeholder, missing approval, or missing key columns), please ")
    out.append("resend the correct version rather than confirming verbally.\n\n")
    out.append("Please send the above at your earliest convenience so we can finalize the ")
    out.append("submission package. Let me know if any item needs a call to clarify scope.\n\n")
    out.append("Best regards,\n")
    out.append("Engagement Team\n")
    return "".join(out)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render reports from submission_package_manifest.json.")
    parser.add_argument("--manifest", required=True, help="Path to submission_package_manifest.json")
    parser.add_argument("--out-dir", required=True, help="Output directory for markdown files")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = load_manifest(args.manifest)
    os.makedirs(args.out_dir, exist_ok=True)

    report_path = os.path.join(args.out_dir, "missing_doc_hunter_report.md")
    missing_path = os.path.join(args.out_dir, "missing_items.md")
    email_path = os.path.join(args.out_dir, "followup_email_draft.md")

    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write(render_report(manifest))
    with open(missing_path, "w", encoding="utf-8") as handle:
        handle.write(render_missing_items(manifest))
    with open(email_path, "w", encoding="utf-8") as handle:
        handle.write(render_followup_email(manifest))

    print(f"Wrote {report_path}")
    print(f"Wrote {missing_path}")
    print(f"Wrote {email_path}")


if __name__ == "__main__":
    main()
