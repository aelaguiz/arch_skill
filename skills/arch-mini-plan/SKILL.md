---
name: arch-mini-plan
description: "One-pass mini architecture planning for smaller tasks that still need the canonical arch blocks: research grounding, current and target architecture, call-site audit, and a phased plan in one pass. Use when a request asks for a mini plan, compressed arch plan, or single-pass plan without the full multi-step flow. Not for tiny 1-3 phase features (`lilarch`), full multi-step arch execution (`arch-plan`), bug investigations (`bugs-flow`), or open-ended loops."
metadata:
  short-description: "Compressed one-pass arch planning"
---

# Arch Mini Plan

Use this skill for the "mini plan" mode of arch, not for the full multi-step flow and not for `lilarch`.

## When to use

- The user explicitly asks for a mini plan or a one-pass architecture plan.
- The task is small or medium-sized, but still benefits from the canonical arch blocks.
- The user wants planning rigor without walking the full research -> deep dive -> external research -> phase plan sequence as separate steps.

## When not to use

- The task is a tiny feature or improvement that should run through `lilarch`.
- The task clearly needs multi-step checkpoints, deep external research, or long execution. Use `arch-plan`.
- The problem is primarily a bug/regression investigation. Use `bugs-flow`.

## Non-negotiables

- This mode is planning-only. Do not modify code here.
- Use the same arch doc contract and block markers as the full arch flow.
- Keep the phase plan tight: usually 1-2 phases, optionally 3 if cleanup truly needs its own pass.
- If the scope expands beyond a compact one-pass plan, escalate to `arch-plan` rather than pretending mini mode still fits.
- If delegation is allowed, keep it read-only and use it only for scanning or evidence gathering.

## First move

1. Read `references/fit-and-contract.md`.
2. Resolve `DOC_PATH` and read it fully.
3. Verify the North Star and scope are coherent enough to plan against.
4. Then write the canonical arch blocks in one pass.

## Workflow

1. Confirm this is the right mode:
   - smaller task
   - still needs real architecture grounding
   - not a `lilarch` fit and not a full `arch-plan` fit
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
  - next action

## Reference map

- `references/fit-and-contract.md` - fit checks, required blocks, and escalation rules
