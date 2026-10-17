# All known theta-source constraints: bounded-energy escape and limits of center estimates

17 October 2026 UTC. **RH_PROOF=NOT-OBTAINED**.

This package proves a specific obstruction using **every** orthogonality
condition from the known source-generated space N. It does not obtain the
critical inequality `E(h)≥||h||²/2` on `D∩N⊥`.

There are real smooth even `h_m∈D∩N⊥`, with `||h_m||_H=1`, such that

```text
|E(h_m)−1/2| ≤ C m³ exp(−sqrt(m)) → 0,
||1_[−T,T]h_m||_H → 0 for every fixed finite T.
```

For every admissible fixed two-shift envelope, `D_R(h_m)→0` as well.
Thus imposing every condition from N cannot yield a uniform gap above 1/2, a
uniform positive center-mass bound, or coercivity of D_R repaired by a fixed
center observation. Both sides of the desired `F≤D` comparison tend to
zero on this sequence; its sign remains open.

Only `N ⊂ ker L` is used; `N = ker L` is neither proved nor assumed.
The historical directory name does not assert removal of the full nullspace.

The construction uses exponential-polynomial modes at zeros of Ξ, including
confluent derivatives at multiple zeros. Each mode satisfies all the
constraints exactly. Classical zero counting supplies narrow clusters, and
explicit theta-weight estimates control their energy. No zero is computed,
and no RH or simple-zero assumption is made. These are noncompact functions
in the actual **minimum** form domain, not compact tail bumps with finitely
many moments removed.

The source audit matches the supplied half measure, probability normalization,
operator, and domain to the original repository. The envelope audit proves
the ground-state identity on that minimum domain, with bounded V tending to
zero, and verifies the scoped oriented-jump coefficient improvement.

## Files

- [한국어 결과 요약](RESULTS_KO.md)
- [Full proof: escape, local density, and quantitative bounds](PROOF.md)
- [Envelope, domain, and signed-jump audit](ENVELOPE_AUDIT.md)
- [Original definitions and exact source paths](SOURCE_AUDIT.md)
- [Assumptions and dependencies](DEPENDENCIES.md)
- [Counterexample scope and remaining open claims](OBSTRUCTIONS_AND_OPEN.md)
- [Review record and publication scope](REVIEW.md)
- [Machine-readable status](STATUS.json)
- [Source identities](PROVENANCE.json)
- [Small exact algebra check](checks/check_exact_algebra.py)

## Verification and publication boundary

Run from this directory:

```sh
python3 checks/check_exact_algebra.py
sha256sum -c MANIFEST.sha256
```

The first command checks two polynomial identities using exact integer
coefficients. It is not a proof checker for the analytic theorems. The second
checks file integrity only. `checks/algebra_output.json` records the exact
algebra result. No numerical zero locations, physical source/action/Gram/FFT
calculations, or numerical spectral data are used. The saved algebra records
are retained unchanged; publication requires no new mathematical runs.

The result supports a scoped research note about failure of a positive gap
after imposing all known source constraints, with the envelope audit as a
technical appendix. A complete analytic proof is supplied. Internal checking
does not constitute external peer review or formal proof verification, and
no global novelty or priority claim is made. The accompanying manuscript
derives the compact source identity from a precisely cited classical explicit
formula and treats the minimum-domain extension.

Original new material follows the repository's CC BY-NC 4.0 scope. Existing
source files were referenced without modification; external sources retain
their rights. See the repository [license](../../LICENSE).
