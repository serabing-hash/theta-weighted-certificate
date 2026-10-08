# A source-product Fourier contract for the frozen four-mode residual block

8 October 2026. Author-original research, code and documentation: CC BY-NC 4.0.

## Decision and scope

**The numerical-method design closes at a concrete, finitely testable contract, subject to independent review. Production is HOLD.** No source value, source transform, new H action, physical Gram, polynomial convolution, new Gamma multiplier, or pilot was evaluated here. The computations in this package are exact saved-coefficient sums and rational scalar majorants only. The additional multiplier cache and measured arithmetic certificates are specified future outputs, not already certified facts.

This is ONE frozen source-product Fourier route. It uses precisely X40 and Y40 from the admitted block, the same 372 observations, old 64 trials, true infinite theta source, minimum operator, eta64 and prime cutoff32. It neither reselects four directions nor enlarges rank or cutoffs on failure. The previous all-C obstruction applies to the old fixed64 trial/action family. These four independently admitted residual functions enlarge that family to dimension68; their new action columns are new information. This is therefore a different finite approximation space, rather than another choice of C inside the obstructed old template. Four remains necessary, not proved sufficient. No RH claim is made.

The result is a proof-and-execution contract, not an implemented or successfully timed producer. Its largest rigorously computed analytic error budget is below 7.473e-9. If each of three future measured arithmetic/moment allowances is at most 2^-30, every action norm error is below 1.027e-8, comfortably below the **exact acceptance target 2^-18**. Those three future gates are not presumed to pass.

The executable arithmetic and rational bounds are in code/ and outputs/. The integration proof is in review/MIXED_GRAM_CONTRACT.md. SOURCE_INDEX.json binds the exact local and nested-archive inputs. Scientific premises inherited from the original theta and source-DFT proofs remain inherited premises; this is not a proof-kernel verification of those premises.

## 1. Frozen function and exact factorization

Use U, a=b^2=kappa/(2cosh(x/2)), P=32pi, K=8192, mstar=24804, cstar=mstar/16, Kold=32996 and Kh=41188. The symbol P for period is distinguished below from P_y, the trial polynomial. All source modulations have frequencies m/16 with integer m.

For one frozen dyadic pair (x,y), define P_y=sum_i y_i P_i, Gamma_y=sum_i y_i Gamma_i, d_y=sum_i y_i d_i and p_y=sum_i y_i p_i. The last three quantities use the *exact stored dyadic coefficients* of the old analytic surrogate. Put

  Q_C = Qx - P_y/64 - sum_l Q_l d_(y,l),
  F_P = a P_y,
  Df = c_Gamma f + sum_(n<=32) c_n [f(.+log n)+f(.-log n)],
  R = Q_C - Gamma_y + D F_P - p_y cosh(x/2),
  Uq = b R,
  h = aR = aQ_C + a(D F_P-Gamma_y) - p_y kappa/2.

Here all18 actual von Mangoldt terms and both signs are included. On Fourier coefficients, D is diagonal with

  D_k = c_Gamma + 2 sum_(18 n) c_n cos(k log(n)/16),  |D_k| <= D0=42.

The bound uses c_Gamma<10 and the inherited BOTH-direction prime sum<32. This factorization keeps every shifted-source product. It removes the need to compute36 separate product convolutions.

Let A_r denote the truncated certified periodization coefficients of x^r a, r=0,1,2, and K_0 those of kappa. Write Q_C=sum_r p_C,r(x)x^r and P_y=sum_r p_P,r(x)x^r, where each p is a finite trigonometric polynomial. Form

  F_C^K = sum_(r=0..2) A_r * p_C,r,
  F_P^K = sum_(r=0..2) A_r * p_P,r,
  H^K = F_C^K + A_0 * (D F_P^K-Gamma_y) - p_y K_0/2.

For a feature vector v, the positive-frequency entries for degree0,1,2 are respectively alpha_s v_(3s)/2, +i alpha_s v_(3s+1)/(8sqrt(3)), and -alpha_s[v_(3s)/96+v_(3s+2)/(48sqrt(5))]/2; negative entries are conjugates. These are the existing action_ops signs, applied to the new exact vectors. Insert them at the actual integer shifts +/-m_s, with no coordinate rotation.

Stars in these formulas are ordinary coefficient convolutions. The two first sums take six convolutions; the last product takes one. Exactly seven per column,28 for all four. F_C^K,F_P^K have support |k|<=32996; H^K has support |k|<=41188.

The proposed output polynomial combines Gamma, local and finite-prime operations:

  J_k = [m_Gamma(k/16)-D_k] H^K_k.

This permits action nodes to evaluate a single stored real-even polynomial J, rather than resampling h at36 outer shifts. The approximation error for those finite shifts is nonetheless charged on |x|<=6 below. It does not delete infinite primes.

## 2. Exact saved-coefficient checks

The new inspect_frozen_constants.py reads nested cache records without importing the action producer. Each retained BASE record is an inclusion for

  d_(r,k) = P^-1 integral_R F_r(x) exp(-ikx/16) dx.

These are full-line Fourier samples, equivalently true periodization coefficients. They are not coefficients of a compact physical source. The inherited model bias2^-300 is already inside each record. For |k|>K the inherited bound is |d_(r,k)|<=2^20 exp(-|k|/128).

The saved midpoint/radius integers prove derivative coefficient norm bounds through order2. For all a primitives needed here the convenient caps are (1/2,2,9); for kappa they are (1,4,18). The replay stores actual rational upper bounds, not these rounded caps.

Define A(V)=2 sum_s[(97/96)|V_(3s)|+|V_(3s+1)|/4+|V_(3s+2)|/48]. Then |sum Q_l V_l|<=A(V)(1+x^2); it also bounds the total absolute physical modulation coefficients. The four (A_P,A_C,Gamma coefficient l1) triples are approximately

- (2.27001546,3.03336424,2.87956156)
- (2.14191520,3.16155330,2.77928049)
- (103.82544733,5.00075957,4.05262630)
- (2.18247216,2.99846640,3.26987667)

Only their exact rational values in FROZEN_CONSTANTS.json enter acceptance. Aggregate old Gamma, frame and pole numerators are saved at denominator2^140. Their formation is a saved linear combination, not a new H action.

## 3. Fourier truncation, phases and differentiated products

For a Fourier series v define N_j(v)=sum_k |k/16|^j |v_k|, j=0,1,2. Translation multiplies coefficient k by exp(iks/16), so exact real translation preserves every N_j. Differentiation and multiplication obey

  N_j(uv) <= sum_(l=0..j) binom(j,l) N_l(u) N_(j-l)(v).

This follows termwise from |(k+l)/16|^j and the binomial theorem. For interval phases, the difference from exact phase is included in the finite coefficient radius; it is not assumed to have modulus1 numerically.

Put t=exp(-1/128), n=8193 and C=2^20. The full omitted derivative tails satisfy

  tau0 = 2 C t^n/(1-t),
  tau1 = (2C/16)t^n[n/(1-t)+t/(1-t)^2],
  tau2 = (2C/256)t^n[n^2/(1-t)+2nt/(1-t)^2+t(1+t)/(1-t)^3].

They bound every relevant a and kappa tail. The replay uses outward *rational* substitutes t<=1-u+u^2/2,u=1/128, and t^n<e^-64<(500/1359)^64. The latter follows from the elementary finite Taylor proof e>1359/500. No transcendental-source evaluation is involved.

Let N_j=max_r N_j(A_r), nA_j=N_j(A_0), and let gamma_j be the exact derivative l1 norm of Gamma_y. Define

  eP_j = A_P sum_l binom(j,l)cstar^(j-l) tau_l,
  eC_j = A_C sum_l binom(j,l)cstar^(j-l) tau_l,
  nP_j = A_P sum_l binom(j,l)cstar^(j-l) N_l,
  nB_j = D0 nP_j + gamma_j,
  eH_j = eC_j + |p_y| tau_j/2
       + sum_l binom(j,l)[tau_l nB_(j-l)
                         +(nA_l+tau_l)D0 eP_(j-l)].

Thus eH_j bounds the coefficient derivative norm difference between the exact product-of-periodizations formula and H^K. Its Gamma image is bounded uniformly by20eH_2, since 0<=m_Gamma(xi)<=20xi^2. After multiplying by b, whose L2 norm<=1/2, the Gamma truncation norm is <=10eH_2.

Exact rational replay gives the four upper bounds 1.661e-10,1.576e-10,7.313e-9,1.601e-10. No omitted coefficient is silently zeroed. Cache radii, phase arithmetic, finite convolutions, multipliers and serialization are separate measured errors in Section6.

## 4. Product-periodization and physical-image errors

Multiplying two periodizations does not equal periodizing a product. This is the new analytic error absent from the old modulation producer.

The inherited strip bounds imply, for F=x^r a,r<=4 or F=x^r kappa,r<=2,

  |F(x+iy)| <=256 exp(-2|x|),  |y|<=1/8.

Indeed (|x|+1/8)^r<=exp(r|x|), and exp(2u)>=4u absorbs the polynomial and extra exponential powers in the inherited theta envelope. No log-concavity of a is used.

For |s|<=log32, the off-diagonal periodic-image sum is

  C_s=(sum_j F(.+jP))(sum_k G(.+s+kP))
       -sum_j F(.+jP)G(.+s+jP).

Writing qP=exp(-2P), its strip supremum is bounded by

  delta_s=2^17 exp(2|s|) qP(5-4qP)/(1-qP)^2.

One proof groups k-j=d!=0. The inner lattice sum is bounded by
(|d|+4)exp[-2(|d|P-|s|)]; summing d and the two directions gives the displayed expression. Absolute convergence justifies regrouping. Cauchy gives ||C_s'||inf<=8delta_s and ||C_s''||inf<=128delta_s. For each physical modulation exp(i mu x), the Gamma error is therefore at most

  delta_s[(2/3)(128+16|mu|+mu^2)+32/3].

The constants follow by splitting the second-difference integral at1, using rho(s)<=4/(3s) below1 and rho(s)<=(4/3)exp(-s/2) above1. Take the common delta with exp(2|s|)<=1024, multiply by D0 A_P, and use |mu|<=cstar. The a Gamma_y term has no product-image error because Gamma_y is exactly P-periodic. The same is true of single-source modulations.

For physical rather than product images, write h as its actual single-source/product modulation terms. Define

  f(c)=128+16c+c^2,
  J0=256(A_C+gamma0+|p_y|/2)+256^2 D0 A_P,
  J2=256[A_C f(cstar)+128gamma0+16gamma1+gamma2+64|p_y|]
       +256^2 D0 A_P f(cstar),
  S_beta(L)=2 exp(beta L)exp(-beta P)/(1-exp(-beta P)).

Then |h(x)|<=J0 exp(-2|x|), integral exp(|x|/2)|h(x)|dx<=4J0/3, and
sup_|y-z|<=1 |h''(y)|<=exp(9/4)J2 exp(-2|z|). In the product term the outer a supplies the real tail; the shifted inner source is uniformly bounded by256.

Consequently on |x|<=L,

  |periodize(h)-h| <= J0 S_2(L).

On |x|<=2 the Gamma physical-image discrepancy is bounded by

  I_G = [(2/3)exp(9/4)J2+(16/3)J0]S_2(2)
          +(16/9)J0 S_(1/2)(2).

For the last term, the translated-source integral is bounded by
(4/3)exp(-|z|/2) integral exp(|y|/2)|h(y)|dy. The local derivative term retains its much faster exp(-2|z|) decay. Summation and Gamma interchange follow from the same absolutely convergent derivative and tail majorants.

Thus define

  E_h0 = eH_0 + delta D0 A_P + J0 S_2(6),
  E_G = 20eH_2 + delta D0 A_P[(2/3)f(cstar)+32/3] + I_G.

On the support[-2,2], all finite-prime arguments have absolute value<6. The norm contribution of Gamma/local/finite-prime analytic approximation is at most (E_G+D0 E_h0)/2. These are distinct truncation, product-image and physical-image errors; none is counted as an absent source coefficient.

## 5. Infinite primes, exterior and finite theta transfer

The inherited norm-convergent sandwiched operator tail remains applicable to ANY admitted q:

  ||(K_p-K_(p,<=32))Uq|| <= d32 ||q||,
  d32=14(9*32^2+24*32+20)/(27*4^32).

A saved-Gram norm enclosure for q can be used. For a self-contained conservative prebudget, the exact inequality

  Nq=1024 A_C+gamma0/2+128 D0 A_P+|p_y|/2 >= ||q||

follows from ||b(1+x^2)||<1024, ||b||<=1/2, ||aP_y||inf<=256A_P and ||bcosh(x/2)||=1/2. This intentionally loose bound already passes the frozen error gate.

The retained finite physical action is

  U H64 q = b[G_Gamma h-Dh+R/64+2cosh(x/2)m_h+sum_l Q_l d_l]

plus its omitted-prime term, where m_h=integral hcosh and d_l=<W_l,q>. The infinite prime expression is only asserted after the outer b, as the bounded sandwiched series.

For the exterior |x|>2, use the inherited bounds
||1_ext b(1+x^2)||<2^-95 and ||1_ext p0||<2^-95. Also
||G_Gamma h||inf <=(4/3)J2+(32/3)J0,
|m_h|<=4J0/3 and sum_l|d_l|<=372*2048*Nq. These give the explicit exterior number computed in check_remaining_prebudget.py:

  Eext=2^-95[(4/3)J2+(32/3)J0+D0J0
       +(A_C+gamma0+256D0A_P)/64
       +2*372*2048*Nq+|p_y|/128+4J0/3].

This bounds the true finite-prime physical action outside the stored support. The omitted infinite-prime error is already charged globally once.

The stored function is exactly zero outside[-2,2] and inside is

  g=b8[J+R8/64+2cosh(x/2)mtilde+sum_l Q_l dtilde_l].

R8 uses the exact same frozen symbolic formula as R, replacing only a by the even eight-term a8. No analytic strip estimate is applied to a8. From the inherited full-line error a-a8<=2^-321 and |b-b8|<2^-160,

  ||R-R8||inf,[-2,2] <=1234 A_P 2^-321.

For example the inner shifts have |y|<6 and |P_y(y)|<=37A_P; c_Gamma<10 and both prime directions total<32. The outer transfer is twice its uniform support error (length4). A completely explicit majorant is in the scalar checker, using the finite J coefficient norm, R8<=5A_C+gamma0+256D0A_P+2|p_y|, |mtilde|<=4J0/3+2^-30 and sum|dtilde|<=372*2048*Nq+2^-41.

The report's displayed floating numbers are summaries only. The exact rational ledger gives analytic totals below

- 1.704e-10
- 1.617e-10
- 7.473e-9
- 1.643e-10

respectively, all below2^-24.

## 6. Multiplier extension, interval arithmetic and serialization

Retain support41188. **No retruncation at32996 is authorized by this contract.** If memory fails, stop; do not drop the extra coefficients. A future separately reviewed retruncation would have to pay the weighted coefficient norm of every discarded mode, but it is not this route.

Read original m_k,0<=k<=32996, byte-identically. Produce precisely8192 additional inclusions with the existing digamma interface:

  m_k=Re psi(1/4+i k/32)+EulerGamma+pi/2+3log2,
  k=32997,...,41188.

Set m0=0 exactly and use even symmetry. At160-bit working precision require finite balls, positive lower endpoint for k>0, native radius<2^-100, and serialize as midpoint/radius integers over2^140. The original formula and primitive are in the nested certify_actions.py; the official acb documentation confirms the interval complex-number interface. Formula proof is the inherited positive series for m_Gamma. No assertion that the new entries have already passed appears in this package.

Build D_k up to41188 once for both inner and outer use. Compute each rho_n=exp(i log(n)/16) in complex balls, recursively obtain its powers, and enclose Re(rho_n^k). Intersect exact cosine range[-1,1] where helpful. Carry the complete recurrence radius; there is no reset to an unvalidated unit-modulus midpoint. All18 weights and log intervals are included. Do not use an ordinary float FFT or trigonometric library for inclusions.

At160 bits use acb_poly for the seven finite products. Form the real-even projection by averaging conjugate/even entries ONLY because the exact target has that symmetry and every relevant ball contains it. Serialize final cosine coefficients at2^-100, with DC included. J need not have zero DC: only m0 is zero, while J0=-D0_mode H0 generally is not. This differs importantly from the old Gamma-only descriptor.

For every output coefficient record the enclosing ball before quantization and the exact dyadic output. Let eJ be the sum of outward absolute discrepancies in *cosine* coordinates. It includes inherited source ball radii, all new phases, convolution rounding, both D uses, multiplier extension and quantization. Require

  eJ/2 <=2^-30.

A separate exact midpoint-convolution replay can verify the arithmetic ledger, but does not prove the source-DFT premises anew. Per-operation polynomial error propagation may equivalently use
E(uv)<=E_u N_v+(N_u+E_u)E_v, applied also to differentiated norms. All errors are deterministic correlated enclosures; independence is never assumed.

Descriptor V2 must bind X,Y,T,cell and old action hashes; specify H64 (not H16), ordinary-dx coordinates, support[-2,2], outside exactly zero, true-q definition, combined J role, Kh41188, J denominator100, inherited Gamma_y/frame/pole aggregate denominator140, prime cutoff32 with both signs, theta8 only in the approximant, new frame and pole dyadics, and every error component. Old V1 readers must reject V2. The old assertion nums[0]=='0' must not be copied to combined J.

## 7. Frame and pole moments

Frame moments need no new physical integration. Let G=G0-(3/64)V be the saved whole-line affine old action, R0=WX-GY, and Delta=q-R0. The inherited analytic transfer gives column errors

  epsilon_j=sum_i |Y_ij| e_i,  ||Delta_j||<=epsilon_j.

With A=W*W,K=G*W, enclose

  d=W*q = A X-K*Y + W*Delta,

entrywise radius2048 epsilon_j, retaining all saved matrix radii. Quantize the resulting frame coefficients, and require2048 sum_l e_(d,l)<=2^-30. Do not substitute the larger old physical action errors B_i for e_i here, or assume the analytic and compact residuals are identical.

For the pole,

  m_h=(1/2)integral kappa Q_C
       +(1/2)integral kappa(D F_P-Gamma_y)-p_y/4.

The last identity is exact because integral kappa cosh=1/2. The first term uses the existing BASE_kappa_r moment interface. A requested frequency outside K is a zero-centered ball with radius P C exp(-|k|/128), never exact zero. For the second term use P/2 times the DC coefficient of K_0*(D F_P^K-Gamma_y); this is a finite coefficient dot, not a new convolution or physical integral. Its truncation radius is bounded by

  (P/2)[tau0(D0 nP0+gamma0)+(N_kappa0+tau0)D0 eP0]
    +(P/2)delta D0 A_P.

Add every primitive, retained coefficient, phase and serialization radius. The image term is the DC coefficient bound for the product-periodization discrepancy. Require the complete pole discrepancy e_m<=2^-30. Its action-norm contribution is e_m, since2bcosh=p0 has norm1; it is not e_m/2.

The final per-column certificate adds

  B_j = (E_G+D0E_h0)/2 + d32*Nq + Eext + Etheta8
         +eJ/2 +2048sum e_d +e_m <2^-18.

With the three measured gates exactly as stated, the precomputed outer totals are below2.965e-9,2.956e-9,1.027e-8,2.959e-9. These are conditional bounds, not measured new action errors.

## 8. New action integration and enlarged Gram assembly

Read the independent derivation in review/MIXED_GRAM_CONTRACT.md. It fixes h=pi/4096, M=131072, nonnegative nodes0,...,3911 and even weights. It supplies strip boundary L1, sampling tail and compact/analytic transfer bounds for the new analytic bracket

  Znew=J+R/64+2mtilde cosh+Qdtilde.

The true-source extension is bZnew. Only this analytic extension enters the strip theorem; transfer back to stored b8 and compact support is bounded in norm. Validate the inherited polynomial-DFT sign/normalization with a tiny exact constant-plus-cosine fixture including nonzero DC, then bind each node cache to the exact combined-J descriptor and grid. Gamma-only old nodes are reused by hash, and R nodes are reconstructed as

  R=Q[X+(3/64)TY]-Zold Y.

Thus old complete Z64 nodes must still be reconstructed, or a previously certified complete-node cache reused; an old Gamma-node cache alone does not supply them. The combined J eliminates *new nested* outer-prime source calls, but does not eliminate this old64 reconstruction cost.

Exactly1754 new unique physical kernels suffice IF the following transfers are included:

  Knew=F*W (4x372), Hnew=F*G (4x64), Nnew=F*F (4x4 symmetric).

There are1488+256+10=1754. Directly integrating both q and F against W,G and themselves would have3524 kernels. The other1770 entries are instead algebraic/transfer outputs, not missing blocks.

For example

  W*q = A X-K*Y + W*Delta,
  G*q = K X-NY + G*Delta,
  q*q = (WX-GY)*(WX-GY) + transfer,
  F*q = Knew X-Hnew Y + F*Delta,
  V*F = T* Knew*.

Use radii ||F_i||epsilon_j and the analogous old-column norm factors, and2||R0||epsilon+epsilon^2 for quadratic transfer. The whole-line affine exterior of G remains -3V/64; recover F*G from the integrated F*G0-(3/64)F*V exactly if integrating old compact G0 nodes.

These assemble every block of P68=U68*U68, D68=U68*W, J68=U68*G68 and N68=G68*G68, where U68=[V,q],G68=[G,F]. Recompute a valid nu68>=||U68|| from the actual68x68 trial Gram. Do not reuse101/100 for the enlarged family. Old eta64 stays fixed. A future inverse consumer must propagate all68 action errors through sigma^2=sum B_i^2 and its deterministic Young bound, then obtain a fresh all372 exact positivity certificate. Model improvement alone is not a physical resolvent certificate. No new C, solve, consumer, or positivity run occurs here.

## 9. Deterministic work and memory schedule

Use one producer process, no worker pool,160-bit arithmetic. Use an external supervisor with monotonic deadlines: graceful termination at590s and mandatory process-group kill at600s, plus a600s CPU limit and512MiB address-space limit; cooperative abort at590s and500MiB RSS. Do not copy timeout600 with a further2s kill-after grace period, which permits602s. Report actual elapsed time and the operating system's scheduling granularity; the600s deadline is an enforced abort policy, not a mathematical guarantee of nanosecond signal delivery. Timeout or allocation failure is HOLD, not a reason to relax a gate or retry at larger precision/rank/cutoff. A hard cap proves bounded consumption by aborting, not successful completion.

The future fixed-block work units are:

-8192 new positive digamma multiplier evaluations;32997 inherited multipliers reused
-18 phase seeds and741384 complex recurrence multiplications (18*41188), plus weight/real arithmetic
-24 polynomial products with operand lengths16385 and49609;4 products with lengths16385 and65993
-131988 inner D coefficient multiplications (4*32997),164756 final multiplier products (4*41189)
-4 pole coefficient dots, each at most16385 terms, plus cached linear moments
-4 new finite-polynomial node DFTs of length131072; source DFTs remain zero
-1754*3912=6861648 independent Gram multiply-add pairs (dense4x4 accumulation uses6885120)
-old64 complete-node reconstruction, if no valid complete cache exists: at most144744 finite-source calls before inherited proved skips,485088 feature phase pairs,279410688 main matrix-product multiply-add pairs, and104779008 prime phase-product pairs

The last item is substantial and cannot be omitted from a pilot forecast. Direct schoolbook expansion of the declared convolution calls would have23833424380 coefficient products; that number is a transparent reference workload, NOT a claim that acb_poly uses schoolbook multiplication or that it predicts its runtime.

Allocation schedule:

1. Validate hashes and scan archive records sequentially. Save scalar norms and aggregate dyadic coefficients. Do not retain64 parsed action JSON objects.
2. Build/share D and extended multipliers. The six needed primitive caches are a_0,a_1,a_2,kappa_0,kappa_1,kappa_2 (the last two supply the pole linear moments); only arrays active in the current stage need be resident; frame matrices are loaded only during frame derivation.
3. Process one new column at a time. Stream its three modulation polynomials. Keep F_P and F_C, overwrite F_P by D F_P-Gamma_y, perform one final source product and serialize H/J. Release all column polynomial temporaries before the next column. At the largest product, owned primary coefficient buffers have lengths16385,65993,65993,82377; a native scratch workspace is additional. If the wrapper copies inputs, count those copies too. Do not retain four columns' ball polynomials at once.
4. Free convolution/cache objects before node transforms. One transform at a time owns at most one length131072 input and one length131072 output plus a length<=41189 coefficient buffer; serialize only3912 requested real nodes, then release both transforms. Cache old Gamma nodes by sequential conversion to dyadic arrays/files rather than64 simultaneous JSON object trees.
5. Integrate chunks of at most128 nodes. Only the current Q372,old Z64,new Z4 and prime-phase work buffers are resident. Accumulate the small4x372,4x64,4x4 matrices; keep no full3912x372 ball matrix. Persist checkpoints atomically. All old64 intervals are used as enclosures, not midpoint-only cache values.

These are deterministic logical live-buffer counts and call/operand bounds. Python-object headers, native multiplication/DFT scratch, allocator fragmentation and actual RSS are implementation properties, not proved by a count of coefficient slots. No guessed bytes-per-ball or false guaranteed completion bound is supplied. The wrapper must count actual allocations where available and record RSS/AS at every phase; the external512MiB cap covers hidden native allocations by abort. A representative pilot is the appropriate later empirical evidence, not an alleged mathematical wall-time theorem.

The current environment lacks python-flint; the supplied replay deliberately uses only Python's exact integer/rational arithmetic. A future producer environment must first verify the already specified python-flint0.9.0 APIs and dependency identity. This is an execution prerequisite, not a missing analytic source certificate. No dependency installation was attempted in this task.

## 10. Finite admission gates and stopping rules

Gate0: independent mathematical and interface review of this report, the rational checkers and the mixed-Gram proof. Any discrepancy is repaired before a pilot. Production remains HOLD now.

Gate1: hash/parity/prefix/domain/frozen-column recheck; source records and output exact dyadic definitions agree. Only four frozen columns exist. Reject any change in their coefficients or operator.

Gate2: certify8192 multipliers, all D phases and preliminary scalar budgets within fixed precision; serialize and rehydrate. Recompute every error from stored records. Reject nonfinite balls or a failed radius/positivity gate.

Gate3: if separately authorized after Gate0, ONE representative pilot uses column index2 (the largest certified analytic prebudget), retains its accepted multiplier/phase/action/node work, and measures shared old64 integration setup as well as its own action. The pilot has the same hard600s/512MiB ceilings and may impose a smaller explicit cap in its authorization. It must not launch the other three columns automatically. The pilot computes only its437 unique kernels (372 observation,64 old-action,one diagonal) and may persist the interval Q/weight/old-Z64/new-F2 node records already required for those kernels. Fixed-width256-bit midpoint/radius pairs at denominator2^100 require bit-length validation; retain radii and hash every cache. Streaming Q records for all nodes occupy93,136,896 bytes on disk, old Z64 records16,023,552 bytes, and one new F column250,368 bytes; none need be resident at once. This avoids silently repeating the expensive old64 node reconstruction in a later authorized block. The remaining block then has1317 new unique kernels, including the three cross kernels with the retained pilot. Record exactly what portion is complete and reusable.

Gate4: the parent reviews pilot outputs, complete workload forecast and peak memory evidence before any separate four-action production authorization. A forecast is empirical; a600s/512MiB guarantee applies only to abort consumption. Failure ends this fixed attempt; no rank/precision/cutoff sweep and no automatic retry.

For a later authorized block, each action must meet B_j<2^-18 and all three measured2^-30 allowances. Every Gram radius must include strip alias, finite sampling, node rounding, analytic/compact transfer and saved-block transfer; any unsupported or oversized interval stops the block. Each completed action is hashed and reused, not recomputed after an unrelated failure. Subsequent all372 acceptance, if requested, requires a fresh interval/exact rational consumer certificate and cannot inherit the old factor.

## Reproduction and license

Run, in order:

  python code/verify_source_bindings.py
  python code/inspect_frozen_constants.py
  python code/check_analytic_prebudget.py
  python code/check_remaining_prebudget.py

These routines do not import action_common, invoke a source function, perform a convolution, evaluate a new special-function multiplier, or call an FFT/Gram/action producer. Their output statuses explicitly distinguish saved/scalar checks from unexecuted physical work.

Author-original material is licensed under Creative Commons Attribution-NonCommercial4.0 International: https://creativecommons.org/licenses/by-nc/4.0/ . Third-party sources retain their original rights. Inherited numerical primitive references: https://python-flint.readthedocs.io/en/latest/acb.html and https://python-flint.readthedocs.io/en/latest/acb_poly.html (read8 October2026).
