# Disk cleanup skill validation

## Job and scope

Repeated job: recover substantial free space on a developer Mac without
repeating a machine-wide search or losing current work. The package owns local
disk housekeeping; `codex-cleanup` owns targeted Codex state maintenance and
`arch-docs` owns documentation cleanup.

Representative asks:

- "I'm running out of disk space. Find the caches and old worktrees and clean them up."
- "Get this coding machine back to 1 TB free."
- "Clean up the developer junk again without scanning the whole disk."

Nearby anti-case: "Clean up stale architecture documentation in this repo."
Nearest-peer anti-case: "Maintain Codex's log SQLite and old session files."

Explicit user constraint: canonical checkouts, especially
`~/workspace/psmobile` and `~/workspace/psagentspace`, must not be removed even
when inactive. The runtime protects all top-level project checkouts and their
contents, resolved aliases, and shared Git owners. The evaluation must verify
that an old manifest cannot override this boundary.

## Package design

The runtime is prompt-only. `SKILL.md` owns selection, preservation, cleanup,
and measured completion. Two bundled references supply the machine-layout
knowledge and Git/filesystem mechanics that otherwise require rediscovery.
UI metadata exposes a reusable invocation. No controller or cleanup runner is
shipped; optional prior local manifests/scripts remain inspected evidence,
not required runtime dependencies.

## Validation plan

Run the repository skill check and verify the installed package. Then start a
new native child with no parent-chat inheritance, pinned to `gpt-5.6-sol` and
`high`, and ask it to use the installed skill on the actual disk cleanup task.
The child gets the user's objective and authorization, the skill path, and its
write/report scope. It does not get the parent's expected removable paths,
expected byte total, or a prescribed implementation script.

The live task is a repeat-cleanup evaluation: earlier local discovery artifacts
exist and can be found through the skill. This tests whether a smaller model
can discover and use those artifacts responsibly; it does not prove the speed
of a first run on an unfamiliar machine.

Record actual before/after free bytes, time to the first actionable selection,
total elapsed time, scope preserved, and any parent intervention. Verify the
child's reported removals and preservation against the filesystem and Git.
Exercise the anti-cases separately without destructive actions.

Results: pending live validation.
