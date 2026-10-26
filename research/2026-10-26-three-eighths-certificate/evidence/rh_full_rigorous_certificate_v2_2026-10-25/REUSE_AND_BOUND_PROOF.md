# H-v2: exact diagonal scaling and domain-only remainder replacement

The first complete rigorous attempt was inconclusive because its fourth-order quadrature remainder was excessively conservative. This version does NOT rerun the candidate, Gamma form, midpoint quadrature assembly, or tail quadrature. It keeps the exact same60-panel midpoint j0+j2 quadrature functional and changes only its remainder bound.

## Exact reuse

The binary64 diagonal D has strictly positive powers-of-two entries. Ustored D, Ctrial D and D Fmid D are formed with ldexp, require all nonzero outputs to remain normal, and are checked by exact reverse scaling. Thus no scaling roundoff is silently omitted. Exact source is Uexact D; its original moment map is D rather than I. D is invertible, so inertia is preserved. Uexactification error is at most eta_U ||D||.

All old nonquadrature error components are explicitly enumerated and multiplied upward by ||D||^2. The old huge total error is never subtracted numerically to recover small components. G entry/congruence certificates, H point/input/exactification error, H BLAS/symmetrization, theta integral tail, analytic endpoint tails and F subtraction error are hash-bound and reused. Only the old fourth-order remainder is replaced. A minimum of two valid panel remainder upper bounds remains valid.

The finite-theta density identity is exact:

    w8 [S+t0 m8 P]^T[S+t0 m8 P]
      = w8 S^T S+2(S^T P+P^T S)+2t0 m8 P^T P.

Thus direct-residual derivative bounds refer to precisely the same density and midpoint derivatives previously enclosed. The physical panel partition, maps, dyadic u widths, precision and exact coefficients are unchanged. This is not an appeal to numerical agreement.

## Endpoint jets

h_contact.hpp encloses S(Lu^8)=log(exp(Lu^8)-1) by logL+8logu plus its regular power series, with an explicit differentiated tail through order4. The logarithmic derivatives are formed directly in u, avoiding interval composition through a nearly vanishing exponential difference. Only the inside/adjacent source contact terms are replaced by this exact identity. Smooth terms, prefactors, reflection and prime branches remain unchanged.

## Correlated full residual derivative enclosure

On each fine target cell, exact original moment functions satisfy v=phi_fine P_sub. Keeping the scalar term already inside r=(Gamma-cGamma-P)Phi_fine, form

    B0=t0*m8_0*(U D)_local-P_sub*(C D)_cell,
    Bj=t0*m8_j*(U D)_local  (j>=1),
    Rj=r_j U D+sum_(l+b=j) phi_l B_b.

The large metric and moment-trial terms cancel in the2x552 coefficient B0 BEFORE multiplication by the local function interval. No scalar term is counted twice. B errors are operator-norm bounds; their chosen-center Frobenius norms are conservative operator bounds.

Each domain fine Gamma/scalar/prime row interval is exported as chosen binary64 center plus outward component radii. Its transformed component-radius bound uses nonnegative radius @ abs(Ustored D), so local column downweight is retained. Classical dot-rounding is bounded by gamma_(2*1104+20) times Frobenius products. The exact-source correction adds eta_scaled*(||row_center||+||row_radius||). Local P_sub and B coefficient errors are enclosed before Leibniz assembly. Therefore the resulting RN_j encloses the Euclidean norm of the ENTIRE exact residual jet for every point in the panel, not a sum of separately squared large metric terms.

The fourth density coefficient norm is at most sum_(k+l+m=4) |(w8 Jacobian)_k| RN_l RN_m. Multiply by2h^5/80, upward, and sum all552 positive target cells. The factor2 is reflection. The two analytic tails use their original scaled certified budget unchanged.

## Arithmetic and resources

The same fixed binary64/MPFR266 arithmetic model applies. Actual single-thread classical OpenBLAS and FE_TONEAREST are checked. Signed nonzero subnormal inputs are rejected by bit pattern. Center magnitudes above1e50 are rejected. Positive-bound arithmetic promotes every operand to at least DBL_MIN, adds DBL_MIN and rounds upward. Gamma factors and norm bounds are inherited from the independently audited first implementation. The1e-280 absolute allowance bounds unamplified dot/row underflow at dimensions1104/552; any subsequent amplification is included by the explicit vector/matrix perturbation bounds. All arrays entering BLAS/einsum are guarded, including coefficient and radius centers.

Reused input hashes are checked before and after the bounded domain stage. The590s observed wall/CPU and500MiB observed live-RSS supervisor thresholds,512MiB per-process address-space cap,600s per-process CPU/alarm, single-thread policy and unconditional process-group cleanup are unchanged. These are honestly reported as polled aggregate/per-process safeguards, not a kernel aggregate cgroup guarantee. One new launch lock, no automatic retry.

A successful conditional finite-parameter inertia certificate would still not prove RH or the required parameter sequence. Failure or an excessive bound remains inconclusive.
