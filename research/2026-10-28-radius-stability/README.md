# Quantitative radius stability for a prime gamma form

Review manuscript v0.1, 28 October 2026.
Author: Jongmin Choi, Independent Researcher, Seoul, Korea.
ORCID: 0009-0008-7448-514X.

## Result and scope

Conditional on the explicit base certificate stated as Assumption 1, the manuscript proves

q_B(u) >= (7/20000000) ||u||_2^2

for the full minimum real-even local form domain and

0 < B <= 1/2 + 1/3000000000.

The proof keeps complete gamma energy, the exact pole, and the active prime-2 reflection. Every other prime-power correlation vanishes exactly by support in this range. The main analytic step is a local bound of 16 for the diagonal Schur lift near the reflection interface, yielding a linear perturbation modulus. This is a very small fixed-window extension, not a practical large-radius certificate, all-radius positivity, or RH.

No historical novelty is claimed. AI assisted exploration and preparation. This review manuscript has not undergone independent human peer review or proof-assistant checking.

## Files

- radius_stability.pdf: eleven-page manuscript.
- radius_stability.tex: editable LaTeX source.
- build.sh: builds only the manuscript using an installed LaTeX distribution; no shell escape.
- evidence/verify_half_support.py: unchanged base-certificate verifier.
- evidence/half_support_certificate.json: unchanged base-certificate output.
- evidence/base_analytic_reduction.tex: unchanged base analytic source, renamed for clarity.
- requirements-base.txt: pinned numerical dependency for optional base reproduction.
- SHA256SUMS: digests of all files above.

The evidence source and result are included to make the numerical premise reviewable. They are not a new certificate evaluated at the enlarged radius. Source hashes are also printed in Appendix A.

## Building the document

With pdflatex and the standard packages listed in the TeX source installed, run:

    sh build.sh

The script does not execute any evidence program. No numerical calculation is necessary to rebuild the PDF.

## Optional base-certificate reproduction

The original base verifier was reproduced once on 28 October 2026 using Python 3.12.14 and python-flint 0.9.0. It passed all assertions and generated a JSON file identical, byte for byte, to the included result. No additional numerical source evaluation was needed for the radius-continuation proof.

A reader who chooses to reproduce the BASE certificate can install the pinned requirement in an isolated environment, then run without Python optimization:

    python -I -B evidence/verify_half_support.py --output reproduced_half_support.json

This is an explicit optional numerical action, separate from the document build. It uses the original fixed 160-bit precision, 16 low modes, mode-tail split 8192, and 24 exponential terms. Review the source before running. Do not mistake its output for a direct computation at the enlarged radius.

Same-code reproduction is not an independent implementation. The trust boundary includes the base analytic reduction, source code, Python, python-flint/FLINT and the execution environment. Printed LDL pivots alone are not eigenvalue bounds or a source-free replacement for the interval calculation.

## Project context

https://github.com/serabing-hash/theta-weighted-certificate

This link identifies the project, not an assertion that this review bundle has already been posted there. No external upload or publication is performed by building or opening the bundle.
