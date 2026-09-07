# Android monetization audit: September 1, 2026

**Fix the checkout recovery and error-handling defects, repair reporting, then investigate why Android players cancel so often around the Google Play handoff.**

Android converted 20.7% of checkout starts (73 of 353), versus 55.0% on iOS (122 of 222); cancellations account for 77.4% of that gap. The reason for those cancellations is unknown because PostHog cannot show the native Google Play billing sheet.

The findings concern app releases 2.1.39 and 2.1.40. All clock times use Chicago time.

## Words used here

A paygate is an app screen that offers a subscription or trial. An offering is the set of plans and prices RevenueCat returns. Canonical events are the cleaned BigQuery events used by the dashboards. A terminal outcome is a recorded purchase, cancellation or error that resolves a checkout. Exact-owner lookup checks entitlement ownership against the RevenueCat and Clerk identities. Plus means the app’s subscription access.

## Cancellations account for most of Android’s conversion gap

Android had 26.5 percentage points more cancellations than iOS, versus 4.7 points more unresolved checkouts and 3.0 points more explicit errors.

The closed population contains 575 distinct checkout starts. The table shows their reconciled outcomes; purchase evidence takes precedence over conflicting cancellation or error events.

| Platform | Checkout starts (sessions) | Purchased (sessions, %) | Cancelled (sessions, %) | Error (sessions, %) | Unresolved (sessions, %) |
|---|---:|---:|---:|---:|---:|
| Android | 353 | 73 (20.7%) | 232 (65.7%) | 17 (4.8%) | 31 (8.8%) |
| iOS | 222 | 122 (55.0%) | 87 (39.2%) | 4 (1.8%) | 9 (4.1%) |

The 34.3-point purchase-rate gap divides as follows. This arithmetic locates the missing conversions; it does not establish why players cancelled.

| Excess Android outcome | Difference from iOS (percentage points) | Share of purchase-rate gap (%) |
|---|---:|---:|
| Cancellation | 26.5 | 77.4 |
| Unresolved checkout | 4.7 | 13.8 |
| Explicit error | 3.0 | 8.8 |

Even converting all 17 final Android errors would raise its purchase rate only to 25.5%, still far below iOS at 55.0%. Store errors are real, but cannot explain most of the gap.

### Android improved in the later release

Android conversion rose 3.9 points, from 19.6% on 2.1.39 to 23.5% on 2.1.40; the later release did not introduce a broad collapse.

| Platform and release | Checkout starts (sessions) | Purchased (sessions) | Purchase rate (%) |
|---|---:|---:|---:|
| Android 2.1.40 | 98 | 23 | 23.5 |
| Android 2.1.39 | 255 | 50 | 19.6 |
| iOS 2.1.40 | 75 | 47 | 62.7 |
| iOS 2.1.39 | 147 | 75 | 51.0 |

Both Android releases still converted far below their iOS counterparts.

### Removing test-market traffic barely reduces the gap

Excluding the 99 test-market starts raises Android conversion only 2.5 points, from 20.7% to 23.2% (59 purchases from 254 starts).

| Android acquisition group | Starts (sessions) | Purchased (sessions) | Purchase rate (%) | Cancelled (sessions) | Error (sessions) | Unresolved (sessions) |
|---|---:|---:|---:|---:|---:|---:|
| Main paid campaigns | 169 | 34 | 20.1 | 105 | 11 | 19 |
| Test-market paid campaigns | 99 | 14 | 14.1 | 74 | 2 | 9 |
| Unlinked or organic | 77 | 22 | 28.6 | 48 | 4 | 3 |
| Other attributed campaigns | 8 | 3 | 37.5 | 5 | 0 | 0 |

The test-market segment cannot explain the 34.3-point platform gap by itself. Other Android and iOS acquisition differences were not normalized, so their contribution remains unknown.

## Offering failures are rare, but some prevent checkout

Android offerings reached ready in 99.1% of paygate sessions (881 of 889), ruling out a broad loading outage while leaving eight sessions without ready evidence.

| Android release | Paygate sessions | Reached ready (sessions) | Refresh failed (sessions) | Still pending (sessions) | No ready or error (sessions) |
|---|---:|---:|---:|---:|---:|
| 2.1.40 | 249 | 248 | 0 | 3 | 1 |
| 2.1.39 | 640 | 633 | 6 | 0 | 1 |

Offering states can overlap: two of the three 2.1.40 sessions that became pending later reached ready. Their exact recovery times were 4.986 and 66.253 seconds, about 5 and 66 seconds.

### One player abandoned loading; another eventually received prices

One lesson-energy paygate on 2.1.40 displayed only “Loading plans…” for roughly 8 to 10 seconds before the player backed out and chose Keep Learning. No ready or terminal offering-error event followed. The back arrow prevented a trap, but the offering never became usable in the observed sequence.

Sources: [Abandoned lesson-energy offering replay](https://us.posthog.com/project/215955/replay/01a0550c-e8a1-7da3-a685-567ded95bfed) · [Loading screen screenshot](https://share.fun.country/20260901-3e8e184c94c8/media/offering-abandoned.jpg)

A different 2.1.40 Play paygate, shown at the daily limit, displayed “This is taking longer than expected” and Retry for about 58 seconds. Pricing then appeared; the canonical ready event followed the pending event (`still_pending`) by about 66 seconds. Retry and eventual recovery worked in that case, but the delay still interrupted checkout.

Sources: [Recovered daily-limit offering replay (flow case 5)](https://us.posthog.com/project/215955/replay/01a05a32-986b-79cb-840c-81df148a2a54) · [Timeout and Retry screenshot](https://share.fun.country/20260901-3e8e184c94c8/media/offering-stall.jpg)

Both sequences show app-owned pixels throughout the relevant delay. Google Play capture gaps do not explain those loading screens.

Six of 640 sessions on 2.1.39, about 0.9%, refreshed to failure; those sessions were concentrated in three people or devices. Four failures belonged to one player across two consecutive days. In the clearest sequence, lessons continued after the first failure, but a later energy-paygate failure repeated and immediately preceded an explicit lesson quit.

Sources: [Repeated offering failures (flow case 13)](https://us.posthog.com/project/215955/replay/01a02144-ccb7-713c-84a5-0daffc9ffdda) · [Same player’s failures on another day (flow case 14)](https://us.posthog.com/project/215955/replay/01a02483-49b0-778c-af7f-1e818b15073b)

The offering failures are confirmed and uncommon. The exact stalled provider stage is unknown for this cohort; preserve Retry and record whether each affected session recovers or exits.

## Purchase errors sometimes disappear and sometimes expose internal text

The 21 explicit store-error recordings show inconsistent handling: some errors produced clear dialogs, several closed silently, and one exposed an internal entitlement exception.

| Error class | Recordings |
|---|---:|
| Purchase not allowed | 10 |
| Store problem | 6 |
| Purchase invalid | 3 |
| Network error | 1 |
| Duplicate-operation guard | 1 |

Four affected players later completed purchases. Several others returned to ordinary content without an explanation; some received clear, dismissible dialogs.

One 2.1.40 puzzle error screen exposed a RevenueCat and Clerk exact-owner failure for about 15 seconds. A manual action in the two-control error area preceded recovery. Which control was tapped is unknown: the pixels cannot distinguish Try again from Back to puzzles.

Sources: [Internal entitlement error replay (store-error case 7)](https://us.posthog.com/project/215955/replay/01a04082-8deb-7cf2-a918-d117015ee3e5) · [Player-visible internal error screenshot](https://share.fun.country/20260901-3e8e184c94c8/media/internal-error.jpg)

The [puzzle deeplink resolver, lines 284–287](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/features/puzzles/presentation/screens/puzzles_deeplink_resolver_screen.dart:284) renders `_resolution.lastError?.toString()` as its subtitle. That directly explains how internal diagnostic text reached the player.

The provider failure remains open under the [exact-owner entitlement-bootstrap issue (psmobile #4484)](https://github.com/funcountry/psmobile/issues/4484). The separate confirmed defect is the resolver’s player-facing error text. Keep the full exception in structured logs, replace the subtitle with player-safe copy and preserve the recovery controls.

## Pending checkout can leave only the back arrow usable

After 10 seconds without a terminal outcome, the release code can show “Checking purchase…” with the primary buy button disabled and no bounded recovery action.

The purchase service returns a pending outcome while the native purchase future continues. The subscription journey renders its checking view (`SubscriptionJourneyView.checking`). Late native or canonical purchase evidence can resolve that state.

The back arrow remains available, but the inspected paywall offers no timeout-specific Check Again or Restore action. If purchase evidence never arrives, the source permits an unbounded wait on that screen. Preserve the double-charge protection and add a safe way to check again or leave.

Source: [Checking-purchase screenshot](https://share.fun.country/20260901-3e8e184c94c8/media/checking-risk.jpg)

The 31 unresolved Android starts do not establish 31 hangs. Every one has a store-start event and no later canonical terminal outcome; 30 have a recording. The six longest selected captures contain these outcomes:

| Observation | Captures | What it establishes |
|---|---:|---|
| The app moved to the background after checkout. | 1 | The capture cannot establish continuous foreground waiting. |
| The player visibly progressed. | 2 | The app recovered or continued in these cases. |
| The recording ended while checking continued. | 1 | The outcome remains unknown after 34.5 seconds of checking. |
| Inactivity dominated a gap that ended like a relaunch. | 2 | Held frames do not establish that the app remained in the foreground. |

Source: [Long-unresolved replay reviews](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/long-unresolved-cases.md)

The recovery risk exists in both releases. Systemic foreground hangs remain unproven; neither a black or torn capture nor a long-held frame establishes one. The initial native-store cause of a pending checkout remains unknown.

## Reporting gaps distort checkout counts

Canonical reporting omits or duplicates checkout evidence, so use distinct-session reconciliation until the existing model is repaired.

| Gap | Consequence and next step |
|---|---|
| PostHog contains 153 Android presentation-invariant events (`paygate_presentation_invariant`) across both releases; canonical BigQuery contains zero. | Restore that event family to the existing canonical path so the warehouse retains the presentation evidence. |
| Five Android and three iOS 2.1.40 purchase commits lack a checkout-start event (`paygate_checkout_started`). | Keep those eight commits outside the start denominator and expose the missing starts as coverage warnings. |
| One visible cancellation emitted three to four copies of paygate-open and result events (`paygate_opened`, `paygate_result`). | That same action produced two checkout start-finish cycles and a late cancellation-verification event. Reconcile the session once. [Duplicated cancellation replay (flow case 15)](https://us.posthog.com/project/215955/replay/01a03caf-2226-74dc-b734-19be96967aa1) |
| The benefits button event (`subscription_benefits_cta`) records navigation from benefits to billing. | Do not count that navigation as a store purchase click. |
| Some successful purchases lack a store-start event. | Raw event-family counts cannot establish a complete checkout population. Reconcile purchase evidence and expose missing coverage in the existing model. |

These are confirmed measurement defects. They distort analysis but do not cause the observed checkout failures.

## Successful controls do not justify reopening repaired purchase work

Four matched purchase controls completed purchases and retained access; the visible app state never contradicted the canonical outcome.

One control recovered after a full process restart. Another showed unlimited energy after purchase despite a duplicate-operation guard. Keep the resolved [purchase-success handoff issue (psmobile #4438)](https://github.com/funcountry/psmobile/issues/4438) closed; the merged [purchase-success handoff fix (psmobile #4662)](https://github.com/funcountry/psmobile/pull/4662) owns that repair.

Source: [Unlimited-energy screenshot after purchase](https://share.fun.country/20260901-3e8e184c94c8/media/purchase-success.jpg)

Cancellation controls showed normal declines, native-store round trips and continued free content. Dead-session and route-removal guards either allowed continuation or fired with no live purchase UI. No player-facing purchase block was reproduced from those guards.

Static paywall frames around a later foreground-return event (`app_foreground`) reflect native or background capture gaps. The recordings cannot identify whether a player rejected the Google Play sheet, disliked the price, lacked a valid payment setup or changed their mind.

Trial labels and renewal terms were visible on audited 2.1.40 screens with trial data. The existing-subscriber plan-change question remains unknown because no recording with the required account state was available. Keep it scoped to the [Android trial-badge issue (psmobile #4225)](https://github.com/funcountry/psmobile/issues/4225).

Source: [Visible free-trial label and renewal terms](https://share.fun.country/20260901-3e8e184c94c8/media/trial-visible.jpg)

## Make five bounded changes

Finish the narrow product repairs and reporting work, then locate Android cancellation around the native billing handoff before changing paywall design or traffic strategy. Individual implementation owners and delivery dates are unknown in the source.

### 1. Add safe recovery while purchase status remains unknown

After a bounded wait for evidence, replace the disabled-only primary action with Check again or the existing Restore/reconcile action, plus a safe exit. Keep Buy disabled while purchase status is unknown and preserve the double-charge guard.

Use one focused test where the native purchase future never completes: recovery must become available without permitting a second charge. Use another where a late purchase completes after the watchdog: access must be granted once and pending state must clear.

### 2. Keep internal exceptions out of player copy

At the [puzzle deeplink resolver, lines 284–287](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/features/puzzles/presentation/screens/puzzles_deeplink_resolver_screen.dart:284), map the subtitle to one player-safe message and retain the full failure in structured logs. Preserve Retry and Back to puzzles.

A unit or widget test should pass an exact-owner failure and verify that rendered text contains no provider, identity or internal class names.

### 3. Record whether an offering recovers or the player exits

Preserve Retry and add one final-disposition field to the existing offering-state event. Suggested values are recovered, backed out, refresh failed and never ready.

That field separates the roughly 5-second and 66-second recoveries from the 8-to-10-second abandonment without another event family, dashboard or state machine. Retry mitigates the experience; it does not establish that the provider cause is fixed.

### 4. Repair the existing canonical checkout model

Use distinct paygate sessions, include the PostHog presentation-invariant family, and reconcile late purchases with purchase precedence. Expose commits without starts and starts without terminal outcomes as coverage warnings in the existing dbt and Evidence surfaces.

### 5. Locate cancellation around the native billing handoff

Start with existing events and distinguish app decline before native handoff, native user cancellation, and cancellation after a store-start event. Segment those outcomes by paygate surface and acquisition group.

If the existing terminal event cannot express that location, add one enum to it. PostHog remains a control for app-owned screens; it cannot show which native Google Play plan, payment method or error the player saw.

### Keep the repair scope small

Do not add a global retry around a potentially live native purchase, a new checkout event family, or a new replay classifier or proof pipeline. Avoid a broad offering rewrite. Do not reopen the merged [purchase-success handoff fix (psmobile #4662)](https://github.com/funcountry/psmobile/pull/4662).

## Appendix: theory dispositions

The recurring theories came from the August 31, August 24 and August 17 reports, as recorded in the [theory inventory](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/theory-inventory.md). Individual report links are unknown in the supplied audit.

| Theory | Finding and follow-through |
|---|---|
| An alternative paygate presentation path caused the platform gap. | The audit classified this theory as disproved: audited paygates rendered, accepted input and continued through purchases and cancellations. No replay or population split tied that path to the 34.3-point gap. Investigate cancellation at the native boundary. |
| Android hides trials that Google Play offers. | Eligibility-specific behavior remains unresolved because no qualified existing-subscriber plan-change recording was available. Eligible-looking screens showed labels and renewal terms. Retain the narrow [Android trial-badge issue (psmobile #4225)](https://github.com/funcountry/psmobile/issues/4225). |
| Purchase dismissal loses success or usable Plus access. | This historical defect is resolved in the [purchase-success handoff issue (psmobile #4438)](https://github.com/funcountry/psmobile/issues/4438) by the merged [purchase-success handoff fix (psmobile #4662)](https://github.com/funcountry/psmobile/pull/4662). Controls retained access, so this cohort does not justify reopening it. |
| RevenueCat exact-owner lookup blocks entitlement bootstrap. | A recording confirmed the failure and subsequent recovery after an unidentified manual control action. The [exact-owner entitlement-bootstrap issue (psmobile #4484)](https://github.com/funcountry/psmobile/issues/4484) remains open. Repair the separate client path that exposed its internal text. |
| Offering loading and refresh errors block valid paygates. | This defect is confirmed but rare. Six refresh failures, an abandoned load and a recovered delay justify preserving Retry and recording final outcomes. The stalled provider stage remains unknown. |
| Dead-session and route-removal guards block valid purchases. | The watched guards behaved as expected: players continued or no purchase UI was active. A duplicate-operation guard fired after successful access. No repair is justified by these controls. |
| Store-side purchase blocks explain the platform gap. | Errors are confirmed, but converting all final Android errors reaches only 25.5%. Continue the [Android purchase-not-allowed investigation (psmobile #4684)](https://github.com/funcountry/psmobile/issues/4684); errors cannot explain most of the gap. |
| Google Play download reporting was frozen. | Stale store reporting can coexist with live checkout recordings and canonical events. This is a reporting-coverage artifact; repair measurement without treating it as a player-flow failure. |
| Zero purchase-attributed coverage means no paid Android purchases. | Canonical outcomes contain real paid Android purchases. The zero reflects attribution or cross-system signal coverage failure. Repair reporting; it does not establish zero product conversion. |
| Android’s acquisition mix explains the checkout gap. | The test-market segment alone cannot explain the gap: removing 99 starts raises conversion only to 23.2%. The broader theory remains unresolved because other acquisition differences were not normalized. |
| Pending checkout lacks bounded recovery. | This newly identified source risk remains unresolved in replay. Both releases disable the primary button after the 10-second watchdog. One recording ends after 34.5 seconds of checking; longer holds are confounded by inactivity. Add safe recovery. |

## Appendix: release source and causal boundaries

The read-only [detached Android audit checkout](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901) uses Android 2.1.40 at [release commit f77a39bc1a53c5dadb5a664f2eadaa2264fda723](https://github.com/funcountry/psmobile/commit/f77a39bc1a53c5dadb5a664f2eadaa2264fda723). Android 2.1.39 uses [release commit 7144eb88f79865d5e07264d48a48f9a9f1fe70b5](https://github.com/funcountry/psmobile/commit/7144eb88f79865d5e07264d48a48f9a9f1fe70b5). These are the deployed and analyzed sources for the audit.

| Component | Source and behavior |
|---|---|
| Checkout watchdog | The [checkout observability source, line 12](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/core/subscriptions/purchase_execution/subscription_checkout_observability.dart:12) sets 10 seconds as an observability and control-return threshold. Reaching it does not establish that the store call failed. |
| Native purchase service | The [purchase service, lines 530–560](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/core/subscriptions/purchase_execution/subscription_purchase_service.dart:530) races the native purchase against the watchdog. It returns pending while late work continues, preserving later store evidence without inventing a terminal outcome. |
| Subscription journey | The [journey machine, lines 656–705](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/core/subscriptions/journey/subscription_journey_machine.dart:656) renders the checking view for nonterminal evidence. It retains protection against another charge while waiting. |
| Primary paywall button | The [paywall readiness component, lines 38–55](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/features/subscription/presentation/components/paywall_readiness_cta.dart:38) disables the primary action while checking. It prevents another purchase but offers no in-place recovery action in that state. |
| Puzzle error subtitle | The [puzzle deeplink resolver, lines 284–287](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901/apps/flutter/lib/features/puzzles/presentation/screens/puzzles_deeplink_resolver_screen.dart:284) displays `lastError.toString()`. This is the direct propagation path for the internal text visible in replay. |

The watchdog, purchase-service race and button behavior exist in both release tags. The purchase-service and button files are unchanged between tags. The journey machine changed, but both versions render checking for nonterminal evidence.

Pending checkout is a recovery blocker; it does not identify what initially delayed the native store. The resolver propagates internal copy from a separately owned provider failure. Offering stalls are confirmed availability failures with an unknown provider stage. Canonical reporting gaps impair observability without causing checkout failure.

## Appendix: cohort construction and evidence coverage

The cohort includes distinct checkout-start sessions (`paygate_checkout_started`) on Android and iOS releases 2.1.39 and 2.1.40. Its closed window runs from August 17 at 19:00 through August 31 at 19:00, exclusive; the source labels it August 18–31.

Each start was reconciled against store interaction (`subscription_checkout_store_interaction`), paygate result (`paygate_result`), checkout finish (`paygate_checkout_finished`) and purchase commit (`subscription_commit`). A valid purchase or commit takes precedence over a conflicting later error or cancellation. A start without a canonical terminal remains unresolved. The five Android and three iOS 2.1.40 commits without starts were excluded from the denominator.

The replay selection contained all 21 recent explicit Android store-error recordings, 15 matched flow and control cases, six long-unresolved captures and four additional offering-problem recordings. The delayed-offering recording appears in both the flow and long-unresolved sets, leaving 45 unique assigned recordings.

Forty-four of 45 recordings were available and watched end to end, frame by frame. One was retention-expired and returned 404. Two available recordings ended before their assigned event; their visual outcomes remain unknown rather than inferred.

PostHog and warehouse clocks differ by seconds, and HogQL rendered some times in the reader’s local clock. Event order and recording-relative time therefore took precedence over exact timestamp equality. Near-zero activity, native handoff and a later foreground-return event limited what a static frame could establish.

| Evidence source | Coverage and limit |
|---|---|
| BigQuery | Canonical queries established the 575-start population, corrected outcomes, acquisition groups, offering states and instrumentation gaps. |
| PostHog events | Events established ordering, lifecycle transitions, duplicate emissions, store outcomes, late commits and offering recovery. |
| PostHog recordings | Production recordings directly reproduced the client findings. Forty-five unique recordings were assigned, 44 were watched in full, one returned 404, and two assigned moments fell outside the available windows. |
| Sentry | No new causal claim relied on Sentry. The existing [exact-owner entitlement-bootstrap issue (psmobile #4484)](https://github.com/funcountry/psmobile/issues/4484) owns the provider failure; the new observation concerns unsafe presentation. |
| Fly logs | Backend logs were unnecessary for the observed client pixels. No new backend-producer claim extended the existing [exact-owner entitlement-bootstrap issue (psmobile #4484)](https://github.com/funcountry/psmobile/issues/4484). |
| Device or simulator | Production recordings supplied the reproduced app pixels, so no device or simulator reproduction was needed. Native Google Play UI remains outside PostHog capture. |

The same-class search in the [regression ledger](/Users/aelaguiz/workspace/psagentspace/REGRESSIONS.md) found existing RevenueCat offering-stall, Android purchase-not-allowed, exact-owner entitlement-bootstrap and Android trial-copy mismatch classes. The audit extended their population and replay evidence and added the separate client error-presentation path without duplicating the provider owner.

No source code, production state, provider state, app data or issue state changed during the September 1 audit.

## Appendix: limitations and private material

Native billing pixels are unavailable. Surrounding app state and lifecycle events can establish continuation, but cannot identify Google Play’s plan, payment method or native error.

A held mobile frame persists through inactivity and OS suspension. The [daily-limit capture (long-unresolved case 2)](https://us.posthog.com/project/215955/replay/01a05a32-986b-79cb-840c-81df148a2a54) records a foreground return; the [backgrounded onboarding capture (long-unresolved case 3)](https://us.posthog.com/project/215955/replay/01a03bfd-e21d-7a4e-bc9d-3189e4c642a6) records backgrounding after checkout. Neither proves a long foreground freeze.

The [unavailable Settings store-error recording (case 19)](https://us.posthog.com/project/215955/replay/01a016b9-f6aa-7d23-b292-61280ef9a174) returns 404. The [onboarding store-error recording (case 18)](https://us.posthog.com/project/215955/replay/01a01cb4-114b-77b5-96a1-32b1ef24be59) ends about 51 seconds before its error, and the [onboarding checkout recording (flow case 7)](https://us.posthog.com/project/215955/replay/01a046bf-e22f-7304-a93c-9227053f52c9) ends about 32 seconds before checkout. Those moments cannot be visually adjudicated.

The trial-badge question lacks the required existing-subscriber plan-change account state. Cancellation cause and the broader acquisition-mix contribution remain unknown. The source does not establish which internal-error recovery control was tapped or how often pending checkout traps an active foreground player.

Raw recordings, timelines and identifier-bearing extracts remain in the git-ignored [private replay directory](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replays.local/), excluded from the shared artifact. Shared screenshots were manually checked and contain no user IDs, device IDs, emails, IPs, tokens or account identifiers. Replay links require an authenticated PostHog session with access to project 215955.

## Appendix: source inventory

Sources: [Published September 1 audit](https://share.fun.country/20260901-3e8e184c94c8/index.html) · [Final working report](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/android-monetization-replay-audit.md) · [Theory inventory](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/theory-inventory.md) · [Candidate and sampling record](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/session-candidates.md) · [Read-only release checkout](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901)

Store-error reviews: [Cases 15–21](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/error-cases-15-21.md) · [Cases 8–14](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/error-cases-08-14.md) · [Cases 1–7](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/error-cases-01-07.md)

Flow-control reviews: [Cases 9–15](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/flow-cases-09-15.md) · [Cases 1–8](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/flow-cases-01-08.md)

Additional reviews: [Long-unresolved cases and final adjudication](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/long-unresolved-cases.md) · [Exhaustive offering review](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/all-offering-problems.md)

The rendered source was fetched September 6, 2026. The conclusions and issue dispositions retain the September 1 audit date.

## Appendix: authenticated replay index

All available recordings were watched in full during the original audit. Case labels preserve its index. Individual source dates are retained because per-case timestamps for conversion to Chicago dates are unknown in the supplied audit.

### Explicit store-error cases

| Recording | Observed result |
|---|---|
| [Store-error case 1 · Aug. 31 · Energy, purchase not allowed](https://us.posthog.com/project/215955/replay/01a058ce-e379-73c7-b647-0858588a7e9a) | The paygate closed without an explanation, and the player continued browsing. |
| [Store-error case 2 · Aug. 31 · Onboarding, purchase not allowed](https://us.posthog.com/project/215955/replay/01a055d2-61fc-7275-9e38-36e25c6990a4) | The native-store portion was not captured. A later purchase committed. |
| [Store-error case 3 · Aug. 30 · Onboarding, purchase not allowed](https://us.posthog.com/project/215955/replay/01a05079-d6e6-7520-8936-178ea6b541b4) | The failure appeared silent, but the frame evidence is lower confidence. The visual outcome remains uncertain. |
| [Store-error case 4 · Aug. 29 · Onboarding, purchase invalid](https://us.posthog.com/project/215955/replay/01a04b8a-3003-770c-9dd8-923a714a8899) | No defect was visible; onboarding continued. |
| [Store-error case 5 · Aug. 27 · Onboarding, purchase invalid](https://us.posthog.com/project/215955/replay/01a044f5-cd37-7eff-a0c0-007a661bc57b) | The native-store portion was not captured. A later purchase committed. |
| [Store-error case 6 · Aug. 27 · Post-puzzle, purchase not allowed](https://us.posthog.com/project/215955/replay/01a040d2-77e5-7807-9422-fdb9c7d5e805) | The failure was silent, and the player continued for more than 25 minutes. |
| [Store-error case 7 · Aug. 27 · Onboarding, purchase not allowed](https://us.posthog.com/project/215955/replay/01a04082-8deb-7cf2-a918-d117015ee3e5) | Internal entitlement text appeared. A manual action preceded recovery, but which control was tapped is unknown. |
| [Store-error case 8 · Aug. 26 · Lesson Energy, store problem](https://us.posthog.com/project/215955/replay/01a03b96-3d60-7de4-9860-2c9d9c1792a1) | The first failure was silent. The paygate appeared again, and the purchase committed. |
| [Store-error case 9 · Aug. 25 · Onboarding, purchase not allowed](https://us.posthog.com/project/215955/replay/01a039b9-7daa-7e48-8013-1ae08ca38bc0) | An alternate paygate appeared, and the player declined normally. |
| [Store-error case 10 · Aug. 25 · Onboarding, purchase not allowed](https://us.posthog.com/project/215955/replay/01a0395a-5e41-72b3-a639-f0710fdb412d) | A clear purchase-not-allowed dialog appeared, and the player continued along the free path. |
| [Store-error case 11 · Aug. 24 · Onboarding, network error](https://us.posthog.com/project/215955/replay/01a032d5-f103-7bc3-879b-ec9158334f74) | The network failure was silent, and free play continued. |
| [Store-error case 12 · Aug. 22 · Onboarding, purchase not allowed](https://us.posthog.com/project/215955/replay/01a02b16-ae9c-738e-b3b0-e4f1f25e4028) | No joined event or visible paywall was available. The visual outcome remains unknown. |
| [Store-error case 13 · Aug. 22 · Onboarding, purchase invalid](https://us.posthog.com/project/215955/replay/01a02a7f-c37b-7170-bb26-d1268c422151) | The native capture was corrupted. An automatic retry committed the purchase. |
| [Store-error case 14 · Aug. 21 · Onboarding, store problem](https://us.posthog.com/project/215955/replay/01a0223b-1b2c-7e9d-b0e7-2049dd63feca) | The store failure was silent, and no retry was visible. |
| [Store-error case 15 · Aug. 21 · Onboarding, store problem](https://us.posthog.com/project/215955/replay/01a02235-f632-7102-b8d2-91d1f00f7a86) | A clear store-problem dialog appeared, and play continued. |
| [Store-error case 16 · Aug. 20 · Onboarding, purchase not allowed](https://us.posthog.com/project/215955/replay/01a020c4-29aa-7b27-a6fd-a868a8ecb3cb) | The failure appeared silent, but no player block was observed. |
| [Store-error case 17 · Aug. 20 · Onboarding, store problem](https://us.posthog.com/project/215955/replay/01a01f60-6aa3-7480-a352-542e6ab584e7) | A clear store-problem dialog appeared, and play continued. |
| [Store-error case 18 · Aug. 20 · Onboarding, store problem](https://us.posthog.com/project/215955/replay/01a01cb4-114b-77b5-96a1-32b1ef24be59) | The assigned error occurred about 51 seconds after the recording ended. Its visible outcome is unknown. |
| [Store-error case 19 · Aug. 18 · Settings, store problem](https://us.posthog.com/project/215955/replay/01a016b9-f6aa-7d23-b292-61280ef9a174) | The recording returned 404 and was unavailable. Its visible outcome is unknown. |
| [Store-error case 20 · Aug. 18 · Onboarding, purchase already in progress](https://us.posthog.com/project/215955/replay/01a01695-297a-7ed3-83d2-f4459d8cdfd1) | The purchase succeeded, and the duplicate-operation guard caused no visible problem. |
| [Store-error case 21 · Aug. 18 · Onboarding, purchase not allowed](https://us.posthog.com/project/215955/replay/01a015e2-507a-7aba-b04c-e0626a2c8427) | Telemetry recorded the error during browsing, with no purchase UI open. |

### Matched flow and control cases

| Recording | Observed result |
|---|---|
| [Flow case 1 · App 2.1.40 · Post-puzzle cancellation](https://us.posthog.com/project/215955/replay/01a05a91-7348-713f-ad1a-4fbd6b750d4c) | The player declined normally, and puzzle results remained usable. |
| [Flow case 2 · App 2.1.40 · Onboarding cancellation](https://us.posthog.com/project/215955/replay/01a05a56-43e7-758e-8147-145be0a72d0b) | The player cancelled voluntarily. Native-store capture gaps were present, but no app defect was observed. |
| [Flow case 3 · App 2.1.40 · Settings cancellation](https://us.posthog.com/project/215955/replay/01a0580a-e5e4-78a1-ae35-e9d6552ad16d) | The player cancelled voluntarily from Settings without a visible defect. |
| [Flow case 5 · App 2.1.40 · Delayed offering and unresolved checkout](https://us.posthog.com/project/215955/replay/01a05a32-986b-79cb-840c-81df148a2a54) | The offering recovered after about 66 seconds, exactly 66.253 seconds. A later checkout had no terminal outcome. |
| [Flow case 6 · App 2.1.40 · Unresolved onboarding checkout](https://us.posthog.com/project/215955/replay/01a05795-a8c4-7b10-bde2-ed0ee0e8afa6) | The recording ended on “Checking purchase…”. A native capture gap is likely but unproven; the outcome remains unknown. |
| [Flow case 7 · App 2.1.40 · Unresolved onboarding checkout](https://us.posthog.com/project/215955/replay/01a046bf-e22f-7304-a93c-9227053f52c9) | The assigned checkout occurred about 32 seconds after recording ended. Its visible outcome is unknown. |
| [Flow case 9 · App 2.1.40 · Successful onboarding purchase](https://us.posthog.com/project/215955/replay/01a05aa2-f93c-713e-ad98-ea62a431caa3) | The purchase completed without a visible defect. |
| [Flow case 10 · App 2.1.40 · Successful onboarding purchase](https://us.posthog.com/project/215955/replay/01a05514-8034-7e08-823c-c0f4692727c6) | The purchase completed despite an 88-second checkout capture gap. Replay cannot distinguish a native overlay from uncaptured app UI. |
| [Flow case 11 · App 2.1.40 · Successful lesson-energy purchase](https://us.posthog.com/project/215955/replay/01a057fe-e92e-70b3-8e8d-19da742eb3bd) | The purchase completed. Later trial-cancellation telemetry did not undo access. |
| [Flow case 4 · App 2.1.39 · Onboarding cancellation](https://us.posthog.com/project/215955/replay/01a05426-3863-7c12-b37f-dcaea50b5e26) | The player cancelled normally and continued into puzzle play. |
| [Flow case 8 · App 2.1.39 · Unresolved onboarding checkout](https://us.posthog.com/project/215955/replay/01a03fd2-3dc2-7c85-81cd-a40abdd6932b) | The first decline was normal. The recording cut off the second attempt while it was in flight. |
| [Flow case 12 · App 2.1.39 · Successful onboarding purchase](https://us.posthog.com/project/215955/replay/01a04ac1-889b-751a-adb6-ec187f7b3dd3) | The purchase completed, and a process restart recovered cleanly. |
| [Flow case 13 · App 2.1.39 · Repeated offering refresh failures](https://us.posthog.com/project/215955/replay/01a02144-ccb7-713c-84a5-0daffc9ffdda) | Two refresh failures occurred. The player explicitly quit after the later energy-paygate failure. |
| [Flow case 14 · App 2.1.39 · Repeated offering refresh failures](https://us.posthog.com/project/215955/replay/01a02483-49b0-778c-af7f-1e818b15073b) | The same player experienced the recurring offering failure on another day. |
| [Flow case 15 · App 2.1.39 · Open-versus-presented instrumentation mismatch](https://us.posthog.com/project/215955/replay/01a03caf-2226-74dc-b734-19be96967aa1) | The player visibly cancelled normally, but the events were duplicated three to four times. |

### Long-unresolved cases

| Recording | Observed result |
|---|---|
| [Long-unresolved case 1 · App 2.1.40 · Onboarding](https://us.posthog.com/project/215955/replay/01a05495-f2af-77fa-932a-b879a53048de) | The 19-hour span contains only 73 active seconds and recovery that resembles a relaunch. It does not prove a foreground hang. |
| [Long-unresolved case 2 · App 2.1.40 · Play vs AI Daily Limit](https://us.posthog.com/project/215955/replay/01a05a32-986b-79cb-840c-81df148a2a54) | The one-hour frame hold ends with a foreground-return event (`app_foreground`). Inactivity or backgrounding explains the gap; it does not prove an hour-long foreground freeze. |
| [Long-unresolved case 5 · App 2.1.40 · Onboarding](https://us.posthog.com/project/215955/replay/01a05047-8f7a-7715-9121-f217c1606dba) | The recording ends 34.5 seconds into “Checking purchase…”. The eventual outcome remains unknown. |
| [Long-unresolved case 3 · App 2.1.39 · Onboarding](https://us.posthog.com/project/215955/replay/01a03bfd-e21d-7a4e-bc9d-3189e4c642a6) | The app recorded backgrounding (`app_background`) 47 seconds after checkout. The pending record later aged out. |
| [Long-unresolved case 4 · App 2.1.39 · Onboarding](https://us.posthog.com/project/215955/replay/01a0345f-ba62-76ed-b90f-3b189659029d) | The player declined normally, entered puzzles and kept playing. |
| [Long-unresolved case 6 · App 2.1.39 · Onboarding](https://us.posthog.com/project/215955/replay/01a02373-530e-7ad4-816d-4f3646b8b3c3) | The checking state cleared to “Opening puzzle…” in about 20 seconds. |

### Additional offering-problem recordings

| Recording | Observed result |
|---|---|
| [Aug. 31 · App 2.1.40 lesson energy](https://us.posthog.com/project/215955/replay/01a0550c-e8a1-7da3-a685-567ded95bfed) | App-owned offering loading remained visible for roughly 8 to 10 seconds. The player backed out before it reached ready. |
| [Aug. 31 · App 2.1.40 onboarding](https://us.posthog.com/project/215955/replay/01a05543-4696-7632-8f08-2c7eae7f7a6a) | The pending offering recovered to localized pricing and an active primary button in about 5 seconds, exactly 4.986 seconds. |
| [Aug. 27 · App 2.1.39 onboarding](https://us.posthog.com/project/215955/replay/01a042f5-56a9-7cfa-8523-bfdd0a21cc4f) | A load-plans error remained visible for about five seconds, then the player continued into a puzzle. |
| [Aug. 19 · App 2.1.39 onboarding](https://us.posthog.com/project/215955/replay/01a01936-4242-788b-8394-7357417b030f) | An offering error was emitted during a normal exit to Learn. No failure was visible in the captured frames. |
