# Analytic appendix: the fixed three-eighths certificate

Jongmin Choi — 26 October 2026 (KST)

This appendix supplies the analytic implication of the saved fixed-parameter certificate. It is a newly edited English mathematical exposition, not a byte-identical copy of earlier working notes. `SOURCE_ORIGINS.json` records the source hashes and editorial scope. Numerical enclosures are premises supplied by the accompanying evidence, not recomputed here. The classical theorems and arithmetic trust boundary are identified explicitly below. No review-status label is a mathematical premise.

## A. Kernel, measure, and the minimum closed realization

Inner products are conjugate-linear in the first variable. For $x\geq0$, put

$$
 t_n(x)=\pi n^2e^{2x},\qquad
 \kappa(x)=e^{x/2}\sum_{n\geq1}(4t_n(x)^2-6t_n(x))e^{-t_n(x)},
 \qquad C(x)=\cosh(x/2).
$$

Use its smooth even theta continuation. The theta transformation, termwise differentiation of normally convergent series, and Mellin integration give

$$
 \widehat\kappa(z)=\int_{\mathbb R}\kappa(x)e^{izx}dx
 =\xi(1/2+iz),\qquad
 \xi(s)=\tfrac12s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s).
$$

Indeed $h(x)=e^{x/2}\sum_{n\geq1}e^{-\pi n^2e^{2x}}$ satisfies
$\kappa=(\partial_x^2-1/4)h$; Mellin integration first in its absolute-convergence half-plane, followed by two integrations by parts and the theta transformation at the other endpoint, gives the displayed normalization. In particular
$\int\kappa C=\xi(1)=1/2$. Each summand of $\kappa$ on the positive half-line is positive. Every fixed derivative decays faster than every exponential. Set

$$
 d\nu=2\kappa C\,dx,\quad H=L^2_{\mathrm{even}}(\mathbb R,\nu),
 \quad m=\frac{2C}{\kappa},\quad w=\frac1m=\frac{\kappa}{2C}.
$$

Thus $\nu$ is a probability measure. The elementary envelopes used throughout are

$$
 k e^{9x/2-\pi e^{2x}}\leq\kappa(x)\leq K e^{9x/2-\pi e^{2x}},
 \quad k=4\pi^2-6\pi,\quad
 K=4\pi^2\sum_{j\geq1}j^4e^{-\pi(j^2-1)}.                 \tag{A.1}
$$

The first summand gives the lower bound; discard the negative part of each summand and use $e^{2x}\geq1$ for the upper bound.

Define $a_n=\Lambda(n)/\sqrt n$, $s_n=\log n$,
$\rho(s)=e^{-s/2}/(1-e^{-2s})$, and
$d\mathfrak j(s)=\rho(s)ds+\sum_{n\geq2}a_n\delta_{s_n}(ds)$.
The initial form on even compact smooth functions is

$$
 \mathcal E_0(f)=\int_{s>0}\int_{\mathbb R}
 \kappa(x)\kappa(x+s)|f(x+s)-f(x)|^2dx\,d\mathfrak j(s). \tag{A.2}
$$

Positive shifts are counted **once**. The operator $A$ in this work is the self-adjoint operator of the **minimum closed form** obtained by closing (A.2) in $H$. It is not an unspecified maximal finite-energy realization, nor an odd-sector operator.

For completeness, the difference map into the edge $L^2$ space is closable. If $f_j\to0$ in $H$ and the differences are Cauchy in that space, choose an almost-everywhere convergent subsequence. The measures $\nu$ and Lebesgue measure have identical null sets. Fubini for continuous shifts and translation invariance of Lebesgue null sets for each of the countably many atomic shifts imply that the edge limit is zero. The representation theorem for closed nonnegative forms therefore applies, and $A\geq0$.

The constant really belongs to this realization. Choose even compact smooth cutoffs $\chi_R\to1$, uniformly bounded between zero and one with uniformly bounded first derivatives. Then $\chi_R\to1$ in $H$. Their differences are bounded by a constant times $\min(s,1)$. Small shifts are dominated using $\int_0^1s^2\rho(s)ds<\infty$. Large shifts and prime atoms are dominated by

$$
 \int|u(x)v(x+s)|dx\leq e^{-|s|}
 \|e^{|x|}u\|_2\|e^{|x|}v\|_2,
 \qquad\sum_{n\geq2}\Lambda(n)n^{-3/2}<\infty.
$$

Dominated convergence applies also to differences of cutoffs. Consequently $1\in\operatorname{Dom}\mathcal E$, $\mathcal E(1)=0$, and form Cauchy–Schwarz gives $\mathcal E(1,g)=0$ for every form-domain $g$. The representation theorem yields $1\in\operatorname{Dom}A$, $A1=0$, and $\|1\|_H=1$.

## B. Source identity and the original weighted congruence

Write $\tau_su(x)=u(x+s)$, and define, on the functions for which the expressions converge,

$$
 D_\Gamma(u,v)=\int_0^\infty\rho(s)\langle u-\tau_su,v-\tau_sv\rangle_2ds,
$$
$$
 Q_{\rm inv}(u,v)=D_\Gamma(u,v)-c_\Gamma\langle u,v\rangle_2
 -\sum_{n\geq2}a_n(\langle u,\tau_{s_n}v\rangle_2+
                         \langle\tau_{s_n}u,v\rangle_2),
$$
$$
 c_\Gamma=\log\pi-\psi(1/4)=\log\pi+\gamma_E+\pi/2+3\log2,
 \quad\mu(u)=\int C u,\quad Q_{\rm full}=Q_{\rm inv}+2\overline{\mu(u)}\mu(v).
$$

These definitions alone make no claim of a global self-adjoint ordinary-$L^2$ realization of $Q_{\rm inv}$.

**Classical input used here.** The polarized compact-test Riemann–Weil explicit formula, in this normalization, identifies $Q_{\rm full}$ with its zero-distribution pairing. If $z$ ranges over zeros of $\Xi(z)=\xi(1/2+iz)$ with multiplicity, that pairing for even tests can be written
$\sum_{\Xi(z)=0}\overline{\widehat u(\bar z)}\widehat v(z)$, with the usual symmetric limiting interpretation before absolute convergence is available. The formula is not a positivity assumption: $z$ is not assumed real. The general explicit formula and the classical bound $N(T)=O(T\log(T+2))$ are external classical inputs, not results proved by the numerical certificate. See the primary and authoritative references in §J.

The archimedean normalization can be checked independently: the finite difference between the coupled archimedean subtraction and the Gamma difference expression is

$$
 2\int_0^\infty\frac{e^{s/2}-1}{e^s-e^{-s}}ds
 =4\int_0^1\frac{dt}{(1+t)(1+t^2)}=\pi/2+\log2.
$$

Together with $\log(4\pi)+\gamma_E$, this is exactly $c_\Gamma$. No divergent integral is split into individually meaningful pieces.

Apply the polarized formula to smooth cutoffs of $\kappa$ and a fixed compact smooth test. Weighted derivative convergence and integrations by parts give uniformly summable transform products on the zero strip; the stated zero count justifies passage to the limit. The transform of $\kappa$ vanishes at each zero, including nonreal zeros. Thus $Q_{\rm full}(\kappa,v)=0$, not merely $Q_{\rm full}(\kappa,\kappa)=0$. The pole row is $C$, since $2\int\cosh((x-y)/2)\kappa(y)dy=C(x)$. It follows that

$$
 L_{\rm phys}\kappa=-C,\qquad
 L_{\rm phys}u=\int_0^\infty\rho(s)(2u-\tau_su-\tau_{-s}u)ds
 -c_\Gamma u-\sum a_n(\tau_{s_n}u+\tau_{-s_n}u).            \tag{B.1}
$$

On compact $x$-sets the symmetric Gamma numerator is $O(s^2)$ at zero; the prime summands at infinity are bounded by a polynomial times $e^{-c n^2}$. The same holds for fixed derivatives. Hence the distributional row is continuous and (B.1) holds pointwise.

For later use put $H_b=(\kappa(\cdot+b)+\kappa(\cdot-b))/2$, $c_b=\cosh(b/2)$. Translation invariance of the row gives $L_{\rm phys}H_b=-c_bC$. Its transform is $\cos(bz)\Xi(z)$; equivalently the same polarized argument applies. Also $\mu(H_b-c_b\kappa)=0$.

Expanding the jump squares and using (B.1) gives on the defining core

$$
 \mathcal E(f,g)-\tfrac12\langle f,g\rangle_H
      =Q_{\rm inv}(\kappa f,\kappa g),\qquad
 \|f\|_H^2=\int m|\kappa f|^2.                           \tag{B.2}
$$

Equivalently $\mathcal E(f)=Q_{\rm full}(\kappa f)+\operatorname{Var}_\nu(f)/2$; its two rank-one terms cancel because $\mu(\kappa f)=\tfrac12\int f\,d\nu$.

For $I_R=(-R,R)$, the killed domain is the closure of even compact smooth tests strictly inside $I_R$, zero extended. Exterior jumps remain in the energy. At fixed $R$, $\kappa,m$ and their inverses are bounded; the scalar, compressed-prime, and metric terms are bounded $L^2$ forms. Thus multiplication $J_Rf=\kappa f$ identifies the actual minimum killed closures and extends (B.2). It is an invertible form **congruence**, not a unitary map into ordinary $L^2(dx)$. It is norm-preserving into $L^2(mdx)$.

Sharp restrictions and the cell functions below belong to the minimum form domain. A boundary-layer smoothing error of width $\delta$, bounded amplitude and uniformly bounded total variation, has squared translation difference $O(\min(s,\delta))$. Its small-shift Gamma energy is $O(\delta(1+|\log\delta|))\to0$; the other compact terms converge in $L^2$. A bounded piecewise smooth zero extension also satisfies
$\|\tau_su-u\|_2^2\leq s^2\|u'\|_{2,\rm pieces}^2+C_us$.
Since $\rho(s)\sim1/(2s)$, the coupled Gamma row is Bochner-integrable in $L^2$ at zero. Its far tail is integrable. Pairing that row with core tests identifies these cell functions with elements of the killed **operator** domain. They are not being treated as $H^1$ functions across jumps.

## C. Exterior Hardy inequality and the complete interface

Fix $0<b<(\log2)/2$, and set

$$
 \gamma_b=\pi(1-e^{-2b}),\quad d_b=\frac{k e^{-9b/2}}{2K},
 \quad B_H=\frac{c_b}{2d_b},\quad S_b=H_b/\kappa.
$$

The envelope (A.1), retaining the inward shifted summand, gives
$S_b(x)\geq d_b\exp(\gamma_b e^{2|x|})$ for $|x|\geq b$.
The source row gives $AS_b=(S_b-c_b)/2$ in the core pairing. The jump ground-state identity (obtained by expanding the square of $f/S_b$, with positive factor $S_b(x)S_b(x+s)$) therefore gives

$$
 \mathcal E(f)-\tfrac12\|f\|_H^2+
 \int\frac{c_b}{2S_b}|f|^2d\nu\geq0.                   \tag{C.1}
$$

One may first use compact tests; the edge-$L^2$ closure extends the inequality to the minimum domain. No equality of minimum and maximum domains is needed. In the exterior killed domain,

$$
 A_o\geq\left(\tfrac12-B_H e^{-\gamma_b e^{2R}}\right)I. \tag{C.2}
$$

For clarity, the genuine unitary used for the interface is
$\mathcal U f=\sqrt{2\kappa C}\,f$, different from $J_R$. Put
$W=\sup w$, $\omega_R=\sup_{|x|\geq R}w(x)$. Then
$W\leq Ke^{-\pi}$ and $\omega_R\leq K e^{4R-\pi e^{2R}}$.
The Gamma cross kernel in these coordinates is
$\sqrt{w(x)w(y)}\rho(|x-y|)$. Since $\rho(s)\leq2/s$, Schur's test with weight $u^{-1/2}$ and
$\int_0^\infty v^{-1/2}/(u+v)dv=\pi u^{-1/2}$
gives $2\pi\sqrt{W\omega_R}$ at one boundary; the two orthogonal exterior input sides give the norm bound
$2\sqrt2\pi\sqrt{W\omega_R}$.

For a prime shift $s$, a crossing pair has one endpoint of modulus at least $R$, and one endpoint of modulus at least $s/2$. These need not be the same endpoint. Interpolating the two resulting bounds yields, for $0<\theta<1$,

$$
 \sqrt{w(x)w(x+s)}\leq
 \sqrt W\,\omega_R^{\theta/2}\omega_{s/2}^{(1-\theta)/2}.
$$

Thus the **full**, infinite Gamma-plus-prime interface $T_R$ satisfies

$$
 \|T_R\|\leq M_\theta\omega_R^{\theta/2},\quad
 M_\theta=2\sqrt2\pi W^{1-\theta/2}+2\sqrt W S_\theta,
 \quad S_\theta=\sum_{n\geq2}a_n\omega_{\log n/2}^{(1-\theta)/2}. \tag{C.3}
$$

The summands are bounded by a constant times
$(\log n)n^{1/2-\theta}e^{-(1-\theta)\pi n/2}$; hence the prime interface converges in operator norm, with both orientations retained.

Sharp splitting of a core test is admitted by §B. Expanding its energy gives
$\mathcal E(f)=\mathcal E(f_i)+\mathcal E(f_o)-2\Re\langle\mathcal U f_i,T_R\mathcal U f_o\rangle$.
The bounded cross term controls the sum of the two killed energies by the original energy plus a constant times the squared $H$-norm. Applying this bound to differences of core approximants extends splitting to every form-domain vector. Conversely the two killed domains embed into the original minimum domain. This establishes the direct-sum form domain and the block operator with diagonal blocks $A_i,A_o$ and off-diagonal blocks $-T_R,-T_R^*$.

## D. Strict spectral counts and fixed admission

Let $\lambda=1/2-\epsilon$. If
$B_H e^{-\gamma_b e^{2R}}\leq\epsilon/2$, then
$D_o=A_o-\lambda\geq\epsilon/2$. Completing its square gives the exact interior Schur form

$$
 F_i(\lambda)=A_i-\lambda-T_RD_o^{-1}T_R^*,\qquad
 0\leq T_RD_o^{-1}T_R^*\leq\eta_R I,
 \quad\eta_R=2M_\theta^2\omega_R^\theta/\epsilon.         \tag{D.1}
$$

The triangular change preserves the form domain: $D_o^{-1}T_R^*$ maps interior $H$ into the exterior operator domain. Negative index and the spectral theorem give

$$
 N_{A_i}(\lambda)\leq N_A(\lambda)\leq N_{A_i}(\lambda+\eta_R),
 \quad N_A(t)=\dim\operatorname{Ran}\mathbf1_{(-\infty,t)}(A). \tag{D.2}
$$

The count is strict. Compactness of the interior resolvent can also be checked from the logarithmically increasing small-Gamma Fourier multiplier and compact-support translation compactness; no positive Sobolev order is asserted. The negative-index argument itself does not presuppose a discrete global spectrum.

For explicit admission replace $W,S_\theta,M_\theta$ by

$$
 \overline W=Ke^{-\pi},\quad
 \overline S=K^{(1-\theta)/2}\sum_{n\geq2}(\log n)n^{1/2-\theta}
               e^{-(1-\theta)\pi n/2},\quad
 \overline M=2\sqrt2\pi\overline W^{1-\theta/2}
                    +2\sqrt{\overline W}\,\overline S,
$$
$$
 \overline\eta=2\overline M^2K^\theta
        e^{4\theta R-\pi\theta e^{2R}}/\epsilon,
 \qquad t_0=\epsilon-\overline\eta.                       \tag{D.3}
$$

The accompanying scalar enclosure uses $R=1,\epsilon=1/8,b=1/4,\theta=9/10$, with $q=1/2,L=3/4$ below. Its outward intervals give

- $0.00823814126241773813<\overline\eta<0.00823814126241773817<1/16$;
- $0.11676185873758226183<t_0<0.11676185873758226187$;
- the Hardy admission inequality and the 552-moment coercivity gate in §E.

These decimal inequalities summarize saved intervals; the producer uses the full endpoint strings in `inputs.hpp`, not these shortened bounds. The scalar field named `hardy_defect` is an admission **slack**, $\gamma_b e^{2R}-\log(2B_H/\epsilon)$, not the exterior spectral defect itself.

Under $J_R$, the required interior form is

$$
 B_{\epsilon-\eta_R}=Q_{{\rm inv},R}+(\epsilon-\eta_R)\|\cdot\|_m^2
 =B_{t_0}+(\overline\eta-\eta_R)\|\cdot\|_m^2\geq B_{t_0}. \tag{D.4}
$$

## E. Original moment kernel: Gamma coercivity and prime absorption

Partition $(-R,R)$ symmetrically into cells of length at most $\delta$. Keep every independent functional
$\ell_J(u)=\int_J e^{x/2}u(x)dx$ in the even sector, and denote their common kernel in the killed form domain by $X$.

For $u\in X$, define on $J=(a,b)$
$k_u(x)=e^{-x/2}\int_a^x e^{y/2}u(y)dy$.
It vanishes at both endpoints; its piecewise zero extension is $H^1$, and $u=k_u'+k_u/2$. Integration of the cross term and Dirichlet Poincaré give

$$
 \|u\|_2^2=\|k_u'\|_2^2+\tfrac14\|k_u\|_2^2
 \geq((\pi/\delta)^2+1/4)\|k_u\|_2^2.
$$

Plancherel consequently gives

$$
 \frac1{2\pi}\int\frac{|\widehat u(\xi)|^2}{1+4\xi^2}d\xi
 \leq\frac{\|u\|_2^2}{1+(2\pi/\delta)^2}.                \tag{E.1}
$$

Expanding $\rho(s)=\sum_{j\geq0}e^{-(2j+1/2)s}$, the exact Gamma symbol is

$$
 d_\Gamma(\xi)=\sum_{j\geq0}\frac{2\xi^2}{a_j(a_j^2+\xi^2)},
 \quad a_j=2j+1/2,
 \quad d_\Gamma(\xi)\geq\tfrac12\log(1+4\xi^2).
$$

The last inequality follows by comparison of the decreasing summand with its integral over $a\geq1/2$, with mesh factor $1/2$. Apply Jensen to $-\log$ for the probability density $|\widehat u|^2/(2\pi\|u\|^2)$ and use (E.1). Truncation justifies the step for finite energy; infinite energy is immediate. Thus

$$
 D_\Gamma(u)\geq b_\delta\|u\|_2^2,
 \quad b_\delta=\tfrac12\log(1+(2\pi/\delta)^2),\quad u\in X. \tag{E.2}
$$

All active prime powers are retained in
$P_Ru=\sum_{\log n<2R}a_n(\tau_{\log n}u+\tau_{-\log n}u)$, with zero extensions. Let
$W_r=\sum_{2\leq n\leq e^{2r}}a_n$, $\beta_r=W_r+W_{r/2}$.
At $x\geq0$, the two available travel lengths are at most $R+x\leq2R$ and $R-x\leq R$; the nonnegative symmetric row sum is at most $\beta_R$. Schur's test proves $\|P_R\|\leq\beta_R$.

For $0<L<R$, central compression is precisely $P_L$. From (A.1),
$m\geq K^{-1}e^{\pi e^{2|x|}-4|x|}$, an increasing lower bound in $|x|$. Put

$$
 T=\frac{qt_0}{K}e^{\pi e^{2L}-4L},\quad
 K_2=\frac{\beta_L+\beta_R-T+
 \sqrt{(\beta_L-\beta_R+T)^2+4\beta_R^2}}2,
$$
$$
 m_0=e^\pi/K,\qquad
 \widehat K=\min\{\beta_R-qt_0m_0,K_2\}.                 \tag{E.3}
$$

Indeed, for central and outer norms $a,b$, the quadratic form of $P_R-qt_0m$ is at most
$\beta_La^2+2\beta_Rab+(\beta_R-T)b^2$; (E.3) is its larger two-by-two eigenvalue, combined with the global weight floor. No splitting or deletion of Gamma energy occurs. Equations (E.2)–(E.3) imply

$$
 B_{t_0}(u)\geq(b_\delta-c_\Gamma-\widehat K)\|u\|_2^2
                 +(1-q)t_0\|u\|_m^2,\qquad u\in X.     \tag{E.4}
$$

The saved $R=1$ gate uses $\delta=1/276,q=1/2,L=3/4$, and establishes $b_\delta\geq c_\Gamma+\widehat K$. Hence the actual retained variable weight is

$$
 B_{t_0}(u)\geq\int\alpha|u|^2,
 \qquad\alpha=t_0m/2>0,\qquad u\in X.                   \tag{E.5}
$$

Its saved scalar floor exceeds $0.03417647168812305$, but the residual integral uses the function $\alpha$, not that floor. The lower bound plus the global estimate
$B_{t_0}\geq D_\Gamma-(c_\Gamma+\beta_R)\|\cdot\|_2^2$
makes $B_{t_0}$ coercive in the minimum form topology on $X$.

There are 276 positive cells and their reflections, giving 552 independent moments, **not** 276. On one positive cell evenness turns its two reflected functionals into integration against $e^{x/2}$ and $e^{-x/2}$, which are independent. Their span is the local cosh/sinh span. This count concerns a sufficient complete quotient, not a necessary minimum for all possible methods.

## F. Exact finite reduction and arbitrary residual trials

Let $\Phi_o:\mathbb C^{552}\to L^2_{\rm even}(I)$ have orthonormal columns spanning the original moment representers; let $L_0=\Phi_o^*$. Smooth dual lifts exist because this finite independent moment map is surjective already on the dense smooth core. Coercivity (E.5) permits a unique $B=B_{t_0}$-orthogonal correction of each lift into $X$. If the corrected lifts are $r_j$, the full minimum killed domain is the direct sum of $X$ and their span, with no cross terms. Therefore

$$
 n_-(B)=n_-(S),\quad S_{ij}=B(r_i,r_j),\quad
 z^*Sz=\inf_{h\in X}B(\Phi_o z+h).                      \tag{F.1}
$$

The use of $\Phi_o$ in the infimum is legitimate by its operator-domain admission in §B. Its affine moment classes are the same as those of smooth lifts.

More generally choose any operator-domain source map $u$ with $L_0u=D$, where $D$ is invertible, and any trial coefficient matrix $C_t$ in the **original** moment span. Put

$$
 r=A_Bu-\Phi_oC_t,\quad G=u^*A_Bu,\quad
 H_r=r^*\alpha^{-1}r,\quad F=G-H_r.
$$

For $h\in X$, the subtraction $\Phi_oC_t$ annihilates $h$ in the ordinary $L^2$ pairing. Completing the weighted square proves

$$
 B(uz+h)\geq z^*Fz+
 \|\alpha^{1/2}h+\alpha^{-1/2}rz\|_2^2,
 \qquad F\leq D^*SD.                                   \tag{F.2}
$$

This is true for arbitrary fixed trials. It needs no exact projection, exact minimizer, or inverse of a numerically guessed negative block. Ordinary moment orthogonality is not confused with orthogonality in $L^2(\alpha^{-1}dx)$. In particular, a failed lower enclosure does not establish a negative direction of the exact Schur form.

The complete row used in (F.2) is, almost everywhere in $I_R$,

$$
 A_Bv=\int_0^{2R}\rho(s)(2v-\tau_sv-\tau_{-s}v)ds
 +2vJ(2R)-c_\Gamma v-P_Rv+t_0mv,\quad
 J(L)=\operatorname{atanh}(e^{-L/2})+\arctan(e^{-L/2}).   \tag{F.3}
$$

The identity for $J$ follows by substitution $e^{-s/2}$; alternatively
$J(L)=\sum_{j\geq0}e^{-(2j+1/2)L}/(2j+1/2)$.
Thus the infinite Gamma tail is retained exactly or enclosed, while the finite internal prime list at $R=1$ is $n=2,3,4,5,7$. The infinite exterior prime list remains controlled separately by (C.3).

## G. Exact lifts, coverage, and what v4 certifies

On a positive cell of width $\delta$, centered at $c$, the even reflected-pair modes have positive-half expressions

$$
 \frac{\cosh((x-c)/2)}{N_0},\quad
 \frac{\sinh((x-c)/2)}{N_1},\qquad
 N_0^2=\delta+2\sinh(\delta/2),\quad
 N_1^2=2\sinh(\delta/2)-\delta.
$$

The negative half is their even reflection. Halve each original positive cell to obtain 552 fine positive cells and 1104 fine even modes $\Phi_f$. Write $n_{f0},n_{f1}$ and $n_{c0},n_{c1}$ for fine and coarse normalizers. With $d=\delta/8=1/2208$, define locally

$$
 A=\frac{n_{f0}\cosh d}{n_{c0}},\quad
 B=\frac{n_{f1}\sinh d}{n_{c0}},\quad
 C=\frac{n_{f0}\sinh d}{n_{c1}},\quad
 D_1=\frac{n_{f1}\cosh d}{n_{c1}}.
$$

In the four fine coordinates the columns are

$$
 p_0=(A,-B,A,B),\quad p_1=(-C,D_1,C,D_1),\quad
 x_0=(B,A,B,-A),\quad x_1=(D_1,C,-D_1,C).
$$

Hyperbolic addition and the integral normalizations prove
$P^*P=X_f^*X_f=I,P^*X_f=0,\Phi_o=\Phi_fP$.
For the stored finite dyadic matrix $Z$, define the **exact analytic** map
$U=P-X_fZ$. Then $P^*U=I$ and $U^*U=I+Z^*Z$.
The stored floating array `Ufloat.bin` is only an enclosed surrogate, not the definition of $U$.

The v4 source is $u=\Phi_fUD$ for its invertible powers-of-two diagonal $D$. Its moment map is $L_0u=D$, not $I$. The residual subtraction is $\Phi_o C D$, with stored $C$ interpreted as exact dyadics. These trials cover all original 552 quotient directions without enlarging the projection space to the 1104-dimensional fine source span.

The frozen numerical chain supplies:

1. Exact-candidate enclosures for the analytic lifts and their floating surrogates, complete fine $G$ intervals, and the full row formulas.
2. Complete-domain derivative/contact bounds and the rational refinement plan for the residual Gram.
3. A fresh v4 58-point baseline with explicit multiplication, combined with the saved signed 88-new-minus-16-old patch: the same 130 composite smooth panels and two analytic cap templates.
4. A fresh $G$ congruence, complete error aggregation, and a positive 551-dimensional restriction of the full 552-coordinate sufficient matrix.

The v4 replacement removes reliance on the old baseline's NumPy `hh**3` behavior. The earlier final matrix centers and their old final signs are not substituted for v4. Valid fine-$G$, candidate, derivative-domain, and signed-patch objects are reused only in their stated roles.

The saved total Loewner-error upper bound is $0.010231573894279825$. The saved projected-center lower bound is $0.03995839074390939$. After all errors, the saved restriction margin is $0.02972681684942717>0$, with trial Gram defect bounded by $1.978060563959767\times10^{-11}$. Consequently the sufficient coordinate matrix has at most one negative eigenvalue (and its increasingly ordered second coordinate eigenvalue exceeds $0.02972$ under the saved norm conversion). This last number is **not** an eigenvalue of the original operator and not the increment in §I.

The numerical premises require correct directed Decimal/MPFR arithmetic, the declared binary64/BLAS error model and operation counts, and truthful correspondence between frozen sources, inputs, runtime, and outputs. Hashes identify bytes; runtime fingerprints do not formally verify a compiler, library, hardware, or execution. Saved-ledger checking and independent regeneration are distinct activities; see `../REPRODUCE.md` for the actual supported verification scope.

## H. The fixed original-space conclusion

From §G, $n_-(F)\leq1$. The inequality $F\leq D^*SD$, invertibility of $D$, and (F.1) imply $n_-(B_{t_0})\leq1$. The nonnegative perturbation in (D.4), followed by (D.2), gives

$$
 N_A(3/8)\leq1.
$$

Since $A\geq0$ and $A1=0$, this count is exactly one. Its spectral subspace is precisely the constants. The spectral theorem therefore gives

$$
 \mathcal E(f)\geq\tfrac38\|f\|_H^2,
 \qquad f\in\operatorname{Dom}\mathcal E,\quad\langle1,f\rangle_H=0. \tag{H.1}
$$

The strict-count statement alone would not exclude spectrum at $3/8$. That requires the separate uniform coercivity argument below.

## I. Strict local improvement, with no evaluated increment

Let $Q:\mathbb C^{551}\to\mathbb C^{552}$ be the saved injective restriction map. Use $W=uQ$ and $r_Q=rQ$. The saved restriction establishes
$Q^*FQ\geq\mu I$; one may take the conservative rational $\mu=1/64$ in these $Q$-column coordinates. No claim that $Q$ is exactly orthonormal is needed.

Every killed vector whose moments lie in $D\operatorname{Ran}Q$ has the form $v=Wz+h$, $h\in X$. Equation (F.2) gives

$$
 B(v)\geq\mu|z|^2+\|y\|_2^2,\qquad
 y=\alpha^{1/2}h+\alpha^{-1/2}r_Qz.
$$

As an $L^2$ identity,
$v=(W-\alpha^{-1}r_Q)z+\alpha^{-1/2}y$.
The latter terms need not separately belong to the form domain. Set

$$
 \overline L=\|W\|_{\ell^2\to L^2(m)}+
             \sqrt{2/t_0}\|r_Q\|_{\ell^2\to L^2(\alpha^{-1})},
 \quad\kappa_*=(\overline L^2/\mu+2/t_0)^{-1}>0.
$$

These norms are finite because there are finitely many admitted source and residual columns on a compact interval and $m/\alpha=2/t_0$. Weighted Cauchy–Schwarz gives

$$
 B(v)\geq\kappa_*\|v\|_m^2.                            \tag{I.1}
$$

The moment constraint defines a closed codimension-one subspace: moment functionals are bounded in $L^2(m)$, and surjectivity follows from $L_0u=D$. Under $J_R$ it is a closed codimension-one interior subspace $M_i$ in the original metric, not necessarily an interior mean-zero subspace.

Use $K_o=D_o^{-1}T_R^*$ in the exact exterior square. The admission bounds give
$\|K_o\|^2\leq2\overline\eta/\epsilon$, and for $f_i\in M_i$, writing $z_o=f_o-K_of_i$,

$$
 \mathcal E(f)-\tfrac38\|f\|^2\geq
 \kappa_*\|f_i\|^2+(\epsilon/2)\|z_o\|^2,
$$
$$
 \|f\|^2\leq(1+2\|K_o\|^2)\|f_i\|^2+2\|z_o\|^2.
$$

Hence a valid symbolic positive increment is

$$
 c=\min\left\{\frac{\kappa_*}{1+4\overline\eta/\epsilon},
                      \frac\epsilon4\right\}>0.         \tag{I.2}
$$

The global condition $f_i\in M_i$ has codimension one. If the spectral subspace strictly below $3/8+c$ had dimension at least two, a two-dimensional part of it would meet this constraint nontrivially, contradicting its lower bound. The zero constant fills the only subthreshold direction. Thus

$$
 \mathcal E(f)\geq(3/8+c)\|f\|_H^2\quad(f\perp1).       \tag{I.3}
$$

No numerical value of $c$ is evaluated here. This excludes the centered endpoint $3/8$ under the certificate premises, but does not establish the target $1/2$.

In particular, the exterior construction can be arranged for a sequence $\epsilon\downarrow0$ with $\eta_R=o(\epsilon)$ when $2\gamma_b/\pi<\theta<1$. What is **not** supplied is the necessary full-domain sign at every radius of such a sequence. A fixed certificate, a finite coordinate margin, or fixed-radius density does not provide that missing family. No zero-free strip or RH conclusion is claimed; no conversion of $3/8$ into a zeta-plane boundary is proved.

## J. External inputs, public evidence, and limitations

The mathematical chain above reconstructs the application-specific arguments; it does not reprove the general theta transformation, Mellin/Fourier theory, polarized explicit formula, classical zero count, closed-form representation theorem, Riesz representation, or spectral theorem. These are external classical inputs. In particular the zero-distribution pairing in §B must not be replaced by a sum of nonnegative absolute squares unless reality of the relevant zeros has independently been proved.

Primary / authoritative references:

- André Weil, *Sur les formules explicites de théorie des nombres*, Math. USSR-Izvestiya 6 (1972), 1–17: [publisher/archive record](https://www.mathnet.ru/php/archive.phtml?jrnid=im&option_lang=eng&paperid=2289&wshow=paper). The general explicit-formula framework is an external input; §B states the specialization and constants consumed here, not a new proof of Weil's theorem.
- NIST Digital Library of Mathematical Functions, [§20.7, theta transformations](https://dlmf.nist.gov/20.7), [§20.10, theta integrals](https://dlmf.nist.gov/20.10), and [§25.10, zeta zeros and counting](https://dlmf.nist.gov/25.10). These are authoritative general identities/counting references, not evidence for this paper's operator bound.
- Tosio Kato, *Perturbation Theory for Linear Operators*, second edition, Springer, 1995 reprint, [DOI:10.1007/978-3-642-66282-9](https://doi.org/10.1007/978-3-642-66282-9). General closed-form representation and self-adjoint spectral theory; no theorem-number attribution or application-specific certificate is inferred from this reference.
- Nicholas J. Higham, *Accuracy and Stability of Numerical Algorithms*, second edition, SIAM, 2002, [DOI:10.1137/1.9780898718027](https://doi.org/10.1137/1.9780898718027). General rounding-error theory only.
- Laurent Fousse, Guillaume Hanrot, Vincent Lefèvre, Patrick Pélissier, Paul Zimmermann, *MPFR: A Multiple-Precision Binary Floating-Point Library With Correct Rounding*, ACM TOMS 33(2), Article 13 (2007), [DOI:10.1145/1236463.1236468](https://doi.org/10.1145/1236463.1236468), and the [GNU MPFR manual](https://www.mpfr.org/mpfr-current/mpfr.html). Directed-arithmetic semantics, not formal certification of this complete program.

The minimum numerical dependency roles and the mathematical directed graph are listed in `DEPENDENCY_MAP.json`. Public numerical files retain their own hashes and provenance in `../evidence/` and the release manifest. A missing required enclosure is not repaired by this appendix. Conversely, historical exploratory source-only results, optimization success, or earlier final-sign labels are not needed for this fixed-trial implication.

This release provides no external peer-review claim, novelty verdict, proof-assistant formalization, formal verification of the numerical stack, or new numerical production. Author-owned exposition follows the release license; cited works and third-party components retain their own copyrights and licenses.
