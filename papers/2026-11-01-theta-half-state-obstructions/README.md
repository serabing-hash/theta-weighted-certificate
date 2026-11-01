# Theta half eigenstates and obstructions to curvature and local square factorizations

**Jongmin Choi**  
Independent Researcher, Seoul, Korea  
ORCID: [0009-0008-7448-514X](https://orcid.org/0009-0008-7448-514X)

Manuscript v1.0, November 1, 2026. Research manuscript, not peer reviewed or accepted.

## Contents

- `theta_half_state_obstructions_v1.pdf`: complete manuscript.
- `theta_half_state_obstructions_v1.tex`: self-contained editable LaTeX source, including proofs and bibliography.
- `build.sh`: document-only compilation script.
- `theta_half_state_obstructions_v1_source.zip`: source distribution containing the TEX, this README, and the build script.
- `PAPER_MANIFEST.json`: version, scope, and artifact checksums.
- `SHA256SUMS.txt`: checksums of the release files other than the checksum file itself.
- `DOCUMENT_QA.json`: document-build and all-page visual-review record.

The source archive contains no PDF, computational research code, external datasets, TeX cache, build intermediates, or rendered page images.

## Established results

The paper studies the actual self-adjoint operator associated with the full theta prime-Gamma energy. It proves a smooth invariant domain for the complete generator and accounts for both mixed Gamma/prime orders and prime-prime compositions.

For the explicit half-eigenstate `g = kappa''/kappa - 1/4`, the full pointwise curvature quotient tends to `1/4` in both tails. Therefore every pointwise curvature lower bound with constant greater than `1/4` fails, even on real even compact smooth profiles with exact global mean zero. The half-curvature defect of the actual eigenstate has integral zero.

The span of all derivative half-eigenstates is dense in the compact-open smooth topology on even profiles. Special centered compact cutoffs converge to each half-eigenstate in the actual operator graph norm. These facts exclude an exact common nonnegative-square factorization of the integrated half defect by continuous local linear rows, even when the proposed identity is asserted only on the centered compact smooth class. Each row can be an arbitrary compactly supported distribution; supports need not be uniformly bounded. Positive semidefinite finite-path matrices on the actual compatible data image are covered as well. Every lower bound of the same type must have a trivial local remainder.

The integrated defect is strictly positive on some centered compact smooth high-frequency profiles. This is a positive witness showing that the defect is not identically zero, not a negative direction.

Appendices prove the theta normalization, closed integral form and form core, classical explicit-formula source identity, compact and full form-domain bridges, complete weighted prime bound, and actual derivative half-eigenstates. No prior paper by the author is needed as a cited premise.

## Scope limits

The paper does **not** establish:

- a pointwise curvature lower bound at `1/4` or any other positive universal constant;
- weighted Hilbert-space, form-norm, or graph-norm completeness of the half-state family;
- a negative integrated-defect direction or an actual subthreshold eigenstate;
- the integrated half inequality, the global variance half bound, or the Riemann hypothesis.

The obstruction does not exclude genuinely global rows, nonlocal inverses, nonlinear constructions, or signed identities with global cancellation. The classical explicit formula is used without a zero-location assumption. No historical-priority, peer-review, journal-acceptance, or formal proof-assistant-verification claim is made.

No numerical research, eigenvalue calculation, prime enumeration, or numerical sign certificate is reported. Compilation and rendering only produce and check the document.

## Rebuild

Use a complete LaTeX installation with `pdflatex` and the packages `fontenc`, `lmodern`, `amsmath`, `amssymb`, `amsthm`, `geometry`, `microtype`, and `hyperref`.

```sh
sh build.sh
```

The script runs pdfLaTeX three times with shell escape disabled, keeps intermediates in `build/`, and copies the completed PDF to the release filename. It needs no network, BibTeX run, external data, or research computation. The supplied PDF was produced with pdfTeX 1.40.26. Other TeX distributions may differ in metadata or pagination; byte-identical rebuilds are not claimed.

## References

The bibliography contains only external classical sources: NIST DLMF for the Jacobi transformation and digamma integral; Paul Garrett's University of Minnesota notes for the Guinand explicit formula and zero-counting estimate; and Kato for the representation theorem for closed forms. The manuscript includes the specialized proofs needed for its results.

## Version and license

This is a separate manuscript v1.0. Existing manuscripts are preserved and are not overwritten or replaced.

The repository's existing **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license is unchanged. See the existing repository license notice and the [CC BY-NC 4.0 license](https://creativecommons.org/licenses/by-nc/4.0/). This distribution introduces no new license terms.
