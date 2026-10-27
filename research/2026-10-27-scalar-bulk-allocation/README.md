# A scalar bulk allocation cannot control both negative spectral regions

Jongmin Choi, Independent Researcher, Seoul, Korea  
ORCID: https://orcid.org/0009-0008-7448-514X  
27 October 2026. Preprint version 1.0.

## Results

This manuscript gives two obstructions for the complete prime-power multiplier and phase-defined bulk observation specified in its definitions.

1. For every fixed nonzero real even compactly supported smooth test, assigning the central allowance `18432 log(log N)/(pi log N)` times the bulk observation leaves a residual that tends to negative infinity. The actual central cost is smaller than the allowance by a divergent amount.
2. No nonnegative scalar sequence, independent of the test, can simultaneously satisfy the stated central and outer estimates for all such tests with bounded weighted-norm errors. The proof uses a fixed nonnegative even bump and its second derivative. It does not require the scalar sequence to be at most one.

The full form is exactly constant for each compact test once the prime cutoff exceeds the exponential of its support diameter. A positive bulk observation nevertheless grows at least as fast as a positive test-dependent constant times the square root of the cutoff. These facts, and the differing central costs of the two tests, give the contradiction.

The proof uses a fixed positive smooth weight only to make the error norm finite on compact tests. No numerical theta evaluation or special normalization of that weight is needed.

## Scope and limitations

The obstruction concerns allocating a test-independent scalar multiple of this bulk observation while discarding the unused central allowance. It does not invalidate a valid central absorption estimate by itself. It excludes neither input-dependent allocation, frequency-local allocation, nor a direct signed estimate.

The exact refund formula is an algebraic identity, not a new upper or lower bound. For arbitrary nonnegative scalars it does not guarantee that a remaining budget is nonnegative. The manuscript retains the exact signed refund and does not assert a nonnegative remainder for scalars above one.

No full-form positivity theorem, proof or disproof of the Riemann hypothesis, historical priority, journal acceptance, or human peer review is claimed. Noncompact ground-state extensions and a separate signed main-phase cancellation argument are not part of this manuscript.

## Files

- `scalar_bulk_allocation.pdf`: typeset manuscript.
- `scalar_bulk_allocation.tex`: complete editable LaTeX source, including its bibliography.
- `build.sh`: local three-pass PDF build, with shell escape disabled.
- `reproducibility/exact_checks.py`: source-free finite integer, rational, and polynomial checks.
- `reproducibility/exact_checks.json`: deterministic output of those checks.
- `LICENSE`: unchanged existing CC BY-NC 4.0 license.
- `SHA256SUMS`: content-file checksums, excluding the manifest itself.
- `scalar_bulk_allocation_source_v1_0.zip`: clean manuscript and source package, including the inner manifest.
- `RELEASE_SHA256SUMS`: outer checksums, including the archive and inner manifest; kept outside the archive.

The archive excludes build caches, rendered page images, raw conversations, private research notes, account records, and operational records.

## Reproduction

A standard TeX Live or MiKTeX installation with the packages listed in the source is sufficient. Python 3's standard library is sufficient for the exact checks. From the unpacked directory:

```sh
sha256sum -c SHA256SUMS
python3 reproducibility/exact_checks.py > /tmp/scalar-allocation-checks.json
cmp /tmp/scalar-allocation-checks.json reproducibility/exact_checks.json
sh build.sh
```

In the release directory, `sha256sum -c RELEASE_SHA256SUMS` also checks the archive. Verify the supplied artifacts before rebuilding: the fixed metadata date does not guarantee byte-identical PDFs across different TeX distributions, fonts, or build paths.

The 22 successful assertions check only the finite arithmetic and formal polynomial identities described in their output. They do not certify the analytic proof, evaluate a theta function, enumerate primes, verify the prime number theorem numerically, perform quadrature, run spectral numerics, approximate an operator norm, read source files, access a network, or use an external dataset.

## External mathematical input

The sole cited arithmetic input is Daniel R. Johnston and Andrew Yang, *Some explicit estimates for the error term in the prime number theorem*, arXiv:2204.01980v2, Theorem 1.1, printed page 2:
https://arxiv.org/pdf/2204.01980v2

The manuscript supplies the partial-summation transfer, phase geometry, fixed-test estimates, and contradiction. Its conclusions require only sufficiently large integer cutoffs; it does not advertise an optimized explicit threshold. The cited unconditional theorem incorporates finite-height computational ingredients, which this package accepts through the theorem and does not independently regenerate.

## Status and license

The designated release directory is `research/2026-10-27-scalar-bulk-allocation/` in the repository:
https://github.com/serabing-hash/theta-weighted-certificate/tree/main/research/2026-10-27-scalar-bulk-allocation

This package is a preprint version, not a claim of journal acceptance or human peer review. Repository availability is established by the release itself, not by the presence of this destination link. The author's original manuscript and author-owned companion artifacts retain the existing Creative Commons Attribution-NonCommercial 4.0 International license. Third-party rights and licenses are unchanged. See `LICENSE`.
