---
name: arch-mini-plan
description: "Create or repair a standalone one-pass mini architecture plan that writes the canonical arch blocks into one doc and then hands follow-through to `arch-step`. Use when a request asks for a mini plan, compressed arch plan, or single-pass planning pass without running the full staged arch workflow. Not for tiny 1-3 phase features, bugs, open-ended loops, or full-arch execution."
metadata:
  short-description: "Compressed one-pass arch planning"
---

# Arch Mini Plan

Use this skill for the one-pass mini-plan version of arch: enough rigor to produce the canonical blocks, but not a multi-stage full-arch run.

## When to use

- The user explicitly asks for a mini plan or a one-pass architecture plan.
- The task is small or medium-sized, but still benefits from the canonical arch blocks.
- The user wants planning rigor without walking the full research -> deep dive -> external research -> phase plan sequence as separate steps.
- The likely next step after planning is implementation against the same doc via `arch-step`.

## When not to use

- The task is a tiny feature or improvement that should run through `lilarch`.
- The task clearly needs staged full-arch execution, long-running plan shaping, or full-arch implementation/audit work. Use `arch-step`.
- The problem is primarily a bug/regression investigation. Use `bugs-flow`.
- The path is intentionally open-ended or hypothesis-driven. Use `goal-loop` or `north-star-investigation`.

## Non-negotiables

- This mode is planning-only. Do not modify code here.
- Keep one canonical `DOC_PATH` as the source of truth.
- Use the same canonical arch markers and compatible section shapes that `arch-step` expects.
- Keep the phase plan tight: usually 1-2 phases, optionally 3 if cleanup truly needs its own pass.
- If the scope expands beyond a compact one-pass plan, escalate to `arch-step reformat` rather than pretending mini mode still fits.
- Ask questions only when repo/docs/tools cannot answer them.
- When the changed behavior is agent- or LLM-driven, inspect prompt surfaces, native model capabilities, and existing tool/file/context exposure before designing.
- For agent-backed systems, prefer prompt engineering, grounding, and native-capability use before new harnesses, wrappers, parsers, OCR layers, or scripts.
- If mini mode still concludes that custom tooling is needed for agent-backed behavior, say why prompt-first and capability-first options were insufficient.
- If the real lever is prompt repair, say so plainly and recommend `prompt-authoring` instead of inventing deterministic scaffolding.
- When source material includes prompts, agent instructions, or other instruction-bearing doctrine, preserve explicit structure by default instead of silently condensing it.
- External guidance is optional and narrow. Do not turn mini mode into hidden full-arch research.

## First move

1. Read `references/artifact-contract.md`.
2. Read `references/shared-doctrine.md`.
3. Read `references/fit-and-escalation.md`.
4. Resolve `DOC_PATH` and read it fully.
5. Verify the North Star and scope are coherent enough to plan against.
6. Read `references/quality-bar.md`.
7. Read `references/one-pass-plan.md`.
8. Then write the canonical arch blocks in one pass.

## Workflow

1. Confirm this is the right mode:
   - smaller task
   - still needs real architecture grounding
   - not a `lilarch` fit and not a staged `arch-step` fit
2. Gather the minimum evidence needed:
   - internal ground truth and reusable patterns first
   - external guidance only if correctness depends on it
3. Update the canonical blocks together:
   - research grounding
   - current architecture
   - target architecture
   - call-site audit
   - phase plan
4. Stop with a clear "ready to implement" verdict and the recommended next move.

## Output expectations

- Update `DOC_PATH` only.
- Keep the console summary short:
  - North Star reminder
  - punchline
  - which blocks changed
  - any "too big for mini mode" warning
  - exact next move, usually `arch-step implement` or `arch-step reformat`

## Reference map

- `references/artifact-contract.md` - canonical mini-plan artifact, required blocks, status rules, and handoff contract
- `references/shared-doctrine.md` - evidence, question policy, SSOT rules, and anti-fallback discipline
- `references/fit-and-escalation.md` - concrete fit examples, non-fit examples, and exact escalation rules
- `references/one-pass-plan.md` - the one-pass planning workflow and write order
- `references/quality-bar.md` - strong vs weak bars for the blocks mini mode owns
