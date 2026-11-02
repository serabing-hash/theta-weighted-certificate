# Mean adapted interface bounds and joint source estimates

**Author:** Jongmin Choi  
Independent Researcher, Seoul, Korea  
ORCID: https://orcid.org/0009-0008-7448-514X

**Version:** Manuscript v1.0, November 1, 2026  
**License:** Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).

## Results and dependency classes

The manuscript concerns the complete even theta prime-Gamma energy on its full finite-energy domain.

1. **Accepted local-sign input.** Whole-domain local positivity at radius 4/5 implies the global variance coefficient **493/1000**. The same comparison has exact endpoint (19985 - sqrt(69921))/40000. No inverse-response enclosure is required.
2. **Additional explicit response contracts.** Complete local-residual and centered-response enclosures imply the stronger coefficient **2861149/5760000**. These contracts are not implied by local positivity. The analytic source bound is ||J|| < 11101/403200; the conditional inverse cost is at most 13/5000.

The two branches are kept separate. The theta normalization, physical bridge, equality of minimum and maximal energy domains, rank-64 lifted coercivity, full-prime tails, and signed exterior cap are proved in the manuscript's appendices. Only classical external sources appear in its bibliography.

The actual regularized exterior sign S + A2 >= 0, the global coefficient 1/2, and the Riemann hypothesis are **not proved**. The hypothetical coefficient 5741149/11520000 requires that unproved sign and is not an achieved result.

## Files

- mean_adapted_interface_bounds.pdf — complete manuscript.
- mean_adapted_interface_bounds.tex — main editable LaTeX source.
- appendix_scalar.tex — full-series scalar estimates.
- appendix_lift_slack.tex — analytic local lift and signed exterior cap.
- appendix_foundations.tex — normalization, classical explicit-formula bridge, and domain proofs.
- appendix_response_rows.tex — precise centered-row and infinite-tail contract definitions.
- appendix_provenance.tex — computational input identities and validation boundary.
- build.sh — document-only build.
- mean_adapted_interface_bounds_source.zip — clean source distribution.
- DOCUMENT_QA.json, PAPER_MANIFEST.json, SHA256SUMS.txt — artifact checks and integrity metadata.

## Build

With a standard TeX installation containing pdflatex, Latin Modern, AMS packages, geometry, microtype, booktabs, longtable, enumitem, and hyperref, run:

    sh build.sh

The script makes two LaTeX passes with shell escape disabled and copies the PDF from build/ to this directory. It runs no research code and requires no numerical dataset.

The computational input data are not included in the clean source ZIP. Their absence does not affect document compilation. The manuscript states exactly which accepted local theorem or additional response contracts each conclusion uses; compilation does not validate those premises.

## Verification boundary

Document production used the preinstalled TeX and Poppler tools. No source-generation program, numerical research calculation, certificate replay, or enclosure regeneration was executed. Hashes identify files, not mathematical truth. The manuscript is not represented as journal accepted, peer reviewed, or formally proof verified.
