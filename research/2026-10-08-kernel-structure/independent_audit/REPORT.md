# Independent audit of the theta derivative kernel

8 October 2026 UTC. Original review text is licensed CC BY-NC 4.0. This is a separate analytic review, not external human peer review, formal proof verification, a numerical inclusion audit, or a proof of RH.

## Verdict

**PASS for the stated all-orders minimum-operator theorem and its finite-rank consequences, with the analytic premises identified below. No fatal flaw was found.**

For every fixed integer j ≥ 0, the argument establishes f_j = κ^(2j)/κ ∈ D(L) and Lf_j = 0 for the same minimum closed realization. The f_j are linearly independent and have mean 4^(−j). Hence ker L ∩ {1}⊥ is infinite-dimensional. For every bounded finite-rank observation map W and every δ > 0, δ is an infinite-multiplicity eigenvalue of H_δ = L + δI + WW*. Under the additional hypothesis H_δ ≥ ηI with η > 0, the claimed matrix lower barrier also holds.

The review did not accept any prior PASS label as evidence. It checked the displayed estimates, the compact-to-minimum-domain passage, the mixed radical argument and its arithmetic normalization, and the operator and finite-dimensional consequences. No source, phase, H-action, FFT, Gram, eigensolver, or numerical verification program was run. Only local text was read and this report written; no external write was made.

## Precise premises and arithmetic check

The inherited analytic inputs are the Jacobi theta identity and completed-zeta Mellin identity, the classical compact-test multiplicative explicit formula as transcribed in the bridge, the unconditional zero-strip and zero-counting facts, and the standard theory of closable nonnegative forms and their self-adjoint representations. In particular, the external primary articles were not freshly retrieved for this review. The normalization and use of the supplied explicit formula were checked directly rather than promoted from a source label.

The minimum form is exactly the closure of the stated even compact smooth core for the positive continuous-plus-atomic jump energy E. The operator is exactly L = A − I/2 + P_1/2, with ν(dx) = 2κ(x)cosh(x/2)dx and ν(R) = 1. The original paper and bridge agree on these objects. Positivity of κ, its parity, and decay of each fixed derivative follow from their stated theta calculation. Closability follows from the positive edge measure: an H-null subsequence is null Lebesgue almost everywhere, and hence at both edge endpoints almost everywhere. This does not identify the minimum domain with a maximal-energy domain.

For the explicit formula, Φ(u) = u^(−1/2)C_h(log u) has Mellin transform F_h(z) overline(F_h(conjugate z)) at 1/2 + iz. Its pole contribution is 2|μ(h)|², and its prime contribution is subtracted with coefficient 2Λ(n)/√n. The negative archimedean term is

    −(log(4π)+γ_E)||h||²
    −2∫₀∞ [e^(s/2)C_h(s)−||h||²]/(e^s−e^(−s)) ds.

Subtracting the difference-energy expression leaves the finite correction

    2∫₀∞ (e^(s/2)−1)/(e^s−e^(−s)) ds
      = ψ(1/2)−ψ(1/4) = π/2+log 2.

Thus the stated c_Γ = log π + γ_E + π/2 + 3log 2, prime sign, and pole coefficient are consistent. Polarization gives the actual signed pairing, not an off-RH sum of absolute squares. The elementary edge expansion then gives Q(κf) = E(f) − Var_ν(f)/2 on the compact core, including the atomic coefficient without an extra factor two.

## Mixed radicality and cutoff control

The norm M(u) = ||u||_(H¹) + ||e^|x|u||₂ controls every signed-Q component. Small Gamma shifts use s||u′||₂, large shifts use 2||u||₂, and the prime correlation bound follows from |x|+|x+s| ≥ |s|. The resulting prime series is bounded by ΣΛ(n)n^(−3/2) < ∞. The pole functional is bounded because e^(−|x|)cosh(x/2) ∈ L². This proves a bound |Q(u,v)| ≤ C M(u)M(v), without Q ≥ 0.

For u = κ^(2j), smooth cutoffs converge both in M and in the bridge's S₂ norm, which is the exponentially weighted L¹ sum of derivatives of orders zero through two. The latter gives uniform O((1+|z|)^(−2)) Fourier control in the zero strip. Together with N(T) = O(T log(2+T)), it permits passage of the polarized zero sum to the cutoff limit.

F_u(z) = (−1)^j z^(2j)Ξ(z) vanishes at every zero argument and its conjugate, irrespective of the zeros' locations. Therefore Q(u,k) = 0 for every compact smooth even k. This is genuine mixed radicality. A zero diagonal value alone would not have sufficed. No RH, signed-form positivity, or global physical Weil operator is used.

## Ratio growth and the exact minimum domain

The recurrence P_(r+1) = P_r/2 + 2zP_r′ − 2zP_r has degree r+3, with leading coefficient −2 times the previous leading coefficient. For t = πe^(2x), x ≥ 0, the denominator is at least 2e^(x/2)t²e^(−t), since P₀(t) ≥ 2t². The derivative numerator is bounded by

    A_r e^(x/2)t^(r+2)e^(−t)
       Σ_(n≥1) n^(2r+4)e^(−3(n²−1)).

The series is finite for every fixed r. Division and parity therefore give |κ^(r)|/κ ≤ C_r e^(2r|x|). All constants may depend on r. This yields f_j ∈ H for each fixed j; no uniform-in-j estimate is needed to produce an infinite sequence.

The decisive step is correctly made on compact differences. Set f_(j,R) = χ_R f_j and u_(j,R) = κf_(j,R) = χ_Rκ^(2j). Weighted dominated convergence gives f_(j,R) → f_j in H and u_(j,R) → κ^(2j) in M. For d = f_(j,R) − f_(j,S), the compact identity gives

    0 ≤ E(d) ≤ C M(u_(j,R)−u_(j,S))² + ||d||²_H/2 → 0.

Hence the compact approximants are Cauchy in the actual minimum form norm. Closability identifies their H-limit with an element of that minimum domain. This is stronger than a finite maximal jump-energy calculation or convergence of individual diagonal energies.

For compact g, form convergence and signed-Q continuity give ℓ(f_j,g) = Q(κ^(2j),κg) = 0. The form is continuous in the minimum form norm, so core density extends this to every g in the form domain. Its representing H vector is zero. The representation theorem then gives f_j ∈ D(L) and Lf_j = 0. The proof neither changes the self-adjoint realization nor assumes that compact tests alone define an operator action without this extension.

## Independence and finite-rank consequences

A finite relation among the ratios gives a finite relation among κ^(2j). Fourier transformation yields p(t)Ξ(t) = 0 with p a polynomial. Since Ξ is nonzero on an interval, p vanishes identically. Integration by parts 2j times is legitimate at both ends and gives the mean 4^(−j). The centered vectors g_j = f_j − 4^(−j)1, j ≥ 1, are consequently independent null vectors in {1}⊥. They also satisfy Ag_j = g_j/2, so the stated infinite multiplicities and essential-spectrum assertion follow.

If K = ker L, then K ∩ ker W* is infinite-dimensional because W* has finite-dimensional range. It lies in D(L), and H_δ acts on it as δI. Thus every coercivity constant for H_δ is at most δ; no finite-rank frame can make the zero-shift operator coercive. Intersecting additionally with the orthogonal complement of any finite-dimensional deflation space preserves this obstruction. For a nonreducing deflation space the candidate correctly speaks of form restriction or compression.

For a closed K₀ ⊂ ker L, put V = P_(K₀)W and C₀ = V*V. Restrict the positive-inverse variational principle to K₀. The restricted quadratic term is δ||f||² + ||W*f||², so

    W*H_δ^(−1)W ≥ V*(δI+VV*)^(−1)V
                  = C₀(δI+C₀)^(−1).

Every vector in K₀ already belongs to the operator domain; W itself need not map into D(L). Positivity with a strictly positive lower bound for H_δ is essential here. If c₀ = ||C₀|| > 0, the resulting margin ceiling is ε ≤ δ/(δ+c₀). An infinite kernel alone gives no new numerical c₀ and no additional delta64 numerical exclusion.

## Consistency with constant deflation

The companion note's exact block factorization, finite congruence, and distinction between a Hilbert-space inverse bound and a coefficient-space certificate are consistent with this theorem. In its notation, U = PW and V = UQ are finite rank. The newly admitted family discharges its conditional premise dim ker L₀ = ∞. Therefore ker L₀ ∩ ker U* is infinite-dimensional, and both S and H have eigenvalue δ there. Whenever the inverses exist as bounded positive inverses, ||S^(−1)|| and ||H^(−1)|| are at least 1/δ.

The note's hypothetical sufficient assumption L₀ ≥ gI with g > 0 cannot hold for this actual operator once the present theorem is used. Its finite-dimensional examples remain legitimate illustrations of the abstract algebra, as explicitly scoped there. Nothing here proves that the reduced finite matrix F must have an O(δ) gap: observation overlap with the remaining kernel would be needed. The scalar inverse obstruction and a finite-matrix margin are distinct.

## Provenance and limits

The original paper already proves the constant and second-derivative operator admissions. The bridge already states all-order physical mixed radicality. The October 6 exterior proof §8 already contains fixed-order quotient growth, weighted integrability, centered saturation, and compact-cutoff energy convergence, while explicitly not asserting the current minimum operator realization. The September records already contain derivative source cancellation and the strict-constant obstruction.

The added content here is the explicit all-orders admission to the same minimum operator via compact differences, followed by independence and the infinite-kernel and finite-rank corollaries. It is a short operator-domain extension of established local ingredients, not discovery of the derivative family, a new saturation theorem, or a claim of global literature priority. The candidate's bounded novelty statement is accurate.

No kernel completeness, negative-spectrum exclusion, L ≥ 0, RH, growing-order estimate, new overlap enclosure, numerical certificate, or computational improvement has been established by this review.

## Local sources inspected

1. `/workspace/shared/theta_derivative_kernel_audit_20261008/PROOF.md`, all sections, and `SOURCES.md`.
2. `/workspace/shared/phase_checkpoint_review_delivery_20261008/published_text/bridge/PROOF.md`, especially §§1–5 and 7, and `SOURCES.md`.
3. `/workspace/shared/theta_delta32_release_20261007/theta_delta32_certificate.tex`, definitions and source representation, plus “The two noncompact source directions.”
4. `/workspace/shared/weighted_cost_1305/rh_theta_weighted_observation_audit/sources/inherited/EXTERIOR_COERCIVITY_PROOF.md`, §§1–4 and 8.
5. `/workspace/shared/local_compactness_audit/sources/history/SERABI_RH_SOURCE_SUBSPACE_AND_SCHUR_2026-09-18.md`, derivative and saturation passages, and `THETA_SOURCE_AUDIT_2026-09-18.md`, §8.
6. `/workspace/shared/saturation_sources/SERABI_RH_GROWING_DEGREE_SATURATION_COUPLING_PROOF_2026-10-06.md`, scope and inherited inputs only; its growing-order claims were not needed or audited.
7. `/workspace/shared/constant_mode_deflation_20261008/DEFLATION_NOTE.md`, and `/workspace/shared/constant_mode_margin_20261008/ADVISORY.md`. Saved numerical inclusions remain outside this analytic review.
