# 실제 Xi 원천의 유한 도함수 공간 양성과 남는 Schur 응답

2026-09-18. `RH_PROOF=NOT-OBTAINED`, `RH_DISPROOF=NOT-OBTAINED`, `G4=LOCKED`.

## 0. 이번에 증명한 것과 증명하지 못한 것

**실제 최저 고유값의 간격, canonical prolate proxy의 정렬 비율, 전체 Schur 보완의 양성은 증명하지 못했다.** 이번에 증명한 것은 한 방향의 작은 에너지보다 강한, 다음의 **부분공간 전체의 양성**이다.

고정된 정수 \(m\ge0\)에 대해
\[
V_m=\operatorname{span}_{\mathbb C}\{\kappa,\kappa',\ldots,\kappa^{(m)}\},
\quad a=\log\lambda,\quad I_a=[-a,a].
\]
그러면 \(m\)에만 의존하는 \(\lambda_m\)가 존재하여
\[
\boxed{
q_\lambda[1_{I_a}v]
\ge \frac12\log\lambda\,\|1_{I_a^c}v\|_2^2>0
\quad(0\ne v\in V_m,\ \lambda\ge\lambda_m).
}\tag{T1}
\]
계수는 복소수여도 되고 \(\lambda\)에 의존해도 된다. 따라서 경계값이나 여러 경계 미분값을 소거하는 조합도 포함한다. 대각 에너지 각각의 양성이 아니라 모든 교차항을 포함한 행렬 부등식이다.

다만 **\(m\)은 고정**되어 있다. \(m=m(\lambda)\to\infty\)에 대한 균일성, 명시적 최소 시작점, 전체 함수공간에 대한 양성은 주장하지 않는다. 모든 큰 실수 \(\lambda\)에서 성립하므로 각 큰 dyadic 구간 전체와 기존의 선택된 cofinal schedule에 적용된다. schedule이나 canonical prolate proxy를 바꾸지 않는다.

| 항목 | 판정 |
|---|---|
| 실제 원천의 모든 고정 유한 도함수 조합에 대한 (T1) | 본문 일반 증명 |
| 해당 유한 블록의 양정치성과 내부 Schur 보완 | 본문 일반 증명 |
| 전체 형식에서 남는 결합 응답을 포함한 정확한 Schur 식 | 본문 일반 항등식 |
| \(\kappa\) 변환으로 얻은 가중 차이 제곱 비교의 정확한 포화 | 본문 일반 증명 |
| 그 비교에서 고정된 소수 하나의 양의 기여를 버리는 방법 | 실제 원천 반례로 HOLD |
| 실제 전체 Schur 보완의 양성, 음의 고유값 개수, ground gap | OPEN |
| 원래 prolate proxy의 실제 ground 정렬 비율 | OPEN |

‘증명’은 이 문서에 제시한 논증을 뜻한다. 유한 검산 개수가 무한차원 정리를 인증했다거나 독립적인 동료 심사가 끝났다는 뜻이 아니다. 문헌상 최초라는 주장도 하지 않는다.

## 1. 대상과 정규화

\[
N=\lambda^2,\qquad
\widehat f(t)=\int_{\mathbb R}f(x)e^{-itx}\,dx,
\quad b(t)=\Re\psi(1/4+it/2)-\log\pi.
\]
\[
q_\lambda[f]=\frac1{2\pi}\int b(t)|\widehat f(t)|^2dt
+2\Re\!\left(\widehat f(i/2)\overline{\widehat f(-i/2)}\right)
-2\sum_{2\le n\le N}\frac{\Lambda(n)}{\sqrt n}
\Re\int\overline{f(x)}f(x+\log n)\,dx .\tag{1.1}
\]
여기서 \(f\)는 \(I_a\) 밖에서 0이다.
승수에 별도의 \(1/(2\pi)\)를 더 넣지 않는다. \(\Lambda\)는 prime powers를 모두 포함하는 실제 von Mangoldt 함수다. 기존 객체의 정의는 [Connes–Consani–Moscovici, *Zeta Spectral Triples*, §3, §7](https://arxiv.org/html/2511.22755v1)의 정규화를 따른다.

\[
\kappa(x)=e^{x/2}\sum_{n\ge1}
\bigl(4\pi^2 n^4e^{4x}-6\pi n^2e^{2x}\bigr)e^{-\pi n^2e^{2x}}.
\tag{1.2}
\]
이 함수는 실수·짝수·엄격히 양수이며, 모든 고정 차수 도함수와 함께 양 끝에서 초지수 감소한다. \(\widehat\kappa=\Xi\),
\[
\int e^{x/2}\kappa(x)dx=\int e^{-x/2}\kappa(x)dx=\tfrac12.
\tag{1.3}
\]
전체 실선의 sesquilinear Weil 표현을 \(\mathcal B\)라고 쓴다. 이는 (1.1)의 소수합을 모든 \(n\ge2\)로 확장한 표현이며, 각 항이 수렴하는 함수에만 사용한다. 전체 실선에 새로운 자기수반 연산자를 구성했다고 가정하지 않는다.

## 2. 실제 산술을 쓰는 단계: 모든 도함수 조합의 정확한 소거

이 단계는 이전 source 보고서의 항등식이다. 이번 증명에 필요한 부분을 다시 적는다.
\(h_\Xi(u)=(4\pi^2u^4-6\pi u^2)e^{-\pi u^2}\)라 두자.
\[
F(s)=\tfrac12s(s-1)\pi^{-s/2}\Gamma(s/2),\qquad
J(x)=e^{x/2}\sum_{r\ge1}\log r\,h_\Xi(re^x).
\]
Gaussian Mellin 적분은 \(F(s)\zeta(s)=\xi(s)\)를 준다. 실제 약수 항등식
\[
\sum_{d\mid r}\Lambda(d)=\log r
\]
을 절대수렴하는 이중합에 적용하면
\[
(\mathcal P\kappa)(x)=J(x)+J(-x),\qquad
\mathcal P f=\sum_{n\ge2}\frac{\Lambda(n)}{\sqrt n}
\bigl(f(x+\log n)+f(x-\log n)\bigr).\tag{2.1}
\]
\(-F(s)\zeta'(s)\)의 Mellin 적분선을 \(\Re s>1\)에서 \(1/2\)로 옮길 때 \(s=1\)의 residue는 \(1/2\)이다. Gamma의 감소와 고정 strip의 다항 성장으로 수평 변은 사라진다. 미분한 기능방정식은
\[
-F(s)\zeta'(s)-F(1-s)\zeta'(1-s)=b(t)\Xi(t),
\quad s=1/2+it
\]
를 주므로
\[
H\kappa=J(x)+J(-x)-\cosh(x/2).
\]
극 항의 실제 kernel은 \(2\cosh((x-y)/2)\)이고 (1.3)에 의해 \(\Pi\kappa=\cosh(x/2)\)다. 따라서
\[
(H+\Pi-\mathcal P)\kappa^{(j)}=0\quad(j\ge0).\tag{2.2}
\]
미분 교환은 고정 차수의 theta 감소로 정당하다. 영점의 위치나 RH를 쓰지 않는다.

\(v\in V_m\), \(v_a=1_{I_a}v\), \(\tau=1_{I_a^c}v\)라 하면
\[
\boxed{q_\lambda[v_a]=\mathcal B[\tau].}\tag{2.3}
\]
실제로 \(\mathcal B(v,\cdot)=0\)를 두 조각에 적용한다. 점프 때문에 항등식이 깨지지 않는다. \(v_a,\tau\)는 BV이고 Fourier 변환이 \(O(1/|t|)\)이므로 로그 에너지가 유한하다. prime pairing은 초지수 감소를 임의의 \(Ce^{-M|x|}\)로 지배하여 절대수렴시킬 수 있다.

**일반적인 작은 잔차 반례와 구별되는 원천 고유의 성질은 (2.1)–(2.3)이다.** 아래에서 절댓값을 취하는 대상은 이 공동 소거를 마친 뒤의 좁은 두 꼬리뿐이다. 임의 함수의 bulk 소수합을 제어했다고 주장하지 않는다.

## 3. 계수에 균일한 꼬리 집중 보조정리

고정 \(m\)에 대해 상수 \(C_m\)와 시작점이 존재하여, 모든 \(v\in V_m\) 및 충분히 큰 \(\lambda\)에 대해
\[
\boxed{
|\tau(x)|\le C_m\sqrt N\,\|\tau\|_2
\,1_{|x|>a}e^{-N(|x|-a)}.
}\tag{3.1}
\]
이 부등식은 경계 소거로 \(\|\tau\|_2\)가 작아진 경우도 포함한다. 각 도함수를 따로 상계한 뒤 계수의 합으로 대체해서는 얻을 수 없는 균일성이다.

### 3.1 다항식의 정확한 표현

\(z_n=\pi n^2e^{2x}\)라 두면
\[
\kappa^{(j)}(x)=e^{x/2}\sum_{n\ge1}P_j(z_n)e^{-z_n},
\quad P_0(z)=4z^2-6z,
\]
\[
P_{j+1}(z)=\tfrac12P_j(z)+2zP'_j(z)-2zP_j(z).\tag{3.2}
\]
\(\deg P_j=j+2\), 최고차 계수는 \(4(-2)^j\)다. 따라서 오른쪽 꼬리의 임의 조합은 어떤 \(\deg P\le d=m+2\)를 사용한
\[
f_P(x)=e^{x/2}\sum_{n\ge1}P(\pi n^2e^{2x})e^{-\pi n^2e^{2x}}
\]
이다. 왼쪽 꼬리는 계수를 \((-1)^j\)배 한 별도의 같은 차수 다항식에 해당한다.

### 3.2 경계에서 이동한 다항식의 노름

\(Z=\pi N\), \(u=Z(e^{2(x-a)}-1)\ge0\), \(Q(u)=P(Z+u)\)라 하자. \(n=1\) 항 \(f_{P,1}\)에 대해 정확히
\[
\|f_{P,1}\|_{L^2(a,\infty)}^2
=\frac{e^a e^{-2Z}}{2Z}\,
J_Z(Q)^2,
\]
\[
J_Z(Q)^2=\int_0^\infty(1+u/Z)^{-1/2}e^{-2u}|Q(u)|^2du.\tag{3.3}
\]
\(Z\ge1\)이면 이 노름은 차수 \(d\) 이하의 모든 다항식에서 계수의 Euclidean 노름과 균일하게 동치다. 구체적으로 \(Q=\sum q_k u^k\), \(G_d=(1/(i+j+1))_{0\le i,j\le d}\)라 하면
\[
J_Z(Q)^2\ge \frac{e^{-2}}{\sqrt2}\int_0^1|Q(u)|^2du
\ge \frac{e^{-2}}{\sqrt2\,\operatorname{tr}(G_d^{-1})}
\sum|q_k|^2.\tag{3.4}
\]
\(G_d>0\)는 다항식의 적분 Gram 표현으로 즉시 따른다. 상계도 유한한 Gamma moments에서 따른다. 특히
\[
|Q(u)|\le C_d(1+u)^dJ_Z(Q)\quad(u\ge0).\tag{3.5}
\]
여기에는 \(P\)의 계수가 \(Z\)에 따라 변하지 않는다는 가정이 없다.

(3.5)와 다항식의 지수 흡수로
\[
|f_{P,1}(x)|\le C_d\sqrt Z\,
\|f_{P,1}\|_2 e^{-u/2}
\le C_d\sqrt Z\,\|f_{P,1}\|_2 e^{-Z(x-a)}.\tag{3.6}
\]
마지막에는 \(u\ge2Z(x-a)\)를 사용했다.

### 3.3 나머지 theta 항은 계수 소거 후에도 작다

\[
P(n^2(Z+u))=Q((n^2-1)Z+n^2u)
\]
와 (3.5)를 쓰면 \(n\ge2\) 항들의 합은
\[
C_d Z^d e^{-3Z}e^{a/2}e^{-Z}J_Z(Q)e^{-u/2}
\]
로 지배된다. 여기서 \(\sum_{n\ge2}n^{2d}e^{-(n^2-4)Z}\)는 \(Z\ge1\)에서 유계다. \(dx=du/(2(Z+u))\)로 적분하면
\[
\|f_P-f_{P,1}\|_2
\le C_dZ^de^{-3Z}\|f_{P,1}\|_2.\tag{3.7}
\]
충분히 큰 \(Z\)에서 우변의 상대 인자는 \(1/2\) 이하이다. 따라서 실제 \(\|f_P\|_2\)로 (3.6)의 노름을 바꿀 수 있다. \(Z=\pi N\), \(e^{-Zr}\le e^{-Nr}\)를 사용하고 양쪽 꼬리를 합치면 (3.1)이 증명된다.

유한 차원 노름 동치에 숨겨진 상수들은 (3.4)와 다항식·지수 비교에서 유한하고 계산 가능하다. 이번 보고서는 이들을 최적화하거나 수치 \(\lambda_m\)를 인증하지 않는다.

## 4. 로그 에너지의 하계

\(T=\|\tau\|_2\)라 하자. (3.1)에서
\[
\|\tau\|_1\le C_mN^{-1/2}T.
\]
따라서 낮은 주파수 질량은
\[
\frac1{2\pi}\int_{|t|\le\lambda}|\widehat\tau(t)|^2dt
\le \frac\lambda\pi\|\tau\|_1^2
\le\frac{C_m}{\lambda}T^2.\tag{4.1}
\]
Digamma의 점근 전개와 실축 위의 연속성으로 절대상수 \(C\)가 존재하여
\(b(t)\ge-C\) 및 \(|t|\ge1\)에서 \(b(t)\ge\log|t|-C\)이다. 사용하는 표준식은 [NIST DLMF 5.11.2](https://dlmf.nist.gov/5.11#E2)다.

Plancherel과 (4.1)을 사용하면
\[
\boxed{
h[\tau]\ge
\left(\log\lambda-C-C_m\frac{\log\lambda}{\lambda}\right)T^2.
}\tag{4.2}
\]
이는 Fourier 꼬리를 버린 근사가 아니라 전체 적분의 하계다.

## 5. 극 항과 실제 소수 꼬리

### 5.1 극 항

(3.1)로부터
\[
\int e^{\pm x/2}|\tau(x)|dx
\le C_mN^{-1/4}T.
\]
그러므로
\[
|\Pi[\tau]|\le C_mN^{-1/2}T^2=\frac{C_m}{\lambda}T^2.\tag{5.1}
\]

### 5.2 서로 반대쪽 꼬리의 산술 간격

\(F_{a,N}(x)=1_{|x|>a}e^{-N(|x|-a)}\)라 두면 \(s\ge0\)에서 정확히
\[
\int F_{a,N}(x)F_{a,N}(x+s)dx
=\frac{e^{-Ns}}N+(s-2a)_+e^{-N(s-2a)}.\tag{5.2}
\]
따라서 실제 autocorrelation은
\[
\left|\int\overline{\tau(x)}\tau(x+s)dx\right|
\le C_mT^2\left[e^{-Ns}+N(s-\log N)_+e^{-N(s-\log N)}\right].\tag{5.3}
\]
\(\Lambda(n)\le\log n\)을 쓰되 모든 prime powers를 유지한다. 첫 항의 소수합은
\(\sum_{n\ge2}(\log n)n^{-N-1/2}=O(e^{-cN})\)이다.

두 번째 항에는 \(n>N\)만 기여한다. \(N<n\le2N\)에서는
\[
\frac{n-N}{2N}\le\log(n/N)\le\frac{n-N}{N},
\]
이므로 합이
\[
\frac{\log(2N)}{\sqrt N}
\sum_{n>N}(n-N)e^{-(n-N)/2}
\le C\frac{\log N}{\sqrt N}
\]
이하이다. 마지막 상수는 \(N\)의 소수 부분에도 균일하다. \(n>2N\)은 \((2^kN,2^{k+1}N]\)로 나누면
\[
C N^{3/2}\sum_{k\ge1}(\log N+k)(k+1)2^{k/2-kN}
=O(N^{3/2}\log N\,2^{-N})
\]
이며 같은 상계에 흡수된다. 따라서
\[
\boxed{|\mathcal P[\tau]|\le
C_m\frac{\log\lambda}{\lambda}T^2.}\tag{5.4}
\]
\(N\)이 정수 또는 prime power 문턱을 지날 때도 동일하다. \(n=N\)이면 서로 반대 꼬리의 겹침 길이가 0이므로 별도의 점 질량 에너지 항이 생기지 않는다.

## 6. (T1)의 결론과 정확한 적용 범위

(2.3), (4.2), (5.1), (5.4)를 합치면
\[
q_\lambda[v_a]\ge
\left(\log\lambda-C-C_m\frac{\log\lambda}{\lambda}\right)\|\tau\|_2^2.
\]
고정 \(m\)에 대해 \(\lambda\)가 충분히 크면 (T1)이 따른다.
비영 \(v\in V_m\)의 꼬리는 0일 수 없다. \(v\)는 실해석적이고, \(P_j\)의 차수와 최고차항으로 이 함수족은 선형 독립이다.

\[
G_{ij}(\lambda)=q_\lambda(1_{I_a}\kappa^{(i)},1_{I_a}\kappa^{(j)}),
\quad
T_{ij}(\lambda)=\langle1_{I_a^c}\kappa^{(i)},1_{I_a^c}\kappa^{(j)}\rangle
\]
라 하면 동등하게
\[
\boxed{G(\lambda)\succeq\tfrac12\log\lambda\,T(\lambda)\succ0.}\tag{6.1}
\]
이는 실제 소수 공동 원천과 직교성에 호환되는 이차형식 부등식이다. 기저를 정규직교화해도 congruence에 의해 보존된다.

그러나 \(T(\lambda)\)는 매우 작고 조건수가 나쁠 수 있다. (6.1)은 \(A_\lambda\)의 실제 첫 \(m+1\) 고유값 하계가 아니다. 이 공간의 Ritz 값에 대한 하계일 뿐이며, min–max로 실제 고유값의 하계로 방향을 뒤집을 수 없다. 정확한 prolate proxy가 이 고정 공간에 속한다고도 가정하지 않는다.

## 7. 전체 Schur 보완: 결합 응답을 그대로 남긴다

\(U_{m,\lambda}=1_{I_a}V_m\), \(P\)를 이 공간의 직교사영, \(Q=I-P\)라 하자. \(1_{I_a}\kappa^{(j)}\)는 BV이며 \(\log^2(2+|t|)|\widehat f(t)|^2\)도 적분 가능하므로 실제 \(A_\lambda\)의 operator domain에 속한다. 다음 블록이 잘 정의된다.
\[
\mathsf B=P A_\lambda P\succ0,
\qquad R=Q A_\lambda P,
\qquad\mathsf C=Q A_\lambda Q.
\]
\(\mathsf C\)는 form restriction으로 해석한다. \(u\in U_{m,\lambda}\), \(v\in Q\mathcal D(q_\lambda)\)에 대해 완전제곱을 만들면
\[
\boxed{
q_\lambda[u+v]
=\langle\mathsf B(u+\mathsf B^{-1}R^*v),u+\mathsf B^{-1}R^*v\rangle
+\mathsf S[v],
}\tag{7.1}
\]
\[
\boxed{\mathsf S=\mathsf C-R\mathsf B^{-1}R^*.}\tag{7.2}
\]
유한 랭크 결합은 bounded이고 삼각변환은 form domain 위의 가역변환이다. 따라서
\[
A_\lambda\succeq0\iff\mathsf S\succeq0,
\qquad n_-(A_\lambda)=n_-(\mathsf S).\tag{7.3}
\]
이 등식은 **음의 고유값 개수를 제어했다는 뜻이 아니다**. 양수임을 증명한 유한 블록을 제거한 뒤 정확히 어디에 문제가 남는지를 뜻한다.

이 공격에서 처음으로 남는 부등식은
\[
\boxed{
q_\lambda[v]\ \ge
\langle R^*v,\mathsf B^{-1}R^*v\rangle
\quad\text{모든 }v\in Q\mathcal D(q_\lambda),
}\tag{OPEN-S}
\]
를 필요한 cofinal 구간에서 증명하는 것이다. **이번에는 이를 증명하지 못했다.**
작은 \(R\)만으로는 우변이 작다고 할 수 없다. \(\mathsf B^{-1}\)의 증폭을 함께 통제해야 한다. 또한 \(z=0\)에서의 양성만으로 simple-even ground 및 proxy 정렬 비율이 자동으로 나오지 않는다. 그 목표에는 실제 근방의 스펙트럼 분리와 정렬 추정도 필요하다.

## 8. \(\kappa\) 변환을 통한 두 번째 공격: 정확한 포화가 드러난다

작은 잔차와 별개로, 양의 원천을 이용한 전체 부호 강제를 시도했다. 이 시도의 정확한 계산과 막힌 지점은 다음과 같다.

\[
w(s)=\frac{e^{-s/2}}{1-e^{-2s}},\quad s>0,
\qquad d\mu(x)=2\kappa(x)\cosh(x/2)dx.
\]
(1.3)에 의해 \(\mu\)는 확률측도다. Digamma의 적분 표현에서
\[
h[f]=b(0)\|f\|^2+\tfrac12\iint w(|x-y|)|f(x)-f(y)|^2dxdy.
\]
\(f=\kappa g\)를 대입하고 \(\mathcal W\kappa=0\)를 \(\kappa|g|^2\)와 pairing하면
\[
\boxed{\mathcal B[\kappa g]=\mathcal D_+(g)-\mathcal N(g),}\tag{8.1}
\]
\[
\mathcal D_+(g)=\tfrac12\iint w(|x-y|)\kappa(x)\kappa(y)|g(x)-g(y)|^2dxdy
+\sum_{n\ge2}\frac{\Lambda(n)}{\sqrt n}
\int\kappa(x)\kappa(x+\log n)|g(x+\log n)-g(x)|^2dx,
\tag{8.2}
\]
\[
\mathcal N(g)=\tfrac12\operatorname{Var}_\mu(g)
+\tfrac12\left|\int\tanh(x/2)g(x)d\mu(x)\right|^2.\tag{8.3}
\]
먼저 \(g\in C_c^\infty\)에 대해 계산한다.
복소수 경우에도 \(\operatorname{Var}_\mu(g)=\int|g|^2d\mu-|\int g\,d\mu|^2\)로 정의한다.

계수를 확인하기 위해 \(\nu=\mu/2\), \(t(x)=\tanh(x/2)\)라 두자.
극 kernel에서 나오는 차이의 제곱은
\[
\tfrac12\iint2\cosh((x-y)/2)\kappa(x)\kappa(y)|g(x)-g(y)|^2dxdy
=\int|g|^2d\nu-2|\int g\,d\nu|^2+2|\int tg\,d\nu|^2,
\]
이며, 이것이 (8.3)과 일치한다.

이제 실제 원천의 도함수 비율
\[
g_j=\kappa^{(j)}/\kappa\quad(j\ge1)
\]
을 넣는다. 이 함수와 고정 도함수들은 많아야 \(e^{C_j|x|}\)로 자라고, \(\kappa\)의 감소 때문에 위 적분과 합은 수렴한다. 원점 근처의 kernel 특이성은 차이의 제곱으로 제거된다. prime 합은 \(\kappa\) 및 \(\kappa|g_j|^2\)의 임의 지수 감소로 지배된다. 따라서 (8.1)을 이 함수들로 연장할 수 있다. (2.2)로
\[
\boxed{\mathcal D_+(g_j)=\mathcal N(g_j).}\tag{8.4}
\]
특히 \(g_2\)는 짝수이고 \(\int g_2d\mu=1/4\)이므로
\[
\mathcal D_+(g_2)=\tfrac12\operatorname{Var}_\mu(g_2)>0.\tag{8.5}
\]
따라서 짝수 함수 전체에서 계수 \(1/2\)를 \(1/2+\varepsilon\)로 높이는 균일한 가중 Poincaré 부등식은 거짓이다. 이는 **실제 원천**에서 생기는 정확한 등호이며 일반 행렬 반례가 아니다.

### 8.1 소수 하나의 양의 기여도 고정량 버릴 수 없다

\(p\)를 임의의 고정 소수, \(\mathcal D_p\)를 (8.2)의 \(n=p\) 항이라 하자. 그러면
\[
\mathcal D_p(g_2)>0.\tag{8.6}
\]
0이라면 양의 가중치 때문에 \(g_2(x+\log p)=g_2(x)\)가 모든 \(x\)에서 성립해야 한다. 그러나
\(g_2(x)\sim4\pi^2e^{4x}\) as \(x\to+\infty\) 이므로 주기성을 가질 수 없다.

따라서 고정 \(\eta>0\)에 대해
\[
\mathcal D_+(g_2)-\eta\mathcal D_p(g_2)-\mathcal N(g_2)
=-\eta\mathcal D_p(g_2)<0.\tag{8.7}
\]
이것은 비콤팩트 함수에서만 생기는 현상도 아니다. \(g_{2,a}=1_{I_a}g_2\)라 하면
\[
\mathcal D_+(g_{2,a})-\mathcal N(g_{2,a})
=q_\lambda[1_{I_a}\kappa'']\longrightarrow0,
\]
\(\mathcal D_p(g_{2,a})\to\mathcal D_p(g_2)>0\)다. 첫 극한은 고정 source 꼬리의 BV·Fourier 추정으로 얻으며, (T1)의 하계만으로 극한을 추론하지 않는다. 따라서 (8.7)의 부호는 충분히 큰 모든 \(a\)에서 유지된다. 필요하면 compact support의 매끄러운 함수로 form approximation할 수 있다.

**정확한 판정:** 같은 우변 \(\mathcal N\)을 유지하면서 고정된 소수 기여를 버리는 비교법은 HOLD다. 이는 원래 \(q_\lambda\)에서 소수 하나를 삭제하면 음수가 된다는 주장이 아니다. 원래 식의 소수항은 음의 부호이며, 여기의 양의 차이 제곱 표현은 전체 source 소거 후에만 성립한다.

### 8.2 남는 비교의 지위

\[
\mathcal D_+(g)\ge\mathcal N(g)
\quad\text{모든 }g\in C_c^\infty(\mathbb R)\tag{OPEN-D}
\]
는 (8.1) 때문에 모든 매끄러운 compact support \(f\)에 대한 Weil 양성과 정확히 같은 명제다. \(\kappa>0\)이고 매끄러우므로 \(g\mapsto\kappa g\)는 이 test space 위의 전단사다. 따라서 **고전적인 Weil 양성 판정법을 사용하면 이 특정 비교는 RH와 동치**다. 이는 논증이 실패했다는 이유로 붙인 난이도 판정이 아니라, 명시적인 전단사와 항등식에 의한 환원이다. RH 아래에서는 explicit formula의 영점합이 절댓값 제곱의 합이 된다. 역방향에는 고전적인 Weil 판정법을 사용한다. 판정법의 배경은 [Bombieri, 공식 문제 해설 §V](https://www.claymath.org/wp-content/uploads/2022/05/riemann.pdf), 여기의 실제 form과 compact-support domain은 [Connes–Consani–Moscovici §3](https://arxiv.org/html/2511.22755v1)에 명시되어 있다.

(8.4)–(8.7)은 (OPEN-D)를 반박하지 않는다. 그 부등식이 참이라면 꼭 맞아야 하는 등호 방향과, 사용할 수 없는 여유분을 특정한다. 실제 gap·정렬 명제가 RH와 동치라고 주장한 것도 아니다.

## 9. 적대적 검사

1. **경계 소거:** (3.3)–(3.7)은 계수별 추정이 아니라 이동한 전체 다항식 \(Q\)의 노름으로 증명했다. \(P(Z)=P'(Z)=\cdots=0\)인 조합에도 적용된다. 검증 코드에 실제 \(P_j\)의 유리수 조합으로 만든 경계 소거 입력을 포함했다.
2. **차수 순서:** \(\lambda_m\)의 \(m\)-의존성을 버리지 않는다. \(m\to\infty\)와 \(\lambda\to\infty\)를 교환하지 않았다.
3. **양쪽 꼬리 및 jump:** (5.2)에 서로 반대 꼬리의 겹침을 포함했다. BV jump의 Fourier 에너지도 (4.1)–(4.2)에 포함된다.
4. **산술 문턱:** (5.4)는 실수 \(N\)에 균일하다. 소수가 아닌 정수까지의 상계는 꼬리 오차 제어에만 쓰며, (2.1)의 실제 소수 공동 소거를 대체하지 않는다.
5. **Schur 응답 누락:** \(0<\epsilon<1\)에 대해
   \[
   A_\epsilon=\begin{pmatrix}\epsilon^4&2\epsilon^2\\2\epsilon^2&1\end{pmatrix}
   \]
   는 두 대각 블록이 양수이고 첫 방향의 에너지·잔차가 모두 0으로 가지만, 그 블록을 제거한 Schur 보완은 정확히 \(-3\)이다. 이는 일반 논리의 반례이며 실제 산술 연산자의 반례라고 주장하지 않는다.
6. **ground 선택:** \(\operatorname{diag}(\epsilon^4,-1)\)의 첫 방향은 양의 작은 에너지와 잔차 0을 가지지만 ground가 아니다. 작은 에너지의 근사 벡터를 ground로 승격하지 않는다.
7. **가중 비교의 등호:** (8.4)의 실제 source 방향 때문에 전체 비교에 임의의 양의 여유를 추가할 수 없다. 이 결과를 모든 RH 방법의 불가능성으로 확대하지 않는다.

## 10. 검증과 재현

`code/verify_source_schur.py`는 표준 Python의 정확한 `Fraction` 연산만 사용한다. 다음을 검사한다.

- 도함수 다항식 recurrence, 최고차항, Mellin 미분 관계;
- 다항식 노름에 쓰인 적분 Gram 행렬과 정확한 LDL 분해;
- 실제 도함수 다항식 조합의 여러 경계 소거;
- source 변환과 Schur congruence의 유리수 행렬 항등식;
- 작은 잔차와 양의 두 대각 블록이 전체 양성을 주지 않는 반례.

이 검산은 유한 대수·반례 검사이다. 실제 Weil 고유값, 실제 gap, (OPEN-S), (OPEN-D)를 수치 인증하지 않는다. 무한차원 부등식의 근거는 §2–6의 일반 증명이며, 그 분석적 도메인 조건을 유한 검산으로 대체하지 않는다.

이번 실행에서 **72/72개의 정확 유리수 검사가 통과**했다. 실제 Weil gap 인증 개수와 전체 Schur 양성 인증 개수는 모두 0으로 기록했다.

실행:
```bash
python3 code/run_verification.py
python3 code/build_package.py
```
입력 원문, 정의 JSON, 코드, 로그, 결과 JSON, SHA-256 manifest를 패키지에 포함한다.

## 11. 최초의 남은 부등식과 최종 상태

새로 제어한 항은 **고정 유한 source 공간의 교차항 전체**다. (T1)은 그 공간을 실제로 양수 블록으로 만들지만, 그 밖의 상태에 대한 ground 배제는 하지 못한다.

최초의 남은 실제 연산자 부등식은 (OPEN-S), 즉
\[
\mathsf C\succeq R\mathsf B^{-1}R^*
\]
이다. 전체 차이 제곱 비교 공격에서는 (OPEN-D)가 남았고, 고정 소수 기여를 버리거나 등호보다 강한 균일 Poincaré 여유를 요구하는 가지는 정확한 source 포화 때문에 HOLD다.

`FIXED_SOURCE_SUBSPACE_POSITIVITY = PROVED-IN-REPORT`  
`ACTUAL_FULL_SCHUR_POSITIVITY = NOT-OBTAINED`  
`ACTUAL_GAP_AND_ALIGNMENT_RATIO = NOT-OBTAINED`  
`RH_PROOF = NOT-OBTAINED`.
