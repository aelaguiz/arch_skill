# Dispatch routing: resolve transport and execution against real steps

Dispatch routing is how the orchestrator turns the shared native preference,
host capabilities, target doctrine, and optional user preferences into
per-step transport/context choices and any external runtime/model/effort. It
exists so a user can say
"do all copywriting steps with Claude Fable 5" without forcing every step
onto that model or teaching the skill a hidden taxonomy.

Routing is a manifest-resolution step, not a script concern. The orchestrator
chooses transport after it has drafted the real steps from target-repo
doctrine. `run_stepwise.py` runs only an already-selected external
runtime/model/effort; it does not decide that an external process is needed.

## Inputs

- The raw user prompt.
- Target-repo doctrine and the drafted StepDescriptors.
- Active-host native capabilities and any external execution defaults from
  `model-and-effort.md`.
- Optional routing preferences extracted from user language.

## Preference shape

Each preference should preserve the user's wording and the orchestrator's
reasoning:

```json
{
  "source_quote": "all copywriting steps using Claude Fable 5",
  "applies_to": "steps whose primary artifact is learner-facing copy",
  "step_execution": {
    "transport": "external",
    "starting_context": "clean",
    "runtime": "claude",
    "model": "claude-fable-5"
  },
  "resolution_rationale": "The user named a semantic class, so resolve it against step labels, declared instructions, and expected artifacts after manifest drafting."
}
```

`step_execution` applies to worker roles. `critic_execution` is
optional and applies only when the user clearly says the critic should use a
different runtime/model/effort. Do not apply worker preferences to critics by
analogy.

If an override omits effort, inherit the base effort for that lane. If it
omits runtime but names a model that only belongs to one runtime family, infer
that runtime and say so in the rationale. If the runtime cannot be inferred
responsibly, ask.

The user's raw wording stays in `source_quote`; an explicit provider or exact
model preference selects `transport: external` when the native host cannot
honor it. `step_execution.model` and
`critic_execution.model` store runnable model identifiers resolved by
`model-and-effort.md`. When Codex uses Fugu, `step_execution.codex_profile` or
`critic_execution.codex_profile` stores the profile name; the subprocess
command uses `codex exec -p <profile>`. Do not pass raw shorthand such as
`opus-4-7` to a subprocess when the runtime requires `claude-fable-5`.

## Resolution order

For each drafted step, resolve execution in this order:

1. **Transport benefit and feasibility.** Prefer a clean native child when it
   can do the same-host job. Select the external adapter when an explicit
   provider/model request, durability, isolation, automation/receipt, or
   another concrete benefit warrants it. Do not claim a native child has a
   model, permission, background, or worktree capability the host does not
   expose.
2. **External runtime feasibility.** When external transport is selected, a
   runtime that cannot run the step is invalid. Do not force a CLI that cannot
   satisfy target doctrine or continuation mechanics.
3. **Hard target doctrine.** If the target repo or process explicitly requires
   Claude, Codex, or Grok for a step, honor that unless the user explicitly
   overrides it and accepts the conflict.
4. **Explicit step or label preference.** A user phrase like "step 4 on
   Codex" or "the copy pass on Claude" beats a broader semantic preference.
5. **Semantic category preference.** A phrase like "copywriting steps" applies
   only after comparing it to the drafted step label, instruction, inputs,
   and expected artifact.
6. **Defaults.** Use clean native dispatch when no external benefit or hard
   doctrine applies. Use external defaults only within a selected external
   lane.

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
    "transport": "external",
    "starting_context": "clean",
    "continuation": "new-then-exact-resume",
    "runtime": "claude",
    "model": "claude-fable-5",
    "effort": "xhigh",
    "source": "execution_preferences[0]",
    "reason": "Matched learner-facing copy artifact lesson-copy.json."
  },
  "critic_execution": {
    "transport": "native",
    "starting_context": "clean",
    "continuation": "new-each-verdict",
    "runtime": "active-host",
    "model": null,
    "effort": null,
    "source": "shared native preference",
    "reason": "The active host can run the independent critic without an external capability benefit."
  }
}
```

Repair attempts resume the exact worker using the original dispatch block.
Upstream repairs reuse the reopened step's block. Downstream replacement runs
start new clean children from the confirmed manifest's resolved blocks; the
orchestrator does not reinterpret the user's prompt mid-run.

## Anti-patterns

- Do not build a fixed taxonomy such as copywriting -> Claude or coding ->
  Codex.
- Do not let examples become rules. "Copywriting" is a user-supplied class in
  the example, not a permanent category.
- Do not apply worker preferences to critics unless the user clearly said so.
- Do not hide conflicts by falling back to defaults.
- Do not route to an external process merely because the examples name CLI
  models; require the concrete benefit.
- Do not change model or effort because a step failed. Step failure is handled
  by the diagnose-and-repair protocol, not by changing the runtime.
