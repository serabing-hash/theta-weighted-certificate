# Historical producer: arithmetic qualification

**This is not the primary regeneration profile.** Use the separately identified
[corrected profile](../README.md). Original producer files and recorded execution
reports are preserved here byte-for-byte for provenance, not silently repaired.

The original `src/interval_bounds.py` has SHA-256
`0c11bbcf4cb7e92bd1e57853f3d364001d3ce2d237e3223c5db0e95d5bd5531c`.
Its integer-power implementation calls Decimal endpoint powers under directed
rounding. At precision 70 on the audited libmpdec 4.0.0 runtime, the upper endpoint
of `(1 + 10^-40)^2` is below the exact value by `10^-80`. A negative odd-power
lower-endpoint counterexample also exists. Thus its general outward-enclosure
contract is false. This is not a claim that an actual production operand failed,
or that the final analytic inequality is false.

The historical code's printed `CERT`, matching output hashes, and original
31-test success do **not** resolve that arithmetic obligation. Preserved JSON
reports retain their original statements and scopes; a `PASS` for byte equality
or execution is not retroactively relabeled as validated source enclosure.
Likewise, the preserved numerical-contract notes describe the intended
mathematical contract, not proof that this primitive implements every operation
correctly. The historical model and Gamma comparisons remain reproduction facts.

The corrected profile replaces integer power by sign-aware, directed
multiplication with a monotonicity proof and exact-rational tests. That primitive
repair alone is not a complete source replay: see
[GENERATION_VALIDATION.md](../GENERATION_VALIDATION.md) for the dependent
recomputation and final sign status. It must not be made to match historical data
by replacing expected hashes or suppressing failed checks.

The a1024 archived source uses the same power method; its prior same-code replay
is historical evidence, not a corrected a1024 enclosure certificate. No actual
failing a1024 production operand is asserted. Exact stored-matrix integer and
rational checks remain valid, with operator consequences conditional on their
source-enclosure and full-domain premises.

The original shared candidate and identity records are one directory above in
`inputs/`. Large historical runtime arrays, private execution logs and upstream
third-party source archives are not redistributed here. The global half bound
and the Riemann hypothesis remain unproved.
