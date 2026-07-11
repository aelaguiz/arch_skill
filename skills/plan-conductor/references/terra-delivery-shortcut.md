# Terra Delivery Shortcut

`plan-conductor terra` is the explicit end-to-end delivery preset for a user
who wants the standard high-rigor path without restating every handoff. It
composes existing skills; it does not replace their contracts or add a runner.

## Trigger Boundary

Activate this preset when the user explicitly asks for `plan-conductor terra`
or clearly asks for the standard Terra delivery path. A normal
`plan-conductor` request that happens to choose a Terra worker is still the
normal conductor workflow unless the user also asks for the preset's
worktree, three-review, and PR follow-through path.

The plan path or recoverable target plan is still required. Natural-language
scope such as an explicit phase range remains binding.

## Locked Policy

- This preset deliberately selects the external `$agent-delegate` lane. The
  exact Terra xhigh profile, dedicated-worktree continuity, durable session
  receipts, and downstream delivery handoffs are the benefit; do not silently
  replace it with a generic native child.
- Reuse a target-matching dedicated worktree when one exists; otherwise create
  one from the intended base branch using the repo's branch and worktree
  conventions. Reuse the current checkout when it is already the right
  dedicated worktree. Inspect `git worktree list --porcelain`, branch state,
  and existing PR state before choosing. Never delete, clean, or repurpose an
  unrelated worktree, and never move unknown uncommitted work between
  worktrees.
- Resolve `terra xhigh` exactly as
  `runtime=codex, model=gpt-5.6-terra, effort=xhigh`. Use that policy for
  implementation, repair, delegated verification, the cold verifier, and the
  three cynical review sessions. Do not ask for runtime, model, or effort and
  do not silently substitute another choice.
- The conductor owns plan interpretation, slice contracts, audit, finding
  triage, proof freshness, and the final acceptance decision. Terra workers
  own source edits and proof runs during the conductor stage.
- Keep the ordinary cold verifier enabled unless the user explicitly disables
  it. The three new clean external cynical reviews satisfy and strengthen the
  ordinary cynical-instrument portion of the final gate; they do not duplicate
  direct instrument runs, and they do not replace the cold verifier.
- Keep the same worktree and branch through implementation, review repairs,
  PR publication, and PR follow-through.

## Delivery Path

1. **Worktree.** Select the safe matching worktree or create the dedicated
   worktree and branch. Record the worktree path and branch in the conductor
   log's Resume Snapshot.
2. **Conductor implementation.** Run the normal plan-conductor lifecycle with
   external Codex `gpt-5.6-terra` at `xhigh`: intake, readiness, phase-sized
   `$agent-delegate` fresh-resumable workers, independent verification,
   cynical parent audit, send-backs, checkpoints, plan completion annotations,
   whole-plan sweep, and cold verifier.
3. **Three independent reviews.** Once the conductor believes the plan is
   complete, use `$agent-delegate` to launch three `fresh-one-shot` Terra xhigh
   external sessions, parallel when safe. Give each the plan path, exact review
   target, base/head boundary, and applicable repo instructions, but not the other
   reviewers' conclusions or the implementation story. Assign exactly one
   installed review skill per session:
   - `$cynical-code-review`
   - `$cynical-architecture-review`
   - `$cynical-cruft-removal`
4. **Triage and repair.** Treat every reviewer result as a claim. The conductor
   checks each finding against the plan and current repo, judges factual
   validity separately from scope disposition, and sends only `authorized`,
   `frozen-convergence-required`, or required subtraction work to the
   healthy owning implementation session, or a new clean external Terra xhigh
   repair worker when ownership or session health requires it. A broader
   reviewer recommendation needs explicit human approval and re-freeze.
   Independently reproduce the affected proof.
5. **Re-review.** A review is clean only at its own native clean verdict:
   `approve` for code and architecture, and `no-material-cruft-found` for
   cruft. After material repairs, rerun every affected review in another new
   clean external Terra xhigh session. `coverage-incomplete`, `scope-incomplete`,
   `unsafe-to-judge`, or open required repairs do not pass the gate.
6. **Publish the PR.** After all plan proof and all three review lanes are
   clean and the scope-provenance gate is `frozen-clean`, invoke
   `$pr-authoring` against the same branch and worktree. Let that
   skill inspect repo truth, publish or update the GitHub PR, and return the PR
   URL.
7. **Follow through.** Treat this preset as the user's explicit authorization
   to invoke `$pr-review-followthrough` on that PR. Poll live GitHub state,
   answer every actionable thread, make and verify warranted same-branch
   fixes, push, and continue until its merge-ready stop line is true. Do not
   merge, enable auto-merge, or enter a merge queue unless the user separately
   asks.

## Completion Line

The shortcut is complete only when the plan and conductor log are complete,
the cold verifier and all three new clean external cynical review lanes are
clean on the accepted code, the PR exists, and `$pr-review-followthrough`
reports the current PR head merge-ready. A missing CLI, unsafe worktree state,
unavailable review skill, GitHub authorization failure, irreducible CI failure,
or real human product decision is a blocker to report, not a reason to skip a
stage.

The shortcut may repair authorized findings and subtract unauthorized work. It
must not implement a broader reviewer recommendation automatically, and it may
not publish or enter PR follow-through while a scope-cycle or human scope
decision remains open.
