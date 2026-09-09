# ELINE Vocabulary Floor

Use this reference when you are unsure whether a term should be assumed,
glossed, or collapsed, or when a previous explanation missed the floor in
either direction.

The floor is the line between what the reader already has words for and what
only this system's engineers know. Everything above the line is used plainly.
Everything below it gets one role gloss or is collapsed.

## Assumed

Use these plainly. Do not define them, do not replace them with analogies,
and do not narrate what they do.

- Data and storage: relational versus document store, index, transaction,
  isolation level, migration, ORM, cache, TTL, eviction, write-through,
  invalidation, replication, eventual consistency, idempotency key.
- Concurrency and time: race condition, deadlock, lock, atomic, debounce,
  throttle, timeout, retry, exponential backoff, jitter, circuit breaker,
  cancellation, in-flight request, backpressure, queue, worker, cron, tick.
- Networking and APIs: HTTP verbs and status codes (401, 403, 404, 429, 5xx),
  REST, RPC, WebSocket, TLS, DNS, CDN, rate limit, Retry-After, pagination,
  webhook, long-polling, payload, header.
- Auth: session, token, JWT, refresh token, OAuth, OIDC, SSO, expiry, scope,
  identity provider, claims.
- Client and mobile: app lifecycle, foreground and background, cold start,
  deep link, push notification, offline cache, main thread, frame, render
  loop, state management, hot path.
- Delivery and ops: CI, build matrix, flaky test, feature flag, kill switch,
  canary, rollout, rollback, A/B test, p50 and p95, SLO, alert, log, trace,
  error tracking, sampling.
- Architecture words: gateway, wrapper, adapter, SDK, client library, service,
  worker, scheduler, provider, store, controller, middleware, monorepo,
  package, module, fork.

The architecture words are the ones to reach for when collapsing. "Our auth
gateway" and "the vendored SDK" are complete descriptions for this reader.

## Glossed

Anything the reader could not look up: service names, package names,
product-domain terms, team acronyms, internal codenames, house metrics, and
internal modes or tiers. Gloss once, on first use, then keep the real name.

Gloss patterns:

- Name, role, contract fact. "`ClerkAuthGateway`, our wrapper around Clerk's
  SDK; every screen that needs a token goes through it."
- Name plus category word. "PostHog, our feature-flag and analytics provider."
- Product term plus unit or role. "A hand is one full game round; it is the
  unit of every downstream count."
- Codename plus what it actually is. "The 3p lane is the local stack that runs
  three-player tables against the AI service."
- Acronym: expand once when it is team-local or has more than one common
  expansion, then use the acronym. "PvAI (play versus AI)". Industry acronyms
  the reader already has, such as JWT, CI, TTL, or p95, are assumed.

A gloss is one clause. If it needs a sentence, the term is probably on the
problem's path and belongs in L1 as a component with a role, not in a
parenthetical.

## Collapsed

Internals on the periphery of the problem. Replace the chain with the role of
the whole, and expand only if the reader digs there.

- Chain to role: "the token fetch, cache, and refresh scheduler" becomes "our
  auth gateway".
- Fan-out to count and role: "puzzles, streaks, friends, leaderboard, and Play
  vs AI" becomes "every screen that needs a token" unless the list is the
  point.
- Off-path branch to one clause: "there is a saved-session fallback that works
  and is untouched here."
- Multi-step flow to its contract: "the backend validates the token and
  returns the puzzle."

Collapse hides mechanism the reader does not need. It never hides a fact the
thesis depends on. If the collapsed thing is the cause, it is not off the
path.

## Numbers

Keep exact the numbers that carry the argument: 8 seconds versus 10 seconds,
14 of 14 sampled events, 36 milliseconds between two writes. Round or drop the
numbers that are color. "67 reports in 21 minutes from one device" stays exact
when it is the evidence for "the retry loop had no limit"; it becomes "dozens
of reports per device" when it is only setting the scene.

## The Two Failure Directions

Every draft can miss the floor in one of two ways. Check for both.

**Floor too low.** The draft explains what the reader already knows or swaps
components for characters.

```text
Clerk hands out a short-lived pass the app must show at the door. Think of the
client library as an errand-runner that goes to ask for a fresh pass.
"Minting" just means asking for a fresh token.
```

For this reader:

```text
Clerk issues ~60-second session JWTs, so the app refreshes constantly. The
vendored Clerk SDK is the HTTP client; our gateway wraps it.
```

Signals: "think of it as", a cast list, a definition of token, retry, cache,
flag, or queue, a story with characters, an analogy from outside engineering.

**Floor too high.** The draft front-loads identifiers the reader cannot place.

```text
PlayTabHostScreen's base gate reads navigation_flags.dart's frozen snapshot
before flag_refresher.dart's deferred values write lands, so the one-shot
refreshIdentityKey correction is consumed stale.
```

For this reader:

```text
The tab bar freezes its feature-flag snapshot at startup and allows one late
correction. The correction fires on the "fetch succeeded" signal, which lands
before the values do, so it consumes the correction with stale defaults.
```

Signals: a file path, class name, PR number, Sentry short ID, or unglossed
codename in the first two paragraphs; method names standing in for architecture; the
reader having to reverse-engineer the components from identifiers.

The test is two questions about a strong engineer from another company reading
L0 and L1: would they ask what a word means (too high), and would they be
annoyed that something was explained (too low)?
