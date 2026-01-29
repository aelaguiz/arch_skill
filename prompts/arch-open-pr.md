---
description: "12) Open PR: merge default branch, run CI-equivalent checks locally, then commit/push and open a detailed PR."
argument-hint: "<Optional: PR title + intent + any constraints. Slang ok.>"
---
# /prompts:arch-open-pr — $ARGUMENTS
# COMMUNICATING WITH AMIR (IMPORTANT)
You are doing the “make CI boring” finalization pass.

- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give a short update in natural English (bullets optional; only if they help).
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Keep console output high-signal; put deep logs/long outputs in a file if needed.

Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately.
$ARGUMENTS is freeform steering (title ideas, intent, constraints). Infer what you can.

Question policy (strict):
- You MUST answer anything discoverable from code/tests/CI config/docs or by running repo tooling; do not ask me.
- Allowed questions only:
  - Product/UX decisions not encoded in repo/docs
  - External constraints not in repo/docs (policies, launch dates, KPIs, access)
  - Missing access/permissions (e.g., can’t push, can’t open PR)
  - Irreducible ambiguity about “what PR are we opening?”

Goal:
Get the current branch into a state where:
1) it cleanly incorporates the latest default branch (usually `origin/main`),
2) it passes the same checks CI will run (locally, before we burn CI cycles),
3) it is pushed, and
4) the PR is opened with a detailed, template-based description.

## 1) Sync with default branch (thoughtful merge)
- Identify the repo’s default branch from git (prefer `origin/main`, otherwise `origin/HEAD`).
- Ensure we are on a feature branch (not the default branch) before doing PR work. If we’re on the default branch, create a branch with a sensible name.
- Ensure changes are safely committed before merging:
  - If there are in-progress changes you created, commit them (stage only what you touched).
  - Do not sweep unrelated local files into commits.
- `git fetch origin`, then merge the default branch into the feature branch.
- If conflicts occur: resolve them thoughtfully using repo conventions and our intended behavior.
  - If a conflict forces a real product/UX decision not in the repo, stop and ask with the smallest possible question.

## 2) Run “what CI will run” locally (don’t guess—derive)
Discover what checks CI runs for PRs in THIS repo, then run the closest local equivalent:
- Read `.github/workflows/*` and any referenced scripts/Make targets to learn the actual commands.
- Prefer running the repo’s canonical “one command does CI” entrypoint if it exists (`make ci`, `./script/ci`, `npm run ci`, etc.).
- Otherwise run the equivalent set of checks CI runs (typically: format/lint, typecheck, tests, build, static analysis).
- Use best judgment on install/setup:
  - If CI installs deps, do the same locally (use the repo’s preferred package manager / setup step).
  - If there’s a `make install` that clearly matches CI setup, use it.

Iterate until green:
- When a check fails, fix the root cause, then re-run the smallest check that proves it’s fixed.
- Avoid scope creep: fix what blocks CI; record “nice-to-haves” as follow-ups instead of expanding the PR.

## 3) Finalize commits + push
- Ensure the branch has clean commits for review (not “temp debug”).
- Stage only files you touched; keep commits cohesive.
- Push the branch to origin (set upstream if needed).

## 4) Open a PR with the repo’s template (repo-relative)
Produce a PR title + body that is detailed and matches THIS repo’s template:
- Load the PR template from THIS repo (repo-relative), preferring:
  - `.github/pull_request_template.md`
  - (fallback) `.github/pul_request_template.md`
  - (fallback) `.github/PULL_REQUEST_TEMPLATE.md`
- Fill it in with specifics from the actual diff:
  - What changed and why (user impact + technical summary)
  - How it was tested (commands + results)
  - Risks/rollout/monitoring notes (if applicable)
  - Screenshots/logs/QA notes if relevant

Then open the PR:
- If GitHub CLI `gh` is available and authenticated, create the PR and print the URL.
- Otherwise, print the prepared title + body clearly so Amir can paste it (and provide the exact `gh pr create` command to run).

OUTPUT FORMAT (console only; Amir-style):
This is the information it should contain but you should communicate it naturally in english not as a bulleted list that is hard to parse for the user.
Include:
- North Star reminder (1 line)
- Punchline (1 line)
- What you did (merge + checks you ran)
- Result (green/red; what’s blocking if red)
- What got committed + pushed (branch name + commits)
- PR status (opened URL or ready-to-paste title/body)
- Need from Amir (only if required)
