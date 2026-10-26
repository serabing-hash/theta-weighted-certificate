# Safe-baseline repair: fixed full-matrix certificate

## Result
The one authorized production run completed 58/58 fresh baseline point evaluations and the 551-dimensional strict-positive trial restriction passed verification.

- Total certified Loewner error: **0.010231573894279825**.
- Verified projected-center lower bound: **0.039958390743909389**.
- Verified positive-subspace margin after error: **0.029726816849427171 > 0**.
- Trial columns independently verified linearly independent: True.
- Center SHA256: `112286c53eb5476866a0eee3a84dfc03cd8688c03032b97824f230d84d02476f`.

This closes the identified old-baseline arithmetic premise without assuming historical NumPy power correctness. The new baseline uses explicit hh*hh*hh/6; the saved 104-point explicit-multiplication patch gives the same 130-panel composite functional. New scaled G congruence is computed from certified Gmid/Grad. Old Hmid/Fmid, old H point/BLAS/symmetry errors and old coefficient-radius repair are excluded. No old computation was rerun or altered.

The helper remains conditional on its input Loewner premise; the surrounding integration ledger supplies that premise. Within the stated MPFR interval and classical binary64 dot/FMA arithmetic model, the fixed sufficient 552-coordinate matrix has a strictly positive codimension-one restriction, hence a positive second ordered eigenvalue. D is an invertible dyadic congruence, so its floating eigenvalue magnitudes are not physical-operator eigenvalues. This is fixed R=1, epsilon=1/8 and the frozen candidate/original moment constraints; it is not the full RH parameter-family proof. RH_PROOF remains NOT_OBTAINED.

## Provenance and runtime scope
All 24 input fingerprints remained unchanged. All seven production runtime snapshots matched the frozen 1538-file inventory, including actual point-worker and actual pipeline entry/exit. The inventory binds Python executable, NumPy/SciPy source and shared objects, actual loaded BLAS, MPFR/GMP, libc/libm, and listed standard-library extensions. FE_TONEAREST and single-thread OpenBLAS were checked by the arithmetic code. Hashes are provenance evidence, not an independent proof of every machine/compiler/kernel floating-point behavior; the explicit arithmetic model remains an assumption of the certificate.

The older `runtime_static_readback.json` records the preliminary 1535-file import-only inventory before actual-process hooks were added. It is preserved as preparation history and is not used by the production certificate. `RUNTIME_EXPECTED.json` and every production snapshot use the final 1538-file inventory. No numerical fixture or Max run was part of this v4 production run.

## Resource receipt
Exit 0, wall 223.417881s, CPU 223.276354s, observed live-tree RSS peak 257835008 bytes. One launch, zero retries. Aggregate observation thresholds and per-process kernel limits are distinguished in RUN_CONTRACT.md.

## Audit path
Read REPAIR_PROOF.md, RUN_CONTRACT.md, HSAFE_LEDGER.json, error_ledger.json, output.json/inertia/inertia_ledger.json, runtime snapshots and guard_receipt.json. PRELAUNCH_SHA256SUMS binds frozen source and runtime inventory. Final SHA256SUMS binds outputs. The independent terminal-chain audit is saved separately when available.
