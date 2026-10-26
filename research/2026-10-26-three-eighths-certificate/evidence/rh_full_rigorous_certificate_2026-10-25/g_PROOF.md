# Complete fine-source physical form G: analytic certificate specification

25 October 2026. Implementation prepared and compiled only. No execution or numerical certificate is claimed by this document.

## Scope and exact sources

There are N=552 positive cells of width δ=1/552. On the centered base cell, let ψ₀(x)=cosh(x/2)/n₀ and ψ₁(x)=sinh(x/2)/n₁, with n₀²=δ+2sinh(δ/2) and n₁²=2sinh(δ/2)−δ. Each half-cell mode has squared norm 1/2. The actual source φᵢα is the even reflection of its positive-cell translate, so the complete 1104 sources are orthonormal in the physical full-domain L² metric. The positive-series normalizers include a geometric remainder.

The computed form is G=Γ−cΓ I−P+t₀m. It retains the full killed/full-zero-extension Gamma operator, the five active powers 2,3,4,5,7 (Λ(4)=log 2), the original input enclosures for t₀,cΓ,π, and the complete theta source. It does not change the original coarse moments or compute a projection. This fine-source matrix is a building block for a later exact admissible lift congruence, not the final corrected inertia certificate.

## Six elementary/dilogarithmic primitives

For s>0, G₊(s)=s+½log(1−e^(−2s)) and G₋(s)=½log tanh(s/2). Let Jσ,k' = e^(ks)Gσ(s), k∈{−1,0,1}. The implementation uses

- J₊,−1=−e^(−s)G₊(s)−atanh(e^(−s));
- J₊,0=s²/2+Li₂(e^(−2s))/4;
- J₊,1=e^sG₊(s)−e^s+atanh(e^(−s));
- J₋,−1=−e^(−s)G₋(s)+½log(1−e^(−2s));
- J₋,0=[Li₂(e^(−s))−Li₂(−e^(−s))]/2;
- J₋,1=e^sG₋(s)−G₊(s).

Their continuous values at zero, in this order, are −log2, π²/24, log2−1, log2, π²/8, −log2. Direct differentiation verifies each identity using G₊'=1/(1−e^(−2s)) and G₋'=e^(−s)/(1−e^(−2s)). The zero limits remove cancellation of divergent individual terms at the endpoint.

MPFR `mpfr_li2` is called with directed rounding. Li₂ is increasing on (−∞,1], because its derivative is −log(1−x)/x>0 (with the continuous derivative 1 at zero). All arguments in this application lie in [−1,1]. Thus endpoint evaluation gives a valid interval extension; no numerical quadrature of Gamma remains.

## Half-cell Gamma block and full reflection

Write the base mode as the sum of exp(τx/2), τ=±1, with coefficients c₀τ=1/(2n₀), c₁τ=τ/(2n₁). Let Kαβ(dδ) be the Gamma bilinear form of the centered target base mode and source mode translated by dδ. The exact source row is the previously derived full Gamma primitive row. Multiplication by a target exponential leaves a power k=(τ+σ)/2∈{−1,0,1}, so the six J functions integrate every term.

For d≥1, set a=(d−½)δ, b=(d+½)δ. The exponential-pair integral equals

    −exp(−σdδ/2) {
      exp(kb)[Jσ,−k((d+1)δ)−Jσ,−k(dδ)]
      − exp(ka)[Jσ,−k(dδ)−Jσ,−k((d−1)δ)] }.

For d=0 it equals

    C₀ ∫[-δ/2,δ/2]exp(kx)dx
    − exp(kδ/2)[Jσ,−k(δ)−Jσ,−k(0)]
    − exp(−kδ/2)[J−σ,k(δ)−J−σ,k(0)],

where C₀=2log2+π/2. Summing with cατ cβσ gives K. All distances passed to the primitive cache are nonnegative integer multiples of δ; zero is handled by the exact continuous-limit branch.

Translation and reflection invariance give Kαβ(−d)=(-1)^(α+β)Kαβ(d), and self-adjointness gives Kβα(d)=(-1)^(α+β)Kαβ(d). The mixed d=0 entry is exactly zero. Independent interval formulas for K₀₁ and −K₁₀ are intersected, then the latter is assigned as the exact interval negation. This enforces a symmetric full enclosure without discarding any exact value.

For i,j=0,...,551, the full even-reflected matrix is

    Γᵢα,jβ = 2[Kαβ((j−i)δ)+(-1)^α Kαβ((i+j+1)δ)].

Only separations 0,...,1103 are required. This is a Toeplitz-plus-reflected-block construction of the complete matrix, not a submatrix or a finite Gamma-tail truncation.

## Exact prime overlaps

For a generic source-center displacement z with |z|<δ, the target/source intersection is [z−δ/2,δ/2] when z>0 and [−δ/2,z+δ/2] when z<0. The exponential-pair overlap is

    exp(−σz/2) ∫[lo,hi]exp((τ+σ)x/2)dx.

The integral is elementary, including the k=0 case. Outside |z|<δ the overlap is exactly zero. For each d and each prime power, use z=dδ±log n and coefficient Λ(n)/sqrt(n). Threshold and sign decisions are interval-certified; ambiguity fails closed. The same parity and full-reflection formula as for Gamma assembles all prime couplings. No shifted band is omitted.

## Metric blocks without large density-derivative amplification

The metric is supported on disjoint source cells, so it consists of 552 independent 2×2 blocks. On each original fine cell, approximate m₈(x)=2cosh(x/2)/κ₈(x) by its degree-five Taylor polynomial about the exact rational center. A seven-coefficient normalized interval jet supplies the midpoint coefficients and a sixth-coefficient range enclosure M₆ on the whole cell. Then

    |m₈(x)−p₅(x)| ≤ M₆ (δ/2)^6.

The polynomial is integrated against the basis products analytically through positive series for centered moments of cosh x±1 and sinh x. Ten positive terms plus a geometric tail enclose each moment; parity-zero moments are set exactly to zero. The basis is not differentiated to estimate the Taylor remainder. Since the reflected basis is orthonormal, a pointwise multiplier error E gives each block-entry error at most E by Cauchy–Schwarz, and an operator error at most E on that block. The implementation conservatively adds E to the radius of every block entry, which permits an operator row-sum error up to 2E.

The positive omitted theta tail obeys the inherited bound

    T(x)=4π² exp(9x/2) 9⁴ exp(−81π exp(2x))
         / [1−(10/9)⁴ exp(−19π exp(2x))].

For x≥0, κ=κ₈+Δ with 0≤Δ≤T, so

    0≤m₈−m≤2cosh(x/2) T / [κ₈(κ₈+T)].

This pointwise bound is evaluated on the entire cell and added to the Taylor remainder. No derivatives of the infinite theta tail are assumed. The exact interval t₀ multiplies the integrated polynomial and its remainder.

## Output and error meaning

All arithmetic and elementary functions use the existing 266-bit directed MPFR backend. Each exact matrix entry is enclosed before conversion. `Gmid.bin` contains a chosen binary64 center; `Grad.bin` contains an outward-rounded binary64 upper bound for the absolute distance of the exact entry from that center. Row-major order is the original fine physical source order (cell0 mode0, cell0 mode1, ...).

The enforced Gamma/prime block symmetry and identical metric mixed entries make the binary midpoint and radius matrices symmetric. The maximum radius row sum is therefore a valid global operator-norm error bound for G−Gmid. Input, normalizer, transcendental, primitive-cancellation, metric Taylor, theta-tail, summation and binary-conversion uncertainties are included. The output does not by itself certify a corrected congruence, a second eigenvalue, the infinite-dimensional bridge, or RH.

## Compile and execution boundary

The source was compiled against the already available MPFR/GMP runtime; no executable has been run as part of preparation. Numerical execution remains subject to the parent-approved bounded supervisor, exact frozen source hashes, independent static audit, output readback, and final spectral validation.
