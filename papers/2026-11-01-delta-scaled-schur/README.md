# A delta-scaled Schur framework and an explicit analytic variance bound for a theta prime–Gamma energy

**Jongmin Choi**  
Independent Researcher, Seoul, Korea  
ORCID iD: [0009-0008-7448-514X](https://orcid.org/0009-0008-7448-514X)

**Version:** Research manuscript v1.0  
**Date:** November 1, 2026  
**Status:** Research manuscript; not a peer-reviewed or accepted publication.

## Contents

- `theta_delta_scaled_schur_v1.pdf`: the complete typeset manuscript.
- `theta_delta_scaled_schur_v1.tex`: the complete editable LaTeX source, including the bibliography.
- `build.sh`: document-only PDF build script.
- `README.md`: scope and build instructions.
- `LICENSE_NOTICE.md`: notice preserving the existing CC BY-NC 4.0 terms.
- `theta_delta_scaled_schur_v1_source.zip`: clean source package containing the TEX, build script, README, and license notice.
- `MANIFEST.json` and `SHA256SUMS`: release inventory and file-integrity information.

## Mathematical scope

The manuscript proves the full-domain bound

`E[f] >= c_log2 Var_mu(f)`,

where

`c_log2 = (4/85)(63/128 - 7238 exp(-12)) > 8939/425000 > 1/48`.

Its proof retains all prime powers, the complete Gamma difference form, the original global mean, and the maximal integral domain. The theta normalization, classical explicit-formula source identity, ground-state bridge, domain correspondence, and compact-resolvent ordinary-L2 pencil are proved in the text. Only external classical sources appear in the bibliography.

At `delta = 23/48`, the actual pencil has negative index one and operator nullity zero, with centered weighted margin at least `509/2550000`. The exact open inertia interval furnished by this bound is `1/2 - c_log2 < delta < 1/2`; the exponential coefficient is not replaced by its weaker rational rounding when stating this endpoint. No optimality of this coefficient is asserted.

For every positive parameter and every relative tolerance between zero and one, explicit finite interior moments produce a positive infinite complement on the correct delta scale. Ordinary-L2 density of the derivative radical gives finite interpolation; the manuscript separately proves that the radical is not dense in the weighted centered space. The exact scaled Schur formula, Neumann response error, weighted residual bound, and signed continuation identity retain the interpolation cost.

The reference iterations use exact infinite-dimensional positive solves. They are analytic constructions, not evaluated finite matrices or local numerical certificates. The fixed-interval finite Schur sign follows from the global energy inequality. The finite sign at smaller parameters, uniform interpolation conditioning, and a certified parameter sequence tending to zero remain unresolved. The global variance half bound and the Riemann hypothesis are not proved.

No numerical integration, prime enumeration, eigenvalue computation, local computer certificate, or numerical reference solve is used. Document compilation and rendering do not constitute mathematical certification. No proof-assistant-verification or historical-priority claim is made.

## Build

Use a standard complete LaTeX installation with `pdflatex` and the packages `fontenc`, `lmodern`, `amsmath`, `amssymb`, `amsthm`, `geometry`, `microtype`, and `hyperref`.

```sh
sh build.sh
```

The script runs pdfLaTeX twice with shell escape disabled, writes intermediates into `build/`, and copies the completed PDF into this directory. It does not download dependencies, read external data, or perform research computations. No BibTeX run is required. A different TeX distribution may produce different metadata or pagination; byte-identical rebuilds are not claimed.

## License

This manuscript preserves the existing **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** terms. It does not change the license. See `LICENSE_NOTICE.md` and the [license text](https://creativecommons.org/licenses/by-nc/4.0/).
