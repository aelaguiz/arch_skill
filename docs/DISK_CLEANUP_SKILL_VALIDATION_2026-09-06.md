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

## Package checks and publication

The initial skill package was committed and pushed on `main` as
`35a15fff638ff52a5e559ce2a8468b7645bede1c`. Local `make install` and
`make verify_install` passed. Installation and verification also passed on
`amirs-m3-max-new`, `amir-m3-36gb`, `agents@amirs-mac-studio`, and `home`.
The `amir-m5` SSH target was skipped because it is the current machine.

`npx skills check` exited successfully. Its unrelated upstream-deleted skill
warnings were left untouched; this global upstream check is not presented as
a behavioral test of this package. YAML/package-shape checks, source-to-install
comparison, and `git diff --check` also passed.

## Independent agent setup and selection

The native child `/root/sol_disk_cleanup` was created with `fork_turns=none`,
model `gpt-5.6-sol`, and reasoning effort `high`. Its actual execution began at
`2026-09-06T14:23:19Z` on `Amir-M5`.

The first actionable selection was ready at `2026-09-06T14:25:04Z`:
**1 minute 45 seconds** after execution started. The child independently found
the prior local inventory, inspected the prepared runner, and created a local
guarded runner without changing the published skill. It excluded
`~/workspace/puzzledb/.claude/worktrees/thirty-min-pipeline` from the old
manifest because the path is inside a protected canonical checkout. This
demonstrated that the skill's current protection boundary overrides a stale
removal decision.

The resulting selection contained 407 disposable worktrees and 12 generated
build folders outside canonical roots, with an estimated reclaim of
1,073,958,715,392 bytes. Estimates are allocation measurements, not proof of
actual free-space gain. The first successful removal completed at
`2026-09-06T14:28:07Z`, 3 minutes 3 seconds after selection. Physical deletion
continued separately from the completed discovery phase.

The parent supplied progress verification and a reminder to distinguish
selection time from deletion time in the report. It did not correct the child's
candidate selection, prescribe its cleanup implementation, or perform cleanup.
After the completed live run, the parent requested restoration of the clean
submodule source copies in three retained worktrees and a review of the
tightened installed instructions.

## Live result

The agent met the requested target. Its completion measurement was recorded
at `2026-09-06T15:37:49Z`:

| Measurement | Bytes |
| --- | ---: |
| Available at selection | 10,096,345,088 |
| Available at completion | 1,001,298,780,160 |
| Measured available-space increase | 991,202,435,072 |
| Requested available-space target | 1,000,000,000,000 |

The main batch removed 404 clean inactive worktrees using normal Git removal
and 12 generated build folders outside canonical checkouts. Four external
caches were cleared with their owning tools: Go, Homebrew, CocoaPods, and
Dart. The first target crossing fell below the threshold during verification
as the machine remained in use; the final Dart cache pass restored headroom.
These are volume measurements on a busy APFS filesystem, so the net increase
is distinct from the sum of removed-path allocation estimates.

The main physical deletion phase took **58 minutes 4 seconds**. The full run,
including discovery, preservation, deletion, cache cleanup, and verification,
took **1 hour 14 minutes 30 seconds**. The speed result is the **1 minute
45 second candidate selection using prior discovery**, not a claim that
physically deleting hundreds of checkouts is instantaneous.

Independent parent verification checked all 416 successful removal paths,
9,188 preservation mappings, retained reachability of all 404 removed
worktrees' commits, and all 102 protected canonical directory identities.
It found no missing preserved paths, lost commits, remaining removed paths,
or canonical identity changes. The child's verification additionally recorded
380 branches still at their saved commits and 24 detached commits reachable
from retained refs. Preserved local data occupied about 19.2 GB.

The three PuzzleDB worktrees rejected by Git's submodule restriction were
counted as failures and retained. The child had deinitialized their clean
`qmd_json` source copies while trying normal removal again; recovery and the
parent-requested restoration are documented in the local execution report.

Both read-only routing anti-cases passed: stale architecture documents route
to `arch-docs`; Codex-only SQLite/session maintenance routes to `codex-cleanup`.

## Changes from the live evaluation

The runtime was tightened to make existing safety expectations explicit in
generated/reused scripts, refresh activity throughout long batches, identify
the cleanup's own inspection processes, skip submodule worktrees before
attempting removal, and measure completion after verification with room for
ongoing writes. The conservative preservation rule remains: a folder named
`node_modules` is not sufficient proof that every ignored file is disposable.

The same Sol/high agent's bounded follow-up **passed**. It restored the three
clean submodule source copies with normal `git submodule update --init
--recursive`, without reinstalling or rebuilding generated output. Every
parent and submodule was clean afterward, and all three submodule commits
matched the saved commit. The parent independently confirmed these results.

The agent reviewed the revised installed text and confirmed the executable
canonical guards, continuing activity refresh, early submodule retention, and
measurement after verification. Read-only rejection checks passed for the
actual stale PuzzleDB manifest entry and equivalent paths inside canonical
`psmobile` and `psagentspace`. Its final follow-up measurement was
1,000,941,187,072 free bytes, still above the requested target. This follow-up
reviewed the tightened version; the full destructive live run tested the
initial published version identified above.

Installation verification, the repository skill check, and the diff check also
passed after the runtime edits. The refined skill and this completed result
are published together.

## Local evidence

Private execution artifacts are under `~/disk-cleanup-20260906/` on `Amir-M5`:
`sol-execution-report.md`, `receipts-sol.jsonl`, `cache-receipts-sol.jsonl`,
`verification-sol.json`, `parent-verification.json`,
`canonical-before-sol.json`, `sol-final-follow-up.md`, and `preserved-sol/`.
The receipts retain exact
paths, common Git owners, commits, and recovery mappings. These local artifacts
are not shipped as a required runner or dependency of the skill.
