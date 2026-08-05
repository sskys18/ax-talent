# musinsa-smell-remover

`musinsa-smell-remover`는 로컬 CSV/JSON 데이터를 읽어 무신사처럼 랭킹 영향력이 큰 패션 플랫폼에서 생길 수 있는 **클론룩 위험(추천 다양성 저하)**을 계산하고, 스타일 콘텐츠/MD 검토용 대안 코디를 Markdown, JSON, CSV로 생성하는 Codex 워크플로우 플러그인입니다.

> **공개·검증 가능한 문제 입증은 [`PROBLEM.md`](./PROBLEM.md) 참조** (무신사 최근 실적,
> 패션 플랫폼 지배력, 클론룩/추천 다양성 현상 출처 인용). AX 해커톤 예선의 "문제 입증" 요건 대응.
> 비공식 고지: 이 플러그인은 해커톤용 독립 프로토타입이며, 무신사의 공식 제품·제휴·도입 사례가 아닙니다. 모든 데이터는 로컬 샘플입니다.

## 플러그인 개요

- 플러그인 이름: `musinsa-smell-remover`
- 목적: 상품, 랭킹, 리뷰, 사용자 요청 데이터를 기반으로 Clone Risk Score를 산출하고 예산 안에서 안전하지만 덜 흔한 스타일 콘텐츠 후보를 추천합니다.
- 실행 방식: 외부 API나 pandas 없이 Python 표준 라이브러리만 사용합니다.

## 문제 정의

"무신사 냄새"라는 표현은 개인 취향이나 브랜드를 비난하는 표현으로 쓰지 않습니다. 이 프로젝트에서는 이를 랭킹·인기 품목 중심 소비에서 생기는 **클론룩 위험과 추천 다양성 저하**로 재정의합니다. 플러그인은 인기 랭킹, 리뷰의 흔함 신호, 색상, 실루엣, 소재, 사용자가 피하고 싶은 요소를 함께 보고 위험도를 계산합니다.

## 누가 사용하는가

- 무신사 같은 패션 플랫폼의 상품 MD, 스타일 에디터, 추천 실험 담당자
- 랭킹 상위 상품 위주의 콘텐츠가 너무 비슷해지는지 검토하려는 리서처
- 쇼핑 앱이 아니라 재현 가능한 스타일 다양성 워크플로우 출력물이 필요한 사람

## 왜 "Clone-look Risk"로 표현하는가

표현 자체는 주관적이고 공격적으로 들릴 수 있습니다. 그래서 이 프로젝트에서는 이를 "흔한 조합에 과도하게 가까운 정도"로 재정의합니다. 점수는 상품의 좋고 나쁨이 아니라, 현재 데이터 안에서 얼마나 클론룩으로 보일 가능성이 높은지를 나타냅니다.

## 파일 구조

```text
musinsa-smell-remover/
├── src/
│   ├── .codex-plugin/
│   │   └── plugin.json
│   ├── skills/
│   │   └── musinsa-smell-remover/
│   │       └── SKILL.md
│   ├── tools/
│   │   ├── clone_risk.py
│   │   └── outfit_report.py
│   ├── examples/
│   │   ├── products.csv
│   │   ├── rankings.csv
│   │   ├── reviews.csv
│   │   └── user_request.json
│   ├── outputs/
│   │   └── .gitkeep
│   └── tests/
│       └── test_clone_risk.py
├── README.md
└── logs/
    └── README.md
```

## 실행 방법

프로젝트 루트에서 다음 명령을 실행합니다.

```bash
python src/tools/clone_risk.py \
  --products src/examples/products.csv \
  --rankings src/examples/rankings.csv \
  --reviews src/examples/reviews.csv \
  --request src/examples/user_request.json \
  --out-dir src/outputs

python src/tools/outfit_report.py \
  --products src/examples/products.csv \
  --scores src/outputs/clone_risk_scores.csv \
  --request src/examples/user_request.json \
  --out-dir src/outputs

python -m unittest discover src/tests
```

## 예시 명령

```bash
cd musinsa-smell-remover
python src/tools/clone_risk.py --products src/examples/products.csv --rankings src/examples/rankings.csv --reviews src/examples/reviews.csv --request src/examples/user_request.json --out-dir src/outputs
python src/tools/outfit_report.py --products src/examples/products.csv --scores src/outputs/clone_risk_scores.csv --request src/examples/user_request.json --out-dir src/outputs
python -m unittest discover src/tests
```

## 생성되는 출력

- `src/outputs/clone_risk_scores.csv`: 상품별 Clone Risk Score와 점수 이유
- `src/outputs/recommendation.json`: 추천 코디의 기계 판독용 결과
- `src/outputs/musinsa_smell_removal_report.md`: 사용자 요청, 회피 요소, 추천 코디, 예산 확인, 검토 노트가 포함된 보고서

## 검증 방법

> 실측 검증 결과(정상 경로 실측값, 예외 경로 재현 명령, 테스트 결과, 남은 한계)는 [`VERIFICATION.md`](./VERIFICATION.md)에 정리되어 있습니다.

`unittest` 테스트는 다음을 확인합니다.

- Clone Risk Score가 항상 0부터 100 사이인지
- 회피 키워드와 직접 충돌하는 상품의 위험도가 더 높게 계산되는지
- `clone_risk_scores.csv`가 생성되는지
- `recommendation.json`이 생성되는지
- 추천 상품에 직접 회피 키워드 충돌이 없는지

## 한계와 Human Review Notes

- 이 도구는 로컬 예시 데이터 기반 휴리스틱 모델입니다.
- 실시간 판매량, 재고, 계절별 급상승 트렌드, 실제 착용감은 반영하지 않습니다.
- 추천 결과는 사람의 최종 검토가 필요합니다.
- 사용자의 기존 옷장과 신체 선호, 정확한 사이즈, 실제 판매 가능 여부는 별도로 확인해야 합니다.

## 로그 제출 안내

`logs/` 폴더에는 제출용 실제 AI 대화 로그가 포함되어 있습니다: `ai-conversation-chatgpt-share.txt`, `chatgpt-share-url.txt`, `LOG_SOURCE.md`, `README.md`. 동일한 공유 ChatGPT 대화가 세 플러그인 제작·검토 과정을 모두 포함하므로 각 독립 제출물에 같은 전체 대화 로그를 포함합니다. 가짜 로그는 생성하지 않습니다.
