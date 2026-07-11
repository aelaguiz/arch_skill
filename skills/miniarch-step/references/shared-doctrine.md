# Arch Step Shared Doctrine

## Communication contract

- Start console output with a one-line North Star reminder.
- Then give the punchline plainly.
- Then give a short natural-English update.
- Do not dump logs, giant lists, or full inserted sections to the console.
- Put deep detail in `DOC_PATH` or `WORKLOG_PATH`.
- Never be pedantic or ceremony-heavy. Optimize for the real task.

## Worktree and execution discipline

- Do not block on unrelated dirty files.
- Ignore unrecognized changes unless they directly conflict with the task.
- The user may be editing or implementing in parallel in the same repo.
- If a task-relevant file changes unexpectedly underneath you, do not revert or overwrite it; stop, name the file, explain the intended edit, and ask the user to say when that file is safe to resume.
- If committing, stage only files you touched unless instructed otherwise.
- When the command is clear, begin the work instead of restating the ask.
- Planning commands are docs-only.
- `implement` and `implement-loop` may change code and must respect branch discipline.

## Convergence rule

- `miniarch-step` always works toward one finished full-arch artifact.
- Local ownership is subordinate to artifact convergence.
- If a command updates one part of the plan and can see that nearby sections are now stale, it should repair the necessary safe set of contradictions before exiting.

## Intent-first gate

Before forming any blocker question, consult the approved intent on the plan doc in this order:

- Section 0 (North Star)
- TL;DR
- Section 7 phase frontier
- any other approved section that constrains the decision

If intent plus repo evidence settles the question, answer it yourself, proceed, and append an `Intent-derived` entry to the Decision Log using the shape in `artifact-contract.md`. Only ask the user when intent plus repo evidence genuinely leave two credible branches that materially change scope, migration burden, compatibility posture, or user-visible truth.

If Section 0 is still draft, weak, or contradictory, that itself is the question. Route back to North Star confirmation; do not invent intent.

The point of this gate is reinforcement. Writing the derivation down is what produces good answers under pressure. Do not skip the Decision Log entry when you answer from intent.

## Question policy

Use repo evidence first.

You must answer anything discoverable from:

- code
- prompt files or agent instructions
- tests
- fixtures
- logs
- docs
- repo tooling
- referenced materials already in the plan

Allowed questions are narrow:

- true product or UX decisions not encoded anywhere
- external constraints not present in repo or docs
- real doc-path ambiguity after best-effort resolution
- missing access or permissions

If a question is still necessary, say where you looked first and ask the exact blocker question instead of offering a guess as if the plan were already decided.

## Blocker-question shape

- Ask only when repo truth plus approved intent leave two credible branches and the choice materially changes scope, migration burden, compatibility posture, or user-visible truth.
- When you ask, present:
  - what you found
  - the default recommendation
  - why that default is strongest
  - what changes if the answer flips
- Strong example:
  - `I found the YAML schema generator plus a neighboring JSON example tied to the same contract. Default: update both now so the contract story stays single-source. If you want a YAML-only first cut, say so; otherwise I will include the JSON example in the same change.`
- Weak example:
  - `Should I also update the JSON example?`

## DOC_PATH resolution defaults

- Use an explicit `docs/<...>.md` path when present.
- If the current session just created or most recently updated one canonical full-arch doc, prefer that doc for later `miniarch-step` commands that omit `DOC_PATH`.
- If multiple candidates exist, prefer the most plan-like doc:
  - canonical headings
  - stable `arch_skill:block:` markers
  - frontmatter with `status` or `doc_type`
- Never choose `*_WORKLOG.md` as `DOC_PATH`.
- If ambiguity survives best effort, ask the user to choose from the top 2-3 candidates.

## Scope model

- Apply `../../_shared/scope-and-convergence.md` as the semantic authority.
- Requested behavior scope comes from the human-authorized outcome.
- During initial plan architecture only, minimal convergence may add the
  evidenced same-contract caller migrations, owner moves, cutovers, or deletes
  needed to avoid competing authority. Record that closure before scope freeze;
  use explicit `none` when no closure is needed.
- After scope freeze, workers and reviewers may not broaden touched files,
  symbols, adopters, proof categories, or product capability beyond the frozen
  contract. A newly discovered adjacent path needs a human decision.
- Bad scope adds new commands, modes, templating, plugin or config layers, dry-run surfaces, speculative tooling, or operational surfaces that were not required by the ask.
- Every plan-backed finding must be dispositioned as `authorized`,
  `frozen-convergence-required`, `new-scope-needs-human`, `out-of-scope`, or
  `unauthorized-built-scope`. Only the first two are automatic repair work.

## Scope, simplicity, and proportionality contract

Treat overbuilding as a known default agent failure mode. Thoroughness feels safe, so an agent can keep adding abstractions, harnesses, edge cases, reviewers, and proof long after the real fix is sufficient. Assume that bias is active. Before adding machinery, ask whether the canonical path can own the behavior, whether existing proof is already enough, and what can be deleted or left unbuilt.

Section 0 must use the Scope and Simplicity Contract from
`references/artifact-contract.md`, including the human authorization anchors,
initial minimal convergence closure or `none`, and scope-freeze boundary.
It also makes these proportionality decisions binding:

- `Smallest sufficient fix`: the narrowest real end-to-end change that resolves the demonstrated failure class at its canonical owner boundary
- `Enough proof`: the smallest credible evidence set that proves the observed failure is fixed, the successful path works, and the important boundary does not regress
- `Do not build`: the tempting frameworks, harnesses, duplicate verifiers, commands, speculative edge-case machinery, or other expansion that must stay out

Match the solution surface and proof surface to the demonstrated failure and blast radius. A systemic problem deserves a systemic fix, but systemic means fixing the shared cause at the narrowest authoritative boundary. It does not mean generalizing one incident into a new subsystem.

Prefer a change that reduces or preserves net system complexity. Large code growth is an overbuild warning, not automatic proof: migration or deletion work can justify a large diff, but new concepts, code paths, operational steps, and test machinery need direct necessity. If the fix adds more machinery than the demonstrated problem requires, stop and simplify.

Every phase-plan item must directly serve the human-authorized outcome, frozen
initial convergence closure, or `Enough proof`. If it serves none, remove it.
Do not preserve rejected overbuild as a follow-up merely because the planner
already imagined it.

The confirmed Scope and Simplicity Contract outranks later plan expansion.
Machinery does not become approved merely because a planner, worker, or reviewer
wrote it into target architecture, a phase checklist, verification, or the
Decision Log. After freeze, remove unauthorized work or obtain explicit human
approval and re-freeze the contract.

During implementation, an unapproved framework, harness, verifier, abstraction,
command, dependency, operational surface, test category, or newly discovered
adjacent path is a hard stop. Classify it as `new-scope-needs-human` before it
is built. Record new approval with the `Scope expansion (human-approved)`
Decision Log shape; legacy `Complexity expansion` entries remain readable.

Testing stays proportional too: cover the demonstrated failure, the successful path, and the most important boundary regression. Add more only for a distinct, demonstrated risk. Do not model every malformed response, lifecycle branch, or hypothetical failure merely because it is possible.

Good example:

- Failure: a deploy can publish artifacts that the real runtime cannot load.
- Smallest sufficient fix: before publication, load the catalog-selected artifacts through the real runtime and prove one real create/close flow; publish completion markers last; run the same probe after startup.
- Enough proof: one invalid release is rejected, one valid release passes, and the live service passes the same probe.
- Do not build: a generalized verification framework, a second integrity subsystem, new diagnostic command families, or exhaustive malformed-response and lifecycle tests.

Bad example:

- Turn that deploy incident into thousands of lines of verifier production code, a broad fake-cloud harness, a second hydration-integrity layer, and dozens of hypothetical response tests. The root fix may be valid, but that solution creates more failure surface than the incident justifies.

## Adjacent-surface rule

- Before locking target architecture or the authoritative phase plan, inspect adjacent surfaces tied to the exact changed contract, source of truth, or migration boundary. This initial architecture window closes at implementation readiness.
- Common adjacent surfaces include sibling formats, readers and writers, embedded examples, fixtures, generated artifacts, mirrored config, live docs, and agent instructions.
- For each adjacent surface, classify one truthful disposition:
  - include in the pre-freeze minimal convergence closure
  - sequence later inside the already-frozen destination map
  - explicitly out of scope
  - blocker question
- If repo truth plus approved intent make the disposition obvious, decide it without asking.
- Do not silently leave a directly competing same-contract path contradictory
  during initial planning. Merely similar siblings do not enter scope.
- A named later phase preserves the destination map; an unnamed deferral is an unresolved decision, not a disposition.
- Pattern similarity, parity, general correctness risk, or reviewer concern can
  shape an authorized implementation but cannot authorize another surface.

## Compatibility posture

- Compatibility posture is a separate plan decision from `fallback_policy`.
- Resolve one truthful posture for each changed contract or migration boundary:
  - preserve the existing contract
  - clean cutover or breaking change allowed
  - timeboxed bridge with explicit removal plan
- Do not assume compatibility merely because it feels safer.
- Do not assume a breaking cutover merely because it looks cleaner.
- If repo truth and approved intent do not settle the posture, ask the exact blocker question before deeper planning.
- `fallback_policy` still governs runtime shims and fail-loud exceptions, not whether a planned cutover is breaking.

## Capability-first rule for agent-backed systems

- If the changed behavior is meaningfully agent- or LLM-driven, understand the current prompt surfaces, runtime or agent configuration, native model capabilities, and existing tool/file/context exposure before designing.
- Do not design around presumed incapability when that fact is discoverable from the repo or runtime surface.
- If capability details remain unclear after inspection, ask narrowly instead of assuming the model lacks them.
- Default decision ladder for agent-backed systems:
  1. prompt change or prompt-structure change
  2. grounding or context-shaping change
  3. better use of existing files, tools, or native capabilities
  4. narrow deterministic support tooling only if the earlier options are insufficient
- Custom tooling for agent-backed behavior must explain which capability-first options were considered, why they were insufficient, and why the tool augments rather than replaces the intended model reasoning.
- Default anti-examples:
  - OCR layers when the runtime already has native vision
  - fuzzy retrieval wrappers when grounded file access and synthesis are the intended path
  - parser, wrapper, or orchestration layers whose main purpose is to make the model act deterministic instead of improving prompt or capability use

## Instruction-fidelity rule for agent and prompt content

- When porting prompts, agent instructions, behavioral doctrine, or other instruction-bearing content, default to structure-preserving transfer rather than summarization.
- Preserve explicit order, step granularity, conditions, hard negatives, escalation logic, and recognition examples when they constrain behavior.
- Do not condense instruction-bearing content unless the artifact explicitly records why that condensation is safe and keeps the original text recoverable.
- Ordinary architecture prose may still be summarized when that does not erase behavioral constraints.

## Alignment checks before deeper work

The North Star is an alignment lock, not a mission statement.

- TL;DR should say what is changing and why.
- Section 0 should say what must remain true while we do it.
- Later commands should be able to resolve ordinary tradeoffs, adjacent-surface scope, and compatibility posture from those sections without re-asking the user.

Before substantive planning or implementation:

- North Star must be concrete and scoped
- claim must be falsifiable
- credible acceptance evidence proportional to the work and risk must be explicit
- requested behavior scope must be explicit
- allowed architectural convergence scope must be explicit enough to tell convergence from product creep
- adjacent-surface dispositions must be explicit enough to tell include-now work from intentional defers or exclusions
- compatibility posture must be explicit enough to tell contract preservation from clean cutover or an approved bridge
- scope must not silently expand
- plan-shaping decisions must be resolved explicitly enough that later commands do not need to guess, invent alternatives, or silently cut requested behavior

If the North Star, requested behavior scope, allowed architectural convergence scope, adjacent-surface scope, compatibility posture, or any other plan-shaping decision is unclear, contradictory, or still branchy, stop, repair what repo evidence can settle, and ask the user the remaining exact blocker question before going deeper.

## Evidence philosophy

- Prefer existing credible signals that genuinely prove the claim.
- For agent-backed systems, prefer prompt, grounding, and native-capability changes before new harnesses or scripts.
- Prefer existing tests, typecheck, lint, build, instrumentation, or log signatures before new harnesses.
- Prefer direct code-path convergence, real runtime guards, or existing behavior checks before inventing any repo-policing validation.
- If no cheap programmatic signal exists, use a short manual checklist.
- Manual verification is usually separate from code completeness until finalization and should not be mistaken for missing code.
- Avoid verification bureaucracy.

Negative-value defaults to avoid:

- deleted-code proof tests
- visual-constant or unstable-golden tests
- doc-inventory gates
- keyword or stale-term grep gates
- file-absence or folder-absence proof checks
- repo-structure policing tests
- CI checks whose primary job is enforcing doc, taxonomy, comment, or naming cleanliness
- helper scripts whose main purpose is auditing docs/help or checking that certain strings are absent
- mock-only interaction tests with no behavior assertion
- bespoke harnesses or frameworks added just to create ceremony
- bespoke harnesses, wrappers, OCR stacks, parsers, or fuzzy match layers added mainly to avoid using native agent or model capabilities
- timing-hack tests when a behavior-level check or smaller signal would do

## Behavior-preservation rule

- Any refactor, consolidation, shared-path extraction, or call-site migration must preserve existing behavior.
- Prefer existing behavior-level checks, integration tests, targeted unit tests, builds, typechecks, instrumentation, or stable manual checklists over new machinery.
- If refactor risk is real and no existing signal buys enough confidence, add a targeted behavior-level, structure-insensitive check that would fail for the right reason.
- Do not call convergence work complete until the preservation signal has actually run.

## Architecture doctrine

- Code is ground truth.
- Prefer the most idiomatic existing repo pattern unless there is a concrete reason not to.
- Search for the canonical existing path before designing a new abstraction or code path.
- Single source of truth is the default.
- Avoid parallel implementations, duplicate writers, and shadow contracts.
- Git is the history for retired live truth surfaces. Do not keep dead competing code paths, stale live docs, stale comments, or stale instructions for archaeology.
- If a touched live doc, comment, or instruction still matters after the change, update it to current truth in the same run instead of leaving a legacy explanation behind.
- Boundaries and invariants should be real in shipped code, runtime routing, types, APIs, or behavior, not outsourced to keyword greps, absence checks, or docs-audit scripts.
- Prefer hard cutover, explicit deletes, and fail-loud boundaries over compatibility shims.
- Runtime fallbacks or shims are forbidden unless the plan explicitly approves them via `fallback_policy: approved` plus a Decision Log entry with a removal plan.

## Scope-authority defaults

- Treat the frozen Scope and Simplicity Contract plus explicit later human
  approvals as authoritative; later agent-authored plan text is not enough.
- During initial architecture only, record the smallest directly competing
  same-contract migration or delete needed for one canonical owner. After
  freeze, implement only that recorded closure. A newly discovered adopter,
  duplicate path, or regression risk needs a human scope decision unless it is
  already inside the frozen contract; do not include it and proceed from repo
  evidence alone.
- If work adds new product functionality, alternate ways of doing the same thing, or speculative architecture, exclude it or record it as follow-up.
- For agent-backed systems, tooling that substitutes for prompt work or native capability use without necessity is architecture theater by default.
- Repo truth proves facts, not scope authority. If requiredness is not anchored
  to the human outcome or frozen initial convergence closure, ask the human
  decision owner. Do not downgrade that uncertainty into follow-up, defer,
  optional, or a silent scope cut.
- Do not remove or relabel approved behavior just because it looks larger than expected. Only the user or explicit plan text can narrow approved intent.
- Stop and ask whenever the plan cannot truthfully become decision-complete without a user choice.
- Feature cut is a hard stop. Any time you are about to remove, downgrade, defer, label-optional, or "simplify away" approved behavior, acceptance criteria, or a phase obligation, stop execution and surface to the user with: what you want to cut, why it looks necessary, what Section 0, TL;DR, and Section 7 say about it, and the exact approval you need. Do not resume until the user explicitly approves. Record the approved cut in the Decision Log using the `Scope cut (user-approved)` shape in `artifact-contract.md`. Silent narrowing is forbidden.

## Warn-first sequencing

Recommended flow:

1. Research
2. Deep dive
3. Phase plan
4. Consistency pass
5. Implement

This is a quality guard, not a hard blocker. Missing passes should be surfaced clearly but should not automatically stop useful work.

## Consistency repair doctrine

- Do not knowingly leave the plan internally contradictory just because the local section you owned is now correct.
- If target architecture changes, check TL;DR, Section 0, Section 1, Section 7, and Section 8 for stale claims.
- If sequencing or verification changes, check TL;DR, Section 0, Section 7, Section 8, and Section 10.
- If rollout or telemetry implications change, check Section 9 and Section 10.
- If adjacent-surface scope or compatibility posture changes, check TL;DR, Section 0, Section 3, Section 6, Section 7, and Section 10.
- If architecture, ownership, or behavior changes, check touched live docs, comments, and instructions and either delete dead truth surfaces or sync surviving ones to reality.
- If prompts, agent instructions, or other instruction-bearing content are being re-homed, check that operational structure was preserved or that any intentional condensation is explicitly recorded with source text still recoverable.
- Prefer direct truthful edits over broad rewrites.
- Record meaningful drift or approved exceptions in the Decision Log instead of silently rewriting history.

## Authoritative surfaces

- `DOC_PATH` is the one planning source of truth.
- `WORKLOG_PATH` is execution evidence, not a second plan.
- Section 7 is the one authoritative execution checklist.
- Helper blocks may sharpen or constrain the plan, but they must not create competing execution surfaces.
- The Decision Log is append-only and should capture real plan drift, approved exceptions, and meaningful sequencing changes.
- Append-only plan history does not justify stale live product docs, stale comments, or retired competing instructions elsewhere in the repo.

## Pattern propagation

- When introducing a new SSOT, contract, lifecycle primitive, or non-obvious sharp edge, note where a short code comment should live at the canonical boundary.
- Prefer a few high-leverage comments over comment spam.
- The point is future drift prevention, not prose volume.

## Quality principle

Presence is not enough.

- A section is only useful when it is concrete enough for later phases to trust.
- A stage is only complete when the sections it owns are both present and strong enough to support downstream decisions without guesswork.
- A plan is not implementation-ready until its plan-shaping decisions are resolved in the main artifact.
- Consistency across sections matters as much as local section quality.
