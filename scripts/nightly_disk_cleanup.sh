#!/usr/bin/env bash
set -euo pipefail
umask 077

# Native launchd/systemd owns the schedule. The selected skill owns cleanup.
# Arguments are the report host label, expected short hostname, and mission file.
JOB_HOST="$1"
EXPECTED_MACHINE="$2"
MISSION_FILE="$3"
export PATH="${HOME}/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
STATE_DIR="${HOME}/.local/state/disk-cleanup"
mkdir -p "${STATE_DIR}/runs"
RUN_DIR="$(mktemp -d "${STATE_DIR}/runs/$(date -u +%Y%m%dT%H%M%SZ).XXXXXX")"
export DISK_CLEANUP_RUN_DIR="${RUN_DIR}" DISK_CLEANUP_HOST_LABEL="${JOB_HOST}"
ln -sfn "${RUN_DIR}" "${STATE_DIR}/latest"
date -u +%FT%TZ > "${RUN_DIR}/started-at"

status=0
if [[ "$(hostname -s)" != "${EXPECTED_MACHINE}" ]]; then
  echo 'Hostname does not match the scheduled cleanup target.' > "${RUN_DIR}/error.log"
  status=64
else
  if [[ "$(uname -s)" == Darwin ]]; then TIMEOUT=/opt/homebrew/bin/gtimeout; else TIMEOUT=/usr/bin/timeout; fi
  stop_run() {
    trap '' TERM INT
    kill -TERM "${run_pid}" 2>/dev/null || true
    wait "${run_pid}" 2>/dev/null || true
    printf '143\n' > "${RUN_DIR}/exit-code"
    date -u +%FT%TZ > "${RUN_DIR}/finished-at"
    exit 143
  }
  "${TIMEOUT}" --signal=TERM --kill-after=30s 20m \
    "${HOME}/.local/bin/aim" codex run -- exec \
    --model gpt-5.6-sol -c 'model_reasoning_effort="medium"' -c 'features.computer_use=false' \
    --dangerously-bypass-approvals-and-sandbox --ephemeral \
    --skip-git-repo-check --cd "${STATE_DIR}" --json \
    --output-last-message "${RUN_DIR}/final.md" - \
    < "${MISSION_FILE}" > "${RUN_DIR}/events.jsonl" 2> "${RUN_DIR}/error.log" &
  run_pid=$!
  trap stop_run TERM INT
  wait "${run_pid}" || status=$?
  trap - TERM INT
fi

if [[ "${status}" -eq 0 ]]; then
  python3 - "${RUN_DIR}" "${JOB_HOST}" <<'PY' || status=$?
import json, pathlib, sys
p = pathlib.Path(sys.argv[1])
assert (p / 'final.md').stat().st_size > 0, 'Missing final report'
s = json.loads((p / 'summary.json').read_text())
assert s['host'] == sys.argv[2], 'Wrong report host'
assert s['status'] in ('ok', 'warning'), 'Cleanup did not complete'
assert s['volumes'], 'Missing volume measurements'
for volume in s['volumes']:
    assert volume['path'], 'Missing volume path'
    for key in ('before_free_bytes', 'after_free_bytes', 'net_reclaimed_bytes'):
        assert type(volume[key]) is int, 'Invalid byte measurement: ' + key
    assert volume['net_reclaimed_bytes'] == volume['after_free_bytes'] - volume['before_free_bytes']
PY
fi
printf '%s\n' "${status}" > "${RUN_DIR}/exit-code"
date -u +%FT%TZ > "${RUN_DIR}/finished-at"
printf 'Disk cleanup host=%s exit=%s report=%s\n' "${JOB_HOST}" "${status}" "${RUN_DIR}"
exit "${status}"
