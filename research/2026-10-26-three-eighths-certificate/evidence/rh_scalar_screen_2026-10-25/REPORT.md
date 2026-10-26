# One bounded scalar screen — completed

**Only R=1, weighted q=1/2, a0=0 passes the1024-cell cap: its certified sufficient count is552.** This is a cell-count candidate only, not a residual-sign certificate or evidence that the second eigenvalue has the required sign.

Exactly one approved numerical process was executed, after independent static review. It completed normally (exit0), reporting0.1773s wall,0.2553s process CPU (including same-PID setup), and10,240KiB peak resident memory. Pre-exec limits were59s hard wall alarm,59s CPU, and256MiB address space. No child processes, retries, matrices, quadrature, residual rows, or eigenvalues were used. Full outward-rounded bounds are in `output.json`; decimals below are display summaries only.

## Admission and sufficient cell counts

All six Hardy inequalities pass. The interface threshold is epsilon/2=1/16. Counts are exact ceilings of the displayed sufficient recipe, certified by agreement of both interval endpoints; they are **not necessary lower bounds for all possible methods**.

| R | Interface etabar, approximate | Admission | Baseline a0=0 | Baseline a0=1 | Weighted a0=0 | Weighted a0=1 | Active prime powers |
|---|---:|---|---:|---:|---:|---:|---:|
|3/4|12.4461|Not admitted|—|—|—|—|Not evaluated|
|1|0.00823814|Admitted|2,088|5,675|**552: cap pass**|1,499|5|
|5/4|2.63419e-8|Admitted|18,686|50,793|2,610|7,095|8|
|3/2|1.27955e-17|Admitted|300,059|815,644|22,423|60,952|12|
|7/4|3.14765e-33|Admitted|9,224,216|25,074,017|350,069|951,584|18|
|2|3.23158e-59|Admitted|504,198,609|1,370,553,917|10,541,961|28,656,019|24|

Every evaluated count except552 exceeds1024. No frozen-precision comparison or ceiling is unresolved. Nonadmission at R3/4 means this sufficient bridge does not license that row; it is not a disproof of its underlying spectral claim. Cap failures reject this bound-based recipe within the declared budget, not every possible certificate.

## The552-cell candidate and the corrected floor

At R1, L3/4, the stronger target has t0=epsilon-etabar approximately0.11676185873758226. Actual finite sums give beta_R approximately3.41636325391068 and beta_L approximately1.96111583434608. The finite-radius weighted bound is Khat approximately2.08471964467036; no asymptotic replacement was used.

With a0=0, the retained metric gives **a_star=t0*m0/2 approximately0.03417647168812305>0**. The a0=1 option has a_star approximately1.03417647168812305 but raises the sufficient count from552 to1499. Thus removing the artificial positive-a0 restriction genuinely changes this cap decision. The smaller floor can worsen coarse residual-error constants through sqrt(2R/a_star); smaller cell count need not mean cheaper total certification. The actual alpha(x), not this coarse floor, must remain in any future weighted Gram integral.

The baseline a0=0 option likewise remains coercive because q0 retains the full positive metric, giving a_star=t0*m0. It is a conservative cell-count comparison, not deletion of the metric from the form.

## Scope and unresolved mathematics

The result removes **one cell-count obstacle for one fixed epsilon=1/8 candidate**. It does not determine a useful complement trial dimension, conditioning, approximation budget, signed second residual eigenvalue, or total solver cost. None was evaluated. The decisive signed control of the actual joint Gamma–prime residual form remains unproved. RH through this bridge would additionally require suitable full-domain signs along an epsilon-to-zero sequence.

No automatic residual construction, larger screen, parameter search, or new numerical run follows from this result. Source, rounding/tail argument, output, guards, logs, and static review are preserved in this directory; the two original gate/review documents remain unchanged.
