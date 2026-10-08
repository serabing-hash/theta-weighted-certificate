"""REVIEW-ONLY primitive for the SINGLE proposed fixed-160-bit repair.

No source/cache/logarithm evaluation and no production entrypoint.
Use the inspected v2_support.rec callable as record. This audit never imports
or executes the Work producer. The caller must prove a single exact unit rho
is enclosed in R; an arbitrary complex ball alone is insufficient.
"""
from flint import acb, arb, ctx
PHASE_BITS = 140


def step_exact_unit_phase(q_previous, E_num_previous, R, record):
    """Retain |rho**k-q|_2 <= E_num / 2**140 with exact integer bookkeeping.

    Native products remain at ctx.prec=160. Exact dyadic centers use the existing
    outward denominator-140 record helper. E is a Euclidean absolute-error bound;
    its increment is the conservative sum of coordinate local-error bounds.
    """
    if ctx.prec != 160:
        raise ValueError('fixed 160-bit arithmetic required')
    if not q_previous.is_exact() or not q_previous.is_finite():
        raise ValueError('phase center must be exact finite dyadics')
    if not isinstance(E_num_previous, int) or E_num_previous < 0:
        raise ValueError('cumulative error numerator must be nonnegative integer')
    if not R.is_finite():
        raise ValueError('nonfinite root enclosure')

    P = q_previous * R
    if not P.is_finite():
        raise ArithmeticError('nonfinite local phase product')
    c_re, r_re = map(int, record(P.real, PHASE_BITS))
    c_im, r_im = map(int, record(P.imag, PHASE_BITS))
    if r_re < 0 or r_im < 0:
        raise ArithmeticError('invalid outward local records')
    q = acb(arb((c_re, -PHASE_BITS)), arb((c_im, -PHASE_BITS)))
    if not q.is_exact() or not q.is_finite():
        raise ArithmeticError('center does not fit exact fixed-precision dyadics')
    # Integer addition is exact. No inherited error is lost or reset.
    E_num = E_num_previous + r_re + r_im
    cosine = arb((c_re, -PHASE_BITS), (E_num, -PHASE_BITS))
    if not cosine.is_finite():
        raise ArithmeticError('nonfinite cosine inclusion')
    return q, E_num, cosine, [c_re, r_re, c_im, r_im]


def initial_state():
    if ctx.prec != 160:
        raise ValueError('fixed 160-bit arithmetic required')
    return acb(1), 0
