# Theta–prime cancellation and limits of real-zero positivity criteria

This directory contains analytic proof and reproducibility material for the manuscript of the same title. It isolates three results about explicitly defined exterior functionals built from the actual von Mangoldt weights and a rapidly decaying theta source.

## Mathematical scope

1. **T1 Full-$L^2$ cancellation.** The continuous prime-density contribution cancels an exponential term exactly. The remaining Stieltjes kernel contains an essential lower-boundary term. The input function needs neither a derivative nor a boundary trace.
2. **T2 Fixed-order absolute bounds.** For each separately fixed theta-derivative order $j$, the arithmetic kernel has an unconditional $L^2$ bound of order $|\kappa^{(j)}(R)|e^{-R}(1+R)$. The archimedean kernel has an upper bound of order $|\kappa^{(j)}(R)|e^{-R}$. No uniformity for $j$ growing with $R$ is asserted.
3. **T3 Failure of a relative-positivity implication.** For every prescribed finite differentiability order, there are nonnegative, full-support splines with real-zero Fourier transforms and the stated normalization whose arithmetic-to-archimedean ratio is $-M^3(1+o(1))$ along $R=\log M$, $6\mid M$. The construction uses the actual prime weights and chooses a finite spline at each radius.

These statements are not a proof or disproof of the Riemann hypothesis. The splines are not asserted to be eigenfunctions or minimizers, and no sign conclusion for an actual ground eigenvalue follows. T3 refutes the proposed relative estimate on its explicitly defined test class, not a ground-specific theorem. No priority or novelty claim is made.

## Files

- [PROOFS.md](PROOFS.md) contains definitions, complete T1–T3 proofs, supporting lemmas, limitations, and contextual bibliography.
- [REPRODUCIBILITY.md](REPRODUCIBILITY.md) specifies the mathematical objects, conventions, assumptions, constant dependencies, order of limits, and finite-diagonal choice.
- [MANIFEST.sha256](MANIFEST.sha256) identifies the exact bytes of these three Markdown files by SHA-256.

The mathematical reproduction is analytic, not numerical. No numerical data set, simulation, benchmark, executable theorem checker, formal proof certificate, or computed value of the diagonal spline order is supplied or claimed. A checksum verifies file identity, not a theorem.

## How to read and reproduce the arguments

Start with the definitions in PROOFS.md, keeping the Fourier sign and strict prime cutoff unchanged. Check T1 before using its kernels on arbitrary $L^2$ functions. For T2, fix $j$ before selecting the large-$R$ threshold. For T3, fix each composite integer $M$ before taking the spline order to infinity, then select a sufficiently large finite order satisfying both stated error tolerances.

The bibliography records context for the theta kernel, real-zero questions, spline constructions, and prime-error estimates. None of those works' variational or numerical claims is used as a proof premise. The arguments do not assume the Riemann hypothesis or a prime-number theorem.

This directory contains the support material only, not a TeX source or PDF edition of the manuscript.
