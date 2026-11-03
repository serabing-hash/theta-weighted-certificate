# The actual prime tail has two essential signs on the positive range

3 November 2026 UTC. An actual theta/Gamma/prime counterexample to one-sided tail positivity after known-radical or full-kernel removal. This is not a negative direction for the complete q_0 form and does not disprove a relative tail bound at the zero threshold. The constructed sources lie in strictly POSITIVE spectral bands of the complete actual operator.

## Result

Fix ANY finite prime cutoff M. Let D_raw=D_{>M} be the complete actual prime-tail operator on H=L2_even(dx/W), and D=C D_raw C|H_c its centered compression. Let

    L_c = actual complete centered operator,
    P_+ = 1_(0,infinity)(L_c),
    P_* = I-1_{0}(L_c),
    N = known derivative-radical closure,
    K=N^perp intersect H_c.

No identification N=ker L_c is made. Choose any prime power n_0>M; one may explicitly use a power of two, so no prime search is needed. Put

    a_0=Lambda(n_0)/sqrt(n_0)>0,
    x_0=(log n_0)/2,
    w_0=W(x_0)>0,
    A_0=a_0 w_0,
    c_M=A_0/8>0.

For EVERY finite r there are r-dimensional represented ACTUAL source spaces F_r^+ and F_r^- contained in Dom L_c intersect Ran P_+, such that

    p_{>M}[v]>= c_M||v||_H^2,  v in F_r^+,
    p_{>M}[v]<=-c_M||v||_H^2,  v in F_r^- .             (1)

All nonzero vectors in either space have strictly positive COMPLETE q_0 energy, since the spaces are contained in positive spectral bands. In particular these tail signs survive exact removal of N and of the ENTIRE physical kernel, and the actual inverse-free range is retained: the selected bands stay a positive distance from zero, so every constructed vector belongs to Ran L_c.

Consequently the bounded self-adjoint compression P_+ D P_+ has infinite positive and negative spectral dimensions bounded away from zero. Its essential spectrum has both a positive and a negative part. The same holds on the larger full-kernel complement and on K. No compact correction, including the compact known-radical null repair, can make this tail one-sided or compact there.

This does NOT claim the complete head or full form is negative on these sources. In fact their COMPLETE q_0 energies grow with the carrier, while the tail amplitudes stay fixed. Their tail/q_0 relative ratios tend to zero.

## 1 A complete, actual two-packet source retaining exactly one prime correlation

Fix a real even eta in C_c^infinity((-1,1)) with ||eta||_2=1, and define

    eta_e(y)=e^(-1/2) eta(y/e),
    E_e(x)=eta_e(x-x_0)+eta_e(x+x_0),
    u_t(x)=sqrt(W(x))E_e(x)cos(tx).

Here e>0 denotes packet width, not Euler's number. It is fixed BEFORE the carrier tends to infinity. Each u_t is a real even compact-smooth actual admitted source.

Choose e so the two supports are disjoint, 2e<log 2, and no log n with integer n>=2 other than n_0 lies in (log n_0-2e,log n_0+2e). This is possible by the positive distance to the neighboring integer logarithms. It kills EVERY other prime-power correlation exactly, not by a tail estimate. The same-packet correlations have shifts smaller than log 2; the only positive cross-packet shift is within 2e of log n_0.

Put

    g_e(y)=eta_e(y)^2 sqrt(W(x_0+y)W(x_0-y)),
    A_e=a_0 integral g_e(y)dy.

Then g_e is real, even, smooth, compactly supported and nonnegative. As e->0, A_e->A_0. Direct cosine multiplication gives the EXACT full-tail formula

    p_{>M}[u_t]
       =a_0[cos(t log n_0) integral g_e
                         +integral g_e(y)cos(2ty)dy].       (2)

Thus choosing t log n_0 congruent to 0 or pi modulo 2pi gives respectively limits +A_e and -A_e as t->infinity. No other tail term has been dropped: all of them vanish on the unprojected source by support geometry.

Its H norm satisfies

    ||u_t||_H^2=integral E_e(x)^2cos(tx)^2dx ->1.         (3)

Also ||Cu_t-u_t||_H->0 by ordinary oscillatory integration of the compact smooth mean integrand. C is used only as a bounded H projection, never on arbitrary ordinary-L2 functions.

## 2 The full Gamma/prime operator makes these high-energy quasimodes

The COMPLETE Gamma symbol has

    d_Gamma(t)=log t+O(1),
    |d_Gamma'(t)|<=C/t,  t>=1.

Its fixed-envelope modulation estimate, retaining all Gamma shifts, is

    ||(D_Gamma-d_Gamma(t))(A cos(tx))||_2
        <=C[log(2+t)/t]||A'||_2,  t>=2.                 (4)

One proof splits Fourier shifts at |xi|=t/2, uses the derivative bound inside and the global logarithmic symbol bound outside, obtaining
|d_Gamma(t+xi)-d_Gamma(t)|<=C[log(2+t)/t]|xi|. Plancherel proves (4), separately on the two reflected carrier orientations.

Let

    omega_e=sup_support |W(x)/w_0-1| ->0,
    lambda_t=w_0 d_Gamma(t) ->infinity.

For the fixed A=sqrt(W)E_e, formula (4) and T_Gamma u=W D_Gamma u imply

    ||(T_Gamma-lambda_t)u_t||_H
       <=lambda_t omega_e||u_t||_H+O_e(log t/t).

The COMPLETE correction D_full in the actual L=T_Gamma-D_full is bounded H->H. Its norm divided by lambda_t tends to zero. The mean projection C commutes with this complete L because kappa is its exact mean eigenvector. Therefore

    ||(L_c-lambda_t)Cu_t||_H/lambda_t
       <=omega_e||u_t||_H+o_e(1).                      (5)

Every prime power, both shift orientations, and the full Gamma operator remain in (5). The bounded full correction is paid before taking the large-carrier limit.

Let

    Pi_t=1_[lambda_t/2,3lambda_t/2](L_c),
    v_t=Pi_t Cu_t.

Spectral calculus and (5) give

    ||v_t-u_t||_H
       <=||Cu_t-u_t||_H
          +(2/lambda_t)||(L_c-lambda_t)Cu_t||_H
       <=2omega_e||u_t||_H+o_e(1).                     (6)

In particular, after fixing e and taking t sufficiently large,

    ||v_t-u_t||_H<=5omega_e.                           (7)

Each v_t is an admitted vector in a bounded positive spectral interval. It is orthogonal to the entire kernel, lies in K, and is in the ACTUAL range of L_c. Its complete energy is between lambda_t/2 and 3lambda_t/2 times its squared H norm.

## 3 Mixed tail correlations and actual Grams

Fix the sign sigma=+1 or -1 and a desired finite rank r. Use phase-aligned carriers

    t_j log n_0 congruent to 0  (sigma=+1),
    t_j log n_0 congruent to pi (sigma=-1).

For two unprojected packets, direct integration gives the COMPLETE tail matrix entry

    p_{>M}(u_(t_i),u_(t_j))
       =a_0 cos((t_i+t_j)x_0) integral g_e(y)cos((t_i-t_j)y)dy
        +a_0 cos((t_i-t_j)x_0) integral g_e(y)cos((t_i+t_j)y)dy.  (8)

The off-diagonal entries tend to zero when the fixed finite carriers are chosen successively with sufficiently large differences. The diagonal tends to sigma A_e by (2). Formula (8) keeps both orientations and handles all mixed cross terms; a diagonal test alone is not used.

Likewise the true H Gram entries are integrals of E_e^2 cos(t_i x)cos(t_j x). They have diagonal limit one and off-diagonal limit zero. No coefficient identity Gram is substituted: the following verified-nearness conditions are imposed using these actual integrals.

Write Uc=sum c_j u_(t_j). The finitely many phase-aligned carriers can be chosen so that

    ||U^*U-I||<=1/8,
    ||U^*D_raw U-sigma A_e I||<=A_e/8.                 (9)

They can simultaneously be made large enough for (7), for the small means in (6), and so that their positive spectral intervals are pairwise disjoint if desired. The phase constraints leave an unbounded arithmetic progression of carrier values, so all these finite conditions can be satisfied inductively. No simultaneous prime-phase approximation is required: there is exactly one retained prime-power shift.

## 4 Quantitative order of choices and the projected matrix sign

Let tau be ANY proved H->H norm cap for the ENTIRE D_raw tail, such as

    tau=80 sum_(n>M) Lambda(n)n^(3/2)exp(-pi n).

The order is important:

1. Fix M, n_0, r, eta and the positive A_0. These do not vary with the carrier.
2. Fix e small enough for the exact support separation of Section 1 and

       omega_e<=min(1/2,1/(40sqrt r), A_0/(400tau sqrt r)).    (10)

   Then A_e>=A_0/2. The width remains fixed for all subsequent carrier limits. Although it may be very small, no uniform varying-envelope estimate is assumed.
3. Choose the r carriers sufficiently large and separated to meet (7) and (9).
4. Only then form the actual complete-operator spectral projections v_j=Pi_(t_j)Cu_(t_j).

Write Vc=sum c_j v_j and E=V-U. By (7),

    ||E||<=5sqrt r omega_e<=1/8.

Since (9) gives ||U||<2,

    ||V^*D_raw V-U^*D_raw U||
       <=tau[2||U||||E||+||E||^2]
       <=25tau sqrt r omega_e
       <=A_0/16<=A_e/8.                               (11)

The same true-Gram bounds give

    (1/2)I<=V^*V<=2I.

Combining (9)--(11),

    sigma V^*D_raw V>=(3A_e/4)I.

Thus for v=Vc,

    sigma p_{>M}[v]
       >=(3A_e/8)||v||_H^2
       >=(3A_0/16)||v||_H^2
       >=c_M||v||_H^2.

This proves (1) on all complex coefficient combinations and both signs. It also proves actual represented independence and pays every cross term after the projection.

## 5 Infinite signed dimensions, noncompactness, and compact repairs

For every r the SAME positive c_M works in (1), even though the width and carriers may depend on r. Min-max for the bounded tail compression therefore gives infinite positive and negative spectral dimensions uniformly away from zero. Equivalently its essential spectrum cannot be contained in [0,infinity), (-infinity,0], or {0}.

There is also a direct noncompactness witness. Fix a width meeting the r=1 conditions and let phase-aligned carriers tend to infinity. The normalized v_t have spectral support above lambda_t/2->infinity, hence converge weakly to zero in H. Their complete tail quadratic forms stay respectively bounded positively or negatively away from zero. A compact compression would send both to zero, a contradiction.

Since Ran P_+ is contained in (ker L_c)^perp and K, all these conclusions persist after the exact removal of either kernel space. Finite-rank corrections cannot remove the two infinite signed indices. More generally compact corrections cannot remove the two essential signs.

The known-radical compact null repair is compatible with this obstruction: it removes only blocks touching N. Its quadratic form on K is exactly zero, so it does not change these tail signs on K at all.

### A concrete essential-norm lower bound after every compact repair

The positive first theta term gives, for n>=2,

    W((log n)/2)>=pi^2 n^2 exp(-pi n).

Indeed the ratio exp(x/2)/(2cosh(x/2)) is at least 1/2 for x>=0, and 4pi^2 n^2-6pi n>=2pi^2 n^2. The complete theta series has positive summands, so keeping that first term is a valid lower bound.

Thus, for the explicit choice n_0=2^k>M, the tail compression on K, on the entire kernel complement, and already on the positive range has essential norm at least

    c_M>= (pi^2 log2/8) n_0^(3/2)exp(-pi n_0).          (12)

Every compact correction leaves that essential-norm lower bound. Along M=2^k-1 this has the same exponential exp(-pi(M+1)) scale as the complete upper tail bound. Exact null removal does not produce an additional exponential improvement of the entire tail operator norm.

This is an absolute essential-norm statement. It is not a relative lower bound at the spectral threshold.

## 6 The precise unresolved threshold question

This counterexample rules out one-sided tail positivity, finite-rank tail-sign repair, or compactness of the complete tail on the kernel-free range. It does not rule out a signed RELATIVE bound against the actual q energy or a positive reference.

Indeed, on the constructed bands q_0[v] is of size lambda_t||v||_H^2 with lambda_t->infinity, whereas |p_{>M}[v]|<=tau||v||_H^2. Their relative tail cost tends to zero. The theorem deliberately gives no low-energy or collar sign claim.

Near the zero threshold the still-needed estimate must compare the tail and the full retained signed response at delta scale, not declare the tail positive after compact null repair. The compactness D_tail(L_c+s)^(-1), for a safe shift with -s in the actual resolvent set, remains valid and does not contradict this noncompactness on the full high-energy range.

## 7 A stronger fixed-envelope positive-range projection estimate

There is an independent full-Gamma parametrix that removes the width-loss term omega_e from the positive-range projection. The preceding proof and its audited constants do not depend on this strengthening.

Fix ANY smooth compact even E, not necessarily narrow, and put

    u_t=sqrt(W) E cos(tx),
    h_t=u_t/[W d_Gamma(t)]
       =[E/sqrt(W)]cos(tx)/d_Gamma(t).

Both are actual compact smooth admitted sources. Since W is strictly positive on their fixed compact support, the constant

    B_E=||E/W||_2

is finite and

    ||h_t||_H<=B_E/d_Gamma(t).

Apply the COMPLETE modulation estimate (4) to the FIXED envelope E/sqrt(W). Since d_Gamma(t) is asymptotic to log t,

    ||T_Gamma h_t-u_t||_H<=C_E/t

for all sufficiently large t. Let d=||D_full|| for the complete bounded correction. Then

    ||L h_t-u_t||_H<=C_E/t+d B_E/d_Gamma(t).           (13)

This uses every prime through the actual bounded D_full; it is not a finite-head identity. Centering commutes with the COMPLETE L, hence

    ||L_c C h_t-Cu_t||_H<=C_E/t+d B_E/d_Gamma(t).

Fix any A>0 and let Q_A=1_[A,infinity)(L_c). Since L_c>=-d, the complementary spectral row has norm at most K_A=max(d,A). It follows that

    ||(I-Q_A)Cu_t||_H
       <=C_E/t+(d+K_A)B_E/d_Gamma(t).

The mean of u_t is O_E(1/t), by one integration by parts in its compact smooth mean integrand. Absorbing this term proves the explicit independent estimate

    ||Q_A Cu_t-u_t||_H
       <=C'_E/t+(d+K_A)B_E/d_Gamma(t)
       =O_(E,A)(1/log t).                            (14)

Thus ANY fixed compact high-carrier envelope is asymptotically preserved by projection onto a fixed ACTUAL strictly positive spectral range. These projected vectors are in Dom L_c intersect Ran L_c, and therefore perpendicular to the ENTIRE physical kernel, with no identification of that kernel required.

Applied to the packets above, (14) lets one fix e only for exact support isolation. For any finite r, the carriers can then be made large enough that the projected whole-matrix perturbation is arbitrarily small. The rank-dependent shrinking-width condition (10) is unnecessary for this alternative proof; it is not being silently mixed with the earlier order of limits.

In fact for every A>0, the compression Q_A D Q_A on Ran Q_A has

    sup sigma_essential(Q_A D Q_A)>=A_0,
    inf sigma_essential(Q_A D Q_A)<=-A_0.              (15)

To see this, first fix e. In (9), take the true Gram and tail errors arbitrarily small and use (14) to make the projected matrix errors arbitrarily small as well. For arbitrary finite r this gives tail Rayleigh subspaces of either sign with constants arbitrarily close to A_e. Min-max gives the corresponding essential spectral extrema. Finally let e->0, so A_e->A_0. Every envelope width is held fixed during its carrier limit.

Equation (15) is stronger than the conservative c_M=A_0/8 in the main theorem. The first-theta-term lower bound following (12) accordingly gives an essential-norm lower bound A_0>=pi^2Lambda(n_0)n_0^(3/2)e^(-pi n_0). It is still ABSOLUTE rather than threshold-relative.

## Inputs

- Complete theta positivity/smoothness of W, the actual bounded full correction, mean reduction, and admitted compact smooth source domain from the unified source.
- Complete Gamma modulation estimate, derived from the full symbol in HIGH_CARRIER_FAILS_UNIFORM_DERIVATIVE_LOWER_SIGN.md.
- Complete H-tail norm bound, independently proved with constant 80 in FINITE_PRIME_HEAD_HAS_INFINITE_SIGNED_INDEX_ON_ACTUAL_RADICAL.md.
- Only one explicit known prime power n_0=2^k is used to determine phase and support geometry; EVERY other prime contribution vanishes exactly before projection and is paid by the whole-tail operator norm afterward.

No RH, full-kernel identity, simple-zero count, numerical source calculation, matrix enumeration, or global sign is assumed.
