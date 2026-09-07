# Fix checkout recovery and measurement, then locate why Android players cancel.

September 1, 2026 · Poker Skill · Android monetization audit for releases 2.1.40 and 2.1.39. Times use Chicago time; replay durations are elapsed time.

Android converted 20.7% of checkout starts (73 of 353), versus iOS at 55.0% (122 of 222); extra cancellations account for 77.4% of that 34.3-point gap.

The three product repair areas are pending-checkout recovery, player-facing error handling, and rare offering failures. Repair those and the reporting gaps before changing paywall design or traffic strategy. Broad paywall-loading failure and mass foreground hangs are not established. The reason for cancellation around the native Google Play handoff remains unknown because PostHog cannot capture that billing sheet.

## Android’s conversion gap is mostly cancellations

Android had 26.5 percentage points more cancellations than iOS, compared with 4.7 points more unresolved outcomes and 3.0 points more explicit errors.

| Platform | Checkout starts | Purchased, count (%) | Cancelled, count (%) | Error, count (%) | Unresolved, count (%) |
|---|---|---|---|---|---|
| Android | 353 | 73 (20.7%) | 232 (65.7%) | 17 (4.8%) | 31 (8.8%) |
| iOS | 222 | 122 (55.0%) | 87 (39.2%) | 4 (1.8%) | 9 (4.1%) |

The 575 starts belong to a closed cohort. These outcome differences locate the purchase-rate gap; they do not establish why players cancelled.

| Excess Android outcome versus iOS | Percentage points | Share of purchase-rate gap |
|---|---|---|
| Cancellation | 26.5 | 77.4% |
| Unresolved | 4.7 | 13.8% |
| Error | 3.0 | 8.8% |

Even if all 17 final Android error outcomes became purchases, Android would convert only 25.5% of starts, still far below iOS at 55.0%. Store errors are real but cannot explain most of the gap; continue the [Android purchase-not-allowed investigation (psmobile #4684)](https://github.com/funcountry/psmobile/issues/4684).

### Both releases convert below iOS

Android improved 3.9 percentage points from 19.6% in 2.1.39 to 23.5% in 2.1.40, so the later release did not introduce a broad new collapse.

| Platform and release | Starts | Purchased | Purchase rate |
|---|---|---|---|
| Android 2.1.40 | 98 | 23 | 23.5% |
| Android 2.1.39 | 255 | 50 | 19.6% |
| iOS 2.1.40 | 75 | 47 | 62.7% |
| iOS 2.1.39 | 147 | 75 | 51.0% |

### Removing test-market traffic leaves most of the gap

Excluding the 99 test-market starts raises Android conversion only 2.5 points, from 20.7% to 23.2% (59 purchases from 254 remaining starts), far short of the 34.3-point platform gap.

| Acquisition group | Starts | Purchased | Purchase rate | Cancelled | Error | Unresolved |
|---|---|---|---|---|---|---|
| Main paid campaigns | 169 | 34 | 20.1% | 105 | 11 | 19 |
| Test-market paid campaigns | 99 | 14 | 14.1% | 74 | 2 | 9 |
| Unlinked or organic | 77 | 22 | 28.6% | 48 | 4 | 3 |
| Other attributed campaigns | 8 | 3 | 37.5% | 5 | 0 | 0 |

The labeled test-market segment converted worse, but the broader acquisition-mix explanation remains unresolved. Other Android and iOS acquisition differences were not normalized; their contribution is unknown.

## Rare offering failures block valid paygates

Android offerings reached ready in 99.1% of paygate sessions (881 of 889), while a small set of visible loading and refresh failures interrupted checkout.

| Android release | Paygate sessions | Reached ready, sessions | Refresh failed, sessions | Still pending, sessions | No ready or error, sessions |
|---|---|---|---|---|---|
| 2.1.40 | 249 | 248 | 0 | 3 | 1 |
| 2.1.39 | 640 | 633 | 6 | 0 | 1 |

These offering states can overlap: two of the three 2.1.40 sessions that were still pending later reached ready, after 4.986 and 66.253 seconds. The remaining player backed out after roughly 8 to 10 seconds of loading and never received a ready event.

A 2.1.40 lesson-energy paygate displayed only app-owned “Loading plans…” for those 8 to 10 seconds. The player backed out and chose Keep Learning; neither an offering-ready nor a terminal offering-error event followed. Source: [Lesson-energy paygate abandoned while loading](https://share.fun.country/20260901-3e8e184c94c8/media/offering-abandoned.jpg).

A separate 2.1.40 Play vs AI daily-limit paygate showed “This is taking longer than expected” and Retry for about 58 seconds before pricing appeared. Its canonical ready event arrived 66.253 seconds after the pending state (`still_pending`). Source: [Play vs AI offering delay that recovered](https://share.fun.country/20260901-3e8e184c94c8/media/offering-stall.jpg).

Both sequences show app-owned screens, so missing Google Play pixels cannot explain the visible delays. Retry and eventual pricing worked in the recovered case; the other player could exit, but the offering never became ready.

The six refresh failures in 2.1.39 affected three people or devices. Four failures belonged to one player across two consecutive days. In the strongest sequence, the first failure allowed lessons to continue; a repeated energy-gate failure was immediately followed by an explicit lesson quit.

Offering failure is confirmed and uncommon. The exact provider stage that stalled is unknown for this cohort. Preserve Retry, then record each session’s final disposition; recovery does not establish that the provider cause is repaired.

## Purchase errors sometimes disappear silently or expose internal details

The 21 explicit store-error recordings included clear dialogs, silent returns to content, and one internal entitlement error shown to a player.

| Error class | Recordings |
|---|---|
| Purchase not allowed | 10 |
| Store problem | 6 |
| Purchase invalid | 3 |
| Network error | 1 |
| Duplicate operation guard | 1 |

Four affected players later committed purchases. Some failures produced clear, dismissible purchase dialogs; several returned silently to ordinary play. One puzzle error screen exposed an internal RevenueCat and Clerk exact-owner failure for about 15 seconds. A manual action in the two-control error area was followed by recovery; the tapped control is unknown because the pixels cannot distinguish Try again from Back to puzzles. Source: [Internal entitlement error shown to the player](https://share.fun.country/20260901-3e8e184c94c8/media/internal-error.jpg).

The [Puzzle deep-link resolver, lines 284–287](https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/features/puzzles/presentation/screens/puzzles_deeplink_resolver_screen.dart#L284-L287) renders `_resolution.lastError?.toString()` as the subtitle. This is the confirmed, narrow and transient propagation defect. Keep diagnostics in structured logs and replace the subtitle with player-safe copy. The provider failure remains separately owned by the open [RevenueCat exact-owner entitlement-bootstrap failure (psmobile #4484)](https://github.com/funcountry/psmobile/issues/4484).

## Pending checkout can leave the buy button disabled without a recovery action

After 10 seconds without a terminal result, the paywall can show “Checking purchase…” with no in-place recovery action if purchase evidence never arrives.

The watchdog returns control with a pending outcome while the native purchase future continues. The journey renders `SubscriptionJourneyView.checking` and disables the primary CTA. A back arrow remains, but the inspected state offers no timeout-specific Check again or Restore action. Sources: [Checkout watchdog, line 12](https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/core/subscriptions/purchase_execution/subscription_checkout_observability.dart#L12) · [Native purchase and watchdog race, lines 530–560](https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/core/subscriptions/purchase_execution/subscription_purchase_service.dart#L530-L560) · [Purchase journey, lines 656–705](https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/core/subscriptions/journey/subscription_journey_machine.dart#L656-L705) · [Paywall CTA, lines 38–55](https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/features/subscription/presentation/components/paywall_readiness_cta.dart#L38-L55) · [Disabled Checking purchase button](https://share.fun.country/20260901-3e8e184c94c8/media/checking-risk.jpg).

Disabling Buy protects against a double charge and allows late native or canonical evidence to resolve the purchase. The recovery risk is an unbounded wait if neither result arrives. The initiating native-store cause is unknown.

All 31 unresolved Android starts had a store-start event and no later canonical terminal; 30 had recordings. These counts do not establish 31 hangs. The six longest selected captures contained one confirmed background transition, two visible forward-progress outcomes, one recording ending 34.5 seconds into checking, and two gaps dominated by inactivity with recovery resembling a relaunch.

Systemic foreground incidence remains unknown. One long capture explicitly logged backgrounding (`app_background`); another logged return to foreground (`app_foreground`). Held mobile frames can span inactivity or OS control of the screen. Add bounded recovery while preserving the double-charge guard.

## Canonical checkout coverage needs one reconciled session model

Missing and duplicated events distort the conversion analysis without causing the player’s checkout to fail.

| Measurement gap | What it changes |
|---|---|
| PostHog recorded 153 Android presentation-invariant events (`paygate_presentation_invariant`) across 2.1.39 and 2.1.40; canonical BigQuery recorded zero. | Bring this event family into the existing canonical path. |
| Five Android and three iOS purchase commits on 2.1.40 lacked a checkout-start event (`paygate_checkout_started`). | Exclude them from the start denominator and expose the missing starts as coverage warnings. |
| One visible cancellation emitted three to four copies of `paygate_opened` and `paygate_result`, two checkout start-finish cycles, and a late cancellation-verification event. | Count distinct paygate sessions; raw event totals overcount the player’s action. |
| The benefits CTA event (`subscription_benefits_cta`) records navigation from benefits to billing. | Keep that navigation separate from a store purchase click. |
| Some successful purchases lacked a store-start event. | Reconcile events at session level; raw event-family counts do not provide a complete checkout population. |

Google Play download reporting can stay stale while checkout recordings and canonical app events continue. Zero purchase-attributed coverage also does not mean zero paid Android purchases: canonical outcomes include real paid purchases. Repair signal parity and attribution coverage in the existing dbt and Evidence surfaces.

## Successful purchases and cancellation controls preserve access

Four matched successful-purchase controls purchased and continued with entitlements; their captured app states never contradicted canonical outcomes.

One recovered cleanly after a full process restart. Another displayed unlimited energy after purchase despite a duplicate-operation guard event. Source: [Unlimited energy after successful purchase](https://share.fun.country/20260901-3e8e184c94c8/media/purchase-success.jpg).

The historical [Purchase-success handoff (psmobile #4438)](https://github.com/funcountry/psmobile/issues/4438) was valid and is closed through the merged [Purchase-success handoff repair (psmobile #4662)](https://github.com/funcountry/psmobile/pull/4662). This cohort supplies no reason to reopen entitlement-loss work.

Cancellation controls showed ordinary declines, native-store round trips, and continued free content. Static frames around a later foreground-return event were native or background capture gaps. The recordings cannot establish whether players rejected Google Play’s sheet, disliked the price, lacked valid payment setup, or changed their minds.

The audited 2.1.40 screens with trial data showed the free-trial label and renewal terms. Eligibility-specific behavior is unknown because no qualifying existing-subscriber plan-change recording was available. Keep the investigation scoped to the [Android trial-badge eligibility (psmobile #4225)](https://github.com/funcountry/psmobile/issues/4225). Source: [Visible free-trial label and renewal terms](https://share.fun.country/20260901-3e8e184c94c8/media/trial-visible.jpg).

## Make five focused repairs and checks

Use the existing checkout events and models to fix the observed defects and locate cancellation around native handoff.

### 1. Give pending checkout a bounded recovery state

Keep the double-charge guard. After a bounded evidence wait, replace the disabled-only action with Check again or the existing Restore or reconciliation action plus a safe exit. Do not re-enable Buy while purchase status is unknown.

Test a native purchase future that never completes: recovery must become available without allowing a second charge. Test a late purchase completing after the watchdog: access must be granted once and pending state must clear.

### 2. Stop rendering internal exceptions as player copy

Keep the full failure in structured logs at the [Puzzle deep-link resolver, lines 284–287](https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/features/puzzles/presentation/screens/puzzles_deeplink_resolver_screen.dart#L284-L287) and map the subtitle to one player-safe message. Preserve Retry and Back to puzzles. A unit or widget test should pass an exact-owner failure and verify that provider, identity, and internal class names do not appear in rendered text.

### 3. Preserve offering Retry and record the final outcome

Add a final-disposition field to the existing offering-state event, with values such as recovered, backed out, refresh failed, or never ready. This distinguishes the 4.986-second and 66.253-second recoveries from the 8-to-10-second abandonment with no ready event. No new event family, dashboard, or state machine is needed.

### 4. Repair the canonical checkout model

Use distinct paygate sessions. Include PostHog’s presentation-invariant events, give valid purchases precedence when reconciling late outcomes, and show commits without starts and starts without terminals as coverage warnings. Keep the work in the existing dbt and Evidence surfaces.

### 5. Locate cancellations around native handoff

Use existing events to separate app declines before native handoff, native user cancellations, and cancellations after a store-start event. Segment by paygate surface and acquisition group. If the current terminal event cannot express the location, add one enum to it.

Keep PostHog replay as a control for app-owned screens. It cannot reveal the Google Play plan, payment method, or native error the player saw. The implementation owners and dates for these five actions are unknown in the source.

Do not add a global retry around a possibly live native purchase, a new checkout event family, a replay classifier or proof pipeline, or a broad offering rewrite. Keep the merged purchase-success handoff work closed.

## Appendix: method and evidence coverage

### Cohort and outcome reconciliation

The closed cohort contains 575 distinct checkout-start sessions on Android or iOS 2.1.39 or 2.1.40. Its Chicago boundaries are August 17 at 19:00 through August 31 at 19:00, with the end excluded; this preserves the source’s full August 18–31 date window.

Each `paygate_checkout_started` was reconciled against `subscription_checkout_store_interaction`, `paygate_result`, `paygate_checkout_finished`, and `subscription_commit`. A valid purchase or commit took precedence over conflicting later errors or cancellations. Starts without canonical terminal outcomes remained unresolved. The five Android and three iOS commits without starts were excluded rather than allowed to inflate conversion.

Warehouse and PostHog clocks can differ by seconds; some HogQL timestamps used the reader’s local clock. Adjudication therefore used event order and recording-relative time rather than second-level timestamp equality.

### Production observation and release sources

Production recordings directly reproduced the visible defects. Canonical BigQuery events were joined to complete PostHog mobile recordings and checked against the exact release source.

| Source | Evidence and limits |
|---|---|
| BigQuery | The closed population supplied corrected checkout outcomes, acquisition groups, offering states, and instrumentation gaps. |
| PostHog events | Events supplied ordering, lifecycle changes, duplicate emissions, store outcomes, late commits, and offering recovery. |
| PostHog recordings | The selection assigned 45 unique recordings. All 44 available recordings were watched end to end; one returned 404, and two assigned moments occurred outside their recording windows. |
| Sentry | No new causal claim used Sentry. The [RevenueCat exact-owner issue (psmobile #4484)](https://github.com/funcountry/psmobile/issues/4484) owns the provider class; the observed client defect is unsafe presentation of its internal error. |
| Fly logs | Client-visible findings did not require Fly logs. No backend-producer claim extended beyond the existing exact-owner issue. |
| Device or simulator | Production pixels established the visible failures without another reproduction. Native Google Play UI was not captured, so its contents remain unknown. |

The recorded detached worktree is unavailable at its original path; its current location is unknown. The exact release files are linked by commit.

Android 2.1.40 and the [Detached read-only Android release checkout](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901) used [release commit f77a39bc1a53c5dadb5a664f2eadaa2264fda723](https://github.com/funcountry/psmobile/commit/f77a39bc1a53c5dadb5a664f2eadaa2264fda723). Android 2.1.39 used [release commit 7144eb88f79865d5e07264d48a48f9a9f1fe70b5](https://github.com/funcountry/psmobile/commit/7144eb88f79865d5e07264d48a48f9a9f1fe70b5).

| Release-code location | Behavior |
|---|---|
| [Checkout watchdog, line 12](https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/core/subscriptions/purchase_execution/subscription_checkout_observability.dart#L12) | The 10-second threshold returns control and records missing terminal evidence; it does not prove the store call failed. |
| [Native purchase and watchdog race, lines 530–560](https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/core/subscriptions/purchase_execution/subscription_purchase_service.dart#L530-L560) | Native purchase races the watchdog. Pending returns while late work continues, preserving access to the eventual store result. |
| [Purchase journey, lines 656–705](https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/core/subscriptions/journey/subscription_journey_machine.dart#L656-L705) | Nonterminal evidence renders the checking view and protects against another charge while waiting. |
| [Paywall CTA, lines 38–55](https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/features/subscription/presentation/components/paywall_readiness_cta.dart#L38-L55) | Checking disables the primary action, with no in-place recovery action in that state. |
| [Puzzle deep-link resolver, lines 284–287](https://github.com/funcountry/psmobile/blob/f77a39bc1a53c5dadb5a664f2eadaa2264fda723/apps/flutter/lib/features/puzzles/presentation/screens/puzzles_deeplink_resolver_screen.dart#L284-L287) | The subtitle displays `lastError.toString()`, which propagates the internal text seen in replay. |

The watchdog, purchase-service race, and CTA behavior exist in both release tags. The purchase service and CTA files are unchanged between them. The journey machine changed, but both versions render checking for nonterminal evidence.

The [Regression ledger](/Users/aelaguiz/workspace/psagentspace/REGRESSIONS.md) already contained offering stalls, Android purchase-not-allowed errors, exact-owner entitlement-bootstrap failures, and trial-copy mismatches. The audit extended their population and replay evidence and added the separate client presentation defect without duplicating the provider owner.

No source, production state, provider state, app data, or issue state changed during the original audit.

### Theory dispositions

The recurring theories came from the [August 31 operations draft](/Users/aelaguiz/workspace/psagentspace/_artifacts/2026-08-31-monday-update/DRAFT_EMAIL.md), [August 24 operations report](/Users/aelaguiz/workspace/psagentspace/_artifacts/2026-08-24-monday-update/SENT_EMAIL_2026-08-24.md), and [August 17 operations report](/Users/aelaguiz/workspace/psagentspace/_artifacts/2026-08-17-monday-update/SENT_EMAIL_2026-08-17.md). Source: [Theory inventory](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/theory-inventory.md).

| Theory | Final disposition and reason |
|---|---|
| Alternative paygate presentation caused the conversion gap | The audit classified this explanation as disproved. Paygates rendered, accepted input, entered checkout, and continued after purchases and cancellations; no replay or population split tied this path to the 34.3-point gap. |
| Android hides eligible trial badges | The claim remains unresolved because no qualified existing-subscriber plan-change recording was available. Trial data produced visible labels and renewal terms in the checked 2.1.40 screens; continue the [Android trial-badge eligibility (psmobile #4225)](https://github.com/funcountry/psmobile/issues/4225). |
| Purchase dismisses without success or usable Plus | The historical defect was confirmed and resolved through the [Purchase-success handoff (psmobile #4438)](https://github.com/funcountry/psmobile/issues/4438) and merged [Purchase-success handoff repair (psmobile #4662)](https://github.com/funcountry/psmobile/pull/4662). Purchase controls continued with entitlements; keep that work closed. |
| RevenueCat exact-owner lookup blocks entitlement bootstrap | The provider defect is confirmed and remains open under the [RevenueCat exact-owner entitlement-bootstrap failure (psmobile #4484)](https://github.com/funcountry/psmobile/issues/4484). The recording also confirms unsafe presentation; recovery followed a manual action, but the selected control is unknown. |
| Offering loading and refresh failures block valid paygates | The defect is confirmed and rare: six of 640 2.1.39 sessions had refresh failures, while 2.1.40 included an abandoned 8-to-10-second load and a roughly 58-second timeout that recovered. Preserve Retry and record final outcomes. |
| Dead-session and route-removal cleanup guards block purchases | The watched guards behaved as expected. Players continued or had no live purchase UI; one duplicate guard followed a successful purchase with unlimited energy. No player-facing block was reproduced. |
| Store-side purchase blocks explain the gap | Store, network, invalid-purchase, and purchase-not-allowed errors are confirmed, but the audit rejected them as the main cause. Converting all final Android errors would reach only 25.5%; continue the [Android purchase-not-allowed investigation (psmobile #4684)](https://github.com/funcountry/psmobile/issues/4684). |
| Google Play download reporting was frozen | Stale store reporting is a measurement artifact. Checkout recordings and canonical events continued; repair reporting coverage separately from player flow. |
| Zero purchase-attributed coverage means paid Android checkout failed | The zero is a signal-parity or attribution artifact because canonical outcomes include paid Android purchases. Repair coverage rather than infer zero conversion. |
| Overall acquisition mix explains the Android gap | The explanation remains unresolved because other acquisition differences were not normalized. Removing the 99 test-market starts raises Android only from 20.7% to 23.2%. |
| Checking purchase lacks bounded recovery | This newly identified source risk remains unresolved in production incidence. Both releases have the 10-second watchdog and disabled CTA; one recording ends after 34.5 seconds of checking, while longer holds are confounded by backgrounding or inactivity. Add safe recovery. |

### Sampling and limitations

Selection included all 21 recent Android recordings with explicit store errors, 15 matched flow and control recordings, the six longest available unresolved captures, and four additional offering-problem recordings. One delayed-offering recording belongs to both the flow and long-unresolved sets, giving 45 unique assignments.

Forty-four recordings were available and watched in full, frame by frame. [Store-error case 19](https://us.posthog.com/project/215955/replay/01a016b9-f6aa-7d23-b292-61280ef9a174) was retention-expired and returned 404. [Store-error case 18](https://us.posthog.com/project/215955/replay/01a01cb4-114b-77b5-96a1-32b1ef24be59)’s error occurred about 51 seconds after recording ended; [flow case 7](https://us.posthog.com/project/215955/replay/01a046bf-e22f-7304-a93c-9227053f52c9)’s checkout occurred about 32 seconds after recording ended. Those event moments remain unverified.

Black, torn, or held frames cannot prove a hang while native Google Play is uncaptured. Mobile replay preserves the last app screenshot during inactivity and OS suspension. [Long-unresolved case 2](https://us.posthog.com/project/215955/replay/01a05a32-986b-79cb-840c-81df148a2a54) logs foreground return; [Long-unresolved case 3](https://us.posthog.com/project/215955/replay/01a03bfd-e21d-7a4e-bc9d-3189e4c642a6) logs backgrounding after checkout. Surrounding app state, lifecycle events, and event order supplied the usable evidence.

The missing existing-subscriber account state leaves the trial-badge question unresolved. The cancellation outcome is measurable; its cause inside the billing sheet remains unknown. A native plan, payment method, or error cannot be inferred from these app-only recordings.

### Privacy and source inventory

[Private replay recordings, timelines, and extracts](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replays.local/) remain git-ignored and excluded from the shared artifact. Shared screenshots were manually checked and contained no user IDs, device IDs, emails, IPs, tokens, or account identifiers. Replay links require the existing authenticated PostHog session and access to project 215955.

Sources: [Final working audit, September 1, 2026](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/android-monetization-replay-audit.md) · [Theory inventory](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/theory-inventory.md) · [Candidate and sampling record](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/session-candidates.md).

Replay reviews: [Store-error reviews, cases 15–21](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/error-cases-15-21.md) · [Store-error reviews, cases 8–14](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/error-cases-08-14.md) · [Store-error reviews, cases 1–7](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/error-cases-01-07.md) · [Flow-control reviews, cases 9–15](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/flow-cases-09-15.md) · [Flow-control reviews, cases 1–8](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/flow-cases-01-08.md).

Additional evidence: [Long-unresolved reviews and final adjudication](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/long-unresolved-cases.md) · [Exhaustive offering review](/Users/aelaguiz/workspace/psagentspace/research/2026-09-01-android-monetization-replay-audit/replay-reviews/all-offering-problems.md) · [Detached read-only Android release checkout](/Users/aelaguiz/workspace/psmobile-worktrees/android-monetization-replay-audit-20260901).

### Authenticated replay index

Every available recording was watched in full during the original audit. Case numbers identify the source’s review assignments. Replay dates retain the original date labels; their time zone was not stated, so Chicago calendar dates are not verified.

#### Explicit store-error cases

| Recording | Observed outcome |
|---|---|
| [Store-error case 1 · Aug. 31 · Energy, purchase not allowed](https://us.posthog.com/project/215955/replay/01a058ce-e379-73c7-b647-0858588a7e9a) | The paygate closed silently, and the player continued browsing. |
| [Store-error case 2 · Aug. 31 · Onboarding, purchase not allowed](https://us.posthog.com/project/215955/replay/01a055d2-61fc-7275-9e38-36e25c6990a4) | Native-store pixels are missing; a later purchase committed. |
| [Store-error case 3 · Aug. 30 · Onboarding, purchase not allowed](https://us.posthog.com/project/215955/replay/01a05079-d6e6-7520-8936-178ea6b541b4) | The failure was likely silent, but the frame evidence has lower confidence. |
| [Store-error case 4 · Aug. 29 · Onboarding, purchase invalid](https://us.posthog.com/project/215955/replay/01a04b8a-3003-770c-9dd8-923a714a8899) | Onboarding continued with no visible defect. |
| [Store-error case 5 · Aug. 27 · Onboarding, purchase invalid](https://us.posthog.com/project/215955/replay/01a044f5-cd37-7eff-a0c0-007a661bc57b) | The native-store capture has a gap; a later purchase committed. |
| [Store-error case 6 · Aug. 27 · Post-puzzle, purchase not allowed](https://us.posthog.com/project/215955/replay/01a040d2-77e5-7807-9422-fdb9c7d5e805) | The failure was silent, and the player continued for more than 25 minutes. |
| [Store-error case 7 · Aug. 27 · Onboarding, purchase not allowed](https://us.posthog.com/project/215955/replay/01a04082-8deb-7cf2-a918-d117015ee3e5) | The screen exposed internal entitlement text; a manual action was followed by recovery. |
| [Store-error case 8 · Aug. 26 · Lesson energy, store problem](https://us.posthog.com/project/215955/replay/01a03b96-3d60-7de4-9860-2c9d9c1792a1) | The first failure was silent. The paygate reopened, and the purchase committed. |
| [Store-error case 9 · Aug. 25 · Onboarding, purchase not allowed](https://us.posthog.com/project/215955/replay/01a039b9-7daa-7e48-8013-1ae08ca38bc0) | An alternate paygate appeared, and the player declined normally. |
| [Store-error case 10 · Aug. 25 · Onboarding, purchase not allowed](https://us.posthog.com/project/215955/replay/01a0395a-5e41-72b3-a639-f0710fdb412d) | A clear purchase-not-allowed dialog appeared, and the player continued on the free path. |
| [Store-error case 11 · Aug. 24 · Onboarding, network error](https://us.posthog.com/project/215955/replay/01a032d5-f103-7bc3-879b-ec9158334f74) | The network failure was silent, and free play continued. |
| [Store-error case 12 · Aug. 22 · Onboarding, purchase not allowed](https://us.posthog.com/project/215955/replay/01a02b16-ae9c-738e-b3b0-e4f1f25e4028) | No joined event or visible paywall was available; the outcome remains unresolved. |
| [Store-error case 13 · Aug. 22 · Onboarding, purchase invalid](https://us.posthog.com/project/215955/replay/01a02a7f-c37b-7170-bb26-d1268c422151) | The native capture was corrupted; an automatic retry committed the purchase. |
| [Store-error case 14 · Aug. 21 · Onboarding, store problem](https://us.posthog.com/project/215955/replay/01a0223b-1b2c-7e9d-b0e7-2049dd63feca) | The store failure was silent, and no retry was visible. |
| [Store-error case 15 · Aug. 21 · Onboarding, store problem](https://us.posthog.com/project/215955/replay/01a02235-f632-7102-b8d2-91d1f00f7a86) | A clear store-problem dialog appeared, and play continued. |
| [Store-error case 16 · Aug. 20 · Onboarding, purchase not allowed](https://us.posthog.com/project/215955/replay/01a020c4-29aa-7b27-a6fd-a868a8ecb3cb) | The failure was likely silent; no player block was visible. |
| [Store-error case 17 · Aug. 20 · Onboarding, store problem](https://us.posthog.com/project/215955/replay/01a01f60-6aa3-7480-a352-542e6ab584e7) | A clear store-problem dialog appeared, and play continued. |
| [Store-error case 18 · Aug. 20 · Onboarding, store problem](https://us.posthog.com/project/215955/replay/01a01cb4-114b-77b5-96a1-32b1ef24be59) | The assigned error occurred about 51 seconds after recording ended; its visible outcome is unknown. |
| [Store-error case 19 · Aug. 18 · Settings, store problem](https://us.posthog.com/project/215955/replay/01a016b9-f6aa-7d23-b292-61280ef9a174) | The recording returned 404; its visible outcome is unknown. |
| [Store-error case 20 · Aug. 18 · Onboarding, purchase already in progress](https://us.posthog.com/project/215955/replay/01a01695-297a-7ed3-83d2-f4459d8cdfd1) | The purchase succeeded, and the duplicate-operation guard caused no visible problem. |
| [Store-error case 21 · Aug. 18 · Onboarding, purchase not allowed](https://us.posthog.com/project/215955/replay/01a015e2-507a-7aba-b04c-e0626a2c8427) | The error appeared only in telemetry during browsing; no purchase UI was open. |

#### Matched flow and control cases

| Recording | Observed outcome |
|---|---|
| [Flow case 9 · 2.1.40 · Successful onboarding purchase](https://us.posthog.com/project/215955/replay/01a05aa2-f93c-713e-ad98-ea62a431caa3) | The purchase succeeded with no visible defect. |
| [Flow case 1 · 2.1.40 · Post-puzzle cancellation](https://us.posthog.com/project/215955/replay/01a05a91-7348-713f-ad1a-4fbd6b750d4c) | The player declined normally, and puzzle results remained usable. |
| [Flow case 2 · 2.1.40 · Onboarding cancellation](https://us.posthog.com/project/215955/replay/01a05a56-43e7-758e-8147-145be0a72d0b) | The player cancelled voluntarily; native-store capture gaps limit visibility. |
| [Flow case 5 · 2.1.40 · Delayed offering and unresolved checkout](https://us.posthog.com/project/215955/replay/01a05a32-986b-79cb-840c-81df148a2a54) | The offering recovered after 66.253 seconds; the later checkout had no terminal outcome. |
| [Flow case 3 · 2.1.40 · Settings cancellation](https://us.posthog.com/project/215955/replay/01a0580a-e5e4-78a1-ae35-e9d6552ad16d) | The player cancelled voluntarily from Settings. |
| [Flow case 11 · 2.1.40 · Successful lesson-energy purchase](https://us.posthog.com/project/215955/replay/01a057fe-e92e-70b3-8e8d-19da742eb3bd) | The purchase succeeded; later trial-cancellation telemetry did not undo access. |
| [Flow case 6 · 2.1.40 · Unresolved onboarding checkout](https://us.posthog.com/project/215955/replay/01a05795-a8c4-7b10-bde2-ed0ee0e8afa6) | The recording ends during checking. A native capture gap is likely but unproven. |
| [Flow case 10 · 2.1.40 · Successful onboarding purchase](https://us.posthog.com/project/215955/replay/01a05514-8034-7e08-823c-c0f4692727c6) | The purchase succeeded despite an 88-second capture gap. Replay cannot distinguish a native overlay from uncaptured app UI. |
| [Flow case 4 · 2.1.39 · Onboarding cancellation](https://us.posthog.com/project/215955/replay/01a05426-3863-7c12-b37f-dcaea50b5e26) | The player cancelled normally and continued puzzle play. |
| [Flow case 12 · 2.1.39 · Successful onboarding purchase](https://us.posthog.com/project/215955/replay/01a04ac1-889b-751a-adb6-ec187f7b3dd3) | The purchase succeeded, and a process restart recovered normally. |
| [Flow case 7 · 2.1.40 · Unresolved onboarding checkout](https://us.posthog.com/project/215955/replay/01a046bf-e22f-7304-a93c-9227053f52c9) | The assigned checkout occurred about 32 seconds after recording ended; its visible outcome is unknown. |
| [Flow case 8 · 2.1.39 · Unresolved onboarding checkout](https://us.posthog.com/project/215955/replay/01a03fd2-3dc2-7c85-81cd-a40abdd6932b) | The first decline was normal; the second attempt was cut off in flight. |
| [Flow case 15 · 2.1.39 · Open-versus-presented instrumentation mismatch](https://us.posthog.com/project/215955/replay/01a03caf-2226-74dc-b734-19be96967aa1) | The visible cancellation was normal, but events were duplicated three to four times. |
| [Flow case 14 · 2.1.39 · Repeated offering refresh failures](https://us.posthog.com/project/215955/replay/01a02483-49b0-778c-af7f-1e818b15073b) | The same player experienced the recurring offering failure on another day. |
| [Flow case 13 · 2.1.39 · Repeated offering refresh failures](https://us.posthog.com/project/215955/replay/01a02144-ccb7-713c-84a5-0daffc9ffdda) | Two refresh failures occurred; the player explicitly quit after the later energy failure. |

#### Long-unresolved cases

| Recording | Observed outcome |
|---|---|
| [Long-unresolved case 2 · 2.1.40 · Play vs AI Daily Limit](https://us.posthog.com/project/215955/replay/01a05a32-986b-79cb-840c-81df148a2a54) | The one-hour frame hold ended when the app returned to foreground (`app_foreground`). Inactivity or backgrounding explains the gap; an hour of foreground freeze is unproven. |
| [Long-unresolved case 1 · 2.1.40 · Onboarding](https://us.posthog.com/project/215955/replay/01a05495-f2af-77fa-932a-b879a53048de) | The 19-hour span contained only 73 active seconds, with recovery resembling a relaunch. It does not prove a foreground hang. |
| [Long-unresolved case 5 · 2.1.40 · Onboarding](https://us.posthog.com/project/215955/replay/01a05047-8f7a-7715-9121-f217c1606dba) | The recording ends 34.5 seconds into checking; the outcome remains unresolved. |
| [Long-unresolved case 3 · 2.1.39 · Onboarding](https://us.posthog.com/project/215955/replay/01a03bfd-e21d-7a4e-bc9d-3189e4c642a6) | The app entered the background (`app_background`) 47 seconds after checkout. The pending record later aged out. |
| [Long-unresolved case 4 · 2.1.39 · Onboarding](https://us.posthog.com/project/215955/replay/01a0345f-ba62-76ed-b90f-3b189659029d) | The player declined normally, entered puzzles, and kept playing. |
| [Long-unresolved case 6 · 2.1.39 · Onboarding](https://us.posthog.com/project/215955/replay/01a02373-530e-7ad4-816d-4f3646b8b3c3) | Checking cleared to “Opening puzzle…” in about 20 seconds. |

#### Additional offering-problem recordings

| Recording | Observed outcome |
|---|---|
| [Aug. 31 · 2.1.40 onboarding](https://us.posthog.com/project/215955/replay/01a05543-4696-7632-8f08-2c7eae7f7a6a) | The pending offering recovered after 4.986 seconds to localized pricing and an active CTA. |
| [Aug. 31 · 2.1.40 lesson energy](https://us.posthog.com/project/215955/replay/01a0550c-e8a1-7da3-a685-567ded95bfed) | App-owned loading remained visible for roughly 8 to 10 seconds; the player backed out before ready. |
| [Aug. 27 · 2.1.39 onboarding](https://us.posthog.com/project/215955/replay/01a042f5-56a9-7cfa-8523-bfdd0a21cc4f) | A load-plans error was visible for about five seconds; the player continued into a puzzle. |
| [Aug. 19 · 2.1.39 onboarding](https://us.posthog.com/project/215955/replay/01a01936-4242-788b-8394-7357417b030f) | An offering error was emitted during a normal exit to Learn; captured frames showed no visible failure. |
