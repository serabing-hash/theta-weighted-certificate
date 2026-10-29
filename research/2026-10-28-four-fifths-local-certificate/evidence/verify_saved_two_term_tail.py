#!/usr/bin/env python3
"""Disabled saved-data two-term signed-tail sign gate; a new approval is required.

No source-function evaluations, quadrature, parameter search, retry, or eigensolver.
Only the fixed analytic rank-one plus quartic diagonal replacement is applied.
Elementary pi/sqrt/sinh/exp enclosures are required; source rows are not reevaluated.
The CLI flag prevents accidental execution; it does not confer authorization.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

INPUT_SHA256 = 'be35a1bfedcbe49e775c4855fe740a846a0d85173a9630c505b60de1f4d0e4b3'
ORIGINAL_PRODUCER_SHA256 = 'f7288fe5eb238d2e1350fad683c0c4290ba9f4c6fdfb5c891e6457e2c834b00e'
A_COEFF = Fraction(5, 12347453440914696)
D_COEFF = Fraction(1225, 138087071076825292750731)
SIZE = 32
PRECISION_BITS = 256
JSON_CAP = 8 * 1024 * 1024 - 64 * 1024


def fraction_text(q):
    return str(q.numerator) + '/' + str(q.denominator)


def verify(data, export):
    # All numerical imports occur only after guarded main and input hash checks.
    import flint
    from flint import arb, fmpq, ctx
    if flint.__version__ != '0.9.0':
        raise RuntimeError('Requires existing python-flint 0.9.0')
    if not __debug__:
        raise RuntimeError('Assertions must be enabled; do not use -O')
    ctx.prec = PRECISION_BITS

    def exact_endpoint(x, upper):
        assert x.is_finite()
        point = x.upper() if upper else x.lower()
        assert point.is_finite() and point.is_exact()
        q = point.fmpq()
        result = Fraction(int(q.p), int(q.q))
        roundtrip = arb(q)
        assert roundtrip.is_exact() and roundtrip == point
        return result

    def rational_ball(q):
        return arb(fmpq(q.numerator, q.denominator))

    def load_ball(record):
        lo = Fraction(record['lower_rational'])
        hi = Fraction(record['upper_rational'])
        if lo > hi:
            raise ValueError('Reversed stored endpoints')
        result = rational_ball(lo).union(rational_ball(hi))
        # Check exact containment even if importing a rational rounded outward.
        assert exact_endpoint(result, False) <= lo
        assert exact_endpoint(result, True) >= hi
        return result

    def record_ball(x):
        return {'lower_rational': fraction_text(exact_endpoint(x, False)),
                'upper_rational': fraction_text(exact_endpoint(x, True)),
                'display': str(x)}

    def record_matrix(matrix):
        return [[record_ball(x) for x in row] for row in matrix]

    records = data['witness_matrices']['Ffull']
    assert len(records) == SIZE and all(len(row) == SIZE for row in records)
    matrix = [[load_ball(x) for x in row] for row in records]
    for i in range(SIZE):
        for j in range(i):
            assert (matrix[i][j] - matrix[j][i]).contains(0)
            common = matrix[i][j].union(matrix[j][i])
            matrix[i][j] = common
            matrix[j][i] = common
    scalar = load_ball(data['low_tail_scalar'])
    assert scalar > 0
    # A is the original actual low compression, not Ffull or the new matrix.
    actual_records = data['witness_matrices']['A']
    assert len(actual_records) == SIZE and all(len(row) == SIZE for row in actual_records)
    actual_row = [load_ball(x) for x in actual_records[0]]
    pi = arb.pi()
    b0 = rational_ball(Fraction(4, 3)).sqrt()
    bpos = rational_ball(Fraction(8, 3)).sqrt()
    sh = rational_ball(Fraction(3, 8)).sinh()
    e_minus_b = rational_ball(Fraction(-3, 4)).exp()
    e_minus_3 = arb(-3).exp()
    E0 = e_minus_b / (1 - e_minus_3)
    assert 1 - e_minus_3 > 0
    w = []
    for m in range(SIZE):
        bm = b0 if m == 0 else bpos
        vm = bm * ((-1) ** m)
        km = rational_ball(Fraction(4 * m, 3)) * pi
        w.append(vm * (4 * sh ** 2 - E0) - km ** 2 * actual_row[m] / b0)
    a_ball, d_ball = rational_ball(A_COEFF), rational_ball(D_COEFF)
    for i in range(SIZE):
        for j in range(i + 1):
            entry = matrix[i][j] - a_ball * w[i] * w[j]
            if i == j:
                entry += scalar - d_ball * ((i + 1) ** 4)
            matrix[i][j] = entry
            matrix[j][i] = entry
    base = {
        'status': 'PRE_GATE_NOT_CERTIFICATE',
        'scope': 'New saved-data sufficient comparison at B=3/4; no RH claim',
        'input_sha256': INPUT_SHA256,
        'original_producer_sha256': ORIGINAL_PRODUCER_SHA256,
        'precision_bits': PRECISION_BITS,
        'matrix_size': SIZE,
        'tail_rank_w_coefficient': fraction_text(A_COEFF),
        'tail_diagonal_coefficient': fraction_text(D_COEFF),
        'signed_tail_vector_w': [record_ball(x) for x in w],
        'saved_actual_A_first_row': [record_ball(x) for x in actual_row],
        'elementary_enclosures': {key: record_ball(value) for key, value in
            [('pi', pi), ('b0', b0), ('bpos', bpos), ('sinh_3_over_8', sh),
             ('exp_minus_3_over_4', e_minus_b), ('exp_minus_3', e_minus_3), ('E0', E0)]},
        'diagonal_weights': [(i + 1) ** 4 for i in range(SIZE)],
        'replacement': 'F_two_term = Ffull + low_tail_scalar I - a ww* - d diag((m+1)^4)',
        'unchanged': ['rank tail', 'Theta', 'S', 'G', 'Z', 'Woodbury correction',
                      'complete prime/Gamma/pole source arrays'],
        'original_source_row_evaluations': 0,
        'new_elementary_constant_enclosures': True,
        'retry_or_search': False,
        'F_two_term': record_matrix(matrix),
        'global_all_radii_positivity': 'NOT_PROVED',
        'RH': 'NOT_PROVED',
    }
    export('diagnostic', base)

    lower = [[arb(0) for _ in range(SIZE)] for _ in range(SIZE)]
    pivots = []
    # One fixed-index LDL, with no restart, pivot search or precision change.
    for i in range(SIZE):
        lower[i][i] = arb(1)
        pivot = matrix[i][i] - sum(
            (lower[i][j] ** 2 * pivots[j] for j in range(i)), arb(0))
        if not pivot > 0:
            strict_negative = exact_endpoint(pivot, True) < 0
            export('failure', {
                'status': ('FAILED_STRICT_NEGATIVE_PIVOT_NOT_CERTIFICATE' if strict_negative
                           else 'INCONCLUSIVE_NONPOSITIVE_GATE_NOT_CERTIFICATE'),
                'failed_pivot_index': i,
                'failed_pivot': record_ball(pivot),
                'positive_prefix_pivots': [record_ball(x) for x in pivots],
                'interpretation': 'Sufficient comparison only; not a negative original-Q witness or RH counterexample',
            })
            return False
        pivots.append(pivot)
        for n in range(i + 1, SIZE):
            lower[n][i] = (matrix[n][i] - sum(
                (lower[n][j] * lower[i][j] * pivots[j] for j in range(i)), arb(0))) / pivot

    inverse_lower = [[arb(0) for _ in range(SIZE)] for _ in range(SIZE)]
    for i in range(SIZE):
        inverse_lower[i][i] = arb(1)
        for j in range(i):
            inverse_lower[i][j] = -sum(
                (lower[i][k] * inverse_lower[k][j] for k in range(j, i)), arb(0))
    d_min = min(exact_endpoint(p, False) for p in pivots)
    assert d_min > 0
    inverse_norm_upper = Fraction(0)
    for i in range(SIZE):
        for j in range(i + 1):
            bound = max(abs(exact_endpoint(inverse_lower[i][j], False)),
                        abs(exact_endpoint(inverse_lower[i][j], True)))
            inverse_norm_upper += bound * bound
    assert inverse_norm_upper >= SIZE
    mu = d_min / inverse_norm_upper
    # Conservative trace bound for the NEW majorant; do not assume it is
    # Loewner-below the old majorant. Discarding its -32*scalar term is safe.
    old_trace_upper = Fraction(data['uncorrected_complete_coupling_bound_trace']['upper_rational'])
    w_norm_squared_upper = sum((max(abs(exact_endpoint(x, False)),
                                     abs(exact_endpoint(x, True))) ** 2 for x in w), Fraction(0))
    trace_upper = old_trace_upper + A_COEFF * w_norm_squared_upper + D_COEFF * sum(i ** 4 for i in range(1, SIZE + 1))
    assert trace_upper > 0
    kappa = Fraction(8, 5)
    gap = min(mu * kappa / (kappa + 2 * trace_upper), kappa / 2)
    assert gap > 0
    assert gap * (1 + 2 * trace_upper / kappa) <= mu
    assert 2 * gap / kappa <= 1
    export('success', {
        'status': 'PASS_INTERVAL_SAVED_TWO_TERM_TAIL_SCHUR_CERTIFICATE',
        'scope': 'Real even minimum compact-support Gamma-form domain, 0 < B <= 3/4',
        'q_lower_bound_L2': fraction_text(gap),
        'schur_margin_low_mode_L2': fraction_text(mu),
        'pivot_lower_bound': fraction_text(d_min),
        'inverse_L_frobenius_squared_upper_bound': fraction_text(inverse_norm_upper),
        'safe_complete_coupling_trace_upper_bound': fraction_text(trace_upper),
        'old_coupling_trace_upper_bound': fraction_text(old_trace_upper),
        'signed_w_norm_squared_upper_bound': fraction_text(w_norm_squared_upper),
        'trace_policy': 'old trace upper + a upper(||w||^2) + d sum(m+1)^4; subtractive -32*scalar discarded',
        'high_block_floor': '8/5',
        'L': record_matrix(lower),
        'L_inverse': record_matrix(inverse_lower),
        'LDL_pivots': [record_ball(x) for x in pivots],
        'trust_boundary': 'Analytic contracts, original source enclosure, saved-data transformation, python-flint/FLINT and Python; not formal proof verification',
        'global_all_radii_positivity': 'NOT_PROVED',
        'RH': 'NOT_PROVED',
    })
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute-approved-once', action='store_true')
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if not args.execute_approved_once:
        parser.error('Disabled: obtain new explicit approval and use a bounded single-use supervisor')
    if not __debug__:
        raise RuntimeError('Run without -O')
    paths = {kind: args.output.with_name(args.output.stem + '.' + kind + '.json')
             for kind in ('diagnostic', 'failure', 'success')}
    if args.output.exists() or any(p.exists() for p in paths.values()):
        raise FileExistsError('Refusing existing output or sibling')
    raw = args.input.read_bytes()
    if hashlib.sha256(raw).hexdigest() != INPUT_SHA256:
        raise RuntimeError('Saved input hash mismatch')
    data = json.loads(raw)
    if data['verifier_sha256'] != ORIGINAL_PRODUCER_SHA256:
        raise RuntimeError('Wrong original producer')
    expected = {'support_radius': '3/4', 'precision_bits': 256, 'low_modes': 32,
                'source_columns': 64, 'actual_trial_indices': [32, 63],
                'trial_columns': 32, 'tail_start': 16384, 'exponential_terms': 32,
                'active_prime_powers': [2, 3, 4], 'python_flint_version': '0.9.0'}
    if data['fixed_parameters'] != expected or data['missing_matrices']:
        raise RuntimeError('Wrong or incomplete saved diagnostic')
    if data['high_block_floor_used'] != '8/5' or data['tail_floor_used'] != '39/5':
        raise RuntimeError('Wrong inherited floors')
    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    marker_path = args.output.parent / 'ATTEMPT_ONCE.json'
    if not marker_path.is_file():
        raise RuntimeError('Bounded supervisor attempt marker required before numerical import')
    marker = json.loads(marker_path.read_text())
    relative_source = str(Path(__file__).resolve().relative_to(Path(__file__).resolve().parent.parent))
    if (not marker.get('approval_reference') or not marker.get('single_attempt')
            or marker.get('input_hashes', {}).get(relative_source) != source_hash
            or marker.get('cpu_seconds') != 30 or marker.get('wall_seconds') != 45
            or marker.get('address_space_bytes') != 512 * 1024 * 1024):
        raise RuntimeError('Missing or mismatched bounded attempt marker')
    written = set()
    total_bytes = 0

    def export(kind, payload):
        nonlocal total_bytes
        if kind in written:
            raise RuntimeError('Duplicate artifact kind')
        payload['saved_gate_sha256'] = source_hash
        payload['input_sha256'] = INPUT_SHA256
        encoded = (json.dumps(payload, indent=2) + '\n').encode('utf-8')
        if total_bytes + len(encoded) > JSON_CAP:
            raise RuntimeError('JSON artifact cap exceeded')
        with paths[kind].open('xb') as output:
            output.write(encoded)
        written.add(kind)
        total_bytes += len(encoded)
        print('Wrote ' + kind + ': ' + paths[kind].name + ', ' + str(len(encoded)) +
              ' bytes, sha256 ' + hashlib.sha256(encoded).hexdigest(), flush=True)

    passed = verify(data, export)
    if not passed:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
