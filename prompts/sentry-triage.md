---
description: "Sentry triage: list, analyze, and rank the top ongoing client + server problems by user experience impact."
argument-hint: "<Optional: org, client projects, server projects, envs, release/version to focus on, time window, topN, key journeys, categorization schema. If no release is provided, default to last 2 days.>"
---
# /prompts:sentry-triage — $ARGUMENTS
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list.
Inputs: $ARGUMENTS is freeform steering. Parse it intelligently.

Primary objective:
- Use Sentry MCP tools to list, analyze, and evaluate the **top ongoing problems** affecting **client** and **server**.
- Always view issues through the lens of **user experience (UX)**. A WARN may outrank an ERROR if UX harm is higher.

Question policy (strict; stop early when needed):
- If you are missing any *essential* input to run accurate queries (org slug, projects, environment, scope), STOP and ask the smallest set of clarifying questions (max 6).
- If something is ambiguous but not essential, proceed with a sensible default and include the ambiguity in “Questions for Dev”.
- After getting answers, resume exactly where you stopped.

## 0) Essential inputs gate (do this first)
If $ARGUMENTS does not clearly include all of the following, STOP and ask for them:
- `organizationSlug`
- `clientProjectSlugsOrIds` (one or more)
- `serverProjectSlugsOrIds` (one or more)

Defaults (only if not specified):
- `environments`: ["production"]
- `topN`: 10 overall + 5 client + 5 server (but do not duplicate the same issue across lists)

## 1) Scope rule (release vs last 2 days)
You MUST “look for a version to focus on”:
- If $ARGUMENTS includes a release/version (e.g. `release=...`, `version=...`, or a clearly named release string), use it as `releaseVersionFocus`.
- If no release/version is provided:
  - Restrict all issue analysis to **the last 2 days**.
  - Still try to identify which releases dominate the top issues (via release tag distributions on the top issues), and ask Dev if they want to focus on a specific release next.
  - Optional (fast): call `find_releases` per project to surface the most recent releases (helps if release tags are missing on events).

Time window defaults:
- If `releaseVersionFocus` is provided and no explicit time window is provided: use last **7 days** (and call out the assumption).
- If `releaseVersionFocus` is NOT provided: time window MUST be last **2 days**.

## 2) Categorization (required)
For each issue, assign:
- `Surface`: Client | Server | Shared
- `Priority`: P0 | P1 | P2 | P3 | P4 (definitions below)
- `UX Impact Type` (pick 1): Crash/Hang/Blocked | Data loss/corruption | Severe disruption | Buggy/janky UX | Minor annoyance | Tracking noise | Unknown
- `User Journey` (best-effort; ask if unclear): Onboarding | Login/Auth | Core browsing/usage | Create/Publish | Payments | Settings | Notifications | Background/Sync | Unknown

### Priority definitions (use these exactly)
- **P0**: Crash, app hang/ANR, or user is prevented from continuing a core flow.
- **P1**: Serious disruption to UX and/or a data problem (lost data, corrupted state, irreversible incorrectness).
- **P2**: Negative UX users typically move on from, but it feels buggy; **no significant loss of state**.
- **P3**: Hardly noticeable bug; limited disruption.
- **P4**: Harmless; primarily nuisance/noise for error tracking (unnecessary alerts, benign exceptions, non-actionable spam).

Important:
- Do not map Sentry level (error/warn/info) directly to priority. Use UX harm.
- If the issue is clearly not user-facing and not actionable, it is likely P4.

## 3) How to gather issues (efficient; focus on impact)
You will run **separate** passes for client and server, then merge and rank globally.

For each project in client + server:
1) Pull candidate ongoing issues (unresolved) within scope:
   - Use `search_issues(organizationSlug=..., naturalLanguageQuery=...)`.
   - Query should bias toward: most users impacted, most events, most recent, and production env (unless Dev specifies otherwise).
   - Example query shape (adapt as needed):
     - “Top unresolved issues affecting the most users in production in the last 2 days”
     - If `releaseVersionFocus` set: “Top unresolved issues affecting the most users in production for release <release> in the last 7 days”
2) Pull candidate issues that are **resolved** within scope:
   - Use `search_issues` again, but include resolved issues in the query.

Then:
- Deduplicate issues across projects/surfaces.
- Shortlist: topN overall plus top 5 client and top 5 server (unless overlap already covers them).

## 4) Enrich top issues (context + quantities)
For each shortlisted issue:
- Use `get_issue_details(...)` to extract:
  - title/message, issue id/url, status (unresolved/resolved/ignored), level/type, firstSeen/lastSeen
  - **# events** and **# users impacted** (use whatever Sentry provides; if not time-scoped, say so)
- Use `get_issue_tag_values` *selectively* when it changes UX interpretation or helps isolate a regression:
  - Recommended tagKeys: `release`, `environment`, `url`, `transaction`, `browser.name`, `os`, `device`
- If a top issue looks like P0/P1 and needs deeper root-cause help, run `analyze_issue_with_seer(...)` (limit ~3–5 issues).

Optional (only if needed for UX understanding):
- Use `search_issue_events` (small limit) to sample recent events and infer “what the user experiences”.

## 5) Ranking rubric (order by UX impact, then scale)
Rank issues primarily by user harm:
1) P0 > P1 > P2 > P3 > P4
2) Within same priority:
   - More users impacted > more events
   - Still happening now (recent lastSeen) > older
   - Concentrated in a new release/environment/device/journey (possible regression) gets bumped up

If key UX details are unknown, say so and ask a targeted question rather than guessing.

## 6) Output format (EVERY response must follow this structure)
### 1) North Star (1 sentence)
State the guiding principle for this report.

### 2) Punchline (max 5 bullets)
Most important takeaways, ordered by UX impact.

### 3) Questions for Dev (max 8 bullets)
Only questions that would change prioritization, scope, or next actions (release focus, key journeys, known incidents, what “core flow” means, etc.).

### 4) Summary of analysis (concise)
1 short paragraph or up to 5 bullets summarizing what you found at a high level (no deep lists here).

### 5) What I analyzed (concise)
- Scope: `releaseVersionFocus` OR explicit “last 2 days”
- Environments
- Client projects + Server projects
- Tooling: which Sentry tools were used (high level)

### 6) Ranked issues (ordered by UX impact)
Provide a table or numbered list. For each issue include:
- Rank, Priority (P0–P4), Surface, UX Impact Type, User Journey
- Issue title + status (explicitly note **resolved** issues)
- Quantities: **#users impacted**, **#events** (within scope when possible; otherwise state limitation)
- “What the user experiences” (1 sentence)
- “Engineer summary” (1–2 sentences)
- Key evidence (release/env concentration, top url/transaction, spike/regression note)

### 7) Resolved issues callout (required)
If any shortlisted issues are marked resolved, list them explicitly and note whether they still show new events in-scope (if you can tell).

### 8) Optional: Out-of-the-box ideas (clearly labeled optional)
1–2 creative ideas/questions to accelerate understanding or prevention (optional, not required).

