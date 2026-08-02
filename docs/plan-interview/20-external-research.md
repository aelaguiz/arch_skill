# External Research: Interview-Style Planning/Spec Frameworks (mid-2026)

Date: 2026-08-02. Web survey of frameworks whose job overlaps the planned
interview skill. Mechanics fetched from primary sources; items marked
*(knowledge)* are from training knowledge.

## 1. GitHub Spec Kit / `specify` CLI

https://github.com/github/spec-kit · https://github.github.com/spec-kit/

- Flow: `/constitution → /specify (what+why, no tech) → /clarify (targeted
  Q&A) → /plan → /tasks → /analyze (cross-artifact lint) → /implement`.
- **/clarify is the interview engine.** Scans the spec against a 9-category
  ambiguity taxonomy, each scored Clear/Partial/Missing: functional scope &
  behavior; domain & data model; interaction & UX flow; non-functional
  attributes; integrations; edge cases & failure handling; constraints &
  rejected alternatives; terminology & consistency; completion signals
  (testable acceptance criteria, DoD).
- Hard budget: **max 5 questions per session**. Question format: the question,
  one "why it matters" sentence, then a table of ≤5 multiple-choice options
  with the **recommended option first plus 1–2 sentences of reasoning**; user
  answers with a letter, "recommended", or ≤5 free words.
- After each answer: append `- Q: … → A: …` to a `## Clarifications` session
  log AND **immediately rewrite the affected spec sections**, replacing
  contradicted text. Ends with a per-category coverage table.
- Spec template: user stories prioritized P1/P2/P3, each "INDEPENDENTLY
  TESTABLE — if you implement just ONE of them, you should still have a viable
  MVP"; numbered FRs; measurable tech-agnostic success criteria; explicit
  `[NEEDS CLARIFICATION: …]` inline markers as the ambiguity currency.
- **/checklist = "unit tests for requirements writing."** Items grade the
  spec's English, never the system: "Is 'prominent display' quantified with
  specific sizing/positioning?" ≥80% of items must cite spec sections.
- **/analyze**: read-only lint across spec/plan/tasks/constitution —
  duplication, vague adjectives, requirements with zero tasks, tasks with no
  requirement, terminology drift; constitution conflicts auto-CRITICAL.

## 2. Amazon Kiro (spec mode)

https://kiro.dev/docs/specs/feature-specs/ · https://kiro.dev/blog/deep-spec-analysis/

- Three artifacts, three phases with **explicit approval gates**:
  `requirements.md → design.md → tasks.md`; "Quick Spec" is the ungated fast
  lane for well-understood work.
- **Draft-first, not question-first**: create a best-guess requirements draft
  from the idea, then iterate. Gate wording: "Do the requirements look good?"
  Iteration rule: "Make one focused change at a time."
- Requirements format: numbered requirements = user story + **EARS acceptance
  criteria** (`WHEN [event] THEN [system] SHALL [response]`, plus IF/WHILE/
  WHERE patterns; "unwanted behaviour" pattern for failure paths). Tasks trace
  back to requirement numbers.
- **Deep spec analysis** (2026): four requirement-bug classes — wrong level of
  detail, ambiguity ("two developers would implement it differently"),
  inconsistency, incompleteness — detected via LLM refinement +
  auto-formalization (SMT) with "semantic entropy" (divergent formalizations =
  ambiguous English); generates concrete accept/reject scenarios for the user
  to confirm intent.
- Reported weakness: pipeline inflates small work ("turned a small bug fix
  into 4 user stories with 16 acceptance criteria").

## 3. BMAD Method (v6)

https://github.com/bmad-code-org/BMAD-METHOD · https://docs.bmad-method.org/

- Persona-based agent team (Analyst, PM, Architect, brainstorming coach, ~30
  personas); 4 phases: Analysis (optional) → Planning (PRD, UX, SPEC.md) →
  Solutioning (architecture, epics/stories, readiness gate) → Implementation.
- PM "builds the PRD section by section rather than spitting out a massive
  document at once"; express and guided modes.
- **Advanced Elicitation** (signature mechanic): a structured second pass over
  the most recent output. Menu of 5 methods picked from a catalog (pre-mortem
  "assume the project already failed, work backward", first principles,
  inversion, red team vs blue team, Socratic questioning, constraint removal,
  stakeholder round table, hindsight 20/20). Shows what each method revealed
  and proposed changes; **never applies without explicit yes**; refinements
  compound.
- Weakness: heavy ceremony; brownfield friction reported.

## 4. Agent OS (Builder Methods) + PRP / context-engineering

https://buildermethods.com/agent-os · https://github.com/Wirasm/PRPs-agentic-eng · https://github.com/coleam00/context-engineering-intro

- **Agent OS**: persistent `agent-os/product/` (mission, roadmap, tech-stack)
  and `agent-os/standards/` extracted from the codebase, so context isn't
  re-taught per prompt. `/shape-spec` must run in plan mode. Shaping question
  sequence: "What are we building?" → "Do you have any visuals to reference?"
  → **"Is there similar code in this codebase I should reference?"** → product
  goal alignment → applicable standards. Output: timestamped spec folder with
  `plan.md`, `shape.md` (decisions and scope), `standards.md`,
  `references.md`, `visuals/`.
- **PRP** ("PRD + curated codebase intelligence + agent/runbook"): `/prp-prd`
  runs a 7-phase gated interview — INITIATE (restate understanding, gate on
  confirmation) → FOUNDATION (Who / What problem / Why can't they solve it
  today / Why now / How will you know) → GROUNDING (parallel web + codebase
  research subagents) → DEEP DIVE (persona, job-to-be-done, non-users,
  constraints) → technical GROUNDING → DECISIONS (MVP, **MoSCoW**, explicit
  out-of-scope, open uncertainties) → GENERATE. PRD includes **"What We're NOT
  Building (explicit deferrals)"**, evidence marked "Assumption" when unproven,
  "TBD - needs research" instead of fluff.
- **/prp-plan quality gates**: "CODEBASE FIRST, RESEARCH SECOND"; every task
  needs ≥1 executable validation command; **"No Prior Knowledge Test: could an
  agent unfamiliar with this codebase implement using ONLY the plan?"**
- context-engineering-intro: `INITIAL.md` = FEATURE (specific) + EXAMPLES
  (curated folder) + DOCUMENTATION + OTHER CONSIDERATIONS (gotchas). "Most
  agent failures aren't model failures — they're context failures."

## 5. Claude Code / Anthropic official + community interview skills

- **Anthropic best practices** (https://code.claude.com/docs/en/best-practices):
  documented "Let Claude interview you" pattern — "Interview me in detail
  using the AskUserQuestion tool… Don't ask obvious questions, dig into the
  hard parts I might not have considered. Keep interviewing until we've
  covered everything, then write a complete spec to SPEC.md." Then **"start a
  fresh session to execute it"**; the best specs are self-contained, "state
  what is out of scope", and end with an end-to-end verification step.
  Proportionality: "If you could describe the diff in one sentence, skip the
  plan." Reviewer caveat: "A reviewer prompted to find gaps will usually
  report some, even when the work is sound… Chasing every finding leads to
  over-engineering."
- **Anthropic feature-dev plugin**: Discovery → parallel codebase explorers
  (each targeting a different aspect, returning 5–10 key files) → Clarifying
  Questions ("one of the most important phases. DO NOT SKIP… Wait for
  answers") → 2–3 competing architecture designs with trade-offs + a
  recommendation → gated implementation → three parallel reviewers.
- **snarktank/ai-dev-tasks** (the ur-create-prd prompt): 3–5 essential
  questions max, numbered with lettered options so the user can answer
  "1A, 2C"; PRD has mandatory **Non-Goals (Out of Scope)**; audience
  calibration: write for a **junior developer**, "explicit, unambiguous, avoid
  jargon."
- **obra/superpowers brainstorming**: check project state first; **one
  question per message**; propose 2–3 approaches with trade-offs; present the
  design **section by section, confirming each**; self-review for
  "placeholders, contradictions, ambiguity, scope"; hard gate on
  implementation until approval.
- **Sorbh/interview-me**: interviews "like a senior architect", one question
  at a time, pushes back on contradictions; outputs spec with decisions log;
  `--verify` mode re-scans code against the spec and reports drift.
- **m4vic/socratic**: 697 questions across 15 domains, **signal-based domain
  loading** (mention "auth" → security domain loads); output contract includes
  assumptions + open questions (ideally 0–3).

## 6. Elicitation research applied to LLMs

- arXiv 2507.02858: LLM follow-up questions **beat human interviewers only
  when guided by an explicit taxonomy of common interviewer mistakes** —
  highest-leverage scaffold for question generation.
- arXiv 2510.12015: sequential adaptive questions (each shaped by prior
  answers) outperform batch dumps.
- EARS (alistairmavin.com/ears): six patterns double as a completeness
  checklist — always-true? on trigger? during state? on failure? optional?
- Classic mappings: 5 Whys ≈ PRP FOUNDATION; user story mapping = journey
  before features; MoSCoW / Non-Goals / PRFAQ = scope-freezing formats.

## 7. Reported failure modes of spec-driven pipelines

- **Markdown factory**: Scott Logic rebuilt a ~1000-line feature via Spec Kit:
  2,577 lines of markdown, ~10x slower than iterative prompting, and the code
  still shipped an obvious bug. "Asking an agent to write 1000s of lines of
  markdown rather than just asking it to write the code is a misuse."
- **Waterfall regression**: front-loaded design does not remove execution
  uncertainty; undocumented decisions accumulate each iteration ("spec
  drift"), and there's no back-channel for folding discoveries into the spec.
- **Ceremony ignores problem size** (Kiro bug-fix inflation) — every surviving
  framework added a proportionality escape hatch.
- **False sense of control**: agents both ignore and over-apply constitutions
  and checklists.
- **Greenfield bias**: tools that spec "from nothing" fail on brownfield
  repos; the interview must start from what exists.
- **Interrogation fatigue** and **batch question dumps** → shallow answers;
  fixes are budgets, defaults, adaptive sequencing.
- **Interview answers ≠ user knowledge**: users can't answer low-level
  questions; surviving frameworks give recommended options, mark assumptions,
  or write "TBD" instead of forcing answers.

## Patterns worth stealing (the shortlist for our skill)

1. **Draft first, interview about the delta** (Kiro) — generate a best-guess
   intent draft from codebase+request; ask only where the draft is uncertain.
2. **Ambiguity taxonomy with per-category coverage state driving question
   order** (Spec Kit /clarify) + end-of-session coverage table.
3. **Recommended-option multiple choice with reasoning; "recommended" is a
   legal one-word answer** (Spec Kit, ai-dev-tasks, AskUserQuestion).
4. **One topic per message, adaptively sequenced; question budget with
   checkpoints** (superpowers, interview-me, arXiv).
5. **Guide question generation with an interviewer-mistake taxonomy** (arXiv
   2507.02858) — for us: Amir's five failure classes ARE that taxonomy.
6. **Write answers back into the artifact immediately, replacing contradicted
   text; keep a separate Q→A log** (Spec Kit).
7. **Interview context separated from execution context; the artifact is the
   only carrier** (Anthropic).
8. **Parallel codebase explorers each targeting a different aspect, returning
   key files** (feature-dev) — the "immerse" stage.
9. **Growing artifact folder: plan + decisions/scope + references + visuals as
   separate files** (Agent OS) — the "doc pack".
10. **No Prior Knowledge Test** as the acceptance bar (PRP) — matches Amir's
    "such that a lesser agent could implement it."
11. **Decisions log with rejected alternatives** (interview-me, PRP).
12. **Mandatory Non-Goals / "What We're NOT Building"** (everyone).
13. **EARS / Given-When-Then for acceptance criteria** where testability
    matters (Kiro, Spec Kit).
14. **"Checklists as unit tests for requirements writing"** — grade the pack's
    English before freezing (Spec Kit /checklist).
15. **Elicitation-method second pass (pre-mortem, red team) applied only with
    explicit yes** (BMAD).
16. **Competing approaches (2–3) with trade-offs + recommendation before
    locking a design decision** (feature-dev, superpowers).
17. **Section-by-section confirmation; self-review for placeholders /
    contradictions / ambiguity / scope before showing the user** (superpowers).
18. **Proportionality gate / quick lane** (Kiro Quick Spec, Anthropic
    one-sentence rule).
19. **Audience calibration: artifact written for a junior developer, plain
    English** (ai-dev-tasks) — the artifact side of the no-jargon rule.
20. **Drift verification**: re-scan code against the frozen artifact after
    implementation (interview-me `--verify`) — in our suite this is already
    owned by cynical reviews + plan-audit; the pack just has to be precise
    enough to triage against.
