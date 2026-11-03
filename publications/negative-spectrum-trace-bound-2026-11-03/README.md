# A Trace Bound for Negative Theta-Form Spectrum

## Prior result and scope clarification (3 November 2026)

Scott Schubr, [*Joint Cutoffs and Negative-Spectrum Decay for Weighted Weil Operators*, edition 3](https://research.luminaryoddities.com/joint-cutoffs-negative-spectrum-decay-weighted-weil-operators/v/3), [Theorem 1.1, pp. 1–2](https://research.luminaryoddities.com/joint-cutoffs-negative-spectrum-decay-weighted-weil-operators/v/3/files/Joint_cutoffs.pdf#page=1), already states a negative-depth counting bound of order exp(O(sqrt(log(1/epsilon)))) as epsilon tends to zero, and membership of the negative part in every Schatten class S_p for p > 0 under its stated hypotheses. The present manuscript's weaker direct trace bound should therefore not be read as the first such decay or Schatten result.

A scoped comparison of the even sectors identifies the form correspondence through Uu = u / sqrt(W), with the factor 2 in the form normalization retained; given the ambient operator-core input, the public minimal even-sector closure corresponds to the local maximal centered form domain. In operator notation, H_pub restricted to its constrained even sector equals 2 U L_c U^(-1), so the stated count and Schatten conclusions transfer after constant rescaling of the depth. The comparison preserves the exact domains, centering and realization hypotheses. It is not a blanket identification of operators with different domain or normalization choices.

The present manuscript supplies its direct trace-bound argument within its explicitly assumed exact centered form realization, with the full prime tail and optional finite radical-Gram constraints. Its own direct trace estimate yields Schatten membership for p > 1 and remains weaker than the prior theorem above, and its argument does not independently establish S1 membership, positivity, an actual negative eigenvalue or RH. The separate scalar numerical references are not inputs to either this comparison or the manuscript's theorem calculations.

This notice records the identified preceding theorem and the scoped operator/form comparison. It is not a comprehensive assessment of the independent paper's historical priority, a verification of all of its proofs, or a claim of a new strongest bound. The published TeX and PDF are unchanged; this README clarification should be read alongside them.

The scoped independently audited paper and all individual files of its reviewed source package are published here. **The original ZIP archive is on hold and is not published here.** All constituent files are available individually.

- [Paper PDF](paper.pdf)
- [Editable TeX](paper.tex)
- [Publication status](PUBLICATION_STATUS.md)
- [Original preparation README and build instructions](README.prepublication.md)

The result depends on the stated exact centered self-adjoint form realization and its analytical inputs. The trace-count principle is classical. The manuscript supplies upper bounds on negative spectral counts and the stated negative-part Schatten conclusions; **it does not establish positivity, an actual negative eigenvalue, S1 membership, or RH.**

Separate scalar numerical references have an unresolved implementation ABI/header cross-check and are not used to compute or prove the manuscript's theorem bounds. In particular, no floating-point N=2 certificate is imported into the result.

The code checks elementary exact algebra, a finite Gram identity and the equality/closed-cutoff case. It is not a numerical trace or sign certificate, and does not prove the analytical realization inputs. Run ./build.sh for document compilation and python3 checks/check_algebra.py with SymPy for these limited checks.

The original README and manifest are preserved as README.prepublication.md and SHA256SUMS.prepublication. Their review-pending statements describe preparation before the scoped independent audit. Current SHA256SUMS and PUBLICATION_SHA256SUMS cover the public files.
