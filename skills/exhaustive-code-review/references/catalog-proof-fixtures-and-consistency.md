# Catalog Slice: Fixtures And Consistency

Applies when the target has tests with fixtures or helpers, or an analysis or
completion claim that sits beside earlier conclusions on the same subject. Needs
the diff including tests and fixtures, the repository at head, the production
code that would really produce the fixture's data, and the earlier documents on
the subject.

Three checks, three baselines: V-24 sets a test's helpers against the outcome
they were supposed to identify, V-25 sets a fixture against what the real
producer could emit, V-23 sets a new conclusion against the canonical earlier
one. Report each defect once, under the check whose comparison found it. Never
report a missing test or a missing fixture here.

## V-24 A test that drains or retries its way to green

Question: Could this test reach its assertions by consuming or re-attempting
whatever it met, instead of by the expected thing happening?

Needs: the test and every helper it calls, transitively; the production journey
the test claims to prove; the repository at head, for what else can appear in
that path.

Read: Walk the test's path and list every loop, wait, or helper whose exit
condition is "nothing matched" rather than "the expected thing happened", and
every catch inside a re-attempt that continues. For each, ask what the later
assertions would read if an unrelated item had been consumed on the way: a
helper that dismisses, claims, advances, or flushes without asserting the
identity of what it acted on turns an unexpected state into a pass. Follow
helpers all the way down, since a setup or navigation helper reaches the same
generic clearing the direct path dropped. Then ask what counts as success after
a failed attempt, because a loop wide enough to reach an error-recovery path
proves recovery, not the journey. Last, look for a helper doing work the product
does itself, such as forcing a load the screen already performs; the test then
proves the helper.

Block when: a helper acts on whatever it finds without asserting its identity; a
re-attempt loop accepts a state reached only after a failure; or the test drives
work the product under test is supposed to do on its own.

Do not block when: the wait names the condition it waits for and fails when that
does not arrive; the helper asserts each item's identity before acting; setup
deliberately clears a named, expected precondition. The repair is to identify
what was consumed, and to put an unexpected item in the path so the test goes
red, never a longer wait or another attempt. A fixed sleep standing in for
waiting on the condition is C-32's; a test that could not fail on the defect at
all is V-04's; a doubled boundary is V-06's; re-attempt machinery added to
production code is C-30's.

Examples:

- **[REQUIRED REPAIR] A generic interstitial drain consumes whatever appears.**
  The helper dismisses, claims, or advances whichever gate is on screen without
  checking which one it is, so an unexpected reward is cleared and the paid
  journey still ends green. Compared the helper's exit condition with the
  identity the journey requires. Repair target: assert each gate's identity
  before acting, and place an unexpected one in the path so the test fails.
- **[REQUIRED REPAIR] Six attempts and a broad catch make recovery a pass.** A
  sign-in test retries the flow six times, catching and continuing between
  attempts, so reaching the error-recovery screen satisfies it. Compared what
  the loop accepts as success with the happy path it claims to prove. Repair
  target: fail on the first failed attempt.
- **[OBSERVATION] A wait that names its condition.** It polls for one named
  element and fails on timeout, so its exit is the expected thing appearing
  rather than nothing matching.

## V-25 A fixture the real producer could not emit

Question: Could the production path that feeds this code have produced exactly
this input?

Needs: the fixture, seed, or recorded payload; the code path under test with its
predicates, joins, and flags; the producer that emits the data in production; the
domain rules that say which states are reachable.

Read: Three comparisons, then a reachability question. Compare the fixture's
fields with every predicate the path evaluates, including joins and flags the
top-level object does not carry, since a seed can create the record a reader
wants while the row it joins on is never written. Compare each field's
provenance with the field production actually reads, not a same-named neighbour
from another source. Compare the values with the raw upstream shape: a fixture
already holding the value the transformation should compute leaves that
transformation untested, and a representation the writer never emits, such as a
native number where the wire format is a decimal string, hides the conversion
defect. Then ask whether the domain's own rules allow this combination at all,
and whether the ordering is the one the producer emits. For a regression
fixture, compare its shape with the payload captured in the incident: an empty
collection is not the same input as one a helper always populates.

Block when: the fixture's field combination, ordering, or provenance is one the
real producer cannot emit, or the domain's rules forbid, and the test rests on
it; or a seed skips a production setup step, so a row the path reads never
exists.

Do not block when: the omitted fields are ones the path never reads and every
predicate it evaluates is present; the combination is a state the domain
explicitly models and the test names it; the comparison is declared a shape
check and claims nothing more. Ask for a fixture the producer could emit,
generated through the production path where that is available, rather than one
more case added beside it. A fixture supplying the very condition whose absence
is the defect is V-04's; where an expected value came from is V-07's; a wrong
value satisfying the assertion is V-08's; a fixture dated against the current
date is C-32's.

Examples:

- **[REQUIRED REPAIR] Seed suppresses the signals that build the rest of the
  record.** It inserts an active, indexed listing while suppressing the creation
  and activation events, so the version row the indexer reads is never written
  and the index comes back empty; the same seed skips the default-feature setup
  that normal onboarding runs. Compared the rows the seed creates with the joins
  and flags the path reads. Repair target: create the record through the
  production path.
- **[REQUIRED REPAIR] Events supplied in an order the producer never emits.** A
  presentation test feeds the elimination before the level-change event, the
  opposite of the engine's emission order, so it gives false confidence about
  the exact sequence it claims to establish. Compared the fixture's order with
  the producer's. Repair target: drive the sequence from the producer.
- **[OBSERVATION] A trimmed fixture that still reaches the defect.** It omits
  fields the path never reads while carrying every predicate, join, and flag it
  evaluates: the smallest producible input, not an impossible one.

## V-23 A conclusion that contradicts the earlier one

Question: Does this conclusion disagree with what the canonical earlier document
on the same subject concluded, without saying which is true?

Needs: the new analysis, report, or verdict; the earlier documents on the same
subject, in the repository, the workbook, or the issue thread; the reasoning each
rests on; the outputs of any parallel effort on the same question.

Read: Take each load-bearing conclusion and find what was concluded before on
the same subject: an earlier analysis in the same directory, a previous tab, a
prior verdict in the issue, the read a colleague or another agent gave. Compare
the claims themselves, not their wording, since the two are usually phrased
differently: a different cause for one incident, a verdict reversed, a
recommendation now dropped, the same quantity restated at another value. The
defect is the silent switch, where the new document states its position as if it
were the only one on record. Look the other way too: a second analysis offered
as independent confirmation whose reasoning reads the first one's output is one
analysis twice, and a contradicting read dismissed without engaging its evidence
is the same failure from the other side.

Block when: a conclusion, cause, or verdict differs from the canonical earlier
one on the same subject and the new document neither names the contradiction nor
says which holds and why; a second analysis presented as independent rests on
the first one's output; or a contradicting read is overruled without addressing
what it was based on.

Do not block when: the reconciliation is written down, whichever side it
favours, including a plain statement that the earlier conclusion was wrong or
that the underlying state has changed since; the earlier document is marked
superseded; the two conclusions cover different populations, windows, or
definitions and the new one says so. Surfacing the conflict is what this check
wants, not winning it. A fact whose only source is a document is V-15's.

Examples:

- **[REQUIRED REPAIR] Two analyses, opposite causes, no acknowledgement.** The
  new report names a different cause for the same incident than the analysis
  filed beside it days earlier, and recommends against the action that one
  required. Compared the two stated causes and recommendations. Repair target:
  name the contradiction and say which holds and what changed.
- **[REQUIRED REPAIR] The second pass read the first pass's answer.** Two
  efforts were run by different routes so the results could converge; the second
  cites the first one's output in its reasoning, so it agrees rather than
  checks. Repair target: redo it from the source data alone.
- **[OBSERVATION] A reversal with its reason.** The new conclusion contradicts
  the earlier verdict and explains it: a behavior shipped between the two dates,
  so the earlier reading was right for its own time.
