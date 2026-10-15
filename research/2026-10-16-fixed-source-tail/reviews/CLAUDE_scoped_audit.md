# Claude scoped scientific audit (curated excerpt)

The following is a mathematical excerpt from the completed review, not a browser transcript or an independent full certificate rerun. Sections 2-6 are retained, excluding an unsupported approximate comparison and unrelated bookkeeping. Private execution paths and account/session information are omitted. The forward-looking response section is not included and is not adopted.

The reviewer reported conditional PASS for source binding, PASS for interval implementation, and PASS for the narrow bound-only scope. A short exact-rational script ran once under a 120-second timeout and a 512 MiB address-space limit; 14 checks were true. A preceding timing-wrapper attempt failed before Python started. The reported wall time was 0.089 seconds; peak memory was not measured. The publication process has not rerun this script or the full source certificate.

The recovered code is checks/claude_source_tail_sanity_run.py, SHA-256 4a91b6276d309b130f55cf85343e830df9a1fb7f5fcff11de82f3f0bf2b50392, matching the reviewer-displayed executed-code hash. checks/claude_source_tail_sanity_out.json is the exact JSON extracted from the visible command output; it is not claimed to have the original saved-output file's hash. Its display-only approximate numbers are not interval endpoints and must not replace source_tail_M128/run/result.json. The complete exact ratio is also checked by the separate saved-output checker. A safe short display is y_cert/Y_crude < 3.73e-10.

## 2. 해석적 source binding: 조건부 PASS

- **(1) 정규화와 구조**
  - dx=Bdt, E0, e_m 정규화와 W 쪽 계수(1/8, −√(2m+1)/4, 추가 √2 없음)가 일관됩니다.
  - h_A는 하나로 고정되어 끝까지 유지됩니다.
  - h_A, W, 대칭 shift 합이 모두 짝이므로 F도 짝입니다. 그래서 0:2:128의 65개 모드 Parseval 차분이 정확한 T-꼬리를 줍니다.
  - TΠ_X = T입니다.
  - old Y0와 혼동한 곳은 없습니다. Y0는 Ycrude 전제에서만 쓰입니다.
- **(2) kernel**
  - k(s)=e^{−s/2}/(1−e^{−2s}) − 1/(2s) = ¼[csch u − 1/u + sech u] (u=s/2)를 손으로 확인했습니다.
  - K_k h = ∫k(|x−y|)h(y)dy입니다. 홀수 차수(≤95) 항은 y=x에서 나눠 적분하므로 출력 차수가 ≤ 95+28+1 = 124이고 짝입니다. 따라서 T K_k96 h_A = 0입니다.
  - 실제 K_k의 꼬리는 0으로 두지 않고 ‖K_k − K_k96‖ ≤ (3/2)Ek로 지불합니다. 근거는 A=sinh u/u ≥ 1, C=cosh u ≥ 1인 product remainder와, 길이 3/2 구간에서의 Schur 판정입니다. 각 항이 u에 대해 증가하므로 sup은 u=3/4에서 취해지며, 이것도 성립합니다.
- **pole 항**
  - th는 degree-30 cosh 전체 잔차입니다. ‖T·2M(h)cosh(x/2)‖ ≤ 3cosh(3/8)·th·‖h‖ ≤ (9/2)th‖h‖이고, 한 번만 지불됩니다.
- **(3) shift 항**
  - Beta 모멘트(E0[W]=1−log2로 대조)를 확인했습니다.
  - branch 6개와 순서쌍 36개(비순서 21개 × 중복도)를 확인했습니다.
  - n=2의 두 branch는 (−0.0758, 0.0758)에서 겹치며, 이 cross 항도 포함되어 있습니다.
  - log4 = 2log2를 같은 L2 box로 묶어 처리합니다.
  - 끝점 비교가 애매하면 ArithmeticHold로 멈춥니다.
- **조건:**
  - Y_actual = Π_X[W_B h − K_k h + 2M(h)cosh − Σc_n S_n h]가 원천 연산자의 올바른 정의라는 점은 이번 감사의 범위 밖이며 계승된 전제입니다.

## 3. Interval implementation: PASS

- 10^-120 정수 격자에서 lo는 floor, hi는 ceil입니다.
  - Python `//`는 음수에서도 floor이므로 맞습니다. `ceildiv` = −((−a)//b), b>0도 맞습니다.
- 곱셈은 네 끝점 곱의 min/max를 바깥쪽으로 반올림합니다. 나눗셈은 부호가 바뀌는 경우를 처리합니다.
- 제곱은 구간이 0을 지나면 하계를 0으로 둡니다. sqrt는 isqrt 하계와 +1 상계를 씁니다.
- 꼬리 제곱 상계는 U = N^up − P^low이고 clamping이 없습니다. 음수일 경우 assert로 멈추므로 하계를 상계처럼 쓰는 경로가 없습니다.
- 소거 손실은 구간 폭이 덮습니다. 폭은 ~1e-65(W 부분)와 ~1e-53(S 부분)이고, 꼬리 제곱은 2.7e-25와 6.4e-23입니다.
- ycert = yW + yS + yrem은 삼각부등식으로 합친 보수적 상계입니다. cross 항 상쇄는 이용하지 않습니다.

## 4. 결과 scope: PASS (좁은 범위로만)

- ycert singleton은 안전한 상계 상수입니다. 하계나 양면 enclosure가 아닙니다.
- ratio는 ycert.hi / crude.lo로, 방향이 맞습니다. 다만 두 상계를 비교한 것이지 실제 ‖Y‖ 대비 비율이 아닙니다.
- **표시 정밀도 주의:**
  - 표시값끼리 나누면 3.72545059024758659584e-10이 나와 주장값보다 약 4.3e-30 큽니다.
  - 원인은 Ycrude 표시가 내림되어 있기 때문입니다(실제 ≥ 0.022782392677405310185264).
  - 이를 보정한 제 손계산은 주장값과 마지막 자리에서 일치합니다. 기계 검산은 하지 않았습니다.
  - 20자리째는 result.json의 정확 끝점에 달려 있습니다. 표시값만 보고 인용한다면 ≤ 3.7254505902475865959e-10 또는 ≤ 3.73e-10을 권합니다.
- **(6) 자원 상한:**
  - 코드에 설정된 상한(내부 290s, 외부 295s + kill-after 1s, AS 768MiB, symbolic 8192bit)은 정적으로 확인했습니다.
  - 실제 실행 지표(1.892281s, 13568KiB, 976356 ops)와 manifest 해시는 로그와 사용자 보고에 의존하며, 제가 검증한 것은 아닙니다.

## 5. 운영 결함 (수학 결함 아님)

- **위치:** certify_tail.py의 main 흐름입니다.
  - OUT 할당과 mkdir가 `ATTEMPT_STARTED`를 `'x'` 모드로 여는 것보다 앞에 있습니다.
  - 재실행 시 FileExistsError가 `except Exception`에 잡힙니다.
  - 이어서 finally가 OUT/result.json을 HOLD로 덮어씁니다.
- **최소 수정(둘 중 하나):**
  - marker를 `'x'`로 연 뒤에 OUT을 할당하고, finally를 `if OUT is not None`으로 보호합니다.
  - 또는 FileExistsError를 별도로 잡아 아무것도 쓰지 않고 종료합니다.
- 현재 COMPLETE 결과는 재실행만 하지 않으면 유효합니다.

## 6. 인용 가능한 좁은 결론

> 고정된 h_A, B=3/4, low16, M=128에서
> ‖Π_{even,>128} Y_actual‖₂ ≤ 8.4874678247291907546e-12 (norm **상계**)

- 이 결론은 다음에 의존합니다.
  - Y_actual 정의의 원천 바인딩(계승)
  - Max 실행 로그(신뢰)
- 상수 box, Ek, th, H_A는 이번에 독립적으로 확인했습니다.
- Ycrude 대비 ratio는 계승 전제(‖Y0‖ ≤ 28‖h‖, eop)를 받아들였을 때만 의미가 있습니다.
- 이 결론에 포함되지 않는 것: response, Schur 부호, 원래 L의 양성, RH. Schur 부호는 NOT EVALUATED/HOLD입니다.

