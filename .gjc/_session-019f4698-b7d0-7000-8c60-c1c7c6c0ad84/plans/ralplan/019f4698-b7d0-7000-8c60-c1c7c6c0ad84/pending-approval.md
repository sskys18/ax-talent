# Final Ralplan: Submit Three Independent Codex Plugin Entries

## Status

Pending approval. This plan authorizes no product-file mutation, packaging, browser action, upload, or final external submission until the user approves execution.

## Consensus Receipts

- Planner stage 1: `.gjc/.../stage-01-planner.md`, sha `fbc9f9ffce96580e867e71bb23387174981e5f2a25748af75515543e59b9d325`
- Planner revision stage 2: `.gjc/.../stage-02-revision.md`, sha `0f611de957c8529efa3a308ee7a510e7bf5a51aa23e565da50bc2e1a87c0a6b2`
- Architect review stage 2: `CLEAR` / `APPROVE`, sha `cf29edca74a9ccbe6feebf0e52a9954da62427fc70a5c4b973c8920c5d157a0c`
- Critic review stage 2: `OKAY`, sha `f89a96477e244f8b0b540639b34863fed8d975dfced367494fa95bc1fc7da291`
- Post-interview reconciliation stage 2: sha `789d31c10ca8815304bd94c1a2bacee332eccd25a511048302d931ef27260ce0`

## Decision

Submit the three plugins as **three separate company-specific entries**, each with its own form content, zip package, source/evidence URL handling, validation gates, and receipt tracking:

1. `musinsa-smell-remover` for Musinsa / fashion platform style-diversity problem.
2. `guru-avatar` for KakaoPay Securities / beginner investor education and prohibited-phrase lint problem.
3. `missing-doc-hunter` for Samil PwC / audit-tax-advisory PBC evidence readiness screening problem.

Use the stage-02 revised Planner artifact as the detailed execution source for per-field answer copy, packaging checklists, validation checklists, browser sequence, and risk controls.

## Decision Drivers

1. **Company separation:** the hackathon requires separate submissions when multiple companies are selected.
2. **Evidence integrity:** every claim must trace to the matching plugin's `PROBLEM.md` and must not imply official company affiliation.
3. **External-submit safety:** logs, source URL semantics, local path leakage, and final submit approval are hard stop gates.

## Alternatives Considered

- **One umbrella submission:** rejected because it violates the multi-company separation requirement and weakens evidence mapping.
- **Submit only one plugin:** rejected because the user explicitly intends to submit all three, but the execution must keep each entry independent.
- **Stage all three then ask final approval:** accepted as the preferred browser flow if the site supports drafts; otherwise submit one at a time after explicit final approval.

## Intent Reconciliation

1. **AI conversation logs:** user confirmed real AI logs must be obtained and placed in each plugin's `logs/` before packaging. Placeholder-only logs are a stop condition. Fake logs are prohibited.
2. **Source URL field:** user confirmed the live site must be checked first. If `출처(URL)` means source-code/package URL rather than public problem-evidence URL, execution must stop until concrete public code/package URLs exist.
3. **missing-doc path leakage:** user confirmed `missing-doc-hunter/src/outputs/submission_package_manifest.json` must be regenerated or minimally updated so input paths are relative before packaging.

## Execution Plan After Approval

1. Verify the live form field semantics in Aside without submitting.
2. Obtain and place real AI logs into each plugin's `logs/` folder.
3. Remediate `missing-doc-hunter` output paths to relative paths and regenerate dependent reports/tests if execution approval permits.
4. Package three independent zips with one top-level folder each and no cross-plugin files.
5. Run static package validation: plugin identity, `PROBLEM.md` sources, non-affiliation text, sample-data disclaimers, no credentials/private data/local absolute paths, no heuristic overclaims.
6. Fill one form draft per plugin using the stage-02 per-field mapping.
7. Attach only the matching zip to each form draft.
8. Stop before irreversible final submit unless explicit final submit approval has already been granted.
9. After approved submit, capture separate confirmation details per plugin.

## Acceptance Criteria

- Three validated zips exist, one per plugin.
- Each zip includes real approved AI logs and no fake logs.
- `missing-doc-hunter` manifest no longer exposes `/Users/...` paths.
- Source URL field meaning is resolved, and entries use the correct URL type.
- Three separate form drafts are filled with plugin-specific copy and attachments.
- Final approval is obtained before submission, or the workflow stops at staged drafts.

## Follow-ups / Risk Gates

- Stop if real AI logs cannot be obtained.
- Stop if the site requires a source-code URL and no public code/package URL exists.
- Stop if any package contains local absolute paths, credentials, private data, or another plugin's files.
- Stop if any submission copy implies official affiliation, investment advice, audit conclusion, or validated model accuracy.
