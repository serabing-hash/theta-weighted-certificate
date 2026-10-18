# Conditional lifecycle argument and limits

## Scope and premises

Production consists of the trusted external host, observer, controller and one scientific worker. Each of the first three invokes `fork_one` exactly once; the leaf never creates a child. Byte-bound source admission is inherited unchanged from packet30. The host explicitly hashes and compiles only the lifecycle module in addition to its own bound source; it never imports the scientific modules.

The argument assumes correct Linux/CPython primitives and the reviewed, non-adversarial control/runtime behavior. The short pre-seal stubs do only prescribed control work. There is no hidden at-fork callback, competing waiter, namespace/credential mutation, affinity mutation, or hostile native code that changes the signal/control state. All UID fields must equal the same nonzero real UID; capability sets must be zero and inherited NoNewPrivs must be one. These are gates, not settings that this packet tries to repair. Python audit hooks remain supplemental observations/rejections, not a native sandbox.

## Birth and identity

`fork_one` creates two private pipes, forks once, and immediately seals the parent with `(RLIMIT_NPROC.soft, hard)=(0,0)`. Its child inherited the pre-seal limit and remains in the reviewed child stub. The stub installs and reads back PDEATHSIG, verifies its original parent, applies leaf limits if applicable, sends PID/PPid/start-time readiness, and blocks awaiting a release token. The parent holds its own unreaped PID, opens pidfd, binds procfs identity, reads and compares the readiness record, and samples again before release.

Inductively, the host's only admitted birth is the observer, the observer's only admitted birth is the controller, and the controller's only admitted birth is the worker. Kernel NPROC enforcement forbids later processes and threads for these unprivileged sealed callers. The still-unsealed next role can make only its prescribed single birth under the reviewed-source premise. No native scientific runtime is loaded in that window. This is the basis for historical completeness; PPid snapshots are not used as a census.

An own child cannot have its PID recycled while retained unreaped with SIGCHLD DFL and no other waiter. `Child` forbids numeric PID reads after its `wait4` succeeds. The observer is not the worker's reaper: its remote samples therefore test pidfd termination both before and after procfs/prlimit reads, discarding the entire sample if termination occurs. An unchanged start time alone is not claimed to rule out arbitrary PID reuse.

## Closure and failure

Each owner waits for its exact registered child. The observer and external host are subreapers. Normal success requires exit code zero, final registered-child receipt bindings, and `wait4(-1, WNOHANG|__WALL)` reporting ECHILD. A zero return means a live/nonwaitable child remains and is HOLD. An unexpected returned PID is HOLD even though that wait reaped it. Other errors, unsupported syscalls, failed identity reads, extra threads, privilege/affinity changes and unexpected reparenting are HOLD.

When a registered parent dies, PDEATHSIG terminates its direct child; the nearest surviving subreaper can collect descendants. Failure cleanup kills only registered identities and drains adopted children within the original deadline. It never extends a budget or converts failure into success. If cleanup cannot complete, its outcome is explicitly unclosed/uncertain, and no acceptance record is issued. Kernel scheduling and signal delivery are not asserted to have zero latency.

Final ECHILD is a current-state fact. It cannot reveal an arbitrary historical child already reaped by its creator. Historical completeness additionally uses the fixed-birth/zero-NPROC/source premises above. Unexpected escaped ancestry or malicious native behavior outside those premises is not certified.

## Time, memory and source boundaries

The science host's interval starts before the first fork. All child startup, handshakes, byte admission, native/scientific work, serialization, fsync, checker, controller/observer finalization, actual waits and final ECHILD precede its endpoint. All roles inherit one CPU before creation; under the fixed-tree premise the elapsed capacity bounds aggregate CPU in this interval. Diagnostic wait4 usage is not summed with recursive child usage. Existing 60-second, 384-MiB worker AS and 320-MiB observed RSS/HWM gates are unchanged.

Only immutable external audit follows the endpoint. The actual final tool exit must still confirm completion of that receipt writer. A tool call's `wall_time_seconds` remains an output-wait duration, not the full-run timing witness. The original source bootstrap's BEGIN/exclusive-directory ordering is byte-identical. New host reservation and new attempt paths do not reset or reuse the failed launch.

## Primary references

- [Linux getrlimit](https://man7.org/linux/man-pages/man2/getrlimit.2.html): NPROC counts real-UID processes/threads, hard-limit behavior and privilege exceptions.
- [Linux pidfd_open](https://man7.org/linux/man-pages/man2/pidfd_open.2.html): unreaped own-child PID retention conditions and stable descriptors.
- [Linux wait](https://man7.org/linux/man-pages/man2/wait.2.html): WNOHANG, ECHILD, zombie retention and __WALL.
- [Linux subreaper](https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html): orphan adoption; the setting is not inherited automatically by fork.
- [CPython 3.12.14 PyOS_setsig](https://github.com/python/cpython/blob/v3.12.14/Python/pylifecycle.c#L2975): the sigaction branch replaces flags with SA_ONSTACK, excluding SA_NOCLDWAIT.
- [Python audit hooks](https://docs.python.org/3.12/library/sys.html#sys.addaudithook): Python-level audit hooks are not a security sandbox.

Reading these specifications and parsing source does not establish actual syscall support in this environment. That is the purpose of the separately directed one-bundle fixture.
