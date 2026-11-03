# Short extrapolation and growing zero jet bands

Author: Jongmin Choi, Independent Researcher, Seoul, Korea. Contact: 24ping@naver.com. ORCID: https://orcid.org/0009-0008-7448-514X.

This standalone manuscript proves a strip and full-prefix extrapolation inequality, an explicit complete prime-power cap, and a two-sided ordinary-L2 asymptotic on each entire actual zeta zero-jet band of width o(log(T) sqrt(loglog(T))). It also proves positivity for a conservative small fixed multiple of that boundary width and an exact inverse-retaining Schur consequence within a covered union.

The result includes complex roots, every actual multiplicity prefix, arbitrary complex coefficients, the complete theta weight, all prime powers, and the full Gamma integral. It does not establish RH, positivity on arbitrary adjacent coverings, or a uniform reciprocal-theta weighted gap.

The real-frequency elimination method and the classical Takenaka–Malmquist all-pass system are explicitly credited to Zhang's paper and the classical construction. The manuscript proves the required varying-real-part and confluent extension. Earlier work in this research supplied the normalization and carrier comparison; both are rederived here. No prior manuscript by the author appears in the bibliography or is required to use the theorem.

## Files

- `growing_zero_jet_bands.tex`: complete editable manuscript.
- `growing_zero_jet_bands.pdf`: compiled manuscript.
- `build.sh`: document-only, no-network build. It can configure a local pdfTeX format and local font map in minimal Debian TeX installations without modifying the system.
- `reproducibility/check_constants_and_identities.py`: Python-standard-library scalar and identity checks.
- `reproducibility/check_results.json`: recorded checks.
- `reproducibility/PROOF_LEDGER.md`: dependency and verification scope.
- `reproducibility/PRIMARY_SOURCES.md`: sources and exact scope.

## Reproduce

Run `sh build.sh` from the folder to rebuild the PDF. A working pdfLaTeX installation is required, with article, geometry, fontenc, Latin Modern, microtype, amsmath, amssymb, amsthm, mathtools, xcolor, hyperref and enumitem. Shell escape is disabled. No network or external data is used by the build.

Run `python3 reproducibility/check_constants_and_identities.py > reproducibility/check_results.json` to regenerate the checks. The script performs 61 exact rational or polynomial-algebra checks, plus clearly labelled floating-point illustrations. It is not a formal proof checker and does not calculate any actual theta sign matrix.

The optional explicit counting budget cites the published Hasanalizade–Shen–Wong bound, whose proof includes finite-height numerical zero verification. No zero enumeration is performed here. The asymptotic theorems require only the classical Riemann–von Mangoldt asymptotic and do not depend on the specific explicit constants.

## Review and repository

The mathematical chain, including the direct derivative proof, passed a separate scoped analytical review. The classical basis attribution and the published zero-counting theorem's numerical verification dependency were clarified during review. This review is not formal verification. Successful compilation and the check script are separate reproducibility checks, not proof of RH.

Canonical repository folder: https://github.com/serabing-hash/theta-weighted-certificate/tree/main/publications/growing-zero-jet-bands-2026-11-03 .
