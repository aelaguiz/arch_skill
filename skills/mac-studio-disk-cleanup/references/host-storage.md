# Mac Studio storage operations

All paths below are on `agents@amirs-mac-studio`, with home `/Users/agents`.
These are inspection leads. Confirm what exists and what uses it on each run.

## Baseline and activity

Use `df -k /System/Volumes/Data` or Python `shutil.disk_usage('/System/Volumes/Data')`
for actual free bytes. Use `du -x -k -d 1 <known-root>` for allocated owner sizes.
Bound unfamiliar commands to 60 seconds and narrow on timeout. Do not traverse
mounted simulator runtimes repeatedly or sum APFS clone sizes as reclaimed space.

Inspect process arguments and open paths privately, scoped to candidates.
Use `lsof` plus process ownership; absent output is useful only when the probe
succeeded. Never log complete environments or credential file contents.
Do not suppress a probe failure with `|| true` and then interpret blank output
as no activity. A recursive `lsof +D` timeout is inconclusive. Prefer a bounded
`/usr/sbin/lsof -nP -u agents -F pftn` capture to a private file, check its actual
exit status, and inspect candidate path references including `cwd` and `txt`.
Before removing generated directories in retained checkouts, capture `git
status --porcelain=v1 -z --untracked-files=all`, check `git ls-files` and `git
check-ignore` for the exact target, and compare status afterward. The separate
linked-worktree policy below authorizes removal of old worktree files, not Git
branches or unique commits.

## Rolling 48-hour worktree retention

Every nightly run audits linked Git worktrees under `~/work/`, `~/worktrees/`,
`~/workspace/prime-agent-worktrees/`, `~/workspace/work/**/worktrees/`, and
`~/workspace/agents/work/**/worktrees/`. Use Git's registration (`git worktree
list --porcelain`) to distinguish a linked worktree from a primary checkout.
The cutoff is 48 hours before the run starts. A worktree is recent if its
directory, any source file (tracked or untracked), or HEAD commit was modified
after the cutoff. Exclude generated build/cache output and Git administrative
files from source activity; those can be written by orphaned workers. Record
the cutoff, all registrations examined, removed paths, and deferrals in the
private report. A healthy free-space number does not skip this audit.

For each old linked worktree, capture Git status and the branch/detached tip.
Dirty changes and ignored build data older than the cutoff may be discarded as
Amir requested. Keep branch refs; preserve an otherwise unreferenced detached
tip under a named archive ref before removing its worktree. Check process
working directories, open files and live agent sessions. If only abandoned
test/build/probe workers hold it, identify their exact PIDs, terminate them,
wait, and repeat the activity check. Never kill Prime, Hermes, a current agent
session, or an uncertain process solely because the worktree is old; defer it
with its owner and reason. Skip locked worktrees until their owner and lock
purpose are established. Immediately recheck source activity and references,
then use `git worktree remove --force <exact-path>` and verify the registration
and path disappeared. Do not use raw recursive deletion for a registered
worktree or follow a symlink outside the guarded roots.

Keep `/Users/agents/workspace/work/agent_coder/repos/psmobile` as the PS Mobile
primary checkout and `/Users/agents/workspace/work/agent_ops/repos/rustai` as
the RustAI primary checkout. Inspect any new duplicate primary clones, but
remove one only after confirming it is inactive and preserving unique branches
and commits; retain a compatible entrypoint if a current workflow references
its old path. This is slower than linked-worktree removal and should be
reported as deferred if it cannot be established safely in the nightly budget.

## Recurring owners and retention

**Known live owner, verified September 22:**
`~/.hermes/hermes-agent.backup.20260424T000553Z` contains the running Camofox
browser service. PID 40114 then had its working directory under that tree's
`node_modules/@askjo/camofox-browser` and loaded `better-sqlite3`/`impit` binaries
there. Its command is merely `node server.js`; searching command text for
Hermes misses it. Preserve this tree during nightly cleanup. Do not infer it
is retired because gateways use the newer `~/.hermes/hermes-agent` tree.
Service migration or removal is a separate operator action; do not stop it to
make the backup folder eligible.

| Owner | Inspect | Authorized treatment |
| --- | --- | --- |
| Hermes | `~/.hermes/profiles/*/logs/`, root logs, `~/.hermes/backups/`, old staging/copy directories | Compact text logs over 128 MiB to the last 4 MiB in place; remove rotated logs older than 7 days. Remove obsolete migration/staging/runtime copies only after checking processes, open files and launch configuration. Keep live databases, memories, sessions, skills, auth and configuration. |
| AIM | Direct children of `~/.aimgr/` | Delete timestamped `secrets.json.bak.*` and `local-state.json.bak.*` snapshots older than 7 days by both name timestamp and mtime. Preserve current files, recent snapshots and open files. Never read or print their values. |
| Development | `~/work/`, `~/worktrees/`, `~/workspace/prime-agent-worktrees/`, `~/workspace/work/**/worktrees/`, `~/workspace/agents/work/**/worktrees/` | Remove linked worktrees after 48 hours of source inactivity using the procedure above. For retained checkouts, remove ignored, untracked `apps/flutter/build` and generated `.dart_tool` output when inactive and older than 24 hours. Under capacity pressure, recent reproducible output is also eligible once current activity is ruled out. Preserve primary checkouts and Git history. |
| Developer caches | `~/.gradle/caches`, `~/Library/Developer/Xcode/DerivedData`, package/build caches identified by owner | Clear stale reproducible output when no current build/open files use it. Prefer old entries; do not repeatedly evict healthy hot caches simply to increase the reclaimed counter. |
| Figma updater | `~/Library/Caches/com.figma.Desktop.ShipIt/ShipIt_stderr.log` | Use the same 128 MiB trigger and 4 MiB recent tail as Hermes logs. |

For AIM's observed timestamp format, the exact basename pattern is
`^(secrets|local-state)\.json\.bak\.(\d{8}-\d{9})$`. Validate the date; skip
unrecognized names. Precompute the guarded roots once instead of resolving
every protected root for each of tens of thousands of backups. Recheck file
identity/mtime immediately before unlinking. Keep only path/count/byte metadata.

For live log compaction, retain the inode so existing writers continue using
the file. Inspect whether the writer appends. Do not blindly truncate a
non-append writer and create a large sparse hole. Use its native reopen/rotation
mechanism where necessary. Preserve a recent tail without copying gigabytes
into a new archive; a small concurrent diagnostic tail loss is acceptable for
these disposable logs. Verify growth and service health after compaction.

## Simulators

Inventory with `xcrun simctl list devices --json` and
`~/Library/Android/sdk/platform-tools/adb devices -l`. Device app data is
disposable. Runtime SDKs and device definitions need not be removed.

For iOS, target an eligible device by UDID using `xcrun simctl shutdown <UDID>`
if needed, followed by `xcrun simctl erase <UDID>`. Prefer substantial data
owners; do not reset an already-empty device just to record activity. Defer
devices belonging to a current build/test during nightly maintenance.
`xcrun simctl shutdown all` then `xcrun simctl erase all` is the explicit
all-device cleanup operation, as authorized in the September 21 interactive run.

For Android, identify each AVD with `adb -s <serial> emu avd name` and stop the
eligible device with `adb -s <serial> emu kill`. Reset through the SDK emulator,
not by guessing which files inside the AVD are its writable state:

```sh
emulator -avd <name> -wipe-data -no-window -no-snapshot -no-audio \
  -no-boot-anim -gpu swiftshader_indirect -port <unused-even-port>
```

Run one reset at a time in an owned process group. Wait at most 120 seconds for
`adb -s emulator-<port> shell getprop sys.boot_completed` to return `1`, then
send `emu kill`. Reap the process and any owned crashpad/helpers; verify its
port and serial disappeared. On failure terminate that exact process group.
The prior AVD names were `Medium_Phone_API_36.1` and `Pixel_9`; rediscover rather
than assuming those remain the current set. Never touch physical devices.

## Other large owners

Git transfer `.bundle` files in `/private/tmp` can be discarded when no process
uses them and every included tip is retained by a named ref in an existing
repository. Verify with `git bundle list-heads` and `git for-each-ref --contains`.
Do not delete Git object packs based on their size or temporary-looking name.

Docker/Colima, swap and local models can account for substantial remaining
space. Inspect current owners. Do not delete the VM disk, prune persistent
volumes, restart shared services or kill unrelated jobs to reach the target.
Use supported cache/image cleanup only when current reference checks establish
it is disposable. A running inference service can use a model even when this
host does not run RustAI. Inspect RustAI metadata only; never open, hash, expand
or load multiplayer policy payloads to decide whether to delete them.

## Evidence and scheduler

The September 21 baseline and action log remain at
`~/disk-cleanup-2026-09-21/README.md`, `summary.json`, and `actions.jsonl`.
They explain prior actions but are not a current inventory. That cleanup
raised available space from 1,676,214,272 to 174,862,479,360 bytes.

Nightly runtime state is `~/.local/state/mac-studio-disk-cleanup/`:
`latest/` points to the most recent run, containing `final.md`, `summary.json`,
`actions.jsonl` when applicable, `events.jsonl`, and the launcher's `exit-code`.
Delete completed run directories older than 14 days; retain the current run,
the latest pointer target and the original incident evidence. Do not let the
cleanup job itself accumulate unlimited diagnostics.

The sole timer is `~/Library/LaunchAgents/com.funcountry.agents_host.nightly_disk_cleanup.plist`.
The tracked launcher is
`~/workspace/agents/deploy/mac/host_runner/nightly_disk_cleanup.sh`.
Inspect with `launchctl print gui/502/com.funcountry.agents_host.nightly_disk_cleanup`.
An operator can trigger it with `launchctl kickstart gui/502/com.funcountry.agents_host.nightly_disk_cleanup`.
The previous `host_disk_control.mjs` remains an operator tool; do not invoke
its mutation pipeline automatically alongside this skill.
