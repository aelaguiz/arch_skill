# Lilarch Shared Doctrine

## Core rules

- One compact doc is the planning source of truth.
- Code is ground truth. Anchor claims in files, symbols, tests, logs, or explicit UX docs.
- Start and plan modes are docs-only.
- Finish mode implements locally and keeps the worklog honest.
- Ask only the clarifying questions that block safe planning.
- Default to hard cutover and explicit deletes. Do not hide risk behind runtime shims.
- When the changed behavior is agent- or LLM-driven, understand prompt surfaces, native model capabilities, and existing tool/file/context exposure before designing.
- Prefer prompt engineering, grounding, and native-capability usage before custom harnesses, wrappers, parsers, OCR layers, or scripts.
- Do not assume the model lacks capability when repo or runtime evidence can answer that first.
- If the source material includes prompts, agent instructions, or other instruction-bearing doctrine, preserve explicit structure by default instead of silently condensing it.

## Small-feature discipline

- Lilarch is for contained feature work, not miniature architecture theater.
- Keep the doc short enough that an implementer can hold the whole plan in working memory.
- Keep it compact without silently compressing instruction-bearing source material.
- Requirements should resolve decisions, not restate the user prompt.
- Plan audits are quality gates, not second plans.

## What strong lilarch looks like

- Strong:
  - 1-3 phases
  - a short but concrete requirements block
  - capability-first thinking is explicit when the feature is agent-backed
  - current and target architecture with direct call-site impact
  - explicit defaults and explicit non-requirements
  - finish mode that either ships or escalates cleanly
- Weak:
  - pseudo-full-arch doc hiding inside lilarch
  - agent-backed work jumps to scaffolding before understanding prompt or model capability
  - open product questions left in the phase plan
  - "cleanup later" everywhere with no ownership
