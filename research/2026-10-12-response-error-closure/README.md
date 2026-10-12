# Response-only reduction limits for a frozen residual enclosure

This is the supporting evidence package for a standalone closure note on a
completed diagnostic route. It records what follows from two saved rational
budget reports, and the limits of that inference. It is not a proof of the
Riemann Hypothesis and does not certify a new residual sign.

## Claim and its exact scope

The saved residual interval has midpoint approximately
`1.4936700507432036e-19` and radius approximately `2.1333753720055062e-14`.
The saved ordered radius attribution assigns approximately
`2.1274731489160268e-14` to `response_enlargement` and leaves approximately
`5.9022230894794060e-17` in the other terms. The latter is approximately
`395.1490549431` times the absolute saved midpoint.

**If the midpoint and all nonresponse attribution terms are frozen, reducing
the response attribution alone, even to zero, leaves an interval containing
zero.** This is a statement about that enclosure and design comparison.
It is not a lower bound on the error of the actual mathematical object, a
proof that a coupled reformulation cannot succeed, or a proof that the
underlying residual is zero. The attribution is an ordered telescoping
decomposition; mixed terms are not unique physical causes.

If all attribution terms were reduced by one common factor while the midpoint
stayed fixed, strict sign separation would require a factor strictly greater
than approximately `142827.7530867011`; the saved smallest sufficient integer
factor is `142828`. A new enclosure may move the midpoint. A sufficient
recentered criterion is a certified bound
`abs(m_new - m_old) + rho_new < abs(m_old)`, or one may directly certify that
the entire new interval lies strictly on one side of zero. The old midpoint
alone supplies neither certificate.

## Files

- `evidence/SAVED_ERROR_DECOMPOSITION.json`: unchanged saved exact fractions,
  residual interval, ordered radius attribution, and premise caveat.
- `evidence/R_SIGN_SEPARATION_BUDGET.json`: unchanged fixed-center design
  comparison and exact response/nonresponse ratios.
- `history/shared_jet/PROOF_KO.md`: unchanged historical Korean inclusion
  argument and preparation report.
- `history/whole_r/PROOF_KO.md`: unchanged historical Korean whole-R inclusion
  argument with conditional source premises.
- `history/whole_r/README_KO.md`: unchanged historical implementation report.
- `code/whole_r.py`: unchanged historical whole-R implementation, provided
  for inspection. This file is not a self-contained runnable distribution.
- `verify_saved_budget.py`: a new standard-library-only inspection tool.
- `PROVENANCE.json`: byte identities, scope, dependency limits, and packaging
  checks.
- `MANIFEST.sha256`: SHA256 of every payload file other than the manifest.

## Historical status, counts, and unavailable dependencies

The original reports and source retain their historical `numeric_count = 11`
or equivalent wording. The project count reported at publication preparation
is `12`; this package does not incorporate or describe that additional
attempt. Preserving `11` is intentional and does not reset the project count.
No new research evaluation was performed while preparing this package.

The historical proof texts are preserved records, not new execution receipts.
References in them to tests, wrappers, original protected inputs, manifests,
or other files do not mean those items are included here or independently
reverified by this package. Their implementation status and resource notes
describe the earlier snapshot, not the present publication operation.

`code/whole_r.py` directly imports `shared_jet` and `center_replay`; those
modules, their transitive dependencies, actual center-jet streams, complete
source packets, admission material, and fixtures are not bundled. Therefore
this package cannot reproduce a whole-R run or its historical test claims.
The historical analytic/source/domain, complete-Gamma-tail, and coercivity
premises remain conditional. Hashes establish byte identity, not their
mathematical truth.

## Inspect and verify

Use Python 3.9 or later. From this directory, run:

```text
python verify_saved_budget.py
```

This default operation verifies the complete payload manifest only. To replay
the exact rational identities in the two saved JSON files and report the
frozen-center interval with all saved response attribution removed, run:

```text
python verify_saved_budget.py --verify-budget
```

For a finite hypothetical reduction factor, for example `1000`, run:

```text
python verify_saved_budget.py --verify-budget --response-factor 1000
```

The budget mode uses `fractions.Fraction`; decimal summaries are not used as
proof data. It checks the saved interval/midpoint/radius identity, the full
attribution sum, the cross-file exact fractions, the saved improvement ratios,
the integer-factor condition, zero containment, and snapshot counts. It then
forms `m_old +/- (rho_nonresponse + rho_response/factor)`, with the response
term set to zero for `all`. It performs no Gamma, theta, prime, source-polynomial,
inverse, center-jet, or production evaluation.

The publication workspace performed syntax, JSON parsing, byte-preservation,
manifest, and content-disclosure checks. In a separate existing Work task,
the manifest-only and saved-budget modes were each run once. The reported
readback matched all nine payload hashes; both modes exited 0 with no stderr.
The exact saved identities, ratios, and integer-factor condition passed, and
the response-zero fixed-center interval contained zero. This audit performed
no actual source evaluation and did not increase the project research count.
Its raw runtime receipt is not bundled in this package. A hash PASS is a
packaging result; the exact-identity PASS is a saved-budget result, not an RH
result. The original analytic premises and scientific HOLD remain unchanged.

## Publication and rights

This package adds a new scoped directory in the existing repository, without
replacing prior files or rewriting history. Cite the exact commit-pinned
directory URL recorded in the accompanying paper, so later branch updates
cannot silently change its evidence. The repository's existing root `LICENSE`
is unchanged; no additional relicensing statement is introduced here.
