# A Trace Bound for Negative Theta-Form Spectrum

The scoped independently audited paper and all individual files of its reviewed source package are published here. **The original ZIP archive is on hold and is not published here.** All constituent files are available individually.

- [Paper PDF](paper.pdf)
- [Editable TeX](paper.tex)
- [Publication status](PUBLICATION_STATUS.md)
- [Original preparation README and build instructions](README.prepublication.md)

The result depends on the stated exact centered self-adjoint form realization and its analytical inputs. The trace-count principle is classical. The manuscript supplies upper bounds on negative spectral counts and the stated negative-part Schatten conclusions; **it does not establish positivity, an actual negative eigenvalue, S1 membership, or RH.**

Separate scalar numerical references have an unresolved implementation ABI/header cross-check and are not used to compute or prove the manuscript's theorem bounds. In particular, no floating-point N=2 certificate is imported into the result.

The code checks elementary exact algebra, a finite Gram identity and the equality/closed-cutoff case. It is not a numerical trace or sign certificate, and does not prove the analytical realization inputs. Run ./build.sh for document compilation and python3 checks/check_algebra.py with SymPy for these limited checks.

The original README and manifest are preserved as README.prepublication.md and SHA256SUMS.prepublication. Their review-pending statements describe preparation before the scoped independent audit. Current SHA256SUMS and PUBLICATION_SHA256SUMS cover the public files.
