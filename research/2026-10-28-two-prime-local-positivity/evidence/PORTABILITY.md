# Portable saved witness check

The original saved-data arithmetic checker had SHA256
071c2f154233aeeb80f41564de4401506c702f11f3f0438a29f919e9cfe680b4.
The public adaptation changes only the initialization/provenance header:
it locates the producer and witness beside the checker and verifies their
frozen hashes. Private operational receipts and private analytic-note path
checks are not public dependencies. From `count=0` through the end of the
file, the mathematical body is byte-identical to the original checker.
A direct byte comparison confirmed that identity. The portable variant
was run successfully on the saved witness; the producer was not imported
or executed. The report is included beside the checker.

This fresh check includes its own interval LDL and rational congruence
Gershgorin certificate, not merely a rereading of saved positive pivots.
It does not repeat source-function evaluations or establish the analytic
form-domain and infinite-tail arguments. Those belong to the manuscript
and the frozen producer trust boundary.
