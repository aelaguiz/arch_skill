# Catalog Slice: Fix Quality

Applies when the change fixes a reported defect. Needs the diff, the repository
at head, and the bug report, issue, or counterexample the fix cites.

These five checks look at the same fix from five different baselines. Report
each defect once, under the check whose comparison found it.

## C-15 The fix landed on the reported site only

Question: Does every other consumer of the thing this fix is about have the
same protection the patched site now has?

Needs: the diff; the repository at head; the bug report or counterexample; the
PR description, to see which siblings it says were checked.

Read: Name the value, attribute, helper, predicate, or literal the bug is really
about. Find every site that consumes it, not only the one in the diff: other
callers of the touched function, other dereferences of the same field,
structurally similar siblings in the same file family, duplicated SQL, and the
fix's own test helpers. Compare each site's guard with the patched one and
decide whether it inherits the fix or is exempt, and why. When verifying a
repeat fix, walk the original counterexample through the code again instead of
reading only the changed line.

Block when: a structurally identical sibling consumes the same value or helper
with the pre-fix behavior, and the change neither updates it nor states that it
was checked and why it is exempt.

Do not block when: the change names the siblings it checked and the reason each
is exempt; the request deliberately limited the fix to one site; the sibling is
unreachable. The repair this check asks for is an enumeration and a shared
guard, never a rewrite of neighbouring subsystems.

Examples:

- **[REQUIRED REPAIR] Three other constructors still build the unpinned
  container call.** The fix pinned the runtime compose call to the bound Docker
  endpoint, but an inspection script, a forwarding shell script, and an inline
  maintenance helper each construct their own ambient `docker` invocation.
  Compared every constructor of a container invocation with the pinned one.
  Repair target: route all of them through the bound endpoint.
- **[REQUIRED REPAIR] Third caller discards the strict-fulfillment result.** Two
  call sites gate the place-order signal on the helper's boolean; the third
  ignores it and emits the non-idempotent signal whenever the plan is complete.
  Compared each call site's use of the return value. Repair target: gate the
  third site the same way.
- **[REQUIRED REPAIR] The fix's own test helper repeats the repaired
  assumption.** Production budget accounting no longer truncates by prefix, but
  the new test helper still does, so the test passes on the old bug. Compared
  the helper's computation with the production path. Repair target: make the
  helper exercise the production rule instead of restating it.

## C-16 Asymmetric fix: one branch of two

Question: Was the same defect left in the mirror branch of the decision this fix
touched?

Needs: the diff and the full body of each changed function; when the change
states a rule of the form "this operation always does X", every branch and
caller of that operation.

Read: Write out the whole branch set of the condition the fix touches: success
and failure, purchase and refund, primary path and repair path, granted, denied,
not determined, and lookup failed. Check the patch against each branch. For a
new guard, list every way the guarded state can be reached (dismissal gesture,
programmatic route change, deep link, restore, native back, fallback,
reconnect) and confirm each is covered. A search for call sites will not find
this defect, because the sibling is the other half of the same decision.

Block when: a mirror branch keeps the identical defect and the change does not
show why that branch cannot be reached.

Do not block when: the mirror branch is genuinely unreachable and the change says
so; covering it would mean redesigning the neighbouring branch. Ask for the
shared guard, not a rewrite.

Examples:

- **[REQUIRED REPAIR] Completion race closed, cancellation race left open.** The
  new guard blocks while a charge is pending or delivery is outstanding, but a
  retained guard still rejects the "concluded with no charge" case
  unconditionally, so the symmetric store-cancellation race remains. Compared the
  guard against every terminal state of the purchase attempt. Repair target:
  cover the cancelled state with the same ownership rule.
- **[REQUIRED REPAIR] Lifetime check on two of four permission outcomes.** The
  flow captures the originating lifetime, but only the granted and denied
  branches check it; the not-determined and lookup-failed branches can still
  navigate for a flow that has been retired. Compared every outcome branch with
  the guarded ones. Repair target: apply the lifetime check before acting in all
  four.
- **[REQUIRED REPAIR] Repair path skips the filter the normal path applies.**
  Normal assignment filters candidates by the activities the player allowed;
  the repair path walks a default order with no filter, so a repair can assign
  an excluded family. Compared the two paths that produce the same assignment.
  Repair target: share one candidate filter.

## C-17 Symptom fixed, cause untouched

Question: After this fix, can the condition that produced the failure still
occur?

This is a primary concern, not one check among many: a change that makes a
failure quieter while the thing that fails is still there is the defect the
requester most wants caught, and the more important the failing path, the more
it matters. Report it first when it is present.

Needs: the diff; the report naming the symptom; the cause the change states; the
PR description and the issue, because a change of this kind often says in its
own words that the cause is unknown; the repository at head, to read the path
that produces the bad state.

Read: First fix what "the failure" is. When a change alters how a failure is
handled — stops a retry loop, fails forward, adds a terminal state, captures
the exception better — the failure for this check is the thing that failed,
not the handling around it. An issue that names the handling as the defect
("retries for minutes", "never records why") has named a symptom of the
failure; the question is still whether the thing that failed can still fail.
Then compare the change's description of the fix with its hunks. Find the code
that creates the bad state and see whether any hunk touches it. A change whose
only behavioral edit sits on the failure path (a catch, a default, a
null-coalesce, a retry, a delay, a clamp, a truncation) while the producer is
unchanged has treated the symptom. So has a fix that only changes logging,
telemetry, or the text of an error.

Block when: every behavioral change is downstream of the failure, no hunk
touches the producer of the bad state, and the change names no cause. A cause
that is "unknown", "historical", "tracked separately", or handed to a follow-up
issue is a cause the change does not name: the tracking issue is not the cause,
and containment of a symptom whose cause nobody has found is this finding, not
an exemption from it. Grade it a required repair when the symptom blocks the
user or sits on the path where money moves, however tidy the containment.

Do not block when: the cause is named and a blunt parameter change is the right
fix for it; the requester, in their own words, accepts shipping with the known
defect. An issue, plan, or scope statement that the agent or its reviewers
wrote or amended cannot stand in for that acceptance, even when the requester
asked them to set the scope. If
the fix renders the failure as a screen or a message, report that under C-12. If
the cause is shared and only one site was patched, report that under C-15. Size
of the fix belongs to C-08.

Examples:

- **[REQUIRED REPAIR] Audio defect handled by going silent.** When the bad
  playback state occurs the player now mutes; nothing changed in the code that
  lets the state occur. Compared the patched handler with the producer of the
  state. Repair target: prevent the state, then remove the mute.
- **[REQUIRED REPAIR] Wrong number replaced by a placeholder that flips.** The
  screen shows a placeholder until data arrives and then the value, but the
  request was for the correct number to be known before the screen renders.
  Compared the render path with where the value is computed. Repair target:
  make the value available at render time.
- **[REQUIRED REPAIR] A retry loop on a failed opening is made to stop, and the
  opening still fails.** After sign-in a purchase surface sometimes failed to
  open; the change makes the failure terminal after one attempt and moves the
  user on, and its own description says the original throw is unknown and
  tracked in another issue. Compared the hunks with the path that opens the
  surface: every hunk is downstream of the failure. Repair target: find the
  throw before shipping suppression, or bring the requester the decision to
  ship containment first, in those words.
- **[OBSERVATION] A long timeout is the root fix here.** The window was failing
  because it was too tight for a measured duration, and the change says so. A
  plain parameter change is sufficient when the cause is named.

## C-18 The check was loosened to pass

Question: Did the acceptance bar move in the same change that claims the thing
now passes?

Needs: the diff including tests; the base version of each touched test or check;
any coverage statement in the test file's own header; the stated purpose of the
change.

Read: Compare each touched assertion before and after: exact value to range,
equality to non-null, unchanged to empty, present to defaulted. Do the same for
thresholds, tolerances, timeouts, and a general check replaced by a list of
known cases. Compare the set of test names before and after with what the file
says it covers. When a shared condition gains a disjunct or a wider comparison,
compare everything it now admits with the requirement's stated scope. When logic
was extracted or generalized, compare the new rule's conditions with the old
rule's, and confirm retained tests read the path the running product uses.

Block when: a threshold, tolerance, expected value, skipped or deleted test, or
narrowed check changed in the change that claims a pass, and nothing in the
request authorized it.

Do not block when: the request asked for that test to be removed or turned off;
the request explicitly accepts the known defect. A missing test is never a
finding here, and added test machinery is C-36's subject. If the weakened test
could never have failed on the defect, report it under V-04 instead.

Examples:

- **[REQUIRED REPAIR] Precondition weakened from "unchanged" to "empty".** The
  verification gate used to require the queue to be unchanged; it now requires
  it to be empty, but two retained jobs are part of the accepted starting state,
  so the new predicate no longer proves what the old one did. Compared the
  predicate before and after. Repair target: restore the original condition.
- **[REQUIRED REPAIR] Widened comparison demotes entitled users.** Changing
  `earnedStars <= 1` to `earnedStars < 3` makes two-star subscribers lose their
  recovery action. Compared the set of states the condition admits with the
  requirement. Repair target: add the new case without widening the old one.
- **[REQUIRED REPAIR] Six tests vanished during a rewrite while the header still
  lists them.** Ownership rejection, value selection, and coverage explanation
  are no longer tested, and the file's own coverage comment still claims them.
  Compared test names before and after with the header. Repair target: restore
  the tests or the behavior they covered.

## C-42 The fix's own new code reopens the class

Question: Does the code this fix adds contain a fresh instance of the defect
class it repairs?

Needs: the diff; the report or finding the fix answers, with the class it names;
the repository at head; the earlier review rounds on this same work, when the
target carries them.

Read: Name the defect class in the report's own terms — a state read after an
await with nothing proving the owner is still alive, a missing value turned into
a valid one, an error caught and dropped, an expected value taken from the code
under test, a write that is not atomic with the thing it replaces. Then read the
lines this change adds as though they were new code arriving for the first time,
and apply that same class to them. Everything a fix adds is new code written
under the habit that produced the defect: the added guard, the fallback, the
retry, the reconciliation pass, the cache invalidation, and the tests and
helpers that come with them. Where earlier rounds exist, compare what round N-1
named with what round N added; the recurring shape is a fix that closes the
exact counterexample it was shown and reopens the same class one step over,
inside its own repair.

Block when: the lines this change adds contain an instance of the class this fix
names, or of a class an earlier round on this same work already named.

Do not block when: the instance you find is in code this change did not add and
nothing ties it to the repair, which is C-15's sweep of sibling sites; the new
code's version of the shape is unreachable and the change says why; the mirror
branch of the same decision is C-16; a moved acceptance bar is C-18; a repair
that never touched the producer at all is C-17.

Examples:

- **[REQUIRED REPAIR] The guard added for a disposal defect reads a disposed
  handle.** The repair for a post-await access on a torn-down screen adds a
  recovery path that awaits a refresh and then reads the same handle without
  rechecking it. Compared the added lines with the class the report named.
  Repair target: capture what the continuation needs before the await, in the
  new code as well as the old.
- **[REQUIRED REPAIR] A circular oracle repaired with another one.** A
  verification was found to take its expected value from the code it verifies;
  the replacement hard-codes a version constant copied out of the same module,
  so the check still agrees with itself. Compared the new oracle's source with
  the class the finding named. Repair target: derive the expected value from the
  external source the verification is about.
- **[REQUIRED REPAIR] The repair for a swallowed failure swallowed a different
  one.** A wrapper script was fixed for a failure that left no trace; the new
  code writes its evidence file without checking the write succeeded and returns
  the wrong exit status when it does not. Compared the added lines with the
  class the report named. Repair target: fail loudly on the evidence write and
  return the real status.
