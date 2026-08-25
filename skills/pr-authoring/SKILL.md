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

- The user wants a findings-first code review before merge. Use the host
  agent's normal review response.
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
- For plan-backed work, include a compact scope receipt: canonical plan path,
  one-line human-authorized outcome, approved initial convergence closure or
  `none`, explicit human-approved expansions or `none`, and material
  out-of-scope findings intentionally not built. Point to plan anchors; do not
  copy the contract or create a second plan.
- Every PR body includes a `## User-Facing Changes` section, in one of three
  shapes: an exhaustive numbered list of every user-visible change, each item
  with at least one embedded screenshot captured from the running app; the
  literal claim `None. Nothing a user can see, read, hear, or do changes in
  this PR.`; or a quoted human waiver recorded verbatim. Exhaustive includes
  loaders, spinners, skeletons, empty states, error toasts, copy edits, layout
  shifts, color, animation, and timing changes, re-sequenced screens, and
  removed states. Only a human can approve or waive the section: never write a
  waiver the human did not utter, and never downgrade an enumerated list to
  `None`.
- Verify every embedded image URL before publishing: it must be HTTPS and
  return HTTP 200 with an image or video content type. `file://`, localhost,
  and local filesystem paths are forbidden. A dead image is a publication
  blocker, not a caveat.
- When the PR enumerates user-facing changes, or changes behavior a human
  could verify, include a QA Test Plan written from the tester's seat, not the
  debugger's: numbered steps on a real build with the expected result per
  step, runnable by a non-engineer; the setup lane that gets a tester into
  the right state (account type, seeded data, dev-menu toggle, internal
  build), or exactly what an engineer must hand the tester; and a link to a
  visual guide when the path is more than a couple of steps. "Verified
  locally" and test-file names are not a test plan.
- Every bug-fix PR includes a `Reproduction: Before And After` section: the
  exact steps that made the bug happen on a build without the fix with the
  observed failure, then the same steps re-run on the fixed build with the
  observed correct behavior, naming the build identity (version/build or
  commit) on both sides. The pair is the proof that the fix fixes the bug
  rather than a theory about it. Compressed triggers, seeded state, and
  direct entry at the failing step are encouraged over soaks and
  full-journey replays; name the compression so the reader knows why it is
  equally valid. Write `not attempted because <blocking fact>` plus the
  substituting evidence only when reproduction was genuinely impossible;
  "low value", "obvious", and time pressure are not blocking facts.
- Do not turn the final answer into "here is the PR text." The final answer is a publication receipt plus any real caveats.

## First move

1. Identify the PR target: current branch by default, or the user-specified branch, diff, commit range, or existing PR.
2. Read the governing repo instructions and any repo-local PR template.
3. Inspect the branch relationship, changed files, diff, and recent commits enough to explain intent, implementation, risk, and verification accurately.
4. Check whether a PR already exists for the branch so the work updates the right GitHub object instead of creating a duplicate.
5. Read `references/pr-body-scaffold.md` and select only the useful structure for this change.

## Workflow

1. **Map the change.** Summarize the user-facing purpose, changed subsystems, important design decisions, compatibility impact, and likely reviewer concerns from repo evidence. Enumerate every user-facing change in the diff and collect or capture the screenshot that proves each one before writing the body.
   For plan-backed work, recover the human scope and approval anchors before
   treating the latest plan text as authority.
2. **Choose the PR shape.** Use the vendored scaffold to pick the minimum set of sections that fit the change. Prefer a shorter precise PR over a comprehensive but noisy one.
3. **Write the title.** Make it specific and reviewable. Avoid template headings, vague verbs, and implementation-only titles when the user impact is clearer.
4. **Write the body.** Include the real problem or motivation, approach, notable implementation details, blast radius, verification, and follow-up boundaries that matter for this PR.
5. **Validate the body.** Remove placeholders, unsupported claims, irrelevant template sections, stale file names, and any text that could have been written without reading the diff. Confirm the `## User-Facing Changes` section is present and truthful, and fetch every embedded image URL to confirm it renders.
   Confirm the diff does not exceed the scope receipt. If it does, stop for
   subtraction or a human approval/re-approval instead of publishing a laundered
   scope story.
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
