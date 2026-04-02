---
description: "Automation QA (sims): run existing mobile automation on an already-running iOS/Android sim, then reopen plan issues with evidence."
argument-hint: "<Paste anything. Include docs/<...>.md to pin the plan doc. Slang ok: 'smoke ios', 'both sims', 'run maestro onboarding'.>"
---
# /prompts:arch-qa-autotest — $ARGUMENTS
# COMMUNICATING WITH USERNAME (IMPORTANT)

- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give a short update in natural English (bullets optional; use them only if they improve clarity).
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH / QA_WORKLOG_PATH, not in console output.

Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output should be short and high-signal (no logs); see OUTPUT FORMAT for required content.

Goal:
Run **end-to-end automation QA** against an already-running iOS Simulator and/or Android emulator/device as the smallest credible “did we actually ship it?” signal.
Then update the plan doc so it reflects reality:
- what automation passed,
- what failed (with evidence),
- and which plan phase(s) must be **reopened** because automation proved missing/incorrect work.

$ARGUMENTS is intentionally freeform (slang allowed). Infer intent:
- Platform intent: ios / android / both
- Scope intent: smoke / “fundamentals” / focused feature flows

DOC_PATH (required):
- If $ARGUMENTS includes a `docs/<...>.md` path, use it as DOC_PATH.
- Otherwise infer from the conversation.
- If ambiguous, ask the user to pick from the top 2–3 candidates (no other questions).

QA worklog doc (authoritative transcript for this run):
- If DOC_PATH is known: create/use `docs/<DOC_BASENAME>_QA_WORKLOG.md` (same folder as DOC_PATH).
- Keep this worklog readable and append-only; store commands + logs + screenshots refs there.

Question policy (strict: no dumb questions):
- You MUST answer anything discoverable from code/tests/fixtures/logs or by running repo tooling; do not ask me.
- Allowed questions only:
  - Product/UX decisions not encoded in repo/docs
  - External constraints not in repo/docs (policies, launch dates, KPIs, access)
  - Doc-path ambiguity (top 2-3 candidates)
  - Missing access/permissions

Autonomy policy:
- Do NOT stop to “check in” mid-run. Run end-to-end until COMPLETE / BLOCKED / TIMEBOXED.
- Only print a console summary when you are about to STOP.

Device + environment rules (shared machine; avoid collateral damage):
- Prefer the `sim` CLI (mobile-sim skill) over raw `xcrun simctl` / `adb` for status/boot/servers/logs.
- DO NOT create new simulators/AVDs/devices. Use what already exists; boot an existing device only if needed.
- Assume another agent may be using a simulator/emulator. If anything feels “weird”, assume contention first.
- Do not kill/reset anything unless it is the smallest unblock step and you can justify it with evidence.

If you must fall back to platform tools (only when `sim` is insufficient):
- iOS: `xcrun simctl ...`
- Android: `adb ...` and emulator tooling

What to run (harness selection):
1) If DOC_PATH explicitly names an automation harness or command, use that as the primary signal.
2) Otherwise, discover the repo’s canonical automation entrypoint:
   - Prefer Make targets / scripts / documented commands.
   - Prefer a baseline smoke suite if it exists (fast, high-signal).
3) If $ARGUMENTS is focused (“onboarding”, “auth”, “play tab”), run the smallest set of flows that covers the happy path end-to-end.

Process (systematic; minimal bureaucracy):
1) Ground from DOC_PATH:
   - North Star, UX scope, definition-of-done signals, and the current phase state.
   - Identify the smallest automation signal(s) that validate the plan’s highest-risk surfaces.
2) Choose target platform(s) from $ARGUMENTS:
   - If $ARGUMENTS mentions android/emulator → Android only
   - If $ARGUMENTS mentions ios/simulator/iphone → iOS only
   - If $ARGUMENTS mentions both → both (iOS then Android)
   - Otherwise default to both (iOS then Android)
3) Acquire a usable device without disrupting others:
   - Start with `sim status --json` to see what is booted/connected.
   - If multiple devices are available, prefer the one least likely to be “in use”.
   - If behavior is strange (timeouts, app not responding, installs flaking):
     - Run minimal contention triage:
       - `sim servers status` (what metros/backends are up + where)
       - `sim servers tmux status` (what this repo started)
       - Lightweight process scan (ps/lsof), or use terminal-context skill if available
     - If you can’t be confident you “own” the sim: switch to a different already-booted device; otherwise STOP and report the smallest unblock step.
4) Run the automation end-to-end:
   - Prefer the smallest smoke first, then expand only if needed.
   - Record each run in the QA worklog (command, result, what it proves).
5) When something fails, classify and respond:
   - Product bug/regression (in-scope): capture repro + evidence; reopen the smallest relevant phase in DOC_PATH.
   - Harness flake / automation drift: note it; only fix if it’s a small, high-confidence harness fix that restores signal (avoid scope creep).
   - Environment/sim contention: treat as shared-machine issue; switch devices or STOP with the smallest unblock step.
6) Update DOC_PATH (required):
   - Insert/update an “Automation QA” block with pass/fail summary + evidence anchors.
   - Reopen phases in-place only when automation proves missing/incorrect work (not because “we didn’t record a screenshot”).

DOC UPDATE RULES (anti-fragile; do NOT assume section numbers):
A) Insert/replace an automation QA block in DOC_PATH:
Placement rule (in order):
1) If `<!-- arch_skill:block:automation_qa:start -->` exists: replace inside it.
2) Else insert near the end of the doc:
   - Prefer inserting before the Decision Log (if present),
   - otherwise append.

<!-- arch_skill:block:automation_qa:start -->
## Automation QA (sims/emulators)
Date: <YYYY-MM-DD>
Result: <PASS|FAIL|PARTIAL>
Platforms: <ios|android|both>
Devices used: <brief, human-readable>
Harness: <maestro|detox|flutter integration|custom> — `<primary command>`
QA worklog: `<path>`

### What we validated (highest signal)
- <behavior> — <why it matters to the North Star>

### Failures (evidence-anchored)
- <flow/test> — <what failed> — Evidence: <log/screenshot path or snippet ref in QA worklog>

### Plan impact (reopened work)
- Phase <n> (<name>) — REOPENED because: <what automation proved> — See: <QA worklog section>

### Non-blocking follow-ups
- <manual QA / extra coverage> (does not block code-complete)
<!-- arch_skill:block:automation_qa:end -->

B) Reopen phases in-place (only when justified by failures):
- Find the smallest phase section that should have delivered the failing behavior.
- Add/replace a status line directly under the phase heading:
  - `Status: REOPENED (automation found failure)`
- Add a short `Automation failures:` list with evidence anchors and the minimal fix expectation.

OUTPUT FORMAT (console only; USERNAME-style):
Only print this when STOPPING (complete/blocked/timeboxed) or when a real product decision is required.

This is the information it should contain but you should communicate it naturally in english not as a bulleted list that is hard to parse for the user.
Include:
- North Star reminder (1 line)
- Punchline (1 line; pass/fail + what’s blocking)
- What you ran (platform(s) + harness + scope)
- Result (per platform)
- What got reopened in the plan (if anything)
- Next (only if blocked/timeboxed: decision needed or smallest unblock step)
- Pointers: DOC_PATH=<path>, QA worklog=<path>
