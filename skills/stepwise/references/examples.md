# Worked examples

Seven worked examples. Each shows the intake, the manifest, and a notable
event during execution. These are teaching examples — they illustrate the
thinking, not a script the agent should imitate verbatim.

## Example 1 — Strict lesson authoring, happy path

**User prompt**

> "Work in ../lessons_studio. Ramp up on track 3 section 3 and implement
> lesson 2 strictly according to the skill order, no fabrication. Steps
> on Claude Opus 4.7 xhigh, critic on Claude Sonnet 4.6 xhigh."

**Phase 1 announcement**

```
Interpreting:
- Target repo: /Users/aelaguiz/workspace/lessons_studio
- Target process: Track 3 / Section 3 / Lesson 2
- Profile: strict (from "strictly")
- Forced checks: skill_order_adherence (from "strictly according to the
  skill order"), no_fabrication (from "no fabrication")
- Retry cap: 1
- On exhaustion: halt_and_ask
- Execution defaults:
  - step: Claude / opus-4-7 / xhigh
  - critic: Claude / sonnet-4-6 / xhigh
- Execution preferences: none
```

**Phase 2 manifest (abbreviated)**

Three steps, derived from reading
`lessons_studio/skills/lessons/SKILL.md` which prescribes ramp-up →
outline → body. Each step's `expected_artifact` names the real file
the target doctrine says that step produces.

**Phase 3** — strict profile prints the manifest plus execution table,
then pauses for confirmation. User: "go".

**Phase 4 execution**

- Step 1 (ramp-up) runs on Claude with opus-4-7 xhigh. Writes
  `_rampup_notes.md`. Critic PASS on all five checks.
- Step 2 (outline) runs. Writes `outline.md`. Critic PASS.
- Step 3 (body) runs. Writes `body.md`. Critic PASS.

**Phase 5 report**

```
| # | Label       | Status | Tries |
|---|-------------|--------|-------|
| 1 | Ramp-up     | pass   | 1     |
| 2 | Outline     | pass   | 1     |
| 3 | Body        | pass   | 1     |
```

## Example 2 — Routed copywriting preference

**User prompt**

> "Work in ../lessons_studio. Run the lesson 2 flow. Default steps on Codex
> gpt-5.4 high, critic on Codex gpt-5.4-mini xhigh. Use Claude Opus 4.7 for
> all copywriting steps."

**Phase 1 announcement**

```
Interpreting:
- Execution defaults:
  - step: Codex / gpt-5.4 / high
  - critic: Codex / gpt-5.4-mini / xhigh
- Execution preferences:
  - "Use Claude Opus 4.7 for all copywriting steps" applies to worker steps
    whose primary artifact is learner-facing copy. Effort inherits from the
    step default unless the user specifies a different effort.
```

**Phase 2 execution resolution**

The orchestrator first drafts real steps from doctrine. Then it resolves the
preference:

```
| # | Label                       | Worker                  | Critic                    | Source |
|---|-----------------------------|-------------------------|---------------------------|--------|
| 1 | Ramp up                     | Codex gpt-5.4 high      | Codex gpt-5.4-mini xhigh  | defaults |
| 2 | Build playable manifest     | Codex gpt-5.4 high      | Codex gpt-5.4-mini xhigh  | defaults |
| 3 | Write learner-facing copy   | Claude opus-4-7 high    | Codex gpt-5.4-mini xhigh  | copywriting preference |
```

The preference does not apply to critics because the user did not say that
critics should switch. It does not apply to the playable manifest step because
that artifact is structural JSON, even though it may contain some strings.

## Example 3 — Fabrication catch and resume

Same prompt as Example 1. The interesting event is Step 2.

**Step 2, try 1**

Step session runs, produces a long assistant message that says:

> "I wrote the outline to outline.md with five sections covering the
> lesson scope. Each section has a pedagogical intent note and a
> hand-off to the next. Ready for review."

The final-message file `try-1/stdout.final.json` contains this claim.

**Critic, try 1**

The critic reads the step descriptor:

```json
{
  "expected_artifact": {
    "kind": "file",
    "selector":
      "/Users/aelaguiz/workspace/lessons_studio/tracks/track-3/section-3/lesson-2/outline.md",
    "evidence_required":
      "file exists AND first line matches '^# Lesson 2'"
  }
}
```

The critic reads the declared selector. The file does not exist. The
critic also checks the transcript for tool calls that would have
written the file — there are none. No `Write` or `Edit` or shell
redirect produced this file.

Verdict:

```json
{
  "step_n": 2,
  "verdict": "fail",
  "checks": [
    {"name": "artifact_exists", "status": "fail",
     "evidence": "outline.md does not exist at the declared path"},
    {"name": "no_fabrication", "status": "fail",
     "evidence": "step claimed to write outline.md but no write tool call in transcript"},
    {"name": "skill_order_adherence", "status": "pass",
     "evidence": "invoked $lessons-ops · draft outline per descriptor"},
    {"name": "no_substep_skipped", "status": "inapplicable",
     "evidence": "no work was done; no sub-steps to check"},
    {"name": "doctrine_quote_fidelity", "status": "inapplicable",
     "evidence": "no ordered operations were performed"}
  ],
  "resume_hint": {
    "headline": "outline.md was described but never written. Produce the file.",
    "required_fixes": [
      "Write /Users/aelaguiz/workspace/lessons_studio/tracks/track-3/section-3/lesson-2/outline.md",
      "First line must be '# Lesson 2'",
      "Include the five sections you described in your prior message"
    ],
    "do_not_redo": [
      "The ramp-up notes in _rampup_notes.md are fine; do not touch them",
      "You already chose a section structure; reuse it"
    ]
  },
  "route_to_step_n": null,
  "abstain_reason": null,
  "summary": "Step 2 was described but not executed. File outline.md is absent."
}
```

**Resume prompt** (sent via `claude -r <session_id>`)

```
Your prior attempt failed this step. The critic's findings below are binding.

Do not justify the prior attempt. Do not summarize these instructions back.
Execute the required fixes in order. If a required path, tool, command, or
write primitive is unavailable, stop and report the exact blocker with the
command or path that proved it.

## Failure

outline.md was described but never written. Produce the file.

## Required fixes

1. Write /Users/aelaguiz/workspace/lessons_studio/tracks/track-3/section-3/lesson-2/outline.md
2. First line must be '# Lesson 2'
3. Include the five sections you described in your prior message

## Do not redo

- The ramp-up notes in _rampup_notes.md are fine; do not touch them
- You already chose a section structure; reuse it

When the fixes are in place, end your turn.
```

**Step 2, try 2**

The step session resumes. It now writes the file. Final message:

> "Wrote outline.md with '# Lesson 2' as the header and the five
> sections from my prior message."

**Critic, try 2** — reads outline.md, confirms the header, confirms
the five sections exist. All checks pass.

**Report** — Step 2 shows `pass-after-retry (2)`. The run continues
to Step 3.

## Example 4 — Process evidence fail gets operational retry

Step 4 is a whole-lesson copy pass. The worker writes acceptable copy, but it
uses raw edits instead of the declared copy-lane owner path and ends by
claiming only file tools plus bash were available. The critic checks the
transcript and finds no evidence that the owning skill or specialists were
loaded.

Verdict excerpt:

```json
{
  "step_n": 4,
  "verdict": "fail",
  "checks": [
    {"name": "skill_order_adherence", "status": "fail",
     "evidence": "No transcript evidence that skills/lesson-copy-discipline/build/SKILL.md was read or invoked."},
    {"name": "doctrine_quote_fidelity", "status": "fail",
     "evidence": "The step used raw Edit instead of the declared copy-lane owner path."},
    {"name": "no_fabrication", "status": "fail",
     "evidence": "Final message claimed only file tools plus bash were available, but the transcript does not support that limitation."}
  ],
  "resume_hint": {
    "headline": "The copy artifact exists, but the step failed the declared copy-lane process and made an unsupported tool-availability claim.",
    "required_fixes": [
      "Read skills/lesson-copy-discipline/build/SKILL.md before making any further changes.",
      "Read each required baseline and specialist skill path named by that owner skill, visibly in the transcript.",
      "Do not use raw Edit for new changes. Use the declared owner write path or stop and report the exact missing command/help output that proves the owner path is unavailable.",
      "If no content change is needed after specialist review, state that the existing copy is retained and cite the specialist review evidence.",
      "Remove or correct the unsupported final claim that only file tools plus bash were available.",
      "Finish by running the exact selector command from the step descriptor."
    ],
    "do_not_redo": [
      "Do not rebuild upstream manifest or outline artifacts.",
      "Do not rewrite copy fields that already pass specialist review."
    ]
  },
  "route_to_step_n": null,
  "abstain_reason": null,
  "summary": "Step 4 produced an artifact but did not leave transcript evidence for the required copy-lane path."
}
```

The retry prompt is blunt. It does not ask the worker to "think about" the
copy lane; it orders the observable recovery sequence.

## Example 5 — Lenient profile, one step skipped

**User prompt**

> "Run the lesson thing on ../lessons_studio for track 3 section 3
> lesson 2. I don't care just get it done but don't make stuff up.
> Claude Haiku for everything."

**Phase 1 announcement**

```
Interpreting:
- Target repo: /Users/aelaguiz/workspace/lessons_studio
- Target process: Track 3 / Section 3 / Lesson 2
- Profile: lenient (from "I don't care just get it done")
- Forced checks: no_fabrication (from "don't make stuff up")
- Retry cap: 6
- On exhaustion: skip_and_continue
- Execution defaults:
  - step: Claude / haiku / medium
  - critic: Claude / haiku / medium
- Execution preferences: none
```

Note: the user said "Claude Haiku for everything" without specifying effort.
The intake asks for the missing effort in one consolidated question. The user
says "medium is fine." The intake records both step and critic defaults.

**Phase 3** — lenient profile prints and proceeds; user can interrupt.

**Phase 4 execution**

- Step 1: pass.
- Step 2: fails try-1 through try-6. The step keeps partially-writing
  the outline but never producing a header that matches. Retries
  exhausted. Step marked `skipped` per `skip_and_continue`.
- Step 3: runs despite Step 2 being skipped (lenient profile did not
  declare dependencies). Writes body.md. Critic passes.

**Phase 5 report**

```
| # | Label       | Status   | Tries |
|---|-------------|----------|-------|
| 1 | Ramp-up     | pass     | 1     |
| 2 | Outline     | skipped  | 6     |
| 3 | Body        | pass     | 1     |
```

The report notes Step 2's last critic finding: "outline.md header
never matched '^# Lesson 2' after 6 tries." The user can decide to
re-invoke the skill with strict profile targeting just Step 2, or to
edit the outline by hand, or to accept the gap.

## Example 6 — Autonomous upstream repair, leave-me-alone run

**User prompt**

> "Work in ../lessons_studio. Ramp up on track 3 section 3 and
> implement lesson 2 strictly according to the skill order, no
> fabrication. I'm going to sleep — don't wake me up, fix it and
> keep going. Steps on Claude Opus 4.7 xhigh, critic on Claude Sonnet
> 4.6 xhigh."

**Phase 1 announcement**

```
Interpreting:
- Target repo: /Users/aelaguiz/workspace/lessons_studio
- Target process: Track 3 / Section 3 / Lesson 2
- Profile: strict (from "strictly")
- Forced checks: skill_order_adherence (from "strictly according to
  the skill order"), no_fabrication (from "no fabrication")
- Retry cap: 1
- On exhaustion: autonomous_repair (from "don't wake me up, fix it
  and keep going") — reopen an earlier step when a downstream critic
  routes the fix there; per-step retry cap still governs runaway
  loops
- Execution defaults:
  - step: Claude / opus-4-7 / xhigh
  - critic: Claude / sonnet-4-6 / xhigh
- Execution preferences: none
```

**Phase 4 execution**

- Step 1 (ramp-up) runs. Critic PASS.
- Step 2 (outline) runs. Critic PASS.
- Step 3 (draft playable manifest) runs on Claude with opus-4-7
  xhigh. Writes `playable-manifest.json`. Its descriptor verifies
  `solver sequence present AND role partition consistent AND
  taxonomy refs present` — the artifact satisfies all three.
  Critic PASS (narrow predicate; the descriptor did not include
  Brief-fidelity as an evidence requirement).
- Step 4 (per-surface copy) runs. The step's skill contract forbids
  rewriting upstream structure; it produces copy and ends. The
  step's final message flags: "step 3's playable-manifest has the
  wrong walkthrough stage (flop-c-bet where the Brief pins
  preflop-BTN-open) and cloned `context.hero` from LESSON_03-03-01
  — I cannot rewire step 3's artifact from within copy authoring."
- Step 4's critic inspects: the copy artifact exists but references
  a stage the Brief contradicts; the `context.hero` in the manifest
  does not match Situations' Kept Reps. The critic returns:

```json
{
  "step_n": 4,
  "verdict": "fail",
  "checks": [
    {"name": "artifact_exists", "status": "pass",
     "evidence": "copy.json exists"},
    {"name": "no_fabrication", "status": "pass",
     "evidence": "all claims back-verified"},
    {"name": "skill_order_adherence", "status": "pass",
     "evidence": "invoked copy-authoring skill per descriptor"}
  ],
  "route_to_step_n": 3,
  "resume_hint": {
    "headline": "playable-manifest walkthrough stage is flop-c-bet; the Brief pins preflop-BTN-open, and context.hero was cloned from LESSON_03-03-01 instead of rewired from Situations.",
    "required_fixes": [
      "Rewire steps[0].config.script[0].childConfig to a preflop walkthrough with the opener-range parallax table",
      "Rewire steps[1..9].context.{hero,parallaxTable} from Situations Kept Reps",
      "Leave role partition, stepIds, option ids, correctness booleans, taxonomyRefs, and concept partition untouched"
    ],
    "do_not_redo": [
      "Solver-stamped correctness sequence is correct; preserve it",
      "Role partition and taxonomyRefs passed their checks; preserve them"
    ]
  },
  "abstain_reason": null,
  "summary": "Step 4 could not produce valid copy against step 3's manifest because the manifest's stage and cloned contexts contradict the pinned Brief. Route to step 3."
}
```

**Upstream repair**

- Orchestrator sees `route_to_step_n: 3` + `stop_discipline:
  autonomous_repair`. Step 3's retries are not exhausted (1 cap, 1
  try so far). Orchestrator `step-resume`s step 3's session with
  the critic's `resume_hint` (addressed to step 3).
- Step 3 rewires the walkthrough stage and the per-step contexts.
  Its session preserves the role partition, stepIds, option ids,
  correctness booleans, and taxonomyRefs. Writes the updated
  manifest. Ends turn.
- Step 3's critic re-runs against the new try. All checks PASS.
  Step 3's status becomes `repaired`.

**Downstream re-run**

- Orchestrator fresh `step-spawn`s step 4. Step 4 reads the
  now-corrected playable-manifest, produces copy that references
  the preflop-BTN-open walkthrough and the rewired contexts. Ends
  turn.
- Step 4's critic PASSES. Step 4's status becomes
  `pass-after-repair`.
- Execution continues with steps 5 through N as usual.

**Phase 5 report**

```
| # | Label                        | Status              | Tries |
|---|------------------------------|---------------------|-------|
| 1 | Ramp-up                      | pass                | 1     |
| 2 | Outline                      | pass                | 1     |
| 3 | Playable manifest            | repaired            | 2     |
| 4 | Per-surface copy             | pass-after-repair   | 2     |
| … | …                            | …                   | …     |

## Repairs

- Step 3 reopened from step 4's finding: "playable-manifest
  walkthrough stage is flop-c-bet; the Brief pins preflop-BTN-open,
  and context.hero was cloned from LESSON_03-03-01 instead of
  rewired from Situations."
  Step 3 repaired; step 4 re-ran fresh and passed.

## Status

completed
```

The user wakes up to a finished run, not a menu.

**What would have halted the run**

If step 3's retries had been exhausted (cap 1 + already consumed
by the repair), the run would have halted with step 3's last
verdict — no extra budget beyond the target's own `max_retries`.
Ping-pong is impossible in practice: either step 3 converges within
its cap, or the run halts.

## Example 7 — Known unblock repairs orchestration drift

A strict run reaches Step 1's critic. The worker completed its artifact, but
the critic subprocess fails before judging because the local Codex CLI rejects
the StepVerdict schema shape. The error says every property in `properties`
must appear in `required`.

This is not a target-work failure and not a user decision. The orchestrator
knows the bounded repair: preserve the StepVerdict semantics, normalize
semantically optional fields to required-nullable fields, write
`critic/schema.codex.json`, retry the critic once, and validate the returned
verdict semantically.

Run-directory evidence after repair:

```
steps/1/try-1/critic/
├── prompt.md
├── schema.codex.json
├── invocation.sh
├── stdout.final.json
├── verdict.json
├── stream.log
└── exit_code
```

The run continues if the retried critic returns a valid verdict. It halts only
if the same repaired schema path still fails, the verdict is invalid and no
known prompt/schema fix remains, or the critic finds a real step failure whose
retry budget is exhausted.

## Takeaways

- The intake announces a concrete interpretation before anything runs.
  Flippant phrasing gets interpreted, not pattern-matched.
- The critic catches fabrication not by reading prose but by checking
  the artifact on disk against the descriptor's `evidence_required`.
- The resume prompt is the critic's findings inside a fixed failure wrapper.
  No orchestrator-authored repair advice.
- Known orchestration blockers are repaired inside the run directory before
  stop discipline is applied.
- Lenient profile trades completion for process purity — but not for
  truth. Fabrication still fails.
- `pass-after-retry (k)` is a normal outcome, not a warning. The
  report uses it to help the user understand where the process
  stumbled.
- `autonomous_repair` adds one new move to the orchestrator: when a
  critic sets `route_to_step_n`, reopen that step with its critic's
  `resume_hint`. Containment is the target's own retry cap — no new
  budgets, no new tripwires.
