# Execution routing: resolve user preferences against real steps

Execution routing is how the orchestrator turns optional user preferences
into per-step runtime/model/effort choices. It exists so a user can say
"do all copywriting steps with Claude Opus 4.7" without forcing every step
onto that model or teaching the skill a hidden taxonomy.

Routing is a manifest-resolution step, not a script concern. The script runs
the runtime/model/effort it is given. The orchestrator decides those values
after it has drafted the real steps from target-repo doctrine.

## Inputs

- The raw user prompt.
- Target-repo doctrine and the drafted StepDescriptors.
- Base execution defaults from `model-and-effort.md`.
- Optional routing preferences extracted from user language.

## Preference shape

Each preference should preserve the user's wording and the orchestrator's
reasoning:

```json
{
  "source_quote": "all copywriting steps using Claude Opus 4.7",
  "applies_to": "steps whose primary artifact is learner-facing copy",
  "step_execution": {
    "runtime": "claude",
    "model": "claude-opus-4-7"
  },
  "resolution_rationale": "The user named a semantic class, so resolve it against step labels, declared instructions, and expected artifacts after manifest drafting."
}
```

`step_execution` applies to worker step sessions. `critic_execution` is
optional and applies only when the user clearly says the critic should use a
different runtime/model/effort. Do not apply worker preferences to critics by
analogy.

If an override omits effort, inherit the base effort for that lane. If it
omits runtime but names a model that only belongs to one runtime family, infer
that runtime and say so in the rationale. If the runtime cannot be inferred
responsibly, ask.

The user's raw wording stays in `source_quote`; `step_execution.model` and
`critic_execution.model` store runnable model identifiers resolved by
`model-and-effort.md`. Do not pass raw shorthand such as `opus-4-7` to a
subprocess when the runtime requires `claude-opus-4-7`.

## Resolution order

For each drafted step, resolve execution in this order:

1. **Runtime feasibility.** A runtime that cannot run the step is invalid.
   If the chosen CLI cannot satisfy the target doctrine or session mechanics,
   do not force it.
2. **Hard target doctrine.** If the target repo or process explicitly requires
   Claude or Codex for a step, honor that unless the user explicitly overrides
   it and accepts the conflict.
3. **Explicit step or label preference.** A user phrase like "step 4 on
   Codex" or "the copy pass on Claude" beats a broader semantic preference.
4. **Semantic category preference.** A phrase like "copywriting steps" applies
   only after comparing it to the drafted step label, instruction, inputs,
   and expected artifact.
5. **Defaults.** Use base step or critic execution defaults when no preference
   applies.

Critic execution resolves independently. The default critic runtime is the
critic default from intake; if missing, it may inherit the step runtime only
when `model-and-effort.md` says that inheritance is unambiguous.

## Matching discipline

Use all available manifest evidence:

- step label
- `skill_or_instruction`
- doctrine path for the step
- expected artifact kind and selector
- input artifacts from prior steps
- target process description

Good resolution:

- "Step 5 is `Write learner-facing hints` and produces
  `lesson-copy.json`; it matches the user's copywriting preference."
- "Step 2 is `Build playable manifest`; although it contains strings, its
  primary artifact is structural JSON, so the copywriting preference does not
  apply."

Weak resolution:

- "The word copy appears in the filename, so use Claude."
- "Claude is usually better at writing, so route copywriting to Claude even
  though the user did not ask."

## Ambiguity and conflicts

Surface unresolved routing in Phase 3 before any step executes.

Ask or pause when:

- a preference matches no drafted steps
- a preference could reasonably match several steps but the cost difference
  matters
- target doctrine requires one runtime and the user asked for another
- a model name does not identify a runtime family clearly
- a model phrase cannot be resolved to a runnable identifier with the same
  family and exact version
- applying a preference to critics would be an inference rather than an
  explicit user instruction

Do not silently ignore a preference. If it is rejected, record why in the
manifest's `execution_preferences` rationale and the Phase 3 table.

## Per-step result

Every StepDescriptor gets both resolved execution blocks:

```json
{
  "step_execution": {
    "runtime": "claude",
    "model": "claude-opus-4-7",
    "effort": "xhigh",
    "source": "execution_preferences[0]",
    "reason": "Matched learner-facing copy artifact lesson-copy.json."
  },
  "critic_execution": {
    "runtime": "codex",
    "model": "gpt-5.5",
    "effort": "xhigh",
    "source": "execution_defaults.critic",
    "reason": "No critic-specific override was provided."
  }
}
```

Repair attempts reuse the same execution block as the original step. Upstream
repairs reuse the reopened step's block. Downstream fresh re-runs use the
confirmed manifest's resolved blocks; the orchestrator does not reinterpret
the user's prompt mid-run.

## Anti-patterns

- Do not build a fixed taxonomy such as copywriting -> Claude or coding ->
  Codex.
- Do not let examples become rules. "Copywriting" is a user-supplied class in
  the example, not a permanent category.
- Do not apply worker preferences to critics unless the user clearly said so.
- Do not hide conflicts by falling back to defaults.
- Do not change model or effort because a step failed. Step failure is handled
  by the diagnose-and-repair protocol, not by changing the runtime.
