# V5: selected research evidence, 12 November 2026

Companion artifacts for the V5 working paper by Jongmin Choi. **This is not a proof of RH. The sign of mu_2 remains uncertified.**

## Contents and scope

The archive supplies 158 scientific files: selected reports, exact stored scalar outputs, scoped audit/checker sources, and available pinned coefficient/input data. The selection covers the full-P off-diagonal bound (1.716409), the same-trial form bound (6.825), the covariance component and conditional energy/sign gates. These bounds must not be confused with the unresolved absolute joint-energy bound or endpoint/RH conclusions. Post-snapshot91 diagnostic work is excluded.

The archive is split solely for reliable transfer. Every part and the reassembled ZIP have exact SHA256 hashes in ARCHIVE.json. No old repository files were replaced.

## Obtain and verify

Download this directory at the paper's pinned commit (or clone the repository), then:

```sh
python3 assemble.py
mkdir extracted
python3 -m zipfile -e v5_selected_research.zip extracted
cd extracted
python3 verify_bundle.py
```

Python 3 standard library suffices for assembly and public-byte verification. A successful checksum check establishes byte integrity only, not mathematical correctness.

## Important reproducibility limitations

This is a **selected evidence release, not a closed reconstruction of the entire historical computation**. REPRODUCIBILITY_LIMITS.json inventories unavailable or mismatching historical pins. Original packet manifests and checkers refer to predecessor files not all included here; do not expect every original producer/checker to run from this directory alone. A pin listed as unavailable means it was not resolved at the checked canonical location, not that no backup exists elsewhere.

Original numerical producers may require python-flint (Arb), NumPy, SciPy, mpmath and historical/native inputs. Exact package-version and full dependency closure are not established by this release. No numerical producer was rerun as part of publication; the publication checks were file hashes and ZIP integrity. Historical audit reports describe their own narrower checks and are not a complete independent audit of V4/V5.

Conditional numerical implications remain conditional. In particular an asserted sufficient energy threshold is not an attained energy certificate. Finite-dimensional diagnostics are not whole-space certifications. The mu_2 interval containing zero, the whole joint-energy bound, endpoint control, universal positivity and RH remain unresolved.

Operational backup receipts, access registries, private coordination and credentials are excluded. Scientific files supplied here retain their exact source bytes; the top-level MANIFEST_SHA256.json defines this public selection.
