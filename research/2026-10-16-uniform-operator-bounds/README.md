# Uniform Source-Tail and Response Operator Bounds at B = 3/4

Research completed 2026-10-15 UTC; publication collection dated 2026-10-16. This archive contains analytical theorems for the displayed compact-interval source, their proofs, complete remainder definitions, and small exact-algebra checks. It contains no newly evaluated all-low16 tail matrix or Schur sign.

## Result and scope

1. For every input in L=span(e₀,e₂,…,e₃₀), the source tails converge uniformly on its physical L² unit ball. An exact 16×16 tail Gram formula and complete kernel/pole remainder reduce an all-coefficient numerical bound to a finite certificate that has not yet been computed.
2. For each s>0 at fixed B, the displayed source H^s_even→L² is compact. A quantitative H² endpoint-jet estimate retains the nonzero endpoint-profile tails. Unrestricted L² boundedness fails; the logarithmic graph norm gives boundedness but not uniform L² tails.
3. The full response admits a simultaneous Hermitian residual certificate, preserving the full pole, filtered forcing, operator-domain trials, cross terms, and the physical coordinate metric. The sharp response bound 1/(a+c) requires H_X≥A₀+cI and 0<c≤a; an inverse norm bound alone is insufficient.
4. An actual interior shift jump rules out uniform full-source O(M^(-s)) tails for s>1 on the low16 or H² unit balls. No sharp two-sided M^(-1/2) theorem is adopted.

The fixed-vector h_A certificate from the preceding archive is not an operator norm. No 16×16 numerical matrix sign, positivity of the original whole-line operator, or RH conclusion is established. Original source binding, high/shell transfer, weighted realization, and a genuine form-core/global argument remain separate assumptions or obligations.

## Contents

- ACCEPTED_RESULTS.md: compact adopted theorem ledger
- proofs/UNIFORM_SOURCE_PROOFS.md: complete low16, compactness, H² and response-algebra proofs
- proofs/RESPONSE_CERTIFICATE.md: corrected full error contract, full-pole filter, metric and domain conditions
- proofs/RATE_OBSTRUCTION.md: elementary proven s>1 rate obstruction
- sources/KERNEL_REMAINDER.md: exact k96 recurrence and complete kernel/pole remainder proof
- sources/REMAINDER_CONSTANTS.json: exact scalar values copied from the preceding published certificate
- SCOPE_AND_DEPENDENCIES.md: public immutable dependencies and original-operator obligations
- checks/check_exact_identities.py and checks/expected_output.json: tiny independent exact-rational checks; no source moments or full numerical certificate execution
- PROVENANCE.json: scientific selection identities
- MANIFEST.sha256: SHA-256 of every archive file except the manifest itself

Proof text and the ledger are curated scientific documents. Raw review transcripts, private session URLs, account metadata, and optional unproved asymptotic refinements are excluded. Superseded claims of impossible isotropic budgets or a necessary nonzero trial are not adopted.

## Reproduce the checks

From this directory with Python 3 and sha256sum:

```sh
sha256sum -c MANIFEST.sha256
python3 checks/check_exact_identities.py
```

The script uses only the Python standard library and exact Fraction arithmetic. It checks structural normalization, degree bounds, kernel Taylor coefficients and complete rational remainders, a finite response counterexample, a residual-identity fixture, and physical-metric/Loewner algebra. It does not prove every analytical theorem, evaluate source integrals, produce the actual 16×16 Gram matrix, rerun the earlier certificate, or certify the Schur target.

All analytic constants left as suprema or finite-profile tails remain unevaluated. The next finite gate is one simultaneous Hermitian inequality Q_lower−ε_out N−C_upper≥λN with λ>0 and a fully matched source/domain/error contract.
