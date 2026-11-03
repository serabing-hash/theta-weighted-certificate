# Explicit convergent positive-reference Gram algorithm

3 November 2026 UTC. Analytical algorithm and proof, not a matrix computation. No long computation was run. Inherited inputs are the actual theta weight and its envelope, the Gamma label expansion, the prime-tail bound, and the ambient form-core theorem in INDEPENDENT_CONSTRUCTION.md. The construction below supplies finite scalar integration primitives for the positive-reference inverse; it asserts neither practical complexity nor a new sign.

## 1. A bounded compact-frequency approximation

Fix N and delta with epsilon=delta-r_N>0, and write a=(d-c_N)_+. Work first on the ambient H, with A represented by

    p[u]=epsilon ||u||_H^2 + integral a(t)|F u(t)|^2 dt.

For integers n>=1 put

    m_n(t)=min(a(t),n) 1_{[-n,n]}(t),
    S_n=J* F^{-1} m_n F J,
    A_n=epsilon I+S_n.

Then 0<=S_n<=n M I, M=sup W<=1/2, and the forms increase pointwise to p. Consequently A_n^{-1} decreases strongly to A^{-1}. This is monotone convergence of closed positive forms, not an operator-norm approximation to A. A short variational proof is the same weak-compactness argument given for Gamma-label heads in the earlier construction.

Take alpha_n=epsilon+n/2, q_n=1-epsilon/alpha_n, Y_n=I-A_n/alpha_n, and

    P_{n,k}=alpha_n^{-1} sum_{j=0}^k Y_n^j.

The completely explicit bounds are

    0<=Y_n<=q_n I,
    P_{n,k}<=A_n^{-1}<=P_{n,k}+q_n^{k+1}/epsilon I,
    <f,A^{-1}f><=<f,P_{n,k}f>+q_n^{k+1}||f||_H^2/epsilon.  (1)

Only the last upper bound is valid for the full inverse. P_{n,k} is NOT generally a lower bound for A^{-1}. Choose k to make its displayed remainder smaller than any prescribed tolerance. No unknown high-frequency inverse is used.

## 2. Finite integrals, with explicit error control

Let W_hat denote the unitary Fourier transform. For j>=1,

    <f,S_n^j f>_H
      = integral_{[-n,n]^j} conjugate(f_hat(t_1)) f_hat(t_j)
          product_{l=1}^j m_n(t_l)
          product_{l=1}^{j-1} [W_hat(t_l-t_{l+1})/sqrt(2 pi)] dt.

For j=1 the second product is 1. Expanding the finite Neumann polynomial uses these finitely many compact integrals and ||f||_H^2. This expansion can be very expensive and cancellation-prone, but arbitrary precision interval arithmetic makes it a convergent algorithm. It is an existence construction, not a recommended production implementation.

The Gamma series permits direct compact-interval enclosure. Set a_L=2L+1/2 and d_L=sum_{l<L} 2t^2/[a_l(a_l^2+t^2)]. For |t|<=T,

    0<=d(t)-d_L(t)
       <=2 T^2 [a_L^{-3}+1/(4a_L^2)].                 (2)

The omitted decreasing step-two sum is bounded by its first term plus half its integral. In particular d(t)<=17t^2 and |d'(t)|<=34T on [-T,T]; these follow from sum_l 2/a_l^3<17. Taking positive parts and caps is 1-Lipschitz, so (2) also bounds their scalar evaluation errors. Their Lipschitz constants on [-T,T] are at most 34T+L_N, where L_N=2 sum a_n log n. There is no need to locate or certify every zero of d-c_N. Integrate on the fixed cube; the sharp frequency-window endpoints lie on its boundary.

The inherited theta envelope implies, for x>=0,

    W(x)<=42 exp(-3) exp(-2x),
    kappa(x)=2 cosh(x/2) W(x)<=84 exp(-3) exp(-3x/2).

Thus

    integral_{|x|>X} W <=42 exp(-3) exp(-2X),
    integral_{|x|>X} |kappa| <=112 exp(-3) exp(-3X/2),
    integral_{|x|>X} kappa^2/W <=336 exp(-3) exp(-X).   (3)

The stronger double-exponential envelope may of course replace these deliberately crude bounds. Multiplication by |x|^j gives explicit polynomial-times-exponential tail integrals, by repeated integration by parts.

For the repaired inputs g_i=W psi_i, psi_i=F^{-1}(b 1_E/sqrt(beta_i)), one has

    |psi_i(x)|<=sqrt(beta_i/(2 pi)),
    ||g_i||_H^2<=beta_i B_0/(2 pi).

Consequently their spatial L1 tails and H-norm tails are bounded by the corresponding W tails times sqrt(beta_i/(2 pi)) and beta_i/(2 pi), respectively. A finite linear combination of the g_i and kappa has certified tails by the triangle inequality. Its Fourier transform is uniformly computable on any compact interval using (3). Likewise W_hat is uniformly computable, and its modulus of continuity obeys

    |W_hat(t)-W_hat(s)| <= |t-s| integral |x|W(x) dx/sqrt(2 pi).

The analogous bound holds for f_hat using integral |x f(x)| dx. All moments needed here are bounded by (3) and its polynomial versions. Certified Riemann integration on the compact cubes therefore converges with an explicit modulus and interval evaluation errors. On a bounded spatial interval the explicit positive theta series and its geometric/Gaussian tails give uniform scalar evaluation of W and kappa; this elementary implementation is required, not claimed already written. Strict positivity of W on each compact interval permits certified division by W after refinement.

## 3. Independent full-form lower bounds

Enumerate rational finite linear combinations of even compactly supported C1 cubic splines with rational knots, vanishing together with their first derivative at support endpoints. Such splines approximate C_c^infinity_even in H1 on a fixed compact interval. Since d<=17t^2 and W is bounded away from zero there, they form a core for p using the inherited ambient C_c^infinity form-core theorem and d<=a+C_N, a<=d+C_N.

For every such trial u, set

    L_f(u)=2 Re<f,u>_H-p[u].

Then L_f(u)<=<f,A^{-1}f>, and the supremum over the enumerated rational trials is equality. The full form, not a symbol-truncated form, must be used. It is computably enclosed: if D=||u''||_1 (piecewise classical second derivative; u and u' continuous), integration by parts gives |u_hat(t)|<=D/(sqrt(2 pi)t^2). Hence

    integral_{|t|>T} a(t)|u_hat(t)|^2 dt
       <= D^2/pi [17/T+C_N/(3T^3)].                 (4)

Finite-frequency integrals use (2), and physical compact integrals use interval evaluation of W. Both <g_i,u>_H=integral psi_i conjugate(u) and <kappa,u>_H=integral 2 cosh(x/2) conjugate(u) avoid division by W. The p[u] norm term still uses positive W on the compact support.

Dovetail n, polynomial degree, rational trials, and all integral precisions. Retain the largest certified primal lower bound and smallest certified upper bound (1). Stop when their difference is less than a requested h>0. The loop terminates for each fixed f,h: monotone form convergence gives the correct upper limit, the core gives the correct lower limit, and every finite integral can be refined. There is no established uniform iteration or wall-time bound.

For a stored primal trial u with lower endpoint l and upper endpoint U,

    ||u-A^{-1}f||_H <= sqrt((U-l)/epsilon).

This also yields certified vector approximants and can avoid evaluating every Gram entry through an independent scalar solve. No claim that same-trial H-residuals tend to zero is needed; form density alone would not justify that claim.

## 4. Exact centering and finite Gram errors

Compute ambient bilinear entries for the finite input list (g_1,...,g_r,kappa), either by real polarization of quadratic enclosures or certified vector approximants. All these functions are real even. With R=A^{-1}, set

    G_ij=<g_i,Rg_j>, v_i=<g_i,Rkappa>, s=<kappa,Rkappa>,
    M_ij=G_ij-v_i v_j/s.                              (5)

This is exactly the centered inverse Gram, with no extra approximation to the mean constraint. The source normalization gives ||kappa||_H=1 and

    s>=1/p[kappa]>0.

Alternatively, the convergent scalar lower bound for s eventually becomes positive, so evaluating p[kappa] separately is unnecessary. Interval division is performed only after certifying a positive lower bound. Arbitrarily narrow ambient enclosures then give arbitrarily narrow centered enclosures.

If a symmetric midpoint matrix Mtilde has per-entry radii E_ij, a rigorous operator error is at most max_i sum_j E_ij; the simpler uniform bound r e suffices when every radius is <=e. Certify lambda_max(Mtilde) by any verified symmetric-matrix procedure, or certify positivity of (1-eta-error)I-Mtilde by interval Cholesky/LDL with positive pivot margins. The stopping test is

    certified lambda_max(Mtilde) + max_i sum_j E_ij + eta < 1.  (6)

Cell masses must have positive certified lower endpoints before division. Cells whose positivity remains unresolved can be omitted only with a certified total omitted mass, charged by B_0 B_omit/(2 pi epsilon). The b scalar integration itself is uniformly computable by (2), positive-part Lipschitz continuity, and compact support, including its possible zero branches.

## 5. The delta=1/2 pilot: guaranteed termination, not demonstrated speed

For N=4 the inherited gap and tail yield

    g=1/48-2r_4>0,
    m_0=g/(9/2+g)=18217217993/7439920705481.

This is the prior manuscript's sign, not a consequence newly obtained from numerical entries. Since lambda_max(K_ref)<=1-m_0 and 0<=K_fin<=K_ref, choose certified eta<=m_0/4, a centered Gram spectral enclosure width <=m_0/4, and a largest-eigenvalue arithmetic error <=m_0/4. Then (6) eventually succeeds with positive spare budget. The allocation can be loosened; it is stated to make all three error sources explicit.

A crude fully proved support cutoff is T_0=2^15: d(T_0)>=log(1+4T_0^2)/2>16 log 2>32/3>9>=C_4. Together with B_2<=1/2, B_b<=18 T_0 and epsilon>63/128, this supplies a finite completely explicit cell count through the existing eta formula. It is extremely pessimistic. The exploratory T_0 near 123, B_2 near 0.0113 and B_b near 27.5 are not substitutes for certified scalar integrations and support verification. With those scales the present eta=m_0/4 allocation would suggest roughly 1,570 uniform cells; this is only a scaling estimate, not a certified count or resource promise.

The scalar and matrix algorithms now have rigorous stopping criteria and eventual termination for this inherited pilot. Practical feasibility remains open because polynomial degree, compact-cube dimension, trial search and centering precision may be large. No actual inverse entry, matrix eigenvalue or new near-zero sign has been computed here.

## 6. Two limits that cannot be strengthened without new evidence

A bounded-head Neumann lower bound is not a full-inverse lower bound: in the scalar example A=2I and A_n=I, the exact bounded-head inverse and its converged polynomial both equal I, strictly exceeding A^{-1}=I/2. The separate full-form primal bound is essential.

Nor does monotonicity alone supply a uniform convergence rate. The increasing scalar sequence A_n=I for n<H and A_n=2I for n>=H converges for every finite H, but its inverse error stays 1/2 for arbitrarily long H. This is not a theta-specific cost lower bound; it identifies exactly why the proof of eventual stopping is not a practical complexity estimate.
