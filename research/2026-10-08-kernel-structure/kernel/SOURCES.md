# Local sources and bounded duplication check

Inspected on 8 October 2026 UTC. This audit uses the supplied analytic identities and independently checks the derivative-ratio estimate, compact-difference minimum-domain argument, representation step, independence, and operator consequences. No external write or numerical evaluation was made.

## Current exact operator and bridge

1. /workspace/shared/phase_checkpoint_review_delivery_20261008/published_text/bridge/PROOF.md
   - §2: strict positivity, evenness, fixed-order theta decay, Fourier transform, probability normalization
   - §4: signed-Q controlling norm, compact-cutoff continuity, and the explicit statement Q(κ^(2j),k)=0 for every fixed j and compact smooth even k
   - §5: compact source-transform identity, minimum closure, and semibounded representation
   - §7: the distinction between form and operator admission and the core-to-full-domain representation argument
   - §9: finite shifted certificates remain separate from sign positivity

2. /workspace/shared/theta_delta32_release_20261007/theta_delta32_certificate.tex
   - §2, “Theta source and the minimum closed domain”: exact κ, ν, C, E, D, A, and L
   - §3, “Source cancellation and the signed representation”: Q and exact compact transform
   - subsection “The two noncompact source directions”, approximately lines 402–467 of this local file: already proves 1∈D(L), L1=0, and κ''/κ∈D(L) with zero action; includes the polynomial recurrence, derivative-ratio bounds, a direct jump-energy minimum-cutoff proof, and mixed-pairing representation
   - The paper's numerical theorem and saved inclusion claims are not needed for the null-family proof.

## Earlier derivative and saturation statements

3. /workspace/shared/weighted_cost_1305/rh_theta_weighted_observation_audit/sources/inherited/EXTERIOR_COERCIVITY_PROOF.md
   - §1, equation (3): explicitly inherits full radicality for every even derivative
   - §8, equations (33)–(37): centered ratios κ^(2j)/κ−4^(−j), all fixed-order ratio bounds, weighted integrability, finite transformed energy, exact critical equality, and compact cutoff energy convergence
   - §8 explicitly says its domain is the explicit transformed energy domain and does not postulate a closed global operator. Therefore it is not by itself an assertion of all-orders membership in the exact minimum D(L).
   - This is the closest prior local statement. Most of the derivative estimate and saturation content is inherited, not new.

4. /workspace/shared/local_compactness_audit/sources/history/SERABI_RH_SOURCE_SUBSPACE_AND_SCHUR_2026-09-18.md
   - §2, equation (2.2): full source derivative cancellation
   - §8, especially (8.4): exact source-ratio saturation and exponential quotient growth for fixed derivatives
   - These concern the source transform and saturation, and are not treated as an all-orders minimum-operator-domain proof.

5. /workspace/shared/local_compactness_audit/sources/history/THETA_SOURCE_AUDIT_2026-09-18.md
   - §8: audits the exact weighted transform, second-derivative saturation, cutoff passage, and obstruction to increasing the global critical constant
   - This establishes prior provenance for the strict-constant obstruction.

6. /workspace/shared/saturation_sources/SERABI_RH_GROWING_DEGREE_SATURATION_COUPLING_PROOF_2026-10-06.md
   - §1 inputs (I1)–(I3): inherited entire theta transform, derivative radicality, and form control
   - Later finite-dimensional Fourier saturation results concern a different physical truncation/projection question. They are not needed or reused as minimum-domain membership here.

## Certificate context

7. /workspace/shared/constant_mode_margin_20261008/ADVISORY.md
   - Defines H_δ=L+δI+WW* and B_δ=W*H_δ^(−1)W
   - Proves the constant-mode barrier under coercivity and its already-saved overlap enclosure
   - Read only for the scope and notation of shifted margin consequences. This audit does not recalculate that enclosure or assert any new numerical kernel-observation overlap.

## Limits of this search

This was a narrow inspection of the current paper, the supplied bridge, and the indicated historical source/exterior/saturation files. No exhaustive literature-priority or all-files search is claimed. The all-orders physical radical identity, quotient growth, and saturation are known within these records; the present text makes the exact minimum-operator extension and infinite-kernel consequences explicit.
