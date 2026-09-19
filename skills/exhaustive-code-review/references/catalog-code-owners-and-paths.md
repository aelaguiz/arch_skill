# Catalog Slice: Owners And Paths

Applies when the change has a diff. Needs the repository at head as well: every
check here compares something in the change against code that is not in the
change, so none can be done from the diff text alone.

These five checks are cut apart on purpose, because a change can pass any two
and fail a third. C-01 asks whether the replaced thing is gone. C-02 asks
whether the number of real implementations went down. C-03 asks whether every
caller moved. C-04 asks whether this new symbol should have existed at all.
C-05 asks whether two deciders that both exist can disagree. Report each defect
once, under the check whose comparison found it. Where the logic sits in the
wrong layer, or an interface leaves its invariant to the caller, the layers and
contracts slice owns it (C-38 and C-39).

## C-01 The superseded path is still on disk

Question: Did everything this change says it removed actually stop existing?

Needs: the diff; the repository at head; the claim of removal, retirement,
migration, or deprecation, wherever the target makes it.

Read: List every removal claim, then look for the file and the symbol at head.
The comparison is the claim against disk, never the claim against the change's
own narrative: a path made impossible to compile, a redirect stub, or a rename
with a legacy or versioned suffix is still on disk. Then sweep the residue
around the removed feature — constants, flags, enrollment tables, telemetry
definitions, generated artifacts, comments, acceptance prose, and live
documentation, examples, or install instructions naming a changed symbol,
command, route, schema, environment variable, or entry point. Removed behavior
that survives as a callable, tested option inside a shared engine is the same
finding, and so are retained tests and handoff notes still demanding what the
change deleted. Ask what still reaches the symbol, not whether the product's
entry point does. Then look the other way: find what existed only to feed,
consume, or measure the thing that was removed — an ingest, a metric, a column,
a job, a label reader. When the change removes the only producer or the only
reason for such machinery, the machinery is part of the same deletion, and
leaving it live is this finding, not a follow-up.

Block when: a path the change claims to have removed exists at head and
something live can reach it — a caller, a registered route, a flag, an alias, or
a test that is now its only caller — or residue of the removed feature still
names it in code, configuration, telemetry, generated artifacts, or live docs,
or machinery that existed only to serve the removed thing is still running with
nothing left to serve.

Do not block when: the retained code carries a comment naming a planned
restoration or a deliberate placeholder; the request named a carve-out, or the
survivor is a front-of-house entry point kept deliberately while the machinery
behind it went; the plan staged the migration and this is the staged step — but
a hedge is not a stage, and "delete or migrate", "quarantine for now", and
"remove in a follow-up" all read as keeping it; a document is marked historical.
A developer-facing surface people use — a playground, a demo, sample data, seed
support — is live, and deleting it is the finding in the other direction; a test
alone is not such a surface. Tie the finding to the claim the change made or to
residue of the feature it removed; do not widen it into a dead-code sweep.

Examples:

- **[REQUIRED REPAIR] A deleted mode was only made impossible to compile.** The
  instruction said delete, the plan's verb softened to retire, and the module
  and its symbols are still at head. Compared the instruction's verb with the
  plan's, then with the files on disk. Repair target: delete the module and its
  symbols, keeping only the entry point that was carved out.
- **[REQUIRED REPAIR] The install guide still teaches the direct writer.** Draft
  writes go through the shared owner now, while the guide's example still
  imports the old function, so the next reader restores the old path. Compared
  the changed call path with every document naming the old symbol. Repair
  target: update the example or delete it.
- **[REQUIRED REPAIR] Retained tests still demand the deleted rule.** After an
  exclusion rule was removed from a generator, retained assertions still require
  generation from inventory that can no longer fit the budget, and a published
  migration inventory still tells the next implementer to keep the cutoff.
  Compared both with the new requirement. Repair target: delete the assertions,
  correct the inventory.

## C-02 Unification in name but not in fact

Question: Did the number of live implementations actually go down?

Needs: the diff; the repository at head, for the call graph and the data flow;
the text that makes the unification claim.

Read: When a change claims to unify, centralize, consolidate, or produce a
single owner, count the real implementations before and after by tracing the
call graph and the data flow, not the names. Three comparisons find it: whether
the new owner is called by every surface or delegates back to the old ones;
whether a file moved and was renamed with its body unchanged; and, when
something is claimed switched off, whether the mechanism stopped running or only
its symptom disappeared. A wrapper that forwards its arguments unchanged,
repeats the method names of the thing it wraps, and owns no invariant is a
second API, not a unification. Read the call sites before and after, the
repeated logic the new layer claims to remove, and the tests: one that asserts
the new label or mocks the wrapper instead of the outcome is evidence the old
behavior is untouched.

Block when: the change claims unification, centralization, consolidation, or a
single owner, and the count of live implementations did not go down — the new
owner delegates back to the old ones, the old implementations keep their
callers, or the removal is a rename, a barrel file, or a move with an unchanged
body.

Do not block when: the approved plan called for a facade, or for a temporary
bridge with a named deletion point and no new callers; the wrapper now owns a
real invariant, hides a risky boundary, or reduces caller burden; the two things
genuinely differ in contract and you can say how — do not deduplicate
reflexively, since merging two comparators that look alike can leave one
over-rejecting and the other under-checking; the divergence has a named
user-visible reason, which "it is intentional", "it is historical", and "the
code is different here" are not; both sites carry comments saying why two
patterns exist and what the cleanup is. A layer whose only justification is
future flexibility is C-08; a helper built for one call site is C-04.

Examples:

- **[REQUIRED REPAIR] One new interface in front of three surviving caches.** A
  proposed asset pipeline put a single new API over three existing caches and
  reported one owner. Compared the count of real implementations before and
  after. Repair target: collapse to one implementation and delete the other two.
- **[REQUIRED REPAIR] The unified import owner leaves the old path live.** The
  new service gives the migration a unified name while scheduled jobs still call
  the old importer directly, so one behavior has two live owners. Compared the
  new owner's callers with the old function's. Repair target: route the job
  through the new owner, or delete the old path.

## C-03 Callers not moved, or an adoption count of one

Question: Does any surface doing the same job still reach the old mechanism?

Needs: the diff; the repository at head or the trunk, to enumerate the old
mechanism's callers; the plan or issue, if it staged the migration.

Read: Enumerate the old mechanism's callers on the trunk and check each against
the changed-file list. Count adopters in both directions: a new owner with two
adopters and eleven stragglers is not done, and a new shared component, pattern,
or helper whose only caller is the code that introduced it has an adoption count
of one. Look for the sibling forms a changed-file list hides: an adjacent route
still accepting the old shape, a command alias still pointing at the old
registry, a fallback reader, a direct mutation path, one generated consumer
regenerated while another is stale, a flag that keeps both selectable after the
migration is claimed. When a migration leaves both a new method and an older,
more permissive one callable with different ownership rules, the old one is the
finding, and the repair is deleting it rather than documenting which to use.

Block when: after the change a surface doing the same thing still reaches the
old mechanism and nothing in the target says the migration was staged; or a new
shared component's adoption count is one.

Do not block when: the approved plan staged the migration and named the
remaining callers and their phase, or the new component is the first step of an
adoption list the plan enumerates; the user narrowed the sweep to the pieces
causing trouble; the user asked for the narrow landing plus a follow-up, since
the defect is a split nobody was told about rather than the split itself;
compatibility normalizes immediately through one adapter with no shared
invariant broken; no pattern existed before and this change establishes and
documents one. That the old path still exists after a deletion claim is C-01;
that the new owner never took the work is C-02.

Examples:

- **[REQUIRED REPAIR] The command line moved to the new config owner; the
  scheduled job did not.** The entry point loads through the shared config
  service while the nightly job still reads environment variables directly, so
  the same import runs with different defaults depending on how it starts.
  Compared the two entry points' configuration sources. Repair target: move the
  job to the shared owner, or give both one adapter.
- **[REQUIRED REPAIR] The new storage pattern's only adopters are the features
  that introduced it.** The migration was reported complete while every feature
  already on the trunk still used the old per-surface pattern. Compared the old
  mechanism's callers on the trunk with the changed-file list. Repair target:
  move the existing features, or drop both the claim and the new pattern.

## C-04 A second implementation of an owned concept

Question: Does something in the repository already own the concept this new
symbol computes, parses, validates, styles, fetches, or decides?

Needs: the diff; the repository at head, to search for the existing owner; the
repository's conventions, such as a canonical styles file, a components
directory, or a shared resolver; the ask, when it names a thing to reuse.

Read: For every new function, record, enum, parser, comparator, predicate, fetch
path, query, style constant, or widget the diff introduces, search for the
symbol that already owns that concept; the new code should call it. The owner is
usually close at hand: the canonical styles, the existing component, the fixture
sitting directly above the work, the server call that already carries the data.
Look the same way for a rule copied rather than called — a caller repeating
validation, a test encoding a production rule instead of exercising the owner, a
script reimplementing runtime behavior, a prompt copying policy that belongs in
a shared reference — and for direct mutation that reaches around the owner of a
piece of state. When two fields end up encoding one fact, ask which wins if they
disagree; the repair is to pick one carrier and delete the other, never to add a
reconciliation rule. A helper that exists for one call site and names no domain
concept is the small form of the same defect.

Block when: a new symbol computes, parses, validates, styles, fetches, decides,
or writes the same thing an existing symbol in the repository already owns, and
the new code does not call it.

Do not block when: the request said not to force reuse, or the existing owner is
known bad and research was asked for first; no pattern exists yet, since
establishing one and documenting it is correct and the failure is inventing
without looking, not the existence of a new component; the two contracts
genuinely differ and merging them would over-reject or under-check; the local
rule is truly presentation-only, or ordinary adapter glue that normalizes a
shape immediately; the supposed central owner turns out not to own the changed
concept once you read it. Two deciders that both survive and can disagree at
runtime are C-05; a surface left on the old mechanism is C-03.

Examples:

- **[REQUIRED REPAIR] A screen hand-writes a parser the repository owns.** A new
  inline glossary span builder with a hand-written word-boundary rule duplicates
  an existing glossary link widget, and the specification had said not to add a
  parser. Compared the new parser with the owner the repository names. Repair
  target: call the existing widget.
- **[REQUIRED REPAIR] Form validation duplicates the account schema.** The form
  reimplements name length and character rules locally while the shared schema
  already owns that contract, so the service and the interface can disagree
  about a valid name. Compared the local checks with the schema. Repair target:
  validate through the schema.
- **[REQUIRED REPAIR] A toolbar button writes the draft itself.** The new button
  calls the low-level writer directly while the rest of the editor saves through
  the session service, which owns validation and retry. Compared the button's
  save path with every other save path. Repair target: save through the session
  service, or move the new validation into that owner.

## C-05 Two live paths decide the same fact differently

Question: Can two live paths give different answers about the same fact?

Needs: the diff; the repository at head, to find the sibling deciders; the
requirement naming which decider is authoritative, if one exists.

Read: Start from whatever the change calls selected, eligible, assigned,
winning, or valid. Find every place that decides membership or ordering of that
set — the query, the in-process filter, the audit or coverage query, the fixture
— and put their predicates side by side: the conditions, the sort key, the sort
stability, the tie-break order, and any field one side requires that the other
does not. Many of these bugs live entirely in the tie-break. The same shape
appears when one feature reads the central store while another reads a local
copy, when two schemas describe one contract, and when two generated artifacts
can drift apart. This is the runtime consequence of C-04, and a separate check
because the two owners usually both existed before the change; the diff only
made their disagreement reachable.

Block when: two live paths can disagree about the same fact, nothing makes one
authoritative, and a user-visible or recorded outcome depends on which one
answers.

Do not block when: one is documented as the authority and the other reads it
rather than recomputing; the two contracts genuinely differ and you can name the
difference; the disagreement is unreachable because one path is not live; both
sites carry comments saying why two rules exist and what the cleanup is; there
is one writer, or the work is idempotent and fenced. A new symbol duplicating an
existing owner, with no second live decision yet, is C-04.

Examples:

- **[REQUIRED REPAIR] The item that justifies the choice is not the item
  assigned.** The policy picks the content family from the most recently worked
  saved item, while the candidate list for that family sorts by category, band,
  authored order, and identifier, so the user can be handed a different item
  than the one that chose the family. Compared the policy's selection rule with
  the candidate comparator. Repair target: one shared rule, so the item that
  wins selection is the item assigned.
- **[REQUIRED REPAIR] A coverage query certifies what the selector would
  reject.** The verification query judges an association usable from exact
  pairing and a non-null owner, while the selector it certifies also requires a
  cutoff, representative uniqueness, and owner agreement, so a missing answer
  can be certified as recovered. Compared the query's predicate with the
  production selector's. Repair target: have the query call the selector.
