---
description: "12) Open PR: merge default branch, do a post-merge smoke check (no redundant suites), push, open a detailed draft PR, then watch CI until mergeable."
argument-hint: "<Optional: PR title/intent/constraints. Add `parity` to run CI-equivalent locally. Add `no-watch` to skip CI watching.>"
---
# /prompts:arch-open-pr — $ARGUMENTS
# COMMUNICATING WITH USERNAME (IMPORTANT)
You are doing the “get the PR live fast, then let CI be the referee” finalization pass.

- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Keep console output high-signal; deep logs/long outputs go in a file if needed.

Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately.
$ARGUMENTS is freeform steering (title ideas, intent, constraints). Infer what you can.

Question policy (strict):
- You MUST answer anything discoverable from code/tests/CI config/docs or by running repo tooling; do not ask me.
- Allowed questions only:
  - Missing access/permissions (e.g., can’t push, can’t open PR)
  - Irreducible ambiguity about “what PR are we opening?”

Goal:
Get the current branch into a state where:
1) it cleanly incorporates the latest default branch (usually `origin/main`),
2) it passes a **post-merge smoke check** (no redundant long suites),
3) it is pushed, and
4) the PR is opened as a **draft** with a detailed, template-based description.
5) if CI runs on PRs, we watch it to completion and report whether the PR is mergeable.

Modes (keep it simple):
- Default = FAST: open the PR quickly; avoid re-running suites we already ran.
- If $ARGUMENTS includes `parity` / `full`: run the CI-equivalent checks locally (can take a while).
- If $ARGUMENTS includes `no-watch`: do not watch CI.

## 1) Sync with default branch (thoughtful merge)
- Identify the repo’s default branch from git (prefer `origin/main`, otherwise `origin/HEAD`).
- Ensure we are on a feature branch (not the default branch) before doing PR work. If we’re on the default branch, create a branch with a sensible name.
- Ensure changes are safely committed before merging:
  - If there are in-progress changes you created, commit them (stage only what you touched).
  - Do not sweep unrelated local files into commits.
- Capture `PRE_MERGE_SHA` (current `HEAD`), then `git fetch origin`, then merge the default branch into the feature branch.
- If conflicts occur: resolve them thoughtfully using repo conventions and our intended behavior.
  - If a conflict forces a real product/UX decision not in the repo, stop and ask with the smallest possible question.

## 2) Local checks (post-merge smoke; FAST = minimal)
Default (FAST):
- Do NOT re-run long suites we already ran earlier in this work unless the merge introduced conflicts or we changed behavior after the last known green run.
- Prefer to rely on PR CI to re-validate the full suite.
- Run only a post-merge smoke check that proves we didn’t break basics:
  - compile/build the affected target(s) (and both iOS + Android if you’re changing a mobile app),
  - run a small, relevant unit test set only if conflicts occurred or the merge diff touches core code.
- If the merge was conflict-free and `git diff --name-only "$PRE_MERGE_SHA..HEAD"` is empty or trivially irrelevant: prefer skipping local checks and proceed to opening the PR.
- Avoid heavy setup/install steps unless a check fails and indicates missing deps.

If $ARGUMENTS includes `parity` / `full`:
- Derive what CI actually runs from workflows/scripts and run the closest local equivalent until green.

## 3) Finalize commits + push
- Ensure the branch has clean commits for review (not “temp debug”).
- Stage only files you touched; keep commits cohesive.
- Push the branch to origin (set upstream if needed).

## 4) Open a draft PR with the repo’s template (repo-relative)
Before opening the PR: if this repo has an explicit docs policy / doc lifecycle policy (in `AGENTS.md`, `docs/AGENTS.md`, `docs/ORIENTATION_ARTIFACT_MAP.md`, or similar), follow it first (e.g., required doc summaries, moving plan docs to the right place, not committing huge raw logs/artifacts, adding `gitignore` rules). Do not invent new policy; obey only what’s clearly specified.

Produce a PR title + body that is detailed and matches THIS repo’s template:
- Load the PR template from THIS repo (repo-relative), preferring:
  - `.github/pull_request_template.md`
  - (alternate) `.github/pul_request_template.md`
  - (alternate) `.github/PULL_REQUEST_TEMPLATE.md`
- Fill it in with specifics from the actual diff:
  - What changed and why (user impact + technical summary)
  - How it was tested (commands + results)
  - Gotchas / sharp edges worth propagating (and where they’re documented in code comments)
  - Risks/rollout/monitoring notes (if applicable)
  - Screenshots/logs/QA notes if relevant

Then open the PR:
- ALWAYS open the PR as a **draft** (never “ready for review” by default).
- If a PR already exists for the branch, do not create a duplicate:
  - Ensure it is in draft mode (GitHub UI: “Convert to draft”, or `gh pr ready --undo`), then print the URL.
- If GitHub CLI `gh` is available and authenticated, create the PR as a draft and print the URL (use `gh pr create --draft …`).
- Otherwise, print the prepared title + body clearly so USERNAME can paste it (and provide the exact `gh pr create --draft …` command to run).
- If using the GitHub web UI, choose “Create draft pull request”.

## 5) Watch PR CI (default)
If CI checks run on PRs, prefer to watch them to completion so we know whether the PR is green/mergeable:
- If GitHub CLI `gh` is available and authenticated: run `gh pr checks --watch` for this PR.
- Summarize whether checks are green, and if not, which check failed and the smallest next action.
- Skip CI watching if $ARGUMENTS includes `no-watch`.

OUTPUT FORMAT (console only; USERNAME-style):
This is the information it should contain but you should communicate it naturally in english not as a bulleted list that is hard to parse for the user.
Include:
- North Star reminder (1 line)
- Punchline (1 line)
- What you did (merge + checks you ran)
- Result (green/red; what’s blocking if red)
- What got committed + pushed (branch name + commits)
- PR status (opened URL or ready-to-paste title/body)
- CI status (watched/pending; mergeable or what failed)
- Need from USERNAME (only if required)
