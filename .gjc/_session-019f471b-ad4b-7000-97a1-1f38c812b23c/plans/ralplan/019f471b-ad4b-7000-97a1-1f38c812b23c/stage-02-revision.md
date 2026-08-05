# Revised Submission Execution Plan for Three Independent Codex Workflow Plugin Submissions

## Summary

Create three separate AX hackathon submissions for `musinsa-smell-remover`, `guru-avatar`, and `missing-doc-hunter`. This is still planning only: no product file edits, no zip creation, no test/build/formatter runs, no Aside/browser action, and no external submission.

This revision preserves the stage 1 structure and adds three required hard gates from architect review:

1. Real approved AI conversation logs are a hard prerequisite for final packaging and submission for every plugin. If unavailable, stop. No fake logs. [High]
2. Source-code URL strategy must be resolved before browser staging. If the live form's Source URL means code, do not proceed without concrete public plugin-specific code/package URLs. [High]
3. `missing-doc-hunter` local absolute paths must be sanitized, regenerated, or omitted before any final zip, regardless of whether the upload is public or private. [High]

Evidence basis from prior inspection: each plugin's `README.md`, `PROBLEM.md`, `src/.codex-plugin/plugin.json`, `src/skills/*/SKILL.md`, selected `src/outputs/*`, and `logs/README.md` were inspected. [High]

## Intent Diff

- Requested outcome: a revised submission execution plan, not implementation or upload. [High]
- Required separation: three independent plugin folders and three independent company submissions. [High]
- Required caution: preserve problem evidence, non-affiliation disclaimers, and reduced overclaims. [High]
- Required revisions:
  - Logs are mandatory for final packaging, not optional or form-dependent. [High]
  - Source-code URL availability must be resolved before browser staging. [High]
  - `missing-doc-hunter` absolute path remediation is mandatory before final zip. [High]
- Not requested: improving plugin code, changing product files, creating zips, running tests/builds/formatters, operating Aside, or submitting to the hackathon site.

## Principles

1. **Separate every company and plugin**: one form draft, one zip, one positioning angle, and one evidence set per plugin.
2. **Evidence-grounded copy only**: every problem claim must trace to that plugin's `PROBLEM.md`; do not add unsupported market, legal, financial, or audit claims.
3. **Human-review framing**: present each plugin as a Codex workflow that prepares or screens outputs for human review, not as an automatic decision-maker.
4. **Required artifacts only, never fake artifacts**: real approved AI conversation logs are required for final packaging; never invent logs, source URLs, test results, sample data, business affiliations, or submission receipts.
5. **Resolve gates before staging**: source-code URL strategy, log availability, and known path sanitization must be closed before any browser staging or final zip work.
6. **Stop before irreversible action**: browser execution may stage drafts only after all pre-staging gates pass and execution is approved; final submit requires explicit final approval unless already granted.

## Decision Drivers

1. **Company separation and form integrity**: Musinsa, KakaoPay Securities, and Samil PwC/PwC are different targets, so combined packaging or shared form answers would weaken the submission and increase non-affiliation risk. [High]
2. **Required artifact completeness**: each plugin's `logs/README.md` states the logs folder is reserved for the full AI conversation log required for submission, so final packaging cannot proceed without real approved logs. [High]
3. **Upload safety and URL correctness**: generated outputs and form URLs need validation before packaging or staging. Known mandatory fix: `missing-doc-hunter/src/outputs/submission_package_manifest.json` contains local absolute input paths under `/Users/...`; these must be sanitized, regenerated, or omitted before any final zip. Source-code URLs must also be concrete and plugin-specific if the form's Source URL means code. [High]

## Options

| Option | Description | Pros | Cons | Decision |
|---|---|---|---|---|
| A | Three separate submissions, each with its own final zip, real log artifact, source strategy, problem evidence, and form copy | Matches the stated multi-company constraint; isolates risks; preserves plugin-specific evidence; supports clean judging | Requires more validation and hard gates | **Chosen** |
| B | One umbrella submission covering all three plugins | Fastest single form flow | Violates the separate-company constraint; dilutes problem evidence; creates affiliation and attachment confusion | Rejected |
| C | Stage all three browser drafts first, then request a single final approval before submitting all | Efficient final review after all gates pass; supports batch final approval | Requires careful tab/form tracking; unsafe unless source URLs, logs, and package sanitation are already resolved | Use inside Option A only after hard gates pass |
| D | Submit one plugin fully, then repeat for the next | Lowest risk per form and easiest recovery if the site is unstable | Slowest; can create inconsistent copy if later submissions change wording | Fallback if the site has unstable drafts |
| E | Package without logs and rely on `logs/README.md` placeholder | Fast when logs are not available | Conflicts with logs/README requirement and architect review; risks invalid submission | Rejected |

Chosen plan: Option A with Option C as the normal execution pattern only after hard gates pass. If the site cannot safely hold separate drafts, fall back to Option D. Option E is explicitly forbidden.

## In Scope / Out of Scope

### In scope

- Submission positioning for all three plugins.
- Per-plugin form-answer mapping for: what/who/situation, why, source URL, how it works, AI usage, and verification.
- Source-code URL strategy gate before browser staging.
- Required real-log gate before final packaging and submission.
- Mandatory `missing-doc-hunter` local path remediation before final zip.
- Packaging checklist for each independent zip.
- Pre-upload validation checklist.
- Aside/browser execution sequence with pre-staging and final-submit stop gates.
- Risk controls for non-affiliation, sample data, logs, source URLs, heuristic overclaims, and company separation.
- Acceptance criteria for the eventual execution.

### Out of scope for this assignment

- Editing product files.
- Creating zip files.
- Running tests, builds, formatters, or plugin commands.
- Using Aside or another browser.
- Uploading files or submitting the hackathon form.
- Fabricating missing source URLs, logs, or verification evidence.

## File-Level Changes

No product file changes are planned or allowed for this planning assignment.

Future execution may require an approved remediation step for `missing-doc-hunter` path leakage before final packaging. Acceptable remediations are:

1. regenerate `submission_package_manifest.json` with relative paths,
2. sanitize the `inputs` path fields to relative paths or neutral sample paths, or
3. omit that output artifact from the final zip if the package still contains enough demonstrable outputs.

This remediation is mandatory before any final `missing-doc-hunter` zip, regardless of whether the upload is public or private. It must be approved and recorded rather than silently applied during this planning task.

## Required Pre-Staging Gates

These gates must pass before any Aside/browser staging or final zip work.

### Gate 1: Real AI Conversation Logs

- For each plugin, obtain the real approved AI conversation log required for submission.
- Place or include the approved log artifact only through the approved execution process after plan approval.
- Do not treat `logs/README.md` as a substitute for the required log.
- Do not create fake logs, summaries pretending to be logs, or synthetic transcripts.
- If real approved logs are unavailable for any plugin, stop final packaging and submission for that plugin.

### Gate 2: Source URL Strategy

Resolve before browser staging whether the hackathon form's Source URL field means:

- public problem/evidence source URL, or
- source-code/package URL.

If it means problem evidence, use the per-plugin evidence URLs in the mapping below.

If it means code, obtain concrete public plugin-specific code/package URLs before staging, for example URLs that directly identify each folder or package:

| Plugin | Required code URL status before staging |
|---|---|
| `musinsa-smell-remover` | Must have concrete public plugin-specific code/package URL or stop |
| `guru-avatar` | Must have concrete public plugin-specific code/package URL or stop |
| `missing-doc-hunter` | Must have concrete public plugin-specific code/package URL or stop |

Do not discover missing code URLs during browser data entry. If unavailable, stop and ask the main agent/user for the URLs.

### Gate 3: `missing-doc-hunter` Path Remediation

Before any final `missing-doc-hunter` zip:

- Inspect packaged outputs for local absolute paths.
- Remediate `src/outputs/submission_package_manifest.json` by sanitizing, regenerating, or omitting the path-bearing artifact.
- Verify no `/Users/...`, personal workstation path, or local absolute path remains in the zip.
- This gate is mandatory regardless of public/private visibility.

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

For the Source URL field, use the following rule:

- If the field means problem/evidence URL, use the URLs listed below.
- If the field means source-code/package URL, use only the concrete plugin-specific public code/package URL resolved in Gate 2. Move the problem evidence URLs into the why/evidence text.
- If the code URL is unavailable, stop before browser staging and ask for it.

### `musinsa-smell-remover`

| Field | Submission mapping |
|---|---|
| What / who / situation | `무신사처럼 랭킹 영향력이 큰 패션 플랫폼의 MD, 스타일 에디터, 추천 실험 담당자가 상위 랭킹 중심 콘텐츠로 인해 안전하지만 비슷한 착장이 반복되는 상황에서 쓰는 Codex 워크플로우입니다. 로컬 상품, 랭킹, 리뷰, 사용자 요청 파일을 읽고 "무신사 냄새"를 취향 비난이 아니라 클론룩 위험과 추천 다양성 저하 문제로 재정의해 점검합니다.` |
| Why | `무신사는 최근 실적과 성장세로 패션 플랫폼 영향력이 크고, 인기 품목 중심 소비는 착장 획일화와 클론룩 논의를 낳습니다. 이 플러그인은 브랜드를 비판하지 않고, 랭킹과 리뷰 흔함 신호, 색상, 소재, 실루엣, 회피 키워드를 함께 보아 "덜 흔하지만 여전히 입기 쉬운" 후보를 사람 검토 전에 정리합니다.` |
| Source URL | Problem/evidence mode: `https://biz.newdaily.co.kr/site/data/html/2026/04/08/2026040800264.html`, plus `https://www.news1.kr/industry/distribution/6130067` and `https://www.hanbat.ac.kr/prog/bbsArticle/BBSMSTR_000000000077/view.do?nttId=B000000105566Mn0bG3r&mno=sub01_07`. Code mode: use the resolved public plugin-specific code/package URL for `musinsa-smell-remover`; if unavailable, stop. |
| How it works | `Codex가 스킬 정의를 따라 로컬 CSV/JSON 입력(products, rankings, reviews, user_request)을 읽고, Python 표준 라이브러리 도구가 상품별 Clone Risk Score(0-100)를 계산합니다. 회피 키워드와 직접 충돌하는 상품을 제외한 뒤 예산 안에서 3-5개 코디 후보를 고르고, clone_risk_scores.csv, recommendation.json, musinsa_smell_removal_report.md를 생성합니다.` |
| AI usage | `AI는 문제 프레이밍과 사람 검토용 리포트 구성을 돕고, Codex 워크플로우는 로컬 데이터와 명시된 휴리스틱만 사용합니다. 외부 쇼핑 API나 실시간 크롤링을 하지 않으며, 결과는 최종 스타일 판단이 아니라 MD/에디터의 검토 초안입니다.` |
| Verification | `샘플 출력 기준 22개 상품이 0-100 점수로 평가되었고, 추천 코디 평균 위험도는 16.0/100으로 로컬 평균 40.6/100보다 낮으며, 총액 199,000원은 200,000원 예산 안입니다. 직접 회피 항목(black wide pants, oversized graphic t-shirt, german army sneakers)은 추천에서 제외됩니다. README의 테스트 범위는 점수 범위, 회피 충돌 가중, CSV/JSON 생성, 추천 충돌 부재를 확인하도록 되어 있습니다. 이번 계획 단계에서는 테스트를 실행하지 않았다고 명시합니다.` |

### `guru-avatar`

| Field | Submission mapping |
|---|---|
| What / who / situation | `카카오페이증권 같은 초보 투자자 기반 금융 플랫폼의 투자자교육 콘텐츠팀, 서비스기획, 준법 검토 보조 담당자가 종목별 교육 콘텐츠를 빠르게 초안화하고 명백한 금지 표현을 사람 검토 전에 걸러내는 Codex 워크플로우입니다.` |
| Why | `카카오페이증권은 초보/MZ 투자자 기반과 AI 기반 투자정보 서비스 확대 맥락이 있고, 개인투자자의 고위험 상품 노출과 투자광고/투자권유 표현 리스크가 함께 존재합니다. 콘텐츠팀은 초보자에게 도움이 되는 설명을 만들되 매수/매도/보유 권유나 수익 보장처럼 오해될 표현을 피해야 하므로 반복 가능한 초안 생성과 phrase lint가 필요합니다.` |
| Source URL | Problem/evidence mode: `https://www.news2day.co.kr/article/20260609500200`, plus `https://v.daum.net/v/20260623230143657`, `https://www.edaily.co.kr/News/Read?newsId=04178726645451544`, and `https://www.fsc.go.kr/no010101/76045`. Code mode: use the resolved public plugin-specific code/package URL for `guru-avatar`; if unavailable, stop. |
| How it works | `Codex가 user_profile.json의 대상 티커와 로컬 stock_metrics.csv, public_holdings.csv, guru_lenses.json을 읽습니다. 도구가 Buffett, Peter Lynch, Dalio, Momentum, Dividend 렌즈별로 확인 기준, 지지 신호, 주의 신호, 투자자 질문을 생성하고 Beginner Safety Check와 안전한 다음 행동만 포함합니다. 이후 compliance_check.py가 buy/sell/hold, 수익 보장 등 금지 표현을 스캔해 compliance_check.md를 생성합니다.` |
| AI usage | `AI는 투자 철학 템플릿을 초보자용 판단 질문과 교육 초안으로 바꾸는 데 사용됩니다. 투자 조언, 매수/매도/보유 신호, 수익 예측을 생성하지 않으며 모든 출력은 decision support와 human review draft로 제한됩니다. 모든 수치는 로컬 샘플 데이터이므로 1차 출처 재확인이 필요합니다.` |
| Verification | `샘플 출력은 NVDA 교육 리포트, JSON 구조화 결과, 투자자 질문, compliance_check.md를 생성합니다. compliance_check.md는 16개 금지 표현을 스캔했고 Status: PASS, detected risky phrases none으로 기록되어 있습니다. README의 테스트 범위는 네 개 결과물 생성, 금지 추천 표현 부재, 모든 렌즈의 질문 포함, Beginner Safety Check 포함, compliance check PASS를 확인하도록 되어 있습니다. 이번 계획 단계에서는 테스트를 실행하지 않았다고 명시합니다.` |

### `missing-doc-hunter`

| Field | Submission mapping |
|---|---|
| What / who / situation | `삼일PwC 같은 회계감사, 세무, 자문 조직의 실무팀이 고객 PBC 요청 목록과 로컬 evidence manifest를 대조해 누락, 불충분, 기간/법인/승인/연결 키 문제를 사람 검토 전에 찾는 Codex 워크플로우입니다.` |
| Why | `PBC 포털은 자료 요청과 수령 상태를 관리할 수 있지만, 받은 자료가 충분하고 적합한지, 기간과 법인이 맞는지, 필수 연결 키와 승인 로그가 있는지는 여전히 사람이 확인해야 합니다. 이 왕복이 늦어지면 제출 패키지 준비와 고객 커뮤니케이션이 지연됩니다. 이 플러그인은 명백한 누락과 약한 증빙을 보수적으로 표시해 전문가가 원문 검토에 들어가기 전 후속 요청을 정리합니다.` |
| Source URL | Problem/evidence mode: `https://m.ddaily.co.kr/page/view/2026051115581496536`, plus `https://www.frc.org.uk/library/standards-codes-policy/audit-assurance-and-ethics/auditing-standards/isa-uk-500/`, `https://fss.or.kr/fss/bbs/B0000129/list.do?menuNo=200437`, `https://fss.or.kr/fss/bbs/B0000135/list.do?menuNo=200448`, `https://connect.pwc.com/`, `https://www.auditdashboard.com/`, and `https://www.edaily.co.kr/News/Read?newsId=01587526645486312`. Code mode: use the resolved public plugin-specific code/package URL for `missing-doc-hunter`; if unavailable, stop. |
| How it works | `Codex가 PBC request list, evidence manifest, optional trial balance를 읽도록 스킬을 적용합니다. Python 표준 라이브러리 도구가 요청 목적과 유형을 추론하고 required evidence와 linking keys를 분해한 뒤 manifest의 파일 메타데이터와 매칭합니다. missing_document, partial_period_mismatch, entity_mismatch, missing_required_columns, missing_approval, weak_source, needs_manual_judgment를 탐지하고 각 요청을 Ready, Partially ready, Missing, Needs human review로 분류합니다. 결과로 submission_package_manifest.json, missing_doc_hunter_report.md, missing_items.md, followup_email_draft.md를 생성합니다.` |
| AI usage | `AI는 PBC 요청의 목적을 해석하고 사람 검토용 리포트와 후속 요청 초안을 구성하는 데 사용됩니다. 증빙을 만들거나 있다고 가정하지 않으며, Ready도 감사 결론이 아니라 샘플 manifest 기준의 사전 스크리닝 상태로만 표시합니다. 애매하면 Needs human review로 보수적으로 남깁니다.` |
| Verification | `샘플 출력은 5개 요청을 평가해 Ready 1, Partially ready 2, Needs human review 1, Missing 1로 요약합니다. 리포트는 CUT-01의 contract_id 누락과 기간 불일치, JE-02의 placeholder/approval 문제, INV-04의 nrv/allowance_amount 및 valuation support 누락, RP-05의 entity mismatch와 missing evidence를 표시합니다. README의 테스트 범위는 manifest 생성, 5개 요청 포함, 상태 분포, AR 필수 키 포함, Markdown 3종 생성, issue type 포함을 확인하도록 되어 있습니다. 이번 계획 단계에서는 테스트를 실행하지 않았다고 명시합니다.` |

## Packaging Checklist for Each Zip

General rule for all three zips: one top-level folder per archive, no combined submission, no `.git`, `__pycache__`, local virtual environments, OS metadata, hidden editor state, private notes, credentials, unrelated plugin folders, or unsanitized local paths.

Hard log rule for every zip: final zip creation is blocked until the plugin includes the real approved AI conversation log required for submission. `logs/README.md` is only an instruction placeholder, not the required log. No fake logs.

### `musinsa-smell-remover.zip`

- Top-level directory must be `musinsa-smell-remover/`.
- Include `README.md` and `PROBLEM.md`.
- Include `src/.codex-plugin/plugin.json` with name `musinsa-smell-remover` and skills path `./skills/`. [High]
- Include `src/skills/musinsa-smell-remover/SKILL.md`.
- Include the plugin source, examples, tests, and output artifacts needed to demonstrate the workflow after safety scan.
- Include the real approved AI conversation log required for submission. If unavailable, stop before final zip. [High]
- Before finalizing zip, scan included outputs for real customer data, credentials, local absolute paths, and overclaim language.

### `guru-avatar.zip`

- Top-level directory must be `guru-avatar/`.
- Include `README.md` and `PROBLEM.md`.
- Include `src/.codex-plugin/plugin.json` with name `guru-avatar` and skills path `./skills/`. [High]
- Include `src/skills/guru-avatar/SKILL.md`.
- Include the plugin source, examples, tests, and output artifacts needed to demonstrate the workflow after safety scan.
- Include the real approved AI conversation log required for submission. If unavailable, stop before final zip. [High]
- Before finalizing zip, scan outputs for investment advice overclaims, buy/sell/hold phrasing, return forecasts, stale-data claims without disclaimers, private data, credentials, and local absolute paths.

### `missing-doc-hunter.zip`

- Top-level directory must be `missing-doc-hunter/`.
- Include `README.md` and `PROBLEM.md`.
- Include `src/.codex-plugin/plugin.json` with name `missing-doc-hunter` and skills path `./skills/`. [High]
- Include `src/skills/missing-doc-hunter/SKILL.md`.
- Include the plugin source, examples, tests, and output artifacts needed to demonstrate the workflow only after path/privacy validation.
- Include the real approved AI conversation log required for submission. If unavailable, stop before final zip. [High]
- Mandatory before final zip: sanitize, regenerate, or omit `src/outputs/submission_package_manifest.json` because it currently contains local absolute input paths. Verify no local absolute paths remain anywhere in the zip. [High]

## Validation Checklist Before Upload

Perform this checklist separately for each plugin immediately before any browser staging and again before final upload.

1. **Hard gate status**
   - Real approved AI log exists and is included for the plugin.
   - Source URL strategy is resolved before browser staging.
   - If Source URL means code, the concrete public plugin-specific code/package URL exists.
   - For `missing-doc-hunter`, absolute path remediation is complete before final zip.
2. **Folder identity**
   - Zip filename, top-level folder, plugin manifest `name`, skill folder, and form title all match the same plugin.
   - No files from another company/plugin are present.
3. **Problem evidence**
   - `PROBLEM.md` exists and has public source URLs.
   - Form copy uses only the matching plugin's source URLs.
4. **Non-affiliation disclaimer**
   - Submission copy says independent hackathon prototype.
   - It does not imply official product, partnership, deployment, customer access, or endorsement.
5. **Sample data safety**
   - No private customer data, credentials, access tokens, local absolute paths, or personal machine paths in packaged outputs.
   - Any sample company/person/entity is clearly demo data.
6. **Logs**
   - Include only real approved AI conversation logs.
   - Do not use `logs/README.md` as a substitute.
   - Stop final packaging/submission for any plugin without the required real log.
7. **Heuristic limits**
   - Musinsa: no claim of real-time stock, sales, fit, or trend accuracy.
   - Guru: no investment advice, recommendation, return forecast, or legal compliance approval claim.
   - Missing-doc: no audit conclusion, no evidence sufficiency opinion, and no claim that document contents or numbers were verified.
8. **Verification honesty**
   - Do not claim tests were run during this planning assignment.
   - Use observed sample outputs and README-described tests as verification evidence.
   - If future approval allows tests, record exact commands and results before adding any run claim.
9. **Browser readiness**
   - Have one final copy block per form field and one matching zip per plugin.
   - Have the correct source URL value ready for the resolved Source URL meaning.
   - Use a submission tracker with status: gates passed, drafted, zip attached, reviewed, approval received, submitted, receipt captured.

## Sequencing and Dependencies

1. **Plan approval gate**
   - Main agent or user reviews this revised plan.
   - No packaging or browser action before approval.
2. **Resolve required pre-staging gates**
   - Obtain real approved AI conversation logs for all plugins intended for submission.
   - Resolve Source URL semantics and obtain public plugin-specific code/package URLs if the field means code.
   - Decide and approve the `missing-doc-hunter` path remediation method.
3. **Prepare per-plugin final copy**
   - Use the mapping above.
   - Trim to live field character limits only after preserving disclaimers, evidence, source strategy, and human-review boundaries.
4. **Package each plugin independently**
   - Build `musinsa-smell-remover.zip`, `guru-avatar.zip`, and `missing-doc-hunter.zip` only after approval and only for plugins whose log gate passes.
   - Do not finalize `missing-doc-hunter.zip` until path remediation is complete and verified.
5. **Pre-upload validation**
   - Inspect contents and form copy against the validation checklist.
   - Stop on any risk gate.
6. **Aside/browser staging**
   - Open or use the target URL only after execution approval and pre-staging gates pass.
   - Create or open one submission draft per plugin.
   - Fill fields from the matching mapping and attach only the matching zip.
7. **Final approval gate**
   - If explicit final approval was not already given, stop before the irreversible final submit and request final approval with a concise summary of the three staged submissions.
8. **Submit only with approval**
   - Submit each plugin separately.
   - Capture confirmation ID, timestamp, final form title, Source URL value, and uploaded zip filename after each successful submit.

Dependencies: approved final copy, real approved AI logs, resolved Source URL semantics, concrete public plugin-specific code URLs if Source URL means code, approved packaging method, approved `missing-doc-hunter` path remediation, and final submit approval.

## Aside / Browser Execution Sequence

This sequence starts only after the pre-staging gates pass.

1. Confirm that the required real logs are available and included for the specific plugin being staged.
2. Confirm the Source URL field strategy has already been resolved:
   - evidence mode: use the problem evidence URLs from the mapping,
   - code mode: use the concrete public plugin-specific code/package URL,
   - unresolved or missing code URL: do not open/stage; stop and ask for it.
3. Open Aside to `https://hack.primer.kr/rounds/10?mode=` only after execution approval and gate completion.
4. Confirm login/session and identify whether the form creates drafts or submits immediately.
5. Submission 1: `musinsa-smell-remover`
   - Enter plugin name/title consistently.
   - Paste Musinsa-only field copy.
   - Attach `musinsa-smell-remover.zip` only.
   - Review preview for required logs, non-affiliation, source URL correctness, and no overclaim.
6. Submission 2: `guru-avatar`
   - Start a new form/draft.
   - Paste KakaoPay Securities-only field copy.
   - Attach `guru-avatar.zip` only.
   - Review preview for required logs, source URL correctness, and no investment advice wording.
7. Submission 3: `missing-doc-hunter`
   - Start a new form/draft.
   - Paste Samil PwC/PwC-only field copy.
   - Attach `missing-doc-hunter.zip` only after path remediation verification.
   - Review preview for required logs, source URL correctness, no audit conclusion, and no path/PII leakage.
8. Before any final submit button:
   - Stop unless explicit final approval has already been given for the exact staged submissions.
   - If approval is partial, submit only approved plugins and leave the others unsubmitted.
9. After approved submit:
   - Record confirmation details separately per plugin.
   - Do not edit or resubmit unless the site explicitly permits safe updates and approval is granted.

## Risk Controls

| Risk | Control | Stop condition |
|---|---|---|
| Missing real AI logs | Treat logs as a hard prerequisite for final packaging for all plugins; `logs/README.md` is not a substitute | Any plugin lacks a real approved AI conversation log |
| Fake logs | Never create synthetic logs, summaries pretending to be logs, or backfilled transcripts | Any request would require inventing logs |
| Source URL ambiguity | Resolve Source URL semantics before browser staging; prepare either evidence URLs or concrete plugin-specific code URLs | Source URL means code and a concrete public plugin-specific code/package URL is unavailable |
| Non-affiliation | Include "independent hackathon prototype" and "not official product/partnership" in each submission; avoid company logos or endorsement language unless already in allowed assets | Any copy says or implies official Musinsa, KakaoPay Securities, Samil PwC, or PwC affiliation |
| Sample data | State all inputs are local samples; scan outputs for PII, credentials, real customer data, and local absolute paths | Any packaged file exposes private data, tokens, or personal paths |
| `missing-doc-hunter` local absolute paths | Mandatory sanitize/regenerate/omit before final zip, regardless of public/private visibility | Any `/Users/...` or local absolute path remains in final zip |
| Heuristic overclaims | Use words like "screen", "draft", "candidate", "human review", "local sample", and "heuristic"; avoid "guarantee", "prove", "certify", "recommend", "audit conclusion" | Any field states or implies automated final decisions, financial advice, legal compliance approval, or audit assurance |
| Company separation | One browser draft and one zip per company; source URLs and examples may not cross over | Any mismatch between zip, plugin name, company, source URL, log artifact, or form copy |
| Final irreversible submit | Explicit final approval required unless already provided | Approval absent, partial, unclear, or only plan approval |

## Verification

Current planning verification:

- The revised plan directly addresses all three architect-blocking requirements. [High]
- No product files were edited. [High]
- No tests, builds, formatters, zips, Aside actions, uploads, or external submissions were run in this assignment. [High]
- Verification evidence is limited to inspected sample outputs, plugin metadata, logs README requirements, and README-described test coverage from the prior planning inspection. [High]

Submission verification to perform after approval:

- Confirm each plugin has a real approved AI conversation log in the final package.
- Confirm Source URL semantics and values before browser staging.
- Confirm each zip has a single matching top-level folder.
- Confirm each `plugin.json` name matches the zip and form title.
- Confirm each `SKILL.md` describes the same workflow as the form copy.
- Confirm every form answer preserves non-affiliation and human-review boundaries.
- Confirm source URLs correspond to the resolved field meaning and the matching plugin.
- Confirm `missing-doc-hunter` final zip has no local absolute paths.
- Confirm final preview shows the correct attachment before stopping for final approval.

## Verification Plan

No test/build/formatter commands are part of this plan because the assignment explicitly forbids running them. Use static validation instead:

1. Verify real approved AI logs are available for each plugin.
2. Resolve Source URL semantics and prepare concrete URL values before browser staging.
3. Re-read each final form draft against the per-plugin mapping.
4. Inspect each zip's file list before upload.
5. Spot-check included generated outputs for private data, local paths, logs, and overclaims.
6. Specifically verify `missing-doc-hunter` path remediation before final zip.
7. Compare live preview fields against the source plugin one last time.
8. Capture receipt details only after approved final submission.

If a later approval explicitly expands scope to allow tests, run only the plugin README's existing `python -m unittest discover src/tests` within each plugin and record exact results before adding test-run claims to the form. Until then, do not claim test execution.

## Acceptance Criteria

This revised planning assignment is complete when:

- A full revised Markdown plan covers all requested sections.
- The plan preserves the core stage 1 structure.
- The plan makes real approved AI conversation logs a hard prerequisite for final packaging and submission for every plugin.
- The plan requires Source URL strategy and any needed public plugin-specific code/package URLs before browser staging.
- The plan makes `missing-doc-hunter` local absolute path sanitization, regeneration, or omission mandatory before any final zip, regardless of upload visibility.
- The plan includes 3-5 core principles plus the necessary revised gate principle, top 3 decision drivers, at least 2 viable options with pros/cons and a chosen option.
- Each plugin has independent positioning and form-answer mapping for what/who/situation, why, source URL, how it works, AI usage, and verification.
- Each plugin has a packaging checklist and the plan has a shared validation checklist.
- Browser execution steps include pre-staging gates and the final-submit stop gate.
- Risk controls cover non-affiliation, sample data, logs, source URLs, heuristic overclaims, path leakage, and company separation.
- The plan states that no product edits, zips, tests/builds/formatters, Aside actions, or submissions were performed.

Future execution is complete only when:

- Three separate validated zips exist, each with the required real approved AI log.
- Source URL values are resolved and correct for the live form semantics.
- `missing-doc-hunter` final zip has no local absolute paths.
- Three separate form drafts are filled with plugin-specific copy and matching attachments.
- Final approval is obtained or the workflow stops before irreversible submit.
- If approved and submitted, each plugin has its own confirmation record.

## Escalation / Risk Gate

- Use an executor only after plan approval for gate resolution, packaging, and browser staging.
- Use a critic for final copy review if field length trimming is needed or if any wording risks overclaiming.
- Use the main agent or user for required real log artifacts, Source URL semantics, public code/package URLs, final submit approval, and any decision to sanitize, regenerate, or omit risky packaged outputs.
- Use architect only if approval expands scope into plugin compatibility, structure changes, or another blocked plan review.
- Do not use ultragoal for this three-submission execution unless the task expands into many more companies or repeated submission automation.

## Risks and Mitigations

- **Risk: real logs are unavailable.** Mitigation: stop final packaging/submission for the affected plugin; do not fabricate or substitute `logs/README.md`.
- **Risk: live form Source URL means code but no public plugin-specific URL exists.** Mitigation: resolve before browser staging; stop and ask for concrete URLs.
- **Risk: live form fields differ from assumed labels.** Mitigation: use the resolved field semantics and map content by intent, not by field order.
- **Risk: missing-doc output leaks local paths.** Mitigation: mandatory sanitize/regenerate/omit before final zip regardless of visibility.
- **Risk: investment or audit copy sounds too strong.** Mitigation: keep decision-support and human-review language; run critic review before browser submit if copy is shortened.
- **Risk: browser draft cross-contamination.** Mitigation: handle one plugin at a time or maintain an explicit submission tracker; check zip filename, company, logs, and source URL before final preview.
- **Risk: package contains stale or unapproved remediation.** Mitigation: verify final zip contents after remediation and before upload.
