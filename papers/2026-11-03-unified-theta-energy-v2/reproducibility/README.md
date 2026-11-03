# Portable exact-arithmetic checks

These files provide **saved-data arithmetic replay**, not a new evaluation of the
theta source, fresh physical Gram inclusions, or a proof of the Riemann hypothesis.
The finite-matrix checks retain the manuscript's analytic, domain, and numerical
inclusion premises. Read the manuscript for the hypotheses of each conclusion.
The historical Decimal integer-power primitive has a known outward-enclosure
defect; matching source outputs does not resolve it. These exact finite checks
remain valid as stored-data arithmetic. Any operator consequence additionally
needs valid source enclosures, with corrected execution assessed separately.

## Run

Python 3.9 or newer, standard library only; no network, NumPy, SymPy or external
data are required. Do not run Python with `-O`, which disables assertions.

```sh
python3 test_replay_contract.py
python3 replay_saved_gates.py > saved_gates.json
python3 replay_a2048_analytic.py > a2048_analytic.json
python3 replay_a2048_retained_margin.py > a2048_retained_margin.json
python3 replay_sparse_constants.py > sparse_constants.json
python3 low_sparse_scalar_checks.py > low_sparse_scalars.json
diff -u EXPECTED_SAVED_GATES.json saved_gates.json
diff -u EXPECTED_A2048_ANALYTIC.json a2048_analytic.json
diff -u EXPECTED_A2048_RETAINED_MARGIN.json a2048_retained_margin.json
diff -u EXPECTED_SPARSE_CONSTANTS.json sparse_constants.json
diff -u EXPECTED_LOW_SPARSE_SCALARS.json low_sparse_scalars.json
```

The helper tests include negative/singular examples that must be rejected.
`EXTRACTION_REPORT.json` records the original-field comparison and
`EXECUTION_REPORT.json` records the measured portable replay.

The five expected outputs are deterministic: they contain no timestamps, timing,
absolute paths, hardware identifiers or floating-point premises. Optional
`--parameter 1024` or `--parameter 2048` restricts the matrix replay. The largest
step consists of dense 256-by-256 integer matrix products; allow roughly a minute
on an ordinary current CPU, with machine-dependent timing.

## What is checked

- Both inputs reconstruct the exact G, K, T matrices from their upper triangles;
  their lower triangles are restored by symmetry. Positive denominators and all
  canonical matrix hashes are checked.
- For a = 1/1024, all 65,536 entries of the sufficient matrix M are reconstructed
  from G, K, T and the scalar lower bound for F. An exact integer congruence proves
  M − I/2000 positive definite. Every one of 256 diagonal-dominance margins is
  strictly positive.
- In the same a1024 data, the exact Gershgorin upper bound U < 5944 I is checked,
  followed by the scalar-slack coefficient. A separate exact integer congruence
  checks M − (3/20000) U positive definite and the generalized coefficient
  `1381250815636970598719595/2767005669802701449752576`.
- For a = 1/2048, all 65,536 entries are reconstructed separately for the exact
  penalty and the conservative penalty 26240. Each sufficient matrix satisfies
  M − I/2000 > 0 by a distinct integer congruence with 256 positive margins.
- The analytic a2048 script rechecks the rational constant chain, the residual
  penalty, composition identities and strict remaining half-bound deficit. It
  does not itself check a response gate.
- The retained-margin a2048 script uses the unchanged original exact-gate
  witness to check `M - (1/2000) I - beta U > 0`, with
  `beta = 10508819/40000000000`, all 256 strict integer congruence margins and
  `U < 4060 I`. It applies the existing conditional extraction with
  `alpha = 6099134007/32480000000000`, yielding the exact coefficient
  `2415896663121887366359985794094352519/4835272370827926282795053961934979072`,
  strictly above the rounded-down value `0.499640243163` and below the unchanged
  fixed-complement method ceiling. It verifies this fixed beta; it performs no
  search, new witness fit or source generation. All enclosure/full-domain
  premises and the distinction between the actual response Gram and its upper
  bound U remain necessary.
- The sparse-window script checks the listed finite rational inequalities and
  optimized localization constants. It does not prove the analytic estimates or
  the external theorems cited in the manuscript.

- The low-to-sparse script checks five scalar identities in the restricted
  response estimate. It does not check a theta/Gram matrix, packet estimate,
  residual row or positivity margin. The theorem's global theta-exponential-
  polynomial low space is not identified with the sharp-cut a2048 source space;
  no positive low-space q0 margin is established by this script.

## Lossless mathematical-field extraction

The original G/K/T/F files also contain production metadata and additional
fields not needed for this finite arithmetic replay. The curated gzip inputs
include only the exact matrix/scalar fields and integer witnesses needed here.
No numerical precision is rounded or reduced.

`inputs/a1024_PROVENANCE.json` and `inputs/a2048_PROVENANCE.json` record the SHA-256
of each original source file and witness, and both the compressed and decompressed
curated input. Their original-file hashes identify provenance; they do not claim
that the complete original files are included in this compact packet.

The M matrices are not redundantly stored. The checker reconstructs them from
G/K/T/F in their original denominator and compares every numerator through a
canonical SHA-256 digest. Canonical matrix serialization is UTF-8 JSON with sorted
keys and compact separators, holding `common_denominator` and
`matrix_numerators` as decimal strings. This distinguishes byte-level source
identity from exact mathematical-field identity.

These portable adapters modify file loading, report layout and input packing from
the original research checkers. The original research inputs are not modified.
The a2048 matrix adapter follows the independently implemented stored-gate audit;
the analytic and sparse-window adapters retain their exact rational formulas.

## Why the integer certificate suffices

For each saved integer witness Q, the checker computes H = Qᵀ A Q exactly. H is
symmetric with positive diagonal entries strictly larger than the sum of the
absolute off-diagonal entries in each row, hence H is positive definite. This
forces Q to be nonsingular; congruence then gives A > 0. A floating-point routine
may propose a witness during historical production, but floating-point signs are
not assumptions in this replay.

## Limits

A passed finite-matrix replay does not regenerate source functions, moments,
quadrature, tail bounds or physical inclusion intervals, and does not replace
complete-domain arguments. The separate [source-regeneration package](../source_regeneration_a2048/README.md)
supplies the original generator and frozen input. Its actual execution status is
documented in the release verification summary, with historical and corrected
profiles explicitly separated. Correcting a2048 does not by itself revalidate
the distinct a1024 historical run. Cryptographic identity is not mathematical proof.
Neither the global half bound nor RH is established.

The repository's existing CC BY-NC 4.0 terms apply to the author's original
contributions; no new license is introduced by this packet.
