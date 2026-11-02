# Theta Prime Gamma Energy and its Spectral Structure

Jongmin Choi, Independent Researcher, Seoul, Korea  
ORCID: https://orcid.org/0009-0008-7448-514X

## Manuscript

- `unified_theta_energy.tex`: the complete, self-contained manuscript source.
- `unified_theta_energy.pdf`: the corresponding 121-page manuscript.

These are the only two files intended for the author's own Zenodo upload. No Zenodo submission is performed by this release. All mathematical appendices and the bibliography are inline. No external TeX input, bibliography database, figure asset, certificate data or research executable is needed to compile the manuscript.

The manuscript integrates the common analytic foundations, domain and spectral structure, comparison bounds, Schur reductions, obstruction results, weighted spectral synthesis, exact zero-jet cores and finite-complexity results.

## Build

With a standard TeX installation:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error unified_theta_energy.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error unified_theta_energy.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error unified_theta_energy.tex
```

Packages: `fontenc`, `lmodern`, `amsmath`, `amssymb`, `amsthm`, `mathtools`, `mathrsfs`, `booktabs`, `longtable`, `enumitem`, `geometry`, `microtype`, and `hyperref`.

Alternatively, run `sh build.sh`. This script performs document compilation only. For minimally configured Debian TeX trees, it can generate a local format and font map from installed standard TeX resources. It does not fetch data, execute research code, or access the network. Rebuilding may change PDF metadata; the supplied PDF's exact byte identity is recorded in `SHA256SUMS.txt`.

## Mathematical trust classes

- **Analytic results:** the wholly analytic results do not require numerical prime or zero enumeration or a response computation.
- **Local-sign input:** the coefficient `49307/100000` uses the stated whole-local-minimum-domain sign input at radius `4/5`.
- **Additional response contracts:** the coefficient `2861149/5760000` additionally assumes the displayed complete-operator residual and centered-response enclosure contracts. It is not a local-sign-only conclusion.
- **Unproved endpoint:** the global coefficient `1/2` and the Riemann hypothesis remain unproved.

Every Gamma shift, prime power, exact mean constraint and relevant minimum domain is retained. Ongoing global 64-response computation is outside this release and contributes no certified result.

## Public supporting materials

- [Immutable public baseline](https://github.com/serabing-hash/theta-weighted-certificate/tree/f539e52fe08379c0639ff94a812ec73a40d29a0e)
- [Radius-four-fifths local certificate package](https://github.com/serabing-hash/theta-weighted-certificate/tree/f539e52fe08379c0639ff94a812ec73a40d29a0e/research/2026-10-28-four-fifths-local-certificate)

The response archive identified by SHA-256 in the manuscript is not public at this pinned baseline. No response certification or public reproducibility of the response-dependent input is claimed. A cryptographic identity is not a proof of an enclosure.

See `VERIFICATION_SUMMARY.md` for the document and byte-identity checks, `PUBLICATION_FILES.txt` for the eight-file release manifest, and `SHA256SUMS.txt` for checksums.

## License

Copyright 2026 Jongmin Choi. Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0): https://creativecommons.org/licenses/by-nc/4.0/ . External references retain their respective rights. See the unchanged `LICENSE.txt`.
