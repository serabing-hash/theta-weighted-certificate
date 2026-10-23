# A quadratic-error radius improvement for centered frequency pairs

## Finding and precise scope

A genuine improvement is available by canceling the odd frequency displacement BEFORE estimating the actual form. For pairs whose midpoint m lies in I=[14,29/2], average/central-divided-difference coordinates give an O(h²), rather than O(|h|), Gram error, where the two frequencies are m−h and m+h. This includes every sufficiently close pair with both frequencies in I.

The resulting full-gap radius is explicitly proved below to exceed 100 times the anchored theorem’s conservative radius, without evaluating any source integral or radius. This comparison is meaningful on the overlapping domain: an original first frequency in I AND the midpoint in I. It is not a replacement for the previous theorem for pairs going outward across an endpoint with midpoint outside I.

The improvement uses the already proved finite source moments A_0,…,A_3. It does not assert favorable signs for unknown mixed third-derivative pairings. Its gain is exact parity cancellation, not a renamed unknown modulus of continuity.

## 1. Proven inputs and notation

Use the exact full theta source and actual infinite-prime/Gamma bilinear form B=Q_inv. The coefficient implication in NEARBY_FREQUENCIES.md §4, using PHYSICAL_PROOF.md, gives uniformly for m∈I,

    Gram_B(q_m,∂_m q_m)>I₂/64000,
    q_m=W cos(mx).

NEARBY_FREQUENCIES.md establishes

    |B(f,k)|≤22 N(f)N(k),
    N(f)²=||f||₂²+||f′||₂²+||exp(|x|)f||₂²,
    N(∂_m^j q_m)≤A_j,       m∈[13,16],

where

    L_j=12^(−j−1/2)Γ(j+1/2),
    A_j²=exp(−6)[C L_j+19200j² L_(j−1)],
    C=127808000,

and the second term is omitted for j=0. These inequalities retain the full source and every prime power. No bounded full prime multiplier on unweighted L² is used. The maps involved are smooth into N's space.

## 2. Central coordinates remove every first-order displacement

For |h|≤1 and m∈I define

    c_(m,h)=[q_(m+h)+q_(m−h)]/2,
    d_(m,h)=[q_(m+h)−q_(m−h)]/(2h),
    c_(m,0)=q_m,       d_(m,0)=v_m=∂_m q_m.

Their integral representations and the symmetric second difference give

    N(c_(m,h))≤A_0,
    N(d_(m,h))≤A_1,
    N(c_(m,h)−q_m)≤h²A_2/2,                         (1)
    N(d_(m,h)−v_m)≤h²A_3/6.                         (2)

For (1), apply the integral Taylor remainder to q_(m+h) and q_(m−h), so their ±h v_m terms cancel. For (2), use

    d_(m,h)=(1/2)∫_(−1)^1 q′_(m+th)dt.

The first-order term th q″_m integrates to zero, and the quadratic remainder is bounded by h²t²A_3/2. Its average is h²A_3/6. These are Banach-space identities, not pointwise heuristics. All intermediate frequencies remain in [13,16].

For additional clarity, the exact signed Taylor coefficients in the actual form are

    B(c,c)=a+h²B(q,q″)+O(h⁴),
    B(c,d)=c₀+h²[B(q″,v)/2+B(q,q‴)/6]+O(h⁴),
    B(d,d)=b+h²B(v,q‴)/3+O(h⁴).                     (3)

Here c₀=B(q,v), all derivatives are at m, and the remainders are uniform on I by the already finite higher A_j. Each first h derivative is exactly zero. No sign of the second-order coefficients in (3) is inferred from positivity of the original two-plane.

## 3. Explicit square-root radius

Let G_c(m,h) be the B-Gram of (c_(m,h),d_(m,h)). From (1), (2) and the actual form bound,

    |(G_c−G_c(m,0))_00|≤22 A_0A_2 h²,
    |(G_c−G_c(m,0))_01|≤22(A_1A_2/2+A_0A_3/6)h²,
    |(G_c−G_c(m,0))_11|≤(22/3)A_1A_3 h².

For the mixed entry, write B(c,d)−B(q,v)=B(c−q,d)+B(q,d−v), so no uncontrolled mixed term is omitted. The diagonal estimates use sums of the two bounded norms. A convenient conservative operator-norm constant is

    K_c=22[A_0A_2+A_1A_2/2+A_0A_3/6+A_1A_3/3],
    ||G_c(m,h)−G_c(m,0)||op≤K_c h².                 (4)

Define

    h_* = min{1, (128000 K_c)^(−1/2)},
    Δ_* = 2h_* .                                    (5)

Then, uniformly for m∈I and |h|≤h_*,

    G_c(m,h)≥I₂/128000.                              (6)

Thus every distinct pair with midpoint in I and full gap |e|=2|h|≤Δ_* spans a positive physical two-plane. All constants in (5) are explicit factorial/Gamma expressions already bounded analytically; neither an unknown derivative constant nor a new numerical evaluation is involved.

## 4. A strict analytic comparison with the previous radius

The anchored theorem’s radius was

    δ_old=min{1,1/(128000 K_old)},
    K_old=11A_2(A_0+2A_1).

Set T=A_0 and η=19200/C<1/6000. The exact moment ratios are

    L_1/L_0=1/24,
    L_2/L_0=1/192,
    L_3/L_0=5/4608.

Consequently the following deliberately coarse inequalities follow by rational comparison:

    A_1<T/4,
    T/14<A_2<T/12,
    A_3<T/24.

For example A_2²/T²=1/192+η/6 and A_3²/T²=5/4608+3η/64. They imply

    K_old>T²/2,
    K_c<22T²[1/12+1/96+1/144+1/288]
        =(55/24)T²<3T².                              (7)

Also

    T²=exp(−6)C sqrt(π/12)>C/1458>1,

using exp(1)<3 and π>3. Thus δ_old=1/(128000K_old)<1/64000. If h_*=1, then Δ_*=2>100δ_old. Otherwise, (7) gives

    (Δ_*/δ_old)²
      =512000 K_old²/K_c
      >(128000/3)T²
      >10000.

Therefore, in either case,

    Δ_*>100δ_old.                                    (8)

This is an exact coarse inequality, not a computed spacing or sampled numerical comparison. It does not imply either radius is practically large.

## 5. Original-coordinate lower bound and unavoidable degeneration

For the two original cosine modes,

    αq_(m−h)+βq_(m+h)=(α+β)c_(m,h)+h(β−α)d_(m,h).

Since |h|≤1, (6) implies

    B(αq_(m−h)+βq_(m+h))
       ≥[(α+β)²+h²(β−α)²]/128000
       ≥h²(α²+β²)/64000
       =e²(α²+β²)/256000.                            (9)

The symmetric and antisymmetric coefficient directions make the second inequality exact at the level of its comparison matrix. Conversely the unit antisymmetric coefficient vector has form value

    e² B(d_(m,h),d_(m,h))/2≤11A_1²e².

The least original-coordinate eigenvalue still has order e². Centering improves the certified neighborhood and the lower-bound coefficient, not the unavoidable coalescence degeneration.

## 6. What remains unavailable, and why the scope must not be inflated

For an anchored pair (g,g+e) with g at an endpoint of I and e pointing outward, its midpoint m=g+e/2 leaves I. The same-frequency margin then supplies no value at m. Smoothness alone bounds the lost midpoint margin by a first-order error involving the derivative of Gram(q_m,v_m). Its entries include

    2B(q,v),
    B(v,v)+B(q,q″),
    2B(v,q″).

The same-frequency theorem controls the first entry's sign, but does not provide the directional matrix inequality needed to extend its full coefficient margin outward at both endpoints. In particular no favorable signs or sufficiently sharp endpoint bounds for B(q,q″) and B(v,q″) have been established here. Applying the generic weighted-norm estimate to this midpoint displacement reinstates a linear error, so the centered quadratic improvement cannot honestly be advertised as uniform over the entire old anchored rectangle.

The old theorem remains valid for those outward pairs. This new theorem is stronger on midpoint-in-band pairs, including pairs with both frequencies in I. A genuinely larger band-uniform endpoint extension would require additional signed/matrix estimates or a same-frequency margin on a larger band.

Using ORIGINAL_DOMAIN.md and the form-domain differentiability in NEARBY_FREQUENCIES.md, the positive-semidefinite pole update transfers (6) and (9) to the projected family. No actual zero pair is asserted to satisfy either gap bound; no arbitrary-pair, arbitrary-rank, density, root-simplicity, or global/RH claim follows.
