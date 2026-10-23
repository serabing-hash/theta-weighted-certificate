# Reproduction and verification

## Byte identity

From this directory in a checkout of the immutable publication commit, run:

    sha256sum -c MANIFEST.sha256

The manifest covers every other file in this package and does not hash itself. It does not certify mathematical correctness. The repository license and earlier support files are unchanged. To verify the older proof dependency, retrieve its exact immutable URL in REFERENCES.md and compare its SHA-256 there.

## Analytic reproduction

No mathematical program is required or supplied. Reproduce the proof in this order:

1. PHYSICAL_PROOF §§2–5: check full-source normalization, Fourier measure du/(2π), complete envelopes and residual moments. Do not replace the theta sum by its first term in an upper bound.
2. §§6–9: retain all exterior Gamma losses and all prime powers; check positive unsigned midpoint/tail bounds, actual c>0 and the derivative coefficient 5/4.
3. §§10–12: verify the three affine entry rows, simultaneous lifted source constraints, reduction to the lower Z boundary and all six rational vertices. Use actual 0<c<c_bar before squaring; entrywise bounds alone are not a Loewner-order bound.
4. ORIGINAL_DOMAIN: follow the compact-test explicit formula, source radical identity, closability, cutoff convergence and polarized projection before using the rank-one pole update. The pole square can vanish.
5. NEARBY_FREQUENCIES: verify weighted norm continuity including the complete prime series, explicit A_j, smooth divided differences, δ and the gap² coordinate conversion.
6. CENTERED_RADIUS: cancel the odd displacement before estimating; check K_c, Δ, the >100 comparison only on the overlapping domain, and gap²/256000. Do not infer a larger outward endpoint band.
7. SIGNED_CROSS_FREQUENCY: check both signed channels and their factors, the all-prime remainder and determinant cancellation. Do not replace the shifted Gamma multiplier by the same-frequency one or invoke Cauchy–Schwarz for an unproved positive form.

Classical analytic inputs are listed in REFERENCES.md. Review labels are not mathematical premises. The radii are explicit analytic expressions, not numerical spacing certificates.
