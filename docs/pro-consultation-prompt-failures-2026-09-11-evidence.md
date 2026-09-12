# Pro consultation prompt audit: evidence appendix

Collected September 11, 2026. Display times are America/Chicago (CDT); original UTC timestamps and source JSONL line numbers are retained. These are authored prompt strings extracted from actual tool calls, not prompts reconstructed from the agent’s claims. A composer call alone is not proof of successful submission. C01 and C02 additionally have submitted-message readback. Repeated fill attempts are not counted as separate consultations.

[Read the findings](pro-consultation-prompt-failures-2026-09-11.md).

## C01: First SNG campaign results

Clear overconstraint: the requested concise parent summary became a capped Pro answer; the attachment also freezes the experiment ladder.

**Source:** `home`, session `01a0906a-c125-7c43-b500-e38ed4dfda31`, September 11, 2026, 15:58:18 CDT. Original UTC: `2026-09-11T20:58:18.552Z`.

**Exact source anchor:** `/home/aelaguiz/.codex/sessions/2026/09/11/rollout-2026-09-11T07-21-50-01a0906a-c125-7c43-b500-e38ed4dfda31.jsonl:8335`.

```text
Now read the attached brief. Interpret the measured #680 campaign as a peer research reviewer. Return only the requested five bullets; do not invent additional runs.
```

### The actual user request

Same session, line 5989, `2026-09-11T18:02:25.354Z`.

> All right I want you to run that campaign, then take the results back to Pro, have Pro interpret them, and then I want you to show me the results and the interpretation concisely.

### The attached brief

The retained `pro_input.md` matches the prompt and evidence referenced by the submitted message. Its creation is recorded at source line 8143; the complete file is reproduced to expose instructions hidden outside the composer.

```markdown
# HU SNG #680 full control campaign: Pro interpretation brief

## Ask
Interpret the measured results below as a peer research reviewer. Give a concise diagnosis of what the campaign establishes, what it does not establish, and the single next experiment that best removes the remaining ambiguity. Do not claim causality from one campaign. Separate direct evidence from hypotheses. Pay attention to seat asymmetry, the paired confidence intervals, the evaluator contract, the E10/E60 direction, and the `es_opponent_read_fallbacks` counter. Explain whether the result points more toward the SNG shell/payoff/stack accounting or toward the learner/geometry. Do not propose broad new machinery.

## Exact campaign
- Remote VM: `nlhe-training-96`, `us-central1-b`, 96 vCPU, kept running.
- Code: `c1ce737b39a39c7cc7054a194527f4b6944035c6`, branch `codex/hu-sng-680-controls`.
- K200 asset: canonical digest `b933eca1dfff311b835e0cde7056bec4d2e2a3b9118eca0eab2c5ead581c41de`.
- Training seed: C100 `68020260911`; C75 `68020260912`.
- Evaluation seed: `5668206826306682`.
- 6 x 600-second epochs per arm; E10 is epoch 1; E60 is final epoch.
- 30,000 LocalBR hands per checkpoint and seat, 1,000 rollouts, same deal corpus SHA256 `382c197f752233cc1f905d5ac4d4d437d55a16c630d43293f91e1731a0aaa9de`.
- C100 is 200/200 cash, 1/2 blinds, direct chip reward.
- C75 is 1500/1500 reset HU WTA SNG, 10/20 blinds, fixed opening root, current ICM/WTA payoff.

## Training receipts
- C100 final: 144,093,262 traversals/iterations, 6 epochs, no training error; E10 checkpoint exported.
- C75 final: 138,672,040 traversals, 65,683,710,515 regret updates, 18,244,854.5 regret updates/s, 188,749,222 final rows, no training error; `es_opponent_read_fallbacks=94,061,931`; E10 checkpoint exported.
- C75 per-epoch regret updates/s: E10 18,158,628.6; E20 18,226,175.9; E30 18,199,773.6; E40 18,225,882.5; E50 18,243,064.6; E60 18,244,854.5.

## LocalBR marginal results (avg exploiter mBB; lower is better)
| arm | checkpoint | seat 0 | seat 1 |
|---|---:|---:|---:|
| C100 | E10 | 290.37 +/- 277.00 | 267.30 +/- 277.37 |
| C100 | E60 | 106.23 +/- 260.24 | 425.77 +/- 259.51 |
| C75 | E10 | -116.96 +/- 234.77 | 154.20 +/- 234.92 |
| C75 | E60 | 58.31 +/- 225.55 | 75.55 +/- 223.39 |

All eight LocalBR evaluations had `errors=0` and `fallbacks_total=0`.

## Paired E60 minus E10 LocalBR results
Negative means E60 is less exploitable/better.

### C100 cash
- seat 0: `-184.13 +/- 253.24 mBB` (n=30,000)
- seat 1: `+158.47 +/- 256.81 mBB` (n=30,000)
- combined: `-12.83 +/- 178.67 mBB` (n=30,000)

### C75 SNG
- seat 0: `+175.27 +/- 210.57 mBB` (n=30,000)
- seat 1: `-78.65 +/- 213.02 mBB` (n=30,000)
- combined: `+48.31 +/- 148.83 mBB` (n=30,000)

The paired JSON says `n=30000` for combined because each row pairs the two seat-specific results by the same hand corpus; report the seat-specific and combined values exactly as shown.

## CallBot lineup results
These are raw `hero_net_bb` means from 30,000 rows, computed from each lineup's `rows.jsonl`; they are not LocalBR and are a secondary control.

| arm | mean hero net BB | 95% CI |
|---|---:|---:|
| C100 E10 vs call-bot | +3.350 | +/-0.283 |
| C100 E60 vs call-bot | +3.200 | +/-0.260 |
| C75 E10 vs call-bot | +2.862 | +/-0.244 |
| C75 E60 vs call-bot | +2.903 | +/-0.230 |

## Required output
Return no more than 5 bullets:
1. result in one sentence;
2. strongest evidence;
3. what remains unresolved;
4. best causal interpretation with confidence level;
5. one next experiment, keeping the baseline ladder intact.

```

### What the visible Pro response did

Source line 8403 contains submitted-message readback, the attachment name, “Worked for 4m 28s,” and five response sections matching the requested fields. It identifies measurement limits, confounding, and a matched-geometry control. The following excerpts are from that visible answer, not the parent’s summary.

> Result: #680 establishes executable controls and useful play against CallBot, but neither a resolved E10→E60 LocalBR improvement nor a resolved SNG-specific deterioration—and therefore neither a learning-curve success nor a plateau.

> What remains unresolved: The opposing seat directions partly cancel, and the direction reverses between arms; these are unresolved seat-specific changes, not proof of a physical-seat bug or a genuine seat tradeoff. The data cannot distinguish a small learning effect, improvement mostly before E10, insufficient training duration, or limited LocalBR sensitivity. CallBot profitability demonstrates elementary capability, not improvement between checkpoints—the brief supplies no paired CallBot-difference interval. Near-zero or negative LocalBR returns do not establish equilibrium: Brown’s thesis describes LocalBR as a heuristic, restricted-response measure of exploitability. Nor does this fixed-opening campaign establish changing-stack or complete-SNG strength.

> One next experiment: Complete the missing matched-geometry 75BB cash baseline, before adding root diversity or changing depth buckets: one direct-chip cash trajectory at 1,500/1,500 chips and 10/20 blinds, retaining the frozen K200/solver/averaging recipe, 96 workers, C75’s training-seed setting, and the existing six-epoch E10/E60 schedule. Compare it with the retained C75 SNG checkpoints using the same paired corpus and matched effective LocalBR execution rules, not just the same seed. Estimate the difference between their E60−E10 changes directly; do not infer a difference because one arm is significant and the other is not. This removes depth and chip-scale differences from the shell comparison. A resolved adverse SNG-relative change would implicate the SNG-specific pipeline collectively—not ICM alone; an unresolved comparison leaves the baseline question open rather than advancing the ladder.

## C02: Corrected SNG consultation

Improved prompt: expressly allows plan changes, discarded controls, alternatives, and an answer in Pro’s own structure. Only submission and interim response are established in the captured window.

**Source:** `home`, session `01a0906a-c125-7c43-b500-e38ed4dfda31`, September 11, 2026, 16:32:24 CDT. Original UTC: `2026-09-11T21:32:24.628Z`.

**Exact source anchor:** `/home/aelaguiz/.codex/sessions/2026/09/11/rollout-2026-09-11T07-21-50-01a0906a-c125-7c43-b500-e38ed4dfda31.jsonl:8722`.

```text
Read the attached working-state document as the complete current evidence for the HU SNG deconfounding investigation. Treat this as a peer research review, not a task-extraction request. Independently assess what the first C100/C75 campaign actually establishes, what it cannot establish, whether our current causal ranking is sensible, and whether the matched 75BB cash control now running is the right next move. Tell us how these results should change the plan, what assumptions or proposed controls you would discard or reorder, what alternative experiment you would choose if better, and what each candidate result would teach us. Challenge our framing where warranted, distinguish evidence from hypotheses, and account for the seat asymmetry, paired intervals, CallBot check, evaluator limits, and the C75 opponent-read fallback counter. Give a complete research judgment in your own structure. Do not force five bullets, do not merely restate the document, and do not lead yourself toward our proposed conclusion.
```

### Recovery scope

The user requested holistic re-prompting at source lines 8634 and 8671. The agent added a five-part consultation rule to its working document at line 8642. The new composer at line 8722 explicitly frees response structure and plan choice. At line 8748, the browser body includes the new submitted prompt and this interim message:

> I’ll separate measured effects from causal claims, then judge what the running 75BB control can resolve and which proposed controls add little information.

The same read reports `stop: false` while the visible body still contains “Stop answering.” The body establishes ongoing response activity; that boolean alone is not a completion signal. This audit does not claim the corrected final review had completed.

## C03: SNG campaign design

Structured planning request with permission to challenge the baseline. Structure alone does not establish a failure.

**Source:** `home`, session `01a0906a-c125-7c43-b500-e38ed4dfda31`, September 11, 2026, 07:53:33 CDT. Original UTC: `2026-09-11T12:53:33.771Z`.

**Exact source anchor:** `/home/aelaguiz/.codex/sessions/2026/09/11/rollout-2026-09-11T07-21-50-01a0906a-c125-7c43-b500-e38ed4dfda31.jsonl:435`.

```text
Read the attached HU_SNG_DECONFOUNDING_EPIC_BRIEF.md and treat it as a peer research request. Independently design the full deconfounded campaign as an epic with ordered subissues, hypotheses, controls, acceptance evidence, stop/continue rules, compute budgets, risks, and definition of done. Challenge the candidate baseline where needed. Do not implement code or create GitHub issues yet; return the complete plan for parent review.
```

## C04: SNG implementation-stack review

A scoped code and integration review. Its required evidence and PR-specific questions suit that job; they should not be carried into an open research interpretation by default.

**Source:** `home`, session `01a0906a-c125-7c43-b500-e38ed4dfda31`, September 11, 2026, 10:13:34 CDT. Original UTC: `2026-09-11T15:13:34.171Z`.

**Exact source anchor:** `/home/aelaguiz/.codex/sessions/2026/09/11/rollout-2026-09-11T07-21-50-01a0906a-c125-7c43-b500-e38ed4dfda31.jsonl:2714`.

```text
Peer review request for the implementation stack that follows your earlier HU SNG deconfounding plan.

Review the actual GitHub diffs and issue context for this dependency-ordered stack:
- #678 / PR #692: https://github.com/funcountry/rustai/pull/692 — commit e99b16dbdf — freezes the verified cash reference contract.
- #679 / PR #693: https://github.com/funcountry/rustai/pull/693 — commit 71f32ed918 — runs the 4,096-block cash/SNG/WTA differential.
- #680 / PR #694: https://github.com/funcountry/rustai/pull/694 — commit 866ca125b4 — adds the paired 100BB cash / 75BB HU SNG learning-control runner.

Treat this as a peer architecture and correctness review, not a request to implement code. The intended method is the brutally deconfounded baseline: freeze the cash reference, prove the cash/SNG/WTA same-hand differential, then compare training duration under matched dials while adding no new abstraction assumptions. The #680 runner must fail closed until the sanctioned K200 card abstraction is available; it must not silently substitute an artifact. Full controls have not been run because that asset is not hydrated.

Give a final review of:
1. whether the three PRs form the correct dependency order and faithfully implement the deconfounding mandate;
2. any correctness, scope, or reproducibility blockers in the actual diffs;
3. whether each PR is merge-ready after CI, and whether the stack should proceed to the next conditional experiment;
4. the smallest concrete repair for every blocker.

Do not merge, release, deploy, create issues, or invent extra machinery. State clearly what evidence is still missing.
```

## C05: Prior SNG reset decision

Useful counterexample: gives the original goal, evidence, competing experiments, an explicit third-option escape, and a complete-answer request.

**Source:** `home`, session `01a0820d-9a9d-74e1-83a7-22c6beff29ff`, September 10, 2026, 16:39:32 CDT. Original UTC: `2026-09-10T21:39:32.126Z`.

**Exact source anchor:** `/home/aelaguiz/.codex/sessions/2026/09/08/rollout-2026-09-08T12-25-24-01a0820d-9a9d-74e1-83a7-22c6beff29ff.jsonl:18558`.

```text
We reset the HU SNG delivery goal after an independent Claude Fable xhigh cold review found partial drift. Please challenge the next decision, not merely agree.

North star: a credible full-domain HU winner-take-all SNG blueprint that improves usefully with materially more training toward roughly 6–7 hours. Amir requires back-to-basics, incremental scale, and residual LocalBR exploitability is expected. A 15→60 minute gain exists; useful improvement beyond one hour is still unproved. Do not treat unresolved intervals as plateaus or as permission to repeat short diagnostics forever.

Completed evidence:
- T60→T120 live SNG: LocalBR unresolved, candidate win-rate +0.26 pp with 95% CI [-0.67,+1.19].
- W60–120 output-window policy versus T120: +19.8 ±28.380334679 chips LocalBR (negative favors W), candidate win-rate -0.66 ±0.946011156 pp; unresolved.
- W versus T120 CallBot is worse at 50/100: -307.6225 ±132.188738905 mbb/hand, and at 100/50: -116.895 ±115.981795316. W is also worse versus T60 at 50/100. W is evaluation-only, derived from the T trajectory, not an independent training run. Its output-window explanation should not be chained into another window search.
- The repeated 50/100 regression and earlier state-sharing witnesses leave stack/depth strategy-row sharing as the leading untested representation hypothesis.

Two candidate next experiments:
A. One unchanged live-SNG trajectory trained to 240 minutes with retained 60/120/240 checkpoints; evaluate all checkpoints on one fresh common panel plus the five existing CallBot roots, primary 240 versus 60. This directly tests the multi-hour learning requirement and uses existing checkpoint support.
B. A general stack/depth-sharing representation ablation with horizon and recipe held fixed. This directly tests the leading abstraction hypothesis but does not answer whether the current recipe improves with more training.

Read the attached prior evidence and the current plan/mission context. Choose which is the smallest next discriminating experiment, or explain why a third option is better. Give:
1. recommendation and why it changes a product/training decision;
2. exact hypothesis, comparison, sample size/evaluator, and stop/continue rule;
3. what result would justify extending toward 6–7 hours versus switching to the representation ablation;
4. risks of confusing evaluator precision, undertraining, or abstraction harm;
5. any correction needed in our reset goal or live plan.

Do not propose another panel, approval layer, broad parameter grid, or arbitrary quality threshold. This is a planning consultation only; do not launch a run. Return a complete answer with a short decision record the parent can paste into the canonical plan.
```

## C06: Prior SNG four-hour result

Mixed: explicitly invites challenge, but supplies a chosen boundary, frozen recipe, evaluation design and stop rules before asking for judgment. The prior user request did support incremental experiments, so not every restriction is invented.

**Source:** `home`, session `01a0820d-9a9d-74e1-83a7-22c6beff29ff`, September 11, 2026, 06:41:02 CDT. Original UTC: `2026-09-11T11:41:02.271Z`.

**Exact source anchor:** `/home/aelaguiz/.codex/sessions/2026/09/08/rollout-2026-09-08T12-25-24-01a0820d-9a9d-74e1-83a7-22c6beff29ff.jsonl:20148`.

```text
@GitHub Review the current PR626 source and the bounded HU WTA SNG plan against this result. North star: a credible full-domain heads-up winner-take-all SNG blueprint with useful improvement toward roughly 6–7 hours; residual LocalBR exploitability is expected and is only comparative evidence. Fresh H60/H120/H240 completed validly on one trajectory: 935,559,498 source traversals, 467,779,749 logical blocks, 319,937,742,032 regret updates, 30,012 complete SNG matches and 300,480 reset hands. Primary H240-H60 was -13.2 chips, 95% CI [-42.741,+16.341], n=5,000; H120-H60 -22.2 [-49.950,+5.550]; H240-H120 +9.0 [-18.088,+36.088]. This is unresolved, not a plateau, so no unchanged six-hour run. Proposed smallest next test: one X60/X120 trajectory with exactly one representation change, insert effective-depth boundary 50 into the existing (40,75] bucket, all source/solver/K200/seed 20260913/96 workers/24x300s otherwise fixed. Compare X120-H120 complete-SNG LocalBR on existing 5,000 paired blocks; negative favors X. Mechanism check: opening-root per-hand LocalBR plus a 32-hand mechanics check; secondary: the five existing CallBot roots. Stop: U<0 and no resolved CallBot collapse adopts split; L>0 closes hypothesis; unresolved does not add seeds or samples and asks Amir before expansion. Challenge whether boundary 50 is the right single ablation, whether the metrics and opening-root owner are valid, whether there is a smaller better test, and what code/tests are required before launch. Read the actual repository through GitHub where needed. Do not launch or edit; return one concrete recommendation.
```

## C07: Payments architecture planning

Useful counterexample in the composer: challenges the proposed abstractions and allows scope and acceptance changes. It is still necessary to review the attached plan as part of the prompt.

**Source:** `local`, session `01a08300-bf72-7610-869f-8caf2915cd2b`, September 08, 2026, 17:04:16 CDT. Original UTC: `2026-09-08T22:04:16.743Z`.

**Exact source anchor:** `/Users/aelaguiz/.codex/sessions/2026/09/08/rollout-2026-09-08T16-50-59-01a08300-bf72-7610-869f-8caf2915cd2b.jsonl:518`.

```text
@GitHub Review the attached payments/paygates Patrol architecture and issue set for funcountry/psmobile. Independently challenge scope, duplication, authority boundaries, and coverage holes, especially returning users and failure paths where AppsFlyer, Meta, or RevenueCat data can be lost or falsely emitted. Recommend the smallest coherent implementation architecture, identify any issue split or acceptance changes needed, and state the critical path for making the suite merge-ready. Do not assume the proposed abstractions are correct.
```

## C08: Payments final review and retry

Limiting language added during retry: after an Internal Server Error, the prompt changes to “Assess only” four checks and a short table. It retains the named acceptance issues and an any-material-source-defect check, so this does not by itself prove lost review coverage. This is a code-review example, not evidence that every checklist is inappropriate.

**Source:** `local`, session `01a08300-bf72-7610-869f-8caf2915cd2b`, September 08, 2026, 18:53:44 CDT. Original UTC: `2026-09-08T23:53:44.720Z`.

**Exact source anchor:** `/Users/aelaguiz/.codex/sessions/2026/09/08/rollout-2026-09-08T16-50-59-01a08300-bf72-7610-869f-8caf2915cd2b.jsonl:3543`.

```text
Perform the final independent source and acceptance review for the payments/paygates Patrol epic #5374.

Current implementation heads:
- #5383 returning-account failure boundaries: 0f349062ba
- #5384 helper reuse: f037821ab1
- #5389 provider delivery recovery: 65aa3234c7
- #5282 native purchase/Restore/renewal parent: 1410c05165
- #5283 five paygate entries: c7f063373d
- #5291 native value arms: be9b6f7ea8
- #5290 registration receiver evidence is merged at its documented boundary.

The final review must inspect the current PR/source state and the attached architecture plan, not rely on prior verdicts. Check whether the latest #5383 listener capture actually proves the unresolved returning-account state before automatic recovery, and whether #5389 now composes real AppsFlyer and Meta sinks with file-backed SQLite, account replacement, persisted pending-provider ownership, original diagnostics, and no replay of completed providers. Check for second payment authority, generic runner, duplicated observation/correlation logic, provider retry ownership mistakes, and false claims about local sink completion versus receiver acceptance.

Audit every named issue acceptance in #5276, #5277, #5278, #5279, #5286, #5288, #5375, #5376, and #5377. Keep native Apple/Google device runs, iOS five-entry coverage, six native value outcomes, clean-state Restore, original-after-renewal, and installed returning-user recovery open if the evidence is absent. A green host check or Test Store run cannot substitute for those boundaries. Report findings first, classify each item as proven, incomplete, or unverified, and identify the smallest concrete repair for any material defect. Do not give a merge-ready verdict unless all acceptance evidence supports it. No merge, release, production mutation, or real charge.
```

**Source:** `local`, session `01a08300-bf72-7610-869f-8caf2915cd2b`, September 08, 2026, 18:58:14 CDT. Original UTC: `2026-09-08T23:58:14.959Z`.

**Exact source anchor:** `/Users/aelaguiz/.codex/sessions/2026/09/08/rollout-2026-09-08T16-50-59-01a08300-bf72-7610-869f-8caf2915cd2b.jsonl:3667`.

```text
Retry the final review with a concise findings-first answer. Use the current GitHub heads, not the old quoted review:
#5383 0f349062ba, #5384 f037821ab1, #5389 65aa3234c7, #5282 1410c05165, #5283 c7f063373d, #5291 be9b6f7ea8, and merged #5290.

Assess only:
1) Does #5383's listener capture prove the exact unresolved returning-account state before automatic recovery, and does its delayed A→B→A test admit then reject a stale result?
2) Does #5389's file-backed SQLite test use real AppsFlyer and Meta sinks, retain original occurrence/account/diagnostics, persist only the failed provider, and avoid replaying completed providers?
3) For #5276/#5277/#5278/#5279/#5286/#5288/#5375/#5376/#5377, classify each acceptance as proven, incomplete, or unverified. Native Apple/Google execution, five iOS paygate entries, six native value outcomes, clean-state Restore, original-after-renewal, and installed returning-user recovery must stay open if absent.
4) Identify any material source defect or second authority/generic runner/false provider-success claim.

Do not call the epic merge-ready unless all required evidence is actually present. Return a short table and a final verdict. No merge, release, production mutation, or real charge.
```

### Retry context

Between these prompts, source line 3656 contains the visible message “Internal Server Error.” The retry is authored at line 3667. That establishes that the wording and response format changed during error recovery; it does not establish lost coverage or that the shorter wording fixed the server error.

## C09: Payments targeted source repair

Appropriate narrow follow-up: asks whether a named defect was fixed while keeping unrun acceptance open. The conclusion is explicitly limited to that repair.

**Source:** `local`, session `01a08300-bf72-7610-869f-8caf2915cd2b`, September 08, 2026, 19:13:04 CDT. Original UTC: `2026-09-09T00:13:04.337Z`.

**Exact source anchor:** `/Users/aelaguiz/.codex/sessions/2026/09/08/rollout-2026-09-08T16-50-59-01a08300-bf72-7610-869f-8caf2915cd2b.jsonl:4049`.

```text
Follow-up source review only for the repair just pushed:
- #5282 parent: f6da47cba4
- #5384 propagated stack: 4aff640b85

Inspect the exact native_restore_purchases_test.dart diff. Confirm whether the contradictory post-Restore lock/Plus-required assertions are now correctly replaced by unlocked, usable Plus-content assertions, and whether exact subscriber/product/period, explicit Restore, and zero-acquisition coverage remain intact. Check that #5384 still contains only the intended helper adoption plus this parent correction and that no shared purchase assertion was lost. Give a short PASS or findings verdict for this source repair. Keep all unrun Apple/Google/native and installed provider acceptance explicitly open. No merge, release, production mutation, or real charge.
```

## C10: Payments major architecture decision

Closed choice: asks Pro to select A or B and does not expressly permit another architecture. Some limits concern genuine authorization or existing design ownership; the risk is presenting the caller’s solution space as exhaustive.

**Source:** `local`, session `01a08300-bf72-7610-869f-8caf2915cd2b`, September 08, 2026, 19:25:42 CDT. Original UTC: `2026-09-09T00:25:42.315Z`.

**Exact source anchor:** `/Users/aelaguiz/.codex/sessions/2026/09/08/rollout-2026-09-08T16-50-59-01a08300-bf72-7610-869f-8caf2915cd2b.jsonl:4468`.

```text
Major architecture decision for the same payments Patrol epic. Current audit found no safe way to prove OS process death for a native pending checkout with existing owners: the payment Patrol target arms the pending state in-process, the existing scripts/sim controller can force-stop but has no payment checkpoint, app.snapshot does not expose the pending checkout row, and Android Test Orchestrator clearPackageData destroys persistence. The existing #5292 stopped-process controller is therefore not directly reusable without adding a sanitized pending readback plus a host-visible arm/force-stop handshake. Separately, Money workflow 34291870994 ran all four Android Money cases but all failed before payment assertions at Flutter NavigatorState._updateHeroController null-check during signed-out onboarding remount; this is an auth/onboarding owner issue now documented on #5381. Please decide the smallest acceptable architecture: (A) add the two narrow existing-owner seams and reuse the existing force-stop controller to prove pending obligation across process death, or (B) explicitly defer this boundary as a separate #5377 acceptance gap and preserve the no-new-runner rule. Also confirm whether the #5381 HeroController repair should block rerunning Money evidence. Do not propose a generic runner, second payment authority, production mutation, provider mutation, merge/release, or real charges. Give a concise decision with exact acceptance wording and whether a new issue/PR is warranted.
```

## C11: Provider-loss prevention architecture

Concise composer with permission to challenge overbuild and proof boundaries. Included as a structured planning comparison, not labeled a failure.

**Source:** `local`, session `01a082fd-81a5-7041-a7ec-86a89f75d358`, September 08, 2026, 16:58:19 CDT. Original UTC: `2026-09-08T21:58:19.394Z`.

**Exact source anchor:** `/Users/aelaguiz/.codex/sessions/2026/09/08/rollout-2026-09-08T16-47-27-01a082fd-81a5-7041-a7ec-86a89f75d358.jsonl:395`.

```text
@GitHub Review the attached provider-patrol-epic-pro-brief.md and give the architecture and issue-set decision for this data-loss prevention Patrol epic. Challenge overbuild and identify any acceptance that Patrol cannot honestly prove. Return concrete prioritized child boundaries for implementation.
```

## C12: Provider final epic review

Structured source/acceptance review. A per-PR verdict is appropriate here; calling it broad research interpretation would overstate its scope.

**Source:** `local`, session `01a082fd-81a5-7041-a7ec-86a89f75d358`, September 08, 2026, 17:51:14 CDT. Original UTC: `2026-09-08T22:51:14.226Z`.

**Exact source anchor:** `/Users/aelaguiz/.codex/sessions/2026/09/08/rollout-2026-09-08T16-47-27-01a082fd-81a5-7041-a7ec-86a89f75d358.jsonl:1513`.

```text
@GitHub Final epic review for #5374. Review the completed stack against the attached architecture and current source at origin/main ab33dd140f: PR #5385 fd8d7b1f7e6e7ac7ed9b544c6d76856368afac1f (shared occurrence observations), PR #5389 feec96d399 (mixed-provider queue/restart recovery), plus existing PRs #5383, #5384, #5282, #5283, #5290, and #5291. Judge whether the thin shared layer preserves real AppsFlyer/Meta/RevenueCat ownership, whether the acceptance correctly distinguishes durable recording, native handoff, provider response/readback, RevenueCat state, logical commit cardinality, and Unknown timeout outcomes, and whether any code or test boundary is duplicated, overclaims Patrol proof, or leaves a material data-loss gap. Return: (1) merge-readiness verdict per PR, (2) material findings ordered by severity, (3) exact repairs required before merge, (4) what remains outside Patrol proof. Do not ask for merge/release.
```

## C13: Morning Money Suite reliability

Useful goal-preserving composer: asks why the recurring failure happens, seeks a durable plan, and permits challenging the provisional diagnosis. The original attached brief was not retained at its temporary path, so this case supports a claim about the composer only.

**Source:** `local`, session `01a08671-01c4-7d21-bb7c-5d9d4d01be21`, September 09, 2026, 09:05:51 CDT. Original UTC: `2026-09-09T14:05:51.935Z`.

**Exact source anchor:** `/Users/aelaguiz/.codex/sessions/2026/09/09/rollout-2026-09-09T08-52-28-01a08671-01c4-7d21-bb7c-5d9d4d01be21.jsonl:439`.

```text
Read PRO_BRIEF.md and use GitHub to inspect current funcountry/psmobile source. Explain why the daily Money Suite keeps failing and propose the smallest durable plan that makes it reliable and its morning Slack useful, including how to stop recurrence before merge and how to handle existing repair PRs. Challenge the provisional diagnosis and scope where needed. Return the plan and issue acceptance here only; make no GitHub or other external changes.
```

## Instruction-loading evidence

In the current SNG session, line 5995 attempted to load the skills from `~/.codex/skills`; line 5998 reports that the path does not exist. The agent corrected the path to `~/.agents/skills` at line 6004. Line 6007 returns all three entries (`prompt-authoring`, `chatgpt-web`, and `browseros`) with no actual tool-output truncation warning. The returned text includes the anti-heuristic guidance and actual-populated-brief requirement. This repaired path error did not prevent the agent from receiving the relevant rules.

At the time of this audit, the home-server entries matched the inspected
repository copies exactly. The later combined revision is tracked in the
[improvement plan](chatgpt-web-consultation-improvement-plan-2026-09-11.md).

| Skill | SHA-256 | Entry lines |
| --- | --- | ---: |
| chatgpt-web | `c47bee0f5e9a9146a197e60deadf64981b1a587a23c9aff58c9712cb69630be9` | 167 |
| prompt-authoring | `0304cf1c11b9f180de7e459f979e269beae26eda1c286af3976b52be8c8f51f8` | 121 |

## Coverage and retention

The audit indexed recent Codex metadata on Amir-M5 and home, then inspected seven selected exact rollouts: the five parent sessions represented here, a solver-history continuation (`01a08175-9f5e-7322-9230-2380c173befc`), and an iOS rollout-readiness investigation (`01a09187-9edc-74d3-9536-3ea5cf37f876`). The last two did not add a direct Pro prompt case to this appendix. Session selection used named workstreams and the September 4–11 activity window, rather than a recursive home-directory search. Historical content inside those selected sessions was followed where relevant.

The discovery index contained 1,107 local and 291 home Codex rows in the named project families, including child sessions. Those are metadata candidates, not 1,398 reviewed conversations and not a denominator for a failure rate. Thirteen consultation episodes from five parent sessions are documented here; C08 includes both the original and retry wording. The set deliberately contains positive and mixed examples.

Additional agent-history lookups found no matching Prime sessions for home’s rustai project or Claude sessions for the local psagentspace project in the same seven-day window. This is a bounded search result, not proof that those runtimes never use Pro. The behavioral findings are about the reviewed Codex traces.

Temporary extraction receipts are in `/tmp/pro-consultation-audit-20260911`. The current SNG snapshot ends around 21:33 UTC, so it does not establish the later outcome of its corrected consultation. This appendix preserves the prompt text and exact source anchors even if temporary files are cleaned later. Full historical browser responses and every historical attachment were not independently re-fetched.
