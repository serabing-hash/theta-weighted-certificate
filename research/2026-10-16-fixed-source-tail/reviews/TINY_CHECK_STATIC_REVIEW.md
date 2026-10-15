# Static review of Claude's source-tail audit

2026-10-15 UTC. No sanity script, source-tail code, numerical moments, or response calculation was run in this review. Only file reads, hashing, AST/literal inspection, and this report were performed.

## Verdict

Claude's conditional source-binding PASS, interval-implementation PASS, and narrowly scoped source-tail result are supportable. Its recovered constant-enclosure checks are rigorous. Do not adopt the forward-looking claims that the pole can be ignored or that a Q_up comparison establishes an actual negative Schur sign. No defect found here invalidates the existing source-tail certificate.

Recovered script SHA256 is exactly `4a91b6276d309b130f55cf85343e830df9a1fb7f5fcff11de82f3f0bf2b50392`, matching the reported actual-run hash. Static literal comparison found **9** fields, all exactly matching the frozen input. Claude's “10 keys” at response line 24 is a minor counting error.

## Constant boxes: sound methods

Code line references refer to `../checks/claude_source_tail_sanity_run.py`.

- **ln2/ln3 (72–86):** For 0<x<1, `2 artanh(x)=log((1+x)/(1-x))`. The omitted positive terms after j=N−1 are bounded above by `2*x^(2N+1)/((2N+1)*(1-x^2))`. Therefore x=1/3 gives ln2 and x=1/2 gives ln3, with rigorous rational lower/upper endpoints. `inside` checks the computed enclosing interval is contained in the inherited box, the correct direction.
- **pi (76–89):** Consecutive alternating partial sums enclose arctan(x) for the positive x<1 used here. Machin's identity `pi=16 atan(1/5)-4 atan(1/239)` is exact; the minus term uses the reversed endpoints. This produces a rigorous pi enclosure.
- **1/sqrt2 and 1/sqrt3 (90–92):** The squared inequalities prove enclosure because both literal endpoints are positive. The upper endpoint's positivity is supplied by the inspected input, although it is not a separate assertion.
- Fraction arithmetic is exact. Float and Decimal conversions at 93 and 122–142 are display-only and do not participate in these tests.

Given the recovered run's reported true checks, these five constant boxes are independently checked rather than merely assumed. The physical source/operator identification remains inherited.

## What the 14 checks actually establish

Exactly 14 `check` calls occur at lines 51,52,63,65,67,84,86,89,91,92,96,113,120,121:

1. Exact H_A from the original polynomial coefficients.
2. Degree 28, using nonzero ps[14] and zero z[15].
3–4. Exact Ek and th match their defining formulas.
5. Both reciprocal recurrences cancel all positive even coefficients through degree 96.
6–10. The five constant boxes above enclose their true constants.
11. `(2k)! >= 2^k` for k=0,...,79 and `128/119 < 3/2`.
12. Even Legendre coefficients through m=40 match Bonnet recurrence.
13–14. The stated ordering and interior location of the shift endpoints, including the n=2 overlap condition.

Two distinctions matter:

- Check 11 is finite; it alone does not prove the infinite cosh bound. The simple general inequality `(2k)! = product_{j=1}^k (2j-1)(2j) >= 2^k` supplies that proof for every k. Summing the geometric majorant gives `cosh(3/8) < 128/119 < 3/2`. The unconditional `res["cosh38_bound"]=True` at 97 is a label, not an additional test.
- Check 12 is only through m=40, not all 65 certificate modes. The closed-form coefficient identity is valid generally, so this is a legitimate sanity check but not a rerun of all modes.

None of the 14 checks recomputes the 65+65 W/shift moments, branch-pair integrals, ycert, or the full-precision ratio. The script records failed checks rather than raising them; **exit code 0 alone does not imply all checks passed**. The actual `checks`, `failed`, and `all_checks_passed` output must be used. This review did not re-execute or freshly evaluate those inequalities.

## Caps and provenance

Line 4 installs RLIMIT_AS of 512 MiB; if installation fails, the script terminates. The recovered script has no internal wall timer or symbolic-bit cap. Its claimed 120-second bound therefore depends on the separately reported external `timeout 120s` command. That wrapper and the reported 0.089-second runtime cannot be independently established from this Python file alone. The script consists of small fixed finite loops and contains no full certificate execution. The initially missing `/usr/bin/time` wrapper, if it prevented process start as reported, is not a second numerical run.

## Qualifications to Claude's final response

Response references use line numbers in the full archived reviewer response. Only its curated scientific excerpt is published here as CLAUDE_scoped_audit.md; the private full response is not included.

1. **Pole “negligible” (119): reject as permission to drop it.** The norm bound on v is valid, but it is nonzero. Any downstream inverse or response certificate must retain the rank-one pole or explicitly pay a proved complete error bound, including denominators and relevant cross terms. The displayed v bound alone does not establish that an undefined epsilon_lambda is harmless relative to a future sign margin.
2. **“||F|| about 5e−4, roughly 45×” (78): only an approximate scale inference.** The calculation did not evaluate the joint F norm. The separate total norms imply `|sqrt(N_S)-sqrt(N_W)| <= ||W_Bh_A-S|| <= sqrt(N_S)+sqrt(N_W)`, so the asserted rough scale is plausible and can be justified this way. It is not a directly computed F norm, an exact 45× certificate, or the norm of the low16-projected full actual source containing the kernel and pole. The genuine certified comparison remains ycert versus Ycrude.
3. **Q_up “KILL” (122): restrict to one certification formula.** For a valid quadratic upper U_C on C(Y), `U_C >= Q_up` means that this particular upper-bound test cannot certify `C(Y)<Q_actual`. It does **not** prove `C(Y)>=Q_actual`, a negative Schur sign, or failure of every q=0 method. Conversely, `U_C<Q_up` is not a positivity certificate; a compatible actual-Q lower bound is needed. Norm and quadratic quantities must not be compared directly.
4. **“Tail no longer the precision bottleneck” (114): restrict to this source-tail arithmetic.** Its tiny enclosure widths support that conclusion locally. They do not show the tail magnitude is small enough after the downstream response/inverse map or that no tail-related bottleneck remains.
5. **Proposed head reuse (116–121):** Reuse the signed W and S moment intervals, not merely squared coefficient records. Kernel coefficients and complete pole/kernel allowances remain required. This is a proposed next calculation, not a completed actual-C(Y) upper or a scalar that already replaces the old baseline.
6. **Displayed ratio (79–83):** Claude correctly warns against recomputing the last digit from rounded displays. The earlier independent review of full `result.json` already verified `<=3.7254505902475865958e-10` from exact saved endpoints. No change to that certified bound is required; `<=3.73e-10` is a convenient coarse quotation.
7. **Duplicate-run result overwrite (90–97):** Correct nonmathematical warning, independently found earlier. Preserve the original artifact; do not rerun or modify it as part of this audit.

## Safe final claim

The fixed-h_A, B=3/4, low16, M128 source-tail norm upper bound `8.4874678247291907546e-12` survives this review. Its comparison with the inherited crude norm bound survives. The actual source binding remains conditional, and response, Schur sign, original-operator positivity, and RH remain unevaluated. The independent constant checks improve confidence in the input boxes without expanding that mathematical conclusion.
