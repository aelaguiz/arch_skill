# Catalog Slice: Comments And Claims

Applies when the change contains code whose correctness is not visible from
reading it, a deliberate departure from what the surrounding code does, or prose
that describes the change. Needs the diff, the repository at head with history
for the touched lines, and whatever prose accompanies the change: the request,
the pull request body, the README, and changed comments.

C-19 is the reasoning behind a change, C-20 is the state of the code, and C-26
is what the prose says about both. Report each defect once.

## C-19 Non-obvious code with no why-comment

Question: Does each delicate thing this change introduces say why it is that way
and what breaks if someone changes it?

Needs: the diff; the repository at head with history for the touched lines; the
review discussion, if a finding was raised there and declined.

Read: Go through the diff for the parts whose correctness is not visible from the
code — a tuning constant, a cache key, an ordering constraint, a lifecycle hook,
a clamp, a pre-warm, a timing window, a performance optimization, a fix whose
shape looks arbitrary. For each, look for an adjacent comment giving the reason
and the breakage: why this value, what goes wrong if the next reader moves it.
The strongest form of the finding compares the history of the touched lines with
the current hunk — a repair landing on lines an earlier repair already touched,
with nothing recorded either time, is the area that will be regressed again. Read
comment density against delicacy: a large performance-sensitive change with no
comments on the performance-sensitive parts is this finding. Where a review
raised a finding and the author declined it, look for the reason at the cited
file and symbol; a reason living only in the review discussion is invisible to
the next reader, who will undo it. Errors thrown at a boundary are comments for
whoever reads them: check that the message says in plain language what the
condition means.

Block when: a delicate change lands with no adjacent comment giving its reason
and what breaks, and especially when the same lines already carry an earlier
repair; or the rationale for a declined review finding exists only in the review
discussion.

Do not block when: the code is self-evident — never ask for a comment that
restates it; the block is merely hard to follow, where the repair is
restructuring and not a comment; the delicate code is a test. Missing standalone
documentation is never this finding, and naming and formatting never are. If a
comment exists and now teaches something the code no longer does, that is C-26.

Examples:

- **[REQUIRED REPAIR] Layout clamp repaired again with nothing recorded.** The
  clamp that handles long text changed in an area whose history shows two earlier
  repairs, and the new value says nothing about which outlier it protects or what
  it costs the common case. Compared the history of the touched lines with the
  comments in the hunk. Repair target: state at the clamp which case it handles
  and what degrades when the value moves.
- **[REQUIRED REPAIR] Declined finding recorded only in the review.** The author
  explained in the review why the ordering is deliberate and closed the thread;
  the file says nothing, so the next reader will make the same objection and act
  on it. Compared the review record with the code at the cited symbol. Repair
  target: put the reason, and the alternative that was rejected, at that symbol.
- **[OBSERVATION] The block needs restructuring, not a comment.** The new branch
  is correct but takes several readings to follow, because three conditions are
  inlined into one expression. A comment on top of an unreadable block is the
  weaker repair; name the structure instead.

## C-20 Temporary or divergent code with no label

Question: Does every deliberate departure in this change say at the site that it
is deliberate, why it is there, and what the end state is?

Needs: the diff; the request, plan, or pull request body, to see whether a probe
was authorized and whether the permanent fix is in the same change; the
repository's own instructions, where carve-outs and waivers live.

Read: Walk the diff for departures from what the surrounding code does: a debug
constant, a local-testing toggle, a disabled path, a diagnostic throw, a marker
that opts out of the repository's own pattern, raw access around an owner,
retained legacy code, a second pattern for something that already has one. For
each, look for an adjacent comment saying it is deliberate, why, and when it
goes. The label is the requirement, not the absence of the hack: a throwaway
probe is a legitimate thing to write, and the comment is the condition on it,
while the same code becomes a defect the moment it is load-bearing. Compare the
change against its own request: a probe written to de-risk a fix has no reason
to ship in the same change as the fix it informed. Where a token or admin
affordance appears, the comment also has to say what it is not for, because that
is what stops the next reader reusing it.

Block when: a deliberate departure carries no adjacent comment saying it is
deliberate, why, and when it goes; or a probe ships alongside the permanent fix
it was written to inform.

Do not block when: the comment is there — the word "temporary" in a comment is
what this check asks for, not a smell; the retention is commented and tracked,
such as a planned restoration, a placeholder for work not yet written, or a
carve-out the repository names; the repository marks the work as a hobby project
or an experiment. Two live paths stay quiet here only when the divergence is
labelled at both sites and the request or the repository's instructions show it
was decided; otherwise C-01 governs. Hedged retention with no stated
restoration — kept for now, quarantined, delete or migrate later — is how an old
path survives, and belongs with C-01 rather than being reported twice.

Examples:

- **[REQUIRED REPAIR] Debug-only constants ship with nothing saying so.** Two
  constants exist to shorten a timer during local testing and are compiled into
  the shipped build, with nothing at the site saying they are debug-only or why
  they exist. Compared the constants' purpose with what the file tells a reader.
  Repair target: name them debug-only at the site, with the reason and what
  removes them.
- **[REQUIRED REPAIR] Probe ships with the fix it was written for.** The change
  contains both the permanent repair and the one-line probe that proved the
  theory, unlabelled; left there, the probe becomes load-bearing for the next
  reader. Compared the change's own description of the fix with the lines that
  remain. Repair target: remove the probe, or label it and name what removes it.
- **[OBSERVATION] Two completion patterns kept and explained.** One flow
  completes on the device and its sibling completes on the server; both sites
  carry a comment saying the divergence is deliberate, why unifying them now
  costs more than it returns, and that server-side unification is the intended
  end state. A labelled, decided divergence is what this check asks for.

## C-26 Prose claims more than the code establishes

Question: Does every claim in the prose around this change have a line of code
or a named test that makes it true?

Needs: the pull request body, README, examples, and changed comments; the diff;
the repository at base and at head; the tests the prose names.

Read: Pull out every sentence that makes a factual claim, especially those
carrying an absolute or a capability word — nothing, fully, proven, complete,
native, cold, byte-for-byte, always — and find the exact line that makes each one
true. A claim with no such line is the finding. Recompute any stated count,
ratio, or diff-stat from the artifact it summarizes instead of trusting it. Treat
"no user-visible change" as a claim to check against the diff, not a label to
accept. For a claim that something was already true before, or that one thing
caused another, fetch the cited file at base and at head and compare them rather
than trusting the stated diagnosis. When the prose names a test as proof, open
that test and see what it actually exercises. Comments and vendored documents are
claims too: a manifest comment about what a dependency does, a vendored contract
document telling clients how to behave, a file that says it owns every instance
of something. So are the surfaces the change leaves behind — a README command, an
example instantiating the replaced API, a generated artifact that was not
regenerated, a telemetry name implying the old behavior — because the next reader
or agent will copy them.

Block when: a claim's supporting line does not exist, a stated count contradicts
the artifact it summarizes, a "nothing user-visible changed" line sits over a
deliberate behavior change, or a live doc, comment, or example teaches a contract
the change just replaced. The repair is rewriting the prose to match the code,
never adding code to make the claim true.

Do not block when: the claim is stated at the level that was actually measured —
a mismatch between the claimed level and the measured one is V-05's; a document
is clearly marked historical; the stale surface is unrelated to the changed
behavior. Naming and formatting are never findings here, except a name or comment
that states a falsehood, which is a documentation defect rather than a
preference. Two declarations of one environment that disagree are C-27. Grade
honestly: this class is real and often an observation rather than a blocker.

Examples:

- **[REQUIRED REPAIR] Body promises a control the screen does not render.** The
  description says the error state keeps the same retry button and layout; the
  generic error state renders an empty-state widget with no action label and no
  handler. Compared each claim sentence with the widget the screen builds. Repair
  target: rewrite the description to describe what the screen does — not add a
  retry button so the claim comes true.
- **[REQUIRED REPAIR] README still teaches the replaced writer.** Draft writes
  now go through the canonical service, and the README example still imports the
  direct writer, so the next reader copies the path this change was meant to
  retire. Compared the README example with the code the change leaves reachable.
  Repair target: update the example to the canonical service, or delete it.
- **[OBSERVATION] Stated split of the change is off by one.** The body describes
  twenty-two behavior-preserving edits and one behavior change; fetching the
  cited file at base and at head shows twenty-one and two. Nothing in the code
  needs to change, but the body does.
