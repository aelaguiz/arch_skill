---
name: home-disk-cleanup
description: "Free disk space on Amir's Linux home server: its main disk and its data drives (/mnt/p1, /mnt/p2), where RustAI checkouts, training runs, policies, experiment rounds and QA stacks pile up. Use for its nightly cleanup, a full root or data drive there, or old RustAI checkouts and finished experiments on home. Applies $disk-cleanup's judgment with this machine's map. Use disk-cleanup for the Macs and mac-studio-disk-cleanup for the Mac Studio."
metadata:
  short-description: "Clean the home server's main disk and RustAI data drives"
---

# Home Server Disk Cleanup

This is SSH host `home`: Linux machine `amir-server`, user `aelaguiz`, home `/home/aelaguiz`. It is the biggest machine. RustAI training, experiments, solver runs and long batches run here, and Play vs AI and the QA stacks serve from it. So it fills faster than any Mac, and nothing on it is backed up: a deletion here is final.

Read [$disk-cleanup](../disk-cleanup/SKILL.md) first. Its judgment is the judgment here: almost everything on this disk is left over from finished work, so you find what is alive and clear the rest. Its [checking-use.md](../disk-cleanup/references/checking-use.md) has the commands, and on this machine you run them with `sudo -n` so the snapshot covers every user. [host-storage.md](references/host-storage.md) is this machine's map.

## What is on this machine

The live work at any time is a handful of things:

- Amir's own `~/workspace/rustai` checkout, with his sessions in it;
- the agents' RustAI checkout `~/workspace/rustai-agents` and its policy store `/mnt/p2/rustai-agents`;
- the Play vs AI and Sit & Go servers;
- whatever QA stack, experiment round or training run is running now.

The snapshot shows them in a minute. Name them before deleting anything.

Everything else falls into three kinds:

- **Task checkouts.** RustAI and PS Mobile task checkouts under `~/workspace`, `~/workspace/rustai-worktrees` and `/mnt/p2`. They are task copies under the same salvage-then-delete procedure as on the Macs.
- **Experiment and run output.** Rounds under `/mnt/p2/ms12`, Sit & Go runs, curriculum runs, challenge stores, archives, and `rebel-*` work on `/mnt/p1`. When nothing runs an experiment and nothing has been written in it for days, it keeps its readings, manifests and reports and loses its bulk: checkpoints, policies of finished runs, captures and generated data. A finished smoke, sanity or failed run loses all of its policies. The newest candidates of a live project, and the baseline current work compares against, stay with that project.
- **Copies that regenerate.** Cargo `target/debug` and `target/release`, Flutter builds, `/mnt/p2/machines-run-mirror` (`machines run` copies Mac folders there and copies them again on its next run), caches and rotated logs.

## What stays here

- **What serves players**, and the policy folders it reads. The agents' store `/mnt/p2/rustai-agents` is linked from `~/workspace/rustai-agents` through `policies`, `policies_blueprint`, `runs/policies` and `artifacts/cardabs`. Those four links mark what Play vs AI and Sit & Go need. Other folders inside that store are experiments like any other.
- **Whatever a live checkout links to.** Amir's `rustai` links its `policies` and `policies_blueprint` into `/mnt/p2`, so those targets stay while it does.
- **Every policy catalog entry.** Resolve each `config/catalog.toml` entry through its links before calling a policy unreferenced.
- **Live databases and service volumes**, Docker's persistent data, and credentials.
- **Amir's personal files**, such as `~/Games` and recordings like a `dictation_*.wav`.

Never read, hash, expand or fetch policy payloads to decide anything. Never aim a deletion at a mount, `~/workspace` or the home folder.

## Each run

1. Confirm the host and each mount: `findmnt --target <path> -n -o TARGET,UUID,FSTYPE` should return the identities in the map. If a data drive is missing, skip it and say so. Never clean the folder underneath a missing mount.
2. Measure free space on `/`, `/mnt/p1` and `/mnt/p2`. Space freed on a data drive doesn't count toward root. Keep about 150 GB free on root and about a tenth of each data drive.
3. Run one size pass with newest-file times over `~` and each data drive, and save it.
4. Take one `sudo -n` process snapshot, and check services, containers, cron and links for all the large candidates at once.
5. Name the live work. Delete dead clean checkouts and dead output first, then salvage and delete the rest. Take a fresh snapshot before each batch.
6. Write the record the nightly mission asks for. The scheduler checks its fields.

Earlier reports are a map of where things are. Their "deferred" lists are not decisions, so decide each large folder again from what you see now.

## Scheduled operation

The user systemd timer `nightly-disk-cleanup.timer` runs `~/.local/bin/nightly-disk-cleanup` at 01:45 Central, which starts one Codex session with the mission in `~/.config/disk-cleanup/mission.md`. The launcher chooses the model and the deadline. Work directly: don't start other agents, change the schedule, the launcher or this skill, or send messages. The only commits you make are salvage commits, pushed with `[skip ci]`. If something fails, say so in the report rather than retrying forever or switching accounts.
