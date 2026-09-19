# Catalog Slice: Run Evidence

Applies when the target has run logs, a named CI run, a test guide, or a
scheduled job. Needs the completion claim, the diff, and the run evidence
itself. V-02 compares the claim's surface against the surface that ran and V-22
compares the run's inputs against the changed paths, so one end-to-end run on
the real surface satisfies both and is flagged by neither.

## V-02 No end-to-end run on the real surface

Question: Was the behavior this claim names exercised on the surface a user
actually touches?

Needs: the completion claim or PR body; the diff, including test and harness
code; the run log or the named run; the ask.

Read: Set the behavior the claim names beside the surface the evidence
exercised. A unit test, a widget test, a golden test and a component harness
each exercise a different surface from the one a user reaches, so none can
carry a claim about user-visible behavior. Follow how the run reached the state
it reports: state advanced through a skip flag, a QA command, a developer
fast-forward or a direct injection never went through the user-facing control,
and that control is where the defect lives. Read the harness invocation's
configuration against the conditions reported broken, since a run with delays,
retries or error injection switched off exercises the easy path. Two halves
tested separately leave the seam untested.

Block when: the claim is that user-visible behavior works and the only evidence
is a unit, widget, golden or component exercise; state advanced through a skip
flag, QA command or injection rather than the user's control; the harness
disables the conditions reported broken; or the surface run was the nearest
reachable one.

Do not block when: nothing user-visible changed; the repository is a hobby
project or probe; the user said they will test it themselves; the message is
interim reassurance, not a completion claim. A missing unit test is never a
finding, and this never becomes a demand for a full sweep: V-22 owns that.

Examples:

- **[REQUIRED REPAIR] Both halves of a credential rotation tested, the rotation
  never run.** Compared the claim that rotation works against evidence covering
  each half in isolation. Repair target: drive the whole path once.
- **[REQUIRED REPAIR] "The build works" proved by an upload.** A release
  pipeline ran to store upload with nothing installed or opened. Compared the
  claim against what the run reached. Repair target: install and open it.
- **[REQUIRED REPAIR] Coverage rows filled with the wrong test type.** The
  requirement named device automation; the rows held unit tests. Repair target:
  run the named framework.

## V-03 A run with no device or build identity

Question: Does the run evidence say which device it ran on and which build it
ran?

Needs: run logs or screenshots; the plan or task document that pins the device;
the branch or commit under review.

Read: Two comparisons, both about identity and neither about who ran it. First,
the device or simulator identifier in the log against the instance pinned at
the top of the plan or task document; a run on a second instance is a run on an
unknown machine state. Second, the installed build against the code under
review, tied by a branch, a commit or an install receipt; without that tie a
pass can come from an old build left on the device for another reason. Read the
run for instances booted or shut down mid-branch, for more than one device on
one branch, and for runs with no visible window, where nothing could be
watched. A pass from an unidentified device or unknown build invalidates the
evidence, not the change.

Block when: test evidence carries no build identity, meaning no branch, commit
or install receipt tying the run to the code under review; the device
identifier differs from the one the task named; instances are booted or shut
down mid-branch, or more than one is in use; or the run was hidden.

Do not block when: no device work is involved; the apparent absence was
corrected, such as windows hidden rather than headless; the user changed the
device themselves. Whether an agent may drive the device at all is the user's
call, not this check's. Only identity is.

Examples:

- **[REQUIRED REPAIR] A false pass from an old sideloaded build.** A device
  test ran against a build left there for another reason, with nothing tying it
  to the branch. Repair target: build from a fresh checkout and install that.
- **[REQUIRED REPAIR] Installed on a device the task never named.** The install
  reached a device other than the connected one, on a branch for another
  platform. Repair target: pin one instance for the branch and run on it.
- **[OBSERVATION] Runs bounced between two simulators mid-session.** Each run
  opened a new instance, none named and none shut down, so no result can be
  attributed to a known machine state.

## V-10 Green CI accepted without checking what ran

Question: Did the cited green run select and exercise the changed code at the
head under review?

Needs: the repository at head; workflow, hook and branch-protection
configuration; the PR body or status claim; the CI result itself.

Read: Re-resolve the status yourself at review time, name the exact head you
read, and compare it with the commit the cited run was computed on: a pass on
an ancestor is no evidence for a descendant. Then read the wrapper rather than
the job's name. Compare the required check's file globs with where the changed
code lives, and the discovery root the job invokes with where the new tests
were added, since a suite never selected reports green. Look for steps set to
continue on error, and for shell sequences where a later command's exit status
overrides an earlier failure, such as a hook appending a block after the
command whose result matters. Compare the protection context string with the
producing status's name.

Block when: the cited green run covers an ancestor of the head under review;
the required check's globs exclude the changed code or its tests; a step or
hook masks a failing exit status; the protection context string does not match
the producing status; or a cancelled run is called a pass.

Do not block when: CI is deliberately run last and has not run yet, so there is
nothing to audit; the branch has a gate the user said not to wait on; an
unreadable red check is named as a blocking unknown. Never turn this into a
recommendation to add more CI; spend at the wrong moment is V-22's.

Examples:

- **[REQUIRED REPAIR] The gating check never selected the changed callers.**
  Its globs excluded the integration-test directories, so a shared helper
  passed while an excluded caller no longer built. Repair target: gate them.
- **[REQUIRED REPAIR] A hook whose exit status did not reflect its lint run.**
  It ran lint, then ran an appended block regardless, so it exited on the
  second command and diagnostics were hidden. Repair target: fail on the lint
  result.
- **[REQUIRED REPAIR] Green because the step could not fail.** A device
  test-lab step passed with continue-on-error set, while an integrated run of
  the same suite had two failing cases. Repair target: let it fail the run.

## V-16 A procedure written but never executed

Question: Has anyone walked the procedure this change adds, as written?

Needs: the diff; the guide, runbook or job definition itself; the session
record or worklog for the run.

Read: A procedure-shaped deliverable, such as a test guide, a QA document, a
runbook or a scheduled job, is a claim that its steps work. Look for a record
that someone walked them: screenshots, a log, a result column, a session
record. Writing down how to check something is not checking it, and a guide
that has never been executed usually contains steps that cannot be followed as
written. Then compare the introducing commit of any schedule or cron entry with
the introducing commit of the script it runs: when they arrive in the same
change, the first execution will be unattended, with nobody watching it fail.

Block when: a test guide, QA document or runbook is added or presented as ready
with no record of a run; or a scheduled job is added in the same change that
introduced the script it runs.

Do not block when: the guide documents a procedure already walked in the same
session; the document is explicitly marked unvalidated. A request to
canonicalize an already-executed manual procedure into the permanent suite is a
follow-up, not a block.

Examples:

- **[REQUIRED REPAIR] Twenty-one visual checks presented as ready, never
  followed.** Compared the guides' steps against any record of running them;
  there was none. Repair target: mark them unvalidated and walk each one first.
- **[REQUIRED REPAIR] A schedule whose first run would be its first run.** A
  new routine's script and its schedule entry arrived in the same change.
  Compared the two introducing commits. Repair target: run it by hand once.
- **[OBSERVATION] A journey verified by hand never entered the suite.** The
  coverage existed only for the length of the session; canonicalizing it is
  follow-up work, not a block.

## V-17 An improvement claimed with no number

Question: Does this improvement claim carry a before, an after, and the target
it is measured against?

Needs: the completion claim or PR body; the diff; the plan or issue for the
stated target; any benchmark output with its build mode.

Read: Take each claim of improvement, smoothness, responsiveness, speed or
volume and look for three things: a measurement before the change, a
measurement after it, and the target the work was supposed to reach. An
adjective where the plan already states a threshold is the clearest case,
because the bar exists and was not used. A number with no target is the same
defect from the other side. Read the build mode any performance number came
from, since a debug build measures the debugger and cannot support a release
claim. A claim about data volume, or about how many people something affects,
rests on a count, so look for the query behind it.

Block when: an improvement, smoothness, speed or volume claim carries no before
and after measurement; a measurement is offered with no target; a performance
number was taken in a debug build; or a claim about volume or affected
population is made without querying the data.

Do not block when: the user graded the surface by feel and rejected a passing
number, since the measurement supports the judgment and never overrides it; no
target exists for that surface and the work is not performance-sensitive; the
statement is not an improvement claim. This asks for a measurement, never a
harness.

Examples:

- **[REQUIRED REPAIR] "Silky smooth" against a written frame-rate threshold.**
  The plan set a sustained frame rate with no dips; nothing was measured.
  Compared the adjective against the written threshold. Repair target: measure.
- **[REQUIRED REPAIR] "High volume" with no query behind it.** A data
  population was described as large with nothing read from the warehouse.
  Repair target: produce the count.
- **[OBSERVATION] After-numbers with no before.** A performance document
  captured results after the change with nothing measured first, so there was
  nothing to compare against.

## V-22 Verification spend the user did not authorize

Question: Does each test or CI run here carry information the change actually
needs?

Needs: the diff's changed paths; the test or CI invocation and its run logs;
the completion report; the ordering of the review loop.

Read: Compare the inputs of each test or CI invocation with the paths the
change touches. Targets spanning code the diff never went near cost machine
time and prove nothing about the change; on a large native codebase they
saturate the machine other work runs on. Compare the run history against the
commit: a suite already green at this exact commit, run again, holds no new
information. Read the run for constants added to make it longer, such as a
sleep, a soak, a repeat count or an N-of-3 average, and ask what decision needs
it. Read where CI sits in the loop, since running it between review rounds buys
waiting while running it once at the end buys the same answer.

Block when: the test or CI selection's inputs do not intersect the changed
paths; a suite already green at the same commit is re-run; a sleep, soak or
repeat-count constant is added; CI runs between review rounds rather than last;
or a report withholds its verdict over untouched cases.

Do not block when: the re-run is an implementation re-run or a device-lab
re-run after a fix, since the no-rerun rule applies to external review loops; a
branch-specific gate the user said must pass; the end-to-end run V-02 requires,
which is the minimum. This check is never permission to run nothing.

Examples:

- **[REQUIRED REPAIR] A full mobile automation suite for a narrowly scoped
  change.** Compared the suite's coverage against the changed paths. Repair
  target: run the cases that touch the change.
- **[REQUIRED REPAIR] A verdict withheld over untouched cases.** A completion
  was refused because two dozen cases the change never touched had no execution
  evidence. Repair target: scope the verdict to the change.
- **[OBSERVATION] Waiting on CI between review rounds.** Half an hour went to a
  CI wait between two rounds rather than one run at the end.
