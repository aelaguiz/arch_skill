Run $disk-cleanup as the authorized nightly maintainer on amirs-m3-36gb.
Read /Users/aelaguiz/.agents/skills/disk-cleanup/SKILL.md and its references.
Verify user aelaguiz, home /Users/aelaguiz and short hostname Amir-M3-36gb.
Amir requested this recurring cleanup after the Mac Studio cleanup. Remove
verified disposable developer buildup: inactive generated build/dependency
output, old caches/logs and clean inactive worktrees only when source changes
and Git commits are retained under the skill's rules. Preserve canonical
checkouts, dirty/unique data, active work, credentials, model stores and device
state. Do not stop active simulators, physical devices or unrelated processes.
Never load, hash, expand or fetch RustAI policy payloads for disk inspection.

Target 150 GB available on /System/Volumes/Data. Check recurring retention
above target too: remove old rotated diagnostic logs and recognized timestamped
AIM backup snapshots older than seven days, retaining current/recent/open files
and never printing credential values. Compact eligible append-written text
logs over 128 MiB to a 4 MiB recent tail. Use supported rotation for other
writers. Keep completed cleanup reports for 14 days. Use narrow probes, saved
inventories and actual available bytes; APFS directory totals are not reclaimed
space. Bound unfamiliar probes to 45 seconds, narrow on timeout, and finish
useful routine work instead of repeatedly scanning the whole filesystem.

Run directly on GPT-5.6 Sol medium. Do not spawn children or external model
sessions, change models, edit the schedule/skill, commit source changes, send
messages or invoke interactive sudo. The scheduler stops this run after
20 minutes; approximately 5 to 10 minutes is expected. Reserve the final three
minutes for verification and report writing; stop new discovery in that window.

Save actions.jsonl and summary.json into DISK_CLEANUP_RUN_DIR. The summary must
have host: "amirs-m3-36gb", status: "ok", "warning" or "failed", and volumes: a
list containing /System/Volumes/Data with path, before_free_bytes,
after_free_bytes and net_reclaimed_bytes, all byte values integers and net
equal to after minus before. Also record actions, deferred owners and checks.
Use warning for remaining pressure or material incomplete coverage. Return a
concise final report, which the launcher saves as final.md. Verify affected
source/service/device state and reap task-owned helpers before finishing.
