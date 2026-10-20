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

## Residual action design contract

The [8 October 2026 residual action contract release](https://github.com/serabing-hash/theta-weighted-certificate/releases/tag/v2026.10.08-residual-action-contract) is **DESIGN / PILOT-ADMISSION ONLY**. Both independent reviews admit V2 implementation and exactly one guarded zero-based j = 2 pilot after its required preflight. All-four-column production remains HOLD. **No physical pilot was performed in preparing this contract.**

The separate release preserves the unchanged 101-file contract core, the report, the finalized Korean Work prompt, and SHA-256 checksums. Its small core uses the prior delta32 source archives as explicitly hash-bound external dependencies. The admission does not certify measured arithmetic gates, production timing, delta64 positivity, or RH. The original paper and earlier releases are unchanged.

## Author

Jongmin Choi · Independent Researcher, Seoul, Korea · [ORCID 0009-0008-7448-514X](https://orcid.org/0009-0008-7448-514X)

## License scope and provenance

The CC BY-NC 4.0 notice applies to the author's original contributions within this repository and the accompanying research distribution, including their preserved historical versions, to the extent the author holds the relevant rights. Retain attribution, the license notice, applicable warranty disclaimers, and indications of modifications as required by that license. External dependencies and third-party materials keep their own licenses and notices. The official license text is available from [Creative Commons](https://creativecommons.org/licenses/by-nc/4.0/legalcode.txt).

## 18 October 2026: a conditional fixed-threshold improvement

The new [nine-page PDF](papers/2026-10-18-fixed-threshold-shift/fixed_threshold_shift.pdf)
and [single TEX with embedded bibliography](papers/2026-10-18-fixed-threshold-shift/fixed_threshold_shift.tex)
record one fixed-coefficient improvement for the same minimum theta operator,
all 372 observations and corrected 68 trials. The lower edge changes from
approximately -0.0156184544151869108 to -0.0156055131540838210, a small strict
improvement of approximately 0.0000129412611030897828. Both edges remain negative.

The [commit-pinned source and evidence](https://github.com/serabing-hash/theta-weighted-certificate/tree/dba8f9c497305eeb44fc4590604874480f5d256d/research/2026-10-18-fixed-threshold-shift)
include exact rational results, all 63 input roles, unchanged source, the
full checker output, actual execution/resource evidence, explicit A1–A4/N1–N4
premises, reproduction instructions, fixed limits and separate failure history.
The analytic and physical inclusions were not regenerated. The single
20.839672121-second scientific run is distinct from preparation and publication
time. Paper preparation did not rerun the producer or checker.

This result establishes neither L >= 0 nor RH and makes no literature-priority
claim. RH_PROOF=NOT-OBTAINED. The separate unpublished trace-paper package is
not included in this publication.

Download the [two-file paper ZIP](downloads/THETA_FIXED_THRESHOLD_SHIFT_PAPER_20261018.zip), containing exactly the public PDF and single TEX. ZIP SHA-256: `d4b9f05414618ec8939aafa86752d82cb69cb2e4456e1172c41b73b11bea4a7f`.

## 18 October 2026: a conditional coefficient-only obstruction

The [nine-page paper](papers/2026-10-18-coefficient-obstruction/coefficient_obstruction.pdf) and [single TEX with bibliography](papers/2026-10-18-coefficient-obstruction/coefficient_obstruction.tex) record a failed midpoint128 production and two separately successful exact diagnostics. For the same witness and fixed delta=h=1/128, tau=1/100, observation/trial/action maps, P_up, norm/error bounds, primitive inputs and majorant construction, every coefficient matrix C-prime fails the selected direction. Both nominal-center and physical-majorant exclusions retain the stated premises; the nominal lower bound uses the m_h−rho bridge because direct g0 is nonpositive.

The failed production remains resource_acceptance=false. The later direction and coefficient checks have separate accepted resource/termination evidence. This is not a negative direction of L or a general impossibility at delta1/128. No source premises were re-proved and no new scientific calculation was run for publication. The tau/loss follow-up is unevaluated. RH_PROOF=NOT-OBTAINED.

[Commit-pinned evidence](https://github.com/serabing-hash/theta-weighted-certificate/tree/f61c7af23c7e4027cc3cb768faa40273f1146ffd/research/2026-10-18-coefficient-obstruction) · [Artifact ZIP](downloads/THETA_COEFFICIENT_OBSTRUCTION_ARTIFACTS_20261018.zip) · [PDF/TEX ZIP](downloads/THETA_COEFFICIENT_OBSTRUCTION_PAPER_20261018.zip). The paper ZIP contains exactly two files; SHA256: `6391e99ce8ebd4857d4e561b3c80e5a6949dca85ebd9a08f1cd6660f33e61697`.

## Shared action errors and rank-one inverse responses — 20 October 2026

The [conditional inverse-response research package](research/2026-10-20-inverse-response/) preserves two exact historical reports and checker sources, ten commit-pinned public inputs, and a statically reviewed public arithmetic adapter. Its [reproduction instructions](research/2026-10-20-inverse-response/REPRODUCTION.md) separate byte verification from optional reader execution. Publication preparation did not execute a scientific replay. The fixed shared-error majorant is excluded; the saved rank-one result is inconclusive. `RH_PROOF=NOT-OBTAINED`.

The companion [16-page paper and self-contained TeX](papers/2026-10-20-inverse-response/) give the proofs, fixed artifact commit, report field map, and explicit reproduction limits. A [Korean summary](papers/2026-10-20-inverse-response/RESULT_KO.md) separates proved statements, saved outcomes and unexecuted work.

The [public reproduction ZIP and checksum distribution](releases/2026-10-20-inverse-response/) is also stored in Git, with separate exact byte counts and SHA256 values. It contains the paper and safe replay packet; the ten public inputs are restored from their fixed URLs.
