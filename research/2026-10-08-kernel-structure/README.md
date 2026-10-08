# 세타 가중 연산자의 무한 커널과 정확한 상수 모드 제거

2026년 10월 8일 UTC · 정적 수학 연구 묶음

같은 최소 폐쇄 연산자 L에서 모든 고정 정수 j≥0에 대해 f_j=κ^(2j)/κ가 D(L)에 속하고 Lf_j=0임을 검사한 논증, 별도의 전체 분석 감사, 정확한 상수 모드 제거 revision 2를 담았습니다. 원본은 바이트 그대로 복사했고, 중복 스냅샷은 SOURCE_IDENTITIES.json에 동등성을 기록해 한 사본으로 통합했습니다.

핵심 결과는 ker L과 ker L∩{1}⊥가 무한차원이라는 것입니다. 유한 차원 제거 및 유한 랭크 W를 추가해도 H_δ=L+δI+WW*에는 δ 고유값이 무한 중복도로 남습니다. 따라서 유효한 전역 coercivity 상수는 η_δ≤δ입니다. 상수 모드 제거의 C=QFQ는 정확한 재표현입니다. 실제 reduced finite-matrix margin은 OPEN이며, 양의 유계 역연산자가 존재할 때 ||S_δ^(-1)||, ||H_δ^(-1)||≥1/δ입니다.

## 읽는 순서

1. AUDIT_README.md: 전제, 새로 확인한 범위와 남은 문제
2. kernel/PROOF.md: 모든 고정 차수의 최소 form 및 operator 정의역 진입
3. independent_audit/REPORT.md: 별도의 전체 분석 감사와 PASS의 정확한 의미
4. deflation/DEFLATION_NOTE_REVISION_2.md: 상수 모드 제거와 실제 무한 커널의 결과
5. bridge/PROOF.md: 동일 연산자와 명시공식의 정확한 연결
6. SOURCE_IDENTITIES.json, ATTRIBUTION.md: 원본 정체성, 중복 대응, 출처와 권리

## 범위

Jacobi theta 및 completed-zeta Mellin 항등식, 고전적 compact-test 명시공식, unconditional zero-strip·zero-counting 사실, 폐쇄 이차형식의 표준 표현정리는 상속된 분석 전제입니다. 역사적 도함수 radicality와 saturation은 이미 알려져 있었고, 원 논문은 j=0,1의 D(L) 진입과 null action을 이미 증명했습니다. 이번 추가 확인은 모든 고정 차수를 같은 최소 D와 D(L)로 확장하는 compact-difference 논증, 독립성 및 그 결과입니다. 전 세계 우선권 주장이 아닙니다.

L≥0, 음의 스펙트럼 배제, RH, 커널의 완전한 기술, growing-degree uniform estimate, 새 수치 enclosure·certificate 또는 계산상 이득은 얻지 않았습니다. 원본 문서의 과거 수치 결과는 재계산·재인증하지 않았습니다. 새 source·phase·H action·FFT·Gram·고유값 계산 및 연구 프로그램 실행은 모두 0건입니다. 파일 복사·해시·ZIP·텍스트 비교만 수행했습니다.

이 묶음의 ‘자체 포함’은 위의 고전적 분석 전제를 명시한 수학 논증과 출처 재구성 범위입니다. 과거 수치 인증을 재실행하는 배포판이나 모든 외부 문헌의 전재본은 아닙니다. 외부 원문은 넣지 않았고, 검증된 원 출처 링크와 필요한 식의 기존 간결한 스냅샷을 유지했습니다.

Astra의 최종 HOLD는 별도 운영 결정 묶음에 있습니다. 이 수학 묶음의 증명·감사 판정에 합치지 않았습니다. frozen request packet과 기존 원본은 수정하지 않았습니다.

## 파일 확인과 권리

이 디렉터리에서 sha256sum -c MANIFEST.sha256로 모든 포함 파일을 확인할 수 있습니다. manifest 자체의 해시와 ZIP 해시는 별도의 전달 검증 기록에 있습니다. 원문의 절대 경로는 출처 식별용이며, 로컬 열람 경로 대응은 SOURCE_IDENTITIES.json을 따르세요. 원문의 오래된 상태 문구와 링크도 변경하지 않았습니다.

새 포장·안내문은 CC BY-NC 4.0입니다. 각 원본의 기존 라이선스와 저작자 표시는 그대로 유지합니다. 별도 라이선스가 없는 과거 원본에 소급 일괄라이선스를 부여하지 않습니다. ATTRIBUTION.md를 확인하세요. 외부 게시·공유·실행은 이번 포장 작업에서 하지 않았습니다.
