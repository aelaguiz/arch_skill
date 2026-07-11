# Arch Mini Plan Shared Doctrine

## Core rules

- One doc is the source of truth.
- Apply `../../_shared/scope-and-convergence.md`. Human scope plus the initial
  pre-freeze minimal convergence closure is the only automatic implementation
  scope; later reviewers and implementers cannot add to it.
- Code is ground truth. Anchor claims in files, symbols, tests, logs, or explicit docs.
- Planning is docs-only in this skill. No code edits.
- Ask only for true product, UX, or access gaps that repo evidence cannot answer.
- Default to fail-loud boundaries and hard cutover. Do not hide uncertainty behind runtime shims.
- When the changed behavior is agent- or LLM-driven, understand prompt surfaces, native model capabilities, and existing tool/file/context exposure before designing.
- Prefer prompt engineering, grounding, and native-capability usage before custom harnesses, wrappers, parsers, OCR layers, or scripts.
- Do not answer safety, drift resistance, or cleanup with docs-audit scripts, stale-term greps, absence checks, repo-structure tests, or CI cleanliness gates unless the user explicitly asked for that tooling class.
- Do not assume the model lacks capability when that fact is discoverable from repo or runtime evidence.
- If the source material includes prompts, agent instructions, or other instruction-bearing doctrine, preserve explicit structure by default instead of silently condensing it.

## Mini-mode discipline

- Mini mode compresses the planning passes; it does not lower the quality bar.
- Mini mode may compress planning passes, but it must not silently compress instruction-bearing source content.
- Write only the evidence needed to make the next implementation step safe.
- Keep the result compact enough that one implementer can read the whole thing quickly.
- Prefer one strong phase plan over a bloated "maybe later" backlog.
- Freeze the compact Scope and Simplicity Contract at the ready verdict.

## What good compression looks like

- Strong:
  - one clear North Star
- a small set of repo anchors
- capability-first analysis before new tooling when the work is agent-backed
- instruction-bearing source material keeps explicit structure when it is ported into the plan
- direct current and target architecture
- a concrete call-site audit
- real behavior- or boundary-level checks instead of repo-policing heuristics
- a 1-2 phase plan with obvious deletes and verification
- Weak:
  - vague aspirations instead of architecture
  - jumps to scaffolding for agent behavior before understanding prompt or model capability
  - proposes docs-audit scripts, stale-term greps, absence checks, or repo-layout policing as if they were runtime safety
  - silently condenses prompt or agent doctrine into vague bullets
  - long speculative external research
  - a "future ideas" list standing in for a phase plan
  - unresolved scope fights hidden in the TL;DR
