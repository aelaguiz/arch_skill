# Standing Doctrine

The user's standing rules and defaults, extracted from their repeated
run-to-run instructions. These are baked into every Intent Pack by default:
the interview states them in one line and asks only about deviations. They
are never re-interviewed.

## Core requirements (written into every pack)

1. **No new user experience unless this pack names it.** The standing
   default is: same UX, faster and cleaner internals. In non-feature
   projects any new user-facing noun is auto-rejected.
2. **No duplicate patterns.** One source of truth, one way — never the old
   way and the new way side by side, no bifurcated features or legacy
   patterns kept "for safety."
3. **Reduce code.** Prefer subtraction; don't add code where deletion or
   consolidation achieves the outcome.
4. **Delete, don't quarantine.** Bad or retired code is removed, not
   parked, commented out, or fenced behind a flag.
5. **No hypothetical overbuild.** Tiny team; wall-clock is the scarcest
   resource. Protection against imaginary future problems (kill switches,
   sandbox modes, approval workflows, receipt systems) needs a named,
   current, real failure to justify it.
6. **Reviewer findings are input, never scope.** Review waves will propose
   more than the outcome needs; each finding is triaged against the approved
   boundary, feature-shaped findings are rejected by default, and review
   loops are capped — reviewers never terminate on their own.
7. **Proof at the right altitude, wall-clock efficient.** Journey-level
   claims need journey-level automation (simulator or device), not
   widget-only tests; new automation joins the default suite; passed tests
   are not re-run without an invalidator; broken tests in touched areas
   get fixed properly, never waived as pre-existing.
8. **Human-readable surfaces.** Labels and copy stay human. PRs carry
   before/after journey screenshots as embedded images plus an exhaustive
   list of user-facing changes — a PR without them is not valid.

## Execution policy defaults (one consolidated confirm)

| Role | Default |
|---|---|
| Implementation | Codex `gpt-6-astra` at `xhigh`, conducted via `$conductor` |
| Three cynical reviews | Terra (`gpt-5.6-terra`) xhigh, new clean sessions |
| Adversarial implementation reviewer (post-build) | Fable 5.1 xhigh, at most 2 rounds |
| Optional extra cheap reviewer | Luna Max |
| PR authoring + follow-through | Astra xhigh delivery worker, never the parent |
| Secrets, keys, credentials | An Opus 5 sub-agent scoped to that step only |
| Usage limits | `aim codex use` rotation + exact-session resume, never a model swap |
| Worktree | Cut off origin/main; path pinned in the plan document |
| Simulator (mobile work) | A new, renamed, dedicated sim pinned in the document — never a booted one taken over |
| Branching | One branch, one PR; the PR happens when the work is fully done |
| Plan review before dispatch | Astra xhigh and/or Fable 5.1 xhigh, 1–3 rounds hard cap |

## Autonomy defaults (attendance + one question)

- When the user is away, the pack pre-authorizes decisions: the agent
  unblocks itself from first principles and the pack's north stars instead
  of stopping on questions.
- Questions that genuinely need the user are batched, on-screen, in plain
  English, each with a stated default so silence equals the default —
  never dripped one at a time, never in code symbols.
- "Blocked" requires proving the blocker is real, external, and not a
  decision the agent could make; state it as one plain sentence ("waiting
  on you for exactly X") while all unblocked work continues.
- Interruptions and rate limits are resume events, not stops: rotate,
  resume the exact session, continue.
- The pack lists proven capabilities (e.g. "device automation works; docs
  at X") to pre-empt invented blockers that contradict established setup.

## How the interview uses this file

State the applicable block in one line ("standard setup — any changes?"),
record the confirmation, and move on. A deviation the user names is written
into the pack as an override with its reason. If the user's ask itself
conflicts with a core requirement (e.g. a feature request during a
declared repair project), surface the conflict as a question — the user
outranks the default, but the conflict never resolves silently.
