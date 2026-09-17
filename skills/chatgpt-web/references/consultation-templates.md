# Consultation Templates

Read the shape and the check, then the family that matches the ask, before
writing any submission to Pro.
Each family gives the brief as it should be written, in the user's own voice,
then the anti-patterns to keep out of it, one example of the shape agents
drift into, and what to attach. Slots are in square brackets. "Amir" below is
the user; Pro knows him by name, so the brief uses it.

Sections: [the shape and the check](#the-shape-and-the-check),
[A. Reviewing a PR](#a-reviewing-a-pr), [B. After fixes](#b-after-fixes),
[C. Checking the written-up plan](#c-checking-the-written-up-plan),
[D. Planning an issue with Pro](#d-planning-an-issue-with-pro),
[E. Standing advisor and on-track checks](#e-standing-advisor-and-on-track-checks),
[F. Design and research rounds](#f-design-and-research-rounds),
[G. Diagnosing a bug or a data anomaly](#g-diagnosing-a-bug-or-a-data-anomaly),
[H. Auditing content, an issue set, or a candidate list](#h-auditing-content-an-issue-set-or-a-candidate-list),
[I. Recovery: resend the whole thing](#i-recovery-resend-the-whole-thing),
[J. Starting a new thread or moving accounts](#j-starting-a-new-thread-or-moving-accounts),
[bugs the reviewer checks against](#bugs-the-reviewer-checks-against).

## The shape and the check

Every brief is a handoff to a colleague, not a request form. It makes five
moves, in this order:

1. **Open with where we are.** What we are building, in product words, and
   when something is being authored, what the finished thing will contain.
2. **Hand over the sources whole.** The canonical requirements source (the
   workbook, the spec, the design record) as a full export, the plan, the
   issue as filed, the user's words verbatim, raw evidence, and the PR or
   branch with the `@GitHub` pill in the composer. Never a link in place of the file,
   never the rows the agent picked, never the agent's summary.
3. **Say what was done and what was seen**, in three to five plain sentences.
4. **Offer the status as a belief.** "I think I'm done." "Where I'm least
   sure is…" The reviewer is invited to overturn it.
5. **Ask one question about intent**, and for a review say what kinds of
   problems to look for. Then say what happens with the answer.

The moves are sentences, not headings. A brief split under labels (Goal,
Context, Instructions, Output, or any renamed set of them) is a request form
again, even when the words under the labels are right. The brief goes into
the composer as written, paragraphs and bullets intact, with the paste method
in the composer reference. Files carry the sources, never the ask.

`@GitHub` and `@BigQuery` are written literally in the brief. Entered with
the paste method in the composer reference, each becomes the connector pill,
and the pill is what gives Pro the repo or the data. The words "GitHub
connector" in a message attach nothing. Every template below writes `@GitHub`
where the PR or branch is handed over: keep it, and verify the pill before
Send.

Wherever something is being authored, Pro writes it. The agent brings the
context, asks questions, goes back and forth until it is fully formed, then
carries the agreed result into the issue or the document verbatim.

After Send, the agent watches for Pro's answer. Sending is not done, and
"Pro is running, now I'm waiting" is not a place to end the turn. The
consultation is done when the agent has read the whole answer and acted on
it. The agent never ends its turn by telling the user that Pro is running or
that its answer is pending for the user to read, and never asks the user to
watch the thread. How the agent waits is up to its harness; that it waits is
not.

These families serve whichever model holds the seat, not only Pro. When
`issue-to-pr`'s primary is Sol or Fable, the brief is the same and "Pro" in
the template reads as that model. A seat without connectors gets the
worktree path and branch, `gh pr diff` saved to a file, and the same sources
by absolute path in place of `@GitHub` and attachments.

Never: a verdict token (PASS, APPROVED, VERDICT); a cap on the answer ("only
blocking findings", "one line per", "three sentences maximum"); a fence on
what Pro may conclude ("do not expand into…", "reject any drift into…"); a
commit SHA (say "here's the PR" and Pro reads the latest); the issue body or
any restatement in place of the source; "confirm" or "judge only whether";
the words "GitHub connector" in place of an `@GitHub` pill; handing the wait
back to the user. Narrowing the work never narrows what Pro
sees.

Before Send, read the draft once as the user and answer five questions. Would
he say this to a colleague in these words, as sentences rather than a form?
Could Pro reject my question and still help? Is the canonical source in the
room, whole, with the `@GitHub` pill? Did I narrow what Pro sees because someone
narrowed what I should build? Is my status a belief or a fact? A failed answer
means a rewrite, not a caveat.

## A. Reviewing a PR

When: a PR is pushed and the agent wants Pro's read before calling it
merge-ready. The largest family by far.

**Template A**

Hey. We're working on [plan name]; it's for [what it does for the player, one
sentence]. The [spreadsheet / spec] we've been working out of is attached,
full export; that's the source of truth for requirements. The plan is
attached.

I've been working out of branch [name]. Here's the PR: [#N]. @GitHub, read
the latest code on it yourself.

The issue I picked up was [#M]: [one sentence on what it's for]. [If #M was
cut or split from a bigger ask, say so here: the original issue, what Amir
actually asked for in his words, and what is still owed after this PR.]

What I did: [what changed, in plain words]. [What I ran and what I saw; raw
output attached.] I think I'm done. [If another reviewer already went through
this, say here what it found and what I did about it, attached as files; the
ask below still asks you to read the PR yourself first.]

Where I'm least sure: [one or two things].

Constraints I'm working around: [each one, and where it came from: Amir's
words, a real external limit, or something I read in the code and assumed].

What I'm looking for: did I implement the intent right, and is this the
cleanest, most pragmatic way to do it? Read the plan and the sheet first, then
the PR.

- Where am I introducing risk that really wasn't necessary for this feature?
- Where did I overbuild around edge cases?
- Where did I create new patterns where there were existing clean ones?
- Where did I create split brain: two places that can now answer the same
  question?
- Where did I create a web of individual calls rather than one centralized,
  clear abstraction?
- Where am I working around an architectural limitation that I should be
  tackling first, before I spread code all over the codebase?

If the issue itself got the intent wrong, or what I built will fight the rest
of the plan, say so. Check it against the bugs we've actually shipped
(attached). Real concerns, not pedantic ones. Whatever you find, I'll fix and
bring back.

**More to ask, depending on the PR**

Ownership: what does this PR claim is now true, and which code path owns that
truth now? Is there another live path that can still answer, change, or render
the same thing? Did I leave old entry points, fallbacks, flags, generated
files, tests, or docs teaching the old path? Would a future reader have to ask
which of two things is the real one?

Shape: if we started from what the player needs today, would we choose this
design again? Which requirement forces each new layer, flag, wrapper, or
registry to exist, and what breaks if it disappears? Did I take the nearby
easy path or the separated simple one? Does a caller now have to remember an
ordering, a cleanup call, or which owner to use? Is a flag deciding which
architecture owns behavior, not just which behavior is on?

Machinery: is new machinery hiding a decision I should have made explicit:
one owner, one mode, one type? Is anything generic for one concrete case? Did
a temporary shim become something new code depends on?

Done-ness: does the player's actual job work from the real starting state,
not a prepared test state? Did I move one caller to the new way and leave its
siblings on the old way? Is my proof showing that an artifact exists, or that
the live behavior is right? Do the tests mock the boundary that should be the
real owner?

Scope: would whoever commissioned this be surprised by any behavior change in
the diff? Did anything adjacent change that nobody asked for?

Failures: does it have silent failures? Does it swallow error conditions, or
throw away data we would use to debug? Do all errors make it properly into
Sentry?

Telemetry: does it have the telemetry we need so that, from a business
perspective, we can tell whether the thing is actually happening?

Experience: does it add user experience that wasn't specified, most commonly a
random toast or an interaction nobody asked for? Does it make something
synchronous that used to be asynchronous, so it now blocks and slows the user
down? Does it play nice with deep links? Does it work when users switch? Is
there any experience change that would surprise the person who asked for
this feature? For every change to what the player sees, did Amir personally
approve it, or did an agent convince itself it was fine and record that as
Amir's approval? Approval is his words, quoted and dated, about that change;
a reading of something he said about something else is not approval. If you
can't find his words, treat the change as unapproved and say so.

Data: are we abusing local storage for something that belongs in the actual
database for the user, where it survives a reinstall, a new device, or a
user switch?

Constraints: are we working around a constraint that makes this more
convoluted than it needs to be? Is that constraint real, and how do we know?
Did Amir say it, or did an agent read it in the code and treat it as an
immutable constant when it's something we'd happily change? For each
constraint the PR bends around, name it, say where it came from, and say what
the straight version would look like without it. If freeing us of the
constraint would make this simpler, say so plainly; Amir would rather remove
the constraint than ship the workaround.

Completeness: did we actually accomplish what Amir originally asked for?
Was that ask split into two or three issues along the way, with this PR
covering one of them, so that he thinks things are landing here that aren't?
Was the original issue quietly dropped, deferred, or replaced by a
prerequisite that got cut later? Is every piece of the original ask either in
this PR or named plainly as still owed, with the issue that owes it? If the
PR is being talked about as if it were the original issue, say so.

Tests: does it have the appropriate automation tests? Does it use unit tests
and property tests properly? Where something could conceivably pass a unit
test and still fail in practice, does it get an integration or fully
simulated test? That is how we catch all sorts of bugs. Is it race-prone?

**Anti-patterns**

- Pinning a commit SHA. Say "here's the PR" and let Pro read the latest code,
  all of it.
- Writing "GitHub connector attached" as text. Write `@GitHub` and verify it
  became a pill; otherwise Pro has no repo access.
- Asking for a verdict token. Pro gives its read; the agent owns the verdict.
- Capping the answer: "only blocking findings", "one line per finding",
  "under 1500 words".
- Fencing what Pro may conclude: "do not expand into…", "reject any drift
  into…".
- Pasting the issue body in place of the sheet and the plan. The issue is our
  translation; Pro needs the source.
- "Assess it on that accepted scope." Narrowing what Pro sees because the work
  was narrowed.
- "Review it" with no flavor. Say what kinds of problems you want found.
- Leading with your own test counts and CI status as if they were the verdict,
  then asking Pro to confirm.
- Waiting for CI before sending the review, or between rounds. Pro reads the
  branch; CI is the very last step, after Pro has cleared the PR.

Not this: "Review PR 4734 at exact head 57eb43e4 against the approved plan.
Return APPROVED only if this exact head is correct, complete, minimal, and
merge-ready; otherwise return CHANGES REQUIRED with only blocking in-scope
defects. Do not require RustAI, Patrol, Flutter work, or any other adjacent
milestone scope."

**Attach**: the GitHub PR link with the `@GitHub` pill; the plan document; the
spreadsheet, if there is one, as a full export of every tab; the issue as
filed; the user's words about this work, verbatim; raw test output; the repo's
review policy and incident rules when the repo has them (see the last
section).

## B. After fixes

When: Pro found things, the agent fixed them, and wants Pro's read again.

**Template B**

Back with the fixes. They're pushed to the same PR, [#N]; read the latest.

Last time you found [the findings, in plain words]. Your answer is attached,
and everything from the first round is re-attached so you don't have to scroll
up.

What I did about each: [finding 1: what I did]. [Finding 2: what I did.]
[Finding 3: what I did, or why I disagreed.]

What I'm looking for: same question as last time, does this implement the
intent, and is it still the cleanest way to do it? Read the PR again as a
whole. Don't just tick my fixes; they touched [areas] and I'd rather you catch
something new now than after merge. Where did the fixes add risk that wasn't
needed, overbuild an edge case, create a new pattern beside an existing one, or
leave two owners for one thing? Did fixing your findings push me into working
around something I should have fixed at the source? Check the changed areas
against the bugs we've actually shipped.

**Anti-patterns**

- "Judge only whether each finding is resolved." That certifies the list, not
  the PR.
- Pinning the new SHA. The fixes are on the PR; Pro reads the latest.
- Sending only the fix list and the delta. Re-attach the sheet, the plan, and
  the first-round evidence.
- Running this round more than once. A second round means the basis of the
  review changed; start again as A.

Not this: "Fix verification. The attached plan applies your five findings:
(1)… (5)… Judge only whether each of the five findings is now resolved as you
specified. First line PASS or CHANGES REQUIRED, then one line per finding."

**Attach**: everything from the first review, re-attached; Pro's previous
answer; the GitHub PR link with the `@GitHub` pill.

## C. Checking the written-up plan

When: Pro wrote the plan in D and the agent carried it into the issue or the
plan doc. Before anyone builds, Pro reads the write-up against the code. A
plan Pro did not write is not reviewed here; it goes through D so Pro writes
it.

**Template C**

We lined this plan up together in this thread and I've written it into
[issue #M / the plan doc]; it's attached. Before anyone builds, read it
against the code.

The sheet is attached, full export. The branch is [name], @GitHub; check the
plan's claims against what's actually there. Here's what
Amir has said about this: [his words, dated].

Where I'm least sure: [the part I may have carried over wrong, or the part of
the code I didn't check].

What I'm looking for: did I carry over what we agreed, word for word where it
matters? Does it still have all seven parts, and is each one actually clear:
the outcome, the acceptance criteria, the requirements, the architecture, the
do's, the do not's, the test plan? Is there anything the code makes wrong now
that we didn't see when we outlined it? Is there anything in it that would
leave two owners for one thing, a web of calls, an overbuilt edge case, or a
workaround for something we should fix first? Anywhere the plan says Amir
approved something, especially a change to what the player sees, is his
approval there in his own words, or did an agent infer it? Is the plan
bending around a constraint nobody verified is real, and would Amir just
remove it if he knew? What would you do better? If it's right, say so. I don't
need a list to feel reviewed.

**Anti-patterns**

- Sending Pro a plan the agent wrote from scratch and asking it to check.
  That is D: Pro writes it.
- Asking for APPROVE or REVISE. Ask what's wrong and what's missing.
- A list of what the reviewer may not propose.
- "Return only blocking corrections."
- Calling the agent's own reading of scope "frozen" or "binding". Only the
  user's decisions are, and those are quoted.
- Pinning a commit. Point at the branch.

Not this: "Review the attached D2 implementation plan before any source
changes. Return APPROVE only if the plan is implementation-ready. Otherwise
return REVISE and list only concrete correctness or scope blockers. Reject
any drift into Director, SNG protocol, Go, Flutter, real AI, four-through-six
seats, antes, movement, balancing, or generic mode abstractions."

**Attach**: the written-up plan as it now sits in the issue or the doc; Pro's
outline from the D thread; the spreadsheet as a full export; the user's words
verbatim; the branch with the `@GitHub` pill.

## D. Planning an issue with Pro

When: the agent is picking up an issue. Pro writes the plan; the agent brings
the context, asks the questions, goes back and forth until the plan is fully
formed, then carries the agreed plan into the issue.

**Template D**

Look, I'm trying to turn [issue #M] into a really strong implementation plan,
and I want you to write it up. When it's done it will have:

- a clear outcome we're after
- top-level acceptance criteria
- extremely clear requirements
- a clear architectural plan
- clear do's
- clear do not's
- a clear test plan

Here's where I'm at now. We're working on [plan name]; it's for [what it does
for the player]. The sheet we've been working out of is attached, full export.
The plan we're working from is attached. I've been working out of branch
[name]; @GitHub, read it yourself. The issue is [#M]; in my
words, it asks for [two sentences]. What I found in the code: [what exists,
what the seams are, what surprised me]. Here's what Amir has said about this:
[his words, dated].

Outline it for me. How would you structure it? Give me your first cut with
all seven parts, and say where you're unsure or where you need something from
me. For a really well-architected but highly pragmatic solution, what are the
key requirements, specifically? How would we know we did this well? Is there a
clear separation of concerns? Are there clear patterns, and are they the ones
the codebase already has? Is there one owner for each truth, one abstraction
instead of a web of calls? Is there an architectural limitation we should fix
first rather than plan around? What would you do better? What tests should we
put in up front that would actually tell us we succeeded? Name every
constraint you're planning around and where it comes from: Amir's words, a
real external limit, or something read in the code. If a constraint isn't
Amir's and dropping it would give a simpler plan, say so and outline the
simpler version too, so I can ask him to free us of it.

I'll ask questions and we'll go back and forth until it's fully formed. Then
I'll put the final version in the plan doc and the issue exactly as we agreed.

**Anti-patterns**

- The agent writing the plan and asking Pro to check it. Pro writes; the agent
  asks the questions.
- Handing Pro the agent's own approach as the starting outline.
- A generic opener: "plan this with me", "I need to start thinking through
  this plan." Say what the finished plan will contain.
- Taking Pro's first cut as final. Go back and forth until all seven parts
  are solid.
- Rewording the agreed plan when carrying it into the issue.
- "Do not expand scope" before the plan exists.

Not this: "Review the attached implementation plan for issue #4735 against
current main 20566b4b. Return PASS or CHANGES REQUIRED. Check that it is the
smallest root-cause repair. Name only must-fix defects before implementation
and do not expand scope."

**Attach**: the spreadsheet as a full export; the plan document we're working
from; the issue as filed; the user's words verbatim; the branch with
the `@GitHub` pill; any prior Pro planning in the thread.

## E. Standing advisor and on-track checks

When: an epic is in flight and the agent wants to know whether it is still
building the right thing.

**Template E**

Quick check-in on [the epic]; it's for [what it does for the player]. Here's
what Amir said he wants out of it: [his words, dated]. Sheet and plan
attached, current versions.

Where we are. Done: [plainly]. In flight: [plainly]. Next: [what I'm about to
do and why]. What I'm worried about: [the thing].

What I'm looking for: am I still on the right path for what Amir wants out of
this, or have I drifted? Say it straight. Of what he originally asked for,
what is done, what got split into other issues, and what got dropped without
anyone saying so? If the next thing I've queued is the
wrong thing, tell me what the right thing is. Have I started working around
something I should have fixed at the source? Is the stack growing patterns
we'll regret? If the next step needs a plan, outline it and we'll go back and
forth on it here.

**Anti-patterns**

- "Three sentences maximum." "ON TRACK or OFF TRACK."
- "Answer from thread context, no file reads needed." Attach the current
  sheet and plan every time.
- A wall of queue state with no product framing and none of the user's words.
- Asking whether the queue is right without saying what the epic is for.

Not this: "Boundary on-track check, answer from thread context now (no file
reads needed): six of ten lanes are merge-ready as a PR stack. Three
sentences maximum, then one line: ON TRACK or OFF TRACK with the correction."

**Attach**: the spreadsheet as a full export; the plan document; the user's
words about the epic; the live queue as the agent sees it; the `@GitHub`
pill.

## F. Design and research rounds

When: multi-round design work. Pro writes the design; the agent brings the
record, the user's words, and the questions.

**Template F**

Round [n] on [the topic]; it's for [what it does for the player]. When we're
done, the record will have: [the decision, the interface or contract, worked
examples, what we cut, and the questions only Amir can answer].

Since last time: Amir said [his words, verbatim]. We tried [what] and saw
[what happened]. The current record is attached. The new inputs are attached.

What I'm looking for: you write the next version. The thing I need your
thinking on: [the open question, in one or two sentences]. Don't take my
framing as fixed. If you think we're solving the wrong problem, or that last
round's answer was wrong, say so and why. I'll ask questions and we'll go
back and forth until it holds together.

**Anti-patterns**

- Pointing at an "ask file" with a one-line message. The ask goes in the
  message; the file carries the sources.
- The agent drafting the design and asking Pro to check it.
- Dictating the output format when the answer's shape is Pro's call.
- Leaving out what the user said between rounds.

Not this: "Round 4: Amir rejected the section 8 starters. Go back to the
product need and pick 3 to 5 starter situations. Details and the per-starter
shape are in the attached 30-round4-ask.md. Answer as a markdown file."

**Attach**: the current design record; every new input since the last round;
the user's words from between rounds; the prior round's answer if the thread
moved.

## G. Diagnosing a bug or a data anomaly

When: something is broken or a number is wrong. Pro leads the diagnosis and
writes up the fix; the agent brings the evidence and goes and gets more.

**Template G**

Here's what's happening: [the symptom, in product terms: who sees what, since
when, how often]. Here's what I've looked at and what I found: [the evidence,
plainly]; the data and logs are attached. Here's what I think it might be and
why I'm not sure: [the theories, and what each would predict]. This is
everything I have. @GitHub on the branch. @BigQuery where the data lives.

What I'm looking for: how would you think about figuring out what the problem
is? If you can see what it is, say so. If you need something I haven't given
you, tell me what to go get and I'll go get it. When we've found it, you write
up the diagnosis and the fix, with the tests that would prove it, and we'll go
back and forth until it's solid.

**Anti-patterns**

- "Return only a GitHub issue comment ready for an implementer." Think first;
  file later.
- Handing over the agent's diagnosis as the frame instead of the symptom and
  the evidence.
- Forbidding classes of fixes, or asking for "the smallest fix", before the
  cause is known.
- Pinning a SHA. Give the branch and the data.

Not this: "Read issue #4938 and current main at exact SHA 696ecf16. Derive the
smallest evidence-first solution plan. Return only a GitHub issue comment
ready for an implementer. Do not widen thresholds, mute the verifier, or add
generic retries, fallbacks, modes, flags, or frameworks."

**Attach**: every data pull, log, and screenshot the agent used; the issue if
one exists, offered as a report not a diagnosis; `@GitHub` on the branch;
`@BigQuery` when the question is about data.

## H. Auditing content, an issue set, or a candidate list

When: the agent has a report, an audit, or a list of candidates. Pro sorts
what's real and writes the issue set; the agent asks the questions and files
exactly what was agreed.

**Template H**

Here's [the audit / the list / the report], attached in full. Here's what it's
for and why we made it: [two sentences]. Here's the current state of [the repo
/ the issues]; @GitHub so you can check it against reality. Here's
what Amir has said about this area: [his words, dated].

What I'm looking for: go through it and tell me what's real, what's a
duplicate of something we already have, what should be one issue versus
several, and what we should not build at all. Push back on the audit itself
where it's wrong. Then you write the issue set: for each one, the outcome, the
scope, the acceptance criteria, and what not to build. I'll ask questions and
we'll go back and forth; then I file exactly what we agreed.

**Anti-patterns**

- A one-line pointer at the file with no story about what the artifact is
  for.
- The agent writing the issue set and asking Pro to check it.
- Asking for a filing plan before the sort.
- "Recommend the smallest truthful action for each" as the only allowed
  output.

Not this: "Review the attached DATA WATCHDOG root-cause file. Challenge the
four diagnoses and recommend the smallest truthful action for each, using the
linked issues read-only."

**Attach**: the audit or list in full; the source it was made from; the
user's words about this area; the `@GitHub` pill.

## I. Recovery: resend the whole thing

When: the submission went out without its attachments or `@GitHub`, ran on
the wrong model, or Pro's answer was cut off or the page broke. If Pro is
still generating on a wrong submission, stop it first; its answer is
unusable, and a follow-up with the files does not repair it.

**Template I**

Your last answer [got cut off after X / ran on the wrong model / didn't have
@GitHub attached]. Nothing about the ask has changed. Here's the
whole original ask again, with everything re-attached: [the full original
brief, verbatim]. Start over from the sources, not from your partial answer.

**Anti-patterns**

- Narrowing the retry: "complete only that finding in at most four
  sentences."
- Retrying with fewer attachments than the original carried.
- "If it is not actionable, say PASS."
- Letting a wrong submission finish because "the prompt is self-contained",
  then sending the files afterward.

Not this: "Your response truncated again after 'P1: Valid prepaid
subscription'. Complete only that finding in at most four sentences. If it is
not actionable, say PASS."

**Attach**: everything the original ask carried, re-attached; `@GitHub` and
`@BigQuery` in the brief again, as pills.

## J. Starting a new thread or moving accounts

When: the thread is saturated, the account is rate-limited, or the run resumed
and Pro has none of the history. This is where context is most easily lost.

**Template J**

Starting a fresh thread because [the old one hit its limit / the account is
capped]. You haven't seen any of this, so here's the story so far. What we're
building and why: [product words]. What Amir has decided, in his words:
[quoted, dated]. Done: [plainly]. In flight: [plainly]. Next: [plainly].
Attached: the sheet in full, the plan, the key rulings from the old thread,
the current issues. Read all of it before answering.

Then here's what I need from you today: [the ask, written in the A, C, D, or
E shape].

**Anti-patterns**

- "Full context is in the attached file" with a one-line message. The story
  goes in the message; the file carries the sources.
- Starting the new thread with a narrower ask than the old thread carried.
- Summarizing the old thread's rulings instead of exporting them.

Not this: "Continuation of the epic 4732 advisor thread (other account is
rate limited); full context and the two asks are in the attached
continuation.md. Read-only review of PR #63 on its branch, head a4a0a24c, plus
the on-track check described in the file."

**Attach**: the spreadsheet as a full export; the plan document; the old
thread's rulings, exported; the user's words, quoted with dates; the current
issues; the `@GitHub` pill.

## Bugs the reviewer checks against

A review brief (A, B, C) points Pro at the defects this codebase has actually
shipped, and attaches the list rather than restating it. Where the repo keeps
a review policy, attach those files: for `funcountry/psmobile` they are
`.github/claude/repo_review_policy.md` and
`.github/claude/partials/incident_rules.md`, the human-approved memory of
confirmed defects that PR-Agent already reviews against. For a repo without
one, the cross-repo classes below still apply and go in the brief in the
user's words:

- Two owners for one thing: a second helper, path, entry point, or truth
  source beside an existing one; copy-pasted logic; test-only guards that make
  tests run different code than production; compatibility shims for
  hypothetical cases instead of a migration.
- Stale paths after a claimed migration or centralization: old entry points,
  flags, generated artifacts, docs, or tests still teaching the old path.
- Proof that an artifact exists (a renamed test, a doc, a log line, a
  snapshot) standing in for proof the live behavior is right; verification
  commands that do not run what they claim.
- A behavior change the commissioner would be surprised by, delivered as
  "cleanup" or "while here".
- New locking, elevated isolation, or generic retry machinery where operation
  identity and constraints would do; retries on an error name alone.
- Platform SDK calls without an error boundary; reads after an await without
  proving the owner is still live; fire-and-forget work with no owner.
- Telemetry: event names outside the catalog, paired events out of symmetry,
  enrichment skipped, downstream queries that filter on fields that can be
  NULL.
- A fix for a symptom of something a recent change introduced, instead of the
  root.
