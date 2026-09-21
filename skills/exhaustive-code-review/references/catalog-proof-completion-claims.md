# Catalog Slice: Completion Claims

Applies when the target carries a completion claim, a PR body, a status report,
or a worker's summary. Needs the claim text, the artifacts it cites, the ask,
and the repository at head. Report each defect once, under the check that found
it.

## V-01 A completion claim with nothing outside itself

Question: Does this completion rest on an artifact outside the claim whose
content was read back?

Needs: the claim; the artifacts it cites; the repository at head; where
available, the elapsed time and the files the work opened.

Read: Name what the claim offers as support and ask whether it exists outside
the claim. A receipt file, a marker, a path, a file count, a renamed symbol, a
gate returning "ready", and a worker's summary all restate the claim: they show
a process finished, not that the work is right. Open what the claim cites and
read its content; when the deliverable is a set, compare its items against each
other, since near-duplicates are visible no other way. Then set the claimed
depth against the elapsed time and files opened; scanning a document for terms
cannot see an item implemented in name only.

Block when: a completion or merge-ready claim rests only on a receipt, marker,
path, count, renamed symbol, gate, or worker's summary with no content read
back; or the claimed depth is impossible for the elapsed time and files opened.

Do not block when: the claim is interim status; the artifact's content was read
back and cited; the user said they would test it themselves. Never ask for a
ledger of the verification, which is the opposite defect. An old path still
live in code is C-01 and C-02; a claim measured one hop upstream is V-05's.

Examples:

- **[REQUIRED REPAIR] A whole large plan reviewed in fourteen minutes.**
  Compared the claimed depth against elapsed time and files opened; that depth
  was unreachable. Repair target: reopen each item against its acceptance.
- **[REQUIRED REPAIR] Screenshots relayed upward, never opened.** The images
  did not render, and showed no state. Repair target: embed ones that display.

## V-05 Evidence that proves an earlier hop

Question: Does the cited evidence measure the thing the claim asserts, or
something upstream of it?

Needs: the claim text; the cited evidence; the code path between the measured
point and the claimed outcome.

Read: Write the claim and the measurement each as one sentence and check they
are the same predicate. Name the literal thing measured, such as a status code,
an exit code, an SDK return value or a badge colour, and follow the code from
there to the outcome the claim names. Every hop between is unproven, and hops
hide their own failures: a handler that catches its processing error and still
answers success, a command that logs an exception and returns normally. Where
the flow crosses systems, evidence is needed at each hop, not one result that
proves the first.

Block when: the measurement's predicate is earlier or lower than the claim it
supports: submitted against accepted, a success response against downstream
processed, an exit code against the logged outcome, one run against a rate.

Do not block when: the claim is already stated at the hop measured, or the
report labels the gap itself. This check reads the claim's wording; it never
demands benchmarks or a measurement campaign. A claim with no number at all is
V-17's; whether a test could fail on the defect is V-04's.

Examples:

- **[REQUIRED REPAIR] Delivery claimed from a success response.** The handler
  caught its processing exception and answered success. Compared the status
  code against the claimed delivery. Repair target: answer with the result.
- **[OBSERVATION] Two runs offered as a latency distribution.** They bound
  failure, not typical speed; restating the claim at the hop measured is the
  repair.

## V-11 A prescribed step or model not shown to have run

Question: Did the load-bearing step or model the ask named run, shown by
something that could only exist if it had?

Needs: the ask naming the step and model; the claim; transcripts or links; the
artifact whose character can be judged; the pinned skill or config.

Read: Find the step the ask made load bearing, such as a review by a named
model, and look for an artifact that could not exist unless it ran: a link, a
transcript, or the served model, profile and window read back out of the
session. Judge the artifact's character against the tool it is credited to:
prose, imagery and estimates carry the signature of what produced them. Read
the outside state that would contradict the claim, such as the tracking issue
or the model a skill, config, or schedule file is pinned to. A pin to a retired
model, or an agent holding a skill it never reloaded, is a live defect; an
instruction or skill file that teaches a retired path as live is C-44's.

Block when: a load-bearing prescribed step is claimed and nothing outside the
claim shows it ran; a required model was never read back off the session; or a
fallback to a lesser model was accepted as the answer.

Do not block when: the step is not load bearing; the claim is interim status;
the artifact carries its own link or transcript. Not a ledger of tool calls:
one step shown is the bar. A deliberate, named substitution, such as routing
past a refusing tool, is a decision; the silent swap is the defect.

Examples:

- **[REQUIRED REPAIR] A review credited to the top model was served by a
  fallback.** The prose gave it away first. Compared the served model against
  the model the ask named. Repair target: re-run the review on the named model.
- **[REQUIRED REPAIR] Agents pinned to a superseded model.** Compared the pin
  in agent definitions at head against the model in use. Repair target: update
  the pin.

## V-14 Merged treated as delivered

Question: Is the work this claim calls live actually running from a revision
that contains it?

Needs: the status claim; branch and merge state; the deployed revision and the
live surface; the repository at head.

Read: For work whose value exists only once deployed, such as a dashboard or a
data pipeline, compare the claim against the deployed revision and against the
live surface actually changing. Merging is not deploying: a failed deploy
leaves the merge intact and the surface stale. For integration, establish
ancestry: read whether the commit is an ancestor of the line that ships, rather
than trusting a merge label, a stale merge-ready label, or a conflicting
stacked branch. Check the baseline of any audit, since findings resolved
against a release build or old checkout re-raise defects already fixed at head.

Block when: work that only exists once deployed is called done at merge with no
deploy evidence; an audit's baseline is a stale build and its findings are
fixed at head; or integration is asserted from a label, not ancestry.

Do not block when: a tracking issue closes at merge, which is deliberate
bookkeeping and never excuses an unverified "it is live"; deploy access is
absent and the report states that limitation and stops; nothing user-visible
depends on deployment.

Examples:

- **[REQUIRED REPAIR] Merged data change called done; the dashboard never
  changed.** Compared the claim against the deployed revision; the publishing
  deploy had not run. Repair target: verify the deploy, then claim.
- **[OBSERVATION] Newly visible failures counted as new ones.** A version bump
  added instrumentation, so pre-existing failures entered the count as
  regressions.

## V-15 A claim sourced from a document or an agent

Question: Does each load-bearing fact come from a source that can be executed
or queried rather than from something someone wrote?

Needs: the claim and its citation; the source that would settle it: code at
head, history, telemetry, or a query; the primary source behind a backfill.

Read: For each load-bearing fact, find its citation and classify the source. A
plan document, a README, a prior analysis and a subagent's summary are writing
about the system; code at head, version history, telemetry and the database are
the system. Code defaults show what runs when nothing is set, not what is set,
and a feature existing in code does not establish that its flag is on. Where a
fact can be got from more than one place, take it from each and cross-check; a
number read off a backfilled record while the primary source exists is a
provenance defect.

Block when: a load-bearing fact's only source is a document, a prior report, or
a subagent's summary; a production-configuration conclusion is drawn from code
defaults; or a single-source claim stands where a second source was available.

Do not block when: the fact is the user's own recorded preference or decision;
the document is the deliverable. Provenance is the test, not confidence:
reasoning from a small sample is wanted, and this never becomes statistical
caution. Prose claiming more than the code establishes is C-26's.

Examples:

- **[REQUIRED REPAIR] Flag inventory built from code defaults.** Several
  hundred rows of flag state came from release-code defaults, not from
  production. Repair target: read the flags from the running configuration.
- **[REQUIRED REPAIR] Current state answered from a plan document.** Compared
  the citation, a plan and a README, against the code at head. Repair target:
  read the implementation.

## V-20 A requirement dropped between ask and delivery

Question: Does every requirement in the authorizing ask have an artifact in the
delivery, or an authorization to drop it?

Needs: the ask with its acceptance list; the delivery and its diff; linked
follow-up issues; the thread where scope could have been re-authorized.

Read: Take the requirements from the request itself. A plan, spec, or worklog
that ships with the change is part of the delivery, so it cannot narrow the
request; where it records an exclusion or a reduced list, that is the thing to
check, not the answer. Line the ask's requirements up against what shipped and
list those with no artifact. Where the request is universal (all of something,
every kind, any entity) and the delivery enumerates a fixed list of supported
cases, the enumeration is a narrowing: find who decided it. Follow each into the delivery by behavior, not wording: the ask is
paraphrased, so a requirement met under another name counts, and one echoed in
a heading with nothing behind it does not. Collect every requirement moved to a
follow-up, marked TODO, or narrowed, and find the message authorizing the move;
a deferral naming no issue has no owner, and a split across issues with no
ownership table leaves green checkpoints over work nobody owns. Read each
acceptance item for a pass condition an unavailable check could meet.

Block when: a requirement in the ask has no artifact and no message authorized
dropping or deferring it; the delivery supports a fixed subset of what the
request asked for across the board, and only the delivery's own documents say
so; a deferral names no owning issue; or an acceptance
item's pass condition accepts a documented blocker in place of evidence.

Do not block when: the user authorized the narrow landing plus a follow-up, and
splitting is fine when they say so; the missing item is a minor detail rather
than a user-facing feature or major technical decision; the repository is a
hobby project. The mirror column, an artifact with no requirement, is C-06's.

Examples:

- **[REQUIRED REPAIR] The original issue was abandoned when the work split.**
  Requirements the user believed were in flight had no owner. Compared the
  ask's list against the delivery. Repair target: give them an owner.
- **[REQUIRED REPAIR] An acceptance item satisfied by a note.** "Run the device
  lane, or document why it could not run" let an unavailable lane satisfy done
  for the defect the change claimed to fix. Repair target: require the run.

## V-21 A completion that discloses a defect

Question: Does the completion claim disclose an unresolved defect, a caveat, or
a moved bar in its own text?

Needs: the completion summary, PR body, or worklog; the thread where the trade
could have been authorized; the diff when the completion also moved a bar.

Read: Go through the completion's own text for a known-issues line, a caveat, a
"works except", or a partial result carried as whole, then compare it with the
thread. A completion that names a live defect in its own work is the finding
unless a user message accepted that trade: the trade belongs to the user, made
out loud. Watch for the same shape with the bar moving instead of the defect
being fixed: a threshold raised, a checker narrowed to the cases it handles, a
target re-scoped. Separate the meanings of done a status carries at once, such
as code written, a production step partly failed, and output never published.

Block when: a completion or merge-ready claim carries a known issue, caveat, or
unresolved defect in its own text and no user message accepted that trade.

Do not block when: the user made the trade in the thread, with the real fix
still expected; a failing check was authorized off to unblock a release; an
environment limitation stated with the work marked not complete is status, not
a completion. When the bar moved in the diff, that loosened check is C-18's.

Examples:

- **[REQUIRED REPAIR] A device-test report found a defect and still called the
  work complete.** Compared its own disclosure against the thread for an
  accepted trade. Repair target: fix the disclosed defect, then claim.
- **[REQUIRED REPAIR] Threshold moved in the change that claims the speed
  win.** The goal was to meet the existing bar faster. Repair target: meet the
  original threshold.
