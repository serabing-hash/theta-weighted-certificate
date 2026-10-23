# Nearby distinct frequencies: a genuine physical positivity neighborhood

## Result

Let W be exactly the full, unscaled theta source of PHYSICAL_PROOF.md, and use that document's actual pole-free physical form B=Q_inv and I=[14,29/2]. Put

    q_g(x)=W(x)cos(gx), v_g=∂_g q_g,
    d_(g,e)=(q_(g+e)−q_g)/e for e≠0, d_(g,0)=v_g.

There is a strictly positive, explicitly defined analytic radius δ, uniform for g∈I, for which

    B(r q_g+t d_(g,e), r q_g+t d_(g,e))
        ≥ (r²+t²)/128000                  (|e|≤δ).

In particular every sufficiently close pair of DISTINCT real frequencies, with the first in I, spans a positive physical two-plane. This is genuinely different from the same-frequency derivative-plane theorem. The radius below is extremely conservative, has not been evaluated, and is not claimed to contain any actual pair of zeta-zero ordinates. No root existence, simplicity, global positivity, or RH conclusion follows.

## 1. Actual form continuity, including every prime power

Work on the real Hilbert space X={f∈H¹(R): exp(|x|)f∈L²(R)} with norm

    N(f)²=||f||₂²+||f′||₂²+||exp(|x|)f||₂².

The symmetric real bilinear form is

    B(f,h)=∫₀∞ρ(s)〈f−τ_sf,h−τ_sh〉ds−cΓ〈f,h〉
       −Σ_(n≥2)Λ(n)n^(−1/2)[〈f,τ_(log n)h〉+〈h,τ_(log n)f〉],
    ρ(s)=exp(−s/2)/(1−exp(−2s)).

For 0<s≤1, ρ(s)≤2/s: concavity gives 1−exp(−2s)≥(1−exp(−2))s>s/2. Hence the small-shift integral is at most ||f′||₂||h′||₂. For s≥1, ρ(s)≤2exp(−s/2) and the two difference norms are at most 2||f||₂ and 2||h||₂. Thus the large-shift contribution is at most 16||f||₂||h||₂. The elementary bound cΓ<6 gives a total Gamma-plus-local bound

    ||f′||₂||h′||₂+22||f||₂||h||₂.

Since |x|+|x+s|≥s, weighted Cauchy–Schwarz gives, for s≥0,

    |〈f,τ_sh〉|≤exp(−s)||exp(|x|)f||₂||exp(|x|)h||₂.

Moreover, without any prime distribution theorem,

    Σ_(n≥2)Λ(n)n^(−3/2)≤Σ_(n≥2)(log n)n^(−3/2)
      ≤∫₁∞log(x+1)x^(−3/2)dx
      ≤4+2log2<6.

The cellwise inequality for the middle step uses x∈[n−1,n], log(x+1)≥log n and x^(−3/2)≥n^(−3/2). Consequently the full prime pairing is bounded by 12 times the product of the weighted norms. Cauchy–Schwarz in the three norm coordinates proves

    |B(f,h)|≤22 N(f)N(h).                              (1)

All series and integrals here converge absolutely as pairings on X. This is NOT a boundedness claim for the full prime multiplier on unweighted L². The exponential physical-space weights are essential.

## 2. Independent finite source-derivative constants

Here is an elementary, fully analytic upper bound, avoiding an unbounded or unevaluated derivative hypothesis. Let r=|x|. The full-source envelope is

    |W(x)|≤80 exp(4r−πexp(2r)).

A coarse differentiated bound, derived directly from the same full series, is

    |W′(x)|≤6400 exp(6r−πexp(2r)).                     (2)

Indeed on x≥0 write W=F0 Σp(t_n), t_n=πn²exp(2x), p(t)=(4t²−6t)exp(−t). One has F0≤2, |F0′|≤1/2, 0<p≤4t²exp(−t), and

    |(2t∂_t)p|≤(8t³+28t²+12t)exp(−t)≤48t³exp(−t).

Thus |W′|≤98Σt_n³exp(−t_n). Using n²−1≥3(n−1), n⁶≤64^(n−1), exp(3π)>8000 and π³<32 gives

    Σt_n³exp(−t_n)≤π³exp(6x−πexp(2x))
                          Σ_(n≥1)n⁶exp(−3π(n−1))
                       <64 exp(6x−πexp(2x)).

Now 98·64<6400; evenness handles the other half-line.

For integer j≥0 define

    L_j=12^(−j−1/2) Γ(j+1/2)
       =2∫₀∞r^(2j)exp(−12r²)dr,
    A_j²=exp(−6)[127808000 L_j+19200 j² L_(j−1)],       (3)

with the final term omitted when j=0. These are explicit finite constants, expressible using factorials, π and exp(−6). For every g∈[13,16],

    N(∂_g^j q_g)≤A_j.                                (4)

To verify this, |∂_g^j q_g|≤r^jW, and its x derivative is bounded by

    r^j|W′|+j r^(j−1)W+16r^jW.

Square the three-term bound using (a+b+c)²≤3(a²+b²+c²), and use (2) and the W envelope. Since π>3 and exp(2r)≥1+2r+2r²,

    exp(ar−6exp(2r))≤exp(−6−12r²),   a≤12.

All needed exponents are at most 12, including the exp(2r) weight. The two undifferentiated norm terms contribute 12800 L_j; the derivative terms contribute 3·6400² L_j, 19200j² L_(j−1), and 3·16²·80² L_j. Their sum is exactly (3). The constants are intentionally loose.

## 3. Joint differentiability through the divided-difference seam

The map g↦q_g is C∞ into X. For any fixed finite derivative order this follows from (2), the polynomial factors in x, dominated convergence in each of the three norm components, and the fundamental theorem of calculus in X. On the rectangle g∈I, |e|≤1 all intermediate g+te lie in [13,16]. The identity

    d_(g,e)=∫₀¹∂_g q_(g+te)dt                       (5)

holds in X, INCLUDING e=0. Thus, for all integers a,b≥0,

    ∂_g^a∂_e^b d_(g,e)=∫₀¹t^b ∂_g^(a+b+1)q_(g+te)dt,
    N(∂_g^a∂_e^b d_(g,e))≤A_(a+b+1)/(b+1).          (6)

For joint C² only A_0,…,A_3 are needed. In combination with (1), the product rule proves joint C² (indeed C∞) for every entry of the Gram G(g,e) of (q_g,d_(g,e)). Explicitly each first derivative of B(f,h) is B(f_i,h)+B(f,h_i); each second derivative is B(f_ij,h)+B(f_i,h_j)+B(f_j,h_i)+B(f,h_ij). Equations (1), (4), (6) independently bound every term. No formal differentiation of a conditionally convergent prime sum or of an unbounded spectral multiplier occurs.

## 4. A finite analytic radius, not just continuity language

The physical proof supplies a>9/100, 0<c<1/125, and S=b−c²/a>1/62500 for G(g,0). These give

    G(g,0)>(1/64000)I₂.                              (7)

For clarity, k=c/a<4/45 and y=r+kt imply

    r²+t²≤2y²+(2057/2025)t²,
    a>2/64000,
    S>2057/(2025·64000).

The last comparison is 62500·2057=128562500<129600000=2025·64000. This derives (7) directly from the physical theorem, independently of any original-domain bridge.

From (5), (4),

    N(d_(g,e)−v_g)≤|e|A_2/2,
    N(d_(g,e))≤A_1,  N(v_g)≤A_1.

Hence the Gram difference has zero (0,0) entry and satisfies

    |ΔG_01|≤11 A_0 A_2 |e|,
    |ΔG_11|≤22 A_1 A_2 |e|.

Its operator norm is bounded by its largest absolute row sum, giving

    ||G(g,e)−G(g,0)||op≤K|e|,
    K=11 A_2(A_0+2A_1)>0.

Define the explicit analytic radius

    δ=min{1,1/(128000 K)}.                           (8)

Then (7) implies G(g,e)≥I₂/128000 for |e|≤δ. Formula (8), with the elementary constants (3), is effective in the mathematical sense that it is finitely computable; no numerical value, practical lower spacing, or optimality is claimed. This is stronger than an unspecified compactness radius, but its severe conservatism matters.

## 5. Original two-cosine coordinates inevitably degenerate

For coefficients α,β,

    αq_g+βq_(g+e)=(α+β)q_g+eβd_(g,e).

Therefore, when 0<|e|≤δ,

    B(αq_g+βq_(g+e))
       ≥[(α+β)²+e²β²]/128000
       ≥e²(α²+β²)/384000.                           (9)

The second inequality uses det/trace for [[1,1],[1,1+e²]], whose determinant is e² and trace at most 3. Conversely the unit coefficient vector (1,−1)/sqrt(2) has value

    e² B(d_(g,e),d_(g,e))/2≤11 A_1²e².

Thus the smallest Gram eigenvalue in the ORIGINAL cosine coordinates is uniformly of order e², not uniformly bounded away from zero. Exactly,

    det Gram(q_g,q_(g+e))=e² det G(g,e).

The ε² loss is forced by coalescence, not an artifact of the continuity estimate. Positivity and independence hold for each nonzero ε in the neighborhood; the two-cosine ordered pair loses rank at ε=0.

## 6. Original-domain/projection extension

This section uses the minimum-domain identity, operator-null source space and projection theorem proved in ORIGINAL_DOMAIN.md, with its stated classical analytic inputs.

Under those hypotheses, set h_g=cos(gx)/C(x), C=cosh(x/2), and h_(g,e)^D=(h_(g+e)−h_g)/e, extended by ∂_g h_g at zero. The domain differentiability needed here can be established, rather than presumed, by the following extension of its common-cutoff proof.

For every finite j, ∂_g^j h_g is a polynomial-times-trigonometric function divided by C, uniformly over the enlarged compact band. Its H norm is finite because

    ||∂_g^j h_g||H²≤2∫|x|^(2j)W(x)dx<∞,

and its physical image is ∂_g^j q_g∈X. Common smooth cutoffs converge both in H and X. The core identity bounds cutoff differences by

    E(f)≤|Q_full(κf)|+||f||H²/2
        ≤C N(κf)²+||f||H²/2.

Here the pole is X-continuous: |μ(u)|≤||C exp(−|x|)||₂ ||exp(|x|)u||₂, with the first factor finite. This proves minimum-form-domain admission for all these derivatives by completeness. The same estimate extends to admitted differences and Taylor remainders. Their H and X Taylor remainders tend to zero in the appropriate derivative quotient norms by dominated convergence, so g↦h_g is C∞ in the minimum form norm. Equation (5) then also holds in that form norm for h.

Projection is continuous in this norm under the N⊂ker L result: for n∈N,

    E(n)=||n||H²/2−|〈1,n〉H|²/2≤||n||H²/2,

so ||P_N f||_(E+H)≤sqrt(3/2)||f||H. Thus projected h and divided differences have the same differentiability. By the polarized bridge their complete projected Gram is

    G(g,e)+2 z(g,e)z(g,e)^T,
    z(g,e)=(Ξ(g), [Ξ(g+e)−Ξ(g)]/e),

with the second entry Ξ′(g) at zero. The update is positive semidefinite, so the divided-difference lower bound transfers. In original two-frequency coordinates the pole vector is (Ξ(g),Ξ(g+e)); the coefficient lower bound (9) transfers as well. These conclusions use ORIGINAL_DOMAIN.md and the domain-differentiability argument supplied here.

Neither unprojected constraint admission at arbitrary frequencies nor explicit projection coefficients are claimed. No actual pair of roots is asserted to satisfy (8). Local positivity on this family is not positivity on sums of different such planes, a dense positive core, or a global/RH theorem.
