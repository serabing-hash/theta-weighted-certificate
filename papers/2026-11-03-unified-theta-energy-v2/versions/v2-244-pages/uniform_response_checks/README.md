# Uniform response arithmetic checks

This packet accompanies the analytic note *Uniform response brackets at a fixed Gamma split and an obstruction to fixed graph debits*. It checks exact response constants, noncommuting finite block examples, and elementary complete-correction/prime-tail bounds. It is not a new theta positivity certificate.

## Reproduce

Run the exact rational checks with Python 3:

    python3 check_response.py
    python3 independent_response_audit.py

For the two elementary ball-arithmetic checks, use Python-FLINT 0.9.0 as pinned in requirements.txt:

    python3 check_theta_constants.py
    python3 independent_scalar_audit.py

The scripts write their named JSON result files beside themselves. The first two require only Python's standard library. The supplied outputs were reproduced successfully. The original scalar checker uses 160-bit balls; the independent checker uses 256-bit balls and the quarter-digamma identity.

## What passes

- The exact error e_n=(324/65527)(9/65536)^(2n), with degree one below 9.33e-11 and degree three below 1.76e-18.
- The correct indexing of paired powers, both bracket orders, and both monotonicities in synthetic noncommuting examples.
- The inverse-energy and residual identities without simultaneous diagonalization.
- Same-split Schur stability in a separate two-low/three-high example.
- The elementary complete-correction envelope below 36 and integer tail beyond 32 below 3.609e-18. Every prime power is included by the integer majorant.
- The same-low-space prime Schur error below 3.610e-18 and combined cubic-plus-prime error below 5.37e-18.

The independent rational script performs 2103 exact checks. Finite examples include positive, zero, and negative Schur operators. A zero Schur operator can have negative finite lower brackets; no strict positive endpoint gap is inferred.

## What remains outside the packet

The analytic proof treats complete possibly infinite-dimensional operators. A finite response polynomial is not a finite response-space compression: every term still contains the complete high Gamma operator and exact spectral projections. These scripts do not evaluate any actual theta low matrix, projected moment, spectral projection, or Gamma inverse. They do not pay spatial-integration or matrix-enclosure errors. The theta/shift envelopes and domain assumptions are retained inputs.

Projected exhaustion is conditional on the whole exact zero-jet form-core input, including every required frequency and multiplicity jet. The whole-low theta Schur sign, global one-half inequality, and RH remain unproved. Fixed M=32 does not give a vanishing prime-tail error. Existing finite five/six-direction certificates are not invalidated by the asymptotic obstruction to the fixed raw graph debit.

## Source binding

The reviewed source uniform_response.tex has SHA256 b5155d5e7eb3ecbe68a8b4731d52c644fffae2f569ee57b296db533b20ab4fe6. Both source verification scripts are preserved without changes. SHA256SUMS.txt binds all files in this packet other than itself.
