# Radius-eight analytic complement: producer formula map

This public technical note preserves the mathematical body of the producer's
fixed a = 1/2048 complement derivation. Historical delivery and task-control
logistics are omitted. The integrated manuscript is the authoritative account
of the retained analytic/domain hypotheses and supporting arguments; the
historical label R20 below refers to those inherited estimates, not to a hidden
numerical input required by the code. This note is not a separate new paper.

All retained normalization, minimum/full-domain, theta positivity and weak
source-identity assumptions are unchanged. The source vectors are
C(W 1_I e_n), n=0,...,255. The complement imposes their physical cosine
moments and the single global mean, not independent inside/outside means.

## Local prime norm at the exact endpoint

For L=2B=log(8)=3 log(2), a compressed shift plus its adjoint is a direct
integral of path adjacency matrices. Except for null endpoint fibers the
n=2 paths have three vertices, with norm sqrt(2); the n=3,4,5,7 paths
have two vertices, with norm one. The n=8 overlap has zero measure.
No further factor two is added to these already symmetric shift pairs.
The inherited bounds for a2,a3,a4,a5 sum, after sqrt(2)<3/2, to 493/200.
Also log(7)<39/20 and sqrt(7)>13/5 give a7<3/4. The first logarithmic
inequality follows from a finite positive Taylor sum for exp(39/20)>7.
Thus ||P_I|| <643/200<13/4. Every prime power is accounted for locally;
n=8 remains present in the full operator, source and exterior bounds.

## High-mode Gamma gap

A finite positive Taylor sum gives exp(21/10)>8, so B<21/20. With pi>3,
t=256 pi/B>5120/7. Retaining the first two positive Gamma labels and
integrating the decreasing remaining mesh gives

d(t)>=4t^2/(t^2+1/4)+(4/5)t^2/(t^2+25/4)
      +(1/2)log(1+4t^2/81).

The first two terms exceed 399/100 and 79/100. The last term exceeds
log(2t/9)>log(160)=7log(2)+log(5/4)>392/81+2/9, by the positive atanh
series. Subtracting cGamma<383/70 and 13/4 leaves

h256 > 63521/56700 > 11/10.

The nonnegative local mean pole is dropped only for this lower estimate.

## Complete source, exterior and mean costs

Use the inherited R20 all-tail envelopes at N=8. Put r=27/512. Since
pi<22/7 and pi>3, the source polynomial is bounded by
64+8pi+8/pi+1/pi^2 <5791/63. The exponential bound exp(-pi)<r gives

J2=168(5791/63)^2 r^8,
D=22*42*64*r^8+96*9^3*r^9,
P2=(84*8^3/43)*r^8.

Here P2 bounds half of mu(O), using sqrt(8)<=8 and 16pi-5>43.
The factor168 in J2 includes both source orientations. D is an absolute
exterior lower-order bound including the infinite prime tail.

The exact centered cut identity is
q0[u]=qI[i]+q0[o]-2 Re<J_B o,i>-2|m(o)|^2.
The mean term costs P2 times the weighted exterior norm squared, and
completing the square with h256>11/10 costs J2/(11/10), not twice that.
Consequently the full constrained complement satisfies

ell_a[z]>=(a-epsilon)||z||_H^2,
epsilon=D+P2+(10/11)J2
 =20262735541658121715431/250172086796502324840759296,
nu=a-epsilon
 =101891603714446529085721/250172086796502324840759296 >4a/5.

All exact rational inequalities are independently reconstructed in
inputs/exact_preflight_checks.json by src/check_preflight.py. No finite
prime or Gamma truncation replaces an infinite source estimate.

## Closed reference form on the same constrained complement

Take P_a=qI[i]+tGamma[o]+a||u||_H^2 on the SAME globally centered,
256-moment constrained space Z. Its minimum-domain closure is the retained
R20 reference construction. With Young parameter1/2, the exact cut identity
and the same absolute exterior/mean bounds give

|ell_a-P_a| <= (1/2)qI[i]+eta||o||_H^2,
eta=D+P2+2J2/(11/10) < a/2.

The exact margin is separately checked in inputs/reference_closure_checks.json.
Consequently P_a/2<=ell_a<=3P_a/2 on Z. This supplies the closed positive
form and its energy-space continuity at this new target; it is not a reuse
of the old-radius numerical response. Together with ell_a>=nu||.||_H^2,
the Riesz/Lax-Milgram construction gives the unique harmonic correction.
The trial lies in the full form domain, and its verified weighted row is a
continuous functional on Z. Hence the residual norm and Schur identities
used below apply to every vector in the infinite complement. The numerical
implementation still uses the full weighted row, not a reference-dual solve.

## Sufficient gate and resulting step

For an admitted centered trial f with its actual induced source P_V f,
let T=ell_a[f], G=||f||_H^2, F=||P_V f||_H^2 and let K bound the complete
weighted residual-row Gram. Orthogonality of the true lift gives
S>=T-K/nu and G_actual<=5G/4-F/4+5K/nu^2. Thus

4T_lower-(5a/4)G_upper+(a/4)F_lower-(4/nu+5a/nu^2)K_upper >=0

implies the actual 4S-aG_actual>=0. Its exact penalty is stored in target.py;
26240 is a valid conservative bound since nu>4a/5. This calculation uses
the full weighted row, not an unverified reference-form dual comparison.

Only after a successful full matrix certificate may one take
hstep=a*nu/(a+4nu), b=a-hstep, and infer ell_b>=0. The corresponding
energy coefficient is 1/2-b under the retained energy/form bridge.
Neither the half bound nor RH is proved by this step.
