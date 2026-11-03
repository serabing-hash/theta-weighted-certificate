# Explicit low-collar prime-tail compression and finite radical certificates

3 November 2026 UTC. This is a constructive norm theorem for the actual complete theta/Gamma/prime operator. It is not a sign proof at zero, an identification of the full physical kernel, or a practical dimension claim. No historical novelty claim is made.

## Result and scope

For every fixed bounded spectral window J of the complete centered operator L_c, the actual prime tail has an explicitly controlled finite-rank approximation on Ran 1_J(L_c). The approximation retains all finite prime orientations and bounds the entire omitted infinite prime tail. Its columns can be formed without a sharp spectral projection.

After a continuous spectral filter is applied, finitely many exact known-radical constraints give finite, safe, decreasing upper bounds on both signs of the compressed tail on K=N^perp. They use the actual H Gram, not an identity coefficient Gram. Their convergence is proved, but no effective convergence rate in the number of radical constraints is asserted.

At a relative error target epsilon=c delta (fixed c>0), the explicit generic rank bound grows like exp(O(delta^(-2)[1+log(1/delta)])). Full-kernel removal gives only an o(1) collar modulus from compactness. Neither O(delta) nor o(delta) follows. Removing the known radical N alone need not even make that modulus tend to zero if an additional physical kernel remains.

## 1 Actual setting and independent arithmetic inputs

Work on the centered even Hilbert space

    H=L2_even(dx/W), H_c=ker m,
    C u=u-2m(u)kappa, ||kappa||_H=1,
    N=closure_H span{r_j:j>=1}, r_j=kappa^(2j)-4^(-j)kappa,
    K=N^perp intersect H_c, P_K=I-P_N on H_c.

The complete self-adjoint operator L_c has form

    q[u]=t_Gamma[u]-<D_full u,u>_H,
    t_Gamma[u]=integral d_Gamma(t)|u_hat(t)|^2dt>=0,
    ||D_full||<=d, L_c>=-d I.                         (1)

The Fourier transform here is unitary on ordinary L2(dx). The actual symbol is even, continuous, tends to infinity, and has d_Gamma(t)=log|t|+O(1) at infinity. Define

    nu(T)=inf_(|t|>T) d_Gamma(t) ->infinity.

Using nu avoids requiring a new monotonicity assertion. The actual known radicals satisfy N subset Dom L_c and L_c P_N=0. Write P_0=1_{0}(L_c) for the entire physical-kernel projection. Only P_N<=P_0 is known here.

Fix an integer M>=1. Let D_M=C D_(>M),raw C|H_c be the centered actual prime tail. All later prime cutoffs N are integers with N>=M. Every finite prime-power pair has the raw numerator action

    (Lambda(n)/sqrt n) W(x)[u(x+log n)+u(x-log n)].

The entire theta series gives, with W_*=||W||_infinity,

    W(x)<=40 exp(4|x|-pi exp(2|x|)),
    ||D_M||<=tau_M=80 sum_(n>M) Lambda(n)n^(3/2)e^(-pi n),
    tau_M<=160(M+1)^2e^(-pi(M+1)).                    (2)

For completeness the theta-series estimate uses the successive ratio bound
n^4 exp[-pi(n^2-1)] <= (16 exp(-3pi))^(n-1), whose geometric sum is less than 500/499; multiplying by 4pi^2 is less than 40. For the shift s=log n,

    sup_x sqrt(W(x)W(x+s))<=40 n^2e^(-pi n).

Indeed, writing a=|x|, b=|x+s|, and v=a+b>=s, one has exp(2a)+exp(2b)>=2exp(v). The geometric mean of the two envelope bounds is at most 40 exp(2v-pi exp(v)); this is decreasing for v>=0, so its maximum under v>=s is 40n^2 exp(-pi n). Each paired weighted shift therefore has norm at most 80 Lambda(n)n^(3/2)e^(-pi n). Summing proves the complete prime-power tail bound. The last cap in (2) follows from log n<=sqrt n and a geometric series. No prime list is required.

A single weighted shift is bounded ordinary L2 -> ambient weighted L2, since

    ||W(.)u(.+s)||_H^2<=W_*||u||_2^2.

Pair the two orientations before asserting an even output, and apply C only after reaching H. For the finite sum M<n<=N this gives

    ||D_(M,N)||_(ordinary L2 -> H_c)<=C_(M,N),
    C_(M,N)=2sqrt(W_*) sum_(M<n<=N) Lambda(n)/sqrt n. (3)

The elementary full-prime bound

    C_(M,N)<=2sqrt(W_*)[4(log2)sqrt N+5]             (4)

is available without PNT; W_* may be replaced everywhere by the explicit cap 40e^(-pi). It follows by iterating the binomial bound
psi(n)<=psi(ceil(n/2))+n log2, then partially summing
psi(x)<=2(log2)x+log x+log2. The sum in (3) is finite. No bounded map from ALL ordinary L2 through the infinite prime tail is claimed.

## 2 Uniform finite-dimensional approximation of low-energy inputs

Fix a bounded Borel set J subset [-R,R], 0<=R<infinity, and P_J=1_J(L_c). Every u in Ran P_J belongs to Dom L_c, and (1) implies

    t_Gamma[u]<= (R+d)||u||_H^2,
    ||u||_2<=sqrt(W_*)||u||_H.                       (5)

For B,T>0 with nu(T)>0, let F_T be the ordinary Fourier cutoff |t|<=T and let

    W_B=sup_(|x|>B)W(x).

Spatial and Fourier tails, separately, give

    ||u-1_(|x|<=B)F_Tu||_2
      <=[sqrt(W_B)+sqrt((R+d)/nu(T))]||u||_H.        (6)

For an integer m>=1 approximate exp(itx) by its first m Taylor terms. Because tx is real, the integral remainder has modulus at most |tx|^m/m!, with NO exp(BT) loss. Its Fourier-to-box kernel has Hilbert-Schmidt error at most

    zeta_(B,T,m)=sqrt(2BT/pi)(BT)^m/m!.              (7)

On even inputs only the even powers are needed. Define the finite-rank map

    T_(B,T,m)u=1_(|x|<=B) sum_(0<=k<m, k even) x^k ell_k(u),
    ell_k(u)=(sqrt(2pi) k!)^(-1)
               integral_(-T)^T (it)^k u_hat(t)dt.

Its rank is at most ceil(m/2). From (6)-(7),

    ||u-T_(B,T,m)u||_2<=b_(J;B,T,m)||u||_H,
    b=sqrt(W_B)+sqrt((R+d)/nu(T))+sqrt(W_*)zeta.      (8)

Also ||T_(B,T,m)||_(ordinary EVEN L2 -> ordinary EVEN L2)<=1+zeta. This follows by comparing it with 1_(|x|<=B)F_T on the even sector in Hilbert-Schmidt norm. On ambient ordinary L2, compare the even-only map instead with 1_(|x|<=B)F_T P_even; no closeness to the full non-even map is asserted.

## 3 Actual finite-prime approximation of the whole tail row

Choose N>=M and set

    A=C D_(M<n<=N),raw T_(B,T,m)|H_c.

Every output column is an actual finite-prime shift of the compact ordinary source 1_(|x|<=B)x^k, followed by C. Hence A has rank at most ceil(m/2) and

    ||A||<=C_(M,N)sqrt(W_*)(1+zeta).                 (9)

Combining (2), (3), and (8) proves the full ROW estimate

    ||(D_M-A)P_J||<=E,
    E=tau_N+C_(M,N)b_(J;B,T,m).                    (10)

Thus D_M P_J is compact. This directly proves the bounded-window compactness with an explicit norm approximation, not merely a compactness criterion.

For S=(A+A*)/2, (10) implies only the compressed self-adjoint estimate

    ||P_J(D_M-S)P_J||<=E.                           (11)

We do NOT assert ||(D_M-S)P_J||<=E; the adjoint row is not controlled that way. In particular every low-window source obeys

    |p_(>M)[u]-Re sum_k overline(ell_k(u))<y_k,u>_H|
          <=E||u||_H^2, y_k=C D_(M<n<=N),raw(1_B x^k). (12)

Inner products are conjugate linear in the first argument. The middle quadratic quantity in (12) is exactly <u,S u>_H; with real sources every displayed scalar is real.

## 4 A fully explicit, very expensive rank schedule

Let 0<epsilon<=1. Set

    N=max(M, ceil(3+log(4/epsilon))).

The elementary tail schedule in (2) gives tau_N<epsilon/4. If M=N, the finite sum is empty and A=0 already suffices. Otherwise use any positive cap C>=C_(M,N) from (4). Put

    X=max(exp(2), 4C sqrt(40)/epsilon),
    Y=(4/pi)log X, B=(log Y)/2.

For x>=B>=0 the envelope in (2) is decreasing. Since Y<=X for X>=exp(2),

    C sqrt(W_B)<=C sqrt(40)Y exp(-pi Y/2)
                      <=C sqrt(40)/X<=epsilon/4.

Choose T with nu(T)>0, including in the degenerate case R+d=0, and

    nu(T)>=16 C^2(R+d)/epsilon^2,

and choose an integer m satisfying both

    m>=4 exp(1) BT,
    m>=max(0, log_4[4C sqrt(W_*)sqrt(2BT/pi)/epsilon]).

The inequality m!>=(m/exp(1))^m gives zeta<=sqrt(2BT/pi)4^(-m), so each remaining term in E is at most epsilon/4. Thus E<=epsilon.

For this cost bound choose C at the size of the explicit cap (4), and choose an admissible T no larger than the logarithmic-symbol asymptotic requires; an arbitrarily inflated cap or cutoff would not retain the stated bound. For fixed M and bounded R, (4) then gives C^2=O(1+log(1/epsilon)); the actual logarithmic Gamma asymptotic gives log T=O_(R,d,W)(epsilon^(-2)[1+log(1/epsilon)]). Consequently one valid rank bound is

    rank A <= exp(O_(R,d,W,M)(epsilon^(-2)[1+log(1/epsilon)])). (13)

This is an existence/explicit-parameter bound, not a claim that the rank is manageable or optimal. At epsilon=c delta this particular schedule has the severe cost shown. No lower bound on the optimal rank is claimed. Nothing here signs the true low block.

An equivalent approximation-number consequence is useful. For sufficiently large integer m, take N=max(M,ceil(log log m)), B=(log log m)/2, and T=m/[4 exp(1)B]. Then the Taylor remainder is exponentially small, sqrt(W_B)<=sqrt(40)(log m)m^(-pi/2), nu(T) is comparable with log m, and C_(M,N)=O_W(sqrt(log log m)). Equations (8)-(10) give

    a_m(D_M P_J) <= C_(R,d,W,M) sqrt(log log m/log m), (13a)

where a_m is the error of the best rank-less-than-m approximation; harmless changes of m account for the even rank convention. Thus the number of singular values above epsilon is bounded by exp(O(epsilon^(-2)[1+log(1/epsilon)])). This is an actual quantitative compactness result, independent of the sign of L_c. It is an upper bound, not an optimality claim.

## 5 Continuous filtering avoids a sharp spectral-projector oracle

Take a real Lipschitz function phi, 0<=phi<=1, equal to one on the target interval I and supported in a fixed bounded J subset [-R,R]. Write F=phi(L_c). It is bounded self-adjoint, has range in Ran P_J, and commutes with P_N and P_0. Define

    S_phi=(F A F+F A* F)/2.

The full row estimate (10) now yields the GLOBAL estimate

    ||F D_M F-S_phi||<=E.                            (14)

The rank of S_phi is at most twice rank A. It is important that F D_M F retains the COMPLETE L_c spectral filter; no Gamma-only energy window has been substituted.

There is an explicit route to approximating its finitely many filtered columns without a sharp projection. Choose s>d, R_s=(L_c+s)^(-1), and r_max=1/(s-d). On [0,r_max] define

    h(0)=0, h(r)=phi(1/r-s) for r>0.

It is continuous. If phi is supported in [-R,R], h is Lipschitz with constant at most Lip(phi)(s+R)^2. After rescaling to [0,1], its Lipschitz constant is at most

    L_h=Lip(phi)(s+R)^2/(s-d).

The degree-q Bernstein polynomial p_q in R_s satisfies

    ||p_q(R_s)-F||<=L_h/(2sqrt q).                   (15)

The polynomial has zero constant term because h(0)=0. Thus a certified safe-positive-resolvent primitive suffices for all these finite column actions. The polynomial approximation is not by itself an algorithm or a certificate for those resolvent actions or their Gram entries; those finite numerical obligations must still be certified separately. No inverse near zero is invoked. Such actions can be certified by residuals: for v in Dom L_c, if (L_c+s)v approximately equals f, then

    ||v-R_s f||_H<=||(L_c+s)v-f||_H/(s-d).           (16)

Equation (16) states the required certificate, not a claim that numerical columns were computed in this note. It keeps the actual Gamma and all prime terms; evaluating the latter can use (2).

If a bounded approximation F_tilde has ||F_tilde-F||<=eta, sym(F_tilde A F_tilde) incurs at most the additional error

    eta ||A||(2+eta).                              (17)

This gives a fully stated budget for replacing exact functional-calculus columns by certified approximations. For phi_delta equal to one on [-delta,delta] and zero outside [-2delta,2delta], Lip(phi_delta)=1/delta; even before column accuracy is paid, the generic polynomial degree in (15) is O_s(delta^(-2)eta^(-2)).

## 6 Finite known-radical constraints give safe finite-matrix bounds

Let P_j be the true H projection onto the span of the first j represented independent known radicals, and put Q_j=I-P_j on H_c. For EVERY u in K with F u=u,

    -[max(0,-lambda_min(Q_j S_phi Q_j))+E]||u||_H^2
          <=p_(>M)[u]
          <=[max(0,lambda_max(Q_j S_phi Q_j))+E]||u||_H^2. (18)

This is safe at each FINITE j: u is exactly orthogonal to those finitely many radicals. No completeness of that finite bank is presumed. Because S_phi is finite rank and P_j converges strongly to P_N,

    Q_j S_phi Q_j -> P_K S_phi P_K in operator norm. (19)

The nonnegative upper bounds on either sign in (18) decrease with j. Indeed they are respectively the maximum positive and negative Rayleigh extrema over the nested spaces Ran Q_j, including zero. Their limits are the corresponding extrema of P_K S_phi P_K. There is no quantitative j-rate in (19).

All finite spectra in (18) use the actual Gram. To see this explicitly, represent A=Y G* with rows ell_k(u)=<g_k,u>_H. One may take

    g_k=C(W b_k),
    b_k=Fourier^(-1)[(-it)^k 1_(|t|<=T)/(sqrt(2pi)k!)],
    y_k=C D_(M<n<=N),raw(1_(|x|<=B)x^k).

These g_k and y_k lie in H_c; only even k are retained. For the actual filtered columns put Z=(F Y,F G). Then

    S_phi=Z H_0 Z*,
    H_0=(1/2)[[0,I],[I,0]].

With R_j=(r_1,...,r_j), the true radical Gram H_j=R_j*R_j>0, and B_j=R_j*Z,

    G_Z^(j)=Z*Q_j Z=Z*Z-B_j*H_j^(-1)B_j>=0.        (20)

The nonzero spectrum of Q_j S_phi Q_j is the nonzero spectrum of

    (G_Z^(j))^(1/2) H_0 (G_Z^(j))^(1/2).            (21)

A singular G_Z^(j) is allowed; use its positive-semidefinite square root on the represented support, not a fictitious inverse. Matrix-entry and column errors must be paid in E via a certified operator-norm error, for example (17), before a numerical sign claim is made. The monomial realization can be severely ill conditioned; neither the exact Gram identity nor the rank bound supplies a floating-point stability certificate.

Equations (10), (14), and (18)-(21) are independent arithmetic/functional-analytic estimates, valid without a sign hypothesis for L_c|K. They give a usable finite certificate format but do not assert that its upper bounds are small enough for the endpoint task.

### A finite approximate-preimage certificate

There is a sharper alternative when particular filtered columns have independently verified range responses. Suppose the actual finite column matrix Z above has a verified decomposition

    Z=L_c H+R_j B+E_0,

where every column of H is in Dom L_c, R_j consists of known radicals, and e=||E_0||, h=||H|| are certified H-operator norms from coefficient space. This is an actual full-Gamma/full-prime residual statement. If phi=1 throughout [-delta,delta], then for u in K intersect Ran 1_([-delta,delta])(L_c),

    ||Z* u|| <= (delta h+e)||u||_H.

Since ||H_0||=1/2, (14) yields

    |p_(>M)[u]| <= [E+(1/2)(delta h+e)^2]||u||_H^2. (21a)

This is a genuinely checkable sufficient finite certificate, not an assumption of a uniform inverse on K. It is useful only if concrete independently checked h,e fit the desired budget. For example E<=c_1 delta, e<=c_2 sqrt(delta), h<=c_3/sqrt(delta) give a relative cap c_1+(c_2+c_3)^2/2. We have NOT proved these bounds for the actual column bank. Existence with arbitrary residual e after only known-radical subtraction would require the columns to be orthogonal to any remaining physical kernel. Even after whole-kernel removal, the inverse-response norms h can diverge with e, and no rate follows from compactness. The earlier actual critical-row inverse-growth theorem rules out importing a generic polynomial-height unshifted inverse bound without further arithmetic.

## 7 Infinite kernel and the zero-threshold loss

The compactness in (10) is compatible with infinite-dimensional Ran P_J: if 0 is in J, it contains the infinite known radical N. In fact the independently proved actual finite-prime-head theorem gives infinitely many positive and negative eigenvalues of

    P_N D_M P_N|N,

both sequences tending to zero. Thus compactness does not make a fixed finite-rank approximation an exact endpoint sign certificate, even on the known radical. Its absolute remainder must be paid.

There is a precise full-kernel distinction. Fix J containing a neighborhood of zero and let

    E_delta=1_([-delta,delta] \ {0})(L_c).

Then E_delta converges strongly to zero as delta decreases to zero. Since D_M P_J is compact,

    ||D_M E_delta|| ->0.                            (22)

Hence the full-kernel-free collar compression also tends to zero in norm. Compactness supplies NO rate in (22). In particular it does not prove

    ||E_delta D_M E_delta||=O(delta),

let alone a contraction constant below one for the true low Schur response.

If only the KNOWN radical is removed, phi_delta(L_c)P_K instead converges strongly to P_0-P_N. Using bounded-window compactness gives the stronger exact norm limit

    ||P_K phi_delta(L_c)D_M phi_delta(L_c)P_K
           -(P_0-P_N)D_M(P_0-P_N)|| ->0.             (23)

The residual physical-kernel block in (23) need not vanish from the facts proved here. Calling N the entire kernel would silently delete this obstruction.

Even when P_N=P_0 happens to hold, (22) is only an absolute modulus. To exclude a putative eigenvalue -delta by a delta-relative tail estimate, both the approximation error and the certified finite-matrix contribution must fit an O(delta) budget. Formula (13) controls the first at a severe explicit cost. Neither (18) nor compactness bounds the second by O(delta). Proving that additional arithmetic estimate, or finding an actual low-collar violation, remains open.

## 8 A quantitative bound on the actual negative spectral count

The same explicit construction applies to the ENTIRE bounded correction D_full, not just a tail. On H_c it is the centered compression of

    c_Gamma W u + sum_(n>=2) (Lambda(n)/sqrt n)W(x)
                                      [u(x+log n)+u(x-log n)].

Form A_full=C(raw finite correction)T_(B,T,m)|H_c. The required finite ordinary-L2-to-H cap is for the RAW finite correction followed by C, not for C(raw correction)C on all ordinary L2. It is

    C_N^full=sqrt(W_*)[|c_Gamma|+2sum_(2<=n<=N)Lambda(n)/sqrt n]
             <=sqrt(W_*)[|c_Gamma|+8(log2)sqrt N+10],

and the same omitted prime-tail norm tau_N. Equations (5)-(13a) continue to hold with this cap and D_full in place of D_M. No positivity of D_full is used.

For 0<delta<=min(1,d), let

    P_-delta=1_([-d,-delta])(L_c).

Choose a finite-rank A_full with

    ||(D_full-A_full)P_-delta||<=epsilon<delta.

If dim Ran P_-delta exceeded rank A_full, a nonzero u in Ran P_-delta intersect ker A_full would exist. But then

    q[u]<=-delta||u||_H^2,
    q[u]=t_Gamma[u]-<u,D_full u>_H>=-epsilon||u||_H^2,

which is impossible. Therefore

    dim Ran P_-delta<=rank A_full
       <=exp(O_(d,W,c_Gamma)(delta^(-2)[1+log(1/delta)])), (24)

One may take epsilon=delta/2 in the explicit schedule. The case delta>d is empty. This is an ACTUAL unconditional negative spectral-count upper bound, including multiplicities; it is not an assertion that the count is nonzero or zero. In particular no negative essential spectrum is possible, and negative eigenvalues can accumulate only at zero.

Every negative spectral vector is automatically orthogonal to the entire physical kernel, hence to N. Thus the infinite known radical does not invalidate the dimension argument. Unlike an argument based merely on a small positive Rayleigh subspace of an indefinite matrix, the proof uses the WHOLE actual spectral subspace with q<=-delta I and a rank-nullspace intersection.

The count bound is very weak and does not exclude the collar 0<delta<2^(-26). Its useful content is an a priori dimension bound for the negative spectral subspace at any fixed depth, without an assumed sign or an effective full-kernel projection. It does not itself supply coordinates for that spectral subspace or a complete finite numerical exclusion algorithm.

## 9 What is established and what remains

Established without RH or a sign premise:

- an explicit finite-rank approximation of the COMPLETE prime tail on any actual bounded L_c window;
- a fully retained infinite-tail and Gamma-energy error budget;
- safe finite known-radical upper certificates for both tail signs, with true Gram formulas and qualitative convergence;
- continuous-resolvent filtering with an explicit approximation cost, avoiding a sharp spectral-projection oracle;
- the distinction between compactness, full-kernel removal, and delta-relative control;
- an explicit upper bound on the complete actual negative spectral count below any fixed -delta.

Not established:

- a useful numerical size for the finite tail matrices near zero;
- an effective radical-bank convergence rate;
- N=ker L_c;
- O(delta) or o(delta) low-collar tail control;
- positivity of the true low/history Schur block or a full-history theta_j pivot bound.

## Independent audit

An independent audit checked the four-term epsilon schedule, the complete theta/prime caps, the finite-rank Taylor construction, the Bernstein filter bound, monotonic finite-radical certificates, both norm limits, the true Gram spectrum, and the approximation-number estimate. Two clarifications were incorporated: the even-only Taylor operator is compared on ordinary even L2, and (21a) requires phi=1 on the collar. The same audit then checked the complete-correction cap and the negative spectral-count argument in Section 8. The audit does not certify any numerical column bank or delta-relative arithmetic size.
