# Android monetization audit: September 1, 2026

**Repair checkout recovery and error handling, then investigate why Android players cancel so often at the native Google Play handoff.**

Android cancellations account for 77.4% of its 34.3-percentage-point purchase-rate gap with iOS. The 575 checkout starts do not establish a broad paywall-loading outage or a mass checkout hang.

All times use Chicago. The closed checkout window runs from August 17, 2026 at 19:00 through August 31 at 19:00, with the endpoint excluded. The releases are Android and iOS 2.1.39 and 2.1.40.

## Cancellations explain most of the Android purchase-rate gap

Android converted 20.7% of checkout starts (73 of 353), compared with iOS at 55.0% (122 of 222). Even converting all 17 final Android errors would raise Android only to 25.5%.

| Platform | Starts (sessions) | Purchased (sessions, %) | Cancelled (sessions, %) | Error (sessions, %) | Unresolved (sessions, %) |
|---|---|---|---|---|---|
| Android | 353 | 73 (20.7%) | 232 (65.7%) | 17 (4.8%) | 31 (8.8%) |
| iOS | 222 | 122 (55.0%) | 87 (39.2%) | 4 (1.8%) | 9 (4.1%) |

The gap falls mostly into cancellations. The reasons players cancelled remain unknown.

| Excess Android outcome versus iOS | Percentage points | Share of purchase-rate gap |
|---|---|---|
| Cancellation | 26.5 | 77.4% |
| Unresolved | 4.7 | 13.8% |
| Error | 3.0 | 8.8% |

### Android improved in 2.1.40 but remains far below iOS

Android’s purchase rate rose 3.9 percentage points, from 19.6% in 2.1.39 to 23.5% in 2.1.40. The newer release did not introduce a broad conversion collapse.

| Platform and release | Starts (sessions) | Purchased (sessions) | Purchase rate (%) |
|---|---|---|---|
| Android 2.1.40 | 98 | 23 | 23.5% |
| Android 2.1.39 | 255 | 50 | 19.6% |
| iOS 2.1.40 | 75 | 47 | 62.7% |
| iOS 2.1.39 | 147 | 75 | 51.0% |

### Test-market traffic explains only 2.5 points of the gap

Removing the 99 starts from test-market paid campaigns leaves 59 purchases from 254 Android starts, or 23.2% versus 20.7% overall, far short of iOS’s 55.0%.

| Acquisition group | Starts (sessions) | Purchased (sessions) | Purchase rate (%) | Cancelled (sessions) | Error (sessions) | Unresolved (sessions) |
|---|---|---|---|---|---|---|
| Main paid campaigns | 169 | 34 | 20.1% | 105 | 11 | 19 |
| Test-market paid campaigns | 99 | 14 | 14.1% | 74 | 2 | 9 |
| Unlinked or organic | 77 | 22 | 28.6% | 48 | 4 | 3 |
| Other attributed campaigns | 8 | 3 | 37.5% | 5 | 0 | 0 |

The broader acquisition-mix explanation remains unresolved because the other Android and iOS acquisition differences were not normalized. The recordings cannot establish whether players rejected Google Play’s offer because of price, payment setup or a change of mind.

## Rare offering failures block some players from checkout

Android offerings reached ready in 99.1% of paygate sessions (881 of 889), but several app-owned loading failures prevented or delayed checkout.

| Android release | Paygate sessions | Reached ready (sessions) | Refresh failed (sessions) | Still pending (sessions) | No ready or error (sessions) |
|---|---|---|---|---|---|
| 2.1.40 | 249 | 248 | 0 | 3 | 1 |
| 2.1.39 | 640 | 633 | 6 | 0 | 1 |

These offering states can overlap as a session progresses. Six 2.1.39 refresh-failure sessions involved three people or devices. Four failures belonged to one player over two consecutive days. In the strongest sequence, lessons continued after the first failure, but the player quit the lesson immediately after a repeated energy-paygate failure. [Repeated failures, flow case 13][flow13] · [Same player on another day, flow case 14][flow14]

On 2.1.40, two of three sessions marked still pending eventually reached ready, after about 5 and 66 seconds. The third player left before the offering became ready.

| Paygate | What the player saw and did | Finding and next action |
|---|---|---|
| Lesson energy, 2.1.40 | The paygate showed “Loading plans…” for roughly 8 to 10 seconds. The player backed out and chose Keep Learning. No ready event or final offering-error event followed. [August 31 loading abandonment][offering3] | The offering failed to become available before the player left. Keep the safe exit and record the final outcome on the existing offering event. |
| Play vs AI daily limit, 2.1.40 | The paygate showed app-owned loading UI for about 58 seconds, including “This is taking longer than expected” and Retry. Pricing eventually appeared; the ready event followed the still-pending event by about 66 seconds. [Delayed offering, flow case 5][flow5] | Recovery works, but the delay is a real availability defect. Preserve Retry and investigate the stalled provider stage, which is unknown for this cohort. |

Both recordings show app-owned screens, so missing Google Play pixels do not explain these loading delays. Retry mitigates the failure; eventual pricing does not establish that the provider cause is repaired.

## Purchase errors sometimes disappear silently or expose internal details

The 21 Android recordings with explicit store errors show inconsistent handling: some displayed a clear, dismissible dialog, several returned silently to content and four affected players later completed a purchase.

| Error class | Recordings |
|---|---|
| Purchase not allowed | 10 |
| Store problem | 6 |
| Purchase invalid | 3 |
| Network error | 1 |
| Duplicate operation guard | 1 |

One production flow displayed internal RevenueCat and Clerk ownership details for about 15 seconds. The player tapped within the two-control error area and then recovered; the pixels do not identify whether the player chose Try again or Back to puzzles. [Internal error shown to a player, store-error case 7][error7]

The [puzzle deeplink resolver, lines 284–287][resolver] renders `_resolution.lastError?.toString()` as its subtitle. That is the path that exposes internal diagnostic text. The underlying provider failure already belongs to the [RevenueCat exact-owner entitlement-bootstrap issue (psmobile #4484)](https://github.com/funcountry/psmobile/issues/4484). Keep that owner and fix the separate player-facing presentation defect.

## “Checking purchase…” needs a recovery action

The source allows an indefinite wait when neither a late native result nor canonical evidence arrives. How often players remain on that screen in the foreground is unknown.

After 10 seconds without a final result, the watchdog returns a pending outcome while the native purchase continues. The journey shows `SubscriptionJourneyView.checking`, and the primary CTA becomes disabled with “Checking purchase…” text. A back arrow remains, but the inspected state offers no timeout-specific Check again or Restore action. The code protects against a double charge and can accept a late purchase result. It does not bound the player’s wait on that screen.

All 31 unresolved Android starts have a store-start event and no later canonical final outcome. Thirty have recordings. The six longest selected captures show these different outcomes:

| Observation | What it establishes |
|---|---|
| One player backgrounded the app after checkout. | The long frame hold does not establish a foreground hang. [Background event, long-unresolved case 3][long3] |
| Two players visibly progressed. | One declined and continued puzzles; another left checking for “Opening puzzle…” after about 20 seconds. [Continued play, long-unresolved case 4][long4] · [Checking cleared, long-unresolved case 6][long6] |
| One recording ended 34.5 seconds into checking. | The final outcome is unknown. [Recording cut off during checking, long-unresolved case 5][long5] |
| Two recordings contained long periods with little activity and recovery that resembled a relaunch. | Neither establishes continuous foreground residence. One spans 19 hours but has only 73 active seconds; the other ends an hour-long frame hold with an app-foreground event. [Sparse activity, long-unresolved case 1][long1] · [Foreground return, long-unresolved case 2][long2] |

Pending checkout is a recovery problem in the app; the evidence does not identify the initiating native-store cause. Preserve the double-charge guard while adding a bounded way to check again or exit.

## Canonical checkout reporting misses events and duplicates actions

Repair the existing session-based checkout model before using raw event-family counts as conversion denominators.

| Measurement defect | Consequence and repair |
|---|---|
| PostHog contains 153 Android paygate-presentation diagnostic events (`paygate_presentation_invariant`) across 2.1.39 and 2.1.40; canonical BigQuery contains zero. | Bring this event family into the canonical path so the same diagnostic evidence is available in both systems. |
| Five Android and three iOS 2.1.40 purchase commits have no checkout-start event (`paygate_checkout_started`). | Keep these purchases outside a denominator defined by starts, and expose the missing starts as coverage warnings. |
| One visible cancellation emitted three to four copies of paygate-opened and result events, two checkout start-and-finish cycles and a late cancellation-verification event. [Duplicated events, flow case 15][flow15] | Count distinct paygate sessions and reconcile conflicting outcomes, giving a valid purchase precedence. |
| The benefits CTA event (`subscription_benefits_cta`) records navigation from benefits to billing. Some successful purchases also lack a store-start event. | Do not count benefits navigation as a store purchase click or assume store-start events cover every purchase. |

These gaps distort measurement; they do not cause checkout failures.

## Successful purchases and most observed declines continue normally

The four matched successful-purchase recordings show purchases and usable access consistent with canonical outcomes.

One recovered cleanly after a full process restart. Another showed unlimited energy after purchase despite a duplicate-operation guard event. The [purchase-success handoff repair (psmobile PR #4662)](https://github.com/funcountry/psmobile/pull/4662) has merged and resolves the historical [missing purchase-success handoff (psmobile issue #4438)](https://github.com/funcountry/psmobile/issues/4438). This cohort provides no reason to reopen an entitlement-loss theory.

Most cancellation recordings show normal declines, native-store round trips and continued free content. Static paywall frames near a later app-foreground event are consistent with native or background capture gaps. PostHog does not capture the Google Play billing sheet, so it cannot identify the selected plan, payment method or native error.

The audited 2.1.40 screens with trial data showed free-trial labels and renewal terms. The eligibility-specific question remains open because no qualifying existing-subscriber plan-change recording was available.

## Keep the confirmed defects separate from unresolved theories

The recurring theories from the [August 31 report draft][weekly31], [August 24 report][weekly24] and [August 17 report][weekly17] have different dispositions. The confirmed failures and pending-recovery risk justify narrow repairs. [Theory inventory][theories]

| Theory | Finding and next action |
|---|---|
| An alternative paygate presentation path caused the Android gap. | The observed paygates rendered, accepted input, entered checkout and continued after purchases or cancellations. The evidence disproves this explanation in the audited population: no replay or population split tied the 34.3-point gap to that path. |
| Android hides trial badges on eligible offers. | The broad claim is unsupported because labels and renewal terms appeared where trial data existed. The existing-subscriber plan-change question remains unresolved; keep it scoped to the [Android trial-badge issue (psmobile #4225)](https://github.com/funcountry/psmobile/issues/4225). |
| A purchase can dismiss without success or usable Plus. | The historical defect is resolved under the [purchase-success handoff issue (psmobile #4438)](https://github.com/funcountry/psmobile/issues/4438) and [merged repair (psmobile PR #4662)](https://github.com/funcountry/psmobile/pull/4662). The successful-purchase recordings show access continuing, so do not reopen this work. |
| RevenueCat exact-owner lookup can block entitlement bootstrap. | The defect is confirmed and remains open under the [exact-owner provider issue (psmobile #4484)](https://github.com/funcountry/psmobile/issues/4484). One recording exposes the failure to the player; fix that separate presentation path while retaining the provider owner. |
| Offering loading or refresh errors block valid paygates. | The defect is confirmed but rare: six of 640 sessions on 2.1.39 failed during refresh. On 2.1.40, one player abandoned loading after 8 to 10 seconds and another recovered after about 58 seconds of timeout UI. Preserve recovery and investigate the stalled stage. |
| Dead-session and route-removal cleanup guards block valid purchases. | The observed guards behaved as expected. Players continued, or no live purchase UI existed; one duplicate-operation guard followed a successful purchase with unlimited energy already visible. No player-facing block was reproduced. |
| Store-side purchase blocks explain the platform gap. | The error class is confirmed, but the main-cause theory is disproved: converting every final Android error would produce only 25.5% conversion. Keep the remaining rate investigation in the [Android purchase-not-allowed issue (psmobile #4684)](https://github.com/funcountry/psmobile/issues/4684). |
| Frozen Google Play download reporting means product checkout stopped. | The freeze is a reporting artifact. Store reporting can stay stale while checkout recordings and canonical app events continue. Treat it as a coverage defect. |
| Zero purchase-attributed coverage means paid Android checkouts failed. | Canonical checkout outcomes contain real paid Android purchases. The zero indicates missing attribution or disagreement between purchase signals, so repair measurement. |
| Android’s acquisition mix explains the gap. | The theory remains unresolved. Removing the 99 test-market starts raises conversion only from 20.7% to 23.2%; the remaining platform acquisition differences were not normalized. |
| “Checking purchase…” can leave the player without an in-place recovery action. | The source confirms the 10-second watchdog, pending state and disabled CTA in both releases. Foreground incidence remains unresolved because long captures contain inactivity or backgrounding, and one ends after 34.5 seconds. Add bounded recovery without enabling another purchase. |

## Make five narrow changes before changing paywall design or traffic strategy

Fix the observed reliability and reporting defects, then use the existing checkout events to locate cancellations around the native boundary.

1. Give pending checkout a bounded recovery state. After a bounded evidence wait, offer Check again or the existing Restore action to reconcile purchase status plus a safe exit. Keep Buy disabled while purchase status is unknown. Test a native purchase future that never completes: recovery must become available without allowing a second charge. Test a late purchase after the watchdog: access must be granted once and pending state must clear.
2. Stop displaying internal exceptions. In the [puzzle deeplink resolver, lines 284–287][resolver], retain full details in structured logs and show one player-safe subtitle. Preserve Retry and Back to puzzles. Pass an exact-owner failure through a unit or widget test and verify that rendered text excludes provider, identity and internal class names.
3. Preserve offering Retry and record the final outcome. Add a field to the existing offering-state event for outcomes such as recovered, backed out, refresh failed or never ready. This distinguishes the 4.986-second and 66.253-second recoveries from the 8-to-10-second abandonment without adding another event family, dashboard or state machine.
4. Repair the canonical checkout model in the existing dbt and Evidence surfaces. Use distinct paygate sessions, include PostHog paygate-presentation diagnostic events and reconcile late purchases with purchase precedence. Expose purchases without starts and starts without final outcomes as coverage warnings.
5. Locate cancellations using existing events. Distinguish app decline before native handoff, native user cancellation and cancellation after a store-start event. Segment by paygate surface and acquisition group. If the current final-outcome event cannot express that location, add one enum to it.

Do not add a global retry around a possibly live native purchase, a new checkout event family or a new replay classifier and proof pipeline. Keep the offering changes narrow and the merged purchase-success handoff work closed.

## Appendix: source and coverage

### Cohort construction

The denominator contains distinct sessions with `paygate_checkout_started` in the closed window. Reconciliation uses `subscription_checkout_store_interaction`, `paygate_result`, `paygate_checkout_finished` and `subscription_commit`. A valid purchase or commit takes precedence over a conflicting later cancellation or error. A start without a canonical final outcome remains unresolved. The five Android and three iOS commits without starts are excluded from the 575-start denominator.

PostHog and warehouse clocks can differ by seconds, and HogQL rendered some timestamps in Chicago time. Event order and recording-relative time therefore determine case interpretation rather than exact timestamp equality.

### Replay sampling and limits

The sample contains all 21 recent Android recordings with explicit store errors, 15 matched flow recordings, the six longest available unresolved captures and four additional offering-problem recordings. One delayed-offering recording appears in both the flow and long-unresolved sets, leaving 45 unique assigned recordings.

Forty-four recordings were available and watched end to end, including frame-by-frame inspection. [Store-error case 19][error19] had expired and returned 404. The assigned error in [store-error case 18][error18] and checkout in [flow case 7][flow7] occurred after their recording windows, so those moments cannot be adjudicated.

Native Google Play pixels are absent. Black, torn or held checkout frames cannot establish a hang. Mobile replay preserves the last app screenshot during inactivity and OS suspension. [Long-unresolved case 2][long2] logs `app_foreground` on return; [case 3][long3] logs `app_background` after checkout. No qualified existing-subscriber plan-change recording was available to resolve the trial-badge question.

### Evidence sources

| Source | Coverage |
|---|---|
| BigQuery | Canonical queries establish the closed 575-checkout population, corrected outcomes, acquisition groups, offering states and instrumentation gaps. |
| PostHog events | Events establish ordering, lifecycle transitions, duplicate emissions, store outcomes, late purchases and offering recovery. |
| PostHog recordings | The 45 assigned recordings establish app-owned pixels within their available windows; 44 were available to watch. |
| Sentry | No new causal claim comes from Sentry. The existing exact-owner issue already owns the provider failure class. |
| Fly logs | No new backend producer claim comes from Fly logs; the findings concern player-visible client behavior and the existing provider issue. |
| Device or simulator | Production recordings reproduce the visible defects. No new device or simulator reproduction was needed, and native Google Play contents remain outside capture. |

The search of [REGRESSIONS.md][regressions] found existing RevenueCat offering-stall, Android purchase-not-allowed, exact-owner entitlement-bootstrap and Android trial-copy mismatch classes. The separate client error-presentation path adds a propagation defect without duplicating the provider owner.

### Exact release source

The historical [local audit checkout][worktree] is no longer present on this machine. The code links open the exact release commit on GitHub.

Android 2.1.40 and the [detached read-only checkout][worktree] use [release commit f77a39bc1a53c5dadb5a664f2eadaa2264fda723](https://github.com/funcountry/psmobile/commit/f77a39bc1a53c5dadb5a664f2eadaa2264fda723). Android 2.1.39 uses [release commit 7144eb88f79865d5e07264d48a48f9a9f1fe70b5](https://github.com/funcountry/psmobile/commit/7144eb88f79865d5e07264d48a48f9a9f1fe70b5).

| Behavior | Exact 2.1.40 source and interpretation |
|---|---|
| The watchdog waits 10 seconds for a final result. | The [checkout observability threshold, line 12][watchdog] returns control and records the delay; it does not establish that the store call failed. |
| Native purchase continues after the watchdog returns pending. | The [purchase service, lines 530–560][service] keeps a late store result reachable without inventing a final outcome. |
| Evidence without a final outcome renders the checking view. | The [subscription journey machine, lines 656–705][journey] retains protection against a second charge while waiting. |
| Checking disables the primary CTA. | The [paywall readiness CTA, lines 38–55][cta] prevents another purchase but offers no in-place recovery action in that state. |
| The puzzle resolver renders the last error as text. | The [puzzle deeplink resolver, lines 284–287][resolver] directly exposes the internal text seen in replay. |

The watchdog, purchase-service race and CTA behavior exist in both release tags. The purchase-service and CTA files are unchanged between them. The journey machine changed, but both versions render checking for evidence without a final outcome.

### Source inventory and privacy

[Original local resolver path][resolver-local] · [Original local watchdog path][watchdog-local] · [Original local purchase-service path][service-local] · [Original local journey-machine path][journey-local] · [Original local CTA path][cta-local]

[Original published audit](https://share.fun.country/20260901-3e8e184c94c8/index.html) · [Final working report][working] · [Theory inventory][theories] · [Candidate and sampling record][candidates]

[Store-error reviews, cases 1–7][errors1] · [Store-error reviews, cases 8–14][errors2] · [Store-error reviews, cases 15–21][errors3]

[Flow reviews, cases 1–8][flows1] · [Flow reviews, cases 9–15][flows2] · [Long-unresolved reviews and final adjudication][longs] · [Exhaustive offering review][offerings] · [Read-only release checkout][worktree]

Raw recordings, timelines and identifier-bearing extracts remain in the git-ignored [local replay directory][private], outside the shared artifact. Shared screenshots were manually checked and contain no user IDs, device IDs, emails, IPs, tokens or account identifiers. Replay links require an authenticated PostHog session with access to project 215955.

### Authenticated replay index

Every available recording was watched in full. The case labels retain the original numbering for cross-reference.

#### Store-error cases

| Recording | Observed outcome |
|---|---|
| [Case 1 · Aug. 31 · Energy, purchase not allowed][error1] | The paygate closed silently, and the player continued browsing. |
| [Case 2 · Aug. 31 · Onboarding, purchase not allowed][error2] | The recording misses native-store UI; a later purchase committed. |
| [Case 3 · Aug. 30 · Onboarding, purchase not allowed][error3] | The failure was likely silent, but the frame evidence has lower confidence. |
| [Case 4 · Aug. 29 · Onboarding, purchase invalid][error4] | Onboarding continued without a visible defect. |
| [Case 5 · Aug. 27 · Onboarding, purchase invalid][error5] | The recording misses native-store UI; a later purchase committed. |
| [Case 6 · Aug. 27 · Post-puzzle, purchase not allowed][error6] | The purchase failed silently, and the player continued for more than 25 minutes. |
| [Case 7 · Aug. 27 · Onboarding, purchase not allowed][error7] | The app exposed internal entitlement text. The player tapped in the two-control error area and then recovered; the selected control is not identifiable. |
| [Case 8 · Aug. 26 · Lesson Energy, store problem][error8] | The first failure was silent. The paygate appeared again, and the purchase committed. |
| [Case 9 · Aug. 25 · Onboarding, purchase not allowed][error9] | An alternate paygate appeared, and the player declined normally. |
| [Case 10 · Aug. 25 · Onboarding, purchase not allowed][error10] | The app showed a clear purchase-not-allowed dialog, and the player continued on the free path. |
| [Case 11 · Aug. 24 · Onboarding, network error][error11] | The network failure was silent, and free play continued. |
| [Case 12 · Aug. 22 · Onboarding, purchase not allowed][error12] | The recording has no joined event or visible paywall; the outcome remains unresolved. |
| [Case 13 · Aug. 22 · Onboarding, purchase invalid][error13] | The native capture was corrupted, but an automatic retry committed the purchase. |
| [Case 14 · Aug. 21 · Onboarding, store problem][error14] | The store failure was silent, and no retry was visible. |
| [Case 15 · Aug. 21 · Onboarding, store problem][error15] | The app showed a clear store-problem dialog, and play continued. |
| [Case 16 · Aug. 20 · Onboarding, purchase not allowed][error16] | The failure was likely silent, and the player was not blocked. |
| [Case 17 · Aug. 20 · Onboarding, store problem][error17] | The app showed a clear store-problem dialog, and play continued. |
| [Case 18 · Aug. 20 · Onboarding, store problem][error18] | The assigned error occurs about 51 seconds after the recording ends. |
| [Case 19 · Aug. 18 · Settings, store problem][error19] | The recording is unavailable and returns 404. |
| [Case 20 · Aug. 18 · Onboarding, purchase already in progress][error20] | The purchase succeeded; the duplicate-operation guard caused no visible problem. |
| [Case 21 · Aug. 18 · Onboarding, purchase not allowed][error21] | Telemetry recorded an error during browsing, when no purchase UI was open. |

#### Matched flow and successful-purchase cases

| Recording | Observed outcome |
|---|---|
| [Case 1 · 2.1.40 · Post-puzzle cancellation][flow1] | The player declined normally, and results remained usable. |
| [Case 2 · 2.1.40 · Onboarding cancellation][flow2] | The player voluntarily cancelled; the recording contains gaps during native-store UI. |
| [Case 3 · 2.1.40 · Settings cancellation][flow3] | The player voluntarily cancelled from Settings. |
| [Case 4 · 2.1.39 · Onboarding cancellation][flow4] | The player cancelled normally and continued puzzle play. |
| [Case 5 · 2.1.40 · Delayed offering and unresolved checkout][flow5] | The offering recovered after 66.253 seconds. The later checkout has no final outcome. |
| [Case 6 · 2.1.40 · Unresolved onboarding checkout][flow6] | The recording ends on checking. A native capture gap is likely but unproven. |
| [Case 7 · 2.1.40 · Unresolved onboarding checkout][flow7] | The assigned checkout occurs about 32 seconds after the recording ends. |
| [Case 8 · 2.1.39 · Unresolved onboarding checkout][flow8] | The first decline was normal; the recording cuts off the second attempt in flight. |
| [Case 9 · 2.1.40 · Successful onboarding purchase][flow9] | The onboarding purchase completed without a visible defect. |
| [Case 10 · 2.1.40 · Successful onboarding purchase][flow10] | The purchase completed normally despite an 88-second checkout capture gap. The recording cannot distinguish a native overlay from uncaptured app UI. |
| [Case 11 · 2.1.40 · Successful lesson-energy purchase][flow11] | The lesson-energy purchase granted access. Later trial-cancellation telemetry did not undo access. |
| [Case 12 · 2.1.39 · Successful onboarding purchase][flow12] | After the successful purchase, the app recovered cleanly from a process restart. |
| [Case 13 · 2.1.39 · Repeated offering refresh failures][flow13] | Two offering refreshes failed. The player explicitly quit after the later energy-paygate failure. |
| [Case 14 · 2.1.39 · Repeated offering refresh failures][flow14] | The offering failed again for this player on another day. |
| [Case 15 · 2.1.39 · Open-versus-presented instrumentation mismatch][flow15] | The player visibly cancelled normally, but events were duplicated three to four times. |

#### Long-unresolved cases

| Recording | Observed outcome |
|---|---|
| [Case 1 · 2.1.40 · Onboarding][long1] | The 19-hour span has only 73 active seconds and recovery resembling a relaunch. It does not establish a foreground hang. |
| [Case 2 · 2.1.40 · Play vs AI Daily Limit][long2] | The hour-long frame hold ends when the app returns to the foreground (`app_foreground`). The gap reflects inactivity or backgrounding, without proof of an hour-long foreground freeze. |
| [Case 3 · 2.1.39 · Onboarding][long3] | The app went into the background 47 seconds after checkout (`app_background`). The pending record later aged out. |
| [Case 4 · 2.1.39 · Onboarding][long4] | The player declined normally, entered puzzles and kept playing. |
| [Case 5 · 2.1.40 · Onboarding][long5] | The recording ends 34.5 seconds into checking. The outcome remains unresolved. |
| [Case 6 · 2.1.39 · Onboarding][long6] | Checking cleared to “Opening puzzle…” in about 20 seconds. |

#### Additional offering-problem recordings

| Recording | Observed outcome |
|---|---|
| [Aug. 31 · 2.1.40 onboarding][offering4] | The pending offering recovered in 4.986 seconds to localized pricing and an active CTA. |
| [Aug. 31 · 2.1.40 lesson energy][offering3] | The app showed offering loading for roughly 8 to 10 seconds without recovery. The player backed out before ready. |
| [Aug. 27 · 2.1.39 onboarding][offering2] | The app showed a load-plans error for about five seconds, then the player continued into a puzzle. |
| [Aug. 19 · 2.1.39 onboarding][offering1] | The app emitted an offering error during a clean exit to Learn; the captured frames show no visible failure. |

[error1]: https://us.posthog.com/project/215955/replay/01a058ce-e379-73c7-b647-0858588a7e9a
[error2]: https://us.posthog.com/project/215955/replay/01a055d2-61fc-7275-9e38-36e25c6990a4
[error3]: https://us.posthog.com/project/215955/replay/01a05079-d6e6-7520-8936-178ea6b541b4
[error4]: https://us.posthog.com/project/215955/replay/01a04b8a-3003-770c-9dd8-923a714a8899
[error5]: https://us.posthog.com/project/215955/replay/01a044f5-cd37-7eff-a0c0-007a661bc57b
[error6]: https://us.posthog.com/project/215955/replay/01a040d2-77e5-7807-9422-fdb9c7d5e805
[error7]: https://us.posthog.com/project/215955/replay/01a04082-8deb-7cf2-a918-d117015ee3e5
[error8]: https://us.posthog.com/project/215955/replay/01a03b96-3d60-7de4-9860-2c9d9c1792a1
[error9]: https://us.posthog.com/project/215955/replay/01a039b9-7daa-7e48-8013-1ae08ca38bc0
[error10]: https://us.posthog.com/project/215955/replay/01a0395a-5e41-72b3-a639-f0710fdb412d
[error11]: https://us.posthog.com/project/215955/replay/01a032d5-f103-7bc3-879b-ec9158334f74
[error12]: https://us.posthog.com/project/215955/replay/01a02b16-ae9c-738e-b3b0-e4f1f25e4028
[error13]: https://us.posthog.com/project/215955/replay/01a02a7f-c37b-7170-bb26-d1268c422151
[error14]: https://us.posthog.com/project/215955/replay/01a0223b-1b2c-7e9d-b0e7-2049dd63feca
[error15]: https://us.posthog.com/project/215955/replay/01a02235-f632-7102-b8d2-91d1f00f7a86
[error16]: https://us.posthog.com/project/215955/replay/01a020c4-29aa-7b27-a6fd-a868a8ecb3cb
[error17]: https://us.posthog.com/project/215955/replay/01a01f60-6aa3-7480-a352-542e6ab584e7
[error18]: https://us.posthog.com/project/215955/replay/01a01cb4-114b-77b5-96a1-32b1ef24be59
[error19]: https://us.posthog.com/project/215955/replay/01a016b9-f6aa-7d23-b292-61280ef9a174
[error20]: https://us.posthog.com/project/215955/replay/01a01695-297a-7ed3-83d2-f4459d8cdfd1
[error21]: https://us.posthog.com/project/215955/replay/01a015e2-507a-7aba-b04c-e0626a2c8427
[flow1]: https://us.posthog.com/project/215955/replay/01a05a91-7348-713f-ad1a-4fbd6b750d4c
[flow2]: https://us.posthog.com/project/215955/replay/01a05a56-43e7-758e-8147-145be0a72d0b
[flow3]: https://us.posthog.com/project/215955/replay/01a0580a-e5e4-78a1-ae35-e9d6552ad16d
[flow4]: https://us.posthog.com/project/215955/replay/01a05426-3863-7c12-b37f-dcaea50b5e26
[flow5]: https://us.posthog.com/project/215955/replay/01a05a32-986b-79cb-840c-81df148a2a54
[flow6]: https://us.posthog.com/project/215955/replay/01a05795-a8c4-7b10-bde2-ed0ee0e8afa6
[flow7]: https://us.posthog.com/project/215955/replay/01a046bf-e22f-7304-a93c-9227053f52c9
[flow8]: https://us.posthog.com/project/215955/replay/01a03fd2-3dc2-7c85-81cd-a40abdd6932b
[flow9]: https://us.posthog.com/project/215955/replay/01a05aa2-f93c-713e-ad98-ea62a431caa3
[flow10]: https://us.posthog.com/project/215955/replay/01a05514-8034-7e08-823c-c0f4692727c6
[flow11]: https://us.posthog.com/project/215955/replay/01a057fe-e92e-70b3-8e8d-19da742eb3bd
[flow12]: https://us.posthog.com/project/215955/replay/01a04ac1-889b-751a-adb6-ec187f7b3dd3
[flow13]: https://us.posthog.com/project/215955/replay/01a02144-ccb7-713c-84a5-0daffc9ffdda
[flow14]: https://us.posthog.com/project/215955/replay/01a02483-49b0-778c-af7f-1e818b15073b
[flow15]: https://us.posthog.com/project/215955/replay/01a03caf-2226-74dc-b734-19be96967aa1
[long1]: https://us.posthog.com/project/215955/replay/01a05495-f2af-77fa-932a-b879a53048de
[long2]: https://us.posthog.com/project/215955/replay/01a05a32-986b-79cb-840c-81df148a2a54
[long3]: https://us.posthog.com/project/215955/replay/01a03bfd-e21d-7a4e-bc9d-3189e4c642a6
[long4]: https://us.posthog.com/project/215955/replay/01a0345f-ba62-76ed-b90f-3b189659029d
[long5]: https://us.posthog.com/project/215955/replay/01a05047-8f7a-7715-9121-f217c1606dba
[long6]: https://us.posthog.com/project/215955/replay/01a02373-530e-7ad4-816d-4f3646b8b3c3
[offering1]: https://us.posthog.com/project/215955/replay/01a01936-4242-788b-8394-7357417b030f
[offering2]: https://us.posthog.com/project/215955/replay/01a042f5-56a9-7cfa-8523-bfdd0a21cc4f
[offering3]: https://us.posthog.com/project/215955/replay/01a0550c-e8a1-7da3-a685-567ded95bfed
[offering4]: https://us.posthog.com/project/215955/replay/01a05543-4696-7632-8f08-2c7eae7f7a6a
[working]: /Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/android-monetization-replay-audit.md
[theories]: /Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/theory-inventory.md
[candidates]: /Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/session-candidates.md
[errors1]: /Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/error-cases-01-07.md
[errors2]: /Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/error-cases-08-14.md
[errors3]: /Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/error-cases-15-21.md
[flows1]: /Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/flow-cases-01-08.md
[flows2]: /Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/flow-cases-09-15.md
[longs]: /Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/long-unresolved-cases.md
[offerings]: /Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/all-offering-problems.md
[private]: /Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replays.local/
[worktree]: /Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901
[regressions]: /Users/aelaguiz/workspace/psagentspace/REGRESSIONS.md
[resolver]: https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/features/puzzles/presentation/screens/puzzles_deeplink_resolver_screen.dart#L284
[watchdog]: https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/core/subscriptions/purchase_execution/subscription_checkout_observability.dart#L12
[service]: https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/core/subscriptions/purchase_execution/subscription_purchase_service.dart#L530
[journey]: https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/core/subscriptions/journey/subscription_journey_machine.dart#L656
[cta]: https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/features/subscription/presentation/components/paywall_readiness_cta.dart#L38

[resolver-local]: /Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/features/puzzles/presentation/screens/puzzles_deeplink_resolver_screen.dart:284
[watchdog-local]: /Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/core/subscriptions/purchase_execution/subscription_checkout_observability.dart:12
[service-local]: /Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/core/subscriptions/purchase_execution/subscription_purchase_service.dart:530
[journey-local]: /Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/core/subscriptions/journey/subscription_journey_machine.dart:656
[cta-local]: /Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/features/subscription/presentation/components/paywall_readiness_cta.dart:38
[weekly31]: /Users/aelaguiz/workspace/psagentspace/_artifacts/2026-08-31-monday-update/DRAFT_EMAIL.md
[weekly24]: /Users/aelaguiz/workspace/psagentspace/_artifacts/2026-08-24-monday-update/SENT_EMAIL_2026-08-24.md
[weekly17]: /Users/aelaguiz/workspace/psagentspace/_artifacts/2026-08-17-monday-update/SENT_EMAIL_2026-08-17.md
