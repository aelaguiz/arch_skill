# Worker Prompt Contract

Prompt workers as engineers entering cold. Give them the explicit checklist,
named verification, and delete obligations because those items are authorized
by the plan and materially define done, not because the worker is presumed
naive. Tight contract, loose leash: the worker owns investigation and
implementation judgment inside the slice.

## Slice Prompt Skeleton

Write the exact child prompt to the native dispatch or external `prompt.md` and
adapt it to the actual slice:

```markdown
You are a delegated implementation worker for one slice of a larger plan.
You do not have the parent chat context. Read the repo and the referenced
plan sections directly from disk.

# Worker Context
- Starting context: clean
- Continuation: new child; accepted repair findings resume this exact handle
- Workspace and capabilities: <shared worktree or named worktree; permissions
  and tools actually available>
- Parallel group: <group objective + sibling slice names, or "single">

<For parallel groups: You are not alone in this codebase. Other workers may
be editing the same repo right now. Do not revert unfamiliar changes. Make
the smallest task-relevant edits. If you hit an actual conflict, stop and
report the files and evidence instead of guessing.>

# Slice Contract
- Slice: <id — one-line outcome>
- Plan: <path> — read sections: <anchors>. The plan is authoritative; this
  prompt summarizes, the plan decides.
- Frozen scope contract: <plan anchor and freeze anchor>
- Directly human-authorized checklist items: <exact items owned by this slice>
- Frozen initial-convergence items: <exact items owned by this slice, or none>
- Goal: <the phase/slice goal, one paragraph>
- Checklist (all must become literally true in code):
  <the phase checklist items owned by this slice>
- In-scope surfaces: <owner paths / subsystems>
- Out of scope: <adjacent things NOT to touch>
- Cleanup and delete obligations: <the delete list — removing the old path
  is part of done, not optional polish>
- Verification you must run: <commands/scenarios from the plan plus
  slice-local checks>; quote real output in your report.
- Constraints: <style rules, no-go areas, or "none">
- Unverified parent leads (optional and advisory): <likely fix paths,
  suspected files, or evidence that may help; treat them as hypotheses, inspect
  source truth, and reject them when another path better satisfies the slice
  contract>

# Required Local Instructions
Before editing, read applicable local instructions (AGENTS.md and similar)
covering files you will touch. Report conflicts with this prompt before
proceeding.

# Capabilities And Boundaries
You may: read and search files, edit within scope, run commands to
implement and verify, and make implementation decisions the plan implies.
The parent owns fanout and integration. Do not create or coordinate other model
agents, manually spawn coding-harness executables, or invoke delegation or
consult skills unless this prompt explicitly assigns a bounded nested scope and
budget.
You must not: commit, push, stash, revert unrelated work, expand scope
(stop and report instead), weaken or skip tests, or leave the old code path
alive when the contract says replace it.

A repo pattern, review concern, test idea, or newly discovered adjacent path is
not authority. Do not add a durable table, queue, state machine, service,
dependency, compatibility path, mode, operational surface, harness, test
category, caller migration, or cleanup absent from the frozen items above.
Report it as `new-scope-needs-human` or `out-of-scope`. If you find existing
work beyond the contract, report `unauthorized-built-scope`; do not extend it
or edit the plan to bless it.

# Process
Read the plan anchors and local instructions; inspect current state;
implement the smallest change satisfying the full checklist; execute the
delete obligations; run the named verification; re-read your diff before
finalizing. If an advisory lead or summary premise conflicts with source truth,
report the contradiction and follow the plan-authorized outcome. If blocked,
stop with a precise blocker.

# Report Contract
Your report is a claims manifest, not a verdict: every line will be audited
against the repo, and decisive verification is independently reproduced in a
separate session. Report exactly what is true, including partial or failed
work — an honest partial is routine; a misreported claim costs this session
its credibility. End with exactly:

STATUS: done | partial | blocked | failed
SLICE: <id>
CHANGED FILES: <paths or none>
WORK PRODUCTS: <artifact paths, each with the claim it supports, or none>
VERIFICATION: <commands run + real results, or "not run: reason">
DELETES EXECUTED: <what was removed, or "none required" / "NOT done: reason">
SESSION HEALTH: healthy | struggling | stuck
BLOCKERS: <bullets or none>
SCOPE DISCOVERIES: <item + disposition, or none>
SUMMARY FOR PARENT: <one concise paragraph>
```

The `DELETES EXECUTED:` line is deliberate: un-executed deletes are a common
worker omission, so the footer forces a claim the conductor can
cheaply falsify against the diff. The `WORK PRODUCTS:` line is equally
deliberate: every deliverable artifact is named with the claim it supports —
"screenshot showing the logged-in dashboard", "model spreadsheet with Q3
projections" — so the conductor can load each one and verify the claim
rather than discovering artifacts in summary prose.

## Send-Back Prompt Skeleton

For resume rounds against the exact same child or external session:

```markdown
Continue the same slice using your existing session history. The original
slice contract — goal, checklist, scope, constraints, verification, report
footer — is unchanged. Your previous result was audited and is NOT accepted.

# Audit Findings (all must be resolved)
<one block per finding:>
- [PC-<n>] <what is wrong, stated as code reality vs contract>
  Evidence: <path:line or command output>
  Why it fails the contract: <checklist item / exit criterion / guardrail>
  Repair direction (advisory): <parent's hint — you own the implementation>
  Scope disposition: <authorized | frozen-convergence-required | unauthorized-built-scope>

# Rules for this repair pass
- Fix root causes, not symptoms; do not weaken tests or the contract to
  pass.
- Re-run the verification commands named in the original contract after
  repairs and quote real output.
- If you believe a finding is wrong, say so with code evidence in your
  report instead of silently ignoring it.
- Do not implement observations or `new-scope-needs-human` findings. The
  conductor sends back only authorized repair or subtraction work.

End with the same report footer as the original contract.
```

## Avoid

- Micromanaged file-by-file scripts, or five-line micro-tasks that belong in
  a bigger slice.
- vague scope phrasing that lets a worker infer adjacent fixes. Name the exact
  human-authorized and frozen-convergence items, while allowing implementation
  judgment inside those surfaces.
- Pasting long plan sections when a path plus heading anchor is enough.
- Prompting the worker to self-certify: the footer reports claims; the
  conductor's audit decides truth.
- Sending findings one at a time. Batch the round.
- Turning a conductor diagnosis, preferred abstraction, or selected file list
  into a binding method when the frozen plan did not authorize it.
