# Missing Doc Hunter Report
## Summary
Total requests evaluated: **5**

- Ready: 1
- Partially ready: 2
- Missing: 1
- Needs human review: 1

Trial balance available: yes

## Request-by-Request Review
### AR-03 - Ready
- **Request text**: 2026-03-31 receivables aging report, 90+ day receivables collectability assessment, customer contract terms, and subsequent cash receipts.
- **Inferred purpose**: Support existence, valuation, and collectability of accounts receivable at period end.
- **Request type**: receivables
- **Period / Entity**: 2026-03-31 / ACME Korea Co.
- **Required evidence**:
  - Receivables aging report
  - 90+ day collectability assessment
  - Customer contract terms
  - Subsequent cash receipts
- **Required keys**: customer_id, invoice_id, due_date, amount, receipt_date
- **Matched files**: AR_Aging_20260331.xlsx, Bank_Receipts_April.csv, Customer_Terms_Top10.pdf
- **Trial balance reference**: Accounts receivable=1250000000
- **Issues**:
  - (none)
- **Missing items**:
  - (none)
- **Next actions**:
  - No obvious manifest-level gap found. Perform final human review before relying on the evidence.

### CUT-01 - Partially ready
- **Request text**: Contracts, tax invoices, and delivery evidence for selected revenue cutoff test transactions.
- **Inferred purpose**: Test that revenue is recognized in the correct period (cutoff).
- **Request type**: cutoff
- **Period / Entity**: 2026-03-31 / ACME Korea Co.
- **Required evidence**:
  - Signed contracts for sampled transactions
  - Tax invoices
  - Delivery / shipment evidence
- **Required keys**: invoice_id, contract_id, shipment_date, revenue_recognition_date
- **Matched files**: Sales_Invoices_March.zip, Delivery_Notes_March.pdf, Contract_Terms_Partial.pdf
- **Trial balance reference**: Revenue=8400000000
- **Issues**:
  - `missing_required_columns`: Missing linking keys: contract_id.
  - `partial_period_mismatch`: Contract_Terms_Partial.pdf covers period '2026-02-28', expected '2026-03-31'.
- **Missing items**:
  - Linking keys not evidenced: contract_id
- **Next actions**:
  - Ask client to provide linking keys: contract_id.
  - Confirm the correct reporting period (2026-03-31) for mismatched files.

### JE-02 - Needs human review
- **Request text**: Manual journal entry list, preparer information, reviewer approval logs, and approval dates.
- **Inferred purpose**: Test manual journal entries for appropriate preparation, review, and approval.
- **Request type**: journal entry
- **Period / Entity**: 2026-03-31 / ACME Korea Co.
- **Required evidence**:
  - Manual journal entry list
  - Preparer information
  - Reviewer approval logs and approval dates
- **Required keys**: journal_id, preparer, reviewer, approval_date
- **Matched files**: Manual_JE_List.xlsx, Missing_Approval_Log_Placeholder.txt
- **Trial balance reference**: Manual journal entries=45000000
- **Issues**:
  - `weak_source`: Missing_Approval_Log_Placeholder.txt is a placeholder, not real evidence.
  - `needs_manual_judgment`: Missing_Approval_Log_Placeholder.txt cannot be relied upon; confirm with the client.
  - `missing_required_columns`: Missing linking keys: reviewer, approval_date.
  - `missing_approval`: Manual_JE_List.xlsx approval status is 'pending'.
- **Missing items**:
  - Linking keys not evidenced: reviewer, approval_date
- **Next actions**:
  - Ask client to provide linking keys: reviewer, approval_date.
  - Obtain reviewer approval logs and approval dates.
  - Manually assess weak/placeholder items before relying on them.

### INV-04 - Partially ready
- **Request text**: Inventory valuation allowance calculation support and slow-moving inventory list.
- **Inferred purpose**: Support inventory valuation and the slow-moving/obsolescence allowance.
- **Request type**: inventory
- **Period / Entity**: 2026-03-31 / ACME Korea Co.
- **Required evidence**:
  - Valuation allowance calculation support
  - Slow-moving inventory list
- **Required keys**: item_id, aging_days, nrv, allowance_amount
- **Matched files**: Inventory_Aging_Q1.xlsx
- **Trial balance reference**: Inventory=640000000
- **Issues**:
  - `missing_required_columns`: Missing linking keys: nrv, allowance_amount.
  - `missing_document`: No document covers: Valuation allowance calculation support.
- **Missing items**:
  - Linking keys not evidenced: nrv, allowance_amount
  - Valuation allowance calculation support
- **Next actions**:
  - Ask client to provide linking keys: nrv, allowance_amount.
  - Request document for: Valuation allowance calculation support.

### RP-05 - Missing
- **Request text**: Related-party transaction listing, contract terms, and settlement evidence.
- **Inferred purpose**: Support completeness and terms of related-party transactions and settlements.
- **Request type**: related party
- **Period / Entity**: 2026-03-31 / ACME Korea Co.
- **Required evidence**:
  - Related-party transaction listing
  - Contract terms
  - Settlement evidence
- **Required keys**: counterparty, contract_id, transaction_amount, terms
- **Matched files**: Related_Party_Transactions.xlsx
- **Trial balance reference**: Related-party receivables=320000000
- **Issues**:
  - `entity_mismatch`: Related_Party_Transactions.xlsx belongs to entity 'ACME US Inc.', expected 'ACME Korea Co.'.
  - `missing_document`: No meaningful evidence matched to this request.
- **Missing items**:
  - Related-party transaction listing
  - Contract terms
  - Settlement evidence
- **Next actions**:
  - Request all evidence for RP-05: Related-party transaction listing, Contract terms, Settlement evidence.
  - Confirm entity/placeholder problems with the client for the files that were provided.

## Missing or Insufficient Documents
- **CUT-01** (Partially ready): Linking keys not evidenced: contract_id
- **INV-04** (Partially ready): Linking keys not evidenced: nrv, allowance_amount, Valuation allowance calculation support
- **RP-05** (Missing): Related-party transaction listing, Contract terms, Settlement evidence

## Human Review Notes
- **JE-02**: Missing_Approval_Log_Placeholder.txt is a placeholder, not real evidence.; Missing_Approval_Log_Placeholder.txt cannot be relied upon; confirm with the client.
- **RP-05**: Related_Party_Transactions.xlsx belongs to entity 'ACME US Inc.', expected 'ACME Korea Co.'.

This tool uses heuristic metadata matching only. It does not open or verify the contents of source documents. Do not treat these results as an assurance conclusion.

## Submission Readiness
- Screened as ready for human review: AR-03
- Needs follow-up before human review: CUT-01, JE-02, INV-04, RP-05
- Manifest screening readiness: 1/5 (20%)
