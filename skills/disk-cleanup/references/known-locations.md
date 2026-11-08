# Where space usually is on the Macs

These are leads for Amir's M5, the two M3s and Mini 1, with paths relative to the home folder. They say where to look, not what to decide. The size pass in [checking-use.md](checking-use.md) shows where the space really is today. When the biggest folders are somewhere not listed here, open them anyway.

## Task checkouts

| Where | What it is |
| --- | --- |
| `~/workspace/*-worktrees/`, `~/workspace/*-wt/` | Collections of task checkouts: PS Mobile (2 to 5 GB each with Flutter builds), PuzzleDB, Lessons Studio, RustAI, website, PS Agent Space. |
| `~/workspace/<repo>-<task>` | Top-level task copies such as `psmobile-5966`, `puzzledb-wt-t91` or `rustai2`. Some are linked worktrees and some are standalone clones. |
| `.claude/worktrees/` inside a primary checkout | Agent worktrees nested in a checkout that stays. The worktree can go, and its parent stays. |
| `~/worktrees/`, `~/.codex/worktrees/`, `/private/tmp` | Other places agents put checkouts. `git worktree list` from each primary repository reveals more. |

The primary checkouts are the working copies of the projects that are live: `~/workspace/psmobile` with its shared Git owner `~/workspace/.psmobile-git-root`, `psagentspace`, `psbrain`, `prime-agent`, `arch_skill`, `rustai`, `puzzledb`, `lessons_studio`, `cjdev`, `website` and `agentspace`. On the M3 Max, most of the roughly 200 top-level folders were last touched in April. They are old copies of projects, plus other people's projects cloned to read. Those are copies like any other: salvage the unsaved bits and they go. Amir's personal folders among them stay, as everywhere.

## Build output and caches

| Where | What it is |
| --- | --- |
| A task checkout's `apps/flutter/build/`, `.dart_tool/`, `ios/Pods/`, `target/`, `node_modules/`, `.venv/` | These go with the checkout. In a checkout that stays, see the reference on build output. |
| `~/Library/Developer/Xcode/DerivedData/` | Xcode build output. Clear it when no Xcode build or device run is using it. |
| `~/Library/Caches/go-build/`, `~/.gradle/caches/`, `~/.npm/_cacache/`, `~/Library/Caches/Homebrew/`, `~/Library/Caches/CocoaPods/` | Download and build caches. Use the tool's own cleaning (`go clean -cache`, `brew cleanup -s`) when no build is running. CI refills Go and Gradle within the hour, so clearing them on a busy CI machine gains little. |
| `~/.cache/uv/` | Python environments and wheels, about 150 GB on the M5. The tools Amir's agents run start straight from it all day. `uv cache prune` waits while any uv process is running, and it freed only 100 MB the times it ran, so this isn't the easy win it looks like. |

## Devices and VMs

- **iOS simulators.** `xcrun simctl list devices --json` lists them with their state and last boot. A task simulator nobody is using goes with `xcrun simctl delete <udid>`: check that no test runner, `idb` or Flutter session has it open. A booted device with no app or test activity can be shut down and then deleted. Never shut down all devices or kill the simulator services.
- **Android emulators.** Each lives in `~/.android/avd/<name>.avd`, at 3 to 17 GB, under names like `CLAUDE_<task>_API36`. A running one shows up as a `qemu-system-*` process with its files open. A finished task's emulator goes with `avdmanager delete avd -n <name>`, or by removing the `.avd` folder and its `.ini`. Keep the system images that the remaining emulators use.
- **Colima VMs.** `colima list` shows each profile and whether it runs, and `~/.colima/_lima/_disks/<profile>` shows each disk's size and last change. A stopped profile named for a finished task (a QA environment, a verification run) is a task copy, and `colima delete --profile <name>` removes it with its disk. The default profile, and any profile a current project runs its databases in, stays. Inside a running VM, prune through Docker (`docker image prune`, `docker builder prune`) and leave volumes alone.

## Agent and app state

- **Codex and Claude history** (`~/.codex/sessions`, `~/.aimgr/claude-homes/*/.claude/projects`) is the session history that `$agent-history` reads. It grows by several GB a day on the M5. How long to keep it is Amir's decision, and the work belongs to `$codex-cleanup`, not here.
- **`~/.aimgr`** holds credentials and their backups. Timestamped `secrets.json.bak.*` and `local-state.json.bak.*` files older than a week can go. Never read their contents.
- **Prime.** Inactive session history, recovery snapshots, logs and stale worker records under `~/.prime/agent/` can go. Keep authentication, configuration, custom skills and extensions, and anything a running Prime process uses.
- **Browsers.** Caches under `~/Library/Caches/<browser>` can go while that browser isn't running. Profiles under `~/Library/Application Support/` hold logins and stay.
- **This skill's own records** (`~/disk-cleanup-*`) are notes for the next run. Keep the latest few, and remove older ones along with any files an old run "preserved" in them.

## Models and policies

RustAI policies live on the policy drives (`/Volumes/rustai-policies` on the Studio, `/mnt/p2` on the home server), and a checkout's `policies`, `policies_blueprint`, `runs/policies` and `artifacts/cardabs` link to them. A policy store on a Mac's internal disk is a copy that belongs on a drive. If nothing links to it and no process reads it, it goes. Two folders with similar names and sizes aren't necessarily duplicates, and a hard link or an APFS clone holds no second copy.

## Everything else

When these places don't explain the disk, the size pass over the rest of the home folder, `/private/tmp`, `/private/var/folders` and `/Library` will. Amir's own folders (Documents, Desktop, Downloads, Pictures, Movies, and his personal projects) are his: count them, and leave them. When deleting doesn't raise free space, Time Machine's local snapshots are almost always the reason ([time-machine-local-snapshots.md](../../_shared/time-machine-local-snapshots.md)).
