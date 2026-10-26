"""Verified positive-subspace test for an already certified Loewner enclosure.

No integration-error claim is made here.  The caller must establish F >= M-delta I.
M and every trial Q entry are interpreted as their exact binary64 dyadic values.
BLAS products are enclosed by gamma_(2k) classical-dot bounds, including a
conservative minimum-normal absolute underflow allowance.  Nonzero subnormal
multiplicative inputs, unsupported rounding, nonfinite values, and overflow-risk
inputs fail closed.  Floating eigensolutions select a trial; they are not evidence.
"""
import os
for _v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_v] = '1'
import argparse
import ctypes
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
import sys
import time

import numpy as np
from scipy.linalg import eigh
from threadpoolctl import threadpool_info, threadpool_limits

TINY = float.fromhex('0x1.0000000000000p-1022')
U = Fraction(1, 2**53)

class ValidationFailure(RuntimeError):
    pass

def _hash_bytes(a):
    return hashlib.sha256(np.asarray(a, dtype='<f8', order='C').tobytes()).hexdigest()

def _finite(a, name):
    a = np.asarray(a, dtype=np.float64)
    if not np.all(np.isfinite(a)):
        raise ValidationFailure(name + ': nonfinite value')
    return a

def _multiplicative_input(a, name):
    a = _finite(a, name)
    # Float comparisons can silently treat subnormal inputs as zero under DAZ.
    # Inspect the stored IEEE-754 bits instead; sign is irrelevant, and signed
    # zero is allowed.  This test does not perform arithmetic on the input.
    magnitude_bits = a.view(np.uint64) & np.uint64(0x7fffffffffffffff)
    if np.any((magnitude_bits > np.uint64(0)) &
              (magnitude_bits < np.uint64(0x0010000000000000))):
        raise ValidationFailure(name + ': nonzero subnormal multiplicative input')
    return a

def _up(x):
    # Extra TINY covers flush-to-zero at this individual bound operation.
    a = _finite(x, 'upward-bound intermediate')
    if np.any(a < 0):
        raise ValidationFailure('negative nonnegative-bound intermediate')
    with np.errstate(over='ignore', invalid='ignore', under='ignore'):
        z = np.nextafter(a + TINY, np.inf)
    return _finite(z, 'upward bound')

def _add_up(a, b):
    return _up(np.asarray(a) + np.asarray(b))

def _mul_up(a, b):
    _multiplicative_input(a, 'bound multiplicand A')
    _multiplicative_input(b, 'bound multiplicand B')
    return _up(np.asarray(a) * np.asarray(b))

def _div_up(a, b):
    if not np.all(np.asarray(b) > 0):
        raise ValidationFailure('nonpositive bound denominator')
    return _up(np.asarray(a) / np.asarray(b))

def _down_sub(a, b):
    a = _finite(a, 'lower-bound minuend')
    b = _finite(b, 'lower-bound subtrahend')
    with np.errstate(over='ignore', invalid='ignore', under='ignore'):
        z = np.nextafter((a - b) - TINY, -np.inf)
    return _finite(z, 'lower subtraction')

def _fraction_up(q):
    q = Fraction(q)
    if q < 0:
        raise ValidationFailure('negative rational upper bound')
    # Clamp in exact rational arithmetic before float conversion, so DAZ/FTZ
    # cannot turn a positive subnormal-sized bound into a zero upper bound.
    if 0 < q < Fraction.from_float(TINY):
        return TINY
    x = float(q)
    if not math.isfinite(x):
        raise ValidationFailure('rational upper bound overflow')
    if Fraction.from_float(x) < q:
        x = float(np.nextafter(x, np.inf))
    return x

def _constants(k):
    if not isinstance(k, int) or k < 1 or 2*k*U >= 1:
        raise ValidationFailure('invalid dot dimension')
    den = 1 - 2*k*U
    # At most k rounded products and k additions. FMA only reduces this count.
    gamma = _fraction_up(2*k*U / den)
    eta = _fraction_up(Fraction(2*k) * Fraction.from_float(TINY) / den)
    den_lower = float(_down_sub(1.0, gamma))
    if not 0 < den_lower <= 1:
        raise ValidationFailure('invalid gamma denominator')
    return gamma, eta, den_lower

def _guard_dot(A, B):
    A = _multiplicative_input(A, 'dot A')
    B = _multiplicative_input(B, 'dot B')
    if A.ndim != 2 or B.ndim != 2 or A.shape[1] != B.shape[0]:
        raise ValidationFailure('dot shape mismatch')
    k = A.shape[1]
    aa = float(np.max(np.abs(A), initial=0.0))
    bb = float(np.max(np.abs(B), initial=0.0))
    # Huge margin makes all classical dot partial sums and their rounding finite.
    exact_abs_sum_bound = Fraction.from_float(aa)*Fraction.from_float(bb)*k
    if exact_abs_sum_bound >= 2**900:
        raise ValidationFailure('dot overflow-risk guard')
    return A, B, int(k)

def _positive_product_upper(A, B):
    A, B, k = _guard_dot(A, B)
    if np.any(A < 0) or np.any(B < 0):
        raise ValidationFailure('signed input to nonnegative product')
    c = _finite(A @ B, 'nonnegative BLAS product')
    if np.any(c < 0):
        raise ValidationFailure('negative nonnegative BLAS result')
    gamma, eta, den = _constants(k)
    # |c-S| <= gamma*S+eta => S <= (c+eta)/(1-gamma).
    return _div_up(_add_up(c, eta), den)

def _product_with_error(A, B):
    A, B, k = _guard_dot(A, B)
    c = _finite(A @ B, 'signed BLAS product')
    s_upper = _positive_product_upper(np.abs(A), np.abs(B))
    gamma, eta, _ = _constants(k)
    err = _add_up(_mul_up(gamma, s_upper), eta)
    return c, err

def _row_sum_upper(A):
    A = _multiplicative_input(A, 'row-sum input')
    if A.ndim != 2 or np.any(A < 0):
        raise ValidationFailure('invalid row-sum array')
    k = int(A.shape[1])
    gamma, eta, den = _constants(k)
    s = _finite(np.sum(A, axis=1), 'nonnegative row sum')
    return _div_up(_add_up(s, eta), den)

def _parse_delta(value):
    if isinstance(value, (float, np.floating)):
        q = Fraction.from_float(float(value))
    elif isinstance(value, (str, int)):
        q = Fraction(value)
    else:
        raise ValidationFailure('delta must be an exact decimal string or binary64 scalar')
    if q < 0:
        raise ValidationFailure('negative delta')
    return _fraction_up(q)

def _check_rounding():
    if not sys.platform.startswith('linux'):
        raise ValidationFailure('rounding environment supported only on Linux')
    try:
        f = ctypes.CDLL(None).fegetround
        f.restype = ctypes.c_int
        mode = f()
    except Exception as e:
        raise ValidationFailure('cannot inspect floating rounding mode: '+str(e))
    if mode != 0:  # Linux FE_TONEAREST
        raise ValidationFailure('floating rounding mode is not FE_TONEAREST')
    return mode

def _json_write(path, obj):
    p = Path(path)
    t = p.with_suffix(p.suffix + '.tmp')
    t.write_text(json.dumps(obj, indent=2, allow_nan=False)+'\n')
    t.replace(p)

def certify_inertia(center, delta_upper, *, provenance=None, output_dir=None):
    """Return a conditional CERT/INCONCLUSIVE ledger, never an integration proof.

    CERT establishes: if F >= center-delta_upper*I, F has at most one negative
    eigenvalue.  The caller must combine this with its independent Loewner proof.
    """
    start = time.monotonic()
    ledger = {'status':'INCONCLUSIVE', 'scope':'positive n-1 dimensional trial subspace of an input Loewner lower enclosure',
              'integration_error_proved_here':False,
              'required_external_premise':'F >= exact_dyadic_center - supplied_delta_upper * I',
              'provenance':provenance or {},
              'arithmetic_model':'binary64 classical dot/FMA, <=2k rounded operations, gamma_(2k), minnormal absolute underflow allowance; no nonzero subnormal multiplicative inputs',
              'thread_environment':{v:os.environ.get(v) for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')}}
    out = Path(output_dir) if output_dir is not None else None
    if out is not None:
        out.mkdir(parents=True, exist_ok=True)
    limiter = None
    try:
        limiter = threadpool_limits(limits=1, user_api='blas')
        pools = [p for p in threadpool_info() if p.get('user_api') == 'blas']
        if not pools or any(p.get('internal_api') != 'openblas' or p.get('num_threads') != 1 for p in pools):
            raise ValidationFailure('expected single-thread OpenBLAS classical BLAS kernels')
        ledger['blas_libraries'] = pools
        ledger['fegetround'] = _check_rounding()
        M = np.array(center, dtype=np.float64, order='C', copy=True)
        _multiplicative_input(M, 'center')
        if M.ndim != 2 or M.shape[0] != M.shape[1] or M.shape[0] < 2:
            raise ValidationFailure('center must be square of dimension at least two')
        if not np.array_equal(M, M.T):
            raise ValidationFailure('center is not exactly symmetric')
        n = int(M.shape[0]); delta = _parse_delta(delta_upper)
        ledger.update(dimension=n, trial_dimension=n-1, center_binary64_sha256=_hash_bytes(M),
                      delta_upper_binary64_hex=delta.hex(), delta_upper_binary64=delta,
                      delta_input=str(delta_upper))
        vals, eigvec = eigh(M, driver='evr', check_finite=True)
        Q = np.array(eigvec[:,1:], dtype=np.float64, order='C', copy=True)
        _multiplicative_input(Q, 'trial Q')
        _check_rounding()
        ledger['trial_sha256'] = _hash_bytes(Q)
        ledger['floating_eigenvalue_diagnostics_NOT_USED_AS_PROOF'] = {'smallest':float(vals[0]),'second':float(vals[1])}
        gram, eg = _product_with_error(Q.T, Q)
        dev = np.abs(gram)
        ii = np.diag_indices(n-1)
        dev[ii] = _up(np.abs(np.diag(gram) - 1.0))
        defect = float(np.max(_row_sum_upper(_add_up(dev, eg))))
        qnorm2 = float(_add_up(1.0, defect))
        ledger.update(trial_gram_defect_norm_upper=defect, trial_norm_squared_upper=qnorm2,
                      trial_columns_independent=bool(defect < 1.0))
        if defect >= 1.0:
            raise ValidationFailure('trial Gram enclosure does not prove independence')
        T, et = _product_with_error(M, Q)
        _multiplicative_input(T, 'computed M Q')
        b, eb_local = _product_with_error(Q.T, T)
        eb = _add_up(eb_local, _positive_product_upper(np.abs(Q.T), et))
        off = _add_up(np.abs(b), eb)
        np.fill_diagonal(off, 0.0)
        offsum = _row_sum_upper(off)
        diag_lower = _down_sub(np.diag(b), np.diag(eb))
        center_lower = float(np.min(_down_sub(diag_lower, offsum)))
        perturb = float(_mul_up(delta, qnorm2))
        lower = float(_down_sub(center_lower, perturb))
        ledger.update(projected_center_gershgorin_lower=center_lower,
                      input_loewner_error_after_congruence_upper=perturb,
                      positive_subspace_margin_lower=lower,
                      projected_product_error_max_row_sum_upper=float(np.max(_row_sum_upper(eb))),
                      trial_gram_product_error_max_row_sum_upper=float(np.max(_row_sum_upper(eg))),
                      status='CERT_CONDITIONAL_ON_INPUT_LOEWNER_BOUND' if lower > 0 else 'INCONCLUSIVE',
                      conclusion=('At most one strictly negative eigenvalue of F, conditional on the supplied Loewner premise.' if lower > 0 else 'No sign certificate established.'))
        _check_rounding()
        if out is not None:
            np.save(out/'trial_positive_subspace.npy', Q, allow_pickle=False)
            np.save(out/'projected_center_float.npy', b, allow_pickle=False)
            np.save(out/'projected_product_error_upper.npy', eb, allow_pickle=False)
    except Exception as exc:
        ledger.update(status='INCONCLUSIVE', reason=type(exc).__name__+': '+str(exc))
    finally:
        if limiter is not None:
            limiter.restore_original_limits()
    ledger['wall_seconds'] = time.monotonic()-start
    if out is not None:
        _json_write(out/'inertia_ledger.json', ledger)
    return ledger

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--matrix', required=True)
    p.add_argument('--dimension', type=int, default=552)
    p.add_argument('--delta-json', required=True)
    p.add_argument('--delta-key', default='total_error_upper')
    p.add_argument('--output-dir', required=True)
    a = p.parse_args()
    matrix_path = Path(a.matrix); ledger_path = Path(a.delta_json)
    raw = matrix_path.read_bytes()
    if matrix_path.suffix == '.npy':
        M = np.load(matrix_path, allow_pickle=False)
    else:
        if len(raw) != a.dimension*a.dimension*8:
            raise ValueError('raw matrix byte count mismatch')
        M = np.frombuffer(raw, dtype='<f8').reshape(a.dimension,a.dimension)
    input_ledger = json.loads(ledger_path.read_text())
    delta = input_ledger[a.delta_key]
    provenance = {'matrix_path':str(matrix_path), 'matrix_file_sha256':hashlib.sha256(raw).hexdigest(),
                  'delta_ledger_path':str(ledger_path),'delta_ledger_sha256':hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
                  'delta_key':a.delta_key}
    result = certify_inertia(M, delta, provenance=provenance, output_dir=a.output_dir)
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result['status']=='CERT_CONDITIONAL_ON_INPUT_LOEWNER_BOUND' else 2

if __name__ == '__main__':
    raise SystemExit(main())
