# Positive-Source Compression and All Schatten Classes for a Centered Theta Form

## Publication update, 3 November 2026

The prior-acknowledged manuscript completed two scoped independent reviews before publication. The preparation-time review-pending statement retained below is historical; the reviews are not peer review or proof-assistant formalization. **The original ZIP is on hold and is not published here. Every constituent file is available individually.**

- [Paper PDF](paper.pdf)
- [Editable TeX](paper.tex)
- [Publication status](PUBLICATION_STATUS.md)
- [Unchanged preparation README](README.prepublication.md)

Scott Schubr's [edition 3, Theorem 1.1](https://research.luminaryoddities.com/joint-cutoffs-negative-spectrum-decay-weighted-weil-operators/v/3/files/Joint_cutoffs.pdf#page=1) already states the same qualitative subpolynomial negative-count and all-p>0 Schatten conclusions. The present work gives an alternative centered source-bank/positive trace-defect proof under the stated exact form-realization inputs. It does not claim priority, a stronger qualitative conclusion or a better constant. RH and the actual spectral sign remain unresolved. The third-party paper is linked only; its PDF is not redistributed.

The original README and checksum manifest are preserved as README.prepublication.md and SHA256SUMS.prepublication. Current SHA256SUMS and PUBLICATION_SHA256SUMS cover the public files.

This separate manuscript is conditional on the stated actual theta/Gamma/prime form realization. Schubr had previously established the same subpolynomial count and all-positive-Schatten conclusion for the equivalent even realization. This paper gives an alternative positive-source trace-defect proof and an explicit illustrative constant, and improves the particular weaker count in a later publicly posted trace-bound paper. It claims neither priority nor a better constant. It does not claim historical priority, positivity, an actual negative eigenvalue, a finite negative index, a gap at zero, or an RH conclusion. The source bank is only required to lie in the centered Hilbert space; no form-domain invariance or inverse-solver implementation is used.

## Build and checks

Run `./build.sh` in this directory using pdflatex, standard LaTeX packages, Latin Modern and AMS fonts. It uses no network or shell escape and runs three passes. A minimal Debian TeX image may generate a local format and font map under `build/tex-runtime`. The supplied prior papers are snapshots and are not rebuilt.

Run `python3 checks/check_algebra.py` with SymPy for elementary exact checks of constants, trace-defect slack, and a finite true-projection model. This code does not evaluate actual theta Grams, certify a spectral sign, or prove the analytic realization. Run `sha256sum -c SHA256SUMS` to verify the delivered files. The included working notes and analytical audits are source records, not peer-reviewed publications. Independent review of this complete manuscript is required before any public release.
