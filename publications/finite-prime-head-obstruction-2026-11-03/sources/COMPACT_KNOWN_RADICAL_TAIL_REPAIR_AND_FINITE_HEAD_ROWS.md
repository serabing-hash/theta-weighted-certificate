# Compact known-radical tail repair from finite prime-head rows

3 November 2026 UTC. A noncircular norm result for the actual complete operator and its known derivative radical. This supplies a convergent finite-rank null-repair construction, not a global sign, a uniform convergence rate, a full physical-kernel algorithm, or an exhaustive theta_j estimate. No historical novelty claim is made.

## Main result

Fix a finite prime cutoff M. Write D_raw=D_{>M} for the actual bounded self-adjoint prime tail on H and D=C D_raw C|H_c for its centered compression. Both satisfy the same norm cap. For the centered operator,

    D P_N compact,

where N=closure_H span{r_j:j>=1} is the known derivative radical and P_N is its exact H projection. No identification N=ker L_c is made.

Let P_m be the exact H projection onto span{r_1,...,r_m}, after any represented dependencies are removed. Put

    F_m=P_m D+D P_m-P_m D P_m,
    F_infinity=P_N D+D P_N-P_N D P_N.

Then F_infinity is compact, F_m has rank at most 2m, and

    ||F_infinity-F_m|| <= 2 e_(m,M) ->0,
    e_(m,M)=||D(P_N-P_m)||.                            (1)

For the centered finite-head operator L_M=L_c+D, the repaired operator

    L_M^(m)=L_M-F_m

annihilates the first m exact derivative radicals. Its whole known-radical row is uniformly small:

    ||L_M^(m)P_N|| <=e_(m,M) ->0.                     (2)

Most usefully, F_m can be constructed from the FINITE PRIME-HEAD rows L_M r_j alone. No action of the infinite tail or exact P_N is required to FORM this finite-rank correction. The nonconstructive quantity e_(m,M), or a certified upper bound for it, is still required to certify its convergence at a chosen numerical target.

## 1 Actual setting and centering

Use

    H=L2_even(dx/W), H_c=ker m,
    C u=u-2m(u)kappa,
    r_j=kappa^(2j)-4^(-j)kappa,
    N=closure_H span{r_j}, K=N^perp intersect H_c.

The complete operator L_c is the self-adjoint representative of q_0 on X_c and satisfies

    N subset Dom L_c, L_c|N=0.

Its complete correction D_full is independently bounded, with d=||D_full||. The centered form decomposition is L_c=Gamma_c-(D_full)_c; no invariant restriction of the raw T_Gamma is asserted. Every prime cutoff and remainder in this note is compressed by C when regarded as an operator on H_c. The uncentered raw prime head is not asserted to reduce H_c.

The absolute full-theta bound

    ||D_{>M}||<=80 sum_(n>M) Lambda(n)n^(3/2)e^(-pi n)

is proved directly from the entire theta series and weighted translations in FINITE_PRIME_HEAD_HAS_INFINITE_SIGNED_INDEX_ON_ACTUAL_RADICAL.md. Thus all prime partial sums converge in H-operator norm, including every prime power and both orientations.

## 2 Compactness of the known radical in ordinary L2

For n in N, the exact zero operator row gives

    t_Gamma[n]=<D_full n,n>_H<=d||n||_H^2.              (3)

Therefore the H-unit ball of N is bounded in the actual form space X. Its inclusion into ordinary L2(dx) is compact. Here is a short proof of the latter fact rather than an H-compactness assertion:

- The weighted norm makes ordinary spatial tails uniformly small:

      ||1_(|x|>R)u||_2^2
           <=sup_(|x|>R)W(x) ||u||_H^2 ->0.

- Since d_Gamma(t)->infinity, a uniformly bounded complete Gamma form gives uniformly small ordinary Fourier tails:

      integral_(|t|>T)|u_hat(t)|^2dt
           <=[inf_(|t|>T)d_Gamma(t)]^(-1)t_Gamma[u] ->0.

  Fourier-tail control also gives uniform ordinary translation continuity, by splitting the multiplier |exp(ith)-1| at fixed T.

- Spatial tightness, boundedness, and translation continuity give ordinary-L2 relative compactness by the standard compactness criterion.

Combining this with (3) proves that the inclusion J_N:N->ordinary L2 is compact. It emphatically does NOT make the H-unit ball of N compact in H.

## 3 Each prime row is compact on N, hence so is the complete tail

For a single prime-power shift s=log n, the numerator operator is a_n W(x) times either translation u(x+s) or u(x-s), with a_n=Lambda(n)/sqrt n. The following single-shift estimate is in the AMBIENT non-even ordinary and weighted spaces; a single shift does not preserve evenness. Its map from ordinary L2 to weighted L2(dx/W) is bounded, since

    ||W(. )u(.+s)||_H^2
         =integral W(x)|u(x+s)|^2dx
         <=||W||_infinity||u||_2^2.

Compose this map with the compact inclusion J_N and P_N. Each shifted row times P_N is compact into the ambient weighted space. Pair the +s and -s rows to obtain an even output; each actual paired prime-power row times P_N is then compact H->H. The centered compression C is bounded and does not change compactness.

Finite sums are compact. The full prime tail converges in H-operator norm, so D_{>M}P_N is compact as well. Self-adjointness also makes P_N D_{>M} compact. This proves the main compactness claim without an inverse of L_c or a spectral gap on its kernel complement.

## 4 Finite radical projections converge in operator norm after the tail

The nested finite radical projections P_m converge strongly to P_N, with P_m P_N=P_m. Since DP_N is compact,

    D(P_N-P_m)=DP_N(I-P_m) ->0 in operator norm.

The assertion follows, for example, by first approximating the compact DP_N by a finite-rank operator and then using strong convergence on the finitely many adjoint row vectors. The limiting operator is DP_N(I-P_N)=0. Thus e_(m,M)->0.

The exact difference identity is

    F_infinity-F_m
       =(P_N-P_m)D(I-P_m)+(I-P_N)D(P_N-P_m).

Both projections have norm at most one; D is self-adjoint. This proves (1) with coefficient two.

Since L_M=L_c+D and L_cP_N=0,

    (L_M-F_infinity)P_N=0,
    (L_M-F_m)P_N=(I-P_m)D(P_N-P_m).

The second identity proves the sharper equation (2) directly. All these products are well-defined operator rows: P_N maps H into the actual Dom L_c with zero L_c row.

## 5 The finite repair uses only finite-head actual rows

Write the source columns and TRUE H Gram as

    R_m=(r_1,...,r_m), G_m=R_m^*R_m>0,
    Y_(m,M)=L_M R_m.

By the exact complete radical row,

    Y_(m,M)=D R_m.

The left side is a complete Gamma action and FINITELY MANY prime shifts on finitely many actual theta derivatives. It can be formed without summing the tail or invoking a full-kernel projection. Since

    P_m=R_m G_m^(-1)R_m^*,

the correction is explicitly

    F_m=R_m G_m^(-1)Y_(m,M)^*
         +Y_(m,M)G_m^(-1)R_m^*
         -R_m G_m^(-1)(R_m^*Y_(m,M))G_m^(-1)R_m^*.       (4)

All inverse Grams are the actual weighted H Grams. No identity Gram, coefficient conditioning bound, rank-one soft-space premise, or missing prime orientation has been substituted. Formula (4) also shows rank(F_m)<=2m. Direct multiplication gives

    (L_M-F_m)R_m=0.

This is an exact finite null repair with a proved qualitative norm limit on the entire KNOWN derivative radical.

## 6 What this achieves, and the remaining signed question

At the limit,

    L_M-F_infinity
       =L_c+P_K D P_K,

understood on H_c; P_K=I-P_N there. It has the SAME known derivative radical N as a null space, possibly together with additional nulls. It differs from the actual complete L_c by a bounded operator of norm at most ||D||, so its self-adjoint domain is the actual Dom L_c. Finite repaired operators have that same domain.

The companion infinite-index theorem says every FINITE repair still leaves infinite positive and negative indices on N. There is no contradiction: the remaining whole known-radical operator rows have norm at most e_(m,M), which tends to zero. Compactness permits approximation, not a finite exact endpoint annihilation.

For each fixed positive target shift delta, one may seek an explicit certified m with 2e_(m,M)<delta and choose M so the complete tail norm is also below a chosen delta budget. The present proof supplies existence, not a practical or uniform rate for m. A finite-rank correction is NOT declared sufficient before this residual norm is paid.

Finally the unknown range-sector sign is unchanged: neither compactness nor exact radical repair proves

    L_c|K>=0,

or signs the actual low Schur matrix or full-history pivot. The result isolates a genuine noncircular kernel/tail norm control and an explicit finite-head-row construction, while retaining that arithmetic sign obligation.

## 7 The compressed tail has two infinite signed eigenvalue sequences

The operator

    T_(M,N)=P_N D P_N|N

is compact and self-adjoint. Its form is exactly q_M|N, because the complete q_0 annihilates N. The companion infinite-index theorem therefore gives infinitely many positive eigenvalues and infinitely many negative eigenvalues of T_(M,N), each sequence tending to zero. This is an actual compact tail-compression statement on the known radical, not a finite coefficient-Gram convention or a claim that the whole head operator leaves N invariant.

It provides a direct spectral explanation for why fixed finite-rank exact repairs fail while the finite-rank corrections above still converge in operator norm.

## 8 Relative compactness and the negative spectrum of every finite prime head

There is also a full centered-operator consequence. Choose a fixed safe s so that L_c+s and L_M+s are positive and boundedly invertible. The resolvent (L_c+s)^(-1) sends H_c boundedly into X_c by the coercive shifted-form estimate. Its map into ordinary L2 is therefore compact by Section 2.

As in Section 3, composing with any finite paired prime row and then C gives a compact H_c operator. The absolutely norm-convergent prime sum yields

    D(L_c+s)^(-1) compact.

The exact resolvent identity gives

    (L_M+s)^(-1)-(L_c+s)^(-1)
       =-(L_M+s)^(-1)D(L_c+s)^(-1),

which is compact. Hence L_M and L_c have the same essential spectrum. With the independently proved actual result sigma_essential(L_c)=[0,infinity),

    sigma_essential(L_M)=[0,infinity)

for EVERY finite prime cutoff M.

The next negative-spectrum conclusion needs only the older source's ABSENCE of negative essential spectrum, not the stronger equality or the newer construction of every positive essential spectral value.

The form q_M has infinite negative index already on the known radical. Consequently the negative spectral subspace of L_M is infinite dimensional. No negative essential spectrum is present, and L_M is lower bounded. Therefore EVERY finite prime-head operator has infinitely many negative DISCRETE eigenvalues, of finite multiplicity, accumulating at zero.

This remains true even under the hypothesis q_0>=0 for the complete form; under that hypothesis L_M>=-||D||I and these negative eigenvalues all lie in [-||D||,0). Without that hypothesis, no claim is made that every negative head eigenvector is purely an artifact: the rigorous artifact statement is that the complete form is exactly zero on the known-radical negative witnesses.

The fixed-head global endpoint sign is thus false for the actual operator. A successful approach must keep a positive shift and pay the tail budget, or handle the infinite null cancellation exactly, before asking for the remaining range-sector arithmetic sign.

## 9 The entire physical kernel is distinguished

The same compactness proof applies to P_0=1_{0}(L_c), the projection onto the ENTIRE physical kernel: its H-unit ball also satisfies (3), so D P_0 is compact. This does not identify P_0 with P_N or supply an effective full-kernel projection.

The explicit finite columns in Section 5 span only the known derivative-radical closure N. Their norm limit is the N-repair, not automatically the full P_0-repair. Additional physical-kernel directions, if any, must be retained separately. No completeness claim for a lower divided-chain bank is used here.
