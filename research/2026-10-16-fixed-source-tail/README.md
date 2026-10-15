# Fixed-source tail certificate at B = 3/4 and M = 128

This directory preserves a completed finite interval certificate for one frozen even polynomial input h_A. Conditional on the stated identification of Y_actual with the original source operator,

    ||Pi_even,>128 Y_actual||_2 <= 8.4874678247291907546e-12.

This is a norm upper bound, not the actual tail norm, a lower bound, a response quadratic, a Schur-sign certificate, operator positivity, or a proof of RH. The source identification remains an inherited premise. The scalar boxes and remainder constants received independent exact-rational checks. No new witness, cutoff expansion, quadrature, inverse, matrix calculation, or full source-tail rerun was performed for this publication.

## Files and provenance

- source_tail_M128_certificate.zip is the unmodified original archive, SHA-256 53ec1d14ba2a7384d14d2f41e34d520a537ba474ee02dffada285678771916a3.
- source_tail_M128/ contains every original archive member byte-for-byte: input, certificate code, execution wrapper, stdout/stderr, full result, proof report, request, attempt marker, and the original nine-entry manifest.
- SOURCE_BINDING.md explains the actual-parameter reduction and complete kernel/pole remainder. It is the historical pre-computation note, not a claim that the computation is still pending.
- sources/ contains only the required historical mathematical excerpts and selected exact scalar/vector fields. PROVENANCE.json identifies their full-source hashes and selection boundaries.
- reviews/ preserves a static review, the original mathematical result summary, and a curated scientific excerpt of Claude's completed review.
- checks/lightweight_checks.py verifies the saved record and isolated interval primitives without evaluating any source moments or running the certificate main. Its portable-path adaptation produced exactly the same stdout as the original 337-check audit.
- checks/claude_source_tail_sanity_run.py is the recovered, hash-matched independent short script. Its saved JSON contains 14 true checks; see the review's evidence-status note.
- MANIFEST.sha256 covers the publication files other than itself. The original manifest is unchanged inside source_tail_M128/.

Private browser/session/account information and unrelated material are not included. Review excerpts are labeled as curated. The original numerical artifacts have not been edited to fix or conceal any defect.

## Exact setup and normalization

Let B=3/4, Omega=(-B,B), E0[u]=(1/2) integral_{-1}^1 u(t) dt, and

    h_A(Bt) = p(t)/sqrt(2B),
    p(t) = sum_(r=0)^15 z_r (1-t^2)^r,
    e_m(x) = sqrt((2m+1)/(2B)) P_m(x/B).

The exact z_r are the grid-10^-40 numerators in source_tail_M128/input.json. They are coordinates in (1-t^2)^r, not orthonormal Legendre coordinates. z_15=0 and z_14 is nonzero, so p has degree 28. The exact H_A=||h_A||_2^2 is also in input.json and independently verified.

For f(Bt)=u(t)/sqrt(2B), ||f||_2^2=E0[|u|^2] and <e_m,f>=sqrt(2m+1) E0[P_m u]. Exactly 65 even modes m=0,2,...,128 are subtracted, including the low16 modes 0,...,30.

Set W_B(x)=-log(1-(x/B)^2)/2. Each S_n contains both zero-extended translations by +/-log(n); c_2=log(2)/sqrt(2), c_3=log(3)/sqrt(3), c_4=log(2)/2, with log(4)=2log(2) kept dependent. The six weighted branches retain all 21 unordered pair terms with multiplicities totaling 36, including the n=2 overlap.

The inherited source formula is

    Y_actual = Pi_X [W_B h_A - K_k h_A
                     + 2 M(h_A) cosh(x/2) - sum_(n=2)^4 c_n S_n h_A],
    M(h)=integral_Omega h(x)cosh(x/2) dx,
    k(s)=[csch(s/2)-2/s+sech(s/2)]/4,
    K_k h(x)=integral_Omega k(|x-y|)h(y) dy.

Pi_X removes low16, and T=Pi_even,>128 satisfies T Pi_X=T. The degree-96 kernel surrogate maps the fixed input to an even polynomial of degree at most 124, so its T-projection is exactly zero. The actual kernel tail is not set to zero: the complete remainder is bounded by (3/2)E_k ||h_A||. The complete pole tail is bounded by (9/2)t_h ||h_A|| and is paid once. The certificate conservatively retains e_op=e_par+(3/2)E_k+(9/2)t_h, with e_par=4(23 sqrt(d)+20700d)+26d and d=10^-96.

For W and the full combined shift component S separately, Parseval gives the complete infinite tail from the whole squared norm minus all 65 projection squares. Polynomial antiderivatives on every branch intersection and analytic logarithmic beta moments avoid quadrature or an artificial tail truncation. Shift-internal cross terms are retained; W/S cross cancellation is deliberately discarded by a norm triangle.

## Numerical record and rounding

    y_W <= 5.1659078865082153152e-13
    y_S <= 7.9708770360783692231e-12
    y_rem <= 2.1032758515993360719e-35
    y_cert <= 8.4874678247291907546e-12

The code uses integer endpoints on a fixed 10^-120 grid with outward rounding after every operation. It forms tail-square upper bounds as whole-norm upper minus prefix-square lower, then outward square roots. Negative tail upper endpoints are rejected, never clipped. All full endpoints are in source_tail_M128/run/result.json; shortened displays must not be subtracted to reconstruct them.

The ratio of the certificate constant to the inherited crude bound Y_crude=(28+e_op)sqrt(H_A) is below 3.73e-10. This compares two upper-bound constants; it is not a ratio of actual norms, an improvement over a matched previous tail algorithm, or a downstream response improvement. A finite tail estimate alone does not establish that the tail is no longer a response bottleneck.

The original record reports one completed run, exit 0, 1.8922807050000756 seconds, 13,568 KiB peak RSS, 976,356 interval operations, maximum product degree 156, and maximum exact-symbolic size 1696 bits. Those are preserved execution-record claims, not measurements repeated for publication.

## Verify without rerunning the source computation

From this directory on a system with Python 3 and sha256sum:

```sh
sha256sum -c MANIFEST.sha256
(cd source_tail_M128 && sha256sum -c MANIFEST.sha256)
python3 checks/lightweight_checks.py
```

Expected check summary: 337 lightweight checks, 315 interval records, all 130 mode squares and both prefixes, 21 shift pairs, final bounds, and 186 isolated arithmetic operations. This does not recompute any source integral or moment. The portable check was run during publication and matched checks/lightweight_checks_original_stdout.txt exactly.

The recovered independent reviewer script can be inspected or optionally run separately:

```sh
/usr/bin/timeout --signal=TERM --kill-after=1s 120s \
  python3 checks/claude_source_tail_sanity_run.py
```

It uses Python's resource module to enforce 512 MiB, and checks scalar boxes, H_A, E_k, t_h, reciprocal recurrences, low-degree Legendre coefficient identities, and selected support ordering. Its approximate display fields are not certified full-result endpoints. This script was not rerun during publication.

## Optional independent full reproduction: fresh output only

WARNING: Do not run source_tail_M128/run_once.sh in the preserved bundle, and do not point certify_tail.py at source_tail_M128/run. The original marker blocks another calculation in that directory, but the generic error/finally handler can overwrite the existing result.json with HOLD. This operational flaw does not alter the already preserved COMPLETE result. It is documented, not silently patched.

An independent reproducer may use a fresh temporary directory on Linux with Python 3 (original record: 3.12.14), the standard library, and GNU timeout:

```sh
work=$(mktemp -d)
/usr/bin/timeout --signal=TERM --kill-after=1s 295s \
  python3 -u source_tail_M128/certify_tail.py \
  source_tail_M128/input.json "$work/run" \
  > "$work/stdout.txt" 2> "$work/stderr.txt"
printf 'New reproduction only: %s\n' "$work"
```

The code internally requires RLIMIT_AS=768 MiB and a 290-second alarm; timeout adds 295 seconds and a one-second kill grace. The exact-symbolic ceiling is 8192 bits. If unsupported or exceeded, report HOLD; do not expand resources or alter the fixed input and claim the same run. Execution metrics/timestamps can differ, so a new result file need not have the archived file's hash. This command is provided for reproduction and was not executed for publication.

## Review limits

Static review found no blocking mathematical or implementation defect within scope. Claude accepted the analytic binding conditionally and interval implementation/scope after a short independent scalar check, without rerunning the 65-mode certificate. Neither audit establishes the source formula from the entire original operator framework. The old independent Y0 reference tuple/raw signed rows were not recovered and were not replaced by invented values. The saved record certifies a finite upper-bound input to later work, not any later response or positivity conclusion.
