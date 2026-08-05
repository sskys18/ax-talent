Approved ralplan execution for three separate AX hackathon plugin submissions. Constraints: use real logs only; no fake logs; sanitize missing-doc local paths; create three independent zips; verify live Source URL semantics in Aside before staging; if Source URL means code/package URL and no public URL exists, stop; stage each submission separately; stop before irreversible final submit unless explicit final submit approval is obtained.

@goal: Prepare logs and sanitize submission artifacts
Privacy-review the supplied real log sources, place approved real logs into each plugin's logs/ folder, and remediate missing-doc-hunter output JSON so input paths are relative. Verify no local /Users paths remain in packaged outputs.

@goal: Build and validate three independent plugin packages
Create separate zip packages for musinsa-smell-remover, guru-avatar, and missing-doc-hunter. Each zip must have one matching top-level folder, include required docs/source/examples/outputs/tests/logs, exclude caches/private files, and pass static validation for non-affiliation, sample data, and overclaim boundaries.

@goal: Verify live form semantics and stage three submissions in Aside
Use the already-open Aside browser session or Aside CLI to inspect https://hack.primer.kr/rounds/10?mode=, verify whether 출처(URL) expects problem evidence or code/package URL, then fill/stage one draft per plugin with matching form copy and matching zip. If code/package URL is required and unavailable, record a human-blocked blocker instead of guessing.

@goal: Final submit gate and receipt capture
Before any irreversible submit, verify explicit final submit approval exists. If not, stop with a durable human-blocked checkpoint describing the staged drafts and approval needed. If approval exists, submit each plugin separately and capture confirmation details.
