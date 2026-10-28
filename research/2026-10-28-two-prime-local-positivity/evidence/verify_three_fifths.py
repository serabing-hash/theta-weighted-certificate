#!/usr/bin/env python3
"""Prepared, unexecuted sufficient Schur certificate at B=3/5.

Fixed parameters: python-flint 0.9.0; precision 256; M=16, N=8192, J=24.
Requires a separate explicit authorization before any numerical execution.
The command-line flag is an accidental-execution guard, not authorization.
No parameter search, retry, precision escalation, or eigenvalue calculation.
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def verify():
    # Numerical imports and all source evaluations occur only after the CLI guard.
    import flint
    from flint import arb, acb, ctx

    if flint.__version__ != "0.9.0":
        raise RuntimeError("This fixed verifier requires python-flint==0.9.0")
    if not __debug__:
        raise RuntimeError("Assertions must remain enabled; do not use -O")
    ctx.prec = 256
    M, N, J = 16, 8192, 24
    pi = arb.pi()
    B = arb(3) / 5
    omega = pi / B
    primes = (2, 3)
    shifts = [arb(p).log() for p in primes]
    weights = [shifts[i] / arb(p).sqrt() for i, p in enumerate(primes)]
    sigma = sum(weights, arb(0))
    kappa = arb(6) / 5
    kappa_N = arb(36) / 5

    # Precisely prime powers 2 and 3 are active; both are reflection channels.
    assert B < shifts[0] < shifts[1] < 2 * B < arb(4).log()
    k = [omega * n for n in range(N + 1)]
    b = [(arb(1) / B).sqrt()] + [(arb(2) / B).sqrt()] * (M - 1)
    v = [b[m] * ((-1) ** m) for m in range(M)]
    sh = (B / 2).sinh()
    c = [v[m] * sh / (2 * (arb(1) / 4 + k[m] ** 2)) for m in range(M)]
    psi = [acb(arb(1) / 4, k[n] / 2).digamma() for n in range(N + 1)]
    D = [z.real - pi.log() for z in psi]
    U = [acb(arb(1) / 4).polygamma(1).real / 4]
    U += [psi[n].imag / (2 * k[n]) for n in range(1, N + 1)]
    # Redundant numerical sanity checks of newly proved symbolic floors.
    assert D[M] - sigma > kappa
    assert D[N] - sigma > kappa_N

    alpha = [arb(2 * j) + arb(1) / 2 for j in range(J)]
    wt = [x * x * (-2 * x * B).exp() for x in alpha]
    lowV = [[1 / (x * x + k[m] * k[m]) for x in alpha] for m in range(M)]
    first = arb(2 * J) + arb(1) / 2
    exp_error = (-2 * first * B).exp() / (first * first * (1 - (-4 * B).exp()))
    Sdiag = [U[0]] + [
        psi[m].imag / (4 * k[m])
        + acb(arb(1) / 4, k[m] / 2).polygamma(1).real / 8
        for m in range(1, M)
    ]

    def row(n):
        bn = (arb(1) / B).sqrt() if n == 0 else (arb(2) / B).sqrt()
        en = (-1) ** n
        kn = k[n]
        kn2 = kn * kn
        nv = [wt[j] / (alpha[j] * alpha[j] + kn2) for j in range(J)]
        cn = bn * en * sh / (2 * (arb(1) / 4 + kn2))
        out = []
        for m in range(M):
            km = k[m]
            km2 = km * km
            val = Sdiag[m] if n == m else (kn2 * U[n] - km2 * U[m]) / (kn2 - km2)
            val -= sum((nv[j] * lowV[m][j] for j in range(J)), arb(0))
            # Signed b_n*b_m factors are applied after enclosing the inner tail.
            val += arb(0, exp_error.upper())
            boundary = bn * en * v[m] * val
            prime = arb(0)
            for s, a in zip(shifts, weights):
                if n >= M:
                    integral = -(
                        kn * ((-1) ** m) * (kn * (s - B)).sin()
                        + km * en * (km * (B - s)).sin()
                    ) / (kn2 - km2)
                else:
                    length = 2 * B - s
                    diff = kn - km
                    total = kn + km
                    sd = arb(1) if n == m else (diff * length / 2).sin() / (diff * length / 2)
                    st = arb(1) if n + m == 0 else (total * length / 2).sin() / (total * length / 2)
                    integral = length / 2 * (
                        sd * (total * s / 2).cos() + st * (diff * s / 2).cos()
                    )
                prime += a * bn * b[m] * integral
            value = boundary + 4 * cn * c[m] - prime
            if n == m:
                value += D[n]
            out.append(value)
        return out

    A = [row(n) for n in range(M)]
    # Exact analytic symmetry permits one common enclosing triangle.
    for i in range(M):
        for j in range(i):
            assert (A[i][j] - A[j][i]).contains(0)
            A[j][i] = A[i][j]
    C = [[arb(0) for _ in range(M)] for _ in range(M)]
    for n in range(M, N):
        r = row(n)
        inv = 1 / (D[n] - sigma)
        for i in range(M):
            for j in range(i + 1):
                C[i][j] += r[i] * r[j] * inv
        if n % 1024 == 0:
            print(f"Enclosed modes through {n}", flush=True)

    E0 = (-B).exp() / (1 - (-4 * B).exp())
    kN = k[N]
    constants = []
    for m in range(M):
        km = k[m]
        den = 1 - (km / kN) ** 2
        Hm = arb(0) if m == 0 else 1 + pi * km / 4
        constants.append(
            b[m] * (Hm / den + E0 + sigma * (km + km * km / kN) / den)
            + 2 * sh * abs(c[m])
        )
    tail_rank = 4 * (pi / 4 + sigma + 1 / kN) ** 2 / (
        B * kappa_N * omega ** 2 * (N - 1)
    )
    tail_scalar = 4 * sum((x * x for x in constants), arb(0)) / (
        3 * B * kappa_N * omega ** 4 * (N - 1) ** 3
    )
    for i in range(M):
        for j in range(i + 1):
            C[i][j] += tail_rank * v[i] * v[j]
            if i == j:
                C[i][j] += tail_scalar
            C[j][i] = C[i][j]
    trace = sum((C[i][i] for i in range(M)), arb(0))
    F = [[A[i][j] - C[i][j] for j in range(M)] for i in range(M)]

    # One fixed LDL factorization of F itself. There is no guessed old margin.
    L = [[arb(0) for _ in range(M)] for _ in range(M)]
    pivots = []
    for i in range(M):
        L[i][i] = arb(1)
        pivot = F[i][i] - sum((L[i][j] ** 2 * pivots[j] for j in range(i)), arb(0))
        assert pivot > 0, f"Positive Schur pivot not certified at {i}: {pivot}"
        pivots.append(pivot)
        for n in range(i + 1, M):
            L[n][i] = (
                F[n][i] - sum((L[n][j] * L[i][j] * pivots[j] for j in range(i)), arb(0))
            ) / pivot

    # Unit lower triangular inversion, outward-rounded once, not a second run.
    Linv = [[arb(0) for _ in range(M)] for _ in range(M)]
    for i in range(M):
        Linv[i][i] = arb(1)
        for j in range(i):
            Linv[i][j] = -sum((L[i][k0] * Linv[k0][j] for k0 in range(j, i)), arb(0))

    def exact_endpoint(x, upper):
        assert x.is_finite(), "Nonfinite interval cannot be exported as evidence"
        endpoint = x.upper() if upper else x.lower()
        assert endpoint.is_finite() and endpoint.is_exact()
        rational = endpoint.fmpq()
        # Directed endpoints and the exact export round-trip are checked again.
        roundtrip = arb(rational)
        assert roundtrip.is_exact() and roundtrip == endpoint
        assert x <= roundtrip if upper else roundtrip <= x
        return Fraction(int(rational.p), int(rational.q))

    def rational_text(q):
        return f"{q.numerator}/{q.denominator}"

    d_star = min(exact_endpoint(p, False) for p in pivots)
    assert d_star > 0
    inverse_norm_upper = Fraction(0)
    for i in range(M):
        for j in range(i + 1):
            bound = max(abs(exact_endpoint(Linv[i][j], False)), abs(exact_endpoint(Linv[i][j], True)))
            inverse_norm_upper += bound * bound
    assert inverse_norm_upper >= M
    mu = d_star / inverse_norm_upper
    tau = exact_endpoint(trace, True)
    assert tau > 0 and mu > 0
    kappa_q = Fraction(6, 5)
    gap = min(mu * kappa_q / (kappa_q + 2 * tau), kappa_q / 2)
    assert gap > 0
    assert gap * (1 + 2 * tau / kappa_q) <= mu
    assert gap * 2 / kappa_q <= 1

    def ball_record(x):
        return {
            "lower_rational": rational_text(exact_endpoint(x, False)),
            "upper_rational": rational_text(exact_endpoint(x, True)),
            "display": str(x),
        }

    def matrix_record(matrix):
        return [[ball_record(x) for x in row0] for row0 in matrix]

    return {
        "status": "PASS_INTERVAL_SCHUR_CERTIFICATE",
        "scope": "real even minimum compact-support Gamma-form domain, 0 < B <= 3/5",
        "fixed_parameters": {
            "support_radius": "3/5", "precision_bits": ctx.prec,
            "low_modes": M, "tail_start": N, "exponential_terms": J,
            "active_prime_powers": list(primes), "python_flint_version": flint.__version__,
        },
        "schur_gap_policy": "One strict LDL of F, then pivot lower bound divided by inverse-L Frobenius upper bound",
        "q_lower_bound_L2": rational_text(gap),
        "schur_margin_low_mode_L2": rational_text(mu),
        "pivot_lower_bound": rational_text(d_star),
        "inverse_L_frobenius_squared_upper_bound": rational_text(inverse_norm_upper),
        "coupling_trace_upper_bound": rational_text(tau),
        "high_block_floor_used": "6/5",
        "tail_floor_used": "36/5",
        "high_block_floor_at_M": ball_record(D[M] - sigma),
        "high_block_floor_at_N": ball_record(D[N] - sigma),
        "prime_weights": [ball_record(a) for a in weights],
        "prime_weight_sum": ball_record(sigma),
        "rank_one_tail_coefficient": ball_record(tail_rank),
        "scalar_tail_coefficient": ball_record(tail_scalar),
        "coupling_bound_trace": ball_record(trace),
        "exponential_entry_error": ball_record(exp_error),
        "witness_matrices": {
            "A": matrix_record(A), "C": matrix_record(C), "F": matrix_record(F),
            "L": matrix_record(L), "L_inverse": matrix_record(Linv),
            "LDL_pivots": [ball_record(p) for p in pivots],
        },
        "trust_boundary": "Analytic reduction and complete-tail bounds, this source, python-flint/FLINT, Python and the execution environment; not proof-assistant verification or an independent implementation.",
        "global_all_radii_positivity": "NOT_PROVED",
        "RH": "NOT_PROVED",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-approved-once", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.execute_approved_once:
        parser.error("Disabled preparation: a separately authorized run and --execute-approved-once are required")
    if not __debug__:
        raise RuntimeError("Run without -O")
    if args.output.exists():
        raise FileExistsError("Refusing to overwrite an existing output")
    result = verify()
    result["verifier_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    data = json.dumps(result, indent=2) + "\n"
    if len(data.encode("utf-8")) > 8 * 1024 * 1024:
        raise RuntimeError("Witness output exceeds the fixed 8 MiB output cap")
    with args.output.open("x", encoding="utf-8") as stream:
        stream.write(data)
    print(data)


if __name__ == "__main__":
    main()
