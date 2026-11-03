# Computable Ground-Energy Brackets with Finite Null Constraints

This manuscript is conditional on the precisely identified complete theta/Gamma/prime form realization and its computable arithmetic inputs in the supplied source manuscript. It proves existence of a terminating rational enclosure procedure, not an evaluated bracket, an implementation of the full procedure, an exact-zero decision, a practical runtime bound, an actual relative tail sign, or a Riemann hypothesis result. Finite null constraints need not exhaust the physical kernel.

## Reproduction

Run `./build.sh` in this directory with pdflatex, standard LaTeX packages, Latin Modern and AMS fonts. It uses no network and no shell escape, builds three times, and writes `paper.pdf`. A minimal Debian TeX installation may create a local format and font map under `build/tex-runtime`. The supplied prior manuscript is a source snapshot and is not rebuilt by this script.

Run `python3 checks/check_algebra.py` with SymPy to check elementary exact finite identities for the overlapping thresholds, a model constrained inverse, and a finite Neumann remainder. This script is not an implementation or proof of the full analytic algorithm. `sha256sum -c SHA256SUMS` checks delivered file integrity. The explicit reference inverse note is included as `sources/EXPLICIT_REFERENCE_INVERSE_ALGORITHM.md`; its needed general-cap mechanism is independently described in Section 5. The working notes are not independently published references. Independent mathematical review is required before any public release.
