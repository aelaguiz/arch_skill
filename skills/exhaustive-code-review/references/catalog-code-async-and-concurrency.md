# Catalog Slice: Async And Concurrency

Applies when the change contains asynchronous work, concurrency control, shared
or persisted state written from a response, or a destructive write. Needs the
diff and the repository at head; C-30 also needs the repository's own
instructions.

These checks all ask what happens to work that outlives the moment it started.
Report each defect once, under the check whose comparison found it.

## C-21 Guard before the await, not after

Question: Can the owner of this work change between the guard that approved it
and the write that follows?

Needs: the diff; the repository at head, to read the lifecycle of whatever scopes
the work — who can change the account, session, day key, generation, or mounted
state while an awaited call is outstanding.

Read: For each await in code scoped to an identity, session, route, or
lifecycle, find the guard before it and the write after it, and ask whether
anything between them re-reads live state. A guard comparing two values both
captured before the await proves nothing, because the point is that the owner
changed during the wait. Write the reachable sequence out step by step from the
source alone: one owner starts the work, a second signs in while the call is
outstanding, the first resumes and writes into the store it captured. Do this
for every branch rather than the one a report named — these defects are usually
branch-specific, covering the granted outcome and not the undetermined one, the
non-empty token and not the null one. A check placed after an awaited helper
returns is too late when the helper already wrote. Where the host can swap the
scope without rebuilding the subtree, an alive-or-mounted check says nothing
about identity.

Block when: an await sits between the ownership check and a write to shared,
identity-scoped, or persisted state, and nothing re-reads the live owner before
the write.

Do not block when: a guard genuinely re-reads live state immediately before the
write; the awaited work cannot outlive its owner by construction. The repair is
a re-read and an early return. Never propose a mutex, a lock, or a retry layer
here — C-30 blocks those.

Examples:

- **[REQUIRED REPAIR] Identity re-checked on one branch of two.** After awaiting
  a token refresh, the binder re-reads the live account only on the non-empty
  token branch; the null-token branch writes the previous account's data under
  the new session. Compared each branch's post-await guard with the write after
  it. Repair target: re-read the live account on both branches and return early
  when it changed.
- **[REQUIRED REPAIR] Stale response applied as clean state.** The hydrate path
  checks pending and dirty state before awaiting the fetch, then applies the
  response as clean, discarding an edit that committed while the fetch was in
  flight. Compared the moment of the check with the moment of the write. Repair
  target: re-read pending and dirty state after the response arrives and drop it
  when they changed.

## C-22 Detached async work with no error owner

Question: If this detached work fails, does anything hear about it?

Needs: the diff; the repository at head, to find the existing error-attaching
helper and to see whether a caller's failure path assumes a report already
happened.

Read: Find every call that starts work without waiting for it: an explicit
unawaited wrapper, a call whose returned future is dropped, a future read with
no retained subscription or owner. For each, follow the failure and name the
handler that would receive it. The sharpest form is a detached call inside a
synchronous try/catch — the block returns before the work can fail, so the catch
covers only the failure to start it, and the caller believes an error was
reported when nothing reported it. Then read the caller's failure path and see
whether it is written as if that failure would arrive there. Check what the
change leaves running: a listener, timer, subscription, or handle registered
with no teardown on the owner's disposal has nobody to stop it or hear from it.
Finally, find anything that reads the value the detached work produces with no
bounded wait, tests included, and check the reverse direction — whether a
committed mutation waits on, or takes cancellation from, a best-effort side
channel.

Block when: detached work can fail with no attached handler, a caller's error
handling is written as if that failure would surface there, or a committed
mutation takes its lifetime from best-effort work.

Do not block when: the failure is genuinely inconsequential and the code says so;
the detachment primitive's documented semantics attach a handler — read the
provider's documentation rather than assuming. Prefer the repository's existing
error-attaching helper to a new wrapper. A result that arrives too late is C-23.

Examples:

- **[REQUIRED REPAIR] Synchronous catch around queued work.** The transfer wraps
  a try/catch around a call that returns a queued future, so storage, decode, and
  enqueue failures happen after the block has returned, and the caller's error
  callback assumes a report that never happens. Compared the lifetime of the try
  block with the lifetime of the work. Repair target: attach a failure handler
  through the repository's existing helper so the caller's error path receives it.
- **[REQUIRED REPAIR] Committed mutation takes a best-effort lifetime.** A
  committed product mutation is made to wait on, and take cancellation from, a
  best-effort message delivery, so cancelling the delivery cancels the mutation.
  Compared the two operations' guarantees. Repair target: commit the mutation
  independently of the side channel.

## C-23 A result that arrives after its moment

Question: Can a late, superseded, or cancelled result still change state or be
reported as accepted?

Needs: the diff; the repository at head; the full set of writers for the state in
question; the transport's documented cancellation semantics.

Read: Two comparisons. First, for every handler that writes shared state from a
response, look for an explicit revision compared against the one currently held
before the write, and check that the revision is written in the same transaction
as the data it orders. Ordering keyed on a creation timestamp, a random
identifier, a pre-commit sequence, arrival order, or a count is a finding: a
database sequence is not rolled back with an aborted transaction, so a failed
write can still consume an ordering value. Second, for every deadline, race,
dispose, or cleanup path, trace the losing branch forward — does the underlying
work stop, is it fenced from writing or reporting after it loses, and if it
already succeeded, does that acceptance survive the teardown? A deadline stops
the caller waiting; it does not cancel the source work or anything downstream of
it. Where two independent facts travel in one payload, they can have different
ages.

Block when: a late or superseded result can overwrite newer accepted state, a
cancelled operation can still write or report, or teardown discards an acceptance
the remote side already granted.

Do not block when: there is a single writer; the work is idempotent and fenced
against writing after it loses. Do not accept "the whole reply is one unit" as
the repair, and do not accept a lexicographic comparison of two numbers as a
version check. If the gap is a missing error owner rather than an ordering rule,
that is C-22.

Examples:

- **[REQUIRED REPAIR] Unconditional upsert applies an older snapshot.** The stats
  store overwrites with no version comparison, so a hydration already in flight
  lands on top of a newer applied value — a refill to 50 followed by an older
  value of 100. Both writes are transactional, so ordering, not atomicity, is the
  defect. Compared the write path with the concurrent producers. Repair target:
  carry a revision written in the same transaction and reject a reply that is not
  newer.
- **[REQUIRED REPAIR] Route disposal discards a granted acceptance.** The submit
  runs inside route-scoped overrides; disposing the route retires that scope, so
  a successful response can be dropped before the acceptance boundary records it.
  Compared the operation's lifetime with the route's. Repair target: register the
  operation against the longer-lived authenticated owner before dispatch, and
  separate "may this be shown" from "was this accepted".
- **[REQUIRED REPAIR] Recovery restarts the generation counter.** A reconnect
  path opens a fresh generation-one namespace although a seat had published a
  higher generation before the restart, so the client rightly rejects the lower
  value as stale and can never consume the recovered snapshot. Repair target:
  derive the new value so it is provably greater than anything published.

## C-30 New locking or elevated isolation

Question: Does this change add concurrency machinery to business state that
operation identity and database constraints would handle?

Needs: the diff; the repository's own instructions, which govern here.

Read: Look for a new row, table, or advisory lock over user or business state, a
transaction raised to a stricter isolation level, a mutex over shared state, or
generic compare-and-swap, version, or retry machinery. For each, find the
corruption it answers: an observed incident, a reproduced sequence, a failing
test. Defensive locking added against a corruption nobody has observed is the
common case, and the deadlocks that reach production are usually created by the
lock ordering itself. Then ask what the same guarantee costs without it: a unique
constraint on the operation's identity, an idempotent write keyed by that
identity, one owning transaction. Read a retry layer the same way — it must
retry on a demonstrated transient conflict rather than an error's name, and
restart the whole owned transaction rather than a partial unit whose side
effects then run twice. Check initialization order too: timers, callbacks, and
mutable state set up after the owner is reachable by a concurrent lifecycle.

Block when: the diff adds locking, elevated isolation, a mutex on shared state,
or a generic retry, version, or compare-and-swap layer over business state, and
cites no observed corruption that it answers. A rationale in a comment or commit
message does not settle this one: the machinery answers an observed corruption
or comes out.

Do not block when: the shape is a bounded competing-worker claim on one
operation-specific queue that commits the claim before any network work; the
repository's own instructions authorize the mechanism by name. Where the
repository says nothing, treat this as a strong prior and still tie the finding
to the changed lines. If the machinery is also most of the diff for a small fix,
the size belongs to C-08; report the machinery here.

Examples:

- **[REQUIRED REPAIR] Distributed lock redesign inside a cleanup.** A cleanup of
  historical fee rows grew into a multi-file change carrying a non-expiring
  distributed-lock design that also touches normal subscription and shipment
  paths, for a backlog that turned out to be empty. Compared the incident being
  cleaned up with the machinery introduced for it. Repair target: drop the lock
  layer and key the cleanup on the operation's identity.
- **[OBSERVATION] Queue claim is the retained shape.** Workers claim one row each
  from a single operation-specific queue and commit the claim before any network
  work, so two workers cannot take the same item and nothing is held across a
  remote call. A bounded competing-worker claim is the exception this check
  keeps.

## C-35 A destructive write before the replacement lands

Question: If the process dies between the deletion and the completed
replacement, what is left live, and can it be rebuilt?

Needs: the diff for the ordering; the repository at head, to find every other
writer of the same recovery flag or ledger row.

Read: Find every clear, delete, truncate, or batched removal issued before a
bounded replacement has completed, and ask what an observer sees in between. The
safe order is stage then commit: write the new content, then remove the stale
remainder. Chunked writes make this concrete — a clear followed by values sent in
chunks leaves the live artifact empty or partly written when a chunk fails, and
recording the job as failed afterwards does not restore the last good state. The
same shape appears wherever a write is not atomic and partial state matters:
truncating a live file before rewriting it, or saving records before the cursor
that orders them. For any restore-on-failure promise, check that the recovery
state is durably persisted before the first destructive call, that a fresh
process can rediscover it, and that a cleanup failure preserves the original
error instead of replacing it. For any "recovery owed" record, enumerate every
write path that can clear it, including a failure on a different axis. Whether
the artifact can be re-derived from a source that outlives the process decides
how bad it is.

Block when: a failure between the destructive step and the completed replacement
leaves the live artifact empty, half-written, or unrecoverable, or the recovery
record lives only in process memory or in one status branch.

Do not block when: the target is genuinely disposable — a cache, a scratch table,
a regenerable artifact — and nothing reads it between the two steps.

Examples:

- **[REQUIRED REPAIR] Import saves records before the cursor advances.** Records
  are written before the remote cursor update succeeds, and the failed update is
  logged without rolling them back, so the next run imports the same page again.
  Compared the ordering of the two writes with what a crash between them leaves
  behind. Repair target: put the record writes and the cursor update in one
  transaction, or make the import idempotent through its canonical service.
- **[REQUIRED REPAIR] Recovery record lives only in memory.** The dispatcher
  commits its destructive preparation before sending the first copy request, and
  the specification needed to restore the original lives in a local variable, so
  a failure mid-restore deletes the original with nothing to rebuild it from.
  Compared what a fresh process could discover with what the restore promises.
  Repair target: persist the record before the first destructive call.
