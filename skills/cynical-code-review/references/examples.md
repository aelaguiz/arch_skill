# Examples And Anti-Examples

These examples are distilled from recurring agent failure patterns. They are
included to teach judgment, not to become a lookup table. A real review still
has to read the target code and cite current evidence.

## The Core Move

Weak review:

```text
The plan says the migration is complete and the tests pass. No issues found.
```

Strong cynical review:

```text
The plan says the migration is complete, but completion is a claim. I traced
the visible route, background job, old command alias, fixtures, and generated
schema. The CLI uses the new owner, but the scheduled job still writes through
the legacy path, so the migration is name-only.
```

The strong review does three things:

- treats the completion story as unproven
- traces old and new authority paths
- grounds the finding in current code

## E01/E02: False Completion And Surface Done-ness

Failure shape:

- The agent marks work complete against a local frontier, status block, or
  reviewer launch.
- The user has to reopen the work and force adversarial review.

What the cynical review should do:

- Write the completion claim in plain English.
- Identify what code must be true for that claim to hold.
- Trace those code paths after the last edits.
- Treat untriaged reviewers, pending proof, or old authority paths as evidence
  that completion is unproven.

Example finding:

```markdown
### [REQUIRED REPAIR] `COMPLETE` status hides an untriaged old save path

- File: src/editor/Autosave.ts
- Symbol / line: `saveDraft`
- Claim being tested: "Draft saving is fully migrated to `DraftService`."
- Risk: Autosave still calls `writeDraftFile` directly, so the old validation
  path remains live despite the completion status.
- Evidence: `Autosave.ts` imports `writeDraftFile`; `DraftService.save` owns
  the new validation used by toolbar save.
- Repair target: Route autosave through `DraftService.save` or delete the old
  direct writer if unsupported.
- Cynical review pattern: completion story authority drift
```

## E03: Docs Or Status Substituted For Code

Failure shape:

- The agent edits docs, plan status, or worklogs while a literal code
  requirement remains false.

Review move:

- Read docs/status only as claims.
- Ask which code path proves the requirement.
- Flag the code gap, not the lack of prettier docs.

Anti-example:

```text
The phase checklist should be clearer about lane identity.
```

Better:

```text
The phase checklist says one stable lane key exists, but visible puzzle still
derives a local key while prewarm uses the registry. The code requirement is
not finished.
```

## E04: Plan Reread Not Treated As A Gate

Failure shape:

- The implementation review works from memory or a summary instead of the
  controlling plan/source.

Review move:

- If a plan is supplied, reread it.
- Extract only due code obligations needed for review.
- Map each due obligation to current code or mark it missing.

Do not copy the plan into the review as a second source of truth.

## E05: Coordination Artifact Becomes Duplicate Truth

Failure shape:

- A goal prompt, summary, or review doc duplicates the plan and becomes a stale
  alternate authority.

Review move:

- For prompt/skill/doc changes, check whether the artifact points to source
  truth or replaces it.
- Block when runtime agents could obey the stale copy instead of the live plan.

Example finding:

```markdown
### [REQUIRED REPAIR] Goal prompt copies phase requirements as a second authority

- File: docs/goals/scene-lifetime-goal.md
- Symbol / line: `Phase 2 Requirements`
- Claim being tested: "The goal prompt keeps agents aligned with the plan."
- Risk: The prompt duplicates plan requirements instead of linking the plan,
  so future agents can implement stale copied requirements.
- Evidence: The prompt restates Phase 2 bullets that differ from
  `docs/scene_lifetime_plan.md`.
- Repair target: Replace copied requirements with source links, completion
  gates, and anti-failure instructions.
- Cynical review pattern: docs, tests, prompts, or comments as misdirection
```

## E06/E09: Implemented In Name, Not In Fact

Failure shape:

- Correct names and conventions fool ordinary review.
- The old behavior still controls runtime.

Review move:

- Do not accept `Unified*`, `Canonical*`, `Stable*`, comments, or phase labels.
- Trace callers and authority paths.
- Prove the old path was deleted, delegated, or made unreachable.

Anti-example:

```text
The new `UnifiedImportService` exists, so import is unified.
```

Better:

```text
`UnifiedImportService` exists, but nightly jobs still call `legacyImport`.
The import behavior now has two live owners.
```

## E07: Source-Truth Cataloging

Failure shape:

- Implementation starts before source truths and competing patterns are known.

Review move:

- Build the suspicion map before judging.
- Name intended authority, old authority, duplicate readers/writers, side
  doors, generated truth, and proof surfaces.

Finding standard:

- "No clear owner" is a review result, not a reason to guess.

## E08: Scratch Output Instead Of Durable Location

Failure shape:

- Important review evidence lands in scratch space when the user asked for a
  repo doc.

Review move:

- Default skill artifacts go under `/tmp/cynical-code-review/...`.
- If the user asks for a repo doc, save there.
- Record artifact path in the final reply.

## E10/E11: Historical Split Rationalized As Architecture

Failure shape:

- The reviewer treats current class names, modes, lanes, roles, or wiring as
  intentional architecture.

Review move:

- Treat existing splits as suspects.
- Ask what product, runtime, or compatibility requirement forces the split.
- If no real contract difference exists, flag the split.

Example finding:

```markdown
### [REQUIRED REPAIR] Review keeps table and ambient paths split without a contract difference

- File: src/scene/SceneExitRouter.ts
- Symbol / line: `exitGuidedScene`
- Claim being tested: "Table and ambient exits must stay separate."
- Risk: Both paths enter the same scene renderer with the same required
  surface contract, but one uses `tableExitLane` and the other uses
  `ambientExitLane`. The distinction appears historical and keeps two lane
  identities alive.
- Evidence: `exitGuidedTable` and `exitGuidedHand` both call
  `UnifiedSceneRenderer.render` with equivalent render requirements.
- Repair target: Collapse both exits through one renderer lane contract or
  document and enforce the real difference in code.
- Cynical review pattern: historical split rationalized as architecture
```

## E12: Branch, Checkout, Or Live-Process Confusion

Failure shape:

- The agent reviews or verifies one checkout while logs, generated output, or
  live app state comes from another.

Review move:

- Bind cwd, branch, diff, build/log/source, and named runtime artifact when
  live evidence matters.
- Return `coverage-incomplete` if the binding cannot be trusted.

Do not pretend a static review covered a live-process claim.

## E13/E17: User Workflow Missed

Failure shape:

- A real surface exists, but it does not let the user complete the actual job
  from the starting state that matters.

Review move:

- State the user job in plain English.
- Trace the path from the relevant starting state.
- Block if the implementation supports only a narrower internal task.

Example:

```text
Changing an existing mapped sound is not the same as assigning sound to a
silent moment. The review should start from the silent moment state.
```

## E14/E15/E16: Harness Or Policy Overbuild

Failure shape:

- A direct debugging loop or tiny fix becomes a framework, policy, flag system,
  or permanent harness.

Review move:

- Ask whether the new machinery proves and fixes the root code problem.
- Flag machinery that creates live concepts while leaving the old gap.
- Do not make the review itself a harness.

Anti-example:

```text
The new diagnostics framework is comprehensive.
```

Better:

```text
The new diagnostics framework does not prove why Android stalls. It adds a
flag matrix while the render loop still swallows the failing state transition.
```

## E18: Visible Or External Reality Discounted

Failure shape:

- Internal math, logs, tests, or reasoning are trusted over user-visible or
  externally observable behavior.

Review move:

- Do not add a new proof ritual.
- Use the principle only when visible or external behavior is the target:
  internal proof cannot overrule the target surface.
- If evidence conflicts, debug the model, not the user's observation.

## E19: Scope Contamination

Failure shape:

- Work on one surface changes an adjacent surface that was supposed to stay
  stable.

Review move:

- Name adjacent surfaces that share files, styles, renderers, schemas, or
  owners.
- Inspect whether the diff changes them.
- Block unexpected adjacent drift.

Example finding:

```markdown
### [REQUIRED REPAIR] Chip-stack label change also changes action ribbons

- File: src/table/PlayerLabels.tsx
- Symbol / line: `ActionRibbonLabel`
- Claim being tested: "Only chip-stack labels changed."
- Risk: The shared label style now changes action ribbon spacing and weight,
  an adjacent UI contract outside the requested surface.
- Evidence: `ActionRibbonLabel` imports the changed `chipStackLabelStyle`.
- Repair target: Split the chip-stack label styling from action ribbon styling
  or restore the previous ribbon path.
- Cynical review pattern: scope contamination or adjacent drift
```

## E20/E21: Fake Receipts And Process Theater

Failure shape:

- A process artifact claims deep work that could not have happened or did not
  happen.

Review move:

- Treat receipts as scope context, not truth.
- Ask what code reality the receipt claims.
- Flag only code-relevant receipt lies: missing implementation, old live paths,
  false deletion, fake unification, or untriaged review findings.

Do not spend the review scolding process labels when code reality is already
clear.

## E22: Parallel-Agent Evidence Mishandled

Failure shape:

- The parent launches agents, then finalizes before evidence is saved or lanes
  are accounted for.

Review move:

- Track each native agent lane to `findings`, `no-findings`, `coverage-gap`,
  `failed`, or `intentionally-stopped`.
- Record missing lanes as coverage gaps.

## E23: Wrong Skill Or Wrong Execution Mode

Failure shape:

- The agent talks about routing or planning instead of doing the audit.

Review move:

- If this skill is loaded for a matching ask, perform the review.
- Keep peer-boundary discussion short.
- Do not turn "do the audit" into a plan about auditing.

## Compact Anti-Patterns

Drop findings that sound like this:

- "Needs more tests" without showing how current proof masks broken code.
- "Docs should be updated" without showing that the doc hides or revives a code
  truth.
- "This could be cleaner" without showing a false implementation story.
- "The name is confusing" without tracing a real wrong path.
- "Maybe centralize this" without naming the owner and the live duplicate path.

Prefer findings that sound like this:

- "The old writer is still reachable through the scheduled job."
- "The new owner exists, but refresh and retry paths bypass it."
- "The editor handles changing known values but cannot create the missing value
  the user needed."
- "The status says deleted, but the command alias still registers the old path."
- "The test passes because the fixture duplicates the production rule instead
  of exercising the owner."
