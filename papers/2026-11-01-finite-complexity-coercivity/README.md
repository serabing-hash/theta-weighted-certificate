# Uniform Logarithmic Gamma Coercivity at Fixed Exponential Complexity

**Author:** Jongmin Choi, Independent Researcher, Seoul, Korea  
**ORCID:** https://orcid.org/0009-0008-7448-514X  
**Manuscript date:** 1 November 2026  
**License:** Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).

## Result and scope

For a positive C¹ weight W such that W and W′ decrease faster than every exponential, the manuscript proves:

1. Uniform comparison of the weighted L²(dx/W) and ordinary L² norms of WP when the exponential polynomial P has fixed total confluent complexity and frequencies in a fixed imaginary strip.
2. Uniform escape from every fixed low Fourier band as every real carrier height tends in absolute value to infinity.
3. Uniform divergence to +∞ of the exact Gamma-minus-bounded-self-adjoint-perturbation Rayleigh quotient, in both function norms.

The proofs include colliding complex frequencies, polynomial jets, arbitrary coefficients, and arbitrary real separations. The classical theta weight is verified directly. Its full prime-power correction is constructed as a norm-absolutely convergent weighted operator series, without assuming boundedness of a bare prime row on ordinary L². Finite cosine-jet corollaries, a fixed-width carrier estimate, two auxiliary complexity counterexamples, and an entire two-frequency kernel are included.

The manuscript **does not prove** positivity for all actual zeta-zero jets, a complexity-independent height threshold, an effective numerical threshold, a raw coefficient-space eigenvalue bound, a global centered half inequality, or the Riemann hypothesis. The auxiliary examples are not actual Xi-zero jets and establish no negative value of the theta form. No physical energy bridge, Guinand zero-sum formula, or previous paper by the author is imported.

## Files

- `finite_complexity_coercivity.tex` — complete editable LaTeX source, with embedded bibliography.
- `finite_complexity_coercivity.pdf` — compiled manuscript.
- `build.sh` — document-only compilation and all-page render commands.
- `LICENSE.txt` — copyright and CC BY-NC 4.0 notice.
- `QA_REPORT.md` — build, mathematical scope, and all-page visual quality review.
- `MANIFEST.json` — metadata and byte/hash identities for the canonical payload.
- `PAYLOAD_SHA256SUMS.txt` — SHA-256 identities of the payload and manifest; included in the source archive.
- `finite_complexity_coercivity_source.zip` — portable source/PDF package.
- `SHA256SUMS.txt` — final outer checksums, including the archive; distributed beside it, not embedded in itself.

Local `qa/`, `.texcache/`, compilation auxiliaries, and working drafts are not part of the portable release archive. No private predecessor manuscript is needed to build or understand the paper.

## Build

Requirements: a standard TeX Live installation with pdfLaTeX, Latin Modern, AMS math/theorem/fonts, mathtools, geometry, microtype, hyperref, and enumitem; Poppler's `pdfinfo`, `pdftotext`, and `pdftoppm`; and Bash.

```sh
chmod +x build.sh
./build.sh
```

The script performs two pdfLaTeX passes with shell escape disabled and a fixed document timestamp, then extracts text and renders every PDF page at 110 dpi into `qa/pages/`. It includes a local-cache fallback for this environment's read-only Debian TeX tree when generated format caches are unavailable. The fallback writes only inside the extracted package directory. No installation, network, prime enumeration, zero enumeration, matrix solve, numerical research, or numerical checker is invoked.

Check the packaged bytes before rebuilding:

```sh
sha256sum -c PAYLOAD_SHA256SUMS.txt
```

Rebuilding with another TeX distribution can change PDF bytes or pagination. The checksums identify the delivered artifacts; they are not formal verification of the mathematical claims. A successful build alone does not establish visual quality or proof correctness.

## References and research status

The only bibliography entry is the NIST Digital Library of Mathematical Functions, with the digamma integral (5.9.16) and Jacobi transformation (20.7.32). Their use and normalization are explained in the text; the finite-complexity estimates are proved in full. The manuscript makes no historical-priority claim and is not represented as peer reviewed, accepted, or proof-assistant verified.

License: https://creativecommons.org/licenses/by-nc/4.0/  
Legal code: https://creativecommons.org/licenses/by-nc/4.0/legalcode
