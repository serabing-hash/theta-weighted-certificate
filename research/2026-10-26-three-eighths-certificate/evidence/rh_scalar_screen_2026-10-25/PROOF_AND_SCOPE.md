# Frozen scalar screen: arithmetic, tails, scope

This is one approved scalar admission/dimension execution, not a Schur certificate. Original gate/review documents are read-only and unchanged. No matrices, residual rows, quadrature, eigenvalues, parameter optimization, extra radii, or extra numerical executions are permitted. Implementation preparation and static inspection do not evaluate its mathematical fixtures.

## Frozen specification

b=1/4, theta=9/10, epsilon=1/8, q=1/2; a0=0,1; R=3/4,1,5/4,3/2,7/4,2; L=R-1/4; integer cap1024. K uses j=1,...,8. Sbar uses **256 summands n=2,...,257**, first omitted n258. Decimal working precision is70 significant decimal digits (>128 bits). Analytic tail width is retained, not confused with working precision.

## Rounding

Every mathematical scalar is an interval of Decimal endpoints. Basic operations use explicit70-digit ROUND_FLOOR/ROUND_CEILING contexts. Multiplication takes the extrema over all four endpoint products; reciprocal excludes zero. The square implementation handles intervals spanning zero. Rational numbers enter via exact integer endpoints and directed division. No binary floating-point mathematics is used (runtime telemetry is not a mathematical result).

Python Decimal's exp and ln are correctly rounded using ROUND_HALF_EVEN, and sqrt is correctly rounded. Each monotone transcendental is evaluated at each endpoint in the70-digit nearest context, then widened by one adjacent representable Decimal in the outward direction. The sqrt lower endpoint is kept0 at exact0. This encloses the true endpoint value even when the nearest rounded result lies on the wrong side. Real powers use exp(exponent*ln(base)), enclosing all intermediate rounding. Min/max interval operations are monotone. Exact integer ceilings are declared only when both endpoints have the same ceiling; otherwise certified integer bounds are retained.

## Constants independent of unverified literals

Pi is enclosed by Machin's identity pi=16atan(1/5)-4atan(1/239). Each atan uses128 alternating terms (j=0,...,127); the even partial sum is a lower bound, and adding the next positive term1/(257 m^257) gives an upper bound. Fractions are computed exactly with Python integers before directed conversion.

Euler's constant uses n256 and

 gamma_E = H_n - log(n) - 1/(2n) + sum_{k=1}^{11} B_(2k)/(2k n^(2k)) + remainder.

The remainder is between B24/(24 n^24) and0. This follows from the standard positive Binet integral for the digamma remainder: expand1/(n^2+t^2) as a finite alternating geometric series inside the positive integral. Its remainder has the next term's sign and magnitude bounded by that term. Equivalently the digamma Euler–Maclaurin expansion is strictly enveloping for positive n. The Bernoulli coefficients through B24 are explicit rational constants in source. The harmonic sum is exact rational arithmetic. Neither pi nor gamma_E is supplied as an unverified decimal string.

## Positive series tails

For u_j=j^4 exp[-pi(j^2-1)],

 u_(j+1)/u_j = ((j+1)/j)^4 exp[-pi(2j+1)]
             <= (10/9)^4 exp(-19pi) = r_K, j>=9.

Both factors decrease with j. Thus omitted K terms are positive and at most4pi^2 u9/(1-r_K). Directed intervals enclose r_K and the resulting upper bound, with the denominator required positive by interval division. K is its partial sum plus[0,tail_upper].

Let a=(1-theta)pi/2 and f_n=(log n)n^(1/2-theta)exp(-an). Here1/2-theta=-2/5. For n>=258, the negative-power ratio is <=1, and

 log(n+1)/log n <= 1+1/(n log n) <= 1+1/n <=259/258.

Therefore f_(n+1)/f_n <=(259/258)exp(-a)=r_S<1. The omitted unscaled sum is bounded by f258/(1-r_S). Sbar multiplies the partial sum plus this positive tail interval by K^((1-theta)/2). These are genuine positive-tail enclosures, not an assumption that the cutoff truncation is exact.

## Finite prime sums and admission

All primes up to54 are identified by exact integer divisibility; their powers up to54 are enumerated without approximation. The run certifies log54<4<log55. Every inclusion/exclusion at thresholds2r and r is resolved using outward log intervals; unresolved membership raises an inconclusive failure rather than dropping a term. Finite beta sums use the actual Lambda(p^k)=log p weights, not Lambda(n)<=log n. Since every comparison is strictly separated, <= in the beta definition and < in the active-shift list select exactly the same sets at these fixed thresholds.

All R satisfy R>=b analytically. Hardy defect gamma exp(2R)-log(2B_H/epsilon) must be nonnegative; etabar must be <=epsilon/2. A failed sufficient admission test does not mean the underlying mathematical statement fails. Only admitted rows proceed to t0=epsilon-etabar, beta, Khat, and cap gates.

For D>0 the exact finite-radius K2 is evaluated in the algebraically identical, cancellation-resistant form

 K2=beta_L+2 beta_R^2/(sqrt(D^2+4 beta_R^2)+D).

Otherwise the displayed original formula is used. This is not an asymptotic replacement or a parameter search.

## Coercivity and meaning

Baseline has q0, Khat=beta_R, and retains the full metric in alpha. Thus even its a0=0 option has a_star=t0 m0>0; cell counting does not discard the metric from the form. Weighted q1/2 retains half the metric and has a_star=a0+t0 m0/2>0. Actual alpha(x), not a_star, would belong in any later Gram integration. Smaller a0 reduces F and its sufficient cell count but weakens the coarse error denominator sqrt(2R/a_star); no residual-error calculation is performed here.

A cap failure rejects only this sufficient recipe within1024 cells. A pass is only a cell-count candidate: no signed residual margin, useful solver cost, fixed-radius spectral certificate, or epsilon-to-zero RH sequence follows.

## Single-run guard

`bash rh_scalar_screen_2026-10-25/run_once.sh` creates an exclusive launch lock and an initial receipt. Before mathematical executable launch, address space is capped at256MiB and CPU at59seconds. The setup process arms a59second real-time alarm and `exec`s the numerical script: same PID, no child, no supervisor. Exec preserves the alarm. This uses a1second safety margin relative to the authorized60second numerical wall/CPU limit. The alarm retains its default hard-termination disposition; a timeout/OOM leaves the initial receipt and last output state for the parent to record as inconclusive. No retries occur. The marker prevents another launch. The shell and setup only prepare guards; no mathematical fixture is run there.
