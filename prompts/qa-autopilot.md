---
description: "QA autopilot: run existing QA automation, fix broken flows idiomatically, and document results (plan-aware)."
argument-hint: "<Paste anything. Include docs/<...>.md to pin the plan doc (optional).>"
---
# /prompts:qa-autopilot — $ARGUMENTS
Execution rule: ignore unrelated dirty git files; if committing, stage only what you touched.
Do not preface with a plan. Begin work immediately.

Goal:
Use QA automation to prove the fundamentals first, then expand coverage. Stay fast and systematic.
If QA automation is broken or missing coverage, fix it in an architecturally elegant / idiomatic / unified way that prevents drift, then rerun and record results.

Context:
$ARGUMENTS is freeform steering. Treat it as intent + constraints + any relevant context from the session.

DOC_PATH (optional plan doc):
- If $ARGUMENTS includes a docs/<...>.md path, use it as DOC_PATH.
- Otherwise infer from the conversation.
- If no plan doc exists, proceed plan-less (this prompt still runs).

QA worklog doc (authoritative for this run):
- If DOC_PATH is known: create/use `docs/<DOC_BASENAME>_QA_WORKLOG.md`.
- Otherwise create a new doc in `docs/`:
  - `docs/QA_AUTOPILOT_<TITLE_SCREAMING_SNAKE>_<DATE>.md`
  - TITLE_SCREAMING_SNAKE = derived from $ARGUMENTS in 5–9 words.
  - DATE = today's date in YYYY-MM-DD.

Question policy (strict: no dumb questions):
- Do NOT ask technical questions you can answer by reading code, tests, existing QA flows, or running commands. Go look and decide.
- Ask only if you hit a real product-level decision that blocks correctness (UX expectation, behavior spec conflict, etc.).
- If you must ask, STOP and report with full context: repro, what failed, and the concrete decision needed.

Operating principles:
- Start with fundamentals: the smallest, highest-signal smoke tests first.
- Prefer existing QA harnesses. Do not invent new frameworks if one already exists.
- If multiple harnesses exist, choose the fastest/most reliable one to validate the North Star / core UX surfaces.
- QA fixes must be unified + drift-proof:
  - Prefer reusable subflows/helpers over copy/paste tests.
  - Centralize selectors/ids/helpers where the project’s idioms suggest.
  - Avoid parallel ways to test the same thing.

Stop conditions:
- If you discover a product-level issue that requires a decision: STOP and report (no guessing).
- If QA is impossible due to infra/environment issues: STOP and report the single smallest unblock step.

Unblock policy (default: fix it, don’t ask):
- Do NOT get stuck on obvious compile/build/test failures. Treat them as part of the work.
- If a run fails due to compilation, typecheck, lint-as-error, missing imports, etc.:
  - Note it in the QA worklog doc (briefly).
  - Fix it immediately (small, local, high-confidence fix).
  - Re-run the smallest relevant QA signal.
- Only stop for “infra/environment” when you truly cannot unblock from repo code (e.g., missing SDKs/credentials/CI-only resources). Even then, propose the single smallest unblock step.
- “Obvious bug” rule: if you can clearly see the bug and the fix is small + high-confidence, note it and fix it (don’t debate it).

Environment preflight (fast; do early; don't repeat needlessly):
- If this is the first time you’re running QA in this repo/session (or you’re unsure), do a quick preflight BEFORE running tests:
  - Ensure the app is built from the latest code and installed on the target simulator/emulator/device.
  - Ensure the app can actually launch and reach any required dev servers/backends.
  - Check that required servers are up (packager/dev server, backend, mocks). Prefer a health check / curl / open-port check over guesswork.
- If you already verified preflight earlier in the same session and nothing changed, skip re-doing it—just note “preflight already verified”.

Process (systematic):
1) Grounding:
   - If DOC_PATH exists, read it and extract: North Star, UX in-scope/out-of-scope, any acceptance evidence expectations, and any known risky surfaces.
   - Determine the minimal “fundamental behaviors” to validate first (core flows, not edge cases).
2) Preflight (only if needed):
   - Verify app + server readiness using the “Environment preflight” rules above.
   - Record what you checked in the QA worklog doc (briefly).
3) Choose QA harness:
   - Detect existing automation tooling in the repo (e.g., existing e2e folders, scripts, CI targets).
   - Prefer the canonical entrypoint (Makefile target / package.json script / documented command).
4) Smoke first:
   - Run the smallest, fastest smoke(s) that validate the fundamental behaviors.
   - Record command + result in the QA worklog doc.
5) Expand coverage:
   - Add or run the next most fundamental tests (still high-signal).
6) If automation is broken / missing coverage:
   - Create/extend a section in the QA worklog doc:
     - "Automation Gaps (blocking)" — what’s broken and why it blocks signal
     - "Unified Fix (idiomatic)" — the single clean way to solve it without drift
   - Implement the fix (tests/flows/helpers) using existing repo idioms.
   - Re-run the smallest relevant test and record the new result.
7) If a failure is a real product bug (not test flake):
   - Create a "Product Bugs Found" section with crisp repro steps + evidence.
   - If the fix requires a product decision, STOP and ask (with context).
   - If it does NOT require a product decision, you may fix it if it is clearly in-scope of the plan (otherwise record and stop).
8) If a failure is a build/compile/test-harness failure:
   - Follow “Unblock policy” above: note → fix → re-run smallest signal.
   - Prefer the smallest fix that restores the canonical QA entrypoint and avoids drift.

QA WORKLOG FORMAT (write to the QA worklog doc; keep it readable; no ASCII tables):
# QA Autopilot Worklog
Date: <YYYY-MM-DD>
Repo: <path>
Plan doc: <DOC_PATH or "none">

## Scope
- Fundamental behaviors under test:
  - <bullet>
- Out of scope (explicit):
  - <bullet>

## Preflight (environment readiness)
- App build/install:
  - <how you ensured latest build + installed>
- App launch sanity:
  - <does it start? any immediate crash?>
- Required servers:
  - <what you checked + how (health check / curl / port)>
- Notes:
  - <only if needed>

## Harness selection
- Chosen harness: <name>
- Why this one:
  - <bullet>
- How to run:
  - `<command>`

## Runs (append-only)
### Run 1 — <smoke name>
- Command:
  - `<command>`
- Result:
  - <pass/fail + key output>
- What this proves:
  - <bullet>

## Automation gaps (blocking)
- <gap> — impact — proposed unified fix

## Unified fixes implemented (anti-drift)
- <fix>
  - Files changed:
    - `<path>`
  - Why this is the idiomatic/unified approach:
    - <bullet>
  - Re-run signal:
    - `<command>` — <result>

## Product bugs found (if any)
- <bug title>
  - Repro:
    - <steps>
  - Evidence:
    - <logs/screenshots/etc>
  - Needs product decision? <yes/no>

## Current status
- Confidence: <low|medium|high|certain>
- What is still unverified:
  - <bullet>

CONSOLE OUTPUT FORMAT (friendly + human readable; no giant dumps):
Summary:
- QA worklog: <path>
- Harness: <chosen>
- Runs:
  - <name> — <pass/fail>
- Fixes landed:
  - <bullet>
- Product issues:
  - <none|bullet list>
Status:
- <complete|blocked>
Next:
- <single next most fundamental test to run OR decision needed>
