# Closed physical realizations and a compact resolvent pencil for a theta prime Gamma energy

**Jongmin Choi**  
Independent Researcher, Seoul, Korea  
ORCID iD: [0009-0008-7448-514X](https://orcid.org/0009-0008-7448-514X)

**Version:** v0.1 analytical preprint draft  
**Date:** November 1, 2026

## Contents

- `theta_confining_pencil_v01.pdf`: the 12-page manuscript.
- `theta_confining_pencil_v01.tex`: complete editable LaTeX source, including the bibliography.
- `build.sh`: document-only PDF build command.
- `README.md`: scope and build instructions.

## Mathematical scope

The paper proves a complete weighted prime-power form estimate and constructs a closed self-adjoint physical pencil with compact resolvent for each positive parameter. The compactness proof combines spatial confinement from the theta weight with logarithmic Fourier coercivity of the Gamma form.

The relation to the original positive energy is **conditional on the compact physical bridge hypothesis (H)**, stated explicitly in the abstract and the main theorem. The bridge is assumed, not reproved in this manuscript. Under this assumption, the paper proves exact form-domain identification, correspondence with actual operator-domain subthreshold eigenstates, a negative-index formula, and fixed-distance spectral finiteness. It also distinguishes the weighted mean from ordinary physical L2 orthogonality and proves the theta kernel's operator-domain obstruction.

The proposed strict positivity of the second pencil eigenvalue for every parameter in (0, 1/2) is **not proved**. The paper does not establish the global variance half bound or the Riemann hypothesis. It does not assert an exact essential threshold or an infinite-multiplicity half-eigenspace. No claim of historical priority, peer review, or formal proof-assistant verification is made.

The manuscript is analytical. It does not report numerical eigenvalues, numerical research, prime enumeration, or numerical sign certification. Its finite prime heads are proof devices with an explicitly retained infinite tail.

## Rebuild the PDF

Use a standard, complete LaTeX installation with `pdflatex` and the packages `amsmath`, `amssymb`, `amsthm`, `fontenc`, `lmodern`, `geometry`, `microtype`, and `hyperref`. No BibTeX run, network access, shell escape, external data, or computational research script is required.

From the directory containing the source:

```sh
sh build.sh
```

The script runs pdfLaTeX twice, puts intermediate files in `build/`, and copies the completed PDF to `theta_confining_pencil_v01.pdf`. It builds the document only. The archived PDF was compiled with pdfTeX 1.40.26 and visually checked on every page. A rebuild with another TeX distribution may differ in layout or metadata; byte-for-byte reproducibility is not claimed.

## References

The bibliography contains the [NIST DLMF Jacobi transformation](https://dlmf.nist.gov/20.7.E32) and [Kato's treatment of closed forms and associated operators](https://doi.org/10.1007/978-3-642-66282-9). The manuscript includes the full proofs of its stated domain, prime-tail, compactness, and correspondence results, with their dependence on (H) made explicit.
