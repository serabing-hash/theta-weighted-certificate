# Corrected all-coefficient response certificate

This is a curated theorem and proof, not a numerical certificate or review transcript. All norms below are physical Hilbert-space norms unless a coordinate norm is explicitly displayed. Inner products are conjugate-linear in the first argument; † denotes the adjoint. No noncommuting factors may be reordered.

## 1. Operators, domains, and two different bounds

Let X be the high Hilbert space. Assume a>0, A₀=aI+2vv†, a nonnegative self-adjoint form/operator B_plus, and the form sum B_*=B_plus+A₀≥aI. Put K=B_*⁻¹. Let H_X be the self-adjoint operator associated with the densely defined closed form A₀+C_g, and assume H_X≥βI for some β>0; put R=H_X⁻¹, which is bounded. The original minimum high domain is separate from this auxiliary realization.

Define

    U = B_plus^(1/2) K,
    V = A₀ K,
    M_resp = U†U + V† R V.

The form meaning gives U†U=K−KA₀K, so U is bounded. In particular

    U†U ≤ K−aK² ≤ (4a)⁻¹ I,
    ||V|| ≤ κ_p := (a+2||v||²)/a.

Two constants have distinct purposes:

- ρ_R≥||R|| controls the inverse residual term.
- ρ_resp≥||M_resp|| controls source head/tail splitting.

With only the displayed positivity and R≤ρ_R I, the valid conservative choice is

    ρ_resp = 1/(4a) + ρ_R κ_p².

If the stronger form-order assumption H_X≥A₀+cI holds with 0<c≤a, then

    ρ_R = ρ_resp = ρ := 1/(a+c)

is valid. Indeed R≤(A₀+cI)⁻¹, so

    Δ := A₀−A₀RA₀ ≥ c A₀(A₀+cI)⁻¹ ≥ dI,
    d = ac/(a+c).

Consequently 0≤M_resp=K−KΔK≤K−dK²≤ρI. For the last inequality apply the scalar function b↦1/b−d/b² on b≥a; it is decreasing because 2d≤a. This proof does not assume B_plus, A₀, or C_g commute.

The assumption cannot be replaced by R≤ρI alone. The exact example

    a=c=1, ρ=1/2, A₀=diag(1,2),
    B_plus=(1/10)[[1,1],[1,1]], H_X=2I, R=I/2,
    K=(1/23)[[21,−1],[−1,11]]

has

    M_resp=(1/1058)[[525,−25],[−25,505]],
    λ_max(M_resp)=(515+5sqrt(29))/1058 > 1/2.

Here H_X−A₀=diag(1,0) does not dominate cI. This is an exact algebraic counterexample to the weakened premise, not a counterexample to the theorem.

## 2. Physical coordinates and complete source split

Let E:ℂ¹⁶→L be an injective coefficient map, with physical Gram matrix N=E†E>0. For a coefficient vector ξ define ||ξ||_N²=ξ†Nξ and ||A||_N=sup_(ξ≠0)||Aξ||/||ξ||_N. The orthonormal basis e₀,e₂,…,e₃₀ gives N=I.

Set S=YE, S_h=(P_M−Π_L)S and S_t=T_MS. Thus S=S_h+S_t. For every η>0, positivity of M_resp and the Hilbert-space Young inequality yield

    C := S†M_resp S
      ≤ (1+η) S_h†M_resp S_h
        +(1+η⁻¹)ρ_resp S_t†S_t.

At M=128, write S_t=T_MFE+Δ_src with ||Δ_src ξ||≤ε_M||ξ||_N, where ε_M=(3/2)E_k+(9/2)t_h is the complete remainder from sources/KERNEL_REMAINDER.md. For any η'>0,

    S_t†S_t ≤ (1+η')G^F +(1+η'⁻¹)ε_M²N,
    G^F[i,j]=〈T_MF b_i,T_MF b_j〉, b_i=E e_i.

Use an independently justified ε_M at other cutoffs. The full signed Gram includes all log/translation cross terms, branch overlaps, and the entire even projection prefix. Alternatively, triangle or trace bounds may be used with their demonstrated loss. The old fixed-vector h_A bound is not a bound for ||S_t||_N.

## 3. Residual identity and admissible trial

Let J:ℂ¹⁶→D(H_X) be complex-linear. Its columns must belong to the operator domain, so H_XJ is an X-valued map. Membership only in the form domain does not suffice for this L² residual formula.

Put W_h=US_h, F_h=VS_h and Ξ_h=F_h−H_XJ. Since RH_XJ=J, direct expansion proves the exact simultaneous matrix identity

    S_h†M_resp S_h
      = W_h†W_h + F_h†J + J†F_h − J†H_XJ + Ξ_h†RΞ_h
      ≤ W_h†W_h + F_h†J + J†F_h − J†H_XJ + ρ_R Ξ_h†Ξ_h.

This is one Loewner inequality for all complex coefficient vectors. It is not sixteen scalar diagonal checks. J=0 is admissible. A nonzero trial can improve sharpness, but its necessity is not established.

The same identity holds without head/tail splitting by replacing S_h with S. In that alternative, all source truncation errors must be included in the approximation contract below.

## 4. Approximation and outward-interval error contract

Assume certified bounds

    ||W_h−Ŵ||_N≤η_W,
    ||F_h−F̂||_N≤η_F,
    ||H_XJ−T̂||_N≤η_T.

Define Ξ̂=F̂−T̂, η_Ξ=η_F+η_T and the Hermitian matrix

    Ĉ_h = Ŵ†Ŵ + F̂†J + J†F̂
          −(J†T̂+T̂†J)/2 + ρ_R Ξ̂†Ξ̂.

Expanding the Gram terms and bounding their cross terms in operator norm gives

    S_h†M_resp S_h ≤ Ĉ_h+e_C N,
    e_C = 2||Ŵ||_N η_W + η_W²
          +2||J||_N η_F + ||J||_N η_T
          +ρ_R(2||Ξ̂||_N η_Ξ+η_Ξ²).

The J†T̂ term must be symmetrized. Errors in admissibility of J cannot be replaced by a numeric radius. The bounds must cover the full exact filter, full pole, source remainder, and any approximation of H_XJ.

Suppose C₀ is a Hermitian center and a symmetric nonnegative radius matrix r satisfies |(Ĉ_h−C₀)_(ij)|≤r_(ij). Then

    −D_r ≤ Ĉ_h−C₀ ≤ D_r,
    D_r = diag(sum_j r_(ij)).

For every ξ, this follows from

    |ξ†(Ĉ_h−C₀)ξ|
      ≤ sum_ij r_(ij)|ξ_i||ξ_j|
      ≤ sum_i (sum_j r_(ij))|ξ_i|².

D_r is a coordinate matrix; do not multiply it by N. By contrast an isotropic error in the physical norm becomes e_C N. When transforming from orthonormal coefficients ξ_on=V_coord ξ, V_coord†V_coord=N, transform every matrix by congruence V_coord†(·)V_coord, including any already-formed radius enclosure.

Let G^{F,up}≥G^F be obtained through a valid Loewner enclosure. A complete upper matrix is

    C_upper = (1+η)[C₀+D_r+e_C N]
      +(1+η⁻¹)ρ_resp[(1+η')G^{F,up}+(1+η'⁻¹)ε_M²N].

A sufficient remaining finite target is

    Q_lower − ε_out N − C_upper ≥ λN,  λ>0.

This target has not been evaluated. Isotropic budgets are valid sufficient constructions. Matrix-valued or endpoint-adapted budgets may be sharper, but no impossibility theorem for isotropic budgets is claimed.

## 5. Full-pole filter and its nonfinite tails

For the diagonal high comparison, impose separately D≥aI, B_plus=D−aI, and that D is reduced by the head/tail projections. Then B_*=D+2vv†. With

    u=D⁻¹v, d=1+2〈v,u〉,
    K=D⁻¹−(2/d)uu†,
    V=aD⁻¹+(2/d)(v−au)u†,

the full rank-one pole remains exact. For a finite head approximation Ŝ=PŜ, P=P_M−Π_L, set u_P=Pu, b=v−au, w=B_plus^(1/2)u, and ℓ=u_P†Ŝ. Then

    VŜ=aD⁻¹Ŝ+(2/d)bℓ,
    UŜ=B_plus^(1/2)D⁻¹Ŝ−(2/d)wℓ.

Even a finite head source generally produces filtered tails. If τ_v≥||T_Mv||, scalar spectral bounds for D≥aI give

    ||T_Mu||≤τ_v/a,
    ||T_Mb||≤τ_v,
    ||T_Mw||≤τ_v/(2sqrt(a)).

Writing s_P=〈Pv,D⁻¹Pv〉 gives

    2/[1+2(s_P+τ_v²/a)] ≤ 2/d ≤ 2/[1+2s_P].

These estimates require that D commute with/reduce the head projection; they are not valid merely because D≥aI. Truncating v and then calling the inverse exact omits the full-pole error.

For an orthogonal head/tail source approximation, bounds δ_head and δ_tail imply δ_S≤sqrt(δ_head²+δ_tail²). Safe propagation through the exact filter is

    η_W≤δ_S/(2sqrt(a))+δ_filter,W,
    η_F≤κ_p δ_S+δ_filter,F.

The δ_filter terms include all finite representation, denominator, and tail errors in the full-pole formulas.

## 6. Form-domain transfer and status

For application to an original form, require independently V_high⊂D(𝔥_X)=D_g∩X, original high-form domination of 𝔥_X on V_high, the actual mixed identity, low-projection admissibility, and the shell comparison. The inclusion concerns the form domain. Operator-domain membership is required only for J in the residual formula.

Admissible enlargement can then bound a supremum over V_high by the auxiliary inverse form over D(𝔥_X). It does not prove equality of the domains.

A rigorously positive finite matrix yields only the corresponding conditional fixed-supported-sector theorem. Actual all-low16 Schur sign, original weighted realization/core, support exhaustion and whole-line operator positivity remain unresolved here. No RH conclusion follows.
