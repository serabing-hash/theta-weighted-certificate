# Reproducibility and inspection

## Byte verification

From this directory, run a standard SHA-256 tool:

    sha256sum -c MANIFEST.sha256

On systems with shasum instead:

    shasum -a 256 -c MANIFEST.sha256

This checks publication payload identity only. It does not prove the theorem. The manifest excludes itself to avoid self-reference. PROVENANCE.json separately records hashes and lengths of the complete supplied research sources and review texts from which excerpts were selected. Because this publication contains excerpts, its files are not expected to equal the hashes of those full sources.

## Analytic reproduction route

1. Recompute the displayed finite artanh-series lower bounds and geometric remainder bounds for log(2), log(3), log(5). Establish the ordered bands and all excluded shifts.
2. Expand the complex edge square. Check every row and its coefficient slack with c2<1/2, c3<13/20, c4<7/20.
3. Apply the separate weighted Schur bound. Check each 7/4/2 adjacency directly; no numerical eigenvalue estimate is needed.
4. Differentiate the complete-tail identity and prove kernel monotonicity from the displayed sinh/cosh series. Do not truncate R.
5. Derive the two position reserves. Prove c_Gamma, j_7 and delta_0 bounds by the displayed rational series/integral comparisons.
6. Expand the matrix cancellation once, retaining each nonnegative term once. Obtain c_coer=omega delta_0+theta j_7.
7. Check dense closedness on D_g and the distinct operator domain. Read the endpoint counterexample in the reviews to distinguish form-norm closedness from an L2-closed set.
8. For minimal Gamma-domain inclusion, use the direct nonnegative exterior decomposition in the Claude local audit. Do not import an unproved Legendre identity or a Q/b_full equality.

A self-contained manuscript should reproduce these proofs, not rely on source labels or review conclusions as lemmas. The selected review files are mathematical working evidence and may use original notation; PROOF_PREMISES.md supplies the adopted naming and scope.

## What was and was not run during publication

Packaging operations only: UTF-8 reading, source line selection, JSON generation/parsing, SHA-256 computation, payload manifest verification, and a disclosure scan. No numerical integration, physical form evaluation, matrix spectral experiment, checker replay, coefficient search, or new research calculation was run. No research code is distributed or required by this package.

The original archives, complete broader-domain proofs, historical numerical engines, masked source M, and unavailable original first-overlap source are not distributed. Their broader results are not reproducible from this package and are not adopted premises. The later scalar reconstruction is explicitly labeled.
