# Source-clarification revision, 17 October 2026

This revision makes two source-proof clarifications without changing the theorem scope or numerical claims.

1. Lemma 2.3 now displays the polarized zero sum with the first variable conjugate-linear: `Q(u,v) = sum_rho conjugate(F_u(conjugate(z_rho))) F_v(z_rho)`. Its proof identifies conjugation invariance of the zero multiset and states the sufficient absolute-convergence condition that both transforms are `O((1+|z|)^(-2))` uniformly on `|Im z| <= 1/2`. The subsequent source-cancellation proof refers to that explicit mixed formula.
2. Proposition 2.5 now gives a second closability proof from the identity already established on the core. For an energy-Cauchy core sequence tending to zero in H, bounded lower-order terms imply that its physical images are Cauchy in the closed Gamma graph norm. Their L2 limit is zero, so the Gamma energy, and then the original energy, tend to zero. The paragraph explicitly states that no extension of the identity to the minimum domain is used in this argument.

The manuscript retains its original edge-measure closability proof as well. No source or numerical experiment was added; no research calculations were rerun. `N = ker L`, critical positivity, and RH remain unproved. No operator Weyl-sequence or essential-spectrum conclusion is claimed.

The single TeX was compiled in isolation with three `pdflatex` passes and shell escape disabled. The revised PDF has **15 pages**. The final structural report has no overfull boxes, undefined references/citations, multiply defined labels, out-of-page text spans, missing bibliography entries, or external authoring inputs. The repository version contains only the stated author email and ORCID.

All 15 pages were inspected in four rendered contact sheets. The pages containing the added polarized identity, closability argument, and final bibliography were also checked individually at the original rendered resolution. No clipping or equation-number overlap was observed. The current source/PDF hashes and page count are in `checks/build-receipt.json`; `checks/document-validation.json` records the structural checks. These checks concern the document and do not constitute independent verification of the analytic proof.

## Repository version

The title page now carries the author's email and ORCID. The data-availability
paragraph identifies the fixed public research-artifact commit after remote
readback. These publication details do not alter the mathematical arguments.

**RH_PROOF=NOT-OBTAINED.**
