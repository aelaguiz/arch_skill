# Catalog Slice: Environment And Data

Applies when the change touches how the software is built, installed, or
launched, or contains SQL. Needs the diff and the repository at head, plus the
build, continuous-integration, and deploy declarations for C-27, and the schema
of every column the changed SQL compares for C-34.

Both checks are settled by an artifact outside the diff: a second declaration,
or a row the producer can really emit. Report each defect once, under the check
whose comparison found it.

## C-27 Environment and config parity gap

Question: Does the path this change was exercised on declare the same
environment as the path that ships?

Needs: the diff; the repository at head; every build, continuous-integration,
and deploy declaration plus lockfiles; the release build's flags; and the
environment identity of whatever run evidence is offered.

Read: Take each logical input the change touches — a dependency set, an
environment variable, an install command, a build flag, a pinned version, a base
image, a launch command — and list every place it is declared. Then compare those
declarations field by field against the path the artifact actually ships through.
One conceptual input declared twice is the signal: a manifest and a lockfile, two
images, two runners, the development environment and the integration one, the
integration one and production. Do not accept that it was validated elsewhere;
ask which declaration that validation used. For a bumped dependency, read the
package's own declared floor for its native side and its changed defaults instead
of its version number — a bump can raise the minimum platform version underneath
it, or turn a capability on by default. For a compiled runtime, compare the
shipping image's build flags with the ones the tests were built with, then check
that the runtime base actually carries the shared libraries that choice needs.
For a launch command, compare it argument by argument with the one it replaced
and follow the startup path to the first use of whatever the omitted arguments
were supposed to initialize. Where a gate recomputes an environment identity,
check that it does so where the declared values exist. Read added imports as
part of the declaration: an import of a platform-specific or optional library is
resolved when the code is built, so a runtime check around the call site cannot
rescue the platforms that then fail to compile or start. Find the import, not
the guarded call.

Block when: the exercised path and the shipping path declare the same input
differently, and the difference can change whether the artifact builds, starts,
or behaves as tested; or a changed import binds a platform-specific or optional
dependency unconditionally while the code is still expected to build or run
where that dependency does not exist.

Do not block when: one declaration is generated from the other; the difference is
formatting, generated output, or lockfile churn you have confirmed mechanical —
diff size is not a proxy for risk; the repository marks the work as a hobby
project. Never propose a new environment-verification harness as the repair; the
repair is making the two declarations agree. A document that teaches an install
command the code no longer uses is C-26; this check is about two live
declarations that disagree.

Examples:

- **[REQUIRED REPAIR] Integration installs from the lock, production from the
  manifest.** The integration job installs only the frozen lock file while the
  production image installs from the requirements manifest, so a root requirement
  can change without any run exercising it. Compared each installer's input with
  the one the shipped image uses. Repair target: have both install from the same
  resolved input.
- **[REQUIRED REPAIR] Server image cannot build the package it now imports.** The
  image is built with the C interoperability layer disabled, and the new import's
  real implementation lives in a file that requires it; the local tests were built
  with it enabled and passed. Compared the image's build flags with the test
  build's. Repair target: build the image the way the code requires, and confirm
  the runtime base carries the shared library that choice needs.
- **[OBSERVATION] Lock file churn is mechanical.** The lock file diff is large and
  is entirely re-resolution of the same declared ranges; the manifest, the image,
  and the runner still name the same inputs. Size alone is not this check's
  subject.

## C-34 SQL construction defects

Question: Can a value the producer really emits make this query return something
other than what its author intends?

Needs: the changed SQL; the producer's real value set — schema, enum members,
nullability — for every column the query compares; the canonical model the query
is meant to agree with; and the fixtures' as-of dates.

Read: Read the changed SQL against what its columns can actually contain and try
to build a counterexample: one row that makes the query answer wrongly. Several
shapes repay attention. A comparison against a literal inside a conditional
expression, with no null coalescing, evaluates to unknown rather than true when
the column is null, so the branch falls through and a genuinely missing value is
silently treated as the benign case. A distinct count used as an unambiguity test
ignores nulls, so rows carrying no value at all are counted as agreement. A
coalesce where a minimum or maximum is meant collapses a set to its first
non-null member. An ingestion-time or partition column bounding an event window
measures when the row arrived, not when the event happened. A row-number
deduplication whose filter runs in a different order from the canonical model's
keeps a row the model already dropped. String replacement applied to an assembled
query corrupts any other expression containing the same token; the safe form
edits the tagged field before assembly. An ordering predicate reading a receipt
or emission timestamp orders by when a record was written rather than when the
thing happened, which is a different sequence whenever a record is reconstructed
later. Fixtures computed relative to the current date make the result depend on
the day the suite runs.

Block when: you can state a value the producer really emits that makes the query
return something other than what the author intends. Report the shape and its
counterexample together.

Do not block when: you cannot produce the counterexample — say so rather than
arguing the shape; the repository has no SQL. Platform and library choice is not
a finding, and deliberate repetition in fixtures, such as repeated explicit type
declarations, is not one either. Add no statistical caution about
denominators, populations, or completeness. The same
null-dropping comparison written in code rather than in query construction is
C-24 when it gates a status or an enum and C-11 when it supplies a default for a
missing value.

Examples:

- **[REQUIRED REPAIR] Missing health silently becomes "nothing to see".** A
  conditional compares a feed-health column against a literal with an inequality;
  when the column is null the comparison is unknown, the branch falls through,
  and a feed with no health reported at all is treated as benign instead of as an
  unknown that should hold the alarm. Counterexample: one row with that column
  null. Repair target: coalesce the column to an explicit unknown before
  comparing.
- **[REQUIRED REPAIR] Distinct count treats two nulls as agreement.** The query
  tests campaign unambiguity with a distinct count of at most one; distinct
  counting ignores nulls, so two rows that both carry no campaign are labelled
  exact rather than mixed and an attribution is claimed that the data does not
  support. Counterexample: two rows, both null. Repair target: count the absent
  value as its own value, or exclude those rows before the test.
- **[REQUIRED REPAIR] Pairing ordered by the wrong clock.** The replay pairing
  predicate orders on the delivery timestamp the pipeline stamps rather than the
  domain timestamp in the payload, so a terminal event emitted by the following
  session sorts beside the next cold start instead of at the end of the
  interrupted one. Counterexample: a pair scoring zero of two on delivery time
  and one of two on the domain time, with no clock skew involved. Repair target:
  order on the domain timestamp.

