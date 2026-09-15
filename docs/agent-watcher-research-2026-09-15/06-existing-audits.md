# Existing scope-creep and overbuild audits

Research slice 06 for the Agent Watcher. Everything here was already written by
Amir's agents. No new audit was run. Each document was read read-only; findings
are transcribed, not re-derived.

Four clusters dominate. Two are in **psagentspace / psmobile**: the **M1 Skills
epic (#5605)** and the **Home routing epic (#4895 / #5641 / #5653 / PR #5642)**,
both September 2026. Two more are in **agentspace / cratejoy**: the **inclusive
marketplace pricing epic (#16151)**, audited four separate times between
2026-09-03 and 2026-09-14, and the **CircleCI cost-reduction epic (#16198)**.
Three older documents (telemetry overbuild, puzzle Finish recovery stack, the
mined correction casebook) supply the long-run pattern evidence, and one
2026-08-20 review of psmobile issue #4126 supplies the cleanest recorded case of
a review loop generating its own scope.

The single most valuable prior artifact is
`skills/startup-pragmatism/references/correction-casebook.md`: an existing mined
catalog of **141 overbuild corrections across 83 sessions** (6,858 prompts,
2026-08-05 to 2026-08-23), already organized into **eight named anti-patterns**
with verbatim trigger quotes. The watcher should treat that file as its detector
prior, not rebuild it.

---

## 1. Inventory

| # | Document | Date | Author model | Subject audited | Findings | Cut status |
|---|---|---|---|---|---:|---|
| A1 | `psagentspace/plans/drafts/2026-09-11-skills-m1-mock-scope/audits/FABLE_AUDIT.md` | 2026-09-12 | Claude Fable 5.1 (independent) | Installed M1 build vs. Figma mocks (PR #5643/#5644) | 13 functional + 9 visual + 15 uncertainties | **Cut done.** #5643/#5644 closed "Superseded" 2026-09-12 |
| A2 | `…/2026-09-11-skills-m1-mock-scope/audits/SOL_AUDIT.md` | 2026-09-12 | GPT (Sol), independent | Same build vs. same mocks (second opinion) | 3 visual severity rows + reuse verdicts | Same closure |
| A3 | `…/remediation/FABLE_REMEDIATION_REVIEW_2026-09-12.md` | 2026-09-12 | Claude Fable 5.1 xhigh, fresh context | The M1 **remediation plan** and its 9 published issues | 5 headline + 9 defect sections + 6 wrong-feature risks + 22-row keep/delete/replace + 12 ranked edits | **Mostly applied** (see §4) |
| A4 | `…/remediation/pragmatism/CODE_SCOPE_EVIDENCE.md` | 2026-09-12 | Codex parent (startup-pragmatism pass) | M1 backend issues #5666/#5614/#5610 | 14 explicit cuts in 3 cut lists | **Applied**; issue bodies rewritten, `*-before.json` snapshots retained |
| A5 | `…/remediation/FABLE_M1_SCOPE_IMPLEMENTATION_AUDIT_2026-09-13.md` | 2026-09-13 | Claude Fable 5.1 (AI Manager, independent, rev 2) | M1 Result→Analysis implementation vs. Amir's verbatim requests | 13 (F1–F13) + 13 accepted behaviors | **Partly applied** — F1/F2 fold landed (see §4) |
| A6 | `…/remediation/FABLE_M1_TESTING_AUDIT.md` | 2026-09-14 | Claude Fable 5.1 xhigh (AI Manager pro5) | M1 test/automation surface | 12 (F1–F12) + explicit "cut list (do not build)" | Test plan issue drafted; cut list authored |
| A7 | `…/remediation/M1_REQUIREMENTS_AUDIT.md` | 2026-09-15 | 302 fresh GPT-5.6 **Sol xhigh** reviewers, one per row | All 302 M1 requirement rows vs. PR #5825 stack | 19 distinct (33 records across 29 rows) | Findings published to sheet; no fixes made by design |
| A8 | `…/remediation/M1_REQUIREMENTS_REGISTER.md` + Sheet `1VPT7C…` tab "M1 requirements · AUDIT" | 2026-09-14/15 | Codex parent + Sol xhigh reviewers | 307-row register from 108 human messages across 4 Codex sessions | 307 rows, 2,149→2,114 assessment cells | Register is the intent ledger; **no pedantic section** (see §6) |
| B1 | `psagentspace/audits/2026-09-12-home-heuristic-fable-review/FABLE_XHIGH_REVIEW.md` | 2026-09-12 | Claude Fable 5.1 xhigh (AIMgr fresh-consult) | Home heuristic refresh, PR #5642 @ `76a4c7dfe4f` | 4 confirmed defects + 5 risks | Verdict **fail**; branch reworked |
| B2 | `…/2026-09-12-home-heuristic-fable-review/FABLE_XHIGH_IMPLEMENTATION_REVIEW.md` | 2026-09-12 | Claude Fable 5.1 xhigh | Same PR + uncommitted merge | reproduced defects + decisions needed + coverage gaps | Fed the repair draft |
| B3 | `psagentspace/audits/2026-09-12-home-instant-live-refresh/FABLE_PLAN_REVIEW.md` | 2026-09-12 | Same Fable reviewer | Pro's **first repair draft** vs. source | corrections + findings on the repair plan + missing causal coverage | Draft revised |
| B4 | `…/2026-09-12-home-instant-live-refresh/FABLE_XHIGH_REVIEW_2026-09-13.md` | 2026-09-13 | Claude Fable 5.1 xhigh | PR #5642 @ `6b41adf4e6` | 6 blocking (B1–B6) + 7 non-blocking | Verdict **not mergeable** |
| B5 | `…/2026-09-12-home-instant-live-refresh/FABLE_XHIGH_FINAL_AUDIT_2026-09-13.md` | 2026-09-13 | Claude Fable 5.1 xhigh | Home epic end-to-end @ `17d64d7b60` | **11 overbuild (O1–O11) + 7 split-brain (S1–S7) + 8 missed-point + 11 failure paths + 15 ranked (F1–F15)** | Explicit "remove entirely" list; **PR #5642 still open, unmerged** |
| B6 | `…/2026-09-12-home-instant-live-refresh/FABLE_FINAL_REVIEW_2026-09-13.md` | 2026-09-13 | Claude Fable 5.1 | Home source audit @ `d88637ea3f` | 12 requirement rows, 6 fail/partial | Priority order issued |
| B7 | `…/2026-09-12-home-instant-live-refresh/PRO_PRAGMATIC_REASSESSMENT_PROPOSAL.md` | 2026-09-12 | GPT-6 Pro (PS Architecture) | Home architecture, reassessment | ~6 rejects + 2 explicit decisions Amir must make | Advisory; explicitly "not adopted requirements" |
| B8 | `…/2026-09-12-home-instant-live-refresh/UNUSED_STATE_SUBTRACTION_VERIFICATION.md` | 2026-09-13 | Codex parent | 472-line subtraction delta | 18 focused cases, 0 introduced diagnostics | **Cut executed and verified** |
| C1 | `psagentspace/_artifacts/2026-08-13-telemetry-overbuild-review/report.md` | 2026-08-13 | Codex + panel (1,581 lines) | Whole telemetry subsystem, Apr–Aug history | 9 self-inflicted mechanisms + 9 recurring examples + 6 degradation causes + 4 accumulation stages | Target architecture proposed; "what exists after the cut" |
| C2 | `psagentspace/research/2026-09-06-puzzle-stack-fable-review/STACK_REVIEW.md` | 2026-09-06 | Claude Fable 5.1 XHI | PRs #4737 + #5140 Puzzle Finish recovery | 14 (F1–F14), classified by evidence class | No blockers; 2 product decisions to record |
| C3 | `arch_skill/skills/startup-pragmatism/references/correction-casebook.md` | ~2026-08-24 | Mining agent over Codex history | 141 overbuild corrections, 83 sessions, 6,858 prompts | 8 anti-patterns + 4 meta-patterns + correction vocabulary | Shipped as a live skill |
| C4 | `psagentspace/_artifacts/2026-09-14-missions-v12-requirements-audit/` (49 row reports + README) | 2026-09-14 | 2 Astra xhigh + 46 Sol xhigh, one row per fresh agent | Missions V1.2 (PRs #5701/#5813) | 42 code gaps + 46 test gaps across 48 rows | 7 new issues + 4 amendments filed under epic #5694 |
| C5 | Sheets `1QqvZ…`, `1SFte…`, `1VPT7…`, `1-YXN…` | 2026-09-12→15 | Codex parents + Sol/Astra reviewers | Missions V1.2, PVP SNG, M1 Skills, Inclusive Pricing | 59 / 120 / 308 / 119 rows | Only Missions has a real P4 "Pedantic / non-blocking" section |
| D1 | `agentspace/plans/retros/2026-09-03-epic-16151-intent-audit.md` | 2026-09-03/04 | **GPT-5.6 Pro** (Cratejoy Architecture project) | Pricing epic #16151, all 18 open PRs at exact heads | 6 named + 18 PR dispositions (5 merge-ready / 5 with fixes / **8 do-not-merge**) | First cut recommendations; superseded by D3 |
| D2 | `agentspace/plans/drafts/2026-09-13-fable-scope-review/FABLE-SCOPE-REVIEW.md` | 2026-09-13 | AI Manager **Fable** (cold-reader) | Same epic, independent cold read | 3 expansion directions + blast-radius quantification + a 7-point stop rule | Converged with D3 |
| D3 | `agentspace/plans/drafts/2026-09-13-epic-16151-scope-creep-review.md` | 2026-09-13 | `/root` reviewer + second reviewer **"AI manager Fable, GPT-6 Astra, extra-high"** | Pricing epic #16151 vs. its original body | **7 expansion areas + 3 must-fix blockers + a 14-row keep/cut classification + a 7-point completion cut line** | **Verdict: "scope creep confirmed."** Cut adopted in D5 |
| D4 | `agentspace/plans/drafts/2026-09-13-pro-rescope-review/PRO-RESCOPE-REVIEW.md` and `…/2026-09-13-fable-rescope-review/FABLE-RESCOPE-REVIEW.md` | 2026-09-13 | GPT Pro; **Claude Fable 5.1 xhigh** (run `fable-rescope-20260913T130613Z-gh4ifqhb`) | How to re-scope #16151 | Two independent rescope proposals | Reconciled in D5 |
| D5 | `agentspace/plans/drafts/2026-09-13-agreed-rescope/RESCOPE-DECISION.md` | 2026-09-13 | Codex parent, reconciling D4 | The decision | — | **Cut executed:** epic split into E1 (5 units) / E2 deferred / E3 parked; "broad runtime/certification program" stopped |
| D6 | `agentspace/plans/drafts/2026-09-14-inclusive-requirements-register/` (`pro-pragmatic-scope-cut-review-2026-09-14.md`, `issue-16155-fresh-sol-audit.md`) | 2026-09-14 | GPT Pro; **Sol** (fresh, independent) | Post-cut re-audit | 18 issues → 9 (11 duplicates closed); 104 requirements ranked P0–P3 | **Cut verified held:** "no new registry, approval hash, QA platform, E2/E3 branch, or CircleCI overhaul" |
| E1 | `agentspace/docs/audits/circleci-2026-09-12/implementation/FABLE-X-END-TO-END-AUDIT-20260914.md` | 2026-09-14 | **Fable X (Claude Fable 5.1 via AIMgr)**, independent, findings-first | CircleCI cost-reduction epic #16198, 4 core PRs + 1 private repo PR | **14 (F1–F14)** + a 4-bucket final disposition | Repair sequence issued; "Do not adopt, activate, or fund anything on the current evidence" |
| F1 | `psmobile-worktrees/4126-review-governance-20260819/plans/drafts/2026-08-20-app-review-scope-recovery-plan.md` | 2026-08-20 | Clean external **Claude Fable 5 xhigh** (session `4d03fa6a…`) | psmobile issue #4126 review-continuity implementation | **4 overbuild findings + a 20-row scope ledger** (keep / delete / simplify / freeze) | Draft for Amir's decision; explicitly "does not authorize any edit… or scope expansion" |

**Totals: 29 inventory rows covering 30 Markdown audit documents and 4 requirement
workbooks** (some rows pair two companion documents; the M1 workbook appears in
both A8 and C5). **Roughly 260 discrete overbuild / drift / split-brain /
missed-the-point findings**, plus the 88 requirement-row gaps in C4 and the 141
historical corrections already mined in C3.

---

## 2. Cluster A — M1 Skills epic (#5605)

### The original ask, as the audits restate it

From `remediation/fable-implementation-audit/USER_REQUIREMENTS.md` (the verbatim
user-message ledger the auditors were pointed at):

> "ramp up on M1 epic #5605: Skills on one completed puzzle result… review my
> mocks using figma MCP… Looking at those mocks, what features are implied here?"

> "No hold on. Why do we need a loading state? Why do we need a retry state? No
> you're building in all sorts of shit that I don't fucking want. **It just pops
> in and it's loaded** and there's no error state, and there's no unavailable
> state, and there's no retry state, and there's no loading state."

> "I'm just looking at what I see on screen and it does not match our Figma
> mocks. **Did you build it off of our Figma mocks or did you find some old
> images and use them?**"

> "we built the wrong thing… **I don't want the wrong code in my codebase**…
> so that the next time you tell me you're done, I look at it and **I recognize
> the feature that I gave you in the first place**."

> "figure out where we're overbuilding relative to what I asked for, because I
> know it's there. **I know we're building some crazy shit that I didn't ask
> for.** The product features are locked."

And the audit-commissioning prompt itself (A5's charter):

> "overbuilt unnecessary machinery based off of hypotheticals / introduced split
> brain and multiple sources of truth / sort of missed the point / didn't
> holistically accomplish what I'm after / built something that's going to
> create weird fallback states and new errors that are user-facing / did
> something that's going to create new loader states that don't need to exist"

### A1 — Fable: installed build vs. Figma mocks (2026-09-12)

**Verdict: the build answers a different question than the mocks.** "The app
presents… this attempt's grade where the mocks present historical
optimal-decision progress, answer distributions, and a separate Puzzle Analysis
page."

Missed-the-point findings (root cause given in brackets):

- F1 The whole 8-frame **Puzzle Analysis screen does not exist** — no route, no widget, no chart, none of the drawn strings. [never attempted; plan self-scoped away from the mocks]
- F2 No "Analysis" CTA or handler anywhere in `features/puzzles`. [same]
- F3 Result row shows **this attempt's grade**, mocks show the user's **cumulative parent-skill rate with a trend** — "different quantity, not a styling gap". Backend service comment says no history *by design*. [agent inferred the feature from the code that existed, not from the mock]
- F4 Sub-skills render as a per-puzzle list of 13 classifier situations instead of 4 named child rows with % or unlock thresholds. [taxonomy taken from the classifier's shape, not the design]
- F5 **No peer data at all** — no proto field, no query. [never attempted]
- F6 No optimal-over-time chart, no history endpoint, no chart primitive. [never attempted]
- F7 Headline "N% OPTIMAL / N of M decisions / comparison line" absent (depends on F3). [same]
- F8 "Optimal Move" explanation shown untruncated on the result screen instead of two lines + "Read more" in Analysis. [pre-existing slot reused unchanged]
- F9 On `NotFound` or any transport error the client **silently omits the Skills card and the screen looks normal** — an undesigned silent-omission state that hides exactly the breakage the product rule wants surfaced. [defensive catch-and-log added by the agent; the backend side is loud, the client swallows it]
- F10 The onboarding outro **is** a designed frame; the build excludes onboarding deliberately at **four layers** (locator, view-model gate, call sites, auth-only backend actor gate). [four independent hedges accreted around one unconfirmed assumption]
- F11 Card is inserted into the scroll region after settlement — an unobserved shift risk against "it just pops in and it's loaded".
- F12 Model carries `usedHint`, `usedHelp`, `practiceRepeat`, `assessedRelevance`, `amountAssessment`, `definition`; the mocks show none of them and `definition` is never rendered. [speculative data surface]
- F13 First-day result row is a genuine gap in the design set (not a build defect).

**Recommended cut / reuse split:** keep backend auth/ownership/settlement plumbing, the classifier as a taxonomy source, the Flutter transport, and the lifecycle guards. **Replace the body of `puzzle_outro_skills_card.dart`.** Everything else the mocks ask for was never started, so it is new work, not rework.

**Cut evidence:** issues **#5643 and #5644 were closed "Superseded" on 2026-09-12T15:11Z**; A3 later confirms `git grep` on main finds no surviving `THIS PUZZLE · SKILLS`, `GetPuzzleSkillResult` or `PuzzleOutroSkillsCard`.

### A2 — Sol: same comparison, independent

Same verdict, different phrasing: "The principal mismatch is **semantic as well
as visual**." Starting over justified for the reporting/presentation layer only;
not for settlement, classification, transport, stars, XP/time, path progress, or
navigation. Three severity rows: Critical (concept mismatch — a tall
"THIS PUZZLE · SKILLS" card vs. a one-row historical summary), High (header
context and star artwork differ), High (explanation placement pushes Skills
below the fixed action stack).

### A3 — Fable: review of the remediation plan itself (2026-09-12)

**Verdict: "Not ready to execute as published."** The key sentence, and the most
transferable one in the whole corpus:

> "The problems are in the machinery the plan prescribes underneath those
> screens. **Several pieces are shaped by code that exists on unmerged branches
> rather than by what the thirteen frames need.**"

Findings, with the audit's own stated trigger:

- 3.1 The classifier the whole backend depends on **is not on main**; the plan declares the dependency without naming the PR, without saying main has none of the files, without saying the catalog is committed nowhere, and with no landing scope. Consequence named: "the path of least resistance is to stack the M1 backend branch on #5470's branch, **the same stacking that left #5643 depending on an unrelated warehouse and Play-vs-AI campaign for its CI**." [under-specified dependency → stacking drift]
- 3.2 "Reuse PR #5285" is **architecture shaped by existing code**. Warehouse evidence: pooling costs two columns, content-apply changes and a per-revision compatibility declaration **to add at most 87 votes across 14 puzzles**. The screens need one short query. [reuse instruction read as "adopt this PR wholesale"]
- 3.3 The sidecar, display-registry versioning and seed manifest are **"inherited ceremony"** from a superseded reviewed-metadata design; the `reviewed_metadata JSONB` field encodes "Directly assessed", **a label no frame shows**. [dead concept carried forward because the draft code existed]
- 3.4 The Preflop registry was called blocked; it is composable. The audit **withdraws its own first-draft claim**. [reviewer drift, self-corrected]
- 3.5 Onboarding adoption **is already implemented**; the issue says the implementation "was not certified" and asks the child to "trace and test the actual owner before extending it". "Nothing needs extending… the 'exactly once' property is already the ledger's primary key." [uncertified-therefore-rebuild]
- 3.6 Issue #5665 "Remove and reconcile" **deletes code that main does not contain**; its "before/after grep showing no reachable old widget" is a grep of main that already passes. What is actually lying around is two branches, two worktrees, an uncommitted draft and a stale plan document, none of which the issue mentions. [ceremony aimed at an already-solved problem]
- 3.7 The plan invokes **"the existing transport's bounded recovery"** which does not exist (the only recovery on main is one token refresh) and a **prefetch nobody needs** with a self-acknowledged risk of exposing a graded report before settlement. "Implementers will either write a retry the plan claims already exists, or ship the old catch-and-log branch under a new name… **it just should not be dressed up as reuse.**" [invented reuse claim]
- 3.8 #5614 and #5270 **have no surface of their own**; both land in the same Go service and the same RPC as #5610. The split follows inherited issue numbers, not a code boundary.
- 3.9 Five issues enumerate largely the same test cases and add cases for machinery this review recommends cutting — "that duplication is what reads as a validation program."

**Also flagged as "could still produce a wrong feature":** unsourced glossy star artwork; the arrow rule that two implementers would build two different ways; adjacent cards on one screen carrying different time windows with no label; a gap caption that can be literally false; a custom chart painter treated as an afterthought.

**Cut list (22-row keep/delete/replace inventory).** Delete/do-not-take: #5285 compat-group columns, choice maps, apply.go changes, legacy coverage classes, terminal summaries, dbt analysis, ingest changes; #5470 dbt models, raw artifact writers, Play-vs-AI inputs, campaign wiring; the reviewed-metadata sidecar migration and service and stage script; PuzzleDB #85 as a dependency; the `GetPuzzleSkillResult` RPC/proto/handler/service/tests; `PuzzleOutroSkillsCard` and its plumbing; `SKILLS_CATALOG_PATH` startup requirement (replace with `go:embed`); the two closed-PR worktrees; duplicate evidence PNGs. Explicitly: "What this omits compared with the plan: compat groups and choice maps, normalized choice tables, PuzzleDB inventory joins, registry versioning in the database, version-bundle rejection, coverage-evidence fields, prefetch, warehouse reconciliation gates, and the #5285/#5470 overlap reconciliation. **None of those changes a pixel on any of the thirteen frames.**"

**Cut evidence:** #5665 is now titled *"Land the canonical classifier and retain exact cleanup ownership"* (recommendation 6 applied); #5666 is *"Derive narrow revision facts through the existing content owner"* (recommendation 3 applied); #5610 is *"Return and publish one complete Result with immediate local Analysis"*. **Not applied:** recommendation 12 — #5614 and #5270 are still separate open issues.

### A4 — startup-pragmatism cut pass on the M1 backend (2026-09-12)

This document is the clearest statement of the mechanism, because it names the
anti-patterns explicitly:

> "That extra work applies startup-pragmatism **anti-patterns 1, 2, 3, and 6**:
> default architecture expansion, verification machinery, scope contagion from
> one report into all content admission, and protection against unobserved
> lifecycle hazards."

What the plan was about to build: "certify the global readiness of every
finished, open, and admitted revision; investigate historical retention
completeness; persist several independently named derivation versions and source
identities; and build a route recovery controller driven by transport
reachability, app resume, account transitions, pending destinations, and
coalescing."

Cut list (14 items across three issues):

*From #5666* — (1) do not copy payload hash / catalog source revision / catalog hash / canonical / mapping / classifier / native versions / `classified_at` into the serving table; (2) do not model all 98 classifier candidates, typed facts, evidence anchors, source locators or coordinates in the M1 table; (3) do not build a required-universe scanner over all finished attempts, open encounters, current items, surfaces, onboarding selections, direct entry and replay entry; (4) do not add a second Open-time readiness check; (5) do not turn the backfill into a check/apply campaign runner with failure censuses and coverage certification; (6) do not investigate or encode a universal historical capture boundary.

*From #5614* — (7) do not give each bucket a separately researched coverage/capture state; (8) do not add a coverage registry, exclusion table, waiver path, source-bound configuration or legacy-history reconciliation ("**None is currently proposed by name, but the requested capture-bound investigation and 'fully covered' conditions invite exactly that machinery**"); (9) do not repeat all reducer cases in report-service, wire-adapter and screenshot tests.

*From #5610* — (10) no transport-state or app-lifecycle subscriptions on the result route; no auto-refetch on reconnect, reachability, resume, signup/adoption, logout or account change; (11) no report lifecycle state machine, retry coordinator, pending-destination store, readiness object or retirement matrix; (12) no actor scope / payload hash / classifier identities / provenance bundle in the response; (13) **do not revalidate the same grade, counts, puzzle/revision/hash tuple and child/peer relationships in SQL, the Go service, protobuf mapping, the Flutter adapter and the widget**; (14) no separate peer transformation layer.

Explicit guard against over-cutting: "The formulas themselves stay" — all 24 named metric rules preserved.

**Cut evidence:** `issue-5270-before.json` … `issue-5668-before.json` snapshots retained alongside the rewritten bodies.

### A5 — Fable: M1 implementation vs. the requests (2026-09-13)

**Holistic verdict:** "The team built the product Amir drew… The one place the
implementation still departs from Amir's stated experience is the seam between
Finish and the report."

The audit's own requirements-to-delivery table answers Amir's two questions
directly:

| Amir's question | Audit's answer |
|---|---|
| "Where did we overbuild on hypotheticals?" | F5, F7, F9 — "The subtraction pass removed the large certification machinery. **What remains is small**: a deferral branch with no traced path, defensive self-validation, unused wire echoes." |
| "Split brain / multiple sources of truth?" | F4, F8 — "A second reader of the device zone that ignores the QA override; three access paths to one report response; two copies of the onboarding caller." |

Findings:

- **F1 (High, present behavior).** The Result renders **twice**; the second render moves title (44px), answer cards (50px) and XP/time tiles (62px) upward on four-answer and small-viewport Results. Requirement violated: "It just pops in and it's loaded." Repair is one guard removal — unconditional, independent of the transport decision. [layout reclaim made conditional on late-arriving data]
- **F2 (High, plan drift, unresolved).** The report is a second round trip whose only production caller is the moment after Finish. Root cause stated exactly: *"The plan's 'Reporting stays outside Finish and cannot settle, award or adopt' is about writes and is right. **It was extended to** 'the already-settled Result remains usable while its complete progress row arrives,' **which accepts the two-phase render that Amir's wording does not.**"* [a correct narrow rule silently widened into a product concession]
- **F3 (Med-High).** Analysis taps during the read are honored late with no cue, and silently on persistent failure. The codebase already records the opposite lesson for this exact control: "a silent refusal on an enabled-looking control was a rage-click source (#3105)."
- **F4 (Low, split brain).** A second reader of the device time zone on a new platform channel that ignores the existing QA offset override. Repair: carry the IANA zone in the client time context that already exists; delete the per-report method.
- **F5 (Low-Med).** Actor-change deferral branch with **no traced ordinary path** — it and its test exist for an untraced condition.
- **F6 (High as rollout dependency).** Whole-history derivation invariant: one underivable stored revision poisons every report for every user who ever played it. The audit **withdraws its own first-draft remedy** ("a mandated zero-failure gate… is the certification the subtraction plan canceled") and names an unfixable generation window the plan explicitly accepted.
- **F7 (Med, hypothetical overengineering).** Server re-grades the pinned revision and compares five grade fields, then decodes the settlement JSON and compares eight more — **both written in one transaction by Finish**. The client re-derives stars with a **second hard-coded map** that must equal the existing one. "Requirement violated: the plan's 'reuse the existing immutable revision/hash check once … do not validate the same arithmetic in every layer.'" Consequence: "**No happy-path benefit.** Any future divergence produces [a dead button] rather than a visible bug."
- **F8 (Low-Med, duplication).** Three near-identical copies of the caller glue; three access paths to one response, one of them executed on every build.
- **F9 (Low).** Cruft in the production model and wire: `report_cutoff`, `time_zone`, `peers.observed_at`, `children[].key`, discarded `remaining_puzzles`, fixture-only `shareSubject/shareText/asOfUtc/glossaryTerms`, a still-computed `actions.secondary` no Result renders, and an untracked seed script sitting outside any PR.
- **F10 (Med, plan mandate vs. product need).** The optimal-explanation check runs inside fact projection, so "a current-puzzle rendering requirement [is] promoted into a history-wide gate." Plan said "validate… as part of this one projection boundary"; "nothing requires the two to fail together."
- **F11 (accepted with caveat).** The inherited classifier does three native calls and 98 candidate projections per derivation to yield **4 of 98 memberships plus one context value**. "**This survived because it existed**, and the plan said so openly." Kept anyway — cost is once per immutable revision and a thinner entry point would be more machinery, not less.
- **F12.** One fixture case (`M1-D22`) specifies a state the production reducer **cannot emit**; consistent with the plan, but "should not be read as a state the backend can emit."
- **F13.** 8 accepted/intentional behaviors listed explicitly "so they are not re-litigated."

**Recommended architecture (subtractive):** layout independent of report arrival; **one** measured transport decision, "either fold… or keep… **Not both**"; one client time context; decouple the explanation check; trim validation to binding and shape.

**Cut evidence — this one landed.** Sheet `1VPT7C…` row 4 ("One complete Result"), audited at `861ef3a5…`: *"FinishPuzzle returns settlement and the complete report in one response; Flutter validates and maps the full Result, Skill Progress, and Analysis presentation before its only Result publication."* Row 8 ("Locked capability scope"): *"No concrete discrepancy found… Finish is the only report transport, one report is composed and mapped before Result publication, Analysis is local."* The F1/F2 two-phase render was removed by folding the report into Finish.

### A6 — Fable: M1 testing audit (2026-09-14)

Findings F1–F12. The scope-relevant ones:

- **F1 (blocking).** The stack deleted 18 outro test-ID constants **without migrating them**, breaking five Patrol files including the nightly money-suite target; CI cannot see it because `analysis_options.yaml` excludes integration tests and CI analyzes exactly one file. The PR body called them "14 preexisting integration-harness errors"; the base commit still has the constants, so **the stack introduced them**. [deletion without consumer sweep + a self-serving "pre-existing" label]
- F3 The two real-Postgres tests that matter most are env-gated and **never run in CI**.
- F4 Post-commit failure proof is guest-only and single-stage, so "no duplicate grant" is vacuous.
- F8 Every "113/115 golden cases" claim across the PR bodies is local-only, and a real mismatch artifact sits in the working tree contradicting the worklog's "running without updates".
- F9 Connected native evidence **predates the one-stage repair**.
- F11 "Weak or tautological assertions worth trimming" — `reportRequests == 1` is recorded inside the double's own `finish()`; a link assertion tests a getter that builds exactly that string; an isolation test asserts absence of a string the screen never renders; spoiler checks assert absence of words the input never contained. [proof-shaped tests that prove nothing]
- F12 A 1,741-line non-test source file against a 1,000-line repo rule; a Go test reading a Flutter source file by relative path; a function with no callers.

**Explicit "Cut list (do not build)":** a per-caller Patrol matrix, Android duplication of the journey, a 37-case native recapture, a report-value QA snapshot command, screenshot checksum manifests, a timing benchmark platform, process-kill or offline Finish device tests, "**and any loader, retry, or error UI to make fault tests observable**."

### A7 / A8 — the 302-row requirements audit and register

302 rows, one fresh Sol xhigh reviewer each, 4 at a time. Result: **272 satisfied, 29 rows carrying 33 finding records, reduced to 19 distinct findings**, 1 unresolved wording question. Named drift findings include: a puzzle-ID-only destination map that loses placement identity (M1-028/029); the client **replacing a missing server percentage with its own label calculation** and **discarding the supplied remaining-puzzle count to recalculate it** (M1-072/073/074 — client re-deriving what the server already sent); Patrol journeys using prohibited global settle waits; Settings still targeting a non-rendered legacy Result action; a recorded transition captured with animations disabled.

Two process observations worth keeping for the watcher:

- **"Orchestration correction: the M1-061 reviewer briefly launched an unauthorized extra Astra child."** The parent killed the owned process tree and resumed the original session. Sub-agent scope creep, caught and logged.
- **"Some earlier reviewers nevertheless read neighboring output files as formatting examples, so repeated findings are not claimed as blind independent corroboration."** And M1-085 was held unpublished "because its report **repeated an unsupported neighboring test-gap claim**." Contamination between supposedly independent reviewers is a real, observed failure.

---

## 3. Cluster B — Home routing epic (#4895 / #5641 / #5653 / PR #5642)

### The original ask, as the audits restate it

From the audit's extracted requirement table (B5 §2), 13 requirements. The
load-bearing ones:

- R2 "Home is complete and current on its first exposed frame; **no loader, skeleton, blank frame, stale-then-replace, artwork pop-in or flicker**"
- R3 "Home preparation adds **no user-facing workflow** (no pending/failure notices, disabled controls, navigation holds, Home-specific Retry)"
- R4 "Failed required sources are **real errors** with original cause, stack, attribution and Sentry visibility; **never normalized**"
- R8 "**No hidden fallbacks or silent healthy defaults**"
- R9 "**One source of truth**; reuse existing clean patterns; **no split brain**"

### B1/B2 — the first Fable pass (2026-09-12): verdict **fail**

Four confirmed defects, each with a stated mechanism:

1. **Critical.** The coordinator's refresh and the startup preload are **auto-disposed one event-loop turn after they start**, so the cache is never written in production. "The feature is a **silent no-op with zero Sentry signal**" because the failure is logged at `warn`, which the sink turns into a breadcrumb. The existing dedupe test cannot see it "because it overrides the RPC body and never yields to the event loop."
2. **Critical.** Warm adoption requires entry-reason equality, so every return from Lesson, Puzzle, Play or another tab **can never adopt the refreshed plan** — the exact scenario the issue was opened to remove. "**The untouched test… asserts `HomeTestIds.loading` on return, so the suite currently pins the flicker.**"
3. **High.** No completion handoffs exist, and the only trigger fires **before** the action, so "the user sees the action they just finished as Next Up."
4. **High.** "The no-flicker and latest-plan claims are **asserted, not evidenced**, and the PR is not green." The refresh slice **reuses the fail-loud screenshot as its visual witness**; no frame sequence exists.

Risks: a provider refresh and network request started from `build()`; a dead `_generation` field that is only logged, never compared; `catchError` and `on ProviderCancelledError {}` that "swallow every outcome, which is why defect 1 is invisible in production"; stale retention up to one hour with no cue and no consumer for `cacheState`; **three coexisting refresh owners**, one of them dead but still in test fakes.

### B5 — Fable X-high final audit (2026-09-13): the fullest overbuild taxonomy in the corpus

**Verdict: "needs repair. Not mergeable."** With the fair framing preserved:
"None of this makes the work mis-scoped; **it makes it unfinished and heavier
than needed.**"

**Overbuild audit (O1–O11), each with "why unnecessary":**

- O1 Flag **configuration candidate staging** — a whole parallel presentation path with staged snapshot, activate/discard/ensure/has methods and its own test. "It exists to avoid a frame where flags changed but Home was not re-evaluated. **Evaluation is now synchronous and local, so re-evaluating inside the same turn has no frame gap.**" [machinery that survived the architecture change that obsoleted it]
- O2 An **11.7 MB Wasm module bundled as a release asset** whose only reader is the debug playground. "11.7 MB added to every release build with zero production use."
- O3 A **second recovery future with its own error logging** on top of a dedupe that already exists — "a second `catchError` that logs an already-captured exception (duplicate Sentry), and an `// ignore: disallow_silent_catch` the linter still flags."
- O4 **Three overlapping failure-dedupe checks** — "Three ways to say 'same failure.' Keep the fingerprint check only."
- O5 **Three fields describing one failure state**, which BootGate then has to reconcile and `coversRequiredState` checks four of.
- O6 A **dead test-only production API** whose only caller is one test.
- O7 **Legacy Dart fact types** including `.unavailable()` / `.excluded()` constructors with **zero callers** — "the 'unavailable' constructor is the vocabulary #5641 removed."
- O8 **Legacy telemetry producers** with only test callers.
- O9 **Dead telemetry fields** that always send `Duration.zero` and `0`, plus revision fields whose meaning silently changed.
- O10 A **never-completing prerequisite future** used to mean "not applicable" — "a hang-shaped signal."
- O11 **Stale coverage documentation** still specifying the `failure`/`retryFailure` phases and Retry controls the work removed.

Explicitly **not** overbuild (guard against over-cutting): the retained-vs-canonical dual plan, exposure history, entry-reason attribution, the module trial-and-swap, Mission/Streak paired acceptance.

**Split-brain audit (S1–S7):**

- S1 Puzzle display state has **two producers**, and Puzzle hydration **awaits Home's preload future and rethrows Home's error as a Puzzle error** — "A Home failure can break the Puzzles tab."
- S2 Flag activation has a staged Home presentation separate from `state`.
- S3 **Two byte copies of the same module**, with a verification doc recording repeated SHA parity checks between them. [the parity ceremony is the tell]
- S4 Play facts mirrored client-side, with the monotonic allowance-day rules now living in two places.
- S5 Failure state carried in three places; BootGate consults two error sources.
- S6 **Two acquisition entry points with different failure semantics**, and a third component choosing between them.
- S7 Evaluation-failure diagnostics reported through **two channels** for one underlying failure.

**Missed-point / holistic gaps (8):**

1. **"The failure-time user experience is undefined and currently silent-stale."** The locked requirements forbid both a Home error UI and stale success; the implementation resolved the contradiction by keeping the last plan painted with a loud diagnostic — "a product decision Amir has not made; **the PR body describes it as 'the invalid plan is cleared', which is inaccurate.**"
2. **Cold start became a network-and-compile gate that fails closed.** Every launch re-downloads and eagerly compiles 11.7 MB; any preload failure shows "Startup failed". "Before this PR a returning user with a signed-in session could open the app offline… **no recorded decision, no seed, no persistence and no device timing.**"
3. Device performance and memory **unmeasured**: synchronous Wasm evaluation on the UI isolate inside feature flows, 244 ms median / 449 MB peak on the dev host, 512 MB guest cap, jetsam risk on iOS.
4. The delivery contract for a newly published heuristic is real but **never written down**.
5. **Offline replay does not exercise the production projection layer** — "a new heuristic can pass trace replay while projection is wrong."
6. Trap recovery has **no app-level test** despite the re-review asking for one.
7. A clock-offset race reports a benign superseded read as a source failure.
8. The Puzzles tab's availability now depends on Home (S1).

**User-facing failure audit:** 11 paths enumerated with reachability, including "previous plan stays painted after a failed evaluation; cards remain tappable; **no message**", "every cold launch downloads and eagerly compiles the module", "duplicate Sentry event", and "same-fingerprint failures captured once until success — **flood control that hides recurrence**."

**Final scope recommendation** splits cleanly into *belongs here*, *split out* (5 items, including a proto relocation and unrelated Core test failures that landed in this PR), and **"Remove entirely"** (12 items, matching O1–O11 plus the Puzzle/Home join and the duplicate FlutterError).

### B6 — Home source audit at a later head

Twelve requirement rows; six Fail or Partial. Notable:

- `homeprojection/features.go` **silently ignores errors** from `StableKeyForTarget` in four production-path constructors (`stableKey, _`) and can omit an archive card — "a concrete swallowed-error pattern."
- A first-flight error can be **captured twice**, obscuring event counts and grouping.
- `recordRefreshFinished` and its catalog event exist with **no call site** — "the event contract exists but no refresh terminal event is emitted."
- Every `stateKey` value is `unresolved`; the wire carries no such field, and the modern events cannot report it. "Either remove the unused state-key contract or add it end to end. **Do not emit a fabricated state.**"
- The game-content bundle resolver **catches every resolution error and returns the bundled release**, tagged in a disposition but raising no Home failure — the selected content release can silently differ from the attempted one.

### B7 / B8 — the cut

B7 (Pro) rejects "both proposed native-linked and downloadable Go runtimes, the
new `ApplicationBootstrapState` protocol, speculative successor trees, client
ranking, and a general readiness/navigation framework," and insists two
decisions be made explicitly, with the line the watcher should borrow verbatim:
**"Do not represent silence as approval."**

B8 records an executed 472-line subtraction with 18 focused cases passing and
zero introduced analyzer diagnostics — and, notably, refuses to launder the
remaining red: "The separate strict first-visible diagnostic remains a genuine
red result. It was not run, edited, suppressed, or counted as passing here."

**Cut status: incomplete.** PR #5642 is **still open and unmerged**; issues
#4895, #5641, #5653 remain open, and follow-on issues #5823 and #5809 were
opened for the unfinished contract and its proof.

---

## 4. Cluster C — older and cross-cutting

### C1 — Telemetry overbuild review (2026-08-13)

Outside the 2026-08-25 window but the single best account of *how* overbuild
accumulates. It names four stages: useful event contracts → **destinations
became policy** → **every constraint gained another mechanism** → **repairs
began governing repairs**.

**The fundamental mistake, in its own words:** "For a valuable event, Poker Skill
repeatedly lacked one owner for the obligation… Instead, different layers owned
fragments… **The same event therefore had several authorities but no complete
owner. More retries did not fix that. More states made the disagreement
durable.**"

Nine "complexity we created without equivalent value" entries: several physical
senders without a common occurrence id; **product navigation or payment awaiting
telemetry** ("converts observer readiness into player failure"); optional context
owning event validity; runtime catalog validation that drops release events;
routing truth duplicated across four layers; one shared queue policy for
heterogeneous providers; a permanent RAM fallback after one SQLite failure;
"**recovery machines, alarms, timers, and verifier fleets for states created by
the above mechanisms** — they measure and govern accidental complexity instead
of removing its cause"; internal outboxes when the provider already retries.

Six named reasons the subsystem stays broken, including: "**Monitoring reproduces
the same ownership problem**" and "**The repair target is often machinery, not
truth.** The response to a latch is a recovery machine; the response to
quarantine is a larger state machine; the response to duplicate senders is
policy. **The original duplicate or overbroad owner survives.**"

### C2 — Puzzle Finish recovery stack (2026-09-06)

Fourteen findings, and — uniquely useful — **every finding classified by
evidence class**: demonstrated defects (0), source-traced behavior (F3, F5, F6,
F7, F10, F13, F14), **future coupling** (F2, F4, F8, F9, F11), **hypothetical
hardening** (F1, F12).

Drift findings: scope creation and owner-identity rules **duplicated across six
surfaces with two different ownership idioms**; controller-to-recovery ordinal
arithmetic reconciled **in three places**; free-form stage strings; a `canRetry`
rule computed two ways; a **retained-failed-Open slot** that "exists to make
counts exact for Open-failure scenarios whose **production incidence is
unknown**. That is where cost concentrates."

Complexity verdict: "For a two-person startup this is more than the smallest
coherent change; it is also internally consistent and isolated from product
state, so it is a **maintenance cost rather than a risk**." And on F1: "It is a
**hypothetical hardening of an invariant the surrounding code already
protects**."

### C3 — The correction casebook (the prior detector catalog)

Mined from 2026-08-05 to 2026-08-23: **6,858 prompts, 141 overbuild corrections
across 83 sessions — about seven per day.** Eight anti-patterns:

1. **Overbuild by default** — harnesses, frameworks, registries, provenance, locking added to simple asks. Case: a 17-string copy feature grew a 518-spot "golden corpus" fixture harness, a lint framework with byte budgets, unit tests for an unreachable state, provenance versioning and a data-driven registry for three branches. All cut.
2. **Proof/receipt machinery nobody asked for** — "Every time you say the word 'proof' you're overbuilding." *The vocabulary itself — proof, receipt, pinning, contract, gate — is a trusted overbuild symptom.*
3. **Scope contagion / defensibility expansion** — one finding becomes an everything-fix; threat models imported from the wrong industry ("NASA grade", gambling regulation for a poker training app).
4. **Pedantic precision over UX and business truth** — copy failed in evals for rounding 39.7% to 40% as an "accuracy error."
5. **Refusing to decide on partial information** — refused to classify 389 attribution cases without row-level provability, for days.
6. **Hypothetical-hazard armor** — mutexes and check-and-set locks on a streaks feature; "the bugs the user actually hit came FROM the locking."
7. **Wall-clock as tell** — "A run that grinds for hours or overnight is treated by the user as near-proof of overbuild — **and he has been right every time.**"
8. **Experimental-scaffolding reflex** — a decided copy replacement reframed as a flag-gated A/B experiment.

Four meta-patterns, one of which is a direct warning to the watcher itself:

> **"The oversight machinery itself overbuilds (2026-08-16).**
> *'shut down the intent police and stop using it, it actually contributed to
> the runaway overbuild of the plan'*
> A telemetry plan had grown to a 223 KB plan plus 3 MB of manifests through
> repeated reviewer rounds; the agent admitted 'I let exhaustive reconciliation
> become recursive refinement.' **Verification and review layers compound each
> other. Adding a watcher to a spiral feeds the spiral.**"

Also: "The proof spiral must end in deletion, not a freeze"; "He now corrects
preemptively — **that is the failure signal**"; and the balancing rule that
prevents mis-tuning the detector — "**He also routinely DEMANDS exhaustive plans
and specs… Perfectionism in machinery, proofs, and gates is the failure. Do not
flatten this into 'do less everywhere.'**"

### C4 — Missions V1.2 requirements audit (2026-09-14)

48 functional requirements audited by 48 fresh agents (2 Astra xhigh, 46 Sol
xhigh), one row per agent, four at a time. Result: **42 code gaps and 6 scoped
passes; 46 test/coverage gaps and 2 scoped passes** — "requirement-row counts,
not unique bugs." Three specification gaps were resolved by a Pro+Codex
consultation and — importantly for provenance tracking — **explicitly labeled as
adopted by the agents, not attributed to Amir**: "They were **not silently
attributed to Amir** or represented as present in the original materials."
Seven new issues and four amendments were filed under epic #5694.

---

## 5. Cluster D — Cratejoy inclusive pricing epic (#16151)

The best-documented scope-creep case in the corpus: **four independent audits by
four different models across eleven days, converging, then an executed cut, then
a fresh re-audit confirming the cut held.**

### The original ask, as every audit restates it

> "Put the complete buyer price into the Shopify merchandise price, preserve
> seller economics and seller-facing behavior, support historical fee-line
> orders, migrate existing contracts, remove active fee writers, and provide one
> small catalog-level treatment with optional legitimate compare-at
> merchandising."

With **explicit non-goals in the original epic body**: no personalized or
geographic pricing, no pricing microservice, no pricing-rule DSL / registry /
admin UI, no elasticity optimizer, no second promotions system, no seller-semantic
rewrites, no `ServiceFee` rename, no historical rewriting. The epic named seven
ordinary application seams and a dependency-ordered set of child slices.

### D3 — the scope-creep review (2026-09-13). Verdict: **"scope creep confirmed; product completion not proven; cut line recommended."**

The framing sentence:

> "The strongest problem is not lack of effort; it is that **the work keeps adding
> machinery and proof obligations faster than it closes the original buyer/seller
> outcome.**"

Three directions of expansion — "(1) Inclusive buyer pricing and accounting. (2)
A distributed publication, approval, recovery, and evidence control plane. (3) A
persistent shared QA/testing platform with its own lifecycle, network, storage,
and browser-isolation infrastructure. **The first program is the product.**"

Seven findings:

1. **"Pricing implementation became a distributed control plane."** Signed price contracts, variant token maps, product modes, shop-wide release latches, complete product censuses, cohort authorization files, object-store manifests, immutable receipts, Redis leases, publication ownership, recovery obligations, cross-service fingerprints. The audit is careful to name what is justified (a signed accepted-price fact, a narrow idempotent operation record, a product-level pending fence) before the verdict: "**The aggregate has become a second platform.**" Root cause given: "durability additions at real write boundaries kept compounding instead of staying narrow."
   **Split brain produced by it, enumerated:** current price exists in Shopify, signed tokens, Typesense, cohort artifacts and release receipts (5 places); treatment membership in code constants, cohort JSON, product metafields and Marketplace maps (4 places); publication state in product mode, a global latch, Redis ownership and object-store current pointers (4 places). Controlling rule proposed: "**Receipts record what happened; they must not become competing current truth.**"
2. **"The one small alternate treatment became a second activation product."** It acquired its own release binding, exact cohort identity, publication checks, global census conditions, measurement SQL, QA authority artifacts and activation path — and this produced a **concrete correctness failure, not only overengineering**: a normal state of ten alternate products plus one other default-inclusive product is unreleasable, because releasing the ten fails the global census, releasing all eleven fails the exact-cohort rule, and leaving the latch off blocks the marked products. "This is the kind of contradiction created when **a small experiment inherits catalog-wide activation machinery.**"
3. **"Optional legitimate compare-at became formula-derived."** The original says compare-at is optional and must not be fabricated automatically; the implementation derives a reference price from the seller base and the default treatment, writes it through ordinary product sync, and the Marketplace can reject a publication without one. "A seller-base edit can silently produce a new 'was' price from a formula." — a direct violation of a stated non-goal.
4. **"Typesense garbage collection acquired global publication authority."** Obsolete-collection deletion was routed through the same global `PublicationOwner` used for live publication, so a lost response deleting a *retired* index can permanently fence *all* current publication.
5. **"Migration machinery looks complete while the real writer refuses."** ~13k lines of state machine, manifests, classifications, compensation logic, receipts and recovery paths built around a provider path that unconditionally raises `ATOMICITY_UNPROVEN`. "The refusal is the safe behavior. **It is not migration completion.**" And: "**Refusal is not a pass.**"
6. **"Gate 2 became a separate persistent QA platform."** A dedicated Studio project, private Postgres/Redis/Kafka/Typesense/MinIO/Mailpit, persistent offsets, per-role images, Cloudflare tunnel and DNS routes, browser network isolation, local mail/error sinks, outbound guards, restart/reset behavior and a large evidence ledger. "This is a valid integration-environment project **if explicitly funded and owned. It is not the definition of the pricing product.**" Replacement: one disposable four-step critical-path check.
7. **"API #1450 and general runtime repairs are adjacent enabling work, not product features."** Webhook HMAC auth, seller launch guards, buyer account mapping, diagnostics redaction, Docker endpoint ownership, lifecycle supervisors. "Do not use it to enlarge the pricing definition of done."

Plus a process finding in the cut table: "**Repeated Pro/Fable/source/evidence rounds → Process overhead → One implementation review and one final acceptance review.**"

**Self-correction worth preserving.** Both D2 and D3 originally attributed the separate CircleCI epic #16198 to pricing scope creep. Live GitHub verification showed #16198 is a separate top-level epic with its own children and no reference in #16151's body, children or comments. The finding was **explicitly withdrawn with a dated banner** in both documents: "The original review inferred pricing scope from **unrelated files in the shared workspace.** That inference is withdrawn." — a shared-worktree false positive the watcher will hit too.

### D2 — the Fable cold read

Converges independently on the same three expansion directions, and adds
blast-radius numbers: three pricing commits alone add ~16,800 lines; the Gate 2
worklog is 2,339 lines. "Documentation volume is not itself a defect, but this is
a warning that **the process has become an end in itself.**"

Its recommendation 7 is the most directly reusable rule in the whole corpus:

> "**Use a stop rule.** If a proposed item cannot be mapped to one original
> definition-of-done bullet, a named hard invariant, or one of the three concrete
> blocker repairs above, defer it and require explicit user approval in a
> separate issue."

### D1 — the earlier Pro intent audit (2026-09-03)

18 open PRs at exact heads: 5 merge-ready (dormant), 5 merge-with-fixes,
**8 do-not-merge**. Findings: Shopify price ↔ signed token ↔ Typesense can
disagree in steady state so a customer sees a stale low price then a higher
checkout price; PayWhirl written first and Shopify second on routine retargeting
with no compensation on failure; treatment membership duplicated four ways; and
the charge-neutral migration promise "**silently superseded** by a policy that can
raise total tax — a conscious policy amendment… but it contradicts the literal
original hard invariant." It also caught **an unrelated dependency-pin PR
(`marketplace#8817`) riding along in the epic's merge train** despite being
"explicitly not required by the epic."

### D5 / D6 — the cut, and proof it held

D5 records the reconciliation: "**Pro and Fable both identify the same overbuild:**
a pricing release control plane, a persistent QA/runtime platform,
approval/evidence/checksum machinery, formula-derived compare-at, and migration
work being treated as a prerequisite to the buyer outcome." Decision: E1 = five
units on the core commerce path; E2 = legacy convergence, deferred; E3 = one
catalog treatment, parked until a real test is named; "**Stop the broad
runtime/certification program**" and replace it with a dormant deployment and one
canary product/order/refund. Money-boundary safety explicitly preserved.

D6 then re-scoped 18 issues into 9 (11 duplicates closed) and ranked 104
requirements P0–P3, and a **fresh independent Sol audit of issue #16155**
confirmed the cut survived contact with implementation: "no new registry,
approval hash, QA platform, E2/E3 branch, or CircleCI overhaul."

**Cut evidence on GitHub — this is the most completely executed cut in the
corpus.** Epic `cratejoy/cratejoy#16151` has been **retitled to "E1 inclusive
marketplace pricing: nine delivery owners, bounded real E2E"**; the rescope
landed in the epic title itself. Issue **#16213 "Remove the inclusive-pricing
release control plane from E1" is CLOSED** — the control-plane cut was filed as
its own issue and completed. **#16212 "Decide first-activation cart shape with
data"** (D5's unresolved data gate N3) and **#16211 "Keep legacy fee-bearing
contract servicing intact during E1"** are also closed. #16155 and #16210 remain
open as the E1 delivery work.

## 6. Cluster E — CircleCI cost-reduction epic (#16198)

### The original ask, as the audit restates it

Keep CircleCI; give every PR cheap checks plus native test-impact
change-focused Python feedback with a mandatory full-suite fallback; one release
validation path; one policy revision merged inactive in the existing repo; a
small GitHub Actions relay; **one** status context `ci/circleci: ci-gate`; and a
bounded 2+8-comparison economics experiment **before** claiming savings.

### E1 — Fable X end-to-end audit (2026-09-14)

Fourteen findings. The scope-relevant ones, with the audit's own severity labels:

- **F1 (Wrong, must be rebuilt).** "The savings mechanism is not 'missing an adapter'; **five independent layers hard-code full fallback**, so the delivered feedback path cannot narrow work without a redesign of the contract." The selector code exists and nothing can reach it.
- **F2 (Wrong; economics unproven and directionally adverse).** "Under the delivered full-fallback contract, the new orchestration **most likely costs more per month than today**, not less. No document quantifies this." Double setup pipelines, serialized cheap-checks plus shards, hourly reconcile-all-open-PRs, full reruns on every base movement, no cancellation. Estimated −11% to +46% vs. baseline.
- **F3 (Split-brain source of truth).** "The trusted-policy layer is a **second, disconnected CI system with its own copy of the runner**; the core repo and the policy repo now disagree about which `run_python.py` is 'the' runner."
- **F4 (Contradictory designs).** "**The architecture of record was replaced mid-run, and the requirements were rewritten to match the replacement.**" Live GitHub issue bodies were edited to describe the replacement with no supersession banner.
- **F5.** The trust-boundary proof ran only the positive case; all four denial cases were created with disabled triggers and never run; the one production-critical artifact-capture job failed 3/3 and was undiagnosed.
- **F6 (Not demonstrated).** The epic's own mandatory acceptance economics are **0 of 2 baselines, 0 of 8 comparisons, 0 of 190 revisions replayed.**
- **F7 (Wrong; blocks future merge protection).** One GitHub status context **per target hash**, so every PR update creates a new check name — the opposite of the epic's single-context requirement.
- **F8 (Scope drift, named as such).** A production Kafka worker retry loop and its test were added to a CI-cost PR although the epic says that work stays outside "unless Amir explicitly expands scope" — "**no scope expansion by Amir is recorded.**" Also: a 77-line `test-suites.yml` declaring a suite nothing invokes, whose only consumer is a test asserting substrings of the file — "**a vacuous test of an orphan**"; a permanently `BLOCKED` evaluator (2,533 + 238 + 564 + 351 lines) shipped into the product repo's `.circleci/` — "audit material, not CI configuration"; and `docs/RELEASE.md` documenting "a release path that does not exist on the provider."
- **F9 (Reframe).** RESULT documents describe deleted and superseded code as "implemented", with no correction banner. And the process tell: "the sheer volume (48 MB, 2,679 evidence files, **~60 review checkpoints in ~34 hours**) is itself a signal: **review throughput was spent on repeatedly re-hashing rewritten code rather than on the one experiment the epic made mandatory.**"
- **F10 (Design decision needed).** "The selector rejection is **partly self-imposed**; the epic's mandatory 2+8 application experiment was never attempted on the mechanism that *did* work on the fixture."

Its §4 heading is literally a list of split-brains: **"two runners… two controllers… two publishers… two definitions of Q… two status models… two test-suite declarations."**

**Final disposition** uses a four-bucket vocabulary the watcher should steal wholesale — **Genuinely built / Only a design / Contradictory / Adverse** — and ends: "Freeze the policy package until that decision exists. **Do not adopt, activate, or fund anything on the current evidence.**"

## 7. Cluster F — psmobile #4126: the review loop as the drift engine

`psmobile-worktrees/4126-review-governance-20260819/plans/drafts/2026-08-20-app-review-scope-recovery-plan.md`,
2026-08-20, clean external Claude Fable 5 xhigh. This is the corpus's clearest
single case of **oversight machinery generating its own scope**, and it maps
directly onto C3's meta-pattern.

**Verdict:** "the T1 core is on-scope and well built; T2 is delivered but wrapped
in **four rounds of reviewer-driven cross-user hardening that the plan never
authorized**; T3–T6, the part users would actually see, has not been started."

> "The work is stuck in a T1–T2 acceptance loop (**nine repair cycles**, each cold
> reviewer surfacing new hypothetical races in progressively more peripheral
> surfaces: push cadence, dev-only overlays, chapter-complete asks,
> Mission/leaderboard reads). The plan's own rule, '**a reviewer finding cannot
> expand the plan**', has been violated in effect, if not in ledger form: **every
> expansion was recorded as 'authorized T1-T2 repair' and implemented.**"

Four overbuild findings:

1. **Push-ask cadence rollback machinery.** Built to defend a user signing out in the milliseconds between a cadence reservation and sheet presentation, "where the worst harm is **one skipped optional push ask** for the departed user (keys are already per-user). The cure carries its own concurrency proof… an adversarial interleaving test, a new error branch, and a resequenced call on a shared surface. **This is more failure surface than the defended failure.**"
2. **Cross-user guards on durable, pre-existing side effects** — 7 checks in one file, 10 in another, on paths "the plan explicitly froze". "The guards change durable semantics (early `return false` can skip completion recording), encode a **repo-wide cross-user doctrine nobody approved**, and are precisely **what kept the review loop alive, each round of guards exposed the 'next' unguarded read.**"
3. **Dev-tool ownership plumbing** — six ownership checks inside a developer-only Force Perfect action, "defend[ing] a developer signing out mid-QA-tap. Delete entirely."
4. **"The review-loop process itself."** "Repairs 6–9 each passed a full green independent gate and were still failed on newly invented seams. The pending post-repair9 consult will, on this trajectory, find a tenth. **The loop, not the code, is now the main schedule and risk driver.**"

And the consequence nobody noticed while the loop ran: the tree, if shipped,
"would silently disable all iOS review prompts while still consuming the
foreground-session opportunity and emitting `eligible=true` telemetry with no
card" — because the user-visible deliverable was never started.

Its 20-row scope ledger uses a four-verdict vocabulary: **keep / keep, freeze /
simplify / delete**, with "keep, freeze" reserved for machinery that is already
sanctioned by doctrine and whose removal "restarts the loop."

---

## 8. Cross-document recurring drivers

Counted across the 22 Markdown audits that carry findings (A1–A7, B1–B7, C1–C3,
D1–D3, E1, F1). A document counts once per driver even if it names several
instances.

| # | Driver | Docs | Representative instances |
|---|---|---:|---|
| **1** | **Duplicated authority / split brain: one fact or rule owned in two-to-six places.** | **11** — A3, A5, A6, B5, B6, C1, C2, C3, D1, D3, E1 | Three access paths to one response plus a second hard-coded star map (A5 F7/F8); seven split-brain rows including two byte copies of one module with a SHA-parity ceremony (B5 S1–S7); scope rules across six surfaces and ordinal arithmetic in three (C2); "several authorities but no complete owner" (C1); price in 5 places, treatment membership in 4, publication state in 4 (D3); "two runners… two controllers… two publishers… two definitions of Q… two status models" (E1 §4) |
| **2** | **Architecture shaped by the code that already exists, not by the requirement.** The agent finds a branch, a draft, a PR or a service and lets its shape become the design. | **10** — A1, A3, A4, A5, B1, B5, C1, C2, C3, D3 | "Several pieces are shaped by code that exists on unmerged branches rather than by what the thirteen frames need" (A3); "This survived because it existed" (A5 F11); "inherited ceremony" from a superseded design (A3 3.3); configuration candidate staging surviving the change that obsoleted it (B5 O1); "the aggregate has become a second platform" (D3); anti-pattern 1 (C3) |
| **3** | **Hypothetical-hazard armor: machinery for failures with no observed incidence.** | **10** — A1, A3, A4, A5, B5, C1, C2, C3, D3, F1 | Route recovery controller driven by reachability/resume/account transitions (A4); actor-change deferral branch "for an untraced condition" (A5 F5); retained-failed-Open slot whose "production incidence is unknown" (C2 F10); "recovery machines, alarms, timers, and verifier fleets for states created by the above mechanisms" (C1); **"This is more failure surface than the defended failure"** — a cadence rollback defending one skipped optional push ask (F1); mutexes on streaks (C3 ap6) |
| **4** | **Verification and proof machinery nobody asked for — and tests that prove nothing.** | **10** — A3, A4, A5, A6, B5, C1, C3, D3, E1, F1 | Global readiness census, coverage certification, apply-twice manifest proof, warehouse reconciliation as acceptance (A3/A4); server re-grading data it wrote in the same transaction (A5 F7); tautological assertions (A6 F11); Gate 2's private Postgres/Kafka/Typesense/MinIO/Mailpit QA platform and evidence ledger (D3); "a vacuous test of an orphan" plus 2,679 evidence files (E1 F8/F9); a concurrency proof and an adversarial interleaving test for a millisecond window (F1); "Every time you say the word 'proof' you're overbuilding" (C3 ap2) |
| **5** | **A narrow, correct rule silently widened into a product concession — and the widening never reaches the user.** | **9** — A3, A5, B5, B6, B7, C1, D1, D3, E1 | "'Reporting stays outside Finish' is about writes and is right. **It was extended to** [a form] that Amir's wording does not [accept]" (A5 F2); "the PR body describes it as 'the invalid plan is cleared', which is inaccurate" (B5); "**Do not represent silence as approval**" (B7); charge-neutral migration "silently superseded" by a policy that can raise tax (D1); optional compare-at became formula-derived and mandatory (D3); "the requirements were rewritten to match the replacement" (E1 F4) |
| **6** | **Claimed complete on machinery, not on outcome.** Green gates, volume, and confident status text while the user-visible deliverable is unstarted, unrun, or locally-only. | **6** — A6, B1, B5, D3, E1, F1 | Every "113/115 golden" claim is local-only and a failing artifact contradicts the worklog (A6 F8); "asserted, not evidenced" (B1 #4); "**Refusal is not a pass**" (D3); 0 of 2 baselines, 0 of 8 comparisons, 0 of 190 revisions (E1 F6) and RESULT docs describing deleted code as implemented (E1 F9); nine green repair rounds while T3–T6 was never started (F1) |
| **7** | **Review/oversight machinery generating its own scope.** | **6** — A3, B3, C3 meta, D3, E1, F1 | **"Every expansion was recorded as 'authorized T1-T2 repair' and implemented"; nine repair cycles; "the loop, not the code, is now the main schedule and risk driver"** (F1); "Repeated Pro/Fable/source/evidence rounds → Process overhead → one implementation review and one final acceptance review" (D3); "~60 review checkpoints in ~34 hours… review throughput was spent on repeatedly re-hashing rewritten code" (E1 F9); "the oversight machinery itself overbuilds" — a 223 KB plan plus 3 MB of manifests through repeated reviewer rounds (C3); Pro's "reuse previously started storage" read as "adopt PR #5285 wholesale" (A3 3.2) |
| **8** | **Defensive catch-and-continue that converts a loud failure into an invisible one.** | **6** — A1, B1, B5, B6, C1, C2 | Client swallows `NotFound` and the screen looks normal (A1 F9); `catchError` + `on ProviderCancelledError {}` making a critical defect invisible in production (B1); silent-stale plan with tappable cards (B5 F4); four `stableKey, _` discards that can omit a card (B6); "the system fails closed on context" (C1) |
| **9** | **Blocker workaround / dependency stacking that drags unrelated scope along.** | **6** — A3, A6, B5, C1, D1, E1 | Stacking the M1 backend on #5470, "the same stacking that left #5643 depending on an unrelated warehouse and Play-vs-AI campaign for its CI" (A3 3.1); a proto relocation and unrelated Core test failures inside the Home PR (B5); deleted test IDs breaking the nightly money suite (A6 F1); an unrelated dependency-pin PR riding the epic's merge train (D1); a production Kafka worker retry loop inside a CI-cost PR with "no scope expansion by Amir recorded" (E1 F8) |
| **10** | **Plan self-authored, then treated as authority over the user's words.** | **6** — A3, A4, A5, A6, B5, E1 | The plan's own "certify readiness" text becoming the requirement (A4); "plan mandate versus product need" as a finding class (A5 F10); test cases enumerated for machinery the review recommends cutting (A3 3.9); live GitHub issue bodies rewritten to match the replacement architecture with no supersession banner (E1 F4) |
| **11** | **Dead surface left behind after a pivot.** | **5** — A3, A5, B5, B6, E1 | Zero-caller `.unavailable()` / `.excluded()` constructors, dead telemetry producers and fields, a stale coverage doc (B5 O6–O11); unused wire echoes and an untracked seed script outside any PR (A5 F9); an event contract with no call site (B6); an orphan `test-suites.yml` and a `BLOCKED` evaluator shipped into the product repo (E1 F8) |
| **12** | **Sub-agent / reviewer drift and cross-contamination.** | **5** — A5, A7, D2, D3, F1 | "the M1-061 reviewer briefly launched an unauthorized extra Astra child"; "M1-085 was held unpublished because its report repeated an unsupported neighboring test-gap claim" (A7); **two reviewers independently blamed pricing for a separate CircleCI epic because its files were in the shared workspace — withdrawn after live verification** (D2/D3); A3 and A5 both open with revision notes withdrawing first-draft claims |

**Top five, by count and by consequence:**

1. **Split brain** — one fact owned in two to six places (11 docs).
2. **Architecture shaped by the code that already exists**, not by the requirement (10 docs).
3. **Hypothetical-hazard armor** — machinery for failures with no observed incidence (10 docs).
4. **Proof and verification machinery**, including tests that assert tautologies (10 docs).
5. **A correct narrow rule silently widened** into an unapproved product concession, with the widening never disclosed (9 docs).

Two more deserve the watcher's attention even at lower counts, because they are
the ones that make drift *invisible*: **"claimed complete on machinery, not on
outcome"** (6 docs — this is exactly the "progress reports looked normal in that
window" signal) and **"review machinery generating its own scope"** (6 docs — a
direct warning about what the watcher itself could become).

---

## 9. Vocabulary

### What the audits call drift (candidate detector features and report labels)

**Naming the overbuild:** overbuild · overbuilt · unnecessary machinery ·
inherited ceremony · ceremony · certification machinery · validation program ·
recovery machinery · verifier fleets · repair factory · control plane ·
"a second platform" · "a second activation product" · "a separate persistent QA
platform" · hypothetical hardening · defensive self-validation · speculative ·
hedges · armor · scaffolding · "code retained only because it already exists" ·
"shaped by code that exists on unmerged branches" · "This survived because it
existed" · "more failure surface than the defended failure" · accidental
complexity · self-inflicted complexity · bug vectors.

**Naming the ownership failure:** split brain · multiple sources of truth ·
duplicated authority · competing authorities · two producers · three access paths ·
competing writers · second owner · parallel path · second presentation path ·
byte copies · mirror · "several authorities but no complete owner" ·
"receipts must not become competing current truth" · SSOT · "one owning merge" ·
drift by omission.

**Naming the requirement failure:** missed the point · plan drift · scope drift ·
scope creep · scope contagion · "the plan departs from the request" · "plan
mandate versus product need" · "was extended to" · "silently superseded" ·
"promoted into a [wider] gate" · "the architecture of record was replaced
mid-run" · "the requirements were rewritten to match the replacement" ·
"didn't holistically accomplish what I'm after" · "I recognize the feature I gave
you in the first place" · locked product boundary · original ask · intent ·
non-goals · hard invariant · definition of done.

**Naming the invisibility:** silent · silently · swallowed · catch-and-continue ·
catch-and-log · normalized · stale success · silent-stale · dead button ·
no-op · "invisible in production" · "hides recurrence" · flood control ·
undisclosed · "asserted, not evidenced" · "Refusal is not a pass" · "no
supersession banner" · tautological · vacuous · "a vacuous test of an orphan" ·
"pins the flicker" · fail closed · fail loud.

**Naming the cut:** cut plan · cut list · cut line · "lean completion cut line" ·
"do not build" · subtraction · subtraction pass · "remove entirely" ·
keep/delete/replace · keep / keep-freeze / simplify / delete · smallest coherent
repair · smallest defensible direction · "the architecture I would retain,
starting from the requirements" · "what exists after the cut" · delete-first ·
clean-start architecture · "what this omits compared with the plan" · rescope ·
E1/E2/E3 split · park · defer.

**Classification words the audits use to keep themselves honest (borrow these):**
present code behavior · plan drift · speculative risk · future coupling ·
hypothetical hardening · accepted/intentional · source-traced · corroborated ·
static analysis · demonstrated defect · "assessment" · "justified unknowns" ·
"evidence limits" · "what I withdraw" · "listed so they are not re-litigated" ·
"a lean, not a finding" · "This choice is Amir's." · and E1's four-bucket final
disposition, which is the most compact honest summary format in the corpus:
**Genuinely built / Only a design / Contradictory / Adverse.**

**Two reusable rules the audits state as rules, not findings:**

> "**Use a stop rule.** If a proposed item cannot be mapped to one original
> definition-of-done bullet, a named hard invariant, or one of the three concrete
> blocker repairs above, defer it and require explicit user approval in a
> separate issue." (D2)

> "Reclassify every remaining plan item as **direct product**, **required
> safety**, **separate enabling work**, or **defer**. If it cannot map to an
> original definition-of-done bullet or one of the three blocker repairs, defer
> it." (D3)

### Amir's own correction vocabulary (from C3, verbatim — highest-signal triggers)

- "overbuild" in every inflection — **the single most-used correction word**
- "You always default to maximizing perfection" / "You always do that shit"
- "defensively correct at a scientific level" / "a fucking scientific survey" / "defensible if you were writing an academic paper"
- "bug vectors" — overbuild priced as future bugs for "my tiny team"
- "NASA grade" / "NSA grade" / "insane cryptographic standards"
- "pedantic" / "insanely pedantic" / "pedantic horse shit"
- "is it purely hypothetical or is it a real concern that actually happens?"
- "receipt shit" / "protection shit" / "the stupid receipts"
- "Every time you say the word 'proof' you're overbuilding"
- scale reminders: "my early-stage startup" / "our small app" / "my tiny team" / "internal only tool that only I use ever" / "this is just a niceity"
- "Don't turn everything into everything just because you found one fucking thing"
- "Just fucking fix it simply" / "super minimal dude"
- and from this window: "some crazy shit that I didn't ask for" / "figure out where we've scope crept into some insane shit" / "artificial blocker that's fucking pedantic and annoying"

### Calibration guard

C3 states the counter-rule explicitly, and the watcher must carry it:

> "He also routinely DEMANDS exhaustive plans and specs ('I want it to be
> exhaustive'). **Depth of thinking, root-cause fixes, and thorough requirements
> are wanted. Perfectionism in machinery, proofs, and gates is the failure. Do
> not flatten this into 'do less everywhere.'**"

And: "It costs more resources to fix the same thing root cause 19 separate times
than it costs to fix at one time deeply. However it costs even more if in fixing
at one time deeply you overbuild and introduce nine other bug vectors."

---

## 10. Coverage and gaps

### What was searched

**Filesystem.** `find` over `psagentspace`, `psmobile`, `psmobile-worktrees/*`,
`puzzledb`, `puzzledb-worktrees/*`, `agentspace`, `website-worktrees/*`,
`logan`, `aimgr`, `prime-agent`, `arch_skill` for `*.md` / `*.txt` newer than
2026-08-25, excluding `node_modules`, `.git`, `build`, `.dart_tool`, `Pods`,
`vendor`, `.venv`, `site-packages`, `.pub-cache`. **249,309 files** matched the
date filter. Keyword grep (`scope creep`, `overbuil`, `cut plan`, `split brain`,
`missed the point`, `what I actually asked`, `original ask`, `unrequested`,
`never asked for`, `unintended consequence`, `hypothetical`, `source of truth`,
`intent ledger`) reduced the psagentspace/arch_skill/agentspace/logan/aimgr/
prime-agent set of 21,646 files to **855 hits**, then ranked by keyword density
to isolate the real audits. The non-psagentspace roots were swept by a delegated
read-only search agent; every document that agent reported was then verified to
exist and read directly here. Every document in the inventory was read directly.

**Roots searched that produced nothing qualifying**, with the reason:

- **`psmobile` main checkout.** No standalone scope audit. Three near-misses worth not re-checking: `docs/INTENT_LEDGER_ONBOARDING_ANDROID_ATT_PREPROMPT_2026-08-16.md` is a *forward-looking* non-goals guardrail, not a built-vs-asked audit; the dozens of `*_PLAN_AUDIT.md` files are arch-step **plan-readiness** audits, a different genre; and **nearly every implementation plan in this repo carries a boilerplate "Overbuild cut" / "Scope and overbuild cut" section** — house style baked into the planning template, which is itself a finding (the anti-overbuild discipline is already templated into psmobile planning, and it did not prevent the M1 or Home drift).
- **`puzzledb` + ~50 worktrees.** Untracked docs are almost entirely `docs/reports/*_puzzle_final_quality_*.md` — poker-content quality audits, a different genre. `puzzledb-worktrees/psagentspace` is a symlink into psagentspace.
- **`website-worktrees`.** One stray `_pr_body.md`.
- **`logan`.** A personal legal-case workspace; wrong domain entirely.
- **`aimgr`.** `docs/PRIME_AGENT_PERFORMANCE_AUDIT_2026-09-02.md` audits CPU/disk, not scope. `docs/aelaguiz/PRIME_MCP_REMOTE_CONTROL_PLAN_2026-08-25_RESEARCH_USAGE.md` mines Amir's own past prompts for product research (it quotes, among others, *"stack the PRs and DO NOT ALLOW SCOPE CREEP"* and *"Build a new plan that isn't insanely overbuilt"*) — useful as raw correction vocabulary, not an audit of built work.
- **`prime-agent`.** "split-brain" appears only in a crash-observability sense.
- **`~/Documents/Codex/{2026-07-26, 2026-08-07, 2026-08-10, 2026-08-25, 2026-09-02, 2026-09-03}`.** Almost entirely empty scratch `work/` and `outputs/` task folders; the only real content is an unrelated audio-transcription script.
- **`~/.codex/memories/epic-4926-continuation.md`.** A live operational continuation memory (CI/PR merge-readiness tracking for psmobile #4926). It never compares built work to an original ask.

**GitHub.** `gh issue list --search "scope OR overbuilt OR cut plan OR cleanup"
--state all` across `funcountry/agentspace`, `funcountry/psmobile`,
`funcountry/puzzledb`. Individual state checks on the M1 children (#5610, #5611,
#5614, #5270, #5665–#5668), the superseded pair (#5643, #5644), the Home epic
(#4895, #5641, #5653, #5809, #5823), eleven psmobile PR heads (#5642, #5690,
#5692, #5693, #5738–#5743, #5754, #5813, #5701), and the Cratejoy epics and
E1 children (`cratejoy/cratejoy` #16151, #16198, #16155, #16210–#16213).

**Google Sheets (read-only via `gws`, authenticated).** All four IDs fetched
successfully:

| ID | Workbook | Relevant tab | Out-of-scope / pedantic section |
|---|---|---|---|
| `1QqvZvN-CIrlHKdU1AmqwgUqA3lEHEqh4jkVPJaVJBRk` | Poker Skill \| Missions & Achievements (26 tabs) | "Missions v1.2 requirements" (59 rows) | **Yes.** Row 56 header **"Pedantic / non-blocking"**, rows 57–59 at priority **P4**: *Exact internal names* (equivalent spellings are non-blocking), *Exact artwork sizes* (32px/128px supplied; different internal sizing non-blocking if icons stay sharp and correctly fitted), *Concurrency mechanism* (conditional revision update preferred over a row lock; changing a safe mechanism solely to match the preference is non-blocking absent lost progress, duplicate grants or real contention). Rows 49–51 are the later Natasha Johnson lifecycle addendum. |
| `1SFte_YEH0Cjb3ViwtHPbCoFpqQM8h1A4pC6BZIGZd5g` | PVP SNG | "SNG requirements - AUDITED" (120 rows, all *Not assessed*) | **No labeled section.** Scope boundaries appear as ordinary P1 rows instead: *Locked mock intent* ("Treat approved mocks and later corrections as the feature boundary… Mocks explain intention rather than pixel-perfect coordinates"), *Preserve other modes* ("does not change AI eligibility, old XP settlement…"), *No new manual sit-out command* ("Visual variants do not expand the production controls"), *No AI seat filling*, *Free human entry*. |
| `1VPT7CroENZqaNvo7QPkQW8rpHFdvhJJtlAgtPBFtJ7o` | Skills Tracking | "M1 requirements · AUDIT" (308 rows, 14 cols) | **No pedantic section** — A7 states this explicitly: "The live M1 register had no labeled pedantic section. The working scope therefore includes every current requirement: 302 rows." The equivalents are rows 5–8 and 13 (*No invented loading UX*, *No sanctioned failure UX*, *No alternate layout mode*, ***Locked capability scope*** — "Remove hypothetical machinery, split ownership and code retained only because it already exists", *M1 boundary* — "M2 skill drill-in, profile dashboards, rankings, generic comparison history and weekly challenges remain separate capabilities"), plus rows 305–308 which preserve superseded design history explicitly ("Design exploration only; it does not authorize a new tablet UI"; "Do not use abandoned images as implementation references"). Row 12 is the over-cutting guard: *Preserve requested features* — "Simplification must not cut approved UI, history, peers, locks or fixture cases." |
| `1-YXNEGzup4j5oOEm4tMNcsOQbhd6EYIvhJqQQWL_n-E` | Fee Tracking | "Pricing requirements" (119 rows, all UNAUDITED) | **Partial.** Explicit exclusion rows rather than a pedantic block: R008 *Marketplace boundary* ("Seller storefront/SaaS economics are excluded"), R050 *Explicit exclusion decisions* ("Record every retained first-activation restriction with business rationale and reconsideration trigger"), R087 *CircleCI scope excluded* ("the user is handling it separately"), and R110–R114 which mark retired designs as history only — R111 "Two-provider coordination retired… **Do not reintroduce an invalid provider architecture**", R112 "Gate 2 certification retired", R113 "Retain prior Pro/Fable and GitHub review observations **without adopting their verdicts**", R114 "UNAUDITED register only". |

### Gaps and limits

- **PDFs not read.** `remediation/ACTUAL_FIGMA_MOCKS.pdf`, `ACTUAL_INSTALLED_BUILD.pdf`, and the Home `FINAL_CONNECTED_NATIVE_EVIDENCE.pdf` are visual evidence; their conclusions are already transcribed in the Markdown audits.
- **`COMPARISON.md` (1,692 lines / 332 KB) read only via cross-references** from A3 and A5 (e.g. "COMPARISON.md line 953, item F13"). It is a frame-by-frame comparison table, not an independent finding set; its findings appear in A1/A2.
- **Large supporting corpora skimmed, not exhausted:** `M1_REQUIREMENTS_AUDIT.md`'s 302-row review index (§"Row review index", lines 137–443) and the 49 `row-NN.md` reports in the Missions audit. The distinct-finding counts quoted are the documents' own reconciled totals.
- **`_artifacts/` volume.** `psagentspace/_artifacts` alone holds 8,034 recent Markdown/text files across ~597 run directories. Ranked keyword density was used to select; there may be additional per-run audits below the threshold.
- **Worktree duplication.** Each `psmobile-worktrees/*` checkout carries ~1,350 copies of the same repo documentation, so worktree-local search was scoped to files unique to a worktree.
- **The Missions V1.2 audit is a requirements-conformance audit, not a scope-creep audit.** Its 42 code gaps are "requirement not met", not "built something unrequested". It is included for the pedantic-section evidence and the fresh-agent-per-row method, not for overbuild findings.
- **Sheet row numbers shift.** The Missions sheet was re-sorted by priority on 2026-09-14 and a five-row lifecycle addendum was inserted; the row numbers above are as fetched on 2026-09-15. Use requirement labels, not row numbers, as the stable key.
- **Cluster D/E supporting corpora skimmed, not exhausted.** `2026-09-03-epic-16151-intent-audit.md` is 2,608 lines and `PRO-RESCOPE-REVIEW.md` / `FABLE-RESCOPE-REVIEW.md` are ~300 lines each; headline findings and verdicts were read, per-PR dispositions were not transcribed row by row. The CircleCI evidence tree is 2,679 files / 43 MB and was not opened beyond what E1 cites.
- **Cluster F is outside the 2026-08-25 window** (2026-08-20) and lives only in a worktree. It is included because it is the clearest recorded instance of driver 7 and because its worktree is still present.
- **Shared-worktree contamination is a proven false-positive source.** D2 and D3 both attributed a separate epic's scope creep to the epic under review purely because that epic's files were in the same workspace. Any watcher that infers scope from files on disk will make the same mistake; live issue hierarchy was what corrected it.
- **Nothing outside the named roots was searched.** `~/Documents/Codex/` (six dated directories) and `~/.codex/memories/epic-4926-continuation.md` were enumerated and checked but contain no qualifying audit; live-session evidence is covered by slices 01–05 of this research series.
- **`cjdev` / `cjdev-worktrees` were not searched.** The CircleCI audit cites source heads under `~/workspace/cjdev/worktrees/*` and `~/workspace/cjdev-worktrees/*` (109 and 7 directories respectively). These were outside the assigned roots and may hold additional per-PR audit material.
