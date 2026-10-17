# Document production and review record

17 October 2026. This record concerns manuscript integrity and presentation. It is not external peer review or formal verification of the analytic proof.

## Build and layout

The single TeX was copied into an isolated temporary directory and compiled with three `pdflatex` passes, with shell escape disabled. No external bibliography, images, research files, or data were supplied as authoring inputs. The output is a **15-page A4 PDF**.

The final log contains no overfull boxes, undefined references or citations, or multiply defined labels. All PDF text spans are within the page rectangle. All 15 pages were rendered at scale 1.5 (108 dpi) and inspected in four contact sheets. The title/author page and the page containing the fixed GitHub artifact URL were additionally inspected at the original rendered resolution. No clipping, missing material, or overlapping equation numbers was observed. The artifact URL wraps within the text block and its PDF link target is the full fixed commit URL.

The author fields are Jongmin Choi; Independent Researcher, Seoul, Korea; 24ping@naver.com; ORCID 0009-0008-7448-514X. Both identifiers appear in the TeX and PDF. No unexpected contact identifier was detected. The inline bibliography has the same four classical references and contains no earlier paper by the author.

## Mathematical-content boundary

The abstract, mathematical sections preceding the scope section, and appendices/bibliography are byte-identical in the TeX to the reviewed source-clarification draft. The publication edit changes the author metadata and artifact-availability text. It adds no new mathematical result or computation.

The source clarification explicitly displays the conjugate-linear-first polarized zero sum and its absolute-convergence condition. Its second closability proof uses the core source identity and bounded lower-order terms before extending to the minimum domain. Known-source orthogonality is distinguished from the unproved equality N=ker L. Critical positivity and RH remain open; no operator Weyl-sequence, essential-spectrum, or priority claim is made. Constants, starting indices, and a specific numerical envelope pair remain uncertified.

## Reproducibility and publication evidence

`checks/build-receipt.json` records the exact source/PDF hashes, page count, and TeX engine. `checks/document-validation.json` records the structural checks. `checks/artifact-readback.json` records unauthenticated public readback of the 14 files in the fixed research-artifact commit: every remote byte sequence matched the local artifact before the manuscript URL was inserted.

The exact algebra script and saved output are unchanged. They concern two polynomial identities only; they are not an analytic proof verifier and were not rerun for publication. The source and domain arguments still merit independent mathematical review, and no comprehensive novelty survey is claimed.

Only manuscript, proof/dependency documentation, reproduction code, and compact validation records are part of this public package. Local build products and private delivery metadata are excluded.

**RH_PROOF=NOT-OBTAINED.**
