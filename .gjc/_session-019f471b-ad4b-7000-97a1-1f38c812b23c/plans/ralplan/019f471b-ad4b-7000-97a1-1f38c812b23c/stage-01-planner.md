# Submission Execution Plan for Three Independent Codex Workflow Plugin Submissions

## Summary

Create three separate AX hackathon submissions for `musinsa-smell-remover`, `guru-avatar`, and `missing-doc-hunter`. This assignment is planning only: no product file edits, no zip creation, no test/build/formatter runs, no Aside usage, and no external submission. Execution after approval should package and submit each company-specific plugin independently, with a hard stop before the final irreversible submit unless explicit final approval has already been given.

Evidence inspected: each plugin's `README.md`, `PROBLEM.md`, `src/.codex-plugin/plugin.json`, `src/skills/*/SKILL.md`, selected `src/outputs/*`, and `logs/README.md`. [High]

## Intent Diff

- Requested outcome: a submission execution plan, not implementation or upload. [High]
- Required separation: three independent plugin folders and three independent company submissions. [High]
- Required caution: use the recent fixes already present in the files, including problem evidence, non-affiliation disclaimers, and reduced overclaims. [High]
- Not requested: improving plugin code, changing copy in product files, creating zips, running tests/builds/formatters, operating Aside, or submitting to the hackathon site.

## Principles

1. **Separate every company and plugin**: one form draft, one zip, one positioning angle, and one evidence set per plugin.
2. **Evidence-grounded copy only**: every problem claim must trace to that plugin's `PROBLEM.md`; do not add unsupported market, legal, financial, or audit claims.
3. **Human-review framing**: present each plugin as a Codex workflow that prepares or screens outputs for human review, not as an automatic decision-maker.
4. **No fake artifacts**: do not invent AI logs, source URLs, test results, sample data, business affiliations, or submission receipts.
5. **Stop before irreversible action**: browser execution may stage drafts after approval, but final submit requires explicit final approval unless already granted.

## Decision Drivers

1. **Company separation and form integrity**: Musinsa, KakaoPay Securities, and Samil PwC/PwC are different targets, so combined packaging or shared form answers would weaken the submission and increase non-affiliation risk. [High]
2. **Public problem proof plus controlled claims**: each plugin has a `PROBLEM.md` with public evidence and a non-affiliation disclaimer; submission copy should preserve that evidence chain and avoid stronger claims than the files support. [High]
3. **Upload safety**: generated outputs and logs need a privacy/overclaim scan before upload. Known gate: `missing-doc-hunter/src/outputs/submission_package_manifest.json` contains local absolute input paths under `/Users/...`, so packaging must stop for sanitization or omission if public upload would expose local path metadata. [High]

## Options

| Option | Description | Pros | Cons | Decision |
|---|---|---|---|---|
| A | Three separate submissions, each with its own zip, problem evidence URLs, and form copy | Matches the stated multi-company constraint; isolates risks; lets each plugin use its strongest niche | More browser work; repeated validation | **Chosen** |
| B | One umbrella submission covering all three plugins | Fastest single form flow | Violates the separate-company constraint; dilutes problem evidence; risks confusing judges | Rejected |
| C | Stage all three browser drafts first, then request a single final approval before submitting all | Efficient final review; supports batch approval | Requires careful tab/form tracking to prevent cross-plugin upload mistakes | Use as execution pattern inside Option A |
| D | Submit one plugin first, wait for confirmation, then repeat | Lowest risk per form | Slowest; may create inconsistent copy if changes are made between submissions | Fallback if the site has unstable drafts |

Chosen plan: Option A with Option C staging. If the site cannot save separate drafts safely, fall back to Option D.

## In Scope / Out of Scope

### In scope

- Submission positioning for all three plugins.
- Per-plugin form-answer mapping for: what/who/situation, why, source URL, how it works, AI usage, and verification.
- Packaging checklist for each independent zip.
- Pre-upload validation checklist.
- Aside/browser execution sequence with final-submit stop gate.
- Risk controls for non-affiliation, sample data, logs, heuristic overclaims, and company separation.
- Acceptance criteria for the eventual execution.

### Out of scope for this assignment

- Editing product files.
- Creating zip files.
- Running tests, builds, formatters, or plugin commands.
- Using Aside or another browser.
- Uploading files or submitting the hackathon form.
- Fabricating missing source URLs, logs, or verification evidence.

## File-Level Changes

No product file changes are planned or allowed for this assignment.

Future execution, only after approval, may create transient zip artifacts outside the product source or through the submission workflow. If validation reveals unsafe packaged content, stop and request explicit approval for the minimum corrective action rather than silently editing source files.

## Per-Plugin Submission Positioning

### 1. `musinsa-smell-remover`

- Target company: Musinsa. [High]
- Positioning: a Codex workflow for fashion platform MD/style/recommendation teams to quantify clone-look risk from local product, ranking, review, and request data, then propose less-common but wearable outfit candidates for human review. [High]
- Core proof: Musinsa platform influence is supported by recent performance sources, while clone-look/style homogenization is defined through public discussion in `PROBLEM.md`. [High]
- Claim boundary: not a brand critique, official Musinsa product, live shopping recommender, or taste-only chatbot. [High]
- Demo proof from outputs: 22 products scored, local average clone risk 40.6/100, recommended outfit average risk 16.0/100, total 199,000 KRW within a 200,000 KRW budget, with direct avoid conflicts excluded. [High]

### 2. `guru-avatar`

- Target company: KakaoPay Securities. [High]
- Positioning: a Codex workflow for beginner investor education content teams and compliance-adjacent reviewers to generate neutral decision-support drafts and phrase-lint prohibited investment recommendation language before human review. [High]
- Core proof: `PROBLEM.md` ties beginner investor growth, risky product exposure, and investment advertising/compliance needs to recent public sources. [High]
- Claim boundary: not financial advice, not a buy/sell/hold signal, not a future-return predictor, and not a complete legal review. [High]
- Demo proof from outputs: NVDA educational report includes lens-by-lens support/caution/questions, beginner safety checks, safe non-directive next actions, and a `PASS` compliance check with 16 prohibited phrases scanned and none detected. [High]

### 3. `missing-doc-hunter`

- Target company: Samil PwC / PwC-style professional services teams. [High]
- Positioning: a Codex workflow for audit, tax, and advisory teams to compare PBC request lists against local evidence manifests, identify missing or insufficient evidence, and draft follow-up requests before expert review. [High]
- Core proof: `PROBLEM.md` cites audit evidence standards, PBC workflow tooling, regulatory findings, and accounting-firm AI adoption to justify the evidence-readiness gap. [High]
- Claim boundary: not an audit opinion, not document-content verification, not a generic accounting chatbot, and not a PwC official product. [High]
- Demo proof from outputs: five requests screened with status summary Ready 1, Partially ready 2, Needs human review 1, Missing 1; issues include missing columns, period mismatch, weak placeholder source, missing approval, entity mismatch, and missing documents. [High]

## Per-Plugin Form-Answer Mapping

Use Korean field copy unless the live form requires English. Keep each answer independent. Do not paste another company's source URLs or examples into a different plugin submission.

### `musinsa-smell-remover`

| Field | Submission mapping |
|---|---|
| What / who / situation | `무신사처럼 랭킹 영향력이 큰 패션 플랫폼의 MD, 스타일 에디터, 추천 실험 담당자가 상위 랭킹 중심 콘텐츠로 인해 안전하지만 비슷한 착장이 반복되는 상황에서 쓰는 Codex 워크플로우입니다. 로컬 상품, 랭킹, 리뷰, 사용자 요청 파일을 읽고 "무신사 냄새"를 취향 비난이 아니라 클론룩 위험과 추천 다양성 저하 문제로 재정의해 점검합니다.` |
| Why | `무신사는 최근 실적과 성장세로 패션 플랫폼 영향력이 크고, 인기 품목 중심 소비는 착장 획일화와 클론룩 논의를 낳습니다. 이 플러그인은 브랜드를 비판하지 않고, 랭킹과 리뷰 흔함 신호, 색상, 소재, 실루엣, 회피 키워드를 함께 보아 "덜 흔하지만 여전히 입기 쉬운" 후보를 사람 검토 전에 정리합니다.` |
| Source URL | `https://biz.newdaily.co.kr/site/data/html/2026/04/08/2026040800264.html` plus `https://www.news1.kr/industry/distribution/6130067` and `https://www.hanbat.ac.kr/prog/bbsArticle/BBSMSTR_000000000077/view.do?nttId=B000000105566Mn0bG3r&mno=sub01_07`. If the form accepts only one URL, use the NewDaily URL in the field and put the other two in the why/evidence text. |
| How it works | `Codex가 스킬 정의를 따라 로컬 CSV/JSON 입력(products, rankings, reviews, user_request)을 읽고, Python 표준 라이브러리 도구가 상품별 Clone Risk Score(0-100)를 계산합니다. 회피 키워드와 직접 충돌하는 상품을 제외한 뒤 예산 안에서 3-5개 코디 후보를 고르고, clone_risk_scores.csv, recommendation.json, musinsa_smell_removal_report.md를 생성합니다.` |
| AI usage | `AI는 문제 프레이밍과 사람 검토용 리포트 구성을 돕고, Codex 워크플로우는 로컬 데이터와 명시된 휴리스틱만 사용합니다. 외부 쇼핑 API나 실시간 크롤링을 하지 않으며, 결과는 최종 스타일 판단이 아니라 MD/에디터의 검토 초안입니다.` |
| Verification | `샘플 출력 기준 22개 상품이 0-100 점수로 평가되었고, 추천 코디 평균 위험도는 16.0/100으로 로컬 평균 40.6/100보다 낮으며, 총액 199,000원은 200,000원 예산 안입니다. 직접 회피 항목(black wide pants, oversized graphic t-shirt, german army sneakers)은 추천에서 제외됩니다. README의 테스트 범위는 점수 범위, 회피 충돌 가중, CSV/JSON 생성, 추천 충돌 부재를 확인하도록 되어 있습니다. 이번 계획 단계에서는 테스트를 실행하지 않았다고 명시합니다.` |

### `guru-avatar`

| Field | Submission mapping |
|---|---|
| What / who / situation | `카카오페이증권 같은 초보 투자자 기반 금융 플랫폼의 투자자교육 콘텐츠팀, 서비스기획, 준법 검토 보조 담당자가 종목별 교육 콘텐츠를 빠르게 초안화하고 명백한 금지 표현을 사람 검토 전에 걸러내는 Codex 워크플로우입니다.` |
| Why | `카카오페이증권은 초보/MZ 투자자 기반과 AI 기반 투자정보 서비스 확대 맥락이 있고, 개인투자자의 고위험 상품 노출과 투자광고/투자권유 표현 리스크가 함께 존재합니다. 콘텐츠팀은 초보자에게 도움이 되는 설명을 만들되 매수/매도/보유 권유나 수익 보장처럼 오해될 표현을 피해야 하므로 반복 가능한 초안 생성과 phrase lint가 필요합니다.` |
| Source URL | `https://www.news2day.co.kr/article/20260609500200` plus `https://v.daum.net/v/20260623230143657`, `https://www.edaily.co.kr/News/Read?newsId=04178726645451544`, and `https://www.fsc.go.kr/no010101/76045`. If only one URL is allowed, use the News2day URL and include the compliance URLs in the why text. |
| How it works | `Codex가 user_profile.json의 대상 티커와 로컬 stock_metrics.csv, public_holdings.csv, guru_lenses.json을 읽습니다. 도구가 Buffett, Peter Lynch, Dalio, Momentum, Dividend 렌즈별로 확인 기준, 지지 신호, 주의 신호, 투자자 질문을 생성하고 Beginner Safety Check와 안전한 다음 행동만 포함합니다. 이후 compliance_check.py가 buy/sell/hold, 수익 보장 등 금지 표현을 스캔해 compliance_check.md를 생성합니다.` |
| AI usage | `AI는 투자 철학 템플릿을 초보자용 판단 질문과 교육 초안으로 바꾸는 데 사용됩니다. 투자 조언, 매수/매도/보유 신호, 수익 예측을 생성하지 않으며 모든 출력은 decision support와 human review draft로 제한됩니다. 모든 수치는 로컬 샘플 데이터이므로 1차 출처 재확인이 필요합니다.` |
| Verification | `샘플 출력은 NVDA 교육 리포트, JSON 구조화 결과, 투자자 질문, compliance_check.md를 생성합니다. compliance_check.md는 16개 금지 표현을 스캔했고 Status: PASS, detected risky phrases none으로 기록되어 있습니다. README의 테스트 범위는 네 개 결과물 생성, 금지 추천 표현 부재, 모든 렌즈의 질문 포함, Beginner Safety Check 포함, compliance check PASS를 확인하도록 되어 있습니다. 이번 계획 단계에서는 테스트를 실행하지 않았다고 명시합니다.` |

### `missing-doc-hunter`

| Field | Submission mapping |
|---|---|
| What / who / situation | `삼일PwC 같은 회계감사, 세무, 자문 조직의 실무팀이 고객 PBC 요청 목록과 로컬 evidence manifest를 대조해 누락, 불충분, 기간/법인/승인/연결 키 문제를 사람 검토 전에 찾는 Codex 워크플로우입니다.` |
| Why | `PBC 포털은 자료 요청과 수령 상태를 관리할 수 있지만, 받은 자료가 충분하고 적합한지, 기간과 법인이 맞는지, 필수 연결 키와 승인 로그가 있는지는 여전히 사람이 확인해야 합니다. 이 왕복이 늦어지면 제출 패키지 준비와 고객 커뮤니케이션이 지연됩니다. 이 플러그인은 명백한 누락과 약한 증빙을 보수적으로 표시해 전문가가 원문 검토에 들어가기 전 후속 요청을 정리합니다.` |
| Source URL | `https://m.ddaily.co.kr/page/view/2026051115581496536` plus `https://www.frc.org.uk/library/standards-codes-policy/audit-assurance-and-ethics/auditing-standards/isa-uk-500/`, `https://fss.or.kr/fss/bbs/B0000129/list.do?menuNo=200437`, `https://fss.or.kr/fss/bbs/B0000135/list.do?menuNo=200448`, `https://connect.pwc.com/`, `https://www.auditdashboard.com/`, and `https://www.edaily.co.kr/News/Read?newsId=01587526645486312`. If only one URL is allowed, use the DigitalDaily URL and summarize the standards/PBC-tool URLs in the why text. |
| How it works | `Codex가 PBC request list, evidence manifest, optional trial balance를 읽도록 스킬을 적용합니다. Python 표준 라이브러리 도구가 요청 목적과 유형을 추론하고 required evidence와 linking keys를 분해한 뒤 manifest의 파일 메타데이터와 매칭합니다. missing_document, partial_period_mismatch, entity_mismatch, missing_required_columns, missing_approval, weak_source, needs_manual_judgment를 탐지하고 각 요청을 Ready, Partially ready, Missing, Needs human review로 분류합니다. 결과로 submission_package_manifest.json, missing_doc_hunter_report.md, missing_items.md, followup_email_draft.md를 생성합니다.` |
| AI usage | `AI는 PBC 요청의 목적을 해석하고 사람 검토용 리포트와 후속 요청 초안을 구성하는 데 사용됩니다. 증빙을 만들거나 있다고 가정하지 않으며, Ready도 감사 결론이 아니라 샘플 manifest 기준의 사전 스크리닝 상태로만 표시합니다. 애매하면 Needs human review로 보수적으로 남깁니다.` |
| Verification | `샘플 출력은 5개 요청을 평가해 Ready 1, Partially ready 2, Needs human review 1, Missing 1로 요약합니다. 리포트는 CUT-01의 contract_id 누락과 기간 불일치, JE-02의 placeholder/approval 문제, INV-04의 nrv/allowance_amount 및 valuation support 누락, RP-05의 entity mismatch와 missing evidence를 표시합니다. README의 테스트 범위는 manifest 생성, 5개 요청 포함, 상태 분포, AR 필수 키 포함, Markdown 3종 생성, issue type 포함을 확인하도록 되어 있습니다. 이번 계획 단계에서는 테스트를 실행하지 않았다고 명시합니다.` |

## Packaging Checklist for Each Zip

General rule for all three zips: one top-level folder per archive, no combined submission, no `.git`, `__pycache__`, local virtual environments, OS metadata, hidden editor state, private notes, credentials, or unrelated plugin folders.

### `musinsa-smell-remover.zip`

- Top-level directory must be `musinsa-smell-remover/`.
- Include `README.md` and `PROBLEM.md`.
- Include `src/.codex-plugin/plugin.json` with name `musinsa-smell-remover` and skills path `./skills/`. [High]
- Include `src/skills/musinsa-smell-remover/SKILL.md`.
- Include the plugin source, examples, tests, and output artifacts needed to demonstrate the workflow.
- Include `logs/README.md`; include real AI conversation logs only if exported from the actual session and approved. Do not invent logs. [High]
- Before zipping, scan included outputs for real customer data, credentials, local absolute paths, and overclaim language.

### `guru-avatar.zip`

- Top-level directory must be `guru-avatar/`.
- Include `README.md` and `PROBLEM.md`.
- Include `src/.codex-plugin/plugin.json` with name `guru-avatar` and skills path `./skills/`. [High]
- Include `src/skills/guru-avatar/SKILL.md`.
- Include the plugin source, examples, tests, and output artifacts needed to demonstrate the workflow.
- Include `logs/README.md`; include real AI conversation logs only if exported from the actual session and approved. Do not invent logs. [High]
- Before zipping, scan outputs for investment advice overclaims, buy/sell/hold phrasing, return forecasts, stale-data claims without disclaimers, and any private data.

### `missing-doc-hunter.zip`

- Top-level directory must be `missing-doc-hunter/`.
- Include `README.md` and `PROBLEM.md`.
- Include `src/.codex-plugin/plugin.json` with name `missing-doc-hunter` and skills path `./skills/`. [High]
- Include `src/skills/missing-doc-hunter/SKILL.md`.
- Include the plugin source, examples, tests, and output artifacts needed to demonstrate the workflow only after privacy/path validation.
- Include `logs/README.md`; include real AI conversation logs only if exported from the actual session and approved. Do not invent logs. [High]
- Gate before zipping: `submission_package_manifest.json` currently includes local absolute paths in `inputs`; if the upload will be public, stop for explicit approval to sanitize/regenerate/omit that artifact rather than uploading personal path metadata. [High]

## Validation Checklist Before Upload

Perform this checklist separately for each plugin immediately before opening or using the browser form.

1. **Folder identity**
   - Zip filename, top-level folder, plugin manifest `name`, skill folder, and form title all match the same plugin.
   - No files from another company/plugin are present.
2. **Problem evidence**
   - `PROBLEM.md` exists and has public source URLs.
   - Form copy uses only the matching plugin's source URLs.
3. **Non-affiliation disclaimer**
   - Submission copy says independent hackathon prototype.
   - It does not imply official product, partnership, deployment, customer access, or endorsement.
4. **Sample data safety**
   - No private customer data, credentials, access tokens, local absolute paths, or personal machine paths in packaged outputs.
   - Any sample company/person/entity is clearly demo data.
5. **Logs**
   - Use only real exported AI conversation logs if available and approved.
   - If no real logs are available, leave `logs/README.md` as the truthful placeholder and do not fabricate.
   - If the live form requires a log upload, stop and request the actual approved log artifact.
6. **Heuristic limits**
   - Musinsa: no claim of real-time stock, sales, fit, or trend accuracy.
   - Guru: no investment advice, recommendation, return forecast, or legal compliance approval claim.
   - Missing-doc: no audit conclusion, no evidence sufficiency opinion, and no claim that document contents or numbers were verified.
7. **Verification honesty**
   - Do not claim tests were run during this planning assignment.
   - Use observed sample outputs and README-described tests as verification evidence.
   - If future approval allows tests, record exact commands and results before adding any run claim.
8. **Browser readiness**
   - Have one final copy block per form field and one matching zip per plugin.
   - Keep plugin-specific source URLs visible during entry.
   - Use a submission tracker with status: drafted, zip attached, reviewed, approval received, submitted, receipt captured.

## Sequencing and Dependencies

1. **Plan approval gate**
   - Main agent or user reviews this plan.
   - No packaging or browser action before approval.
2. **Prepare per-plugin final copy**
   - Use the mapping above.
   - Trim to live field character limits if needed without removing disclaimers or evidence.
3. **Package each plugin independently**
   - Build `musinsa-smell-remover.zip`, `guru-avatar.zip`, and `missing-doc-hunter.zip` only after approval.
   - Run the packaging checklist per zip.
4. **Pre-upload validation**
   - Inspect contents and form copy against the validation checklist.
   - Stop on any risk gate.
5. **Aside/browser staging**
   - Open the target URL only after execution approval.
   - Create or open one submission draft per plugin.
   - Fill fields from the matching mapping and attach only the matching zip.
6. **Final approval gate**
   - If explicit final approval was not already given, stop before the irreversible final submit and request final approval with a concise summary of the three staged submissions.
7. **Submit only with approval**
   - Submit each plugin separately.
   - Capture confirmation ID, timestamp, final form title, and uploaded zip filename after each successful submit.

Dependencies: approved final copy, approved packaging method, actual source-code/package URL if the live form's "source URL" means code URL rather than problem-evidence URL, and actual AI logs if the form requires logs.

## Aside / Browser Execution Sequence

1. Open Aside to `https://hack.primer.kr/rounds/10?mode=` only after execution approval.
2. Confirm login/session and identify whether the form creates drafts or submits immediately.
3. Confirm the exact meaning of the live "source URL" field:
   - If it asks for public problem evidence, use the URLs listed in the mapping.
   - If it asks for source code URL, use the plugin-specific repository/package URL and move the public evidence URLs into the why field. Do not fabricate a repository URL.
4. Submission 1: `musinsa-smell-remover`
   - Enter plugin name/title consistently.
   - Paste Musinsa-only field copy.
   - Attach `musinsa-smell-remover.zip` only.
   - Review preview for non-affiliation and no overclaim.
5. Submission 2: `guru-avatar`
   - Start a new form/draft.
   - Paste KakaoPay Securities-only field copy.
   - Attach `guru-avatar.zip` only.
   - Review preview for no investment advice wording.
6. Submission 3: `missing-doc-hunter`
   - Start a new form/draft.
   - Paste Samil PwC/PwC-only field copy.
   - Attach `missing-doc-hunter.zip` only.
   - Review preview for no audit conclusion and no path/PII leakage.
7. Before any final submit button:
   - Stop unless explicit final approval has already been given for all three submissions.
   - If approval is partial, submit only approved plugins and leave the others unsubmitted.
8. After approved submit:
   - Record confirmation details separately per plugin.
   - Do not edit or resubmit unless the site explicitly permits safe updates and approval is granted.

## Risk Controls

| Risk | Control | Stop condition |
|---|---|---|
| Non-affiliation | Include "independent hackathon prototype" and "not official product/partnership" in each submission; avoid company logos or endorsement language unless already in allowed assets | Any copy says or implies official Musinsa, KakaoPay Securities, Samil PwC, or PwC affiliation |
| Sample data | State all inputs are local samples; scan outputs for PII, credentials, real customer data, and local absolute paths | Any packaged file exposes private data, tokens, or personal paths, especially the known missing-doc manifest path issue |
| Logs | Include only actual AI conversation logs if available and approved; otherwise leave truthful placeholder README | Live form requires logs but no real approved log artifact exists |
| Heuristic overclaims | Use words like "screen", "draft", "candidate", "human review", "local sample", and "heuristic"; avoid "guarantee", "prove", "certify", "recommend", "audit conclusion" | Any field states or implies automated final decisions, financial advice, legal compliance approval, or audit assurance |
| Company separation | One browser draft and one zip per company; source URLs and examples may not cross over | Any mismatch between zip, plugin name, company, source URL, or form copy |
| Source URL ambiguity | Verify live label in browser; use evidence URLs for problem-source field or code URL for source-code field | No valid plugin-specific code URL exists when source-code URL is mandatory |
| Final irreversible submit | Explicit final approval required unless already provided | Approval absent, partial, unclear, or only plan approval |

## Verification

Current planning verification:

- Relevant allowed files were inspected for all three plugin folders. [High]
- No product files were edited. [High]
- No tests, builds, formatters, zips, Aside actions, uploads, or external submissions were run in this assignment. [High]
- Verification evidence is limited to inspected sample outputs and README-described test coverage. [High]

Submission verification to perform after approval:

- Confirm each zip has a single matching top-level folder.
- Confirm each `plugin.json` name matches the zip and form title.
- Confirm each `SKILL.md` describes the same workflow as the form copy.
- Confirm every form answer preserves non-affiliation and human-review boundaries.
- Confirm source URLs correspond to the matching `PROBLEM.md`.
- Confirm final preview shows the correct attachment before stopping for final approval.

## Verification Plan

No test/build/formatter commands are part of this plan because the assignment explicitly forbids running them. Use static validation instead:

1. Re-read each final form draft against the per-plugin mapping.
2. Inspect each zip's file list before upload.
3. Spot-check included generated outputs for private data, local paths, and overclaims.
4. Compare live preview fields against the source plugin one last time.
5. Capture receipt details only after approved final submission.

If a later approval explicitly expands scope to allow tests, run only the plugin README's existing `python -m unittest discover src/tests` within each plugin and record exact results before adding test-run claims to the form. Until then, do not claim test execution.

## Acceptance Criteria

This planning assignment is complete when:

- A full Markdown plan covers all requested sections.
- The plan includes 3-5 principles, top 3 decision drivers, at least 2 viable options with pros/cons and a chosen option.
- Each plugin has independent positioning and form-answer mapping for what/who/situation, why, source URL, how it works, AI usage, and verification.
- Each plugin has a packaging checklist and the plan has a shared validation checklist.
- Browser execution steps include the final-submit stop gate.
- Risk controls cover non-affiliation, sample data, logs, heuristic overclaims, and company separation.
- The plan states that no product edits, zips, tests/builds/formatters, Aside actions, or submissions were performed.

Future execution is complete only when:

- Three separate validated zips exist.
- Three separate form drafts are filled with plugin-specific copy and matching attachments.
- Final approval is obtained or the workflow stops before irreversible submit.
- If approved and submitted, each plugin has its own confirmation record.

## Escalation / Risk Gate

- Use an executor only after plan approval for packaging and browser staging.
- Use a critic for final copy review if field length trimming is needed or if any wording risks overclaiming.
- Use the main agent or user for final submit approval and any decision to sanitize, regenerate, or omit risky packaged outputs.
- Use architect only if approval expands scope into plugin compatibility or structure changes.
- Do not use ultragoal for this three-submission execution unless the task expands into many more companies or repeated submission automation.

## Risks and Mitigations

- **Risk: live form fields differ from assumed labels.** Mitigation: verify labels in Aside after approval and map content by intent, not by field order.
- **Risk: source URL means code URL, not evidence URL.** Mitigation: do not fabricate; use approved plugin-specific repository/package URL, or stop if unavailable.
- **Risk: missing-doc output leaks local paths.** Mitigation: gate packaging on path scan; request approval to sanitize/regenerate/omit.
- **Risk: logs are required but not available.** Mitigation: stop and request real exported logs; never create fake logs.
- **Risk: investment or audit copy sounds too strong.** Mitigation: keep decision-support and human-review language; run critic review before browser submit if copy is shortened.
- **Risk: browser draft cross-contamination.** Mitigation: handle one plugin at a time or maintain an explicit submission tracker; check zip filename and company before final preview.
