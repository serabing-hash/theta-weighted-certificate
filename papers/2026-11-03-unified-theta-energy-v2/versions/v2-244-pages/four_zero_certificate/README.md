# Four-zero theta certificate reproducibility files

This directory contains the complete runnable arithmetic for the finite theorem in the integrated paper. It verifies q0[v] >= ||v||_H^2/32 on the span of W(x) cos(gamma_j x), where gamma_j are the first four positive zeta-zero ordinates, using the actual reciprocal-theta norm. It also verifies K_V^2 < 32.

## Run

Use Python 3.10 or later and python-flint 0.9.0. A clean virtual environment is recommended. Run without Python optimization flags so assertions remain enabled.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python certify_four_zeros.py
python check_sparse_constants.py
python export_rational_matrix.py
python check_rational_matrix.py
python audit_serialization.py
```

The producer regenerates CERTIFICATE.json and quadrature_checkpoint.json in this directory. The scalar check regenerates SPARSE_CONSTANTS.json. The exporter and final verifier regenerate RATIONAL_MATRIX.json and RATIONAL_CHECK.json. The serialization check reruns the producer and final verifier, and writes SERIALIZATION_CHECK.json. Files with those names are overwritten as part of reproduction; preserve copies if comparing the supplied outputs.

The initial complete producer replay took about 12 seconds with 38 MiB peak resident memory in the audit environment. Runtime varies by machine and load. The numerical settings are 160-bit balls, eight theta terms with an explicit omission bound, physical radius two with complete physical tails, 8192 interpolation cells, 128 positive Gamma labels with a full-Gamma interpolation debit, and every prime power through 32 with a complete operator tail.

## What is checked

The matrix sign checker uses only standard-library Fraction arithmetic. It proves positivity of every symmetric matrix in the exported rational entry boxes after a row-radius debit. It does not prove those boxes correspond to the analytical form on its own. Read the integrated paper's complete error argument and the producer together.

The source review and full replay reproduced the supplied finite-integral checkpoint, rational matrix, rational sign result, and sparse-scalar ledger byte for byte. The complete certificate differs only in elapsed time. A 256-bit repeat returned the same rational ledger and sign result. The live-ball check proves that all sixteen computed matrix balls remain enclosed after text serialization and outward rational export.

## Conditional sparse extension

The scalar verifier instantiates the displayed explicit recipe and checks its sufficient whole-ray inequalities at log(U)=2^512. The sparse infinite attachment remains conditional on the stated envelope, derivative, mixed-form, and sparse-family analytical estimates with those constants and threshold conditions. Arithmetic checks do not independently prove that analytical input. An unspecified existence statement for finite constants would not justify the explicit U.

The explicit scalar run uses total paired complexity at most 8 log(T). It does not cover all complete unit-window zero-jet spaces under the separate coarse count requiring coefficient 168. Actual permitted high zero jets must satisfy the stated smaller budget.

The finite four-dimensional certificate does not depend on the sparse hypotheses. Neither result proves a global one-half inequality, an increasing-dimensional low-space gap, all-window exhaustion, or the Riemann hypothesis. This is not formal proof-assistant verification or a separate full quadrature implementation.

REPLAY_VERIFICATION.json records the exact replay scope. SHA256SUMS.txt binds every supplied artifact. The first four original programs are preserved byte for byte from the supplied scientific source. The original standalone article, personal contact block, account provenance, and archives are not included here. Refer to the integrated paper for the full proof and project license.
