**Publication update:** The scoped independent mathematical audit was completed after this preparation record. See [current publication status](../PUBLICATION_STATUS.md). The original record below is retained for provenance; its audit-pending statement describes the earlier assembly stage.

# Validation record

- Manuscript built with `./build.sh` using pdflatex, three passes, shell escape disabled. PDF has 5 pages. No undefined references or overfull boxes were reported. The epstopdf shell-escape-disabled warning is harmless: the document contains no EPS graphics.
- `python3 checks/check_algebra.py` passes exact symbolic checks on a representative polynomial identity and finite-row repair, and exact rational checks on the numerical majorants. These checks do not prove the analytic theorems.
- The two note snapshots and the previous manuscript TeX/PDF are bundled and covered by SHA256SUMS. Their contents have not been independently certified by these checks.
- DLMF equations 5.9.16 and 5.11.2 were consulted for the digamma integral and asymptotic.
- The all-prime tail is only asserted as a norm-convergent bounded operator on the weighted H space. The ordinary L2-to-H bound is used only for each single shift. The centered projection is applied on H, not asserted bounded on all ordinary L2.
- The cutoff M is restricted to integers M >= 1. The optional enclosure of all negative eigenvalues in [-tau_M,0) is conditional on L_c >= 0.
- Independent mathematical audit remains necessary before public release; no public posting is made by this package.
