# Definitions, premises, and the closed local proof route

## Fixed setup

B=3/4, Omega=(-B,B), H=L2(Omega;C), with conjugate-linear first inner product. Functions in shift integrals are extended by zero. theta=2^-16 and omega=1-theta. Set t=log(2), u=log(3), r=B-t, v_g=u-t, w_g=2t-u.

rho(s)=exp(-s/2)/(1-exp(-2s)); R(s)=integral_s^infinity rho; V(x)=R(B+x)+R(B-x); V0=2R(B); W_B(x)=-log(1-x^2/B^2)/2; Delta=V-V0-W_B. All tails are complete, with no cutoff.

The bounded adjacency has coefficients c2=t/sqrt(2), c3=u/sqrt(3), c4=t/2. Each undirected edge contributes 2 Re(c conjugate(z_i) z_j), so the form matrix has off-diagonal -c, not -2c.

## Actual fibers and two distinct weight systems

- Seven: parameter x in (-r,r); coordinates x+(0,t,-t,v_g,-v_g,w_g,-w_g).
- Path: parameter s in (u+B-2t,2t-B); coordinates (s-t,s,s-u,s-u+t).
- Pair: parameter y in (B+t-u,u-B); coordinates (y-t,y).

J_geometry_tail_and_edge_squares.txt supplies the disjoint physical bands and every edge. Translation Jacobians are one, boundaries are null, and there is no omitted positive-measure band.

For the joint edge-square comparison, seven vertex-type weights are (10/9,1,9/10,1/2), with row upper bounds dbar=(9/10,2683/1800,1,9/10) for center/t/v/w. Path leaf/interior bounds are 5/6 and 19/20; pair bound is 1/2. Set p_g=omega(W_B+9/10-dbar). This is nonnegative almost everywhere by the position reserves.

For the separate 6/5 adjacency norm bound, seven vertex-type weights are (5/6,1,2/3,5/18). Paths and pairs use constant weights. These two systems must not be interchanged.

## What must be proved, rather than inherited

1. Exhaustive geometry and actual edge coefficients, including n=4 exactly once.
2. Complex edge-square identity and nonnegative row slack: diag(dbar)-A_C >= 0.
3. Fiberwise Schur estimate ||A_C|| <= 6/5.
4. Kernel monotonicity on (0,3/2], giving Delta >= 0 through the complete tail.
5. Rational logarithm and location bounds, giving p_g >= 0.
6. Scalar bounds c_Gamma < 759/140 and delta_0 > 209447/93913400 > 0, hence j_7 > 53/140 > 0.
7. Exact cancellation, with no duplicate c_Gamma charge:

    M_C - diag(a+p_g)
      = omega[diag(dbar)-A_C+diag(Delta+delta_0)]
        + theta[(7-c_Gamma)I-A_C].

Thus M_C >= diag(a+p_g+omega Delta)+c_coer I. The matrix M_C represents aI+C, not C alone.

8. Closed multiplication form on D_g, bounded self-adjoint perturbation by the adjacency, and the operator domain {Vf in L2}. Closedness is in the form norm; D_g is not a closed subset of unweighted L2.
9. Reflection follows from coordinate permutations and even V. The minimal completion of compact smooth functions under the complete Gamma energy plus the L2 norm is included in D_g via the nonnegative exterior term and Tonelli. Equality with a maximal energy domain is not claimed.

Only elementary series, exact rational comparisons, finite graph identities, measure theory and standard closed-form/operator facts enter this local route. The historical special value a>4/5 is unnecessary: a can be any positive real. The missing historical first-overlap original is not replaced by relabeling the later scalar reconstruction as an original.
