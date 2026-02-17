---
description: "Sentry triage: list, analyze, and rank the top ongoing client + server problems by user experience impact."
argument-hint: "<Optional: envs, release/version to focus on, time window, topN, optional serverIssueFilter (e.g. service:backend), key journeys, categorization schema. Defaults: org=funcountry; project=psmobile-production (or psmobile-staging when env includes staging); if no release is provided, default to last 2 days.>"
---
# /prompts:sentry-triage — $ARGUMENTS
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list.
Inputs: $ARGUMENTS is freeform steering. Parse it intelligently.

Primary objective:
- Use Sentry MCP tools to list, analyze, and evaluate the **top ongoing problems** affecting **client** and **server**.
- Always view issues through the lens of **user experience (UX)**. A WARN may outrank an ERROR if UX harm is higher.

Question policy (default to action):
- Do not block on missing scope details. Start with defaults and run triage immediately.
- Ask follow-up questions only when absolutely essential to proceed (for example: org/project access fails or tools return no reachable scope). Max 3 concise questions.
- If something is ambiguous but not essential, proceed with defaults and capture the ambiguity in “Questions for Dev”.

## Default scope (auto-fill unless overridden)
- `organizationSlug`: `funcountry`
- `environments`: ["production"]
- `clientProjectSlugsOrIds`:
  - If environment is production (default): ["psmobile-production"]
  - If environment includes staging: ["psmobile-staging"]
  - If both production and staging are requested: query both projects
- `serverProjectSlugsOrIds`: not required; ignore unless explicitly provided in $ARGUMENTS
- `topN`: 10 overall + 5 client + 5 server (but do not duplicate the same issue across lists)
- `serverIssueFilter`: optional optimization only (never a gate)

## Scope (release vs last 2 days)
You MUST “look for a version to focus on”:
- If $ARGUMENTS includes a release/version (e.g. `release=...`, `version=...`, or a clearly named release string), use it as `releaseVersionFocus`.
- If no release/version is provided:
  - Restrict all issue analysis to **the last 2 days**.
  - Still try to identify which releases dominate the top issues (via release tag distributions on the top issues), and ask Dev if they want to focus on a specific release next.
  - Optional (fast): call `find_releases` per project to surface the most recent releases (helps if release tags are missing on events).

Time window defaults:
- If `releaseVersionFocus` is provided and no explicit time window is provided: use last **7 days** (and call out the assumption).
- If `releaseVersionFocus` is NOT provided: time window MUST be last **2 days**.

## Categorization (required)
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

## Gathering issues (efficient; impact-first)
You will run **separate** client and server passes, then merge and rank globally.

Project scope selection:
- Use `clientProjectSlugsOrIds` from defaults/overrides.
- If explicit `serverProjectSlugsOrIds` are provided, include them for the server pass.
- If no explicit server projects are provided, run server pass against the same project pool and classify by issue evidence (service tags, stack traces, logger names, transactions, URLs, SDK/platform context).

For each project in the selected pool:
- Pull candidate ongoing issues (unresolved) within scope:
  - Use `search_issues(organizationSlug=..., naturalLanguageQuery=...)`.
  - Query should bias toward: most users impacted, most events, most recent, and production env (unless Dev specifies otherwise).
  - For server pass, if `serverIssueFilter` is provided include it (e.g., append `service:backend`); otherwise infer backend/server issues from issue content and tags. Do not stop if the filter is missing.
  - Example query shape (adapt as needed):
    - “Top unresolved issues affecting the most users in production in the last 2 days”
    - If `releaseVersionFocus` set: “Top unresolved issues affecting the most users in production for release <release> in the last 7 days”
- Pull candidate issues that are **resolved** within scope:
  - Use `search_issues` again, but include resolved issues in the query.

Then:
- Deduplicate issues across projects/surfaces.
- Shortlist: topN overall plus top 5 client and top 5 server (unless overlap already covers them).

## Enrich top issues (context + quantities)
For each shortlisted issue:
- Use `get_issue_details(...)` to extract:
  - title/message, issue id/url, status (unresolved/resolved/ignored), level/type, firstSeen/lastSeen
  - **# events** and **# users impacted** (use whatever Sentry provides; if not time-scoped, say so)
- Add a **version status hint** for each issue:
  - If `releaseVersionFocus` is set: use that version.
  - Otherwise: use the **latest release** for the issue’s project (use `find_releases` once per project; cache the latest version).
  - Then, for the chosen version, check whether the issue is still happening:
    - Use `search_issue_events(..., naturalLanguageQuery=...)` with `release:<version>` + environment + the same time window; `limit=1`.
    - If events exist: `Version hint = "Unresolved in <version> (still firing in scope)"`.
    - If no events: `Version hint = "Likely resolved in <version> (not observed in scope)"`.
    - If release filtering is impossible (missing release tag): `Version hint = "Unknown (no release tag)"`.
- Use `get_issue_tag_values` *selectively* when it changes UX interpretation or helps isolate a regression:
  - Recommended tagKeys: `release`, `environment`, `url`, `transaction`, `browser.name`, `os`, `device`
- If a top issue looks like P0/P1 and needs deeper root-cause help, run `analyze_issue_with_seer(...)` (limit ~3–5 issues).

Optional (only if needed for UX understanding):
- Use `search_issue_events` (small limit) to sample recent events and infer “what the user experiences”.

## Ranking rubric (UX first, then scale)
Rank issues primarily by user harm:
- Priority order: P0 > P1 > P2 > P3 > P4
- Within the same priority:
  - More users impacted > more events
  - Still happening now (recent lastSeen) > older
  - If Sentry status is “resolved” but the issue is still **unresolved in the focus/latest version** (per version hint), bump it up (likely regression or premature resolve).
  - Concentrated in a new release/environment/device/journey (possible regression) gets bumped up

If key UX details are unknown, say so and ask a targeted question rather than guessing.

## Response format (senior-dev-friendly; no pointless numbering)
Use this structure in EVERY response. Do not number headings. Only number the ranked issues (the rank is the point).

### North Star (1 sentence)
State the guiding principle for this report.

### Punchline (max 5 bullets)
The 2–5 most important takeaways, ordered by UX impact.

### Questions for Dev (max 8 bullets)
Only questions that would materially change prioritization, scope, or next actions.

### Scope & method (concise)
- Release focus: `releaseVersionFocus` OR “none”
- Time window: explicit (e.g. “last 2 days”)
- Environments
- Client project scope + server pass strategy (explicit server projects vs in-project classification)
- Tools used (high level)
- Caveats (release tagging missing, counts not time-scoped, etc.)

### Ranked issues (ordered by UX impact)
Prefer a table when it stays readable; otherwise use a numbered list.

For each issue include:
- Rank, Priority (P0–P4), Surface, UX Impact Type, User Journey
- Issue title + Sentry status (explicitly note **resolved** issues)
- Version hint (required): **resolved/unresolved in the specified (or latest) version** (label as a hint)
- Quantities: **#users impacted**, **#events** (within scope when possible; otherwise state limitation)
- “What the user experiences” (1 sentence)
- “Engineer summary” (1–2 sentences)
- Key evidence (release/env concentration, top url/transaction, spike/regression note)

### Resolved & regression watch (required)
Explicitly list:
- Issues marked resolved that are still firing (per version hint)
- Issues marked resolved that appear not to be firing anymore (per version hint)

### Optional: Out-of-the-box ideas (clearly labeled optional)
1–2 creative ideas/questions to accelerate understanding or prevention.

### Response template (copy/paste and fill in)
Use this exact skeleton:
```md
### North Star
<one sentence>

### Punchline
- <most important finding>
- <next most important finding>

### Questions for Dev
- <question that changes prioritization/scope>

### Scope & method
- Release focus: <value or "none">
- Time window: <explicit>
- Environments: <...>
- Client projects: <...>
- Server pass: <explicit server projects OR in-project classification>
- Tools used: <search_issues, get_issue_details, ...>
- Caveats: <1–3 bullets>

### Ranked issues
| Rank | Pri | Surface | Version hint (hint) | Sentry status | Issue | Users | Events | UX (what user sees) | Engineer summary | Evidence |
| ---: | :--: | :-----: | :------------------ | :------------ | :---- | ----: | -----: | :------------------ | :-------------- | :------- |
| 1 | P0 | Client | Unresolved in <v> | unresolved | <title / link / id> | <#> | <#> | <1 sentence> | <1–2 sentences> | <tags/urls/releases> |

### Resolved & regression watch
- <resolved-in-sentry but still firing>
- <resolved-in-sentry and not firing>

### Optional: Out-of-the-box
- <optional idea>
```
