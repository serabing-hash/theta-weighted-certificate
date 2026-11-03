**Publication update:** The scoped independent mathematical audit was completed after this preparation record. See [current publication status](PUBLICATION_STATUS.md). The original record below is retained for provenance; its audit-pending statement describes the earlier assembly stage.

# Finite Prime Heads and the Known Theta Radical

`paper.tex` and `paper.pdf` are the standalone manuscript and its compiled output. The proof is conditional on precisely identified analytical inputs from the accompanying working manuscript `sources/unified_theta_energy.pdf` and `sources/unified_theta_energy.tex`; the immediate dated research notes are supplied alongside them. The source manuscript and notes are working documents, not an independent publication or an independent audit. In particular, this result does not prove or disprove the Riemann hypothesis, does not determine the sign on the orthogonal complement of the known radical, and does not identify that radical with the entire operator kernel.

## Build

Run `./build.sh` from this directory. It requires a TeX Live installation with pdflatex, standard LaTeX packages, Latin Modern and AMS fonts. It uses no network or shell escape, runs three passes, and writes `paper.pdf`. On the particular minimally configured Debian TeX image used here, the script creates a local format and font map under `build/tex-runtime`. The source PDF snapshot is not rebuilt by this script.

## Checks and boundaries

Run `python3 checks/check_algebra.py` with SymPy available. It checks a finite polynomial-radical convention, exact algebra of a sample finite-rank correction, a rank bound, and rational majorants. These checks are illustrative and do not establish the infinite-dimensional conclusions. Run `sha256sum -c SHA256SUMS` to verify the delivered snapshots. The PDF build log should contain no undefined references or overfull boxes. A shell-escape-disabled epstopdf warning is harmless for this document.

Analytical dependencies are identified in Section 1 and mapped by source labels in Section 6. The infinite index, the compactness proof, and the spectral argument are given in the manuscript, conditional on these clearly identified inputs. An independent line-by-line mathematical audit is still needed before publication.
