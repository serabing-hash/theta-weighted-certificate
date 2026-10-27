# A directional prime mean bound in anchored gamma energy

Jongmin Choi, Independent Researcher, Seoul, Korea  
ORCID: https://orcid.org/0009-0008-7448-514X  
27 October 2026 — preprint version 1.0

## Claim and boundary

The manuscript proves `M(f) <= (3/25) E_Gamma(f)` on the specified minimum even homogeneous gamma-energy completion, using anchored representatives. The full theta source and every prime-power label are retained. The numerator cutoff at 64 is only an intermediate decomposition: both denominators are complete throughout, and all discarded labels and output points are restored with analytic error bounds.

This is a component inequality, not a proof of the Riemann hypothesis, a sign theorem for a full signed operator, or an eigenstate exclusion theorem. No optimality or novelty claim is made. This preprint makes no claim of human peer review, journal acceptance, or priority.

## Files

- `directional_mean.pdf`: readable preprint.
- `directional_mean.tex`: main editable mathematical source.
- `dependencies.tex`: included proofs of the source identities and complete row estimates. It must remain beside the main source.
- `build.sh`: standard PDF build command.
- `reproducibility/check_entry_constants.py`: exact scalar and polynomial checks for the entry estimates.
- `reproducibility/check_branch_constants.py`: exact branch constants, core-mass margins, and final coefficient comparisons.
- `reproducibility/check_tail_constants.py`: exact output-tail and label-tail scalar bounds.
- `reproducibility/*_constants.json`: saved output of these scripts.
- `LICENSE`: the repository's existing CC BY-NC 4.0 license, copied without modification.
- `SHA256SUMS`: file integrity checks for the manuscript and accompanying source files.
- `directional_mean_source_v1_0.zip`: clean distributable source and PDF package (listed separately from its own internal manifest).

The bibliography contains external sources only. The body gives the analytic derivations rather than referring to unpublished source notes or internal review labels.

## Reproduce the rational checks

A standard Python 3 installation is sufficient; no third-party packages are required.

```sh
python3 reproducibility/check_entry_constants.py
python3 reproducibility/check_branch_constants.py
python3 reproducibility/check_tail_constants.py
```

The checks use only integers, `fractions.Fraction`, finite polynomial operations, and rational Taylor or geometric bounds. They do not evaluate the theta kernel, enumerate primes, run quadrature, calculate a spectrum, or replay an interval-source computation. Passing them verifies the saved rational arithmetic, **not** the complete analytic proof. The infinite-series estimates, source identities, changes of variables, anchoring, folds, and minimum-completion argument must be read and checked in the manuscript.

The tail script also retains a secondary `(Y,N)=(5/4,32)` arithmetic check from the underlying tail calculation. That secondary pair is not needed for the main theorem. The branch script retains both the weaker `49/400` combination and the disjoint-output `3/25` improvement; the manuscript states the latter.

## Build the PDF

Install a standard TeX Live or MiKTeX distribution providing `pdflatex`, the AMS packages, Latin Modern, `mathtools`, `geometry`, `booktabs`, `microtype`, `hyperref`, and `xurl`. Then run:

```sh
./build.sh
```

No shell escape, network access, or external data file is needed by the TeX source. A rebuilt PDF can have different metadata and binary bytes while having the same mathematical content. The supplied PDF was compiled and every page visually inspected.

## Data availability

The PDF, editable TeX source, and source-free exact-rational checks accompany this preprint.

Repository: https://github.com/serabing-hash/theta-weighted-certificate  
Version directory: `research/2026-10-27-directional-prime-mean-bound/`

No external numerical dataset is needed. The package contains no numerical spectral certificate.

## License

The author's original manuscript and accompanying author-owned research artifacts are licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0), as specified by the repository's existing `LICENSE`. The license text is copied unchanged from the repository root. Third-party material remains subject to its respective rights and licenses. No additional rights to third-party works are granted here.

## Assistance disclosure

Artificial intelligence assistance was used for drafting, mathematical exposition checks, and document preparation. Separate AI-assisted checks are not human peer review. The theorem concerns only the directional mean form in its stated domain.
