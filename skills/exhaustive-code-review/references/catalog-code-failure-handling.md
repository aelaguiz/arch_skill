# Catalog Slice: Failure Handling

Applies when the change touches an error path, a default for a missing value, a
user-facing state that exists because something went wrong, a status gate, or a
call into a vendor SDK. Needs the diff and the repository at head; C-12 also
needs the request. These six checks ask what the code does when something is
missing or fails. Report each defect once, under the check that found it.

## C-10 A catch or guard that reports nothing

Question: Can an error path this change touches fail with nothing reporting it?

Needs: the diff; the repository at head, for the boundary above the frame and
the severity the error reporting sink actually captures.

Read: For every added or changed catch, error-return branch and error callback,
decide what the frame does: re-throw, return an error a caller inspects, or
capture it. Then follow each new failure this change can produce, from where it
is raised to the reporting sink, through every handler it passes on the way.
Those handlers are usually unchanged lines outside the diff, and they are in
scope because the change now depends on them: an existing catch that returns
early, logs below the severity the sink captures, or discards the error swallows
the new failure just as a new catch would. A log line is not a report: compare the severity written with the
severity the sink reports, since a warning where warnings are breadcrumbs lowers
visibility. A frame that records its own message and returns normally leaves the
exit status or response code claiming success, and an error leaving as a type
the caller's dispatcher does not recognize is dropped, not retried. Check guards
that now skip work the path used to do, and compare the span of a try with the
operation it guards: a span over post-success work manufactures a failure after
the work succeeded.

Block when: an added or changed error path is reachable in production and
nothing at that frame or above it reports it — no re-throw, no inspected error
return, no capture — or a guard silently skips work the path previously did, or
a failure this change introduces travels through an existing handler that never
reports it.

Do not block when: the enclosing boundary demonstrably captures and this frame
re-throws or returns into it; the condition is one the product genuinely expects
and tolerates. A missing test for the error path is never the finding, and a
retry wrapper, a flag or a kill switch is never the repair. A frame that reports
a classification instead of the cause is C-13's finding; a failure turned into a
screen state is C-12's.

Examples:

- **[REQUIRED REPAIR] A failed run exits successfully.** A scheduled command
  caught its exception, wrote its own error record and returned zero. Compared
  the exit status with the outcome. Repair target: propagate the failure.
- **[REQUIRED REPAIR] The guard covers work that happens after success.** A
  submission handler's try spanned the delegate call, the confirmation and
  navigation, so a failure there offered a retry of an accepted submission.
  Repair target: guard the submission call only.

## C-11 A missing value defaulted into a valid one

Question: Can a consumer tell a measured value from no measurement here?

Needs: the diff; the field's specification, comment or catalog entry; the
repository at head, to follow the substituted value to its first consumer.

Read: Collect every place the change supplies a value when the real one is
absent: a null-coalesce, a coalesce inside a query, an unwrap-with-default, a
lookup with a default, a decode of an optional field into a plain numeric type,
a catch returning a healthy-looking empty result. For each, state what the
surrounding specification calls that state and set it against what the code
substitutes; a specification that says unknown against code that says false,
empty or zero is the finding. Then follow the value to the first join key,
equality test, denominator, gate, published status or rendered number, where an
absence becomes an asserted fact. Read the test named for the behavior: a
fixture supplying the same default on both sides never exercises the case.

Block when: a consumer cannot distinguish a measured value from no measurement,
and a join, denominator, gate, published status or rendered number consumes the
substituted value as observed.

Do not block when: the default is deliberate and benign and the absence is
captured by a warning at the same site; the contract genuinely permits the value
and the source's coverage supports an observed zero. This check covers code and
data pipelines; in a written report, "unknown" is the honest value and never a
finding. A comparison against a literal that silently drops missing rows is
C-24's when it gates a status and C-34's when the defect is in the query itself.

Examples:

- **[REQUIRED REPAIR] An absent environment normalized to the production
  value.** Ingestion substituted it for events carrying none, a derived fact
  joined on environment equality and published the pair as verified, and the
  test named for the case supplied the same value on both sides so could never
  fail. Repair target: keep the absence distinct and exclude it from the join.
- **[REQUIRED REPAIR] Corruption converted into healthy absence.** A local store
  logged the decode error, deleted the payload and returned an empty answer set.
  Compared that with what a user who answered nothing produces. Repair target:
  return the failure.

## C-12 A failure rendered as a user experience

Question: Does this change render a state that exists because something failed?

Needs: the diff; the issue text and acceptance criteria, so each rendered state
can be traced to a requirement line.

Read: Enumerate every new empty state, "unavailable" or "try again" string,
retry control, banner, toast, spinner, and enum member named for absence or
failure. Ask two things of each: which requirement line asked for it, and
whether anything reports the underlying condition when it appears. A branch that
renders something and reports nothing is the finding, because the failure then
looks like a supported product state and reaches nobody who could fix it. On a
refresh path, compare what the screen shows while the new value loads with what
it showed before; blanking a good value is the same defect. In a change
described as a fix, a new user-facing affordance is itself evidence the cause
was not found, so compare it with the cause the change names.

Block when: a user-visible state, string or control exists because something
failed or was missing, and no requirement line asked for it or nothing reports
the condition behind it.

Do not block when: the condition is one the product genuinely expects rather
than a failure; a requirement asked for that state; the code defaults benignly
and captures a warning with no user-visible surface. Never offer a loading
skeleton, a retry affordance, a flag or a staged rollout as the alternative —
proposing one is the defect this check exists to catch. A failure that is silent
rather than rendered is C-10's; a fix whose only behavioral edit sits downstream
of the failure is C-17's.

Examples:

- **[REQUIRED REPAIR] "Unavailable right now" shipped as an ordinary home-screen
  state.** An absent goal set renders as a normal state, nothing reports it, and
  no requirement asked for it. Compared each rendered state with the acceptance
  criteria and the captures on that path. Repair target: report the absence.
- **[REQUIRED REPAIR] A failing purchase path answered with a new button.** The
  fix added a continue control and an unavailable state instead of changing the
  path that failed. Repair target: repair the path, or report it as blocked.

## C-13 Diagnostic data trimmed, mapped, or redacted

Question: Does the report leaving this code carry what the provider returned?

Needs: the diff alone.

Read: Find every place the change stands between a provider's response and the
reporting sink: a handler that destructures a response and keeps a subset, an
error converted into a local enum, code or string before it is reported, a
wrapper that retains a classification instead of the cause it wrapped, a helper
that replaces a wrapped cause on its way to the sink, a failure mapped onto a
benign outcome such as cancelled, and any newly added function that masks,
scrubs or strips fields, or caps their length or count. Compare what the
provider returned with what survives into the capture call, including what the
wrapper's string form exposes: a type name plus a classification is not the
cause. One change can widen what is captured and add a new masking or
truncation step at the same time. Judge each added step on its own: a net gain
in captured data does not clear a new step that removes some of it.

Block when: provider error bodies, callback payloads, native error codes or
third-party responses are narrowed, re-typed, masked or truncated before they
reach the reporting sink, or a real failure is recorded as a benign outcome,
which files it as something nobody will investigate. Also block when the change
adds any helper or step that masks, redacts, hashes, or truncates values inside
diagnostic data and the request did not ask for it, whatever kind of value it
targets: identifiers, addresses, tokens, keys, or long strings. What such a step
calls sensitive is not a reason to keep it; the repair is to remove it.

Do not block when: the change restructures a handler in order to capture more,
which is this finding inverted — although a control-flow change made only to
capture more is worth an observation, since instrumentation should not take
product risk. That clears the restructuring only. It never clears a masking or
truncation step added in the same change. Missing redaction of personal data is never a finding in this
catalog, and removing an unrequested redaction helper is the repair, not the
defect. No check in this catalog asks for anything in a log or an error report
to be masked. A path that reports nothing at all is C-10's.

Examples:

- **[REQUIRED REPAIR] A payments callback keeps the status and discards the
  body.** The handler kept the status code and reported that alone, so the
  fields that would explain the failure were gone before the capture call.
  Repair target: report the payload whole.
- **[REQUIRED REPAIR] Unrequested masking shipped inside an instrumentation
  change.** It masked user names and profile fields no requirement asked for,
  and added the helper that performs it. Repair target: remove both.

## C-24 A fail-open status gate

Question: Does an unrecognized, blank or missing value take the good path here?

Needs: the diff; the repository at head, to enumerate the values the producer
can actually emit, including members added after the gate was written.

Read: For each status or enum gate the change adds or touches, decide whether it
is an allowlist of the values that are good or a denylist of the values
currently known to be bad; the denylist is the finding, because the producer
will eventually emit a value the gate has never seen. Enumerate the producer's
real value set — blank strings, missing rows, values from a second writer,
misspellings, members added since — and place each on a side of the gate. In a
query, a comparison against a literal with no null handling evaluates to neither
true nor false when the column is missing, so the branch falls through instead
of firing; read what the fall-through does. In exception handling the same shape
is a catch-all treating everything outside one recognized value as terminal,
turning a recoverable refusal into a permanent failure; compare the branches
with the causes the platform documents.

Block when: a gate deciding publication, an alarm, retry safety or user
eligibility lets an unrecognized, blank or missing value take the good path, or
maps a recoverable condition to a terminal one.

Do not block when: the gate's job is to block users — enforcement machinery
should fail open and report rather than crash or lock people out, the one
standing exception to failing loudly; the producer's value set is closed and
enforced where it is written. Defects in how the query itself is constructed
belong to C-34; this check owns only what the gate admits.

Examples:

- **[REQUIRED REPAIR] Freshness degraded only for two named bad verdicts.** A
  pipeline degraded a feed on two known-bad values, so pending, unknown, blank
  and later-added verdicts published as healthy. Compared the recognized values
  with everything the producing job can write. Repair target: require a verdict.
- **[REQUIRED REPAIR] Every activation error but one treated as permanent.** An
  audio-session helper mapped all activation exceptions except one enum value to
  terminal failure, although the platform keeps a temporary refusal recoverable.
  Repair target: match on the stage, error domain and numeric code.

## C-31 An unwrapped platform SDK call

Question: Can a changed call into a vendor SDK throw past its error boundary?

Needs: the diff; the repository at head, for the boundary wrapper already in use
and the initialization sequence. Scoped to a mobile application repository.

Read: List every changed call into a vendor SDK — purchases and subscriptions,
identity and sign-in, messaging, attribution, secure storage, deep links, the
local database — and compare each with the wrapper the repository already
applies to that class of call. Three adjacent shapes belong here. A call that
assumes an initialization order the SDK does not guarantee: read what
establishes the order, including what a second initialization does. A state read
or write after an await with no check that the owner is still alive: compare the
lifetime of the object written with that of the operation. A throw inside a
router builder or a build method, which runs outside every handler that reports.
Treat global mutable vendor state as global: a two-step "configure, then act"
sequence does not snapshot the configuration, and a retained native task can
re-read the shared field long after the call returned.

Block when: a changed call into a vendor SDK can throw across the language
boundary with no wrapper, a throw is introduced inside a builder or a build
method, an SDK call depends on an initialization order nothing establishes, or
per-operation correctness depends on global mutable SDK state.

Do not block when: the repository is not the mobile application; the canonical
boundary already owns the failure mode and the changed code routes through it.
The repair is the existing error boundary or a value captured for the one
operation — never a retry wrapper, a flag or a staged rollout.

Examples:

- **[REQUIRED REPAIR] A throw inside the router builder escapes every
  boundary.** Route construction runs outside any handler that reports, so the
  failure ended the session with nothing captured. Repair target: move the
  failure into the owner that can report it.
- **[REQUIRED REPAIR] A configured identity re-read when the native task
  retried.** A sequence set the identity on an attribution SDK and then sent an
  event; the retained task re-read the shared field on retry, so a delayed event
  arrived under a later identity. Repair target: pass it with the event.
