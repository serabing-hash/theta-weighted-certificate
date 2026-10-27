# An explicit weighted localization bound for a signed prime-gamma form

Jongmin Choi, Independent Researcher, Seoul, Korea  
ORCID: https://orcid.org/0009-0008-7448-514X  
27 October 2026 — preprint version 1.0

## Statement and boundary

The manuscript proves an explicit localization-defect bound for the complete real even signed prime-gamma form in a Jacobi-theta weighted space. It retains all prime powers, the complete gamma energy, the exact pole, and the full exterior gamma coefficient. For S = exp(2R), R >= 1, the error is at most 9000(1 + log S) S^(-5/2) exp(-pi S/2) times the squared weighted norm. It also gives exact main-phase/pole cancellation and support-matched finite-N formulas.

The remaining localized interior form is signed and infinite-dimensional. No positivity margin, spectral exclusion, proof or disproof of the Riemann hypothesis, historical priority, journal acceptance, or human peer-review claim is made.

## Files

- `signed_localization.pdf`: 11-page preprint.
- `signed_localization.tex`: main editable source.
- `theta_appendix.tex`: self-contained Gaussian-periodization, theta-envelope, and normalization proofs; keep beside the main source.
- `build.sh`: conventional no-shell-escape PDF build.
- `reproducibility/check_constants.py`: source-free exact rational scalar checks.
- `reproducibility/constants.json`: saved check output.
- `LICENSE`: existing CC BY-NC 4.0 license text, preserved unchanged.
- `SHA256SUMS`: inner manifest covering the eight manuscript and supporting content files.
- `signed_localization_source_v1_0.zip`: clean package containing those eight content files and the inner manifest only.
- `RELEASE_SHA256SUMS`: outer manifest covering every content file, the inner manifest and the ZIP; it excludes itself.

The theta dependencies are derived directly in the paper. No external numerical dataset or spectral certificate is required.

## Exact scalar checks

Run `python3 reproducibility/check_constants.py` with Python 3. The script uses only integers, finite rational arithmetic, and positive Taylor sums. It does not evaluate theta or prime sources, enumerate primes, run quadrature, or calculate a spectrum. A successful check establishes only the recorded scalar arithmetic, not the complete analytic proof.

## PDF build

With a standard TeX Live or MiKTeX installation providing `pdflatex`, Latin Modern, AMS packages, `mathtools`, `geometry`, `microtype`, and `hyperref`, run `./build.sh`. No network, shell escape, or external data is required by the document. PDF metadata and binary bytes can differ after rebuilding. The supplied PDF was rendered and all 11 pages were visually inspected; no clipping, overlap, missing glyphs, or reference defects were found.

## Designated release directory

https://github.com/serabing-hash/theta-weighted-certificate/tree/main/research/2026-10-27-signed-cubic-localization

The manuscript source, PDF, appendix, build script, and source-free arithmetic checks are packaged for this release location. No external numerical dataset is required.

## License and assistance

The original manuscript and accompanying author-owned artifacts are licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0), as specified in `LICENSE`. Third-party materials retain their respective rights. Artificial intelligence assistance was used for drafting, exposition checks, and document preparation. Such assistance is not human peer review.
