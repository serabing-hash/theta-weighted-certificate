# Fixed a2048 numerical enclosure contract

This public technical companion preserves the mathematical and numerical-contract
body of the original producer note for a = 1/2048, B = log(8)/2 and k = 256.
Historical delivery/task-control paragraphs are omitted. It describes what the
implementation is intended to enclose, not a claim that source regeneration was
performed merely by copying these files. See the release verification summary
for the actual audit status and the integrated manuscript for analytic premises.
The original exact frozen candidate uses 3072 positive-side P1 cells of width
1/2560 and support [-6/5, 6/5]. No later parameter step is included.

## Space, source coordinates and admissibility

c=cosh(x/2), W=kappa/(2c), dmu=2c*kappa dx, mu(R)=1. The even H norm
is integral |u|^2/W. The mean is m(u)=integral c*u and C u=u-2m(u)kappa.
The full Gamma difference form and every prime power with weight
Lambda(n)/sqrt(n) occur in q0; ell_a=q0+a||.||_H^2.

The source basis is v_n=C(W 1_I e_n), I=(-B,B), with physical Neumann
cosines e0=(2B)^(-1/2), en=B^(-1/2)cos(n*pi*x/B). Define d_n=m(W1_I e_n)
and M_ij=integral_I W e_i e_j. Then F0=M-4dd^T. For f_j=C u_j the source
columns are v'_j=P_V f_j by definition. J_ij=integral_I f_j e_i has a
certified inverse witness; the true source Gram is J^T F0^-1 J, never I.
The enclosure F0<=2I and a certified lower singular bound for J give the
positive scalar F_lower used in the gate. Infinity-to-Euclidean conversion
uses sqrt(256)=16. All frozen candidate/witness floats are checked as exact
dyadics. They define the trial, not an interval enclosure of a floating solve.

Raw u is compact even continuous P1, including its zero endpoints. Its
second derivative is a finite atomic slope-jump measure. The exact Phi
convolution, with logarithmic behavior at knots, belongs to the weighted
row space using the enclosed outer tail. There is no assumed L2 second
derivative. Centering is handled by the inherited weak identity
B_operator*kappa=-kappa/2. Thus q0(Cu,Cu')=q0(u,u')+2m(u)m(u') and
G_centered=G_raw-4mm^T exactly.

## Nonrational boundary and primal forms

All frequencies and normalizations use directed enclosures of true B.
The two terminal hat moments are integrated analytically using
sin(n*pi)=0 and cos(n*pi)=(-1)^n. Both terminal nodes are retained.
The boundary cell is derived by directed comparisons. The 120-bit dyadic
cutoff B0 is only a residual integration model. Its displacement from B
is charged in weighted row norm, and its exact phase splits the boundary
cell in the polynomial-square and polynomial/log cross terms.

T_lower uses 1024 complete positive Gamma labels and drops only the
remaining nonnegative primal form. It subtracts an upper cGamma and every
raw-support prime correlation through11, including n=8. Exact integer
convolution and matrix contractions include their scalar interval radii.
Whole-cell reciprocal-weight lower bounds bound the positive a term.
The additional centered term (2-4a)mm^T is positive and safely dropped.
G_upper uses whole-cell reciprocal-weight upper bounds and exact cell
polynomial integrals; G_centered<=G_raw. Kernel, weight and candidate
dependencies are regenerated in this run.

## Complete residual enclosure

r=D_Gamma u-cGamma*u-Pu+a*u/W-alpha*c-1_(x<B)e*beta,
K=2 integral_0^infinity W r^T r dx.

Fixed alpha and beta witnesses annihilate Z; no unstable numerical projector
is required. D_Gamma u=-sum_l J_l Phi(|x-t_l|) uses all Gamma labels. Exact
jump sum and first moment cancellations are checked. Near zero the checked
Bernoulli/log representation and Cauchy tail are used; away from zero the
positive exponential sum has its full tail. Modular convolution uses five
checked NTT primes, exact CRT dynamic range and explicit 60-bit sample/jump
quantization debits. Model degree32 follows removal of both knot logs.
All current jump norms and coefficient errors are recomputed.

The residual compact interval is [0,2], with 5120 cells. All13 prime powers
2,3,4,5,7,8,9,11,13,16,17,19,23 are included. Shift/weight approximations
have explicit translation and coefficient budgets. No n=8 global term is
deleted because its local source-interval overlap is zero. Every shifted
prime phase, weight-panel boundary and B0 phase is in the integration
partition. Polynomial products are integrated by an enclosed exact-degree
Gauss rule; separate analytic log moments include all series remainders.
The full row cancels before taking its outer product.

Whole-panel positive upper weights produce K_model. A freshly computed
trace upper gives U>=sqrt(trace(K_model)); no previous U is reused. With
weighted row error epsilon_row and arithmetic radius delta,
K_full<=Khat+[delta+2U*epsilon_row+epsilon_row^2+tail_outer]I.
The tail outside |x|>=2 includes all Gamma labels, unenumerated prime
powers and mean witness and is added once. Raw compact terms vanish there.

## Gate, proof implication and verification labels

M=4T_lower-(5a/4)G_upper+(a/4)F_lower*I-(4/nu+5a/nu^2)K_upper.
The sign verifier applies directed400-digit LDL to M-gap*I. A positive
pivot is not used as an eigenvalue estimate. A separate dyadic congruence
witness is checked by exact integer products and then pure Python integers.
Only the actual shifted positive matrix yields a certified gap.

If M>=0, harmonic orthogonality and the full complement floor imply
4S_a-aG_actual>=0. With hstep=a*nu/(a+4nu), b=a-hstep, the completed-square
argument gives ell_b>=0, and coefficient1/2-b under the retained external
energy bridge. This does not establish half or RH.

The implementation's trust boundary includes Python exact integers/Fraction,
directed Decimal elementary operations, IEEE binary64/nextafter, and
single-thread BLAS with explicit ball errors. Re-executing these same modules is
not a second independently developed scientific implementation. The public
saved-matrix adapter uses separate exact reconstruction and integer congruence
checks, but does not itself regenerate source inclusions.
