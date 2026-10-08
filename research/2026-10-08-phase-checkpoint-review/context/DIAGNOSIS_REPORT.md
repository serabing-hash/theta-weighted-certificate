# Why the fixed delta 1/64 bound failed

**Date:** 7 October 2026  
**Scope:** the unchanged minimum closed even weighted operator, the exact
372 observation coordinates, and the existing 64 trial functions.  
**Status:** two new exact finite certificates; one bounded saved-data
projection diagnosis; actual off-trial spectral sign remains open.

## 1. Answer

The failure is now localized substantially more precisely than “the number
1.4826 exceeds 1.”

1. **CERT — the current trials do not contain a delta64 negative witness.**
   For every `v` in their span,
   
   `⟨v,Lv⟩ >= −(1/250000000)||v||²`,
   
   and therefore
   
   `⟨v,(L+I/64)v⟩ >= (3906249/250000000)||v||² > 0`.
   
   The latter constant is exactly `0.015624996`. These inequalities include
   all saved Gram radii and the actual certified action errors. They are
   restricted inequalities, not full-operator bounds.

2. **CERT — coefficient selection cannot rescue the existing estimator.**
   For every real `64 × 372` coefficient matrix `C`, the same fixed `G64`
   quadratic residual model satisfies
   
   `lambda_max M_G64(C) > 37/25 = 1.48`.
   
   This statement also includes all saved Gram radii. Its positive
   normal matrix has the exact certified bound `S >= I/50000` and condition
   number at most `204489.516`. The error allowance for the frozen
   coefficient-direction rounding and normal-equation residual is only
   about `1.0231e−17`. The obstruction is not a bad numerical solve.

3. **DIAG — most of the large model penalty is off the trial space.**
   In the saved model's worst observation direction, 89.03% of the
   approximate residual squared lies orthogonal to the trial span. The
   scalar `eta64⁻¹` charge on that part contributes `1.19812` to the model
   value `1.48263`.

4. **OPEN — the actual spectrum outside that span.**
   These results distinguish a failed certificate template from a negative
   spectral witness. They do not establish whether the actual resolvent
   crosses the threshold. They also do not establish that adding trials is
   the only remedy: sharper control of the residual under `H64⁻¹` could
   improve the estimator without changing the family.

Thus the justified diagnosis is: **the existing family together with its
scalar-coercivity residual estimator is insufficient; the existing trials
are rigorously positive at the requested shifted threshold; an actual
negative off-trial obstruction is neither exhibited nor excluded.**

## 2. Objects and correct shifts

All notation refers to the same inherited minimum domain. Write

- `V = WT64`, with 372 observation columns and 64 trial columns;
- `H16 = L + I/16 + WW*` and `H64 = L + I/64 + WW*`;
- `H16 V = G0 + E`, with individual actual bounds `||Ei|| <= Bi`;
- `G64 = G0 − (3/64)V` on the entire real line;
- `H64 V − G64 = E` exactly.

The exterior of `G64` is `−3V/64`, not zero. No compact truncation of that
exterior, change of source, maximum-domain replacement, or alternate
operator is used.

The inherited coercivity parameter is the exact positive rational

`eta64 = 1446776856241610348487954379752034183297365381007 /
92620636523388719034562694367509285563269120000000`.

It is a proved coercivity lower bound, not an assertion that it equals the
bottom of the spectrum of `H64`.

Define whole-line matrices

`A=W*W`, `P=V*V`, `D=V*W`, `J0=V*G0`,

`K64=G64*W`, `N64=G64*G64`, `F64=sym(J0)−3P/64`.

The actual signed trial forms are

`V*L V = sym(J0) − P/16 − DD* + sym(V*E)`,

`V*(L+I/64)V = F64 − DD* + sym(V*E)`.

No eigenvalue of `M`, `H64`, or a finite compression is silently relabeled
as an eigenvalue of `L`.

## 3. Exact restricted signed-energy certificate

The input center/radius pairs have denominator `2^100`. The producer forms
`sym(J0)−P/16−DD*` with exact integer products and propagates every product
radius. For the action term it uses

`|c* sym(V*E)c| <= ||Vc|| ||Ec|| <= nu sigma ||c||²`,

where

`nu = 101/100`,

`sigma <= 443292754562665/151115727451828646838272`,

`nu sigma = 8954513642165833/3022314549036572936765440`.

This last number is about `2.96280003185647e−9`. No independence assumption
is made. The induced saved-Gram radius loss is about `3.37826e−16`.

The target matrix is `V*LV + (1/250000000)P`, not the incorrectly normalized
matrix with an identity in place of `P`. After subtracting an exact row-sum
radius bound and the outward action allowance, a full square rational
congruence `Z` is checked by integer strict diagonal dominance. All 64
Gershgorin lower margins are positive; the smallest, after rescaling, is
about `1.0341651e−9`. Positivity of the full square congruence itself proves
that `Z` is invertible. Floating eigenvectors merely proposed the dyadic
entries of `Z`; the acceptance test uses no floating spectral assertion.

A separate exact directional calculation for the rounded almost-null
trial gives the signed `L` Rayleigh interval

`[−2.105461118904113e−11, +2.105462098027031e−11]`.

Accordingly, **nonnegativity of even the finite trial form is not certified**.
The source theorem already states `1 ∈ D(L)` and `L1=0` (equation
`constant` in the unchanged manuscript). Near-zero trial values are not
by themselves suspicious; this calculation does not assert that the
rounded trial is exactly that constant function.

Artifacts: `outputs/TRIAL_ENERGY_CERTIFICATE.json`,
`outputs/trial_congruence_Z40.csv`, and
`code/verify_trial_energy.py`.

## 4. Exact obstruction for every coefficient choice in this model

For the actual saved approximant `G64`, put

`S=N64−eta64 F64`, `rhs=K64−eta64 D`,

`M_G(C)=[A−rhs* C−C* rhs+C* S C]/eta64`.

This is the same quadratic model as

`Qhat(C) + Rhat(C)*Rhat(C)/eta64`.

The original FLOAT diagnostic did not certify this as an upper bound on
`B64=W*H64⁻¹W`, because `G64` is approximate. The new all-coefficient
certificate is likewise a statement about the model, not a lower bound
on the physical resolvent.

The exact replay proves `S >= mu I`, `mu=1/50000`, uniformly over the saved
Gram enclosures. It freezes dyadic vectors `x` and `y` from the one failed
model direction. If `b=rhs x` and `d=Sy−b`, completing the square gives

`inf_c [x*Ax−2c*b+c*Sc]/eta64`

`>= [x*Ax−2y*b+y*Sy]/eta64 − ||d||²/(eta64 mu)`.

Every scalar and radius on the right is enclosed by integer/rational
arithmetic. After dividing by the exact `x*x`, the lower bound is an exact
rational greater than `37/25`. For any matrix `C`, its vector `Cx` is one
candidate in this minimization, proving the all-`C` claim.

The scalar Gram uncertainty is about `3.415e−17`; the solve/rounding
correction is about `1.023e−17`. The stored upper-model failure is therefore
not an enclosure artifact or a coefficient-conditioning artifact.

Moreover, for every `tau>0`, the same fixed-template error-corrected model
satisfies

`Umodel−M_G = (tau/eta64) Rhat*Rhat`

`+ [nu sigma + (1+1/tau)sigma²/eta64] C*C >= 0`.

Consequently no choice of `C` or positive `tau` rescues that same fixed
`G64`, same-`eta64` template. A different estimator is not ruled out.

Artifacts: `outputs/MODEL_OBSTRUCTION_CERTIFICATE.json`, the exact
`model_obstruction_x40.csv`, `model_obstruction_y40.csv`,
`model_S_congruence_Z40.csv`, and
`code/verify_model_obstruction.py`.

## 5. Projection and complement diagnosis (FLOAT only)

One new saved-data analysis read the old saved `M`, rather than rebuilding
or rescreening the old full coefficient matrix. Let `x` be its unit top
model direction, `y` the corresponding 64-vector, and
`rhat=Wx−G64 y`. The ordinary Hilbert-space trial projection is
`Pi_V=V P⁻¹ V*`. The results are:

- saved-model value: `1.48262763806155`;
- signed `Qhat` contribution: `0.136900179799514`;
- total residual norm squared: `0.021020880599657`;
- trial-projected residual norm squared: `0.002305734455942`;
- orthogonal residual norm squared: `0.018715146143714`;
- trial residual divided by `eta64`: `0.147609904071914`;
- orthogonal residual divided by `eta64`: `1.198117554190121`.

The residual is 89.0312% off-trial by squared norm. In contrast, the
observation `Wx` itself has squared norm `0.195929418748626` and only about
`7.2644e−10` squared norm outside the trial span. The loss therefore cannot
be explained simply as failing to represent this observation vector.
The image under the approximate action creates the substantial component
that the trial span does not capture.

The floating generalized signed trial minimum is approximately
`1.5e−15` for `L`, or `0.0156250000000015` for `L+I/64`. The Galerkin model
`D*F64⁻¹D` has maximum approximately `0.992265133962373`. These two
positive-threshold observations are Schur-complement-equivalent statements
about the same restricted block, not two independent pieces of evidence
for positivity of the whole operator. With approximate `F64`, that
floating Galerkin number itself is not a certified physical resolvent bound.

For an **exact-action** inverse approximation, the ideal identity is

`M_exact(C)−B64 = R*(eta64⁻¹ I−H64⁻¹)R >= 0`.

This identifies the possible overestimate from using scalar coercivity in
place of actual residual resolvent geometry. It does not apply verbatim to
the uncorrected approximate-action model. Also, `V` need not be
`H64`-invariant: the off-trial 89.03% is **not** 89.03% of the true
resolvent error, whose cross terms need not vanish.

## 6. Exact unresolved certificate and one bounded next admission

The actual threshold question is the sign of `L+I/64` on the **whole**
minimum form domain. Since `H64>0`, it is equivalent to whether
`B64=W*H64⁻¹W <= I`. To decide it one needs either:

- a certified full 372-coordinate upper bound `B64<I`, proving that the
  old failure was only a certificate limitation; or
- a rigorously negative signed Rayleigh value for `L+I/64` on an admitted
  function, with a quantitatively verified smooth compact witness before
  any RH-negative interpretation.

A read-only inspection of the **already saved** model eigenvalues gives four
values above 1:

`1.0862756147941655`, `1.1470818326101900`,
`1.4564715772268324`, `1.4826276380615548`.

No new eigensolve was used for this readout. These are FLOAT diagnostics.
For an exact fixed-eta quadratic model with positive enlarged normal matrix,
adding `k` trial directions reduces the optimized model by a positive
semidefinite Schur-complement term of rank at most `k`. Interlacing therefore
requires at least as many new directions as there are old eigenvalues above
1. The saved numbers indicate **at least four**, not one. That rank count
still needs exact certification before it is used as a theorem. A rank-one
experiment must not be sold as a possible full pass for this same template.

The proposed **single next task is a bounded admission test** for one fixed
four-mode residual block. It is not yet authorization for four new actions,
a broad rank sweep, or another unchanged 64-column run.

**The admission test should do exactly this:**

1. Using only the saved matrices, freeze dyadic representatives of the four
   failing model modes and certify their four-dimensional obstruction if
   affordable. The existing one-direction certificate proves failure, but
   does not by itself certify the count four.
2. For each frozen mode `x_j` and its frozen 64-vector `y_j`, define the
   prescribed analytic whole-line residual surrogate
   
   `q_j = W x_j − (G0_an − 3V/64)y_j`,
   
   where the source release's analytic surrogate is exactly
   `U G0_an = b Z` (manuscript discussion after `g0definition`). Retain its
   inherited transfer bound to `G0`. Prove the new functions belong to the
   same minimum operator domain; do not use the discontinuously truncated
   `G0` itself as a domain-admitted new trial.
3. Certify the residual block's independence from the old span and from
   itself, and establish a lower bound on its smallest new Gram eigenvalue.
   One plausible scalar gate is that the projected residual-block Gram is
   at least one tenth of its full Gram, but it must be certified; the
   single-mode 89.03% diagnostic is not a four-mode certificate.
4. Before physical production, check that the fixed analytic producer
   supports these higher-frequency functions, justify all index/tail
   bounds, and forecast a complete fixed-block run within a preapproved
   hard wall/CPU/memory budget. The old producer is not assumed to support
   the new functions automatically.

**Admission / KILL:** admit only if the fixed block is domain-valid,
nonredundant, and supported by a credible bounded production plan. If these
checks fail, or provide no credible route to a closing certificate, **HOLD**
this approach and report the exact obstruction. Do not silently add modes,
expand precision, change the source, or sweep ranks. No part of this next
admission or physical experiment was performed in this report.

If admitted later, a single fixed-block production would have two genuinely
discriminating outcomes:

- A certified full-372 bound `B64<I` shows that the old failure was a
  limitation of its family/estimator at this threshold.
- A strictly negative outward signed Rayleigh upper bound for `L+I/64`
  shows an actual threshold obstruction on an admitted function. Produce
  and verify a smooth compact cutoff retaining strict negativity before
  any compact-witness or RH-negative claim.

If neither certificate closes, the outcome remains **OPEN**. Four modes
are a necessary-rank diagnostic for the old template, not a guarantee that
four new trials are sufficient. The admission task supplies the evidence
needed to decide whether even that one bounded production is worth doing.

## 7. Resources, provenance, and limitations

The three bounded producer cores recorded, respectively:

- projection diagnosis: `0.328 s` wall, `0.324 s` CPU, `55000 KiB` peak RSS;
- restricted energy certificate: `0.292 s` wall, `0.288 s` CPU,
  `38964 KiB` peak RSS;
- model obstruction certificate: `0.445 s` wall, `0.443 s` CPU,
  `99572 KiB` peak RSS.

Each used 30-second CPU/wall and 512-MiB address-space guards with one BLAS
thread. These are internal computational-core ledgers, not total editing,
inspection, copying, packaging, or external tool wall times. The first
analysis used four finite eigensolves (including reading out the saved
372-dimensional top direction), four linear solves, and one Cholesky
factorization. The model-certificate proposal used one further 64-dimensional
saved-matrix eigensolve. Exact acceptance and the independent replays use
no eigensolve or linear solve.

Across all work: zero new `H` actions, zero new source evaluations, zero
FFTs, zero new physical Gram integrals, zero trial changes, zero rank
changes, and no rerun of the old full-coefficient screen. The scripts do not
import action-generation or physical-integration modules.

The two exact claims were independently replayed from integer witnesses and
source inputs by a separate arithmetic implementation. The portable replays
also passed once each. Their wall times are recorded; CPU time and peak RSS
were not captured for those separate replay runs and are not inferred.
They retained the 30-second and 512-MiB guards. This means separate
arithmetic checking, not external peer review or formal proof-kernel
verification. The inherited source/domain/whole-line numerical inclusion
premises were not regenerated.

The separate weighted-Weil bridge audit supplies an equivalence argument,
not a positivity proof. It is not external formal verification. This report
provides no fully certified compact negative witness, no all-negative
spectral exclusion, and no RH proof or disproof. The released delta32 theorem
and all its premises remain unchanged.

## License

Author-original research, analysis, code, and documentation: Creative Commons
Attribution-NonCommercial 4.0 International (CC BY-NC 4.0),
https://creativecommons.org/licenses/by-nc/4.0/ . See `LICENSE`.
Third-party material retains its original rights and applicable terms.
