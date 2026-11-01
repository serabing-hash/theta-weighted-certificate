# Closed physical realizations and a compact resolvent pencil for a theta prime Gamma energy

**Jongmin Choi**  
Independent Researcher, Seoul, Korea  
ORCID iD: [0009-0008-7448-514X](https://orcid.org/0009-0008-7448-514X)

**Version:** Manuscript v1.0  
**Date:** November 1, 2026  
**Status:** Research manuscript; not a peer-reviewed or accepted publication.

## Contents

- `theta_confining_pencil_v1.pdf`: complete typeset manuscript.
- `theta_confining_pencil_v1.tex`: complete editable LaTeX source, including the bibliography.
- `build.sh`: document-only PDF build command.
- `README.md`: scope and build instructions.
- `CHANGELOG.md`: substantive changes from the preserved v0.1 draft.

## Mathematical scope

The compact physical bridge, formerly hypothesis (H), is now proved from the classical Guinand explicit formula and the entire theta transform. The manuscript derives all normalization constants, justifies the noncompact theta cutoff on both the zero and prime sides, and retains both endpoints in the ground-state calculation. No zero-location assumption is used.

The bridge extends to an exact bijection of the maximal closed form domains. The paper proves a complete weighted prime-power tail estimate, constructs the closed self-adjoint physical pencil with compact resolvent at every positive parameter, and establishes correspondence with actual operator-domain subthreshold eigenstates and an exact negative-index formula. Even theta derivatives provide infinitely many independent centered operator-domain eigenstates at eigenvalue 1/2, proving that the essential spectral bottom is exactly 1/2. This is not a completeness assertion for that derivative family. The paper also distinguishes the original weighted mean from ordinary physical L2 orthogonality and proves the theta kernel's operator-domain obstruction.

The strict positivity of the second pencil eigenvalue for every parameter in (0, 1/2) is **not proved**. The paper does not exclude subthreshold eigenstates, establish the global variance half bound, or prove the Riemann hypothesis. No historical-priority claim, peer-review claim, or formal proof-assistant verification is made.

This is analytical work. No numerical eigenvalue computation, prime enumeration, numerical research, or numerical sign certification is reported. Finite prime heads are proof devices with their complete infinite remainder retained.

## Rebuild the PDF

Use a standard, complete LaTeX installation with `pdflatex` and the packages `amsmath`, `amssymb`, `amsthm`, `fontenc`, `lmodern`, `geometry`, `microtype`, and `hyperref`. No BibTeX run, network access, shell escape, external data, or research computation is required.

From this directory:

```sh
sh build.sh
```

The script runs pdfLaTeX twice, writes intermediates into `build/`, and copies the completed PDF to `theta_confining_pencil_v1.pdf`. It only builds the document. The supplied PDF uses pdfTeX 1.40.26. Rebuilds on another distribution can differ in metadata or page layout; byte-for-byte reproducibility is not claimed.

## References

The bibliography contains only external classical sources: the NIST DLMF for the Jacobi transformation and digamma integral, Paul Garrett's university lecture notes for the Guinand explicit formula and classical zero-counting bound, and Kato's treatment of closed forms and associated operators. The manuscript includes the normalization, theta-transform, cutoff, core, prime-tail, compactness, and spectral-correspondence proofs used for its own conclusions.

## Version preservation

The v0.1 draft is preserved separately and has not been overwritten. Its conditional bridge statement remains part of the historical version; the current theorem replaces that assumption by a proof, not by a change of terminology.

## License

This version preserves the repository's existing **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license. It does not introduce a new license or change the existing terms. See the repository license notice and the [CC BY-NC 4.0 license](https://creativecommons.org/licenses/by-nc/4.0/).
