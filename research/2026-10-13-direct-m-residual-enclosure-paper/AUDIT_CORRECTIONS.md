# Canonical reserve and target correction

The canonical dbar is the even piecewise rational upper bound on the
weighted actual row sum sum_j c_ij w_j/w_i. Its positive-band values are
9/10, 5/6, 9/10, 1/2, 1, 19/20, 2683/1800 in the physical order specified
in `source_definitions.json` and Table 1 of the paper.

It is not the unweighted row sum P_B 1_Omega. On the central band that row
sum is 2c2=sqrt(2)log(2), so replacing dbar by it makes
p_eta=omega(W_B+9/10-dbar) negative near zero. This prevents reusing the
canonical p_eta nonnegativity or target-specific m/M values under that
changed definition. The physical A_b remains the same after consistent
cancellation. A bounded even change preserves the auxiliary weighted-domain
relation; it does not preserve p_eta or the signed functional.

An earlier audit's shorthand `p=P_B1 replacement` is corrected to
`dbar=P_B1 substituted into p's definition`. The manuscript uses the latter
meaning, without publishing unrelated historical audit records.

The vector p=P0F in a different fixed-trial objective is not the scalar
multiplier p_eta. The original full-pole moment M(f) is not M_b here.
Prime coefficients have no additional omega or duplicate factor of two.

The general affine theorem, zero-start limitation and analytic source
lower bound are proved in the manuscript, without treating previous PASS
flags as proof. Missing m/Gx0/full residual norm certificates remain missing
within the inspected input scope. Incomplete beta verification and the
numerical result degraded by endpoint transcription are not evidence here.

No original whole-line operator or its minimum domain is identified with
the finite-interval auxiliary A_b. No numerical sign or RH conclusion follows.
