# License: CC BY-NC 4.0

© 2026 Jongmin Choi. Except where otherwise indicated, the author's original paper and accompanying author-owned research artifacts are licensed under [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/). See [LICENSE](LICENSE) for the official legal text. Third-party material remains subject to its original terms; no third-party rights are relicensed here.

# Theta-weighted certificate

Research and reproducibility materials for **A Fixed One Thirty Second Threshold for a Theta Weighted Quadratic Form**, Jongmin Choi, 7 October 2026.

## Result and verification boundary

Under the paper's explicit analytic-source and numerical-inclusion premises, the fixed-delta certificate establishes a positive lower bound for `L + I/32` for the specified minimum closed even weighted operator. This excludes spectrum at or below `-1/32` for that operator. It does not establish `L >= 0`, remove all negative spectrum, identify a physical Weil operator, or prove or disprove the Riemann hypothesis.

The independently implemented **exact saved-data arithmetic replay** was documented as passing during paper preparation. The analytic-source, action, and physical Gram/numerical-inclusion premises have not been independently regenerated. Hash agreement establishes byte identity, not mathematical correctness. The same-family delta-1/64 FLOAT diagnostic is a failed diagnostic, not an impossibility theorem.

## Publication-only revised paper

- [PDF](https://github.com/serabing-hash/theta-weighted-certificate/releases/download/v2026.10.07-delta32/theta_delta32_certificate.pdf)
- [LaTeX source](https://github.com/serabing-hash/theta-weighted-certificate/releases/download/v2026.10.07-delta32/theta_delta32_certificate.tex)
- [Revised-paper SHA-256 checksums](https://github.com/serabing-hash/theta-weighted-certificate/releases/download/v2026.10.07-delta32/REVISED_PAPER.sha256)

This 35-page revision adds the repository, versioned release, and CC BY-NC 4.0 notice on page 35. Pages 1–34 and all mathematical content are unchanged. The original manuscript remains inside the unchanged Part 1 ZIP. No new delta64 diagnosis is incorporated into this paper.

## Reproduction distribution

The original 7 October 2026 distribution is preserved in three unchanged ZIP parts. Download all three parts and extract them into the **same directory**, preserving the shared top-level folder `theta_delta32_release_20261007`:

1. [THETA_DELTA32_PAPER_PART1_2026-10-07.zip](https://github.com/serabing-hash/theta-weighted-certificate/releases/download/v2026.10.07-delta32/THETA_DELTA32_PAPER_PART1_2026-10-07.zip)
2. [THETA_DELTA32_INPUTS_AB_PART2_2026-10-07.zip](https://github.com/serabing-hash/theta-weighted-certificate/releases/download/v2026.10.07-delta32/THETA_DELTA32_INPUTS_AB_PART2_2026-10-07.zip)
3. [THETA_DELTA32_INPUTS_CDE_PART3_2026-10-07.zip](https://github.com/serabing-hash/theta-weighted-certificate/releases/download/v2026.10.07-delta32/THETA_DELTA32_INPUTS_CDE_PART3_2026-10-07.zip)

The three original ZIPs and their [SHA-256 checksums](https://github.com/serabing-hash/theta-weighted-certificate/releases/download/v2026.10.07-delta32/ASSETS.sha256) are published in [release v2026.10.07-delta32](https://github.com/serabing-hash/theta-weighted-certificate/releases/tag/v2026.10.07-delta32). GitHub's generated source-code download does not contain the full certificate data; download all three release assets above. The published asset SHA-256 digests match the original files. The release tag identifies the documentation commit; use the asset checksums to verify the research data.

Together the three parts contain 205 files, including all 158 original manifest-bound files, the original manifest, and five byte-preserved input ZIPs. The original archives include a historical manuscript and README that predate the GitHub publication and license notice. They are retained as provenance, not silently revised. The publication-only revised paper is separately linked above and has its own checksums.

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

## Separate delta64 failure diagnosis

The [7 October 2026 delta64 diagnosis release](https://github.com/serabing-hash/theta-weighted-certificate/releases/tag/v2026.10.07-delta64-diagnosis) is a separate follow-on analysis, not part of the original delta32 paper or reproduction ZIPs.

- [Complete diagnosis ZIP](https://github.com/serabing-hash/theta-weighted-certificate/releases/download/v2026.10.07-delta64-diagnosis/delta64_failure_diagnosis_20261007.zip)
- [Report](https://github.com/serabing-hash/theta-weighted-certificate/releases/download/v2026.10.07-delta64-diagnosis/REPORT.md)
- [Diagnosis SHA-256 checksums](https://github.com/serabing-hash/theta-weighted-certificate/releases/download/v2026.10.07-delta64-diagnosis/DELTA64_DIAGNOSIS.sha256)

The follow-on report certifies positivity on the existing trial span at the delta64 shifted threshold and an obstruction within the fixed residual estimator. The actual off-trial spectral sign remains open. These restricted results do not prove full-operator positivity, exclude all negative spectrum, or prove/disprove RH. The original delta32 theorem and its premises remain unchanged.

## Residual block admission preservation

The [8 October 2026 admission preservation release](https://github.com/serabing-hash/theta-weighted-certificate/releases/tag/v2026.10.08-residual-admission) archives the complete available admission, independent audit, diagnosis, and inherited source data. **Physical numerical production remains HOLD.** Domain, four-mode rank obstruction, and nonredundancy passes remain conditional on inherited inclusion premises.

- [Preservation archive](https://github.com/serabing-hash/theta-weighted-certificate/releases/download/v2026.10.08-residual-admission/RESIDUAL_BLOCK_ADMISSION_ARCHIVE_2026-10-08.zip)
- [Preservation report and replay limits](https://github.com/serabing-hash/theta-weighted-certificate/releases/download/v2026.10.08-residual-admission/RESIDUAL_BLOCK_ADMISSION_PRESERVATION_REPORT_2026-10-08.txt)
- [Admission SHA-256 checksums](https://github.com/serabing-hash/theta-weighted-certificate/releases/download/v2026.10.08-residual-admission/RESIDUAL_ADMISSION.sha256)

The archive preserves 263 original files unchanged. It is a source/data snapshot, not a hermetic runtime or new end-to-end numerical audit. Frozen replay scripts retain absolute paths and external dependencies. No new physical evaluation was performed.

## Author

Jongmin Choi · Independent Researcher, Seoul, Korea · [ORCID 0009-0008-7448-514X](https://orcid.org/0009-0008-7448-514X)

## License scope and provenance

The CC BY-NC 4.0 notice applies to the author's original contributions within this repository and the accompanying research distribution, including their preserved historical versions, to the extent the author holds the relevant rights. Retain attribution, the license notice, applicable warranty disclaimers, and indications of modifications as required by that license. External dependencies and third-party materials keep their own licenses and notices. The official license text is available from [Creative Commons](https://creativecommons.org/licenses/by-nc/4.0/legalcode.txt).
