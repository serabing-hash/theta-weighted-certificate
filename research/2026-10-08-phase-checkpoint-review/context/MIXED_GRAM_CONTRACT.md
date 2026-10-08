# Fixed four-column mixed-Gram and quadrature contract

8 October 2026. License: CC BY-NC 4.0.

This is a proof/code contract derived by reading saved files. No source value,
H action, FFT, physical Gram, or pilot was evaluated. The input numerical
inclusion premises remain premises. In particular, operation counts below
are not a wall-clock or RSS completion guarantee.

## Coordinates and one recommended action interface

Write t=3/64, G=G0-tV, and Z for the 64 true-source analytic brackets of G0.
Then R=Q(X+tTY)-ZY and the four exact new trials satisfy Uq=bR. The saved
compact residual is R0=WX-GY, with column error

    ||q_j-R0_j|| <= epsilon_j := sum_i |Y_ij| e_i.

The parent's combined-polynomial construction freezes J_j of degree at most
41188 after applying the finite Gamma-minus-local-minus-prime multiplier to
its source polynomial. Its analytic quadrature surrogate is

    F_an,j = b F_j,
    F_j = J_j + R_j/64 + Q dtilde_j + 2 mtilde_j cosh(x/2).

The exact delivered finite action can be defined on [-2,2] by replacing b,R
with b8,R8 and setting the result to zero outside. Its full-line difference
from F_an must have its own xi_j ledger. The separate physical error
||H64 q_j-F_saved,j|| <= Bnew_j must not be identified with xi_j.

This combined J design does not call a new source at an outer prime shift.
It retains all inner signed shifts through R and through the proved source
polynomial approximation. The proof of that approximation is a separate
producer obligation.

## A proved complex-strip envelope for the infinite source

Take d=1/8. On Re z=u>=0 and |Im z|<=d, the theta formula gives

    a(z) = sum_(n>=1) [4 pi^2 n^4 e^(4z)-6 pi n^2 e^(2z)]
                         exp[-pi n^2 e^(2z)] / (1+exp(-z)).

Its locally uniform convergence gives holomorphy in |Im z|<pi/4. The theta
identity giving real evenness extends there by the identity theorem;
2cosh(z/2) has no zero there, so a(z)=a(-z). For u>=0,
|1+exp(-z)|>=1 and pi cos(1/4)>3, using pi>31/10 and
cos(1/4)>=31/32. Also pi<22/7 and
sum_(n>=1) n^4 exp[-3(n^2-1)]<2. The latter follows, for example, by a
geometric bound on successive terms. Thus for r=|Re z|,

    |a(z)| <= A(r) := 128 exp(4r-3 exp(2r)) < 7.                 (1)

A is decreasing for r>=0. This is a bound on the full analytic source,
not an asserted complex error for the reflected eight-term function. No
source log-concavity, holomorphic square root, or source evaluation is used.

## Explicit coefficient-derived bracket envelopes

Let C_s be the feature-coefficient majorant at a real shift s:

    A_v(s,d)=sum_cells alpha_l [
       |v_3l| (1+(1+|s|+d)^2/96)
       + |v_(3l+1)| (1+|s|+d)/(4 sqrt(3))
       + |v_(3l+2)| (1+|s|+d)^2/(48 sqrt(5)) ].

Replacing alpha_l by 2, sqrt(3),sqrt(5) by lower rational bounds, and each
|log n| by a rational upper bound makes this entirely rational. It proves

    |Q_v(z+s)| <= exp(K_Q/128) A_v(s,d) (1+r)^2,
    K_Q=24804.

For each residual column let P_y=Q_(Ty), Gamma_y have exact stored dyadic
coefficients, d_y be its old saved frame combination, and p_y its old pole
coefficient combination. Set

    v = x - Ty/64 - d_y,
    C_R = A_v(0,d) + ||gamma_y||_1
          + 10*7*A_(Ty)(0,d)
          + 7 sum_(n<=32,epsilon=+/-1) c_n A_(Ty)(epsilon log n,d),
    D_R = |p_y|,  K_R=32996.

All 18 nonzero Mangoldt terms and both directions occur in this sum. Using
c_Gamma<10 and (1),

    |R(z)| <= exp(K_R/128) [C_R(1+r)^2+D_R cosh(r/2)].          (2)

For the new analytic action bracket use

    C_F = ||J||_1 + C_R/64 + A_dtilde(0,d),
    D_F = D_R/64 + 2|mtilde|,   K_F=41188.                     (3)

The same form (2) holds for F with these constants. For each old Z bracket,
a valid choice is

    C_Z = A_(T_i)(0,d)/16 + ||gamma_i||_1
          +70 A_(T_i)(0,d)
          +7 sum_(n,epsilon) c_n A_(T_i)(epsilon log n,d)
          +A_(d_i)(0,d),
    D_Z=|p_i|, K_Z=32996.

For W_l use C=A_(unit_l)(0,d), D=0, K=24804. For cosh(x/2) use C=0,D=1,K=0.
The constants without their exponential frequency factor also bound real
brackets; retaining d in their polynomial factors only enlarges the bound.

## One fixed integration rule

Use exactly the existing spacing h=pi/4096, N=3912 nonnegative nodes,
M=131072 for new finite-polynomial evaluation, and 160-bit interval
arithmetic. For every even real kernel f=aXY use

    I_N(f)=h f(0)+2h sum_(n=1)^(3911) f(nh).

The old 64 Gamma node caches are on precisely this grid. New J polynomials
fit below its Nyquist index; a new length-M polynomial DFT, if later
separately authorized, is an evaluation transform rather than a source DFT.

Put L_X=C_X+D_X. Since (1+r)^2<=exp(2r) and cosh(r/2)<=exp(2r), the integral
of |aXY| on each boundary Im z=+/-1/8 is at most

    128 L_X L_Y exp((K_X+K_Y)/128) * (26/27) exp(-3).

Indeed, the remaining real integral is
2 int_0^infinity exp(8r-3exp(2r)) dr
= int_1^infinity u^3 exp(-3u) du = (26/27)exp(-3).
The standard strip trapezoidal theorem therefore gives the fully explicit
alias bound

    E_alias(X,Y) =
      16 L_X L_Y exp((K_X+K_Y-131072)/128)/(1-exp(-1024)).      (4)

The coefficient 16 exceeds 256*(26/27)*exp(-3), as exp(3)>20.
All strip integrability and vanishing vertical-edge conditions follow from
(1)-(2), so no unsupported bounded-strip implication is needed. There is
no automatic inheritance of the old 2^-400 threshold: evaluate the actual
coefficient bound (4) outward and either retain it in the interval or reject
the fixed precision/cutoff gate. In the largest-frequency case its exponent
is (82376-131072)/128=-380.4375.

For a sampling tail set r0=299/100, which is below the final node, and
u0=exp(2r0). The positive majorant exp(8r-3exp(2r)) is decreasing for r>=r0.
Integral comparison yields

    E_tail(X,Y) <= 128 L_X L_Y exp(-3u0)
                      [u0^3/3+u0^2/3+2u0/9+2/27].           (5)

This bounds the omitted weighted lattice sum. Adding (4) and (5), native
interval evaluation error, and serialization radii encloses the full-line
analytic integral. Formula (5) is scalar arithmetic, not source quadrature.
As a coarse exact fallback, u0>256 makes its bracketed tail no larger than
its value at 256 and exp(-768)<20^-256. The monotonicity used is that of an
explicit envelope, not of the source.

All pointwise source balls and all old skipped-shift pads must be retained.
The inherited reflected finite evaluator is not used as a holomorphic
function. Its uniform real source discrepancy is a separate pointwise pad.
When obtaining R by Q(X+tTY)-ZY, old node and skip radii propagate through
Y by interval matrix multiplication. Old exact coefficient hashes and
100-bit node radii remain bound to the read records.

## Analytic-to-saved transfer, including the exterior

For any pair of proxies u_an,v_an and delivered functions u,v, if
||u_an-u||<=xi_u, ||v_an-v||<=xi_v and N_u,N_v bound the proxy norms, add

    xi_u N_v + xi_v N_u + xi_u xi_v                            (6)

to the analytic Gram interval. A one-sided transfer sets the other xi to
zero. Formula (6) applies to new/old and new/new action kernels; inherited
old e_i are used for old G0. For W no transfer is needed. A proxy norm is
bounded by the same integral envelope or an already enclosed Gram diagonal.

One elementary new-action xi ledger is available without a lower source
bound. Let delta bound |a-a8| on all real arguments (2^-320 is a safe stated
uniform choice). On [-2,2], |b-b8|<=sqrt(delta). For residual j,

    |R-R8| <= delta [10 |P_y(x)|
                     +sum_(n,epsilon) c_n |P_y(x+epsilon log n)|].

Let B_R be a coefficient-based supremum of the bracket here on [-2,2], and
T_F a coefficient-based supremum of the finite action bracket, using
|J|<=||J||_1, (1+|x|)^2<=9, and cosh(x/2)<=cosh(1). Then an interior L2
bound is

    2 [sqrt(delta) T_F + sqrt(7+delta) delta B_R/64].

Use the corresponding true or finite bracket consistently when splitting
the difference; enlarge T_F by delta B_R/64 if necessary. The exterior
norm is bounded by the square root of

    128 L_F^2 exp(-3u2)
        [u2^3/3+u2^2/3+2u2/9+2/27],   u2=exp(4).

The sum is a valid xi_j. Tighter transfer ledgers may replace it, but a
Boolean analytic-extension flag cannot. The action error budget must also
retain the physical infinite-prime, source-polynomial, multiplier,
coefficient, and exterior errors from the producer contract.

## The complete enlarged matrices and exact kernel count

Let K=G*W, N=G*G and J=V*G refer to the old affine action G. Write F for the
four delivered new action columns and define K_F=F*W, C_GF=G*F, N_F=F*F.
The 1754 new physical kernels are 1488 K_F entries, 256 C_GF entries, and
10 symmetric N_F entries. If integration uses G0 rather than G, set
C_GF=G0*F-t T* K_F* on the whole line; no exterior is dropped.

However the enlarged problem also needs q*W (1488 entries), q*G (256),
q*q (10), and q*F (16). Direct independent integration of everything would
therefore require 3524 kernels. Old trial mixed blocks are linear images
through V=WT and require no separate integrals. The extra 1770 entries must
be supplied even when only 1754 kernels are integrated.

Use the saved residual identity to supply them:

    R0*W = X* A - Y* K,
    R0*G = X* K* - Y* N,
    R0*R0 = X* A X-X* K*Y-Y*K X+Y*N Y,
    R0*F = X* K_F* - Y* C_GF.

Replace R0 by q with the explicit column pads

    q_j*W_l: epsilon_j ||W_l||,
    q_j*G_i: epsilon_j ||G_i||,
    q_j*F_k: epsilon_j ||F_k||,
    q_j*q_k: epsilon_j ||R0_k|| + epsilon_k ||R0_j||
                              +epsilon_j epsilon_k.

Norm bounds come from enclosing diagonals with outward square roots. Thus
1754 is defensible as the new physical integral count only together with
these 1770 algebraic/transfer entries. Optional direct q*F quadrature would
raise the physical count to 1770; it is not logically required.

For the enlarged fixed-eta normal matrix, the actual blocks are

    S_cross = G*F - eta/2 (V*F+G*q),
    S_new   = F*F - eta sym(q*F),
    B_new   = F*W - eta q*W,
    V*F     = T* K_F*.

All normal and energy blocks, including the non-Hermitian 4x4 q*F before
symmetrization, occur here. The 68x68 trial Gram is also required to bound
||[V,q]|| in the deterministic action-error correction. The old bound
101/100 cannot simply be reused.

New frame moments d=<W,q> are the inherited q*W block above. The four pole
moments can be obtained by the parent's certified cached coefficient-dot
construction, with separate product/image/tail errors; no physical pole
quadrature is necessary in that design. Failure of that cached pole contract stops this fixed route; there is no
automatic replacement integration. A stored pole p=2m has coefficient-error
norm |delta p|/2; when storing m itself it is |delta m|, since
||2b cosh(x/2)||=||U1||=1.

## Fixed streaming operation and memory schedule

1. Verify hashes and transform/coordinate conventions. Read each old Gamma
   cache separately, validate its 3912 records, and put them in a compact
   fixed-width file. For example, 256-bit signed midpoint and 256-bit radius
   slots use 64 bytes/record, with bit-length gates checked first. All 64
   old caches then occupy 16,023,552 bytes. Do not retain 64 JSON trees.
2. Evaluate one new J polynomial at a time by the fixed length-131072
   polynomial transform, serialize its 3912 retained nodes, and release the
   full transform vectors/workspace before the next one. Four node files
   use 1,001,472 bytes in the same format. Producer convolution arrays and
   multiplier workspaces are released before quadrature starts.
3. Use 31 blocks of at most 128 nodes. Reconstruct the old Z64 with the
   inherited analytic evaluator, retaining all its pointwise radii. Build
   new F directly as

       J_nodes + Q[(X+tTY)/64+dtilde] - Z(Y/64)
               +2 cosh(x/2)mtilde.

   There is no need to materialize a separate R block or outer prime
   evaluation. Compute weighted new-action blocks against Q, old Z, and
   themselves, immediately accumulate, and release the block. Weight one
   new-action block rather than keeping both Q and a weighted Q duplicate
   when possible. Six prime phase products, shift scratch, trig scratch,
   and old64 frame/trial products must all be in the live-buffer ledger.
4. Add quadrature and analytic/saved transfer pads once, serialize/read back
   K_F,C_GF,N_F, then construct all remaining blocks by exact enclosing
   algebra. Release node and feature buffers before 68- and 372-dimensional
   consumer arithmetic. A future full certificate run must separately
   budget its own 372-dimensional matrices and factor workspace.

The unique-kernel count entails 3912*1754=6,861,648 scalar interval
multiply-add pairs. Dense 4x4 self-products execute 6,885,120 instead.
Direct integration of all 3524 kernels would execute 13,785,888 pairs.
These are not the dominant evaluation costs: the existing old64 evaluator
has three (3912x372)(372x64) products, or 279,410,688 scalar multiply-add
pairs, plus six prime phase products totaling 104,779,008. It has 485,088
feature sine/cosine pairs and at most 144,744 source calls before proved
skips. New F assembly adds 5,821,056+1,001,472 scalar matrix multiply-add
pairs, apart from its four polynomial transforms and cheap scalar work.

This schedule bounds mathematical array dimensions and avoids avoidable
Python-object retention. It does not establish a 512-MiB peak: the Arb/DFT
backend's precision-dependent limb allocation, transform scratch, Python
parsing buffers, allocator retention, and BLAS/native workspaces still need
an explicit allocation bound. A guard that aborts at a limit is not a
completion proof. No sub-600-second claim follows from these operation
counts or from old-family timings.

## Exact proof boundary

The original M_i strip gate and the arithmetic check of exp((2*32996-M)/128)
refer to the old Z family; they do not prove a strip bound for source
products or a new polynomial of degree 41188. Real theta error and real
L2 closeness also do not imply complex-strip control. Equations (1)-(4)
provide a replacement proof for the enlarged analytic quadrature family,
provided the new J descriptor and its physical approximation are separately
certified. The unresolved physical producer error is not repaired by a
successful quadrature gate. Every threshold on the derived constants,
new coefficient radii, node radii, and the final interval width remains a
future arithmetic obligation; none was numerically tested here.
