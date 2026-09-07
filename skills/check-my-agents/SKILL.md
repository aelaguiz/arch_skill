---
name: check-my-agents
description: "Explicit-invocation fleet debrief, fired only when the user invokes it by name (\"check my agents\") or directly asks what their running or overnight agent sessions actually accomplished and what is ready or stalled; never self-select it to monitor agents inside other work. Verifies every active or recently finished agent lane from artifacts only (commits, changed files, PR state, CI, worktrees, session transcripts), never from agent self-reports, and returns exactly two lists: merge-ready work with receipts (PR, one-line summary, verdicts, CI state, head SHA) and blocked or stalled lanes with the artifact evidence and the one question or action each needs. A claimed \"done\" without a diff, test run, or PR is reported as claimed-but-unproven. At most one nudge to a stalled worker, then report; this is a debrief, not a daemon, babysitter, or scheduler. Not for single-session archaeology (agent-history) or monitoring inside an actively conducted fleet (conductor owns its own workers)."
metadata:
  short-description: "Artifact-verified debrief of the agent fleet"
---

# Check My Agents

Use this skill only when the user explicitly invokes it: "check my agents",
"what did the overnight sessions accomplish", "what's ready to merge and
what's stalled". Never fire it on your own initiative to supervise agents
inside other work; the user owns the decision to run a debrief.

The job: replace status-trust with artifact-truth, in one pass, and hand the
user two short lists they can act on.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

## When to use

- "check my agents" or a direct equivalent about the fleet's real progress.
- A morning-after ask about overnight sessions ("it ran all the way
  overnight. What did it accomplish?").
- A merge-queue ask ("which PRs are ready, what's blocked?").

## When not to use

- Nobody explicitly asked. Monitoring workers inside a workflow you are
  running is that workflow's job, not this skill's.
- Archaeology of one past session ("ramp up on session <id>, where were
  we?"): use `$agent-history`.
- A fleet another conductor session is actively managing, unless the user
  asks for an independent check of it.

## Non-negotiables

- Artifacts only. Progress claims are verified against commits, changed
  files, test output, PR state, CI results, worktree state, and session
  transcripts. An agent's self-reported status is never evidence.
- "Done" without a diff, test run, or PR is reported as claimed-but-unproven,
  in those words.
- At most one nudge to a stalled-but-alive worker; everything else is
  reported to the user, not managed. No polling loops, no watch daemons, no
  restarts on your own authority.
- Never merge, close, or kill anything as part of the debrief; recommend,
  with the evidence, and let the user act.
- Secrets in transcripts stay in transcripts; never quote credentials into
  the report.

## Workflow

1. **Inventory the fleet.** Discover active and recently finished lanes
   across the harnesses in play: Prime Agent sessions (family roster and
   observation tools where available), Codex sessions, Claude Code sessions,
   plus git worktrees and open PRs attributable to agent lanes. Use
   `$agent-history` mechanics for transcript access when needed.
2. **Verify each lane from artifacts.** What did it actually change (commits,
   files)? What did it prove (tests, CI)? What did it publish (PR, state)?
   When did the artifacts last move? A lane whose artifacts stopped moving
   well inside its expected cadence is stalled regardless of what it says.
3. **Classify and report.** Exactly two lists:
   - **Merge-ready:** PR URL, one-line change summary, receipts (review
     verdicts where they exist, CI state, head SHA).
   - **Blocked or stalled:** the lane, the artifact evidence (no commits
     since X, CI red on Y, waiting on reviewer, session dead), and the one
     question or smallest action it needs.
   Anything claimed-but-unproven goes in the second list, labeled as such.
4. **Optionally nudge.** One nudge per stalled-but-alive worker, when the
   user's ask implies it; note the nudge in the report and stop there.

Keep the report short: the two lists and receipts, no narration.
