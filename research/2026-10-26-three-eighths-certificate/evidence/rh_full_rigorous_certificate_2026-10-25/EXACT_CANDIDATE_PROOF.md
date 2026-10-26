# Exact candidate helper contract and proof

Prepared 25 October 2026. Owned files: exact_candidate.cpp, prepare_candidate.py, this proof. Compilation/syntax checks only at preparation time; no candidate arithmetic or matrix multiplication has been run by this author. The main certificate runner must guard and authorize execution. Independent review is required because the full-matrix auditor authored this helper.

## Fixed inputs and outputs

Source: preserved corrected q24 matrices_q24.npz, keys penalty_Z (552x552), penalty_U (1104x552), projection_coefficients (276x2x1104). prepare_candidate.py verifies dimensions/finiteness, chooses Ctrial = floating projection_coefficients times stored penalty_U, and saves raw little-endian binary64 Z_dyadic.bin, Ufloat.bin and Ctrial.bin. Each result is bitwise read back and hashed. Existing output files cause failure rather than overwrite. Ctrial is an arbitrary exact dyadic trial coefficient array: rounding in its selection affects tightness, not validity. This is not a claim that Ctrial is the exact projection.

The C++ helper requires binary64 and a little-endian host, reads precisely the required number of bytes with no trailing data, rejects nonfinite values, and imports each double by directed mpfr_set_d at 266 bits. Binary64 values are exactly representable at that precision; the imported intervals are point intervals.

Output exact_candidate.json contains exact-candidate norm/error bounds and each original cell's C trial Frobenius bound. The fields U_norm_upper, U_error_norm_upper and C_cell_norm_upper are upward-rounded binary64 bounds printed at 17 significant decimal digits for exact binary64 round-trip. Companion interval fields retain outward 90-digit decimals. Consumers must not round a bound downward or replace an upper bound with a center.

## Exact analytic source definition

The actual source is U_exact=P_exact-X_exact Z_dyadic, not the saved floating U. The local P/X blocks use the previously proved hyperbolic addition identities. Fine and coarse normalizers enclose their positive series with the same explicit geometric tail as the previous certified construction. For delta=1/n,

    s=2sinh(delta/2)-delta,
    N0=sqrt(2delta+s), N1=sqrt(s).

The sum includes terms k=1..8, then adds the interval from zero to next_term/(1-delta^2/4), a valid geometric majorant for all remaining positive terms. All constants and arithmetic use the existing directed MPFR wrapper.

With d=1/2208=coarse_delta/8 and A=nf0 cosh(d)/nc0, B=nf1 sinh(d)/nc0, C=nf0 sinh(d)/nc1, D=nf1 cosh(d)/nc1, columns are

    p0=(A,-B,A,B), p1=(-C,D,C,D),
    x0=(B,A,B,-A), x1=(D,C,-D,C).

They are exactly orthonormal by the analytic restriction/addition identities. The code additionally checks each enclosed local inner product contains the corresponding identity entry; this is a consistency check, not the proof of the identities. Thus original moments satisfy P_exact*U_exact=I exactly and

    U_exact*U_exact=I+Z_dyadic*Z_dyadic.

## Certified source-map and surrogate-error bounds

The helper bounds ||Z||_2^2 by the minimum of its directed Frobenius square and ||Z||_1||Z||_infinity. Consequently sqrt(1+that bound) bounds ||U_exact||_2. It also records sqrt(552+||Z||_F^2) as a Frobenius upper bound.

For each fine row i in original cell c and each source column j, it directly encloses

    U_exact[i,j] = P_exact[i,j]
                  - X_local[i,0] Z[2c,j]
                  - X_local[i,1] Z[2c+1,j].

Only two products per entry are needed. Subtracting the exact dyadic stored U value yields a componentwise absolute error bound. The helper takes the minimum of the resulting Frobenius bound and sqrt(maximum row sum times maximum column sum), both valid bounds on ||U_exact-U_stored||_2. It does not assume that the floating source was formed exactly or reuse a floating moment-defect as an operator bound.

For each original cell the exact dyadic 2x552 Ctrial block receives a directed Frobenius upper bound, hence also an operator-norm bound. A global stacked Frobenius bound and maximum local bound are recorded.

These are candidate exactification and norm certificates only. No quadrature, residual Gram, physical form, finite inertia or RH claim follows without the rest of the validated calculation.
