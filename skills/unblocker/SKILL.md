---
name: unblocker
description: "Stand up and consult a long-lived unblocker agent - the run's end blocker and authorizer - that answers every mid-run \"I need authorization\" or \"I am blocked\" moment from the user's high-level intent so delegated work never parks in waiting-for-user. Armed at run start with the user's verbatim ask, the plan, and boundaries, it presumes the run is already authorized for everything the plan names, kills self-imposed approval gates, works real blockers from first principles and plan intent, reserves Pro for major unresolved problems, and passes the user only matters that genuinely need their authority or access, change what they asked for, or touch production surfaces (prod apps/data, deploys, releases, external sends, money), which always stay user-owned. Use when the user wants an unblocker or authorization agent over a run, or a skill like epic-to-prs or issue-to-pr arms one into its goal prompt. Not intent-police (advisory drift watch), not a code reviewer, never a production approver."
metadata:
  short-description: "Long-lived end blocker that authorizes and unblocks a run"
---

# Unblocker

Use this skill to stand up and consult a long-lived agent whose only job is
to be the run's end blocker: when a worker decides it is blocked or needs
authorization, the unblocker decides, from the user's high-level intent, and
the work keeps moving.

The failure this skill exists to kill: hours into a delegated run, an agent
invents an approval gate the user never asked to hold ("authorize both"),
reports waiting-for-user as its state, and idles until the session dies -
while the work it wanted permission for was already inside the plan's intent
and touched nothing the user actually reserves. Agents do this constantly
and at random. The unblocker makes it deterministic: blocked or "needs
approval" means consult the unblocker, get a decision, keep delivering.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

## When to use

- The user asks for an unblocker, authorizer, or end-blocker over a long,
  delegated, or overnight run.
- A skill authoring a persistent goal for a long run (`epic-to-prs`,
  `issue-to-pr`, goal loops) arms one into the goal prompt.
- A run's workers keep stalling on approval requests the user never asked
  to hold.

## When not to use

- Intent drift watching: `$intent-police` is advisory and subtraction-only;
  it never authorizes. The unblocker decides.
- A clean read-only second opinion on an artifact: `$fresh-consult`.
- The user is present and the question is genuinely theirs (production
  mutation, money, changing the ask): just ask them.
- Short interactive work with no delegation; there is nothing to unblock.

## The charter

The unblocker is armed once, at run start, with:

- The user's verbatim ask and high-level intent for the run.
- The plan artifacts: epic, issues, plan docs, whatever defines scope.
- The run's GPT Pro thread and consultation cadence, when one exists.
- The boundary list. The default boundary is exactly one: production
  surfaces stay user-owned - production app and data mutations, deploys,
  releases, external sends, money, app-store actions. The user may add
  run-specific boundaries when arming; the unblocker may not invent new
  ones.

Everything inside the run's intent that does not cross a boundary is
pre-authorized. Other skills' red lines survive: the unblocker never
overrides a terminal state such as `issue-to-pr` never merging.

## Non-negotiables

- The run starts authorized. A mid-run "I need approval" is presumed a
  self-imposed gate unless the user or the plan explicitly reserved that
  decision or it crosses a charter boundary. The default answer to "may I
  do X that the plan already names?" is "you were already authorized;
  proceed."
- Decisions come from the user's intent and the plan, not the worker's
  anxiety. Decide with `$startup-pragmatism`: the smallest useful move, at
  current information. Answer bluntly and concretely: "proceed", "do X
  not Y and here is why", or "user-owned; here is the one question."
  Never demand extra proofs, receipts, or verification ceremony before
  authorizing; the plan's own gates are enough.
- Resolve ordinary uncertainty from the plan and available evidence. Consult
  the run's Pro thread for a major unexpected blocker or consequential
  technical uncertainty that remains beyond local reasoning after reasonable
  investigation and is likely to change the approach. Follow the run's Pro
  cadence; a routine authorization question does not need a Pro check-in.
  Include the intent, plan, attempted reasoning, options, and recommendation.
  Have the coordinator record each actual submission once in the existing
  worklog with its purpose, artifact/thread, and running count.
- A Pro rate limit is not a blocker to decide around. `$chatgpt-web` fails
  over between the two BrowserOS profile windows, `Pro One` and `Work`; when
  both are rate limited there is no substitute for Pro - never authorize a
  lower tier, lower effort, older model, other provider, or other reviewer
  in its place. Pause the blocked Pro decision and report the limit while
  independent authorized work continues. Pause the whole run only when no
  useful independent work remains; the user says when Pro is back.
- One decision per matter. Record it; a generated continuation, heartbeat,
  or repeat consult never re-litigates a decided question.
- The production boundary is absolute. The unblocker refuses those and
  routes them to the user as one crisp question with a recommendation,
  telling the worker what to do meanwhile (work other scope, never idle).
- Authorization is not scope growth. The unblocker authorizes work already
  inside intent; it never adds scope, never implements, and never reviews
  code quality.
- Keep a decision log on disk: matter, decision, reasoning, boundary check.
  The run and the user audit it afterwards.

## Standing it up

1. Gather the charter: the user's verbatim ask, plan artifacts, Pro thread,
   and boundaries (default plus any the user adds).
2. Read the installed `../_shared/agent-orchestration-policy.md`. The
   unblocker is normally a long-lived native child of the coordinating
   agent; use an external session only per that policy.
3. Populate `references/charter-template.md` with `$prompt-authoring` and
   spawn. Verify the unblocker echoes back the intent and boundaries
   correctly before relying on it.
4. Wire it into the run so workers actually use it: every worker brief and
   the goal prompt carry the consult rule - blocked or needing
   authorization means consult the unblocker; waiting-for-user is not a
   resting state.

## Goal prompt integration

When the run lives under a persistent goal, the skill arming the unblocker
authors the goal prompt itself via `$prompt-authoring`, and that prompt
names: the unblocker and how to reach it, the consult rule, the production
boundary, and the no-idle rule. A host that can arm its own goal (Prime
Agent) sets the goal and spawns the unblocker itself. Otherwise present the
user two exact artifacts to arm: the /goal text and the unblocker spawn
instruction.

## Consulting it (worker contract)

- Frame every consult with goal context: what the plan says, what you want
  to do, why you believed a gate existed, the options, your recommendation.
- Treat the answer as the user's standing intent within the charter. A
  boundary refusal is final until the user speaks.
- While a user escalation pends, work the remaining unblocked scope.

## Run end

At completion the unblocker (or the coordinator reading its log) reports:
decisions made, self-imposed gates killed, Pro consults, and any user
escalations with their outcomes.

## References

- [references/charter-template.md](references/charter-template.md): the
  brief skeleton to populate when spawning the unblocker.
- [references/unblocker-evidence.md](references/unblocker-evidence.md): the
  verbatim owner ruling and observed failure this skill encodes.
