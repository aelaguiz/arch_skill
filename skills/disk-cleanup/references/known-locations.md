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

## First: duplicate worktrees

| Location | What to inspect |
| --- | --- |
| `~/workspace/psmobile-worktrees/` | Many full PS Mobile checkouts; Flutter builds and dependencies can multiply their size. |
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
candidates. Protect all top-level project checkouts, especially
`~/workspace/psmobile` and `~/workspace/psagentspace`, plus their resolved
targets and shared Git owners. Nested `.claude/worktrees/` inside a protected
canonical checkout stays outside routine cleanup too. A standalone top-level
checkout remains protected even if Git calls it a linked worktree.

A shallow listing of `~/workspace` finds newly added `*-worktrees` collections
and standalone checkouts. Do not limit discovery to a fixed repo list when
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
as independent reclaimable space. Discarding a clean inactive checkout can
recover its source copy and outputs together, so start there when collections
contain hundreds of checkouts.

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

Colima storage can be concentrated in `~/.colima/_lima/`; Docker data may be
inside a VM disk. Start with `docker system df` and the current Colima/Docker
configuration. A large sparse disk is not all disposable, and deleting the VM
image can destroy volumes. Use owner-supported pruning and space reclamation
after identifying what is unused.

`~/Library/Developer/CoreSimulator/`, `~/Library/Android/`, and `~/.android/`
hold simulator/emulator runtimes and device data. Inventory installed devices
and active processes before considering obsolete runtimes. Do not erase device
state as a substitute for cleaning build caches.

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
