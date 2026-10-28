# Separate failed fixed candidate

This subfolder is a transparency record, NOT a positive certificate.
The exact frozen source was executed once with B=3/4, M=32, N=16384,
J=32, 256-bit arithmetic and python-flint 0.9.0. It exited with code 1
at the fourth (zero-based index 3) LDL pivot. See FAILURE_STATUS.json
and failure.stderr.txt. No successful witness JSON or certified
nonvanishing of the selected zeta vector was exported.

The assertion failure concerns a sufficient comparison matrix. It does
not exhibit a negative vector for the original form and is not a RH
counterexample. A failed sufficient bound does not invalidate the
analytic inequalities in the accompanying paper.

The source is byte-identical to the executed version. Its original
"prepared, unexecuted" header is historical and retained to preserve
its SHA256. FAILURE_STATUS.json supersedes that preparation status.
The error record changes only absolute directory prefixes to the source
basename. It contains no internal execution receipts or approval data.

## Manual reproduction

Use an isolated Python environment with python-flint exactly 0.9.0.
Do not use Python optimization (-O), because assertions are proof gates.
The recorded computation was bounded by CPU 180 seconds, wall time
240 seconds, address space 1 GiB and output size 8 MiB. Those limits are
not a runtime guarantee on another machine.

When you deliberately choose to reproduce this failed computation:

    python3 -I -B verify_three_quarters_defect.py --execute-approved-once --output candidate.json

The explicit flag guards accidental execution; it is not itself
permission to use any particular system. Use your own resource limits.
The source refuses to overwrite an existing output. Failure before
export should leave no successful candidate.json. Neither the paper
build script nor the scalar arithmetic checks execute this source.
