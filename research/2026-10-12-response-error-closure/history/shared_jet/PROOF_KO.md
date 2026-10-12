이번 준비의 결론은 공통 좌표를 유지하는 유리수 jet 포함식과 complete form 결합의 조건부 정당성이다. 실험 횟수는 11이고, 기존 저장 패킷의 산술 PASS 및 과학 HOLD를 유지한다. 실제 연구 셀에서 다항식 값·도함수·Γ·θ·prime을 새로 평가하지 않았다. 아래 실제 입력을 넣는 공식은 증명과 미래 검증 조건이며 이번 실행은 합성 fixture에만 적용했다.

**고정 대상과 좌표.** 고차 방향은 현재 코드의 같은 유한 다항식

\[
 F(x)=\sum_{m=32,34,\ldots,128} C_m P_m(x/B),\qquad B=3/4
\]

이다. 49개 C_m은 이미 저장된 `norm_trace.physical_fhat_coefficients`의 포함 구간을 사용한다. 코드상 정의는 원래 saved prefix coefficient를 sqrt(2B)로 나눈 것이며, 새 정규화나 고차 source extension을 넣지 않는다. low16은

\[
 E_j(x)=s_j P_{2j}(x/B),\quad s_j=\sqrt{(4j+1)/(2B)},\quad 0\le j<16
\]

으로 최대 차수 30이다. F의 차수 128은 이 유한 방향의 차수다. 원래 inverse의 미계산 tail이나 complete Γ tail을 0으로 놓는 주장이 아니다.

같은 native 셀 [l,r]의 모든 vertex에 하나의 t∈[-1,1]를 쓴다.

\[
 y_c=(l+r)/2,\quad h=(r-l)/2,\quad y=y_c+ht,
 \quad z_v(t)=\{L_c+S_v+\ell_c y_c\}/B+(\ell_c h/B)t.
\]

L_c, S_v, ell_c와 모든 parameter는 실제로는 셀 안에서 고정된 값이며 그 저장 구간이 불확실성을 감싼다. Jet coefficient interval이 이 고정 parameter의 가능한 값을 감싸도록 한다. 모든 vertex, F, E와 후속 곱·합은 같은 source_context/component/cell/[l,r] 좌표를 유지하며, 다른 셀이나 order를 섞으면 코드가 거부한다. 상수 parameter 사이의 추가 상관은 이번 표현에서 더 넓은 포함으로 지불한다.

**차수16과 엄밀 나머지.** vertex의 affine offset box A_v와 slope box D_v에 대해 q_v=mid(A_v)를 정확한 유리수 중심으로 정한다. z_v=q_v+eta_v+d_v t이며 eta_v∈A_v−q_v, d_v∈D_v이다. 보수적인 displacement는 delta_v=rad(A_v)+mag(D_v)다. affine 전체 구간이 [-1,1]에 포함되는 것을 요구한다. Taylor 계수는 F를 먼저 결합한 후

\[
 b_{v,k}=\sum_m C_m P_m^{(k)}(q_v)/k!,\qquad
 T_{v,16}(t)=\sum_{k=0}^{16}b_{v,k}(\eta_v+d_vt)^k
\]

로 만든다. 각 b와 affine 조합의 coefficient interval을 정확한 유리수 연산으로 포함시킨다. 실제 q_v의 b_{v,k} 값을 이번 작업에서 평가하지 않았다. `prefix_taylor`는 합성 중심과 합성 coefficient만으로 검사했다.

Jacobi 도함수 식을 k회 적용하면

\[
 P_m^{(k)}(z)=2^{-k}(m+1)_k P_{m-k}^{(k,k)}(z).
\]

k≥0의 Jacobi 최대값 부등식은 [-1,1] 전체에서 적용되므로

\[
 \sup_{[-1,1]}|P_m^{(k)}|
 \le D_{m,k}=\frac{(m+k)!}{2^k k!(m-k)!},\quad k\le m;
 \qquad D_{m,k}=0\ (k>m).
\]

이는 [NIST DLMF 도함수 식 18.9.15](https://dlmf.nist.gov/18.9#E15)와 [Jacobi 최대값 및 그 적용 조건 18.14.1](https://dlmf.nist.gov/18.14#E1)을 α=β=k로 적용한 결과다. k≥0은 α≥β>−1 및 α≥−1/2 조건을 만족한다.

따라서 Taylor 정리와 삼각부등식으로 실제 모든 coefficient/geometry 값과 t에 대해

\[
 |F(z_v(t))-T_{v,d}(t)|
 \le\rho_{v,d}
 =\frac{\delta_v^{d+1}}{(d+1)!}
   \sum_m\operatorname{mag}(C_m)D_{m,d+1}.
\]

coefficient·정규화 불확실성은 Taylor coefficient interval 및 mag(C_m) 양쪽에 포함돼 있다. d=128이면 이 유한 다항식의 나머지는 정확히 0이다. 준비 default는 d=16이며 나머지를 버리지 않는다. low16도 같은 공식을 사용하거나 차수30 전체 finite representation을 보존할 수 있다. source-free test는 degree128의 정확한 recurrence coefficient를 독립 Rodrigues 계수식과 비교하고, 정확한 합성 다항식 값이 Taylor 나머지 이내임을 검사했다. defining recurrence는 [NIST DLMF Table18.9.1](https://dlmf.nist.gov/18.9#T1)과 같다.

**Jet 포함식과 곱.** Jet J=(A_0,...,A_d;rho)는 실제 함수 u(t)에 대해 고정 실제 coefficient a_k∈A_k 및 잔차 함수 epsilon(t)가 존재해

\[
 u(t)=\sum_{k=0}^d a_k t^k+\epsilon(t),\qquad |\epsilon(t)|\le\rho
\]

라는 뜻이다. 두 polynomial 부분을 같은 t로 convolution한 interval coefficient를 V_k라 하고, P=Σmag(A_k), Q=Σmag(B_k)라 하면 product의 low d coefficient는 V_0..V_d이며 새 나머지는

\[
 \rho_{uv}=\sum_{k=d+1}^{2d}\operatorname{mag}(V_k)
       +\rho_u Q+\rho_v P+\rho_u\rho_v.
\]

증명은 polynomial product의 버린 고차항에 |t|≤1을 적용하고, p epsilon_v + q epsilon_u + epsilon_u epsilon_v를 각각 감싸는 것이다. 덧셈은 coefficient를 더하고 두 나머지를 더한다. 합과 convolution을 수행한 뒤에 range나 integral enclosure로 내려가므로 공통 좌표의 polynomial cancellation을 유지한다. interval coefficient의 서로 다른 불확실성과 remainder 사이의 상관을 가정하지 않는다. F/E의 product에서 원래 생기는 차수158·256 및 모든 input 나머지 교차항도 이 규칙으로 포함된다.

**변동 Γ와 적분의 필수 조건.** saved complete Γ box [a,b]는 전체 셀의 변동 함수값을 감싼다. 이 함수는 고정 coefficient [a,b]가 아니다. 정확한 midpoint (a+b)/2와 변동 remainder (b−a)/2로 Jet에 넣어야 한다. 예를 들어 Γ(t)=t이면 Γ(t)t의 평균은 1/3인데, [−1,1]을 고정 coefficient로 취급해 [−1,1]t의 홀수항 평균을 0으로 만드는 것은 잘못이다. 합성 회귀가 이 오류를 검출한다. `Jet.varying_box`는 Γ의 전체 셀 변동·입력·저장 outward error를 나머지에 남긴다. 새로운 Γ derivative나 Γ 값은 평가하지 않는다.

고정 polynomial coefficient에 대해서는

\[
 \tfrac12\int_{-1}^1t^kdt=0\ (k\text{ odd}),\quad
 \tfrac12\int_{-1}^1t^kdt=1/(k+1)\ (k\text{ even}).
\]

그러므로 전체 평균은 Σ A_{2k}/(2k+1)+[−rho,rho]로 포함된다. arbitrary varying remainder의 평균은 [−rho,rho]를 그대로 지불한다. dx=ell_c h dt이므로 physical cell integral은 평균 구간 × ell_c(r−l)이다. Jacobian은 1회다. 기록의 centre=(lo+hi)/2와 complete_eta=(hi−lo)/2는 모든 coefficient, input, geometry, truncation, Γ 변동 나머지를 지불한 적분 구간의 값이다. 이 새 method는 `synthetic_shared_coordinate_jet_average_v1`로 표기한다. 기존 `whole_cell_box` packet으로 위장하지 않는다.

**기존 complete form과 결합.** 모든 vertex에서 같은 f_v/E_vj와 저장된 양·음 두 거리의 complete Γ box를 사용해

\[
 M_{vv}=a+\kappa+\omega(V_v^++V_v^-),\quad
 M_{uv}=M_{vu}=-c_{uv}
\]

를 만든다. seven/path/pair의 기존 모든 prime edge를 유지한다. 실제 primitive inclusion 및 M(t)≥a_*I>0은 원래 analytic/source/domain 전제다. 합성 code에서는 diagonal lower minus offdiagonal absolute row sum≥a_*를 실제 interval로 검사해 충분한 coercivity certificate를 준다. 이 조건은 quadratic form에서 2|u_vu_w|≤u_v²+u_w²를 적용하면 증명된다. 합성 certificate가 실제 연구 source의 coercivity proof를 새로 증명한다는 뜻은 아니다.

같은 Jet 객체들로

\[
 g=a f-E\alpha,\quad r_v=g_v-(Mc_0)_v,
 \epsilon= a_*^{-1}\sum_v\sup_{t\in[-1,1]}|r_v(t)|
\]

를 감싼다. 실제 u=M^{-1}g에 대해

\[
 \|u-c_0\|_2\le a_*^{-1}\|g-Mc_0\|_2
 \le a_*^{-1}\sum_v\sup_t|r_v(t)|=\epsilon.
\]

각 u_v는 c_{0,v}+변동 remainder epsilon으로 모델링한다. 실제 inverse를 계산하거나 이전 low-only response error를 재사용하지 않는다. 이 변동 remainder를 고정 coefficient처럼 적분해 상쇄하면 안 된다.

complete targets는

\[
 \chi_j=\sum_c\int E_{c,j}^TM_cf_c\,dx+\chi_{j,\rm endpoint},\quad
 A_g=\sum_c\int f_c^TM_cf_c\,dx+A_{g,\rm endpoint},
\]
\[
 \beta_j=\sum_c\int E_{c,j}^Tu_c\,dx+\beta_{j,\rm endpoint},\quad
 W=\sum_c\int u_c^T(E_c\chi)\,dx+W_{\rm endpoint},
\]
\[
 H=A_g+2\ell^2,\qquad R=W-2\sigma\ell
\]

이다. polynomial convolution → sum → rigorous physical integral 순서로 같은 좌표를 유지한다. global χ는 endpoint까지 합산한 full χ이며 이후 모든 residual target에 같은 full χ packet을 결합해야 한다. complete endpoint strip·로그 tail bounds, whole signed σ/ell, H coercivity intersection은 기존 전제와 source binding을 유지한다. pole square와 pole cross는 각각 global 1회다. R이 0을 포함하면 HOLD를 유지하고 s0·Ψ 분기로 가지 않는다.

이로써 개별 Jet 포함과 원래 complete primitives/coercivity/domain 전제가 만족될 때 기존 full targets를 포함하는 결합의 수학적 정당성이 증명된다. 실제 packet authoring, native row SHA/manifest verifier 변경, 실제 centre coefficient 생성 및 production admission은 구현하거나 실행하지 않았다. 합성 source_context와 synthetic-only guard를 실제 packet으로 바꿔 쓰는 것은 허용되지 않는다.

**저장 자료로 가능한 정량 경계와 최초 미증명 조건.** 실제 centre-jet 값을 만들지 않고 저장된 C_m magnitudes와 4,416개 셀의 physical X box 폭만 읽었다. 기존 native geometry 포함 검증을 전제로, rational vertex centre가 같은 X box 안에 있으므로 width(X)/B는 그 centre로부터의 모든 실제 displacement를 감싸는 보수적 상계다. full width를 사용해 uncertain centering/geometry를 지불했다. 양의 length, normalized y_c≥h, 기존 geometry enclosure에서는 canonical affine midpoint의 rad(A)+mag(D)도 이 full width 상계 이내다.

차수16의 component-wise uniform fhat 나머지 상계는 seven 3.12196135349e-24, path 4.30993460679e-21, pair 8.36843129960e-49다. 이 나머지가 forcing와 response를 통해 W에 전달되는 부분만, 기존 E/χ envelopes를 그대로 사용해

\[
 C_F=\sum_{\rm cells}\ell\Delta y\,
       (a_{\rm hi}/a_*)\Bigl(\sum_v\rho_v\Bigr)
       \sum_{v,j}\operatorname{mag}(E_{vj})\operatorname{mag}(\chi_j)
 \le1.25230821731545\times10^{-26}
\]

으로 감쌀 수 있다. 이는 F 나머지의 response 경로 부분상계다. F 나머지가 new χ/Ag에 전달되는 오차나 forcing의 central residual 등 전체 budget이 아니다.

Γ가 interval midpoint에서 벗어나는 부분이 Mc0에 전달되는 상계도 저장 자료로 계산했다.

\[
 C_\Gamma=\sum_{\rm cells}\ell\Delta y\,
 \frac{|\omega|}{a_*}\sum_v|c_{0,v}|(\operatorname{rad}V_v^++\operatorname{rad}V_v^-)
 \sum_{v,j}\operatorname{mag}(E_{vj})\operatorname{mag}(\chi_j)
 \le4.75115215769736\times10^{-19}.
\]

이 상계가 기존 중심보다 크므로 이 보수적 budget만으로 부호를 인증하지 못한다. Γ 오차의 실제 하한이나 개선 불가능성 증명으로 해석하지 않는다.

기존 R 중심은 m=1.49367005074320358758e-19, 반경은 rho=2.13337537200550624235e-14다. 중심이 고정된다는 설계 가정 아래 rho_new<|m|, 따라서 감소배수>142827.7530867011가 필요하다. integer factor 142828은 그 고정 중심 조건을 만족하는 최소 정수다. 99.7233387444643% response 항을 완전히 제거해도 남은 반경은 5.9022230894794060e-17, 즉 중심의 395.1490549431배다. response만 줄여서는 이 고정-envelope 판정이 되지 않는다.

최초 미증명 조건은 같은 geometry/M/c0/F/E source에 결합된 실제 degree0..16 centre-jet/forcing residual 포함 자료가 완전한 new χ/Ag/E product/Γ remainder/endpoint/global R budget을 제공해 0을 제외한다는 것이다. 이번 검증을 마친 fhat FORM stream에는 실제 centre-jet 계수 field가 없으며, 이번 작업에서는 실제 중심의 다항식·도함수를 새로 평가하지 않았다. 계수와 geometry는 유한 다항식의 centre coefficients를 이론상 결정하므로, 이 자료로 정밀 계산이 영원히 불가능하다는 정보론적 주장을 하지 않는다. 현재 허용된 저장 magnitude/width 상계와 합성 준비만으로 충분한 전체 정량 경계가 증명되지 않았다는 결론이다. 중심이 움직이면 |m_new−m_old| 상계와 rho_new의 합이 |m_old|보다 작다는 충분 조건을 증명하거나 m_new−rho_new>0를 직접 인증해야 한다. 기존 interval midpoint는 실제 residual의 부호나 새 centre가 유지된다는 증거가 아니다. 일반 포함식과 합성 회귀 준비는 완료했지만 전체 정량 부호 인증과 생산 준비는 HOLD다.
