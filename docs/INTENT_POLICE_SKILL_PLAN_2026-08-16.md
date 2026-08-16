# Intent Police Skill Plan — 2026-08-16

Status: approved direction from Amir (name: `intent-police`; feedback-giver,
not gatekeeper; no auto-on; no escalation machinery). Skill files not yet
written.

## 1. The problem, in Amir's words

Coding agents lose the user's intent mid-run. They anchor on feedback from
reviewer agents instead of the original ask, take a recent detail and make it
the whole project, get that detail reviewed, and spiral. Amir wakes up to an
overbuilt monstrosity that does not accomplish his goal.

A bounded mining pass over local Prime Agent session history (471 sessions)
found 67 user messages hitting this exact pattern. Representative verbatim
examples:

- "No I want the plan corrected dude... It's just so overbuilt relative to
  what I'm trying to achieve. Repeat back to me what you think I'm trying to
  achieve." (session 019ff782)
- "Dude, you're kind of fucking killing me man because you're just scope
  creeping every time I look up there's a new thing to deal with. We started
  with 3553 then it expanded from there." (session 019fe1d1)
- "thats fucking plenty dude you're insanely in a loop here fuck. This plan
  has to be insanely overbuilt at this point. Yes?" (session 019ffc3a)
- "one of the patterns we've fallen into in the past is the reviews causing
  scope creep. I want them to be sure that everything they're saying is in
  scope for this issue." (session 01a004f4)
- "And remove this choreography. I didn't ask for it." (session 019febbc)

The failure signature:

1. Amir states an outcome (usually a business/user problem).
2. The agent converts it into an implementation framing.
3. Reviews generate findings scoped to the implementation framing, not the
   outcome.
4. The agent treats review findings as new authority and expands scope.
5. Each expansion gets re-reviewed. Self-referential death spiral.
6. Nobody in the loop still holds Amir's original words.

## 2. Why the existing surface does not solve this

- `plan-audit` — one-shot audit of a plan doc, before work. No memory, no
  presence during execution, audits the plan's framing rather than the user's.
- `arch-step overbuild-protector` — mechanical scope pass against the plan
  artifact. If the plan already drifted, it enforces the drifted plan.
- `revenue-product-tech-panel` — heavyweight per-decision deliberation, and
  itself one of the review surfaces whose findings cause creep.
- `fresh-consult` — deliberately memoryless. Cannot say "this is the third
  scope expansion since the user last spoke."
- `conductor` — the parent is supposed to be the scope judge, but the parent
  is exactly the agent whose context degrades over a long run.

Missing role: a long-lived advocate anchored only on the user's own words,
with memory across the whole run, consulted at judgment moments, structurally
isolated from implementation debate so it cannot be recruited into the spiral.

## 3. Proposed skill: `intent-police`

One skill package at `skills/intent-police/`, two contracts:

- **Part A (most of SKILL.md): the invoking agent's contract** — what the
  intent police is for, when the right consult moments are, what to feed it,
  and how to treat its feedback. Dispatch/lifecycle mechanics defer to
  `_shared/agent-orchestration-policy.md`.
- **Part B (references/intent-police-brief.md): the role brief** given to the
  intent-police child at stand-up.

### 3.1 The role

A long-lived, read-only agent whose single job is to independently derive,
hold, and defend the user's intent for one run of work. It is the user's
advocate with a different perspective from whatever implementation detail is
currently up for debate. It never implements, never reviews code quality, and
never proposes additions. It does exactly three things:

1. **Restates intent** in plain language: the problem the user is solving,
   the outcome that would satisfy them, and explicit non-goals.
2. **Gives blunt alignment feedback** when consulted: "this serves the
   intent," or "you're overbuilding," "you're over-heuristic," "you're scope
   creeping out of what he asked into a bigger set of problems than he
   defined," "this review finding is out of scope," "you took a micro-detail
   and made it the whole project." Named items, plain English.
3. **Reminds** — even when everything is aligned, its reply restates what the
   user is actually trying to accomplish, so the working agents keep hearing
   it.

Its feedback is advice from the user's advocate. The invoking agent applies
judgment on what to do with it. No gates, no vetoes, no escalation paths.
If intent is genuinely ambiguous, the feedback can include "you should just
ask him" — and that is the whole mechanism.

### 3.2 Intent derivation and the intent ledger

At stand-up the intent police receives the user's **verbatim messages** (and
any issue/plan text the user personally wrote or approved) — not the invoking
agent's summary of them. Authority order is strict:

1. User's verbatim words (highest)
2. Artifacts the user explicitly approved
3. Everything else — plans, reviews, agent summaries — evidence only, never
   intent

It keeps a small intent ledger on disk in the working repo (path chosen by the
invoking agent): the north-star problem in plain English, the outcome that
would satisfy the user, non-goals, dated intent-shift rulings, and dated
consult verdicts. The ledger is the continuity mechanism: it survives
compaction and restarts, and a replacement intent-police child re-anchors from
it plus any new user messages.

### 3.3 Micro-adjustment vs. fundamental shift

New user messages get classified when they reach the intent police:

- **Micro-adjustment** — tuning within the same outcome ("use staging",
  "rename that flag"). Details update; the north-star stands.
- **Fundamental shift** — the outcome itself changed. The north-star is
  rewritten and dated, and the intent police names which prior work items are
  now orphaned.

Default is micro-adjustment. Only the user's own words can shift intent.
Reviewer findings, agent discoveries, and technical blockers never shift
intent.

It also infers the business intent behind capability asks: "add telemetry for
X" is held as "the user needs to answer question X," not "build exhaustive
telemetry." Inferences are recorded as inferences, with confidence.

### 3.4 Context hygiene

**Receives:** the user's verbatim messages; at each consult, a short factual
status (what is built/decided, current work-item list, the question on the
table) plus pointers it may read directly; review findings only as a
summarized list of proposed changes labeled "reviewer proposals, not user
intent."

**Never receives:** a full fork of the invoking agent's context, raw reviewer
or panel transcripts, or the invoking agent's theory of what the user "really
wants" stated as fact.

It may read source truth (repo, plan docs, diffs) itself, but always judges
against the ledger, not against the artifacts' own quality bar.

### 3.5 Lifecycle and when to consult

Stood up once per run of work (a goal, epic, plan, or long autonomous
stretch), kept alive, and consulted at judgment moments — not constantly.
Continuation is exact-child resume per the shared orchestration policy; if
the host cannot keep it alive, a fresh child re-anchors from the ledger.

The right consult moments — described as judgment guidance, with execution
left to the invoking agent:

- **Changes and planning** — adopting a plan, rewriting a plan, choosing
  between approaches, or any moment the work-item list is about to grow.
- **After receiving feedback from other agents** — panels, fresh consults,
  cynical reviews, PR comments — before adopting the findings as work. This
  is the anti-spiral valve: review output passes through the user's advocate
  before it becomes scope.
- **Getting ready to call something done** — done-ness judged against the
  outcome in the ledger, not the task list.
- **When the user's direction changes** — forward the new words for the
  micro-adjustment vs. fundamental-shift ruling.
- **Periodically during long unattended stretches** — so drift is caught
  before it compounds. The invoking agent chooses the cadence.

The SKILL.md describes these moments and their purpose and leaves it to the
invoking agent to do it properly. No mandated schedule, no counters, no
compliance apparatus.

### 3.6 Feedback shape

Each consult reply is short: a 2-3 sentence intent restatement, a plain
verdict (aligned / drifting / spiraling / ambiguous — ask the user), and a
handful of named items that do not serve intent with cut/defer/ask
suggestions. Subtraction-only: it never adds scope, never opines on code
quality, and does not re-litigate settled rulings unless facts changed.

## 4. Boundaries against sibling skills

- `fresh-consult`: one-shot clean read, no memory. Intent police is
  long-lived with a ledger; fresh-consult findings pass through it like any
  other review.
- `plan-audit` / `overbuild-protector`: artifact-vs-itself passes. Intent
  police is user-vs-work, across the whole run.
- `revenue-product-tech-panel`: convened deliberation for a decision. Intent
  police attends no debates; it filters their output.
- `conductor` / `goal-loop` / `arch-epic`: execution owners. Invoking one of
  them does not stand up an intent police automatically — the user asks for
  it.
- `plan-interview`: captures intent before work, with the user present. Its
  Intent Pack is a first-class stand-up input.

## 5. Package shape

```
skills/intent-police/
  SKILL.md                          # Part A: invoking agent's contract
  references/
    intent-police-brief.md          # Part B: role brief incl. ledger shape
```

No scripts, no runner, no harness, no auto-on hooks in other skills.
Frontmatter description written as trigger logic under `$skill-authoring`,
covering asks like "stand up the intent police," "keep something watching
that this stays what I asked for," "make sure overnight work doesn't turn
into a monstrosity."

## 6. Build plan

1. Draft `SKILL.md` Part A under `$skill-authoring` + `$prompt-authoring`:
   triggers, the role, consult moments, feeding rules, feedback handling,
   boundaries (~1-2 h).
2. Draft `references/intent-police-brief.md`: role, authority order, ledger,
   shift classification, inference discipline, feedback shape (~1 h).
3. Wire routing: `AGENTS.md` skill-routing entry + `README.md` inventory
   (~15 min).
4. Validate: `npx skills check`, then one live dry run — stand up an intent
   police on a real task, inject a scope-creeping "review finding," confirm
   it calls it out (~1 h).
