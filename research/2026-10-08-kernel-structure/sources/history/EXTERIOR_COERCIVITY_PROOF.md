# Theta-source transformation and exterior coercivity of the signed Weil form

Jongmin Choi — author-side analytic proof, 2026-10-06 (Asia/Seoul).

**Verdict: PASS-FIRST-KEY on the exterior theorem stated below.** The inherited full-radical source identity is used in its stated form domain. The prime-number input is unconditional. There is no assertion of global positivity, a selected arithmetic ground state, or RH. No arithmetic matrix, eigenvalue computation, or parameter sweep is performed.

## 1. Exact scope and inherited definitions

All functions in the main theorem are real and even. The Fourier convention is
\[
F_u(z)=\int_{\mathbb R}u(x)e^{-izx}\,dx,
\qquad \Xi(z)=\xi(1/2+iz),
\]
where \(\xi(s)=\tfrac12s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)\). The source is exactly
\[
\kappa(x)=e^{x/2}\sum_{n\ge1}(4z_n^2-6z_n)e^{-z_n},
\qquad z_n=\pi n^2e^{2x}.                                      \tag{1}
\]
It is not a new prolate candidate or a modification of a Fourier compression.

For the full real-even signed Weil form, put
\[
\begin{aligned}
Q(u,v)&=D_\Gamma(u,v)-c_\Gamma\langle u,v\rangle
 -2\sum_{n\ge2}\frac{\Lambda(n)}{\sqrt n}C_{uv}(\log n)
 +2\mu(u)\mu(v),\\
D_\Gamma(u,v)&=\int_0^\infty\rho(s)
 \langle u-\tau_su,v-\tau_sv\rangle\,ds,\\
\rho(s)&=\frac{e^{-s/2}}{1-e^{-2s}},\quad
c_\Gamma=\log\pi+\gamma_E+\pi/2+3\log2,\\
\tau_su(x)&=u(x+s),\quad C_{uv}(s)=\int u(x)v(x+s)\,dx,\quad
\mu(u)=\int u(x)\cosh(x/2)\,dx.                              \tag{2}
\end{aligned}
\]
Here \(\Lambda\) is von Mangoldt's function, including every prime power. Evenness gives \(C_{uv}(s)=C_{vu}(s)\), so (2) is symmetric. The polarization convention is \(Q(u+tv)=Q(u)+2tQ(u,v)+t^2Q(v)\). There is no extra factor two in the bilinear pole term.

These conventions are the ones in `sources/internal/SOURCE_ENERGY_PROOF.md`, §2, and in the polynomial-ambiguity source, §§1,3. The archimedean finite part has already been coupled into \(D_\Gamma-c_\Gamma\|u\|_2^2\). In particular a divergent diagonal integral is never separated from its subtraction. The original pole correlation \(4\int_0^\infty \cosh(s/2)C_u(s)\,ds\) equals \(2\mu(u)^2\) in this even sector.

The inherited full-radical statement is
\[
Q(\kappa^{(2j)},v)=0,\qquad j\ge0,                         \tag{3}
\]
initially for admissible compact tests and then by the form majorant below. It follows from the full explicit formula and \(F_{\kappa^{(2j)}}(z)=(-1)^jz^{2j}\Xi(z)\); every nontrivial zero is annihilated irrespective of its location. We inherit that explicit-formula identity, rather than assume RH, a positive Weil operator, or a closed global realization. Source identity (3), its original scope and provenance are retained as a separate dependency; extending its test domain below uses continuity, not an operator eigenvector argument.

The majorant retained from the source is
\[
\begin{aligned}
\|u\|_W^2={}&c_\Gamma\|u\|_2^2+D_\Gamma(u)
 +20\|e^{|x|}u\|_2^2
 +2\left(\int|u(x)|\cosh(x/2)\,dx\right)^2,\\
|Q(u,v)|&\le\|u\|_W\|v\|_W.                              \tag{4}
\end{aligned}
\]
The third integrand is \(e^{2|x|}|u|^2\). This is continuity of the signed pairing, not positivity of it. In particular
\[
|C_{uv}(s)|\le e^{-s}\|e^{|x|}u\|_2\|e^{|x|}v\|_2,
\quad s\ge0,
\]
because \(|x|+|x+s|\ge s\). Together with \(\sum_{n\ge2}\Lambda(n)n^{-3/2}<5\), this proves absolute convergence of all prime sums used in the proof. The latter bound follows from \(\Lambda(n)\le\log n\) and the integral test. Gamma polarization is controlled by Cauchy--Schwarz in its positive translation-difference integral. The same componentwise argument gives (4).

The older failure of absolute-value contraction and positivity-preserving ground-state selection is preserved verbatim. The transformation proved here does not contradict that failure: the pole leaves a **negative variance term**.

**Historical duplication check.** `SERABI_RH_SOURCE_SUBSPACE_AND_SCHUR_2026-09-18.md` §8, equations (8.1)--(8.4), already contains this exact theta-source transformation and its derivative saturation. `THETA_SOURCE_AUDIT_2026-09-18.md` §8 checks it and rejects a strict global increase of the critical constant or deletion of a fixed positive prime energy at the same right-hand side. Those results are inherited; §§2--4 and §8 below supply convention/domain checks and are not counted as new theorems. The historical probability measure is called \(\mu\); it is the present \(\nu\), whereas the historical temporary \(\nu=\mu/2\) has half its mass. The historical non-even transform has an additional negative squared tanh moment, which is exactly zero for the even tests here. The new task does not retry its RH-equivalent global comparison. The exterior all-test estimate and central-edge PNT remainder in §§5--7 were not found in those originals or the other records inspected; this is a bounded duplication check, not a claim of literature priority.

## 2. Source positivity, monotonicity, and normalization

### Lemma 1

The full source (1) is smooth, strictly positive, even, and strictly decreasing for \(x>0\). Every fixed derivative decreases superexponentially in absolute value at both ends. Moreover
\[
0<\kappa(x)\le2e^{-|x|},\qquad
m_\kappa:=\int\kappa(x)\cosh(x/2)\,dx=\frac12.             \tag{5}
\]

**Proof.** For \(x\ge0\), every summand in (1) is positive, since \(z_n\ge\pi>3\) and \(4z_n^2-6z_n>0\). For theta evenness one may use
\(A(x)=e^{x/2}\sum_{n\ge1}e^{-\pi n^2e^{2x}}\), theta inversion \(A(-x)=A(x)+\sinh(x/2)\), and \(\kappa=(\partial_x^2-1/4)A\). The added hyperbolic sine is killed by that differential operator. Polynomial--Gaussian domination gives termwise differentiation on compact sets and, for each fixed \(r\),
\[
|\kappa^{(r)}(x)|\le C_r e^{B_r|x|}e^{-b_r e^{2|x|}},
\quad C_r,B_r,b_r>0.                                    \tag{6}
\]
This is the full series; no finite theta truncation is substituted.

For the useful elementary decay bound, discard \(-6z_n\) and observe that \(z^{11/4}e^{-z}\) decreases for \(z\ge3\). Thus, for \(x\ge0\),
\[
e^x\kappa(x)\le4\sum_{n\ge1}(\pi n^2)^2e^{-\pi n^2}
 \le36\sum_{n\ge1}n^4e^{-3n^2}<2.                         \tag{7}
\]
The ratios of the last summands are at most \(16e^{-9}<1/100\), since \(e>8/3\); hence the final bound follows from
\(36(3/8)^3/(1-1/100)=675/352<2\). Evenness proves (7) on both sides.

For completeness, strict decrease, also used for a variation estimate below, can be verified without a sampling calculation. With
\[
\begin{aligned}
P_0(z)&=4z^2-6z,\\
P_{r+1}(z)&=(1/2-2z)P_r(z)+2zP_r'(z),\\
P_1(z)&=-8z^3+30z^2-15z,\\
P_2(z)&=16z^4-112z^3+165z^2-\tfrac{75}{2}z,                \tag{8}
\end{aligned}
\]
one has \(\kappa^{(r)}(x)=e^{x/2}\sum P_r(z_n)e^{-z_n}\). For \(0\le x\le1/10\), \(3<z_1<4\), using \(\pi<22/7\) and \(e^{1/5}\le5/4\). Write \(z_1=3+t\), \(0\le t\le1\). Direct expansion gives
\[
P_2(3+t)=-\tfrac{711}{2}-\tfrac{687}{2}t+21t^2+80t^3+16t^4
 \le-\tfrac{711}{2}.                                    \tag{9}
\]
Indeed the positive terms are at most \(117t\). The first term in \(\kappa''\) is at most \(-711/162\), using \(e<3\). For \(n\ge2\),
\[
e^{x/2}P_2(z_n)e^{-z_n}
 \le\frac{20}{19}(1296n^8+1485n^4)e^{-3n^2}.
\]
The positive majorant has ratios at most \((3/2)^8(3/8)^{15}<1/10000\); its sum is less than
\[
\frac{20}{19}\frac{355536(3/8)^{12}}{1-1/10000}<3.
\]
Consequently \(\kappa''(x)<-25/18\) on this short interval. Evenness gives \(\kappa'(0)=0\), hence \(\kappa'(x)<0\) there for \(x>0\). For \(x\ge1/10\), all \(z_n>18/5>13/4\). The quadratic \(8z^2-30z+15\) is positive at \(13/4\) and increasing thereafter, so every summand of \(P_1(z_n)e^{-z_n}\) is strictly negative. This proves strict decrease everywhere on the positive half-line. All rational bounds in this paragraph are independently checked by the bundled exact-arithmetic script; the analytic domination is proved here.

The inherited theta Mellin identity is \(F_\kappa=\Xi\), valid throughout the complex plane by (6) and analytic continuation. Evaluate it at \(z=i/2\). Evenness changes \(\int\kappa e^{x/2}\) to \(\int\kappa\cosh(x/2)\), and \(\xi(0)=\xi(1)=1/2\). The latter follows directly by taking the limit at the simple pole of \(\zeta(s)\) at 1 in its completed expression. This proves (5). Alternatively the Mellin identity and its endpoint limit can be checked before making any use of the Weil pairing. No zero-location assumption is involved. ∎

It follows that
\[
\nu(dx)=2\kappa(x)\cosh(x/2)\,dx,
\qquad c_\kappa=2m_\kappa^2=\frac12                       \tag{10}
\]
is a positive probability measure and the requested threshold is exactly \(1/2\). The subscript in \(m_\kappa\) denotes a source integral, not a derivative order.

## 3. Domain of the transformation

Take real-even \(f\in C_c^\infty(\mathbb R)\), and put \(u=\kappa f\), \(w=\kappa f^2\). Both are compact smooth. The noncompact \(\kappa\) belongs to every weighted space appearing in (4), by (6). In particular its Gamma difference energy is finite: for an \(H^1\) function,
\[
D_\Gamma(v)\le\|v'\|_2^2+16\|v\|_2^2,                    \tag{11}
\]
using \(\rho(s)\le2/s\) for \(s\le1\), \(\rho(s)\le2e^{-s/2}\) for \(s\ge1\), and the translation estimates \(\|v-\tau_sv\|_2\le s\|v'\|_2\) and \(\le2\|v\|_2\). Therefore \(Q(\kappa,w)\) is an absolutely controlled mixed pairing, and inherited radicality gives
\[
Q(\kappa,\kappa f^2)=0.                                  \tag{12}
\]
The source is not silently cut off in this step. A compact source approximation converges in (4), so the full pairing is also the limit of those approximations. On the zero side, the original full explicit formula remains the inherited justification of its vanishing.

When (3) is first stated against finite Fourier tests, its extension to compact smooth tests uses the same supported Fourier approximation in the parent's endpoint-valid \(H^{1/4}\)-to-\(W\) estimate and (4). For smooth superexponentially decreasing tests, subsequent smooth compact cutoffs converge in \(H^1\), weighted \(L^2\), and weighted \(L^1\); (11) and (4) extend the identity again. Neither extension assumes \(L^2\)-continuity of an unbounded Weil form, or a closed global self-adjoint operator.

## 4. Exact mixed continuous--atomic source transformation

### Proposition 2

For the functions of §3,
\[
\boxed{Q(\kappa f)=\mathcal E_\kappa(f)
                    -\tfrac12\operatorname{Var}_\nu(f)}, \tag{13}
\]
where
\[
\begin{aligned}
\mathcal E_{\kappa,\Gamma}(f)
 &=\int_0^\infty\rho(s)\int_{\mathbb R}
   \kappa(x)\kappa(x+s)[f(x)-f(x+s)]^2\,dx\,ds,\\
\mathcal E_{\kappa,\mathrm{prime}}(f)
 &=\sum_{n\ge2}\frac{\Lambda(n)}{\sqrt n}\int_{\mathbb R}
   \kappa(x)\kappa(x+\log n)[f(x)-f(x+\log n)]^2\,dx,\\
\mathcal E_\kappa&=\mathcal E_{\kappa,\Gamma}
                  +\mathcal E_{\kappa,\mathrm{prime}}.     \tag{14}
\end{aligned}
\]
Both terms are finite and nonnegative. In particular the proposed prime coefficient is correct, with no added factor two.

**Proof.** Subtract (12). At a Gamma edge write \(a=\kappa(x)\), \(b=\kappa(x+s)\), \(F=f(x)\), \(G=f(x+s)\). The exact algebra is
\[
(aF-bG)^2-(a-b)(aF^2-bG^2)=ab(F-G)^2.                     \tag{15}
\]
The local \(-c_\Gamma\) terms cancel identically. At a prime edge, evenness and symmetry of the correlation give
\[
C_{\kappa,w}(s)=\tfrac12\int\kappa(x)\kappa(x+s)
                           [f(x)^2+f(x+s)^2],dx.
\]
Thus \(-2\Lambda(n)n^{-1/2}[C_u(s)-C_{\kappa,w}(s)]\) equals the corresponding term of (14). The factor \(-2\) and the symmetrization factor \(1/2\) have both been retained.

Finally \(\mu(u)=m_\kappa\int f\,d\nu\), \(\mu(w)=m_\kappa\int f^2\,d\nu\). The pole difference is exactly
\[
2\mu(u)^2-2m_\kappa\mu(w)
 =-2m_\kappa^2\left[\int f^2d\nu-(\int f d\nu)^2\right].   \tag{16}
\]
This proves (13), including its sign.

The Gamma integrals of the square and of the mixed differences are integrable by (4),(11) and Cauchy--Schwarz. Their difference (15) is nonnegative and finite. The prime correlations of \(u\), and the mixed correlations of \(\kappa,w\), are absolutely summable by (4). Their difference, after even symmetrization, proves both finiteness and the positive formula in (14). Equivalently one can first use a finite prime sum and Gamma integration over \([\eta,M]\), then pass to the limit with these absolute bounds and Tonelli on the nonnegative side. All prime powers remain present even though the original compact diagonal pairing has only finitely many active correlations. ∎

This is the quadratic ground-state representation algebra, not a claim of invention. Frank--Seiringer, arXiv:0803.0503v2, Assumption 2.1 and Proposition 2.3, formulate it for a symmetric nonnegative kernel and give equality in the quadratic case; Remark 2.4 discusses other underlying measures. Here the continuous part corresponds to the double-integral kernel \(\rho(|x-y|)/2\). The prime jump measure is singular on lines \(y=x+\log n\), and its infinitely many diagonal compensators cannot simply be split into finite potentials. We therefore prove the combined identity directly by (15), finite sums, and the convergence just verified. No undocumented extension of their measurable-kernel theorem, nor their ground-state hypothesis for a different operator, is used.

## 5. One fixed central cutoff and edge counting

Set \(\eta(t)=e^{-1/t}\) for \(t>0\), and \(\eta(t)=0\) otherwise. Define
\[
\theta(t)=\frac{\eta(1-t)}{\eta(t)+\eta(1-t)},\quad
\chi_R(y)=\theta(|y|-R),\quad R\ge1,\quad H=R+1.           \tag{17}
\]
The denominator is positive for every real \(t\). This is a smooth even cutoff, constant near zero, equal to one on \([-R,R]\), zero outside \([-H,H]\), and monotonically decreasing on the positive transition interval. In particular \(\int_R^H|\chi_R'|=1\), and \(\chi_R\uparrow1\) as \(R\to\infty\).

Let \(f=0\) on \([-S,S]\) with \(S>H\). Retain, in the prime part of (14), just the following two disjoint types of edges:

* left endpoint \(y\in[-H,H]\), right endpoint \(x=y+\log n\ge S\);
* left endpoint \(x\le-S\), right endpoint \(y=x+\log n\in[-H,H]\).

At the central endpoint \(f(y)=0\). Multiplying the edge contribution by \(\chi_R(y)\le1\) is a legitimate lower bound. Each retained edge has exactly one exterior and one central endpoint. The two types cannot overlap since \(S>H\). Each edge was originally counted once with a positive shift \(\log n\); no reversed copy is added. Edges with both endpoints outside are simply not used. Consequently
\[
\mathcal E_\kappa(f)\ge
 \int_{|x|\ge S}r_R(|x|)f(x)^2\,\nu(dx),                 \tag{18}
\]
where, for \(x\ge S\),
\[
r_R(x)=\frac{m_\kappa}{\cosh(x/2)}
 \sum_{n\ge2}\frac{\Lambda(n)}{\sqrt n}
              \kappa(x-\log n)\chi_R(x-\log n).          \tag{19}
\]
To see the coefficient, divide the retained positive-half density
\(\kappa(x)\sum\Lambda(n)n^{-1/2}\kappa(x-\log n)\chi_R(x-\log n)\)
by \(d\nu/dx=\kappa(x)\cosh(x/2)/m_\kappa\). On the negative half replace \(x\) by \(-x\), using evenness of \(\kappa\) and \(\chi_R\). There is no extra factor from even reflection. Tonelli justifies edge selection in the infinite sum. The bound holds for arbitrary signs of \(f\).

## 6. Prime-number theorem with the exact variation remainder

Write \(w_R=\kappa\chi_R\), and let
\[
I_R=\int e^{-y/2}w_R(y)\,dy,
\quad A_R=\int e^{-y/2}|\tfrac12 w_R(y)+w_R'(y)|\,dy.     \tag{20}
\]
These are explicit source integrals, not unknown response norms. They are independent of \(f\). Evenness and (5) give
\[
I_R=\int\kappa(y)\cosh(y/2)\chi_R(y)\,dy\uparrow m_\kappa,
\quad 0\le m_\kappa-I_R\le8e^{-R/2}.                      \tag{21}
\]
The tail estimate uses (7) and \(\cosh(y/2)\le e^{y/2}\).

There is also a useful uniform, elementary variation bound:
\[
A_R\le\tfrac12 I_R+
        \int e^{-y/2}|\kappa'(y)|\chi_R(y)\,dy+
        \int e^{-y/2}\kappa(y)|\chi_R'(y)|\,dy
       \le\frac{17}{2}<9.                               \tag{22}
\]
Indeed the middle integral is at most
\[
2\int_0^\infty\cosh(y/2)(-\kappa'(y))\,dy
 =2\kappa(0)+\int_0^\infty\kappa(y)\sinh(y/2)\,dy
 \le4+\frac14.
\]
The last integral is at most \(4e^{-R/2}\le4\), using monotonicity of the cutoff and its total variation one on each side; the first is at most \(1/4\). Boundary terms in this integration by parts vanish by (6).

Put \(\psi(v)=\sum_{n\le v}\Lambda(n)\), including prime powers, and \(E(v)=\psi(v)-v\). For \(x-H>\log2\), use the smooth compact Stieltjes test
\[
g_x(v)=v^{-1/2}w_R(x-\log v),\quad
\operatorname{supp}g_x\subset[e^{x-H},e^{x+H}].            \tag{23}
\]
Its endpoint values and all endpoint derivatives are zero. Therefore, including every atom, the exact formula is
\[
\begin{aligned}
\sum_{n\ge2}\frac{\Lambda(n)}{\sqrt n}w_R(x-\log n)
 &=\int g_x\,d\psi
  =e^{x/2}I_R-\int E(v)g_x'(v)\,dv,\\
g_x'(v)&=-v^{-3/2}[\tfrac12w_R(x-\log v)
                         +w_R'(x-\log v)].              \tag{24}
\end{aligned}
The Stieltjes boundary term \([g_x(v)E(v)]\) is zero, including if an endpoint is an integer prime power. No cutoff derivative or prime-power contribution has been discarded.

If \(|E(v)|\le\delta v\) for all \(v\ge e^{x-H}\), then
\[
\left|\sum_{n\ge2}\frac{\Lambda(n)}{\sqrt n}w_R(x-\log n)
                -e^{x/2}I_R\right|
 \le\delta e^{x/2} A_R.                                 \tag{25}
\]
This follows by the same change of variable \(y=x-\log v\). It is a full PNT bound on a fixed multiplicative interval, not a short-interval prime theorem. Consequently
\[
\left|r_R(x)-\frac{2m_\kappa I_R}{1+e^{-x}}\right|
 \le2m_\kappa\delta A_R.                                 \tag{26}
\]
The unconditional theorem \(\psi(v)=v+o(v)\) says that for each fixed \(\delta>0\) one threshold works for **all** larger \(v\). Applying it after fixing \(R\) proves
\[
\lim_{x\to\infty}r_R(x)=2m_\kappa I_R,
\qquad \lim_{R\to\infty}2m_\kappa I_R=c_\kappa.           \tag{27}
\]
This already proves the qualitative exterior theorem with the required quantifiers; no numerical prime experiment is needed.

## 7. Exterior theorem, including an optional effective radius

### Theorem 3 (all-test exterior coercivity)

For every \(0<\varepsilon<c_\kappa=1/2\), there is a radius \(S(\varepsilon)\), independent of \(f\), such that every real-even \(f\in C_c^\infty(\mathbb R)\) vanishing on \([-S,S]\) satisfies
\[
\boxed{\mathcal E_\kappa(f)\ge
        (\tfrac12-\varepsilon)\|f\|_{L^2(\nu)}^2.}        \tag{28}
\]
It suffices to take the following explicit, nonoptimized radius if the published unconditional bound specified below is used:
\[
\begin{aligned}
R_\varepsilon&=2\log(24/\varepsilon),\quad H_\varepsilon=R_\varepsilon+1,\\
\sigma_\varepsilon&=\max\{32,\tfrac52\log(270/\varepsilon)\},\\
S(\varepsilon)&=\max\{H_\varepsilon+1+\sigma_\varepsilon^2,
                         1+\log(3/(2\varepsilon))\}.     \tag{29}
\end{aligned}
\]

**Proof.** First fix \(\varepsilon\). Choose \(R=R_\varepsilon\), so (21) gives \(I_R\ge1/2-\varepsilon/3\). Fix \(\delta=\varepsilon/27\). Unconditional PNT provides a threshold beyond which (25) holds for all \(x\); also choose \(S>H\) and \(e^{-S}\le2\varepsilon/3\). From (22),(26), with \(2m_\kappa=1\),
\[
r_R(x)\ge I_R-I_Re^{-x}-\delta A_R\ge1/2-\varepsilon,
\quad\text{for every }x\ge S.                            \tag{30}
\]
Both halves in (18) have this same lower bound. Since \(f\) vanishes in the center, integrating (30) proves (28). The choices were \(\varepsilon\), then one cutoff \(R\), then one \(S\); they preceded the arbitrary choice of \(f\). Thus pointwise convergence was not substituted for an all-test uniform inequality.

To verify the optional formula (29), use Fiori--Kadiri--Swidinsky, *Sharper bounds for the Chebyshev function* \(\psi(x)\), arXiv:2204.02588v3 (17 May 2023), Corollary 1.4:
\[
|\psi(v)-v|/v<9.22022(\log v)^{3/2}
                         e^{-0.8476836\sqrt{\log v}},\quad v>2.
\]
Increasing the leading constant to 10 and reducing the decay coefficient to \(4/5\) is valid. For \(\sigma\ge32\), \(3\log\sigma\le(2/5)\sigma\); the inequality holds at 32 from \(\log2<7/10\), and its difference increases thereafter. Hence for \(\log v\ge\sigma_\varepsilon^2\),
\[
|\psi(v)-v|/v\le10e^{-(2/5)\sqrt{\log v}}
 \le\varepsilon/27=\delta.                              \tag{31}
\]
Formula (29) ensures \(x-H>\sigma_\varepsilon^2\), \(S>H\), and the required exponential-prefactor bound. It therefore meets every condition in (30). This radius relies on the published unconditional theorem, including its external computational dependencies; those dependencies have not been independently replayed here. The qualitative theorem uses only classical unconditional PNT and does not depend on that explicit numerical corollary. Neither version assumes RH. ∎

Combining (13) and (28) also gives, for these exterior tests only,
\[
Q(\kappa f)\ge-\varepsilon\|f\|_{L^2(\nu)}^2
                   +\tfrac12(\int f\,d\nu)^2.            \tag{32}
\]
This is an inequality in the transformed weighted space, not a uniform lower bound in the original physical \(L^2(dx)\) norm, and it is not a global nonnegative Weil form.

## 8. Fixed derivative boundary check: domain and critical equality

This section checks and centers the already inherited saturation family from the historical source's (8.4). Neither the family nor the global strict-constant obstruction is a new result of this task.

For each fixed integer \(j\ge0\), let
\[
f_j=\frac{\kappa^{(2j)}}{\kappa}-4^{-j},\quad
u_j=\kappa f_j=\kappa^{(2j)}-4^{-j}\kappa,
\quad w_j=\kappa f_j^2.                                 \tag{33}
\]
These are noncompact functions. Strict positivity of \(\kappa\) makes the quotients smooth. For \(x\ge0\), the first positive summand gives
\(\kappa(x)\ge2e^{x/2}z_1^2e^{-z_1}\). The derivative polynomial expansion and
\(\sum n^{2r+4}e^{-(n^2-1)z_1}\le\sum n^{2r+4}e^{-3(n^2-1)}<\infty\)
give, for each fixed \(r\),
\[
|\kappa^{(r)}(x)|/\kappa(x)\le B_r(1+z_1)^r.             \tag{34}
\]
Quotient differentiation gives analogous polynomial-in-\(z_1\) bounds for each fixed derivative of \(f_j\). Together with (6) these imply
\[
f_j\in L^2(\nu),\quad u_j,w_j\in H^1(\mathbb R),
\quad \|u_j\|_W+\|w_j\|_W<\infty.                        \tag{35}
\]
They establish the necessary weighted integrability, not merely \(L^2\) membership of an unweighted derivative.

The source identities extend to \(w_j,u_j\) by the cutoff continuity in §3. Every term in the algebra of §4 is again finite: Gamma by (11) and mixed Cauchy--Schwarz, prime terms by the correlation majorant. Thus (13)--(14) hold for \(f_j\) as well, and \(\mathcal E_\kappa(f_j)<\infty\). This defines its membership in the explicit transformed energy domain; it does not postulate a closed global operator.

Integration by parts \(2j\) times, with all boundary jets vanishing by (6), gives
\[
\int\kappa^{(2j)}(x)\cosh(x/2)\,dx=4^{-j}m_\kappa,
\quad\int f_j\,d\nu=0.                                  \tag{36}
\]
Inherited radicality also gives \(Q(u_j)=0\). Therefore
\[
\boxed{\mathcal E_\kappa(f_j)=\tfrac12\|f_j\|_{L^2(\nu)}^2.} \tag{37}
\]
For \(j=0\) the function is zero. For every \(j\ge1\) it is nonzero: \(\kappa^{(2j)}=4^{-j}\kappa\) would imply \([(-1)^jt^{2j}-4^{-j}]\Xi(t)=0\) near \(t=0\), where \(\Xi(0)>0\), an impossibility.

There is also no global strict improvement of the constant on the smooth even compact core. To see this rigorously, take \(\chi_a f_j\). The corresponding \(u_a=\chi_a u_j\) and \(w_a=\chi_a^2 w_j\) converge in \(W\), while their \(\nu\)-moments converge by (35). Applying (13) to the compact functions and passing to the limit shows convergence of their transformed energies to (37). Hence an inequality \(\mathcal E_\kappa(f)\ge c'\operatorname{Var}_\nu(f)\) for all those compact tests cannot hold with \(c'>1/2\). This is an upper barrier on a possible global constant, **not a proof of the critical global Poincaré inequality itself**. Fixed derivative orders are sufficient for this check; no growing-order assertion is made.

## 9. What is proved, and the exact unproved central term

The new source-specific statement on the searched research-record scope is (28), including the retained-prime rate and its fully tracked Stieltjes remainder. General ground-state algebra, the previously established exact theta transform and saturation, full radicality, theta Mellin normalization, and unconditional PNT are dependencies, not claimed inventions. The exterior result applies to all prescribed smooth tests, not only theta derivatives or finite candidate spaces.

For a general \(f=f_c+f_o\), the exact remaining coupling is
\[
\mathcal E_\kappa(f)=\mathcal E_\kappa(f_c)+\mathcal E_\kappa(f_o)
                    +2\mathcal E_\kappa(f_c,f_o),         \tag{38}
\]
where the bilinear jump integrand is \(\kappa(x)\kappa(x+s)
[f_c(x)-f_c(x+s)][f_o(x)-f_o(x+s)]\), with the same Gamma and prime measures as (14). The associated variance coupling is
\[
\operatorname{Var}_\nu(f)=\operatorname{Var}_\nu(f_c)
 +\operatorname{Var}_\nu(f_o)
 +2\left[\int f_cf_o\,d\nu-\int f_c\,d\nu\int f_o\,d\nu\right]. \tag{39}
\]
Even for disjoint central/exterior supports the jump cross terms need not vanish. The retained exterior--center edges that prove (18) do not give an upper bound on (38). No localization error estimate, small coupling, global critical Poincaré inequality, subcritical spectral discreteness or absence, or full ground-state selection follows here. Fourier truncation and R24/R33 are not used or newly activated.

The prior sign-preservation counterexample remains valid. This is neither a failure nor a proof of the actual 0/4-prolate alignment. The research task ends at the exterior theorem and the fixed-order domain check; it is not expanded into a new spectral program.

## 10. Verification and references

The code verifies exact finite polynomial identities and rational constants, checks snapshot digests and complete package coverage, and runs in a clean Python environment. It does not numerically prove the all-test inequality, formally verify the analytic proof, or independently audit the inherited theorems or the external PNT computation. Those distinctions are recorded in `STATUS.json`, `REPRODUCIBILITY.md`, and `INDEPENDENT_AUDIT_GUIDE.md`.

External sources read for this task:

1. R. L. Frank and R. Seiringer, *Non-linear ground state representations and sharp Hardy inequalities*, arXiv:0803.0503v2, 14 November 2008, §2.1, Assumption 2.1, Proposition 2.3, Remark 2.4. <https://arxiv.org/pdf/0803.0503v2>. General quadratic representation context; the mixed continuous--atomic case above is proved directly.
2. A. Fiori, H. Kadiri and J. Swidinsky, *Sharper bounds for the Chebyshev function* \(\psi(x)\), arXiv:2204.02588v3, 17 May 2023, equation (1.2) and Corollary 1.4. <https://arxiv.org/pdf/2204.02588v3>. Classical unconditional PNT supports existence of a uniform threshold; the explicit corollary supports only the optional effective radius. The version-specific constant is 9.22022; an earlier abstract's 9.22106 is not mixed into this calculation.

Full user-owned inherited proof snapshots and primary-source locators are included in `sources/`. Third-party articles are referenced by exact version and theorem; the bundled external snapshots contain bibliographic metadata and selected mathematical inputs, not copies of complete third-party texts.

```text
EXTERIOR_COERCIVITY = PROVED-AUTHOR-SIDE-FIRST-KEY
THETA_TRANSFORM = VERIFIED-ANALYTICALLY-WITH-INHERITED-RADICALITY
EXTERNAL_INDEPENDENT_AUDIT = NOT-PERFORMED
FORMAL_PROOF_VERIFICATION = NOT-PERFORMED
GLOBAL_CRITICAL_POINCARE = NOT-OBTAINED
FULL_GROUND_SELECTION = NOT-OBTAINED
RH_PROOF = NOT-OBTAINED
RH_DISPROOF = NOT-OBTAINED
V13_TO_RH = CHAIN_UNRESOLVED
```
