# 검증 기록 (VERIFICATION)

검증 일시: 2026-07-10 / 환경: macOS(Apple Silicon), Python 3 표준 라이브러리만 사용, 외부 API 없음.
아래 결과는 전부 이 저장소의 예시 데이터로 실제 실행해 얻은 값입니다.

## 1. 정상 경로: 입력에서 결과까지

```bash
python3 src/tools/guru_lens.py \
  --metrics src/examples/stock_metrics.csv --holdings src/examples/public_holdings.csv \
  --lenses src/examples/guru_lenses.json --profile src/examples/user_profile.json \
  --out-dir src/outputs
python3 src/tools/compliance_check.py \
  --report src/outputs/guru_avatar_report.md --out src/outputs/compliance_check.md
```

입력 조건: `user_profile.json`의 `target_ticker: NVDA`, 초보(beginner) 프로필, 3년 투자 기간.

관찰된 결과:

| 항목 | 실측값 |
| --- | --- |
| 지표 분해 | 매출성장 94%, 영업이익률 54%, PER 55.2, FCF $27B 등 로컬 지표가 리포트 상단 Snapshot에 표시 |
| 렌즈 분석 | Buffett, Lynch, Dalio, Momentum, Dividend 5개 렌즈 모두 지지/주의 신호와 투자자 질문 생성 |
| 투자자 질문 예시 | Buffett 렌즈: "경쟁사가 이 사업을 왜 쉽게 못 베끼는지 한 문장으로 설명할 수 있는가" |
| 산출물 | `guru_avatar_report.md`, `guru_avatar_report.json`, `investor_questions.md`, `compliance_check.md` 4종 생성 |
| 컴플라이언스 | 금지 표현 16종 스캔 결과 PASS, 검출 0건 |
| 고지 | 리포트 최상단에 "Educational decision support only. Not financial advice." 고정 표기 |

## 2. 예외 경로

| 시나리오 | 명령 조건 | 관찰된 동작 |
| --- | --- | --- |
| 없는 티커 | `--ticker ZZZZ` | 데이터를 지어내지 않고 "not found in metrics file" 에러와 함께 사용 가능한 티커 목록(AAPL~TSLA)을 출력하고 exit 1로 종료 |
| 금지 표현 검출 | "strong buy", "지금 매수", "수익 보장", "매수 추천"을 심은 가짜 리포트를 스캔 | Status: FAIL, 4개 표현 전부 줄 번호와 함께 검출, exit 1 |

## 3. 자동 테스트

```bash
python3 -m unittest discover src/tests
```

8개 테스트 통과 (Ran 8 tests, OK):

- 4개 산출물이 모두 생성되는지
- 모든 렌즈에 투자자 질문이 포함되는지
- Beginner Safety Check가 포함되는지
- 생성 리포트에 금지 추천 표현이 없는지 / compliance가 PASS를 반환하는지

## 4. 발견했지만 아직 고치지 않은 점

- phrase lint는 문자열 매칭이므로 돌려 말한(패러프레이즈된) 위험 표현은 잡지 못합니다. 사람 검토가 반드시 필요합니다.
- 최신 시세·수익 전망은 다루지 않으며 로컬 샘플 지표 기준입니다.
