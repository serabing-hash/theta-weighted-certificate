# Independent audit: subpolynomial negative counts and every positive Schatten exponent

3 November 2026 UTC. Mathematical proof audit only. No numerical run, inverse solve, runtime estimate, or zero-sign assertion was used.

## Verdict and exact scope

The stronger consequence is valid. For the complete centered theta/Gamma/prime operator described below,

    dim Ran 1_(-infinity,-delta](L_c)
        <= exp(O(sqrt(1+log(1/delta)))), delta -> 0+,

and consequently

    (L_c)_- in S_p for every p>0, including S_1.

The proof uses a genuine finite-dimensional source subspace in the actual weighted Hilbert space, not a coefficient-space identity Gram. Its source columns need only belong to that Hilbert space. The negative spectral vectors, rather than the source columns, supply all operator-domain membership needed by the argument.

The audit found no missing cross term, Fourier factor, centering tail, prime power, or threshold multiplicity. It does not certify the inverse-residual interface of Section 6 of the companion source-compression note. It independently verifies the compression, actual negative-count, and Schatten consequences in its Sections 1-5 and 7-8. Trace class does not imply nonnegativity, finite negative index, a gap at zero, or RH.

The companion note examined was `EXPLICIT_POSITIVE_SOURCE_COMPRESSION_AUDIT.md`, SHA256 `136bebc353c898d74ff3f817836a813022d39e7cfb7cfa4858222d757f75763d`. Its provisional wording is a publication-status issue, not a mathematical defect in the audited consequence.

## 1. Actual space, normalization, and full-domain decomposition

Use natural logarithms unless a base is displayed. The Hilbert space and projection are

    H = L2_even(R,dx/W), W= kappa/(2 cosh(x/2)),
    ||kappa||_H=1, C=I-kappa tensor kappa, H_c=kappa^perp.

The actual theta formula is positive on the full line. In particular W and kappa are strictly positive everywhere, and

    B0 := integral_R W(x) dx <= 1/4.

Indeed the normalization is integral 2 cosh(x/2) kappa(x) dx=1, while

    W(x) = [2 cosh(x/2) kappa(x)]/[4 cosh(x/2)^2].

The full theta envelope, not a finite theta truncation, gives

    W(x) <= 40 exp(4|x|-pi exp(2|x|))
          <= 40 exp(4|x|-3 exp(2|x|)).                 (1)

Let J:H->L2_even(dx) be inclusion and F the unitary Fourier transform with factor (2pi)^(-1/2). The full centered closed form has domain

    X_c={u in H_c: integral d(t)|FJu(t)|^2 dt < infinity},
    d(t)=sum_(l>=0) 2t^2/[a_l(a_l^2+t^2)], a_l=2l+1/2.

For every integer N>=1, define

    c_N(t)=cGamma+2 sum_(2<=n<=N) Lambda(n)n^(-1/2)cos(t log n),
    C_N=cGamma+2 sum_(2<=n<=N) Lambda(n)n^(-1/2),
    cGamma=log pi+gamma+pi/2+3 log 2,
    a_N=(d-c_N)_+, b_N=(c_N-d)_+.

Because |a_N-d|<=C_N, the nonnegative a_N form has exactly domain X_c. Write A_N>=0 for its self-adjoint representative. Complete finite-head Plancherel and the full prime-tail norm convergence give

    q[u]=a_N[u]-<u,B_N u>_H-<u,D_(>N)u>_H, u in X_c,
    L_c=A_N-B_N-D_(>N), Dom L_c=Dom A_N,
    ||D_(>N)||<=tau_N<=160(N+1)^2 exp(-pi(N+1)).       (2)

These are full-domain identities. The prime sum includes every prime power through Lambda(n); n is not restricted to primes. The bound in (2) comes from the complete series

    80 sum_(n>N) Lambda(n)n^(3/2) exp(-pi n).

Centering both sides of a paired prime shift cannot increase its norm. There is no assertion that the infinite tail is bounded from all ordinary L2 into H.

For reference, the tail proof uses the isometry u->u/sqrt(W) and

    sup_x sqrt(W(x)W(x+log n))<=40 n^2 exp(-pi n).

Pairing both orientations, summing, using Lambda(n)<=log n<=sqrt(n), and bounding the successive ratio of n^2 exp(-pi n) by 1/2 for n>=2 proves (2). Thus no infinite prime tail is suppressed in the new consequence.

## 2. Exact centered Fourier source and support factor

The true Fourier evaluation vector on the even H space is

    g_t(x)=W(x)cos(tx)/sqrt(2pi).

For u in H_c, <Cg_t,u>_H=FJu(t). This pointwise identity is legitimate: Cauchy-Schwarz and B0<infinity imply H is continuously included in L1, so its ordinary Fourier transform has a continuous integral representative.

The decreasing-summand integral comparison gives

    d(t)>=(1/2)log(1+4t^2).

Consequently, with the finite positive number

    T=T_N=(1/2)sqrt(exp(2C_N)-1)<exp(C_N)/2,

b_N is supported on [-T,T]. The sharp-enough integrated bound is

    integral_0^T b_N(t)dt
      <= integral_0^T [C_N-(1/2)log(1+4t^2)]dt
      =T-(1/2)arctan(2T)<=T.                         (3)

Since ||Cg_t||_H^2<=B0/(2pi), the trace-norm integrable positive representation is exactly

    B_N=2 integral_0^T b_N(t) |Cg_t><Cg_t| dt.        (4)

The factor 2 is the full-line even-frequency factor. The factor (2pi)^(-1) comes from squaring the actual Fourier-vector normalization. Their product below is 1/pi, not 1/(2pi) or 2/pi.

## 3. An independent actual H bank, including its entire centering tail

For R>0 and integer m>=0 let

    v_j=C[W(x)x^(2j)1_(|x|<=R)]/sqrt(2pi), j=0,...,m,
    V=(v_0,...,v_m), r=m+1.

Every raw vector lies in H because its H norm squared is a finite compact-interval moment of W. Applying the bounded projection C puts each v_j in H_c.

The columns are independent. If C[W p 1_(|x|<=R)]=0 for an even polynomial p of degree at most 2m, then W p 1_(|x|<=R) is a scalar multiple of kappa. Outside [-R,R], kappa is strictly positive while the left side is zero, so the scalar is zero. On the interval, W>0 then forces p=0 almost everywhere and hence identically. This argument applies equally to complex coefficients.

Thus the true Gram G=V*V is positive definite and the actual orthogonal projection is

    P=V G^(-1)V*, Q=I-P on H_c, rank P=r.

Its entries are exactly

    G_ij=(w_(i+j)-a_i a_j)/(2pi),
    w_l=integral_(-R)^R W(x)x^(2l)dx,
    a_j=integral_(-R)^R kappa(x)x^(2j)dx.              (5)

No identity Gram, truncated centering, or numerical inverse is used. Formula (5) states matrix positive definiteness, not entrywise positivity. No lower bound on its conditioning is inferred.

The indicator functions do not need to lie in Dom A_N or even in its form domain. P is only a finite-dimensional orthogonal projection in H_c. This is enough for the bounded positive operator B_N and the later codimension argument.

## 4. Source approximation and the trace defect

Put k=2m+2=2r and

    p_(m,t)(x)=sum_(j=0)^m (-1)^j(tx)^(2j)/(2j)!.

Taylor's theorem through order 2m+1 has a zero final odd coefficient and bounded next derivative. For |x|<=R and 0<=t<=T it therefore gives

    |cos(tx)-p_(m,t)(x)|<=E=(TR)^k/k!.

There is no exp(TR) loss. The centered truncated Taylor vector belongs to Ran P. Orthogonal projection minimizes distance, and C is a contraction, so

    ||Q Cg_t||_H^2
      <= ||C[g_t-W p_(m,t)1_(|x|<=R)/sqrt(2pi)]||_H^2
      <= [W_tail(R)+B0 E^2]/(2pi),
    W_tail(R)=integral_(|x|>R) W(x)dx.                (6)

Inside and outside the interval the uncentered error has disjoint support. Thus (6) introduces no unnecessary cross-term factor. More importantly, the contraction is applied to the entire uncentered error: it retains the global kappa component of both centered vectors exactly. No separate kappa tail is dropped or presumed zero outside the interval.

Using the positive trace integral (4), Tonelli, and (3) gives

    epsilon_P:=tr(QB_NQ)
      =2 integral_0^T b_N(t)||Q Cg_t||_H^2dt
      <=(T/pi)[W_tail(R)+B0 E^2].                    (7)

This verifies the exact normalization requested for the stronger claim.

## 5. Explicit radius and integer degree, without numerical input

For R>=0 put Y=exp(2R)>=1. Integrating the weaker full envelope (1) gives

    W_tail(R)<=40 integral_Y^infinity y exp(-3y)dy
              =40(Y/3+1/9)exp(-3Y)
              <=40 exp(-Y).                         (8)

The last inequality follows, for example, from Y/3+1/9<=1+2Y<=exp(2Y). The stronger pi envelope gives the parallel exact primitive 40(Y/pi+1/pi^2)exp(-pi Y), but is not needed.

For any epsilon>0 choose the following actual real parameters and integer rank:

    h=max(1,T/epsilon),
    R=(1/2)log log(80h)>0,
    r=ceil(max{1,3TR,(1/2)log_2(2h)}),
    k=2r, m=r-1.                                    (9)

All logarithms are defined, r>=1 is an integer, k>=2 is even, and m>=0 is an integer. In (8), Y=log(80h), so W_tail(R)<=1/(2h). The factorial bound k!>=(k/e)^k, e<3, and k>=6TR give

    E<=(eTR/k)^k<=2^(-k)<=1/(2h),

where the last inequality uses k>=log_2(2h). Hence

    epsilon_P
      <=(T/pi)[1/(2h)+1/(16h^2)]
      <=9T/(16pi h)<=9epsilon/(16pi)<epsilon.         (10)

This is an explicit analytic bound. An implementation may replace the real cutoffs by certified upper bounds and increase the integer degree accordingly; deciding exact equality at a ceiling boundary is unnecessary.

A uniform general-parameter rank statement is

    r<=3TR+(1/2)log_2(2h)+2,
    r=O(1+T log log(80h)+log h).                      (11)

The use of h=max(1,T/epsilon) in this statement avoids the undefined or negative nested logarithms that an unqualified expression log log(T/epsilon) could have when T/epsilon is small. This is only a notation qualification; it does not alter the small-delta conclusion.

## 6. Elementary arithmetic inputs and the allowed delta range

For the actual negative-count application fix

    0<delta<=1,
    M=max(8,ceil(log_2(2/delta))), N=M-1.              (12)

Then M>=8 and N>=7, so in particular every N>=1 requirement is satisfied. The full tail obeys

    tau_N<=160M^2 exp(-pi M)
          <=exp(-pi M/2)<=2^(-M)<=delta/2.            (13)

For completeness, at M=8 the needed inequality 160M^2<=exp(pi M/2) follows from pi>3, e>5/2, and the exact rational inequality 160*8^2<(5/2)^12. The logarithmic ratio increases for all real M>=8 because pi/2-2/M>0. This proves the middle step uniformly, without numerical root finding.

The finite prime-power bound

    sum_(2<=n<=N) Lambda(n)/sqrt(n)
       <=4(log 2)sqrt(N)+5

is also elementary. Let psi(x)=sum_(n<=x) Lambda(n). Every prime power in (ceil(n/2),n] contributes its prime to the integer binomial coefficient (n choose floor(n/2)); this gives

    psi(n)<=psi(ceil(n/2))+n log 2.

Iterating to 1 and then passing from integers to real x yields

    psi(x)<=2(log 2)x+log x+log 2, x>=1.

Partial summation from 1 to N gives, in fact,

    sum_(2<=n<=N) Lambda(n)/sqrt(n)
       <=4(log 2)sqrt(N)+2-log 2-2/sqrt(N).

The loose +5 bound is therefore safe. There is no PNT or zero-location input. Using cGamma<6 and 8 log 2<6 gives

    C_N<=16+6sqrt(N).                                (14)

The elementary constant cGamma<6 does not require numerical evaluation: gamma<1, pi<22/7, log pi<6/5, and log 2<7/10 give cGamma<411/70<6. The logarithmic inequalities follow from finite positive exponential Taylor sums: exp(6/5)>1+6/5+18/25+36/125>22/7 and exp(7/10)>1+7/10+49/200+343/6000>2.

## 7. Full-operator min-max, with all cross effects retained

Use (12), T=T_N, and (9) with epsilon=delta/4. The resulting rank r is fully explicit, and (10), (13) give

    epsilon_P<delta/4, tau_N<=delta/2.

For u in Ran Q,

    <u,B_Nu>_H=<u,QB_NQ u>_H
       <=||QB_NQ|| ||u||_H^2
       <=epsilon_P ||u||_H^2.                        (15)

This does not replace B_N by its block diagonal. On the chosen subspace the vector has zero P component, so the cross contribution vanishes for that vector exactly. No statement about the norm of B_N-PB_NP is needed.

The usual compact min-max principle equivalently gives lambda_(r+1)(B_N)<=epsilon_P. A direct full-operator argument is even shorter and makes the domain point explicit. Let

    E_delta=Ran 1_(-infinity,-delta](L_c).

The operator L_c is semibounded, so the spectral support of E_delta lies in a bounded interval [ell,-delta] for a finite lower bound ell. Every vector of E_delta belongs to Dom L_c, since its spectral second moment is bounded by max(|ell|,delta)^2 times its norm squared. Consequently every such vector lies in X_c and satisfies q[u]<=-delta||u||_H^2.

If dim E_delta>r, the map P:E_delta->Ran P has a nonzero kernel vector u. This u lies simultaneously in E_delta and Ran Q. Applying the full form identity (2), A_N>=0, and (15), gives

    q[u]>=-(epsilon_P+tau_N)||u||_H^2
          >-(3delta/4)||u||_H^2,

contradicting q[u]<=-delta||u||_H^2. Thus

    dim Ran 1_(-infinity,-delta](L_c)<=r, 0<delta<=1. (16)

This proves the closed-threshold result and hence also the open-threshold result. The strict epsilon_P bound leaves ample slack at every spectral equality. The exact intermediate general comparison with B_N is likewise consistent:

    dim Ran 1_(-infinity,-delta](L_c)
       <=dim Ran 1_[delta-tau_N,infinity)(B_N).

But (16) does not require constructing that spectral projector.

## 8. Delta-independent asymptotic constants and an optional absolute cap

Let L=1+log(1/delta)>=1. Formulas (12)-(14) give N=O(L), C_N=O(sqrt(L)), and T<exp(O(sqrt(L))). With epsilon=delta/4,

    log h=O(L), R=O(1+log L),
    r=O(T[1+log L]+L)=exp(O(sqrt(L))).                (17)

All constants here are independent of delta. They depend only on the fixed numerical constants already displayed for the actual operator; no bank conditioning, inverse norm, or unproved arithmetic constant enters.

One deliberately loose entirely fixed cap is

    r<exp(40 sqrt(L)), L=1+log(1/delta), 0<delta<=1.  (18)

Here is a verification, included so the independence of constants is explicit. Since log 2>1/2, (12) gives M<=8L and N<8L. Hence C_N<34sqrt(L), and T<exp(34sqrt(L)). With h=max(1,4T/delta), log h<36L. Since log 80<5 and log 41<4,

    R<(1/2)log(41L)<2+(1/2)log L<=(5/2)sqrt(L).

For x=sqrt(L)>=1, the elementary inequalities log L<=sqrt(L) and (5/2)x<=exp(2x) give TR<exp(36x). Also (1/2)log_2(2h)<37L. Therefore (11) yields

    r<3exp(36x)+37L+2<=42exp(36x)<exp(40x),

using L=x^2<=exp(36x) and exp(4)>42. This cap is not an efficiency claim or an optimal exponent.

## 9. Compact negative part and all positive Schatten exponents

Set K=(L_c)_-=(-L_c)_+. Semiboundedness makes K bounded. Equation (16) gives a finite-rank spectral projector 1_(delta,infinity)(K) for each 0<delta<=1; thresholds above 1 are covered by monotonicity. The operators K 1_(delta,infinity)(K) are finite rank and approach K in norm with error at most delta. Thus K is compact independently of any prior Schatten assertion.

Let n_-(delta)=dim Ran 1_(-infinity,-delta)(L_c). The open count is the layer-cake count for K. For each p>0, (17), or the explicit (18), implies

    n_-(delta)<=C_p delta^(-p/2), 0<delta<=1,

for some finite delta-independent C_p. Indeed the square-root growth in log(1/delta) is dominated by (p/2)log(1/delta), with the remaining bounded portion absorbed in C_p. Consequently the nonnegative layer-cake identity gives

    tr(K^p)=p integral_0^||K|| delta^(p-1)n_-(delta)d delta
            <infinity,

because near zero its integrand is bounded by a constant times delta^(p/2-1), which is integrable for every p>0. Away from zero, the count is bounded and ||K|| is finite.

It follows that K belongs to every S_p, p>0. For 0<p<1 this means the usual Schatten quasi-class, namely summability of the p-th powers of the singular values. In particular K is trace class. The argument permits infinitely many negative eigenvalues accumulating at zero; it does not force that set to be empty or finite.

## 10. Frozen-source preservation and limitations

The earlier fixed note was not changed. Its three existing copies all retained SHA256

    16a0abbf796b1606aff6cf93dcc1954ea098b5cb90b72424e11efae1ee8c86b0

at the following locations:

- `scalar_first_bracket_20261103/NEGATIVE_SPECTRAL_COUNT_AND_SCHATTEN_AUDIT_20261103.md`
- `theta_negative_trace_paper_20261103/sources/NEGATIVE_SPECTRAL_COUNT_AND_SCHATTEN_AUDIT_20261103.md`
- `theta_negative_trace_publication_stage_20261103/sources/NEGATIVE_SPECTRAL_COUNT_AND_SCHATTEN_AUDIT_20261103.md`

Additional local sources checked were `scalar_first_bracket_20261103/SCALAR_BRACKET_PROOF_AND_CODE_CONSTANTS.md`, `scalar_first_bracket_20261103/FINITE_BANK_EIGENVALUE_AND_KY_FAN_ADDENDUM_20261103.md`, and Section 1 of `residual_gram_sign_attack_20261103/LOW_COLLAR_EXPLICIT_TAIL_COMPRESSION_AND_FINITE_RADICAL_CERTIFICATES.md`.

The stronger conclusion is an added analytic consequence, not a numerical re-certification or a silent revision of the fixed S_p, p>1 note. No RH, positivity, fixed-gap estimate, radical completeness, identification of the entire kernel, inverse sign, or runtime premise is used. The source projection P is not a radical projection or a low-collar spectral projection. No effective inverse-trial count, Gram conditioning, arithmetic-precision bound, or actual positive sign margin follows from this audit.
