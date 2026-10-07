# License: CC BY-NC 4.0

© 2026 Jongmin Choi. Except where otherwise indicated, the author's original paper and accompanying author-owned research artifacts are licensed under [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/). See [LICENSE](LICENSE) for the official legal text. Third-party material remains subject to its original terms; no third-party rights are relicensed here.

# Theta-weighted certificate

Research and reproducibility materials for **A Fixed One Thirty Second Threshold for a Theta Weighted Quadratic Form**, Jongmin Choi, 7 October 2026.

## Result and verification boundary

Under the paper's explicit analytic-source and numerical-inclusion premises, the fixed-delta certificate establishes a positive lower bound for `L + I/32` for the specified minimum closed even weighted operator. This excludes spectrum at or below `-1/32` for that operator. It does not establish `L >= 0`, remove all negative spectrum, identify a physical Weil operator, or prove or disprove the Riemann hypothesis.

The independently implemented **exact saved-data arithmetic replay** was documented as passing during paper preparation. The analytic-source, action, and physical Gram/numerical-inclusion premises have not been independently regenerated. Hash agreement establishes byte identity, not mathematical correctness. The same-family delta-1/64 FLOAT diagnostic is a failed diagnostic, not an impossibility theorem.

## Reproduction distribution

The original 7 October 2026 distribution is preserved in three unchanged ZIP parts. Download all three parts and extract them into the **same directory**, preserving the shared top-level folder `theta_delta32_release_20261007`:

1. `THETA_DELTA32_PAPER_PART1_2026-10-07.zip`
2. `THETA_DELTA32_INPUTS_AB_PART2_2026-10-07.zip`
3. `THETA_DELTA32_INPUTS_CDE_PART3_2026-10-07.zip`

Publication of these assets is in progress. This repository's source download currently does not contain the full certificate data. Verified download links and checksums will be added when the upload is complete.

Together the three parts contain 205 files, including all 158 original manifest-bound files, the original manifest, and five byte-preserved input ZIPs. The original archives include a historical manuscript and README that predate the GitHub publication and license notice. They are retained as provenance, not silently revised. The repository's later paper revision will be separately identified.

From the clean extracted top-level directory, check identities before replay:

```sh
sha256sum -c MANIFEST.sha256
(cd replay/restored_full && sha256sum -c MANIFEST.sha256)
python3 replay/current_exact/independent_verify.py replay/restored_full
```

The saved-data replay requires Python 3, NumPy, and a POSIX host. It has fixed 120-second wall/CPU and 512-MiB address-space guards. It does not perform new source evaluation, H actions, FFTs, physical integrals, or Gram computations. No fully pinned production environment is asserted.

The verifier writes `replay/current_exact/verdict.json`; timing/environment fields can change its hash. Run manifest checks first and preserve a clean extraction for later byte-identity checks. Do not weaken the verifier to obtain a pass.

Expected historical verdict:

```text
PASS-EXACT-SAVED-DATA-REPLAY-CONDITIONAL-ON-INCLUSION-AND-ANALYTIC-PREMISES
```

## Author

Jongmin Choi · Independent Researcher, Seoul, Korea · [ORCID 0009-0008-7448-514X](https://orcid.org/0009-0008-7448-514X)

## License scope and provenance

The CC BY-NC 4.0 notice applies to the author's original contributions within this repository and the accompanying research distribution, including their preserved historical versions, to the extent the author holds the relevant rights. Retain attribution, the license notice, applicable warranty disclaimers, and indications of modifications as required by that license. External dependencies and third-party materials keep their own licenses and notices. The official license text is available from [Creative Commons](https://creativecommons.org/licenses/by-nc/4.0/legalcode.txt).
