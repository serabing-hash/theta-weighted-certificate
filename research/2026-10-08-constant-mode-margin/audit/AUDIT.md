# Independent saved-data audit: constant-mode margin

8 October 2026. New audit text and rational checker: CC BY-NC 4.0.

## Verdict

PASS, conditional on the explicitly inherited analytic and saved-enclosure inclusion premises. The advisory correctly establishes

- c = ||W*1||² > 127/64;
- λmax(B1/64) > 127/128 > 99/100;
- therefore B1/64 ≤ 0.99 I is impossible for the unchanged minimum operator and fixed 372-coordinate W;
- this does not establish or rule out B1/64 < I. If the latter is separately proved, its positive gap must be strictly less than 1/128.

No mathematical correction to the advisory is required within its stated premise boundary.

## Domain and normalization

The release paper’s equations eq:measure and eq:constant state ν(R) = 1, 1 ∈ D(A) = D(L), and L1 = 0 for the minimum closed even realization. Its compact-cutoff argument admits the constant into the minimum form domain with zero energy; the closed-form representation then admits it into the operator domain. This is stronger than merely observing that a formal constant has zero jump energy.

With e = 1, ||e|| = 1, W bounded, and Hδ ≥ ηI for η > 0, bounded perturbation gives D(Hδ) = D(L), and Hδ has a bounded positive inverse. The advisory’s computation uses e ∈ D(Hδ), not e ∈ D(Hδ²). Injectivity alone would not suffice for that inverse assertion. No assumption L ≥ 0 is needed.

An independent short derivation confirms the barrier. Set x = W*e and c = ||x||². Then ⟨e,Wx⟩ = c and ⟨e,Hδe⟩ = c + δ. Cauchy–Schwarz in the Hδ/Hδ⁻¹ pairing gives

c² ≤ (c + δ)⟨Wx,Hδ⁻¹Wx⟩ = (c + δ)x*Bδx.

Dividing by c > 0 and applying the Rayleigh bound gives λmax(Bδ) ≥ c/(c + δ). The generic statement is non-strict. Strictness at δ = 1/64 follows from the strict lower bound on c, without an additional non-eigenvector claim.

The paper’s eq:Qfeatures and eq:trial64 fix w = 2κcosh(x/2) and Wt = P0/(2cosh(x/2)). Hence ⟨1,Wt⟩ν = ∫R κP0 = p0. There is no factor 1/2. The action ledger’s factor 1/2 belongs to the pole operator’s action norm and is not an overlap normalization.

## Exact arithmetic and provenance

I executed the supplied verifier with --bind-sources, without --emit, so its source package was not rewritten. It passed. I also wrote and executed a separate rational checker, verify_audit.py. It checks the original outer/nested archives and selected member hashes, exact saved-record correspondence, phase/base headers, 372-row T32/T64 prefix, both moment routes, and the positive delta64 cover bound. It does not import or run the source/action producer.

The exact first-column norm is

||t||² = 574870339585334557 / 1152921504606846976.

The positive lower endpoint of the saved pole interval is

p0,lower = 1386963357479687028045559562424556245249617 / 2^140.

Coefficient-space Cauchy–Schwarz yields c ≥ p0,lower²/||t||². Independent denominator clearing verifies the strict comparison to 127/64. This lower bound is approximately 1.9859166963200081; the decimal is explanatory only. The corresponding exact λ barrier is recorded in STATUS.json and is approximately 0.9921935176125845.

The second route reads all 372 saved phase records and 315 saved κ-moment records. The remaining 57 pairs use the inherited |d(r,m)| ≤ 2^20 exp(-m/128), enlarged to the exact ball ±2^(20-floor(m/128)) using e > 2. A rational alternating-series Machin enclosure supplies π. This route exactly reproduces the advisory’s recombined interval and strict lower fraction.

Its factor 64π and odd-component sign are correct: the period is P = 32π, the frequencies are m/16, and the two ±m contributions are +2 p(r,m)d(r,m), including the imaginary odd components. Thus p0 = 2P Σ p(r,m)d(r,m). No physical transform or integral is newly evaluated.

The cover threshold recomputes as ρ = εcover + dsharp. The exact inherited estimate at delta64 is positive:

η1/64 = 1446776856241610348487954379752034183297365381007 / 92620636523388719034562694367509285563269120000000 > 0.

This supplies the advisory’s uniform inverse premise at delta64 under the same inherited cover premises. The difference 127/128 − 99/100 is exactly 7/3200 > 0, so the target obstruction is strict. The lower barrier is below 1 and contains no upper estimate; it cannot decide B1/64 < I.

## Boundary and limits

The physical meaning of the saved whole-line source and phase balls remains an inherited inclusion premise. Their producer proof accounts for finite-source substitution, sampling alias, periodic/exterior tails and arithmetic. The archived phase audit binds the phases to the frozen coordinates. Reading its stored PASS and checking hashes does not independently regenerate or prove those inclusions.

The separate pole interval is supported by the saved whole-line moment construction, not by isolating a component of the total action residual. Cancellation makes that latter inference invalid. Both moment routes share inherited source information; they are independent algebraic routes, not independent physical integrations.

At or below ρ, failure of this particular coercivity estimator does not determine the true spectrum. Neither this lower barrier nor the saved-data audit proves positivity of L + δI, convergence to 1 without an upper bound, a delta64 upper certificate, or RH. The .99 target’s failure at delta64 does not contradict the existing delta32 target.

All new source, phase, H-action, FFT, physical Gram-integral and numerical eigensolve counts are zero. No Work prompt or external write was made.

## Saved anchors and reproduction

Reviewed: constant_mode_margin_20261008/ADVISORY.md; its code/verify_constant_mode.py; sources/constant_mode_inputs.json; inherited_PROOF.md sections 1, 4 and 6; inherited_ANALYTIC_REVIEW.md; the producer’s build_frame_and_pole and moment definitions; the stored phase audit; and theta_delta32_certificate.tex equations eq:measure, eq:constant, eq:Qfeatures, eq:trial64 and eq:genericsharp.

Run python verify_audit.py from this audit folder. It reads the existing source release at its recorded paths and writes only this folder’s STATUS.json. STATUS.json contains source hashes and exact outcomes.

New audit text and checker are licensed under Creative Commons Attribution–NonCommercial 4.0 International: https://creativecommons.org/licenses/by-nc/4.0/. Reused source material retains its original rights and terms. See LICENSE.
