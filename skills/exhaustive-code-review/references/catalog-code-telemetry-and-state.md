# Catalog Slice: Telemetry And State

Applies when the change introduces or changes a user-visible flow, or touches
analytics events, a persisted or published status field, the shape of state a
caller has to interpret, a clock read, or a schema, wire or dependency contract.
Apply C-14 to new flows even when the diff contains no telemetry changes;
missing instrumentation is something to investigate, not a reason to skip it.
Needs the diff and the repository at head; C-14 and C-33 also need the relevant
contract context — the event definitions
and their intended uses or readers, or the client, second repository or lockfile
still holding the old shape. These five checks ask what the system records and
how it represents it. Report each defect once, under the check that found it.

## C-14 Telemetry value, volume, and decision continuity

Question: Did this change lose useful visibility, or ship a flow whose necessary
exposure, outcome, or failure cannot be measured? Does each added signal justify
its cost?

Needs: the diff; event definitions, emit sites, enrichment and destinations;
affected queries, metrics and alerts; the product or engineering question the
change serves. A concrete planned use can justify a new signal before its
dashboard exists.

Read: Explicitly inspect both removed events and newly introduced user-visible
flows. Compare emit paths before and after the change for deleted calls, new
guards, and lost outcome or failure branches, even when the event's name and
definition survive. For each new flow, identify its necessary exposure, outcome
and failure visibility and the records that provide it, even if no telemetry
code changed. Absence of a telemetry diff does not establish adequate visibility.

Telemetry earns its collection and storage cost by answering a named,
actionable question. Valuable signals measure whether an experience is reached,
started or finished, where people drop or convert, an experiment's exposure and
outcome, or a reliability/performance condition an engineer can act on. Preserve
the denominators, identity and diagnostic detail those uses need. A rare failure
can matter more than a frequent action; volume alone says nothing about value.

First check whether a shared event, screen view, durable server row or error
report already answers the question at the needed population, timing and grain.
If it does, require no new event. A record of every tap, panel, network request
or repeated callback is extraneous when it adds no distinct answer. "Coverage"
and "might be useful someday" do not explain what someone would decide or do.
Dev-, QA- and staging-only surfaces do not need product analytics coverage.

For additions or broader emission, require an estimate of events per user or
session and in aggregate, plus expected property cardinality; state assumptions
where volume is not yet measured. Prefer the lowest-volume semantic action or
durable state transition. Repeated render, animation, polling or visibility
callbacks should not recount the same fact. Consider aggregation, sampling and
selective destination routing where they retain the needed answer. Check their
effect on rates, rare failures, latency tails, experiment populations and
conversion delivery; sampling only successes can silently change a denominator.

Trace changed signals from emit sites through enrichment and routing to their
readers. Compare timing, population, count and fields, not just event names:
moving an emit can change its meaning, and an unstarted identity binder can
leave an apparently healthy stream unjoinable. Require fields the actual
contract needs, not assumed vendor requirements or authenticated identity before
login. Before endorsing removal, establish the producer and what decisions or
diagnostics survive. A search that finds no consumer is incomplete evidence,
not proof of no value; report unavailable readers or unresolved purpose instead
of inventing a dependency or recommending blind deletion.

Block when: a new experience's necessary exposure, outcome or failure cannot be
measured by any record; an emit is wired to the wrong moment, population or
count; or a change breaks a metric, alert, experiment, conversion dependency or
required diagnostic. Name the question or operational action that becomes
unanswerable or misleading, and the broken contract. Missing optional detail is
not a blocker. Report redundant or
unjustified additions and missing volume/cardinality estimates as observations
(SHOULD-FIX), unless a concrete correctness or operational consequence warrants
a required repair. Existing untouched events are outside the PR's repair scope.

Do not block when: existing records answer the question, or a justified
consolidation, removal, aggregation, sampling or routing change preserves the
needed measurement and diagnostics. Do not demand shown, completed and error
events for every control, or a unit test for every event. New events and fields
receive the same value-and-cost scrutiny as existing ones touched by the diff.

Examples:

- **[OBSERVATION] Every request gains another success event.** Existing service
  metrics already provide the required error rate and latency distribution;
  the new event duplicates that answer at request volume. Repair target: use
  the existing metrics, or explain the distinct question and the least costly
  signal that answers it.
- **[REQUIRED REPAIR] Sampling destroys an experiment's conversion rate.** The
  change samples exposures but leaves outcomes and the reader's denominator
  unchanged. Repair target: preserve a valid population and measurement method.
- **[REQUIRED REPAIR] Failure diagnosis loses its join.** An identity binder is
  never started, so error events cannot be joined to the affected operation.
  Repair target: restore the correlation required for diagnosis.
- **[NO FINDING] Extra panel events are absent.** An existing screen view and
  durable completion record already answer reach and completion for the new
  experience. Another event for each panel would add no decision-relevant fact.

## C-25 Derived status recorded as observed fact

Question: Does each status field's name match the event that sets it?

Needs: the diff for the name-against-assignment comparison; the repository at
head when the terminal event lives in another file; any prose or vendor field
the value feeds.

Read: For each boolean, enum or summary field the change writes or publishes,
restate the right-hand side of its assignment as one plain sentence and set it
against what the name asserts. The finding is a field set from a request rather
than a response, from an acceptance rather than a completion, from a dispatch
rather than an observation, or from the caller's own deadline rather than the
operation's outcome: the parser accepted the row, so it is marked published; the
button returned, so the alert is marked dismissed. Trace the status back to the
event it is assigned from, ask whether that event is the terminal fact the name
claims, then read the consumer to see whether it treats the field as terminal.
Follow the value into generated prose and vendor fields too: a predicted number
written into a field the vendor documents as actual revenue becomes a claim
about actual revenue. Build the counterexample by hand — take a case where the
earlier hop succeeds and the later one fails, and trace which branch fires.

Block when: a persisted or published field, or a sentence generated from it,
asserts a hop the code never observed, and a consumer treats it as the terminal
fact.

Do not block when: the name states the earlier hop honestly — submitted,
accepted, attempt started. Renaming to the honest hop is a valid repair and is
often the whole fix, so report this as an observation when no consumer treats
the field as terminal. It is a real defect class, not a nit, but rarely blocks a
merge on its own. A name claiming a migration that did not happen is C-01's.

Examples:

- **[REQUIRED REPAIR] A navigation transaction completed against the requested
  destination.** The transaction finished on the destination computed inside the
  resolver, not an observed final location, so issuing the navigation counted as
  arriving. Repair target: complete it on the observed destination.
- **[REQUIRED REPAIR] A reconciliation status that means only that rows exist.**
  The published status asserted spend reconciled to cash truth while the code
  established only that ad rows were present, so a campaign with a fraction of
  its spend published as evidence-backed. Repair target: compare the totals.
- **[OBSERVATION] An event named for a click that fires on presentation.** The
  name asserts a user action the code never observed; nothing downstream treats
  it as terminal today. Compared the emit site with the name. Repair target:
  rename it to the hop the code observes.

## C-29 One field carrying two meanings

Question: Does any field this change touches take part in two decisions?

Needs: the diff; the repository at head when checking whether an extended
message or protocol already has another owner.

Read: For each field, name the one thing it decides. The finding is a field that
is both identity and content, both a key and a payload, or both a presence
signal and a value; a state a caller can only reconstruct by combining booleans,
nullability checks, caches and provider values; a sentinel such as minus one,
zero or an empty string standing in for a state with no name; and an existing
message or protocol, built for one feature, extended to carry another feature's
payload, so the message means different things depending on who produced it.
Read the consumers: if two of them read the same field to answer different
questions, the field has two owners. Where one level's sequencing value rides in
another level's field, check whether a sort or a key lets one owner's private
ordering decide another owner's fact. Read the type definitions too — a bare
number standing for a domain quantity carries the quantity and its unit in one
place.

Block when: a changed field decides two things, a sentinel encodes a state, or a
caller must combine several values to reconstruct one state that should have a
named owner.

Do not block when: the two meanings are genuinely one meaning; a type, parser,
schema or runtime guard makes the impossible combination unrepresentable; the
state is private to one file and every reader is visible and safe. Naming and
type-preference arguments are never the finding. When the honest answer is that
the overloaded value should not exist, say so — hardening it institutionalizes
the complexity. This check owns one field or one state carrying two meanings;
an interface whose shape makes a caller remember an ordering, a pairing, a call
order, or which combination is legal is C-39. Where one field is both, report
the two meanings here and the contract there.

Examples:

- **[REQUIRED REPAIR] A crash on an overloaded run identifier, hardened instead
  of removed.** The identifier carried both a run's identity and a validity
  signal, and the proposed repair made it more robust; the consumer did not need
  it at all. Repair target: delete it from the path that does not need it.
- **[REQUIRED REPAIR] Two levels of ordering in one value.** A parent's ordinal
  and a child's ordinal shared a field, so one level's sequencing could order
  the other level's facts. Repair target: two named values, one per level.
- **[OBSERVATION] One field, one meaning, two readers.** A completion timestamp
  is read by a screen that displays it and by a job that orders work by it, and
  both ask it the same question. Two readers are not two owners.

## C-32 Device clock used to derive product state

Question: Is a clock read here stamping an event, or deciding something?

Needs: the diff; the plan or issue when the acceptance criteria are themselves
time-dependent.

Read: Split every clock read and local-timezone conversion into two buckets —
writing a time onto a record, and deciding an outcome — and look only at the
second. Deciding reads are day-boundary computation on the client, expiry
evaluated locally, eligibility or a reset keyed to the local date, and any
comparison between a locally sampled time and one from the server: two samples
of "today" can disagree, and the local one then silently vetoes correct dated
state. Timestamps written by different processes are not an ordering proof
either; tens of milliseconds of skew can exclude a real event. In tests, the
same read catches fixed sleeps standing in for waiting on the condition under
test, and fixtures dated relative to the current date, so the suite's result
depends on the day it runs. When a plan describes behavior that resets at
midnight, or an acceptance criterion whose outcome depends on when it is run,
ask the same question of it.

Block when: product state such as eligibility, expiry, a day key, a reset or a
gate is derived from the device clock or the local timezone instead of being
delivered by the server, or a proof depends on wall-clock timing rather than on
the condition it claims to test.

Do not block when: the value is a timestamp being written onto a record. Tie the
finding to a reachable decision; a clock read is not a finding by itself. The
shape to ask for is a server-delivered, day-keyed set of successor states so the
client does no date math, never a wider tolerance or a retry.

Examples:

- **[REQUIRED REPAIR] A locally recomputed day vetoes the server's dated
  response.** A controller published the response only when its own computation
  of today matched the day on the response, so two local computations could
  disagree and one discarded correct state. Repair target: accept the server's
  dated state and delete the local recomputation.
- **[REQUIRED REPAIR] Cross-process timestamps used as an ordering proof.** A
  consumer excluded a genuine event because its creation time, written by
  another process, sat tens of milliseconds past the cutoff. Compared the two
  clocks the comparison assumes are one. Repair target: order by one writer.
- **[REQUIRED REPAIR] Fixtures dated relative to today.** A suite compared rows
  against the current date and waited a fixed interval instead of on the element
  it needed, so its result depended on the day and the machine. Repair target:
  pin an as-of date and wait on the condition.

## C-33 A schema or wire change with no compatibility answer

Question: What does a reader or writer on the old contract do after this lands?

Needs: the diff; the repository at head; the other side's consumer when the
contract crosses a boundary — a second repository, a released client, a
lockfile, a deploy manifest; the change description, for a claim that both sides
ship together.

Read: For every changed value, name who else reads or writes it: the installed
client, the validator in another repository, the binary a rollback would
restore, the mapper compiled against the old shape, the compatibility window the
wire schema promises. Open the other side's consumer rather than assuming a
top-level change propagates. The findings are a schema change with no migration,
a removed or renumbered field, a new required field with no default for old
readers, and a constraint change a previous release's writes no longer meet —
read the old writer's conflict target against the new key. On a
dependency change, walk the transitive floors yourself: two manifests pinning
different native versions cannot describe one resolved graph. When one side of a
contract moves, read the sibling paths that still speak the old shape: commands,
scheduled jobs, fallback readers and generated artifacts. For new persisted user
data, the answer is a migration, a backfill, a defined default for records with
none, telemetry on that default, and old clients that keep working.

Block when: a changed contract can be read or written by something that still
holds the old shape, and nothing in the change answers for it.

Do not block when: both sides ship in the same build and the change says so; the
data is genuinely a device-local preference rather than user data; both shapes
normalize immediately through one adapter. The persistence expectations above
are a strong preference for user data in an account record, not a rule for
caches or device settings.

Examples:

- **[REQUIRED REPAIR] A wire schema drops fields a released client parses.** An
  enum value and several message fields were deleted, and the mapper in the last
  released build throws on the new payload. Repair target: restore them and test
  against the old wire shape.
- **[REQUIRED REPAIR] A new composite key breaks the rollback binary's writes.**
  A migration changed a settlement table's primary key to a pair of columns
  while the release plan still promised rollback to the previous image, whose
  conflict target names one. Repair target: keep the old unique constraint.
- **[REQUIRED REPAIR] A producer shipped a version its consumer never learned.**
  A backend published a new pricing version while a checkout validator in
  another repository still required a different release flag. Repair target:
  update the consumer's gate in the same change, or hold the producer.
- **[REQUIRED REPAIR] One entrypoint moved to the shared config owner.** The
  command-line path loads settings through the config service while the
  scheduled job still reads environment variables. Repair target: route the job
  through the same loader.
