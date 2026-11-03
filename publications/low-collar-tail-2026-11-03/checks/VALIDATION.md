# Validation record

- The manuscript was rebuilt from a removed build directory with pdflatex, three passes and shell escape disabled. The PDF has six pages. No unresolved references or overfull boxes were reported; the epstopdf warning about disabled shell escape is harmless because no EPS graphics are used.
- `python3 checks/check_algebra.py` checks the symbolic inversion of the explicit Gamma cutoff, an exact finite-dimensional radical Gram identity, and sample factorial inequalities. It is not a functional-analytic proof or a numerical sign certificate.
- The supplied low-collar note has SHA-256 `574df9d07520bf122ba48221197540fdd6cdfa6cbdad283d149c3912d8c32ebc`. The source manuscript and other notes are retained as working records.
- The row estimate is distinguished from its symmetrized compressed estimate. The bounded ordinary-L2-to-weighted estimate is applied only to finite prime rows. Whole-kernel and known-radical projections are not identified.
- The Gamma cutoff is explicit and positive even when R+d=0. The rank-cost estimate chooses the smallest positive integer satisfying its two displayed lower bounds; no cost estimate is claimed for arbitrarily inflated m. The rank bound is neither optimality nor a practical computation claim.
- No filtered column, Gram entry, tail sign, negative-spectrum exclusion, or low-collar relative estimate has been numerically certified. Independent line-by-line review is required before publication.
- Review corrections clarify that the Taylor output is used only as an ordinary L2 vector (without denying weighted membership) and distinguish the Chebyshev function psi_C from the digamma function psi. The PDF was rebuilt from a clean build directory after these corrections.
