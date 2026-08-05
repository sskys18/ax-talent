# 검증 기록 (VERIFICATION)

검증 일시: 2026-07-10 / 환경: macOS(Apple Silicon), Python 3 표준 라이브러리만 사용, 외부 API 없음.
아래 결과는 전부 이 저장소의 예시 데이터로 실제 실행해 얻은 값입니다.

## 1. 정상 경로: 입력에서 결과까지

```bash
python3 src/tools/doc_matcher.py \
  --requests src/examples/pbc_requests.csv --evidence src/examples/evidence_manifest.csv \
  --trial-balance src/examples/trial_balance.csv \
  --out src/outputs/submission_package_manifest.json
python3 src/tools/report_writer.py \
  --manifest src/outputs/submission_package_manifest.json --out-dir src/outputs
```

관찰된 결과: 요청 5건이 상태 4종으로 전부 분기되어 재현됩니다.

| 요청 | 상태 | 근거 (실측) |
| --- | --- | --- |
| AR-03 | Ready | 필수 컬럼·연결 키·기간·법인 모두 일치, 이슈 0건 |
| CUT-01 | Partially ready | 계약 증빙이 기준일 2026-03-31이 아닌 2026-02-28까지만 커버(partial_period_mismatch) + contract_id 연결 키 누락 |
| JE-02 | Needs human review | 승인 로그가 placeholder 파일(weak_source) + 승인 상태 'pending'(missing_approval) + reviewer/approval_date 키 누락 |
| INV-04 | Partially ready | 평가충당금 계산 근거 문서 자체가 없음(missing_document) + nrv/allowance_amount 키 누락 |
| RP-05 | Missing | 증빙이 요청 법인 'ACME Korea Co.'가 아닌 'ACME US Inc.' 소속(entity_mismatch) |

산출물 4종(`submission_package_manifest.json` + Markdown 리포트 3종) 생성 확인. `missing_items.md`에 누락/약한/애매 증빙이 사유별로 정리되고, `followup_email_draft.md`에 후속 요청 초안이 생성됩니다.

## 2. 예외 경로

| 시나리오 | 명령 조건 | 관찰된 동작 |
| --- | --- | --- |
| 선택 입력 생략 | `--trial-balance` 없이 실행 | 크래시 없이 동일한 상태 분포(Ready 1, Partially ready 2, Needs human review 1, Missing 1) |
| 증빙 전무 | 헤더만 있는 빈 evidence manifest | 5건 전부 Missing으로 보수적으로 처리, 없는 증빙을 지어내지 않음 |

## 3. 자동 테스트

```bash
python3 -m unittest discover src/tests
```

11개 테스트 통과 (Ran 11 tests, OK):

- 요청 5건이 모두 manifest에 포함되는지
- AR 요청에 필수 연결 키가 포함되는지
- missing_document / missing_required_columns 이슈가 검출되는지
- Ready, Partially ready, Missing/Needs human review가 각각 1건 이상 존재하는지
- Markdown 산출물 3종이 생성되는지

## 4. 테스트하며 고친 점 / 아직 남은 한계

- 개발 중 산출물 JSON에 로컬 절대경로가 직렬화되는 문제를 발견해 프로젝트 상대경로 직렬화로 수정했습니다.
- Ready는 감사 결론이 아니라 "샘플 manifest 기준 명백한 누락 신호 없음"입니다. 실제 문서 원문의 충분성·적합성 판단은 사람 몫입니다.
