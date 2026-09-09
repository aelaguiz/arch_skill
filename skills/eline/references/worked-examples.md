# ELINE Worked Examples

Use these to calibrate the floor and the ladder. They teach the shape; they are
not templates to copy. The layer labels (L0 to L3) are shown here for
teaching; the reader never sees them.

## One Incident, Three Ways

The incident: a mobile app's session-token refresh path stalls for minutes
under a slow auth provider, every token-dependent screen reports "timeout",
and an alarm fires. The facts are the same in all three versions. Only the
rendering changes.

The ask: "explain what is going wrong with token refresh and what the fix
is." Because the ask names the fix, L3 is included for the changed settings.
A pure "what is going wrong" ask would omit it.

### Version A: Cast and metaphor (floor too low)

```text
The cast
- Clerk: the outside company that runs our login. Their servers hand out a
  session token, a short-lived pass the app must attach to every request to
  prove "this user is signed in."
- Clerk's client library (what I was calling "the fork"): think of it as the
  errand-runner. It knows how to go ask Clerk for a token.
- Our token manager (what I was calling "the gateway"): our own code that sits
  between the app and the errand-runner.
- "Minting": just "asking Clerk for a fresh token."

What happens today (the story)
1. A screen needs a token. The manager sends the errand-runner to Clerk and
   says: "I'll wait 8 seconds."
2. But the errand-runner has its own instructions, written by Clerk, that the
   manager never reads...
```

Why it fails for an engineer: it defines "token", it replaces the SDK and the
wrapper with characters the reader must translate back into the mechanism
they already have words for, and it hides the real names behind "what I was
calling". The reader spends effort decoding the story instead of placing the
components.

### Version B: Repo soup (floor too high)

```text
ClerkAuthGateway wraps the fork in packages/clerk_auth_0_0_14_hotfix with an
8s timeout; the fork's request loop applies retryOptions (8 attempts, 10s per
attempt) and sleeps Retry-After on 429 inside the send path. The gateway's
backoff ladder (500ms..30s) re-enters while the prior send is unresolved,
producing concurrent token POSTs and 429s; the 5-minute alarm 1AQ fires with
reason=timeout and 1EJ aggregates the per-caller token failures.
```

Why it fails: every fact is true, but the reader learns there are two timeout
policies only by reverse-engineering the architecture from identifiers. The
setup and the nuance are in the same paragraph, so nothing can be skipped.

### Version C: ELINE

L0, thesis:

```text
Token refresh runs two competing timeout-and-retry policies: our gateway wraps
Clerk's SDK with an 8-second timeout and its own backoff ladder, the SDK
applies its own 10-second-per-attempt, 8-retry policy underneath, and the
gateway cannot cancel the SDK. Under a slow Clerk that produces overlapping
requests, 429s, and a self-sustaining loop that every token-dependent screen
sees as "timeout". The fix is one clock and one retry policy, both in the
gateway.
```

L1, setup:

```text
Auth is Clerk, a third-party identity provider. Their session token is a
~60-second JWT the app attaches to every backend call, so the app refreshes it
constantly. Two pieces of ours are on the path: a vendored fork of Clerk's
Dart SDK, which is the HTTP client to Clerk, and `ClerkAuthGateway`, our
wrapper that caches the current token, decides when to refresh, and handles
failure. Every screen that needs a token goes through the gateway.
```

L2, problem area:

```text
The gateway calls the SDK with an 8-second timeout and, on failure, retries on
its own ladder (0.5s, 1s, 2s, 4s, up to 30s). The SDK independently applies 10
seconds per attempt, up to 8 retries, and on a 429 sleeps for Retry-After
(about 30s) before retrying. Nothing cancels the SDK when the gateway's 8
seconds expire.

So under a slow Clerk: the gateway times out at 8s and fails every waiting
caller; half a second later it starts a second SDK request while the first is
still retrying; concurrent requests hit a slow endpoint; Clerk starts returning
429; each subsequent 8-second window fails again. The loop feeds itself.

There is also a plain arithmetic bug: the gateway's 8-second budget is below
the SDK's 10-second single attempt, so a merely slow Clerk can never succeed
at all.

Evidence: the 5-minute alarm fired with reason "timeout" in 14 of 14 sampled
events and never "offline" or "DNS", which means our clock expired, not the
network. The per-screen failures are the separate Sentry issue that piles up
during the same windows. Confirmed from the SDK and gateway code plus
telemetry. The 429 rate during an episode is inferred, not measured.
```

L3, included because the ask named the fix (only the changed settings):

```text
Three changes. The SDK's `retryOptions` drops to a single attempt, so the
gateway's ladder is the only retry policy. The gateway timeout goes from 8s to
12s so one full SDK attempt fits inside it. The SDK's 429 handling returns
`rate_limited` plus the Retry-After value instead of sleeping, and the gateway
honors the wait and labels the failure.
```

Dig handles:

```text
Ask about:
- the 429 change, which is the one part that touches the fork's code
- whether the startup sign-in path wraps the same SDK with the same two clocks
- what this does not fix: Clerk fully unreachable for minutes, and the ~4% of
  errors where two parts of the app disagree about sign-in state
- what would prove the fix: the doc has a stalled-server test pattern and two
  alarm tags that split "timeout" from "rate limited"
```

Why it works: the reader can stop after L0 and repeat the thesis correctly,
stop after L1 and place every component, stop after L2 and believe it, and
knows exactly what to ask for the rest. No term was defined that an engineer
already has, no identifier appeared before its role, and L3 appeared only
because the ask called for the fix.

## A Follow-Up Exchange

Reader: "Why can't the gateway just cancel the SDK request at 8 seconds?"

Descend one layer on that piece only:

```text
The fork's request loop runs inside the request future, and the fork does not
expose a cancellation handle, so the gateway's timeout abandons the future
without stopping it. Adding cancellation means changing the fork's send loop,
which is a larger change than turning retries off and still leaves two retry
policies in play. Confirmed from the fork's code. Whether upstream Clerk has
since added cancellation is not checked.
```

Weak follow-up: restarting with "So, to recap, Clerk is the third-party
identity provider..." or answering with the whole fix plan again.

## Rewrite From Repo Soup: A Feature-Flag Race

Original opening:

```text
PlayTabHostScreen's base gate reads the frozen snapshot from
navigation_flags.dart before flag_refresher.dart's deferred values write
lands, so the one-shot refreshIdentityKey correction is consumed with stale
defaults and PlayVsAiUnavailableScreen sticks until process restart.
```

ELINE rendering:

L0:

```text
The Play tab stuck on its "unavailable" screen because the tab bar spent its
single allowed flag correction on stale values: the "fetch succeeded" signal
and the fetched values are written separately, and the signal landed first.
```

L1:

```text
The Play tab is gated by a PostHog feature flag. Unknown flag state defaults
to off in staging and production. The tab bar freezes its flag snapshot at
startup so tabs do not reorder mid-session, and allows exactly one late
correction: the first successful flag fetch for the signed-in user may
replace the snapshot. A flag fetch writes two things: a status and the
values, with the values write deferred to the end of the UI frame.
```

L2:

```text
An in-session account switch resets the values to defaults and re-freezes the
snapshot with Play off. When the new account's fetch completes, the status
write fires the one-shot correction, which reads the still-default values and
consumes the correction with Play off. The values write lands 36 milliseconds
later and is ignored because the correction is spent. The tab stays off until
process restart.

Evidence, from one session's timeline: sign-out at 18:06:24, sign-in at
18:06:41, two successful fetches at 18:06:51 with PostHog serving Play on,
recovery only after the restart at 18:09:42. The flag was on at 100% with the
kill switch off for the whole window. Confirmed from logs and the flag config.
Only users who switch accounts without restarting can hit this, which is why
it was not widespread.
```

Handles, with L3 omitted because the ask was "why did this happen", not
"what exactly changed":

```text
Ask about: the code comment in the refresher that promised the ordering and
is what broke, how the correction could be keyed to the identity that
produced the values, what the tab should show while the new account's flags
are unknown, and why the unavailable screen emits no analytics event.
```

The stage-crew analogy from the original explanation is deleted. The timeline
already carries the mechanism.

## A Design Decision

Ask: "Dashboards are slow. Should we add a Postgres read replica?"

```text
No, not for this. The slow dashboards are one unindexed query, not read
load, and a replica would add replication lag to a screen that reads its own
writes.

The API server and the dashboards share one Postgres primary. Dashboards run
aggregate queries over the orders table; the "order placed" screen reads the
row it just inserted. Primary CPU sits around 30% at peak.

The query stats show one dashboard query at 92% of dashboard time, doing a
sequential scan on orders filtered by account and date. That is an index
problem: a composite index on account and created-at turns it into an index
range scan. A replica would not change that plan; it would run the same scan
on a second box. It would also introduce replication lag, so the "order
placed" screen could read a replica that does not yet have the row, unless
that path is pinned to the primary, which is a new routing rule to maintain.
Confirmed from the query stats and the plan; the CPU figure is two weeks of
metrics.

Add the index and re-measure. Revisit a replica when read CPU on the primary
actually saturates, and pin read-your-writes paths to the primary at that
point.

Ask about: which other dashboard queries share the same filter shape, and
whether the index build has to run concurrently to avoid blocking writes.
```

Why it works: the decision and its forcing constraint come first, the setup
is three sentences with no identifiers, the tradeoff carries its evidence with
confidence marked, and the recommendation says what would reopen the
question. Nothing the reader would act on needed an exact name, so there is no
L3.
