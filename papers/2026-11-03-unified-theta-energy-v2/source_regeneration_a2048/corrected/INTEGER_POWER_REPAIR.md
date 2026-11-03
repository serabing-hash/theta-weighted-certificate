# Integer-power arithmetic repair

The historical producer's precision-70 Decimal endpoint square of the exact
value `1 + 10^-40` has an upper endpoint below its exact square by `10^-80` on
the audited libmpdec 4.0.0 runtime. A negative odd-power lower-bound example also
fails. This disproves the general primitive enclosure contract, not any asserted
actual-production operand or the final analytic inequality.

The original module is preserved under `../historical/src/` with SHA-256
`0c11bbcf4cb7e92bd1e57853f3d364001d3ce2d237e3223c5db0e95d5bd5531c`.
The corrected module `src/interval_bounds.py` has SHA-256
`95f90cb8ac6e1d73ea7639c0e44140a4df4a9ed96923945d16ebde80d0a6a05b`.
The adjacent patch makes the exact scientific change explicit. All other
selected producer modules retain their original bytes.

## One-sided multiplication proof


Assume the existing primitive Decimal multiplication is correctly rounded in the requested directed mode. Restrict this proof to finite results accepted by IV; overflow or another exceptional situation must raise rather than produce an accepted nonfinite interval.

### 1. Nonnegative endpoint powers

Let a be the exact nonnegative finite-decimal endpoint, and let n be a nonnegative integer. Use binary exponentiation with an accumulator initially 1 and a factor initially a. For a lower bound, round every product and square toward negative infinity; for an upper bound, round every product and square toward positive infinity.

For the lower algorithm maintain 0 ≤ stored accumulator ≤ its corresponding exact accumulated power and 0 ≤ stored factor ≤ its corresponding exact squared power. Multiplication is monotone in both arguments on the nonnegative quadrant. Correct downward rounding therefore preserves both inequalities at each update. The upper algorithm maintains the reversed inequalities by the same argument. Binary exponentiation's exact exponent identity then proves the final lower ≤ a^n ≤ upper. Repeated occurrence of a introduces dependency, but does not invalidate these bounds.

This proof relies on one-sided multiplication, not a power approximation's guard-digit count. It applies equally to sequential multiplication and exponentiation by squaring. Rounding an endpoint that initially has more digits than the working precision also preserves the invariant, provided rounding is directed and no context-rounded preprocessing alters the exact input first.

### 2. Signed endpoints

For x < 0 and even n, x^n = |x|^n, so use the same bound direction on the exact magnitude.

For x < 0 and odd n, x^n = -|x|^n. A lower endpoint therefore requires the **upper** magnitude bound followed by exact negation; an upper endpoint requires the **lower** magnitude bound followed by exact negation. Use `copy_abs()` and `copy_negate()`, which do not round to the unrelated ambient context. Ordinary context-rounded unary operations outside the directed context must not silently shorten an input or result.

### 3. Interval range and parity

For odd positive n, the power function is increasing on the real line; directed endpoint images enclose the whole interval. For even positive n, the function decreases to zero on the negative half-line and increases on the positive half-line. Therefore the extrema are endpoint powers if the interval excludes zero, and zero plus the larger endpoint magnitude's power if it contains zero. Taking the minimum of downward endpoint evaluations and maximum of upward endpoint evaluations is valid for the zero-excluding case.

A generic IV-multiplication implementation is also safe without these monotonicity shortcuts, though it may produce a wider lower bound when squaring an interval across zero.

### 4. Zero and negative exponents

n = 0 returns [1,1], preserving the existing IV convention, including a zero-containing base. n = 1 may return the interval unchanged or perform valid directed endpoint rounding.

For n < 0, reject any interval containing zero. On either remaining half-line, reciprocal is decreasing, so the existing directed reciprocal `[round_down(1/hi), round_up(1/lo)]` encloses every reciprocal. Applying the proved positive-power algorithm to that enclosing interval then encloses x^n. If underflow causes the intermediate reciprocal enclosure to contain zero, the resulting wider positive-power interval is still safe; any unbounded/overflowing endpoint must fail closed under the finite-IV contract.

## Test and inventory scope

The original 31 tests and six new exact-rational power test groups passed.
A separately authored checker passes 3,347 exact-Fraction interval cases and 21
type/domain rejections; its additional range tests pass 64 underflow cases and
32 fail-closed overflow cases. A further independent review passed 1,344 cases.
These finite tests support the preceding invariant argument, not a universal
proof by enumeration.

`reports/POWER_SITE_INVENTORY.json` preserves the 23-module, 127-site audit. Only
three original sites use raw Decimal endpoint powers, and the patch replaces
all three. The other sites were traced to IV, exact integer/Fraction arithmetic,
exact binary power-of-two constants or floating diagnostics. The public source
selection excludes unused historical orchestration modules; their hashes remain
in the complete inventory. This inventory is not an audit of every floating
error bound or arbitrary external call with unexpected types.

From this corrected-profile directory, the two portable independent checks are:

```sh
python3 audits/test_repaired_power_independently.py --snapshot src \
  --output work/INDEPENDENT_POWER_CHECK.json
python3 audits/test_repaired_power_boundaries.py --snapshot src \
  --output work/POWER_RANGE_CHECK.json
```

Create the output directory first. The checkers import only the selected interval
module and test synthetic primitive inputs; they never run source production.
Their small path/output adaptations are declared in
`reports/AUDIT_ADAPTER_PROVENANCE.json`.

## What this repair does not establish

It does not retroactively validate unrecomputed historical enclosures, does not
repair the separate a1024 run by association, and does not certify the complete
a2048 pipeline merely because the module tests pass. Dependent corrected
production, fresh reference binding and exact finite signs have separate
execution evidence in `../GENERATION_VALIDATION.md`. The complete analytic and
form-domain premises remain necessary. The global half inequality and RH remain
unproved.
