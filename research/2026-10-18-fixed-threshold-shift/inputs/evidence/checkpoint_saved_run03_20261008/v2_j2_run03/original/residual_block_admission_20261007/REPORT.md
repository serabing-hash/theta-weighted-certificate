# Four-mode residual-block admission

Review begun 7 October and completed 8 October 2026 (UTC).
Decision: **HOLD physical production**.

This is an implementation-and-resource admission decision, not a mathematical
impossibility result. The unchanged minimum weighted operator, infinite theta
source, 372 observation coordinates, and existing 64 trials are retained.
No new H action, FFT, source value, or physical Gram integral was evaluated.

## Result

1. **The necessary rank is now certified.** The optimized fixed-G64,
   fixed-eta quadratic model has at least four eigenvalues strictly greater
   than 27/25. A positive-semidefinite correction of rank at most three
   cannot make this model at most I. The old floating count was not used as
   an acceptance test.
2. **The one frozen analytic block is domain-valid and nonredundant.** For
   the four specified columns q, the saved-data certificate proves
   q*(I-Pi_V)q >= (1/10)q*q + beta I4, with beta > 0.01200536124944.
   Thus adjoining these columns gives dimension 68. Domain validity follows
   from the explicit minimum-domain proof below, not from a Boolean file flag.
3. **The current action producer cannot certify this block unchanged.** Its
   supported inputs are degree-at-most-two polynomial modulations of the
   fixed observation frequencies. The proposed block contains source
   products, shifted-source products, and the stored Gamma polynomials.
   New convolution/error contracts and action/Gram enclosures are required.
4. **No rigorous complete-run bound below 600 s and 512 MiB is available.**
   Old timings describe another function class, and even their old forecast
   understated the eventual memory peak. This review therefore does not
   admit a four-action production, rank sweep, or automatic enlargement.

There is no RH proof or disproof. Even a future successful 1/64 certificate
would be a fixed-threshold milestone, not all-negative spectral exclusion.

## 1. Frozen inputs and exact finite result

The immutable release is
`/workspace/shared/theta_delta32_release_20261007`.
The new diagnosis is
`/workspace/shared/delta64_failure_diagnosis_20261007`.
This separate directory contains only review-derived artifacts.

The source definitions are in the diagnosis's
`sources/INHERITED_SOURCE_MANUSCRIPT.tex`, especially equations `coordinates`,
`Qfeatures`, `g0definition`, and `quadmajor64`, and its paragraphs following
`g0definition`. The actual producer is in the release's
`replay/restored_full/code/{action_common,action_ops,extension,cert_support}.py`.

One saved-M eigensolve and one 64-by-4 saved-S solve proposed four columns.
Their entries were frozen as integers in `outputs/X40.csv` and `Y40.csv`,
divided by 2^40. There was no search, iteration, or mode enlargement.
All acceptance arithmetic then used integers and rational numbers.

Let eta be the exact inherited eta64, t=3/64, G=G0-tV, and

  S=G*G-eta sym(V*G), B=G*W-eta V*W,
  M(C)=(A-B*C-C*B+C*SC)/eta.

The inherited rational congruence is rechecked, establishing S>=I/50000.
For frozen X,Y, E=SY-BX, completing the square gives

  X*M_opt X = F(X,Y)/eta - E*S^-1 E/eta
             >= F(X,Y)/eta - ||E||_F²/(eta mu) I4,

where F=X*AX-Y*BX-X*B*Y+Y*SY and mu=1/50000.
All Gram radii are propagated through F and E; the matrix radius is
subtracted as its maximum row sum. Exact strict diagonal dominance proves

  X*(M_opt-(27/25)I)X > 0.

The minimum certified Gershgorin margin is about 0.00627561479384.
The entire solve/rounding correction is bounded by about 4.964e-17.
This proves a four-dimensional positive subspace of M_opt-(27/25)I,
including full rank of X. These are model eigenvalues, not physical
operator eigenvalues or lower bounds on W*H64^-1W.

## 2. Exact low-rank update and its scope

For k additional trial/action pairs, suppose the same fixed-eta quadratic
model has positive enlarged normal matrix

  S_plus = [[S,T],[T*,R]],   B_plus = [B;b].

Set J=R-T*S^-1T>0 and D=b-T*S^-1B. Block elimination gives exactly

  M_plus,opt = M_opt - eta^-1 D*J^-1D.

The improvement is positive semidefinite of rank at most k. On a
four-dimensional positive subspace of M_opt-(27/25)I, every rank-at-most-three
correction has a nonzero kernel vector. Therefore its corrected Rayleigh
value remains greater than 27/25. In particular, a one-trial repair cannot
close this same template. The statement extends to a positive-semidefinite,
well-posed normal matrix using its range and pseudoinverse. It does not apply
to an indefinite unbounded-below surrogate optimization.

Four is a necessary lower bound, not a sufficient number. Changing eta,
changing the estimator, or controlling H^-1 on a residual subspace is a
different mathematical method and is not ruled out by this rank statement.

## 3. The actual analytic residual, without omitted source terms

Write Qx=sum Q_l x_l, P_y=sum P_i y_i, Gamma_y=sum Gamma_i y_i,
d_y=sum d_i y_i and p_y=sum p_i y_i. In ordinary coordinates the prescribed
analytic surrogate is U G0_an=b Z, with the **true** source a=b² throughout.
For each frozen pair (x,y), Uq=bR, where

  R = Qx - P_y/64 - Gamma_y + c_Gamma a P_y
      + sum_{n<=32} c_n sum_{epsilon=+-1}
          a(x+epsilon log n) P_y(x+epsilon log n)
      - sum_l Q_l d_{y,l} - p_y cosh(x/2).

The sum retains all 18 nonzero von Mangoldt terms and both signed shifts.
The -P_y/64 coefficient is important: 1/16-3/64=1/64.
In weighted coordinates q=R/(2cosh(x/2)), and its physical source is h=aR.
Thus h contains all of the following:

- a times the Q and P modulations, and a times the frame modulations;
- -a Gamma_y, with Gamma frequencies up to 32996/16;
- c_Gamma a² P_y;
- both-direction products a(x)a(x+-log n)P_y(x+-log n);
- -p_y a cosh(x/2)=-p_y kappa/2.

Neither the finite eight-term source nor the discontinuously zero-extended
saved G0 is silently substituted for this analytic function.
It is also not silently identified with the exact residual Wx-H64Vy:
their norm difference is at most sum_i |y_i|(B_i+e_i), by the inherited
whole-line action and analytic-surrogate transfer bounds.

## 4. Minimum operator domain proof for the analytic block

The inherited theta theorem states that every fixed derivative of kappa
decays faster than every exponential on both real tails. Since
a=kappa/(2cosh(x/2)), the same property holds for a and every fixed derivative.
A finite real translate of a has the same property, with constants depending
on that translate. Each Q and P is a finite degree-two polynomial modulation.
Every derivative of the finite Gamma polynomial is bounded by
sum_k |gamma_k|(k/16)^m. These constants are finite; no uniform-in-index
bound or unsupported smoothness assumption is being made.

It follows term by term from the displayed R that h=aR belongs to H^m(R)
for every fixed m and decays faster than every exponential. The cosh term
in R produces the constant -p_y/2 in weighted q; therefore it would be wrong
to claim that all of q decays to zero. Nevertheless q and its derivatives
are bounded, and q belongs to L²(nu), since nu(R)=1.

For smooth even compact cutoffs zeta_R, zeta_R q -> q in L²(nu), and
kappa zeta_R q=zeta_R h -> h in H¹(dx). The source identity and

  D_Gamma(g) <= ||g'||² integral_0^1 s² rho(s) ds
                +4||g||² integral_1^infinity rho(s) ds

together with the bounded sandwiched prime and pole operators make the
cutoffs Cauchy in the **minimum** form norm. Hence q belongs to that form
domain, without identifying it with a maximal domain.

Since h is H², the Bochner integral
G_Gamma h=integral rho(s)[2h-h(.+s)-h(.-s)]ds converges in L²: its norm
integrand is at most s²||h''|| near zero and 4||h|| at infinity.
Multiplication by b is bounded. The infinite prime operator is the same
norm-convergent sandwiched operator as in the inherited theorem. The pole
and fixed frame terms are bounded. The polarized core identity therefore
represents the form by an L² vector, first on compact tests and then on the
minimum form domain by continuity. The representing-operator criterion
proves q in D(L)=D(H64).

Explicitly, with m_h=integral h cosh(x/2) dx and
d_l=integral a Q_l R dx, its actual action is

  U H64 q = b[ G_Gamma h - c_Gamma h
                -sum_{n>=2} c_n (h(.+log n)+h(.-log n))
                +R/64+2 cosh(x/2)m_h+sum_l Q_l d_l ].

This formula defines the mathematical action. It does not assert that a
numerical implementation already encloses it.
The infinite prime series in the displayed bracket is interpreted after
multiplication by the outer b, as the norm-convergent sandwiched operator;
no unsandwiched full-line L² convergence claim is needed.

## 5. Exact nonredundancy, including analytic-surrogate transfer

Let R0=WX-GY be the saved compact-approximant residual block and
Z=V*R0=DX-(J0-tP)Y. The exact saved Grams enclose

  R0*R0 = X*AX-X*K*Y-Y*KX+Y*NY.

The norm certificate gives P>= (1-epsilon)I, epsilon<8.93e-9. Consequently

  R0*Pi_V R0 = Z*P^-1Z <= Z*Z/(1-epsilon).

For Delta=q-R0, its j-th column norm is at most
sum_i |Y_ij| e_i, using the inherited analytic-extension errors, not the
larger physical action errors B_i. The computed Frobenius upper bound is
7.028e-24. Let r bound ||R0|| and e bound ||Delta||. Since
||0.9I-Pi_V||=0.9, transferring the quadratic expression loses at most
0.9(2re+e²)I4. All quantities are bounded outward rationally, including the
square roots. Exact diagonal dominance then proves

  q*(I-Pi_V)q >= 0.1 q*q+beta I4,
  beta > 0.01200536124944.

This is stronger than the proposed one-tenth relative gate, and certifies
the smallest new projected Gram eigenvalue is at least beta in these frozen
coordinates. It does not certify the quality of their future H actions.

## 6. Why the numerical producer is not admitted

`action_ops.gamma_column` forms only three polynomial convolutions of
cached Fourier arrays for a x^r, r=0,1,2, with the original fixed Q modes.
`action_common` fixes K=8192 and MMAX=24804, hence KOUT=32996.
`extension.inherited_caches` requires exactly 32997 Gamma multipliers.
The descriptor, action-error budget, node evaluator, and frame/pole builder
all bind to this original family and its Ai coefficient majorant.

The proposed h has additional source products that this interface cannot
express. Even its finite-polynomial a Gamma term has natural convolution
support through 8192+32996=41188. Products of two cached a polynomials and
the old feature modulations also reach 2*8192+24804=41188. This is an index
accounting fact, not proof that every such coefficient is significant.
Keeping the old cutoff would require a new certified retruncation bound;
keeping the larger support would require additional multiplier inclusions.
Neither exists in the inspected contract.

It may be possible to reuse the existing a and kappa caches with product
convolutions and phase shifts. New source DFT arrays are therefore **not**
proved necessary. What is necessary is a new validated product/tail/image
contract, including source errors propagated through products, translations,
Gamma multiplication, and coefficient serialization. The inherited Ai-only
tail formulas cannot simply be relabeled as bounds for q.

The action's finite-prime evaluation now samples h containing shifted-source
products at further shifts. It must retain every nested signed shift. The
infinite-prime tail can in principle use the already proved operator norm
bound times an independently enclosed ||q||. The new pole moments and all
372 frame coefficients require valid enclosures too. Some frame and trial
Grams can reuse the old matrices and analytic transfer; this does not supply
the missing Gamma-action and action-action enclosures.

For four new action columns alone, the minimum old-style action-Gram count
is 4*372 +4*64+4*5/2 =1754 new unique kernels. This count omits new producer
setup, any additional moments, source-product proofs, and possibly additional
evaluation work; it is not a complete cost estimate. There is no implemented
end-to-end call graph to which a rigorous operation or memory bound can yet
be attached.

The old pilot forecast was 166.7466 s and 359584 KiB. The actual old main
used 185.1128 s wall, 184.8799 s CPU, and 454268 KiB peak RSS. The record
explicitly says its forecast was not a guarantee. Multiplying the old
per-column time by four does not bound product-source actions. A hard
600-second/512-MiB guard bounds consumption by aborting, but is not a proof
that the requested production can complete within it.

## 7. A genuine alternative, and its limit

Discontinuity alone does **not** exclude saved compact G0 from this
log-order operator domain. This review corrects any such inference.

On [-2,2], the saved function U G0= b8 Z8 is piecewise smooth with bounded
one-sided derivatives and finite jumps after zero extension. The reflected
finite theta source may also have derivative corners at zero and at the
finitely many shifted-source knots +-log n inside the support; these do
not change the argument. Since the true w is positive smooth on this
compact interval, the weighted f=U^-1(U G0) and h=kappa f have the same
piecewise-regular structure. For small s,

  ||h-tau_s h||_2 <= C sqrt(s).

The proof separates O(s)-measure neighborhoods of the finitely many breaks
from the remaining intervals, where the derivative bounds apply. Thus the
Gamma Bochner integral converges near zero because
rho(s)||2h-tau_s h-tau_-s h||=O(s^-1/2). Large s is harmless.
For a minimum-domain approximation, compact piecewise-Lipschitz functions
belong to H^alpha for 0<alpha<1/2, as follows from this same translation
estimate and the fractional Sobolev difference integral. Even mollifications
converge in H^alpha, and multiplication by smooth kappa on a common compact
support preserves that convergence. The bound
||g-tau_sg||_2<=C_alpha s^alpha||g||_{H^alpha} makes the Gamma form norm
converge. The source identity and bounded remaining terms then give minimum
form admission; the L² action argument gives operator-domain admission.

Consequently the compact residual WX-(G0-tV)Y is also domain-admissible by
linearity. A direct real-space action producer with the known endpoints
and logarithmic edge behavior is a genuinely different implementation
route, not a renamed smooth-family run. It would require certified singular
quadrature, endpoint treatment, whole-line tails, and all mixed Gram errors.
No such implementation or reliable cost forecast was found. It is not
admitted here, and no speculative timing is assigned to it.

## 8. Actionable gate and stopping decision

**HOLD this four-action production now.** The mathematical domain and
nonredundancy gates pass; numerical action support and the complete bounded
execution gate do not. The present review is finished, not an open-ended
request to keep trying ranks or precisions.

Reopening this route would require a separate explicit decision to develop
one certified producer, either the source-product Fourier method or the
piecewise-regular real-space method. The cheapest missing item is a complete
proof-and-code contract for one fixed new action family, including a declared
finite cutoff, all tails and transfers, and a memory allocation schedule.
Only after that exists could a separately authorized representative pilot
provide empirical timing evidence for a fixed-block run. Empirical timing
would still need to be labeled as a forecast rather than a completion proof.
No pilot or production was launched by this review.

## 9. Reproduction, resources, and limitations

`python code/certify_saved_block.py --replay` reads the frozen integers,
checks the inherited S congruence, and reproduces both four-dimensional
certificates without any solve or eigensolve. The default proposal execution
must not be rerun over an existing block. The source paths and hashes are
listed in `SOURCE_INDEX.json`.

The proposal-plus-exact-check core used approximately 0.548 s wall,
0.542 s CPU, and 105736 KiB peak RSS. The same-code integer replay used
0.298 s wall, 0.293 s CPU, and 78592 KiB. Both had explicit 30-second
CPU/wall and 512-MiB address-space limits. These are computational-core
measurements, not total research or file-preparation time.

The finite claims retain the inherited physical Gram and analytic-transfer
inclusion premises. This review did not freshly regenerate those integrals.
Same-code replay is reproducibility, not independent verification. A separate
common-denominator arithmetic implementation independently matched all four
model and projection margins, including the transfer and solve corrections;
it performed no solve, eigensolve, or physical evaluation. Its script and
result are included under `independent_audit/`. The independent domain and
producer review found no material flaw and agreed with the HOLD decision.
This is separate arithmetic and mathematical review, not external peer
review or proof-kernel verification. All conclusions
refer to this minimum weighted operator; no spectrum outside the current
threshold has been signed by this work.

## License

Author-original research, code, and documentation: Creative Commons
Attribution-NonCommercial 4.0 International (CC BY-NC 4.0),
https://creativecommons.org/licenses/by-nc/4.0/ . Third-party source material
retains its original rights and applicable terms.
