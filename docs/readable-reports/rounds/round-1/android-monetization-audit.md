# Android’s checkout conversion gap is mostly cancellation, with a smaller set of reliability and measurement defects to repair.

Fix pending-checkout recovery, unsafe error copy and offering-failure reporting, then investigate why Android players cancel around the native Google Play handoff.

The audit is dated September 1, 2026, and covers releases 2.1.39 and 2.1.40. All times use Chicago time. The closed checkout window runs from August 17 at 19:00 through August 31 at 19:00, excluding that ending instant.

## Cancellation accounts for 77.4% of Android’s purchase-rate gap.

Android converted 20.7% of checkout starts (73 of 353), compared with iOS at 55.0% (122 of 222), a 34.3-percentage-point gap.

| Each platform has a reconciled checkout population. | Purchases and cancellations account for most starts. | Errors and unresolved outcomes account for the remainder. |
|---|---|---|
| Android recorded 353 checkout starts. | Android players purchased in 73 of 353 starts (20.7%) and cancelled in 232 of 353 (65.7%). | Android ended 17 of 353 starts in error (4.8%) and left 31 of 353 unresolved (8.8%). |
| iOS recorded 222 checkout starts. | iOS players purchased in 122 of 222 starts (55.0%) and cancelled in 87 of 222 (39.2%). | iOS ended 4 of 222 starts in error (1.8%) and left 9 of 222 unresolved (4.1%). |

Android’s excess cancellations account for 26.5 percentage points of the gap, or 77.4%. Excess unresolved outcomes account for 4.7 points, or 13.8%. Excess explicit errors account for 3.0 points, or 8.8%. The displayed contributions are rounded independently.

This arithmetic locates the missing conversions without establishing why players cancelled. Converting all 17 final Android errors would raise purchases to 90 of 353 (25.5%), still well below iOS at 55.0%.

Android offerings reached ready in 881 of 889 paygate sessions (99.1%), which rules out a broad offering outage. Rare offering failures still blocked real players.

The evidence supports three narrow product repairs and fixes to reporting. It does not establish a mass foreground checkout hang. The next product question is why Android players cancel around the native handoff, whose Google Play screens PostHog cannot capture.

### Release 2.1.40 improved Android conversion without closing the iOS gap.

Android’s purchase rate rose 3.9 percentage points between releases, so the later release did not introduce a broad new collapse.

| The platform has a release-specific denominator. | The purchase rate shows the remaining gap. |
|---|---|
| Android 2.1.40 recorded 98 starts. | Android 2.1.40 produced purchases in 23 of 98 starts (23.5%), compared with 19.6% in Android 2.1.39 and 62.7% in iOS 2.1.40. |
| Android 2.1.39 recorded 255 starts. | Android 2.1.39 produced purchases in 50 of 255 starts (19.6%), compared with 51.0% in iOS 2.1.39. |
| iOS 2.1.40 recorded 75 starts. | iOS 2.1.40 produced purchases in 47 of 75 starts (62.7%), compared with 51.0% in iOS 2.1.39. |
| iOS 2.1.39 recorded 147 starts. | iOS 2.1.39 produced purchases in 75 of 147 starts (51.0%), compared with 19.6% in Android 2.1.39. |

### Test-market traffic explains only a small part of the Android gap.

Removing test-market paid traffic raises Android conversion by 2.5 percentage points, from 20.7% to 23.2% (59 purchases from 254 starts).

That lift is too small to explain the 34.3-point platform gap. The broader acquisition-mix theory remains unresolved because other Android and iOS acquisition differences were not normalized.

| Each Android acquisition group has a distinct denominator. | Purchases and cancellations differ by group. | Errors and unresolved outcomes remain visible. |
|---|---|---|
| Main paid campaigns generated 169 starts. | Main paid campaigns produced 34 purchases from 169 starts (20.1%) and 105 cancellations from 169 starts (62.1%). The main paid purchase rate was close to Android’s overall 20.7%. | Main paid campaigns had 11 errors (6.5%) and 19 unresolved starts (11.2%). |
| Test-market paid campaigns generated 99 starts. | Test-market campaigns produced 14 purchases from 99 starts (14.1%) and 74 cancellations from 99 starts (74.7%). The test-market purchase rate was below Android’s overall 20.7%. | Test-market campaigns had 2 errors (2.0%) and 9 unresolved starts (9.1%). |
| Unlinked or organic traffic generated 77 starts. | Unlinked or organic traffic produced 22 purchases from 77 starts (28.6%) and 48 cancellations from 77 starts (62.3%). The unlinked or organic purchase rate exceeded Android’s overall 20.7%. | Unlinked or organic traffic had 4 errors (5.2%) and 3 unresolved starts (3.9%). |
| Other attributed campaigns generated 8 starts. | Other attributed campaigns produced 3 purchases from 8 starts (37.5%) and 5 cancellations from 8 starts (62.5%). The denominator is only 8, compared with 353 Android starts overall. | Other attributed campaigns had 0 errors and 0 unresolved starts. |

## Rare offering failures prevented players from reaching a usable paygate.

One player abandoned a lesson-energy paygate after roughly 8 to 10 seconds of app-owned “Loading plans…” UI, with no later ready event.

The player backed out and chose “Keep Learning.” Neither an offering-ready event nor a terminal offering-error event followed. The back arrow prevented a hard trap, but the offering never became ready in the observed sequence.

A separate Play vs AI daily-limit paygate showed app-owned loading UI for about 58 seconds, including “This is taking longer than expected” and “Retry.” It then recovered to pricing. Its canonical ready event arrived 66.253 seconds after the offering was recorded as still pending.

Both sequences show app-owned pixels, so Google Play capture gaps do not explain them. The recovered case shows that Retry and eventual pricing can work. It does not establish healthy load time or a repaired provider cause.

| Each Android release has an offering population. | Most sessions reached ready. | The remaining offering states require follow-through. |
|---|---|---|
| Android 2.1.40 had 249 paygate sessions. | Offers reached ready in 248 sessions (99.6%), compared with 98.9% in Android 2.1.39. | Zero sessions recorded refresh failure. Three recorded a still-pending state, and one had neither ready nor error. Two pending sessions later reached ready, so these state counts overlap. |
| Android 2.1.39 had 640 paygate sessions. | Offers reached ready in 633 sessions (98.9%), compared with 99.6% in Android 2.1.40. | Six sessions recorded refresh failure (0.94%). Zero remained pending, and one had neither ready nor error. |

The six Android 2.1.39 refresh failures were concentrated in three people or devices. Four failures belonged to one player across two consecutive days. In the strongest sequence, lessons continued after the first failure, but a repeated energy-gate failure was followed immediately by an explicit lesson quit.

Two of the three pending Android 2.1.40 sessions recovered after 4.986 and 66.253 seconds. The remaining session never reached ready before the player backed out after roughly 8 to 10 seconds.

Offering failure is a confirmed, low-incidence defect. The exact stalled provider stage remains unknown for this cohort. Preserve Retry and record the final outcome on the existing offering-state event. The individual implementation owner is unknown.

## Purchase errors sometimes disappeared silently, and one exposed internal account-ownership text.

One production flow showed an internal RevenueCat and Clerk ownership error to the player for about 15 seconds.

The error appeared in the puzzle screen. A manual action in its two-control error area preceded recovery, but the recording cannot distinguish “Try again” from “Back to puzzles.” The selected control is unknown.

The [puzzle deep-link resolver](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/features/puzzles/presentation/screens/puzzles_deeplink_resolver_screen.dart:284) directly renders `_resolution.lastError?.toString()` as its subtitle at lines 284–287. That propagates internal diagnostics into player-facing copy. The provider failure remains owned by the existing [RevenueCat exact-owner entitlement-bootstrap issue (psmobile #4484)](https://github.com/funcountry/psmobile/issues/4484). The separate presentation defect needs a safe message at the resolver boundary.

Some errors showed clear, dismissible purchase dialogs. Several returned players silently to ordinary content. Four affected players later committed a purchase, so an error event does not necessarily describe the final outcome.

- Purchase-not-allowed errors appeared in 10 of 21 explicit-error recordings (47.6%).
- Store-problem errors appeared in 6 of 21 explicit-error recordings (28.6%).
- Invalid-purchase errors appeared in 3 of 21 explicit-error recordings (14.3%).
- A network error appeared in 1 of 21 explicit-error recordings (4.8%).
- A duplicate-operation guard appeared in 1 of 21 explicit-error recordings (4.8%).

The error-presentation defect is confirmed, narrow and transient. Keep full diagnostics in structured logs and map the player subtitle to safe copy. The individual implementation owner is unknown.

## Pending checkout can disable buying without offering an in-place recovery action.

Release code permits an unbounded wait if neither a late native result nor canonical purchase evidence arrives.

The 10-second watchdog returns a pending outcome while the native purchase future continues. The subscription journey then renders its checking state (`SubscriptionJourneyView.checking`). The primary action says “Checking purchase…” and is disabled.

A late result can resolve the pending state. A back arrow remains available, but the inspected paywall has no timeout-specific “Check again” or “Restore” action. This preserves protection against double charging while leaving the player without bounded recovery on the paywall itself.

All 31 unresolved Android starts had a store-start event and no later canonical terminal. Thirty had recordings. Those 31 unresolved starts do not establish 31 hangs.

The six longest available unresolved captures contained one confirmed background transition and two outcomes with visible forward progress. Another recording ended 34.5 seconds into checking. Two captures were dominated by inactivity and gaps shaped like a relaunch, which do not establish foreground residence.

A held frame can persist while the app is inactive or the OS owns the screen. One selected case records the app entering the background (`app_background`). Another records the app returning to the foreground (`app_foreground`). The recordings do not prove indefinite foreground waiting or its population incidence.

Pending checkout is an unresolved recovery risk in source, rather than an established cause of the original native-store delay. Preserve the double-charge guard and add bounded recovery. The individual implementation owner is unknown.

## Canonical checkout reporting misses events and can count one action more than once.

Session-level reconciliation is required until canonical coverage is repaired, because raw event counts do not represent complete checkout populations.

1. PostHog contains 153 Android paygate presentation-invariant events (`paygate_presentation_invariant`) across releases 2.1.39 and 2.1.40, while canonical BigQuery contains 0.
2. Release 2.1.40 has 5 Android and 3 iOS purchase commits without a checkout-start event (`paygate_checkout_started`). These commits were excluded from the start denominator.
3. One watched cancellation emitted three to four copies of paygate-open and result events (`paygate_opened` and `paygate_result`) for one visible action. It also emitted two checkout start-finish cycles and a late cancellation-verification event.
4. The benefits-screen action event (`subscription_benefits_cta`) records navigation to billing, rather than a store purchase click. Treating it as a purchase click would misstate checkout starts.
5. Some successful purchases lack a store-start event. Raw event-family counts therefore cannot establish complete checkout populations.

These are confirmed measurement defects that distort analysis without causing checkout failure. Repair the existing canonical checkout model in dbt and Evidence. The individual implementation owner is unknown.

## Successful controls showed usable purchases and access to Plus.

Four matched successful-purchase controls completed purchases, and the captured app states never contradicted their canonical outcomes.

One recovered cleanly after a full process restart. Another showed unlimited energy after purchase despite a duplicate-operation guard event. A later trial-cancellation event in another control did not remove access.

The historical success-handoff defect was real and is resolved under the [purchase-success handoff issue (psmobile #4438)](https://github.com/funcountry/psmobile/issues/4438). The merged [purchase-success handoff repair (psmobile #4662)](https://github.com/funcountry/psmobile/pull/4662) owns that fix. These controls provide no basis to reopen an entitlement-loss theory.

Most cancellation controls showed normal declines, native-store round trips and continuation into free content. Static frames around a later foreground event remain native or background capture gaps. The recordings cannot establish whether a player rejected the Google Play sheet, disliked the price, lacked payment setup or changed their mind.

Audited Android 2.1.40 screens with trial data showed free-trial labels and renewal terms. The eligibility-specific question remains unresolved because no qualifying existing-subscriber plan-change recording was available. Keep that question under the [Android trial-badge issue (psmobile #4225)](https://github.com/funcountry/psmobile/issues/4225).

## Five actions address the observed defects and the remaining cancellation question.

The recommended work uses existing checkout controls, events and reporting surfaces.

1. Give pending checkout bounded recovery while preserving the double-charge guard. After the evidence wait, offer “Check again” or the existing Restore or reconcile action, plus a safe exit. Keep Buy disabled while purchase status is unknown. One focused test should leave the native future incomplete and require recovery without permitting a second charge. Another should complete the purchase after the watchdog and require access exactly once, with pending state cleared.
2. Stop rendering internal exceptions as player copy in the [puzzle deep-link resolver](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/features/puzzles/presentation/screens/puzzles_deeplink_resolver_screen.dart:284), lines 284–287. Keep the full failure in structured logs, map the subtitle to one safe message and preserve Retry and Back to puzzles. A unit or widget test should pass an exact-owner failure and reject provider, identity and internal class names in rendered text.
3. Preserve offering Retry and add a final-disposition field to the existing offering-state event. The field should distinguish recovered, backed out, refresh failed and never ready. It must distinguish the 4.986-second and 66.253-second recoveries from the 8-to-10-second abandonment with no ready event. No new event family, dashboard or state machine is needed.
4. Repair the existing canonical checkout model using distinct paygate sessions. Include PostHog’s presentation-invariant events and reconcile late purchases with purchase precedence. Show commits without starts and starts without terminals as coverage warnings. Keep the work in existing dbt and Evidence surfaces.
5. Investigate cancellation around native handoff with existing events first. Separate app declines before handoff, native user cancellations and cancellations after a store-start event. Segment by paygate surface and acquisition group. If the existing terminal event cannot express cancellation location, add one enum to it. Use PostHog as a control for app-owned screens, because it cannot show the Google Play plan, payment method or native error.

The implementation owners and delivery dates for these recommendations are unknown.

### The repair scope excludes broad rewrites and new analysis machinery.

The evidence does not call for expanding the work beyond the existing checkout system.

- A global retry must not wrap a potentially live native purchase.
- A new checkout event family is unnecessary.
- A new replay classifier or proof pipeline is unnecessary.
- A broad offering rewrite is unnecessary.
- The merged purchase-success handoff work should remain closed.

## Appendix: Production observation and exact release source support the findings.

The audit reproduced the player-visible defects through direct production observation, joining canonical BigQuery checkout events to complete PostHog mobile recordings.

The source check used deployed Android 2.1.39 at [Android 2.1.39 source commit 7144eb88f79865d5e07264d48a48f9a9f1fe70b5](https://github.com/funcountry/psmobile/commit/7144eb88f79865d5e07264d48a48f9a9f1fe70b5). Android 2.1.40 and the [detached read-only audit checkout](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901) used [Android 2.1.40 source commit f77a39bc1a53c5dadb5a664f2eadaa2264fda723](https://github.com/funcountry/psmobile/commit/f77a39bc1a53c5dadb5a664f2eadaa2264fda723).

No source, production state, provider state, app data or issue state changed during the September 1 audit.

The cited local audit checkout is now unavailable on this machine, so its code was not independently rechecked during this rewrite. The original absolute paths remain linked, alongside commit-pinned source links for Android 2.1.40.

### The checkout denominator reconciles 575 distinct starts.

A checkout start is a distinct paygate session with a checkout-start event (`paygate_checkout_started`) on Android or iOS release 2.1.39 or 2.1.40. The closed window is August 17 at 19:00 to August 31 at 19:00, corresponding to the original August 18–31 warehouse date window.

Each start was reconciled against store-interaction events (`subscription_checkout_store_interaction`), paygate-result events (`paygate_result`), checkout-finished events (`paygate_checkout_finished`) and subscription commits (`subscription_commit`). A valid purchase or commit takes precedence over a conflicting later error or cancellation. A start without a canonical terminal remains unresolved.

The five Android and three iOS 2.1.40 commits without starts were excluded, so they did not inflate conversion. PostHog and warehouse clocks can differ by seconds. PostHog HogQL also rendered some timestamps in the reader’s local clock. Adjudication used event order and recording-relative time instead of exact timestamp equality.

### Forty-four of 45 assigned recordings were available and watched in full.

Reviewers watched all 44 available recordings end to end. The remaining recording had expired under retention and returned 404.

Selection included all 21 recent Android recordings with explicit store errors and 15 matched flow and control recordings. The controls covered cancellation, unresolved checkout, successful purchase, offering failure and instrumentation. Selection also included the six longest available unresolved checkout captures and four additional offering-problem recordings.

Those selections total 46 assignments but 45 unique recordings, because one delayed-offering recording appears in both the flow and long-unresolved groups. The assigned error in one available recording and checkout in another occurred after the recording ended. Those outcomes remain unknown.

Frame-by-frame inspection treated static frames during near-zero activity, native billing handoff or a later foreground event as capture limitations. Those frames alone cannot establish a foreground hang.

| Each evidence source answers a bounded question. | Its limits constrain the causal claim. |
|---|---|
| BigQuery establishes the closed 575-start population, corrected outcomes, acquisition groups, offering states and instrumentation gaps. | BigQuery locates outcomes without establishing why Android players cancelled inside Google Play. |
| PostHog events establish ordering, lifecycle transitions, duplicate emissions, store outcomes, late commits and offering recovery. | Event order and recording-relative time take precedence over second-level clock equality. |
| PostHog recordings show the app-owned screens for 45 unique assigned recordings. | Forty-four recordings were available and watched in full. One returned 404, and two assigned moments fell outside available recording windows. |
| Sentry was not used for a new causal claim. | The existing [RevenueCat exact-owner entitlement-bootstrap issue (psmobile #4484)](https://github.com/funcountry/psmobile/issues/4484) already owns the provider failure. The new claim concerns directly observed unsafe presentation. |
| Fly logs were unnecessary for the player-visible client findings. | No backend-producer claim was added beyond the existing exact-owner issue. |
| A device or simulator reproduction was unnecessary because production recordings showed the relevant app pixels. | Native Google Play UI remains outside PostHog mobile capture, so its contents are unknown. |

The [regression ledger](/Users/aelaguiz/workspace/psagentspace/REGRESSIONS.md) already contained RevenueCat offering stalls, Android purchase-not-allowed errors, exact-owner entitlement bootstrap and Android trial-copy mismatch. The audit extended their population and replay evidence. It added the separate client error-presentation path without duplicating ownership of the provider failure.

### Exact release code explains the pending-state risk and unsafe subtitle.

Both release lines contain the watchdog, native-purchase race and disabled checking action.

| The release code has a specific behavior. | The inspected location establishes its meaning. |
|---|---|
| The no-result threshold fires after 10 seconds. | The [checkout observability threshold](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/core/subscriptions/purchase_execution/subscription_checkout_observability.dart:12), line 12, controls observability and return of control. It does not establish that the store call failed. |
| Native purchase races the watchdog, and pending returns while late work continues. | The [subscription purchase service](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/core/subscriptions/purchase_execution/subscription_purchase_service.dart:530), lines 530–560, avoids inventing a terminal result and keeps late store evidence reachable. |
| Nonterminal purchase evidence renders the checking view. | The [subscription journey machine](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/core/subscriptions/journey/subscription_journey_machine.dart:656), lines 656–705, protects against another charge while waiting. |
| Checking disables the primary action. | The [paywall readiness action](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/features/subscription/presentation/components/paywall_readiness_cta.dart:38), lines 38–55, prevents double purchase but exposes no in-place recovery action in this state. |
| The puzzle resolver displays the last error as text. | The [puzzle deep-link resolver](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/features/puzzles/presentation/screens/puzzles_deeplink_resolver_screen.dart:284), lines 284–287, turns the internal exception into the subtitle seen in replay. |

The commit-pinned sources retain the inspected code locations.

- The [checkout observability threshold at release 2.1.40](https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/core/subscriptions/purchase_execution/subscription_checkout_observability.dart#L12) corresponds to the original local citation.
- The [subscription purchase service at release 2.1.40](https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/core/subscriptions/purchase_execution/subscription_purchase_service.dart#L530) corresponds to the original local citation.
- The [subscription journey machine at release 2.1.40](https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/core/subscriptions/journey/subscription_journey_machine.dart#L656) corresponds to the original local citation.
- The [paywall readiness action at release 2.1.40](https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/features/subscription/presentation/components/paywall_readiness_cta.dart#L38) corresponds to the original local citation.
- The [puzzle deep-link resolver at release 2.1.40](https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/features/puzzles/presentation/screens/puzzles_deeplink_resolver_screen.dart#L284) corresponds to the original local citation.

The subscription purchase service and paywall readiness action files are unchanged between the release tags. The journey machine changed, but both versions render checking for nonterminal evidence. Pending recovery is a blocker after the native-store delay, while unsafe error copy propagates a separately owned provider failure. Offering stalls are confirmed availability failures with an unknown provider stage. Canonical reporting gaps affect observability rather than initiating checkout failure.

### The recurring theories have distinct dispositions.

The [August 31 report context](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/theory-inventory.md), [August 24 report context](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/theory-inventory.md) and [August 17 report context](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/theory-inventory.md) supplied the recurring theories. Their individual original paths are unknown here. The [theory inventory](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/theory-inventory.md) retains their collected context.

| The theory makes a specific claim. | The evidence determines its disposition and follow-through. |
|---|---|
| An alternative paygate presentation path caused Android’s conversion gap. | The audit rejects this explanation. Android paygates rendered, accepted input, entered checkout and continued through purchases and cancellations. No replay or population split connected that path to the 34.3-point gap. No separate repair is supported. |
| Android hides the trial badge when the current Google Play offer includes a trial. | The eligibility-specific question remains unresolved. Eligible-looking 2.1.40 screens showed labels and renewal terms, but no qualifying existing-subscriber plan-change recording was available. Continue only the narrow [Android trial-badge investigation (psmobile #4225)](https://github.com/funcountry/psmobile/issues/4225). |
| Purchase can dismiss without success or usable Plus access. | The historical defect is confirmed and resolved under the [purchase-success handoff issue (psmobile #4438)](https://github.com/funcountry/psmobile/issues/4438). Controls showed access continuing, and the merged [purchase-success handoff repair (psmobile #4662)](https://github.com/funcountry/psmobile/pull/4662) owns the fix. Keep that work closed. |
| RevenueCat exact-owner lookup can block entitlement bootstrap. | One Android recording directly showed the internal failure. A manual action preceded recovery, but the selected control is unknown. The provider defect remains open under the [RevenueCat exact-owner entitlement-bootstrap issue (psmobile #4484)](https://github.com/funcountry/psmobile/issues/4484). Repair unsafe player-facing propagation separately. |
| Offering loading and refresh failures block valid paygates. | The rare defect is confirmed. Six of 640 Android 2.1.39 sessions failed refresh. One 2.1.40 lesson-energy load was abandoned after 8 to 10 seconds without ready. A Play vs AI daily-limit load recovered after about 58 seconds of timeout copy and Retry. Preserve recovery and record final outcomes. |
| Dead-session and route-removal guards block valid purchases. | The observed guards behaved as expected. Cases continued or had no live purchase UI. One duplicate-operation guard fired after successful purchase with unlimited energy visible. No player-facing block was reproduced, so no guard removal is supported. |
| Store-side purchase blocks explain the Android gap. | Purchase-not-allowed, invalid-purchase, store and network errors are real, but they cannot explain most of the gap. Some were silent, some showed usable dialogs, and four players later committed. Converting every final error would reach only 25.5%. Continue the [Android purchase-not-allowed investigation (psmobile #4684)](https://github.com/funcountry/psmobile/issues/4684) for the remaining rate question. |
| Google Play download reporting was frozen. | Google Play download reporting can remain stale while product recordings and canonical app events continue. The finding concerns reporting coverage. The cause of the stale store feed was not checked in this audit. |
| Zero purchase-attributed coverage means paid Android checkouts failed. | Canonical outcomes contain real paid Android purchases. Zero attributed coverage indicates failed signal agreement or attribution coverage, rather than zero product conversion. Repair measurement without treating that zero as a product-failure count. |
| Android’s overall acquisition mix explains the checkout gap. | The overall theory remains unresolved because platform acquisition differences were not normalized. Removing 99 test-market starts raises Android conversion from 20.7% to 23.2%, too little to explain the 34.3-point gap. Further comparison must address the remaining mix differences. |
| Pending checkout can lack bounded in-place recovery. | This new source-backed risk remains unresolved in production frequency. Both release lines have a 10-second watchdog and disabled checking action. One recording ends 34.5 seconds into checking. Longer holds are explained or confounded by backgrounding and inactivity. Add bounded recovery without claiming systemic foreground hangs. |

### Capture limits leave cancellation causes and some individual outcomes unknown.

Native Google Play pixels are absent, so black, torn or held app frames cannot establish what happened on the billing sheet.

Mobile replay preserves the last app screenshot through inactivity and OS suspension. The [daily-limit long-unresolved recording (case 2)](https://us.posthog.com/project/215955/replay/01a05a32-986b-79cb-840c-81df148a2a54) records a foreground return after its hold. The [backgrounded onboarding recording (long-unresolved case 3)](https://us.posthog.com/project/215955/replay/01a03bfd-e21d-7a4e-bc9d-3189e4c642a6) records a background transition after checkout.

The [unavailable store-error recording (case 19)](https://us.posthog.com/project/215955/replay/01a016b9-f6aa-7d23-b292-61280ef9a174) returns 404. The assigned error in the [onboarding store-problem recording (store-error case 18)](https://us.posthog.com/project/215955/replay/01a01cb4-114b-77b5-96a1-32b1ef24be59) occurs about 51 seconds after its recording ends. The assigned checkout in the [unresolved onboarding recording (flow-control case 7)](https://us.posthog.com/project/215955/replay/01a046bf-e22f-7304-a93c-9227053f52c9) occurs about 32 seconds after its recording ends. These gaps prevent adjudication of those assigned moments.

No qualifying existing-subscriber plan-change session was available to settle the trial-badge question. The recordings cannot explain why players cancelled inside Google Play. A static capture does not establish foreground residence, and slightly different event clocks do not establish ordering on their own.

### Private evidence remains separate from the shared artifact.

Raw recordings, timelines and identifier-bearing extracts remain in the [local replay directory](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replays.local/), which is git-ignored and excluded from the shared artifact.

Shared screenshots were manually checked and contain no user IDs, device IDs, emails, IPs, tokens or account identifiers. Replay links require an authenticated PostHog session with access to project 215955.

The [September 1 shared audit](https://share.fun.country/20260901-3e8e184c94c8/index.html) was fetched September 6. The [rendered text source](/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/android-monetization-audit-20260901.txt) and [rendered HTML source](/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/android-monetization-audit-20260901.html) preserve that artifact.

### The source inventory retains the full working evidence.

The working documents preserve population construction and case-level adjudication.

The [final working report](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/android-monetization-replay-audit.md) contains the full audit. The [theory inventory](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/theory-inventory.md) tracks recurring claims, and the [candidate and sampling record](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/session-candidates.md) records selection.

Store-error reviews cover [cases 15–21](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/error-cases-15-21.md), [cases 8–14](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/error-cases-08-14.md) and [cases 1–7](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/error-cases-01-07.md). Flow-control reviews cover [cases 9–15](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/flow-cases-09-15.md) and [cases 1–8](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/flow-cases-01-08.md). The [long-unresolved review](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/long-unresolved-cases.md) contains final parent adjudication, and the [offering-problem review](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/all-offering-problems.md) covers the offering cases exhaustively. The original audit inspected source in the [read-only release checkout](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901), which is now unavailable locally.

### The replay index preserves every assigned case and its outcome.

Every available recording was watched in full, and each link opens the authenticated PostHog replay for that case.

Case dates retain the original date labels. Their Chicago calendar dates were not checked against individual recording timestamps. Undated cases are grouped by release, with 2.1.40 first.

#### Explicit store-error cases show varied presentation and later outcomes.

The 21 store-error assignments include silent failures, clear dialogs and purchases that later committed.

| Each recording has a named case and context. | The observed outcome has a stated limit. |
|---|---|
| The [energy recording with a purchase-not-allowed error (store-error case 1)](https://us.posthog.com/project/215955/replay/01a058ce-e379-73c7-b647-0858588a7e9a) is dated August 31, 2026. | The paygate closed without an explanation, and the player continued browsing. |
| The [onboarding recording with a purchase-not-allowed error (store-error case 2)](https://us.posthog.com/project/215955/replay/01a055d2-61fc-7275-9e38-36e25c6990a4) is dated August 31, 2026. | The recording has a native-store capture gap. A later purchase committed. |
| The [onboarding recording with a purchase-not-allowed error (store-error case 3)](https://us.posthog.com/project/215955/replay/01a05079-d6e6-7520-8936-178ea6b541b4) is dated August 30, 2026. | The failure was likely silent, but the frame evidence has lower confidence. The exact presentation remains unknown. |
| The [onboarding recording with an invalid-purchase error (store-error case 4)](https://us.posthog.com/project/215955/replay/01a04b8a-3003-770c-9dd8-923a714a8899) is dated August 29, 2026. | No visible defect appeared, and onboarding continued. |
| The [onboarding recording with an invalid-purchase error (store-error case 5)](https://us.posthog.com/project/215955/replay/01a044f5-cd37-7eff-a0c0-007a661bc57b) is dated August 27, 2026. | The recording has a native-store capture gap. A later purchase committed. |
| The [post-puzzle recording with a purchase-not-allowed error (store-error case 6)](https://us.posthog.com/project/215955/replay/01a040d2-77e5-7807-9422-fdb9c7d5e805) is dated August 27, 2026. | The failure was silent, and the player continued for more than 25 minutes. |
| The [onboarding recording with a purchase-not-allowed error (store-error case 7)](https://us.posthog.com/project/215955/replay/01a04082-8deb-7cf2-a918-d117015ee3e5) is dated August 27, 2026. | The screen exposed internal entitlement text. A manual action preceded recovery, but the selected control is unknown. |
| The [lesson-energy recording with a store-problem error (store-error case 8)](https://us.posthog.com/project/215955/replay/01a03b96-3d60-7de4-9860-2c9d9c1792a1) is dated August 26, 2026. | The first failure was silent. The paygate appeared again, and a purchase committed. |
| The [onboarding recording with a purchase-not-allowed error (store-error case 9)](https://us.posthog.com/project/215955/replay/01a039b9-7daa-7e48-8013-1ae08ca38bc0) is dated August 25, 2026. | The alternative paygate appeared, and the player declined normally. |
| The [onboarding recording with a purchase-not-allowed error (store-error case 10)](https://us.posthog.com/project/215955/replay/01a0395a-5e41-72b3-a639-f0710fdb412d) is dated August 25, 2026. | A clear purchase-not-allowed dialog appeared, and the player continued on the free path. |
| The [onboarding recording with a network error (store-error case 11)](https://us.posthog.com/project/215955/replay/01a032d5-f103-7bc3-879b-ec9158334f74) is dated August 24, 2026. | The network failure was silent, and free play continued. |
| The [onboarding recording with a purchase-not-allowed error (store-error case 12)](https://us.posthog.com/project/215955/replay/01a02b16-ae9c-738e-b3b0-e4f1f25e4028) is dated August 22, 2026. | No joined event or visible paywall was available. The outcome remains unknown. |
| The [onboarding recording with an invalid-purchase error (store-error case 13)](https://us.posthog.com/project/215955/replay/01a02a7f-c37b-7170-bb26-d1268c422151) is dated August 22, 2026. | The native capture was corrupted, and an automatic retry committed a purchase. |
| The [onboarding recording with a store-problem error (store-error case 14)](https://us.posthog.com/project/215955/replay/01a0223b-1b2c-7e9d-b0e7-2049dd63feca) is dated August 21, 2026. | The store failure was silent, and no retry was visible. |
| The [onboarding recording with a store-problem error (store-error case 15)](https://us.posthog.com/project/215955/replay/01a02235-f632-7102-b8d2-91d1f00f7a86) is dated August 21, 2026. | A clear store-problem dialog appeared, and play continued. |
| The [onboarding recording with a purchase-not-allowed error (store-error case 16)](https://us.posthog.com/project/215955/replay/01a020c4-29aa-7b27-a6fd-a868a8ecb3cb) is dated August 20, 2026. | The failure was likely silent, with no observed player block. The exact presentation remains unknown. |
| The [onboarding recording with a store-problem error (store-error case 17)](https://us.posthog.com/project/215955/replay/01a01f60-6aa3-7480-a352-542e6ab584e7) is dated August 20, 2026. | A clear store-problem dialog appeared, and play continued. |
| The [onboarding recording with a store-problem error (store-error case 18)](https://us.posthog.com/project/215955/replay/01a01cb4-114b-77b5-96a1-32b1ef24be59) is dated August 20, 2026. | The assigned error occurs about 51 seconds after the recording ends. Its visual outcome is unknown. |
| The [settings recording with a store-problem error (store-error case 19)](https://us.posthog.com/project/215955/replay/01a016b9-f6aa-7d23-b292-61280ef9a174) is dated August 18, 2026. | The recording returns 404, so its visual outcome is unknown. |
| The [onboarding recording with a purchase-already-in-progress guard (store-error case 20)](https://us.posthog.com/project/215955/replay/01a01695-297a-7ed3-83d2-f4459d8cdfd1) is dated August 18, 2026. | The purchase succeeded, and the duplicate-operation guard caused no observed problem. |
| The [onboarding recording with a purchase-not-allowed error (store-error case 21)](https://us.posthog.com/project/215955/replay/01a015e2-507a-7aba-b04c-e0626a2c8427) is dated August 18, 2026. | Telemetry recorded an error during browsing, while no purchase UI was open. |

#### Matched controls distinguish working flows from unresolved captures.

The 15 flow assignments include four successful controls and cases where the recording cannot establish a final outcome.

| Each recording has a named case and context. | The observed outcome has a stated limit. |
|---|---|
| The [post-puzzle cancellation recording (flow-control case 1)](https://us.posthog.com/project/215955/replay/01a05a91-7348-713f-ad1a-4fbd6b750d4c) captured release 2.1.40. | The player declined normally, and results remained usable. |
| The [onboarding cancellation recording (flow-control case 2)](https://us.posthog.com/project/215955/replay/01a05a56-43e7-758e-8147-145be0a72d0b) captured release 2.1.40. | The player voluntarily cancelled without an observed defect. Native-store capture gaps limit what is visible. |
| The [settings cancellation recording (flow-control case 3)](https://us.posthog.com/project/215955/replay/01a0580a-e5e4-78a1-ae35-e9d6552ad16d) captured release 2.1.40. | The player voluntarily cancelled from Settings without an observed defect. |
| The [delayed offering and unresolved checkout recording (flow-control case 5)](https://us.posthog.com/project/215955/replay/01a05a32-986b-79cb-840c-81df148a2a54) captured release 2.1.40. | The offering recovered after 66.253 seconds. A later checkout had no terminal event, so its final outcome remains unknown. |
| The [unresolved onboarding checkout recording (flow-control case 6)](https://us.posthog.com/project/215955/replay/01a05795-a8c4-7b10-bde2-ed0ee0e8afa6) captured release 2.1.40. | The recording ends on checking. A native capture gap is likely but unproved, and the final outcome is unknown. |
| The [unresolved onboarding checkout recording (flow-control case 7)](https://us.posthog.com/project/215955/replay/01a046bf-e22f-7304-a93c-9227053f52c9) captured release 2.1.40. | The assigned checkout occurs about 32 seconds after the recording ends. Its visual outcome is unknown. |
| The [successful onboarding purchase recording (flow-control case 9)](https://us.posthog.com/project/215955/replay/01a05aa2-f93c-713e-ad98-ea62a431caa3) captured release 2.1.40. | The successful purchase control showed no observed defect. |
| The [successful onboarding purchase recording (flow-control case 10)](https://us.posthog.com/project/215955/replay/01a05514-8034-7e08-823c-c0f4692727c6) captured release 2.1.40. | The purchase succeeded, with an 88-second checkout capture gap. The recording cannot distinguish a native overlay from uncaptured app UI. |
| The [successful lesson-energy purchase recording (flow-control case 11)](https://us.posthog.com/project/215955/replay/01a057fe-e92e-70b3-8e8d-19da742eb3bd) captured release 2.1.40. | The purchase succeeded, and later trial-cancellation telemetry did not undo access. |
| The [onboarding cancellation recording (flow-control case 4)](https://us.posthog.com/project/215955/replay/01a05426-3863-7c12-b37f-dcaea50b5e26) captured release 2.1.39. | The player cancelled normally and continued into puzzle play. |
| The [unresolved onboarding checkout recording (flow-control case 8)](https://us.posthog.com/project/215955/replay/01a03fd2-3dc2-7c85-81cd-a40abdd6932b) captured release 2.1.39. | The first decline was normal. The second attempt was cut off while in progress, leaving its final outcome unknown. |
| The [successful onboarding purchase recording (flow-control case 12)](https://us.posthog.com/project/215955/replay/01a04ac1-889b-751a-adb6-ec187f7b3dd3) captured release 2.1.39. | The purchase succeeded, and a process restart recovered cleanly. |
| The [repeated offering refresh failures recording (flow-control case 13)](https://us.posthog.com/project/215955/replay/01a02144-ccb7-713c-84a5-0daffc9ffdda) captured release 2.1.39. | Two real refresh failures occurred. The player explicitly quit after the later energy-gate failure. |
| The [repeated offering refresh failures recording (flow-control case 14)](https://us.posthog.com/project/215955/replay/01a02483-49b0-778c-af7f-1e818b15073b) captured release 2.1.39. | The same player encountered the recurring refresh failure on another day. |
| The [paygate-open and presentation-event mismatch recording (flow-control case 15)](https://us.posthog.com/project/215955/replay/01a03caf-2226-74dc-b734-19be96967aa1) captured release 2.1.39. | The visible cancellation was normal, while events duplicated three to four times. |

#### The longest unresolved recordings do not establish long foreground hangs.

The six long-unresolved assignments include backgrounding, forward progress and recordings that end before an outcome.

| Each recording has a named case and context. | The observed outcome has a stated limit. |
|---|---|
| The [onboarding checkout recording (long-unresolved case 1)](https://us.posthog.com/project/215955/replay/01a05495-f2af-77fa-932a-b879a53048de) captured release 2.1.40. | The 19-hour span contains only 73 active seconds and a recovery shaped like a relaunch. It does not establish a foreground hang. |
| The [Play vs AI daily-limit checkout recording (long-unresolved case 2)](https://us.posthog.com/project/215955/replay/01a05a32-986b-79cb-840c-81df148a2a54) captured release 2.1.40. | The one-hour frame hold ends with a foreground-return event (`app_foreground`). Inactivity or backgrounding explains the gap, rather than an established hour-long foreground freeze. |
| The [onboarding checkout recording (long-unresolved case 5)](https://us.posthog.com/project/215955/replay/01a05047-8f7a-7715-9121-f217c1606dba) captured release 2.1.40. | The recording ends 34.5 seconds into checking, leaving the final outcome unknown. |
| The [onboarding checkout recording (long-unresolved case 3)](https://us.posthog.com/project/215955/replay/01a03bfd-e21d-7a4e-bc9d-3189e4c642a6) captured release 2.1.39. | The app entered the background (`app_background`) 47 seconds after checkout. The pending record later aged out. |
| The [onboarding checkout recording (long-unresolved case 4)](https://us.posthog.com/project/215955/replay/01a0345f-ba62-76ed-b90f-3b189659029d) captured release 2.1.39. | The player declined normally, entered puzzles and kept playing. |
| The [onboarding checkout recording (long-unresolved case 6)](https://us.posthog.com/project/215955/replay/01a02373-530e-7ad4-816d-4f3646b8b3c3) captured release 2.1.39. | The checking state cleared to “Opening puzzle…” in about 20 seconds. |

#### Additional offering recordings include recovery and abandonment.

Four additional recordings preserve the offering failures and recoveries not already covered.

| Each recording has a named case and context. | The observed outcome has a stated limit. |
|---|---|
| The [lesson-energy offering recording (August 31)](https://us.posthog.com/project/215955/replay/01a0550c-e8a1-7da3-a685-567ded95bfed) captured release 2.1.40. | The app-owned offering load remained visible for roughly 8 to 10 seconds without recovery. The player backed out before ready. |
| The [onboarding offering recording (August 31)](https://us.posthog.com/project/215955/replay/01a05543-4696-7632-8f08-2c7eae7f7a6a) captured release 2.1.40. | The still-pending offering recovered after 4.986 seconds, showing localized pricing and an active primary action. |
| The [onboarding offering recording (August 27)](https://us.posthog.com/project/215955/replay/01a042f5-56a9-7cfa-8523-bfdd0a21cc4f) captured release 2.1.39. | A load-plans error remained visible for about five seconds. The player then continued into a puzzle. |
| The [onboarding offering recording (August 19)](https://us.posthog.com/project/215955/replay/01a01936-4242-788b-8394-7357417b030f) captured release 2.1.39. | An offering-error event occurred during a clean exit to Learn. The captured frames show no visible failure. |
