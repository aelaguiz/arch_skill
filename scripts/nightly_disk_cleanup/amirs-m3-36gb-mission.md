Run $disk-cleanup as the authorized nightly maintainer on amirs-m3-36gb. Read
/Users/aelaguiz/.agents/skills/disk-cleanup/SKILL.md and the references it
points to before the first deletion. Verify user aelaguiz, home
/Users/aelaguiz and short hostname Amir-M3-36gb. Amir authorized recurring cleanup of
this machine: old task checkouts (unsaved work salvaged first), finished
task output and experiments' bulk, unused builds, caches, task simulators,
emulators and VMs, inactive Prime state and the Time Machine local snapshots
the backup drive already has. This is a cleanup run, not an audit.

Find what is alive first: one process snapshot matched against every large
candidate, plus the other use checks the skill describes. Name the live work
in the report. Then clear what is dead, largest first, and re-decide every
large folder from what you see tonight; earlier runs' deferred lists are not
decisions. Keep about 150 GB available on /System/Volumes/Data, and keep
clearing dead things after that is met. Routine retention: remove rotated
diagnostic logs and timestamped AIM backup snapshots older than seven days
without reading their contents, cut append-written text logs over 128 MiB to
their last 4 MiB, and keep completed cleanup reports for 14 days. Never load,
hash, expand or fetch RustAI multiplayer policy payloads.

The scheduler stops this run at its deadline. Reserve the last few minutes for
verification and the report, and stop new discovery then. Work directly: no
child agents, external model sessions, model switching, schedule or skill
edits, interactive sudo, or messages. The only commits are the skill's salvage
commits, pushed with [skip ci].

Save actions.jsonl and summary.json into DISK_CLEANUP_RUN_DIR. The summary must
have host: "amirs-m3-36gb", status: "ok", "warning" or "failed", and volumes: a
list containing /System/Volumes/Data with path, before_free_bytes,
after_free_bytes and net_reclaimed_bytes, all byte values integers and net
equal to after minus before. Also record the live work you found, actions,
what you kept among the largest owners and why, and checks. Use warning for
remaining pressure or material incomplete coverage. Return a concise final
report, which the launcher saves as final.md. Verify affected source, service
and device state and reap task-owned helpers before finishing.
