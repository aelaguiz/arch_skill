Run $home-disk-cleanup on this home server now as its nightly cleanup. Read
/home/aelaguiz/.agents/skills/home-disk-cleanup/SKILL.md, the disk-cleanup skill
it builds on (/home/aelaguiz/.agents/skills/disk-cleanup/SKILL.md) and the
references they point to before the first deletion. Amir authorized this
recurring cleanup of the main disk and the /mnt data drives, including old
RustAI and PS Mobile checkouts (unsaved work salvaged first) and the bulk of
finished experiments and training runs. This is a cleanup run, not an audit.

Find what is alive first: one sudo -n process snapshot matched against every
large candidate, plus the other use checks the skill describes. Name the live
work in the report. Then clear what is dead, largest first, and re-decide every
large folder from what you see tonight; earlier runs' deferred lists are not
decisions. Keep root above about 150 GB free and each data drive above about a
tenth free, and keep clearing dead things after those numbers are met. Never
read, hash, expand or fetch policy payloads. Measure /, /mnt/p1 and /mnt/p2
separately and confirm each mount's identity; /mnt/p3 is offline on purpose.

The launcher stops this run at its deadline. Reserve the last few minutes for
verification and the report, and stop new discovery then. Work directly: no
child agents, external model sessions, model switching, service restarts,
scheduler or skill edits, or external messages. The only commits are the
skill's salvage commits, pushed with [skip ci].

Save actions.jsonl and summary.json in DISK_CLEANUP_RUN_DIR. The summary must
have host: "home", status: "ok", "warning" or "failed", and volumes: a list
of objects with path, before_free_bytes, after_free_bytes, net_reclaimed_bytes
(all byte values are integers; net is after minus before). Include the live
work you found, actions, what you kept among the largest owners and why,
missing mounts and checks. Use warning for incomplete coverage or unresolved
pressure; failed when cleanup or verification could not execute. Return a
concise final report of actual results; the launcher saves it as final.md.
Verify affected processes and source status and reap task-owned helpers before
finishing. Keep completed run reports for 14 days.
