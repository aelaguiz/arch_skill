# Strictness profiles: interpret the prompt, do not grep it

The user's prompt carries two kinds of signal that shape execution:

1. A **profile** — strict, balanced, or lenient. This sets retry cap, stop
   discipline, and the default set of critic checks.
2. **Forced checks** — specific checks the user wants regardless of profile
   (e.g. "no fabrication", "strictly in skill order").

The intake reasons about the whole prompt, picks a profile and any forced
checks, and **announces the interpretation back to the user before running**.
There is no keyword lookup table. The agent reads, thinks, and decides.

## Why no table

A keyword table trained on the obvious cases breaks on the non-obvious ones.
"Stop if anything goes sideways" means strict. "Bail on the first real
problem" also means strict. "I want this done right" means strict, maybe. A
table hands you "stop" and "bail" and "right" as keys and teaches the agent
to follow the map instead of reading the message. This skill is a thoughtful
interpreter, not a lookup.

The rule for the agent reading this file: understand what each phrase is
trying to communicate about tolerance, halt behavior, and what the user
cares about most. Pick the profile that honors that. If two phrases point in
opposite directions, ask — do not average them.

Strictness is about how hard the critic checks the work and how much retry
budget the run gets. It is not a permission slip to stop at the first
repairable infrastructure problem. Known, safe, bounded unblocks from
`unblocking.md` happen before stop discipline is applied in every profile.

## What each profile means

### `strict`
The user wants the process followed exactly. Any critic fail is a real
problem. The full check vocabulary runs on every step.

- Retry cap: 0–1. One chance to recover; past that, halt.
- Stop discipline: `halt_and_ask`. Pending steps are not executed.
- Checks run: all five (skill_order_adherence, no_substep_skipped,
  artifact_exists, no_fabrication, doctrine_quote_fidelity).
- Critic posture: adversarial. Prefer fail-on-ambiguity over pass-on-hope.

Strict does not mean "ask sooner when the orchestrator knows the fix." If a
critic schema, prompt, command file, or session parser has a known bounded
repair, repair it, record it, and keep the strict check posture.

Signals that suggest strict: "strict", "no fabrication", "no skipping",
"stop on any error", "exactly", "follow the process", "do it right",
"regulatory/compliance", "this needs to match the spec".

### `balanced`
The user wants the process followed with reasonable tolerance for minor
recoveries. Process drift matters but a stumble that's corrected is fine.

- Retry cap: 3. A few chances to resume and fix.
- Stop discipline: `halt_and_ask` on exhaustion.
- Checks run: artifact_exists, no_fabrication, skill_order_adherence.
- Critic posture: rigorous. Require evidence; tolerate imperfect form.

Signals: no explicit profile cue, or mixed mild signals. Balanced is the
quiet default — pick it when the user did not speak strongly either way.

### `lenient`
The user wants completion more than process purity. They know some corners
will be cut and are accepting that — but still not hallucination.

- Retry cap: 6. Let the step try hard before giving up.
- Stop discipline: `skip_and_continue`. Failed step is marked SKIPPED;
  downstream steps still run.
- Checks run: artifact_exists, no_fabrication.
- Critic posture: pragmatic. Fail on fabrication and missing artifact.
  Do not fail on style or ordering if the user asked to just get it done.

Signals: "just get it done", "I don't care", "whatever works", "best
effort", "lazy pass", "quick and dirty".

## Stop discipline signals

Stop discipline is usually inferred from profile (strict →
`halt_and_ask`, balanced → `halt_and_ask`, lenient →
`skip_and_continue`). It is applied only after known unblocks and the
relevant retry budget are exhausted.

When the user signals they want to be left alone — "don't wake me", "I'm
going to sleep", "fix it and keep going", "run through the night" — set
`stop_discipline = autonomous_repair`. This is compatible with any profile: a
strict + autonomous_repair run still has a tight `per_step_retry_cap`, it just
reopens an earlier step when a downstream critic routes the fix there, instead
of halting.

For ordinary execute/orchestrate requests, prefer bounded autonomous repair of
known blockers over asking. Use `halt_and_ask` as the exhausted-step behavior
when that is the selected discipline, not as a reflex for issues the skill can
already repair inside its own authority.

Containment is the same `per_step_retry_cap` strict or not. Every
reopening of a target step counts as another try on that step. When
the target's retries exhaust, the run halts with the target's last
verdict regardless of the chosen discipline.

Interpret the user's prompt the same way you interpret profile
signals: read the intent, do not keyword-match. A user who says "just
get it done, I'll check in the morning" has signaled leave-me-alone;
a user who says "stop on any structural problem" has signaled
halt-and-ask regardless of their other profile cues.

"Stop on any structural problem" is about target work and manifest semantics.
It does not forbid repairing a malformed schema file, bad prompt render, or
known CLI wrapper drift that prevents the critic from producing the verdict.

## Forced checks

Some phrases in the prompt are not about profile — they are about a specific
check the user will not let go of, regardless of profile:

- "no fabrication" / "no made-up steps" → force `no_fabrication` on.
  (Note: this check is in every profile already; a forced mention means the
  user especially cares and the critic should lean hard on it.)
- "strictly in skill order" / "follow the skill order" → force
  `skill_order_adherence` on.
- "every sub-step" / "no skipping any step" → force `no_substep_skipped`.
- "as the doctrine says" / "in the order the SKILL.md lists" →
  force `doctrine_quote_fidelity`.

When forced checks disagree with the chosen profile, the forced check wins
for that specific check. Example: profile `lenient` + "strictly in skill
order" means cap 6, stop discipline `skip_and_continue`, but
`skill_order_adherence` runs on every step and a violation fails the step.

The intake announces this explicitly: "Lenient profile, but
skill_order_adherence forced on per your 'strictly in skill order' request."

## When to ask

The intake asks one clarifying question, not many. Ask when:

- Two clear signals point at opposite profiles and no ordering cue
  resolves them. Example: "stop on any error … but I don't care just get
  it done" — do you want strict or lenient? The user picks.
- The user named a process but not a target repo, and no repo is obvious
  from cwd.
- The user asked for "strict" but the process has no declared sub-steps,
  so there is nothing concrete to enforce.

Do not ask when:

- The profile is obvious from context, even if no specific word triggered
  it. "I want this lesson authored cleanly" is fine as balanced; no ask.
- The user's instruction implies a reasonable profile. Announce the
  interpretation; the user can override before the Phase 3 gate.

## Worked examples

> "ramp up on track 3 section 3 and implement lesson 2 strictly according
> to the skill order, strict usage, no fabrication of any steps."

Profile: `strict` (from "strict usage" and "strictly according to the skill
order"). Forced checks: `skill_order_adherence` (from "strictly according
to the skill order"), `no_fabrication` (from "no fabrication of any
steps"). Retry cap: 1. Stop discipline: `halt_and_ask` after known unblocks
and the step retry cap are exhausted. Announce and proceed.

> "run the lesson thing, don't stop til it's done, I don't care just get
> it done but don't make stuff up"

Profile: `lenient` (from "I don't care just get it done"). Forced check:
`no_fabrication` (from "don't make stuff up"). Retry cap: 6. Stop
discipline: `skip_and_continue`. Announce and proceed.

> "please follow the process strictly but also just get it over with"

Contradiction. Strict profile and lenient posture disagree. Ask one
question: "Do you want me strict (halt on first fail after one retry) or
lenient (push through and skip what won't resolve)?"

> "author lesson 2 in the curriculum, follow the order, high quality"

Profile: `balanced` (quiet default; "high quality" is not a profile cue,
it is a posture cue). Forced check: `skill_order_adherence` (from "follow
the order"). Retry cap: 3. Stop discipline: `halt_and_ask`. Announce and
proceed.

## How to announce

The announcement is short and names the evidence. Example:

```
Interpreting:
- Profile: strict (from "strict usage")
- Forced checks: skill_order_adherence (from "strictly according to the
  skill order"), no_fabrication (from "no fabrication of any steps")
- Retry cap: 1
- On exhaustion: halt_and_ask
```

When the user has signalled leave-me-alone, the stop line names
`autonomous_repair` instead and explains the containment rule:

```
- On exhaustion: autonomous_repair (reopen an earlier step when a
  downstream critic routes the fix there; per-step retry cap still
  governs runaway loops)
```

If the user disagrees, they correct it in one line before the Phase 3 gate
fires. If they say nothing, the interpretation stands.
