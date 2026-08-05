# guru-avatar

거장(guru)들의 투자 철학 템플릿과 주식 지표를 **초보자용 교육 콘텐츠 초안과 금지 표현 점검표**로 변환하는 Codex 워크플로 플러그인입니다. 카카오페이증권 같은 초보 투자자 기반 금융 플랫폼의 내부 콘텐츠·서비스·준법 담당자가 사용할 수 있는 후보 워크플로우이며, 산출물의 수혜자는 소수점·해외주식으로 유입된 초보 투자자입니다.

- 대상 기업: **카카오페이증권** · 축: 그 기업의 **고객(초보 투자자)** 문제를 그 기업의 **내부 팀**이 푸는 후보 도구
- 공개 근거: [`PROBLEM.md`](./PROBLEM.md) 참고 (예선 채점의 핵심)
- 비공식 고지: 이 플러그인은 해커톤용 독립 프로토타입이며, 카카오페이증권의 공식 제품·제휴·도입 사례가 아닙니다. 모든 데이터는 로컬 샘플입니다.

## 플러그인 개요

`guru-avatar`는 로컬 데이터 파일(주식 지표, 공개 보유 현황, 거장 렌즈 정의, 사용자 프로필)을 읽어, 각 투자 철학을 **판단 질문**으로 번역하고 초보자가 스스로 판단할 수 있도록 돕는 교육용 리포트를 생성합니다.

- 매수/매도/보유 추천을 **절대** 하지 않습니다.
- 미래 수익을 **절대** 예측하거나 보장하지 않습니다.
- 모든 결과물은 "투자 조언"이 아니라 "의사결정 보조 자료(decision support)"로 제시됩니다.

## 문제 정의

카카오페이증권은 소수점·해외주식으로 초보/MZ 투자자를 대규모로 확보했고, 이들은 해외주식·인기 종목·고위험 상품 이슈에 노출될 수 있습니다. 회사는 투자 정보·교육 콘텐츠를 확대하려 하지만, 종목·상품 관련 콘텐츠는 투자광고나 투자권유로 오해될 수 있어 사람이 신중하게 검토해야 합니다. 종목마다 안전한 교육 콘텐츠 초안을 일관되게 만들고 명백한 위험 표현을 먼저 걸러내는 작업은 느리고 반복적입니다.

`guru-avatar`는 이 내부 병목을 겨냥합니다: 종목별 교육 콘텐츠 초안을 일관된 템플릿으로 만들고, 매수/매도/보유·수익보장 등 **금지 표현을 배포 전 phrase lint 방식으로 1차 점검**한 뒤, 사람이 최종 검토하도록 합니다. 자세한 문제 근거는 [`PROBLEM.md`](./PROBLEM.md) 참고.

## 누가 사용하나요 (내부 운영자 / 수혜자)

- **운영자(후보)**: 카카오페이증권 같은 금융 플랫폼의 투자자교육 콘텐츠팀 / 서비스기획 / 준법 검토 보조 담당자
- **수혜자(고객)**: 소수점·해외주식으로 유입된 초보 투자자
- Codex에서 로컬 데이터로 재현 가능한 콘텐츠 파이프라인이 필요한 실무자

## 왜 투자 조언이 아닌가요

이 플러그인은 특정 종목의 매수/매도/보유를 권하지 않으며, 수익을 약속하지 않습니다. 모든 수치는 로컬 샘플 파일에서 온 것이며 최신이 아닐 수 있습니다. 산출된 점수와 신호는 휴리스틱이며, 리포트는 **여러분의 공부 출발점**일 뿐입니다. 실제 결정 전에는 반드시 1차 출처로 수치를 검증하고 자격 있는 전문가와 상담하세요.

## 플러그인 동작 방식

1. `user_profile.json`에서 대상 티커(`target_ticker`)를 읽습니다.
2. `stock_metrics.csv`에서 해당 티커의 지표를 읽습니다.
3. `guru_lenses.json`의 렌즈 정의와 `public_holdings.csv`의 공개 보유 맥락을 읽습니다.
4. 렌즈별/기준별로 다음을 생성합니다.
   - 이 렌즈가 무엇을 점검하는지
   - 지지 신호(supporting signals)
   - 주의 신호(caution signals)
   - 투자자를 위한 질문
5. 초보자 안전 점검(Beginner Safety Check) 섹션을 포함합니다.
6. 안전한 행동만 담은 다음 행동(Next Actions) 섹션을 포함합니다.
7. 리포트 확정 전 금지 표현 phrase lint를 실행하고, 명백한 금지 표현이 없을 때만 사람 검토용 초안으로 남깁니다.

### 렌즈 목록

- Buffett Lens: moat, cash flow, margin of safety, quality
- Peter Lynch Lens: understandable story, growth, valuation versus growth
- Dalio Lens: macro cycle, diversification, interest rate sensitivity
- Momentum Lens: trend, price action, market reaction
- Dividend Lens: dividend stability, cash flow, defensive quality

## 파일 구조

```
guru-avatar/
├── src/
│   ├── .codex-plugin/
│   │   └── plugin.json          # Codex 플러그인 매니페스트
│   ├── skills/
│   │   └── guru-avatar/
│   │       └── SKILL.md         # Codex 스킬 정의
│   ├── tools/
│   │   ├── guru_lens.py         # 리포트 생성기 (표준 라이브러리만 사용)
│   │   └── compliance_check.py  # 금지 표현 검사기
│   ├── examples/
│   │   ├── stock_metrics.csv
│   │   ├── public_holdings.csv
│   │   ├── guru_lenses.json
│   │   └── user_profile.json
│   ├── outputs/                 # 생성 결과물 위치
│   └── tests/
│       └── test_guru_avatar.py
├── README.md
└── logs/
    └── README.md
```

## 실행 방법

Python 3 표준 라이브러리만 사용합니다. pandas, 외부 API, 실시간 시세 조회를 쓰지 않습니다.

리포트 생성:

```bash
python src/tools/guru_lens.py \
  --metrics src/examples/stock_metrics.csv \
  --holdings src/examples/public_holdings.csv \
  --lenses src/examples/guru_lenses.json \
  --profile src/examples/user_profile.json \
  --out-dir src/outputs
```

컴플라이언스 검사:

```bash
python src/tools/compliance_check.py \
  --report src/outputs/guru_avatar_report.md \
  --out src/outputs/compliance_check.md
```

테스트 실행:

```bash
python -m unittest discover src/tests
```

## 예시 명령

기본 프로필의 대상 티커는 `NVDA`입니다. 다른 티커로 바꾸려면 `--ticker` 옵션을 쓰거나 `user_profile.json`의 `target_ticker`를 수정하세요.

```bash
python src/tools/guru_lens.py \
  --metrics src/examples/stock_metrics.csv \
  --holdings src/examples/public_holdings.csv \
  --lenses src/examples/guru_lenses.json \
  --profile src/examples/user_profile.json \
  --out-dir src/outputs \
  --ticker KO
```

## 생성되는 결과물

- `outputs/guru_avatar_report.md` : 렌즈별 교육용 분석 + 초보자 안전 점검 + 다음 행동
- `outputs/guru_avatar_report.json` : 기계 판독용 구조화 리포트
- `outputs/investor_questions.md` : 렌즈별 투자자 질문 모음
- `outputs/compliance_check.md` : 금지 표현 phrase lint 결과, 탐지된 위험 표현, 수정 가이드

## 검증 방법

> 실측 검증 결과(정상 경로 실측값, 예외 경로 재현 명령, 테스트 결과, 남은 한계)는 [`VERIFICATION.md`](./VERIFICATION.md)에 정리되어 있습니다.

- `python -m unittest discover src/tests`로 다음을 검증합니다.
  - 네 개의 결과물 파일이 모두 생성되는지
  - 리포트에 금지된 추천성 표현이 없는지
  - 모든 렌즈가 투자자 질문을 포함하는지
  - Beginner Safety Check 섹션이 포함되는지
  - 생성된 리포트에 대해 `compliance_check.py`가 명백한 금지 표현을 탐지하지 않는지
- `compliance_check.py`는 리포트에서 다음과 같은 금지 표현을 스캔합니다: `buy now`, `sell now`, `strong buy`, `guaranteed`, `target return`, `must buy`, `must sell`, `지금 매수`, `지금 매도`, `무조건`, `확실한 수익`, `수익 보장`, `매수 추천`, `매도 추천`, `보유 추천` 등.

## 한계

- 점수/신호는 로컬 샘플 데이터에 기반한 **휴리스틱**이며, 실제 재무 실사가 아닙니다.
- 지표는 예시 파일 값이므로 최신이 아닐 수 있습니다.
- 실시간 시세나 뉴스, 재무제표 원문을 조회하지 않습니다.
- 특정 종목의 매수/매도/보유 판단을 대신하지 않습니다.

## 사람 검토(Human review) 참고

- 스코어링 모델은 규칙 기반 휴리스틱이므로, 리포트를 결정 근거로 삼기 전 사람이 반드시 수치와 논리를 재검토해야 합니다.
- 렌즈 정의(`guru_lenses.json`)와 임계값은 교육 목적으로 단순화되어 있으며, 실제 거장들의 방법론을 완전히 재현하지 않습니다.
- 컴플라이언스 검사는 표현 기반 필터이므로, 새로운 표현이 나타나면 `PROHIBITED_PHRASES` 목록을 갱신하세요.

## 로그 안내

`logs/` 폴더에는 제출용 실제 AI 대화 로그가 포함되어 있습니다: `ai-conversation-chatgpt-share.txt`, `chatgpt-share-url.txt`, `LOG_SOURCE.md`, `README.md`. 동일한 공유 ChatGPT 대화가 세 플러그인 제작·검토 과정을 모두 포함하므로 각 독립 제출물에 같은 전체 대화 로그를 포함합니다. 가짜 로그는 생성하지 않습니다.
