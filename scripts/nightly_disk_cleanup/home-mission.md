Run $home-disk-cleanup on this home server now. Read
/home/aelaguiz/.agents/skills/home-disk-cleanup/SKILL.md and its host storage
reference. Amir explicitly requested nightly cleanup of root and the /mnt
drives, including obsolete RustAI training/test policy clutter.

Use current metadata, catalog references and process/open-file activity to
choose eligible cleanup. Preserve useful retained policies and active work.
Inspect policy metadata only; never read, hash or expand policy payloads.
Measure /, /mnt/p2 and /mnt/p3 separately and verify mount identities.
This is an authorized cleanup run, not just an audit. Complete useful recurring
retention even above the headroom target. Use bounded, narrow probes and avoid
repeating whole-volume scans. Approximately 5 to 10 minutes is expected; an
outer deadline stops this run after 20 minutes.

Run directly without child agents, external model sessions, model switching,
service restarts, scheduler edits, source commits or external messages. The
selected model is GPT-5.6 Sol at medium, deliberately chosen for this task.

Reserve the final three minutes of the deadline for verification and report
writing; stop new discovery in that window.

Save actions.jsonl and summary.json in DISK_CLEANUP_RUN_DIR. The summary must
have host: "home", status: "ok", "warning" or "failed", and volumes: a list
of objects with path, before_free_bytes, after_free_bytes, net_reclaimed_bytes
(all byte values are integers; net is after minus before). Include actions,
deferred owners, missing mounts and checks. Use warning for incomplete coverage
or unresolved pressure; failed when cleanup/verification could not execute.
Return a concise final report of actual results. The launcher saves final.md.
Verify affected processes and source status and reap task-owned helpers before
finishing. Keep completed run reports for 14 days.
