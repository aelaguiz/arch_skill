# Delegated implementation for issue and epic delivery

Status: authored and verified; ready for authorized merge and publication.

## User outcome and authority

Keep the expensive coordinator's context available for planning, scope,
integration, and first-hand review while less expensive subagents implement,
run checks, and repair the work. Preserve the existing issue-to-pr and
epic-to-prs workflows. The user explicitly authorized planning on disk,
implementation, merge, and publication of these skill changes.

User correction during implementation: writing skills must not be delegated.
The parent authors all skill contracts, references, prompts, runtime metadata,
and any bundled helper code, including repairs. Workers may run validation
and return evidence, but they must not write or rewrite skill content. This
exception applies within the new execution contract and both delivery callers.

The requested pairings are Astra to GPT-5.6 Sol at high, and Fable to Opus 5.
“Soul” is interpreted as Sol. Sol is an intentional worker selection, so the
general Astra preference must not replace it. The user did not specify an
Opus effort: preserve the user's or harness's applicable choice rather than
inventing a new fixed effort. The active harness supplies agent capabilities,
model identifiers, and spawning and continuation mechanics.

## Skill-authoring design

This is an edit of two delivery skills plus a small reusable execution skill.
The repeated problem is an executive coordinator doing implementation and
test work itself, or inheriting its expensive model into implementation
children. The improvement is bounded delegation with direct parent review.

Representative asks:

1. “issue-to-pr on 4484” under Astra: the coordinator plans and reviews;
   GPT-5.6 Sol high workers implement and verify through final repairs.
2. “epic-to-prs on epic 4700” under Fable: Opus 5 workers implement independent
   issue scopes while the coordinator owns the queue, integration, and reviews.
3. “Keep your context for architecture and review; have workers implement this
   accepted plan”: reuse the same execution contract without adopting an epic
   loop or conductor's full workflow.

Nearest anti-cases are a read-only issue status request, a standalone code
review, and a request for conductor's full plan delivery workflow. None should
accidentally activate issue or epic delivery. A worker implementing a bounded
assignment must not reinterpret this contract as a demand to recreate the
executive coordinator and recursively delegate its own whole assignment.

Use a prompt-only `delegated-implementation` skill. It has a real reusable job
across both delivery lanes and other explicit executive/worker asks. It owns
requirements briefs, the requested worker pairings, parent/worker ownership,
parallel slice judgment, and direct review/repair. `conductor` is a source of
useful principles, not a runtime dependency. The shared orchestration policy
already owns general dispatch semantics; do not clone those into this skill.
The live harness remains authoritative for mechanics. No launcher, resolver,
script, fleet controller, heartbeat, fixed fanout, or new review system is needed.

## Source findings and ownership

`skills/epic-to-prs/SKILL.md` currently allows in-session implementation and
owns the queue, persistent goal, unblocker, and shared Pro consultation cadence.
`skills/issue-to-pr/SKILL.md` directly instructs the working agent to implement,
test, and repair. Both call the shared orchestration policy but leave the
executive/worker split optional. Both currently lack `agents/openai.yaml`.

`skills/conductor/SKILL.md` teaches parent-owned scope and direct artifact
review with delegated implementation and proof, but also introduces extensive
intake, audit, verification, monitoring, and delivery rules. Borrow only the
role economy, coherent task slicing, and review/send-back principle.

`skills/_shared/agent-orchestration-policy.md` already covers host mechanics and
honors deliberate model selections. Leave its global policy and model resolver
unchanged. Callers retain their domain workflow; the new skill owns execution.

`Makefile` explicitly lists installed skills for agents/Codex, Claude, and
Gemini; Hermes follows the agents list. `README.md` owns the visible inventory,
and `docs/arch_skill_usage_guide.md` describes both delivery lanes. Update these
surfaces so the new dependency exists and its ownership is described consistently.

## Implementation requirements

1. Add a lean `skills/delegated-implementation/SKILL.md`. Require the executive
   to delegate implementation, reproduction, tests/checks, and repair; write
   tight outcome/acceptance/scope briefs while leaving implementation judgment
   to workers. State Astra → `gpt-5.6-sol` at `high` and Fable → Opus 5 once.
   Preserve explicit user overrides and inherited worker assignments. Resolve
   launch details from the harness without embedding tool calls or CLI recipes.
2. Require the parent to personally inspect every deliverable and every changed
   line of code, including test code and later repair/integration diffs. Read
   surrounding code as needed to judge behavior, architecture, maintainability,
   and accepted scope. Worker summaries, check results, bots, or external
   reviews do not replace this review. Send accepted findings to workers; the
   parent does not write code patches or execute tests to close its own findings.
   Skill authorship is the explicit exception: all skill writing and repairs
   stay with the parent, while workers may execute validation.
3. Wire both delivery skills to this contract for Astra/Fable coordinators,
   including planning-time reproduction, implementation, CI repairs, and
   post-Pro corrections. Keep the originating executive accountable when an
   epic hands issues to workers. Allow useful independent work in parallel
   without requiring nested coordinators or prescribing agent topology.
   Preserve accepted scope, worktrees, Pro cadence/ownership, unblocker role,
   locally-ready versus merge-ready distinction, and no-merge/no-release bounds.
4. Update descriptions and minimal runtime metadata to reflect the contract.
   Keep explicit invocation for issue-to-pr and epic-to-prs in metadata with
   `allow_implicit_invocation: false`; their authorized skill-to-skill handoff
   remains valid. The new execution helper should be usable by those callers.
   Update Makefile lists, relevant README descriptions, and the usage guide.
   Avoid edits to unrelated skills, conductor, historical evidence, or global
   agent policy.
5. The parent authors this change's skills and related descriptions itself,
   following the user's correction. Use Sol high only for validation, with no
   permission to edit skill prose. The parent writes this plan, reviews every
   edited file/diff, makes prose repairs, and performs authorized Git integration
   and publication. Keep unrelated local work out of commits and installs.
   Commit only explicit session paths.

## Verification and acceptance

The verification worker runs `npx skills check` and records full output in a
temporary artifact. Interpret its actual coverage honestly; it may be an
installed-skill update diagnostic rather than a local package validator.
Validate YAML/frontmatter, description limits, reference resolution, invocation
metadata, and install inventory with available local tooling. Do not add tests
that assert exact doctrine wording.

Exercise representative dry runs from the use cases and anti-cases above.
Include a failed-CI repair after Pro review, an epic worker handoff, and a
skill-authoring issue to test that responsibility and the authorship exception
survive delegation. Verify that Sol/Opus workers can execute their brief without
becoming expensive coordinators. These are prompt
behavior checks, not live provider or GitHub delivery runs. Report that limit.

After authorship, the parent reads every changed line and complete changed
skill, checks for conflicting role language and unnecessary ceremony, and
reviews verification artifacts. The parent repairs skill content; workers
rerun affected checks.

Register the new skill in all applicable Makefile inventories. Validate the
actual installed surface with `make install` and `make verify_install` as part
of publication, plus direct checks of the three affected packages in installed
roots. No application code is changed; Prime Agent's application checks and
tests are outside this repository and task.

## Merge and publish

Work in the isolated `feat/delegated-issue-implementation` worktree based on
`origin/main` at `d566c58`. The source checkout has unrelated untracked work;
preserve it. After review and required verification, commit this plan and only
the named implementation files, fast-forward the source checkout's main when
possible, and push main. If main advances, integrate without discarding work
and review any changed deliverable before publishing. No force push.

Apply `amir-publish`: install locally, then sync the pushed main branch into
`~/workspace/arch_skill` and install on `amirs-m3-max-new`, `amir-m3-36gb`,
`agents@amirs-mac-studio`, and `home`. Current machine `Amir-M5` is the local
install and is skipped as an SSH target. Continue remaining hosts if one fails,
preserve remote changes, and report exact failed actions rather than claiming
cluster completion. The user's session rule to stage only our changes takes
precedence over amir-publish's broad tracked-file staging default.

## Progress and evidence

- [x] Read source skills, authoring contracts, repo rules, and install ownership.
- [x] Save full plan before implementation.
- [x] Implement the execution helper and caller/install integration.
- [x] Worker validation and parent review of every deliverable.
- [ ] Merge, push, install, and verify publication outcomes.

The first Sol implementation launch failed at model capacity. A retry was
interrupted when the user clarified authorship; no worker edits were present.
The parent authored all skill/package changes. Sol high was assigned a separate
read-only validation role while the parent reviewed the complete changed skills,
runtime metadata, install inventory, and documentation diffs.

Sol high verification passed: all three skill packages passed the existing
skill-creator validator; YAML metadata, description lengths, references, and
Makefile inventories passed structural checks; `git diff --check` was clean.
Temporary installs and direct file comparisons passed for Agents/Codex,
Claude, Gemini, and both default/named Hermes roots. Six bounded behavior
walkthroughs found no unresolved contract contradiction, including skill helper
code remaining parent-authored. The parent read the check outputs, structural
validator, and behavior assessment before accepting them.

`npx skills check` exited 0 but was only a global upstream-update diagnostic;
it did not validate this worktree. Its unrelated upstream-deletion warnings did
not cause deletions. The separate local checks above supply package validation.
Full outputs are in `/tmp/delegated-implementation-validation/`. No live issue,
PR, Pro consultation, provider routing, or application tests were exercised.
