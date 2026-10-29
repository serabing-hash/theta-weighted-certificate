#!/usr/bin/env python3
"""Prepared, unexecuted actual full high-defect Schur candidate at B=4/5.

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


def verify(export, progress):
    # Numerical imports and all source evaluations occur only after the CLI guard.
    import flint
    from flint import arb, acb, arb_mat, ctx

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

    progress["matrix_record"] = matrix_record
    progress["stage"] = "SOURCE_INITIALIZATION"
    if flint.__version__ != "0.9.0":
        raise RuntimeError("This fixed verifier requires python-flint==0.9.0")
    if not __debug__:
        raise RuntimeError("Assertions must remain enabled; do not use -O")
    ctx.prec = 256
    M, N, J = 32, 16384, 32
    SOURCE_COLUMNS, TRIAL_COLUMNS = 64, 32
    pi = arb.pi()
    B = arb(4) / 5
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
    k = [omega * n for n in range(N + 1)]
    b = [(arb(1) / B).sqrt()] + [(arb(2) / B).sqrt()] * (SOURCE_COLUMNS - 1)
    v = [b[m] * ((-1) ** m) for m in range(SOURCE_COLUMNS)]
    sh = (B / 2).sinh()
    c = [v[m] * sh / (2 * (arb(1) / 4 + k[m] ** 2)) for m in range(SOURCE_COLUMNS)]
    psi = [acb(arb(1) / 4, k[n] / 2).digamma() for n in range(N + 1)]
    D = [z.real - pi.log() for z in psi]
    U = [acb(arb(1) / 4).polygamma(1).real / 4]
    U += [psi[n].imag / (2 * k[n]) for n in range(1, N + 1)]
    # Redundant numerical sanity checks of newly proved symbolic floors.
    assert D[M] - rho > kappa
    assert D[N] - rho > kappa_N

    alpha = [arb(2 * j) + arb(1) / 2 for j in range(J)]
    wt = [x * x * (-2 * x * B).exp() for x in alpha]
    lowV = [[1 / (x * x + k[m] * k[m]) for x in alpha] for m in range(SOURCE_COLUMNS)]
    first = arb(2 * J) + arb(1) / 2
    exp_error = (-2 * first * B).exp() / (first * first * (1 - (-4 * B).exp()))
    Sdiag = [U[0]] + [
        psi[m].imag / (4 * k[m])
        + acb(arb(1) / 4, k[m] / 2).polygamma(1).real / 8
        for m in range(1, SOURCE_COLUMNS)
    ]

    # Compute only full first-row entries and 64 direct diagonals. All omitted
    # exponential labels are enclosed BEFORE signed endpoint multiplication.
    alpha2 = [x*x for x in alpha]
    expwt = [(-2*x*B).exp() for x in alpha]
    b0, bnpositive = b[0], b[1]
    sqrt_two=arb(2).sqrt()
    d = [arb(1)] + [sqrt_two*((-1)**m) for m in range(1, SOURCE_COLUMNS)]
    direct_diagonal = []
    for m in range(SOURCE_COLUMNS):
        km = k[m]
        val = Sdiag[m] - sum((wt[j]*lowV[m][j]**2 for j in range(J)), arb(0))
        val += arb(0, exp_error.upper())
        prime = arb(0)
        for shift, weight in zip(shifts, weights):
            length = 2*B-shift
            sinc = arb(1) if m == 0 else (km*length).sin()/(km*length)
            integral = length/2*((km*shift).cos()+sinc)
            prime += weight*b[m]**2*integral
        direct_diagonal.append(D[m]+b[m]**2*val+4*c[m]**2-prime)
    firstrow = [direct_diagonal[0]]
    for n in range(1, N+1):
        kn = k[n]
        en = (-1)**n
        vn = bnpositive*en
        cn = vn*sh/(2*(arb(1)/4+kn**2))
        exponential = sum((expwt[j]/(alpha2[j]+kn**2) for j in range(J)), arb(0))
        inner = U[n]-exponential+arb(0, exp_error.upper())
        prime = sum((a*(kn*(shift-B)).sin()/kn for shift,a in zip(shifts,weights)), arb(0))
        firstrow.append(b0*vn*inner+4*c[0]*cn+b0*bnpositive*prime)
    progress["stage"] = "FIRST_ROW_COMPLETE"

    def row(n):
        if n == 0:
            return firstrow[:SOURCE_COLUMNS]
        n2=n*n
        dn=sqrt_two*((-1)**n)
        return [direct_diagonal[n] if m == n else
                (n2*d[m]*firstrow[n]-m*m*dn*firstrow[m])/(n2-m*m)
                for m in range(SOURCE_COLUMNS)]

    A = [row(n)[:M] for n in range(M)]
    for i in range(M):
        for j in range(i):
            assert (A[i][j]-A[j][i]).contains(0)
            A[j][i]=A[i][j]
    progress["complete_matrices"]["A"]=A
    progress["stage"]="BLOCK_GRAM_ACTUAL_ROWS"
    # Each block is 128 x 64. All 64 x 64 Gram products run in FLINT,
    # never in a Python per-row quadratic loop. X=(C,F), F actual H columns.
    gram=arb_mat(SOURCE_COLUMNS,SOURCE_COLUMNS)
    Btrial=[[arb(0) for _ in range(TRIAL_COLUMNS)] for _ in range(TRIAL_COLUMNS)]
    BLOCK_ROWS=128
    for start in range(M,N,BLOCK_ROWS):
        rows=[]
        weighted=[]
        for n in range(start,min(start+BLOCK_ROWS,N)):
            r=row(n)
            Kn=D[n]-rho
            assert Kn>kappa
            features=[r[M+j]-(Kn if n==M+j else arb(0)) for j in range(TRIAL_COLUMNS)]
            if n<SOURCE_COLUMNS:
                Btrial[n-M]=features[:]
            joined=r[:M]+features
            rows.append(joined)
            inv=1/Kn
            weighted.append([value*inv for value in joined])
        X=arb_mat(rows)
        Y=arb_mat(weighted)
        gram=gram+X.transpose()*Y
        if (start-M)%2048==0:
            print(f"Enclosed actual block through {min(start+BLOCK_ROWS,N)-1}",flush=True)
    Cfinite=[[gram[i,j] for j in range(M)] for i in range(M)]
    C0=[r[:] for r in Cfinite]
    G=[[gram[M+i,M+j] for j in range(TRIAL_COLUMNS)] for i in range(TRIAL_COLUMNS)]
    Z=[[gram[M+i,j] for j in range(M)] for i in range(TRIAL_COLUMNS)]
    for i in range(M):
        for j in range(i):
            assert (C0[i][j]-C0[j][i]).contains(0)
            C0[j][i]=C0[i][j]
            assert (G[i][j]-G[j][i]).contains(0)
            G[j][i]=G[i][j]
            assert (Btrial[i][j]-Btrial[j][i]).contains(0)
            Btrial[j][i]=Btrial[i][j]
    E0 = (-B).exp() / (1 - (-4 * B).exp())
    kN = k[N]
    constants = []
    for m in range(SOURCE_COLUMNS):
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
    # New B=4/5 direct signed two-term tail. No saved old-radius A input.
    tail_w_coefficient=arb(512)/1041816384077177475
    tail_remainder_coefficient=arb(51380224)/4194394783958568267303454125
    w=[v[m]*(4*sh**2-E0)-(k[m]**2/b0)*A[0][m] for m in range(M)]
    for i in range(M):
        for j in range(i+1):
            C0[i][j]+=tail_rank*v[i]*v[j]+tail_w_coefficient*w[i]*w[j]
            if i==j:
                C0[i][j]+=tail_remainder_coefficient*(i+1)**4
            C0[j][i]=C0[i][j]
    trace = sum((C0[i][i] for i in range(M)), arb(0))
    progress["complete_matrices"].update({"C0": C0, "Btrial": Btrial, "G": G, "Z_trial_by_low": Z})
    progress["stage"] = "RAW_TRIAL_TAIL"
    # Raw actual-trial tail: NO tail-floor divisor here.
    trial_tail_rank = 4 * (pi / 4 + sigma + 1 / kN) ** 2 / (
        B * omega ** 2 * (N - 1))
    trial_tail_scalar = 4 * sum((x * x for x in constants[M:SOURCE_COLUMNS]), arb(0)) / (
        3 * B * omega ** 4 * (N - 1) ** 3)
    Theta = [[trial_tail_rank * v[M + i] * v[M + j]
              + (trial_tail_scalar if i == j else arb(0))
              for j in range(TRIAL_COLUMNS)] for i in range(TRIAL_COLUMNS)]
    S = [[Btrial[i][j] + 54 * Theta[i][j] for j in range(TRIAL_COLUMNS)]
         for i in range(TRIAL_COLUMNS)]
    resource = [[S[i][j] + G[i][j] for j in range(TRIAL_COLUMNS)]
                for i in range(TRIAL_COLUMNS)]

    progress["complete_matrices"].update({"Theta": Theta, "S": S, "M_resource": resource})
    progress["stage"] = "PRE_INVERSE"
    common = {
        "status": "NOT_CERTIFICATE", "stage": "PRE_INVERSE",
        "scope": "Diagnostic intervals only; no local positivity, global positivity or RH claim",
        "fixed_parameters": {
            "support_radius": "4/5", "precision_bits": ctx.prec,
            "low_modes": M, "source_columns": SOURCE_COLUMNS,
            "actual_trial_indices": [M, SOURCE_COLUMNS - 1],
            "trial_columns": TRIAL_COLUMNS, "tail_start": N, "exponential_terms": J,
            "active_prime_powers": list(prime_powers), "python_flint_version": flint.__version__,
        },
        "selected_resource_contract": {
            "analytic_note": "rh_four_fifths_window_analytic_contract_2026-10-28.md",
            "analytic_note_sha256": "027a08079d74d85f9de09c52f2d13cd470e3dcdd3cd0a756a8a3c0418474f51d",
            "analytic_audit_sha256": "4083d1f5cfb6f66dd6c53bca79f72bd2d3fc352db3cfabda5069e57e85b5dff5",
            "feature_formula": "F_nj=Q_nj-(D_n-R)*delta_nj, n=32..N-1, j=32..63",
            "selected_S": "Btrial+54*Theta; no factor two or extra scalar K shift",
            "resource_policy": "Full actual signed prime/Gamma/pole defect; no nine-feature correction added",
            "comparison_with_nine_feature": "No Loewner ordering claimed",
        },
        "high_block_floor_used": "8/5", "tail_floor_used": "39/5",
        "high_block_floor_at_M": ball_record(D[M] - rho),
        "high_block_floor_at_N": ball_record(D[N] - rho),
        "prime_weights": [ball_record(a) for a in weights],
        "prime_shifts": [ball_record(s) for s in shifts],
        "row_tail_weight_sum_sigma": ball_record(sigma),
        "high_operator_cap_R": ball_record(rho),
        "low_tail_rank": ball_record(tail_rank),
        "low_tail_w_coefficient": "512/1041816384077177475",
        "low_tail_remainder_coefficient": "51380224/4194394783958568267303454125",
        "low_first_row_64": [ball_record(x) for x in firstrow[:SOURCE_COLUMNS]],
        "direct_diagonal_64": [ball_record(x) for x in direct_diagonal],
        "signed_tail_w_32": [ball_record(x) for x in w],
        "source_acceleration": "Exact rank-two displacement; new first row at B=4/5",
        "source_acceleration_sha256": "f789e00c67e889c2546e84021f3020e942b6b846c5b5185134471282664ff1ac",
        "block_rows": BLOCK_ROWS,
        "raw_trial_tail_rank": ball_record(trial_tail_rank),
        "raw_trial_tail_scalar": ball_record(trial_tail_scalar),
        "exponential_entry_error": ball_record(exp_error),
        "uncorrected_complete_coupling_bound_trace": ball_record(trace),
        "full_norm_trace_policy": "Use trace(C0), not a corrected-cost trace",
        "witness_matrices": {name: matrix_record(mat) for name, mat in (
            ("A", A), ("Cfinite", Cfinite), ("C0", C0), ("Btrial", Btrial), ("Theta", Theta),
            ("S", S), ("G", G), ("Z_trial_by_low", Z), ("M_resource", resource))},
        "missing_matrices": ["M_resource_inverse", "correction", "Ffull"],
        "trust_boundary": "Analytic reduction and complete tails, source, python-flint/FLINT and Python; not formal proof verification",
        "global_all_radii_positivity": "NOT_PROVED", "RH": "NOT_PROVED",
    }
    H_lower, H_pivots, H_failure = ldl_fixed(resource)
    common["witness_matrices"]["resource_LDL_L"] = matrix_record(H_lower)
    common["witness_matrices"]["resource_LDL_pivots"] = [ball_record(x) for x in H_pivots]
    if H_failure is not None:
        i, pivot = H_failure
        common["stage"] = "FAILED_SMALL_INVERSE_GATE"
        common["failed_gate"] = {"matrix": "M_resource", "index": i, "pivot": ball_record(pivot)}
        diagnostic = export("diagnostic", common)
        export("failure", {"status": "FAILED_SMALL_INVERSE_GATE_NOT_CERTIFICATE",
            "diagnostic": diagnostic, "failed_pivot_index": i, "failed_pivot": ball_record(pivot)})
        return False

    progress["stage"] = "RESOURCE_INVERSE_AND_CORRECTION"
    H_inverse = inverse_from_ldl(H_lower, H_pivots)
    progress["complete_matrices"]["M_resource_inverse"] = H_inverse
    solved = [[sum((H_inverse[a][b0] * Z[b0][m] for b0 in range(TRIAL_COLUMNS)), arb(0))
               for m in range(M)] for a in range(TRIAL_COLUMNS)]
    correction = [[arb(0) for _ in range(M)] for _ in range(M)]
    for i in range(M):
        for j in range(i + 1):
            correction[i][j] = sum((Z[a][i] * solved[a][j] for a in range(TRIAL_COLUMNS)), arb(0))
            correction[j][i] = correction[i][j]
    F = [[A[i][j] - C0[i][j] + correction[i][j] for j in range(M)] for i in range(M)]
    progress["complete_matrices"].update({"correction": correction, "Ffull": F})
    common["stage"] = "PRE_GATE_NOT_CERTIFICATE"
    common["missing_matrices"] = []
    common["witness_matrices"].update({
        "M_resource_inverse": matrix_record(H_inverse),
        "resource_inverse_Z": matrix_record(solved),
        "correction": matrix_record(correction), "Ffull": matrix_record(F),
    })
    diagnostic = export("diagnostic", common)

    # Exactly one final fixed-index LDL. Failure keeps the already written evidence.
    L, pivots, failure = ldl_fixed(F)
    if failure is not None:
        i, pivot = failure
        export("failure", {
            "status": "FAILED_POSITIVITY_GATE_NOT_CERTIFICATE", "matrix": "Ffull",
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
        "status": "PASS_INTERVAL_FULL_ACTUAL_DEFECT_SCHUR_CERTIFICATE",
        "scope": "real even minimum compact-support Gamma-form domain, 0 < B <= 4/5",
        "diagnostic": diagnostic,
        "q_lower_bound_L2": rational_text(gap),
        "schur_margin_low_mode_L2": rational_text(mu),
        "pivot_lower_bound": rational_text(d_star),
        "inverse_L_frobenius_squared_upper_bound": rational_text(inverse_norm_upper),
        "coupling_trace_upper_bound": rational_text(tau),
        "witness_matrices": {"L": matrix_record(L), "L_inverse": matrix_record(Linv),
                             "LDL_pivots": [ball_record(p) for p in pivots]},
        "schur_gap_policy": "Fixed LDL of Ffull followed by exact pivot/inverse-factor and trace(C0) norm conversion",
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
    # Enforce the intended supervisor-before-import protocol as well as CLI guard.
    marker_path = args.output.parent / "ATTEMPT_ONCE.json"
    if not marker_path.is_file():
        raise RuntimeError("Supervisor attempt marker required before numerical imports")
    marker = json.loads(marker_path.read_text())
    binding_name = str(Path(__file__).resolve().relative_to(Path(__file__).resolve().parent.parent))
    if marker.get("input_hashes", {}).get(binding_name) != source_hash:
        raise RuntimeError("Supervisor marker does not bind this numerical source")
    if str(args.output.resolve()) not in marker.get("command", []):
        raise RuntimeError("Output not bound to supervisor command")
    # Reserve 64 KiB for bounded combined stdout/stderr capture by the launcher.
    MAX_JSON_BYTES = 8 * 1024 * 1024 - 64 * 1024
    total_bytes = 0
    written = set()
    artifacts = {}

    def export(kind, payload):
        nonlocal total_bytes
        if kind in written:
            raise RuntimeError("Refusing a duplicate artifact kind")
        payload["verifier_sha256"] = source_hash
        data = (json.dumps(payload, separators=(",", ":")) + "\n").encode("utf-8")
        if total_bytes + len(data) > MAX_JSON_BYTES:
            raise RuntimeError("Fixed JSON cap (8 MiB minus 64 KiB stream reserve) exceeded; no new artifact written")
        path = paths[kind]
        with path.open("xb") as stream:
            stream.write(data)
        total_bytes += len(data)
        written.add(kind)
        digest = hashlib.sha256(data).hexdigest()
        print(f"Wrote {kind}: {path.name}, {len(data)} bytes, sha256 {digest}", flush=True)
        artifacts[kind] = {"filename": path.name, "sha256": digest, "bytes": len(data)}
        return artifacts[kind]

    progress = {"stage": "BEFORE_NUMERICAL_IMPORT", "complete_matrices": {}}
    try:
        success = verify(export, progress)
    except Exception as error:
        if "diagnostic" not in written:
            encoder = progress.get("matrix_record")
            available = {name: encoder(mat) for name, mat in progress["complete_matrices"].items()} if encoder else {}
            expected = ("A", "C0", "Btrial", "Theta", "S", "G", "Z_trial_by_low", "M_resource", "M_resource_inverse", "correction", "Ffull")
            export("diagnostic", {
                "status": "NOT_CERTIFICATE", "stage": progress["stage"],
                "exception_type": type(error).__name__, "message": str(error),
                "witness_matrices": available,
                "missing_matrices": [name for name in expected if name not in available],
                "partial_evidence_policy": "Only completed matrices are included; partial row accumulations are not certified full sums",
            })
        if "failure" not in written and "success" not in written:
            export("failure", {"status": "FAILED_EXCEPTION_NOT_CERTIFICATE",
                "stage": progress["stage"], "diagnostic": artifacts["diagnostic"],
                "exception_type": type(error).__name__, "message": str(error)})
        raise
    if not success:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
