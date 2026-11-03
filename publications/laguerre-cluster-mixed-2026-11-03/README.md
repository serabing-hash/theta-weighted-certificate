# Conditional Laguerre clustering and mixed cardinal tests

This is a conditional research manuscript. The fixed TeX/PDF underwent a scoped independent review; this is not peer review, formal verification, or independent reconstruction of every imported analytical result.

- [Manuscript PDF](cluster_mixed.pdf)
- [Editable TeX](cluster_mixed.tex)
- [Exact symbolic algebra checker](checks/check_algebra.py)

## Conditional scope and source availability

The closed form/operator realization, actual cardinal-source domain admission and image identities, and the scalar integral lower bound are assumed inputs from the research drafts named in the bibliography. Those prior drafts and their source archives are **not included in this public distribution, and their public availability is not established here**. The bibliography's hashes identify the drafts used; they do not supply access or verify their mathematical content. Private research notes and source archives are not distributed.

Consequently, a reader can rebuild this manuscript and rerun its exact finite symbolic identities using the files here, but cannot reconstruct or independently verify the complete form/cardinal/scalar input chain from this distribution alone. The scalar integral lower bound is an input, not independently re-certified here. The manuscript is not a self-contained proof of those preceding results.

The Laguerre-sign and global polynomial-form positivity assumptions are different unproved hypotheses. No actual nonreal zero or actual zero configuration is certified, no global Phi positivity is proved, and neither RH nor its negation is established. Historical priority for the cluster estimates is not determined.

## Reproduce the available checks

    sha256sum -c SHA256SUMS.txt
    python3 checks/check_algebra.py
    sh build.sh

The checker requires SymPy and tests exact pair-ratio identities, a positivity polynomial, the cone comparison, mixed-source coefficients and a 2-by-2 determinant. It does not test actual zeros, operator-domain admission, complete theta integrals or global signs. The build requires installed pdflatex, standard LaTeX/AMS packages and Latin Modern fonts; it uses no network or shell escape. PDF byte hashes can change with build metadata or TeX versions.

Only the manuscript, standalone build script, elementary checker, this README and the public checksum manifest are supplied. No ZIP is uploaded, and no private audit or build outputs are included.
