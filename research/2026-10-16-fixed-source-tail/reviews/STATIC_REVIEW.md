# Publication note

This is a scoped static-review record. Public relative paths replace local artifact paths. The original 337-check output is preserved; the portable version makes only path/selected-input-label changes and is separately checked. Later independent constant checks are described in CLAUDE_scoped_audit.md. Statements about prior execution metrics rely on the preserved output record.

# Independent static review of the fixed M=128 source-tail certificate

Date: 2026-10-15 UTC. Scope: read-only review of the completed bundle, original task, and source binding. The source-tail calculation was **not rerun**. The only executed checks were hashes, exact scalar identities, isolated interval primitives, and saved-output consistency.

## Verdict

**No blocking mathematical or implementation defect found.** The supplied certificate is valid for the requested fixed actual-source tail, conditional on the explicitly inherited physical source identification and outward constant boxes. The finite arithmetic record is internally consistent and COMPLETE. The comparison against the inherited crude whole-source norm bound is certified. Response improvement and the Schur sign remain **NOT EVALUATED / HOLD**.

- `||Pi_even,>128 Y_actual|| <= 8.4874678247291907546e-12`.
- `Y_crude` lies in `[2.2782392677405310185e-2, 2.2782392677405310186e-2]`.
- The **certificate constant divided by the crude bound**, not the actual tail's ratio, lies in `[3.7254505902475865957e-10, 3.7254505902475865958e-10]`.
- This is a norm bound. It is neither a squared norm nor `C(Y)`, and it must not be compared directly with the recorded quadratic `Q_up` or prefix-reference baseline.

The relevant bundle directory is `../source_tail_M128/`, relative to this review. Code line references below refer to its `certify_tail.py`.

## 1. Exact task and provenance binding: PASS

- All **9 entries** of `MANIFEST.sha256` verified.
- Bundled `request.txt`, the parent `max_source_tail_request.txt`, and `max_source_tail_artifacts/submitted_input.txt` are byte-identical.
- `input.json` is byte-identical to the JSON appended to the request, not merely structurally equivalent.
- The input and code SHA256 values in `run/result.json` match the actual files, the manifest, and stdout.
- Independently rehashed original `DESIGN.json`, `EXACT_FIXED_DIRECTION.json`, `response_link/MAIN_PROOF.md`, and `SIX_MAIN_PROOF.md`; all four match the request's hashes.
- All 16 witness numerators, exact `H_A`, all four constant boxes, pi box, `Ek`, and `th` match their original source fields.
- Lines 289–308 enforce the frozen B, M, theta, grid denominator, degree-28 polynomial, and exact norm identity. Lines 296–300 correctly expand the `(1-t^2)^r` basis; these are not treated as Legendre coordinates.
- An independent alternate check used `E0[(1-t^2)^j] = 2^(2j)(j!)^2/(2j+1)!` directly in the original basis. It reproduced `H_A` exactly without the code's monomial expansion route.

The original crude-bound premise was also located at `response_link/MAIN_PROOF.md:238–245`: `||Y_actual-Y0|| <= eop||h_A||`, `||Y0|| <= 28||h_A||`. Hence the stated crude comparator follows by the triangle inequality. This review does not reprove the original operator-to-source reduction or the entire earlier proof.

## 2. Physical normalization and complete Parseval subtraction: PASS

For `f(Bt)=u(t)/sqrt(2B)` and `dx=B dt`, the physical norm is `E0[u^2]` and the coefficient is `sqrt(2m+1) E0[P_m u]`. Thus W has the requested `1/8` total-log-squared integral factor and `-sqrt(2m+1)/4` log-moment factor.

- Lines 363–373 construct the standard exact Legendre polynomial coefficients and exactly the 65 even modes `0,2,...,128`. The first 16 are explicitly checked as `0,2,...,30`.
- Lines 375–400 implement the full beta-derivative W and W-squared moments with the correct factors, for W through `k=78` and W-squared through `k=28`. No high-only singular quotient is used.
- Lines 401–413 and 494–510 multiply squared E0 moments by `2m+1`, subtract all 65 modes, use total-norm upper minus prefix-squared-norm lower, and take the upper square root.
- `TW2.hi` and `TS2.hi` are asserted nonnegative before conversion to upper constants (lines 410 and 507); there is no zero-clipping of a negative upper.
- W and the combined S are each even and in L2. Parseval therefore leaves their complete infinite tails, rather than a finite sampling approximation.

The independent saved-output check verified all 130 coefficient-square records and both 65-term prefix sums exactly on the grid. Both saved tail intervals have positive lower endpoints.

## 3. Shift supports, overlaps, cross terms, and dependency: PASS

- Lines 418–436 express boundaries as `(c+a log2+b log3)/3`, check symbolic equality, and otherwise require separated outward intervals before choosing endpoint order. Uncertain order raises HOLD.
- Lines 444–457 use `c2=L2*r2`, `c3=L3*r3`, `c4=L2/2` and displacements `4L2/3`, `4L3/3`, `8L2/3`. Thus `log4=2log2` remains bound to the same variable.
- `shifted_poly` (262–271) is exactly `p(t-delta)` by the binomial theorem. The branch support is the intersection of `[-1,1]` with `[delta-1,delta+1]`.
- Lines 464–480 include all 21 unordered pairs with multiplicity 1 on the diagonal and 2 off diagonal: all 36 ordered terms. All six weighted branch polynomials are retained before pairwise integration.
- The n=2 two-branch overlap is explicitly checked at 481–482. In the saved record 13 of the 21 intersections are nonempty, including this overlap; the others contribute zero due to disjoint supports.
- `integrate` (249–259) uses a polynomial antiderivative evaluated outward by Horner. The factor `1/2` in 474 and 493 is exactly E0, with no extra square-root normalization.
- Lines 489–496 integrate each branch for every requested mode. The independent check confirmed the complete 21-pair list, its multiplicities, and the sum of all saved contributions equals `N_S`.

The code does not replace the discontinuous shifted function by a global polynomial or apply an H2 tail estimate. Only its pieces are polynomial.

## 4. Interval arithmetic and output direction: PASS

The arithmetic grid is exactly `10^-120` (49). Grid values are integer endpoints; no binary floating-point numbers enter the certificate arithmetic.

- Rational conversion, 94–99: floor lower, ceiling upper, including negative numerators.
- Addition and negation, 116–131: exact grid operations with reversed endpoints under negation.
- Multiplication, 133–138: all four endpoint products, floor of minimum and ceiling of maximum.
- Division, 142–155: zero-containing divisors rejected; all four endpoint quotients checked, denominators sign-normalized, outward-rounded. Correct for either sign of a zero-free denominator interval.
- Square, 157–161: lower is zero when the interval contains zero; otherwise minimum endpoint square. Upper is maximum endpoint square, with proper outward rounding.
- Square root, 163–170: `isqrt(lo*SCALE)` for the lower and ceiling integer square root of `hi*SCALE` for the upper.
- Lines 514–525: one upper remainder, sum of upper norm constants, outward crude bound, outward ratio, and strict `ycert.hi < crude.lo` comparison. Both sides have norm units.

Isolated tests extracted only `I`, `ceildiv`, and `ArithmeticHold` by AST, never importing/executing the script top level or calling `main`. Tests covered negative/positive/sign-crossing/zero and tiny grid intervals, division on both denominator signs, squares, and exact/nonexact roots. These are supplemental tests; validity is based on the endpoint argument above.

Every saved interval record has consistent ordered endpoints and exact grid width. All final stored quantities were independently reconstructed from the saved intermediate enclosures, including eop, both tails, their upper square roots, yrem, ycert, crude, ratio, and gap.

## 5. Complete kernel/pole remainder and actual source: PASS

The analytic support and remainder argument in the request (26–39) and binding document (27–111) is correct:

- `k(s) = [csch(s/2)-2/s+sech(s/2)]/4` gives the stated inverse-series recurrences.
- The degree-96 surrogate has odd powers at most 95 and even powers at most 96. Even-power integral outputs have degree at most the kernel exponent; odd-power outputs, split at y=x, have degree at most exponent+input degree+1. For this degree-28 h_A the whole output is even and degree at most 124. Thus `T K_k96 h_A=0` exactly.
- This does **not** set `T K_k h_A=0`. The remaining complete kernel norm is paid by `(3/2)Ek`.
- The recurrence cancels the reciprocal-product residual through degree 96. All remaining factorial-series terms are included in the geometric-tail majorant defining Ek; the apparent division by u in the csch piece is harmless because the residual starts at degree 98.
- The th formula bounds the whole cosh remainder after degree 30, and the complete pole output bound is `(9/2)th sqrt(H_A)`. Since `T Pi_X=T`, using this larger low16-projected bound for T is valid.
- Lines 316–345 verify the exact Ek/th scalar identities. The lightweight audit independently reproduced both exact fractions.
- Lines 347–348 and 514–516 include `epar+(3/2)Ek+(9/2)th` **once** in yrem. The actual-parameter F is not silently identified with old reference Y0.

Consequently the norm triangle `||TY_actual|| <= ||T(W_Bh_A)|| + ||TS|| + eop sqrt(H_A)` justifies precisely the reported certificate. The W/S cross cancellation is deliberately discarded, as requested at request line 42. Shift-internal cross terms are preserved.

## 6. Resource constraints and execution record

- Before the numerical main, lines 31–39 set and verify RLIMIT_AS = 768 MiB, install a 290-second wall alarm, and refuse to proceed if cap setup fails.
- `run_once.sh:9–10` adds an external 295-second timeout with SIGKILL after one further second. These limits are stricter than the requested 300 seconds and 1 GiB.
- Lines 279–280 create an exclusive attempt marker, blocking another attempt in that same output directory.
- Nonblocking operational caveat: rerunning with the same output directory would raise FileExistsError at line 279, then the generic exception/finally path (554–568) would overwrite `run/result.json` with HOLD. The marker prevents a second calculation but does not preserve the old result on that mistaken invocation. Do not invoke the bundled wrapper again; the original archive remains the evidence. No source file was changed in this audit.
- Numerical arithmetic remains on the fixed grid. Separate exact symbolic checks are bounded at 8192 bits (64–71). Reported maximum symbolic size is 1696 bits.
- Product-degree tracking/enforcement is at 220–245; maximum reported product degree is 156, below 160. No quadrature, inverse, matrix computation, optimization, or cutoff expansion appears in the source.
- Stdout and result agree on completion at 1.8922807050000756 seconds and peak RSS 13568 KiB. The code and input hashes bind that record to the inspected artifacts. Stderr is empty.

These are artifact-supported execution claims. A static review cannot independently witness the prior process or prove the absence of attempts in another directory. The marker enforces one attempt in the recorded directory, not globally. No contradiction was found, and this review performed no further source computation. Model identity is outside this static audit.

## 7. Lightweight independent evidence

Files beside this review:

- `../checks/lightweight_checks.py`: exact/read-only audit checks; does not run source-tail main or source integrals/moments.
- `../checks/lightweight_checks_original_stdout.txt`: actual output.

Observed output:

    PASS: 337 lightweight checks; 315 stored interval records validated.
    No source-tail main, integrals, source moments, response, or quadrature executed.
    Exact scalar identities: H_A via alternate beta moments; Ek recurrence; th remainder.
    65+65 mode squares and prefix sums, 21 shift-pair norm sum, tails, sqrt bounds,
    eop, remainder, certificate, crude, ratio all consistent.
    W tail enclosure width = 2.08430776e-65; relative to upper = 7.81031462e-41
    S tail enclosure width = 1.49361628e-53; relative to upper = 2.35086029e-31
    Nonempty shift pairs: 13 of 21
    Primitive checks: 186 isolated test operations; not a source computation.

The very narrow numerical enclosure widths show this completed bound is not limited by outward arithmetic precision at the reported scale. They do not quantify the deliberately discarded W/S cancellation, the conservatism of the crude comparison, or any downstream response loss.

## Final scope boundary

Accept this as a completed **source-tail input certificate** for the frozen h_A and M128, with the stated inherited assumptions. Do not elevate it to an actual tail value, a lower bound, a C(Y) bound, proof that q=0 fails in every method, a Schur-sign verdict, or RH. Those conclusions require separate authorized arguments/calculations not present here.
