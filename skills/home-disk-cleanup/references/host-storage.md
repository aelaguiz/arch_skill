# Home server storage map

Host alias `home` resolves to `home.fairy-salmon.ts.net`. The machine is
`amir-server`, user `aelaguiz` (UID 1000), home `/home/aelaguiz`.

## Mounted volumes

| Path | Expected filesystem identity | Initial September 22 observation |
| --- | --- | --- |
| `/` | Linux root ext4 filesystem | Approximately 288 GiB available |
| `/mnt/p2` | ext4 UUID `33d0a72f-c3b3-4299-a591-dcac986c9327` | Approximately 1.9 TiB available |
| `/mnt/p3` | ext4 UUID `41f6ce2d-a3e0-488b-9550-180ba6642bc7` | Approximately 592 GiB available |

Use `findmnt --target <path> -n -o TARGET,UUID,FSTYPE` and confirm the returned
mountpoint is the expected one. If a data drive is absent, skip its directory
and warn; never clean the root filesystem directory underneath a missing mount.
The other `/mnt` names included unmounted empty directories. Rediscover newly
mounted user data drives before including them, using the same ownership
checks. Never touch EFI, system pseudo-filesystems or unrelated mounted data.

## Known owners

- Root: `~/workspace/rustai`, `rustai2`, their `*-worktrees`/`*_worktrees`
  collections, `~/workspace/checkpoints`, experiment output roots and normal
  developer caches. Catalogs live at each relevant checkout's
  `config/catalog.toml`; also inspect registry/run metadata when applicable.
- `/mnt/p2/rustai_local/` contains `target`,
  `target_relocated_from_root_20260806`, `handbuilder_serving_main_target`,
  `runs`, `artifacts`, `cardabs`, `policies_blueprint`, and `policies_archive`.
  Inspect the leaf owner; the parent holds useful data as well as build output.
  `/mnt/p2/policies_blueprint` and `/mnt/p2/rustai2_artifacts/challenges`
  are potentially canonical artifacts. Worktree collections also live here.
- `/mnt/p3` contains many separately owned Cargo targets, temporary test
  directories, `go-cache`, `go-tmp`, logs, `artifacts`, policy stores and
  archived runs. Use source/config references and filesystem structure to
  identify disposable output rather than treating the names as deletion rules.
- `~/workspace/rustai/policies` resolves into
  `/mnt/p3/policies_hydrated_20260611`. Other policy owners include
  `/mnt/p3/policies_blueprint_0422`, `policies_extra_20260917`, and
  `/mnt/p2/rustai_local/policies_archive`. Resolve catalog entries through
  these aliases before deciding any child policy is unreferenced.
- `~/workspace/rustai/artifacts/policies`, `rustai2/artifacts/policies`,
  per-worktree test outputs and recorded short-run directories are useful
  leads for obsolete throwaway policies. Preserve production/retained-model
  references wherever the payload physically lives.

For AIM backup retention, inspect direct children of `~/.aimgr` matching
`^(secrets|local-state)\.json\.bak\.(\d{8}-\d{9})$`. Require both a valid
name timestamp and mtime older than seven days. Preserve current files and
open snapshots. Precompute path guards once for large candidate sets.

`/run/user/1000` was full because of a 13 GB `dictation_*.wav` recording.
That recording is user data, not training garbage. Do not erase it as routine
cleanup. Do not purge runtime sockets or another session's temporary files.
Docker persistent data and real retained datasets likewise need their own
owner-aware treatment, not broad pruning.

## Runtime operations

The user systemd manager has lingering enabled, so the timer can run without
an interactive SSH login. Inspect with
`systemctl --user status nightly-disk-cleanup.timer` and
`systemctl --user list-timers nightly-disk-cleanup.timer`.
Start one manual verification with `systemctl --user start --no-block
nightly-disk-cleanup.service`. Native systemd owns overlap prevention and its
service control group; use `systemctl --user stop nightly-disk-cleanup.service`
to stop this job. Never kill shared training processes by name.

The installed launcher is `~/.local/bin/nightly-disk-cleanup`; the mission is
`~/.config/disk-cleanup/mission.md`. Latest results are in
`~/.local/state/disk-cleanup/latest/`. An absent `exit-code` means the current
run has not completed. `error.log` and the journal explain failed starts.
