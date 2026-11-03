# A computable ground-energy enclosure with finite exact null constraints

3 November 2026 UTC. An analytical computability theorem for the actual theta/Gamma/prime form. No algorithm is implemented or run here, no new finite sign is evaluated, and no practical or uniform runtime bound is claimed. The theorem approximates a real number to prescribed ABSOLUTE error; it does not decide whether that number is exactly zero.

## Result

Let L_c be the complete actual centered self-adjoint operator on H_c. Its known nonzero derivative radical and independent correction bound give

    -d<=m_0:=inf sigma(L_c)<=0.

For every positive rational epsilon, there is a recursive procedure which terminates and returns certified rational L,U such that

    L<=m_0<=U, U-L<=epsilon.                         (1)

It uses only explicit theta/Gamma/prime arithmetic, finite positive reference matrices, and enumerated actual form-core trials. No exact P_N, unknown physical-kernel projection, RH sign assumption, or decision of equality at a spectral threshold is used.

At each fixed positive shift sigma, a positive-reference branch eventually returns a finite certificate whenever

    q[u]+sigma||u||_H^2>=c||u||_H^2 for some c>0.    (2)

A second branch eventually returns an actual strict witness whenever m_0<b. Overlapping thresholds guarantee that at least one branch terminates at each outer enclosure step, even when m_0 equals one of the tested thresholds.

These statements use the complete theta series and its derivative-tail bounds and complete prime/Gamma operator and form formulas. Section 2 independently proves the ACTUAL ambient compact-smooth form core by cutoff and mollification. They are not claims about an arbitrary abstract computable closed form.

## 1 Actual objects and finite coefficient computability

Use

    H=L2_even(dx/W), H_c=ker m, C u=u-2m(u)kappa,
    ||kappa||_H=1, L kappa=-kappa/2,
    L_c=Gamma_c-D_full, Gamma_c>=0,
    N=closure_H span{r_j} subset ker L_c, r_1!=0.

N is the known derivative-radical closure only. It is never identified with ker L_c. The operator and form domains are those of the complete actual construction.

One may start with a rational bound d_bar>d. For example the coarse certified inputs |c_Gamma|<6, W_*<=40e^(-pi)<2, and

    ||D_(>1)||<=640e^(-2pi)<8/5

give ||D_full||<14, so d_bar=16 is sufficient. The mean constraint is essential: the ambient operator has the known negative mean eigenvector kappa, which is NOT a centered negative witness. The nonzero centered r_1 has q[r_1]=0 and proves m_0<=0.

All scalar constants used below are computable reals with rational enclosures. This includes pi, exponentials and logarithms, Euler's constant, and c_Gamma=log pi+gamma_E+pi/2+3log2. Each finite von Mangoldt coefficient is computable as a real, equal to log p when n is a prime power (determined by finite integer factorization), and exactly zero otherwise. “Computable” throughout means uniformly arbitrarily tight rational enclosures, not a finite exact representation of every transcendental value.

The positive complete theta series and derivative formulas are uniformly computable on every compact physical interval with explicit Gaussian/geometric remainders. W is strictly positive. Its positive minimum on a fixed compact interval can be certified by subdivision, interval evaluation and a derivative bound, so division by W on that interval is computable without a zero oracle.

For clarity, the tail facts needed for derivative constraints can be made explicit. For x>=0 the first positive theta term gives

    W(x)>=pi^2 e^(4x)exp(-pi e^(2x)),

while each fixed theta derivative has a computable bound

    |kappa^(s)(x)|<=A_s exp((2s+9/2)x-pi e^(2x)).     (3)

Reflection handles x<0. One explicit recursion is kappa(x)=e^(x/2)sum_(n>=1)P_0(n^2e^(2x))exp(-pi n^2e^(2x)), P_0(y)=4pi^2y^2-6pi y, and P_(s+1)(y)=P_s(y)/2+2yP_s'(y)-2pi yP_s(y). The degree is s+2. For y>=1, bound |P_s(y)| by the sum of its absolute coefficient bounds times y^(s+2). The remaining sum sum_n n^(2s+4)exp[-pi(n^2-1)] has an effective Gaussian tail: for k=2s+4 and n>=k+1, consecutive ratios are at most 2^k exp[-3(2n+1)]<1/2. A finite sum and a geometric remainder therefore produce a rational A_s upper bound recursively. Quotients such as |r_j|^2/W and all ordinary moments of r_j have computable integrable tails: the remaining exponent is a polynomial-exponential factor times exp(-pi e^(2|x|)). Substitute y=e^(2|x|) and bound the resulting incomplete gamma integrals by integer-power exponential integrals. This certifies H norms, physical scalar integrals, Fourier transforms on compact intervals, and their moduli for every FINITE list of derivative constraints. No uniform-in-j small constant is required.

The complete Gamma symbol is computable on compact frequency intervals from

    d(t)=sum_(ell>=0) 2t^2/[a_ell(a_ell^2+t^2)],
    a_ell=2ell+1/2.

For |t|<=T, truncation after ell<L has error at most

    2T^2[a_L^(-3)+1/(4a_L^2)].                      (4)

Also d(t)<=17t^2 and Lip(d on [-T,T])<=34T. Its complete lower bound is

    d(t)>=(1/2)log(1+4t^2).

These formulas give computable values, moduli and certified frequency-support cutoffs. No unbounded Gamma term is silently dropped.

## 2 Recursive dense form trials and the strict negative branch

Here is an independent short core proof, so no zero-jet completeness premise is involved. Let chi_R be an even compact smooth cutoff, equal to one on [-R,R], between zero and one, and with derivative bounded by C/R. Weighted dominated convergence gives chi_R u->u in H. For the COMPLETE Gamma difference form

    t_Gamma[u]=integral_0^infinity rho(s)||u(.+s)-u||_2^2 ds,

write the increment of (1-chi_R)u as

    (1-chi_R(x+s))[u(x+s)-u(x)]
                   +[chi_R(x)-chi_R(x+s)]u(x).

The first term tends to zero in L2(dx rho(s)ds) by dominated convergence using the full finite Gamma energy of u. The second has squared norm at most

    ||u||_2^2 integral_0^infinity rho(s)min(Cs/R,2)^2 ds ->0.

The dominating integral with R=1 is finite at both endpoints. Hence compact cutoff converges in the full form norm. On a fixed compact support, even smooth convolution converges in ordinary Gamma form by the bounded Fourier mollifier and dominated convergence; it also converges in H because W has a positive minimum on a slightly enlarged compact interval. This proves directly that even C_c^infinity is a form core for X.

Now enumerate even compactly supported C1 piecewise cubic splines with rational knots and coefficients in Q+iQ, with the function and first derivative zero at support endpoints. One may use a rational B-spline basis to enforce these conditions exactly. This is a recursive list and is dense in COMPLEX compact-smooth even functions in ordinary H1 on each fixed support after rational approximation. Since W has a positive compact minimum and d<=17t^2, this gives density in the actual form norm on a fixed support. Combined with the preceding cutoff/mollifier argument, the list is a form core for X.

Apply the EXACT computable mean projection C to each trial v. The resulting u=Cv is an actual centered source. Since kappa belongs to X and m is H-bounded, C is bounded on X, and this list is dense in X_c. It is not necessary to know a convergence rate for the core enumeration: every open strict form inequality contains some trial with a finite index.

Every trial's full q and H norm are computable. For v itself, compact physical integrals use the theta lower bound on its support. Its Fourier transform has

    |v_hat(t)|<=D/(sqrt(2pi)t^2), D=||v''||_1,

so the complete Gamma tail is at most 17D^2/(pi T). Every retained prime shift is a finite compact integral; the entire omitted prime tail costs

    tau_N||v||_H^2,
    tau_N<=160(N+1)^2e^(-pi(N+1)).                   (5)

For compact v the prime sum can alternatively be made EXACTLY finite: all shifts log n greater than the support diameter have zero correlation, and a strict integer cutoff can be chosen using powers of two. Thus no zero-at-a-transcendental-boundary decision is needed. For Cv one can either use the admitted theta tails directly or use the exact mean eigenrow identities

    q[Cv]=q[v]+2|m(v)|^2,
    ||Cv||_H^2=||v||_H^2-4|m(v)|^2.

Here m(v)=integral cosh(x/2)v(x)dx is a compact computable integral. No rounding of m(v) is treated as exact centering; use its symbolic computable-real value with enclosing arithmetic.

For a rational b<0, dovetail the trial list and increasing integral precision until a certified upper enclosure satisfies

    q[Cv]-b||Cv||_H^2<0.                            (6)

This implies m_0<b and automatically implies Cv!=0. If m_0<b, the variational characterization and form-core density ensure a trial with a strict margin, so the branch terminates. If m_0=b it need not terminate, and is not required to do so. The algorithm never attempts to decide whether an individual trial's exact expression equals zero.

## 3 Exact finite known-null constraints before reference normalization

Choose any fixed finite independent bank r_1,...,r_j of known actual radicals, possibly j=0. Let P_j be its H-orthogonal projection on H_c, Q_j=I-P_j. Since L_cP_j=0,

    L_c+sigma I=sigma P_j+Q_j(L_c+sigma I)Q_j.        (7)

Thus for sigma>0 it suffices to certify the strict shifted sign on the residual space S_j, the H-orthogonal complement of

    V=(kappa,r_1,...,r_j)

in the ambient even H. These are FINITE exact constraints. No completeness of this finite bank, effective convergence to P_N, or identification of N with ker L_c is assumed.

For a positive ambient reference A with R=A^(-1), the inverse of its form restricted to S_j, extended by zero on S_j^perp, is exactly

    R_S=R-RV(V*RV)^(-1)V*R.                         (8)

The Gram V*RV is strictly positive: R is positive injective and V has independent columns. Its entries, not an identity Gram, must be computed. Refining certified entries eventually proves a positive smallest eigenvalue and permits certified inversion. There is no a priori conditioning or rate assertion. Formula (8) is a finite Lagrange-multiplier identity and does not use a full-kernel projection.

## 4 The positive reference and all full-tail debits

Fix a positive rational shift sigma. For integer N define the complete signed finite-head scalar

    c_N(t)=c_Gamma+2sum_(2<=n<=N)Lambda(n)n^(-1/2)cos(tlog n),
    a_N(t)=(d(t)-c_N(t))_+,
    b_N(t)=(c_N(t)-d(t))_+.

Use a rational certified cap tau_bar_N on the COMPLETE centered tail norm, obtained from (5), chosen to tend to zero; for example enclose its explicit exponential upper bound to error at most 2^(-N) and take the rational upper endpoint. Only cutoffs with tau_bar_N<sigma are considered, and set

    delta'=sigma-tau_bar_N>0,
    p_ref[u]=integral a_N(t)|u_hat(t)|^2dt+delta'||u||_H^2.

Let A be its positive ambient representative, and A_S its form restriction to S_j. Since |a_N-d|<=C_N with

    C_N=|c_Gamma|+2sum_(2<=n<=N)Lambda(n)/sqrt n,

the domain is the complete X and A>=delta'I. The centered/constraint domain is X intersect S_j. Define B_S by the nonnegative form integral b_N|u_hat|^2 on S_j. Then exactly

    ell_head[u]=p_ref[u]-integral b_N|u_hat|^2
               =q_N[u]+delta'||u||_H^2,
    q[u]+sigma||u||_H^2>=ell_head[u].               (9)

The final inequality pays the whole omitted prime tail, not just selected primes or one orientation.

The positive Birman--Schwinger operator

    K_ref=A_S^(-1/2)B_S A_S^(-1/2)

is trace class. The scalar b_N has compact frequency support; W is integrable and A_S>=delta'I. No sign premise for q enters this construction.

A support cutoff is computable with a strict exterior inequality. For example choose a rational upper C_bar>C_N and an integer T with

    (1/2)log(1+4T^2)>C_bar.

Then b_N=0 for |t|>=T. Enumerating powers of two and refining this strict inequality always terminates. The rough integer cap C_bar=17+8ceil(sqrt N), using |c_Gamma|<6 and the elementary full-prime estimate, is also sufficient and avoids equality issues in choosing C_bar. No root isolation of d-c_N is needed.

## 5 A finite positive matrix without deciding zero cell masses

For t>=0 define the actual H source

    g_t(x)=W(x)cos(tx)/sqrt(2pi).

For an even u, <g_t,u>_H=u_hat(t). Project to S_j only after reaching H, and put

    h_t=A_S^(-1/2)P_S g_t.

The continuous feature formula is

    K_ref=2integral_0^T b_N(t) h_t h_t*dt.            (10)

Let B_0=integral W<=1/4, B_2=integral x^2W<=1/2; these follow from the exact theta normalization ||kappa||_H=1 and W=kappa/(2cosh(x/2)). Put

    G_0=sqrt(B_0/(2pi)), G_1=sqrt(B_2/(2pi)).

Explicit upper bounds for these constants suffice. Then

    ||h_t||<=G_0/sqrt(delta'),
    ||h_t-h_s||<=G_1|t-s|/sqrt(delta').

With L_N=2sum_(2<=n<=N)Lambda(n)n^(-1/2)log n,

    Lip(b_N on [0,T])<=L_b=34T+L_N,
    0<=b_N<=C_N.

Therefore the operator-valued integrand in (10) has Lipschitz constant at most

    L_K=(2/delta')[L_b G_0^2+2C_N G_0G_1].

For r uniform cells, Delta=T/r, midpoint t_i, set

    K_r=sum_(i=0)^(r-1) 2b_N(t_i)Delta h_(t_i)h_(t_i)*.

Its certified quadrature norm error is

    ||K_ref-K_r||<=eta_quad,
    eta_quad=TDelta/(2delta')[L_bG_0^2+2C_NG_0G_1].  (11)

This follows by integrating L_K|t-t_i| on each cell. All finite coefficients and the error bound are computable. At a point where b_N(t_i)=0 no division or zero decision is needed. Nonnegative square roots of the computable weights w_i=2b_N(t_i)Delta are uniformly computable, even at zero.

The exact finite matrix with the same nonzero spectrum as K_r is

    M_r=diag(sqrt(w_i)) [<g_(t_i),R_S g_(t_l)>_H]_(i,l)
                                              diag(sqrt(w_i)). (12)

This is the TRUE constrained positive inverse Gram, including all cross entries. It is not a midpoint approximation to an H identity Gram. Formula (8) computes its entries using finitely many ambient inverse entries for (g_(t_i),kappa,r_1,...,r_j).

If a symmetric rational midpoint enclosure M_tilde has certified entry radii E_il, a norm error is at most max_i sum_l E_il. Include that error and all scalar weight and spectral-arithmetic errors. A safe finite gate is

    lambda_upper(M_tilde)+eta_entries+eta_quad<1.     (13)

No eigenvalue oracle is needed: one can verify positive definiteness of the rational matrix I-M_tilde-(eta_entries+eta_quad)I by exact rational LDL or the Sylvester criterion. If it is positive definite, a rational positive eigenvalue lower bound follows, for example, from its determinant and a rational upper norm bound. As all errors decrease to zero and r increases, this gate succeeds whenever lambda_max(K_ref)<1. No sample-only residual or guessed spectral margin is accepted.

## 6 Computable positive-reference inverse entries

This step supplies a recursive numerical procedure, not merely an assumed inverse oracle. It is the existing construction in EXPLICIT_REFERENCE_INVERSE_ALGORITHM.md, stated for the explicit finite source family needed here and a general W cap. No general inverse oracle on unspecified input representations is assumed.

On the ambient even H put

    m_k(t)=min(a_N(t),k)1_[-k,k](t),
    S_k=J*Fourier^(-1)m_k Fourier J,
    A_k=delta'I+S_k.

These positive closed forms increase to A. Hence A_k^(-1) decreases strongly to A^(-1). With a computable alpha_k>=delta'+k W_bar, W_bar>=W_*, let Y_k=I-A_k/alpha_k and q_k=1-delta'/alpha_k. Then

    0<=Y_k<=q_k I,
    P_(k,l)=alpha_k^(-1)sum_(s=0)^lY_k^s,
    A^(-1)<=A_k^(-1)<=P_(k,l)+q_k^(l+1)/delta' I.   (14)

The last inequality gives an UPPER enclosure for <f,A^(-1)f>. P_(k,l) by itself is NOT a lower bound for the full inverse.

Every finite polynomial action scalar in (14) is a finite compact-frequency integral. Its kernels use W_hat and f_hat. The theta/derivative tails in Section 1 make those Fourier transforms uniformly computable on compact intervals with explicit moduli. The scalar a_N and m_k have computable Lipschitz moduli there by (4), finite-head coefficient bounds, and the fact that max/min are 1-Lipschitz. Compact-cube certified Riemann integration thus gives arbitrarily tight rational enclosures. The number and dimension of these integrals can be very large; no runtime estimate is asserted.

Independent LOWER enclosures come from the recursive ambient form core in Section 2, before applying centering:

    2Re<f,v>_H-p_ref[v] <= <f,A^(-1)f>,

with equality in the supremum over the enumerated core. The FULL a_N form is computable: its high-frequency tail on a spline v is bounded by

    D^2/pi [17/T+C_N/(3T^3)], D=||v''||_1,           (15)

and all retained integrals have the scalar and theta enclosures described above. For input f=g_t,kappa,r_j or a finite linear combination, <f,v> and ||f||_H are computable by Section 1.

Dovetail k,l, core trials, and integration precision. Keep the smallest upper endpoint from (14) and largest primal lower endpoint. Stop once their difference is below the requested positive rational tolerance. The loop is EFFECTIVE because all endpoints are rational enclosures; it TERMINATES because strong monotone inverse convergence gives the correct upper limit and form-core variational density gives the correct lower limit. No rate for either limit is needed to recognize the achieved gap. Polarization gives real bilinear entries for the reference input family, whose sources and multipliers here are real even. The core enumeration permits Q+iQ coefficients for density in complex X; its real sublist already suffices for real inverse inputs. Complex entries, if desired, follow by the usual four quadratic polarizations.

This proves uniform recursive computability for every finite input list in (12). Refinement of V*RV until positive definite and its interval inversion in (8) also terminates because that exact finite matrix is strictly positive. No equality test for a small Gram eigenvalue is used.

## 7 Strict-shift completeness, with no effective margin assumption

Suppose (2) holds for a fixed sigma with some unknown c>0. Dovetail over integer N with tau_bar_N<sigma, all positive matrix refinements, and inverse-entry precisions. For every sufficiently large N with 2tau_bar_N<c,

    ell_head[u]>= (c-2tau_bar_N)||u||_H^2>0

on S_j. Compactness and positivity of K_ref imply lambda_max(K_ref)<1: any eigenvalue >=1 would contradict this strict H lower bound through the exact congruence. If the norm were exactly one, compactness would attain it as a positive eigenvalue, with the same contradiction. At that fixed N, (11)-(15) eventually certify (13). A fair Turing-step diagonal schedule over all finite parameters therefore eventually finds a certificate. This means the search never waits indefinitely for one unresolved strict test while starving other jobs; every fixed inverse-entry tolerance job is total by Section 6.

Conversely every successful (13), with all stated debits, yields an explicit positive H lower bound for ell_head and therefore q+sigma on S_j by (9). Exact full null decoupling (7) gives a positive full centered bound, the minimum of that residual bound and sigma on the removed finite bank. The mean eigenvector was excluded throughout.

A returned lower bound can carry a finite arithmetic certificate: the prime-tail cap; scalar Gamma/theta truncations and compact-integral enclosures; finite constraint inverse-Gram bounds from (14)-(15); the rational matrix and its norm-error debits; and an exact rational positive-definiteness witness for (13). A negative upper bound carries the rational spline trial, exact mean projection formula, and strict full-form enclosure (6). A checker verifies only this finite evidence, not the termination search or an uncomputed spectral projection.

Thus this is a SOUND and COMPLETE semidecision for strict shifted positivity. It need not halt when inf sigma(L_c)+sigma=0. Unknown extra physical-kernel directions are not discarded; all unresolved directions remain in S_j and in the full positive matrix gate.

## 8 Overlapping-threshold enclosure and equality cases

Maintain rational [L,U] containing m_0, initially [-16,0] with the coarse bound in Section 1. If U-L>epsilon, set

    a=L+(U-L)/3, b=L+2(U-L)/3, a<b<0.

Dovetail TWO branches:

- the positive-reference certificate for q-a||.||_H^2, namely shift sigma=-a>0;
- the strict negative trial search q[Cv]-b||Cv||_H^2<0.

At least one branch terminates for EVERY actual m_0 in [L,U]. If m_0>=b then m_0>a and the positive branch is strictly true. If m_0<=a then m_0<b and the witness branch is strictly true. In the overlap a<m_0<b both are true. If m_0=a only the second is needed, and if m_0=b only the first is needed. Hence exact equality at a tested threshold never blocks the combined procedure.

On positive success set L=a; on negative-witness success set U=b. Both updates are sound and reduce interval width by the factor 2/3. Therefore finitely many outer steps, at most

    ceil(log((U_initial-L_initial)/epsilon)/log(3/2))

when epsilon is smaller than the initial width, prove (1). Every inner invocation is a dovetailed pair for which at least one branch is proved to terminate; no exact spectral-equality oracle is hidden in the procedure.

## 9 Meaning and limitations

The ground energy m_0 is thus a computable real in this specific actual problem, given the explicit arithmetic and form-core inputs. The number of outer enclosure steps is bounded above as stated. The proof gives termination for every rational input but no a priori numerical complexity estimate in epsilon for an inner dovetail; positive matrix gaps, inverse convergence and trial search have no useful rate here. Under a fixed machine model the runtime of a proved total algorithm is itself a total computable function by simulation, which is not an advance resource estimate. No practical wall-time bound or demonstrated feasible computation is claimed.

If m_0<0, sufficiently tight enclosures or the direct form-core enumeration eventually produce an actual negative witness. If m_0=0, the algorithm can produce arbitrarily close certified lower bounds but no finite enclosure decides exact equality with zero. Equality of a computable real to zero is not decided by its computability. A global nonnegative sign still needs an independent mathematical argument, not an unending sequence of successful finite absolute enclosures declared complete.

Exact P_N is not required for this fixed-accuracy procedure. Finite exact null constraints are allowed but need not exhaust N. Obtaining an EFFECTIVE delta-relative repair approximation to the infinite null-aware Q_N reference remains a separate unresolved task. Neither the earlier quantitative compression nor this algorithm supplies that rate or signs the unresolved actual finite matrix.

## Independent audit

An independent full-file audit verified the recursive theta-derivative and H-tail bounds, the separate cutoff/mollifier form core, Gamma label errors and complete prime-tail budgets, midpoint feature normalization and eta, finite exact constraint inverse Grams, upper/primal-lower inverse stopping, and overlapping-threshold equality handling. The core enumeration uses Q+iQ coefficients so its density claim applies literally to complex X. The audit certifies the analytical total-recursive procedure, not an implementation, performance estimate, actual matrix result, or equality m_0=0.
