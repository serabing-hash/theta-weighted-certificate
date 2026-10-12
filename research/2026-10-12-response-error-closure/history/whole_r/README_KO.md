# 전체 R shared-jet 통합 구현 — 실제 수치는 HOLD

전체 R을 같은 geometry/M/c0/Fhat/E/Gamma 버퍼로 계산하는 코드와 독립 중심 재생을 구현했다. 원본 supervisor 대신 별도 fail-closed 래퍼도 구현했다. 최종 source-free 검사 27개가 통과했다. 실제 중심값 생성·실제 수학 replay·production child는 실행하지 않았다. 숫자 실험 횟수는 11 그대로다.

이 결과는 실행 허가된 production 준비 완료를 뜻하지 않는다. 실제 새 R/H/chi/중심 이동과 14항 예산은 아직 미평가이며, 값 대신 null로 저장했다. `1.25231e−26`은 이전 response-only 부분 예산이다. 전체 R 반경으로 제출하면 실제 거부한다. 이전 response를 전부 제거해도 저장된 잔여 반경은 이전 중심의 395.149054943배다.

## 실제 추가한 코드

- `center_replay.py`: 생성기의 monomial 방식과 다른 normalized-derivative recurrence로 중심 jet를 포함 검증한다.
- `whole_r.py`: 전체 chi/Ag를 먼저 적분하고, 그 새 전체 chi와 residual `g−Mc0` response를 같은 stream에서 결합한다. 모든 cell과 endpoint, 전체 Gamma 및 prime edge, σℓ cross와 ℓ²를 포함한다. 두 pass의 buffer SHA와 header SHA를 고정한다. 필수 error ledger의 지급합이 정확히 새 R 반경과 일치해야 한다. midpoint 이동은 이전 중심 기준 감사 반경에 포함한다.
- `real_adapter.py`: 기존 원본 입력의 geometry·source·c0·endpoint와 SHA를 확인하는 reader, 실제 center materializer, 전체 verifier가 함수로 구현되어 있다. materializer와 실제 replay는 현재 stage에서 차단된다. 240-place outward serialization과 row/file 크기 제한도 구현했다.
- `safe_wrapper.py`, `resource_common.py`, `watchdog.py`: 실제 inherited 한도를 min으로 유지하거나 낮추고 CPU/AS를 readback한다. exec 전후 counter delta를 구분하고 descendant를 종료·wait한다. 현재 실제 command를 실행할 경로는 허용하지 않는다.
- `pipeline_fixture.py`, `test_whole_r.py`, `test_wrapper.py`: 원본 수학 입력을 사용하지 않는 완전한 세 component fixture와 포함/거부/자원 고장 검사를 제공한다.

수학 포함 관계는 `PROOF_KO.md`, 자원 래퍼의 실제 계약과 남은 한계는 `RESOURCE_WRAPPER_KO.md`에 적었다. 초기 회귀 실패와 중간 PASS는 `regressions/`에 모두 보존했다. 초기 실패를 성공 기록으로 덮어쓰지 않았다.

## 현재 실행된 차단 확인

`probe_readiness.py`는 각 조건을 별도 source-free process에서 검사하고 exit code 1을 반환했다. 상세 raw receipt는 `evidence/PROBE_*.json`에 있다.

| 검사 | 실제 첫 실패 |
|---|---|
| 실제 whole-R verifier 진입 | `ACTUAL_CENTER_JET_STREAM_MISSING: CENTER_JET_CELLS.jsonl` |
| 실제 center materializer 진입 | `CURRENT_STAGE_FORBIDS_NEW_ACTUAL_CENTER_SOURCE_EVALUATION` |
| `1.25231e−26`을 전체 R로 제출 | `partial budget promoted to full R radius` |
| global chi 예산을 0으로 제출 | `underpaid whole-R term global_chi_all_errors` |
| 이전 chi hash 사용 | `residual used stale chi packet` |

합성 whole-R 결과는 `evidence/SYNTHETIC_WHOLE_R_INCLUSION.json`에 있다. 이 파일의 수치는 합성 입력에만 해당한다. 실제의 새 전체 R 수치로 사용할 수 없다.

## 실제 재개 전에 남은 구현·증거

1. 실제 center stream은 없다. 현 단계에서 생성 금지이므로 만들지 않았다. 별도 허가된 한 번의 실행에서 4,416 cell / 19,136 정점의 Fhat degree32..128 및 low16 degree0..30, order16 중심 모델을 생성하고 독립 재생해야 한다. 생성기와 첫 verifier는 실제 중심 source를 각각 평가한다. 두 번째 적분 pass는 동일 stream hash를 검증하고 중심 source를 다시 평가하지 않는다. 전체 Gamma box를 재사용하므로 Gamma/prime/θ의 신규 평가는 요구하지 않는다.
2. 현재 래퍼는 source-free fixture command만 허용한다. 실제 materializer→whole-R verifier를 한 bounded worker에 연결하고 한 번의 attempt와 종료/중단 receipt를 기록하는 production command bridge가 아직 구현되지 않았다. 과거 supervisor 및 lease를 재사용하여 이 공백을 메우지 않는다.
3. 실제 전 구간의 exact rational 중심 생성, 독립 재생과 두-pass 통합을 inherited 한도 안에서 wall/tree CPU 600초 내 완료할 performance·크기 증거가 없다. 새 row/file cap은 존재하지만 실제 input에서 측정하지 않았다. 한도가 부족하면 올리지 않고 HOLD해야 한다.
4. 세 정상 process의 AS hard 합은 기본 464 MiB 이하이다. 예상 밖 fork를 감지·정리하는 fixture는 통과했지만, fork 발생 직후 polling 전의 instantaneous aggregate memory를 강제 제한하는 OS 증명은 없다. 고정 실제 worker/import의 무자식 실행을 증명하거나 기존 허용 containment를 확인해야 한다. 현재 security/network 설정을 바꾸지 않았다.
5. 원본 해석적 coercivity·Gamma·domain/source 전제는 그대로 조건부이다. 새로운 실제 전 구간 packet에서 항별 전체 지급·중심 이동·R의 부호 분리를 확인해야 한다. 이 구현이 부호 분리나 개선된 전체 반경을 보장하지 않는다. 새 s0/Psi/RH/GO 주장은 없다.

최소 single-run 요구 사항은 `SINGLE_RUN_CONTRACT.json`에 저장했다. 실행 승인 요청이나 재개 명령이 아니다. `CURRENT_STAGE.json`의 실제 source 및 production 플래그는 false다. 이 작업은 사용자 PC, Ultra, 업로드, 네트워크 허용 목록 변경, 새 lease 또는 원본 파일 편집을 사용하지 않았다.

## 증거와 보존

최종 검사: `evidence/TEST_RECEIPT.json`, `evidence/TESTS.log`. 자원 fixture의 원시 receipt/readback/종료 기록은 `fixtures/`에 있다. 저장된 기존 예산과 실제 미평가 항은 `evidence/SAVED_ANALYSIS.json`에 있다. 보호 대상 1,967개 원본(39 ZIP, 1 lease)의 최종 SHA/크기/mtime 검사는 `evidence/POST_TASK_PRESERVATION.json`에서 확인한다. 저장소 HEAD는 `f925567236f251072fad2ddd0522e4081352e97b`이며 저장소 내 파일을 수정하지 않았다.
