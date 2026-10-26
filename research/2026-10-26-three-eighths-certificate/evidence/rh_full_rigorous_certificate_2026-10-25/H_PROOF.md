# Full residual-trial enclosure and implementation proof

Fixed original276 moment cells, fine552 source cells,1104 sources,552 quotient coordinates. All computations remain at fixed266-bit MPFR precision. This document describes the implementation; no successful sign is presumed.

## Exact candidate and residual

Exact P/X and dyadic Z define U. Arbitrary original-moment dyadic C defines trial residual r_trial=A Phi_fine U-V C. Weighted projection is optimal, so its exact residual Gram H is bounded above by H_trial=integral w r_trial^T r_trial. The source U is not assumed orthonormal. Its norm and difference from the stored binary64 center are independently enclosed by exact_candidate.

Let p=Phi_fine U, s=(Gamma-cGamma-P)Phi_fine U-V C. Because w=2/(t0 m),

    w r_trial^T r_trial = w s^T s + 2(s^T p+p^T s)+2t0 m p^T p.

This identity avoids differentiating the unknown theta tail. Only kappa8 is differentiated. Delta w=delta_kappa/(t0 cosh(x/2)) and delta m=-2cosh(x/2)delta_kappa/[kappa8(kappa8+delta_kappa)] give an independent pointwise full-theta correction. Both reflected halves contribute factor2.

## Full partition and Gamma cache

All original/fine boundaries and all prime-shift branches are covered by the common phases0,delta and plus/minus log(n) modulo delta for n=2,3,4,5,7. Integer phase floors and strict phase order are MPFR-validated. Unneeded cuts are harmless. Repeat phases on every fine positive cell. No projection onto the fine cell span occurs: original-cell C remains fixed.

For a target fine cell i, source j, and local coordinate xi, the even reflected Gamma row of mode beta is basic(i-j,xi)+(-1)^beta basic(i+j+1,xi). Cache offsets-551 through1103 once per local template. Source normalizers use positive series with explicit remainder. All Gamma tails are retained by exact primitives.

Writing S(s)=gp(s)+gm(s)=log(exp(s)-1),D(s)=gp(s)-gm(s)=log(1+exp(s)) removes the common singular log from D analytically. Outside-source differences additionally use

    S(a+delta)-S(a)=delta+log(1+exp(-a)(1-exp(-delta))/(1-exp(-a))),
    D(a+delta)-D(a)=delta+log(1-exp(-a)(1-exp(-delta))/(1+exp(-a))).

These identities retain shared displacement cancellation before interval evaluation. They are not numerical approximations.

Nonboundary phase pieces have two fixed linear subpanels. Each boundary phase piece uses x=c plus/minus L u^8. The tail0<=u<=2^-10 is analytic. Each of the ten dyadic intervals from2^-10 to1 has two fixed subpanels. No adaptivity or precision increase is used.

## Midpoint matrix quadrature

Jets are normalized derivatives f_j=f^(j)/j!. For each smooth u panel width h,

    integral f = h f0(mid)+h^3 f2(mid)/12+E,
    ||E|| <= h^5 sup||f4||/80.

The domain jet of each scalar weight includes the map Jacobian. The normalized fourth density coefficient is a sum over k+l+m=4. Its operator norm is bounded by sums of scalar weight-jet absolute values times row-jet norm products. For example, the w term is bounded by sum |(wJac)_k| ||s_l|| ||s_m||. Cross and metric terms use the displayed exact decomposition. Each domain row norm uses certified fine-row norm times ||U|| plus original-cell moment-row norm times ||C_cell||. This triangle bound may be conservative but is valid. The full-domain remainder includes factor2 and sums ALL panels.

At midpoint, the full fine row interval is converted to a chosen binary64 center and outward component radii. Its transformation error is bounded by radius-vector norm times ||U||, plus center-row norm times ||U-Ustored||. Original moment trial errors use local C_cell Frobenius bounds. Exact normalization/input uncertainties remain in MPFR point intervals. Matrix products of selected centers are then computed by classical single-thread OpenBLAS. No interval552x552 outer product is performed.

## Floating arithmetic bounds

FE_TONEAREST and actual single-thread OpenBLAS are checked. Nonzero subnormal multiplicative centers are rejected. Center magnitudes above1e50 are rejected, so classical dot partial sums cannot overflow. All nonnegative bound operands are promoted from positive subnormal to at least DBL_MIN before use; each upward add/product adds DBL_MIN and takes nextafter toward infinity. MPFR positive upper exports are also promoted to DBL_MIN. This protects bounds even under flush-to-zero/denormals-are-zero behavior.

For a norm of n binary64 components, sum of squares is bounded using at most2n elementary roundings, an n*DBL_MIN absolute underflow allowance, denominator1-(2n+4)u and final upward square root/division. For sums of n nonnegative terms use denominator1-(n+2)u and n*DBL_MIN. Here u=2^-53. These denominators are exact dyadics at the fixed sizes. Extra divisions/square roots are covered by the spare rounding counts and nextafter.

A length-k matrix product uses gamma_(2k+20) times suitable Frobenius products. Row transformation uses gamma_(2*1104+20). Two-mode transforms use gamma20. Coefficient construction uses gamma12,16,20 as appropriate. Every midpoint outer-product term also includes its scalar-radius and both vector-radius perturbations. Matrix accumulation uses gamma4 times the old matrix and incoming term Frobenius norms. Symmetrization is charged gamma5 times the matrix norm. Diagonal coefficient scaling underflow is charged DBL_MIN*1024*||L||F;1024 exceeds sqrt(552*552). A further1e-280 absolute allowance per transformed row/assembled matrix term dominates dot underflow at all fixed dimensions and operation counts. Positive bound operations themselves use upward helpers.

Quadrature coefficient h is dyadic in u. The fourth-remainder coefficient2h^5/80 is divided upward before summation. Point coefficients are chosen binary64 centers and any construction rounding is included in their radii. GL12/24 agreement from prior diagnostics is not used anywhere as an error certificate.

## Analytic tails

On a boundary tail of physical width h<1, S(s)=log s+R(s),0<=R<=h; D is smooth. Complete reflected Gamma rows have coefficient intervals A+B log(s). Scalar/prime terms join A. Exact theta weight, metric, U norm and original moment C norm give norm bounds A0,B0 for the whole residual. The tail Gram norm is at most

    2 w_max [A0^2 h+2 A0 B0 h(1-log h)+B0^2 h((log h)^2-2log h+2)].

The central tail matrix is zero; this complete positive upper budget is added as Loewner error. No tail is discarded.

## Output and failure semantics

Hmid.bin is an exactly symmetric binary64 chosen matrix. H_ledger.json contains complete quadrature, point/exactification, theta, analytic-tail, BLAS and symmetrization bounds, summed upward. It encloses H_trial in operator norm if every guard and inclusion check passes. A large bound is an inconclusive certificate attempt, not a sign result. A time/resource/domain failure preserves partial checkpoints but supplies no full-domain bound. G and final inertia have separate certificates; neither is inferred from H alone.

## Cached-domain and cached-center optimization

The implementation does not recreate552-by1104 MPFR rows per template. For each of1655 displacement cache entries it stores the componentwise midpoint/radius of the first three point jets and the interval sum of squared absolute domain jets over both modes. MPFR interval prefix sums give a certified squared-norm sum over any contiguous source range. For target i the direct range is[i-551,i] and reflected range[i+1,i+552]. Their square-root bounds are added by the triangle inequality; the sparse scalar/prime rows are added by another triangle inequality. This is potentially more conservative than dense interval recombination but cannot understate the norm.

The two point-cache rows are combined in binary64 with explicit8u(|a|+|b|) and1e-280 error additions, each bound operation upward and padded by DBL_MIN. Sparse scalar and prime contributions are still evaluated by MPFR, converted to outward centers/radii, and added with the same rule. Point-center export rejects nonzero subnormals by IEEE bit pattern, not floating comparisons that DAZ could mask. Positive bound operands, including zero, are raised to at least DBL_MIN before bound arithmetic.

There are exactly60 fixed local templates, including two analytic tails; hence no more than33120 positive-half final pieces. The chosen magnitude cap1e50 and fixed dimensions below2048 imply classical product partial sums below approximately1e104, far from overflow. The absolute1e-280 padding exceeds the unamplified row/dot-output underflow errors at the fixed dimensions. Later amplification of row errors is included in the vector-perturbation terms, not assumed absent. The separately nested G congruence adds4*1104^2*DBL_MIN*(1+||Ustored||F) for first-product underflow amplified by U and for final-product underflow. For coefficient-times-vector scaling, the separate DBL_MIN*1024*||L||F allowance covers a flushed small scaled entry subsequently multiplied by L. The scaled center array is materialized once, checked, and reused for both GEMM and its norm bound.
