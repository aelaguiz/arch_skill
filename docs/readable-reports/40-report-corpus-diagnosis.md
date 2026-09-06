# Report Corpus Diagnosis: Why Agent Reports Are Hard To Read

Date: 2026-09-06. Method: six real reports Amir received, read at a glance the way he
would read them. Every passage that forced a stop, a re-read or a guess was recorded
and classified. 63 passages were flagged across the six reports. Quotes from reports are
verbatim from the saved text files listed in each section. Quotes from Amir are verbatim
from `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/00-intent-and-notes.md`
(Amir, spoken, 2026-09-06). Anything marked "inference" is my reading, not a fact from a
source.

The bar, in Amir's words: "A really smart engineering-focused executive could read this
at a glance and understand it without having to drop everything and fully focus on every
single fucking word."

## The ten findings, ranked by how often they appear and how much they cost

1. **Undefined referents and internal-model words are the dominant mechanism.** 45 of the
   63 flagged passages need a word the report never defines: root, children, reset, signal,
   parity, band, lane, face, canon, offering, exact-owner, adversary, readout, GP, UA. The
   reader has to reconstruct the writer's model before the sentence means anything. This is
   the exact failure in the sentence Amir quoted. Example (morning priorities):
   "Checkout root now clean, children blocked."

2. **Telegraphic compression: dropped subjects, verbs and articles, joined by semicolons.**
   18 passages. The writer saves ten words and the reader pays for each one. This mechanism
   lives mostly in table cells and status rows, which is where the reader is scanning
   fastest. Example (morning priorities, Tim's row): "Reset running September 2/4; audience
   rebuilt; SDK finding and 8 ASO assets September 5."

3. **Bare codes and IDs with no plain-English name.** 18 flagged passages, and the counts
   behind them are large: the Morning Watch alone has 89 PR or issue numbers, 276 raw GitHub
   URLs, 295 mentions of its own "MW-" ids, 91 "FB-" rule ids and 62 commit hashes in one
   page. A number is a pointer, not a fact. Example (morning priorities): "#4792/#4807 open
   at 15:40, same code since September 2".

4. **Noun stacks.** 17 passages. Three to five nouns welded into one term that the writer
   coined during the work: "trigger-to-journey handoff", "no-terminal watchdog", "adjacent
   normalized-frame repeat rate", "campaign and signal recovery". Each one hides a whole
   sentence. Example (Android audit): "the inspected path has no bounded in-place recovery
   action if neither native nor canonical evidence arrives."

5. **The agent narrates its own process where the business fact should be.** 15 passages.
   Run ids, model names, the rules the agent followed, which sources it read, what it
   suppressed. This material is placed at the top of the page or inside the finding, so the
   reader wades through it to reach the point. Example (morning priorities, top of page):
   "Business outcomes first. Tasks last. Preserve continuity. GP is non-authoritative. Plans
   and decisions are not goals; no invented metric targets."

6. **Status labels with no mechanism.** 8 passages, but they sit exactly where a decision is
   made, so each one costs more than its count suggests. "Aligned; finish delivery." says
   neither what it is aligned with nor what delivery means. "clean" and "blocked" are GitHub
   merge-state values used as if they were English. "RECOVERED 2 of 3", "FIXED IN MAIN",
   "spend gate HOLDING" all need the writer's state machine. Example (morning priorities):
   "Settled Purchase parity AppsFlyer 5 / Meta 0; spend gate HOLDING."

7. **Symbols doing the work of sentences.** 10 passages. The morning priorities page uses
   25 arrows in 2,300 words; the Morning Watch uses "=" as a verb throughout ("= the reset
   event", "= FILED BY THE WATCH this run"). Slashes carry at least three meanings on one page:
   "of" (96/6,500), "versus" (AppsFlyer 5 / Meta 0) and "and" (September 2/4,
   purchase/signals). Example (morning priorities): "Profitable acquisition → campaign and
   signal recovery".

8. **Numbers with no comparison, no rate and no so-what, or too many facts in one
   sentence.** 12 passages (6 flagged for a missing comparison, 6 for sentences too long to
   hold, usually because numbers or references pile up). The reader is left to do the division. Example (morning priorities):
   "Paid D30 payer formation: 96/6,500 April →15/2,694 July" (the reader must compute 1.5
   percent to 0.6 percent). Contrast (Monday ops): "iOS converts 56.4% of started checkouts
   this week (79/140), a whisker under the spring's 58 to 66%."

9. **Mixed or unlabeled time zones.** 4 flagged passages, and one systemic case: the Morning
   Watch has 323 timestamps in "Z" form on one page, and the morning priorities report says
   its summary uses Chicago time but then writes "open at 15:40" (UTC) in the summary table
   while the same check is called "10:40" two sections later. Example: "#4792/#4807 open at
   15:40" beside "Final PR check: 10:40."

10. **Structure that hides the answer.** Headings that are labels ("Reproduction", "Status",
    "Lane") before the executive answer; a paragraph introduced as "What happened, in one
    line" that runs 174 words with four URLs; table cells that are fragment lists; and the
    same bug carrying a different name in each report. The 2.1.41 purchase bug is "the
    2.1.41 purchase blackout" (Morning Watch), "purchase-terminal repair" and "Success measurement
    is broken" (morning priorities), and "every 2.1.41 store purchase grants Plus but the app
    never recognizes it" (replay review). A reader who sees two of these does not know they
    are one thing.

Two observations that are not findings but matter for the skill:

- None of the six reports fails in the other direction. Zero passages talk down, explain
  the field or pad. Every flagged passage is on the dense side. The risk of over-correcting
  into "computers are like brains" is real, but it is not what the corpus shows today.
- The reports that read best (the Monday ops letter, the replay review, the executive answer
  of the Android audit, and the September 3 Meta ads report at
  https://share.fun.country/20260903-100ae3d3d04a/index.html) share four habits: full
  sentences with a subject and a verb; a number always next to its comparison; a term
  defined once at first use or replaced with plain words; and headings that state the
  message. The reports that read worst (Morning Watch, morning priorities) are the ones
  whose writers were also maintaining a state machine (ids, counters, labels) and let that
  machine's vocabulary into the prose.

## Per-report diagnosis

Order: the trigger report first, then the other five by how hard they were to read.

### Morning priorities, September 6, 2026

- URL: https://share.fun.country/20260906-763f8a326c72/index.html
- Saved text: `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/20260906-morning-priorities.txt`
- Saved HTML: `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/20260906-morning-priorities.html`
- Source in repo: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06.md

What it is trying to say, in plain English: This is the first daily "what should the company work on" report. Paid acquisition is broken and is priority one. The purchase and ad-signal fixes are written but not in a store build; get them shipped. Keep Tim's March-versus-now Meta campaign comparison honest. Fix the mission events Natasha needs before she can rebuild her lifecycle pushes. Joey (Home screen) and Justin (Play tab, tickets) are on track; let them finish and do not widen their scope. Phil should finish the ad cut he has. Five things need Amir: the two mission-event PRs have not changed since September 2; merged checkout fixes are still not in a store build; Tim's comparison may answer a different question than the one asked; pricing and the 18 free-tool ideas should stay in exploration; four disputed lesson answers and one Android graphics bug have no owner. The bottom half lists 21 data sources the agent read and what it could not read.

Confusing passages (22 flagged):

| Exact text | Mechanism | What the reader must know or guess | Plain rewrite |
|---|---|---|---|
| "Checkout root now clean, children blocked." | Telegraphic compression (dropped subject, verb or article); Undefined referent or internal-model word; Status label with no mechanism | That 'root' and 'children' are the bottom PR and the four PRs stacked on it, that 'clean' and 'blocked' are GitHub merge-state values, and which five PRs these are. | The bottom PR of the five-PR checkout repair stack (#5001, Android checkout cancellation explanation) had no conflicts and passing checks at 10:40 Chicago. The four PRs stacked on top of it (#5056 to #5059) still could not merge. |
| "Profitable acquisition → campaign and signal recovery" | Symbol standing in for a sentence; Undefined referent or internal-model word; Noun stack | That 'signal' means the purchase events the app sends to Meta and AppsFlyer (inference from the page's 'signal verifiers' and 'AppsFlyer 5 / Meta 0' rows), and that the arrow means 'this business outcome is served by this initiative'. | Goal: paid ads that make money. Work: restore the March campaign settings and fix the purchase events we send to Meta and AppsFlyer. |
| "Paid payer formation deteriorated; current purchase parity still fails. Campaign poisoning remains a hypothesis." | Undefined referent or internal-model word; Telegraphic compression (dropped subject, verb or article); Number with no comparison or so-what | What 'payer formation' is (share of paid installs who become payers), what 'purchase parity' is (AppsFlyer and Meta reporting the same purchase count), and that 'campaign poisoning' is a name for the theory that Meta learned from bad purchase signals (inference; the page never defines it). | Fewer paid installs turn into payers than in April. AppsFlyer and Meta still disagree on how many purchases happened. We still do not know whether bad purchase signals taught Meta to find the wrong people. |
| "Business outcomes first. Tasks last. Preserve continuity. GP is non-authoritative. Plans and decisions are not goals; no invented metric targets." | Agent process narration instead of the business fact; Telegraphic compression (dropped subject, verb or article); Undefined referent or internal-model word | That these are the rules the agent followed, not findings, and what GP is (the coverage table calls it a 57-tab workbook with team entries; what GP stands for is not stated anywhere on the page). | facts needed: confirm what GP stands for. Suggested: move this paragraph to the coverage section at the bottom, or cut it. |
| "Aligned; finish delivery." | Status label with no mechanism | Aligned with what (the ranked priorities above), and what 'delivery' means here (getting merged fixes into a store build). | This work matches priority 1. Next step: get the merged fixes into a store build. |
| "Reset running September 2/4; audience rebuilt; SDK finding and 8 ASO assets September 5." | Telegraphic compression (dropped subject, verb or article); Undefined referent or internal-model word; Table cell that is a fragment | That 'Reset' is the Meta campaign reset to March settings, what the 'SDK finding' was, and that 'ASO assets' are App Store screenshots and text. | facts needed: what the SDK finding was. Partial rewrite: Tim restarted the Meta campaigns on March settings on September 2 and 4, rebuilt the audience, and delivered 8 App Store listing assets on September 5. |
| "Push audience cleaned; difficulty copy rotated; broken triggers and first-lesson interruptions identified." | Telegraphic compression (dropped subject, verb or article); Table cell that is a fragment; Undefined referent or internal-model word | What 'difficulty copy rotated' means and which triggers are broken (the Customer.io mission triggers). | facts needed: what 'difficulty copy rotated' refers to. Partial rewrite: Natasha cleaned the push audience and found that the mission triggers in Customer.io are broken and that pushes interrupt the first lesson. |
| "#4792/#4807 open at 15:40, same code since September 2; Natasha still needs working events. No restored-campaign evidence." | Bare code or ID with no plain name; Mixed or unlabeled time zones; Telegraphic compression (dropped subject, verb or article) | What the two PRs do (send mission-completion events to Customer.io), and that 15:40 is UTC while the rest of the summary uses Chicago time. | The two PRs that send mission events to Customer.io (#4792 and #4807) are still open with no new code since September 2. Natasha cannot rebuild her campaigns until they ship. I found no evidence that the campaigns were restored. |
| "Pricing changes deferred until after UA;18 tools rows are modeling. PvP is an authorized bounded milestone." | Telegraphic compression (dropped subject, verb or article); Undefined referent or internal-model word; Agent process narration instead of the business fact | That UA means paid user acquisition, that '18 tools rows' are the 18 free-tool ideas in an SEO workbook, and what 'authorized bounded milestone' means in the agent's vocabulary. | Pricing changes wait until the paid-acquisition work is done. The 18 free poker tool ideas are still being sized, not built. Three-player poker is approved as a small, fixed-scope milestone. |
| "Four objections across two lessons need adjudication; individual owner unknown. New S25 review points at old graphics draft #3923." | Undefined referent or internal-model word; Bare code or ID with no plain name; Noun stack | That 'objections' are user complaints about lesson answers (inference; the row's source link is labeled 'Feedback'), that 'S25 review' is a Google Play review from a Galaxy S25 phone, and that #3923 is a draft PR for an Android graphics bug. | Users disputed four answers across two lessons and nobody owns the decision. A new Google Play review from a Galaxy S25 describes the Android graphics bug whose fix (#3923) has sat in draft since August. |
| "Paid D30 payer formation: 96/6,500 April →15/2,694 July; mature cohorts, partial attribution." | Number with no comparison or so-what; Symbol standing in for a sentence; Undefined referent or internal-model word; Stacked hedges | That D30 means 30 days after install, and the reader must do the division (1.5 percent to 0.6 percent) to see the size of the drop. | Of paid installs, 1.5 percent paid within 30 days in April (96 of 6,500). In July it was 0.6 percent (15 of 2,694). Attribution is incomplete, so some paid payers may be missing from both counts. |
| "29/29 initial store grants received Plus; zero expected client purchase completions." | Telegraphic compression (dropped subject, verb or article); Undefined referent or internal-model word; Inconsistent names for the same thing | That a 'store grant' is a purchase the store completed, that 'Plus' is the paid tier, and that 'client purchase completions' are the app's own record of a finished purchase. | All 29 people who bought through the store got Plus. The app recorded zero of those 29 as completed purchases, so our purchase counts and ad signals are wrong. |
| "Settled Purchase parity AppsFlyer 5 / Meta 0; spend gate HOLDING." | Undefined referent or internal-model word; Status label with no mechanism; Symbol standing in for a sentence | What 'purchase parity' compares (AppsFlyer versus Meta purchase counts, from the numbers themselves), and that the 'spend gate' is a rule about not raising ad spend (inference from the next sentence, 'Green liveness does not mean readiness to scale'). | AppsFlyer recorded 5 purchases and Meta recorded 0 for the same period. Ad spend stays where it is (inference on what HOLDING means). |
| "Readiness labels are separate from merge, release and observed customer behavior." | Agent process narration instead of the business fact; Undefined referent or internal-model word | That 'readiness labels' are GitHub labels like 'merge ready' and 'ufc-approved'. | A 'merge ready' label on a PR does not mean it is merged, shipped, or working for customers. |
| "Mtime alone not progress." | Telegraphic compression (dropped subject, verb or article); Undefined referent or internal-model word | That 'Mtime' is a file's last-modified time. | A file being edited recently does not mean the work moved forward. |
| "Authorship under Amir’s account is not a human assignment." | Agent process narration instead of the business fact | That agents open PRs using Amir's GitHub account. | PRs opened under Amir's GitHub account were mostly opened by agents, so they are not evidence of what Amir personally worked on. |
| "Staging/oldGP jobs sayok while output saysblocked." | Telegraphic compression (dropped subject, verb or article); Undefined referent or internal-model word | Which scheduled jobs these are and what 'ok' versus 'blocked' means for them. | facts needed: which jobs. Partial rewrite: Two scheduled jobs report success even though their output says they were blocked. |
| "Successful Google Play loaders still contain older data." | Undefined referent or internal-model word | That a 'loader' is a data import job. | The Google Play data import runs without errors but still brings in old data (downloads frozen at August 21). |
| "Where everyone’s work stands" | Heading that is a label, not a message | Nothing; this heading is fine. Included as a contrast: the row content under it is what breaks. | No change. |
| "Suggested GP deliveries" | Undefined referent or internal-model word; Heading that is a label, not a message | What GP is. | facts needed: what GP stands for. Suggested: 'What each person should deliver this week'. |
| "Frozen rage aggregate does not mean no live events." | Telegraphic compression (dropped subject, verb or article); Undefined referent or internal-model word | That 'rage' is the rage-tap metric and 'aggregate' is a cached summary. | The rage-tap summary has not updated, but that does not mean rage taps stopped. |
| "Comparison worksheets delivered; repair stacks moving." | Telegraphic compression (dropped subject, verb or article); Undefined referent or internal-model word | Which worksheets (the March-versus-now Meta comparison) and which stacks (the checkout PR stack and the puzzle PR stack). | Amir delivered the March-versus-now campaign comparison worksheets. The checkout and puzzle repair PR stacks are moving. |

### Morning Watch, September 6, 2026 (living daily release-health report)

- URL: https://share.fun.country/20260804-ede086c9eb57/index.html
- Saved text: `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/morning-watch-20260906.txt`
- Saved HTML: `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/morning-watch-20260906.html`
- Source in repo: the HTML is built from run files under `/Users/aelaguiz/workspace/psagentspace/_artifacts/morning-watch/runs/2026-09-06-1/` (leg-money.md, leg-product.md, leg-sentry.md, leg-stores.md, leg-trend-gh.md, parent-adjudication.md); no single source markdown. Rendered copy: `/Users/aelaguiz/workspace/psagentspace/_artifacts/morning-watch/report/index.html`.

What it is trying to say, in plain English: This is a daily release-health report that tracks about 40 open problems by id, each with a status and a three-day recovery counter. Sunday's message: Friday's backend and poker-engine deploy fixed four things at once (League standings errors, the three-player action refusals, the engine CPU burn, and the daily Play vs AI cap that had been off), and Play vs AI had its first normal day on Saturday. The worst item: on release 2.1.41, all 44 store purchases since launch are invisible to the app, 21 of those buyers were shown "cancelled" after paying, the fix is merged on main, and no new build exists to carry it. The data warehouse was repaired by hand on Saturday, but the nightly job still fails on a new check that nobody owns. After the three headlines come 14 sections of metrics, a list of signals the report chose not to raise, and a bug appendix. The page is 34,000 words.

Confusing passages (12 flagged):

| Exact text | Mechanism | What the reader must know or guess | Plain rewrite |
|---|---|---|---|
| "Morning Watch · run 2026-09-06-1 · full run · TWO closed days judged: Fri 2026-09-04 and Sat 2026-09-05 (no watch run fired on Saturday, so the team last heard from the watch at 12:15Z Sep 4) · generated 12:26 UTC · model: claude-fable-5-1 (parent and five sweep legs verified from session records; epics worker claude-opus-5 per FB-023)." | Agent process narration instead of the business fact; Bare code or ID with no plain name; Mixed or unlabeled time zones | That the run id, the model names, the 'sweep legs' and FB-023 are all about how the report was made, and that none of it changes the findings. | This report covers Friday September 4 and Saturday September 5. No report ran on Saturday. Written Sunday September 6 at 7:26am Chicago. (Move the model and run details to the bottom.) |
| "id minted: MW-068 (P2 WATCHING, activation v1 under band, Android-led, on the paid-UA wind-down cohorts: the Sep 3 mature cohort 43.6% on n=243 and the Sep 4 cohort 46.1% vs the 46.7 to 53.6 band; Android 2.1.41 40.1 / 43.7% vs iOS 56.1 / 52.6%; composition caveat carried)." | Bare code or ID with no plain name; Status label with no mechanism; Undefined referent or internal-model word; Number with no comparison or so-what; Stacked parentheticals | What 'activation v1' measures, what 'band' means (the normal range), that 'paid-UA wind-down' means we paused paid ads, and what a 'composition caveat' is. | New watch item: fewer new users are activating. 43.6 percent of September 3 installs and 46.1 percent of September 4 installs activated, under the normal 46.7 to 53.6 percent range. Android is worse (40 to 44 percent) than iOS (52 to 56 percent). Part of this is that the mix of users changed when paid ads were paused. |
| "MW-062 RECOVERED 0 of 3 held (check 2 not credited on the letter; not a relapse) MW-052 SPLIT: Leagues face DEPLOYED, puzzle face SAME MW-066 CLOSED (FIXED AND DEPLOYED, config) P1 residual PR OPEN x3: rustai #594 + psmobile #4995, psmobile #4892" | Telegraphic compression (dropped subject, verb or article); Bare code or ID with no plain name; Status label with no mechanism; Symbol standing in for a sentence; Undefined referent or internal-model word | The watch's own state machine (RECOVERED n of 3, SPLIT, 'face', 'credited on the letter'), plus what each MW id and PR number is. | facts needed: what 'check 2 not credited on the letter' means. Partial rewrite: The Play vs AI outage item is not yet counted as recovered. The League standings half of the entitlement bug is fixed and live; the puzzle half is not. The daily-cap item is closed. Three fix PRs for three-player poker are still open. |
| "What happened, in one line: at 18:02:30Z Sep 4 (1:02pm Central) Fly release v126 put Go backend decfcaee into production (release/2.1.41 plus the EV-free advice backport https://github.com/funcountry/psmobile/pull/4992 plus the restored legacy entitlement bridge = the mechanism the watch named for MW-052 on Sep 2, confirmed by the team's own root-cause doc), the RustAI engine moved 947f5dcf to 0e91d464" | Overlong sentence; Bare code or ID with no plain name; Symbol standing in for a sentence; Stacked parentheticals; Agent process narration instead of the business fact | Commit hashes, PR numbers, what the 'legacy entitlement bridge' is, and what MW-052 is. The sentence labeled 'one line' runs 174 words. | On Friday at 1:02pm Chicago we deployed a new backend and a new poker engine. The backend deploy restored the old entitlement path, which is what the watch said on September 2 would fix the League standings errors. The engine deploy fixed the three-player action bug and removed the CPU-heavy EV calculation. |
| "Leagues face: backend family 1Y ("read leaderboard entitlement") last fired 17:56:33Z Sep 4 on the old backend and is ZERO on decfcaee for 41 hours; the client leaderboard variant of 1EE is ZERO since 17:04Z Sep 4" | Bare code or ID with no plain name; Undefined referent or internal-model word; Mixed or unlabeled time zones | That 1Y and 1EE are Sentry error groups, that 'decfcaee' is the new backend build, and that 'face' means one of two symptoms of the same bug. | The leaderboard entitlement error has not fired since the deploy on Friday at 12:56pm Chicago, 41 hours so far. The matching client-side error also stopped. |
| "P1 MW-064 WORSE (count) roundup RANK 1 held on live cost FIXED IN MAIN (both halves), NOT SHIPPED psmobile #4922 CLOSED at the merge next-cut backlog 60 landings" | Telegraphic compression (dropped subject, verb or article); Status label with no mechanism; Bare code or ID with no plain name; Undefined referent or internal-model word | The watch's status vocabulary and that 'next-cut backlog 60 landings' means 60 merged changes are waiting for the next app release. | Priority 1, getting worse. The fix is merged on main but not in any store build. 60 merged changes are waiting for the next release. |
| "release-cut/2.1.41 is still the newest tag (git ls-remote 11:12Z), next-cut backlog 60 first-parent landings (18 on Sep 4 morning), Shorebird all-false day 15." | Telegraphic compression (dropped subject, verb or article); Undefined referent or internal-model word; Agent process narration instead of the business fact; Mixed or unlabeled time zones | Git tag naming, what a 'first-parent landing' is, and that 'Shorebird all-false' means no over-the-air patch has been sent in 15 days. | No new app release has been cut since 2.1.41. 60 merged changes are waiting. No over-the-air patch has gone out in 15 days. |
| "169 of 170 = 0.994 (Fri) · 127 of 130 = 0.977 (Sat)" | Number with no comparison or so-what; Symbol standing in for a sentence; Heading that is a label, not a message | That this is the share of new accounts that saw the onboarding paywall, and that the normal range is 0.93 to 1.01 (stated two lines later). | Nearly every new account saw the onboarding paywall on both days (99 percent Friday, 98 percent Saturday). Normal. |
| "Fixed and riding or deployed: MW-060 CLOSED (ANR class 3 of 3); MW-045 RECOVERED 2 of 3 (deeplink abandonment zero on both 2.1.41 builds with 55 to 66 served push taps a day); MW-057 1 of 3; MW-063 FIXED IN MAIN (https://github.com/funcountry/psmobile/pull/5022); MW-015 SAME at REOPENED-WORSE with four new iOS 2.1.41 init-failure groupings (appendix A4)." | Bare code or ID with no plain name; Status label with no mechanism; Telegraphic compression (dropped subject, verb or article) | The name behind every MW id (each is defined once, in the bug appendix about 30,000 words below), and the 'n of 3' recovery counter rule. | The Android startup freeze is closed after three clean days. The daily-puzzle deep-link fix has held for two days. The Play vs AI "game already ended" error has been zero for one day. The onboarding crash loop fix is merged but not shipped. The audio startup failure got worse on iOS 2.1.41 with four new error groups. |
| "Live artifact killed against canon: the paid-UA pacing row "Sep 5 Meta $20.08, -97.6% so far" = the one-load ordering artifact; canon Sep 5 Meta = $177.08." | Undefined referent or internal-model word; Symbol standing in for a sentence; Agent process narration instead of the business fact | That 'canon' is the modeled warehouse layer, that a 'live artifact' is a wrong number from a partial data load, and what 'one-load ordering' means. | Ignore the dashboard row that says Meta spend on September 5 was $20 and down 98 percent. That came from a partial data load. Actual Meta spend on September 5 was $177. |
| "0 / 11 / 0 and 0 / 3 / 0" | Table cell that is a fragment; Symbol standing in for a sentence | The column header ('Finished purchased / cancelled / error') and that the two groups are Friday and Saturday. | Friday: 0 bought, 11 cancelled, 0 errors. Saturday: 0 bought, 3 cancelled, 0 errors. |
| "9 rules suppressed or reframed a signal today (FB-001, FB-003, FB-006, FB-009, FB-010, FB-017/FB-019, FB-020, FB-024, FB-025); every one listed with what it withheld in What I did not report." | Agent process narration instead of the business fact; Bare code or ID with no plain name | That FB ids are feedback rules the watch applies to itself. | Cut from the top of the report. Keep in the 'What I did not report' section only. |

### Daily session replay review, September 6, 2026 (living page)

- URL: https://share.fun.country/replay-review-daily/index.html
- Saved text: `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/replay-review-daily-20260906.txt`
- Saved HTML: `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/replay-review-daily-20260906.html`
- Source in repo: run files under `/Users/aelaguiz/workspace/psagentspace/_artifacts/replay-review/runs/2026-09-06/` (summary.md, RUNLOG.md, corpus.local/); no single source markdown. Rendered copy: `/Users/aelaguiz/workspace/psagentspace/_artifacts/replay-review/report/index.html`.

What it is trying to say, in plain English: We watched 103 session recordings from a 48-hour window. Seven new things looked bad or odd: on Android the app dies mid-use and reboots to a different screen (3 cases, rare in the data); an iPhone checkout sat on "Checking purchase..." forever (1 case, now filed); an Indonesian price card mixes two number formats (filed); a new user failed to sign in four times with no visible message; a six-minute-old account ended on the welcome screen with no logout event; people tap close buttons four to six times; map nodes sit under the tab bar. Six more oddities are the app working as designed. Three known problems recurred, six known defects have fixes on main but not in a store build, and six items need a human with a time estimate for each. The rest is what the recordings cannot show and what was cut.

Confusing passages (7 flagged):

| Exact text | Mechanism | What the reader must know or guess | Plain rewrite |
|---|---|---|---|
| "Model anthropic/claude-fable-5-1 (orchestrator at thinking high, every child at thinking medium)" | Agent process narration instead of the business fact | Nothing a reader needs; it is how the report was made. | Move to the bottom of the page. |
| "Each is new to this review and survived the adversary re-check; where the adversary corrected a count or a reading, the corrected version is what is written here." | Undefined referent or internal-model word; Agent process narration instead of the business fact | That 'the adversary' is a second agent that tries to disprove each finding. | A second reviewer re-checked every item and corrected some counts. The corrected numbers are what you see. |
| "Counting cold starts whose device was in the foreground and active less than 60 seconds earlier, Android shows 32 of 1,024 cold starts (about 3 percent) and iOS 17 of 942 (about 2 percent) in the window (react_production.splash_seen against activity and lifecycle events)." | Overlong sentence; Bare code or ID with no plain name | That the parenthetical is a warehouse table name and can be skipped. | About 3 percent of Android cold starts and 2 percent of iOS cold starts happened within a minute of the app being active. So the app dying mid-use is rare and not only an Android problem. (Table: react_production.splash_seen.) |
| "The engineering pass, low to medium confidence: the label stays until the store SDK answers (plan_billing_screen.dart lines 72 and 499, subscription_purchase_service.dart line 747, on the 2.1.41 branch at 9cf34215); whether the store ever called back cannot be told from our side; RevenueCat customer history for that app user would settle it." | Bare code or ID with no plain name; Stacked hedges; Overlong sentence | That file names and line numbers are for an engineer who will open the code, and that the finding is: the button waits forever for the store. | The button says 'Checking purchase...' until the App Store answers. We cannot tell from our side whether the store ever answered. RevenueCat's record for this user would settle it. (Code: plan_billing_screen.dart lines 72 and 499.) |
| "fix current subscription identity before plan changes (psmobile #5012) (merged 2026-09-05 into a stacked branch, not main); preserve current subscription identity before plan changes (psmobile #5043) (merged 2026-09-06 into a stacked branch, not main); the same, restacked (psmobile #5058) (open)." | Bare code or ID with no plain name; Undefined referent or internal-model word; Inconsistent names for the same thing | That three PR numbers are the same fix moved between branches, and what a 'stacked branch' is. | The fix exists (PR #5058) but is not on main yet. Two earlier copies of the same fix were merged into side branches, not main. |
| "12 of 18 store-cancel sessions in the window log the paywall opened and removed 8 to 10 times inside one second right after the cancel, then a No Thanks 1 to 3 seconds later (react_production.paygate_result with terminal_source_event = 'route_disposed'); the person sees one screen." | Overlong sentence; Bare code or ID with no plain name | That the 8 to 10 open-and-remove events are a logging burst, not something the user sees. | When someone cancels at the store sheet, the app logs the paywall opening and closing 8 to 10 times in one second. The person sees one screen. The extra rows are a logging problem, not a user problem. |
| "Every sample was a seeded random draw from the full recording list for its population; the one followed thread is labeled and kept out of the counts." | Agent process narration instead of the business fact; Undefined referent or internal-model word | What 'the one followed thread' is (one user followed across sessions on purpose). | We picked recordings at random. One user we followed on purpose is labeled and not counted. |

### Monday operational status, August 31, 2026 (weekly ops report)

- URL: https://share.fun.country/20260831-5086c8f814c9/index.html
- Saved text: `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/monday-ops-20260831.txt`
- Saved HTML: `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/monday-ops-20260831.html`
- Source in repo: `/Users/aelaguiz/workspace/psagentspace/_artifacts/2026-08-31-monday-update/` (DRAFT_EMAIL.md, PROBLEM_LEDGER.md, CONTAMINATION_MAP.md, RECEIPTS.md; rendered page under share/). Not opened for this diagnosis.

What it is trying to say, in plain English: A weekly letter to the team. The Play vs AI paid tier went live to everyone. iOS checkout conversion is back near spring levels (56 percent), so the screens are no longer the problem; Android converts 21 percent on the same screens, so the gap is in the traffic mix. Best gross revenue week of the six tracked ($1,242), record checkout starts, most trial starts in the series. Day-1 retention fell for a third week and a new dashboard exists to study it. Three self-inflicted incidents: a deleted feature flag killed mission credit for two days; the push-tap dead-end fix did not work at scale; the backend cutover broke app start for 7 percent of users for a day. Cost per new payer is improving but still nine times the target.

Confusing passages (8 flagged):

| Exact text | Mechanism | What the reader must know or guess | Plain rewrite |
|---|---|---|---|
| "The push-tap dead-end got worse, not better: the shipped fix did not survive scale (record 544 events, 92 people, Saturday). It needs an owner this week." | Undefined referent or internal-model word; Noun stack | That 'push-tap dead-end' means someone taps a push notification and lands nowhere useful. | More people than ever tapped a push notification and landed nowhere (544 times, 92 people, Saturday). The fix we shipped did not work at full volume. Someone needs to own this this week. |
| "The retention ladder shipped; its first job is unifying what counts as an action (onboarding vs not, lessons vs puzzles) before the 2-vs-3 day target locks." | Undefined referent or internal-model word; Noun stack | That the 'retention ladder' is a new dashboard that relates active days in week one to whether a user returns, and that '2-vs-3 day target' is an undecided goal. | The new retention dashboard is live. Before we pick a goal (two or three active days in the first week), we need one definition of 'active' that treats onboarding, lessons and puzzles the same way. |
| "The onboarding readout's repair window closes Sep 5; fixing its assignment coverage this week keeps that arm read available." | Undefined referent or internal-model word; Noun stack; Telegraphic compression (dropped subject, verb or article) | Experiment vocabulary: 'readout', 'assignment coverage', 'arm read'. | The onboarding A/B test can only be judged if we fix its tracking by September 5. Today only 68 percent of users are recorded in an arm; the bar is 99.5 percent. |
| "Cohort return on ad spend, net of refunds: the Aug 17 install cohort returned 6.7 cents per spend dollar by day 7 ($404.40 on $6,064.07), the best day-7 read in six cohorts (the Jul 6 week ran 8.8 cents; the weeks between ran 0.5 to 4.8); Aug 10 reads 5.0 cents at day 14 ($278.71 on $5,628.98); Jul 27 stays the series' worst at 0.7 cents through day 28." | Overlong sentence; Number with no comparison or so-what; Stacked parentheticals | Which of the many numbers is the point (day-7 return is the best in six weeks but still under 7 cents on the dollar). | For every ad dollar spent the week of August 17, we got back 6.7 cents within 7 days. That is the best week-one return in six weeks, but still tiny. Older weeks: 0.5 to 8.8 cents. |
| "purchase attribution stays blind, so the class split rides the install lineage" | Undefined referent or internal-model word; Noun stack | That we cannot tie purchases to campaigns, so we guess by which campaign the install came from. | We cannot tie purchases to ad campaigns right now, so we assign each payer to the campaign that brought the install. |
| "The data-contract check is green five straight days: the identity-coverage red was adjudicated Wednesday (the drifting all-time anchor demoted to informational with the rationale written into the check; the stable anchor still blocks and passes at 73.8%)." | Undefined referent or internal-model word; Noun stack; Stacked parentheticals | What a data-contract check is, what the two 'anchors' are, and why one was demoted. | facts needed: what the two anchors measure. Partial rewrite: The nightly data check has passed five days in a row. One of its two identity tests kept failing on old data and was made a warning; the other still blocks and passes at 73.8 percent. |
| "The January home-tab split is still running unread (about 7,800 users split 50/50 this week; no readout lane; second consecutive edition flagged): decide it or kill it." | Undefined referent or internal-model word; Agent process narration instead of the business fact | That 'readout lane' means there is no dashboard that can score the test. | An A/B test on the home tab has run since January with about 7,800 users a week in it, and nothing can score it. Decide it or kill it. |
| "The Meta checkout-event family stays dark by design (day 35, zero steering impact)." | Undefined referent or internal-model word; Telegraphic compression (dropped subject, verb or article) | That we deliberately stopped sending checkout events to Meta 35 days ago, and 'steering' means Meta's ad targeting. | We stopped sending checkout events to Meta 35 days ago on purpose. It has not changed how Meta targets our ads. |

### Android monetization audit, September 1, 2026

- URL: https://share.fun.country/20260901-3e8e184c94c8/index.html
- Saved text: `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/android-monetization-audit-20260901.txt`
- Saved HTML: `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/android-monetization-audit-20260901.html`
- Source in repo: `/Users/aelaguiz/workspace/psagentspace/_artifacts/2026-09-01-android-monetization-replay-audit/share/index.html` (HTML only; no markdown source found beside it).

What it is trying to say, in plain English: Why does Android convert checkouts so much worse than iOS on the last two releases? Because Android users cancel far more often (66 percent of Android checkout starts versus 39 percent on iOS). Paywalls load fine 99 percent of the time. There are three narrow real defects (the price list occasionally never loads; error messages are inconsistent and once showed raw internal text; "Checking purchase..." can wait indefinitely with only a back arrow), plus real gaps in our purchase reporting. Even fixing every error would only move Android from 21 to 25 percent. Do not treat this as a systemic outage. The open question is why Android users cancel at the Google Play sheet, which recordings cannot see.

Confusing passages (7 flagged):

| Exact text | Mechanism | What the reader must know or guess | Plain rewrite |
|---|---|---|---|
| "Status: Reproduced by direct production observation." | Agent process narration instead of the business fact; Heading that is a label, not a message | That the report opens with a method template (Reproduction, Lane, Evidence lane) before the answer, so the reader scrolls to find 'Executive answer'. | Move 'Executive answer' and 'Decision' to the top. Put the method after. |
| "One production lesson-energy paygate showed only app-owned “Loading plans…” UI for roughly 8 to 10 seconds before the player backed out; no offering-ready event followed." | Undefined referent or internal-model word; Noun stack | That a 'lesson-energy paygate' is the paywall shown when a player runs out of energy in a lesson, and 'offering' is RevenueCat's word for the price list. | One player hit the out-of-energy paywall, saw 'Loading plans...' for 8 to 10 seconds, and backed out. The prices never loaded. |
| "Release source contains a 10-second no-terminal watchdog that can put the paywall into “Checking purchase…” with its primary CTA disabled. A late result can resolve it, but the inspected path has no bounded in-place recovery action if neither native nor canonical evidence arrives. This is a credible recovery risk, not a replay-proven indefinite foreground hang." | Noun stack; Stacked hedges; Undefined referent or internal-model word | 'no-terminal watchdog', 'bounded in-place recovery action', 'native nor canonical evidence', 'replay-proven indefinite foreground hang'. | If the store does not answer within 10 seconds, the paywall shows 'Checking purchase...' and disables the buy button. If the answer never comes, the player has no way out except the back arrow. We did not see anyone stuck this way on video, but the code allows it. |
| "Deployed and analyzed source: Android 2.1.39 at 7144eb88f79865d5e07264d48a48f9a9f1fe70b5; Android 2.1.40 and the detached audit worktree at f77a39bc1a53c5dadb5a664f2eadaa2264fda723." | Bare code or ID with no plain name | Nothing; full 40-character commit hashes are for a footnote. | Code audited: the Android 2.1.39 and 2.1.40 release builds. (Commits in the appendix.) |
| "The search of /Users/aelaguiz/workspace/psagentspace/REGRESSIONS.md found the existing RevenueCat offering-stall class, the Android purchase-not-allowed class, the exact-owner entitlement-bootstrap class, and the Android trial-copy mismatch class." | Bare code or ID with no plain name; Undefined referent or internal-model word; Noun stack | Four internal bug-class names, including 'exact-owner', which is a RevenueCat lookup term. | We already track four related bug types in the regressions ledger: price list stalls, Google Play 'purchase not allowed' errors, the entitlement lookup failure at startup, and wrong trial copy on Android. This audit adds evidence to those. |
| "One showed an internal exact-owner entitlement message in a player-facing puzzle error surface." | Undefined referent or internal-model word; Noun stack | 'exact-owner entitlement message'. | One player saw a raw internal error message about their subscription on the puzzle error screen. |
| "The zero is signal-parity or attribution coverage failure, not zero product conversion." | Undefined referent or internal-model word; Noun stack | 'signal-parity' and 'attribution coverage'. | The dashboard shows zero paid Android purchases because attribution is broken, not because nobody bought. |

### Max Responsive Coaching program review, August 21, 2026 (PR delivery report)

- URL: https://share.fun.country/20260821-859dee7c9687/index.html
- Saved text: `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/max-responsive-coaching-program-review-20260821.txt`
- Saved HTML: `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/max-responsive-coaching-program-review-20260821.html`
- Source in repo: not listed in SHARES.md; the page cites /Users/aelaguiz/workspace/psagentspace/plans/drafts/2026-08-20-max-responsive-coaching-iteration-plan.md as its plan

What it is trying to say, in plain English: Two PRs are ready to merge. The first is a tool that plays coached poker matches automatically to generate test data. The second proves a measure-change-verify loop for how the AI coach ("Max") talks. Max repeats the same sentence frame because our own code feeds the model the same instruction sentence every time; the model echoes it 98 percent of the time. Varying that one sentence across four wordings cut back-to-back repetition by 31 to 41 percent on held-out sessions with no loss in accuracy. Amir needs to do a 15-minute blind read of 20 session pairs, approve and merge the two PRs in order, and hold one discussion about the test data before the next phase starts.

Confusing passages (7 flagged):

| Exact text | Mechanism | What the reader must know or guess | Plain rewrite |
|---|---|---|---|
| "First sealed-set win: -38% median adjacent repetition" | Undefined referent or internal-model word; Noun stack; Number with no comparison or so-what | 'sealed set' (held-out test data), 'adjacent repetition' (the same sentence frame in back-to-back coaching lines). | First proven win: Max repeats the same sentence frame back to back 38 percent less often, measured on held-out sessions. |
| "ufc-approved + merge on PR #4278 then PR #4295 (stacked)" | Bare code or ID with no plain name; Symbol standing in for a sentence; Status label with no mechanism | That 'ufc-approved' is a GitHub label Amir applies after checking user-facing changes, and what each PR is. | Add the ufc-approved label and merge the fixture runner PR (#4278) first, then the outro skeleton PR (#4295), which is built on it. |
| "Session corpus (158 sessions, salted tune/check split), parity gate, repetition scorer, paired A/B bench, one pre-registered wording treatment with a sealed-set verdict" | Noun stack; Table cell that is a fragment; Undefined referent or internal-model word | Five pieces of eval machinery named by internal shorthand. | A test set of 158 coached sessions split into tune and check halves, a check that the offline and live game engines agree, a scorer for repeated sentence frames, an A/B comparison tool, and one pre-registered wording change judged on the check half. |
| "The owner table settled it as an identity, not a correlation: the repetition is authored by our own deterministic renderer, not chosen by the model." | Undefined referent or internal-model word; Noun stack | What the 'owner table' is (a table tracing each repeated output sentence to the input that caused it) and what 'identity' means here (every case, not most). | We traced every repeated sentence to its cause. In every case, our own code fed the model the same instruction sentence. The model did not choose to repeat; we told it to. |
| "Pre-registered before the sealed CHECK set was opened: target = adjacent normalized-frame repeat rate, showdown family; bar = median at or below 0.2961 (10 percent better than control) with same-direction improvement in all three repeats." | Symbol standing in for a sentence; Noun stack; Undefined referent or internal-model word | The metric definition and the pass rule. | Before looking at the check set we wrote down the pass rule: the back-to-back repeat rate in showdown coaching must drop at least 10 percent (median at or below 0.296) and improve in all three runs. |
| "One Groq 503 out of 1,560 bench calls made the literal "100 percent accepted" leg read 259/260, so the mechanical verdict file honestly says REVERT." | Bare code or ID with no plain name; Undefined referent or internal-model word; Agent process narration instead of the business fact | That Groq is the model host, 503 is a server error, and the 'verdict file' is a script output. | One of 1,560 model calls failed with a server error, so the automated pass check technically says REVERT. The failed call re-ran clean. We ruled the guardrail passed. |
| "Corpora discussion (gates the next phase): split ratios and the run-identity key; per-family size targets given the 37-distinct-situations fact; whether headless "accepted" stands in for "displayed"; blessing the salt so the benchmark freezes; surface order for treatment two (the model-invented "He had better" headline residue is queued first)." | Noun stack; Undefined referent or internal-model word; Overlong sentence | Every clause is a decision that needs its own background: run-identity key, salt, treatment two, headline residue. | facts needed: the options behind each decision. Suggested: list each decision as its own line with a one-sentence explanation of what it changes. |

## Frequency table across all six reports

63 flagged passages; most carry more than one mechanism, so the counts add to more than 63. Count = number of flagged passages showing that mechanism.

| Mechanism | Count | Example (report) |
|---|---|---|
| Undefined referent or internal-model word | 45 | "Checkout root now clean, children blocked." (morning priorities) |
| Telegraphic compression (dropped subject, verb or article) | 18 | "Checkout root now clean, children blocked." (morning priorities) |
| Bare code or ID with no plain name | 18 | "#4792/#4807 open at 15:40, same code since September 2; Natasha still needs working events. No restored-campaign evidence." (morning priorities) |
| Noun stack | 17 | "Profitable acquisition → campaign and signal recovery" (morning priorities) |
| Agent process narration instead of the business fact | 15 | "Business outcomes first. Tasks last. Preserve continuity. GP is non-authoritative. Plans and decisions are not goals; no invented metric ..." (morning priorities) |
| Symbol standing in for a sentence | 10 | "Profitable acquisition → campaign and signal recovery" (morning priorities) |
| Status label with no mechanism | 8 | "Checkout root now clean, children blocked." (morning priorities) |
| Number with no comparison or so-what | 6 | "Paid payer formation deteriorated; current purchase parity still fails. Campaign poisoning remains a hypothesis." (morning priorities) |
| Overlong sentence | 6 | "What happened, in one line: at 18:02:30Z Sep 4 (1:02pm Central) Fly release v126 put Go backend decfcaee into production (release/2.1.41 ..." (Morning Watch) |
| Table cell that is a fragment | 4 | "Reset running September 2/4; audience rebuilt; SDK finding and 8 ASO assets September 5." (morning priorities) |
| Mixed or unlabeled time zones | 4 | "#4792/#4807 open at 15:40, same code since September 2; Natasha still needs working events. No restored-campaign evidence." (morning priorities) |
| Heading that is a label, not a message | 4 | "Where everyone’s work stands" (morning priorities) |
| Stacked parentheticals | 4 | "id minted: MW-068 (P2 WATCHING, activation v1 under band, Android-led, on the paid-UA wind-down cohorts: the Sep 3 mature cohort 43.6% on..." (Morning Watch) |
| Stacked hedges | 3 | "Paid D30 payer formation: 96/6,500 April →15/2,694 July; mature cohorts, partial attribution." (morning priorities) |
| Inconsistent names for the same thing | 2 flagged, plus one cross-report case | The 2.1.41 purchase bug is "the 2.1.41 purchase blackout" (Morning Watch), "purchase-terminal repair" and "Success measurement is broken" (morning priorities), and "every 2.1.41 store purchase grants Plus but the app never recognizes it" (replay review) |

Mechanism density by report (flagged passages per 1,000 words, from the saved text files):

| Report | Words | Flagged passages | Per 1,000 words | Notes |
|---|---|---|---|---|
| morning priorities | 2,338 | 22 | 9.4 | 25 arrows; 18 PR or issue numbers; time zones mixed in the summary |
| Morning Watch | 34,334 | 12 | 0.3 | 276 raw GitHub URLs; 323 "Z" timestamps; 295 MW-id mentions; 91 FB-id mentions; 62 commit hashes; 286 capitalized status words |
| replay review | 8,237 | 7 | 0.8 | 37 PR or issue numbers, each with a plain title beside it; warehouse table names in parentheses |
| Monday ops | 9,791 | 8 | 0.8 | 3 PR numbers; dense number paragraphs; experiment vocabulary |
| Android audit | 4,725 | 7 | 1.5 | method template before the answer; two 40-character commit hashes; internal bug-class names |
| coaching program review | 1,069 | 7 | 6.5 | 17 PR or issue numbers; eval-machinery shorthand |

The per-1,000-words column understates the Morning Watch. I flagged its patterns, not every instance; its 34,000 words repeat the same six mechanisms on every line.

## What reads well, and why

Ten passages that read at a glance, with the habit that makes each one work.

1. "If you read only this box, you have the week; every number's backing table is in the appendix at the bottom." (Monday ops)
   Why it works: Tells the reader what to read and where the proof is, in one sentence. The reader can stop after the box.

2. "The verdict: iOS converts 56.4% of started checkouts this week (79/140), a whisker under the spring's 58 to 66%." (Monday ops)
   Why it works: A rate, its raw counts, and the comparison that gives it meaning, all in one line. Nothing to compute.

3. "A production flag is code, and deleting one needs the same discipline as deleting code." (Monday ops)
   Why it works: A lesson stated as a plain rule. Subject, verb, no jargon, no hedge.

4. "Android underperformed mainly because many more checkout starts ended in cancellation, not because paywalls broadly failed to load." (Android audit)
   Why it works: One-sentence answer that names the cause and the ruled-out cause. This is the sentence the whole audit exists to deliver, and it is findable under a heading called "Executive answer".

5. "This looks bad: on Android the app dies while the person is using it and comes back on the "Checking for Updates" boot screen, somewhere else" (replay review)
   Why it works: A heading that is a message. The reader knows what happened before reading the body, and the severity word comes first.

6. "I checked the data: rare, and not clearly an Android thing." (replay review)
   Why it works: The so-what comes first; the counts follow in the next sentence. The reader can skip the counts and lose nothing.

7. "Do the blind read (15 min, 20 session pairs, no wrong answers)." (coaching program review)
   Why it works: A request with its time cost and a reassurance. The reader knows what is being asked and how long it takes.

8. "This is a dependency stall, not personal inactivity." (morning priorities)
   Why it works: Pre-empts the wrong conclusion about a person in seven words. This is the same report as the trigger sentence, so the writer can do it.

9. "the 2.1.41 purchase blackout is now 44 of 44 (both stores, monthly and annual), 21 of those buyers were shown "cancelled" after paying, the fix has been in main since Friday 16:19Z, and about 14 user-facing fixes are stranded behind a 2.1.42 cut that does not exist" (Morning Watch)
   Why it works: Long, but every clause is a full plain fact with a number and a consequence. Compare it with the status line right under it in the same report ("P1 MW-064 WORSE (count) roundup RANK 1 held..."), which says less in the same space.

10. "A few words I use throughout, defined once:" (Meta ads report, September 3)
   Why it works: The September 3 Meta ads report (https://share.fun.country/20260903-100ae3d3d04a/index.html, not saved in the samples folder) defines eight terms at the top (install, ad spot, tap rate, Fish King 2 and so on) and then uses them freely. Every later sentence in that report reads at a glance because of this one block.

The pattern across all ten: a subject and a verb; the number next to its comparison; the
consequence in the same sentence as the fact; and terms either defined once or replaced with
the plain thing they stand for. None of them is short for its own sake. The Morning Watch
example is 47 words.

## Case study: "Checkout root now clean, children blocked."

Amir, verbatim (source: `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/00-intent-and-notes.md`, 2026-09-06): "I'm looking at this and it says, 'checkout route now, clean, children blocked.' I don't know what the fuck that means. I could parse it if I had to. I could be like, 'Okay we're talking about something about the checkout.' I don't know what we're talking about, but I know there are checkout issues. What's the root? Does it mean the root PR, like children issues, right?"

His guess was right. It should not have needed a guess.

### Where the sentence sits

The line is in the "Where everyone's work stands" table, in the row for Amir. Full cell, verbatim from `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/20260906-morning-priorities.txt`: "Comparison worksheets delivered; repair stacks moving. Checkout root now clean, children blocked. Aligned; finish delivery." The row describes Amir's own work, to Amir, and he still could not read it. That rules out "the reader lacks context" as the explanation. The sentence is the problem.

The same fact appears twice more on the page and once in the source markdown, in three different forms:

- "Needs Amir's attention" table: "Stores show 2.1.41; purchase-terminal repair merged. Checkout root #5001 now clean; #5056–#5059 blocked."
- "Delivery state at 10:40 Chicago" section: "Checkout root #5001 was clean; downstream #5056–#5059 were blocked."
- Source markdown, "Reconciliations that changed the report" table (`/Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06.md`): "Agent says checkout stack is conflicted; final GitHub root is clean. | Keep real progress: #5001 clean at 15:40; four children still blocked. Report integration friction without repeating a superseded root-conflict claim."

So the writer knew the PR numbers, knew there were exactly four children, knew the time of the check, and knew that an earlier agent had reported a conflict that was no longer true. None of that reached the sentence Amir read.

### Where the words came from

The source markdown links the cell to `2026-09-06/sources/github/final-status.json` (full path: `/Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/github/final-status.json`), collected at 2026-09-06T15:40:31Z, which is 10:40am Chicago. That file records, for five open PRs in funcountry/psmobile:

| PR | Title | mergeStateStatus at 15:40Z |
|---|---|---|
| #5001 | Explain Android checkout cancellations with bounded attempt evidence | CLEAN |
| #5056 | fix(checkout): release confirmed access while storage settlement waits | BLOCKED |
| #5057 | fix: retain checkout-initiating app version on subscription commits | BLOCKED |
| #5058 | fix: preserve current subscription identity before plan changes | BLOCKED |
| #5059 | fix: settle original subscription transactions after renewal | BLOCKED |

"clean" and "blocked" are GitHub's `mergeStateStatus` values copied into prose. CLEAN means GitHub will allow the merge: no conflicts, required checks passing. BLOCKED means GitHub will not allow the merge right now; the JSON does not say why.

"root" and "children" come from the PR bodies. PR #5001's body (read with `gh pr view 5001 --repo funcountry/psmobile`, 2026-09-06) opens: "Epic #4818 implementation root. This PR is the root of the exact dependent checkout repair chain: #5001 → #5056 → #5057 → #5058 → #5059." Each child PR's body says "Exact dependency: #5001 → #5056" and so on. So the five PRs are a stack: #5001 targets main; #5056 targets #5001's branch; #5057 targets #5056's branch; and so on. Epic #4818 is titled "Epic: Make the monetization path correct, fully instrumented, and independently reconcilable". Issue #4823, which #5001 implements, is titled "[Measurement] Explain Android native-checkout cancellations without inventing Google Play intent".

Inference: the four children were BLOCKED because each targets the branch below it rather than main, and a repository rule was unmet on those targets; the usual reading of a stacked PR in this state is "waiting for the one under it to merge". The report's own data does not state the reason, and neither do the PR bodies.

### What happened next

Live state on 2026-09-06 (read with `gh pr view` on each number; nothing was modified): all five PRs are MERGED, with mergedAt between 17:04:23Z and 17:04:27Z, which is 12:04pm Chicago. Every one carried the labels "ufc-approved" and "merge ready", and every check (buildkite/psmobile-pr-ci, user-facing-gate, pr-agent-review) passed. So the sentence was true at 10:40am and stale by lunch. The report never said what "blocked" was waiting on, so the reader could not tell whether the stall would clear itself in an hour or needed him.

### What the sentence actually means, in plain English

Five checkout-repair PRs are stacked on top of each other. As of 10:40am Chicago on September 6, the bottom one (#5001, which adds data explaining why Android users cancel at checkout) could be merged. The four fixes stacked on it (#5056 to #5059: grant Plus access before storage settles, record the right app version on a purchase, keep the current plan identity before a plan change, settle the original transaction after a renewal) could not be merged yet. None of the five were in a store build; the stores were still serving 2.1.41. All five merged at 12:04pm the same day.

### Why the original fails, mechanism by mechanism

- "Checkout root": a noun stack whose second word is stacked-PR jargon. No article, no verb.
- "now clean": a GitHub enum used as an adjective. "Clean" in English means something else.
- "children blocked": a second piece of stacked-PR jargon plus a second GitHub enum, with no count, no names, and no reason.
- No consequence. The reader cannot tell whether this is good news, bad news, or nothing.
- The status label that follows ("Aligned; finish delivery.") does not repair it; it adds a third undefined term.

### Candidate rewrites

At three lengths. Each one is true to the JSON and the PR bodies; the last one includes the inference about why the children were blocked, marked as such.

1. Short (table cell, 15 words): "Checkout repair stack: the base PR can merge; the four fixes above it are waiting."

2. One sentence (38 words): "The five stacked checkout-repair PRs are close: the base one (#5001, explains Android checkout cancellations) can merge now, the four fixes above it (#5056 to #5059) cannot merge yet, and none of them are in a store build."

3. Three sentences (for the "Needs Amir's attention" row): "The checkout repairs are written but not shipped. Of the five stacked PRs, the base one (#5001) passed checks and can merge; the four fixes above it (#5056 to #5059) are waiting, most likely on the base merging first (inference; GitHub reports them as blocked without a reason). The stores still serve 2.1.41, which has none of these fixes, so the next step is to merge the stack and cut a build."

Any of the three would have let Amir read the row without stopping. The first fits the same table cell as the original; it is nine words longer and needs no guess.

## Appendix: method, corpus and limits

### Corpus

| Report | Kind | URL | Saved text |
|---|---|---|---|
| Morning priorities, September 6 | daily company priorities (the trigger report) | https://share.fun.country/20260906-763f8a326c72/index.html | `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/20260906-morning-priorities.txt` |
| Morning Watch, September 6 | daily release-health watch (living page) | https://share.fun.country/20260804-ede086c9eb57/index.html | `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/morning-watch-20260906.txt` |
| Replay review, September 6 | daily session-recording review (living page) | https://share.fun.country/replay-review-daily/index.html | `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/replay-review-daily-20260906.txt` |
| Monday ops, August 31 | weekly operational status letter | https://share.fun.country/20260831-5086c8f814c9/index.html | `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/monday-ops-20260831.txt` |
| Android monetization audit, September 1 | investigation report | https://share.fun.country/20260901-3e8e184c94c8/index.html | `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/android-monetization-audit-20260901.txt` |
| Coaching program review, August 21 | PR delivery report | https://share.fun.country/20260821-859dee7c9687/index.html | `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/max-responsive-coaching-program-review-20260821.txt` |

Each saved `.txt` file is a plain-text extraction of the HTML saved beside it (same name, `.html`). The first line of each `.txt` records the URL and fetch date. Report URLs were taken from `/Users/aelaguiz/workspace/psagentspace/SHARES.md`. The living pages (Morning Watch, replay review) redeploy in place, so the saved copies are the September 6 state and the URLs may show something newer.

### How passages were chosen

I read each report top to bottom once at reading speed, not study speed, and marked every place I stopped, went back, or had to guess a word's meaning. Then I classified each stop. For the Morning Watch I marked patterns rather than every instance; the page is 34,000 words and repeats the same mechanisms on nearly every line. Every quoted passage was checked as an exact substring of the saved text file (whitespace normalized), or of the source markdown for two morning-priorities passages whose HTML rendering breaks a word across an inline element ("96/6,500 April →15/2,694 July", "spend gate HOLDING").

### Rewrites

A rewrite is given only where the underlying fact is stated somewhere in the same report or in the GitHub data read for the case study. Where it is not, the cell says "facts needed" and names the missing fact. No rewrite invents a number, a cause or a date.

### What this diagnosis does not cover

- It does not judge whether the reports are correct. It judges whether they can be read.
- It does not cover visual layout, color or typography. Only words.
- The "reads well" contrast report on Meta ads (https://share.fun.country/20260903-100ae3d3d04a/index.html) was read but not saved to the samples folder, to keep the sample count at the five requested.
- The writing skill Amir referred to ("There are skills in PS Agent space for how I do writing, which I find very understandable", same source as above) is likely `/Users/aelaguiz/workspace/psagentspace/skills/human-writing/SKILL.md` and its neighbors (`copy-editing`, `copywriting`, `brand-voice`). I read the human-writing skill in full. It covers vocabulary (banned words, em dashes, hedges), paragraph length and tone, and it says "Trust the reader's intelligence" and "Don't over-explain obvious points". It does not address undefined referents, bare codes, telegraphic compression, status labels or symbols, which are the mechanisms above. One line in it ("Include occasional sentence fragments") points the other way from finding 2 if read without care. That gap is what the new skill has to fill.
