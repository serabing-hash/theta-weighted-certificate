#!/bin/sh
# Invoke ONCE. Internal RLIMIT_AS is 768 MiB and SIGALRM is 290 seconds.
# timeout enforces an additional 295-second wall limit, then SIGKILL after 1 s.
set -eu
case "$0" in
  /*) task_dir=${0%/*} ;;
  *) task_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) ;;
esac
exec /usr/bin/timeout --signal=TERM --kill-after=1s 295s \
  python3 -u "$task_dir/certify_tail.py" "$task_dir/input.json" "$task_dir/run"
