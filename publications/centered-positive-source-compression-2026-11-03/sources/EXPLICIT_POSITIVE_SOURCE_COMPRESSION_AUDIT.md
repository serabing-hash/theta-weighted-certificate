# Explicit positive-source compression in the actual centered Hilbert space

3 November 2026 UTC. Independent analytical audit, PROVISIONAL pending a separate proof audit. No numerical runs, new inverse solve, runtime bound, sign, gap, or RH conclusion are asserted. The fixed negative-count note remains unchanged.

## 1. Actual operator and the compression problem

Use the exact theta weight and normalization

    H=L²_even(dx/W), W=κ/(2cosh(x/2)), ||κ||_H=1,
    C=I−κ⊗κ, H_c=κ^⊥, B₀=∫W≤1/4,
    W(x)≤40 exp(4|x|−3e^(2|x|)).

The finite prime head has

    c_N(t)=cΓ+2Σ_(2≤n≤N)Λ(n)n^(−1/2)cos(t log n),
    C_N=cΓ+2Σ_(2≤n≤N)Λ(n)n^(−1/2),
    b_N(t)=(c_N(t)−d(t))_+,
    T=T_N=(1/2)√(e^(2C_N)−1)>0.

Here d(t)≥(1/2)log(1+4t²), so b_N is supported on [−T,T], and

    ∫₀^T b_N(t)dt
      ≤∫₀^T [C_N−(1/2)log(1+4t²)]dt
      =T−(1/2)arctan(2T)≤T.                            (1)

The true Fourier evaluation vector and positive operator are

    g_t(x)=W(x)cos(tx)/√(2π),
    B=B_N=2∫₀^T b_N(t)|Cg_t⟩⟨Cg_t|dt.               (2)

These are H vectors and an H trace-class operator. The full centered form is

    L_c=A_N−B_N−D_(>N), A_N≥0,
    ||D_(>N)||≤τ_N≤160(N+1)²e^(−π(N+1)).               (3)

All form comparisons below use the full form domain, not just the compression bank. Statements (1)–(3), including normalization and domain, are the established inputs in the source notes listed at the end.

## 2. An explicit independent bank and its true Gram

For finite R>0 and integer m≥0 define

    v_j=C[W(x)x^(2j)1_(|x|≤R)]/√(2π), j=0,…,m,
    V=(v_0,…,v_m), r=m+1, G=V*V,
    P=VG^(−1)V*, Q=I−P on H_c.                        (4)

The columns are independent. If their linear combination vanishes, the uncentered vector W(x)p(x)1_(|x|≤R) is a multiple of κ. Outside [−R,R] this vector is zero whereas κ>0, so the multiple vanishes. On (−R,R), W>0 and the even polynomial p then vanishes almost everywhere, hence identically.

For

    a_j=∫_(−R)^R κ(x)x^(2j)dx,
    w_l=∫_(−R)^R W(x)x^(2l)dx,

the exact Gram is

    G_ij=[w_(i+j)−a_i a_j]/(2π)>0 as a matrix.          (5)

The inequality is matrix positive definiteness, not entrywise positivity. These are incomplete-interval moments. Replacing them by full-line moments or an identity coefficient Gram would be incorrect.

The indicator bank is only required to belong to H_c. No membership in Dom A_N is used or claimed. Inverse residual trials must separately belong to Dom A_N; they are not these indicator columns.

## 3. Uniform source approximation and the trace defect

Put k=2m+2 and use the real Taylor polynomial

    p_(m,t)(x)=Σ_(j=0)^m (−1)^j(tx)^(2j)/(2j)!.

Taylor's theorem at order 2m+1, whose last odd coefficient is zero, gives

    |cos(tx)−p_(m,t)(x)|≤E:=(TR)^k/k!

for 0≤t≤T and |x|≤R. Centering is an H contraction and the centered truncated Taylor vector belongs to Ran P. Consequently

    ||Q Cg_t||_H²
      ≤[W_tail(R)+B₀E²]/(2π),
    W_tail(R)=∫_(|x|>R)W(x)dx.                         (6)

Inside the interval this is the Taylor error integrated against W; outside it is the bound |cos(tx)|≤1. The two regions are disjoint, so no cross-term factor is needed. From (1), (2), and (6),

    ε_P:=tr(QBQ)
       =2∫₀^T b_N(t)||Q Cg_t||_H²dt
       ≤(T/π)[W_tail(R)+B₀E²].                         (7)

Thus the proposed factor T/π is correct. Using only b_N≤C_N would introduce an unnecessary C_N factor.

## 4. Completely explicit radius and rank

For every R≥0, set Y=e^(2R)≥1. Direct integration of the envelope gives

    W_tail(R)≤(40/9)(3Y+1)e^(−3Y).

The following looser bound is convenient:

    W_tail(R)≤40Y²e^(−3Y)≤40e^(−Y).                    (8)

For the first inequality in (8), the logarithmic derivative of exp(4x−3e^(2x)) is at most −2 for x≥0. Integrating its exponential tangent majorant on both half-lines gives 40exp(4R−3e^(2R)). The second inequality follows from log Y≤Y.

Given any requested error ε>0, choose

    h=max(1,T/ε),
    R=(1/2)log log(80h),
    r=ceil(max{1,3TR,(1/2)log₂(2h)}),
    k=2r, m=r−1.                                      (9)

Then R>0 and (8) gives W_tail(R)≤1/(2h). The elementary factorial inequality k!≥(k/e)^k and e<3, together with k≥6TR, imply

    E≤(eTR/k)^k≤2^(−k)≤1/(2h).

Therefore, using B₀≤1/4,

    ε_P≤(T/π)[1/(2h)+1/(16h²)]
        ≤9T/(16πh)≤9ε/(16π)<ε.                        (10)

This has slack intentionally. In particular,

    r≤3TR+(1/2)log₂(2h)+2,
    R=O(1+log log(e+T/ε)),
    r=O(T[1+log log(e+T/ε)]+1+log(e+T/ε)).             (11)

The formula is an explicit analytic rank bound. For an actual certified implementation, use rigorous upper caps for T, h, and R and choose an even k satisfying the inequalities strictly. This avoids needing to decide whether a computable real equals an integer in a ceiling operation. Increasing the certified radius requires recomputing the degree condition k≥6TR.

## 5. Computable entries without a Gram or domain shortcut

Let Xi(t)=∫κ(x)cos(tx)dx and define

    l_j(t)=⟨v_j,Cg_t⟩_H
      =[∫_(−R)^R W(x)x^(2j)cos(tx)dx−a_j Xi(t)]/(2π).

All quantities are real, and

    K_ij=⟨v_i,Bv_j⟩_H=2∫₀^T b_N(t)l_i(t)l_j(t)dt.     (12)

The theta series on compact intervals, with its explicit summand tails, and the full-line κ envelope provide arbitrarily accurate rigorous enclosures for (5), (12), and Xi. The indicator causes no interior quadrature discontinuity: its moments are integrated directly on [−R,R]. The positive part b_N is computable and locally Lipschitz, so certified compact-interval quadrature does not require root isolation or root-separation assumptions.

Positive definiteness of the exact G proves that sufficient precision eventually certifies a positive lower eigenvalue bound, and hence allows certified orthonormalization U=VG^(−1/2). It gives no useful precision or conditioning bound. Exact Gram computability here means explicitly defined computable real integrals with arbitrarily narrow rigorous enclosures, not a claimed closed-form symbolic evaluation.

## 6. Regularized positive approximation using actual B sources

Let U:C^r→H_c be the isometry above and put

    M=U*BU=G^(−1/2)KG^(−1/2),
    λ>0,
    F=BU(M+λI)^(−1/2), X=FF*=BU(M+λI)^(−1)U*B.       (13)

Then

    0≤X≤B,
    ||B−X||≤tr(B−X)≤ε_P+rλ.                           (14)

Proof of order: with Z=B^(1/2)U, M=Z*Z and

    X=B^(1/2)[Z(M+λI)^(−1)Z*]B^(1/2).

The middle positive operator is a contraction because its nonzero eigenvalues are μ/(μ+λ), μ∈σ(M). This uses B^(1/2) only in the proof, not to compute F.

For the trace, write Q=I−UU*. Since

    U*B²U=M²+U*BQBU≥M²,

cyclicity of the finite trace gives

    tr X≥tr[(M+λI)^(−1)M²],
    tr B=tr M+ε_P,
    tr(B−X)≤ε_P+λ tr[M(M+λI)^(−1)]≤ε_P+rλ.

There is no required positive lower bound for M, and no inverse of M is taken. The λ lower bound does not remove the conditioning of the original true Gram G or the cost of computing its entries. Actual source columns BU are H vectors; the compact integral (2), with (12), computes them. They are distinct from operator-domain inverse trial columns.

More explicitly, every column of F has the form

    f_i=2∫₀^T b_N(t)s_i(t)Cg_t dt=W p_i−κβ_i,
    p_i(x)=2/√(2π)∫₀^T b_N(t)s_i(t)cos(tx)dt,
    β_i=2/√(2π)∫₀^T b_N(t)s_i(t)Xi(t)dt,
    ||p_i||∞≤2/√(2π)∫₀^T b_N(t)|s_i(t)|dt,

where the computable s_i are finite linear combinations of the l_j in (12). Thus the sources are compact-frequency cosine integrals, not generally finite cosine sums. Their uniform p_i bounds and the existing W and κ²/W tails give the same computable physical residual-tail bounds as for finite cosine sources. This supplies the small extension needed when using these sources in the separate residual certificate; no regularity of an unknown inverse solution is presumed.

For any S=A_N+sI with s>0,

    0≤S^(−1/2)(B−X)S^(−1/2),
    ||S^(−1/2)(B−X)S^(−1/2)||≤(ε_P+rλ)/s.             (15)

The nonzero spectrum of S^(−1/2)XS^(−1/2) is represented by the finite inverse Gram F*S^(−1)F. Thus a residual certificate for those r exact H sources can be combined with the explicit additive error (15). For an allocated inverse-Gram error η>0, taking the compression target ε=sη/2 and λ=sη/(2r) suffices. If the allocation is η of order s, the required unshifted source error is of order s². This is an error-budget statement, not a lower bound for the actual Birman–Schwinger margin.

## 7. Rank at a shrinking shift

For 0<δ≤1 choose the established complete-tail schedule

    N=max(8,ceil(log₂(2/δ)))−1,
    τ_N≤δ/2,
    C_N≤16+6√N,
    T_N<e^(C_N)/2.                                    (16)

The elementary bound for C_N uses the full von Mangoldt sum and does not require PNT or a zero-location hypothesis. With L=1+log(1/δ), we have N=O(L) and log T=O(√L).

For every fixed a>0 and p>0, a target ε=aδ^p gives log h=O(L), R=O(1+log L), and hence

    r≤exp(O(√L))=δ^(−o(1)).                            (17)

In particular the order-δ² source target needed by an order-δ inverse-error allocation has subpolynomial source rank. The constants may depend on a and p. This controls only the source dimension. It controls neither inverse trial count nor arithmetic precision, total runtime, the true Gram condition number, or an actual sign margin.

## 8. Additional consequence: all positive Schatten exponents

This section is a new consequence of the explicit compression, beyond the earlier fixed note. It is included for separate independent audit, not silently substituted into that note.

For δ∈(0,1], take (16) and use (9) with ε=δ/4. On Ran Q,

    ⟨u,B_Nu⟩≤||QB_NQ||·||u||²≤ε_P||u||²<δ||u||²/4.

The compact min–max principle gives λ_(r+1)(B_N)≤ε_P. Alternatively, apply the full-domain negative-subspace argument directly: if the spectral subspace of L_c below −δ had dimension greater than r, it would contain a nonzero u∈Ran Q, whereas (3) would give

    q[u]≥−(ε_P+τ_N)||u||²>−3δ||u||²/4,

contradicting q[u]<−δ||u||². The same strict slack handles the closed threshold (−∞,−δ]. Consequently

    dim Ran 1_(-∞,−δ)(L_c)≤r
      ≤exp(O(√(1+log(1/δ)))).                          (18)

This removes the earlier δ^(−1) prefactor by using an explicit finite-rank source approximation, rather than just the total trace. Compactness of (L_c)_− follows as in the fixed note. For every p>0, (18) implies n_−(δ)≤C_p δ^(−p/2) for sufficiently small δ, and therefore

    tr[((L_c)_−)^p]
      =p∫₀^|| (L_c)_− || δ^(p−1)n_−(δ)dδ<∞.            (19)

Thus the new compression argument implies (L_c)_−∈S_p for every p>0, including S_1. For 0<p<1, S_p denotes the usual Schatten quasi-class. This does not imply finite negative index, exclude negative eigenvalues, or give any sign at zero. No inverse, known-radical projection, or full-kernel identification is used in (18)–(19).

## 9. Scope and provenance

The projection P in this note is a source-compression projection, not a projection onto derivative radicals, a low collar, or the entire kernel. No rate for any of those other projections is supplied. No assertion of positivity, a nonzero spectral gap, an actual finite inverse margin, or efficient numerical certification follows from this note.

Sources read locally, without changing or rerunning them:

- `scalar_first_bracket_20261103/SCALAR_BRACKET_PROOF_AND_CODE_CONSTANTS.md`: actual theta normalization, H, C, Fourier vectors, envelope, and complete prime-tail bound.
- `scalar_first_bracket_20261103/NEGATIVE_SPECTRAL_COUNT_AND_SCHATTEN_AUDIT_20261103.md`: finite-head support, integrated b_N bound, full-domain comparison, elementary prime cutoff and prime-sum estimate. Its unchanged SHA256 is `16a0abbf796b1606aff6cf93dcc1954ea098b5cb90b72424e11efae1ee8c86b0`.
- `scalar_first_bracket_20261103/FINITE_BANK_EIGENVALUE_AND_KY_FAN_ADDENDUM_20261103.md`: true-Gram conventions and source-bank domain scope.
- `residual_inverse_audit_20261103/SHIFTED_RESIDUAL_INVERSE_CERTIFICATE.md`: separate provisional inverse-residual certificate and its remaining margin, trial-complexity, and conditioning limits.
