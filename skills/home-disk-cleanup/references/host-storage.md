# Home server map

Host alias `home` resolves to `home.fairy-salmon.ts.net`. The machine is `amir-server`, user `aelaguiz` (UID 1000), home `/home/aelaguiz`. Noninteractive `sudo -n` works. Never type or prompt for a password.

## Volumes

| Mount | Identity | Size | What it holds |
| --- | --- | --- | --- |
| `/` | ext4 UUID `12baa62b-8161-44d2-ad3d-66d348fcc49a` (`/dev/nvme1n1p2`) | 982 GB | `~/workspace`, caches, agent homes. |
| `/mnt/p1` | ext4 on `/dev/nvme0n1p1` | 983 GB | `rebel-turn-port` and `rebel-gap` experiment work, older archives, `caches` (uv, go-build), QA build copies. |
| `/mnt/p2` | ext4 UUID `33d0a72f-c3b3-4299-a591-dcac986c9327` (`/dev/sdb`) | 4 TB | RustAI stores, experiment rounds, QA stacks, `machines run` mirror. The kernel reports past filesystem errors on this drive, so don't run large rewrites on it. |
| `/mnt/p3` | UUID `41f6ce2d-a3e0-488b-9550-180ba6642bc7`, label `p3-degraded` | | It is unmounted on purpose (`noauto` in `/etc/fstab`). Its mountpoint is an empty directory on root. Never touch it. |

## Where things are

- **Primary checkouts.** `~/workspace/rustai` is Amir's: his sessions run in it, and its `policies` and `policies_blueprint` link to `/mnt/p2/policies_hydrated_20260611` and `/mnt/p2/policies_blueprint_0422`. `~/workspace/rustai-agents` is the agents' checkout, linked into `/mnt/p2/rustai-agents`. `psmobile`, `psagentspace`, `agentspace`, `puzzledb` and the other top-level repositories are the working copies of their projects.
- **Task checkouts.** `~/workspace/rustai-worktrees/*`, top-level `~/workspace/rustai-*` copies, `~/workspace/psmobile-worktrees/*`, `~/workspace/experiments/*`, and `/mnt/p2/product-engineer/wt-*` and similar QA checkouts on the data drive.
- **Serving.** The Play vs AI server runs from a worktree under `~/workspace/rustai-worktrees`, with its binary built under `/mnt/p2/rustai_local`. The snapshot shows its current folders; don't assume them.
- **RustAI stores on `/mnt/p2`.** `rustai-agents/` holds the agents' four linked folders plus experiment folders: curriculum runs, Sit & Go census and pruning runs, PR checks. `rustai_local/` holds `artifacts/challenges` (a canonical decision store, a `drafts` store and a `.legacy_*` copy from February), `policies_blueprint`, `policies_archive` and build targets. `policies_blueprint`, `policies_blueprint_0422` and `policies_hydrated_20260611` sit at the top level of `/mnt/p2`. QA layout scripts in `/mnt/p2/product-qa-*` name `rustai_local/artifacts`. Read them before removing anything under it.
- **Hard links.** Many policy files in `/mnt/p2/rustai-agents` are hard links to the same data as Amir's `/mnt/p2` policy folders. Deleting one copy frees nothing while the other remains.
- **Experiment rounds.** `/mnt/p2/ms12/<round>`, `/mnt/p2/sng*`, `/mnt/p2/pluribus-*`, `/mnt/p2/coach-backtest*`, `~/workspace/archives`, `~/workspace/m12-*`, `/mnt/p1/rebel-*`. Running round scripts (`step*.sh`) show up in the snapshot.
- **`/mnt/p2/machines-run-mirror`.** This is where `machines run` copies a Mac's workspace folders so commands can run here. It regenerates on the next `machines run`. A copy with no process using it, and no writes since the run that made it, can go.
- **Caches.** `~/.cargo`, `~/.gradle`, `~/.cache`, `/mnt/p1/caches`, Docker images and build cache (`docker system df`). Docker volumes and the databases in them stay.
- **AIM backups.** Direct children of `~/.aimgr` named `secrets.json.bak.<YYYYMMDD-HHMMSSmmm>` or `local-state.json.bak.<...>` that are older than seven days, by both their name and their modification time. Never read their contents.
- **Logs.** Text logs over 128 MiB that a process appends to can be cut to their last 4 MiB in place, keeping the inode. A writer that doesn't append needs its own rotation.
- **Trash.** `/mnt/p2/.Trash-1000` is a desktop trash can, and nothing there is in use.

## Scheduler and reports

- **Timer.** `systemctl --user list-timers nightly-disk-cleanup.timer` shows it, and `systemctl --user start --no-block nightly-disk-cleanup.service` starts one run by hand. Stop a run with `systemctl --user stop nightly-disk-cleanup.service`, and never kill shared training processes by name.
- **Runs.** Each run's folder is `~/.local/state/disk-cleanup/runs/<time>`, and `latest` points at the newest. The launcher saves `final.md`, `events.jsonl`, `error.log` and `exit-code`, and checks that `summary.json` has `host`, `status` and `volumes`, with integer byte fields. A missing `exit-code` means the run hasn't finished.
- **Retention.** Keep completed run folders for 14 days.
