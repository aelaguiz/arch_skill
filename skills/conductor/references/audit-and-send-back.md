# Audit And Send-Back

The conductor's review is the mechanism that makes delegated workers safe, and it
is where the expensive model's tokens are supposed to go. The posture is
imported from the cynical review canon (`cynical-code-review`,
`cynical-architecture-review`, `cynical-cruft-removal`) and it inverts the
burden of proof:

**The default verdict for every returned slice is NOT ACCEPTED. The slice must
earn acceptance out of repo truth. Everything the worker returns — status,
summary, changed-file list, quoted test output, rationale, labels like
"migrated", "unified", "deleted", "verified" — is a claim, not evidence.
Current code behavior and structure — and the work products the conductor has
personally loaded and checked — are the authority for factual completion; the
frozen plan contract and explicit human approvals are the authority for
scope.**

The trust failure this exists to prevent: reading `STATUS: done`, a plausible
summary, and a green-looking quoted test run, skimming the diff stat, and
accepting. That is consuming the worker's story. The conductor's job is to try
to break the story and accept only what survives.

## Audit Procedure Per Returned Slice

1. **Restate the claims to falsify.** Before reading any diff, write down (in
   the log or scratch) what the slice contract says must now be true in code,
   plus every discrete claim in the worker's footer. The footer is a claims
   manifest — use it to enumerate what to check, never to frame conclusions.
   Do not let the worker's narrative order or emphasis steer the audit.
   Re-read the plan's human authorization anchors, frozen initial convergence
   closure, and freeze anchor. Do not audit against only the latest phase text.
2. **Falsify the cheap claims against git.** `CHANGED FILES` vs `git status`;
   `DELETES EXECUTED` vs the slice's delete obligations vs the actual diff.
   Any mismatch between a worker claim and repo reality is itself a finding
   and counts against session health — a worker that misreports its own
   changes is misreporting everything else too.
3. **Trace beyond the diff.** The diff shows what the worker touched; the lie
   usually lives in what it didn't touch. Trace the authority path for the
   changed behavior: callers, readers, writers, the old path, competing
   same-contract surfaces, generated artifacts, and prompt/config surfaces.
   Confirm the new path is the *only* live path when the contract says
   replace, and that the user-visible job actually works from the starting
   state that matters — not just the narrow internal case the worker
   exercised.
4. **Apply the three lens groups.** These are distinct failure families;
   delegated workers can commit all three:
   - **Integrity lenses** (did the work lie by name, status, or structure?):
     name-only completion — right vocabulary while the intended unification,
     simplification, or behavior change is false underneath; partial
     unification and split-brain owners; side doors and stale authority
     paths still reachable; stopped-short workflows; treat every attractive
     label — unified, canonical, migrated, deleted, complete, verified — as
     a specific claim to trace, not a description to accept.
   - **Architecture lenses** (did the work add structure nothing forces?):
     weak worker runs add rather than integrate. For every new abstraction,
     wrapper, helper file, adapter, flag, registry, layer, or ownership
     split the diff introduces, ask what requirement forces it to exist and
     what breaks if it disappears. No forcing requirement means accidental
     architecture: a finding, even when the behavior is correct.
     Subtraction-first — the slice done with fewer concepts and less code is
     the standard the diff is judged against.
   - **Cruft lenses** (did the work leave or create waste?): a reference
     proves a mention, not a live purpose; a test proves a test exists, not
     that the behavior matters. Hunt dead code introduced or orphaned by the
     change, the old path kept "just in case", compatibility ghosts and
     shims, debug leftovers, commented-out corpses, tests that pin the old
     behavior alive or test mocks instead of behavior, and un-executed
     entries from the plan's delete list. The delete list is a checklist,
     not a hope.
5. **Personally load and verify every claimed work product.** When a slice's
   deliverable is an artifact rather than (or besides) code — a screenshot,
   rendered page, report, spreadsheet or data model, generated file,
   exported document, chart, dataset, recording — its existence is zero
   evidence, and loading it is sanctioned first-class conductor spend, never
   an economy to skim. A worker saying "screenshot attached showing X" has
   made two claims: that a file exists, and that it shows X. Only the second
   one matters, and it is the one routinely taken on faith. Verify
   substance, not shape:
   - a screenshot is viewed and depicts the claimed state — not a blank
     page, error screen, wrong screen, login wall, stale build, or
     placeholder;
   - a spreadsheet or data model is opened and its math is checked:
     spot-recompute representative totals, trace formulas to their stated
     assumptions, tie key numbers to their claimed sources — plausible
     cells are not verification;
   - a report or document is read and its assertions are checked against
     current code or the primary evidence it cites;
   - a generated file is opened, well-formed, current, and spot-checked
     against the source it claims to derive from.
   Delegate inspection only for an artifact class the conductor genuinely
   cannot render — the format cannot be opened with available tools at all,
   such as video or a proprietary binary with no textual extraction. Large,
   tedious, or numerous artifacts are not unrenderable; images, PDFs, HTML,
   spreadsheets, and every text-based format are renderable by default.
   Record the delegation and its cannot-render reason in the acceptance
   entry, and require the inspecting fleet worker to return extracted evidence —
   actual cell values, recomputed figures, quoted text, described screen
   content — never a verdict. "Confirmed, looks correct" from a child is a
   claim, not an inspection. The implementing worker's description of its
   own artifact never counts.
6. **Falsify analytical conclusions before relying on them.** Workers return
   conclusions as well as code and artifacts: "the bottleneck is X", "Y is
   already handled", "this approach can't work", "I checked Z and it's
   fine". Any conclusion the conductor will act on, relay upstream, or use
   to close a finding must carry anchors — files, symbols, commands, data —
   and the conductor verifies the anchors it relies on first-hand or through
   a different clean fleet worker. An unanchored conclusion is a hypothesis: send
   it back for evidence rather than adopting it. Fluent, confident prose is
   exactly what a capable model produces when it is wrong.
7. **Treat proof as a claim until reproduced.** Quoted verification output is
   text a worker produced; it can be stale, partial, run against the
   wrong tree, or fabricated. Decisive proof — the checks the slice's
   acceptance actually rides on — must be independently reproduced by a
   verification worker in a different clean fleet session (or the delegated
   phase verification pass) before the slice is accepted. The implementing
   worker's own run never closes its own slice for anything beyond trivial,
   directly-inspectable changes, and "trivial" is the conductor's judgment
   from reading the diff, not the worker's assurance. Trivial means the
   conductor confirmed correctness completely by direct reading during the
   audit — a doc edit, a config value, a rename traced end to end; anything
   whose correctness rides on runtime behavior is not trivial, and every
   trivial call is recorded in the acceptance entry so the shortcut stays
   auditable. Also check the proof itself proves the right thing: right
   commands for the changed surface, assertions that would actually fail if
   the claim were false.
8. **Judge factual validity** for every finding: `accepted` (technically real),
   `rejected` (wrong, with contradicting evidence), or `unresolved`. Then assign
   a separate scope disposition: `authorized`,
   `frozen-convergence-required`, `new-scope-needs-human`, `out-of-scope`, or
   `unauthorized-built-scope`. Only the first two route to ordinary repair.
   `new-scope-needs-human` is an escalation, `out-of-scope` is an observation,
   and `unauthorized-built-scope` routes to subtraction unless a human approves
   and re-freezes. Findings carry an id (`PC-<n>`), evidence, consequence,
   disposition, and route.
9. **Break the ratchet before send-back.** Compare each proposed repair with
   the original frozen contract. A new table, queue, state machine, service,
   dependency, compatibility path, mode, operational surface, harness, test
   category, caller family, or cleanup area requires an existing authority
   anchor. This is a judgment check, not a numeric threshold. Repeated reviewer
   agreement does not create that anchor.

A clean audit is allowed — but only after the likely ways this slice could be
lying have actually been checked, and the acceptance record says which ones
(see Acceptance below). "Nothing jumped out" is not a verdict.

## Send-Back

Batch all factually accepted findings dispositioned `authorized` or
`frozen-convergence-required`, plus required subtraction for
`unauthorized-built-scope`, into **one** resume prompt to the exact same child
or external session (shape in `worker-prompt-contract.md`). Repair directions are
advisory hints — the worker owns implementation judgment; conductor diagnosis
is context, not a script. The original slice contract stays binding and is
restated by reference, not re-pasted.

**Worker rebuttals do not close findings.** When a send-back response disputes
a finding, the conductor verifies the worker's cited evidence directly in the
repo before changing the finding's status. "The worker disagreed and its
explanation sounded reasonable" is the trust failure this skill exists to
prevent; a finding moves to `rejected` only on conductor-verified evidence.

**Repairs are re-audited from scratch.** A send-back round gets the same
full audit posture as the original return — repair diffs regress adjacent
behavior, quietly weaken tests, or fix the symptom while leaving the named
root cause; do not diff-of-diff skim the repair against the findings list.

Never edit plan scope to make a finding send-back eligible. If a review is the
first agent to find an adjacent same-contract path, it may prevent acceptance,
but it cannot append a late initial-convergence entry. Ask the human or require
redesign/subtraction inside the frozen boundary.

## Caps And Worker Health

- **3 send-backs** per worker handle, then **1 new clean respawn** with a sharpened
  brief (fold what the failures taught into the new slice contract), then
  mark the slice `escalated`. Total worker attempts per slice never exceed 5.
- **Repeated-identical-finding rule:** the same finding surviving two
  consecutive send-backs marks the worker unhealthy immediately — skip the
  remaining send-back budget and respawn or escalate. Identical repeated
  failure without new evidence is the classic no-memory retry smell.
- **Claim-mismatch rule:** a worker caught misreporting repo reality (changed
  files, deletes, verification) gets one strike recorded against session
  health; a second misreport from the same worker forces respawn or
  escalation regardless of remaining send-back budget.
- **Process-failure rule:** two consecutive malformed or failed child runs on
  one slice (non-zero exit, empty final, missing footer, unrecoverable
  child/session handle) escalate the slice. Preserve available receipts and
  external run directories; never silently
  switch runtime, model, or effort.
- A worker reporting `SESSION HEALTH: struggling` or `stuck` weighs toward
  respawn even before caps fire.

## Acceptance

A slice is `accepted` only when:

- every contract claim was traced to current code truth or loaded-artifact
  truth (not to the worker's report),
- every claimed work-product artifact was personally loaded and its substance
  verified against the claim — or, only for an artifact class the conductor
  cannot render, a clean fleet worker inspected it and returned extracted
  evidence that is recorded,
- every analytical conclusion the acceptance relies on was verified at its
  anchors, not adopted from confident prose,
- decisive proof was independently reproduced,
- zero accepted findings remain open, and
- no unauthorized built scope, open human scope decision, or scope-cycle
  finding remains, and
- the log's evidence entry records the refutation attempt: which lens groups
  and lying-modes were checked and what was traced, in one or two lines —
  enough that a later reader can distinguish "audited" from "skimmed".

Record the evidence anchors in the log and commit a local checkpoint.

## Phase Closure

When a phase's slices are all accepted, delegate the phase's plan-required
verification — impact-aware: the plan's named obligations plus changed and
plausibly impacted surfaces, not "run everything." Reuse fresh passing proof
until a real invalidator (new changes touching it, an explicit plan demand,
or review evidence) makes it stale. Record results in the proof ledger, then
record completion in the plan's own format.

## Final Gate

After all phases:

1. **Whole-plan audit sweep by the conductor** against the plan's definition
   of done — hunting specifically what per-slice audits miss: cross-slice
   integration seams, orphaned cruft between slices, requirements no slice
   ended up owning, and accidental architecture that accreted across slices.
   The sweep also personally loads the plan's end-state work products — the
   final deliverable artifacts and whatever the North Star says an observer
   would check — because per-slice audits only ever saw per-slice artifacts.
   This load is part of the non-togglable sweep; disabling the cold verifier
   never disables it.
   Reconstruct the initial human scope, frozen closure, approval history, wave
   findings, plan annotations, and final diff. Any expansion that became
   "required" only through worker/reviewer cycles is a hard fail and normally
   subtraction work.
2. **Cynical review instruments — fleet-executed.** When the cynical review
   skills are installed, dispatch each selected instrument as its own new
   clean external fleet session that invokes the installed skill itself
   against the repo: `$cynical-code-review` over the full change set against
   the plan's completion claims; `$cynical-architecture-review` when the
   plan changed structure, ownership, or boundaries; `$cynical-cruft-removal`
   when the plan carried delete lists or replaced paths. Default to running
   `$cynical-code-review` for any non-trivial plan; add the other two by
   judgment from what the plan changed. Never run these reviews through
   native subagents: they bill the parent's expensive model, and bulk review
   reading is exactly the spend the fleet exists to absorb — a fleet
   reviewer's own slices run on the fleet host's cheap model. The reviews
   stay review-only; the conductor never edits source on their behalf and
   triages their returned findings as claims under the normal audit
   machinery. Give each instrument the plan path, human baseline anchors,
   explicit human approval entries, frozen initial closure, and freeze
   anchor. Its findings use the same scope dispositions and cannot expand
   repair scope. When the review skills or the external runtime are
   unavailable, apply the lens groups from this reference in the conductor's
   own sweep instead.
3. **Cold verifier** (default on): one new clean child with no conductor
   narrative, prompted to *refute* completion — trust only command output,
   code reality, and work products it loads itself; list every plan promise
   not literally true in code or in the artifacts. Its ignorance of the run
   is the feature; it catches what the conductor's accumulated context has
   normalized.
   Give it the same scope anchors. Run it as a clean external fleet one-shot
   by default — a whole-plan cold read is bulk reading, and native subagents
   bill the parent's expensive model. Use a native clean child only on
   explicit user request or when no external runtime exists. It may reject
   completion, but it may not add a newly discovered adjacent path to the
   frozen closure.
4. Triage all instrument findings like any others; repair through send-backs
   (resuming the owning sessions where healthy); re-run the affected
   instrument on material repairs.

## Escalation

Escalation is a first-class outcome. An escalated slice stops only its own
dependency chain. The escalation report names each escalated slice, its
finding and attempt history, and the specific decision the user must make.
Never lower the audit bar to avoid escalating.
