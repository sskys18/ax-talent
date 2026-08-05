# 검증 기록 (VERIFICATION)

검증 일시: 2026-07-10 / 환경: macOS(Apple Silicon), Python 3 표준 라이브러리만 사용, 외부 API 없음.
아래 결과는 전부 이 저장소의 예시 데이터로 실제 실행해 얻은 값입니다.

## 1. 정상 경로: 입력에서 결과까지

```bash
python3 src/tools/clone_risk.py \
  --products src/examples/products.csv --rankings src/examples/rankings.csv \
  --reviews src/examples/reviews.csv --request src/examples/user_request.json \
  --out-dir src/outputs
python3 src/tools/outfit_report.py \
  --products src/examples/products.csv --scores src/outputs/clone_risk_scores.csv \
  --request src/examples/user_request.json --out-dir src/outputs
```

입력 조건: 예산 200,000원, 회피 요소 4개(musinsa smell, black wide pants, oversized graphic t-shirt, german army sneakers), divergence_level `safe-but-different`.

관찰된 결과:

| 항목 | 실측값 |
| --- | --- |
| 채점 상품 수 | 22개, 점수 범위 0~100 유지 |
| 최고 위험 | P001 Essential Black Wide Slacks = 100점 (top-10 랭킹 + 회피어 `black wide pants` 충돌) |
| 최저 위험 | P014 Taupe Pleated Shorts = 0점 (린넨 소재, 톤 다운 색상, 낮은 랭킹) |
| 최종 추천 | P013 네이비 럭비 티(22점) + P016 올리브 립스탑 쇼츠(23점) + P007 브라운 덱슈즈(3점) |
| 예산 확인 | 합계 199,000원 ≤ 200,000원, `budget_ok: true` |
| 추천 평균 위험도 | 16.0/100 (전체 평균 40.6 대비 하락) |
| 회피 충돌 | 추천 3개 상품 모두 `avoid_conflict` 없음 |

산출물 3종(`clone_risk_scores.csv`, `recommendation.json`, `musinsa_smell_removal_report.md`) 생성 확인. 리포트 끝의 Human Review Notes에 "휴리스틱 로컬 채점이며 실시간 트렌드 데이터가 아니다"라는 한계가 명시됩니다.

## 2. 예외 경로

| 시나리오 | 명령 조건 | 관찰된 동작 |
| --- | --- | --- |
| 예산 부족 | `budget_krw`를 10,000으로 축소 | 크래시 없이 종료, 추천 0개 반환. 없는 상품을 지어내지 않음 |
| 전체 회피 | 색상·실루엣·스타일 12개를 모두 회피어로 지정 | 크래시 없이 종료, 추천 0개 반환 |

## 3. 자동 테스트

```bash
python3 -m unittest discover src/tests
```

4개 테스트 통과 (Ran 4 tests, OK):

- Clone Risk Score가 항상 0~100 범위인지
- 회피 키워드 충돌 상품의 위험도가 실제로 더 높게 나오는지
- `clone_risk_scores.csv`가 생성되는지
- 추천 결과에 직접 회피 키워드 충돌이 없는지

## 4. 발견했지만 아직 고치지 않은 점

- 추천이 0개일 때 `recommendation.json`에 "조건을 완화하라" 같은 안내 문구가 없습니다. `budget_ok: true`에 빈 `items`만 반환되므로, 빈 추천의 이유는 사람이 입력 조건을 보고 판단해야 합니다.
- 실시간 판매량, 재고, 시즌 트렌드는 미반영이며 로컬 샘플 데이터 기준입니다.
