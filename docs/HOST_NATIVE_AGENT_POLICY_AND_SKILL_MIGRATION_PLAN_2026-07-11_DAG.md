# Host-Native Agent Policy and Skill Migration Audit DAG

Date: 2026-07-11
Scope: all 46 locally authored live packages at `skills/<slug>/SKILL.md`
Coverage: 46/46 packages, owned exactly once across three clean native walkers (16 + 15 + 15)
Edges: 182 distinct literal semantic relationships; unresolved targets: 0
Extraction contract: dollar-prefixed peer tokens plus exact resolving backticked unprefixed peer slugs in relationship-bearing prose; fenced code, indented code, variables, commands, modes, filenames, self-references, and inert examples are excluded

## Surface A: relationship graph

```mermaid
flowchart LR
    classDef router fill:#FFE4B5,stroke:#B54708,stroke-width:2px
    classDef orchestrator fill:#FFF4D6,stroke:#B54708
    classDef stage fill:#FFFFFF,stroke:#B54708
    classDef specialist fill:#E6F4FF,stroke:#1E5FA8
    classDef primitive fill:#E8F5E8,stroke:#067647
    classDef presentation fill:#F4E6FF,stroke:#6B2FB3
    classDef diagnostic fill:#F0F0F0,stroke:#666,stroke-dasharray:4 2
    classDef external fill:#F8F8F8,stroke:#999,stroke-dasharray:2 2
    classDef unresolved fill:#FFE4E1,stroke:#B54708,stroke-dasharray:2 2

    N_AGENT_DEFINITION_AUDITOR["agent-definition-auditor"]:::diagnostic
    N_AGENT_DELEGATE["agent-delegate"]:::orchestrator
    N_AGENT_HISTORY["agent-history"]:::diagnostic
    N_AGENTS_MD_AUTHORING["agents-md-authoring"]:::specialist
    N_AMIR_PUBLISH["amir-publish"]:::specialist
    N_ARCH_DOCS["arch-docs"]:::stage
    N_ARCH_EPIC["arch-epic"]:::orchestrator
    N_ARCH_FLOW["arch-flow"]:::router
    N_ARCH_MINI_PLAN["arch-mini-plan"]:::stage
    N_ARCH_SKILLS_GUIDE["arch-skills-guide"]:::router
    N_ARCH_STEP["arch-step"]:::orchestrator
    N_ARCH_STEP_GOAL_PROMPT["arch-step-goal-prompt"]:::specialist
    N_AUDIT_LOOP["audit-loop"]:::orchestrator
    N_AUDIT_LOOP_SIM["audit-loop-sim"]:::orchestrator
    N_BUGS_FLOW["bugs-flow"]:::orchestrator
    N_CHATGPT_WEB["chatgpt-web"]:::specialist
    N_CODEX_BABYSIT["codex-babysit"]:::diagnostic
    N_CODEX_CLEANUP["codex-cleanup"]:::specialist
    N_CODEX_REVIEW_YOLO["codex-review-yolo"]:::specialist
    N_COMMENT_LOOP["comment-loop"]:::orchestrator
    N_COMMIT_HISTORY_AUTHORING["commit-history-authoring"]:::specialist
    N_CONTACT_SHEET_BUILDER["contact-sheet-builder"]:::presentation
    N_CYNICAL_ARCHITECTURE_REVIEW["cynical-architecture-review"]:::specialist
    N_CYNICAL_CODE_REVIEW["cynical-code-review"]:::specialist
    N_CYNICAL_CRUFT_REMOVAL["cynical-cruft-removal"]:::specialist
    N_ELI10["eli10"]:::presentation
    N_EXHAUSTIVE_CODE_REVIEW["exhaustive-code-review"]:::specialist
    N_FAL_AI_TOOLS["fal-ai-tools"]:::specialist
    N_FC_BRANDED_PDF["fc-branded-pdf"]:::presentation
    N_FIGMA_BEST_PRACTICES["figma-best-practices"]:::specialist
    N_FLUTTER_REFERENCE["flutter-reference"]:::specialist
    N_FRESH_CONSULT["fresh-consult"]:::orchestrator
    N_GOAL_LOOP["goal-loop"]:::orchestrator
    N_LILARCH["lilarch"]:::orchestrator
    N_MINIARCH_STEP["miniarch-step"]:::orchestrator
    N_MODEL_CONSENSUS["model-consensus"]:::orchestrator
    N_NORTH_STAR_INVESTIGATION["north-star-investigation"]:::orchestrator
    N_PLAN_AUDIT["plan-audit"]:::specialist
    N_PLAN_CONDUCTOR["plan-conductor"]:::orchestrator
    N_PLAN_IMPLEMENT["plan-implement"]:::orchestrator
    N_PR_AUTHORING["pr-authoring"]:::specialist
    N_PR_REVIEW_FOLLOWTHROUGH["pr-review-followthrough"]:::orchestrator
    N_PROMPT_AUTHORING["prompt-authoring"]:::specialist
    N_SKILL_AUTHORING["skill-authoring"]:::specialist
    N_SKILL_FLOW["skill-flow"]:::orchestrator
    N_STEPWISE["stepwise"]:::orchestrator
    N_AGENT_DELEGATE -- "routes_to: routes large ordered architecture workflows to" --> N_ARCH_EPIC
    N_AGENT_DELEGATE -- "routes_to: routes exact Codex yolo-profile reviews to" --> N_CODEX_REVIEW_YOLO
    N_AGENT_DELEGATE -- "routes_to: routes clean read-only second opinions to" --> N_FRESH_CONSULT
    N_AGENT_DELEGATE -- "routes_to: routes iterative two-model convergence work to" --> N_MODEL_CONSENSUS
    N_AGENT_DELEGATE -- "routes_to: routes ordered worker-and-critic workflows to" --> N_STEPWISE
    N_AGENT_HISTORY -- "routes_to: routes deliberate external worker sessions to" --> N_AGENT_DELEGATE
    N_AGENT_HISTORY -- "routes_to: routes Git commit-history rewriting to" --> N_COMMIT_HISTORY_AUTHORING
    N_AGENT_HISTORY -- "routes_to: routes fresh model second opinions to" --> N_FRESH_CONSULT
    N_AGENTS_MD_AUTHORING -- "routes_to: routes repository skill-design work to" --> N_SKILL_AUTHORING
    N_ARCH_DOCS -- "routes_to: routes skill-package selection and editing work to" --> N_SKILL_AUTHORING
    N_ARCH_EPIC -- "routes_to: routes read-only arch status inspection to" --> N_ARCH_FLOW
    N_ARCH_EPIC -- "routes_to: routes one-pass mini planning handoffs to" --> N_ARCH_MINI_PLAN
    N_ARCH_EPIC -- "delegates_to: delegates each sub-plan's implementation loop to" --> N_ARCH_STEP
    N_ARCH_EPIC -- "delegates_to: delegates each sub-plan's planning ownership to" --> N_ARCH_STEP
    N_ARCH_EPIC -- "gates_on: gates planned status on generated receipts from" --> N_ARCH_STEP
    N_ARCH_EPIC -- "gates_on: gates sub-plan North Star progression on" --> N_ARCH_STEP
    N_ARCH_EPIC -- "helper_call: calls inline to scaffold each sub-plan" --> N_ARCH_STEP
    N_ARCH_EPIC -- "references_for_truth: treats as authority for canonical sub-plan documents" --> N_ARCH_STEP
    N_ARCH_EPIC -- "routes_to: routes single-plan full-auto execution to" --> N_ARCH_STEP
    N_ARCH_EPIC -- "routes_to: routes exact external yolo receipt reviews to" --> N_CODEX_REVIEW_YOLO
    N_ARCH_EPIC -- "routes_to: routes open-ended bet-and-learn optimization to" --> N_GOAL_LOOP
    N_ARCH_EPIC -- "routes_to: routes small one-to-three-phase feature work to" --> N_LILARCH
    N_ARCH_EPIC -- "routes_to: routes smaller single-plan full-auto execution to" --> N_MINIARCH_STEP
    N_ARCH_EPIC -- "routes_to: routes foreign-repository ordered process orchestration to" --> N_STEPWISE
    N_ARCH_FLOW -- "routes_to: routes post-audit documentation cleanup to" --> N_ARCH_DOCS
    N_ARCH_FLOW -- "routes_to: routes incomplete one-pass planning blocks to" --> N_ARCH_MINI_PLAN
    N_ARCH_FLOW -- "routes_to: routes broad full-arch execution to" --> N_ARCH_STEP
    N_ARCH_FLOW -- "routes_to: routes small-feature flow steps to" --> N_LILARCH
    N_ARCH_FLOW -- "routes_to: routes faster full-arch and post-mini-plan work to" --> N_MINIARCH_STEP
    N_ARCH_MINI_PLAN -- "routes_to: hands post-audit documentation cleanup to" --> N_ARCH_DOCS
    N_ARCH_MINI_PLAN -- "references_for_truth: references for compatible canonical marker contract" --> N_ARCH_STEP
    N_ARCH_MINI_PLAN -- "routes_to: routes full-arch planning and execution to" --> N_ARCH_STEP
    N_ARCH_MINI_PLAN -- "routes_to: routes bug-dominated investigation work to" --> N_BUGS_FLOW
    N_ARCH_MINI_PLAN -- "routes_to: routes open-ended goal-seeking work to" --> N_GOAL_LOOP
    N_ARCH_MINI_PLAN -- "routes_to: routes tiny feature planning work to" --> N_LILARCH
    N_ARCH_MINI_PLAN -- "references_for_truth: references for compatible artifact-marker contract" --> N_MINIARCH_STEP
    N_ARCH_MINI_PLAN -- "routes_to: hands same-document implementation follow-through to" --> N_MINIARCH_STEP
    N_ARCH_MINI_PLAN -- "routes_to: routes hypothesis-driven investigation work to" --> N_NORTH_STAR_INVESTIGATION
    N_ARCH_MINI_PLAN -- "routes_to: routes agent-prompt repair work to" --> N_PROMPT_AUTHORING
    N_ARCH_SKILLS_GUIDE -- "routes_to: routes documentation cleanup and plan retirement to" --> N_ARCH_DOCS
    N_ARCH_SKILLS_GUIDE -- "routes_to: routes read-only checklist and next-step questions to" --> N_ARCH_FLOW
    N_ARCH_SKILLS_GUIDE -- "routes_to: routes one-pass canonical mini planning to" --> N_ARCH_MINI_PLAN
    N_ARCH_SKILLS_GUIDE -- "routes_to: routes broad full-arch planning and delivery to" --> N_ARCH_STEP
    N_ARCH_SKILLS_GUIDE -- "routes_to: routes repo-wide defect hunting and cleanup to" --> N_AUDIT_LOOP
    N_ARCH_SKILLS_GUIDE -- "routes_to: routes real-app simulator automation audits to" --> N_AUDIT_LOOP_SIM
    N_ARCH_SKILLS_GUIDE -- "routes_to: routes concrete bugs regressions and crashes to" --> N_BUGS_FLOW
    N_ARCH_SKILLS_GUIDE -- "routes_to: routes repo-wide explanatory comment hardening to" --> N_COMMENT_LOOP
    N_ARCH_SKILLS_GUIDE -- "routes_to: routes open-ended goals with unknown paths to" --> N_GOAL_LOOP
    N_ARCH_SKILLS_GUIDE -- "routes_to: routes small one-to-three-phase feature work to" --> N_LILARCH
    N_ARCH_SKILLS_GUIDE -- "routes_to: routes faster full-arch work for smaller features to" --> N_MINIARCH_STEP
    N_ARCH_SKILLS_GUIDE -- "routes_to: routes quantified hypothesis-driven investigations to" --> N_NORTH_STAR_INVESTIGATION
    N_ARCH_STEP -- "routes_to: routes clean post-audit documentation cleanup to" --> N_ARCH_DOCS
    N_ARCH_STEP -- "routes_to: routes read-only next-step questions to" --> N_ARCH_FLOW
    N_ARCH_STEP -- "routes_to: routes one-pass mini-plan work to" --> N_ARCH_MINI_PLAN
    N_ARCH_STEP -- "routes_to: routes arch-suite selection questions to" --> N_ARCH_SKILLS_GUIDE
    N_ARCH_STEP -- "routes_to: routes concrete bug-flow work to" --> N_BUGS_FLOW
    N_ARCH_STEP -- "routes_to: routes open-ended goal-seeking work to" --> N_GOAL_LOOP
    N_ARCH_STEP -- "routes_to: routes small feature-flow work to" --> N_LILARCH
    N_ARCH_STEP -- "routes_to: routes hypothesis-driven investigation work to" --> N_NORTH_STAR_INVESTIGATION
    N_ARCH_STEP -- "routes_to: routes agent-prompt repair work to" --> N_PROMPT_AUTHORING
    N_ARCH_STEP_GOAL_PROMPT -- "references_for_truth: references for ArcStep command behavior and receipt rules" --> N_ARCH_STEP
    N_ARCH_STEP_GOAL_PROMPT -- "routes_to: routes immediate ArcStep execution requests to" --> N_ARCH_STEP
    N_ARCH_STEP_GOAL_PROMPT -- "references_for_truth: references for durable goal-prompt quality doctrine" --> N_PROMPT_AUTHORING
    N_ARCH_STEP_GOAL_PROMPT -- "routes_to: routes non-ArcStep prompt authoring work to" --> N_PROMPT_AUTHORING
    N_ARCH_STEP_GOAL_PROMPT -- "routes_to: routes skill-package creation and editing to" --> N_SKILL_AUTHORING
    N_ARCH_STEP_GOAL_PROMPT -- "routes_to: routes multi-skill flow design and audits to" --> N_SKILL_FLOW
    N_AUDIT_LOOP -- "routes_to: routes fixed-scope architecture work to" --> N_ARCH_MINI_PLAN
    N_AUDIT_LOOP -- "routes_to: routes fixed-scope architecture work to" --> N_ARCH_STEP
    N_AUDIT_LOOP -- "routes_to: routes known bug and regression work to" --> N_BUGS_FLOW
    N_AUDIT_LOOP -- "routes_to: routes open-ended investigation work to" --> N_GOAL_LOOP
    N_AUDIT_LOOP -- "routes_to: routes fixed-scope feature delivery to" --> N_LILARCH
    N_AUDIT_LOOP -- "routes_to: routes open-ended investigation work to" --> N_NORTH_STAR_INVESTIGATION
    N_AUDIT_LOOP_SIM -- "routes_to: routes fixed-scope feature delivery or planning to" --> N_ARCH_MINI_PLAN
    N_AUDIT_LOOP_SIM -- "routes_to: routes fixed-scope feature delivery or planning to" --> N_ARCH_STEP
    N_AUDIT_LOOP_SIM -- "routes_to: routes general repo audits and cleanup to" --> N_AUDIT_LOOP
    N_AUDIT_LOOP_SIM -- "routes_to: routes concrete known regressions and crashes to" --> N_BUGS_FLOW
    N_AUDIT_LOOP_SIM -- "routes_to: routes manual-QA and open-ended optimization work to" --> N_GOAL_LOOP
    N_AUDIT_LOOP_SIM -- "routes_to: routes fixed-scope feature delivery or planning to" --> N_LILARCH
    N_AUDIT_LOOP_SIM -- "routes_to: routes manual-QA and open-ended optimization work to" --> N_NORTH_STAR_INVESTIGATION
    N_BUGS_FLOW -- "routes_to: routes planned feature and architecture work to" --> N_ARCH_MINI_PLAN
    N_BUGS_FLOW -- "routes_to: routes planned feature and architecture work to" --> N_ARCH_STEP
    N_BUGS_FLOW -- "routes_to: routes repo-wide defect hunting to" --> N_AUDIT_LOOP
    N_BUGS_FLOW -- "routes_to: routes open-ended optimization and investigation to" --> N_GOAL_LOOP
    N_BUGS_FLOW -- "routes_to: routes planned feature and architecture work to" --> N_LILARCH
    N_BUGS_FLOW -- "routes_to: routes open-ended optimization and investigation to" --> N_NORTH_STAR_INVESTIGATION
    N_CHATGPT_WEB -- "helper_call: uses as prompt-shaping helper before submission" --> N_PROMPT_AUTHORING
    N_CODEX_BABYSIT -- "routes_to: routes deliberate external worker sessions to" --> N_AGENT_DELEGATE
    N_CODEX_BABYSIT -- "routes_to: routes Codex state-purge work to" --> N_CODEX_CLEANUP
    N_CODEX_BABYSIT -- "routes_to: routes one-off external Codex reviews to" --> N_CODEX_REVIEW_YOLO
    N_CODEX_BABYSIT -- "routes_to: routes self-owned goal-seeking loops to" --> N_GOAL_LOOP
    N_CODEX_CLEANUP -- "routes_to: routes agent-definition file audits to" --> N_AGENT_DEFINITION_AUDITOR
    N_CODEX_CLEANUP -- "routes_to: routes stale repository documentation retirement to" --> N_ARCH_DOCS
    N_COMMENT_LOOP -- "routes_to: routes generic documentation cleanup to" --> N_ARCH_DOCS
    N_COMMENT_LOOP -- "routes_to: routes repo-wide defect and duplication cleanup to" --> N_AUDIT_LOOP
    N_COMMENT_LOOP -- "routes_to: routes concrete regressions and broken behavior to" --> N_BUGS_FLOW
    N_COMMIT_HISTORY_AUTHORING -- "routes_to: routes pull-request title and body work to" --> N_PR_AUTHORING
    N_CYNICAL_ARCHITECTURE_REVIEW -- "routes_to: routes skeptical completion-integrity reviews to" --> N_CYNICAL_CODE_REVIEW
    N_CYNICAL_ARCHITECTURE_REVIEW -- "routes_to: routes coverage-led exhaustive review requests to" --> N_EXHAUSTIVE_CODE_REVIEW
    N_CYNICAL_ARCHITECTURE_REVIEW -- "routes_to: routes plan-centered architecture-bar reviews to" --> N_PLAN_AUDIT
    N_CYNICAL_CODE_REVIEW -- "routes_to: routes coverage-led exhaustive code review to" --> N_EXHAUSTIVE_CODE_REVIEW
    N_CYNICAL_CODE_REVIEW -- "routes_to: routes pre-implementation plan audits to" --> N_PLAN_AUDIT
    N_CYNICAL_CRUFT_REMOVAL -- "routes_to: routes stale-document cleanup and consolidation to" --> N_ARCH_DOCS
    N_CYNICAL_CRUFT_REMOVAL -- "routes_to: routes subtraction-first architecture review to" --> N_CYNICAL_ARCHITECTURE_REVIEW
    N_CYNICAL_CRUFT_REMOVAL -- "routes_to: routes skeptical implementation-completion review to" --> N_CYNICAL_CODE_REVIEW
    N_CYNICAL_CRUFT_REMOVAL -- "routes_to: routes coverage-led exhaustive review to" --> N_EXHAUSTIVE_CODE_REVIEW
    N_ELI10 -- "routes_to: routes prompt authoring work to" --> N_PROMPT_AUTHORING
    N_ELI10 -- "routes_to: routes skill authoring work to" --> N_SKILL_AUTHORING
    N_FRESH_CONSULT -- "routes_to: routes external editful child work to" --> N_AGENT_DELEGATE
    N_FRESH_CONSULT -- "routes_to: routes persistent multi-plan orchestration to" --> N_ARCH_EPIC
    N_FRESH_CONSULT -- "routes_to: routes exact external yolo receipt reviews to" --> N_CODEX_REVIEW_YOLO
    N_FRESH_CONSULT -- "routes_to: routes two-participant convergence work to" --> N_MODEL_CONSENSUS
    N_FRESH_CONSULT -- "routes_to: routes ordered persistent workflow orchestration to" --> N_STEPWISE
    N_GOAL_LOOP -- "routes_to: routes fixed-scope one-pass planning work to" --> N_ARCH_MINI_PLAN
    N_GOAL_LOOP -- "routes_to: routes fixed-scope full architecture work to" --> N_ARCH_STEP
    N_GOAL_LOOP -- "routes_to: routes concrete bug investigations and fixes to" --> N_BUGS_FLOW
    N_GOAL_LOOP -- "routes_to: routes fixed-scope feature plan work to" --> N_LILARCH
    N_GOAL_LOOP -- "routes_to: routes quantified Commander’s Intent investigations to" --> N_NORTH_STAR_INVESTIGATION
    N_LILARCH -- "routes_to: routes compressed one-pass architecture planning to" --> N_ARCH_MINI_PLAN
    N_LILARCH -- "routes_to: routes broad full-architecture workflows to" --> N_ARCH_STEP
    N_LILARCH -- "routes_to: routes dominant root-cause investigation work to" --> N_BUGS_FLOW
    N_LILARCH -- "routes_to: routes smaller full-architecture workflows to" --> N_MINIARCH_STEP
    N_LILARCH -- "routes_to: routes dominant root-cause investigation work to" --> N_NORTH_STAR_INVESTIGATION
    N_LILARCH -- "routes_to: routes primary prompt-repair work directly to" --> N_PROMPT_AUTHORING
    N_MINIARCH_STEP -- "routes_to: hands clean implementation documentation cleanup to" --> N_ARCH_DOCS
    N_MINIARCH_STEP -- "routes_to: routes read-only next-step questions to" --> N_ARCH_FLOW
    N_MINIARCH_STEP -- "routes_to: routes one-pass planning work to" --> N_ARCH_MINI_PLAN
    N_MINIARCH_STEP -- "references_for_truth: adopts full-work artifact discipline baseline from" --> N_ARCH_STEP
    N_MINIARCH_STEP -- "references_for_truth: references for consistency-pass helper ownership" --> N_ARCH_STEP
    N_MINIARCH_STEP -- "routes_to: routes broad ambiguity-heavy architecture work to" --> N_ARCH_STEP
    N_MINIARCH_STEP -- "routes_to: routes primarily bug-shaped work to" --> N_BUGS_FLOW
    N_MINIARCH_STEP -- "routes_to: routes open-ended goal work to" --> N_GOAL_LOOP
    N_MINIARCH_STEP -- "routes_to: routes tiny one-to-three-phase features to" --> N_LILARCH
    N_MINIARCH_STEP -- "routes_to: routes open-ended investigation work to" --> N_NORTH_STAR_INVESTIGATION
    N_MINIARCH_STEP -- "routes_to: routes prompt-first repair work to" --> N_PROMPT_AUTHORING
    N_MODEL_CONSENSUS -- "routes_to: routes epic execution work to" --> N_ARCH_EPIC
    N_MODEL_CONSENSUS -- "routes_to: routes one-shot cold opinions to" --> N_FRESH_CONSULT
    N_MODEL_CONSENSUS -- "routes_to: routes ordered implementation work to" --> N_STEPWISE
    N_NORTH_STAR_INVESTIGATION -- "routes_to: routes planned one-pass architecture delivery to" --> N_ARCH_MINI_PLAN
    N_NORTH_STAR_INVESTIGATION -- "routes_to: routes planned architecture delivery work to" --> N_ARCH_STEP
    N_NORTH_STAR_INVESTIGATION -- "routes_to: routes straightforward bug-fix work to" --> N_BUGS_FLOW
    N_NORTH_STAR_INVESTIGATION -- "routes_to: routes generic open-ended non-quant loops to" --> N_GOAL_LOOP
    N_NORTH_STAR_INVESTIGATION -- "routes_to: routes planned feature delivery work to" --> N_LILARCH
    N_PLAN_CONDUCTOR -- "delegates_to: delegates selected external implementation slices through" --> N_AGENT_DELEGATE
    N_PLAN_CONDUCTOR -- "delegates_to: delegates three clean external review sessions through" --> N_AGENT_DELEGATE
    N_PLAN_CONDUCTOR -- "routes_to: routes single external delegated tasks to" --> N_AGENT_DELEGATE
    N_PLAN_CONDUCTOR -- "routes_to: routes multi-plan epic decomposition work to" --> N_ARCH_EPIC
    N_PLAN_CONDUCTOR -- "routes_to: routes absent plans into one-pass planning with" --> N_ARCH_MINI_PLAN
    N_PLAN_CONDUCTOR -- "routes_to: routes plans lacking observable done-ness to" --> N_ARCH_MINI_PLAN
    N_PLAN_CONDUCTOR -- "routes_to: routes missing full-architecture plan creation to" --> N_ARCH_STEP
    N_PLAN_CONDUCTOR -- "references_for_truth: references for architecture-simplification audit posture" --> N_CYNICAL_ARCHITECTURE_REVIEW
    N_PLAN_CONDUCTOR -- "validates_via: uses as final-gate validator for structural changes" --> N_CYNICAL_ARCHITECTURE_REVIEW
    N_PLAN_CONDUCTOR -- "references_for_truth: references for implementation-integrity audit posture" --> N_CYNICAL_CODE_REVIEW
    N_PLAN_CONDUCTOR -- "validates_via: uses as final-gate validator for non-trivial completion" --> N_CYNICAL_CODE_REVIEW
    N_PLAN_CONDUCTOR -- "references_for_truth: references for subtraction-first cruft audit posture" --> N_CYNICAL_CRUFT_REMOVAL
    N_PLAN_CONDUCTOR -- "validates_via: uses as final-gate validator for delete-heavy plans" --> N_CYNICAL_CRUFT_REMOVAL
    N_PLAN_CONDUCTOR -- "routes_to: routes read-only independent opinions to" --> N_FRESH_CONSULT
    N_PLAN_CONDUCTOR -- "routes_to: routes absent compact-feature plans into planning with" --> N_LILARCH
    N_PLAN_CONDUCTOR -- "routes_to: routes plans lacking observable done-ness to" --> N_LILARCH
    N_PLAN_CONDUCTOR -- "routes_to: routes audit-only plan requests to" --> N_PLAN_AUDIT
    N_PLAN_CONDUCTOR -- "routes_to: routes plan-audit sidecar ownership to" --> N_PLAN_AUDIT
    N_PLAN_CONDUCTOR -- "routes_to: routes plans lacking observable done-ness to" --> N_PLAN_AUDIT
    N_PLAN_CONDUCTOR -- "routes_to: routes parent-implemented plan execution to" --> N_PLAN_IMPLEMENT
    N_PLAN_CONDUCTOR -- "routes_to: routes accepted implementations to PR publication via" --> N_PR_AUTHORING
    N_PLAN_CONDUCTOR -- "routes_to: routes published PRs into review follow-through via" --> N_PR_REVIEW_FOLLOWTHROUGH
    N_PLAN_CONDUCTOR -- "routes_to: routes foreign ordered process orchestration to" --> N_STEPWISE
    N_PLAN_IMPLEMENT -- "routes_to: routes explicit external-worker execution to" --> N_AGENT_DELEGATE
    N_PLAN_IMPLEMENT -- "references_for_truth: references for warm implementation-review lenses" --> N_PLAN_AUDIT
    N_PLAN_IMPLEMENT -- "routes_to: routes pre-implementation plan audits to" --> N_PLAN_AUDIT
    N_PLAN_IMPLEMENT -- "routes_to: routes plan-wide delegated orchestration to" --> N_PLAN_CONDUCTOR
    N_PROMPT_AUTHORING -- "routes_to: routes skill-package authoring and validation to" --> N_SKILL_AUTHORING
    N_SKILL_AUTHORING -- "helper_call: uses as prompt-discipline helper for skill prose" --> N_PROMPT_AUTHORING
    N_SKILL_FLOW -- "routes_to: routes single agent-definition audits to" --> N_AGENT_DEFINITION_AUDITOR
    N_SKILL_FLOW -- "routes_to: routes large execution-goal decomposition to" --> N_ARCH_EPIC
    N_SKILL_FLOW -- "routes_to: routes arch-suite selection questions to" --> N_ARCH_SKILLS_GUIDE
    N_SKILL_FLOW -- "routes_to: routes future catalog additions through" --> N_PROMPT_AUTHORING
    N_SKILL_FLOW -- "routes_to: routes single prompt-contract repair work to" --> N_PROMPT_AUTHORING
    N_SKILL_FLOW -- "routes_to: routes future catalog additions through" --> N_SKILL_AUTHORING
    N_SKILL_FLOW -- "routes_to: routes isolated skill-package work to" --> N_SKILL_AUTHORING
    N_SKILL_FLOW -- "routes_to: routes deterministic worker-and-critic execution to" --> N_STEPWISE
    N_STEPWISE -- "routes_to: routes fixed-plan implementation workflows to" --> N_ARCH_STEP
    N_STEPWISE -- "routes_to: routes exact external yolo receipt reviews to" --> N_CODEX_REVIEW_YOLO
    N_STEPWISE -- "routes_to: routes bet-and-learn optimization workflows to" --> N_GOAL_LOOP
```

## Surface B: complete edge table

| from | to | edge_kind | relationship_label | evidence (path:line) |
| --- | --- | --- | --- | --- |
| `agent-delegate` | `arch-epic` | `routes_to` | routes large ordered architecture workflows to | `skills/agent-delegate/SKILL.md:63` |
| `agent-delegate` | `codex-review-yolo` | `routes_to` | routes exact Codex yolo-profile reviews to | `skills/agent-delegate/SKILL.md:59` |
| `agent-delegate` | `fresh-consult` | `routes_to` | routes clean read-only second opinions to | `skills/agent-delegate/SKILL.md:57` |
| `agent-delegate` | `model-consensus` | `routes_to` | routes iterative two-model convergence work to | `skills/agent-delegate/SKILL.md:61` |
| `agent-delegate` | `stepwise` | `routes_to` | routes ordered worker-and-critic workflows to | `skills/agent-delegate/SKILL.md:63` |
| `agent-history` | `agent-delegate` | `routes_to` | routes deliberate external worker sessions to | `skills/agent-history/SKILL.md:38` |
| `agent-history` | `commit-history-authoring` | `routes_to` | routes Git commit-history rewriting to | `skills/agent-history/SKILL.md:34` |
| `agent-history` | `fresh-consult` | `routes_to` | routes fresh model second opinions to | `skills/agent-history/SKILL.md:36` |
| `agents-md-authoring` | `skill-authoring` | `routes_to` | routes repository skill-design work to | `skills/agents-md-authoring/references/content-budget-and-docs-index.md:120` |
| `arch-docs` | `skill-authoring` | `routes_to` | routes skill-package selection and editing work to | `skills/arch-docs/SKILL.md:26` |
| `arch-epic` | `arch-flow` | `routes_to` | routes read-only arch status inspection to | `skills/arch-epic/SKILL.md:100` |
| `arch-epic` | `arch-mini-plan` | `routes_to` | routes one-pass mini planning handoffs to | `skills/arch-epic/SKILL.md:97` |
| `arch-epic` | `arch-step` | `delegates_to` | delegates each sub-plan's implementation loop to | `skills/arch-epic/SKILL.md:166` |
| `arch-epic` | `arch-step` | `delegates_to` | delegates each sub-plan's planning ownership to | `skills/arch-epic/references/arch-step-integration.md:69` |
| `arch-epic` | `arch-step` | `gates_on` | gates planned status on generated receipts from | `skills/arch-epic/SKILL.md:328` |
| `arch-epic` | `arch-step` | `gates_on` | gates sub-plan North Star progression on | `skills/arch-epic/SKILL.md:156` |
| `arch-epic` | `arch-step` | `helper_call` | calls inline to scaffold each sub-plan | `skills/arch-epic/references/arch-step-integration.md:47` |
| `arch-epic` | `arch-step` | `references_for_truth` | treats as authority for canonical sub-plan documents | `skills/arch-epic/SKILL.md:141` |
| `arch-epic` | `arch-step` | `routes_to` | routes single-plan full-auto execution to | `skills/arch-epic/SKILL.md:96` |
| `arch-epic` | `codex-review-yolo` | `routes_to` | routes exact external yolo receipt reviews to | `skills/arch-epic/SKILL.md:104` |
| `arch-epic` | `goal-loop` | `routes_to` | routes open-ended bet-and-learn optimization to | `skills/arch-epic/SKILL.md:99` |
| `arch-epic` | `lilarch` | `routes_to` | routes small one-to-three-phase feature work to | `skills/arch-epic/SKILL.md:98` |
| `arch-epic` | `miniarch-step` | `routes_to` | routes smaller single-plan full-auto execution to | `skills/arch-epic/SKILL.md:96` |
| `arch-epic` | `stepwise` | `routes_to` | routes foreign-repository ordered process orchestration to | `skills/arch-epic/SKILL.md:102` |
| `arch-flow` | `arch-docs` | `routes_to` | routes post-audit documentation cleanup to | `skills/arch-flow/SKILL.md:38` |
| `arch-flow` | `arch-mini-plan` | `routes_to` | routes incomplete one-pass planning blocks to | `skills/arch-flow/references/recommendation-rules.md:23` |
| `arch-flow` | `arch-step` | `routes_to` | routes broad full-arch execution to | `skills/arch-flow/SKILL.md:36` |
| `arch-flow` | `lilarch` | `routes_to` | routes small-feature flow steps to | `skills/arch-flow/SKILL.md:39` |
| `arch-flow` | `miniarch-step` | `routes_to` | routes faster full-arch and post-mini-plan work to | `skills/arch-flow/SKILL.md:37` |
| `arch-mini-plan` | `arch-docs` | `routes_to` | hands post-audit documentation cleanup to | `skills/arch-mini-plan/SKILL.md:17` |
| `arch-mini-plan` | `arch-step` | `references_for_truth` | references for compatible canonical marker contract | `skills/arch-mini-plan/SKILL.md:34` |
| `arch-mini-plan` | `arch-step` | `routes_to` | routes full-arch planning and execution to | `skills/arch-mini-plan/SKILL.md:22` |
| `arch-mini-plan` | `bugs-flow` | `routes_to` | routes bug-dominated investigation work to | `skills/arch-mini-plan/SKILL.md:23` |
| `arch-mini-plan` | `goal-loop` | `routes_to` | routes open-ended goal-seeking work to | `skills/arch-mini-plan/SKILL.md:24` |
| `arch-mini-plan` | `lilarch` | `routes_to` | routes tiny feature planning work to | `skills/arch-mini-plan/SKILL.md:21` |
| `arch-mini-plan` | `miniarch-step` | `references_for_truth` | references for compatible artifact-marker contract | `skills/arch-mini-plan/references/artifact-contract.md:56` |
| `arch-mini-plan` | `miniarch-step` | `routes_to` | hands same-document implementation follow-through to | `skills/arch-mini-plan/SKILL.md:17` |
| `arch-mini-plan` | `north-star-investigation` | `routes_to` | routes hypothesis-driven investigation work to | `skills/arch-mini-plan/SKILL.md:24` |
| `arch-mini-plan` | `prompt-authoring` | `routes_to` | routes agent-prompt repair work to | `skills/arch-mini-plan/SKILL.md:43` |
| `arch-skills-guide` | `arch-docs` | `routes_to` | routes documentation cleanup and plan retirement to | `skills/arch-skills-guide/SKILL.md:61` |
| `arch-skills-guide` | `arch-flow` | `routes_to` | routes read-only checklist and next-step questions to | `skills/arch-skills-guide/SKILL.md:70` |
| `arch-skills-guide` | `arch-mini-plan` | `routes_to` | routes one-pass canonical mini planning to | `skills/arch-skills-guide/SKILL.md:62` |
| `arch-skills-guide` | `arch-step` | `routes_to` | routes broad full-arch planning and delivery to | `skills/arch-skills-guide/SKILL.md:59` |
| `arch-skills-guide` | `audit-loop` | `routes_to` | routes repo-wide defect hunting and cleanup to | `skills/arch-skills-guide/SKILL.md:66` |
| `arch-skills-guide` | `audit-loop-sim` | `routes_to` | routes real-app simulator automation audits to | `skills/arch-skills-guide/SKILL.md:67` |
| `arch-skills-guide` | `bugs-flow` | `routes_to` | routes concrete bugs regressions and crashes to | `skills/arch-skills-guide/SKILL.md:64` |
| `arch-skills-guide` | `comment-loop` | `routes_to` | routes repo-wide explanatory comment hardening to | `skills/arch-skills-guide/SKILL.md:65` |
| `arch-skills-guide` | `goal-loop` | `routes_to` | routes open-ended goals with unknown paths to | `skills/arch-skills-guide/SKILL.md:68` |
| `arch-skills-guide` | `lilarch` | `routes_to` | routes small one-to-three-phase feature work to | `skills/arch-skills-guide/SKILL.md:63` |
| `arch-skills-guide` | `miniarch-step` | `routes_to` | routes faster full-arch work for smaller features to | `skills/arch-skills-guide/SKILL.md:60` |
| `arch-skills-guide` | `north-star-investigation` | `routes_to` | routes quantified hypothesis-driven investigations to | `skills/arch-skills-guide/SKILL.md:69` |
| `arch-step` | `arch-docs` | `routes_to` | routes clean post-audit documentation cleanup to | `skills/arch-step/SKILL.md:254` |
| `arch-step` | `arch-flow` | `routes_to` | routes read-only next-step questions to | `skills/arch-step/SKILL.md:28` |
| `arch-step` | `arch-mini-plan` | `routes_to` | routes one-pass mini-plan work to | `skills/arch-step/SKILL.md:30` |
| `arch-step` | `arch-skills-guide` | `routes_to` | routes arch-suite selection questions to | `skills/arch-step/SKILL.md:31` |
| `arch-step` | `bugs-flow` | `routes_to` | routes concrete bug-flow work to | `skills/arch-step/SKILL.md:30` |
| `arch-step` | `goal-loop` | `routes_to` | routes open-ended goal-seeking work to | `skills/arch-step/SKILL.md:30` |
| `arch-step` | `lilarch` | `routes_to` | routes small feature-flow work to | `skills/arch-step/SKILL.md:30` |
| `arch-step` | `north-star-investigation` | `routes_to` | routes hypothesis-driven investigation work to | `skills/arch-step/SKILL.md:30` |
| `arch-step` | `prompt-authoring` | `routes_to` | routes agent-prompt repair work to | `skills/arch-step/SKILL.md:80` |
| `arch-step-goal-prompt` | `arch-step` | `references_for_truth` | references for ArcStep command behavior and receipt rules | `skills/arch-step-goal-prompt/SKILL.md:55` |
| `arch-step-goal-prompt` | `arch-step` | `routes_to` | routes immediate ArcStep execution requests to | `skills/arch-step-goal-prompt/SKILL.md:36` |
| `arch-step-goal-prompt` | `prompt-authoring` | `references_for_truth` | references for durable goal-prompt quality doctrine | `skills/arch-step-goal-prompt/SKILL.md:53` |
| `arch-step-goal-prompt` | `prompt-authoring` | `routes_to` | routes non-ArcStep prompt authoring work to | `skills/arch-step-goal-prompt/SKILL.md:37` |
| `arch-step-goal-prompt` | `skill-authoring` | `routes_to` | routes skill-package creation and editing to | `skills/arch-step-goal-prompt/SKILL.md:38` |
| `arch-step-goal-prompt` | `skill-flow` | `routes_to` | routes multi-skill flow design and audits to | `skills/arch-step-goal-prompt/SKILL.md:39` |
| `audit-loop` | `arch-mini-plan` | `routes_to` | routes fixed-scope architecture work to | `skills/audit-loop/SKILL.md:22` |
| `audit-loop` | `arch-step` | `routes_to` | routes fixed-scope architecture work to | `skills/audit-loop/SKILL.md:22` |
| `audit-loop` | `bugs-flow` | `routes_to` | routes known bug and regression work to | `skills/audit-loop/SKILL.md:21` |
| `audit-loop` | `goal-loop` | `routes_to` | routes open-ended investigation work to | `skills/audit-loop/SKILL.md:23` |
| `audit-loop` | `lilarch` | `routes_to` | routes fixed-scope feature delivery to | `skills/audit-loop/SKILL.md:22` |
| `audit-loop` | `north-star-investigation` | `routes_to` | routes open-ended investigation work to | `skills/audit-loop/SKILL.md:23` |
| `audit-loop-sim` | `arch-mini-plan` | `routes_to` | routes fixed-scope feature delivery or planning to | `skills/audit-loop-sim/SKILL.md:23` |
| `audit-loop-sim` | `arch-step` | `routes_to` | routes fixed-scope feature delivery or planning to | `skills/audit-loop-sim/SKILL.md:23` |
| `audit-loop-sim` | `audit-loop` | `routes_to` | routes general repo audits and cleanup to | `skills/audit-loop-sim/SKILL.md:22` |
| `audit-loop-sim` | `bugs-flow` | `routes_to` | routes concrete known regressions and crashes to | `skills/audit-loop-sim/SKILL.md:21` |
| `audit-loop-sim` | `goal-loop` | `routes_to` | routes manual-QA and open-ended optimization work to | `skills/audit-loop-sim/SKILL.md:24` |
| `audit-loop-sim` | `lilarch` | `routes_to` | routes fixed-scope feature delivery or planning to | `skills/audit-loop-sim/SKILL.md:23` |
| `audit-loop-sim` | `north-star-investigation` | `routes_to` | routes manual-QA and open-ended optimization work to | `skills/audit-loop-sim/SKILL.md:24` |
| `bugs-flow` | `arch-mini-plan` | `routes_to` | routes planned feature and architecture work to | `skills/bugs-flow/SKILL.md:21` |
| `bugs-flow` | `arch-step` | `routes_to` | routes planned feature and architecture work to | `skills/bugs-flow/SKILL.md:21` |
| `bugs-flow` | `audit-loop` | `routes_to` | routes repo-wide defect hunting to | `skills/bugs-flow/SKILL.md:20` |
| `bugs-flow` | `goal-loop` | `routes_to` | routes open-ended optimization and investigation to | `skills/bugs-flow/SKILL.md:22` |
| `bugs-flow` | `lilarch` | `routes_to` | routes planned feature and architecture work to | `skills/bugs-flow/SKILL.md:21` |
| `bugs-flow` | `north-star-investigation` | `routes_to` | routes open-ended optimization and investigation to | `skills/bugs-flow/SKILL.md:22` |
| `chatgpt-web` | `prompt-authoring` | `helper_call` | uses as prompt-shaping helper before submission | `skills/chatgpt-web/SKILL.md:58` |
| `codex-babysit` | `agent-delegate` | `routes_to` | routes deliberate external worker sessions to | `skills/codex-babysit/SKILL.md:41` |
| `codex-babysit` | `codex-cleanup` | `routes_to` | routes Codex state-purge work to | `skills/codex-babysit/SKILL.md:46` |
| `codex-babysit` | `codex-review-yolo` | `routes_to` | routes one-off external Codex reviews to | `skills/codex-babysit/SKILL.md:45` |
| `codex-babysit` | `goal-loop` | `routes_to` | routes self-owned goal-seeking loops to | `skills/codex-babysit/SKILL.md:44` |
| `codex-cleanup` | `agent-definition-auditor` | `routes_to` | routes agent-definition file audits to | `skills/codex-cleanup/SKILL.md:37` |
| `codex-cleanup` | `arch-docs` | `routes_to` | routes stale repository documentation retirement to | `skills/codex-cleanup/SKILL.md:36` |
| `comment-loop` | `arch-docs` | `routes_to` | routes generic documentation cleanup to | `skills/comment-loop/SKILL.md:21` |
| `comment-loop` | `audit-loop` | `routes_to` | routes repo-wide defect and duplication cleanup to | `skills/comment-loop/SKILL.md:23` |
| `comment-loop` | `bugs-flow` | `routes_to` | routes concrete regressions and broken behavior to | `skills/comment-loop/SKILL.md:22` |
| `commit-history-authoring` | `pr-authoring` | `routes_to` | routes pull-request title and body work to | `skills/commit-history-authoring/SKILL.md:38` |
| `cynical-architecture-review` | `cynical-code-review` | `routes_to` | routes skeptical completion-integrity reviews to | `skills/cynical-architecture-review/SKILL.md:49` |
| `cynical-architecture-review` | `exhaustive-code-review` | `routes_to` | routes coverage-led exhaustive review requests to | `skills/cynical-architecture-review/SKILL.md:46` |
| `cynical-architecture-review` | `plan-audit` | `routes_to` | routes plan-centered architecture-bar reviews to | `skills/cynical-architecture-review/SKILL.md:51` |
| `cynical-code-review` | `exhaustive-code-review` | `routes_to` | routes coverage-led exhaustive code review to | `skills/cynical-code-review/SKILL.md:42` |
| `cynical-code-review` | `plan-audit` | `routes_to` | routes pre-implementation plan audits to | `skills/cynical-code-review/SKILL.md:43` |
| `cynical-cruft-removal` | `arch-docs` | `routes_to` | routes stale-document cleanup and consolidation to | `skills/cynical-cruft-removal/SKILL.md:54` |
| `cynical-cruft-removal` | `cynical-architecture-review` | `routes_to` | routes subtraction-first architecture review to | `skills/cynical-cruft-removal/SKILL.md:52` |
| `cynical-cruft-removal` | `cynical-code-review` | `routes_to` | routes skeptical implementation-completion review to | `skills/cynical-cruft-removal/SKILL.md:49` |
| `cynical-cruft-removal` | `exhaustive-code-review` | `routes_to` | routes coverage-led exhaustive review to | `skills/cynical-cruft-removal/SKILL.md:46` |
| `eli10` | `prompt-authoring` | `routes_to` | routes prompt authoring work to | `skills/eli10/SKILL.md:56` |
| `eli10` | `skill-authoring` | `routes_to` | routes skill authoring work to | `skills/eli10/SKILL.md:57` |
| `fresh-consult` | `agent-delegate` | `routes_to` | routes external editful child work to | `skills/fresh-consult/SKILL.md:49` |
| `fresh-consult` | `arch-epic` | `routes_to` | routes persistent multi-plan orchestration to | `skills/fresh-consult/SKILL.md:54` |
| `fresh-consult` | `codex-review-yolo` | `routes_to` | routes exact external yolo receipt reviews to | `skills/fresh-consult/SKILL.md:47` |
| `fresh-consult` | `model-consensus` | `routes_to` | routes two-participant convergence work to | `skills/fresh-consult/SKILL.md:52` |
| `fresh-consult` | `stepwise` | `routes_to` | routes ordered persistent workflow orchestration to | `skills/fresh-consult/SKILL.md:54` |
| `goal-loop` | `arch-mini-plan` | `routes_to` | routes fixed-scope one-pass planning work to | `skills/goal-loop/SKILL.md:20` |
| `goal-loop` | `arch-step` | `routes_to` | routes fixed-scope full architecture work to | `skills/goal-loop/SKILL.md:20` |
| `goal-loop` | `bugs-flow` | `routes_to` | routes concrete bug investigations and fixes to | `skills/goal-loop/SKILL.md:21` |
| `goal-loop` | `lilarch` | `routes_to` | routes fixed-scope feature plan work to | `skills/goal-loop/SKILL.md:20` |
| `goal-loop` | `north-star-investigation` | `routes_to` | routes quantified Commander’s Intent investigations to | `skills/goal-loop/SKILL.md:22` |
| `lilarch` | `arch-mini-plan` | `routes_to` | routes compressed one-pass architecture planning to | `skills/lilarch/SKILL.md:21` |
| `lilarch` | `arch-step` | `routes_to` | routes broad full-architecture workflows to | `skills/lilarch/SKILL.md:22` |
| `lilarch` | `bugs-flow` | `routes_to` | routes dominant root-cause investigation work to | `skills/lilarch/SKILL.md:23` |
| `lilarch` | `miniarch-step` | `routes_to` | routes smaller full-architecture workflows to | `skills/lilarch/SKILL.md:22` |
| `lilarch` | `north-star-investigation` | `routes_to` | routes dominant root-cause investigation work to | `skills/lilarch/SKILL.md:23` |
| `lilarch` | `prompt-authoring` | `routes_to` | routes primary prompt-repair work directly to | `skills/lilarch/SKILL.md:60` |
| `miniarch-step` | `arch-docs` | `routes_to` | hands clean implementation documentation cleanup to | `skills/miniarch-step/SKILL.md:250` |
| `miniarch-step` | `arch-flow` | `routes_to` | routes read-only next-step questions to | `skills/miniarch-step/SKILL.md:25` |
| `miniarch-step` | `arch-mini-plan` | `routes_to` | routes one-pass planning work to | `skills/miniarch-step/SKILL.md:26` |
| `miniarch-step` | `arch-step` | `references_for_truth` | adopts full-work artifact discipline baseline from | `skills/miniarch-step/SKILL.md:12` |
| `miniarch-step` | `arch-step` | `references_for_truth` | references for consistency-pass helper ownership | `skills/miniarch-step/references/full-auto.md:63` |
| `miniarch-step` | `arch-step` | `routes_to` | routes broad ambiguity-heavy architecture work to | `skills/miniarch-step/SKILL.md:28` |
| `miniarch-step` | `bugs-flow` | `routes_to` | routes primarily bug-shaped work to | `skills/miniarch-step/SKILL.md:30` |
| `miniarch-step` | `goal-loop` | `routes_to` | routes open-ended goal work to | `skills/miniarch-step/SKILL.md:30` |
| `miniarch-step` | `lilarch` | `routes_to` | routes tiny one-to-three-phase features to | `skills/miniarch-step/SKILL.md:27` |
| `miniarch-step` | `north-star-investigation` | `routes_to` | routes open-ended investigation work to | `skills/miniarch-step/SKILL.md:30` |
| `miniarch-step` | `prompt-authoring` | `routes_to` | routes prompt-first repair work to | `skills/miniarch-step/SKILL.md:108` |
| `model-consensus` | `arch-epic` | `routes_to` | routes epic execution work to | `skills/model-consensus/SKILL.md:49` |
| `model-consensus` | `fresh-consult` | `routes_to` | routes one-shot cold opinions to | `skills/model-consensus/SKILL.md:45` |
| `model-consensus` | `stepwise` | `routes_to` | routes ordered implementation work to | `skills/model-consensus/SKILL.md:48` |
| `north-star-investigation` | `arch-mini-plan` | `routes_to` | routes planned one-pass architecture delivery to | `skills/north-star-investigation/SKILL.md:21` |
| `north-star-investigation` | `arch-step` | `routes_to` | routes planned architecture delivery work to | `skills/north-star-investigation/SKILL.md:21` |
| `north-star-investigation` | `bugs-flow` | `routes_to` | routes straightforward bug-fix work to | `skills/north-star-investigation/SKILL.md:20` |
| `north-star-investigation` | `goal-loop` | `routes_to` | routes generic open-ended non-quant loops to | `skills/north-star-investigation/SKILL.md:22` |
| `north-star-investigation` | `lilarch` | `routes_to` | routes planned feature delivery work to | `skills/north-star-investigation/SKILL.md:21` |
| `plan-conductor` | `agent-delegate` | `delegates_to` | delegates selected external implementation slices through | `skills/plan-conductor/SKILL.md:222` |
| `plan-conductor` | `agent-delegate` | `delegates_to` | delegates three clean external review sessions through | `skills/plan-conductor/references/terra-delivery-shortcut.md:57` |
| `plan-conductor` | `agent-delegate` | `routes_to` | routes single external delegated tasks to | `skills/plan-conductor/SKILL.md:65` |
| `plan-conductor` | `arch-epic` | `routes_to` | routes multi-plan epic decomposition work to | `skills/plan-conductor/SKILL.md:68` |
| `plan-conductor` | `arch-mini-plan` | `routes_to` | routes absent plans into one-pass planning with | `skills/plan-conductor/SKILL.md:60` |
| `plan-conductor` | `arch-mini-plan` | `routes_to` | routes plans lacking observable done-ness to | `skills/plan-conductor/references/plan-intake-and-readiness.md:37` |
| `plan-conductor` | `arch-step` | `routes_to` | routes missing full-architecture plan creation to | `skills/plan-conductor/SKILL.md:60` |
| `plan-conductor` | `cynical-architecture-review` | `references_for_truth` | references for architecture-simplification audit posture | `skills/plan-conductor/references/audit-and-send-back.md:6` |
| `plan-conductor` | `cynical-architecture-review` | `validates_via` | uses as final-gate validator for structural changes | `skills/plan-conductor/SKILL.md:242` |
| `plan-conductor` | `cynical-code-review` | `references_for_truth` | references for implementation-integrity audit posture | `skills/plan-conductor/references/audit-and-send-back.md:5` |
| `plan-conductor` | `cynical-code-review` | `validates_via` | uses as final-gate validator for non-trivial completion | `skills/plan-conductor/SKILL.md:241` |
| `plan-conductor` | `cynical-cruft-removal` | `references_for_truth` | references for subtraction-first cruft audit posture | `skills/plan-conductor/references/audit-and-send-back.md:6` |
| `plan-conductor` | `cynical-cruft-removal` | `validates_via` | uses as final-gate validator for delete-heavy plans | `skills/plan-conductor/SKILL.md:243` |
| `plan-conductor` | `fresh-consult` | `routes_to` | routes read-only independent opinions to | `skills/plan-conductor/SKILL.md:71` |
| `plan-conductor` | `lilarch` | `routes_to` | routes absent compact-feature plans into planning with | `skills/plan-conductor/SKILL.md:61` |
| `plan-conductor` | `lilarch` | `routes_to` | routes plans lacking observable done-ness to | `skills/plan-conductor/references/plan-intake-and-readiness.md:37` |
| `plan-conductor` | `plan-audit` | `routes_to` | routes audit-only plan requests to | `skills/plan-conductor/SKILL.md:67` |
| `plan-conductor` | `plan-audit` | `routes_to` | routes plan-audit sidecar ownership to | `skills/plan-conductor/SKILL.md:182` |
| `plan-conductor` | `plan-audit` | `routes_to` | routes plans lacking observable done-ness to | `skills/plan-conductor/references/plan-intake-and-readiness.md:36` |
| `plan-conductor` | `plan-implement` | `routes_to` | routes parent-implemented plan execution to | `skills/plan-conductor/SKILL.md:63` |
| `plan-conductor` | `pr-authoring` | `routes_to` | routes accepted implementations to PR publication via | `skills/plan-conductor/SKILL.md:173` |
| `plan-conductor` | `pr-review-followthrough` | `routes_to` | routes published PRs into review follow-through via | `skills/plan-conductor/SKILL.md:174` |
| `plan-conductor` | `stepwise` | `routes_to` | routes foreign ordered process orchestration to | `skills/plan-conductor/SKILL.md:70` |
| `plan-implement` | `agent-delegate` | `routes_to` | routes explicit external-worker execution to | `skills/plan-implement/SKILL.md:48` |
| `plan-implement` | `plan-audit` | `references_for_truth` | references for warm implementation-review lenses | `skills/plan-implement/references/continuous-review.md:24` |
| `plan-implement` | `plan-audit` | `routes_to` | routes pre-implementation plan audits to | `skills/plan-implement/SKILL.md:39` |
| `plan-implement` | `plan-conductor` | `routes_to` | routes plan-wide delegated orchestration to | `skills/plan-implement/SKILL.md:46` |
| `prompt-authoring` | `skill-authoring` | `routes_to` | routes skill-package authoring and validation to | `skills/prompt-authoring/SKILL.md:39` |
| `skill-authoring` | `prompt-authoring` | `helper_call` | uses as prompt-discipline helper for skill prose | `skills/skill-authoring/SKILL.md:50` |
| `skill-flow` | `agent-definition-auditor` | `routes_to` | routes single agent-definition audits to | `skills/skill-flow/SKILL.md:35` |
| `skill-flow` | `arch-epic` | `routes_to` | routes large execution-goal decomposition to | `skills/skill-flow/SKILL.md:32` |
| `skill-flow` | `arch-skills-guide` | `routes_to` | routes arch-suite selection questions to | `skills/skill-flow/SKILL.md:33` |
| `skill-flow` | `prompt-authoring` | `routes_to` | routes future catalog additions through | `skills/skill-flow/references/waste-pattern-catalog.md:216` |
| `skill-flow` | `prompt-authoring` | `routes_to` | routes single prompt-contract repair work to | `skills/skill-flow/SKILL.md:29` |
| `skill-flow` | `skill-authoring` | `routes_to` | routes future catalog additions through | `skills/skill-flow/references/waste-pattern-catalog.md:215` |
| `skill-flow` | `skill-authoring` | `routes_to` | routes isolated skill-package work to | `skills/skill-flow/SKILL.md:28` |
| `skill-flow` | `stepwise` | `routes_to` | routes deterministic worker-and-critic execution to | `skills/skill-flow/SKILL.md:34` |
| `stepwise` | `arch-step` | `routes_to` | routes fixed-plan implementation workflows to | `skills/stepwise/SKILL.md:36` |
| `stepwise` | `codex-review-yolo` | `routes_to` | routes exact external yolo receipt reviews to | `skills/stepwise/SKILL.md:40` |
| `stepwise` | `goal-loop` | `routes_to` | routes bet-and-learn optimization workflows to | `skills/stepwise/SKILL.md:38` |

## Surface C: unresolved references

_None._

## Post-fix findings

### Dead-skill check

Six nodes are graph-isolated: `amir-publish`, `contact-sheet-builder`, `fal-ai-tools`, `fc-branded-pdf`, `figma-best-practices`, and `flutter-reference`. Their declared jobs are direct-invocation operational, presentation, provider, or domain-reference capabilities, so zero peer degree does not establish that they are dead. The DAG supports no retirement recommendation without separate harness or usage evidence.

### Over-promotion check

No over-promoted helper is evidenced. The two router nodes, `arch-flow` and `arch-skills-guide`, have relationship-bearing `routes_to` fan-out consistent with their declared routing jobs, while their targets own distinct workflows rather than helper-only contracts. No router-routed node is both bypassed by the router and reduced to helper/validation-only outbound work.

### Duplicate-owner check

No duplicate canonical owner is established. Several arch and loop orchestrators share reciprocal anti-case exits to `arch-step`, `arch-mini-plan`, `lilarch`, `bugs-flow`, `goal-loop`, and `north-star-investigation`, but their `SKILL.md:3` declarations own different artifacts and acceptance criteria. The dense overlap is routing boundary hygiene, not duplicate stage ownership.

### Broken-reference check

No broken peer reference remains. The apparent `$changeset-validation` candidate at `skills/agents-md-authoring/references/content-budget-and-docs-index.md:119` is quoted hypothetical `AGENTS.md` output that teaches a writing pattern; the surrounding package does not assert that `agents-md-authoring` calls or depends on that skill. The current extraction contract therefore excludes it, and no unresolved or `unclassified` edge remains.
