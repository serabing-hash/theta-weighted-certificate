# Every finite prime head has infinite signed index on the actual radical

3 November 2026 UTC. An actual theta/Gamma/prime obstruction, not a generic matrix model. This proves a signed statement on admitted derivative radicals; no historical novelty claim is made. It does not prove a negative direction for the complete form, control an exhaustive historical theta_j, or exclude the negative-eigenvalue collar.

## Result

Let

    q_M[u] = t_Gamma[u] - c_Gamma ||u||_2^2 - p_{<=M}[u],
    p_{<=M}[u] = 2 Re sum_{2<=n<=M} Lambda(n)/sqrt(n)
                          integral u(x+log n) conjugate(u(x)) dx,

where M is any fixed finite integer >=1. No Gamma shift is truncated. Let R be the algebraic span of the actual full-domain derivative radicals

    r_j = kappa^(2j) - 4^(-j) kappa,  j>=1.

Then BOTH the positive and negative indices of q_M restricted to R are infinite. Equivalently, for every integer r>=1 there are r-dimensional actual finite-radical source spaces on which q_M is strictly positive definite, and others on which it is strictly negative definite.

Because the COMPLETE actual form satisfies q_0(r,z)=0 for r in R and z in X, the exact untruncated prime remainder satisfies

    p_{>M}|_R = q_M|_R.                               (1)

Thus the actual infinite prime tail also has infinite positive and negative indices on the known radical, for EVERY finite cutoff M. An arbitrarily small weighted-H operator norm does not change this fact.

In particular, finitely many radical deflations, finitely many exact linear constraints, or any finite-rank Hermitian correction cannot make the finite-head form nonnegative on the remaining full centered domain. They cannot annihilate the entire tail error on the radical either. The complete q_0 remains EXACTLY ZERO on all these witnesses; none is an actual negative q_0 source.

## 1 Actual normalization and admitted witnesses

Use the normalization of unified_theta_energy_20261103/unified_theta_energy.tex:

    F_kappa(z)=Xi(z),  Xi(+-i/2)=1/2,
    H=L2_even(dx/W),  W=kappa/(2 cosh(x/2)),
    H_c=ker m,  C u=u-2m(u)kappa,
    N=closure_H(R),  K=N^perp intersect H_c.

Here L_c is the self-adjoint representative of q_0 on X_c. N is the entire KNOWN derivative-radical closure. It is not silently identified with the entire physical kernel, and K is not identified here with an ordinary zero-jet closure. Those are separate questions in other source conventions.

For a polynomial P in one real variable define the concrete source

    r_P = (-partial_x^2+1/4) P(-partial_x^2) kappa.

It is a FINITE linear combination of the r_j. Indeed the polynomial
Q(y)=(y+1/4)P(y) vanishes at y=-1/4, which is exactly the coefficient relation for a finite centered derivative combination. The complete theta derivative estimates admit r_P to the actual operator domain, and the full-domain radical identity gives

    m(r_P)=0,  L_c r_P=0,  q_0(r_P,z)=0 for every z in X.       (2)

Its ordinary nonunitary Fourier transform is exactly

    F_(r_P)(t) = (t^2+1/4) Xi(t) P(t^2).                      (3)

There is no additional factor 2 in this normalization. Every vector used below is of the concrete form (3), not merely an H-limit or an unadmitted Fourier trial.

## 2 Weighted ordinary density of this finite radical family

Put

    w(t)=1+log(2+|t|),
    R(t)=(t^2+1/4)Xi(t),
    dmu(t)=w(t)|R(t)|^2 dt.

The fixed-strip full-theta bound implies, for every fixed 0<a<pi/4,

    |Xi(t)| <= C_a exp(-a|t|),  t real.                     (4)

For completeness, use F_kappa(t)=integral kappa(x)exp(itx)dx (equal to its cosine transform by evenness). Shift the Fourier contour to Im x=+a for t>0 and to Im x=-a for t<0. The factor exp(it(x+ia)) contributes exp(-at) when t>0. The complete strip envelope is integrable and decreases double-exponentially at both ends, so the vertical end integrals vanish. This proves (4) without a zero-location assumption or a prime estimate.

Consequently mu has a positive exponential moment:

    integral exp(b|t|) dmu(t) < infinity

for some b>0. It is finite, even, and positive almost everywhere, since Xi is a nonzero entire function and has only a discrete real zero set.

The polynomials P(t^2) are dense in L2_even(mu). Here is a proof that retains the weight. If an even f in L2(mu) is orthogonal to every t^(2j), the finite complex measure dnu=f dmu has an exponential moment by Cauchy--Schwarz. Its Fourier transform is holomorphic on a strip containing the real axis. Every derivative at zero vanishes: the even ones by the polynomial orthogonality, the odd ones by parity. Its Taylor series, then the identity theorem, give zero Fourier transform. Fourier uniqueness for finite measures gives f=0 mu-almost everywhere.

Multiplication by R identifies this with the density statement

    { R(t)P(t^2) : P polynomial }
         is dense in L2_even(w(t)dt).                       (5)

Indeed, for any phi in that target space take f=phi/R away from the discrete zeros and define it arbitrarily at the zeros. Then ||f||_(L2(mu))=||phi||_(L2(w dt)). Approximate f by polynomials and multiply by R. No inverse lower bound for Xi is used.

This is an ORDINARY Fourier-space density statement. It does not claim density of the radical in H or X. Those topologies are stronger, and the witnesses may have very large H norm.

## 3 The exact finite-head multiplier has open sets of both signs

Because the head has finitely many terms, Plancherel gives on every r_P

    q_M[r_P] = (1/(2pi)) integral g_M(t)|F_(r_P)(t)|^2 dt,

    g_M(t)=d_Gamma(t)-c_Gamma
              -2 sum_{2<=n<=M} Lambda(n)/sqrt(n) cos(t log n).     (6)

The Gamma symbol is complete. Its retained bounds give

    d_Gamma(0)=0,
    d_Gamma(t)=log|t|+O(1) as |t|->infinity.

In particular g_M is continuous and even, and

    g_M(0)=-c_Gamma-2 sum_{2<=n<=M} Lambda(n)/sqrt(n)<0,
    g_M(t)->+infinity as |t|->infinity.                       (7)

Only c_Gamma>0 and nonnegative von Mangoldt weights are used in the first sign. There is an open interval I_- around zero on which g_M<=-c_Gamma/2. There is also a bounded symmetric open set I_+ at sufficiently large frequency on which g_M>=1.

Moreover |g_M(t)|<=C_M w(t). Thus the quadratic and polarized forms in (6) are continuous for the norm used in (5). This is crucial: ordinary L2 density alone would not control the full unbounded Gamma symbol.

## 4 Infinite negative and positive indices

Fix any r. Choose r even, ordinary-L2-orthonormal smooth functions phi_1,...,phi_r supported in I_-. Their multiplier Gram satisfies

    (1/(2pi)) integral g_M(t)
           |sum c_i phi_i(t)|^2 dt <= -a_M sum |c_i|^2,

with a_M>0. By (5), approximate each phi_i by an actual F_(r_(P_i)) in L2(w dt). Continuity of the polarized form and finite-dimensionality make its whole r-by-r Gram as close to the displayed strictly negative matrix as desired. The ordinary Gram can simultaneously be made close to the identity, so the r_Pi are independent. Their actual finite-radical span is strictly q_M-negative.

Repeat on I_+ to obtain an r-dimensional strictly q_M-positive actual radical span. Since r is arbitrary, both indices are infinite. Real polynomials can be used: the measure and real-even targets are real, and taking the real part of each approximating polynomial can only improve the real-target approximation.

Finally q_0=q_M-p_{>M}, with all prime powers in the tail retained. Equation (2) proves (1), including its polarized version on R. This proves the asserted two-sided signed tail obstruction.

## 5 No finite-rank endpoint repair

Let ell_1,...,ell_k be ANY k linear constraints on the algebraic radical. Choose a strictly q_M-negative space of dimension k+r. Its intersection with all their kernels has dimension at least r and remains strictly q_M-negative. The same statement holds for a strictly positive space. Thus imposing finitely many radical orthogonality conditions does not change either infinite index.

If F is any finite-rank Hermitian correction, its radical on R has finite codimension. Intersect with that radical as above. Hence q_M+F still has infinite positive and negative indices on R. In particular a fixed-rank soft-mode subtraction cannot repair the whole finite-head endpoint form on the centered space.

This does NOT say a rank-adapted correction on one fixed finite source list is impossible, or that the same claim holds on K=N^perp intersect H_c. The witnesses here are in N, not in K. Exact removal of the entire KNOWN derivative radical N is a different operation from finite deflation and does avoid this specific obstruction.

## 6 Quantitative compatibility with the exponentially small true tail norm

The complete actual theta series gives the uniform envelope

    W(x)<=40 exp(4|x|-pi exp(2|x|)).

Here is a short proof with no theta-term truncation. For x>=0, use exp(x/2)/(2cosh(x/2))<=1, drop only the negative -6tau term for an UPPER bound, and retain every theta summand:

    W(x)<=4pi^2 exp(4x-pi exp(2x))
                     sum_{n>=1} n^4 exp(-pi(n^2-1)).

The ratio of consecutive terms in that last positive series is at most 16exp(-3pi)<1/500, so its sum is at most 1/(1-16exp(-3pi))<500/499. The inequality exp(3pi)>8000 follows from pi>3 and exp(3)>20; the latter follows from the positive exponential series through degree eight. Finally 4pi^2(500/499)<40, for example using pi<22/7. Evenness handles x<0.

For s=log n and a=|x|, b=|x+s|, put t=a+b>=s. This envelope and exp(2a)+exp(2b)>=2exp(t) give

    sqrt(W(x)W(x+s))
       <=40 exp(2t-pi exp(t))
       <=40 n^2 exp(-pi n),  n>=2,

because v^2exp(-pi v) decreases for v>=n>=2. Under the exact isometry u->u/sqrt(W), the n-th actual prime term is the pair of weighted translations with coefficient Lambda(n)/sqrt n. Bound each single shift in the ambient non-even weighted/ordinary spaces; a single shift need not preserve evenness. Their +/- pair does preserve evenness, and each single-shift norm is at most the displayed supremum. Therefore the COMPLETE tail, with both orientations and every prime power, satisfies

    ||D_{>M}||_(H->H)
       <= tau_M := 80 sum_{n>M} Lambda(n)n^(3/2) exp(-pi n).    (8)

Here D_{>M} is the actual bounded operator representing p_{>M}, with both shift orientations. The series converges absolutely in H-operator norm. No value or sign of this tail is discarded in Sections 1--5; (8) is used only for the following size comparison.

The negative-band approximation in Section 4 can be chosen so, after ordinary normalization, a concrete finite radical r obeys

    ||r||_2=1,  q_M[r]<=-c_Gamma/4.

Then (1) and (8) force

    ||r||_H^2 >= c_Gamma/(4 tau_M).                       (9)

Thus the ordinary-density argument is not smuggling in bounded H conditioning. As the head grows, some witnesses necessarily escape to extremely large weighted norm. A tiny H-operator norm can still have both signs and infinite index.

An elementary closed bound, requiring no prime enumeration, is

    tau_M <=160(M+1)^2 exp(-pi(M+1)).                     (10)

Indeed Lambda(n)<=log n<=sqrt n, and with n=M+1+k use
(M+1+k)^2<=(M+1)^2(k+1)^2. The remaining series is
sum_(k>=0)(k+1)^2 exp(-pi k)<2, because exp(-pi)<1/20.

Equation (9), using (10), permits witnesses with H/ordinary amplification at least a constant times exp(pi(M+1)/2)/(M+1). This is a lower bound on the norm required by the constructed negative ordinary-normalized witnesses, not a negative defect for q_0.

For a given 0<delta<=1, the explicit cutoff

    M(delta)=ceil(3+log(1/delta))

ensures tau_M<delta. To check this put L=log(1/delta), use pi>3 and 4+L<=M+1<=5+L:

    tau_M<=160(5+L)^2 exp(-12-3L)
          <=4000 exp(-12) delta < delta.

The middle step uses (1+L/5)^2exp(-2L)<=1 for L>=0: its logarithmic derivative is 2/(5+L)-2<0 and its value at zero is one. The last step follows from exp(12)>2^12=4096>4000. Thus the true prime tail is inexpensive to bound at each FIXED positive target shift. The obstruction is endpoint SIGN and exact null cancellation, not convergence of the all-prime series.

## 7 Actual endpoint consequences and actionable continuation

For each fixed M choose one actual r with q_M[r]<0. The positive number

    sigma_M=-q_M[r]/||r||_H^2

satisfies 0<sigma_M<=tau_M. For 0<sigma<sigma_M,

    (q_M+sigma||.||_H^2)[r]<0,

although the COMPLETE shifted form equals sigma||r||_H^2>0 on this same known radical. Consequently a fixed finite prime head cannot be certified nonnegative all the way down to zero shift on the full centered space, even under the hypothesis that the desired full sign is true. These are genuine truncation-induced negative directions.

There are two legitimate next routes:

1. Retain the complete prime tail together with its exact null cancellation. A scalar positive norm debit cannot replace this at an endpoint null direction.
2. Work after exact removal of the entire known derivative radical N, and ultimately the entire physical kernel when needed. If P_K projects onto K=N^perp intersect H_c, then the null-preserving head operator is

       qhat_M(u,v)=q_M(P_Ku,P_Kv),
       Lhat_M=P_K L_M P_K extended by zero on N,

   with the latter read as FORM COMPRESSION. Here L_M means the self-adjoint form operator of q_M on the centered H_c. The uncentered raw finite-prime operator is not claimed to preserve H_c or K. Its bounded tail perturbation is compressed by the same centered projection C when it is restricted to H_c.

   Since the complete L_c annihilates N and reduces K,

       Lhat_M-L_c=P_K C D_{>M} C P_K,
       ||Lhat_M-L_c||<=tau_M.

   This follows directly at the form level from q_M=q_0+p_{>M} and q_0(P_Ku,P_Kv)=q_0(u,v); the bounded perturbation then identifies the self-adjoint operator with domain Dom L_c. No separate domain/invariance assertion for the raw finite-head operator is used.

   This removes the demonstrated radical artifacts, but the signed range-sector inequality remains unproved. Finite radical deflation is not an authorized substitute for this infinite projection, and no algorithm for that projection is supplied here.

Neither route supplies theta_j<1 for the exhaustive ordinary history or signs the remaining low Schur matrix. The result identifies an exact actual-arithmetic barrier that any finite-prime shortcut must handle rather than assuming a uniform gap, a rank-one soft space, or positivity of a tiny error.

## Inputs and verification boundary

- unified_theta_energy_20261103/unified_theta_energy.tex: full-domain derivative radicals, Lemma a:lem:radical; complete strip envelope, Lemma d:lem:theta-tails; normalization F_kappa=Xi; complete Gamma multiplier and logarithmic growth.
- Section 6 proves the all-prime tail constant 80 in (8) directly from the entire theta series and the weighted-shift representation. Sections 1--5 and the infinite-index theorem do not rely on that constant or its numerical sharpness.
- Every new witness is a finite polynomial differential operator applied to the ACTUAL complete kappa, hence an actual finite derivative radical with every theta term and prime power retained.
- No matrix/zero/prime enumeration, long run, numerical theta calculation, external transmission, or endpoint positivity claim was made.
