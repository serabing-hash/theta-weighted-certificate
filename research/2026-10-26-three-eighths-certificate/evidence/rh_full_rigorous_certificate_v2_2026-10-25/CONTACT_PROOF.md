# Exact contact-log jets for the fixed full residual certificate

25 October 2026 UTC. Static derivation only. No numerical evaluation, benchmark, execution, or modification of the running certificate sources was performed for this note.

## Conclusion and scope

The proposed contact substitution is mathematically valid and directly implementable. It removes interval dependency in the known identity `log(L u^8)=log L+8 log u`, rather than hoping that generic interval jet recurrences cancel it. It does not establish that the resulting global error will meet the spectral margin. The current full run must remain unchanged; this is a separate follow-up implementation proposal.

Let `S(s)=Gplus(s)+Gminus(s)` and `D(s)=Gplus(s)-Gminus(s)`. Then, for `s>0`,

    S(s)=log(expm1(s))=log s+s/2+log(sinhc(s/2)),
    D(s)=log(1+exp(s))=log 2+s/2+log cosh(s/2),
    sinhc(z)=sinh(z)/z, sinhc(0)=1.

The full exponential prefactors multiplying S and D in the original Gamma rows must remain. Only the evaluation of a known contact S factor is changed.

## 1. A rational regular polynomial

The classical product for sinh gives, for `|s|<2*pi`,

    log(sinhc(s/2))
      = sum_(k>=1) a_k s^(2k),
    a_k = (-1)^(k+1) zeta(2k)/(k*(2*pi)^(2k)).

The first four coefficients are exactly

    a1=1/24,
    a2=-1/2880,
    a3=1/181440,
    a4=-1/9676800.

They also follow from formal division and integration of the elementary Taylor series for sinh/cosh. No rounded special-function coefficient is needed.

For a contact distance `s=L*u^8`, with `L>0` constant and `u>0`, define

    P(u)=log L+8 log u+(L/2)u^8
         +u^16 L^2/24-u^32 L^4/2880
         +u^48 L^6/181440-u^64 L^8/9676800.

The exact contact function is `P(u)+T(u)`.

## 2. Direct normalized derivatives through order four

Write `J_j f=f^(j)/j!`. On a positive interval U, every occurrence below is evaluated by directed interval arithmetic, with the exact parameter L enclosed consistently.

For j=0,

    J_0 P = log L+8log U+(L/2)U^8
            +sum_(k=1)^4 a_k L^(2k) U^(16k).

For 1<=j<=4,

    J_j P = 8*(-1)^(j-1)/(j*U^j)
            +(L/2)*binom(8,j)*U^(8-j)
            +sum_(k=1)^4 a_k L^(2k)*binom(16k,j)*U^(16k-j).

These formulas are exact. They use no repeated reciprocal/log composition for the singular part. In particular the first term is the derivative of `8log u`, not a bound obtained by differentiating `log(exp(Lu^8)-1)` through intervals.

## 3. Explicit derivative tail, including j=0

Let Lh and b be positive upper bounds for L and U, with `0<b<=1` and `Lh<1` (the present phase lengths are bounded by the fine cell width). Use only the elementary bounds `zeta(2k)<2` and `2*pi>6`.

For j in {0,1,2,3,4}, put

    q=(Lh/6)^2*b^16,
    r_j=q*[96/(81-j)]^j,
    E_j=[(2/5)*(Lh/6)^10*binom(80,j)*b^(80-j)]/(1-r_j).

If the interval implementation proves `r_j<1`, then

    |J_j T(u)| <= E_j for every u in U.

Thus `J_j S(Lu^8)` is enclosed by the direct polynomial/log interval in section 2 plus `[-E_j,E_j]`.

Proof: the absolute normalized derivative of omitted term k is bounded by

    t_(k,j)=(2/k)*(Lh/6)^(2k)*binom(16k,j)*b^(16k-j), k>=5.

Since all relevant exponents are nonnegative, replacing u by b is valid. For k>=5,

    t_(k+1,j)/t_(k,j)
       <= q*[16(k+1)/(16k-j+1)]^j
       <= q*[96/(81-j)]^j = r_j.

For j=0 the bracket power is one. The dropped factor k/(k+1) is <=1. Summing the geometric majorant beginning at k=5 gives the displayed E_j. This bounds derivative tails themselves; it is not the invalid use of a function-only tail as a derivative bound.

All powers, binomial integers, rational coefficients, upper bounds and the denominator must be evaluated outward. The condition `r_j<1` must be checked, not assumed by a floating comparison. No independent numerical value for any E_j is asserted here.

## 4. Exact contact cache locations

The existing universal-phase cache uses `x=q*delta+phase(u)` and branches q<0, q=0, q>0 relative to the source cell (0,delta).

For the left endpoint template, `phase(u)=L*u^8`:

- q=0, the inside term S(x) is contact; S(delta-x) is smooth.
- q=1, the outside-near distance `a=x-delta=L*u^8` is contact.
- All other S distances in that cache are positive away from zero.

For the right endpoint template, `phase(u)=delta-L*u^8`:

- q=0, the inside term S(delta-x) is contact; S(x) is smooth.
- q=-1, the outside-near distance `a=-x=L*u^8` is contact.
- All other S distances in that cache are positive away from zero.

For either outside contact case, replace the singular `Sdiff(a)` implementation by

    Sdiff(a)=S(a+delta)-S_contact(L,u).

Its far term may use the existing directed smooth S jet. The Ddiff term is analytic at a=0 and may retain its existing implementation. The original signs remain:

    left outside:  s=-Sdiff(a)/2, d=-Ddiff(a)/2,
    right outside: s=-Sdiff(a)/2, d=+Ddiff(a)/2.

For the inside source cell,

    s=C0-[S(delta-x)+S(x)]/2,
    d=[D(x)-D(delta-x)]/2.

Only the indicated S factor is replaced; both full cosh/sinh prefactors and normalizers remain unchanged.

## 5. Minimal implementation interface

A helper of the form

    J contact_S(const I& L, const I& u_interval)

can fill its five normalized coefficients directly using sections 2–3. It requires a positive interval `u_interval`, not a general composed jet. The caller computes it once for the point interval and once for the domain interval of each transformed template. Pass these two contact jets into the corresponding cache evaluations.

The existing template metadata already identifies left/right endpoints structurally (`transformed` and sign), avoiding an unreliable floating equality test against zero or delta. The actual analytic endpoint tail u=0 remains in the separate affine-log integration routine and must not be passed to this helper.

## 6. Why it can sharpen, and what remains open

On the first of two subdivisions of a dyadic u band, the endpoint ratio is 3/2. Applying u^8 before interval log differentiation makes the physical distance ratio (3/2)^8. Generic reciprocal/log jet formulas then combine strongly dependent terms with unnecessarily large interval ranges. The direct log-u derivatives avoid this artificial dependency exactly.

This diagnosis does not prove that it is the sole or dominant source of the final global error. Remaining conservative effects include row-norm triangle inequalities, loss of cancellation between the projected residual and its original-cell trial, smooth-distance jet bounds, matrix Taylor remainder summation, and the fixed panel widths. The proposal must be audited and measured in a separately authorized bounded attempt. It does not establish a finite inertia certificate or RH.
