#!/usr/bin/env python3
"""Prepared, unexecuted positive-defect Schur candidate at B=3/4.

Fixed parameters: python-flint 0.9.0; precision 256; M=32, N=16384, J=32.
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
    M, N, J = 32, 16384, 32
    pi = arb.pi()
    B = arb(3) / 4
    omega = pi / B
    prime_powers = (2, 3, 4)
    shifts = [arb(p).log() for p in prime_powers]
    weights = [shifts[0] / arb(2).sqrt(), shifts[1] / arb(3).sqrt(), shifts[0] / 2]
    # sigma bounds signed row tails. rho is the improved mixed-prime cap.
    # The prime-power 4 weight is Lambda(4)/sqrt(4) = log(2)/2.
    sigma = sum(weights, arb(0))
    mixed_sum = weights[2] + weights[1]
    rho = (mixed_sum + (mixed_sum ** 2 + 8 * weights[0] ** 2).sqrt()) / 2
    kappa = arb(8) / 5
    kappa_N = arb(39) / 5
    correction_coefficient = arb(8) / 25
    feature_rank_one_floor = arb(2) / 5
    assert rho < arb(27) / 20

    # Prime 2 has same-side translations and reflection; 3 and 4 reflect.
    # The weighted center/leaf estimate gives rho, not sigma.
    assert 0 < shifts[0] < B < arb(3) * shifts[0] / 2
    assert B < shifts[1] < shifts[2] < 2 * B < arb(5).log()
    assert B < (shifts[0] + shifts[1]) / 2
    assert shifts[1] + 2 * B < 4 * shifts[0]
    assert rho - weights[0] - weights[1] > arb(43) / 380
    # The explicit slack feature is sqrt(8) times 1_[1/8,1/4].
    # It is used only as a bounded L2 functional, not a Gamma-domain multiplier.
    assert B - shifts[0] < arb(1) / 8 < arb(1) / 4 < shifts[1] - B
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
    assert D[M] - rho > kappa
    assert D[N] - rho > kappa_N

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
                # Signed s-B is negative for prime 2: do not take abs or clip.
                # Unified integral over (s-B,B) includes both translations.
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
    C0 = [[arb(0) for _ in range(M)] for _ in range(M)]
    zeta = [arb(0) for _ in range(M)]
    feature_inverse_norm = arb(0)
    feature_prefactor = arb(8).sqrt() * (arb(2) / B).sqrt()
    for n in range(M, N):
        r = row(n)
        inv = 1 / (D[n] - rho)
        feature_n = feature_prefactor * ((k[n] / 4).sin() - (k[n] / 8).sin()) / k[n]
        feature_inverse_norm += feature_n ** 2 * inv
        for i in range(M):
            zeta[i] += feature_n * r[i] * inv
            for j in range(i + 1):
                C0[i][j] += r[i] * r[j] * inv
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
            C0[i][j] += tail_rank * v[i] * v[j]
            if i == j:
                C0[i][j] += tail_scalar
            C0[j][i] = C0[i][j]

    # One use of E=rho*I-P: E_hh >= (2/5)|phi><phi|, where phi is
    # the finite projection of the slack feature to M <= n < N.
    # E >= I/54 was used in its analytic derivation, not added again to K.
    # No alternative edge-energy inverse correction is stacked here.
    assert feature_inverse_norm >= 0
    assert feature_inverse_norm < arb(5) / 8
    C_new = [[arb(0) for _ in range(M)] for _ in range(M)]
    for i in range(M):
        for j in range(i + 1):
            C_new[i][j] = C0[i][j] - correction_coefficient * zeta[i] * zeta[j]
            C_new[j][i] = C_new[i][j]
    # Use the uncorrected complete bound C0 for the full-norm conversion.
    # This does not assume a numerically certified PSD decomposition of C_new.
    trace = sum((C0[i][i] for i in range(M)), arb(0))
    F = [[A[i][j] - C_new[i][j] for j in range(M)] for i in range(M)]

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
    kappa_q = Fraction(8, 5)
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
        "status": "PASS_INTERVAL_POSITIVE_DEFECT_SCHUR_CERTIFICATE",
        "scope": "real even minimum compact-support Gamma-form domain, 0 < B <= 3/4",
        "fixed_parameters": {
            "support_radius": "3/4", "precision_bits": ctx.prec,
            "low_modes": M, "tail_start": N, "exponential_terms": J,
            "active_prime_powers": list(prime_powers), "python_flint_version": flint.__version__,
        },
        "schur_gap_policy": "One strict LDL of F, then pivot lower bound divided by inverse-L Frobenius upper bound",
        "q_lower_bound_L2": rational_text(gap),
        "schur_margin_low_mode_L2": rational_text(mu),
        "pivot_lower_bound": rational_text(d_star),
        "inverse_L_frobenius_squared_upper_bound": rational_text(inverse_norm_upper),
        "coupling_trace_upper_bound": rational_text(tau),
        "high_block_floor_used": "8/5",
        "tail_floor_used": "39/5",
        "high_block_floor_at_M": ball_record(D[M] - rho),
        "high_block_floor_at_N": ball_record(D[N] - rho),
        "prime_weights": [ball_record(a) for a in weights],
        "row_tail_weight_sum_sigma": ball_record(sigma),
        "high_operator_cap_rho": ball_record(rho),
        "prime_shifts": [ball_record(s) for s in shifts],
        "rank_one_tail_coefficient": ball_record(tail_rank),
        "scalar_tail_coefficient": ball_record(tail_scalar),
        "uncorrected_complete_coupling_bound_trace": ball_record(trace),
        "full_norm_trace_policy": "Use trace(C0), not trace(C_new), for the full-norm gap",
        "positive_defect_correction": {
            "feature": "sqrt(8) times indicator_[1/8,1/4] on the positive half interval",
            "feature_projection_modes": {"first": M, "last_inclusive": N - 1},
            "feature_coefficient_formula": "sqrt(8)*sqrt(2/B)*(sin(k_n/4)-sin(k_n/8))/k_n",
            "tail_norm_squared_analytic_bound": "16/(3*(N-1))",
            "defect_coercivity_analytic_floor": "1/54; used only to prove the finite feature bound",
            "finite_feature_form_floor": ball_record(feature_rank_one_floor),
            "finite_feature_inverse_norm": ball_record(feature_inverse_norm),
            "cost_subtraction_coefficient": ball_record(correction_coefficient),
            "zeta": [ball_record(x) for x in zeta],
            "zeta_nonzero_coordinates_certified": [
                i for i in range(M) if zeta[i] > 0 or zeta[i] < 0
            ],
            "strict_correction_status": (
                "CERTIFIED_NONZERO" if any(x > 0 or x < 0 for x in zeta)
                else "NOT_CERTIFIED; no assertion that zeta vanishes"
            ),
            "resource_policy": "One finite-feature lower bound of E; no added I/54 or edge-energy correction",
        },
        "exponential_entry_error": ball_record(exp_error),
        "witness_matrices": {
            "A": matrix_record(A), "C0": matrix_record(C0),
            "C_new": matrix_record(C_new), "F": matrix_record(F),
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
