# Low-Window Prime-Tail Compression and Radical Certificates

This is a separate manuscript (`paper.tex`, `paper.pdf`) with its working source records in `sources/`. The proof uses explicit operator, theta, and full-domain radical inputs from the accompanying working manuscript and notes. It does not establish a low-window sign, identify the known radical with the full kernel, certify numerical columns, or prove or disprove the Riemann hypothesis. The finite rank schedule may be far too large for practical use.

## Build and checks

Run `./build.sh` in this directory. It uses pdflatex, standard LaTeX packages, Latin Modern and AMS fonts, no network, and no shell escape; it runs three passes. On the minimally configured Debian TeX installation used here it creates a local format and font map under `build/tex-runtime`. The source-manuscript snapshot is not rebuilt.

Run `python3 checks/check_algebra.py` with SymPy installed for elementary checks of the Gamma-cutoff inversion, exact finite Gram identity, and sample factorial bounds. These are not proofs of the infinite-dimensional statements or numerical certificates. Run `sha256sum -c SHA256SUMS` to verify the supplied snapshots. The cited research notes are working documents rather than independent published verification. Independent line-by-line mathematical review is required before publication.
