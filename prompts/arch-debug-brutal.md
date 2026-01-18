---
description: "15a) Brutal debug: prove root cause fast (temporary hacks allowed)."
argument-hint: "<Paste symptoms/logs/repro. Optional: include a docs/<...>.md path to write the diagnosis doc.>"
---
# /prompts:arch-debug-brutal — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.

Goal: minimize WALL-CLOCK TIME to prove the root cause with high certainty.
This is a DEV diagnosis workflow. Code is NOT precious here:
- You MAY make temporary "brutal cut" changes (comment out layers, force returns, clamp values, hard-code sizes, bypass caches, etc.).
- You SHOULD prefer the fastest discriminating experiments over elegant solutions.
- We will delete/revert the temporary code later; do not waste time building permanent gates or frameworks.
- Avoid adding dev gates/flags/config surfaces (e.g., `__DEV__`, feature flags, env vars) unless absolutely required. Prefer direct edits + quick reverts.

Question policy (extreme):
- Do NOT ask the user technical questions you can answer by reading code/logs or running a repro; go look and decide.
- Ask the user only if a REQUIRED external fact is missing and cannot be inferred (e.g., “which exact screen/flow triggers it” if no repro exists in repo).
- Never ask “what do you want to do?” about technical approaches. Pick the fastest/most informative one.

Doc policy (diagnosis log):
1) If $ARGUMENTS includes a docs/<...>.md path, use it as DIAG_PATH (write findings there).
2) Otherwise create a new doc in docs/:
   - `docs/DIAG_<TITLE_SCREAMING_SNAKE>_<DATE>.md`
   - TITLE_SCREAMING_SNAKE = derived from the symptom report as a short 5–9 word title.
   - DATE = today's date in YYYY-MM-DD.
This doc is a scratchpad for brutal efficiency. It does NOT need to match the full architecture template.

Stop conditions:
- Stop as soon as the root cause is proven with evidence anchors.
- If you cannot reach certainty quickly, stop with the single smallest next experiment that will settle it.

Process (optimize for binary isolation):
1) Parse $ARGUMENTS into: expected vs actual, repro steps (if any), scope notes (what is NOT affected), and any evidence already present (logs, screenshots).
2) Build a short hypothesis list (max 6). Each hypothesis must be falsifiable and must name a likely earliest failure site.
3) Design a brutal test plan that maximizes information per minute:
   - Start coarse (disable entire suspect subtrees/layers/providers) before going fine-grained.
   - When the render tree is complex, do a literal binary search: cut ~50% of the suspect subtree, repro, then cut again based on results.
   - One change at a time; run the fastest repro; record outcome; revert; repeat.
   - Prefer “hard cut” tests like:
     - Temporarily disable a render layer / overlay / provider / effect scene.
     - Render a neon full-rect sentinel (proves stacking/opacity/culling quickly).
     - Clamp suspect opacities/alphas to 1 (or 0) to isolate alpha accumulation.
     - Replace `SkiaOpacity(requiresLayer)` with a plain Group to eliminate saveLayer behavior.
     - Short-circuit an entire component subtree: `return null`.
     - Freeze state updates (force a constant snapshot) to rule out state churn.
     - Force a single mount (assert only one provider/scene exists).
4) Instrumentation rules (fast, disposable):
   - Add logs at the earliest failure site (and 1–2 key boundaries) only if needed to prove causality.
   - Avoid hot-loop logs unless absolutely necessary.
   - You MAY keep logs/instrumentation in place until the issue is fixed; do not prematurely clean up.
5) Track “files modified” continuously so we can revert quickly.

Write/update the diagnosis doc at DIAG_PATH as you go (do not wait until the end).
Use this structure (adapt as needed; do not be verbose):

# <Title> (Diagnosis)
Date: <YYYY-MM-DD>

## Problem statement
- <1–3 bullets: expected vs actual>

## Scope
- In scope:
- Out of scope:

## Evidence
- <logs/traces/observations already known>

## Theories and tests
### T1 — <hypothesis>
Why plausible:
Test (brutal cut):
Result:
Status: <ruled out | likely | proven>

## Brutal tests (fast binary isolation)
### B1 — <hard cut>
Goal:
Change:
Expected:
Observed:
Conclusion:

## Root cause (proven)
- <one sentence>
- Evidence anchors:
  - <path:line> — <why it proves it>

## Fix shape (proposal, not implementation)
- <minimal fix that removes the cause>
- Cleanup to do after fix:
  - remove diagnostics / revert temporary cuts

OUTPUT FORMAT (console only):
Summary:
- Diag doc: <path>
- Root cause: <proven | not yet proven>
- Confidence: <low|medium|high|certain>
- Experiments run:
  - <B*/T*> — <result>
- Files modified:
  - <path>
Next:
- <single most informative next experiment OR "ready to implement fix"> (yes/no)
