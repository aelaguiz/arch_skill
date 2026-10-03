# milestone-to-pr: skill plan

Date: 2026-09-22. Owner: Amir. Author: Claude (Opus 5.5) via `$skill-authoring`.

Evidence: `/Users/aelaguiz/workspace/psagentspace/docs/ISSUE_TO_PR_MILESTONE_THROUGHPUT_ANALYSIS_2026-09-22.md`
(193 issue-to-pr/epic-to-prs runs on the M5 and the home server, 31 session
families read by hand).

## Job and leverage

**The job.** Amir's specs now arrive as milestones: a sheet or plan, then
M0, M1, 2A and so on, each covering several issues. Today he runs
`issue-to-pr` on them one at a time, so every issue pays the full price:
- its own Pro plan and plan check
- 2 to 12 serial Pro review rounds of about 27 minutes each
- its own PR and CI runs (about 2.8 builds of 11 to 28 minutes each)
- its own closeout

The history shows he already fixes this by hand, mid-run and with
profanity:
- one PR per milestone
- `[skip ci]` until the boundary
- one Pro acceptance
- cheaper reviewers for the middle rounds

Those runs delivered about 5 times the requirement rows per hour.

**The leverage.** The same shape becomes the default for spec milestones.
A skill invocation sets it from the start instead of Amir restating it
("Didn't we revise our plan to not have a CI ceremony except at milestone
boundaries?").

## Canonical asks

- "milestone-to-pr on M0 in the pricing workbook"
- "milestone-to-pr on 2A, primary Opus max, final Pro"
- "use $milestone-to-pr on milestone #5694 and stop at the boundary"

Anti-case: "issue-to-pr 6074" (one issue, its own PR). That stays in
`issue-to-pr`.

## Peer fit

- **Nearest lookalike: `epic-to-prs`.** It works an epic's queue issue by
  issue through `issue-to-pr`, one PR per issue, with shared seats.
  - Discriminator: the unit of delivery. `milestone-to-pr` delivers a
    milestone as one PR per repo and reviews it once at the boundary.
  - Its description currently says "epic or milestone"; add a
    not-for-spec-milestones line pointing to the new skill.
- **`issue-to-pr` stays for single issues.** Add one sentence: an issue
  that belongs to a milestone being delivered by `milestone-to-pr` follows
  the milestone's rules. That kills the "we tackle CI out of habit"
  failure when he runs `issue-to-pr` on a milestone issue.

## What carries over unchanged (the tuned parts)

- **Consultation templates** (`$chatgpt-web` consultation-templates.md).
  Every brief to Pro, the primary, or a reviewer is written from them, in
  Amir's voice, with sources whole:
  - no verdict token, answer cap, scope fence, or SHA
  - the issue as filed plus the completion question in every review
  - Pro writes anything being authored
- **How to reach Pro,** via `$chatgpt-web` and `$browseros`:
  - Pro is literal `Pro` in the picker, read back before Send, plus the
    served slug after
  - consultation profiles only, never `Work`
  - no Pro means no send
  - receipts quote the `6 Pro` pill and the `gpt-6-pro` slug
- **Seat vocabulary.** A primary and a final, named by the user at
  invocation, read exactly as named.
- **`$delegated-implementation`:**
  - workers code, test, and repair
  - the coordinator reviews every changed line
  - skill authorship stays with the parent
- **The rest:**
  - `$startup-pragmatism`
  - `$pr-authoring`
  - the unblocker and goal prompt for long runs
  - never merge
  - scope frozen from the issues and Amir's words
  - bots advisory
  - the Pro wait belongs to the agent
  - browser pages the run opens are the run's to close

## What changes, and the evidence for each

1. **The unit of delivery is the milestone.** One branch and one PR per
   repo per milestone. Issues land as commits. No per-issue PRs, no drafts,
   and no stacks of per-issue rungs.
   - Evidence: stack churn cost 10 to 12 hours in the older epics. Each
     rebase re-ran every rung's CI. Amir: "stop doing individual PRs",
     "What's the fucking point?" (of drafts).
2. **Pro writes the milestone plan once, with family D, in the milestone
   thread,** and the plan carries a work order per issue.
   - An existing Pro-written plan that covers the milestone satisfies this.
   - No separate plan check when the same seat wrote it and it has not
     moved.
   - The plan pins who owns each piece of state before workers code, and
     says how the milestone merges on its own without breaking what ships.
   - Evidence: #5967 went through 12 rounds because the source of truth was
     never specified. 2A was "accepted" but could not merge.
3. **Each issue gets a cheap check as it lands.** The primary reads it with
   Template A in a clean context. The default primary is a native child on
   the coordinator's own model.
   - The next independent issue keeps going during the check, and findings
     go to the next worker brief.
   - Evidence: Opus reviews took 9 to 15 minutes against Pro's 16 to 34,
     and still found real bugs. 2A's single late acceptance took 6 Pro
     rounds (5, 2, 1, 1, 1, 0 findings).
4. **The final (default Pro) reviews the milestone once at the boundary,**
   with the new milestone-review template.
   - Findings are fixed in one batch, then one B round follows.
   - A fresh full review happens only when a fix changed the design.
   - Fixes inside the same design are verified by the primary.
   - The coordinator weighs each finding against the issue's real risk.
   - Evidence: #16155's 19 rounds of "what if it crashes halfway";
     #16213's last 3 rounds on stale assertions.
5. **CI runs once per boundary, alongside the final review.**
   - Intermediate pushes do not trigger CI where the repo allows (for
     example `[skip ci]`). The boundary push triggers CI the normal way,
     with no empty commits or manual builds.
   - Nobody waits on CI before or during the final's read.
   - When the final answers, CI and bot results are read once, and every
     finding (final, CI, bots) is fixed in the same batch before the B
     round.
   - Evidence: CI and bots catch a different class of defect. The 2A
     boundary run found a UI regression that 11 Pro rounds missed, and a
     bot found a route bug after Pro cleared #5962 twice. Running CI after
     Pro clears pushes those findings to the end, where they reopen Pro.
     This keeps the 09-17 rule's point (never wait on CI for a review)
     while removing one round trip.
   - **Deliberate change:** today's rule is "CI only after Pro cleared".
     Flagged for Amir.
6. **Task zero is proving the verification path works.**
   - Local tests start, QA and device lanes the plan needs boot,
     toolchains match, and CI infrastructure is sound.
   - Fix what is broken first, as milestone work.
   - Evidence: cratejoy had 120 of 285 pytest commands never start, and
     Pro stood in for tests for two days. PvP #6073 spent about 15 of 22
     hours on SDK and PATH drift.
7. **Keep moving.** Never end a turn while a worker, Pro, a device run, or
   CI is in flight. No authority asks for in-scope QA and test-environment
   work. Fix red things instead of stopping on them.
   - Evidence: the largest single sink in every slice (93 empty turn
     endings on rustai, 5.3 h dead air on PvP, 4.2 h on decisions already
     made).
8. **Closeout happens once per milestone.** Keep the tracker live if the
   user keeps one. No per-issue Slack posts or handoff comments.
9. **The milestone's delivery rules go into each covered issue.** Amir asked
   for exactly this so later single-issue runs don't fall back to per-issue
   CI.

## Package

- `skills/milestone-to-pr/SKILL.md`: the runtime contract, about 250
  lines, prompt-only.
- `skills/milestone-to-pr/agents/openai.yaml`: `allow_implicit_invocation:
  false`, plus a default prompt.
- **Seat mechanics:** reuse `skills/issue-to-pr/references/primary-and-final.md`
  (as `epic-to-prs` does). Edit its default-seat sentence so a calling skill
  can set its own defaults.
- **Templates:** add two families to
  `skills/chatgpt-web/references/consultation-templates.md`, in Amir's
  voice, shaped from D and A:
  - K, planning a milestone
  - L, reviewing a milestone at its boundary, plus how the primary uses A
    for one issue landing inside the milestone PR

  They live next to their siblings, so there is one owner for templates.
- **Peer edits:**
  - `issue-to-pr`: one sentence about milestone issues
  - `epic-to-prs`: description boundary
  - `delegated-implementation`: description mention
  - `unblocker`: the list of callers
- **Install and docs:** `Makefile` SKILLS / CLAUDE_SKILLS / GEMINI_SKILLS,
  the `README.md` inventory, and `docs/arch_skill_usage_guide.md`.
- No scripts. No dispatch-evidence reference yet; this plan and the
  analysis are the maintainer background.

## Overbuild check (what was cut)

- **No new seat vocabulary or seat reference:** reuse primary and final.
- **No milestone state file or tracker format:** the existing plan doc and
  worklog serve.
- **No per-issue Pro review, no automatic resubmission loop, no round cap
  number:** the stopping rule is judgment about whether a fix changed the
  design.
- **No CI-trigger tooling:** the normal boundary push.
- **No changes to `pr-review-followthrough`:** the milestone reads CI and
  bots itself at the boundary.

## Validation

1. Run `npx skills check`, then `make install` locally, and confirm the
   installed tree.
2. **Dry-run regression.** A fresh Codex session (Astra xhigh, the usual
   parent) is told to use `$milestone-to-pr` on a real milestone scenario
   (read-only), with no browser, builds, GitHub writes, or Pro sends. It
   writes out what it would do and the exact briefs it would send: the Pro
   plan, the primary's per-issue check, the final's milestone review, and a
   worker brief. Check the output against:
   - the template vibe: sentences, Amir's voice, sources whole, `@GitHub`,
     no verdict token, cap, fence, or SHA
   - one PR per repo and no per-issue Pro
   - task zero first
   - CI deferred to the boundary and read with the final
   - the stopping rule
   - no turn-ending while work is in flight
3. Iterate once on what the dry run gets wrong, then rerun it.
4. Publish with `$amir-publish`.

## Dry-run iteration log

**Round 1** used the same read-only M0 ask on two readers: Codex Astra xhigh
through `aim codex run`, and a native Claude reader.
- The Claude reader wrote briefs that kept the template sentences word for
  word. Codex kept the shape but shortened and paraphrased the question
  lists.

Both readers raised real gaps, now fixed in the skill:
- **Template fidelity.** Write from the template's own sentences, keep
  every question, never shorten.
- **CI.** "Once" was wrong after the fix batch. CI now runs at the boundary
  push and again on the repaired head, and is read once each time. The
  commit that completes the milestone goes out without the skip marker. CI
  red from other milestones' code is named, not fixed. A repo without CI is
  reported as having none.
- **Project-wide working PRs** (cratejoy keeps one PR per repo for the whole
  project). A milestone on such a PR ends as "accepted", not merge-ready.
  Template L says to read the whole PR and judge done-ness against this
  milestone's issues.
- **Precedence.** Delivery rules the user already wrote on the issues
  outrank the skill's defaults.
- **Delivery rules** go on each issue as a comment, leaving the Pro-written
  bodies as filed.
- **Adopting a milestone already partly built.** Late primary reads are
  allowed, and nothing still answering is resent.
- **Threads.** The plan is one continuing thread; the boundary review
  starts clean.
- **The rest:**
  - No secret values in attachments.
  - One PR per code repo, wherever the issues are filed.
  - Requirements that need production are named as owed.
  - "Arm the host's wake-up" is replaced with "how it waits is the harness's
    business" (Codex has no heartbeat tool).

Left out on purpose, as workspace policy rather than skill doctrine:
- who drives a browser-only real check
- worker-model pinning mechanics in Codex
