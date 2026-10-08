# Validated whole-line actions of the 32 immutable observation-range trials

7 October 2026. Author-side proof and computation (FIRST-KEY). This document
does not claim an external independent audit or proof-assistant verification.

## 1. The precise operator and coordinates

The Hilbert space is the even complexification of \(L^2(\nu)\), where
\(w=2\kappa\cosh(x/2)\), \(\nu(dx)=w(x)dx\), and \(\int w=1\).
The nonnegative jump form has the **minimum** domain obtained by closing the
even smooth compact core. Its representing operator is \(A\), and
\(L=A-I/2+|1\rangle\langle1|/2\). No equality of the minimum and maximum
domains, or identification with a physical finite Weil matrix, is assumed.

Retain \(U f=\sqrt w f\), \(a=\kappa/(2\cosh(x/2))\), \(b=\sqrt a\),
\(p_0=\sqrt w\). Thus \(b p_0=\kappa\). Throughout, the notation \(V_i\)
for a trial in an ordinary-dx formula means the **unitary image** of the
weighted-space trial. An expression \(H_{\rm new}V_i\) in the action target is
interpreted as \(U H_{\rm new}U^{-1}V_i\), not as an operator acting in two
Hilbert spaces at once.

The inherited continuous-cover certificate gives
\[
 H_{\rm new}=L+I/16+W W^*\ge\eta_* I,
 \quad \eta_*=
 \frac{419595679403863743561948335546070649599577}
 {9852167430742733548274812918870793810608128}>3/80.
\]
Its 124 cells have width \(1/2\). Set \(\alpha_s=\sqrt{V_s/\pi}\) and
write \(Q_j\) for the three source-free features in each cell:
\[
 Q_{3s}=\alpha_s(1-x^2/96)\cos(c_sx),\quad
 Q_{3s+1}=-\alpha_s x\sin(c_sx)/(4\sqrt3),\quad
 Q_{3s+2}=-\alpha_s x^2\cos(c_sx)/(48\sqrt5).
\]
Then \(UW_j=bQ_j\). These are the supplied Cholesky coordinates. With
\(G(\alpha)\) as in the inherited proof, its exact LDL factors are
\(L_{20}=\alpha^2/24\) and
\(D=\operatorname{diag}(\alpha,\alpha^3/12,\alpha^5/720)\).
At \(\alpha=1/2\), multiplication of the derivative Riesz functions gives
precisely the two negative signs and the \(1-x^2/96\) mixture above.
The Gram factor is unchanged by using this factor rather than a principal
square root, but T and C would change under a coordinate rotation; no such
rotation is made.

The fixed CSV matrix \(T\) is 372 by 32, with integer numerators divided by
\(2^{30}\). Set \(P_i=\sum_jT_{ji}Q_j\), \(V_i=bP_i\),
\(h_i=aP_i\). The weighted trial is
\(f_i=U^{-1}V_i=P_i/(2\cosh(x/2))\).
The saved 32 by 372 matrix C is preserved and not used for optimization or
an inverse in this task. Neither exact orthonormality of V nor a diagnostic
eigenvalue is a premise.

Every centre satisfies \(16c_s\in\mathbb Z\). Let \(m_s=16c_s\),
\(m_*=\max m_s\), and \(c_*=m_*/16<2048\). A useful exact rational
coefficient majorant, evaluated from T alone, is
\[
 A_i=2\sum_s\left(\frac{97}{96}|T_{3s,i}|
       +\frac14|T_{3s+1,i}|+\frac1{48}|T_{3s+2,i}|\right)<128.
\]
Indeed \(\alpha_s<2\), since \(V_s<12\) and \(\pi>3\). The total absolute
coefficients of the three terms \(x^r\cos(c_sx)\) or \(x\sin(c_sx)\)
in \(P_i\) are at most \(A_i\), and
\(|P_i(x)|\le A_i(1+x^2)\).

## 2. Minimum operator-domain admission

This is a fresh admission for these noncompact trials. A bounded observation
alone would not imply operator-domain membership.

The actual source is the even analytic theta function
\[
 \kappa(x)=e^{x/2}\sum_{n\ge1}(4z_n^2-6z_n)e^{-z_n},
 \quad z_n=\pi n^2e^{2x}.
\]
Its evenness, probability normalization, minimum-form source identity, and
norm-convergent sandwiched prime series are inherited with their proof
snapshots and exact source identities. On the compact core, and then on its
completion, the source identity is
\[
 \mathcal E(f)=\tfrac12\|Uf\|_2^2+D_\Gamma(\kappa f)
       -c_\Gamma\|\kappa f\|_2^2-\langle Uf,K_pUf\rangle,
\]
\[
 D_\Gamma(h)=\int_0^\infty\rho(s)\|h-\tau_sh\|_2^2ds,
 \quad \rho(s)=\frac{e^{-s/2}}{1-e^{-2s}},\quad \tau_sh(x)=h(x+s).
\]
Here \(c_\Gamma=\log\pi+\gamma_{\rm E}+\pi/2+3\log2\), and
\(K_p=\sum\Lambda(n)n^{-1/2}M_b(\tau_{\log n}+\tau_{-\log n})M_b\).

All derivatives of \(aP_i\) are square-integrable and decay faster than any
exponential; this follows directly from the normally convergent theta
series, its even analytic continuation and finite trigonometric-polynomial
factors. The weighted trial f is smooth, even and bounded, with polynomial
times \(e^{-|x|/2}\) bounds for all its derivatives. Choose even compact
cutoffs \(\zeta_R\), equal to 1 on [-R,R], with derivatives of order j
bounded by constants times \(R^{-j}\).
Then \(\zeta_R f\to f\) in \(L^2(\nu)\), and
\(\kappa\zeta_R f\to\kappa f\) in \(H^1(dx)\).
The inequality
\[
 D_\Gamma(h)\le \|h'\|_2^2\int_0^1s^2\rho(s)ds
                 +4\|h\|_2^2\int_1^\infty\rho(s)ds
\]
and the bounded prime operator show that these compact cutoffs are Cauchy
in the minimum form norm, by applying the core source identity to their
differences. Thus f lies in the minimum form domain, without any density
claim for the maximum integral domain.

For \(h\in H^2\), the Bochner integral
\[
 G_\Gamma h=\int_0^\infty\rho(s)[2h-h(\cdot+s)-h(\cdot-s)]ds
\]
converges in \(L^2(dx)\): its integrand norm is at most
\(s^2\|h''\|_2\) near zero and \(4\|h\|_2\) away from zero.
Since \(b\le1\), the following vector is in \(L^2(dx)\):
\[
 \mathscr H_i=V_i/16+bG_\Gamma h_i-c_\Gamma aV_i
 -b\sum_{n\ge2}\frac{\Lambda(n)}{\sqrt n}
          [h_i(x+\log n)+h_i(x-\log n)]
 +\frac{p_0}{2}\int\kappa P_i
 +b\sum_{j=0}^{371}Q_j\int aQ_jP_i.                 \tag{1}
\]
The prime term is the bounded sandwiched operator, not a separately assumed
bounded unsandwiched prime gain. The pole and finite frame are bounded
operators. Polarizing the minimum-form source identity gives the pairing
of (1) with every compact core test. Passing through the cutoffs and using
form density extends that pairing to the minimum form domain. The closed
form representation theorem therefore gives \(f_i\in D(L)=D(H_{\rm new})\)
and (1) is its actual action. No unknown spectral gap or RH is used.

## 3. Explicit new analytic source bounds

For \(|\Im z|\le1/8\), put \(t=e^{2|\Re z|}\). Normal convergence of the
full theta series and its even identity apply in this strip. Since
\(\cos(1/4)>31/32\), \(3<\pi<4\), and
\(\sum_{n\ge1}n^4e^{-2(n^2-1)}<2\), direct absolute bounds give
\[
 |a(z)|\le256e^{4|\Re z|-(5/2)e^{2|\Re z|}},\qquad
 |\kappa(z)|\le256e^{5|\Re z|-(5/2)e^{2|\Re z|}}.       \tag{2}
\]
For example \(|4z_n^2-6z_n|\le6|z_n|^2\), the theta sum is at most
\(192e^{(9/2)x-(93/32)e^{2x}}\) for \(x\ge0\), and
\(|2\cosh(z/2)|\ge(127/128)e^{x/2}\). Reflection treats negative x.

For \(0\le r\le4\) in \(z^ra(z)\), or \(0\le r\le2\) in
\(z^r\kappa(z)\), both the strip supremum and each horizontal L1 integral
are less than \(2^{20}\). Here is an explicit generous check: on \(0\le x\le1\)
use \((x+1/8)^4<2\), \(e^4<64\), \(e^5<256\).
The two-sided central integral is at most 65536 for a and 262144 for kappa.
For \(x\ge1\), \((x+1/8)^r\le2e^{rx}\); substituting t bounds the
two-sided remainder by \(512\int_7^\infty t^3e^{-(5/2)t}dt<3072\).
The analogous pointwise bound follows from \(t^4e^{-t}\le256\).
In particular the kappa horizontal L1 bounds are individually below
\(2^{19}\), and \(\int\kappa(1+x^2)<2^{20}\).
Contour displacement to \(\Im z=\pm1/8\), with the vanishing vertical
tails from (2), is justified and gives the Fourier bound used below.

On the real line the inherited full-source estimate
\(a\le41e^{4|x|-3e^{2|x|}}\) gives
\(\int a x^r<2^{13}\), for even \(r=0,2,4\): the central integral is
at most 5248 and the remaining integral is at most
\(41\int_0^\infty t^3e^{-t}dt=246\).
Consequently
\[
 \|b(1+x^2)\|_2<2^{10},\quad \|V_i\|_2\le2^{10}A_i,
 \quad \|UW_j\|_2\le2^{11}.
\]
Also \(\int a\le1/4\), since
\(a\,dx=\nu(dx)/(4\cosh^2(x/2))\). Thus \(\|b\|_2\le1/2\).

The eight-term even real source \(\kappa_8\) used in the finite output
function obeys a **uniform full-line** error
\[
 0\le\kappa-\kappa_8<128\,9^4e^{-243}<2^{-320}.        \tag{3}
\]
Every omitted term decreases on the positive half-line, and at zero
\(4\pi^2n^4e^{-\pi n^2}\le64n^4e^{-3n^2}\). Starting at n=9, the
successive majorant ratio is less than \(2e^{-57}<1/2\).
It follows that \(0\le a-a_8\le2^{-321}\) and
\(|b-b_8|\le\sqrt{2^{-321}}<2^{-160}\).
No analyticity of the even **finite** reflected source is asserted at zero;
analytic estimates concern the true infinite source only.

## 4. Commensurate validated source transforms

Set \(P=32\pi\), \(N=65536\), \(K=8192\), and grid
\(x_l=-P/2+lP/N\). The spectral frequencies are \(k/16\), so all
modulations by the actual centres have integer shifts \(m_s=16c_s\).
For a source \(F_r(x)=x^ra(x)\) (r=0,...,4) or
\(x^r\kappa(x)\) (r=0,...,2), its periodization is
\(F_{r,P}=\sum_{j\in\mathbb Z}F_r(x+jP)\). Its exact coefficient is
\[
 d_{r,k}=P^{-1}\int_{\mathbb R}F_r(x)e^{-i(k/16)x}dx,
 \qquad |d_{r,k}|\le C e^{-|k|/128},\quad C=2^{20}.     \tag{4}
\]
The bound is intentionally larger than the horizontal integral divided by P.
All derivatives and periodized series converge locally uniformly.

The computed forward transform is \((-1)^k\operatorname{DFT}_k/N\).
The phase and normalization are independently checked on a four-term
exact DFT, and by parity of every retained component. Sampling uses the
eight-term source for |x|<=3 and exactly zero elsewhere. The source error
in the sampled powers is at most \(81\,2^{-320}\). For |x|>=3, (2) and
\(e^6>400\) give
\(512\cdot400^4e^{-1000}<2^{-1000}\). The same decreasing exponential
majorant sums all omitted periodic copies. Finally sampling alias at a
retained index is bounded by
\[
 2C\frac{e^{-(N-K)/128}}{1-e^{-N/128}}.
\]
The sum of these three biases is less than \(2^{-300}\). That bias is added
to the actual native validated DFT enclosure of **every** retained coefficient;
all primitive source, argument, pi, DFT and serialization rounding is included.
The sampled arrays are not used as a smooth compact substitute for F.

Even r coefficients are real, odd r coefficients are imaginary. Their
inactive components must contain zero. Saved coefficient midpoint and
radius integers have denominator \(2^{140}\). This is enclosure storage,
not an assumed accuracy from working precision alone.

## 5. Noncompact Gamma: convolution, frequency tail and physical images

The exact multiplier is
\[
 m_\Gamma(\xi)=2\sum_{j\ge0}\frac{\xi^2}{a_j(a_j^2+\xi^2)}
 =\Re\psi(1/4+i\xi/2)-\psi(1/4),\quad a_j=2j+1/2.
\]
There is no additional factor two. It obeys \(0\le m_\Gamma(\xi)\le20\xi^2\):
\(2\sum a_j^{-3}<17<20\).

Write P_i as its degree-0 cosine, degree-1 sine and degree-2 cosine pieces.
Multiplying the truncated periodizations of \(a,xa,x^2a\) by these finite
modulations gives Fourier coefficients by three ordinary polynomial
convolutions, at precisely the original frequencies. This is an exact
algebraic operation on the enclosed coefficients; native Arb/Acb polynomial
arithmetic propagates every input radius. The resulting range is
\(|k|\le K_{\rm out}=K+m_*\). The degree-1 positive modulation coefficient
is \(+i\alpha_sT_{3s+1,i}/(8\sqrt3)\); its negative counterpart is its
conjugate. This sign implements the original negative sine feature.

Multiplication by the validated m array, projection onto the exact even
real symmetry, and conversion to exact dyadic **cosine** coefficients
produces \(T_i(x)=\sum_{k=0}^{K_{\rm out}}t_{ik}\cos(kx/16)\).
DC is exactly zero; positive cosine coefficients are twice the complex
Fourier coefficients. The measured sum of outward coefficient discrepancies
\(e_{\Gamma,i}\) bounds the uniform arithmetic/finite-coefficient error.
No inverse DFT or off-grid interpolation is necessary for this finite analytic
output format. This is a choice of representation, not a deletion of a
continuous-model error.

Let \(t=e^{-1/128}\), \(B=(K+1)/16+c_*\). The full omitted Fourier tail
of the periodized Gamma action is bounded uniformly by \(A_i T_*\), where
\[
 T_*=40C t^{K+1}\left[
 \frac{B^2}{1-t}+\frac{Bt}{8(1-t)^2}
 +\frac{t(1+t)}{256(1-t)^3}\right].                  \tag{5}
\]
This is the exact geometric sum of \(40C\sum_{k>K}t^k(k/16+c_*)^2\).
The arbitrary coefficients in the fixed trial combination are accounted
for by A_i, not by a diagnostic trial norm.

It remains to relate a **periodized** Gamma action to the true whole-line
one. From (2) and finite frequencies,
\(\int e^{|y|/2}|h_i(y)|dy\le2^{20}A_i\). For |z|>=48, Cauchy's
derivative bound on a circle of radius 1/8 gives
\(|h_i(z)|,\sup_{|y-z|\le1}|h_i''(y)|\le A_i e^{-|z|}\), with a
harmless factor e absorbed in the following bound. For completeness, its
majorant has exponent
\(256+4(|z|+1/8)-(5/2)e^{2(|z|-1/8)}\) and polynomial factor
\(32768(1+(|z|+1/8)^2)\); at |z|>=47 the negative term dominates by
\(e^{2|z|-1/4}\ge(2|z|-1)^4/24\).
Splitting the Gamma second difference at s=1, using
\(\rho(s)\le4/(3s)\) near zero and
\(\rho(s)\le(4/3)e^{-s/2}\) afterwards, yields
\[
 |G_\Gamma h_i(z)|\le2^{22}A_i e^{-|z|/2}\quad (|z|\ge48).
\]
Uniform convergence and the second-difference bounds justify interchange
with the periodized sum. For |x|<=2 the image discrepancy is at most
\[
 A_i P_*,\qquad
 P_* =2^{23}e\frac{e^{-P/2}}{1-e^{-P/2}}.             \tag{6}
\]
The L2 error after multiplying (5), (6), and the finite coefficient error
by b is at most \((A_i T_*+A_i P_*+e_{\Gamma,i})/2\).
Thus both the new noncompact physical-image error and the infinite
frequency tail are present in the certificate.

## 6. Full frame and pole, without a false finite-interval truncation

At every commensurate frequency \(k/16\),
\(\int F_r(x)e^{-i(k/16)x}dx=P d_{r,k}\).
For |k|>K, its enclosure is the ball centered at zero with radius
\(PCe^{-|k|/128}\); it is never silently set to exactly zero.
Parity gives the cosine moments for even r and the signed sine moments
for odd r. Cosine-cosine, sine-sine, and mixed cosine-sine product identities
then give the actual full-line source overlaps
\(\int aQ_jQ_l\), followed by multiplication by the fixed T to obtain
\(d_{ji}=\int aQ_jP_i\). The small source-overlap cache used for this
**frame action** is not a residual Gram, inverse matrix or spectral matrix.
All 372 coordinates remain in the resulting action. No principal-root
coordinate change or old 1024-observation action is substituted.

The pole moment \(p_i=\int\kappa P_i\) uses the other three shared source
transforms. Since \(\|p_0\|_2=1\), its dyadic midpoint error contributes
\(e_{p,i}/2\) to the action norm. If \(e_{d,ji}\) is the outward frame
coefficient discrepancy, the frame error is at most
\(2^{11}\sum_j e_{d,ji}\). All moment, source, infinite-tail and finite
arithmetic uncertainties are in these balls. No floating diagnostic array
is a moment input.

## 7. Infinite primes, exterior norm, and the stored approximant

Retain all 18 actual prime powers n<=32, including n=4,8,9,16,25,27,32,
with \(\Lambda(p^r)=\log p\), and both shift directions once. The inherited
full sandwiched operator bound gives
\[
 \|K_p-K_{p,\le32}\|\le
 d_{32}=\frac{14(9\cdot32^2+24\cdot32+20)}{27\cdot4^{32}}.
\]
Hence the whole-line omitted-prime action error is at most
\(2^{10}A_i d_{32}\), not a replacement for all other errors.

Let \(Y=e^4\) and
\(I_j(Y)=\int_Y^\infty t^j e^{-3t}dt\), an explicit polynomial times
\(e^{-3Y}\). The exact rational/ball checks show
\(164I_3(Y),164I_2(Y)<2^{-190}\).
They bound, respectively,
\(\|1_{|x|>2}b(1+x^2)\|_2^2\) and
\(\|1_{|x|>2}p_0\|_2^2\).
To check the Gamma exterior, the strip supremum of \(x^ra\) and Cauchy's
formula give \(\|(x^ra)'\|_\infty\le2^{23}\) and
\(\|(x^ra)''\|_\infty\le2^{27}\). Product differentiation with c_*<2048
therefore gives \(\|h_i''\|_\infty<2^{43}A_i\) and
\(\|G_\Gamma h_i\|_\infty<2^{44}A_i\).
Each exact frame coefficient is at most \(2^{21}A_i\); there are 372
features bounded by \(2(1+x^2)\). The pole moment is at most \(2^{20}A_i\).
The sum of the 18 retained prime weights is less than 32.
Together these bounds give a conservative exterior norm
\[
 \|1_{|x|>2}\mathscr H_{i,\le32}\|_2\le A_i2^{-50}.    \tag{7}
\]
Here \(\mathscr H_{i,\le32}\) retains the **true** full Gamma, pole, frame
and source but cuts only the prime sum. The omitted prime term has already
been counted globally by d32; it is not omitted from (1) or counted as a
second copy of an exterior estimate.

The saved finite analytic function, supported on [-2,2], is
\[
 g_i=b_8P_i/16+b_8T_i-c_\Gamma a_8b_8P_i
 -b_8\sum_{n\le32}\frac{\Lambda(n)}{\sqrt n}
                 [a_8(x+\log n)P_i(x+\log n)
                  +a_8(x-\log n)P_i(x-\log n)]
 +\frac{p_{0,8}}2\widetilde p_i
 +b_8\sum_{j=0}^{371}Q_j\widetilde d_{ji},           \tag{8}
\]
and is zero outside. Here \(p_{0,8}=2b_8\cosh(x/2)\), and all t, d and
p tildes are exact stored dyadic coefficients. The finite theta formula,
the original exact T and cells, and the explicit constants log, pi and
square roots completely specify (8). There is no uncomputed H inverse or
source integral in this representation.

For |x|<=2, all prime arguments have |y|<6 and
\(|P_i(y)|\le37A_i\). Put e=2^-160, S_i=\sum|t_{ik}|,
and D_i=\sum_j|\widetilde d_{ji}|. The finite-source transfer in (8) is
bounded uniformly by
\[
 e\{A_i(5/16+30+2368)+S_i+2|\widetilde p_i|+10D_i\}. \tag{9}
\]
For the prime product,
\(\sqrt{2^{-321}}+2^{-321}<2^{-160}\), so each \(ba_y\) discrepancy
is at most e; this explains the factor 2 directions times 37 times 32.
For the local \(a^{3/2}\), the Lipschitz bound on [0,1] is 3/2 and its
tiny source error is dominated by e. Since [-2,2] has length 4, the L2
contribution of (9) is twice this uniform bound.

The final certificate adds exactly: the Gamma Fourier tail, physical
periodic images, measured finite Gamma coefficient error, infinite prime
tail, full frame coefficient error, pole coefficient error, (9), and (7).
There is **zero spatial interpolation error** because (8) itself is the
stored representation. This is distinct from evaluating (8) in ball
arithmetic, whose point enclosures include rounding and are checked.
The certificate must verify the exact sum is <2^-18 for every column.

## 8. Reproduction and scope

The immutable input hashes, core-domain argument, analytic constants and
resource policy are checked before the common-cache pilot. At most one
fixed pilot column is computed and retained. If its measured cost predicts
the remaining 31 columns fit 600 seconds and 512 MiB, the fixed main run
executes them once. The pilot, all shared transforms and all moments are
reused, not regenerated. Every native transform, convolution, source and
full-expression evaluation is counted. Saved lightweight verification
checks hashes, enclosures, coefficient symmetry, arithmetic error sums,
and finite function assembly; it does not rerun transforms or actions.

The consumer must read (8) through the supplied evaluator, in U coordinates.
These files are **not** the older 256- or 512-panel Chebyshev format. A
future Gram integral must include all remaining weighted/ordinary-dx
coordinate factors and its own quadrature and action-error propagation.
The present result alone is not a residual Gram/LDL, Bnew<I, a -1/16
spectral exclusion, an all-negative-spectrum exclusion, or RH.

Primary numerical-library contracts checked: python-flint 0.9.0 `acb`
rectangular ball arithmetic, `acb.dft`, and native `acb_poly` arithmetic:
https://python-flint.readthedocs.io/en/latest/acb.html
and https://python-flint.readthedocs.io/en/latest/acb_poly.html
(accessed 7 October 2026). The four-entry exact DFT checks the sign and
normalization independently of a prose interpretation of the API.

RH_PROOF=NOT-OBTAINED; RH_DISPROOF=NOT-OBTAINED;
V13_TO_RH=CHAIN_UNRESOLVED.
