# Constant mode barrier for future shifted certificates

8 October 2026 · CC BY-NC 4.0

## Conclusion

For the unchanged minimum operator and the fixed 372-coordinate observation map, the constant mode forces

\[
\lambda_{\max}(B_\delta)\ge \frac{c}{c+\delta},\qquad c=\|W^*1\|^2.
\]

The existing exact first trial and its independently recorded whole-line pole moment give **c > 127/64**, conditional on the stated saved enclosure inclusions. A separate exact recombination of already saved source-moment and phase intervals confirms the same strict bound. Therefore

\[
\lambda_{\max}(B_{1/64})>\frac{127}{128}>\frac{99}{100}.
\]

A future delta64 consumer must not reuse the old target B <= 0.99 I. This obstruction does not rule out a valid B < I certificate. It requires any certified positive gap at delta64 to be smaller than 1/128.

## Identity and domain requirements

Let L be the same self-adjoint minimum realization, let e = 1 belong to D(L), and assume Le = 0 and ||e|| = 1. Let W map the finite-dimensional observation space boundedly into the Hilbert space. Set x = W*e, c = ||x||² > 0, and

\[
H_\delta=L+\delta I+WW^*,\qquad B_\delta=W^*H_\delta^{-1}W,\qquad \delta>0.
\]

Assume H_delta >= eta I for some eta > 0. Bounded perturbation gives D(H_delta) = D(L), and the bounded inverse makes every expression below well-defined. Merely saying that a positive self-adjoint operator has zero kernel would not supply a bounded inverse. If one uses that weaker meaning of H_delta > 0, the relevant inverse or inverse-square-root domains must be supplied separately.

Since H_delta e = delta e + Wx,

\[
\begin{aligned}
x^*B_\delta x
&=\langle (H_\delta-\delta)e,H_\delta^{-1}(H_\delta-\delta)e\rangle\\
&=\langle e,H_\delta e\rangle-2\delta+\delta^2\langle e,H_\delta^{-1}e\rangle\\
&=c-\delta+\delta^2\langle e,H_\delta^{-1}e\rangle.
\end{aligned}
\]

This calculation requires e in D(H_delta), but not in D(H_delta²). Cauchy–Schwarz applied to H_delta^(1/2)e and H_delta^(-1/2)e gives

\[
1\le (c+\delta)\langle e,H_\delta^{-1}e\rangle.
\]

Divide the identity by c and use the Rayleigh bound in the nonzero direction x:

\[
\lambda_{\max}(B_\delta)\ge\frac{x^*B_\delta x}{c}
\ge 1-\frac{\delta}{c}+\frac{\delta^2}{c(c+\delta)}
=\frac{c}{c+\delta}.
\]

The generic inequalities are non-strict. Equality in Cauchy–Schwarz holds exactly when H_delta e = (c+delta)e, equivalently WW*e = ce. In that case B_delta x = c/(c+delta) x; equality for the largest eigenvalue additionally requires no larger eigenvalue. Otherwise the Cauchy–Schwarz step is strict. The numerical strict inequality above follows already from c > 127/64 and does not require proving this non-eigenvector condition.

## Small exact saved-data certificate

Use the first existing trial v = WT[:,0], with its exact 372 coefficients t = T[:,0]. The saved T32 is exactly the first 32 columns of T64, so no trial is fitted or changed. Cauchy–Schwarz in coefficient space gives

\[
c\ge\frac{|\langle e,Wt\rangle|^2}{\|t\|^2}.
\]

The source normalization is w = 2 kappa cosh(x/2), while Wt = P_0/(2 cosh(x/2)). Consequently

\[
\langle 1,Wt\rangle_\nu=\int_{\mathbb R}\kappa(x)P_0(x)\,dx=p_0.
\]

There is no factor of 1/2 in this overlap. The factor of 1/2 appearing in the action ledger belongs to the pole action norm and must not be transferred into this identity.

The separate saved pole interval is

\[
p_0\in\frac{1386963357479687028045559562424556245249841\;\pm\;224}{2^{140}},
\]

and exact addition of the frozen coefficient squares gives

\[
\|t\|^2=\frac{574870339585334557}{1152921504606846976}.
\]

Squaring the positive lower pole endpoint and dividing by this exact norm produces

\[
c\ge
\frac{1923667354991326110684944524162808624488355587302110831072674267755960937478638646689}
{968654605984212306374210221979442363967595971739679228298681895365240561284344184832}
>\frac{127}{64}>\frac{99}{64}.
\]

The long lower bound is approximately 1.9859166963; the decimal is explanatory only. All comparisons in the verifier use rational arithmetic.

The verifier also recombines the first column's 372 saved phase records with 315 saved kappa-moment records. For the other 57 pairs it uses the inherited analytic coefficient bound 2^20 exp(-m/128), safely enlarged to the exact dyadic ball 2^(20-floor(m/128)) using e > 2. It checks c > 127/64 again without assuming the saved pole scalar. The signs of the imaginary odd components and the period 32 pi are retained. A rational Machin-series enclosure handles the scalar pi; no new phase, source, transform, action, or physical integral is evaluated.

## What is assumed and what is checked

1. The analytic operator premises are the unchanged self-adjoint minimum domain, e in D(L), Le = 0, and unit normalization. The paper supplies these in its measure and constant equations. The identity and barrier need no assumption that L is nonnegative.
2. The original whole-line source coefficient and phase enclosure inclusions remain explicit inputs. Their source construction charges finite-source substitution, sampling alias, exterior and periodic tails, and directed arithmetic. The archived exact phase audit binds the phase coordinates to the frozen T. This check does not regenerate or independently establish the physical source enclosures.
3. The separate pole interval is justified by that whole-line moment construction, not inferred from the total action residual. A small total action error alone cannot isolate a pole error because component errors can cancel.
4. The new verifier checks exact coefficient norms, interval recombination, strict rational comparisons, and optionally the original archive/member hashes and exact T32/T64 prefix. Hashes establish identity, not mathematical correctness. The two interval routes share the inherited source inputs and are not independent physical integrations.

## How future targets must change

If H_delta remains positive and a separate argument certifies B_delta < I, its true gap satisfies

\[
0<1-\lambda_{\max}(B_\delta)\le\frac{\delta}{c+\delta}.
\]

For fixed W and c > 0, this necessary gap tends to zero as delta tends to zero. Without an independently established upper bound below 1, the lower barrier alone does not prove convergence to 1, exclude an eigenvalue above 1, or prove positivity of L + delta I. In particular, it is not an RH argument.

For a proposed non-strict target B_delta <= q I with 0 < q < 1, a necessary condition is delta >= c(1-q)/q. Thus a fixed positive margin cannot survive arbitrarily small shifts. This is a target-selection constraint before expensive certification work.

## The fixed cover threshold has a separate role

The inherited fixed-W coercivity estimate is

\[
H_\delta\ge\eta_\delta I,\qquad
\eta_\delta=\delta-\epsilon_{\rm cover}-d_\sharp,
\]

where

\[
d_\sharp=\frac{960589}{4389760000000},\qquad
\epsilon_{\rm cover}=
\frac{14194233101692862490101543299783481485}
{3284055810247577849424937639623597936869376}.
\]

Its positivity threshold is exactly

\[
\rho=\epsilon_{\rm cover}+d_\sharp=
\frac{420589436338386427087719740298403628714618993}
{92620636523388719034562694367509285563269120000000}
\approx4.5409905624\times10^{-6}.
\]

The present scalar inverse-bound estimator is justified by this cover only for delta > rho. At or below rho, this particular estimate ceases to establish a positive inverse bound. That is an estimator limit, not a determination of the spectrum or of the true coercivity of H_delta. No finite certificate, nor this barrier, can be extrapolated into RH.

## Reproduction and scope

Run `python code/verify_constant_mode.py --emit` for the portable exact replay. Add `--bind-sources` while the original release remains at its recorded path to check every selected source against that release. Results are in `outputs/EXACT_RESULT.json`; exact extracted inputs and source provenance are in `sources/constant_mode_inputs.json`.

Source anchors: the release paper's equations `measure`, `constant`, `Qfeatures`, `trial64`, and `genericsharp`; the inherited action proof sections 4 and 6; the saved `FRAME_AND_POLE_ENCLOSURES.json`; and the existing phase audit. The proof and producer-code copies in `sources/` document those conventions.

This is a later-consumer advisory. It does not authorize four new columns, alter the frozen j2 pilot, publish any material, or claim a delta64 upper certificate. Counts are zero for new H actions, phase arrays, source evaluations, FFTs, physical Gram integrals, and eigensolves.

New advisory, verifier, and data packaging: Creative Commons Attribution–NonCommercial 4.0 International. See `LICENSE`. Reused source material retains its original rights and terms.
