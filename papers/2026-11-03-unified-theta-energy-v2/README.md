# Theta Prime Gamma Energy and its Spectral Structure — Version 2

Jongmin Choi · Independent Researcher, Seoul, Korea  
[ORCID 0009-0008-7448-514X](https://orcid.org/0009-0008-7448-514X)

## Paper

- [PDF — 244 pages](unified_theta_energy.pdf)
- [Single self-contained LaTeX source](unified_theta_energy.tex)
- [Verification scope](VERIFICATION_SUMMARY.md)
- [Included and omitted data](DATA_AVAILABILITY.md)
- [Portable exact-arithmetic reproduction](reproducibility/README.md)
- [a2048 source-enclosure generator, exact frozen input, and regeneration guide](source_regeneration_a2048/README.md)
- [Four-zero finite certificate and conditional sparse scalar checks](four_zero_certificate/README.md)
- [Five-zero finite certificate, exact Schur checks, and its own derivative bound](five_zero_certificate/README.md)
- [Six-zero fixed-split extension and exact checks](six_zero_certificate/README.md)
- [Conditional graph-to-Schur transfer and complete-high attachment checks](graph_schur_transfer_checks/README.md)
- [Uniform response brackets and operator-error checks](uniform_response_checks/README.md)
- [Synthetic Gamma-sector algebra checks](gamma_sector_synthetic_checks/README.md)
- [Eleven-logarithmic and growing sparse-band scalar checks](eleven_log_band_checks/README.md)

This integrated manuscript brings together the analytic theta/Gamma/prime energy
framework, domain and spectral results, response and Schur tools, conditional
finite-stage numerical applications, and sparse-window and fixed-lattice positivity results.
Every theorem retains its specified norm, domain, geometry and premises.

**The global half inequality and the Riemann hypothesis remain unproved.** A
restricted zero-jet or finite-stage conclusion is not positivity on arbitrary
unions or the full zero family. Numerical enclosure premises, complete-domain
arguments and saved-matrix arithmetic are distinct verification layers.

The historical Decimal integer-power implementation has a demonstrated
outward-enclosure defect. Same-code output equality does not repair it. The
public source package separates a byte-preserved **historical/** profile from
the **corrected/** regeneration route and its actual validation status. Exact
stored-matrix signs remain valid; a corrected a2048 run does not automatically
repair the distinct historical a1024 application.

The PDF and TeX are the two manuscript files prepared for the author's own Zenodo
upload. This GitHub publication does not submit to Zenodo and does not assign a
DOI. The manuscript source contains its bibliography and mathematical appendices;
no external source, figure, bibliography file or research data are needed to
compile it.

The separate four-zero packet records an Arb/Acb finite certificate
`q0[v] >= ||v||_H^2/32` on its stated four-dimensional global theta-carrier space.
Its sparse attachment is conditional on the explicit estimates with complexity
budget `C0=8` and `U=exp(2^512)`; it does not cover all complete unit-window
zero-jet spaces under the separate coarse coefficient `168`.

The separately checked five-zero packet gives `q0[v] >= ||v||_H^2/25`, a
shifted coordinate Schur complement greater than `1/2000`, and a normalized
quotient-direction reserve greater than `27/1000` on its stated five-dimensional
space. Its derivative bound is `K5^2 < 75`, not the four-zero bound. Neither
Schur reserve is an eigenvalue increment to add to `1/25`, and the four-zero
sparse conditions do not transfer automatically to this larger space.

The [graph-to-Schur packet](graph_schur_transfer_checks/README.md) gives a
separate conditional transfer at Gamma cutoff `R=2^18`. Under the stated
closed-sector and operator-row admission hypotheses, it proves `S_R >= 1/35`
on the five-dimensional projected space `L5=P_R V5`, and `q0 >= 1/36` on
`L5` plus the entire complementary Gamma high form domain. It does not certify
the other low directions of `P_R K` or a cofinal family. Its finite matrix and
scalar checks do not themselves compute the spectral projection/high inverse
or prove sector membership.

The [six-zero fixed-split packet](six_zero_certificate/README.md) extends the
admitted projected source at the same cutoff. It certifies a raw six-function
margin `1/40`, a Schur margin `1/50` on `L6=P_R V6`, and margin `1/51` after
attaching the entire complementary Gamma high form domain. The sixth shifted
coefficient Schur reserve exceeds `1/5000`. Its fresh sixth row retains the
certified five-function input blocks. The closed-sector, restricted form-domain,
operator-row and inherited enclosure hypotheses remain explicit. No full-low or
infinite-family exhaustion claim follows from this finite result.

The [uniform-response packet](uniform_response_checks/README.md) checks exact
response constants and noncommuting block identities, with 2,103 independent
rational checks and separate elementary ball-arithmetic audits. The linear and
cubic response errors are below `9.33e-11` and `1.76e-18`; the combined cubic
response and same-low-space prime error is below `5.37e-18`. These are operator
error bounds, not an actual theta sign or a computed low matrix. Finite-degree
response still uses complete high operators and exact spectral projections.
The fixed raw graph-debit obstruction does not invalidate the finite five- and
six-direction certificates, and a fixed prime cutoff does not yield a vanishing
tail for an exhaustion argument.

## Build the document

```sh
sh build.sh
```

The script performs three `pdflatex` passes with shell escape disabled. It uses
only installed TeX resources, not network access or scientific production.
Packages include `fontenc`, `lmodern`, `amsmath`, `amssymb`, `amsthm`, `mathtools`,
`mathrsfs`, `booktabs`, `longtable`, `enumitem`, `geometry`, `microtype`, and
`hyperref`. A minimally configured Debian installation can use the script's local
format/font-map fallback.

Rebuilding can change PDF metadata and byte hashes. Check the supplied release
before running a build or writing replay outputs:

```sh
sha256sum -c SHA256SUMS.txt
```

## Reproduce the exact finite arithmetic

Run Python checkers without `-O` or `-OO`; several preserved source programs
use assertions to enforce their mathematical checks. Verify release hashes
before running programs that write result files, preferably in a working copy.

The [reproducibility packet](reproducibility/README.md) includes lossless curated
G/K/T matrices, the needed F scalar, integer sign witnesses, original-input hash
provenance, portable standard-library Python checkers, and deterministic expected
outputs. It checks a1024 ordinary/generalized gates, a2048 exact/conservative
gates, the analytic a2048 rational composition and listed sparse-window constants.
An additional exact check retains the original a2048 gate margin and witness to
verify the manuscript's conditional improved coefficient `0.499640243163`
(rounded down); it is not a new source replay or an unconditional half bound.

The compact packet does **not** regenerate theta values, physical Gram inclusions,
quadrature, source moments or tail estimates. The separately supplied
[source-regeneration package](source_regeneration_a2048/README.md) provides the
historical generator provenance, a separately identified corrected profile,
exact frozen input, and portable regeneration/checkpoint adapters. The actual
source-regeneration work is stated in [VERIFICATION_SUMMARY.md](VERIFICATION_SUMMARY.md).
The original full input-file hashes identify provenance; the compressed packet
contains a lossless extraction of necessary mathematical fields, not every
original production file. No private archive or communication log is distributed.
The [data-availability map](DATA_AVAILABILITY.md) distinguishes the public
a1024/a2048 finite certificates and a2048 source-generation path from historical
a288/a512 raw archives and other large artifacts that are not bundled here.

## Version preservation

This version is additive. The [previous unified manuscript at commit
663354fe1a649cd92b04525a7cceb28e813c0293](https://github.com/serabing-hash/theta-weighted-certificate/tree/663354fe1a649cd92b04525a7cceb28e813c0293/papers/2026-11-02-unified-theta-energy)
remains unchanged. Historical research material retains the verification scope
under which it was issued; later arithmetic checks do not retroactively turn
conditional statements into unconditional ones.

`PUBLICATION_FILES.txt` enumerates the public files. `SHA256SUMS.txt` hashes all
listed files except itself. Hash equality establishes byte identity, not a proof
of the analytic or numerical-inclusion premises.

## Existing license

Copyright 2026 Jongmin Choi. The repository's existing Creative Commons
Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) terms apply to the
author's original contributions. See the unchanged [LICENSE.txt](LICENSE.txt)
and the [license terms](https://creativecommons.org/licenses/by-nc/4.0/).
Third-party references retain their respective rights. No new license is created
by this release.
