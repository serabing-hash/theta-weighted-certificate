#!/usr/bin/env python3
"""One capped, fixed-input source-tail certificate; Python standard library only.

All numerical enclosures use integer endpoints on the 10^-120 grid, with
outward rounding after every operation. Exact symbolic polynomial/identity
checks are finite and capped at 8192 bits per rational numerator/denominator.
There is no quadrature, matrix, inverse, parameter search, or retry.
"""
import sys
import time
import signal
import resource

START = time.monotonic()
MEMORY_BYTES = 768 * 1024 * 1024
WALL_SECONDS = 290


class BudgetHold(Exception):
    pass


class ArithmeticHold(Exception):
    pass


def stop_for_budget(signum, frame):
    raise BudgetHold("internal wall-clock limit reached")


try:
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_BYTES, MEMORY_BYTES))
    if resource.getrlimit(resource.RLIMIT_AS) != (MEMORY_BYTES, MEMORY_BYTES):
        raise RuntimeError("address-space cap verification failed")
    signal.signal(signal.SIGALRM, stop_for_budget)
    signal.setitimer(signal.ITIMER_REAL, WALL_SECONDS)
except Exception as exc:
    print("HOLD: caps unavailable; numerical computation not started: " + str(exc), flush=True)
    sys.exit(2)

import json
import math
import hashlib
import platform
import traceback
from fractions import Fraction
from pathlib import Path

SCALE = 10 ** 120
MAX_SYMBOLIC_BITS = 8192
MAX_POLYNOMIAL_DEGREE = 160
STATS = {"interval_operations": 0, "max_symbolic_bits": 0,
         "max_polynomial_product_degree": 0, "quadrature_calls": 0,
         "matrix_calls": 0, "inverse_calls": 0, "cutoff_extensions": 0}
RESULT = {"arithmetic_status": "HOLD", "schur_status": "NOT EVALUATED / HOLD",
          "grid_digits": 120, "wall_cap_internal_seconds": WALL_SECONDS,
          "address_space_cap_bytes": MEMORY_BYTES,
          "symbolic_bit_cap": MAX_SYMBOLIC_BITS,
          "constant_boxes_status": "inherited outward enclosures",
          "whole_source_crude_bound_status": "inherited premise"}
OUT = None


def checked(f):
    """Bounded exact symbolic algebra; not an enclosure endpoint operation."""
    f = Fraction(f)
    bits = max(abs(f.numerator).bit_length(), f.denominator.bit_length())
    STATS["max_symbolic_bits"] = max(STATS["max_symbolic_bits"], bits)
    if bits > MAX_SYMBOLIC_BITS:
        raise ArithmeticHold("exact symbolic bit cap exceeded")
    return f


def ceildiv(a, b):
    assert b > 0
    return -((-a) // b)


def decimal_grid(n):
    sign = "-" if n < 0 else ""
    n = abs(n)
    whole, part = divmod(n, SCALE)
    return sign + str(whole) + "." + str(part).zfill(120)


class I:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi):
        assert isinstance(lo, int) and isinstance(hi, int) and lo <= hi
        self.lo, self.hi = lo, hi

    @staticmethod
    def rational(n, d=1):
        if d < 0:
            n, d = -n, -d
        assert d > 0
        STATS["interval_operations"] += 1
        return I(n * SCALE // d, ceildiv(n * SCALE, d))

    @staticmethod
    def fraction(f):
        return I.rational(f.numerator, f.denominator)

    @staticmethod
    def coerce(v):
        if isinstance(v, I):
            return v
        if isinstance(v, int):
            return I(v * SCALE, v * SCALE)
        raise TypeError("only grid intervals and exact integers are allowed")

    def zero(self):
        return self.lo == 0 and self.hi == 0

    def __add__(self, other):
        other = I.coerce(other)
        STATS["interval_operations"] += 1
        return I(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        STATS["interval_operations"] += 1
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-I.coerce(other))

    def __rsub__(self, other):
        return I.coerce(other) + (-self)

    def __mul__(self, other):
        other = I.coerce(other)
        STATS["interval_operations"] += 1
        products = (self.lo * other.lo, self.lo * other.hi,
                    self.hi * other.lo, self.hi * other.hi)
        return I(min(products) // SCALE, ceildiv(max(products), SCALE))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = I.coerce(other)
        if other.lo <= 0 <= other.hi:
            raise ArithmeticHold("interval division by an interval containing zero")
        STATS["interval_operations"] += 1
        lows, highs = [], []
        for a in (self.lo, self.hi):
            for b in (other.lo, other.hi):
                n, d = a * SCALE, b
                if d < 0:
                    n, d = -n, -d
                lows.append(n // d)
                highs.append(ceildiv(n, d))
        return I(min(lows), max(highs))

    def square(self):
        STATS["interval_operations"] += 1
        low = 0 if self.lo <= 0 <= self.hi else min(self.lo ** 2, self.hi ** 2)
        high = max(self.lo ** 2, self.hi ** 2)
        return I(low // SCALE, ceildiv(high, SCALE))

    def sqrt(self):
        assert self.lo >= 0, "negative lower endpoint passed to sqrt"
        STATS["interval_operations"] += 1
        low = math.isqrt(self.lo * SCALE)
        high = math.isqrt(self.hi * SCALE)
        if high * high < self.hi * SCALE:
            high += 1
        return I(low, high)

    def record(self):
        return {"lower": decimal_grid(self.lo), "upper": decimal_grid(self.hi),
                "width": decimal_grid(self.hi - self.lo)}


ZERO = I(0, 0)
ONE = I(SCALE, SCALE)


def interval_box(pair):
    low, high = (checked(Fraction(s)) for s in pair)
    assert low <= high
    return I(I.fraction(low).lo, I.fraction(high).hi)


def short(n, direction):
    """Outward scientific display, 20 significant digits; arithmetic never uses it."""
    if n == 0:
        return "0"
    power = max(0, len(str(abs(n))) - 20)
    unit = 10 ** power
    v = n // unit if direction == "down" else ceildiv(n, unit)
    if v == 0:
        return "0"
    sign = "-" if v < 0 else ""
    digits = str(abs(v))
    exponent = len(digits) - 1 + power - 120
    return sign + digits[0] + "." + digits[1:] + "e" + str(exponent)


def show(name, v):
    assert isinstance(v, I)
    RESULT[name] = v.record()
    print(name + " = [" + short(v.lo, "down") + ", " + short(v.hi, "up") + "]", flush=True)


def checkpoint(label):
    RESULT["last_valid_checkpoint"] = label
    RESULT["elapsed_seconds"] = time.monotonic() - START
    RESULT["peak_rss_kib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    RESULT["stats"] = dict(STATS)
    if OUT is not None:
        temp = OUT / "result.tmp"
        temp.write_text(json.dumps(RESULT, ensure_ascii=False, indent=2) + "\n")
        temp.replace(OUT / "result.json")
    print("checkpoint=" + label + " elapsed_seconds=" + format(RESULT["elapsed_seconds"], ".6f"), flush=True)


def note_degree(degree):
    assert degree <= MAX_POLYNOMIAL_DEGREE, "polynomial degree cap exceeded"
    STATS["max_polynomial_product_degree"] = max(STATS["max_polynomial_product_degree"], degree)


def integer_product(a, b):
    note_degree(len(a) + len(b) - 2)
    out = [0] * (len(a) + len(b) - 1)
    for j, x in enumerate(a):
        if x:
            for k, y in enumerate(b):
                if y:
                    out[j + k] += x * y
    for value in out:
        checked(value)
    return out


def polynomial_product(a, b):
    note_degree(len(a) + len(b) - 2)
    out = [ZERO] * (len(a) + len(b) - 1)
    for j, x in enumerate(a):
        if not x.zero():
            for k, y in enumerate(b):
                if not y.zero():
                    out[j + k] = out[j + k] + x * y
    return out


def integrate(poly, left, right):
    """Closed polynomial antiderivative, ordinary integral (not E0)."""
    primitive = [ZERO] + [c / (j + 1) for j, c in enumerate(poly)]

    def horner(t):
        value = ZERO
        for c in reversed(primitive):
            value = value * t + c
        return value

    return horner(right) - horner(left)


def shifted_poly(poly, delta):
    powers = [ONE]
    for j in range(1, len(poly)):
        powers.append(powers[-1] * (-delta))
    out = [ZERO] * len(poly)
    for k in range(len(poly)):
        for j in range(k, len(poly)):
            if not poly[j].zero():
                out[k] = out[k] + poly[j] * math.comb(j, k) * powers[j - k]
    return out


def main():
    global OUT
    assert len(sys.argv) == 3, "usage: certify_tail.py input.json output_directory"
    input_path, OUT = Path(sys.argv[1]), Path(sys.argv[2])
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "ATTEMPT_STARTED").open("x") as marker:
        marker.write("One computation attempt. Do not rerun in this directory.\n")
    print("attempt=1 grid=10^-120 wall_internal=290s wall_external=295s memory_AS=768MiB", flush=True)
    RESULT["python_version"] = platform.python_version()
    RESULT["input_sha256"] = hashlib.sha256(input_path.read_bytes()).hexdigest()
    RESULT["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print("python=" + RESULT["python_version"], flush=True)
    print("input_sha256=" + RESULT["input_sha256"], flush=True)
    print("code_sha256=" + RESULT["code_sha256"], flush=True)
    data = json.loads(input_path.read_text())
    assert Fraction(data["B"]) == Fraction(3, 4)
    assert data["M"] == 128 and Fraction(data["theta"]) == Fraction(1, 65536)
    denominator = int(data["hA_grid_denominator"])
    nums = data["hA_grid_numerators"]
    assert denominator == 10 ** 40 and len(nums) == 16 and nums[15] == 0 and nums[14] != 0
    assert all(isinstance(z, int) for z in nums)

    # Exact source binding: expand the (1-t^2)^r coefficients, NOT Legendre data.
    pnums = [0] * 29
    for r in range(15):
        for k in range(r + 1):
            pnums[2 * k] += nums[r] * math.comb(r, k) * (-1) ** k
    p2nums = integer_product(pnums, pnums)
    H_exact = Fraction(0)
    for k, c in enumerate(p2nums):
        if c:
            assert k % 2 == 0
            H_exact = checked(H_exact + checked(Fraction(c, denominator ** 2 * (k + 1))))
    H_given = checked(Fraction(data["H_A"]))
    assert H_exact == H_given and H_exact > 0, "H_A exact source binding failed"
    RESULT["H_A_exact_binding"] = "PASS"
    print("H_A_exact_binding=PASS degree_p=28", flush=True)
    H = I.fraction(H_given)
    sqrtH = H.sqrt()
    show("H_A", H)
    show("sqrt_H_A", sqrtH)

    # Finite exact symbolic identity check of the supplied complete remainders.
    U, V = [Fraction(1)], [Fraction(1)]
    for n in range(1, 49):
        u, v = Fraction(0), Fraction(0)
        for j in range(1, n + 1):
            u = checked(u - checked(U[n - j] / math.factorial(2 * j + 1)))
            v = checked(v - checked(V[n - j] / math.factorial(2 * j)))
        U.append(u)
        V.append(v)
    q0 = Fraction(3, 4)

    def tail(j, e):
        numerator = checked(q0 ** (2 * j))
        ratio = checked(q0 ** 2 / ((2 * j + e + 1) * (2 * j + e + 2)))
        return checked(checked(numerator / math.factorial(2 * j + e)) / checked(1 - ratio))

    Ek_exact = Fraction(0)
    for n in range(49):
        first = checked(checked(abs(U[n]) * tail(49 - n, 1)) / q0)
        second = checked(abs(V[n]) * tail(49 - n, 0))
        term = checked(checked(q0 ** (2 * n)) * checked(first + second))
        Ek_exact = checked(Ek_exact + checked(term / 4))
    assert Ek_exact == checked(Fraction(data["Ek"])), "Ek exact recurrence binding failed"
    tq = Fraction(3, 8)
    th_exact = checked(checked(tq ** 32 / math.factorial(32)) /
                       checked(1 - checked(tq ** 2 / (33 * 34))))
    assert th_exact == checked(Fraction(data["th"])), "th exact binding failed"
    RESULT["Ek_exact_binding"] = "PASS"
    RESULT["th_exact_binding"] = "PASS"
    print("Ek_exact_binding=PASS th_exact_binding=PASS kernel_order=96", flush=True)
    Ek, th = I.fraction(Ek_exact), I.fraction(th_exact)
    epar = 4 * (I.rational(23, 10 ** 48) + I.rational(20700, 10 ** 96)) + I.rational(26, 10 ** 96)
    eop = epar + Ek * 3 / 2 + th * 9 / 2
    RESULT["E_k"] = Ek.record()
    RESULT["t_h"] = th.record()
    RESULT["e_par"] = epar.record()
    RESULT["e_op"] = eop.record()
    checkpoint("exact_source_and_remainder_bindings")

    boxes = {name: interval_box(pair) for name, pair in data["constant_intervals"].items()}
    assert set(boxes) == {"L2", "L3", "r2", "r3"}
    pi = interval_box(data["pi_interval"])
    L2, L3 = boxes["L2"], boxes["L3"]
    assert L2.lo > 0 and L3.lo > 0
    assert boxes["r2"].lo > 0 and boxes["r3"].lo > 0
    p = [I.rational(c, denominator) for c in pnums]

    # Exact Legendre coefficients: P_m has common denominator 2^m.
    legendre_int, legendre_grid = {}, {}
    modes = list(range(0, 129, 2))
    assert len(modes) == 65 and modes[:16] == list(range(0, 31, 2))
    for m in modes:
        a = [0] * (m + 1)
        for k in range(m // 2 + 1):
            a[m - 2 * k] = (-1) ** k * math.comb(2 * m - 2 * k, m - k) * math.comb(m - k, k)
        legendre_int[m] = a
        legendre_grid[m] = [I.rational(c, 2 ** m) for c in a]
    RESULT["removed_even_modes"] = modes

    # Closed beta-derivative moments, valid for every nonnegative k.
    harmonic = [ZERO]
    for j in range(1, 159):
        harmonic.append(harmonic[-1] + I.rational(1, j))
    Wmom, W2mom = [], []
    odd_square_sum = ZERO
    pi_square = pi.square()
    for k in range(79):
        D = 2 * harmonic[2 * k + 2] - harmonic[k + 1] - 2 * L2
        Wmom.append(D / (2 * (2 * k + 1)))
        if k <= 28:
            odd_square_sum = odd_square_sum + I.rational(1, (2 * k + 1) ** 2)
            W2mom.append((D.square() + 4 * odd_square_sum - pi_square / 3) / (4 * (2 * k + 1)))
    NW = ZERO
    for k, c in enumerate(p2nums):
        if c:
            NW = NW + I.rational(c, denominator ** 2) * W2mom[k // 2]
    PW = ZERO
    W_records = []
    for m in modes:
        prod = integer_product(legendre_int[m], pnums)
        moment = ZERO
        for k, c in enumerate(prod):
            if c:
                assert k % 2 == 0
                moment = moment + I.rational(c, 2 ** m * denominator) * Wmom[k // 2]
        contribution = (2 * m + 1) * moment.square()
        PW = PW + contribution
        W_records.append({"m": m, "E0_Pm_uW": moment.record(), "squared_coefficient": contribution.record()})
    assert len(W_records) == 65
    RESULT["W_modes"] = W_records
    show("N_W", NW)
    show("P_W", PW)
    TW2 = NW - PW
    show("tail_W_squared_enclosure", TW2)
    assert TW2.hi >= 0, "INVALID ASSERTION: negative W tail upper (no clipping allowed)"
    UW = I(TW2.hi, TW2.hi)
    yW_interval = UW.sqrt()
    yW = I(yW_interval.hi, yW_interval.hi)
    show("U_W", UW)
    show("y_W_upper", yW)
    checkpoint("W_complete_65_modes")

    # Boundary expressions are (c + a log(2) + b log(3))/3.
    # Exact symbolic equality is checked before interval ordering. log(4)=2log(2).
    boundary_cache = {}

    def boundary(expr):
        if expr not in boundary_cache:
            c, a, b = expr
            boundary_cache[expr] = (I.coerce(c) + a * L2 + b * L3) / 3
        return boundary_cache[expr]

    def compare(a, b):
        if a == b:
            return 0
        va, vb = boundary(a), boundary(b)
        if va.hi < vb.lo:
            return -1
        if va.lo > vb.hi:
            return 1
        raise ArithmeticHold("uncertain support-endpoint ordering: " + repr((a, b)))

    def maximum(a, b):
        return a if compare(a, b) >= 0 else b

    def minimum(a, b):
        return a if compare(a, b) <= 0 else b

    coefficients = {2: L2 * boxes["r2"], 3: L3 * boxes["r3"], 4: L2 / 2}
    log_weights = {2: (4, 0), 3: (0, 4), 4: (8, 0)}
    branches = []
    for n in (2, 3, 4):
        for sign in (-1, 1):
            a, b = log_weights[n]
            a, b = sign * a, sign * b
            left = maximum((-3, 0, 0), (-3, a, b))
            right = minimum((3, 0, 0), (3, a, b))
            assert compare(left, right) < 0
            shifted = shifted_poly(p, boundary((0, a, b)))
            poly = [coefficients[n] * c for c in shifted]
            branches.append({"name": str(n) + ("+" if sign > 0 else "-"),
                             "left": left, "right": right, "poly": poly})
    assert len(branches) == 6
    RESULT["branch_supports"] = [
        {"name": b["name"], "left_expression": b["left"], "right_expression": b["right"],
         "left": boundary(b["left"]).record(), "right": boundary(b["right"]).record()}
        for b in branches]
    NS, pair_records = ZERO, []
    for i in range(6):
        for j in range(i, 6):
            left = maximum(branches[i]["left"], branches[j]["left"])
            right = minimum(branches[i]["right"], branches[j]["right"])
            ordering = compare(left, right)
            multiplicity = 1 if i == j else 2
            if ordering >= 0:
                contribution = ZERO
            else:
                product = polynomial_product(branches[i]["poly"], branches[j]["poly"])
                contribution = integrate(product, boundary(left), boundary(right)) * multiplicity / 2
            NS = NS + contribution
            pair_records.append({"i": branches[i]["name"], "j": branches[j]["name"],
                                 "multiplicity": multiplicity,
                                 "nonempty_intersection": ordering < 0,
                                 "contribution": contribution.record()})
    assert len(pair_records) == 21
    n2_pair = next(r for r in pair_records if r["i"] == "2-" and r["j"] == "2+")
    assert n2_pair["nonempty_intersection"], "n=2 branch overlap must be included"
    RESULT["shift_pairs"] = pair_records
    show("N_S", NS)
    print("shift_pairs=21 all_36_ordered_terms_preserved n2_overlap=YES", flush=True)
    checkpoint("shift_norm_all_cross_terms")
    PS = ZERO
    S_records = []
    for m in modes:
        moment = ZERO
        for branch in branches:
            product = polynomial_product(legendre_grid[m], branch["poly"])
            moment = moment + integrate(product, boundary(branch["left"]), boundary(branch["right"])) / 2
        contribution = (2 * m + 1) * moment.square()
        PS = PS + contribution
        S_records.append({"m": m, "E0_Pm_uS": moment.record(), "squared_coefficient": contribution.record()})
        if m in (32, 64, 96):
            RESULT["last_completed_shift_mode"] = m
            RESULT["shift_prefix_partial"] = PS.record()
            checkpoint("shift_modes_through_" + str(m))
    assert len(S_records) == 65
    RESULT["S_modes"] = S_records
    RESULT["last_completed_shift_mode"] = 128
    show("P_S", PS)
    TS2 = NS - PS
    show("tail_S_squared_enclosure", TS2)
    assert TS2.hi >= 0, "INVALID ASSERTION: negative S tail upper (no clipping allowed)"
    US = I(TS2.hi, TS2.hi)
    yS_interval = US.sqrt()
    yS = I(yS_interval.hi, yS_interval.hi)
    show("U_S", US)
    show("y_S_upper", yS)

    yrem_interval = eop * sqrtH
    yrem = I(yrem_interval.hi, yrem_interval.hi)
    ycert = yW + yS + yrem
    crude = (28 + eop) * sqrtH
    assert crude.lo > 0
    ratio = ycert / crude
    show("y_remainder_upper", yrem)
    show("y_certificate", ycert)
    show("Y_crude", crude)
    show("certificate_over_crude", ratio)
    show("crude_minus_certificate", crude - ycert)
    RESULT["reduction_status"] = "PASS" if ycert.hi < crude.lo else "NOT CERTIFIED"
    RESULT["analytical_source_binding_status"] = "PASS conditional on inherited constant boxes and source identification"
    RESULT["arithmetic_status"] = "COMPLETE"
    RESULT["tail_claim"] = "norm(T Y_actual) <= y_certificate.upper"
    RESULT["scope"] = "fixed h_A, M=128, W plus combined shifts plus one complete remainder; no response or Schur evaluation"
    assert STATS["max_polynomial_product_degree"] <= 160
    checkpoint("COMPLETE")
    print("arithmetic_status=COMPLETE reduction_status=" + RESULT["reduction_status"] +
          " schur_status=NOT_EVALUATED_HOLD", flush=True)
    print("elapsed_seconds=" + format(RESULT["elapsed_seconds"], ".6f") +
          " peak_rss_kib=" + str(RESULT["peak_rss_kib"]), flush=True)
    print("stats=" + json.dumps(STATS, sort_keys=True), flush=True)


if __name__ == "__main__":
    exit_code = 0
    try:
        main()
    except AssertionError as exc:
        RESULT["arithmetic_status"] = "INVALID ASSERTION"
        RESULT["error"] = str(exc)
        print("INVALID ASSERTION: " + str(exc), flush=True)
        traceback.print_exc()
        exit_code = 3
    except (BudgetHold, ArithmeticHold, MemoryError) as exc:
        RESULT["arithmetic_status"] = "HOLD"
        RESULT["error"] = type(exc).__name__ + ": " + str(exc)
        print("HOLD: " + RESULT["error"], flush=True)
        exit_code = 2
    except Exception as exc:
        RESULT["arithmetic_status"] = "HOLD"
        RESULT["error"] = type(exc).__name__ + ": " + str(exc)
        print("HOLD: " + RESULT["error"], flush=True)
        traceback.print_exc()
        exit_code = 2
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        if exit_code:
            # Retain the last valid mathematical checkpoint; only status changes.
            RESULT["elapsed_seconds"] = time.monotonic() - START
            RESULT["peak_rss_kib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            RESULT["stats"] = dict(STATS)
            if OUT is not None:
                (OUT / "result.json").write_text(json.dumps(RESULT, ensure_ascii=False, indent=2) + "\n")
            print("final_elapsed_seconds=" + format(RESULT["elapsed_seconds"], ".6f"), flush=True)
    sys.exit(exit_code)
