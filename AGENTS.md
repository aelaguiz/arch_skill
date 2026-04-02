Do not use external multi-model consultation workflows unless the user explicitly asks for a code review.

Verification:
- After skill package changes, run `npx skills check`.
- Use `make verify_install` only when you intentionally want to validate the installed skill surface.

Routing:
- Use `$skill-authoring` for new, edited, refactored, or audited skill packages.
- Use `$agents-md-authoring` for `AGENTS.md` authoring or refactors.
- Use `$arch-step` for the old saved-prompt full-arch flow when the user wants prompt-close commands like `new`, `reformat`, `research`, `deep-dive`, `phase-plan`, `plan-enhance`, `fold-in`, `review-gate`, `implement`, `audit-implementation`, `advance`, or concise full-arch status.
- Use `$arch-flow` for read-only checklist and next-step inspection.

NO EXPOSITION IN SKILLS AND THEIR DOCTRINE MUST BE FULLY SELF CONTAINED NOT REFERENCING HISTORICAL TRUTHS OR THE SKILL DEVELOPMENT PROCESS ITSELF. Only exception is for skill coordinators which explicitely explain how to use other skills.
