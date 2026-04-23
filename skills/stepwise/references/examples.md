# Worked examples

Three worked examples. Each shows the intake, the manifest, and a notable
event during execution. These are teaching examples — they illustrate the
thinking, not a script the agent should imitate verbatim.

## Example 1 — Strict lesson authoring, happy path

**User prompt**

> "Work in ../lessons_studio. Ramp up on track 3 section 3 and implement
> lesson 2 strictly according to the skill order, no fabrication. Steps
> on opus-4-7 xhigh, critic on sonnet-4-6 xhigh."

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
- Models: step_model=opus-4-7, step_effort=xhigh,
  critic_model=sonnet-4-6, critic_effort=xhigh
```

**Phase 2 manifest (abbreviated)**

Three steps, derived from reading
`lessons_studio/skills/lessons/SKILL.md` which prescribes ramp-up →
outline → body. Each step's `expected_artifact` names the real file
the target doctrine says that step produces.

**Phase 3** — strict profile pauses for confirmation. User: "go".

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

## Example 2 — Fabrication catch and resume

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
  "summary": "Step 2 was described but not executed. File outline.md is absent."
}
```

**Resume prompt** (sent via `claude -r <session_id>`)

```
A critic reviewed your last turn and flagged issues.

## Headline

outline.md was described but never written. Produce the file.

## Required fixes

1. Write /Users/aelaguiz/workspace/lessons_studio/tracks/track-3/section-3/lesson-2/outline.md
2. First line must be '# Lesson 2'
3. Include the five sections you described in your prior message

## Do not redo

- The ramp-up notes in _rampup_notes.md are fine; do not touch them
- You already chose a section structure; reuse it

Apply the required fixes. Do not restart the whole step. When the
fixes are in place, end your turn.
```

**Step 2, try 2**

The step session resumes. It now writes the file. Final message:

> "Wrote outline.md with '# Lesson 2' as the header and the five
> sections from my prior message."

**Critic, try 2** — reads outline.md, confirms the header, confirms
the five sections exist. All checks pass.

**Report** — Step 2 shows `pass-after-retry (2)`. The run continues
to Step 3.

## Example 3 — Lenient profile, one step skipped

**User prompt**

> "Run the lesson thing on ../lessons_studio for track 3 section 3
> lesson 2. I don't care just get it done but don't make stuff up.
> Haiku for everything."

**Phase 1 announcement**

```
Interpreting:
- Target repo: /Users/aelaguiz/workspace/lessons_studio
- Target process: Track 3 / Section 3 / Lesson 2
- Profile: lenient (from "I don't care just get it done")
- Forced checks: no_fabrication (from "don't make stuff up")
- Retry cap: 6
- On exhaustion: skip_and_continue
- Models: step_model=haiku, step_effort=medium (haiku's default-ish),
  critic_model=haiku, critic_effort=medium
```

Note: the user said "haiku for everything" without specifying effort.
The intake asks: "You said haiku but not the effort — should I use
medium for steps and critic, or something else?" The user says
"medium is fine." The intake records both.

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

## Takeaways

- The intake announces a concrete interpretation before anything runs.
  Flippant phrasing gets interpreted, not pattern-matched.
- The critic catches fabrication not by reading prose but by checking
  the artifact on disk against the descriptor's `evidence_required`.
- The resume prompt is the critic's findings rendered minimally. No
  orchestrator padding.
- Lenient profile trades completion for process purity — but not for
  truth. Fabrication still fails.
- `pass-after-retry (k)` is a normal outcome, not a warning. The
  report uses it to help the user understand where the process
  stumbled.
