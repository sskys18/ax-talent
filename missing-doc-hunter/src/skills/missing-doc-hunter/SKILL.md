# missing-doc-hunter

Use this skill when a professional services team such as Samil PwC audit, tax, or advisory needs to check a PBC request list against a local evidence manifest, find missing or insufficient documents, and produce a human-review submission readiness report plus follow-up request drafts.

PBC means **Prepared By Client**. A PBC request list is what the engagement team
asks the client to provide.

## What this is and is not

- This **is** an audit, tax, and advisory evidence-readiness workflow.
- This is **not** a generic finance dashboard.
- This is **not** a generic accounting Q&A tool.
- This is **not** just a file-name search tool.

The plugin interprets PBC request text, infers what each request is really for,
and screens whether the available evidence has obvious readiness gaps before human review. It
hunts for missing, weak, mismatched, or incomplete documents.

## Conservatism rules (hard constraints)

- Be conservative. Do not overstate readiness.
- If sufficiency is unclear, mark the item **Needs human review**.
- **Never fabricate evidence.**
- **Never assume a missing document exists.**
- A placeholder, an empty file, or a weak source is not evidence.

## Required inputs

Read these files before evaluating anything:

- `examples/pbc_requests.csv`
- `examples/evidence_manifest.csv`
- `examples/trial_balance.csv` (if available)

The evidence manifest describes files the client provided. It is metadata only.
Do not treat a manifest row as proof that a valid source document exists; evaluate
its fields (period, entity, columns, source, approval_status, notes).

## Required outputs

Write all of these files:

- `outputs/submission_package_manifest.json`
- `outputs/missing_doc_hunter_report.md`
- `outputs/missing_items.md`
- `outputs/followup_email_draft.md`

## Workflow

1. Read the PBC request list.
2. Infer each request's purpose.
3. Decompose each request into the required evidence.
4. Identify the required linking keys (the columns needed to tie evidence together).
5. Match available files from the evidence manifest.
6. Detect missing, weak, mismatched, or incomplete documents.
7. Classify each request as one of:
   - **Ready** (no obvious readiness gap in the sample manifest; not an audit conclusion)
   - **Partially ready**
   - **Missing**
   - **Needs human review**
8. Explain the issues and the next actions.
9. Generate follow-up request drafts for missing or insufficient evidence.

## Request types

The matcher classifies each request into one of these types and derives the
required evidence and linking keys from it:

- **receivables** - keys: `customer_id`, `invoice_id`, `due_date`, `amount`, `receipt_date`
- **cutoff** - keys: `invoice_id`, `contract_id`, `shipment_date`, `revenue_recognition_date`
- **journal entry** - keys: `journal_id`, `preparer`, `reviewer`, `approval_date`
- **inventory** - keys: `item_id`, `aging_days`, `nrv`, `allowance_amount`
- **related party** - keys: `counterparty`, `contract_id`, `transaction_amount`, `terms`

## Issue types

The matcher reports these issue types:

- `missing_document`
- `partial_period_mismatch`
- `entity_mismatch`
- `missing_required_columns`
- `missing_approval`
- `weak_source`
- `needs_manual_judgment`

## Classification guidance

- **Ready**: required evidence appears present in the sample manifest, period and entity match, key
  columns exist, and approval/source metadata appears acceptable. This is not an audit conclusion.
- **Partially ready**: some evidence exists but required keys, period, entity, or
  supporting documents are incomplete.
- **Missing**: no meaningful evidence is matched to a required request.
- **Needs human review**: the match is ambiguous, the source is weak, or
  sufficiency cannot be determined safely.

## Tools

Run the matcher, then the report writer:

```
python src/tools/doc_matcher.py \
  --requests src/examples/pbc_requests.csv \
  --evidence src/examples/evidence_manifest.csv \
  --trial-balance src/examples/trial_balance.csv \
  --out src/outputs/submission_package_manifest.json

python src/tools/report_writer.py \
  --manifest src/outputs/submission_package_manifest.json \
  --out-dir src/outputs
```

The scoring is heuristic and based only on local manifest metadata. Always
include human review notes and never present a heuristic match as an assurance
conclusion.
