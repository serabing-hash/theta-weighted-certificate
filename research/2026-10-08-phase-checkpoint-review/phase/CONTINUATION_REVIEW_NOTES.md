# Review-only continuation package

Nothing here authorizes execution. No approval record or continuation marker
has been created. An explicit execution decision and actual-executor preflight
must precede one continuation. Do not run the original v2_worker.py or shared().

## Proposed installation layout

In the restored v2_j2_local_20261008 root, add exactly these new code files:

- code/v2_action_phase_repair.py from v2_action_PHASE_REPAIR_REVIEW_ONLY.py
- code/v2_checkpoint_continue.py from v2_checkpoint_continue_REVIEW_ONLY.py

Keep all original code, pilot/, supervisor/, static/ and PILOT_SINGLE_USE.json
byte-identical. Restore the four original input archives and inherited trees
according to the archived dependency/restoration record. The new entrypoint
checks the original91source bindings and extracted bytes. Missing data means
HOLD; it does not authorize substituting another source or executor.

New numerical output and copied accepted caches go only to continuation_01/.
CONTINUATION_SINGLE_USE.json is a new exclusive marker bound to the old attempt
and the explicit approval record. A second continuation is blocked.

## Required actual-executor preflight records

The adapter deliberately refuses to start without all of the following:

1. A review/approval JSON with status PASS-PHASE-REPAIR-STATIC-ENTRY and exact
   scope ONE_CHECKPOINT_CONTINUATION_J2_THROUGH_437_KERNELS. That scope must
   be separately authorized; this string is not itself user permission.
2. Hashes of the two new code files, unchanged old PILOT_STATUS and supervisor
   record, and the full runtime-identity manifest.
3. A runtime manifest with status FULL_RECOGNIZED_RUNTIME_IDENTITY_VERIFIED,
   recognized-install/official-source evidence, native dependency closure
   verification, actual runtime_root, tree_roots, flint_module_relative_path,
   and all files' relative paths, bytes and SHA256. This must cover executed
   extension modules and bundled FLINT/GMP/MPFR dependencies, not only __init__.
   The entrypoint rechecks every byte and exact tree coverage before import.
4. A hash-bound actual-executor generic fixture record with status
   PASS_NATIVE_GENERIC_PHASE_FIXTURE, final phase-code/support/runtime hashes,
   precision160, coordinate denominator140, at least4 exact generic unit roots,
   full-error roundtrip success, source_evaluations0 and
   actual_phase_cache_generated=false. No real prime-phase cache may be created
   during preflight.

The validation function in the adapter is the authoritative schema. These
records must report real checks; do not populate pass fields speculatively.

## Single guarded entrypoint after explicit approval

python code/v2_checkpoint_continue.py --root RESTORED_ROOT --approval-record REVIEWED_APPROVAL_JSON

This instruction is included for review; it has not been executed. The adapter
starts its wall clock before validation, enforces TERM564/KILL574, applies
512MiBAS and cooperative500MiBRSS, sets a conservative integer childCPU cap of
at most573s, and monitors supervisor+workerCPU. Prior active wall25.474366778s
andCPU25.447845s are retained. A measured aggregate over600s produces HOLD and
nonzero exit even if the worker returned0. OS signal/accounting granularity is
recorded, not concealed as an exact scheduling theorem.

Gamma extension generation is absent from the continuation call path. The saved
extension, oldGamma-only nodes and frame values are checked and copied. The
producer then runs only the fixed j=2 D/action/oneDFT/437-kernel path with all
original measured gates. Original integer saved verification is redirected to
continuation_01, so the prior saved verification cannot be overwritten.

The supervisor's CONTINUATION_FINAL_STATUS.json is the authoritative completion
status. Worker success alone is insufficient. A successful bounded continuation
still awaits external saved-certificate review and does not authorize the other
three columns, enlarged consumer, or any RH assertion.
