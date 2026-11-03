# Two Essential Signs of the Prime Tail on Positive Spectral Ranges

`paper.tex` and `paper.pdf` are a separate manuscript and compiled PDF. The underlying theta operator, form, source domain and norm bound are explicitly identified inputs from the supplied working manuscript and notes. The work establishes absolute essential signs on every fixed positive spectral range, not a low-energy relative sign or a proof or disproof of the Riemann hypothesis. The known derivative radical is not equated with the full physical kernel. No historical priority is claimed.

## Reproduce

Run `./build.sh` from this directory. It uses pdflatex, standard LaTeX packages, Latin Modern and AMS fonts, no network and no shell escape. It runs three passes and writes `paper.pdf`. On the minimal Debian TeX image used here, the script creates a local format and font map under `build/tex-runtime`. The prior manuscript PDF snapshot is not rebuilt by this script.

Run `python3 checks/check_algebra.py` with SymPy installed to check the elementary packet identity, one Gamma-series derivative, and a theta-bound factorization. These checks do not prove the functional-analytic theorem. Run `sha256sum -c SHA256SUMS` to verify the delivered files. The included source notes and previous manuscript are working records, not independent published verification. Independent mathematical review is required before public release.
