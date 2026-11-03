# Synthetic Gamma-sector response checks

These three examples use exact Python standard-library Fraction arithmetic:

1. A positive full block while a more restrictive scalar sufficient pair cannot hold.
2. Positive individual low/high pairs with a collectively negative coupled example.
3. The complete residual identity and its actual Gram congruence under nonorthogonal coordinates.

They are algebraic structural examples, **not actual theta matrices, a Gamma-low sign certificate, a numerical global coefficient, or a proof of RH**. The Gamma-sector bridge in the manuscript has additional form-domain, reducing-sector and cofinal-sign hypotheses. These examples do not establish them or identify the four-/five-zero spaces with a Gamma-low spectral space.

## Run

From a copy of this directory, run:

```sh
python3 check_identities.py
```

No third-party packages are required. Do not use Python `-O` or `-OO`, since the original program uses assertions for its checks. The command writes `exact_check_results.json` next to the script. Check the release hashes first; compare the new JSON with the supplied expected result rather than altering an expectation to obtain a match.

All three checks were replayed and reproduced the supplied JSON byte for byte. This is a replay of the original small algebraic examples, not an independent implementation of the analytic bridge or a source-enclosure computation.
