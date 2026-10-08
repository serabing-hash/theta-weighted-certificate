# Sources for constant deflation revision 2

8 October 2026 UTC · CC BY-NC 4.0

## Preserved versions

The original `DEFLATION_NOTE.md` is unchanged. The updated argument is in `DEFLATION_NOTE_REVISION_2.md`. The unified textual comparison is `REVISION_2.diff`.

## Directly reviewed completed sources

1. `/workspace/shared/theta_derivative_kernel_audit_20261008/PROOF.md`
   - Snapshot: `revision_2_sources/THETA_DERIVATIVE_KERNEL_PROOF.md`
   - Used: fixed-order quotient growth, compact-difference admission to the same minimum form domain, mixed radicality and representation, independence and centering, and finite-rank consequences.
   - Source states its original text is CC BY-NC 4.0. Its analytic inputs and local provenance remain as stated there.
2. `/workspace/shared/infinite_kernel_independent_audit_20261008/REPORT.md`
   - Snapshot: `revision_2_sources/INDEPENDENT_KERNEL_AUDIT.md`
   - Used: direct signed-Q arithmetic and normalization check; mixed cutoff justification; independent check of minimum-domain passage; PASS verdict with named classical premises; distinction between inverse-norm and finite-matrix margin conclusions.
   - Original license: `/workspace/shared/infinite_kernel_independent_audit_20261008/LICENSE`
   - License snapshot: `revision_2_sources/INDEPENDENT_AUDIT_LICENSE`
3. `/workspace/shared/constant_mode_margin_20261008/ADVISORY.md`
   - Used: existing constant-mode barrier and exact inherited cover threshold. This revision does not recompute either quantity or validate the saved numerical inclusions anew.

## Scope of the update

The new revision discharges the old note's infinite-kernel conditional using the completed proof and independent audit. It explicitly rejects a positive unshifted gap on the actual e-perpendicular space, establishes delta as an infinite-multiplicity eigenvalue of the reduced operator S_delta, and records inverse norms at least 1/delta wherever the positive bounded inverses exist.

It does not assert a new finite reduced margin, a new overlap enclosure, absence of negative spectrum, nonnegativity of L, or RH. The old finite-dimensional examples remain purely symbolic examples, not calculations for the actual operator. No executable verifier, source/phase/H/FFT/Gram calculation, pilot change, external publication, or external message accompanies this revision.
