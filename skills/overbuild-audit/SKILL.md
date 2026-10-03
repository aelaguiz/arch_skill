---
name: overbuild-audit
description: "Audit a plan, spec, issue plan, goal prompt, diff, branch, PR, or finished implementation for overbuilding against what the user actually asked for, and return a cut list: each piece that does not trace to the ask or is heavier than the job, with its one-line simple version and what cutting saves. Use when the user asks whether work is overbuilt, where we are overbuilding, what to rip out, for the simplest version, or whether scope crept; or when a selected planning, delivery, or review skill calls for an overbuild pass before building or before final review. Works on plans before code and on code after. Not for bug hunting or implementation-truth review (cynical-code-review), repo-wide dead-code sweeps with no ask to measure against (cynical-cruft-removal), plan-readiness audits (plan-audit), or resetting an agent's decision frame mid-task (startup-pragmatism)."
metadata:
  short-description: "Cut list for a plan or change measured against the ask"
---

# Overbuild Audit

Measure a plan or an implementation against what the user asked for, and cut
everything else. The output is a cut list: what to delete or never build, the
simple version of each piece, and what cutting saves. It is not a defense of
the work. One pass, review-only unless the user or the calling skill asks you
to apply the cuts.

## Commander's intent

**Build exactly what the user asked for, the simplest way that works, in the
one right place, and let it fail loudly. Anything beyond that is a bug vector
and a maintenance cost for a tiny team.**

What the user wants:

1. **The literal ask, sized for a tiny startup.** The MVP they described, not
   the version an agent imagines they will need later.
2. **One right way.** One path, one owner, one source of truth. New replaces
   old in the same change; git is the archive.
3. **Errors that stay errors.** Throw, crash, report to the error tracker.
   Find the bug rather than hide it.
4. **Reuse over invention.** Existing patterns, the framework used as
   intended, agent judgment instead of scripts and heuristics.
5. **Proportion.** A fix no bigger than the bug, the smallest proof that
   gives confidence, one review, CI at the end.

What the user does not want:

1. **Anything they did not ask for.** Features, screens, modes, "nice to
   haves", and reviewer findings quietly turned into scope.
2. **Armour against hypotheticals.** Flags, fallbacks, retries, guards,
   caches, and gates for problems that have never happened.
3. **Ceremony.** Harnesses, golden sets, receipts, proof systems, review
   rounds, CI waits every turn, approval gates, halt rules.
4. **Old stuff kept alive.** Shims, dual paths, deprecations, quarantines,
   archives, pointer stubs.
5. **Padding in prose.** Over-explained docs, restated doctrine, history
   written into skills and prompts.

**The test:** assume the work is overbuilt and come back with a cut list. For
each piece, can you trace it to what the user asked for? If not, it goes.

**The boundary:** excess is the problem, not ambition. Never cut what traces
to the ask; the user gets angry when asked-for scope shrinks ("I didn't ask
for cheap"). A cut that would remove asked-for behavior goes to the user as a
question.

## When to use

- The user asks whether a plan, PR, branch, diff, or in-flight work is
  overbuilt, where we are overbuilding, what to rip out, what the simplest
  version is, or whether scope crept.
- A selected planning or delivery skill calls for an overbuild pass on its
  written plan before building, or on the change before the final review.
- A review skill's overbuild or subtraction lens needs the type catalog and
  the user's bar.
- You are about to hand over a plan or a change and want to cut your own
  excess first.

## When not to use

- A bug hunt or "is the implementation story true" review: use normal review
  or `$cynical-code-review`.
- A repo-wide hunt for dead or low-value artifacts with no particular ask to
  measure against: `$cynical-cruft-removal`.
- Plan readiness (clarity, completeness, decisions): `$plan-audit`.
- The agent is stuck deciding, over-proving an answer, or refusing to commit
  at partial information: `$startup-pragmatism` resets that frame. Use this
  skill when there is an artifact to cut.

## Non-negotiables

- **Start from the ask, in the user's words.** Authority runs: the user's own
  words, the issue as filed, a plan or scope contract the user approved. An
  agent-written plan revision, a review finding, a worklog, or code that
  already exists is not the ask, even when it is written down.
- **Every piece traces or goes.** A piece stays when the user asked for it, or
  when the asked thing cannot work through its one owner path without it
  (callers migrated, the old path deleted). Everything else is a cut.
- **Traced pieces can still be too heavy.** Cut them to their simple version.
- **Subtraction only.** Never answer overbuild with more machinery: no new
  gate, test tier, review round, flag, or guard as the fix. The fix is
  deletion or a smaller version.
- **One pass.** Do not open a review loop, request re-audits, or spawn review
  rounds. A clean result ends the audit.
- **Asked scope is not yours to cut.** Put it under "Needs the user" with a
  recommendation.
- **One-way doors keep their rigor.** Production data, money, external sends,
  releases, and security boundaries the user set keep real care. Safety
  machinery for hypothetical risks in development and test is still a cut.
- **Be concrete.** Every finding names the piece (file, symbol, section,
  phase, test, step), why it is not needed, the simple version, and what
  cutting saves. No generic advice.
- **"Lean" is a valid result.** Do not pad the list to look thorough.
- **When applying cuts:** delete outright. No deprecation, quarantine, flag,
  archive copy, or pointer stub. Update callers in the same change and delete
  tests that only served the cut piece.

## First move

1. **Find the ask.** Look where the user said it:
   - the issue as filed;
   - the plan's human anchors;
   - the conversation, or the session history (`$agent-history` when
     available).

   The ask often spans several messages. Write it in one or two sentences,
   quoting the user's key words. If there is no recoverable ask, say so and
   audit against the artifact's own stated goal, labeled as a weaker
   yardstick.
2. **Name the target:**
   - **plan:** a plan doc, issue plan, spec, proposal, or goal prompt;
   - **implementation:** a diff, branch, PR, worktree, or running system;
   - **both:** measure each against the ask.

   When a working tree or branch mixes work from several asks, audit only the
   pieces that serve this ask, and name the rest as outside this audit.
3. **Read the references.**
   - Read [references/overbuild-types.md](references/overbuild-types.md)
     before your first audit in a session and whenever a piece is borderline.
   - Read [references/casebook.md](references/casebook.md) for a large plan
     or PR, or when unsure where the line sits.

## Workflow

1. **Inventory every piece.**
   - **Plan:** every component, phase, new file, table, or field, flag or
     mode, test tier or harness, gate, review, CI, or approval step, and doc
     it proposes.
   - **Implementation:** every changed file and new symbol, test, config,
     script, doc, and dependency, plus production and test lines added.
   - **Both:** include anything touched outside the task.
2. **Trace each piece to the ask:**
   - asked for;
   - required for the asked thing to work through its owner path;
   - not asked.
3. **Weigh every traced piece** against the families below. Is it heavier
   than the job?
4. **Check the whole.**
   - Does the codebase come out simpler, or does it gain a system?
   - How does the size compare with your estimate of the simple version?
   - Does the plan imply more review rounds, CI waits, approvals, or phases
     than the work needs?
   - Is anything old still alive beside its replacement?
5. **Write the cut list**, biggest savings first.
6. **Set aside what needs the user:** pieces that trace to the ask but look
   heavy, and pieces whose requiredness is genuinely unclear.

Read-only measurement is in scope and often settles a piece. Count how often a
guard fires on real data, time a lookup, or check whether a variable is ever
set. Never change state to measure.

## The six families

The detail and many real examples of each type are in
[references/overbuild-types.md](references/overbuild-types.md). These are the
questions to run on every piece.

**A. Scope: what got built**
- **Unrequested scope:** features, screens, modes, tools, side quests, or
  coding when only a plan was asked for. What did the user literally ask for?
  What here is not on that list?
- **Speculative generality:** variants, types, scale, or future-proofing
  nobody needs now. Which parts exist only for a hypothetical? At actual
  scale, is this needed?
- **Outside the task:** changes to subsystems, shared contracts, other
  screens, or third-party code. Does every changed file serve the task? Does
  anything behave differently with the feature switched off?
- **Invented rules:** budgets, caps, tiers, safety valves, or algorithm steps
  that trace to nothing the user or the reference said.

**B. Size and shape: how it got built**
- **Heavier than the job:** What is the minimum that would definitely work,
  and how far past it is this? Is the fix bigger than the bug?
- **New layers:** wrappers, adapters, controllers, registries, state
  machines, event or metrics systems, cross-boundary coordination. What does
  the layer buy over a direct call?
- **Flags, modes, options:** feature flags, env vars, kill switches, CLI
  args, dry-run or verbose modes. Could this be one correct way, always on?
- **Guards and gates:** caps, allow-lists, try/except around required things,
  loud invariants, security for a pre-launch dev tool. Would fixing the cause
  remove the guard? Was the risk observed or imagined?
- **Extra state:** caches, leases, timers, history windows, lineage,
  revisions, drafts, stored fields. Is this worth remembering? Can it be
  derived on read?
- **Retry, repair, recovery:** retry loops, background repair, replay on
  read, degraded modes, loading and retry states. Has this failure happened?
  Would failing loudly be simpler and more honest?
- **Heuristic instead of signal:** inferring what the data or the user
  already states. Is there a direct signal being ignored?
- **Code where judgment belongs:** scripts, keyword matching, or
  deterministic gates written to replace a capable agent's judgment. Could a
  clear instruction and the agent's own tools do it?
- **Reinventing:** new code, formats, or processes where an existing owner,
  tool, or framework path already does the job.

**C. Old stuff kept alive**
- **Dual paths and shims:** compatibility layers, deprecations, overloads,
  re-exports, interim mitigations, wrappers added to avoid updating callers.
  Is the old path deleted in the same change?
- **Second owner:** two updaters, two policies, a client copy of server
  rules, a second test stack, documents that repeat each other. Why are
  there two, and which one is canonical?
- **Dead code kept:** unused or test-only code, archives, quarantines,
  pointers, leftover rollout or experiment machinery. Is it used by a real
  user-facing path?
- **Debug residue:** probes, monitors, investigation logging, audit code.
  Which of these was only for the investigation?

**D. Hiding failure**
- **Fallbacks:** silent defaults, relabelled errors, "try the other one",
  empty states that sanction a failure. Would the user rather see this fail?
- **Guessed fixes and hacks:** speculative changes left in, no-effect edits,
  special cases so a test or eval passes. Does each change have a measured
  effect on the diagnosed cause?

**E. Proof and tests**
- **Test sprawl:** harnesses, test databases, fixture platforms, extra test
  tiers, tests for one-time conversions, retesting what did not change.
  What is the smallest set of tests that proves this change?
- **Proof ceremony:** golden sets, drift preventers, certificates, hashes,
  receipts, output schemas, determinism promises, repeated runs. Does anyone
  downstream actually want this proof? Is the proof bigger than the plan?

**F. Process and prose**
- **Process overhead:** review rounds, repeated panel reviews, CI every turn,
  draft PRs, PR stacks, approvals, phase ladders, reruns, extra worktrees.
  Would one of each, at the end, do?
- **Doc and prompt bloat:** over-specified goals, restated doctrine,
  pointers, archaeology, optional phases, several bullets where one line
  would do. Does every line earn its place?
- **Caution and authority plumbing:** approval gates, halt triggers,
  non-negotiables over the user, redaction or policy checks, workflow
  enforcement nobody asked for. Does this dictate the user's workflow?

## Plans and implementations

- **In a plan, look hardest at what is proposed:**
  - scope and speculative generality;
  - the test and proof plan;
  - new layers and reinvention;
  - the process the plan implies: review count, CI cadence, approvals,
    phases.

  Most overbuild starts in the plan, and a cut there costs nothing.
- **In an implementation, look hardest at what remains:**
  - fallbacks, flags, guards, dead and legacy code, debug residue, guessed
    fixes, second owners, and changes outside the task;
  - size against the simple version;
  - whether the code built something the plan forbade.
- **When both exist,** a piece the plan asked for but the user never did is
  still overbuild. Name the plan as its origin, so the next plan does not
  carry it again.

## Where the user wants more

Do not cut these:

- **Scope the user asked for,** however large.
- **Fallbacks the user approved:** visible, counted fallbacks. The rule is
  against silent ones.
- **Tools the user explicitly wanted,** such as a replay harness they asked
  for.
- **Logging the user asked for while debugging.** Removing it later is
  cleanup, not an overbuild finding.
- **Depth of thinking:** requirements, specs, and root-cause understanding.
  The failure is machinery, not thought.
- **Deep root-cause fixes.** Fix the cause once, fully, without adding new
  machinery around it.
- **Real rigor on one-way doors.**

## Output

Reply tight and plain:

- **Ask:** one or two sentences, quoting the user.
- **Verdict:**
  - `lean`: nothing material to cut;
  - `overbuilt`: cuts listed;
  - `needs-decision`: the largest excess traces to something the user may
    have asked for.
- **Size:**
  - implementation: production and test lines added, against your estimate
    of the simple version;
  - plan: how many pieces it has and how many trace to the ask;
  - both: give both.
- **Cut list**, biggest first:

  | Piece | Type | Why it is not needed | Simple version | Saves |
  |---|---|---|---|---|

- **Needs the user:** pieces that trace to the ask but may be heavier than
  it needs, or where it is unclear whether the ask covers them. Give one
  question per item, each with your recommendation.
- **Keep:** pieces that trace to the ask and are needed, listed only when a
  reader would expect you to cut them, each with the reason it stays. Omit
  when empty.

When a calling skill runs the audit, return the same shape. The caller
applies cuts inside its accepted scope and takes "Needs the user" items to
the user once. Save the audit beside the plan or in the worklog when the
caller keeps one; otherwise answer in chat.

## Reference map

- [references/overbuild-types.md](references/overbuild-types.md): every type,
  with the questions and many real examples. Each example gives what was
  built, the user's words, and the simple version. The reference ends with
  how the user phrases the question.
- [references/casebook.md](references/casebook.md): worked audits of plans
  and implementations, end to end, including a lean result and cases where
  cutting would have been wrong.
