---
name: pr-authoring
description: "Write and publish high-quality GitHub pull requests from real repo changes. Use when the user asks to create, open, author, update, or publish a PR, or to turn the current branch/diff into a GitHub PR body/title. This owns PR authoring plus GitHub publication; it is not for code review, release notes, changelogs, or merely printing a suggested PR description."
metadata:
  short-description: "Write and publish GitHub pull requests"
---

# PR Authoring

Use this skill when the user wants a GitHub pull request written and published, not merely drafted.

This is a prompt-only skill. Do not add scripts, controller state, or test harnesses to execute it. Use the host runtime's available GitHub-capable tool or connector to publish the PR.

## When to use

- The user asks to write, create, open, update, or publish a PR.
- The user wants the current branch, diff, commit range, or completed change turned into a polished GitHub pull request.
- The user wants a PR title/body that explains why the change exists, how it works, what changed, risk, rollback, and verification.
- The user explicitly cares that the PR be published to GitHub, not handed back as text.

## When not to use

- The user wants a findings-first code review before merge. Use `$code-review`.
- The user wants release notes, a changelog, commit messages, or a design doc rather than a GitHub PR.
- The repo has no GitHub remote, no publishable branch, no meaningful change set, and no user-supplied PR target. Stop and state the blocker.
- Publishing is impossible because the runtime lacks GitHub access or authentication. Stop and state the blocker instead of printing a pretend PR.

## Non-negotiables

- Publishing is part of the deliverable. Create or update the GitHub PR before returning whenever the required GitHub access exists.
- Work from repo truth: local instructions, branch state, diff, commits, existing PR state, existing repo PR template, and user-provided intent.
- Use `references/pr-body-scaffold.md` as the quality scaffold, not as a paste-all template.
- Choose the relevant narrative lane for the actual change: bug fix, feature, ops/infra, refactor, performance, or a focused mix.
- Delete every placeholder and omit irrelevant sections. Never include template notes, old heading instructions, or empty checklist items.
- Explain why the change exists and how it works. The code already shows what changed; the PR should make review faster and safer.
- Do not invent verification, rollout, rollback, blast radius, metrics, or architecture facts. If evidence is missing, say what is known and what was not verified.
- Do not turn the final answer into "here is the PR text." The final answer is a publication receipt plus any real caveats.

## First move

1. Identify the PR target: current branch by default, or the user-specified branch, diff, commit range, or existing PR.
2. Read the governing repo instructions and any repo-local PR template.
3. Inspect the branch relationship, changed files, diff, and recent commits enough to explain intent, implementation, risk, and verification accurately.
4. Check whether a PR already exists for the branch so the work updates the right GitHub object instead of creating a duplicate.
5. Read `references/pr-body-scaffold.md` and select only the useful structure for this change.

## Workflow

1. **Map the change.** Summarize the user-facing purpose, changed subsystems, important design decisions, compatibility impact, and likely reviewer concerns from repo evidence.
2. **Choose the PR shape.** Use the vendored scaffold to pick the minimum set of sections that fit the change. Prefer a shorter precise PR over a comprehensive but noisy one.
3. **Write the title.** Make it specific and reviewable. Avoid template headings, vague verbs, and implementation-only titles when the user impact is clearer.
4. **Write the body.** Include the real problem or motivation, approach, notable implementation details, blast radius, verification, and follow-up boundaries that matter for this PR.
5. **Validate the body.** Remove placeholders, unsupported claims, irrelevant template sections, stale file names, and any text that could have been written without reading the diff.
6. **Publish to GitHub.** Use the available GitHub-capable path in the current runtime to create or update the PR with the final title/body.
7. **Return the receipt.** Give the PR URL, title, whether it was created or updated, and any concise caveats such as missing verification or blocked publication.

## Quality bar

- Great PRs make the reviewer's first pass obvious: why this exists, what changed, what could break, how it was verified, and what is intentionally out of scope.
- The body should sound like an engineer who owns the change, not a formatter replaying filenames.
- The scaffold should improve judgment and completeness without bloating the PR.
- Weak PRs are generic, placeholder-heavy, unsupported by the diff, or complete-looking but unpublished.

## Output expectations

- On success: return the GitHub PR URL, title, created/updated status, and a compact verification/caveat note.
- On blocked publication: return the exact blocker and the next concrete action needed to publish. Do not include a full standalone PR draft unless the user explicitly asks for it after the blocker.
- Do not run unrelated tests or reviews just to fill the PR body. Report only verification that actually happened or was already evidenced by the repo.

## Reference map

- `references/pr-body-scaffold.md` - vendored PR body scaffold with narrative lanes and quality examples for bug fixes, features, ops/infra, refactors, performance work, and elite PR traits.
