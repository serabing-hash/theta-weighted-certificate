**고정 실제 source tail 인증: 단일 실행 COMPLETE, 거친 상계 대비 축소 PASS.**

대상은 제공된 동일한 h_A, B=3/4, low16, M=128이다. 계산으로 인증한 결론은

\[
\|\Pi_{\mathrm{even},>128}Y_{\mathrm{actual}}\|_2
\le 8.4874678247291907546\times10^{-12}.
\]

이는 tail의 상계이다. 실제 tail의 값이나 하계, 전체 source 노름, response quadratic, Schur 부호를 계산한 결과가 아니다.

| 판정 대상 | 판정 | 근거와 한계 |
|---|---|---|
| 해석적 정규화 및 이번 입력 바인딩 | 조건부 PASS | 물리적 정규화, 닫힌 모멘트, 유한 커널 support와 완전 remainder를 재도출했다. H_A, E_k, t_h의 제공 유리수와 정의식의 정확한 일치도 확인했다. 원래 문제에서 이 Y로 넘어오는 식, 상수 outward boxes 및 거친 whole-source bound는 계승 전제다. |
| 실제 유한 산술 인증 | COMPLETE | 한 번 실행, 종료 코드 0. 65개 짝수 모드 및 shift 내부 모든 교차항을 포함했다. |
| 이번 인증상계 대 계승된 거친 상계 | PASS | y_cert의 상단이 Y_crude의 하단보다 작다. |
| response 개선 및 실제 Schur 부호 | NOT EVALUATED / HOLD | Bstar 역, response, Q와의 최종 비교는 실행하지 않았다. |

**실제 결과.** 아래 표는 계산된 각 구간 또는 인증상수를 다시 20 유효숫자로 외향 표시한 것이다. 120자리 격자의 전체 끝점은 run/result.json에 보존되어 있다. 표시된 수를 재차 빼서 원래 정밀도의 차이를 복원하면 안 된다.

| 양 | 인증된 상단 또는 구간 |
|---|---|
| H_A | [6.6203752054526925755e-7, 6.6203752054526925756e-7] |
| N_W | [7.1236509945057163083e-10, 7.1236509945057163084e-10] |
| P_W | [7.1236509945057136397e-10, 7.1236509945057136398e-10] |
| U_W | <= 2.6686604291887776005e-25 |
| y_W | <= 5.1659078865082153152e-13 |
| N_S | [2.4599574992528012545e-7, 2.4599574992528012546e-7] |
| P_S | [2.4599574992528006191e-7, 2.4599574992528006192e-7] |
| U_S | <= 6.3534880724281488177e-23 |
| y_S | <= 7.9708770360783692231e-12 |
| y_rem | <= 2.1032758515993360719e-35 |
| y_cert | [8.4874678247291907545e-12, 8.4874678247291907546e-12] |
| Y_crude | [2.2782392677405310185e-2, 2.2782392677405310186e-2] |
| y_cert / Y_crude | [3.7254505902475865957e-10, 3.7254505902475865958e-10] |

여기서 y_cert는 프로그램이 출력한 인증상수이고 실제 tail 노름과 동일하다고 주장하지 않는다. 비교 대상 Y_crude=(28+e_op)sqrt(H_A)는 계승된 전체 source 상계를 tail에도 적용한 값이다. 이 비교는 기존의 정밀한 tail 알고리즘이나 전체 오차 상계보다 우수하다는 비교가 아니다. 그런 동일조건 전체 비교는 이번 실행에 없다. W와 S 사이 상쇄는 의도적으로 버렸고, S 내부 상쇄와 교차항은 유지했다. 두 성분의 tail 제곱 구간 하단도 양수이며, 음수 상단을 0으로 잘라낸 적은 없다.

**물리적 정규화의 독립 확인.** x=Bt, f(Bt)=u(t)/sqrt(2B)이면 dx=B dt이므로

\[
\|f\|_2^2=\frac12\int_{-1}^1|u(t)|^2dt,
\qquad \langle e_m,f\rangle=\frac{\sqrt{2m+1}}2\int_{-1}^1P_m(t)u(t)dt.
\]

따라서

\[
\|W_Bh_A\|_2^2=\frac18\int_{-1}^1p(t)^2\log^2(1-t^2)dt,
\quad
\langle e_m,W_Bh_A\rangle=-\frac{\sqrt{2m+1}}4\int_{-1}^1P_m(t)p(t)\log(1-t^2)dt.
\]

짝수 m에서 두 shift branch의 적분은 t를 -t로 바꾸면 같아진다. 각 branch의 1/2와 두 branch의 합이 상쇄되어

\[
\langle e_m,S_nh_A\rangle=\sqrt{2m+1}\int_{-1}^{1-\tau_n}P_m(t)p(t+\tau_n)dt.
\]

추가 sqrt(2)는 없다. z는 (1-t^2)^r 좌표로 정확히 전개했다. z_15=0, z_14!=0으로 실제 차수는 28이며, E0[p^2]가 제공된 H_A와 정확히 일치했다.

**W 모멘트의 독립 확인.**

\[
F_k(b)=E_0[t^{2k}(1-t^2)^{b-1}]=\tfrac12\mathrm B(k+\tfrac12,b).
\]

F_k(1)=1/(2k+1), E0[t^(2k)W]=-F'_k(1)/2, E0[t^(2k)W^2]=F''_k(1)/4이다. digamma 차는 -D_k이고 trigamma 차는 4 sum_{j=0}^k(2j+1)^(-2)-pi^2/3이므로 제공된 두 모멘트 식이 그대로 나온다. 사용한 최대 k는 W에서 78, W^2에서 28이다. low 차수에서 분모가 0이 되는 high-only quotient를 사용하지 않았다.

**유한 kernel support와 complete remainder.** u=s/2에 대해

\[
k(s)=\tfrac14\{\operatorname{csch}u-u^{-1}+\operatorname{sech}u\}.
\]

A(u)=sinh(u)/u, C(u)=cosh(u), U^(48)(u)=sum_{n=0}^{48}U_n u^(2n), V^(48)(u)=sum_{n=0}^{48}V_n u^(2n)로 놓는다. 제공된 recurrence는 A U^(48)-1, C V^(48)-1의 96차까지 계수를 소거한다. 예를 들어 첫 곱의 잔차는

\[
\sum_{n=0}^{48}U_nu^{2n}\sum_{j\ge49-n}\frac{u^{2j}}{(2j+1)!}.
\]

A,C>=1이므로 reciprocal 오차는 이 곱 잔차의 절댓값으로 제어된다. 첫 잔차는 다시 u로 나누지만 모든 지수 2(n+j)-1>=97이므로 u=0에서도 문제가 없다. 0<=u<=q0에서 각 양의 단항식을 q0에서 평가하고 factorial tail의 연속항 비율을 상계하면 정확히 제공된 Tail(j,e) 및 E_k가 나온다. 이 식과 JSON의 E_k 유리수는 이번 실행에서 정확히 일치했다.

짝수 l에서는 |x-y|^l=(x-y)^l이므로 적분 출력 차수는 l 이하이다. 홀수 l에서는 y=x에서 나누어 적분하면 차수가 l+j+1 이하이다. 따라서 실제 28차 입력에 대한 k96 출력은 max(96,95+28+1)=124차 이하이고 짝수이다. 이에 따라 T K_k96 h_A=0이다. 실제 K_k의 tail이 0이라는 주장은 아니다.

커널 차이의 sup 상계 E_k와 구간 길이 3/2에서

\[
\|K_k-K_{k_{96}}\|_{2\to2}\le\tfrac32E_k.
\]

**Pole remainder와 실제 source.** cosh의 30차 절단 뒤 첫 항은 (3/8)^32/32!이며, 이후 비율은 (3/8)^2/(33*34) 이하이다. 따라서 제공된 t_h가 전체 잔차를 제어한다. JSON의 t_h와 이 유리수 식도 정확히 일치했다. 또한 cosh(3/8)<=1/(1-(3/8)^2/2)=128/119<3/2이다. 따라서

\[
\|T[2M(h_A)\cosh(x/2)]\|_2
\le 3\cosh(3/8)t_h\|h_A\|_2
\le\tfrac92t_h\|h_A\|_2.
\]

T Pi_X=T와 위 support를 합치면 실제 F=W_Bh_A-sum c_n S_nh_A에 대하여

\[
TY_{\rm actual}=TF+r,\qquad
\|r\|_2\le(\tfrac32E_k+\tfrac92t_h)\sqrt{H_A}\le e_{op}\sqrt{H_A}.
\]

이번 실행은 요청대로 e_par까지 포함한 e_op 전체를 썼다. Pole는 한 번만 지불했다. F를 옛 독립 reference Y0와 동일시하지 않았으며, 그 raw reference rows는 사용하지 않았다.

**Parseval 인증과 shift 교차항.** W와 합쳐진 S는 모두 짝수 L2 함수이다. 각 성분에서 m=0,2,...,128의 정확히 65개 모드를 제거했다. low 0:30도 포함했다. 실제 계산은

\[
U_W=N_W^{up}-P_W^{low},\quad U_S=N_S^{up}-P_S^{low},
\quad y_{cert}=\sqrt{U_W}^{up}+\sqrt{U_S}^{up}+(e_{op}\sqrt{H_A})^{up}
\]

의 방향을 지켰다. 계수 구간이 0을 가로지르면 제곱의 하단을 0으로 두었다. U_W,U_S의 음수 상단은 assertion 오류로 중단하도록 했으며 실제 둘 다 양수였다.

Shift는 여섯 branch로 표현했다. 6개 대각항과 15개 비대각 pair(후자 배수 2)로 36개 ordered term을 모두 보존했다. n=2의 두 branch 중첩도 포함했다. 모든 support 끝점은 (c+a log2+b log3)/3으로 표현했으며 log4=2log2를 유지했다. 같은 symbolic 끝점은 같다고 처리하고, 다른 끝점의 순서는 outward boxes로 확정했다. 적분은 각 실제 교집합에서 다항식 원시함수만 평가했다. 불연속 shift에 H2 tail을 적용하지 않았다.

**실행 기록과 재현 파일.** Python 3.12.14 표준 라이브러리만 사용했다. 계산 시도는 1회이고 종료 코드는 0이다. 완료 체크포인트 시간은 1.8922807050000756초, peak RSS는 13568 KiB였다. 내부 SIGALRM 290초, 외부 timeout 295초 및 1초 후 SIGKILL, RLIMIT_AS 805306368 bytes(768 MiB)를 설정했다. RLIMIT_AS는 실행 시 읽어 되확인했다.

수치 구간 끝점은 정수/10^120 형식이다. 덧셈, 곱셈, 나눗셈, 제곱과 제곱근 후 모두 외향 반올림했다. 제곱근은 integer isqrt를 사용했다. 별도의 유한 symbolic 등식 검사는 정확한 정수/유리수로 수행하고 numerator/denominator 8192-bit 상한을 걸었다. 그 실제 최대는 1696 bits였다. 이는 무제한 유리수 정밀도 탐색이 아니며 수치 구간 연산의 격자는 끝까지 고정했다.

구간 연산 976356회, 최대 다항식 곱 차수 156이었다. quadrature, matrix, inverse, cutoff 확장, witness 탐색 및 재실행은 모두 0회다. 상수 log2, log3, reciprocal square roots, pi의 boxes가 참값을 포함한다는 사실은 제공 입력의 계승 전제이다. 외부에서 새 상수를 검색하거나 midpoint를 참값으로 사용하지 않았다.

파일 구성:

- certify_tail.py: 실제 실행한 전체 코드. 실행 후 변경하지 않았다.
- run_once.sh: 실제 사용한 외부 시간제한 명령.
- input.json: 첨부 JSON을 그대로 추출한 입력.
- stdout.txt, stderr.txt: 실제 표준 출력과 표준 오류. stderr는 비어 있다.
- run/result.json: 전체 120자리 구간, 65+65개 모드, 모든 shift pair, 자원 기록.
- run/ATTEMPT_STARTED: 1회 실행 표식. 동일 디렉터리 재실행을 차단한다.
- request.txt: 이번 자체 완결 요청 원문 사본.
- MANIFEST.sha256: 패키지 내용의 해시.

입력 SHA256: ae6ed84a6d2986e8d48c4cda4e665b339e6ccc0440e3f9277b0b075c613540e4

코드 SHA256: 3ae344e38cf988ca3d966769bb8d9842b5b1ac653061fe11e88a298b6313a2e6

독립 재현자가 새 출력 디렉터리를 사용하는 명령은 다음과 같다. 이번 세션에서는 이 명령으로 추가 실행하지 않았다.

```sh
/usr/bin/timeout --signal=TERM --kill-after=1s 295s \
  python3 -u certify_tail.py input.json NEW_OUTPUT_DIRECTORY
```

**판정 범위.** 실행 결과를 C(Y)의 상계나 Schur 개선량으로 바꾸는 연결은 이번에 평가하지 않았다. Bstar^{-1}, A0, R을 교환하거나 대각별로 치환하지 않았다. 원래 weighted minimum operator, physical Q와 이 Y의 연결도 이번 코드가 독립 인증한 것은 아니다. 원문에 적힌 네 개 이전 파일의 SHA256는 provenance 전제이며, 그 원본 파일을 이번에 읽거나 재해시하지 않았다.

기록된 특정 q=0 prefix-reference 인증식의 장애는 이번 source-tail 계산으로 해소됐다고 할 수 없다. 그 reference baseline은 실제 C(Y)의 하계가 아니며, 모든 방법에서 q!=0가 필수라는 결론도 나오지 않는다. pure/combined cutoff 및 formal joint/separate 비교는 이 수치 계산에 사용하지 않았다. pure w의 미분은 w'(t)=(2a-t)/t^3이므로 2a 이후의 감소만 보장한다는 정정은 유지한다.

이번에는 새 성공 임계값을 도입하지 않았다. 요청된 비교 y_cert^up<Y_crude^low만 검사했다. 전체 연산자 양성, 전체 L>=0 및 RH 결론은 여전히 없다.
