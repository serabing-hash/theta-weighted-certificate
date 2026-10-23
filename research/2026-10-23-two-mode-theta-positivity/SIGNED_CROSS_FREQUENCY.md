# Exact signed cross-frequency identity and the nonlocal determinant gap

## Outcome

There is an exact two-channel formula for the physical mixed Gram. It preserves the slowly modulated source correlation and the rapidly oscillating midpoint term separately. The already proved prime estimates give a genuinely nonlocal reduction to two low-prime correlations, with a uniform remainder less than 242/10^6. The Gamma contribution has an equally explicit finite-shift spectral identity.

These identities do not yet certify positivity for all separated pairs in the band. The unresolved quantity is a signed, weighted finite-shift Gamma overlap, jointly with two low-prime modulated correlations; the existing same-frequency moment budgets do not establish the matched determinant estimate. The obstruction below is a limitation of the present proof inputs, not a theorem that nonlocal positivity is false.

## 1. Definitions and exact polarized correlation

Use precisely the real-even full source W and pole-free form B=Q_inv of PHYSICAL_PROOF.md. Let

    q_u(x)=W(x)cos(ux),
    m=(u+v)/2,       h=(v−u)/2,
    U_s(y)=W(y−s/2)W(y+s/2),
    R_t(s)=∫_R U_s(y)cos(2ty)dy,
    A(s)=R_0(s),       Y(s)=∫_R y²U_s(y)dy.

The function U_s is positive and even in y; R_t(s) is real and even in t and s. Define J_(u,v)(s)=〈q_u,τ_s q_v〉. Because both physical modes are even, J_(u,v)(s)=J_(v,u)(s)=J_(u,v)(−s). Centering x=y−s/2 and using the product-to-sum identity gives exactly

    J_(u,v)(s)
      =½[cos(ms)R_h(s)+cos(hs)R_m(s)].               (1)

The first channel carries the midpoint frequency in s but the half-gap in y. The second reverses those roles. Neither oscillatory correlation is replaced by its absolute value in this identity. At s=0,

    J_(u,v)(0)=½[R_h(0)+R_m(0)].                    (2)

Since the polarized Gamma difference is 2[J(0)−J(s)], the full form is

    B(q_u,q_v)
      =∫₀∞ρ(s)[R_h(0)+R_m(0)
                  −cos(ms)R_h(s)−cos(hs)R_m(s)]ds
       −(cΓ/2)[R_h(0)+R_m(0)]
       −Σ_(n≥2)Λ(n)n^(−1/2)
                [cos(m log n)R_h(log n)
                  +cos(h log n)R_m(log n)].         (3)

The bracket inside the integral is kept coupled. Its terms are not integrated separately against the singular ρ at zero. The weighted H¹ continuity proof in the NEARBY_FREQUENCIES.md makes the complete expression and the full prime pairing legitimate; alternatively the source's rapid decay and the small-shift difference estimate suffice directly. Every prime power remains included.

## 2. Exact spectral two-channel decomposition

Let F(t)=∫W(x)exp(−itx)dx, dμ(t)=dt/(2π), H(t)=g(t)−cΓ, and

    k_z(t)=[H(z+t)+H(z−t)]/4.

Thus k_z is the h_gamma multiplier in the PHYSICAL_PROOF.md, with a different letter to avoid confusing it with the frequency half-gap. Expanding all four Fourier packets and using evenness gives the exact Gamma-plus-local contribution

    B_Γ(q_u,q_v)
      =∫ k_m(t)F(t−h)F(t+h)dμ(t)
        +∫ k_h(t)F(t−m)F(t+m)dμ(t).                (4)

For example the two same-sign packets have centers ±m and internal separation 2h. Their combined coefficient is precisely k_m, not twice k_m. The opposite-sign packets have centers ±h and separation 2m. At h=0, (4) reduces to the proved cosine carrier plus its opposite-packet term.

This representation is genuinely nonlocal: no expansion in h has been made. There is no assumption that F is nonnegative, unimodal, or log-concave. Such assumptions were not proved for this source and cannot be inserted to give F(t−h)F(t+h) a sign.

A useful exact cancellation identity is

    F(t−h)F(t+h)
      =½[F(t−h)²+F(t+h)²]
        −½[F(t+h)−F(t−h)]².                        (5)

It trades the signed overlap for a finite-difference square, but k_m is not known to be nonnegative everywhere. Thus (5) is not an automatic positivity proof. In particular the proved lower parabola for k_m cannot be multiplied directly by the signed product in (4) without controlling its sign.

## 3. A nonlocal prime reduction from already proved bounds

Pointwise positivity of U_s gives, for every real h,

    |R_h(s)|≤A(s).                                  (6)

The PHYSICAL_PROOF.md §7.2 proves the genuinely unsigned tail

    Σ_(n≥4)Λ(n)n^(−1/2)A(log n)<42/10^6.            (7)

Its §7.1 contour majorant for the complete cosine midpoint sum proves

    Σ_(n≥2)Λ(n)n^(−1/2)|R_m(log n)|
      <200exp(−m)<200/10^6,     m∈[14,29/2].        (8)

This uses a sum of absolute contour majorants, not an absolute value bound on a signed sum; multiplying each term by cos(h log n) therefore preserves it. Equations (6)–(8) show that the ENTIRE prime contribution in (3) equals

    −(log2/√2)cos(m log2)R_h(log2)
    −(log3/√3)cos(m log3)R_h(log3)+E_P(m,h),
    |E_P(m,h)|<242/10^6,                            (9)

uniformly for every real h and m in the band. No small-gap restriction occurs in (9). In particular the all-integer estimates continue to include n=4 and every later prime power.

The exact low-modulation source identity is

    R_h(s)=A(s)−2∫U_s(y)sin²(hy)dy.                 (10)

Hence

    A(s)−2h²Y(s)≤R_h(s)≤A(s).                      (11)

A fourth-moment refinement, with Y_4(s)=∫y⁴U_s(y)dy, is

    |R_h(s)−A(s)+2h²Y(s)|≤(2/3)h⁴Y_4(s).           (12)

These follow from elementary sine/cosine inequalities and keep the actual signed correlation. All moments are finite by full-source decay. However finiteness of Y_4, or an extremely coarse Gaussian upper bound, is not a sharp signed low-prime budget.

The PHYSICAL_PROOF.md's low-prime input contains sharp upper bounds for A(log2), A(log3), a lower bound for Y(log2), and a signed bound for Y(log2)−(log2)²A(log2)/4. Those were sufficient for the tangent Gram's particular combination. They do not, without a new estimate, provide a comparably sharp lower bound for R_h(log2) and R_h(log3) throughout a non-infinitesimal h interval. A lower bound on Y has the wrong direction when used in the lower bound in (11).

This is one concrete remaining source-correlation task, not an assertion that all upper bounds on Y are unavailable: coarse upper bounds follow from the existing envelopes, but no determinant-closing matched bound is established here.

## 4. Why current spectral moments do not finish a nonlocal determinant

For m in the band, the same-frequency proof controls integrals of k_m F², k_m F′², the signed same-frequency cross carrier, and exponentially small opposite-packet errors. In (4), the carrier is instead

    ∫ k_m(t)F(t−h)F(t+h)dμ(t).

The difference-square in (5) admits an h² upper bound through F′ and weighted derivatives, recovering a local perturbation argument. For finite h, the previously proved second/fourth source moments and pointwise Fourier envelopes do not automatically supply the necessary signed comparison with both diagonal entries. A new matched finite-shift inequality would be needed to exploit (5) beyond the proved local neighborhood.

For illustration, the known envelope F(t)²<(441/4)exp(−|t|) gives only

    |F(t−h)F(t+h)|≤(441/4)exp(−max{|t|,|h|}),
    ∫|F(t−h)F(t+h)|dμ(t)
         ≤(441/(4π))(|h|+1)exp(−|h|).               (13)

This is valid but loses precisely the sign and normalization information the determinant requires. On a band of width 1/2, |h|≤1/4, so the envelope has no large-separation suppression. The opposite packet retains large Fourier separation 2m, but its multiplier is k_h, not the same-frequency multiplier k_0. The envelope method requires a new check of that shifted multiplier on the intended half-gap range. No unchanged same-frequency opposite-Gamma constant, including 235/10^6, or bound uniform for all real h is asserted. The all-real-h conclusion above concerns the prime remainder only.

Equation (13) is an unweighted overlap bound, not a bound for the weighted integral with k_m. To bound the latter one must retain the multiplier and its own estimates; dropping it would be invalid. Nothing here assumes a bounded full prime spectral multiplier.

## 5. Exact determinant cancellation and the missing matched estimate

Write

    a_u=B(q_u,q_u),  a_v=B(q_v,q_v),
    b_uv=B(q_u,q_v),
    D_uv=B(q_v−q_u,q_v−q_u).

Bilinearity gives the exact cancellation formulas

    b_uv=(a_u+a_v−D_uv)/2,
    4det Gram(q_u,q_v)
      =2(a_u+a_v)D_uv−D_uv²−(a_u−a_v)².             (14)

In particular controlling |b_uv| by unrelated absolute triangle bounds discards the cancellation as v→u. The physical form is indefinite outside the certified trial planes, so Cauchy–Schwarz for B cannot be invoked to infer b_uv²≤a_ua_v; doing so would assume the desired two-plane positivity.

The positive diagonal bounds and the exact identities (3), (4), (9), (14) do not yet control the sign of the determinant for every separated u,v in I. A nonlocal proof would have to estimate the coupled finite-shift Gamma term and the two low-prime modulated correlations sufficiently sharply to close (14), or establish positivity directly in the centered sine/cosine basis. Neither conclusion is proved in this note.

The CENTERED_RADIUS.md already handles its explicit neighborhood, with the unavoidable gap² coefficient degeneration. This note does not enlarge that neighborhood by relabeling the missing determinant estimate. Its substantive additional results are the exact nonlocal two-channel formulas and the uniform all-prime reduction (9), together with identification of the precise remaining signed source and spectral quantities.

Any projected/original-domain version also requires the established bridge and its domain hypotheses. No actual root-pair application, arbitrary-pair positivity, arbitrary-rank positivity, root simplicity, or global/RH conclusion is asserted.


The same-frequency diagonal bounds apply when u and v individually belong to I. Midpoint membership with unrestricted h alone does not supply those diagonal bounds.
