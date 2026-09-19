# Catalog Slice: Test And Verification Proof

Applies when the change contains tests, fixtures, verification code, or a run
offered as proof. Needs the diff including tests, the repository at head, the
defect or requirement the proof cites, and the run record when a run is evidence.

Seven checks, seven baselines: V-04 sets a test against a production line broken
again, V-06 against the collaborators it replaced, V-07 against the expected
value's provenance, V-08 against the accepted value set, V-09 against a positive
control, V-18 against the new requirement, V-19 against what a verifier compares.
One assertion can trip several, so report each defect once, under the check whose
comparison found it. Never report a missing test here, and a test file added on a
refactor, deletion, or fix is C-36's subject.

## V-04 A test that cannot fail on the defect

Question: If the lines this test guards broke again, would the test go red?

Needs: the diff with both the test and the production change; the repository at
head; the defect the test names; the pre-fix commit if a failing run is shown.

Read: Name the exact production lines the test protects, then enumerate
concrete ways they could be wrong (the added line deleted, an error swallowed,
an early return on a duplicate, a branch dropped, a second call skipped) and
carry each through to the final assertion. Assertions on an empty collection, a
zero count, an absence, or a hardcoded inventory deserve most attention: those
are the values a broken path produces. A test asserting a helper was called, or
a snapshot blessing a contract with no semantic assertion, fails the same way.

Block when: a test is offered as the proof for a named defect and at least one
concrete production mistake leaves it green.

Do not block when: no test was required, or an existing higher-level test
discriminates. A run that goes red at the pre-fix commit is the strongest form
of this evidence, never the bar. A test that fails on the defect but accepts a
family of wrong values is V-08's; one that never runs the path is V-06's.

Examples:

- **[REQUIRED REPAIR] Test asserts the value the failure path also returns.**
  The read returns an empty map when it catches a non-identity failure, and the
  test asserts emptiness. Compared the assertion with the error path's return.
  Repair target: assert the call count and the terminal status.
- **[REQUIRED REPAIR] A fixture named for the missing field supplies it.** An
  event with no environment field normalizes to production, but the fixture sets
  the field. Compared the fixture with the defect. Repair target: drop the field.

## V-06 The test replaces the boundary the change touched

Question: Does this test still run the code the change edited, or a stand-in?

Needs: the diff; the test files; the repository at head, for selectors and
constants; the vendor's documentation when a vendor SDK is substituted.

Read: List every collaborator the test substitutes: doubles, fakes, recording
callbacks, injected clients, a harness standing in for the real host. A double
on the seam the change moved disqualifies the test. Compare literal selectors
with what the product exports now, since an identifier with no live reference
outside tests means the test hunts for what the app no longer renders, and a
vendor callback name with the one the platform delivers. A fake recomputing the
production predicate, or a stand-in left registered after its test, fails too.

Block when: the doubled boundary appears in the diff; a control recomputes the
expected answer instead of invoking the production predicate; selectors have no
live reference outside tests; or the platform never drives that callback.

Do not block when: the substituted boundary is genuinely external and untouched
by the diff and the real reducer, classifier, or client is still called. The bar
is not "no doubles" and this is no demand for end-to-end tests: the cheapest
layer reaching the changed seam is the standard. Provenance is V-07's.

Examples:

- **[REQUIRED REPAIR] Device test drives a control the change replaced.** The
  automation taps the old sheet's button while the change shipped a different
  dialog, and a broad catch retries past "control not found". Compared the driven
  control with the shipped one. Repair target: drive the new dialog.
- **[REQUIRED REPAIR] Negative controls restate the query they test.** Two
  controls copy the expansion, the join, and the mismatch predicate instead of
  invoking the real reconciliation. Repair target: run the real query.

## V-07 The oracle comes from the thing under test

Question: Did the expected value come from anywhere but the code under test?

Needs: the test file; the production function or query under test; the
provenance of both sides; the source for any expected constant.

Read: Follow each expected value back to its producer. If it was read from the
double the assertion checks, computed by calling the function under test, or
selected from the table the actual value comes from, the oracle is not
independent: two transformations from one producer are never two confirmations.
Check arrange and act too, since a test that performs the write it then observes
has proved only that it ran, and watch for a verifier regenerating the manifest
it checks, or a no-regression result that rests on matching the old output.

Block when: expected and actual share a producer; the test performs the
operation it then observes; a verifier regenerates the manifest it compares
against; or a no-regression claim rests on matching the old output.

Do not block when: the expected value is a hand-checked constant with a cited
source, or the comparison is declared a restatement or shape check and claims
nothing more. Which collaborator was invoked is V-06's; a verifier that checks
existence only is V-19's.

Examples:

- **[REQUIRED REPAIR] Expected title comes from the constant under test.** The
  test derives its expected title from the constant the assertion validates, so
  a wrong constant confirms itself. Repair target: capture the real title.
- **[REQUIRED REPAIR] Integrity check regenerates what it authenticates.**
  Replacing a helper file and regenerating that directory's checksum passes,
  since nothing authenticates the input. Repair target: pin the manifest hash.

## V-08 An assertion a family of wrong values satisfies

Question: Does the value the defect produces satisfy this assertion?

Needs: the test; the requirement or defect it names; the real range of values
the production path can emit.

Read: For each assertion, state the set of values that satisfy it, then ask
whether the bug's output is in that set. Non-null checks, length and count
checks, membership checks, numeric bounds, counter increments, and outputs that
only have to be non-empty all accept a set far wider than the contract. Where
the requirement is preservation, the assertion must compare against a value
captured before the operation; a shape check on both sides establishes nothing.

Block when: the known-wrong value the defect produces is inside the accepted
set of an assertion offered as proof of the fix.

Do not block when: the contract genuinely is a bound or a presence check; do not
demand exact values where the specification states a range. This class is the
easiest to over-report and the cheapest to repair. If breaking the production
line would also leave the test green, V-04 owns it; widening is C-18's.

Examples:

- **[REQUIRED REPAIR] Preservation tested by non-null on both sides.** A
  completion timestamp is checked non-null before and after the operation, which
  any value the bug writes satisfies. Repair target: capture and compare it.
- **[REQUIRED REPAIR] Restore check confirms identifiers, not specifications.**
  The test asserts chart identifiers are present after restore, never comparing
  axes and series with the originals. Repair target: compare each specification.
- **[OBSERVATION] Discriminating fixture.** The fixture value is a non-numeric
  error code a broken round trip cannot produce, so the assertion excludes it.

## V-09 An absence proved with no positive control

Question: Does anything show this harness detects the thing it reports zero of?

Needs: the harness or test; the run record with its window and timestamps; the
period of the suppressed behavior; the setup for any store the test reads.

Read: When a run reporting zero occurrences is the evidence that a fix worked,
look for the sibling run that produced an occurrence with the suppression off;
without it, zero is equally consistent with a harness that never observes.
Compare the observation window with the behavior's period, since a few hundred
milliseconds cannot rule out something recurring every few seconds. Check that
the declared cutoff is the gate's real comparison, that an "observed through"
timestamp comes from the captured data, and that setup clears each store read.

Block when: an absence result is the load-bearing evidence and no positive
control exists; the observation window is shorter than the trigger's period; or
the completeness timestamp is wall clock read afterwards.

Do not block when: a positive control exists elsewhere and the report names it,
or the absence is not the load-bearing claim. This class is rare and each
instance consequential, since a false absence closes an incident. A verifier
reporting success is V-19's; a deletion whose old path is reachable is C-01's.

Examples:

- **[REQUIRED REPAIR] Zero captures from a harness never shown to capture.** The
  run reports no captures with the fix on, and no companion run with the feature
  enabled produced one. Repair target: capture once with the feature on, then
  repeat the run.
- **[REQUIRED REPAIR] Leftover state can satisfy the assertions.** The pending
  store reads device preferences, not the test database, and the listener starts
  before the pending code is cleared. Repair target: read and clear that store.

## V-18 A retained test requiring the removed behavior

Question: Does a retained test or document still demand the removed behavior?

Needs: the new requirement text, whether issue, plan, or acceptance criteria;
the retained tests at head; any migration, handoff, or acceptance document.

Read: Compare each retained expectation against the new requirement text, never
against the current code, because code and test agree by construction and the
code cannot be the reference. Two questions decide it. Does the expectation
restate the rule the change just removed, so a correct implementation turns it
red? And for a case the test says must succeed, can the stated inputs still
satisfy the new budget, count, or constraint: work the arithmetic. Run the same
comparison over migration inventories, handoff notes, acceptance prose, and
comments explaining a retired invariant; that half does the most damage, since a
faithful reader reinstates the defect.

Block when: a surviving assertion encodes the behavior the change removes, so a
correct fix would turn it red; or a handoff, migration, or acceptance document
tells the next implementer to keep the removed behavior.

Do not block when: the old behavior is still required somewhere and the test
says where. A test whose bar was loosened inside this change is C-18's, and a
document stale about something this change did not remove is not this finding.

Examples:

- **[REQUIRED REPAIR] Retry test asserts the shortened wait.** It expects a
  server-mandated delay of an hour to become thirty seconds, the defect: a client
  cap overriding the provider's interval. Repair target: expect the full delay.
- **[REQUIRED REPAIR] Migration inventory teaches the removed cutoff.** It tells
  the next implementer to keep an eligibility cutoff the accepted requirements
  delete, reinstating the under-crediting. Repair target: correct the inventory.

## V-19 Verification code that checks existence only

Question: Would this verifier report success on a non-empty but wrong input?

Needs: the diff containing the verification function; the writer, publisher, or
command it pairs with; the values it claims to check.

Read: Take each function or step named for verification, whether a verifier, a
readback, a preflight, an acceptance check, a lint wrapper, or a report runner,
and construct a non-empty wrong input that still passes. It must dereference and
compare the specific field values it claims to verify; a key, a tab name, a row
count, a "formula is present" boolean, or a non-null test is not a verification.
Compare the bytes the writer sends with the value the verifier compares against,
flag any transform applied in between, and check that the step executes what it
claims rather than printing it, on content rather than an absence of errors.

Block when: a function named for verification reports success on presence
alone; it compares a different representation than the one actually published;
or it reports success without executing the thing it claims to verify.

Do not block when: existence genuinely is the contract being checked and nothing
more is claimed of it. A test assertion that accepts too wide a value set is
V-08's; a run whose zero result lacks a positive control is V-09's.

Examples:

- **[REQUIRED REPAIR] Readback checks tab names, not values.** The verifier
  confirms the prepared tabs exist and scans for formula-error strings, so a rate
  of ninety-nine percent from one over two returns no errors and a wrong number
  ships marked verified. Repair target: compare cells with the expected values.
- **[REQUIRED REPAIR] Lint step prints its verdict unconditionally.** The
  analyzer's output is piped through a counting pipeline and a conditional, after
  which the step reports a good dependency graph and exits zero whether or not
  the analyzer ran. Repair target: fail on the analyzer's own status.
