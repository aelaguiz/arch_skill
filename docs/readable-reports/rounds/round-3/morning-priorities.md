# Morning priorities: September 6, 2026

**Put acquisition recovery first by releasing the purchase and attribution repairs, completing Tim’s March comparison and restoring Natasha’s lifecycle triggers.**

All times are Chicago. September 6 is Sunday; the weekly recommendations cover September 7–13, and each teammate’s next work session means their next working day. Keep Joey’s and Justin’s retention work moving.

## Acquisition recovery ranks first; keep retention work moving

The recommended order follows the acquisition priority you stated on September 5: [“I need the business to acquire customers profitably, period.” (FC message 64711)][direction].

| Rank | Outcome | Priority and reason |
|---|---|---|
| 1 | Make acquisition profitable. | Restore the intended campaign settings and repair purchase signals. Paid installs are producing fewer payers, and AppsFlyer and Meta still disagree on purchases. The September 3–5 acquisition focus remains current. Campaign poisoning remains a hypothesis. |
| 2 | Increase LTV. | Restore lifecycle journeys for missions and Play. Natasha still needs the mission events, and more push deliveries have not produced more returners in the checked weeks. |
| 3 | Improve engagement and retention. | Finish Home’s useful next actions, report cards and reliable Play with tickets. Missions have expanded, and the merged improvements still need delivery. |
| 4 | Grow organic acquisition. | Keep current SEO work moving so search and chart traffic reaches learning. Search is growing, but paying outcomes remain sparse. The [18 SEO and tools opportunities][seo] are modeled opportunities, not 18 build commitments. |
| Background | Test multiplayer engagement. | Keep the [three-player SNG MVP (psmobile issue #5080)](https://github.com/funcountry/psmobile/issues/5080) bounded alongside acquisition. It became a commitment on September 6. |

## Purchase measurement still blocks a reliable acquisition read

Release the purchase repairs and finish the campaign comparison before treating the current signals as permission to scale.

| Evidence | What it means for the decision |
|---|---|
| By day 30, 0.6% of July paid installs had paid (15 of 2,694), compared with 1.5% in April (96 of 6,500). Both cohorts are mature, with incomplete attribution. [Paid-cohort rows][paid-rows] | Acquisition economics have deteriorated. The cause is unknown; Tim and the data agent need to complete the historical comparison. |
| All 29 people who started a store subscription on September 4–6 received Plus, but the app recorded zero expected purchase completions. The sample contains 27 trials and 2 direct purchases. [Purchase reconciliation][purchase-rows] | The app is missing successful-purchase events. These are not 29 cash sales. The [repair that records success after Plus arrives (psmobile #4975)](https://github.com/funcountry/psmobile/pull/4975) has merged and needs release. |
| AppsFlyer recorded 5 settled Purchase events while Meta recorded 0 for the same sample. [Settled purchase comparison][parity] | Ad spend remains on hold at its current level. Working event delivery alone does not establish readiness to scale, and this small sample does not explain the acquisition decline. |
| In the August 24 week, push deliveries rose to 12,530 from 10,384 in the August 17 week, while 24-hour returners fell to 3,424 from 3,435. [Push delivery and return rows][push-rows] | Finish useful journeys before increasing sends. The comparison is observational, and the campaign mix differs between weeks. |
| Cached seven-day payers through September 4 rose from 21 to 29, an increase of 8. Complete-week Google Search Console clicks rose from 875 to 1,002, an increase of 127. [Payers and search-click comparison][recent-metrics] | Preserve productive work. Recent acquisition volume also fell during a deliberate wind-down of paid tests. [Morning Watch context][reports] |

## Each person has useful work to finish

Finish the six people’s current work and remove the dependencies preventing delivery.

| Person | Where the work stands | Next action |
|---|---|---|
| You | You delivered the campaign comparison worksheets in [Channel Performance][channel]. The [Android cancellation evidence change (psmobile #5001)](https://github.com/funcountry/psmobile/pull/5001) can merge; four dependent checkout fixes remain blocked. | Finish integration and produce a release candidate with the completed purchase and attribution repairs. |
| Tim | The March comparison remains unfinished. Tim reported the March campaigns running on September 2 and [confirmed they were still running September 4][reset]. He rebuilt the audience, identified an [AppsFlyer SDK issue][sdk] and delivered eight ASO assets on September 5. | Complete the historical comparison with the data agent, using the actual running settings. |
| Natasha | Lifecycle delivery is blocked because the mission events have not shipped. Natasha cleaned the push audience, rotated difficulty-based copy and identified broken triggers and first-lesson interruptions. [Mission campaigns][natasha] · [Difficulty copy][copy] · [First-lesson interruptions][interruptions] | Connect the journeys to repaired events with the backend owner in the next test build. |
| Joey | The [Missions Bar (psmobile #4780)](https://github.com/funcountry/psmobile/pull/4780) is in 2.1.41. The [five-hand Play vs AI mission (psmobile #4859)](https://github.com/funcountry/psmobile/pull/4859) merged September 3 but missed that release branch. Friday’s work covered Home and report-card metrics. [Company Scrum][gp] | Finish Home’s next-action path and carry the merged mission into release. |
| Justin | The [Play completion repair (psmobile #4853)](https://github.com/funcountry/psmobile/pull/4853) merged September 3. The [Play tab and per-table resume changes (psmobile #4939)](https://github.com/funcountry/psmobile/pull/4939) merged September 4. Staging and push-entry tests show progress, but these changes are outside 2.1.41. [Staging test][staging] · [Push-entry test][push-test] | Finish the current Play and tickets work, then carry the completion and resume repairs into release. |
| Phil | The current ad concept still needs work. Phil delivered [two script 2 video variants on September 3][phil] and worked on editing and YouTube on Friday. | Finish the existing cut and hand Tim placement-ready files before starting another concept. |

On September 5, you wrote: [“this tells a story of tim and I partnering and a recovery starting” (FC message 64752)][partnership].

## Unblock lifecycle and release the finished repairs

Use the existing owners to finish these five items.

| Concern | What prevents completion | Intervention |
|---|---|---|
| Lifecycle delivery is dragging. | The [mission-day completion trigger (psmobile #4792)](https://github.com/funcountry/psmobile/pull/4792) and [mission-row completion event (psmobile #4807)](https://github.com/funcountry/psmobile/pull/4807) were still open at 10:40, with no code change since September 2. | Have the existing backend agent finish the event changes with Natasha, then verify that the journeys receive them. The dependency is stalled; the evidence does not establish personal inactivity. |
| Completed purchase repairs still need release. | Stores still serve 2.1.41. The [checkout ownership repair (psmobile #4876)](https://github.com/funcountry/psmobile/pull/4876) and [missing purchase-completion repair (psmobile #4975)](https://github.com/funcountry/psmobile/pull/4975) have merged. The cancellation evidence change can merge, but its dependent fixes cannot yet merge. | Finish the existing integration and build work, then release the repairs. |
| The comparison may answer a different question. | The [March comparison deck][march-deck] and the [later Android-test proposal][later-deck] differ. The combined campaign-and-creative tab in [Channel Performance][channel] remains empty. The March campaigns did run. | Have Tim and the data agent complete the comparison against the actual running settings and make historical differences explicit. |
| Exploration can consume acquisition time. | Pricing work remains deferred: [“in a few weeks” (FC message 64626)][pricing]. The 18 tools rows remain modeling work, while the bounded multiplayer milestone is committed. | Keep pricing changes and broad tools expansion exploratory. Preserve current organic work and the bounded multiplayer milestone. |
| Customer follow-through needs owners. | One player raised four objections across “The Squeeze Play” and “BTN vs Two Callers” on September 4–5. The individual adjudication owner is unknown. A September 5 one-star review from a Galaxy S25 Ultra on 2.1.41 reports missing puzzle buttons and points to the [Adreno 830 graphics repair draft (psmobile #3923)](https://github.com/funcountry/psmobile/pull/3923). [Lesson feedback and device review][customer-evidence] | Route the lessons to the existing content agent. Have Justin route the device issue to its current graphics owner. The draft’s age alone does not establish a stall. |

The four checkout fixes depend on the [Android cancellation evidence change (psmobile #5001)](https://github.com/funcountry/psmobile/pull/5001). At the final 10:40 check, all four remained blocked: [release confirmed access while storage settles (psmobile #5056)](https://github.com/funcountry/psmobile/pull/5056), [retain the checkout’s app version (psmobile #5057)](https://github.com/funcountry/psmobile/pull/5057), [preserve subscription identity before plan changes (psmobile #5058)](https://github.com/funcountry/psmobile/pull/5058) and [settle original transactions after renewal (psmobile #5059)](https://github.com/funcountry/psmobile/pull/5059). [Final PR snapshot][gh-final]

## Put concrete deliveries into the September 7–13 plan

Use these recommendations in the [Company Scrum planning workbook (GP)][gp]. They are not agreed assignments; existing release and campaign approvals still apply.

| Person | Business outcome | Deliver September 7–13 | Finish next work session |
|---|---|---|---|
| You | Improve acquisition through purchase and attribution repairs. | Ship the existing purchase and attribution repairs. | Finish integration of the dependent changes and produce the release candidate containing the completed fixes. |
| Tim | Improve acquisition through a valid historical campaign comparison. | Run the intended comparison with usable evidence from campaign through conversion. | Complete the running-versus-March comparison with the data agent. Populate the missing campaign-and-creative view and correct verified setup mismatches. |
| Natasha | Increase LTV through lifecycle journeys. | Restore mission journeys and finish the current Play lifecycle revision. | Connect the existing journeys to repaired events in the next test build. Complete the path from trigger to message with the backend owner. |
| Joey | Improve engagement and retention through useful next actions. | Ship the current Home work and carry the merged Play vs AI mission into release. | Finish Home’s next-action path before expanding the report-card metrics scope. |
| Justin | Improve engagement and retention through reliable Play. | Ship the current Play and tickets work with working resume and completion. | Finish the current tickets and Play scope. Carry the merged resume and no-advice completion repairs into the release candidate. |
| Phil | Support acquisition with ad creative. | Deliver the current finished ad cut to Tim. | Finish script 2’s concept and hand over placement-ready files before starting another concept. |

## Appendix: source coverage and method

Source collection began at 09:46 on September 6. Main reads ran from 09:51 to 10:05, and the final PR check was at 10:40. Coverage is partial, especially company email and calendar, some Slack conversations, media contents and live Customer.io configuration.

The [morning-priorities process][process] establishes two outputs: ranked business priorities and useful weekly and daily deliveries. Its six steps refresh sources, rank outcomes, reconstruct each person’s work, connect work to priorities, judge progress and derive deliveries. The [Company Scrum workbook][gp] supports continuity but does not overrule newer evidence. Plans and decisions support delivery; they are not delivery goals, and no numerical targets were assigned.

### Coverage across 21 source groups

| Source group | What was read | Coverage and limits |
|---|---|---|
| Slack | The September 6 capture at 09:53 contains 578 messages from 18 selected joined channels, including replies and a 30-day parent-message lookback. [Communications coverage][comms] | The account joined 40 of 103 visible channels. The other 22 joined channels were machine or legacy channels; 63 unjoined channels had metadata only. Human-to-human DMs and unknown private channels were unavailable. Attachments were mostly metadata. |
| Telegram | The 09:53 capture contains 320 FC-group messages since August 31 and four Andrew DM context messages. [Telegram extract][telegram] | Coverage spans two dialogs. The latest FC message was September 5 at 09:55; Andrew’s latest was August 25. Photo, PDF and audio contents were not read. |
| Company Scrum workbook | Reads covered metadata for 57 tabs, current [Company Scrum cells][gp], [Work Lanes][worklanes], [September 2 Sync][sync], relevant raw notes and comments. [Workbook ranges][planning] | Team entries run through September 4. The September 6 workbook edit does not date every tab. The full historical inventory was not reread, and the credentials tab’s contents were excluded. |
| Recent Google files | Discovery covered 30 recent native files, shared-with-me files and all seven shared drives. Reads covered 13 workbooks, five Docs, four decks and comments, and found eight current ASO assets. [File register][planning] | Reads used bounded tabs and ranges. Image and video contents and some cell notes were not read. The Apple preview contains synthetic data. Phil’s final media handoff was not checked. |
| Agent sessions | Reads covered founder messages and selected outputs, goals and work across M5, Studio, M3 Max, M3 36GB and Linux. [History coverage][history] | M5 coverage included 752 prompts in 69 threads and outputs in 49 threads; its latest sampled prompt was at 09:46:39. Other hosts and runtimes were sampled, without an all-account transcript census. |
| ChatGPT and browser AI | Three visible conversations covered Meta diagnosis, retention and post-onboarding conversion. [Conversation notes][browser] | Coverage used one authenticated context. One live thread was absent from the local catalog; other accounts and projects were not exhausted. The discussions favored underlying evidence over a prescriptive verdict board. |
| Local files and memory | Reads covered recent roadmaps, source worklogs, uncommitted planning work, Morning Watch, replay and weekly records, and ledger cursors. [Agent history][history] · [Planning evidence][planning] | No prior equivalent priorities report existed. Ledger records and cursors remain old. A recent file modification alone does not show progress. |
| GitHub | Reads covered PR bodies and status across seven repos, selected commits, reviews and comments, plus metadata for 576 open psmobile issues. Sixteen material PRs were rechecked at 10:40. [GitHub read log][github] | The initial PR list covered updates since August 31; older work was followed selectively. Authorship under your account does not establish human assignment. GitHub Projects coverage remains unavailable. |
| Builds, releases and deployments | Reads covered store, staging and watch outputs, plus merge ancestry in the fetched release branch. [Release states][reports] · [Release containment][containment] | The 09:01 store check found iOS 2.1.41 (130) and Google Play build 702 at 100%, with no newer store candidate. The 06:14 Shorebird check found no OTA patch. Backend and engine observations date to 06:12–06:16. No new deployment or device test ran. |
| BigQuery and Evidence | Reads covered current canonical queries, 21 query-and-result pairs and 15 reports from the 37-report catalog. [Business data][business] | The transform succeeded at 09:01:50. Cached Evidence was built at 02:15 using September 5 data. Live September 5 first opens were 151 versus 88 cached. The other report bodies were not fetched. |
| Operational workbooks and models | Reads covered [Channel Performance][channel], [Checkout Health][checkout], store, retention, profitability, user-analysis and SEO workbooks, including newly discovered files. [Workbook coverage][planning] | Reading did not recalculate stale sheets. Checkout data was pulled September 5 at 18:31; Channel weekly data was pulled September 4 at 21:57; user reactivations were pulled September 4. The app-store workbook shows a September 6 07:00 pull despite a failed scheduled attempt. |
| Telemetry and reliability | Reads covered canonical activity and Play rows, Morning Watch, replay reviews and newer engineering and Sentry summaries. [Metrics][business] · [Recorded checks][reports] | These were existing checks, with no new replay or device test. The frozen rage aggregate does not establish that live events stopped. |
| Revenue and stores | Reads covered canonical revenue and cohorts, RevenueCat feed status, Appfigures, store outputs and native reviews. [Feed horizons][business] | Google Play downloads remain frozen at August 21 and performance at August 25 despite successful 08:00 and 08:20 loaders. RevenueCat closed-period data remains usable; direct credential access remains limited. |
| Ads and attribution | Reads covered current canonical Meta and Apple Search Ads spend, AppsFlyer, signal verifiers, OpenAI pilot rows and campaign context. [Advertising evidence][business] | No exhaustive new partner-mapping or campaign-settings readback occurred. The OpenAI pilot’s three exact installs cannot support performance claims. Apple Search Ads remains paused in the checked context, and no spend changed. |
| Lifecycle | Reads covered the Customer.io event stream, canonical deliveries and returns, mission-event history, Natasha’s discussion and repair PRs. [Lifecycle evidence][business] | Events extend through 07:00. Live journey configurations and restored campaign delivery were not checked. Removed client events alone cannot establish absent server mission completion or current campaign configuration. |
| Website, SEO and research | Reads covered Google Search Console, GA4, website reports, the canonical web funnel, fresh SEO and chart documents and existing research. [Website evidence][business] | Warehouse Search Console data extends through September 3; Morning Watch’s direct read extends through September 4. Ahrefs and Brand Radar quota is unavailable until October 4. Live Contentful and Cloudflare object and configuration changes were not exhaustively checked. |
| Customer and community feedback | Reads covered 64 text-bearing voice-of-customer rows, including 25 that were not generated form-open records, plus 52 social-text rows and current community and review outputs. [Feedback coverage][comms] | Social inboxes and threads were not exhaustively read. Discord activity remains old despite current polling. Appended posted statuses in the community packet supersede its draft heading. |
| Content, creative and design | Reads covered the Figma Home canvas through official MCP, recent ASO assets, Phil’s messages, puzzle and lesson production, and feedback. [Design][browser] · [Content work][history] | The design exists, but shipment is not established. Figma comments and edit authorship were unavailable in metadata. Media contents and the whole live content catalog were not reviewed. Puzzle work continued despite a blocked goal status. |
| Email, calendar and meetings | Six relevant personal-inbox notifications, the calendar window and available meeting documents were read. [Access limits][comms] | Company Gmail and Calendar returned 403 scope errors. Granola is encrypted and had no verified reader. Personal-account access does not establish company-inbox coverage. |
| Scheduled reports and collectors | Reads covered actual latest outputs from all 16 Studio jobs, local morning, replay, community and weekly runs, and warehouse feed state. [Scheduled outputs][reports] | Poker news failed September 6. Weekday-only reports correctly remain September 4. Staging and old GP jobs reported scheduler success while their outputs described blocked work. No sending routine was retriggered. |
| Finance, staffing and other sources | Discovery covered recent files, models, historical agreement role scope and relevant invoice-notification headers. [Finance scope][planning] | No current bank, accounting or payroll integration was established. Profitability is a model and cannot establish cash or runway. Historical compensation was excluded. |

### Evidence reconciliation

Fresh GitHub implementation state supersedes old workbook incidents; observed store delivery still determines whether customers have a repair. The 10:40 PR snapshot supersedes the old claim that the cancellation evidence change had conflicts. The successful 09:01 warehouse transform supersedes the failed-transform state in Morning Watch; cached-report age and frozen Google Play data remain separate limits.

The [approved community posts L-259 and L-258][community] were posted at 07:24. Natasha [retracted the Android-paywall explanation][correction]. The SEO rankings remain recommendations, and your quoted partnership assessment supersedes the isolated older remarks about Tim.

The [Profitability Worksheet][profitability] defines activation as two lesson completions during day 0–1. [Checkout Health][checkout] uses two meaningful completions outside required onboarding within 24 hours. Their activation percentages are not comparable. Direct activity rows and the Morning Watch count also use different cutoffs and identity definitions; the discrepancy does not establish a new business event.

### Original reports and source collections

[Morning Watch][watch] covered September 4–5.

[Published September 6 morning priorities](https://share.fun.country/20260906-763f8a326c72/index.html) · [Original working Markdown][original] · [Morning Watch living report][watch] · [Replay review living report][replay-report] · [Source inventory][inventory] · [Acquisition signal repairs (psmobile issue #5005)](https://github.com/funcountry/psmobile/issues/5005) · [Acquisition work and commitments][history] · [Browser and Figma notes][browser]

[direction]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/communications/telegram.md:1337
[partnership]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/communications/telegram.md:1542
[pricing]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/communications/telegram.md:886
[comms]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/communications.md
[telegram]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/communications/telegram.md
[planning]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/planning-sources.md
[history]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/agent-history.md
[business]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/business-data.md
[reports]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/scheduled-reports.md
[github]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/github.md
[browser]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/browser.md
[gh-final]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/github/final-status.json
[containment]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/github/release-containment.json
[paid-rows]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/business-data/04-profitability.json
[purchase-rows]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/scheduled-reports/money-parity-aggregate.json
[customer-evidence]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/scheduled-reports/_artifacts__morning-watch__runs__2026-09-06-1__leg-product.md
[process]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/README.md
[original]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06.md
[community]: /Users/aelaguiz/workspace/psagentspace/_artifacts/2026-09-06-community-reply-sweep/approval-packet.md
[inventory]: /Users/aelaguiz/workspace/psagentspace/access/everything-available-for-morning-priorities-2026-09-06.md
[watch]: https://share.fun.country/20260804-ede086c9eb57/index.html
[replay-report]: https://share.fun.country/replay-review-daily/index.html
[gp]: https://docs.google.com/spreadsheets/d/1mU0IJ6QFPwGilKTvVzNaYhhuJOnBidO0sOstCaFM9og/edit#gid=314159265
[channel]: https://docs.google.com/spreadsheets/d/1aRQyIT6TJ0C9r1z8GgkAZ2qzTAIhA7ibtBKVtxHoz2k/edit
[seo]: https://docs.google.com/spreadsheets/d/1t8R0MoDzS9AEYxgUGN_-sTVBBd4lZ1DR0plE0_hF9AE/edit
[profitability]: https://docs.google.com/spreadsheets/d/1W4vijIP3L1wNTuyBtiBQfthnxk7I-6C_fFRX4rLo4do/edit
[checkout]: https://docs.google.com/spreadsheets/d/1NJeDqK9NT-fgztW-64f6Svw7vyKWYq0iEZoEXnK2ths/edit
[march-deck]: https://docs.google.com/presentation/d/1HOc9eiNelvRAkqU-cnkIvTqPlDfGGTbBaiaOtVg-IvE/edit
[later-deck]: https://docs.google.com/presentation/d/1gi0y3CSVtL-Frj-hd7x6VipDi948faV0p5Iq4SjsVFs/edit
[reset]: https://app.slack.com/archives/C0BAXM3CS5U/p1788560921995319
[sdk]: https://app.slack.com/archives/C0BAXM3CS5U/p1788603533763819
[natasha]: https://app.slack.com/archives/C01A0JL51GC/p1788291915040409
[copy]: https://app.slack.com/archives/C030LCH08Q6/p1788359650464499
[interruptions]: https://app.slack.com/archives/C07SSLL0CAD/p1788539169432579
[staging]: https://app.slack.com/archives/C07SSLL0CAD/p1788547647535019
[push-test]: https://app.slack.com/archives/C0840843W66/p1788650391520369
[phil]: https://app.slack.com/archives/C0BAXM3CS5U/p1788449121034809
[correction]: https://app.slack.com/archives/C0BAXM3CS5U/p1788379713780599

[parity]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/business-data.md:56
[push-rows]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/business-data/12-notifications-current.json
[recent-metrics]: /Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/business-data.md:12
[worklanes]: https://docs.google.com/spreadsheets/d/1mU0IJ6QFPwGilKTvVzNaYhhuJOnBidO0sOstCaFM9og/edit#gid=2026090101
[sync]: https://docs.google.com/spreadsheets/d/1mU0IJ6QFPwGilKTvVzNaYhhuJOnBidO0sOstCaFM9og/edit#gid=1172340035
