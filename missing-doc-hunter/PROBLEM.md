# PROBLEM.md - missing-doc-hunter

> AX 해커톤 예선 요건: 참여 기업 또는 그 기업의 산업·고객이 겪는 **공개·검증 가능한 문제**를 입증하고, 이를 해결하는 Codex 플러그인을 제출한다.

## 0. 대상과 비공식 고지

- 대상 기업: **삼일PwC (Samil PwC)**
- 축: 삼일PwC가 속한 **회계감사·세무·자문 산업**과 그 고객이 겪는 PBC(Prepared By Client) 증빙 왕복 문제
- 비공식 고지: 이 플러그인은 해커톤용 독립 프로토타입이며, 삼일PwC 또는 PwC의 공식 제품·제휴·도입 사례가 아니다. 모든 입력 데이터는 로컬 샘플이다.

## 1. 문제 한 줄

감사·세무·자문 업무에서 고객이 PBC 자료를 업로드해도, 실무팀은 여전히 그 자료가 **충분하고 적합한 증거인지**, 기간·법인·승인·연결 키가 맞는지 직접 확인해야 한다. 이 확인이 늦어지면 고객에게 같은 자료를 다시 요청하고, 제출 패키지 준비가 지연된다.

## 2. 왜 공개적으로 입증 가능한 문제인가

| # | 근거 | 발행처 | 이 출처가 입증하는 것 | URL |
|---|------|--------|-----------------------|-----|
| E1 | 주요 회계법인의 AI 감사·세무 적용 보도 | 디지털데일리 | 삼일PwC·삼정KPMG·EY한영 등 주요 회계법인이 감사·세무·내부통제 업무에 AI를 적용하고, 반복적인 데이터 정합성 점검·조서화 자동화와 휴먼-인-더-루프 검증을 강조함 | https://m.ddaily.co.kr/page/view/2026051115581496536 |
| E2 | 감사증거의 충분성·적합성 기준 | FRC ISA (UK) 500 | 감사증거는 감사인이 결론을 내리는 기반이며, 충분하고 적합해야 한다는 감사기준상 핵심 원칙 | https://www.frc.org.uk/library/standards-codes-policy/audit-assurance-and-ethics/auditing-standards/isa-uk-500/ |
| E3 | 국내 회계감사기준 원문 목록 | 금융감독원 | 국내 감사기준서가 공식 공개되어 있고 감사증거·감사문서화 판단이 규범화되어 있음을 확인 | https://fss.or.kr/fss/bbs/B0000129/list.do?menuNo=200437 |
| E4 | 심사·감리 지적사례 공식 목록 | 금융감독원 | 회계심사·감리 지적사례가 지속적으로 공개되며, 기업·감사인이 결산·감사 업무에 참고해야 하는 실제 리스크임 | https://fss.or.kr/fss/bbs/B0000135/list.do?menuNo=200448 |
| E5 | PwC Connect 로그인/요청 포털 | PwC | PwC가 고객 요청과 자료 관리를 위한 Connect 플랫폼을 운영한다는 공개 확인. PBC 요청 관리가 별도 업무·도구 영역임을 보여줌 | https://connect.pwc.com/ |
| E6 | PBC 요청관리 상용 제품 | AuditDashboard | Audit, tax, cyber security engagements에서 PBC(Provided by Client) 요청·협업 관리가 복잡한 전용 업무 영역임을 보여줌 | https://www.auditdashboard.com/ |
| E7 | 회계심사·감리 주요 지적사례 보도 | 이데일리 | 금감원이 회계심사·감리 주요 지적사례를 공개해 기업과 감사인이 결산·감사 업무에 참고하도록 한다는 점 | https://www.edaily.co.kr/News/Read?newsId=01587526645486312 |

## 3. 문제에서 플러그인 기능으로의 매핑

| 공개 근거가 보여주는 문제 | 플러그인 기능 | 산출물 |
|---|---|---|
| 감사증거는 충분하고 적합해야 함 (E2, E3) | PBC 요청을 유형별 required evidence와 linking keys로 분해 | `submission_package_manifest.json` |
| 고객 요청·자료 관리가 별도 도구 영역으로 존재 (E5, E6) | PBC request list와 evidence manifest를 자동 대조 | manifest + report |
| 자료가 있어도 기간·법인·컬럼·승인 문제로 재요청 가능 | `partial_period_mismatch`, `entity_mismatch`, `missing_required_columns`, `missing_approval`, `weak_source` 탐지 | `missing_items.md` |
| 감리 지적사례가 반복적으로 공개됨 (E4, E7) | 누락·불충분 항목을 보수적으로 표시하고 후속 요청 초안을 생성 | `followup_email_draft.md` |
| AI 감사 활용은 휴먼-인-더-루프가 필요함 (E1) | 애매하면 `Needs human review`; 증빙을 지어내지 않고 자동 감사 결론을 내리지 않음 | 전체 |

## 4. 이 플러그인이 메우는 갭

PBC 포털은 보통 **자료 요청과 수령 상태**를 관리한다. 그러나 받은 자료가 요청 목적에 충분한지, 필요한 연결 키가 있는지, 기간·법인이 맞는지, 승인 로그가 있는지는 여전히 사람이 확인한다. `missing-doc-hunter`는 이 중간 단계에서 manifest 기반으로 명백한 누락·불일치를 먼저 띄워, 전문 인력이 원문 검토에 들어가기 전에 재요청 항목을 정리하도록 돕는다.

## 5. 한계

- 메타데이터 기반 휴리스틱 매칭이며 PDF/XLSX 원문 내용이나 숫자를 검증하지 않는다.
- `Ready`는 감사 결론이 아니라 샘플 manifest 기준으로 명백한 누락 신호가 없다는 뜻이다.
- 최종 증거 충분성 판단은 반드시 전문가가 수행해야 한다.
- 이 플러그인은 삼일PwC 또는 PwC의 공식 도구가 아니다.
