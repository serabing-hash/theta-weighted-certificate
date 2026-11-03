# The one-derivative Schur lower expression is not uniformly positive

3 November 2026 UTC. Actual-source analytic counterexample to a proposed SUFFICIENT LOWER-EXPRESSION sign, not to the Schur inequality itself or the original theta sign. No numerical source evaluation.

## Result

Let the right-hand side of (A) in SIGNED_SCHUR_BOUND_FOR_NARROW_ACTUAL_SOURCES.md be denoted L_A[h]. That valid lower bound cannot be made positive on all original source directions merely by reusing its narrow-envelope positivity proof.

For every sufficiently large N define

    m_N=ceil(B_N^2N^3),
    A_N=W1_I cos(pi x/(2B_N))^{2m_N},
    n_N=k_N-m_N-1,
    t_N=n_N pi/B_N,
    h_N=A_N cos(t_N x),  v_N=C h_N.

These are EXACT original sources: the product cosine degree is at most m_N+n_N=k_N-1. Endpoint vanishing to order 2m_N admits the operator/domain and g_N in H^1(I) assumptions. Then

    q0[v_N]=(1+o(1))d_Gamma(t_N)||h_N||_2^2>0,

but

    limsup L_A[h_N]/[d_Gamma(t_N)||h_N||_2^2] <= -39.

Thus L_A is strictly negative on actual source vectors, even though their actual q0 is positive. This refutes uniform positivity of this sufficient lower expression, NOT the validity of inequality (A), NOT the actual harmonic Schur sign, and NOT the endpoint.

## 1 A uniform complete-Gamma modulation estimate

The exact full symbol is

    d(t)=2 sum_{j>=0} t^2/[a_j(a_j^2+t^2)],
    a_j=2j+1/2.

Termwise differentiation gives

    d'(t)=4t sum_{j>=0} a_j/(a_j^2+t^2)^2.

Splitting the sum at a_j=t and comparing the tails to integrals shows, for t>=1,

    |d'(t)|<=C/t,
    log t-C<=d(t)<=log t+C.

The latter also follows directly from the decreasing-mesh upper/lower integral comparison. These are full-symbol estimates, not a truncated Gamma claim.

For t>=2, split an arbitrary frequency shift xi into |xi|<=t/2 and its complement. In the first region use the derivative estimate; in the second use the logarithmic symbol bound and |xi|/t>=1/2. This gives the global bound

    |d(t+xi)-d(t)|<=C[log(2+t)/t]|xi|.

Hence every ordinary H^1 envelope A satisfies

    ||(D_Gamma-d(t))(A exp(itx))||_2
         <=C[log(2+t)/t]||A'||_2.                 (1)

It applies separately to both real carrier signs. Applying it also to A' gives

    ||(D_Gamma-d(t))(A cos(tx))'||_2
       <=C log(2+t)[||A'||_2+||A''||_2/t].         (2)

Here the derivative is a FULL-LINE ORDINARY Fourier-multiplier derivative. The odd derivative is not asserted to lie in an even theta operator domain.

## 2 The varying envelope is slow relative to the carrier

For A=A_N, the Gaussian localization and its first two derivative estimates give

    ||A_N||_2^2 asymp N^{-3/2},
    ||A_N'||_2+||A_N''||_2 <=poly(N).

The exact schedule has t_N larger than every fixed power of N, while n_N/k_N->1. Integration by parts in the oscillatory integral of A_N^2 gives

    ||h_N||_2^2=(1/2+o(1))||A_N||_2^2,
    ||h_N'||_2=(1+o(1))t_N||h_N||_2.

Equations (1)--(2) consequently yield

    ||(D_Gamma-d(t_N))h_N||_2=o(d(t_N)||h_N||_2),
    ||(D_Gamma-d(t_N))h_N'||_2
                  =o(t_N d(t_N)||h_N||_2).         (3)

All little-o statements follow from a fixed polynomial in N divided by t_N, or from Gaussian envelope tails. They are uniform along the displayed explicit N-family.

## 3 Full prime row: scalar form and central derivative region

The absolute scalar autocorrelation of h_N is at most that of A_N. Hence, with ALL n<N and both orientations retained,

    |p[h_N]|<=C N^{-1/2}exp(-cN^3).

Terms n>=N are exactly zero by support. The exact centering correction is nonnegative and of order O(N^{-3}), so (3), c_Gamma=O(1), and d(t_N)->infinity prove

    q0[v_N]=(1+o(1))d(t_N)||h_N||_2^2.              (4)

For the derivative row use the CENTRAL interval J_N=(-1/N,1/N), not a global triangle estimate. The envelope and derivative Gaussian tails give

    ||1_{J_N}h_N'||_2=(1+o(1))||h_N'||_2.

For x in J_N, any shifted point x+-log n in the support is at distance at least (log2)/2 from zero, for large N. Thus the COMPLETE prime derivative row there obeys

    ||1_{J_N}P_raw h_N'||_2
       <=poly(N)(t_N+poly(N))exp(-cN^3)
       =o(t_N d(t_N)||h_N||_2).                   (5)

All possibly nonzero n are below N. This uses no assignment of favorable prime phases. The global bound 12sqrt N||h_N'||_2 would not be enough to prove (5); the central localization is essential.

For g_N=(D_Gamma-c_Gamma-P_raw)h_N|_I, combine (3), (5), c_Gamma/d(t_N)->0, and the central mass equality to obtain

    ||g_N'||_{L2(I)}
       >=(1-o(1))t_N d(t_N)||h_N||_2.              (6)

No global prime-output norm asymptotic is claimed or needed.

## 4 A negative actual lower expression

Let h_k=d(k_N pi/B_N). The symbol derivative/logarithmic estimates and n_N/k_N->1 imply

    d(t_N)/h_k->1,
    (B_N/(k_N pi))t_N=n_N/k_N->1.

The shift term a_N||v_N||_H^2 is o(d(t_N)||h_N||_2^2). The exterior debit subtracted in L_A is nonnegative. Inserting (4) and (6) into that lower expression therefore gives

    L_A[h_N]/[d(t_N)||h_N||_2^2]
       <=1-40(n_N/k_N)^2[d(t_N)/h_k](1-o(1))+o(1),

whose limsup is at most -39.

The true harmonic Schur form can still be positive on this family; the derivative bound epsilon<=B||g'||/(k pi) is deliberately crude for a carrier close to the finite cutoff. Sharper frequency projection or a joint high-frequency completion must replace this estimate before claiming a uniform finite-matrix sign. No actual negative energy direction is produced.
