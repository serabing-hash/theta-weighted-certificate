#!/usr/bin/env python3
"""Stdlib-only exact replay of curated a1024/a2048 saved matrix data.

This adapts independent stored-matrix checkers for a portable mathematical-field
extract. It does not regenerate theta values, quadrature or source inclusions.
Floating-point arithmetic is not used in any sign premise. Run without -O.
"""
from pathlib import Path
from fractions import Fraction as F
from math import lcm
import argparse
import gzip
import hashlib
import json


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()


def matrix_view(rows, denominator):
    return {'common_denominator': str(denominator),
            'matrix_numerators': [[str(v) for v in row] for row in rows]}


def exact_linear_combination(parts, diagonal):
    """Return integer rows and a positive common denominator."""
    coefficients = [coefficient / denominator for coefficient, _, denominator in parts]
    D = lcm(diagonal.denominator, *(c.denominator for c in coefficients))
    weights = [int(c * D) for c in coefficients]
    n = len(parts[0][1]); diag = int(diagonal * D)
    rows = [[sum(weight * item[1][i][j] for weight, item in zip(weights, parts))
             + (diag if i == j else 0) for j in range(n)] for i in range(n)]
    return rows, D


def congruence_sign(rows, denominator, witness, gap=F(0)):
    n = len(rows)
    D = lcm(denominator, gap.denominator)
    A = [[v * (D // denominator) - (int(gap * D) if i == j else 0)
          for j, v in enumerate(row)] for i, row in enumerate(rows)]
    Q = [[int(v) for v in row] for row in witness]
    assert len(Q) == n and all(len(row) == n for row in Q)
    cols = list(zip(*Q))
    AQ = [[sum(x * y for x, y in zip(row, col)) for col in cols] for row in A]
    acols = list(zip(*AQ))
    H = [[sum(x * y for x, y in zip(qcol, acol)) for acol in acols] for qcol in cols]
    assert all(H[i][j] == H[j][i] for i in range(n) for j in range(n))
    margins = [row[i] - sum(abs(v) for j, v in enumerate(row) if j != i)
               for i, row in enumerate(H)]
    assert min(margins) > 0
    # H is positive definite by strict diagonal dominance. Consequently Q is
    # nonsingular (otherwise H would have a kernel), so the original A is PD.
    return {'positive_integer_congruence_margins': n,
            'minimum_integer_margin': str(min(margins)),
            'congruence_scaling_denominator': str(D)}


def replay(parameter):
    here = Path(__file__).resolve().parent
    provenance = json.loads((here / f'inputs/a{parameter}_PROVENANCE.json').read_text())
    compressed = (here / f'inputs/a{parameter}_saved_matrices.json.gz').read_bytes()
    assert sha(compressed) == provenance['gzip_sha256']
    raw = gzip.decompress(compressed)
    assert sha(raw) == provenance['curated_json_sha256']
    x = json.loads(raw)
    assert x['format'] == 'theta-exact-triangular-extract-v2'
    assert x['source_sha256'] == provenance['source_sha256']
    assert x['candidate_sha256'] == provenance['candidate_sha256']
    n = x['dimension']; assert n == 256
    a, nu, fl = F(x['a']), F(x['nu']), F(x['F_lower'])
    assert a == F(1, parameter) and nu > 0 and fl > 0
    matrices = {}
    for name, entry in x['matrices'].items():
        upper = entry['upper_triangle_rows']; assert len(upper) == n
        rows = [[0] * n for _ in range(n)]
        for i, row in enumerate(upper):
            assert len(row) == n - i
            for j, value in enumerate(row, i):
                rows[i][j] = rows[j][i] = int(value)
        den = int(entry['common_denominator']); assert den > 0
        assert sha(canonical(matrix_view(rows, den))) == entry['canonical_matrix_sha256']
        matrices[name] = (rows, den)
    G, gd = matrices['G']; K, kd = matrices['K']; T, td = matrices['T']
    results = []
    saved_exact = None
    for name, gate in sorted(x['gates'].items()):
        penalty = F(gate['penalty'])
        if name == 'exact': assert penalty == 4/nu + 5*a/nu**2
        elif name == 'conservative': assert parameter == 2048 and penalty == 26240
        M, D = exact_linear_combination([(F(4), T, td), (-5*a/4, G, gd),
                                        (-penalty, K, kd)], a*fl/4)
        md = int(gate['common_denominator']); assert md > 0
        saved_rows = []
        for row in M:
            converted = []
            for value in row:
                quotient, remainder = divmod(value * md, D)
                assert remainder == 0
                converted.append(quotient)
            saved_rows.append(converted)
        assert sha(canonical(matrix_view(saved_rows, md))) == gate['canonical_matrix_sha256']
        assert F(gate['gap']) == F(1, 2000)
        check = congruence_sign(saved_rows, md, gate['witness_integer_rows'], F(gate['gap']))
        results.append({'gate': name, 'penalty': str(penalty), 'gap': gate['gap'],
                        'reconstructed_entries': n*n, **check})
        if name == 'exact': saved_exact = (saved_rows, md)
    coeff = F(1, 2) - a + a*nu/(a+4*nu)
    result = {'parameter': parameter, 'status': 'PASS', 'candidate_sha256': x['candidate_sha256'],
              'ordinary_coefficient': str(coeff), 'gates': results}
    if parameter == 1024:
        U, ud = exact_linear_combination([(F(5, 4), G, gd), (5/nu**2, K, kd)], -fl/4)
        row_bounds = [F(row[i]+sum(abs(v) for j, v in enumerate(row) if j != i), ud)
                      for i, row in enumerate(U)]
        assert max(row_bounds) < 5944
        m = F(1, 2000); alpha = a/4 + m/(4*5944)
        scalar = F(1, 2)-a+alpha*nu/(alpha+nu)
        assert scalar == F(193711700665728390485973185, 388065364069101325921538048)
        w = x['generalized']; theta = F(w['theta']); assert theta == F(3, 20000)
        M, md = saved_exact
        A, ad = exact_linear_combination([(F(1), M, md), (-theta, U, ud)], F(0))
        check = congruence_sign(A, ad, w['witness_integer_rows'])
        alpha = (a+theta)/4
        improved = F(1, 2)-a+alpha*nu/(alpha+nu)
        assert str(alpha) == w['alpha'] and str(improved) == w['coefficient']
        assert str(coeff) == w['old_coefficient'] and improved > scalar > coeff
        assert improved < F(1, 2)-a+nu < F(1, 2)
        result['scalar_slack'] = {'g': 5944, 'strict_row_margins': n, 'coefficient': str(scalar)}
        result['generalized'] = {'theta': str(theta), 'coefficient': str(improved), **check}
    elif parameter == 2048:
        assert coeff == F(542006223062224701317434549, 1084868104425248291110985728)
        coarse = F(1, 2)-a+a*(F(4, 5)*a)/(a+4*(F(4, 5)*a))
        assert coarse == F(21487, 43008) and coarse < coeff < F(1, 2)
        result['conservative_coefficient'] = str(coarse)
    result['scope'] = ('Exact saved-matrix reconstruction and sign verification only. '
                       'The source enclosures and complete-domain analytic premises are not regenerated. '
                       'The half bound and RH are not proved.')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parameter', choices=['1024', '2048', 'both'], default='both')
    args = parser.parse_args()
    if not __debug__: raise SystemExit('Run without Python -O: assertions are verification gates.')
    parameters = [1024, 2048] if args.parameter == 'both' else [int(args.parameter)]
    print(json.dumps({'status': 'PASS', 'results': [replay(p) for p in parameters]}, indent=2, sort_keys=True))
