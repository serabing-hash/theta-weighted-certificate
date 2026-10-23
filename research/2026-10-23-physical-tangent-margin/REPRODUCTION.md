# Reconstructing the analytic result

This package is reproducible as a written analytic argument. There is no scientific executable, numerical dataset, software dependency lockfile or prior-run output to restore.

## Reading order

1. Read PROOF.md sections 1-2 for the exact source, physical form, Fourier convention, convergence and scope. The theta identity is cited to NIST DLMF and applied explicitly.
2. Check the elementary series and full-source bounds in section 3 and the appendix.
3. Reconstruct the positive residual and source moments in sections 4-5 by polynomial multiplication, factorial integration, Jensen and Taylor remainder signs.
4. Check sections 6-8, keeping the finite-start Gamma error, Fourier normalization and near-zero Gamma region separate.
5. Check sections 9-10, retaining the signed n=2 negative part and all prime powers, and distinguishing carrier losses from midpoint losses.
6. Verify the exact rational subtraction in section 11 and retain the stated scope limitations.
7. Read VERIFICATION.md for the precise extent of the completed analytic checks and the separate packaging checks.

The proof supplies every source-specific constant used by the conclusion. Standard classical analysis is identified in the proof; it is not replaced by an undocumented software output. Optional independent arithmetic checks by a reader would be new checks, not a previously executed verifier distributed here.

## Optional byte-integrity check

From this directory on a system providing sha256sum, run:

    sha256sum -c MANIFEST.sha256

The manifest covers README.md, PROOF.md, VERIFICATION.md and REPRODUCTION.md, but not itself. Successful hash checking establishes file identity only, not mathematical correctness.

A paper citing this support should use the actual immutable artifact commit after publication. A moving branch is not an immutable identity. This package does not claim that a proposed path or a publication commit already exists.
