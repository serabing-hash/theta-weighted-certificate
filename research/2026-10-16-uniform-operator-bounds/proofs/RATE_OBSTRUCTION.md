# A proven obstruction to overly fast full-source tails

Fix the source, B=3/4, orthonormal basis and even cutoffs from ACCEPTED_RESULTS.md. This argument rules out uniform O(M^(-s)) full-source tail bounds for s>1. It does not establish the sharper proposed two-sided M^(-1/2) rate or any positive finite-cutoff lower constant.

## Weighted-energy lemma

Let u∈L²_even(Ω), with Legendre coefficients c_m. Suppose ||T_Mu||≤CM^(-s) for all sufficiently large even M and s>1. Then u∈H¹_loc(Ω).

Write p(x)=B²−x². Legendre integration by parts gives

    ∫_Ω p e_m' e_n' dx = m(m+1)δ_mn.

There is no boundary term since p(±B)=0 and the eigenfunctions are polynomials. In a dyadic block M<m≤2M,

    sum m(m+1)|c_m|²
       ≤2M(2M+1)||T_Mu||² = O(M^(2−2s)).

The dyadic sum converges because s>1. Consequently the Legendre partial sums are Cauchy in the weighted first-derivative norm. On each compact interval I⊂⊂Ω, p≥p_I>0, so the partial sums are Cauchy in H¹(I). Their L² limit is u; hence u|_I∈H¹(I).

## An actual uncancelled source jump

Take u=Ye₀, where e₀=1/sqrt(2B). At

    x₀=B−log 2 ∈ (0,B)

a branch of S₂e₀ switches off. The source's jump has nonzero magnitude c₂/sqrt(2B). The remaining shifts switch at −x₀, ±(log 3−B), ±(2log 2−B), all distinct from x₀. For elementary location bounds, 16<exp(3)<27 follows from the exponential series (the lower bound already follows from its sum through degree 4, and exp(1)<3 gives the upper bound). Thus log 2<B and the listed breakpoints do not coincide.

The functions W_Be₀ and c are continuous in the open interval. The exact regular-kernel term K_ke₀ is H², hence continuous. The low projection Π_LZe₀ is a polynomial. None cancels that isolated jump. Therefore Ye₀∉H¹_loc(Ω), since one-dimensional H¹ functions have continuous representatives.

Since ||e₀||_L²=||e₀||_H²=1 for the standard norm ||h||_H²²=||h||²+||h'||²+||h''||², a uniform O(M^(-s)) estimate with s>1 on either the low16 L² unit ball or the H² unit ball would contradict the lemma. In particular a full-source O(M^(-2)) estimate cannot be obtained by dropping the endpoint-profile tails from the valid H² theorem.

This is an asymptotic obstruction, not a numerical M=128 lower bound and not evidence that a particular finite error budget or J=0 response certificate fails.
