# Constant mode margin advisory

The exact replay proves c > 127/64, conditional on identified inherited source and phase enclosure inputs. The analytic identity then forces lambda_max(B_1/64) > 127/128 > 99/100. Reusing the old 0.99 upper target at delta64 is impossible under those premises; B < I remains undecided.

Read ADVISORY.md for the proof, equality and domain conditions, source-premise boundaries, and the separate fixed-cover estimator threshold.

Run:

    python code/verify_constant_mode.py --emit

To bind selected inputs against the unchanged original release as well:

    python code/verify_constant_mode.py --bind-sources --emit

No third-party Python dependencies are required. No H actions, new phase arrays, source evaluations, FFTs, physical Gram integrals, or eigensolves occur. The replay is exact rational arithmetic. CC BY-NC 4.0 applies to new material; reused sources retain their original terms.
