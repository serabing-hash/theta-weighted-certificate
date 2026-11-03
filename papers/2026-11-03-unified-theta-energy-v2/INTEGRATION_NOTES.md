# Version 3 working integration and input provenance

This public update retains the manuscript title-page status Version 3 (working integration). Its scoped independent integration audit passed without required mathematical edits. It is not peer review or formal verification. The complete previous 268-file release is preserved under versions/v2-244-pages/.

## Inputs and provenance

- The existing integrated source is the published 244-page version in `papers/2026-11-03-unified-theta-energy-v2` at commit `91e8742de9b03fd363c1c6b2c25363dc861c4515`. Its source SHA-256 is `7fb34043acebd8837ef435ef27a5ab9545675491bfe2e3a44519405f84d75a14`.
- The incorporated standalone publication is `publications/growing-zero-jet-bands-2026-11-03` at commit `f2a5e6e390f213149f5f9d1d023aa2dd81d33518`. Its source SHA-256 is `bf587b78fb4e603223822b2797291db2551744e43934c1e220c60e41b4f2c20f`. The local public-release receipt records remote byte verification.
- These input files and the prior computation code were not changed. Only a separate source and build copy was made here.

## Changes

The original article body is preserved except for clearly marked additions to the abstract, a subsection at the end of the existing fixed-lattice section, a macro, and the bibliography; the working-version label is updated. Appendix P incorporates the standalone analytic proof in full. Original section headings are demoted one level, labels and their references are namespaced, and two publication/reproducibility sentences have been adjusted for the combined manuscript. The original reference to Zhang is added, Erdelyi's published journal information is supplied, existing duplicate references are reused, and the standalone publication itself is cited at its fixed commit.

The result concerns the full actual zero-jet space of one contiguous band, its ordinary L2 norm, all multiplicity prefixes, complete prime powers, and the complete Gamma form. The smaller-width result is a two-sided asymptotic; the conservative fixed-boundary result is an eventual positivity consequence under the stated strict constant. The Schur consequence applies within a covered union. It does not establish arbitrary band gluing, a budget-independent reciprocal-theta weighted gap, the global sign, or RH. The optional explicit zero-counting theorem has a finite-height numerical verification dependency; the qualitative result uses the classical asymptotic count.

## Checks

- `sh build.sh`: three no-shell-escape pdfLaTeX passes, no network. A final successful build should yield `unified_theta_energy.pdf` and `build/unified_theta_energy.log`.
- `python3 growing_zero_jet_checks/check_constants_and_identities.py`: 61 exact rational or polynomial-algebra checks and two separately labelled floating-point illustrations. Its output was byte-identical to the recorded standalone publication result. This is not a formal proof checker and does not compute any actual theta sign matrix.
- `audit_integrated_source.py`: compares the incorporated proof with the source inputs, checks namespaced labels, missing references/citations and duplicate labels/bibliography keys. The analytic proof itself requires independent mathematical review; build and numerical/exact checks do not establish it.
