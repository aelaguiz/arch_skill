# Resume semantics: every invocation is a resume

The skill does not have a dedicated `resume` command. Every
invocation of `$arch-epic` is the same thing: read the epic doc,
read the arch-step state for each sub-plan, figure out where we
are, do the next action, end the turn. "Pick up where we left off"
is the only mode of operation, because there is no other mode.

That is why the user can type whatever they naturally type
("continue", "resume the epic", "keep going", "pick up on
../project") — the skill's behavior is the same regardless of
phrasing.

## The re-entry routine

Every turn the skill runs this sequence:

1. Identify the epic doc. Three cases:
   - The user named an explicit path in their invocation. Use it.
   - The user did not name a path but the session context has a
     recently-touched epic doc. Use it. Announce which one.
   - Neither. Look for epic docs in the orchestrator repo's
     `docs/` directory (files matching `EPIC_*.md` with
     `doc_type: epic` in frontmatter). If there is exactly one
     with `status: active` or `status: halted`, propose it. If
     there are several, list them with their last-touched dates
     and ask the user to pick. If there are none, treat this as
     a fresh `start` invocation.

2. Validate the epic doc per `epic-doc-contract.md` (frontmatter
   parses, hashes match, Decomposition present if approved,
   logs present). On validation failure, print the exact
   problem and ask the user to fix the artifact manually. Do not
   auto-repair.

3. Compute each sub-plan's current Status by cross-referencing:
   - The sub-plan entry's stored Status in the Decomposition.
   - The sub-plan's arch-step DOC_PATH frontmatter (`status:
     draft` vs `active`) if DOC_PATH is set and the file exists.
   - The arch-step controller state files for auto-plan and
     implement-loop at both `.codex/` and `.claude/arch_skill/`
     paths.
   - The `arch_skill:block:implementation_audit` block in the
     DOC_PATH if present.
   If the stored Status disagrees with the observed reality
   (e.g., stored `planning` but no auto-plan state and
   consistency-pass is clean), update the stored Status to
   match observed reality before acting. Append an Orchestration
   Log entry naming the discrepancy.

4. Route per `arch-step-integration.md`:
   - First sub-plan with Status `pending` gets `$arch-step new`.
   - Sub-plan with Status `north-star-approved` gets
     `$arch-step auto-plan`.
   - Sub-plan with Status `planning` and state file present: end
     turn (hook drives).
   - Sub-plan with Status `planning` and state file absent:
     advance to `implementing` via `$arch-step implement-loop`.
   - Sub-plan with Status `implementing` and state file present:
     end turn.
   - Sub-plan with Status `implementing` and state file absent
     and audit COMPLETE: run epic critic.
   - Critic verdict drives the next transition per
     `scope-change-discipline.md`.

5. End the turn. The next turn re-runs the same routine. Nothing
   is stored outside the epic doc and arch-step's own state files.

## Why no separate state file for arch-epic

Adding an `arch-epic`-owned state file would introduce a third
source of truth (after the epic doc and arch-step's controller
state). Three sources disagree eventually. Two sources are already
manageable: the epic doc is for orchestration decisions; arch-step's
state files are for live controllers. The skill's job is to read
both every turn.

This also means resuming works across Claude CLI restarts. There
is no volatile cache in RAM that disappears between sessions; the
disk is the state.

## Disagreements between stored Status and observed reality

The most common cause: a previous turn's skill invocation wrote a
Status update but then something happened (user edited the doc,
arch-step's hook advanced further than expected, the user invoked
arch-step commands manually). When reading in step 3 above, the
skill treats observed reality (what arch-step's state files and
the DOC_PATH frontmatter actually say) as authoritative and
updates the stored Status.

Example:
- Stored Status: `planning`.
- Observed: no auto-plan state file, no implement-loop state file,
  but the DOC_PATH's audit block says `Verdict (code): COMPLETE`.
- Action: update stored Status to `implementing`, then advance per
  the Status `implementing` + audit COMPLETE rule (run epic critic).
- Log: `Sub-plan N stored status was 'planning' but observed state
  indicates implementation is complete. Updating and running
  critic.`

The log entry is important — the user reading the epic later sees
the reconciliation happened and why.

## Natural-phrasing hooks

The skill's description field and `When to use` in SKILL.md include
the natural phrasings that map to this single re-entrant pass:

- "continue my epic"
- "keep going on <topic>"
- "pick up where we left off on the <goal> epic"
- "resume <docs/EPIC_*.md>"
- "status of my epic"
- "what's left on this epic?"

All of these land in the same re-entry routine. The status-query
phrasings ("status of my epic", "what's left") trigger `summary`
mode (read-only); everything else triggers the state machine.

## Session-id and cross-restart concerns

arch-step's hook-backed controllers key their state files by
session id. If the user restarts their CLI between turns, the old
session id's state file still exists on disk, and the new session's
state file (when armed) will have a new id.

The skill handles this by scanning for ANY state file matching
`auto-plan-state.*.json` or `implement-loop-state.*.json` whose
payload's `doc_path` matches a sub-plan's DOC_PATH. That means a
sub-plan is `planning` or `implementing` regardless of which
session id armed the controller.

If the skill finds an orphaned state file (state file exists but
the shared controller-contract's staleness sweep has not cleared
it yet), it surfaces to the user: "Found a state file for sub-plan
N's auto-plan from an older session. Is that still running, or
should I disarm it and re-arm fresh?" Recovery procedures are in
`skills/_shared/controller-contract.md` (`--doctor`, `--disarm-all`).

## What the skill does NOT do on resume

- Re-ask decomposition approval if `sub_plans_approved: true`. The
  user already approved the shape.
- Re-ask per-sub-plan North Star if arch-step's DOC_PATH has
  `status: active`. arch-step recorded the approval.
- Re-run the epic critic on a sub-plan already marked `complete`.
  Past verdicts stand.
- Restart a sub-plan from scratch because "something looks weird".
  If something looks weird, surface it to the user with a specific
  question, not a silent reset.
