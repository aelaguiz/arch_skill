---
description: "12) Open PR: merge default branch, run fast local preflight checks, then commit/push and open a detailed PR (CI-parity optional)."
argument-hint: "<Optional: PR title + intent + any constraints. Slang ok.>"
---
# /prompts:arch-open-pr — $ARGUMENTS
# COMMUNICATING WITH USERNAME (IMPORTANT)
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
2) it passes a **fast, local preflight** (lint/typecheck/unit tests/build-as-needed),
3) it is pushed, and
4) the PR is opened with a detailed, template-based description.

Modes (keep it simple):
- Default = FAST: do the minimal high-signal checks that catch 80% of mistakes quickly.
- If $ARGUMENTS includes `full` / `ci parity` / `parity`: run the CI-equivalent checks locally (can take a while).

## 1) Sync with default branch (thoughtful merge)
- Identify the repo’s default branch from git (prefer `origin/main`, otherwise `origin/HEAD`).
- Ensure we are on a feature branch (not the default branch) before doing PR work. If we’re on the default branch, create a branch with a sensible name.
- Ensure changes are safely committed before merging:
  - If there are in-progress changes you created, commit them (stage only what you touched).
  - Do not sweep unrelated local files into commits.
- `git fetch origin`, then merge the default branch into the feature branch.
- If conflicts occur: resolve them thoughtfully using repo conventions and our intended behavior.
  - If a conflict forces a real product/UX decision not in the repo, stop and ask with the smallest possible question.

## 2) Run local checks (fast by default)
Default (FAST):
- Do NOT try to replicate a full CI matrix locally. Run the smallest reasonable set of high-signal checks:
  - lint/format (or the repo’s “check” target),
  - typecheck (if applicable),
  - **compile/build** (so we don’t ship something that doesn’t build),
  - unit tests (relevant/affected only; avoid the full suite).
- Prefer the repo’s canonical “one command does the basics” entrypoint if it exists (`make check`, `make test`, `./script/check`, `npm test`, etc.).
- Use best judgment on install/setup (use the repo’s preferred package manager / setup step). If there’s a `make install`, use it when it clearly matches how the repo expects deps to be installed.
- Skip redundant work: if checks already ran successfully for the current code (same commit / no relevant changes since), do not re-run them — just record the prior commands + results in the PR.
- If a check fails due to a clearly negative-value test/gate (deleted-code proofs, visual-constant/golden noise, doc-driven inventory gates), prefer deleting or rewriting that test/gate instead of “fixing” code to satisfy it. Record the rationale in the PR.
- Timebox: if we’re heading into “this will take forever” territory, pause and ask before running an obviously long suite (unless $ARGUMENTS requested parity).

Monorepo/mobile nuance (compile means “the active app”, not the world):
- If this repo contains iOS + Android apps, ensure **the app we’re actively changing** compiles for BOTH iOS and Android.
  - Do not build every app/package “just because it exists”.
  - Infer the active app from the diff and repo conventions (nearest app folder, project graph tooling, docs, existing scripts).
  - If multiple apps are clearly affected, compile each affected app (still avoid building everything).
  - Only ask a single clarifying question if it’s truly ambiguous which app is the target.
- If iOS/Android compilation is not applicable (backend/lib/web-only repo), do the equivalent compile/build step for that project (e.g., `tsc` build, `cargo build`, `gradle assemble`, `bazel build`, etc.).

Unit tests (relevant only):
- Prefer “affected/related” test selection if the repo supports it (project graph tooling, “changed packages” scripts, `--findRelatedTests`, etc.).
- Otherwise run the smallest set of unit tests that exercise the touched modules/packages.
- Avoid long integration/e2e suites in FAST mode unless the diff clearly touches that surface or CI will block without it.

If $ARGUMENTS includes `full` / `ci parity` / `parity`:
- Derive what CI actually runs from `.github/workflows/*` (and referenced scripts) and run the closest local equivalent.
- Iterate until green: fix what blocks the PR, then re-run the smallest check that proves the fix.
- Still avoid scope creep: fix blockers; record follow-ups instead of expanding the PR.

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
  - Gotchas / sharp edges worth propagating (and where they’re documented in code comments)
  - Risks/rollout/monitoring notes (if applicable)
  - Screenshots/logs/QA notes if relevant

Then open the PR:
- If GitHub CLI `gh` is available and authenticated, create the PR and print the URL.
- Otherwise, print the prepared title + body clearly so USERNAME can paste it (and provide the exact `gh pr create` command to run).

OUTPUT FORMAT (console only; USERNAME-style):
This is the information it should contain but you should communicate it naturally in english not as a bulleted list that is hard to parse for the user.
Include:
- North Star reminder (1 line)
- Punchline (1 line)
- What you did (merge + checks you ran)
- Result (green/red; what’s blocking if red)
- What got committed + pushed (branch name + commits)
- PR status (opened URL or ready-to-paste title/body)
- Need from USERNAME (only if required)
