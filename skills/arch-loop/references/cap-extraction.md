# `arch-loop` Cap and Cadence Extraction

## Why this file exists

Users type `arch-loop` requirements as prose. Caps and cadences are the one place where deterministic code must own meaning, because the model cannot decide that five hours have elapsed or five iterations have run.

This reference documents the first-release phrase families the controller recognizes, how ambiguity is handled, how multiple caps of the same type combine, and how the installed hook timeout bounds cadence and runtime windows.

## Three cap families

- **runtime/window cap** normalizes to `deadline_at = created_at + duration_seconds`
- **cadence** normalizes to `interval_seconds`
- **iteration cap** normalizes to `max_iterations`

Every matched phrase is preserved literally in `cap_evidence` as a `{type, source_text, normalized}` entry. The source text is what the user typed; the normalized value is what the controller enforces. Evidence is additive even when multiple phrases combine into one effective cap (for example, "max runtime 5h, stop if not done in 3h" records both source phrases and picks the strictest cap for enforcement).

## Duration/window phrase family (first release)

Supported:

- `max runtime 5h`
- `maximum runtime 3 hours`
- `time limit 90 minutes`
- `stop after 2h`
- `stop if not done in 3h`
- `stop if you're not done in 3 hours`
- `for the next 6 hours`
- `for 2 days`

Accepted units: `s`, `sec`, `second(s)`; `m`, `min`, `minute(s)`; `h`, `hr`, `hour(s)`; `d`, `day(s)`. Integer and decimal magnitudes are accepted (for example `1.5h`, `90m`). Normalization converts to integer seconds.

If the text contains a likely runtime phrase with no unambiguous number/unit ("a few hours", "a while", "by tomorrow"), the skill must ask once or stop with an invalid-cap blocker. Do not guess a default window.

Strictest-cap rule for runtime: when multiple runtime phrases produce different `deadline_at` values, pick the earliest deadline and preserve every source phrase in `cap_evidence`.

## Cadence phrase family (first release)

Supported:

- `every 30 minutes`
- `every 1 day`
- `every 10s`
- `every hour`
- `check every 15 min`

Normalization converts to integer `interval_seconds`. `every hour` normalizes to `3600`, `every 10s` to `10`, `every 1 day` to `86400`.

Cadence is **not** a strictest-cap: shorter intervals increase runtime load and the product contract does not say "the smallest interval wins." If two or more different cadence phrases are detected (for example `every 30 minutes` and `every hour`), cadence is ambiguous. The skill must ask once or stop with an invalid-cap blocker. Do not silently pick one.

If a single cadence phrase is present but its number/unit is ambiguous ("every so often", "periodically"), the skill must ask once or stop with an invalid-cap blocker.

### Hook-timeout fit

The installed Stop hook timeout is `90000` seconds (set by `upsert_codex_stop_hook.py` and `upsert_claude_stop_hook.py`). The controller enforces:

- `interval_seconds` must be strictly less than the installed hook timeout
- if `deadline_at` is present, each scheduled `next_due_at` (calculated as `now + interval_seconds`) must be `<= deadline_at`
- the total armed window (`deadline_at - created_at`) must itself fit what a single Stop-hook turn can supervise; if the user asks for a window longer than the installed hook timeout but no cadence is armed, the arm must fail loud rather than silently shortening

If any of these checks fail, the arm stops loudly with a hook-timeout-fit error that names the conflicting phrase. Do not turn an interval request into a manual reminder.

## Iteration phrase family (first release)

Supported:

- `max 5 iterations`
- `maximum 4 passes`
- `up to 3 attempts`
- `no more than 2 loops`
- `only try this twice`
- `try this once`
- `stop after 2 attempts`
- `stop after two attempts`

Word-form magnitudes (`once`, `twice`, `three times`) and digit magnitudes (`2`, `5`) both parse. Normalization converts to integer `max_iterations`. The `stop after N ...` phrase is parsed as an iteration cap only when the trailing keyword is `iterations`, `passes`, `attempts`, `loops`, or `times`; without one of those keywords, `stop after 2h` is parsed as a runtime cap instead.

Strictest-cap rule for iterations: when multiple iteration phrases produce different `max_iterations` values, pick the smallest and preserve every source phrase in `cap_evidence`.

If an iteration phrase is likely but the count is ambiguous ("a few times", "several attempts"), the skill must ask once or stop with an invalid-cap blocker.

## Mixing cap types

All three families can coexist in one request. Each normalizes independently:

- `implement this and do not stop until $agent-linter is clean, max runtime 5h, max 3 iterations`
  produces `deadline_at = created_at + 18000`, `max_iterations = 3`, and no cadence.
- `every 30 minutes check whether this host is reachable for the next 6 hours`
  produces `interval_seconds = 1800`, `deadline_at = created_at + 21600`, and no iteration cap.

The strictest-cap rule applies only inside a family. Different families never combine into one cap.

## Ambiguity discipline

- **Ask once or fail loud.** The skill may ask the user exactly one clarifying question when a likely cap or cadence is ambiguous. If the user does not resolve it, stop with an invalid-cap blocker. Do not arm the loop and assume a default.
- **Preserve raw evidence.** Every matched cap phrase is preserved literally in `cap_evidence`. This lets the external evaluator see the user's exact wording when deciding whether a `clean` verdict is honest.
- **Deterministic, not LLM-judged.** Parsing is code, not prose. The evaluator may comment on caps, but it does not enforce them.

## Worked examples

### 1) Simple runtime cap

Input: `Implement this plan and don't stop until $agent-linter is clean, max runtime 5h.`

Output:

- `deadline_at = created_at + 18000`
- `max_iterations`: not set
- `interval_seconds`: not set
- `cap_evidence`: `[{type: "runtime", source_text: "max runtime 5h", normalized: "deadline_at=<created_at+18000>"}]`
- `required_skill_audits`: `[{skill: "agent-linter", target: "<resolved target>", requirement: "clean bill of health", status: "pending", ...}]`

### 2) Cadence plus window

Input: `Every 30 minutes check whether host example.com is reachable, for the next 6 hours.`

Output:

- `interval_seconds = 1800`
- `deadline_at = created_at + 21600`
- `next_due_at` is written by the Stop hook after the first check
- `cap_evidence`:
  - `{type: "cadence", source_text: "Every 30 minutes", normalized: "interval_seconds=1800"}`
  - `{type: "runtime", source_text: "for the next 6 hours", normalized: "deadline_at=<created_at+21600>"}`

### 3) Strictest runtime cap

Input: `max runtime 5h, stop if not done in 3h.`

Output:

- `deadline_at = created_at + 10800` (the 3h phrase is strictest)
- `cap_evidence`:
  - `{type: "runtime", source_text: "max runtime 5h", normalized: "deadline_at=<created_at+18000>"}`
  - `{type: "runtime", source_text: "stop if not done in 3h", normalized: "deadline_at=<created_at+10800>"}`

### 4) Ambiguous cadence → fail loud

Input: `Check every 30 minutes, and also every hour, for the next 6 hours.`

Outcome: two different cadence phrases detected. The skill asks once or stops with `invalid-cap: cadence is ambiguous (every 30 minutes vs every hour)`. No state is armed.

### 5) Cadence that cannot fit the hook timeout → fail loud

Input: `Every 2 days check whether the build is green, for the next 7 days.`

Outcome: `interval_seconds = 172800` exceeds the installed hook timeout of `90000` seconds. The skill stops loudly with a hook-timeout-fit error naming `every 2 days`. The user must either shorten the interval or use a different workflow.

### 6) Likely-cap but ambiguous magnitude → fail loud

Input: `Keep trying for a while until the audit passes.`

Outcome: "a while" is not unambiguous. The skill asks once or stops with `invalid-cap: runtime magnitude is ambiguous ("a while")`. No state is armed.

## What this file does not cover

- Completion semantics (the evaluator decides whether requirements are satisfied; see `evaluator-prompt.md`).
- State schema details (see `controller-contract.md`).
- Routing boundaries against `delay-poll` and specialized loops (see `SKILL.md` and `examples.md`).
