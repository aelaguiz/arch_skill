# Review Catalog Index

Every check in the catalog, grouped by slice file: 67 checks in 16 slice files. Use this index to decide
which slices apply to the review target, to divide slices among children, and
to look up the entry for a finding you are verifying. The entries themselves
are in the slice files: what to read and compare, when to block, when not to,
and example findings.

A slice applies when the target actually contains what its header says it
needs. Record slices that do not apply in `coverage.md` with the input that was
missing.


## Code and pull request checks

Apply when the target has a diff.


### `catalog-code-agent-and-prompt-surfaces.md`

Applies when the diff touches prompts, skills, agent instructions, or workflow configuration: a skill package, a prompt or agent definition file, a repository-level instruction file, a reviewer or generator prompt, and the scripts, metadata, and generated copies that ship beside them. These files are live product surface and get the same reading as application code.

- **C-41 Judgment replaced by a rule, a script, or a gate.** Does this change take a decision away from the agent that the agent should be making?
- **C-44 An agent-facing surface that no longer matches what runs.** Would an agent that has only this changed surface and the repository do the right thing?


### `catalog-code-async-and-concurrency.md`

Applies when the change contains asynchronous work, concurrency control, shared or persisted state written from a response, or a destructive write. Needs the diff and the repository at head; C-30 also needs the repository's own instructions.

- **C-21 Guard before the await, not after.** Can the owner of this work change between the guard that approved it and the write that follows?
- **C-22 Detached async work with no error owner.** If this detached work fails, does anything hear about it?
- **C-23 A result that arrives after its moment.** Can a late, superseded, or cancelled result still change state or be reported as accepted?
- **C-30 New locking or elevated isolation.** Does this change add concurrency machinery to business state that operation identity and database constraints would handle?
- **C-35 A destructive write before the replacement lands.** If the process dies between the deletion and the completed replacement, what is left live, and can it be rebuilt?


### `catalog-code-comments-and-claims.md`

Applies when the change contains code whose correctness is not visible from reading it, a deliberate departure from what the surrounding code does, or prose that describes the change. Needs the diff, the repository at head with history for the touched lines, and whatever prose accompanies the change: the request, the pull request body, the README, and changed comments.

- **C-19 Non-obvious code with no why-comment.** Does each delicate thing this change introduces say why it is that way and what breaks if someone changes it?
- **C-20 Temporary or divergent code with no label.** Does every deliberate departure in this change say at the site that it is deliberate, why it is there, and what the end state is?
- **C-26 Prose claims more than the code establishes.** Does every claim in the prose around this change have a line of code or a named test that makes it true?


### `catalog-code-environment-trust-data.md`

Applies when the change touches how the software is built, installed, or launched, or contains SQL. Needs the diff and the repository at head, plus the build, continuous-integration, and deploy declarations for C-27, and the schema of every column the changed SQL compares for C-34.

- **C-27 Environment and config parity gap.** Does the path this change was exercised on declare the same environment as the path that ships?
- **C-34 SQL construction defects.** Can a value the producer really emits make this query return something other than what its author intends?


### `catalog-code-failure-handling.md`

Applies when the change touches an error path, a default for a missing value, a user-facing state that exists because something went wrong, a status gate, or a call into a vendor SDK. Needs the diff and the repository at head; C-12 also needs the request. These six checks ask what the code does when something is missing or fails. Report each defect once, under the check that found it.

- **C-10 A catch or guard that reports nothing.** Can an error path this change touches fail with nothing reporting it?
- **C-11 A missing value defaulted into a valid one.** Can a consumer tell a measured value from no measurement here?
- **C-12 A failure rendered as a user experience.** Does this change render a state that exists because something failed?
- **C-13 Diagnostic data trimmed, mapped, or redacted.** Does the report leaving this code carry what the provider returned?
- **C-24 A fail-open status gate.** Does an unrecognized, blank or missing value take the good path here?
- **C-31 An unwrapped platform SDK call.** Can a changed call into a vendor SDK throw past its error boundary?


### `catalog-code-fix-quality.md`

Applies when the change fixes a reported defect. Needs the diff, the repository at head, and the bug report, issue, or counterexample the fix cites.

- **C-15 The fix landed on the reported site only.** Does every other consumer of the thing this fix is about have the same protection the patched site now has?
- **C-16 Asymmetric fix: one branch of two.** Was the same defect left in the mirror branch of the decision this fix touched?
- **C-17 Symptom fixed, cause untouched.** After this fix, can the condition that produced the failure still occur?
- **C-18 The check was loosened to pass.** Did the acceptance bar move in the same change that claims the thing now passes?
- **C-42 The fix's own new code reopens the class.** Does the code this fix adds contain a fresh instance of the defect class it repairs?


### `catalog-code-layers-and-contracts.md`

Applies when the change moves logic across a module or package boundary, adds an import between layers, or changes a signature, a type, or a calling convention. Needs the diff, the repository at head for the boundaries and the existing adapters, and the call sites of every changed interface.

- **C-38 Logic placed in the wrong layer.** Does this change put feature-specific or lower-level knowledge in a layer that should not hold it?
- **C-39 A caller must remember an invariant the boundary should enforce.** Can a caller of this changed interface get it wrong without failing immediately?


### `catalog-code-owners-and-paths.md`

Applies when the change has a diff. Needs the repository at head as well: every check here compares something in the change against code that is not in the change, so none can be done from the diff text alone.

- **C-01 The superseded path is still on disk.** Did everything this change says it removed actually stop existing?
- **C-02 Unification in name but not in fact.** Did the number of live implementations actually go down?
- **C-03 Callers not moved, or an adoption count of one.** Does any surface doing the same job still reach the old mechanism?
- **C-04 A second implementation of an owned concept.** Does something in the repository already own the concept this new symbol computes, parses, validates, styles, fetches, or decides?
- **C-05 Two live paths decide the same fact differently.** Can two live paths give different answers about the same fact?


### `catalog-code-scope-and-surprise.md`

Applies when the change has a diff and the target carries what commissioned it: the request, issue, plan, or instruction, plus the description the change ships with. Needs the trunk for comparison, and a run or screenshots for the visual half of C-07 when the target has them.

- **C-06 A user-visible change nobody commissioned.** Would the person who commissioned this work be surprised to find this behavior in the result?
- **C-07 Collateral change under a non-product scope.** The stated scope was not a product change — did look, feel, and when things happen come out identical to the trunk?
- **C-37 The diff leaves the named surface.** Does every changed path fall inside the surface the task named?


### `catalog-code-size-and-machinery.md`

Applies when the change has a diff and the target carries the request that commissioned it. Needs the diff and its stat, the originating request, the repository at head, and the repository's own instruction file, which says whether this is a product, a hobby project, or an experiment. C-40 also needs the report, issue, or alarm the change answers, for how often the defect occurs.

- **C-08 Change size against the ask.** Is the durable machinery in this change a large multiple of what the request describes?
- **C-09 A new flag, mode, knob, or approval state.** Did the request ask for this control surface?
- **C-36 Test or receipt machinery added to a fix.** Did the request ask for the verification machinery this change adds?
- **C-40 A repair riskier than the defect it answers.** Does this change put more at risk than the defect it repairs costs?


### `catalog-code-telemetry-and-state.md`

Applies when the change touches analytics events, a persisted or published status field, the shape of state a caller has to interpret, a clock read, or a schema, wire or dependency contract. Needs the diff and the repository at head; C-14 and C-33 also need the other side of the contract — the event definitions and the queries that read them, or the client, second repository or lockfile still holding the old shape. These five checks ask what the system records and how it represents it. Report each defect once, under the check that found it.

- **C-14 Telemetry removed, renamed, gated, or absent.** Did this change lose an event, or ship a flow without one?
- **C-25 Derived status recorded as observed fact.** Does each status field's name match the event that sets it?
- **C-29 One field carrying two meanings.** Does any field this change touches take part in two decisions?
- **C-32 Device clock used to derive product state.** Is a clock read here stamping an event, or deciding something?
- **C-33 A schema or wire change with no compatibility answer.** What does a reader or writer on the old contract do after this lands?


## Proof and completion checks

Apply when the target includes a completion claim, a PR description, tests, run evidence, or screenshots.


### `catalog-proof-completion-claims.md`

Applies when the target carries a completion claim, a PR body, a status report, or a worker's summary. Needs the claim text, the artifacts it cites, the ask, and the repository at head. Report each defect once, under the check that found it.

- **V-01 A completion claim with nothing outside itself.** Does this completion rest on an artifact outside the claim whose content was read back?
- **V-05 Evidence that proves an earlier hop.** Does the cited evidence measure the thing the claim asserts, or something upstream of it?
- **V-11 A prescribed step or model not shown to have run.** Did the load-bearing step or model the ask named run, shown by something that could only exist if it had?
- **V-14 Merged treated as delivered.** Is the work this claim calls live actually running from a revision that contains it?
- **V-15 A claim sourced from a document or an agent.** Does each load-bearing fact come from a source that can be executed or queried rather than from something someone wrote?
- **V-20 A requirement dropped between ask and delivery.** Does every requirement in the authorizing ask have an artifact in the delivery, or an authorization to drop it?
- **V-21 A completion that discloses a defect.** Does the completion claim disclose an unresolved defect, a caveat, or a moved bar in its own text?


### `catalog-proof-fixtures-and-consistency.md`

Applies when the target has tests with fixtures or helpers, or an analysis or completion claim that sits beside earlier conclusions on the same subject. Needs the diff including tests and fixtures, the repository at head, the production code that would really produce the fixture's data, and the earlier documents on the subject.

- **V-24 A test that drains or retries its way to green.** Could this test reach its assertions by consuming or re-attempting whatever it met, instead of by the expected thing happening?
- **V-25 A fixture the real producer could not emit.** Could the production path that feeds this code have produced exactly this input?
- **V-23 A conclusion that contradicts the earlier one.** Does this conclusion disagree with what the canonical earlier document on the same subject concluded, without saying which is true?


### `catalog-proof-pictures.md`

Applies when the change touches user-visible code and the target carries screenshots, a mock, or both. Needs the images themselves, opened, the diff, and the ask. Both checks need a reviewer that can open images; where it cannot, both return could not evaluate rather than clean. V-12 asks whether the images exist, render, and show the claimed state; V-13 asks what they show against the mock, so a missing image set is V-12's alone.

- **V-12 Before and after images missing or wrong.** Do the images on this change exist, render, and show the states they claim?
- **V-13 The built screen not itemized against the mock.** Did someone open the built screen and the mock together and write out the differences?


### `catalog-proof-run-evidence.md`

Applies when the target has run logs, a named CI run, a test guide, or a scheduled job. Needs the completion claim, the diff, and the run evidence itself. V-02 compares the claim's surface against the surface that ran and V-22 compares the run's inputs against the changed paths, so one end-to-end run on the real surface satisfies both and is flagged by neither.

- **V-02 No end-to-end run on the real surface.** Was the behavior this claim names exercised on the surface a user actually touches?
- **V-03 A run with no device or build identity.** Does the run evidence say which device it ran on and which build it ran?
- **V-10 Green CI accepted without checking what ran.** Did the cited green run select and exercise the changed code at the head under review?
- **V-16 A procedure written but never executed.** Has anyone walked the procedure this change adds, as written?
- **V-17 An improvement claimed with no number.** Does this improvement claim carry a before, an after, and the target it is measured against?
- **V-22 Verification spend the user did not authorize.** Does each test or CI run here carry information the change actually needs?


### `catalog-proof-tests.md`

Applies when the change contains tests, fixtures, verification code, or a run offered as proof. Needs the diff including tests, the repository at head, the defect or requirement the proof cites, and the run record when a run is evidence.

- **V-04 A test that cannot fail on the defect.** If the lines this test guards broke again, would the test go red?
- **V-06 The test replaces the boundary the change touched.** Does this test still run the code the change edited, or a stand-in?
- **V-07 The oracle comes from the thing under test.** Did the expected value come from anywhere but the code under test?
- **V-08 An assertion a family of wrong values satisfies.** Does the value the defect produces satisfy this assertion?
- **V-09 An absence proved with no positive control.** Does anything show this harness detects the thing it reports zero of?
- **V-18 A retained test requiring the removed behavior.** Does a retained test or document still demand the removed behavior?
- **V-19 Verification code that checks existence only.** Would this verifier report success on a non-empty but wrong input?
