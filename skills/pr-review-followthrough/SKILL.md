---
name: pr-review-followthrough
description: "Explicit-invocation PR follow-through loop for an already-open GitHub pull request: poll the PR, handle every new review or comment thread, reply on-thread with accept/decline rationale, push fixes to the same branch, and repeat until the PR is merge-ready."
---

# PR Review Followthrough

Use this skill when the job is not "review a PR once" but "own an already-open PR until review feedback, CI, and merge-readiness are all clean."

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

## When to use

- The user wants the agent to stay on a submitted PR and keep polling for new code-review feedback.
- The user wants every review item, inline comment, and top-level PR ask handled and replied to.
- The user wants the agent to push follow-up commits to the same branch until the PR is fully merge-ready.
- The user wants a convenience loop that keeps working while humans and CI continue to respond.

## When not to use

- The PR does not exist yet and the real job is PR drafting, branch prep, or PR description authoring.
- The user wants a one-shot code review, summary, or diff audit rather than a long-lived follow-through loop.
- The user wants automatic merging, merge-queue submission, or post-merge cleanup. This skill stops at merge-ready.
- The repo, branch, or GitHub client cannot be written to from the current environment.

## Preconditions

- A real PR URL or PR number already exists.
- The agent has authenticated GitHub access that can read PR state and write replies.
- The agent has a local checkout for the same repo and can push follow-up commits to the PR branch.
- The user is okay with the agent staying in a polling loop for minutes or longer until the stop line is met.

## Non-negotiables

- Treat this as explicit-invocation work. Do not start a long-lived polling loop unless the user directly asked for it.
- Poll live GitHub state on every pass. Do not trust stale local memory, notification summaries, or prior screenshots.
- Check the full PR surface each pass:
  - review decision / blocking review state
  - review submissions
  - inline review comments and replies
  - top-level PR comments / asks
  - required checks
  - mergeability, conflict state, and branch-behind state
- Reply to every actionable item on the exact GitHub surface that raised it, even when declining the change or pointing out that it is already fixed.
- Prefer one branch, one PR, one coherent follow-through loop. Do not fork the work into side branches or parallel PRs unless the user explicitly wants that.
- After each accepted change, run the smallest relevant verification, push to the same PR branch, and continue polling.
- Stop at merge-ready. Do not click merge, enable auto-merge, or queue the PR unless the user separately asks for that.
- Fail loud on irreducible blockers:
  - missing GitHub write access
  - missing push access
  - conflicting reviewer direction that changes product or policy meaning
  - failing external systems the agent cannot repair from the repo
  - human-only decisions about scope, design, or release policy

## First move

1. Resolve the PR URL/number, repo, local branch, and current head SHA.
2. Read the repo's actual review-policy and CI surfaces if they exist.
   - Prefer repo-root `AGENTS.md`, `CLAUDE.md`, PR templates, review-policy files, and workflow files over memory.
3. Capture a baseline PR snapshot:
   - draft/open state
   - head SHA
   - review decision / requested-changes state
   - required-check state
   - mergeability / behind / conflict state
   - inline review comments
   - top-level review bodies
   - top-level PR comments
4. Tell the user the loop is running and name the current blocker.

## Canonical loop

1. Snapshot the live PR again from GitHub.
2. Partition inputs into actionable buckets:
   - inline review comments and unresolved review threads
   - top-level review summaries with concrete asks
   - top-level PR comments requesting code, QA, docs, or explanation
   - failing required checks
   - mergeability / branch-update problems
3. For each actionable item, choose one disposition:
   - accept and fix
   - partially accept and fix the bounded part
   - decline with evidence
   - already handled, with a commit or reply pointer
   - blocked on an irreducible human decision
4. Reply on the exact thread or comment surface that raised the item.
5. If a change was accepted:
   - make the smallest coherent patch
   - run the narrowest relevant verification
   - commit
   - push to the PR branch
6. After a push, resnapshot the PR and reset outstanding work against the new head SHA.
7. Wait a few minutes and repeat.
   - Default cadence is about 3 minutes.
   - Shorten only when the next signal is imminent, such as immediately after a push while required checks are starting.
   - Back off only when host constraints or rate limits force it.

## Actionability rules

- Treat these as actionable by default:
  - `CHANGES_REQUESTED`
  - new inline review comments
  - new top-level PR asks
  - failing required checks
  - merge conflicts
  - branch-behind / update-branch requirements
- Treat these as non-actionable once explicitly handled:
  - approvals
  - acknowledgements
  - duplicate notifications
  - already-replied stale comments that have not materially changed
- A review item is not done just because the code changed. It is done when:
  - the code path is updated if needed, and
  - the agent has replied on-thread with the disposition.
- If two reviewers conflict, do not guess. Summarize the conflict, take the safest bounded step if one exists, and escalate only if the disagreement changes product, policy, or merge authority.

## Merge-ready stop line

Consider the loop complete only when all of these are true:

- The PR is open and non-draft.
- The current head SHA has no unhandled actionable review items or top-level asks.
- GitHub no longer shows blocking review state for the current head.
  - If the repo uses required reviews, the PR should be in the repo's approved / mergeable state rather than still waiting on blocking review.
- Required checks are green, or otherwise in the repo's accepted merge-ready state.
- The branch is mergeable, not conflicted, and not blocked on being behind base.
- Every accepted, partially accepted, declined, or already-fixed review item has a reply on the thread that raised it.

## Output expectations

- On start:
  - identify the PR and current head SHA
  - state the first blocker
- During the loop:
  - send concise progress updates only when the blocker changes materially
  - do not spam the user every poll cycle
- On completion:
  - give a short merge-ready summary with:
    - PR URL
    - final head SHA
    - review status
    - checks status
    - any residual human-only note before merge
- On failure:
  - state the exact blocker
  - state the last fully verified PR state
