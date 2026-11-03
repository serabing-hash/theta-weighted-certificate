# Theta Prime Gamma Energy: Version 4 working integration

This is the separate **281-page Version 4 working integration**, preserving the exact reviewed TeX/PDF. It does not replace the [256-page Version 3](../2026-11-03-unified-theta-energy-v2/) or the [244-page prior archive](../2026-11-03-unified-theta-energy-v2/versions/v2-244-pages/). All earlier repository files and Git history remain unchanged.

- [Version 4 PDF](unified_theta_energy.pdf)
- [Self-contained TeX](unified_theta_energy.tex)
- [New theorem map](THEOREM_MAP.md)
- [Reference map](REFERENCE_MAP.md)
- [Public verification scope](PUBLICATION_STATUS.md)

## Changes from Version 3

Four appendices add the finite-prime-head obstruction and compact known-radical repair, positive-range tail signs, bounded-window tail compression, conditional absolute ground-energy computability, and an alternative positive-source trace-defect proof of spectral decay. Frozen v3 inputs, five standalone source manuscripts, elementary checkers and the existing v3 reproducibility folder are retained under source_inputs/. assemble.py checks the frozen hashes and reversible recovery of the original v3 source after removing the named additions.

Scott Schubr's [edition 3, Theorem 1.1](https://research.luminaryoddities.com/joint-cutoffs-negative-spectrum-decay-weighted-weil-operators/v/3/files/Joint_cutoffs.pdf#page=1) already states the same qualitative subpolynomial negative-count and all-positive-p Schatten conclusions for the corresponding even realization. The source-bank argument is an alternative proof; no first-result or better-constant claim is made. The third-party PDF is linked, not redistributed.

## Scope and publication links

All additions retain the stated exact form-realization, domain, normalization and arithmetic inputs. The global sign and RH remain unresolved. No exact-zero decision, actual ground-energy bracket, full implemented algorithm, finite negative index or practical runtime guarantee is established. The known derivative radical is not identified with the entire kernel. Inherited numerical calculations are not freshly re-certified by this integration.

The current manuscript distribution links were corrected to this v4 folder and its source_inputs/v3_support/reproducibility packet. A limited independent re-review confirmed that only the two distribution URIs changed, with PDF links/text, frozen-v3 recovery and artifact manifests checked. The current fixed TeX/PDF hashes identify this corrected version. The title-page wording 'working integration; review pending' records the build-time label; a subsequent scoped integration review found no blocker within its stated limited scope. This is not peer review, formal verification or a complete re-audit of v3.

**The original large ZIP is on hold and is not published.** All document/assembly inputs and mathematical reproduction files selected from it are available individually. Private QA images/reports and internal process plans are excluded. The current manifest covers the public files only.

## Reproduce in a working copy

    sha256sum -c SHA256SUMS.txt
    sha256sum -c source_inputs/SHA256_INPUTS.txt
    mkdir -p qa
    python3 assemble.py
    sh build.sh
    for p in source_inputs/*/check_algebra.py; do python3 "$p"; done

Assembly writes a generated static check report to qa/; no original private QA content is required. TeX compilation uses installed LaTeX packages, Latin Modern/AMS fonts and no shell escape or network. Algebra checkers require SymPy and do not compute actual theta Grams or certify a spectral sign. PDF binary reproducibility is not claimed. The supplied source_inputs/v3_support/ packet retains its original dependencies, expected outputs and verification limitations.
