# SERABI RH — Source subspace / Schur 독립 감사

감사일: 2026-09-18. 대상: 첨부 `SERABI_RH_SOURCE_SUBSPACE_AND_SCHUR_2026-09-18.md` 및 동명 계열 ZIP.

## 1. 결론

**FIXED-m SOURCE THEOREM = CERT-ANALYTIC-AS-SCOPED.** 본문에 적힌 실제 원천 소거, 고정 차수 다항식 꼬리 제어, Fourier 저주파 질량 추정, 실제 prime-power 꼬리 합을 독립적으로 다시 유도했으며 핵심 오류를 발견하지 않았다. 상수의 m 의존성을 유지한 존재형 정리로 유효하다. 명시적 시작점이나 커지는 m에 대한 수치 인증은 아니다.

**GLOBAL SCHUR GATE = OPEN / RH-EQUIVALENT AT COFINAL SCOPE.** 남은 전체 Schur 양성은, 아래에 명시한 구간·정의역·양화사에서 RH와 정확히 동치다. 이 보고서는 그 동치를 증명하며 Schur 양성 자체를 증명하지 않는다.

**LONG-RANGE ADMISSION = HOLD.** 단순히 원래 목표를 다른 기호로 쓴 것에 그치지 않는 유한 원천 정리는 확보됐다. 그러나 전체 음의 방향 수는 Schur 제거 후에도 그대로이며, R18A의 odd resolvent 성장률이나 canonical prolate 정렬로 전달하는 정리는 없다. 주력 장기 분기 승격 근거는 아직 부족하다.

## 2. 무엇을 실제로 검사했는가

주 보고서 전체, 코드 전체, 정의·참고문헌 JSON/Markdown, 최초 OPEN 파일, 기록 로그를 읽었다. 원천 소거의 계승 증명은 패키지 내 `SERABI_RH_SOURCE_CANCELLATION_AND_GAP_GATE_2026-09-18.md`의 §§1–4도 직접 확인했다. 나머지 계승 보고서는 목록과 목차·판정 범위를 확인했으며, 그 안의 모든 prolate 정리나 수치 하계를 독립 인증한 것으로 취급하지 않는다. 현재 정리의 증명은 주 보고서 §§2–6만으로 재구성했다.

ZIP의 manifest 16개 항목이 모두 일치했다. 별도 첨부 보고서는 ZIP 내부 보고서와 바이트 단위로 같다. 원본을 보존하고 별도 복사본에서 원본 verifier를 재실행했다. 정확 유리수 검사 72개가 통과했으며 `exact.log`, `exact_results.json`, `input_hashes.json`이 원본과 각각 바이트 단위로 일치했다. runtime 문자열 차이는 수학적 불일치로 세지 않았다.

이 72개는 유한 대수 검사다. 실제 Weil gap, 전체 Schur 양성, 무한차원 정리의 계산 인증은 각각 0개다. 분석적 판정은 검산 개수가 아니라 아래 증명 감사에 근거한다.

## 3. 객체·정규화·양화사

\[
a=\log\lambda,\quad I_a=[-a,a],\quad \mathcal H_\lambda=L^2(I_a,dx),
\quad \widehat f(t)=\int f(x)e^{-itx}\,dx.
\]

q_lambda는 첨부 (1.1)의 **이동하지 않은** semilocal Weil form이다. 그 자기수반 실현을 A_lambda라 쓴다. form domain은 영연장 Fourier 변환에 대한 로그 에너지가 유한한 함수들이다. 고정 lambda에서 pole 항과 유한 prime-power 항은 유계이므로 archimedean form과 같은 정의역을 가진다. 이 실현의 semiboundedness 및 discrete spectrum은 [CCM v1 §3](https://arxiv.org/html/2511.22755v1#S3)의 객체와 맞는다.

\[
\kappa(x)=e^{x/2}\sum_{n\ge1}
(4\pi^2n^4e^{4x}-6\pi n^2e^{2x})e^{-\pi n^2e^{2x}},
\quad V_m=\operatorname{span}\{\kappa,\ldots,\kappa^{(m)}\}.
\]

입력 정리의 정확한 양화사는

\[
\boxed{\forall m\in\mathbb N_0\ \exists\lambda_m>1\
\forall\lambda\ge\lambda_m\ \forall v\in V_m\setminus\{0\}:\quad
q_\lambda[1_{I_a}v]\ge\tfrac12\log\lambda\,
\|1_{I_a^c}v\|_2^2>0.}
\]

계수의 lambda 의존성은 허용된다. m 의존성을 버리거나 양화사 순서를 바꾸지 않는다.

**표기 주의:** 여기서 `N=lambda^2`는 prime cutoff다. R18A의 `N`은 Fourier 행렬의 truncation index다. 두 N을 같다고 놓는 별도 schedule은 주어지지 않았다. 또한 여기의 `q_lambda`는 이차형식이며, R18A의 `q_N=||A_-^{-1} beta||`는 노름이다. 같은 문자를 사용했다는 이유로 결과를 전달하면 안 된다.

## 4. 분석적 증명 재검토

### 4.1 전체 원천 소거는 RH를 가정하지 않는다

Gaussian Mellin 적분은

\[
\int_0^\infty (4\pi^2u^4-6\pi u^2)e^{-\pi u^2}u^{s-1}du
=F(s)=\tfrac12s(s-1)\pi^{-s/2}\Gamma(s/2)
\]

를 준다. 실제 약수 항등식 `sum_(d|r) Lambda(d)=log r`로 양방향 prime 작용은 J(x)+J(-x)가 된다. Mellin 적분선을 c>1에서 1/2로 옮길 때 -F zeta'의 s=1 residue는 1/2이며, 미분된 기능방정식에서 F'/F의 rational 항들은 s와 1-s 사이에 정확히 소거된다. 남는 승수는 `b(t)=Re psi(1/4+it/2)-log pi`이다. pole 작용이 cosh(x/2)를 복구하므로

\[
(H+\Pi-\mathcal P)\kappa^{(j)}=0
\]

가 모든 고정 j에 성립한다. 전체 실선의 별도 자기수반 연산자나 RH를 가정할 필요가 없다. 각 고정 x에서 급수의 절대수렴, 수직선의 Gamma 감소, 임의 고정 도함수의 theta 감소가 교환을 정당화한다.

v=v_a+tau의 안쪽·바깥 조각을 pairing하면 B(v_a,v_a)=B(tau,tau)가 된다. 두 조각은 BV이고 Fourier 변환이 O(1/|t|)여서 로그 에너지가 유한하다. prime pairing도 각 조각의 임의 지수 감소에서 절대수렴한다. 따라서 경계 jump를 삭제한 논증이 아니다.

### 4.2 경계 소거에 대한 균일성은 실제로 확보된다

P_(j+1)=P_j/2+2zP_j'-2zP_j, deg P_j=j+2이다. 고정 m의 오른쪽 꼬리는 차수 d=m+2 이하의 P에 해당한다. Z=pi lambda^2, u=Z(e^(2(x-a))-1), Q(u)=P(Z+u)로 바꾸면 leading theta 항의 정확한 L2 노름은

\[
\frac{e^a e^{-2Z}}{2Z}J_Z(Q)^2,
\quad J_Z(Q)^2=\int_0^\infty(1+u/Z)^{-1/2}e^{-2u}|Q(u)|^2du.
\]

구간 [0,1]의 Hilbert Gram 행렬로 J_Z(Q)의 계수 노름 하계를 얻는다. 이 하계는 모든 Z>=1과 모든 복소 계수에 균일하다. Q(0)=Q'(0)=...=0인 경우에도 성립한다. 그러므로 경계값 소거가 leading term과 실제 꼬리 사이의 상대 추정을 깨지 않는다.

n>=2 theta 항은 Q((n^2-1)Z+n^2u)로 표현된다. 다항식 노름 추정과 `exp(-(n^2-1)Z)`의 감소를 합하면 leading 항 대비 `C_d Z^d exp(-3Z)`의 L2 오차를 얻는다. 충분히 큰 Z에서 1/2 이하이므로 실제 꼬리 노름으로 교체 가능하다. 양쪽 꼬리를 각각 처리하여

\[
|\tau(x)|\le C_m\sqrt{N}\,\|\tau\|_2
1_{|x|>a}e^{-N(|x|-a)},\qquad N=\lambda^2
\]

가 나온다. 이 단계는 계수별 추정을 합한 것보다 강하며, 첨부의 핵심 기여다.

### 4.3 부호를 강제하는 크기 비교

위 식에서 ||tau||_1<=C_m N^(-1/2)||tau||_2이고, 따라서 |t|<=lambda의 Fourier 질량은 전체 L2 질량의 C_m/lambda 이하이다. [DLMF 5.11.2](https://dlmf.nist.gov/5.11#E2)의 digamma 점근식과 연속성으로 b(t)>=-C 및 b(t)>=log|t|-C (|t|>=1)를 얻는다. 따라서 archimedean 항은

\[
h[\tau]\ge(\log\lambda-C-C_m\log\lambda/\lambda)\|\tau\|_2^2.
\]

pole 항의 절댓값은 C_m/lambda 배, prime 항은 C_m log(lambda)/lambda 배 이하이다. 후자의 핵심은 양쪽 꼬리 envelope의 **정확한** autocorrelation

\[
\int F(x)F(x+s)dx=e^{-Ns}/N+(s-2a)_+e^{-N(s-2a)}
\]

이다. 반대쪽 꼬리의 겹침을 포함하고 있다. s=log n을 대입하면 n>N 부근에만 두 번째 기여가 생기며 `(n-N) exp(-(n-N)/2)`로 합산된다. 이 합은 실수 N의 소수 부분에도 균일하다. 따라서 정수나 prime-power 문턱을 누락하지 않았다.

결합하면 고정 m마다 주장된 1/2 log(lambda) 하계를 얻는다. 원천의 독립성 및 해석성으로 비영 v의 꼬리 노름은 양수다. 명시적 lambda_m을 산출하지 않아도 이 존재형 결론은 유효하다.

## 5. Schur 항등식과 정의역

U=1_(I_a)V_m의 모든 생성자는 영연장 Fourier 변환이 O(1/|t|)이므로 log^2 가중 L2 조건을 만족한다. 따라서 compressed archimedean 연산자, 나아가 A_lambda의 operator domain에 속한다. P를 U의 L2 직교사영, Q=I-P라 하면 P는 form domain을 보존하며 Q도 그렇다.

B=P A_lambda P>0는 U 위의 가역 행렬이다. R=Q A_lambda P는 유한 랭크 유계 연산자, C는 Q form domain 위의 닫힌 form restriction이다. 완전제곱의 삼각변환은 form domain 위에서 가역이다. 따라서

\[
q_\lambda[u+v]=\|B^{1/2}(u+B^{-1}R^*v)\|^2+S[v],
\qquad S=C-RB^{-1}R^*.
\]

이로써 `A_lambda>=0 iff S>=0`와 `n_-(A_lambda)=n_-(S)`는 유효하다. **양수 블록 제거는 음의 방향을 하나도 제거하지 않는다.** 작은 B 때문에 B^-1의 증폭이 커질 가능성도 그대로 남는다.

## 6. 추가 정리: 전체 cofinal Schur gate는 RH와 동치

**정리.** 임의의 고정 m을 택한다. lambda_k>=lambda_m, lambda_k→∞인 임의의 sequence에서 위 Schur form S_(m,lambda_k)를 정의한다. 그러면

\[
\boxed{RH\iff S_{m,\lambda_k}\succeq0\ \text{for every sufficiently large }k.}
\]

**증명.** RH이면 explicit formula의 영점 표현은 절댓값 제곱의 합이므로 모든 compact support Weil test의 q가 비음수다. 고정 구간의 닫힌 form으로 확장하여 A_lambda>=0이고, Schur 항등식으로 S>=0이다.

역으로 cofinal한 S>=0는 해당 구간들의 A_lambda>=0를 준다. 임의의 f in C_c^infty(R)는 충분히 큰 I_(log lambda_k)에 들어간다. 이때 q_lambda_k[f]는 k와 무관한 전역 Weil 표현 B[f]다. support가 허용하지 않는 이동에서는 autocorrelation이 0이므로 prime cutoff 확장으로 값이 달라지지 않는다. 따라서 B[f]>=0가 모든 compact smooth f에 대해 성립한다. 고전 Weil 양성 판정법으로 RH가 따른다. QED.

정확한 compact test criterion의 원천은 [Connes–Consani, 2006.13771v1, 서론 식 (2) 및 Appendix C Proposition C.1](https://arxiv.org/pdf/2006.13771)이다. 그 문헌의 곱셈 변수 g(u)와 여기의 f(x)는 `g(u)=u^(-1/2) f(log u)`로 연결된다. g의 Mellin 값 0,1의 소거 조건은 f의 Fourier 값 -i/2,+i/2의 소거와 같다. 모든 compact f에 대한 q>=0는 이 소거 조건을 만족하는 부분류에도 적용되므로 역방향 criterion을 충족한다. RH에서 pole을 포함한 모든 f의 양성은 explicit formula가 직접 준다.

형식의 정의역 확장은 compact smooth functions의 form density로 정당화된다. 구체적으로 영연장 f를 약간 안쪽으로 dilation한 뒤 smooth convolution한다. Fourier 쪽 dilation은 `1+log(2+|t|)` 가중 L2에서 연속이고, mollification은 지배수렴한다. 고정 구간의 나머지 항은 L2-유계다. 그러므로 경계값이 0이 아닌 form-domain 함수도 근사된다.

**범위:** 한 개의 유한 lambda에서의 S>=0를 RH와 동치라고 한 것이 아니다. eventual/cofinal 전체 양성이 필요하다. ground gap 및 proxy 정렬 각각의 명제와 RH의 동치를 주장하지도 않는다.

## 7. 추가 정리: 가상의 음의 증인은 Schur에 그대로 남는다

어떤 compact smooth f가 B[f]<0라고 가정하자. 이 가정은 반증을 주장하는 것이 아니라 조건부 구조 검사다. 모든 충분히 큰 lambda에서 동일한 f를 넣고 u=Pf, v=Qf라 쓰면

\[
\boxed{S[v]=B[f]-\|B^{1/2}(u+B^{-1}R^*v)\|^2\le B[f]<0.}
\]

v=0이면 q[f]=<Bu,u>>=0가 되므로 모순이다. 따라서 v는 실제 비영 음의 Schur 증인이다. 양수 source 공간을 넓히는 것만으로 기존 음의 증인을 없앴다고 추론할 수 없다.

이 결과는 실제 원천에서 어떤 음의 f가 존재한다는 주장이 아니다. Schur 제거의 난이도 감소를 평가하는 정확한 조건부 정리다.

## 8. ground transform와 정확한 포화

첨부 §8의 계수와 부호를 재계산했다. `w(s)=exp(-s/2)/(1-exp(-2s))`, `d mu=2 kappa cosh(x/2) dx`에서 mu의 전체 질량은 1이다. digamma의 적분 표현으로 H의 차이 제곱 계수가 정해진다. W kappa=0를 사용한 source transform은

\[
B[\kappa g]=D_+(g)-\tfrac12\operatorname{Var}_\mu(g)
-\tfrac12\left|\int\tanh(x/2)g\,d\mu\right|^2
\]

이며 첨부와 일치한다. g_j=kappa^(j)/kappa에서 양쪽 적분의 수렴도 고정 차수 theta 감소로 정당하다. g_2는 짝수이고 E_mu g_2=1/4이므로 D_+(g_2)=Var_mu(g_2)/2>0다.

각 고정 소수 p의 D_p(g_2)>0도 맞는다. 반대라면 양의 가중치 때문에 g_2가 log p 주기여야 하지만, g_2(x)~4 pi^2 exp(4x)이므로 불가능하다. compact cutoff로 옮겨도 해당 부호 실패가 유지된다. 여기서 q[1_I kappa'']→0에는 별도 상계가 필요하며 T1 하계만으로는 나오지 않는다. 고정 함수의 tail L1 노름과 총변동이 모두 초지수로 감소하고 `|hat tau(t)|<=min(||tau||_1,TV(tau)/|t|)`이므로 log 가중 Fourier 에너지도 0으로 간다. prime/pole 항은 이미 확보한 꼬리 추정으로 0으로 간다.

따라서 같은 우변을 유지한 채 양의 prime-difference 기여를 고정 비율 버리는 비교, 또는 모든 짝함수에 Poincare 상수를 1/2보다 엄격히 높이는 비교는 **KILL-AS-STATED**로 표시하는 것이 정확하다. 첨부의 HOLD보다 강한 판정이지만, 적용 대상은 그 특정 부등식들뿐이다.

`D_+>=N`을 모든 compact smooth g에 요구하는 전체 비교는 `f=kappa g`가 해당 시험공간의 전단사이므로 RH와 동치다. 이는 실제 불가능성 정리가 아니라 정확한 문제의 재표현이다.

## 9. 장기 연구 판단 및 다음 행동

R18A에서 요구했던 “실제 원천의 새 부등식”이라는 넓은 조건은 이번 고정-m 정리로 일부 충족했다. 이것은 보존할 수학적 성과다. 그러나 다음 연결은 여전히 없다.

| 연결 | 상태 |
|---|---|
| 실제 divisor identity → 전체 source 소거 | CERT |
| source 소거 + 고정 차수 꼬리 추정 → 유한 블록 양성 | CERT |
| 유한 블록 양성 → 실제 odd resolvent 성장률 | OPEN / 정리 미제시 |
| 유한 블록 양성 → ground gap 및 canonical proxy 정렬 | OPEN / 정리 미제시 |
| 전체 cofinal Schur 양성 ↔ RH | 구조적 동치 CERT; 양성 자체 OPEN |

**권고:** 고정-m 결과를 보존하고 전체 Schur 양성의 직접 반복 공격은 새로운 source inequality가 나올 때까지 HOLD한다. 다음 연구 제안은 (i) 제어할 Schur test class나 beta spectral mass, (ii) 원천에서 이를 제어하는 새 메커니즘, (iii) 필요한 lambda–Fourier-cutoff 관계 및 목표 크기를 먼저 명시해야 한다. 전체 `S>=0` 자체를 새 가정이나 작은 보조정리로 재포장하지 않는다.

```text
FIXED_SOURCE_SUBSPACE_POSITIVITY = CERT-ANALYTIC-AS-SCOPED
ORIGINAL_RATIONAL_REPLAY = PASS-72
ACTUAL_FULL_SCHUR_POSITIVITY = NOT-OBTAINED
COFINAL_FULL_SCHUR_POSITIVITY_IFF_RH = CERT-STRUCTURAL
ACTUAL_GAP_AND_ALIGNMENT_RATIO = NOT-OBTAINED
R18A_ODD_RESOLVENT_RATE_TRANSFER = NOT-OBTAINED
LONG_RANGE_MAIN_BRANCH_ADMISSION = HOLD
G4_STATUS = LOCKED
RH_PROOF = NOT-OBTAINED
RH_DISPROOF = NOT-OBTAINED
```
