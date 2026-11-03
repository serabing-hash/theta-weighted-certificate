# A Trace Bound for Negative Theta-Form Spectrum

The TeX and PDF form a separate manuscript conditional on the stated actual centered self-adjoint form realization. The trace-count principle is classical; this paper applies it to the theta form with full prime tail, exact center, and optional finite radical Grams. It proves an upper bound, not a negative eigenvalue, a nonnegative form, S1 membership, or an RH conclusion. No floating-point N=2 bound is used; the implementation-level ABI/header question for that separate numerical work remains outside this paper.

## Reproduction

Run `./build.sh` from this directory with pdflatex, standard LaTeX packages, Latin Modern and AMS fonts. It uses no network and no shell escape and runs three passes. A minimally configured Debian TeX image may create a local format and font map under `build/tex-runtime`. Prior manuscript and notes in `sources/` are supplied working records, not independently published references.

Run `python3 checks/check_algebra.py` with SymPy for exact checks of the integrated Gamma majorant, a finite Gram identity, and the equality case that requires a closed cutoff. This is not a numerical trace certificate or a proof of the analytic inputs. `sha256sum -c SHA256SUMS` verifies supplied snapshots. Independent review of the manuscript is required before publication.
