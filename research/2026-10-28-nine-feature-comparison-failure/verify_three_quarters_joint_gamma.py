#!/usr/bin/env python3
"""Prepared, unexecuted joint Gamma/pole Schur candidate at B=3/4.

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


def verify(export):
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
    # All block labels below are feature resources, NOT the J=32
    # exponential-subtraction index used by the unchanged actual row().
    feature_count = 9
    blocks = ((4, 16), (16, 64), (64, 256), (256, 1024))
    resource_alpha = [arb(2 * j) + arb(1) / 2 for j in range(1024)]
    resource_alpha2 = [a * a for a in resource_alpha]
    block_scale = [(arb(31) / (32 * (stop - start))).sqrt()
                   for start, stop in blocks]
    individual_num = [(B.exp() - 1).sqrt() / 2]
    individual_num += [resource_alpha[j] * (1 - (-2 * resource_alpha[j] * B).exp()).sqrt()
                       for j in range(1, 4)]
    assert 1 - (-2 * resource_alpha[1] * B).exp() > arb(31) / 32
    slack_scale = (arb(9) / 20).sqrt()
    sqrt3 = arb(3).sqrt()
    period12 = (arb(0), 3 - sqrt3, arb(0), -2 * sqrt3, arb(-6), -3 - sqrt3,
                arb(0), 3 + sqrt3, arb(6), 2 * sqrt3, arb(0), -3 + sqrt3)
    W_inverse = [arb(881) / 800] + [arb(2527) / 2500] * 8

    def feature_row(n):
        # This function is evaluated only for M <= n < N in an approved run.
        # Literal finite positive sums are the frozen choice; no digamma switch.
        kn2 = k[n] * k[n]
        bn_en = (arb(2) / B).sqrt() * ((-1) ** n)
        values = [slack_scale * period12[n % 12] / (pi * n)]
        values += [bn_en * individual_num[j] / (resource_alpha2[j] + kn2)
                   for j in range(4)]
        for block_index, (start, stop) in enumerate(blocks):
            total = sum((resource_alpha[j] / (resource_alpha2[j] + kn2)
                         for j in range(start, stop)), arb(0))
            values.append(block_scale[block_index] * bn_en * total)
        return values

    C0 = [[arb(0) for _ in range(M)] for _ in range(M)]
    Z = [[arb(0) for _ in range(feature_count)] for _ in range(M)]
    G = [[arb(0) for _ in range(feature_count)] for _ in range(feature_count)]
    for n in range(M, N):
        r = row(n)
        inv = 1 / (D[n] - rho)
        features = feature_row(n)
        for i in range(M):
            for j in range(i + 1):
                C0[i][j] += r[i] * r[j] * inv
            for a in range(feature_count):
                Z[i][a] += r[i] * features[a] * inv
        for a in range(feature_count):
            for b0 in range(a + 1):
                G[a][b0] += features[a] * features[b0] * inv
        if n % 1024 == 0:
            print(f"Enclosed modes through {n}", flush=True)
    for a in range(feature_count):
        for b0 in range(a):
            G[b0][a] = G[a][b0]

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
    trace = sum((C0[i][i] for i in range(M)), arb(0))
    H9 = [[G[a][b0] + (W_inverse[a] if a == b0 else 0)
           for b0 in range(feature_count)] for a in range(feature_count)]
    zeta = [Z[m][0] / slack_scale for m in range(M)]
    chi = G[0][0] / (arb(9) / 20)
    assert chi >= 0 and chi < arb(5) / 8
    d_gamma = [G[a][0] / slack_scale for a in range(1, feature_count)]
    lam = 1 / (arb(881) / 360 + chi)
    Y_s = [[Z[m][a] - lam * zeta[m] * d_gamma[a - 1]
            for a in range(1, feature_count)] for m in range(M)]
    F_failed_comparison = [[A[i][j] - C0[i][j] + (arb(8) / 25) * zeta[i] * zeta[j]
                            for j in range(M)] for i in range(M)]

    def exact_endpoint(x, upper):
        assert x.is_finite(), "Nonfinite interval cannot be exported as evidence"
        endpoint = x.upper() if upper else x.lower()
        assert endpoint.is_finite() and endpoint.is_exact()
        rational = endpoint.fmpq()
        roundtrip = arb(rational)
        assert roundtrip.is_exact() and roundtrip == endpoint
        assert x <= roundtrip if upper else roundtrip <= x
        return Fraction(int(rational.p), int(rational.q))

    def rational_text(q):
        return f"{q.numerator}/{q.denominator}"

    def ball_record(x):
        return {
            "lower_rational": rational_text(exact_endpoint(x, False)),
            "upper_rational": rational_text(exact_endpoint(x, True)),
            "display": str(x),
        }

    def matrix_record(matrix):
        return [[ball_record(x) for x in row0] for row0 in matrix]

    def ldl_fixed(matrix):
        size = len(matrix)
        lower = [[arb(0) for _ in range(size)] for _ in range(size)]
        pivots0 = []
        for i in range(size):
            lower[i][i] = arb(1)
            pivot = matrix[i][i] - sum(
                (lower[i][j] ** 2 * pivots0[j] for j in range(i)), arb(0))
            if not pivot > 0:
                return lower, pivots0, (i, pivot)
            pivots0.append(pivot)
            for n in range(i + 1, size):
                lower[n][i] = (matrix[n][i] - sum(
                    (lower[n][j] * lower[i][j] * pivots0[j] for j in range(i)), arb(0))) / pivot
        return lower, pivots0, None

    def inverse_from_ldl(lower, pivots0):
        size = len(lower)
        inverse = [[arb(0) for _ in range(size)] for _ in range(size)]
        for col in range(size):
            forward = []
            for i in range(size):
                forward.append((arb(1) if i == col else arb(0)) - sum(
                    (lower[i][j] * forward[j] for j in range(i)), arb(0)))
            scaled = [forward[i] / pivots0[i] for i in range(size)]
            solution = [arb(0) for _ in range(size)]
            for i in range(size - 1, -1, -1):
                solution[i] = scaled[i] - sum(
                    (lower[j][i] * solution[j] for j in range(i + 1, size)), arb(0))
            for i in range(size):
                inverse[i][col] = solution[i]
        # Analytic symmetry: either solve orientation encloses the same entry.
        for i in range(size):
            for j in range(i):
                assert (inverse[i][j] - inverse[j][i]).contains(0)
                inverse[j][i] = inverse[i][j]
        return inverse

    common = {
        "status": "NOT_CERTIFICATE",
        "stage": "PRE_INVERSE",
        "scope": "Diagnostic intervals only; no local positivity, global positivity or RH claim",
        "fixed_parameters": {
            "support_radius": "3/4", "precision_bits": ctx.prec,
            "low_modes": M, "tail_start": N, "exponential_terms": J,
            "gamma_resource_labels": {"first": 0, "last_inclusive": 1023},
            "active_prime_powers": list(prime_powers), "python_flint_version": flint.__version__,
        },
        "selected_resource_contract": {
            "analytic_note": "rh_joint_gamma_pole_finite_schur_resource_2026-10-28.md",
            "analytic_note_sha256": "9890c782ac8d4c419eea11e956c1374873a257f040102d45b98c7912e29c0d25",
            "analytic_audit_sha256": "124e1073f69fa1edded734f39b76c7c3f4d1968403889db241cc883fd26a479b",
            "individual_gamma_labels": [0, 1, 2, 3],
            "gamma_blocks_half_open": [list(block) for block in blocks],
            "block_formula": "sqrt(31/(32*m))*b_n*(-1)^n*sum_j alpha_j/(alpha_j^2+k_n^2), literal finite sum",
            "merged_zero_pole_formula": "b_n*(-1)^n*sqrt(exp(B)-1)/(2*(1/4+k_n^2))",
            "raw_slack_coefficient_squared": "9/20",
            "tail_Theta_diagonal": ["3/16000"] + ["1/50000"] * 8,
            "W_diagonal": ["800/881"] + ["2500/2527"] * 8,
            "resource_policy": "Split E once: 9/10 for slack, 1/10 >= I/540 for all joint tails. No old 8/25 or I/54 stacked into the new high bound.",
            "J_exp_is_not_gamma_resource_cutoff": True,
            "feature_independence": "Analytic rank nine; not a certificate of nonzero compression to the low cross block",
        },
        "high_block_floor_used": "8/5", "tail_floor_used": "39/5",
        "high_block_floor_at_M": ball_record(D[M] - rho),
        "high_block_floor_at_N": ball_record(D[N] - rho),
        "prime_weights": [ball_record(a) for a in weights],
        "prime_shifts": [ball_record(s) for s in shifts],
        "row_tail_weight_sum_sigma": ball_record(sigma),
        "high_operator_cap_R": ball_record(rho),
        "rank_one_tail_coefficient": ball_record(tail_rank),
        "scalar_tail_coefficient": ball_record(tail_scalar),
        "exponential_entry_error": ball_record(exp_error),
        "uncorrected_complete_coupling_bound_trace": ball_record(trace),
        "full_norm_trace_policy": "Use trace(C0), never infer a norm margin from trace(C_new) alone",
        "finite_overlap_diagnostics": {
            "zeta": [ball_record(x) for x in zeta],
            "chi": ball_record(chi), "lambda": ball_record(lam),
            "Y_s": matrix_record(Y_s),
            "zeta_nonzero_coordinates_certified": [i for i in range(M) if zeta[i] > 0 or zeta[i] < 0],
            "gamma_overlap_nonzero_coordinates_certified": [
                [i, a] for i in range(M) for a in range(8) if Y_s[i][a] > 0 or Y_s[i][a] < 0],
            "interpretation": "An empty list is inconclusive, not proof of vanishing; neither list is a positivity certificate",
        },
        "witness_matrices": {
            "A": matrix_record(A), "C0": matrix_record(C0), "Z": matrix_record(Z),
            "G": matrix_record(G), "H9": matrix_record(H9),
            "F_failed_formula_comparison": matrix_record(F_failed_comparison),
        },
        "trust_boundary": "Analytic reduction and complete tails, this source, python-flint/FLINT, Python and execution environment; no proof-assistant or independent implementation claim",
        "global_all_radii_positivity": "NOT_PROVED", "RH": "NOT_PROVED",
    }
    H_lower, H_pivots, H_failure = ldl_fixed(H9)
    common["witness_matrices"]["H9_LDL_L"] = matrix_record(H_lower)
    common["witness_matrices"]["H9_LDL_pivots"] = [ball_record(x) for x in H_pivots]
    if H_failure is not None:
        i, pivot = H_failure
        common["stage"] = "FAILED_SMALL_INVERSE_GATE"
        common["failed_gate"] = {"matrix": "H9", "index": i, "pivot": ball_record(pivot)}
        export("diagnostic", common)
        print(f"Small inverse pivot not certified at {i}: {pivot}", flush=True)
        return False

    H_inverse = inverse_from_ldl(H_lower, H_pivots)
    correction = [[arb(0) for _ in range(M)] for _ in range(M)]
    solved = [[sum((H_inverse[a][b0] * Z[m][b0] for b0 in range(feature_count)), arb(0))
               for a in range(feature_count)] for m in range(M)]
    for i in range(M):
        for j in range(i + 1):
            correction[i][j] = sum((Z[i][a] * solved[j][a] for a in range(feature_count)), arb(0))
            correction[j][i] = correction[i][j]
    C_new = [[C0[i][j] - correction[i][j] for j in range(M)] for i in range(M)]
    F = [[A[i][j] - C_new[i][j] for j in range(M)] for i in range(M)]
    common["stage"] = "PRE_GATE_NOT_CERTIFICATE"
    common["witness_matrices"].update({
        "H9_inverse": matrix_record(H_inverse), "Z_H9_inverse": matrix_record(solved),
        "joint_correction": matrix_record(correction), "C_new": matrix_record(C_new), "F9": matrix_record(F),
    })
    diagnostic = export("diagnostic", common)

    # Exactly one final fixed-index LDL. Failure keeps the already written evidence.
    L, pivots, failure = ldl_fixed(F)
    if failure is not None:
        i, pivot = failure
        export("failure", {
            "status": "FAILED_POSITIVITY_GATE_NOT_CERTIFICATE", "matrix": "F9",
            "failed_pivot_index": i, "failed_pivot": ball_record(pivot),
            "diagnostic": diagnostic,
            "positive_prefix_pivots": [ball_record(x) for x in pivots],
            "interpretation": "Failure of this sufficient comparison; not a negative original-form witness or RH counterexample",
        })
        print(f"Positive Schur pivot not certified at {i}: {pivot}", flush=True)
        return False

    Linv = [[arb(0) for _ in range(M)] for _ in range(M)]
    for i in range(M):
        Linv[i][i] = arb(1)
        for j in range(i):
            Linv[i][j] = -sum((L[i][k0] * Linv[k0][j] for k0 in range(j, i)), arb(0))
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
    export("success", {
        "status": "PASS_INTERVAL_JOINT_GAMMA_SCHUR_CERTIFICATE",
        "scope": "real even minimum compact-support Gamma-form domain, 0 < B <= 3/4",
        "diagnostic": diagnostic,
        "q_lower_bound_L2": rational_text(gap),
        "schur_margin_low_mode_L2": rational_text(mu),
        "pivot_lower_bound": rational_text(d_star),
        "inverse_L_frobenius_squared_upper_bound": rational_text(inverse_norm_upper),
        "coupling_trace_upper_bound": rational_text(tau),
        "witness_matrices": {"L": matrix_record(L), "L_inverse": matrix_record(Linv),
                             "LDL_pivots": [ball_record(p) for p in pivots]},
        "schur_gap_policy": "Fixed LDL of F9 followed by exact pivot/inverse-factor and trace(C0) norm conversion",
        "global_all_radii_positivity": "NOT_PROVED", "RH": "NOT_PROVED",
    })
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-approved-once", action="store_true")
    parser.add_argument("--output", type=Path, required=True,
                        help="Success JSON name; diagnostic/failure siblings are created exclusively")
    args = parser.parse_args()
    if not args.execute_approved_once:
        parser.error("Disabled preparation: a separately authorized run and --execute-approved-once are required")
    if not __debug__:
        raise RuntimeError("Run without -O")
    paths = {
        "success": args.output,
        "diagnostic": args.output.with_name(args.output.stem + ".diagnostic.json"),
        "failure": args.output.with_name(args.output.stem + ".failure.json"),
    }
    if len(set(paths.values())) != 3:
        raise RuntimeError("Output paths must be distinct")
    for path in paths.values():
        if path.exists():
            raise FileExistsError("Refusing to overwrite an existing output or sibling")
    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    total_bytes = 0
    written = set()

    def export(kind, payload):
        nonlocal total_bytes
        if kind in written:
            raise RuntimeError("Refusing a duplicate artifact kind")
        payload["verifier_sha256"] = source_hash
        data = (json.dumps(payload, indent=2) + "\n").encode("utf-8")
        if total_bytes + len(data) > 8 * 1024 * 1024:
            raise RuntimeError("All-inclusive fixed 8 MiB output cap exceeded; no new artifact written")
        path = paths[kind]
        with path.open("xb") as stream:
            stream.write(data)
        total_bytes += len(data)
        written.add(kind)
        digest = hashlib.sha256(data).hexdigest()
        print(f"Wrote {kind}: {path.name}, {len(data)} bytes, sha256 {digest}", flush=True)
        return {"filename": path.name, "sha256": digest, "bytes": len(data)}

    success = verify(export)
    if not success:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
