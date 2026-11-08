# Mac Studio map

All paths are on `agents@amirs-mac-studio`, with home `/Users/agents`. They say where things usually are, not where to stop looking: the run measures the whole Data volume. Confirm what exists, and what uses it, each run.

## Measuring

Free space is what `df -k /System/Volumes/Data` reports. Time Machine's local snapshots hold deleted data until they go ([time-machine-local-snapshots.md](../../_shared/time-machine-local-snapshots.md)). Make one size pass with newest-file times, `sudo gdu -x -k --time --time-style=+%s -d 6`, over `/Users/agents`, `/Users/aelaguiz` and the other top-level Data volume folders. It costs about the same as a shallow pass. Save all of it, so the rest of the run and the next one read it instead of scanning again. Don't add up APFS clone sizes or traverse the mounted simulator runtimes twice. Process and use checks are in [checking-use.md](../../disk-cleanup/references/checking-use.md). Run the snapshot with `sudo -n`.

## Checkouts

Task checkouts and clones live in `~/workspace/*-worktrees/` (PS Mobile, website, RustAI and others), top-level task folders in `~/workspace/`, `~/work/`, `~/worktrees/`, `~/workspace/work/**/worktrees/` and `~/workspace/agents/work/**/worktrees/`. Most folders under `~/workspace/*-worktrees/` are standalone clones rather than linked worktrees, so `git worktree list` doesn't show them. Salvage them as standalone clones, as [worktrees-and-measurement.md](../../disk-cleanup/references/worktrees-and-measurement.md) describes. The PS Mobile primary that owns linked worktrees is `/Users/agents/workspace/work/agent_coder/repos/psmobile`. Studio RustAI work has run from `~/workspace/rustai`. Confirm both from the snapshot before relying on them: a primary nobody uses is a copy like any other.

## Live services that hide their owner

- **Camofox.** The browser service runs as a bare `node server.js`, so searching command lines for Hermes misses it. Find where it runs from its working directory and loaded files before touching any Hermes copy.
- **Colima.** The VM runs the Cratejoy QA services and their databases. The launcher's preflight cleans images inside it. Never delete or recreate the VM, prune volumes, or force-remove containers. Afterwards, check that the containers that were running before your work still run.
- **CI.** The CI agents (`~/.buildkite-agent-studio` and its builds) are live while a job runs. Their caches refill on the next job.

## Recurring owners

| Owner | Where | What to do |
| --- | --- | --- |
| Hermes | `~/.hermes/profiles/*/logs/`, root logs, `~/.hermes/backups/`, old staging and copy folders | Cut text logs over 128 MiB to their last 4 MiB in place, and remove rotated logs older than a week. Remove old migration, staging and runtime copies that no process, open file or launch configuration uses. Keep live databases, memories, sessions, skills, auth and configuration. |
| AIM | Direct children of `~/.aimgr/` named `secrets.json.bak.<YYYYMMDD-HHMMSSmmm>` or `local-state.json.bak.<...>` | Delete those older than seven days by both their name and their modification time. Never read their contents. |
| Figma updater | `~/Library/Caches/com.figma.Desktop.ShipIt/ShipIt_stderr.log` | Same as Hermes logs. |
| Developer caches | `~/.gradle/caches`, `~/Library/Developer/Xcode/DerivedData`, package caches | Clear old entries when no build uses them. Don't empty hot caches CI refills within the hour. |
| Git bundles | `.bundle` files in `/private/tmp` | Delete when no process uses them and every tip they hold is kept by a named ref in an existing repository (`git bundle list-heads`, `git for-each-ref --contains`). |
| Cleanup reports | `~/.local/state/mac-studio-disk-cleanup/runs/` | Keep 14 days, plus the current run and `latest`. |

## Simulators

List them with `xcrun simctl list devices --json` and `~/Library/Android/sdk/platform-tools/adb devices -l`. Device app data is disposable. Leave runtime SDKs and device definitions in place.

- **iOS.** Erase an eligible device by UDID: `xcrun simctl shutdown <UDID>` if it is booted, then `xcrun simctl erase <UDID>`. Skip devices a current build or test is using.
- **Android.** Identify each emulator with `adb -s <serial> emu avd name` and stop an eligible one with `adb -s <serial> emu kill`. Reset it through the SDK emulator, not by guessing which files are its writable state:

  ```sh
  emulator -avd <name> -wipe-data -no-window -no-snapshot -no-audio -no-boot-anim -gpu swiftshader_indirect -port <unused-even-port>
  ```

  Run one reset at a time. Wait up to 120 seconds for `adb -s emulator-<port> shell getprop sys.boot_completed` to return `1`, then `emu kill`. Reap the process and its helpers. Never touch physical devices.

## Scheduler

- **Timer.** The only one is `~/Library/LaunchAgents/com.funcountry.agents_host.nightly_disk_cleanup.plist`, at 01:15 Central. Inspect it with `launchctl print gui/502/com.funcountry.agents_host.nightly_disk_cleanup`, and start a run with `launchctl kickstart gui/502/com.funcountry.agents_host.nightly_disk_cleanup`.
- **Runs.** Each run's folder is under `~/.local/state/mac-studio-disk-cleanup/runs/`, and `latest` points at the newest. The launcher writes `vm-cleanup.json` and `exit-code` and checks `summary.json`. Its mission, `nightly_disk_cleanup.md` in the same folder as the launcher, lists the fields.
