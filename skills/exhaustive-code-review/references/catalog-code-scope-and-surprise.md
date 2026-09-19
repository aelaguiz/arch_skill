# Catalog Slice: Scope And Surprise

Applies when the change has a diff and the target carries what commissioned it:
the request, issue, plan, or instruction, plus the description the change ships
with. Needs the trunk for comparison, and a run or screenshots for the visual
half of C-07 when the target has them.

All three compare the delivered change against what was asked for, and they are
cut by what they compare. C-06 compares user-visible behavior against the
requirement lines. C-07 compares what a user meets — look, feel, and when things
happen — against the trunk when the stated scope was not a product change. C-37 compares the changed-path list against the
named surface, whether or not a user can see the result. One change can fail all
three, so name the comparison that found each defect and report it once.

A change can be correct, green, and approved elsewhere and still fail these
checks. Passing tests and another reviewer's approval are not reasons to stay
quiet.

## C-06 A user-visible change nobody commissioned

Question: Would the person who commissioned this work be surprised to find this
behavior in the result?

Needs: the diff; the issue or plan with its acceptance criteria; the approved
mocks; the user's own turns where the target carries them; the description,
because a necessary consequence is allowed only if it is disclosed there.

Read: Build the inventory in two columns — what was asked for, and what is
actually there. List every new or changed user-visible thing in the diff:
widgets, copy, navigation destinations, defaults, economics such as costs,
awards, pricing, eligibility, limits, and progression, state transitions,
feature availability, and the meaning of telemetry. Trace each one to a line of
the commissioning artifact. Decide first what that artifact is. When the user's
own words are in the target, column one is built from those words alone. An
issue, plan, or spec that the agent wrote, including one the user told it to
write, enters column one only line by line, and only for lines that restate
something the user said. A line the user never said is the agent's addition,
however reasonable it reads, and tracing a user-visible element to it is the
same as tracing it to nothing. Do not reason that the issue was commissioned
and therefore every line in it was: an instruction to write an issue is not an
instruction to build what the issue says. Requests are dictated and
paraphrased, so compare meaning, not wording. Check the inverted direction too: an approved user-facing
element removed without authorization is the same defect with the sign flipped.
Read the description for disclosure, and remember that an agent's own inference
is not the user's approval — "approved", "confirmed", or "as agreed" written in
an issue, tracker, or description needs a real turn behind it.

Block when: a user-visible behavior change traces to no line of the
commissioning artifact, or only to a line the agent itself added to an issue,
plan, or spec, and the description does not disclose it; or an approved
user-facing element was removed with nothing authorizing the removal.

Do not block when: it is a necessary consequence of the requested work and the
description says so plainly — "cleanup", "refactor", "while we were here", test
updates, generated output, and implementation convenience are not disclosure;
the user authorized the addition in the session; the change is confined to data,
internals, and tracking with no user-visible delta, since non-trivial internal
change is fine and only surprise at the surface is not; the removal or narrowing
is the one the user asked for. The remedy is a cut list naming each unrequested
thing and the requirement line it failed to match, never a flag, a kill switch,
a staged rollout, or a split of the change. A new control surface is C-09's
finding, a visual change under a non-product scope is C-07's, and paths outside
the named surface are C-37's.

Examples:

- **[REQUIRED REPAIR] A haptics task returned a tuning subsystem.** A tuning
  controller, a tuning catalog, persistence, and playlist rotation arrived with
  the requested work, and none of the four traces to a requirement line.
  Compared the delivered capability list with the ask. Repair target: a cut
  list naming the four.
- **[REQUIRED REPAIR] An audio change quietly added de-duplication.** Sounds
  triggered in quick succession now collapse into one, so dragging a control
  plays a single click instead of many. The behavior looks deliberate and
  nothing commissioned it. Compared the new playback rule with the issue text.
  Repair target: remove the de-duplication.
- **[REQUIRED REPAIR] Approved reward screens deleted as ceremony.** The change
  removes user-facing reward screens on the theory that the reward is ceremony,
  while the mocks approved them as a primary part of the experience. Compared
  the removed surface with the approved mocks. Repair target: restore them.
- **[OBSERVATION] A large internal change with no surface delta.** The diff
  rewrites a persistence layer and touches no widget, copy, default, or
  economics value. Traced each changed behavior to the user-visible surface and
  found none.

## C-07 Collateral change under a non-product scope

Question: The stated scope was not a product change — did look, feel, and when
things happen come out identical to the trunk?

Needs: the diff; the stated scope, from the issue, the title and description, or
the instruction; the trunk, for comparison; screenshots or a run for the visual
half, when the target has them.

Read: When the stated scope is performance, refactor, telemetry, migration,
cleanup, or a bug fix, inventory every hunk that touches layout, padding, safe
areas, geometry, animation timing, asset resolution, theme values, tuning data,
copy, navigation, or gating. Compare each against the trunk, not against the
branch's own earlier state: the before state is the trunk. Anything presented as
a restoration is compared with the trunk version of that behavior, because
re-approximating removed behavior from memory brings its own bugs; the restored
code either does what the trunk did or it is new work. Hand-tuned surfaces
deserve the closest reading. Inventory the control flow the same way, because a
scope that only observes — telemetry, logging, metrics, analytics — has no
licence to change when anything runs: a new early return, a new await, a
reordered sequence, or work that used to run in the background and now blocks
the caller all change the product while the diff reads as measurement. The hunk
inventory can be done from the diff alone; the visual verdict needs a run or
pictures, so say which half you could evaluate.

Block when: the stated scope is not a product change, a hunk changes a surface
the user can see, and the description does not disclose it; a hunk under an
observational scope changes control flow on a live path — an early return, an
await, an ordering, or an asynchronous path made synchronous; or something
presented as a restoration does not match the trunk version of that behavior.

Do not block when: the surface is the scope, because the change was commissioned
to alter it; the restoration is the one the user asked for and it matches the
trunk; the description discloses the visual consequence as a necessary result of
the requested work; the difference is pixel-level against a mock, since the mock
explains intent and the application's own styles win — and a pixel-comparison
harness is not the repair, it is C-36's finding if one is added; the
control-flow edit is itself part of what the request asked for. An unrequested
user-visible feature under a scope that was a product change is C-06. Whether the risk the change carries is worth the defect it answers is
C-40. If the real problem is that the reported cause is still untouched, report
that under C-17.

Examples:

- **[REQUIRED REPAIR] A label change restyled the neighbouring ribbons.** The
  work was commissioned for chip-stack labels, and the diff also restyles the
  opponent action ribbons, which are hand-tuned and were not in scope. Compared
  the touched hunks with the stated scope. Repair target: revert the ribbon
  styling.
- **[REQUIRED REPAIR] A rendering-performance change altered what renders.** The
  engine was commissioned to get faster; the result changes which playables
  render and how they look. Compared the rendered result with the trunk. Repair
  target: keep the performance work and restore the trunk's output.
- **[REQUIRED REPAIR] A stability fix left a grey bar on a screen it never
  named.** The fix changed safe-area handling, and an outro screen now renders
  with a grey band across it. Compared that screen against the trunk. Repair
  target: keep the stability fix and leave the screen's insets as the trunk had
  them.

## C-37 The diff leaves the named surface

Question: Does every changed path fall inside the surface the task named?

Needs: the diff, with commit messages and order where available; the task's
named surface — the plan, issue, or instruction naming files, subsystem, branch,
or worktree; the repository's own instruction file, because permissions are
stated per repository and are never inferable.

Read: Compare the changed-path list with the surfaces the task named. Weight
shared and environmental files heavily: environment files, continuous
integration configuration, agent instruction files, build scripts, global
styles, credential inventories, another repository's tree. Commit order is
evidence: the touched-file set usually diverges right after a commit message
about fixing a build, test, lint, or runtime error, because the error was
treated as a new assignment instead of as a reason to re-read the plan. The
sharpest single tell is shared configuration edited so that one machine's run
succeeds; another worktree on the same machine building fine is the evidence
that the fault was local. Check which branch or worktree the commits landed on,
not only what they contain, and read what the diff deletes or rewrites:
personally authored documents, goal files, and canonical checkouts the task
never named.

Block when: changed paths fall outside the named surface and nothing in the
target authorizes them — heaviest on shared configuration, continuous
integration, agent instruction files, build settings, credentials, and commits
on a branch the task did not name; or product code, authentication,
configuration, or global styles were changed to make a local environment fault
go away.

Do not block when: the task named those files, or the user granted the surface
in the session — grants are stated out loud, per repository and per work item,
and do not generalize, so the same week can carry a merge permission in one
repository and a commit ban in another; the change is a necessary consequence
the description discloses; repairing the broken environment is the work and the
diff explains why it broke, since the rule is to fix the tool and say why it
failed, while routing around it by pinning a version, switching environments,
disabling a check, or wrapping a flaky local command in a retry is the defect;
the task named the deletions. Whether an edited instruction file makes an agent
less capable is a different question, owned by C-41 and C-44; this check asks
only whether the edit was in scope.

Examples:

- **[REQUIRED REPAIR] A task scoped to one goal file rewrote the repository's
  agent instructions.** Compared the files the instruction named with the files
  the diff touches. Repair target: revert the instruction-file edit and propose
  it on its own if it is wanted.
- **[REQUIRED REPAIR] Commits landed on the trunk, not the named branch.** The
  task named a branch and a worktree; the history puts the work on the trunk.
  Compared the branch the task named with the branch the commits landed on.
  Repair target: move the commits to the named branch.
- **[REQUIRED REPAIR] A local build fault repaired in the product.** Global
  styles were cleared and authentication changed in the application to get a
  local build working, while other worktrees on the same machine built fine.
  Compared the fault's scope with the changed paths. Repair target: reseed the
  local environment, say why it failed, and revert the product changes.
