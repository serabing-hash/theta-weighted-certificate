# A full-response shift-reuse lemma and its limits

Status: analytic lemma proved below; the fixed candidate completed one conditional computational PASS. The unchanged pre-execution version is frozen/PROOF.md. RH_PROOF=NOT-OBTAINED.

## 1. Fixed operator and data

Let `L` be the same minimum self-adjoint theta realization specified in SOURCE_MAP and ASSUMPTIONS_AND_LIMITS, with form domain `D`. Let `O:C^m→H` be its fixed observation map (`m=372`). Fix

\[
\delta_0=1/64,\quad H_0=L+\delta_0I+OO^*,\quad H_0\ge\eta I>0.
\]

Let `V:C^r→D(H0)`, `r=68`, be the admitted trial map, and `G:C^r→H` its full-line action proxy. Put

\[
E=H_0V-G,\quad \|V\|\le\nu_0,\quad
\|E\|\le\bar\sigma,\quad \|E\|^2\le s^2.
\]

Here `s²` is the archived sum of squared deterministic column action errors, and `bar_sigma` is an archived certified upper square root. These are distinct accepted scalar bounds, not newly sampled errors. Fix any coefficient matrix `C:C^m→C^r`; it need not be optimal, invertible, or solve a normal system. In the proposed application it is the exact saved `C.json`.

Use the following symbols, avoiding confusion between the operator `A` and observation Gram:

\[
M=O^*O,\quad D_0=V^*O,\quad F=\operatorname{sym}(V^*G),
\quad K=G^*O,\quad N=G^*G,\quad P=V^*V.
\]

The archive calls `M` role `A`, `D0` file `D68`, `F` file `E68`, `K` file `K68`, `N` file `N68`. In particular `E68` is not the action-error matrix `E`. The original files have real entries. The statements also hold for complex Hilbert spaces with adjoints as displayed.

## 2. General deterministic response bound

For a positive self-adjoint `H>=a I`, admitted `V`, `G=HV−E` with the above norm bounds, and `Y=VC`, expansion gives the exact finite-operator identity

\[
O^*H^{-1}O=O^*Y+Y^*O-Y^*HY
 +(O-HY)^*H^{-1}(O-HY). \tag{1}
\]

All terms are defined since `Y` takes values in the operator domain; the inverse is bounded on the whole Hilbert space. No action of `H` on `G` or `O` is used.

For every coefficient vector `z`,

\[
|\langle VCz,ECz\rangle|
 \le\nu_0\bar\sigma\|Cz\|^2.
\]

Self-adjointness of `H` gives `V*HV=F+sym(V*E)`. Hence the model error in the negative quadratic term of (1) is at most `nu0*bar_sigma C*C`. Put `R=O−GC`. For any fixed `tau>0`, Young's inequality gives

\[
\|(R-EC)z\|^2\le(1+\tau)\|Rz\|^2
 +(1+1/\tau)s^2\|Cz\|^2.
\]

Using `H^{-1}<=a^{-1}I` in (1), one obtains

\[
O^*H^{-1}O\preceq
C^*D_0+D_0^*C-C^*FC
 +\alpha (O-GC)^*(O-GC)+\beta C^*C, \tag{2}
\]

where `alpha=(1+tau)/a` and `beta=nu0*bar_sigma+(1+1/tau)s²/a`. This is a Loewner inequality on all `C^m`, for every frozen `C`.

## 3. Shift-reuse lemma

**Lemma.** Suppose `0<h<eta`. Keep `O,V,C` fixed and define

\[
H_h=H_0-hI,\quad\eta_h=\eta-h,
\quad G_h=G-hV.
\]

Then `D(Hh)=D(H0)=D(L)`, `Hh>=eta_h I`, and

\[
H_hV-G_h=E. \tag{3}
\]

With

\[
\alpha_h=\frac{1+\tau}{\eta_h},\qquad
\beta_h=\nu_0\bar\sigma+\frac{(1+1/\tau)s^2}{\eta_h},
\]

define

\[
\begin{split}
B_h&=\alpha_h K-(1+\alpha_hh)D_0,\\
\overline S_h&=\alpha_h N-(1+2\alpha_hh)F\\
&\quad+\bigl[\beta_h+(h+\alpha_hh^2)\nu_0^2\bigr]I_r,\\
\overline U_h(C)&=\alpha_h M-B_h^*C-C^*B_h
 +C^*\overline S_h C.
\end{split} \tag{4}
\]

Then

\[
O^*H_h^{-1}O\preceq\overline U_h(C). \tag{5}
\]

In particular the right side needs only the five first-action Grams `M,D0,F,K,N`, the trial norm bound and the existing action-error bounds. No second action or full entrywise `P` enclosure is required.

**Proof.** A bounded scalar perturbation leaves the self-adjoint operator domain and its form domain unchanged. Positivity and (3) follow by direct subtraction on this fixed domain. The shifted Grams satisfy the exact identities

\[
F_h=F-hP,\qquad K_h=K-hD_0,\qquad
N_h=N-2hF+h^2P. \tag{6}
\]

Apply (2) with `Hh,Gh,eta_h`. Expanding its residual square and collecting coefficients gives

\[
\begin{split}
O^*H_h^{-1}O\preceq{}&\alpha_h M-B_h^*C-C^*B_h+C^*S_hC,\\
S_h={}&\alpha_hN-(1+2\alpha_hh)F
 +(h+\alpha_hh^2)P+\beta_hI_r.
\end{split} \tag{7}
\]

Since `P<=nu0² I` and **`h+alpha_h h²>0`**, replacement of `P` by `nu0² I` increases the right side in Loewner order. This proves (4)–(5). No sign assumption on `F`, `S_h` or `Sbar_h` was made. ∎

The norm replacement can lose margin. The proof establishes validity, not sharpness or successful closure for the proposed candidate. It also explains why a separately named optimal coefficient theorem is unnecessary here: `C` is already frozen and arbitrary in (2).

## 4. Outward enclosure and a full positivity witness

Accept the source interval enclosures only under N1–N3. Evaluate (4) by signed outward interval operations, preserving every physical radius and all new rounding radii. The negative multiplier of `F` must reverse its endpoints. Center matrices are symmetric and radius matrices are nonnegative and symmetric after conservative symmetrization.

If the resulting interval has center `Uc` and radii `r_ij`, set

\[
U_{\rm cert}=U_c+\operatorname{diag}\bigl(\sum_j r_{ij}\bigr).
\]

For a Hermitian error `Delta` with `|Delta_ij|<=r_ij`,

\[
z^*\Delta z\le\sum_{ij}r_{ij}|z_i||z_j|
\le\sum_i(\sum_jr_{ij})|z_i|^2.
\]

Thus `Ucert>=Ubar_h`. This uses all372 coordinates. Replacing the interval by entrywise upper endpoints alone would not prove a Loewner upper bound.

A fresh witness for `T=I_m−Ucert` may consist of a unit-lower rational `L0`, positive diagonal `D0fac`, and approximate inverse factor `M0`. If exact checks give

\[
\begin{gathered}
\|T-L_0D_{0\rm fac}L_0^*\|_2\le\rho,\quad
e_1=\|L_0M_0-I\|_1<1,\quad
e_\infty=\|L_0M_0-I\|_\infty<1,\\
m_1=\|M_0\|_1,\quad m_\infty=\|M_0\|_\infty,
\quad d=\min_i(D_{0\rm fac})_{ii}>0,
\end{gathered}
\]

then

\[
\mu_1=\frac{d(1-e_1)(1-e_\infty)}{m_1m_\infty}-\rho>0 \tag{8}
\]

certifies `T>=mu1 I`. Indeed `L0^{-1}=M0(I+(L0M0−I))^{-1}`, and the1/∞ norm bounds control `||L0^{-1}||2²`. The residual norm may be bounded by the exact maximum absolute row sum for the symmetric residual. This is the same valid finite-witness mechanism as the inherited checker; the shifted target requires a new witness and new checks.

For `0<mu1<=1`, (5) and (8) imply on the original form domain

\[
L+(\delta_0-h)I=H_h-OO^*
 \ge\mu_1H_h\ge\mu_1(\eta-h)I. \tag{9}
\]

To justify the first inequality, let `B=Hh^{-1/2}O`. The response bound gives `||B||²<=1−mu1`, hence `||O*f||²<= (1−mu1)||Hh^{1/2}f||²` for every form-domain `f`. No maximal-domain identification or compression to a trial subspace occurs.

## 5. Why scalar continuity alone gives the old lower bound

Let the inherited complete response certificate be

\[
O^*H_0^{-1}O\preceq(1-\mu_0)I,
\quad 0<\mu_0<1,\quad\delta_*=\mu_0\eta.
\]

Functional calculus for `H0>=eta I` gives, for `0<=h<eta`,

\[
H_h^{-1}\preceq\frac{\eta}{\eta-h}H_0^{-1}.
\]

It follows that

\[
I-O^*H_h^{-1}O\succeq
 \frac{\delta_*-h}{\eta-h}I. \tag{10}
\]

For `h<delta_star`, (9) with this margin reads

\[
L+(\delta_0-h)I\ge(\delta_*-h)I,
\quad\text{hence}\quad L\ge(-\delta_0+\delta_*)I.
\]

There is exactly no improvement. At `h=delta_star` this scalar response margin is zero. Beyond it, (10) supplies no positive response margin. This is a limitation of using just those two scalar bounds; it is not a nonpositivity result for the actual response matrix.

## 6. A candidate that tests actual improvement

Fix **`h=2*delta_star`**, with `delta_star` the exact archived rational product. The saved certificate states `0<mu0<1/100`, while `0<eta<delta0`. Therefore

\[
0<h=2\mu_0\eta<\eta,\qquad
\delta_1=\delta_0-2\delta_*>0.
\]

Freeze `tau=1/100`, the existing68 trials and proxy definitions, the original372 observation order, and the original `C.json`. If one evaluation of (4) and one complete positivity verification give `mu1>0`, then (9) yields

\[
L\ge[-\delta_0+2\delta_*+\mu_1(\eta-2\delta_*)]I.
\]

The difference from the inherited lower bound is

\[
\delta_*+\mu_1(\eta-2\delta_*)>0.
\]

Thus success cannot merely restate the old bound. The one execution recorded in evidence/timed/math/INDEPENDENT_CHECK.json established mu1>0 and the displayed strict improvement, conditional on A1–A4/N1–N4. EXACT_RESULT_VALUES.json contains the verbatim exact values. No physical inclusions were regenerated. Failure of this specific conservative witness gives no converse spectral claim. The unchanged cover also has the positive error floor `d_sharp+epsilon_cover`; this single test cannot be iterated toward zero without new evidence.

## 7. Relation to the original source-orthogonality question

The proof is a finite response verification mechanism for the same `L`, valid on its whole form domain. The completed conditional bound therefore also applies to `D∩N_perp`. It does not use full `N` orthogonality to prove a new universal coercivity estimate, does not assume `N=ker L`, and does not settle the earlier projected trace/energy problem. The completed result consists of the reuse lemma, the no-gain scalar-continuity calculation, and one strict improvement verified in all372 coordinates. The new lower edge remains negative. The spectral premises remain explicitly conditional, and no bibliographical novelty claim is made.
