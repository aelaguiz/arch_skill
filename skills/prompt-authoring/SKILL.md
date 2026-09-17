---
name: prompt-authoring
description: "Write, edit, refactor, or audit prompts and reusable prompt contracts, including Markdown-backed Codex goal prompt files and paste-sized /goal prompts, so they match the user's intent, evidence needs, constraints, completion rules, and output expectations without becoming brittle or overbuilt. Use for casual prompt-writing asks, system/agent/reviewer prompts, prompt repair, anti-heuristic refactors, and findings-first prompt audits; use $skill-authoring for skill packages."
---

# Prompt Authoring

Use this skill when the work is prompt authoring or prompt repair, not generic writing.

The user does not need to name a mode, prompt type, or formal input shape.
Treat casual requests like "write me a prompt that does this" as first-class
prompt-authoring work: infer the prompt shape, make reasonable assumptions,
write or repair the prompt, and only ask when missing information would
materially change the result or create real risk.

Match the recipient's freedom and response depth to the judgment the user
needs. In an expert consultation, preserve its ability to reinterpret evidence
and change the approach. Keep the parent's final presentation requirements
separate: a concise summary for the user does not require a capped assessment
from the expert. A focused verification task may legitimately need a narrower
answer. Apply this distinction to the actual prompt and its supporting inputs.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

## When to use

- The user wants a new prompt, system prompt, skill prompt, agent prompt, reviewer prompt, or reusable prompt contract.
- The user wants an agent prompt to create, resume, replace, or coordinate other model agents without leaving the dispatch semantics implicit.
- The user wants a Codex goal prompt or goal prompt file written or rewritten so an agent can pursue an outcome without guessing done-ness.
- The user describes a job in plain language and wants a prompt that will make a model do it well.
- The user wants `SKILL.md`, skill references, or bundled agent prompts written with prompt-quality discipline.
- The user wants to strengthen an existing prompt without rewriting its entire personality.
- The user wants a prompt refactored so brittle heuristics become examples, rationale, or litmus tests.
- The user wants a findings-first audit of a prompt for myopia, wrong-layer content, weak commander’s intent, or hidden heuristics.

## When not to use

- The task is ordinary copy editing, summarization, or product-spec writing rather than prompt design.
- The user only needs a sentence polished, not a prompt contract repaired.
- The task is skill packaging, runtime metadata, trigger boundaries, install behavior, or validation of a skill package; use `$skill-authoring` instead.
- An existing prompt must be edited or audited, but the prompt text is unavailable.

## Non-negotiables

- Push back against heuristic and myopic prompt design aggressively.
- Do not make the user classify the prompt. Infer the job from normal language and use prompt-type doctrine only as an internal lens.
- If several prompt shapes apply, blend the useful guidance instead of forcing a choice.
- Do not delay casual prompt-writing asks because optional details are missing. Make the best reasonable prompt, then name assumptions briefly if they matter.
- Keep simple relays and same-role revisions to the short audited delta. Use
  a full reusable contract only when the task needs it. Sequencing an approved
  architecture preserves its final destination; it does not authorize redesign.
- Keep commander’s intent mission-level; push concrete behaviors lower into success/failure, recognition tests, process, and examples.
- For Codex goal prompts, prefer a Markdown prompt file when the goal is source-doc-backed, long-running, reviewer-gated, architecture-heavy, or likely to exceed paste-sized form. Use paste-sized `/goal` text only when the user asks for it or the host surface requires it.
- For paste-sized `/goal` prompts, respect the form factor: 4,000 characters is a hard cap, 2,000-3,000 is the usual ceiling for complex goals, and source-doc-heavy goals should usually be shorter.
- For all Codex goal prompts, write a mission brief that teaches judgment; do not turn the goal into a rigid field form, prompt-runner checklist, or duplicated plan doc.
- For execution or repair goal prompts, preserve the user's actual desired world state. Do not soften "make it work" into "diagnose why it did not work" or into a tidy report about non-completion.
- For execution or repair goal prompts, make forward motion explicit: when the path is unclear, the agent should read source truth, form sharper theories, build disproof tests, inspect the real path, use required reviewers to choose the next move, and keep repairing until the desired state is real.
- Teach principles and recognition tests, not keyword lists, lookup tables, or canned action menus.
- When a prompt creates, resumes, replaces, or coordinates another model agent, read the installed sibling policy at `../_shared/agent-orchestration-policy.md` and use its seven dispatch dimensions as the authoring and audit lens: role, transport, starting context, continuation, isolation and capabilities, topology, and return contract.
- Apply that audit to the actual populated child brief before first dispatch
  and after a material reframe, not only to the reusable skeleton. Preserve
  independent judgment by separating authoritative outcomes, facts, decisions,
  and constraints from the caller's hypotheses, preferences, and proposed
  evidence path. The recipient must be free to reject caller conjecture and
  still satisfy the authoritative task.
- For a consultation with GPT-6 Astra Pro, or a Fable or Sol audit brief
  under `$delegated-implementation`, the user's phrasing supersedes this
  skill's scaffold. Write it as he would say it to a colleague, in sentences
  rather than labeled sections: open with what we are building and what the
  finished thing will contain, hand over the sources whole, offer the status
  as a belief, ask one question about intent and say what to look for. No
  verdict token, no answer cap, no scope fence, no commit SHA. Where something
  is being authored, the recipient writes it and the caller asks the
  questions. The family shapes live in
  `../chatgpt-web/references/consultation-templates.md`. A lane the user
  selected for a strict verdict, such as `$fresh-consult` or
  `$codex-review-yolo`, keeps its footer.
- Treat bare `fresh`, `fork`, `resume`, or `parallel` language as ambiguous in an agent prompt unless the prompt gives it an operational meaning or clearly delegates that meaning to the shared policy. Do not infer context, isolation, continuation, or topology from one of those words alone.
- Keep the prompt's role, task-local workflow, and acceptance evidence local. Let the shared policy own reusable cross-skill orchestration semantics instead of copying a mini-policy into the prompt.
- Treat skill prose as prompt prose. Keep it intent-driven and anti-heuristic; leave packaging, trigger metadata, and runtime boundaries to `$skill-authoring`.
- Fix the right section instead of smearing new guidance across the whole prompt.
- Preserve useful prompt magic during refactors by extracting the durable principle and demoting brittle heuristics into examples, rationale, or litmus tests.
- Work only from the prompt and the references listed here; do not assume hidden supporting material.
- If an edit or audit needs missing prompt text, ask for that text. If a creation ask gives a useful brief, proceed from the brief instead of inventing prerequisites.

## First move

1. Infer the job from the user's natural language: create, patch, restructure, or audit. Do not ask the user to choose a lane.
2. Read `references/prompt-pattern-contract.md`.
3. Silently identify the prompt shape or blended shapes: reusable contract, personality/collaboration, outcome-first task, evidence/retrieval, creative drafting, formatting/audience, tool-use/workflow, validation, runtime communication, or implementation planning.
4. If the target prompt dispatches model agents, read `../_shared/agent-orchestration-policy.md` before drafting or auditing it.
5. Read the smallest additional reference that matches the job:
   - `references/codex-goal-prompts.md` when the target artifact is a Codex goal prompt, goal prompt file, paste-sized `/goal` prompt, or persistent goal objective
   - `references/workflow-and-modes.md` for internal work-lane routing and output expectations
   - `references/prompt-types-and-selection.md` when the prompt is not just a reusable agent, skill, reviewer, or workflow contract
   - `references/high-leverage-sections.md` for system context, quality bar, output contracts, and rationale patterns
   - `references/edit-refactor-audit.md` for repair loops, litmus tests, and section-targeting
   - `references/examples-and-anti-examples.md` when you need grounded examples or want to sanity-check framing

## Workflow

1. Lock the user's real job and desired outcome before touching wording.
2. Choose the lightest prompt shape that can work. Use a full sectioned contract only when durability, reuse, tools, validation, or risk justifies it.
3. Blend prompt-type guidance when the job needs it, such as personality plus evidence rules plus completion conditions.
4. For an agent-dispatch prompt, make the seven dispatch choices coherent at
   the point where work is launched and audit the populated brief for hidden
   caller framing. State the choices in the smallest useful place rather than
   turning them into a serialized form or routing table. A fixed template does
   not excuse parent-filled goals, success criteria, reading lists, or
   checklists that silently promote conjecture into authority.
5. Keep commander’s intent and success/failure higher than process mechanics.
6. Make the rich sections carry real weight: system context, quality bar, output contract, evidence policy, completion rules, and error handling should teach stakes and judgment, not just fill space.
7. For goal prompts, put the desired world state first, then only add context, workflow rules, signoff, and evidence requirements that change behavior. Reference authoritative docs by path instead of restating them.
8. Place or repair sections in preferred-pattern order rather than patching opportunistically.
9. Use examples and rationale to illustrate the principle, never to replace the principle.
10. Run the anti-heuristic, overbuild, and hidden-context checks before returning.

## Output expectations

- `author` / create: return the finished prompt, plus only the shortest note needed to explain any important assumption.
- `edit` / patch: return the patched prompt and a short explanation of which section changed and why.
- `refactor` / restructure: return the rewritten prompt and a short note on what useful behavior was preserved versus relocated.
- `audit` / review: return findings first. Name the issue, why it is risky, and exactly which section should change. For an agent-dispatch prompt, identify any missing, conflated, or contradictory dispatch decisions and any caller conjecture laundered into the goal, success bar, evidence boundary, or checklist rather than merely counting vocabulary.

## Reference map

- `references/workflow-and-modes.md` — choose the internal work lane and keep the output shape honest without making users name modes.
- `references/codex-goal-prompts.md` — write Codex goal prompt files and paste-sized `/goal` prompts as outcome-driven mission briefs with source truth pointers, quality bars, evidence, persistence rules, first-class signoff, and no competing source-of-truth duplication.
- `references/prompt-types-and-selection.md` — use prompt types as internal lenses for general-purpose asks, blended prompt shapes, evidence rules, drafting guardrails, runtime communication, validation, and completion behavior.
- `references/prompt-pattern-contract.md` — the contract for section order, ownership, and anti-pattern bans.
- `references/high-leverage-sections.md` — how to make system context, quality bar, schema, and rationale sections actually teach.
- `references/edit-refactor-audit.md` — how to repair prompts without flattening them.
- `references/examples-and-anti-examples.md` — real repo-derived examples and anti-examples; use them to teach, not to cargo-cult.
- `../_shared/agent-orchestration-policy.md` — shared transport, context, continuation, isolation, topology, and return semantics for prompts that dispatch model agents.
