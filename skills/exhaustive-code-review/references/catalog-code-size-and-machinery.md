# Catalog Slice: Size And Machinery

Applies when the change has a diff and the target carries the request that
commissioned it. Needs the diff and its stat, the originating request, the
repository at head, and the repository's own instruction file, which says
whether this is a product, a hobby project, or an experiment. C-40 also needs
the report, issue, or alarm the change answers, for how often the defect occurs.

All four checks weigh something the change added against a baseline, and they
differ in what they count. C-08 owns the ratio of the diff's durable surface to
the originating request. C-09 owns new control surfaces. C-36 owns added
verification machinery. C-40 owns the risk the change carries against how often
the defect it answers occurs and what one occurrence costs. Report each defect
once, under the check whose comparison found it. The output of every check here
is a cut list naming the smaller sufficient change, never a verdict on how much
work was done.

## C-08 Change size against the ask

Question: Is the durable machinery in this change a large multiple of what the
request describes?

Needs: the diff and its stat — files touched, new files, additions, deletions,
new subsystems; the originating request, as the issue body, plan, or instruction
states it; the diagnosed root cause, when the change is a fix.

Read: Compare the shape of the diff with the request. Shape matters more than
count, so name what the excess actually is: a registry, a schema, an adapter
layer, a service, a state machine, a second data path, a parallel dependency
environment. When the change is a fix, measure its surface against the number of
call sites the diagnosed cause really touches. When the change is framed as
simplification or unification, count the systems and owners before and after,
because the recurring failure is a unification landing as one more system beside
the ones it was meant to replace — the implementer preserves everything that
exists because it does not know things are allowed to go away. For each durable
new piece, ask whether an existing owner already covers that outcome. The
finding is an enumerated deletion list with the smaller thing that replaces it.

Block when: the diff's surface is a large multiple of what the request describes
and the excess is durable machinery no named symptom requires. Name the smaller
sufficient change and list the machinery to remove.

Do not block when: the diff is large but all of it is the asked-for thing, since
size alone is never the finding and formatting-only, generated, and lockfile
diffs are mechanical; the user authorized the increase, or the extra surface is
a necessary consequence the description discloses; the scope is payment,
pay-gate, or third-party telemetry work, where thorough failure-path handling is
expected rather than trimmed; the repository's instructions mark it a hobby
project or an experiment, where a minimal implementation is correct.
Proportionality is an argument about ceremony, effort, and risk, never a reason
to drop a requirement: a change that is complete except for a known defect is
not complete. Never propose splitting the change, adding a flag, or staging the
rollout as the remedy, and never report the absence of tests. Correct, green,
and independently reviewed is not a reason to stay quiet. A new control surface
is C-09; added test or receipt machinery is C-36; a new layer that duplicates an
existing owner is C-04.

Examples:

- **[REQUIRED REPAIR] A one-line reference fix arrived with a schema and a
  parser.** Persisting four known references landed as a six-file change
  carrying a custom inventory schema, a parser, a dependency environment, and
  parity tests. Compared the change's surface with the four references it had to
  persist. Repair target: persist the references; delete the schema and the
  parity apparatus.
- **[REQUIRED REPAIR] A cleanup grew a distributed lock for an empty backlog.**
  A historical-fee cleanup became a fourteen-file change including a
  non-expiring distributed-lock redesign that touches normal subscription and
  shipment paths, for a backlog that contains no rows. Compared the redesign's
  blast radius with the measured size of the problem. Repair target: delete the
  lock redesign and clean the rows.
- **[REQUIRED REPAIR] A paywall tap modelled as a five-phase state machine.**
  Opening a paywall, showing an error, ignoring a duplicate tap, and
  reinitializing on retry arrived as a dedicated state machine with five phases,
  seven events, and two effect classes. Compared the machinery with the four
  behaviors it produces. Repair target: delete it in favour of screen-local
  state.

## C-09 A new flag, mode, knob, or approval state

Question: Did the request ask for this control surface?

Needs: the diff; the issue or instruction that commissioned the work; the
repository's existing debug-flags file or equivalent, which tells a sanctioned
constant from a new configuration surface.

Read: List every control surface the diff introduces — feature flags,
environment variables, kill switches, enabled or mode parameters, optional
arguments with defaults, approval or draft states, retry and replay queues,
rollout gates — and check each against the text that commissioned the work. The
sharpest comparison: when the instruction asked for a default to change, did the
change move the default, or add a mode beside it and leave the old one
reachable? On a probe, an experiment, or a one-line fix, any of these is a
finding on its own. Read the repository's existing debug-flags file before
reporting, because a commented boolean added to the established file is the
sanctioned shape while a new configuration surface around the same idea is not.
Ask what the control defers: a decision nobody made, or a risk somebody named.

Block when: the diff adds a control surface — flag, mode, knob, environment
variable, approval or draft state, retry or replay path, rollout gate — that the
commissioning artifact never asked for.

Do not block when: the request names a risk to isolate and asks for the switch,
which is the one place a flag is the right answer: a feature behind a flag
defaulting off, so an adjacent product carries no risk; the request asked for the
toggle, including the developer-menu and testing toggles that are ordinary
equipment; the new control is a constant in the repository's existing debug-flags
file; the repository's instructions mark it a hobby project or an experiment.
Never propose a flag, a kill switch, or a staged rollout as mitigation for some
other finding. Where the control is also visible to users, C-06 owns the surface
and this check owns the control; whether an interface's shape forces callers to
combine flags into incompatible modes is C-39.

Examples:

- **[REQUIRED REPAIR] An internal job that mails nobody ships behind a flag.**
  The issue never mentions gating, and the job has no external effect to gate.
  Compared the control surface with the issue text. Repair target: delete the
  flag and run the job.
- **[REQUIRED REPAIR] An edit flow grew an approval state.** The requested
  behavior was that an edit goes live as a new version in the database; the
  result routes every edit through an approval step in a chat tool. Compared the
  approval state machine with the sentence that commissioned it. Repair target:
  write the new version directly.
- **[REQUIRED REPAIR] One place to turn features on and off became a
  configuration system.** The ask was a list of booleans in one commented file,
  flipped by hand; the result is a dependency graph with profiles and support
  for flipping flags while the application runs. Compared the delivered control
  surface with the described one. Repair target: the file of booleans.

## C-36 Test or receipt machinery added to a fix

Question: Did the request ask for the verification machinery this change adds?

Needs: the diff; the stated goal, from the issue, instruction, or description;
the existing test suite, to see whether a test already establishes the property;
the repository's own instruction file for its tier.

Read: Compare the verification surface the diff adds — test files, fixtures,
capture or attestation systems, receipt and evidence files, harnesses, runners,
gates — against the product change and the stated goal. A one-line fix, a
refactor, a deletion, or a debug affordance does not grow test infrastructure.
For each added gate, look for the existing test that already establishes the
same property: content-hash gates, digest gates, query-plan gates, and
source-text linters usually restate what a typed test already proves, and the
same verification duplicated at three layers is two layers too many. Then
compare the size of the verification surface with the size of the product change
it verifies. This check asks whether the proof was commissioned; whether
existing proof is trustworthy is a separate question, and when both fire on one
test file they are one finding, not two.

Block when: a change whose stated goal is a fix, a probe, a debug affordance, a
refactor, or a deletion adds test infrastructure, fixtures, capture systems,
receipt or evidence files, or a proof harness the request did not name; or the
verification surface is larger than the product change it verifies.

Do not block when: the code touches money, pay-gates, or third-party telemetry,
where thorough failure-path simulation under production-like conditions is
expected; the request named the tests, the fixtures, or the harness; the
deliverable is an inventory, an audit, a requirements list, a specification, or
a test plan, since a map of what exists must be complete and an incomplete one
is its own defect; the added thing is a real end-to-end run on the real surface,
which is evidence rather than machinery and is what a completion claim needs;
the diagnostics are live and the investigation is open, so only logging that
existed for the bug just closed should go; the repository's instructions mark it
a hobby project, an experiment, or local tooling. Never report a missing test
here. Whether the evidence behind a completion claim is sufficient belongs to
the proof checks V-01 and V-02; this check only weighs added machinery against
the size of the fix.

Examples:

- **[REQUIRED REPAIR] A throwaway debug flag came back with unit tests and
  fixtures.** The request was for a temporary affordance to look at and then
  delete. Compared the added test surface with the stated goal. Repair target:
  delete the tests and fixtures along with the flag.
- **[REQUIRED REPAIR] A stuck-session check became a solver and a receipt
  scheme.** The question was whether sessions still get stuck; the answer
  arrived as a solver plus receipt-based proof, and editing those receipts
  changed a build hash and broke live routing. Compared the machinery with the
  demonstration the question needed. Repair target: show that the stuck state no
  longer occurs.
- **[REQUIRED REPAIR] A new gate restates what a typed test already proves.** A
  checksum gate verifies a property an existing typed test establishes, and the
  same verification now runs at three layers. Compared the gate with the
  existing test. Repair target: delete the gate and the duplicate layers.
- **[OBSERVATION] Failure-path tests around a purchase path are wanted here.**
  The new tests simulate interrupted, refunded, and deferred purchases. This
  code takes money, so thorough failure-path proof is expected rather than
  trimmed.

## C-40 A repair riskier than the defect it answers

Question: Does this change put more at risk than the defect it repairs costs?

Needs: the diff; the report, issue, or alarm the change answers, for how often
the defect occurs and what one occurrence costs; the repository at head, to see
what the touched paths carry; the stated purpose of the change.

Read: Set two quantities against each other. On one side, how often the defect
actually happens and what one occurrence does — read the target for a count, an
alarm, a backlog size, an affected-user number, and note when it states none. On
the other, what this change can break, which lives in what it touches rather
than in its line count: an edit to control flow on a path every user crosses, a
new early return or await inside a working sequence, work that ran in the
background made blocking, a widened transaction or lock around live writes, a
rewritten persistence or migration path. A change whose stated purpose is
observational — telemetry, logging, metrics, analytics — is the recurring
offender, because measuring something is not a reason to change when it happens.
When the target never establishes frequency and the repair is built as though
the defect were systemic, that missing quantity is the finding. Leaving a rare
thing unmeasured or unfixed is an available answer; shipping product risk to
close it is not.

Block when: the change alters behavior, ordering, concurrency, or persisted
state on a live path in order to remove a defect whose frequency and cost the
target never establishes, or establishes as small. Name the risky hunks and the
smaller repair that leaves the working path alone.

Do not block when: the frequency and cost are stated and match what the change
touches; the defect is rare but one occurrence takes money, loses data, corrupts
state, or exposes a credential, since consequence sets the bar as much as
frequency does; the risky part is the asked-for work itself; the request
commissioned the repair at this size; the repository's instructions mark it a
hobby project or an experiment. Proportionality argues about ceremony, effort,
and risk, never about dropping a requirement — a change that is complete except
for a known defect is not complete. A diff far larger than the ask, with no
extra risk to live behavior, is C-08; a visible or control-flow change under a
scope that was not a product change is C-07; new locking is C-30.

Examples:

- **[REQUIRED REPAIR] A measurement change rewrote the path it measures.** A
  change commissioned to quantify a loop arrived with new early returns and a
  changed order of operations inside the loop's live path. Compared what the
  instrumentation had to observe with the hunks that alter when the work runs.
  Repair target: record the measurements without moving the control flow, and
  leave the part that cannot be measured that way unmeasured.
- **[REQUIRED REPAIR] A background step made blocking to close a rare race.**
  The repair turned an asynchronous write into a synchronous one on the path the
  user waits on, for a race the report shows twice in a month with no lasting
  effect. Compared the delay every user now pays with the measured frequency and
  cost of the race. Repair target: keep the write off the waiting path and make
  the race harmless through the operation's identity.
- **[OBSERVATION] Rare, but one occurrence takes money.** The repair reworks a
  purchase reconciliation path for a defect seen a handful of times, and each
  occurrence charges a user twice. Consequence, not frequency, justifies the
  blast radius here.
