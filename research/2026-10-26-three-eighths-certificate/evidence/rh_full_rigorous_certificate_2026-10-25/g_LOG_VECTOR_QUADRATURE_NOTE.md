# Full-log vector approximation and reusable Gamma jet cache

This is a supplementary analytic construction, not an executed residual certificate. It preserves the original moment space and every source/prime interaction.

## Removable regularization

Let sinhc(s)=sinh(s)/s with the entire extension sinhc(0)=1. Then

    G+(s) = 1/2 log s + 1/2 log 2 + s/2 + 1/2 log sinhc(s),
    G-(s) = 1/2 log s - 1/2 log 2
            + 1/2 log sinhc(s/2) - 1/2 log cosh(s/2).

The series sinhc(s)=sum_(n>=0) s^(2n)/(2n+1)! gives finite interval jets on domains containing zero; its derivative tails must be included explicitly. This separates the FULL varying exponential-prefactor log coefficient, not merely its leading constant. At x=0, reflected source values may cancel the leading log while leaving x log x, so the full coefficient is essential.

After splitting at all fine Gamma endpoints and all prime-shift jumps, a one-sided singular panel with distance d=x-a in [0,h] has the exact weighted residual vector

    f(x)=a(x)+b(x) log d.

The vectors a,b include the actual sqrt(weight), the exact admissible lift U=P-XZ, the scalar -cGamma U, all prime contributions and the fixed dyadic trial-projection coefficients. The scalar term cannot be discarded for corrected U outside the original V.

## A concrete cubic vector remainder

Use degree-three midpoint Taylor polynomials pa,pb. Suppose Ma and Mb bound the Euclidean norms of their normalized fourth derivatives throughout the panel. Taylor's integral remainder gives

    ||a-pa|| <= Ma |x-c|^4,  ||b-pb|| <= Mb |x-c|^4.

Consequently

    e_panel <= h^(9/2) [ Ma/48
       + Mb/16 sqrt((log h)^2-2 log h+2) ].

The constants follow from integral_(0,h)(x-h/2)^8 dx=h^9/2304 and |x-h/2|^4<=h^4/16, together with integral_(0,h)log^2 x dx=h[(log h)^2-2log h+2]. Smooth panels omit the log term and use the first summand. Panel squared errors add over disjoint regions; when integrating only the positive half of an even function, multiply the summed squared error by two.

Ma,Mb may be obtained from fine-source interval-vector jets and certified ||U||, plus direct local trial terms. Do not perform a 1104-by-552 interval matrix multiplication at every panel. Use central coefficient transforms with a validated floating arithmetic bound, and push the fine coefficient-radius Euclidean norm through ||U||. Since P*P=X*X=I and P*X=0 exactly, U*U=I+Z*Z for exact dyadic Z.

## Fixed rational log-polynomial Gram

Put u=d/h, v=u-1/2. Absorb log h into the ordinary polynomial coefficient. The approximate row is

    p(x)=sum_(k=0)^3 A_k v^k + sum_(k=0)^3 B_k v^k log u,
    A_k=h^k(a_k+b_k log h), B_k=h^k b_k.

Its matrix Gram is h C* M C, where C contains eight row coefficient vectors and M is the same 8-by-8 rational Gram on every panel. In the uncentered u monomials,

    integral_0^1 u^j du = 1/(j+1),
    integral_0^1 u^j log u du = -1/(j+1)^2,
    integral_0^1 u^j log^2 u du = 2/(j+1)^3.

Binomial expansion of (u-1/2)^k gives every entry of M exactly as a rational number. Thus there is no singular quadrature, no omitted endpoint cap, and no numerical log-product integral. A single validated factorization of M can convert the accumulation to rank-eight Gram updates, including its own factorization/rounding error. This avoids 552^2 interval products per panel. Polynomial coefficient interval radii, center conversion, matrix products and summation still require explicit bounds.

If ||f-p||_(L2;operator)<=e and a certified bound B>=||p||_(L2;operator) is available, then

    integral f* f <= integral p* p + (2Be+e^2)I.

This supplies the required residual upper Gram for a sufficient lower certificate. A Hilbert-Schmidt/vector L2 bound on e is valid, although conservative. Approximate eigenvalues or two-order quadrature agreement do not replace either e or B.

## Uniform-phase Gamma cache

Use a universal partition in each fine cell: the fine grid endpoints plus every fractional phase of ±log n modulo δ, n=2,3,4,5,7. Extra cuts where a particular shifted source is absent are harmless. Interval-certify phase order and floor choices. Subdivision must use the same fixed phase-local fractions in every fine cell.

The half-source Gamma row jet then depends only on the target-minus-source cell index and the phase-local panel. For target cell i and source j, the complete even row is

    cache(i-j,phase,mode) + (-1)^mode cache(i+j+1,phase,mode).

This follows from translation and reflection, including all Gamma tail terms. Roughly 1655 displacement values suffice for N=552, instead of computing all 552-by-552 source-target jets afresh for every phase. Process one phase-local panel type at a time: form its displacement cache, process all target cells with their actual varying theta/metric/trial data, then discard the cache. This keeps memory bounded while retaining all interactions. It is not a Toeplitz assumption for the weighted Gram; only the unweighted Gamma row evaluation is reused.

No practical panel count or achieved error is asserted without execution of the actual bounds. A fixed initial phase grid and finite refinement cap can be selected, but budget or accuracy exhaustion must return inconclusive. The separate G generator avoids amplifying weighted residual row error by the very large reciprocal-weight/source metric scale.
