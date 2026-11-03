# Six zero fixed split reproducibility packet

This packet checks the sixth actual theta zero source direction at the fixed Gamma spectral cutoff R=2^18. Under the stated closed-sector, dense restricted form-domain, operator-row and inherited enclosing-input assumptions, the certified conclusions are:

- q0 >= 1/40 in the actual raw six-function reciprocal-theta norm.
- S >= 1/50 on the six-dimensional projected source L6=P_R V6.
- q0 >= 1/51 after attaching the entire complementary Gamma high form domain.
- The sixth shifted coefficient Schur reserve is >1/5000.

These are not positivity on all low directions, an all-order uniform sign theorem, a completed exhaustion proof, a global one-half inequality or RH. The complete high inverse and Gamma spectral projections are used analytically and are not numerically constructed.

## Reproduce the incremental enclosure

Use Python-FLINT 0.9.0. The checked runtime used FLINT 3.6.0. In a writable copy of this directory run:

```
python3 certify_six_zeros.py
python3 certify_matrix_error.py
python3 verify_fixed_split.py
python3 check_exact.py
python3 independent_fraction_audit.py
```

The first two scripts freshly evaluate the sixth G/H/prime/Gamma/D2 row and column, retaining only the two frozen first-five input enclosures. They do not read the sixth-function quadrature checkpoint as an input. The first-five blocks were independently regenerated and checked in the preceding five-function certificate; FROZEN_INPUT_BINDING.json records their exact mathematical-field comparison and hashes. The validity of those enclosures remains an inherited analytic input, not a consequence of a hash.

The first script writes timing metadata. Consequently runtime-dependent CERTIFICATE hashes and dependent hashes in later files change on replay; the mathematical fields, quadrature checkpoint and rational ledger are the comparison targets. Regenerate all downstream files in order after a fresh source run.

For live serialization checks, use:

```
python3 audit_live_serialization.py
python3 check_exact.py
python3 independent_fraction_audit.py
```

The live check regenerates all stages, verifies 288 saved matrix entries enclose the corresponding live Arb balls, verifies all 144 exported rational intervals, and checks six higher-precision zero enclosures. These are supplementary checks, not an independent implementation of rigorous integration or zero isolation.

## Portable exact checks

With ordinary Python and no third-party packages, the two commands below check the supplied certificate state:

```
python3 check_exact.py
python3 independent_fraction_audit.py
```

The first uses the author's rational LDL recurrence. The second independently reconstructs all 144 affine interval entries from the saved input balls and computes exact Gaussian determinants. It checks the same 24 pivot floors, the actual raw Gram innovation, failure of the stronger sufficient 1/25 comparison, and the final scalar constants. No floating eigenvalue is a sign premise. Decimals in the reports are display-only.

Both checkers use a symmetric midpoint matrix minus the maximum interval-radius row sum times the identity. The derivative matrix debit is 3/10^10; each of the other three debits is 3/10^18. The matrix_graph sixth exact determinant ratio is approximately 0.0002276653909153501 and is strictly greater than 1/5000.

## Mathematical interpretation

The complete row majorant is Hrow=(153/8)a^2 H+306 b^2 D2+1458 G. It preserves physical and derivative Gram correlations. Its coefficients do not grow with dimension, but this does not imply a uniform D2/G or Schur bound for arbitrary source size.

Saved D2 and Gamma-error arrays are entrywise interval enclosures. Their names do not authorize treating a matrix of entrywise upper endpoints as a Loewner upper bound. They are propagated by interval arithmetic into the final sufficient matrices, whose full interval families pass the rational sign test. The current six-direction interpolation debit is rebuilt, including its six-function boundary trace.

The source's final strict coupling comparison is intended for nonzero ell. For all ell write <= and then state strictness for nonzero ell; at zero both sides are zero. This typographic qualification does not change any certificate.

The fixed-split exhaustion theorem is valid conditional on nested admitted source spaces, complete lower matrices F_m>=-epsilon_m G_m with epsilon_m->0, and Hilbert density of their projected union in P_R K. It uses one fixed raw vector across all later stages before taking a density limit. No uniform lower bound for the projection map is required. Those infinite-family conditions are not established here. Singular leading blocks require coupling in their range, equivalently annihilation of their kernel, before a pseudoinverse Schur criterion applies.

## Verification boundary

REPLAY_SUMMARY.json records the clean 160-bit and incremental 256-bit replays. The latter retains the certified 160-bit five-function blocks and yields the identical rational ledger. All seven source PDF pages were visually inspected. This packet is a bounded computational and analytic audit, not proof-assistant formalization or independent human peer review.

The original four numerical scripts and numerical outputs are preserved. Supplementary audit scripts and reports are clearly named. SHA256SUMS.txt covers every other file in this packet; replay in a copy because scripts intentionally regenerate outputs.
