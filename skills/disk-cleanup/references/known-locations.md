# Known storage locations

Use paths relative to the current user's home. These are discovery leads from
Amir's developer-machine layout, not blanket deletion targets or promised sizes.
Confirm the host, filesystem, and existing paths. Other machines in the cluster
can have different home directories and capacity.

## Reuse local discovery

Look for `~/disk-cleanup-*/manifest.json` and neighboring reports or receipts.
Older one-off inventories may also exist as `/private/tmp/disk-cleanup-*` on
macOS. List these shallowly; read summary fields first and load detailed rows
programmatically. A prior manifest can save a full search, but paths may have
been removed, reused, or made active since it was written.

An old report saying there were no eligible worktrees is not a reusable inventory.
Refresh Git registrations and current eligibility in the known collections each
day. Save detailed rows locally and print counts and the largest candidates;
do not dump hundreds of registrations or thousands of ignored filenames.

## First: task checkouts and worktrees

| Location | What to inspect |
| --- | --- |
| `~/workspace/psmobile-worktrees/` | Many full PS Mobile checkouts; Flutter builds and dependencies can multiply their size. |
| Top-level `~/workspace/<repo>-<task>` folders such as `psmobile-5966`, `psmobile-l10n-m8`, `psmobile-wt-*`, `puzzledb-l10n-*`, `rustai2` | Task copies of canonical repositories, often 2 to 30 GB each; on Amir-M5 in September 2026 they held about 500 GB. Linked worktrees and standalone clones both occur. |
| `~/workspace/rustai-worktrees/` | RustAI checkouts, per-worktree Rust targets, client dependencies, and local artifacts. |
| `~/workspace/puzzledb-worktrees/` | PuzzleDB checkouts, Python environments, generated files, and local datasets. |
| `~/workspace/lessons_studio-worktrees/`, `lessons-studio-worktrees/`, `psagentspace-worktrees/`, `website-worktrees/`, `prime-agent-worktrees/`, `cjdev-worktrees/` | Other recurring agent checkout collections. |
| `~/workspace/worktrees/`, `~/workspace/.worktrees/`, `~/worktrees/`, `~/.codex/worktrees/` when present | Additional checkout roots; Git's registrations reveal paths outside these examples. |

Enumerate worktrees once per common Git directory, using canonical repos such
as `~/workspace/psmobile`, `rustai`, `puzzledb`, `lessons_studio`, `psagentspace`,
`website`, and `prime-agent`. PS Mobile may use
`~/workspace/.psmobile-git-root` as its shared Git owner. Use
`git rev-parse --path-format=absolute --git-common-dir` to resolve the current
owner rather than assuming every checkout has a `.git` directory.

These canonical repositories are read-only inspection anchors, never removal
candidates, together with their resolved targets and shared Git owners. The
other copies of the same repositories are task checkouts under the salvage
rules in `SKILL.md`, including top-level folders and `.claude/worktrees/`
entries nested inside a canonical checkout.

A shallow listing of `~/workspace` finds newly added `*-worktrees` collections
and top-level task copies. Do not limit discovery to a fixed repo list when
current Git registrations or the user's request point elsewhere.

## Next: reproducible build and dependency storage

| Location | What it usually holds |
| --- | --- |
| Worktree `apps/flutter/build/`, `apps/flutter/.dart_tool/`, `apps/flutter/ios/Pods/`, `apps/flutter/macos/Pods/` | Flutter outputs, analysis/build state, and CocoaPods dependencies. |
| Disposable worktree `target/`, `codex-rs/target/`, `node_modules/`, `.venv/` | Rust outputs and installed dependencies; inspect custom output settings and symlinks. Canonical checkout contents are excluded. |
| `~/Library/Developer/Xcode/DerivedData/`, `~/Library/Developer/Xcode/iOS DeviceSupport/` | Xcode outputs and device support files. Check active builds and attached-device use. |
| `~/Library/Caches/go-build/`, `~/Library/Caches/Homebrew/`, `~/Library/Caches/CocoaPods/`, `~/.gradle/caches/`, `~/.npm/_cacache/` | Download and build caches. Prefer the owning tool's cleanup behavior where appropriate. |
| `~/.cache/uv/`, `~/Library/Caches/pip/`, `~/Library/Caches/pnpm/`, `~/.pub-cache/` | Language package caches; uv's archive can share hardlinks with environments, while active tools may run directly from cached environments. |

Measure leaf owners without counting both the worktree and its build folders
as independent reclaimable space. Deleting an old checkout recovers its source
copy and outputs together, so start there when collections contain hundreds of
checkouts.

## Then: application caches, logs, and virtual disks

Browser caches often live under `~/Library/Caches/BrowserOS/` and
`~/Library/Caches/Google/`. Profiles under `~/Library/Application Support/`
contain user data. Keep active browsers usable and distinguish cache files from
profiles and credentials.

Agent state lives under `~/.codex/`, `~/.claude/`, `~/.aimgr/`, and `~/.prime/`.
Inspect sizes of log/cache subdirectories rather than dumping their contents.
`~/.aimgr` can contain credentials and credential backups. Codex databases,
WAL files, and session history are not generic temporary files; do not remove
them while agents are running. A targeted Codex maintenance request belongs
to `$codex-cleanup`.

### Inactive Prime state

Amir has authorized daily removal of unused Prime session and recovery state.
Inspect `~/.prime/agent/` for session history, session artifacts, recovery
snapshots, logs, quarantine, stale worker/lease records, and reproducible runtime
environments. Check live process paths and open files before each batch. Remove
confirmed inactive state rather than reporting the same opportunity every day.
Keep authentication files and their backups, configuration, custom skills and
extensions, source/patch backups, and any currently used runtime. Inspect other
Prime subdirectories by their actual contents; their location alone does not
make unique source files disposable. Record that deleted history and snapshots
cannot be restored from the cleanup. Do not extend this authorization to Codex,
Claude, AIMgr, or other application databases.

### Virtual machines

Colima storage can be concentrated in `~/.colima/_lima/`; Docker data may be
inside a VM disk. Start with `docker system df` and the current Colima/Docker
configuration. A large sparse disk is not all disposable, and deleting the VM
image can destroy volumes. Use owner-supported pruning and space reclamation
after identifying what is unused. Prune unused build cache and images through
the exact Docker context after checking active builds and container references;
keep containers, volumes, and VM disks. Guest deletion may not release host
blocks until trim reaches the data filesystem. For Colima, inspect mounts and
use `colima --profile <profile> ssh -- sudo fstrim -av` when supported. Trimming
only `/` can miss the separate data disk. Verify host free bytes afterward;
trim output is not additional reclaimed host space.

### Unused simulators and runtimes

`~/Library/Developer/CoreSimulator/`, `~/Library/Android/`, and `~/.android/`
hold simulator/emulator runtimes and device data. Inventory installed devices
and active processes on daily runs. Use `xcrun simctl list devices --json` to
record device IDs, names, state, last boot, and reported sizes. Connect named
devices to current worktree/effort activity, direct UDID references, open device
files, app/test runners, Flutter sessions, and automation clients such as idb.

Delete confirmed unused task devices through `xcrun simctl delete <udid>` under
the daily authorization. Recheck identity and activity immediately beforehand.
Old task-specific devices with no live owner or client are candidates; shutdown
status or age alone is insufficient. Preserve recent devices associated with
ongoing work and any deliberately retained test fixture. A booted device that
has only idle simulator OS services, no app/test activity, and no live owner can
be shut down with `xcrun simctl shutdown <udid>` and then deleted. Never shut down
all devices or kill shared simulator services. Save each deleted device's name,
UDID, runtime/type, and reason; recreation does not recover its prior saved state.

Android task emulators in `~/.android/avd/` (names such as
`CLAUDE_<task>_API36.avd`, `CODEX_...`, `PRIME_...`) are the same class and
often larger, 3 to 17 GB each with RAM snapshots. A running emulator shows up
as a `qemu-system-*` process with the AVD's files open. Delete an old,
unreferenced task AVD with `avdmanager delete avd -n <name>`, or remove its
`.avd` directory and matching `.ini` file. Keep the system images under
`~/Library/Android/sdk/` that retained AVDs use.

After device cleanup, check runtime assignments across all retained device sets
and active processes. Keep loaded runtimes and runtimes needed by retained devices.
Only remove an unused runtime when no retained device depends on it, using
`xcrun simctl runtime delete <runtime-id> --dry-run` followed by the exact
owner-tool deletion when authorized. Verify retained devices and their booted
state remain present. Runtime volumes mounted beneath CoreSimulator can inflate
recursive `du` totals; avoid counting both mounted contents and their images.

For suspected duplicate model or policy stores, resolve symlinks and compare
file inventories and sizes first. Aliases consume no second payload copy, and
different checkpoints are not duplicates. Preserve canonical model stores and
unique training outputs; report potential deduplication for a user decision.
Honor repository payload-access restrictions. In RustAI, never fetch, expand,
hash, or load multiplayer policy payloads to investigate metadata or disk use.

## Broaden only for an unexplained remainder

Use one shallow measurement at a time for the remaining likely owner, such as
`~/Library`, `/private/tmp`, or `/private/var`. Inspect APFS snapshots or
deleted-but-open files when deletion does not translate into available space.
macOS may deny access to protected directories; continue with accessible
material owners rather than making Full Disk Access a prerequisite.

Archives, project datasets, models, research, recordings, and downloads can be
large intentional assets. Size and a directory name such as `tmp`, `artifacts`,
or `backup` do not authorize their deletion. Keep the cleanup focused on the
user's requested disposable storage.
