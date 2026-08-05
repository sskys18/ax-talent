# missing-doc-hunter

삼일PwC 같은 전문서비스 조직의 회계감사·세무·자문 업무에서 PBC 요청 목록과 로컬 증빙 목록(evidence manifest)을 대조해 **누락되거나 불충분한 증빙**을 찾아내고, 사람 검토용 제출 준비 리포트와 후속 요청 초안을 생성하는 Codex 워크플로우 플러그인입니다.

이것은 웹앱이 아니라 **Codex 워크플로우 플러그인**입니다. Codex가 스킬 정의와 두 개의
표준 라이브러리 파이썬 도구를 실행해 로컬 파일만으로 동작합니다.

> **공개·검증 가능한 문제 입증은 [`PROBLEM.md`](./PROBLEM.md) 참조** (삼일PwC 및 회계감사 산업 AI 적용 보도,
> ISA 500, 금감원 감사기준·감리 지적사례, PwC Connect 등 실제 공개 출처 인용). AX 해커톤 예선의 "문제 입증" 요건 대응.
> 비공식 고지: 이 플러그인은 해커톤용 독립 프로토타입이며, 삼일PwC 또는 PwC의 공식 제품·제휴·도입 사례가 아닙니다. 모든 입력 데이터는 로컬 샘플입니다.

## 문제 정의

회계감사(audit), 세무(tax), 자문(advisory) 업무에서 전문가팀은 고객에게 수많은 증빙을
요청합니다. 그런데 실제 현장에서 시간을 가장 많이 잡아먹는 일은 분석이 아니라 **증빙
왕복(back-and-forth)** 입니다.

- 고객이 파일을 보냈지만 기간이 맞지 않음
- 파일 이름은 그럴듯한데 필요한 컬럼(연결 키)이 없음
- 승인 로그가 없거나 플레이스홀더만 있음
- 엉뚱한 법인(entity)의 자료가 섞여 있음
- 일부 계약서만 오고 나머지는 "곧 보낼게요" 상태

이런 문제를 사람이 눈으로 하나씩 확인하다 보면 제출 마감이 늦어집니다.
missing-doc-hunter는 이 왕복을 줄이는 데 초점을 맞춥니다.

## PBC의 의미

**PBC = Prepared By Client** (고객이 준비하는 자료). PBC 요청 목록은 전문가팀이 고객에게
"이 자료들을 준비해 주세요"라고 요청하는 리스트입니다.

## 사용 대상

- 삼일PwC 같은 회계법인 / 세무법인 / 자문팀의 감사·세무·자문 실무자
- 제출 패키지(submission package)를 마감 전에 점검해야 하는 매니저
- 고객 측 자료 담당자에게 명확한 후속 요청을 보내야 하는 팀

## 이 니치 문제가 중요한 이유

이건 회계 Q&A 챗봇도, CFO 대시보드도, 범용 문서 검색기도 아닙니다.
"자료가 준비됐는가?"라는 아주 좁지만 반복적이고 비용이 큰 **사람 검토 전 스크리닝**을 자동화합니다.
증빙 왕복 한 사이클을 줄이는 것만으로도 실무 시간과 고객 커뮤니케이션 부담이 줄어듭니다.

## 이름이 missing-doc-hunter인 이유

핵심 동작이 "제출에 필요한데 **없거나 부족한 문서를 사냥(hunt)** 하는 것"이기 때문입니다.
있는 것을 요약하는 도구가 아니라, **빠진 것과 약한 것을 찾아내는 도구**입니다.

## 동작 방식

1. PBC 요청 목록을 읽습니다.
2. 각 요청의 목적을 추론합니다.
3. 요청을 필요한 증빙 항목으로 분해합니다.
4. 필요한 연결 키(linking keys)를 식별합니다.
5. evidence manifest에서 가용 파일을 매칭합니다.
6. 누락/약함/불일치/불완전 문서를 탐지합니다.
7. 각 요청을 다음 4가지로 분류합니다.
   - **Ready** (샘플 manifest 기준 명백한 누락 신호 없음)
   - **Partially ready** (부분 준비)
   - **Missing** (증빙 없음)
   - **Needs human review** (사람 검토 필요)
8. 문제와 다음 조치를 설명합니다.
9. 누락·불충분 증빙에 대한 후속 요청 초안을 생성합니다.

### 보수적 원칙 (중요)

- 애매하면 무조건 **Needs human review**로 표시합니다.
- 증빙을 **절대 지어내지 않습니다.**
- 없는 문서가 있다고 **가정하지 않습니다.**
- **Ready는 감사 결론이 아닙니다.** 최종 증거 충분성 판단은 반드시 전문가가 수행해야 합니다.
- 플레이스홀더, 약한 출처, 빈 파일은 증빙으로 인정하지 않습니다.

### 요청 유형과 필요한 연결 키

| 유형 | 필요한 연결 키 |
| --- | --- |
| receivables (채권) | customer_id, invoice_id, due_date, amount, receipt_date |
| cutoff (기간귀속) | invoice_id, contract_id, shipment_date, revenue_recognition_date |
| journal entry (수정분개) | journal_id, preparer, reviewer, approval_date |
| inventory (재고) | item_id, aging_days, nrv, allowance_amount |
| related party (특수관계자) | counterparty, contract_id, transaction_amount, terms |

### 탐지하는 이슈 유형

`missing_document`, `partial_period_mismatch`, `entity_mismatch`,
`missing_required_columns`, `missing_approval`, `weak_source`, `needs_manual_judgment`

## 파일 구조

```
.
├── src/
│   ├── .codex-plugin/
│   │   └── plugin.json                 # Codex 플러그인 매니페스트
│   ├── skills/
│   │   └── missing-doc-hunter/
│   │       └── SKILL.md                # Codex 스킬 정의
│   ├── tools/
│   │   ├── doc_matcher.py              # 요청↔증빙 매칭, JSON 매니페스트 생성
│   │   └── report_writer.py            # Markdown 리포트/이메일 초안 생성
│   ├── examples/
│   │   ├── pbc_requests.csv            # PBC 요청 예시
│   │   ├── evidence_manifest.csv       # 증빙 목록 예시(메타데이터)
│   │   └── trial_balance.csv           # 시산표 예시(선택)
│   ├── outputs/                        # 생성물 출력 위치
│   └── tests/
│       └── test_missing_doc_hunter.py  # unittest
├── README.md
└── logs/
    └── README.md                       # 실제 대화 로그 보관용
```

## 실행 방법

Python 3 표준 라이브러리만 필요합니다(pandas 등 외부 의존성 없음).

```
# 1) 요청과 증빙을 매칭하여 제출 패키지 매니페스트 생성
python src/tools/doc_matcher.py \
  --requests src/examples/pbc_requests.csv \
  --evidence src/examples/evidence_manifest.csv \
  --trial-balance src/examples/trial_balance.csv \
  --out src/outputs/submission_package_manifest.json

# 2) 매니페스트로부터 리포트/이메일 초안 생성
python src/tools/report_writer.py \
  --manifest src/outputs/submission_package_manifest.json \
  --out-dir src/outputs

# 3) 테스트 실행
python -m unittest discover src/tests
```

> 환경에 따라 `python` 대신 `python3`를 사용하세요.

## 생성되는 산출물

- `outputs/submission_package_manifest.json` - 요청별 목적/유형/필요 증빙/필요 키/매칭 파일/누락 항목/이슈/상태/다음 조치
- `outputs/missing_doc_hunter_report.md` - 사람이 읽는 제출 준비 리포트
- `outputs/missing_items.md` - 누락/약함/애매/검토 필요 항목 요약
- `outputs/followup_email_draft.md` - 고객/내부 담당자용 후속 요청 이메일 초안

## 검증 방법

> 실측 검증 결과(정상 경로 실측값, 예외 경로 재현 명령, 테스트 결과, 남은 한계)는 [`VERIFICATION.md`](./VERIFICATION.md)에 정리되어 있습니다.

`src/tests/test_missing_doc_hunter.py`가 다음을 확인합니다.

- 매니페스트 JSON이 생성되는지
- 5개 요청이 모두 포함되는지
- 최소 1건이 Ready(샘플 manifest 기준 명백한 누락 신호 없음)인지
- 최소 1건이 Partially ready인지
- 최소 1건이 Missing 또는 Needs human review인지
- AR 요청에 customer_id, invoice_id, due_date, amount 키가 포함되는지
- 세 개의 Markdown 산출물이 생성되는지
- 매니페스트에 missing_document / missing_required_columns 등 이슈 유형이 포함되는지

예시 데이터 기준 현재 결과: Ready 1 (AR-03, 샘플 manifest 기준 명백한 누락 신호 없음), Partially ready 2 (CUT-01, INV-04),
Needs human review 1 (JE-02), Missing 1 (RP-05).

## 한계 (Limitations)

- 이 도구는 **메타데이터 기반 휴리스틱 매칭**만 수행합니다. 실제 문서 내용을 열어보거나
  숫자를 검증하지 않습니다.
- evidence_manifest.csv는 데모용 메타데이터입니다. 실제 원본 문서를 가짜로 만들지 않습니다.
- 결과를 감사 의견이나 결론으로 사용해서는 안 됩니다.
- `Ready`는 감사 결론이나 증거 충분성 의견이 아니라 샘플 manifest 기준의 사전 스크리닝 상태입니다.
- 키워드/컬럼 명명이 실제 데이터와 다르면 매칭 정확도가 떨어질 수 있습니다.

## 사람 검토 노트 (Human review notes)

- 상태가 **Needs human review**인 항목은 반드시 실무자가 직접 확인해야 합니다.
- 약한 출처(weak_source)나 플레이스홀더는 자동으로 "충분함"으로 승격되지 않습니다.
- 엔티티/기간 불일치는 자동 무시하지 않고 항상 이슈로 남깁니다.

## 로그 안내

`logs/` 폴더에는 제출용 실제 AI 대화 로그가 포함되어 있습니다: `ai-conversation-chatgpt-share.txt`, `chatgpt-share-url.txt`, `LOG_SOURCE.md`, `README.md`. 동일한 공유 ChatGPT 대화가 세 플러그인 제작·검토 과정을 모두 포함하므로 각 독립 제출물에 같은 전체 대화 로그를 포함합니다. 가짜 로그는 생성하지 않습니다.
