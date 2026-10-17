# Escaping Sequences under Theta-Source Orthogonality Constraints

Research manuscript, 17 October 2026.

**Jongmin Choi**  
Independent Researcher, Seoul, Korea  
Email: 24ping@naver.com  
ORCID: [0009-0008-7448-514X](https://orcid.org/0009-0008-7448-514X)

**RH_PROOF=NOT-OBTAINED.** The critical sign remains open. This is a repository research manuscript, not a claim of journal acceptance, external peer review, or bibliographical priority.

## Files and supporting artifacts

- [English PDF](theta_source_escape.pdf).
- [Single self-contained TeX](theta_source_escape.tex), with an inline bibliography and no external authoring assets.
- [Classical sources and proof dependencies](SOURCE_AND_DEPENDENCY_AUDIT.md).
- [Korean result and scope summary](RESULTS_KO.md).
- [Document review](DOCUMENT_REVIEW.md) and [source clarifications](REVISION_SOURCE_CLARIFICATIONS.md).
- [Machine-readable scope](PUBLICATION_STATUS.json).
- [Build receipt](checks/build-receipt.json), [structural checks](checks/document-validation.json), and [public artifact readback](checks/artifact-readback.json).

The proof notes, source audit, assumptions, exact counterexample scope, saved algebra checks, and reproduction instructions are fixed in [artifact commit 2447014b009ed432b353d6a3817294df59ff712e](https://github.com/serabing-hash/theta-weighted-certificate/commit/2447014b009ed432b353d6a3817294df59ff712e). This public snapshot was read back without authentication and all 14 files matched the local bytes before the manuscript reference was inserted.

## Result and limits

For the exact infinite theta source and symmetric half jump measure, the paper constructs real smooth unit vectors in the minimum form domain satisfying every orthogonality condition from the known source-generated space N. Their energy approaches 1/2 with error at most C m^3 exp(-sqrt(m)), and their mass on every fixed bounded interval tends to zero. The transformed energy tends to zero for each fixed admissible two-shift envelope.

This obstructs a positive uniform margin above 1/2 and the specified fixed-center coercivity estimates. It does not determine the critical sign. The paper proves N is contained in ker L from the stated classical inputs; it neither proves nor assumes equality. It makes no operator Weyl-sequence, essential-spectrum, RH, global mode-completeness, or novelty claim.

## Reproduce the document

Copy only `theta_source_escape.tex` to a clean working directory and run:

```sh
pdflatex -interaction=nonstopmode -halt-on-error -no-shell-escape theta_source_escape.tex
pdflatex -interaction=nonstopmode -halt-on-error -no-shell-escape theta_source_escape.tex
```

The bibliography is inline: no BibTeX/Biber, research notes, external figures, or data files are required. Use a further pass if the engine requests a reference rerun. Standard TeX Live supplies the preamble's packages, including Latin Modern, AMS packages, geometry, microtype, xcolor, xurl, and hyperref.

For three-pass isolated compilation, document checks, text extraction, and page renders, run:

```sh
python3 build_document.py
```

This additionally requires Python 3, PyMuPDF (`fitz`), and Pillow. The script uses no network operation and disables TeX shell escape. It records source/PDF hashes, checks references, page bounds, the stated author fields, and the fixed artifact link. It does not verify analytic proofs or remote publication. Rendered pages and verbose build logs are local build products; the compact validation reports are included here. Different TeX versions may produce different PDF bytes.

## Exact algebra records

`checks/check_exact_algebra.py` and `checks/algebra_output.json` are unchanged copies of the research package's exact integer-coefficient checks and saved output. `checks/algebra-provenance.json` records their hashes. The two zero polynomial remainders concern the complex edge identity and the square underlying Young's inequality only. They do not verify the explicit formula, positivity, domain limits, zero counting, or numerical error enclosures. The publication step did not rerun these mathematical checks or perform new mathematical calculations.

For optional independent reproduction of those two checks and artifact integrity:

```sh
python3 checks/check_exact_algebra.py
sha256sum -c MANIFEST.sha256
```

No theta values, zero locations, physical integrals, FFTs, Gram matrices, or eigenvalues were computed for this manuscript. The height exp(m^3) is an analytic existence device, not a zero-computation result.

## Assumptions and review scope

The classical inputs are the Jacobi transformation and completed-zeta normalization, the compact-smooth multiplicative explicit formula, the unconditional strip and zero-counting asymptotic with multiplicities, and the divided-difference simplex formula. Their precise references and application conditions are in the source audit. No earlier paper by the author is cited in the manuscript body or bibliography.

The paper supplies the connecting cutoff, closability, minimum-domain, source-cancellation, and envelope arguments. Its explicit polarized zero sum follows the conjugate-linear-first convention. The second closability proof uses the identity on the core and bounded lower-order terms before any extension to the minimum domain.

The envelope branch requires positive weights, safe shifts, the stated strict exponential inequality, and no common real zero of the two shifts. Suitable parameters are proved to exist, but no numerical shift pair is certified. All asymptotic constants and initial indices are uncalibrated. Internal analytic checking and document checks do not replace independent mathematical review or a comprehensive prior-literature survey.

Original new material follows the repository's [CC BY-NC 4.0 license](../../LICENSE). Classical sources retain their respective rights.
