# Hook Arm/Disarm Audit — arch_skill

Date: 2026-04-19
Scope: every hook-backed skill in `skills/` plus the shared Stop-hook runner, install scripts, and references.
Audience: maintainers planning a cleanup of the arm/disarm doctrine across the suite.

> **2026-04-20 status:** §2.5 (legacy single-slot fallback) and §2.9 (silent install legacy handling) are **resolved — legacy surface removed**. The runner no longer honors unsuffixed state files, the `LEGACY_HOOK_SCRIPT_NAMES` collapse logic is gone from both upsert scripts, the `audit_loop_stop_hook.py` tombstone is deleted, and every loop-skill arm runs `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` first to write the canonical hook entries idempotently under `fcntl.flock`. Drift is fail-loud at dispatch with the exact repair command — no silent migration, no transitional shim.

---

## 0. Executive summary

There is **one real arm/disarm mechanism** — a single shared Python Stop-hook runner at `skills/arch-step/scripts/arch_controller_stop_hook.py` that dispatches on a state file written by the parent turn — **wrapped in twelve near-identical prose descriptions across ten skills plus three reference files that are almost-but-not-quite copies of each other**. The mechanism itself is correct. The doctrine around it is the layered mess.

The user's complaint ("some places say arm first, and others arm last") is directionally accurate but not literally true. Every loop skill *is* technically arm-first. What is actually wrong is:

1. The arm step is **positioned differently in each SKILL.md** — sometimes inside a prose paragraph, sometimes as a numbered workflow step, sometimes in a dedicated "Default arm mode" section. Same concept, three narrative shapes.
2. **Three reference files with overlapping names** (`audit-loop/references/auto.md`, `arch-docs/references/auto.md`, `wait/references/arm.md`, `delay-poll/references/arm.md`) each describe the same runner contract with slightly different emphasis, state shape, and preflight checks.
3. The **12-way hand-maintained constants block** in `arch_controller_stop_hook.py:24-77` makes every new controller a per-surface code change plus three prose re-writes.
4. **"Do not disarm early" is implied, not stated.** No SKILL.md contains a bright-line rule *"you never write code that deletes the state file — only the Stop hook does."* That rule is present in English scattered across six sentences in six files.
5. **Concurrent runner protection exists but is unevenly surfaced.** The conflict gate in the shared runner guards against collisions, but users who hit the "two states armed" wall have no documented path to resolve it.

The recommended fix is a shared contract document, one doctrine paragraph inserted verbatim across every loop SKILL.md, a registry-driven runner, and killing the legacy Claude unsuffixed fallback (or guarding it with `fcntl.flock`).

---

## 1. Current state inventory

### 1.1 Shared infrastructure

- **Shared Stop-hook runner**: `skills/arch-step/scripts/arch_controller_stop_hook.py`. Single entry point. Lines 24-77 declare twelve state-file constants, twelve relative-path constants, twelve command names, and twelve display names as parallel module-level literals. Dispatch is "whichever state file exists for this session."
- **Install scripts**: `skills/arch-step/scripts/upsert_codex_stop_hook.py` and `upsert_claude_stop_hook.py`. Write `~/.codex/hooks.json` and `~/.claude/settings.json` respectively. Both collapse two legacy hook script names (`implement_loop_stop_hook.py`, `audit_loop_stop_hook.py`) into the single current shared runner.
- **Install surface**: `Makefile`. `make install` chains skill copy + hook install; no per-skill hook installation.
- **Feature flags**: Codex requires `codex_hooks` feature flag; Claude requires hook-suppressed child runs for any skill that launches fresh children.

### 1.2 Per-skill inventory

#### arch-step (`skills/arch-step/SKILL.md`)

- Hook-backed modes: `auto-plan`, `implement-loop`, `auto-implement` (alias for `implement-loop`).
- State files:
  - `.codex/auto-plan-state.<SESSION_ID>.json`
  - `.claude/arch_skill/auto-plan-state.<SESSION_ID>.json`
  - `.codex/implement-loop-state.<SESSION_ID>.json`
  - `.claude/arch_skill/implement-loop-state.<SESSION_ID>.json`
- Arm timing: arm-first, before any `research`/implementation work.
- Disarm authority: Stop hook only. Explicit rule at line 210: *"do not clear that state from the implementation side before fresh `audit-implementation` has run, even if the pass believes the work is done."*
- Session-scoped: yes, Codex derives from `CODEX_THREAD_ID`; Claude uses `.claude/arch_skill/` with documented legacy single-slot fallback.
- Preflight: both runtimes required; Claude implement-loop also requires hook-suppressed child runs.

#### miniarch-step (`skills/miniarch-step/SKILL.md`)

- Hook-backed modes: same shape as arch-step with `miniarch-step-` prefixed state files.
- Arm timing: identical pattern to arch-step. Arm-first.
- Everything else: structurally a clone of arch-step. Separate SKILL.md maintained in parallel.

#### audit-loop (`skills/audit-loop/SKILL.md`, `references/auto.md`)

- Hook-backed mode: `auto`.
- State file: `.codex/audit-loop-state.<SESSION_ID>.json` / `.claude/arch_skill/audit-loop-state.<SESSION_ID>.json`.
- Arm timing: arm-first, step 2 of 5 in workflow under `### 3) auto`.
- Disarm authority: Stop hook deletes on `CLEAN` (before removing ledger and `.gitignore` entry) or `BLOCKED`.
- Session-scoped: yes, with legacy single-slot fallback.
- Preflight: both runtimes; Claude requires hook-suppressed child runs for fresh review passes.
- Explicit language at `references/auto.md:18`: *"Do not run the Stop hook yourself. After `auto` is armed, just end the turn and let the installed Stop hook run."*

#### comment-loop (`skills/comment-loop/SKILL.md`, `references/auto.md`)

- Hook-backed mode: `auto`.
- State file: `.codex/comment-loop-state.<SESSION_ID>.json` / `.claude/arch_skill/comment-loop-state.<SESSION_ID>.json`.
- Arm timing: arm-first. `SKILL.md:85`: *"Arm the host-aware `auto` controller state described in `references/auto.md`."*
- Disarm authority: Stop hook on `CLEAN`/`BLOCKED`.
- Reference file: `references/auto.md` — nearly identical to audit-loop's.

#### audit-loop-sim (`skills/audit-loop-sim/SKILL.md`, `references/auto.md`)

- Hook-backed mode: `auto`.
- State file: `.codex/audit-loop-sim-state.<SESSION_ID>.json` / equivalent Claude path.
- Arm timing: arm-first.
- Reference file: a third near-identical `references/auto.md`.

#### arch-docs (`skills/arch-docs/SKILL.md`, `references/auto.md`)

- Hook-backed mode: `auto`.
- State file: `.codex/arch-docs-auto-state.<SESSION_ID>.json` / equivalent Claude path.
- Arm timing: arm-first, before first pass. `SKILL.md:102`: *"Arm the host-aware `arch-docs auto` controller state described in `references/auto.md` before the first pass."*
- Reference file: fourth variant of `auto.md` — similar preamble, different body.

#### arch-loop (`skills/arch-loop/SKILL.md`)

- Hook-backed mode: `arch-loop` (top-level command).
- State file: `.codex/arch-loop-state.<SESSION_ID>.json` / equivalent Claude path.
- Arm timing: arm-first, before any work pass. `SKILL.md:59`: *"Write the runtime-specific `arch-loop` state file before any work pass starts so the loop cannot be forgotten mid-turn."*
- Disarm authority: Stop hook, driven by an **external Codex evaluator** — the only skill that delegates verdicts to a fresh unsandboxed Codex `gpt-5.4` `xhigh` run. `SKILL.md:32`: *"The termination verdict comes from a fresh unsandboxed Codex `gpt-5.4` `xhigh` evaluator. The parent agent never self-certifies completion."*
- No dedicated reference file; all lifecycle prose lives in SKILL.md.

#### wait (`skills/wait/SKILL.md`, `references/arm.md`)

- Hook-backed mode: default arm mode (one-shot timed wait).
- State file: `.codex/wait-state.<SESSION_ID>.json` / equivalent Claude path.
- Arm timing: arm-first and arm-only. `SKILL.md:47-55` under `### Default arm mode`.
- Disarm authority: Stop hook fires `resume_prompt` exactly once when `deadline_at` elapses.
- Preflight: explicitly **does NOT** require Claude hook-suppressed child runs. `references/arm.md:49`: *"`wait` explicitly does NOT require the Claude hook-suppressed child-run preflight that `delay-poll` requires."*
- Conflict gate: if any other arch_skill controller state is already armed for the session, the shared runner halts. `references/arm.md:92`: *"the shared runner's conflict gate (`block_when_multiple_controller_states_armed`) halts the next turn with a conflict message."*

#### delay-poll (`skills/delay-poll/SKILL.md`, `references/arm.md`)

- Hook-backed mode: default arm mode (interval-polled wait with a condition check).
- State file: `.codex/delay-poll-state.<SESSION_ID>.json` / equivalent Claude path.
- Arm timing: **conditional arm** — do one immediate grounded check first; arm only if the condition is still false. `SKILL.md:59-62`.
- Disarm authority: Stop hook, on condition-true or deadline.
- Preflight: **requires** Claude hook-suppressed child runs because each re-check is a fresh child run.
- Reference file: second file named `arm.md` — documents a state schema with `check_prompt`, `interval_seconds`, `attempt_count` fields that `wait`'s `arm.md` explicitly forbids.

#### code-review (`skills/code-review/SKILL.md`)

- Hook-backed mode: "hook-backed invocation" — an optional execution path alongside direct invocation.
- State file: `.codex/code-review-state.<SESSION_ID>.json` / equivalent Claude path.
- Arm timing: arm-first for hook-backed runs only; direct runs never arm.
- Disarm authority: Stop hook, after review run completes.
- Documentation: minimal. `SKILL.md:65` is the one-sentence description of the hook-backed mode.

### 1.3 Runner constants (evidence of hand-maintained duplication)

From `skills/arch-step/scripts/arch_controller_stop_hook.py:24-77`:

```
IMPLEMENT_LOOP_STATE_FILE = Path("implement-loop-state.json")
AUTO_PLAN_STATE_FILE = Path("auto-plan-state.json")
MINIARCH_STEP_IMPLEMENT_LOOP_STATE_FILE = Path("miniarch-step-implement-loop-state.json")
MINIARCH_STEP_AUTO_PLAN_STATE_FILE = Path("miniarch-step-auto-plan-state.json")
ARCH_DOCS_AUTO_STATE_FILE = Path("arch-docs-auto-state.json")
AUDIT_LOOP_STATE_FILE = Path("audit-loop-state.json")
COMMENT_LOOP_STATE_FILE = Path("comment-loop-state.json")
AUDIT_LOOP_SIM_STATE_FILE = Path("audit-loop-sim-state.json")
DELAY_POLL_STATE_FILE = Path("delay-poll-state.json")
CODE_REVIEW_STATE_FILE = Path("code-review-state.json")
WAIT_STATE_FILE = Path("wait-state.json")
ARCH_LOOP_STATE_FILE = Path("arch-loop-state.json")
```

Plus matching parallel lists for `.codex/` relative paths (lines 36-47), command names (lines 53-64), and display names (lines 66-77). Adding a thirteenth controller means four constant additions in this file, plus a dispatch branch, plus a SKILL.md write, plus a reference file copy, plus an install-script update.

---

## 2. What is actually inconsistent

### 2.1 Narrative position of the arm instruction

This is the real source of the "feels different across skills" perception. Read three SKILL.md files side by side:

- **arch-step** (`SKILL.md:174-190`) — the arm rule is embedded in a single 150-word paragraph about auto-plan. You have to read the paragraph to extract it.
- **audit-loop** (`SKILL.md:86-92`) — the arm rule is step 2 of a 5-step workflow under heading `### 3) auto`.
- **wait** (`SKILL.md:47-55`) — the arm rule is the entire purpose of the skill, under heading `### Default arm mode`, as a bullet list.
- **delay-poll** (`SKILL.md:59-62`) — the arm rule is bullets inside `## Default arm mode`, but with an explicit conditional branch ahead of the arm.

All four are arm-first. A reader scanning them thinks they are different because the framing differs: paragraph vs numbered workflow vs bullet list vs conditional branch. This is the "layers of legacy" feel even though no single skill actually says "arm last."

### 2.2 Two `arm.md` files that look identical and are not

- `skills/wait/references/arm.md` — 108 lines. Describes one-shot wait semantics. Documents an explicit rejection list forbidding any `delay-poll` fields (line 84: *"The runner rejects state files that carry any of them"*).
- `skills/delay-poll/references/arm.md` — 57 lines. Describes polling semantics with `check_prompt`, `interval_seconds`, `attempt_count`.

Two files with the same name, describing mutually-exclusive state schemas against the same runner. A reader who opens the wrong one gets the wrong model.

### 2.3 Four `auto.md` files with near-identical preambles

- `skills/audit-loop/references/auto.md`
- `skills/comment-loop/references/auto.md`
- `skills/audit-loop-sim/references/auto.md`
- `skills/arch-docs/references/auto.md`

The first three are near-identical templates. The fourth is a sibling variant. They drift without a master — changing one does not propagate. This is exactly how future layered legacy grows.

### 2.4 The "do not disarm early" rule is implicit, not stated

Closest actual language in the repo:

- `arch-step/SKILL.md:182`: *"the parent `auto-plan` pass must not clear successful controller state"*
- `arch-step/SKILL.md:190`: *"if a stage stops early after controller state is armed, stop honestly and let the Stop hook clear the matching state"*
- `arch-step/SKILL.md:210`: *"do not clear that state from the implementation side before fresh `audit-implementation` has run, even if the pass believes the work is done"*
- `miniarch-step/SKILL.md:184`: equivalent language.
- `audit-loop/references/auto.md:18`: *"Do not run the Stop hook yourself. After `auto` is armed, just end the turn and let the installed Stop hook run."*

These are correct but **specific to individual controllers**. Nowhere in the doctrine does a universal rule appear, in the form:

> Parent turns never delete state files. The Stop hook is the only process that deletes state. If you think you need to disarm early, you are wrong — end your turn and let the hook decide.

### 2.5 Claude legacy single-slot fallback is a race

Every reference file repeats this line verbatim:

> *"otherwise create `.claude/arch_skill/<name>-state.json` only as a legacy single-slot fallback and let the first Stop-hook turn claim it into the session-scoped path"*

This path is a hazard for concurrent runs. Two parallel Claude sessions in the same repo, each missing a session id at arm time, both write to the unsuffixed path. Second overwrites first. The "first Stop-hook turn claims it" protection only works if the hook fires before the second session arms — timing-dependent.

Nothing in the SKILL.md files says "Claude session IDs are now available at arm time — the fallback is dead code." If Claude does expose session id at arm time, the fallback should be removed. If it does not, the fallback is a known race.

### 2.6 No user-facing recovery procedure

Scenario: terminal dies mid-loop. State file on disk. User restarts.

- `README.md:71`: *"the user must clear the stale state manually"*
- No SKILL.md tells the user which file to delete.
- No skill ships a `--disarm` or recovery command.
- No staleness sweep on runner startup.

### 2.7 Runner duplication

`arch_controller_stop_hook.py:24-77` is 54 lines of parallel constants (state file × relative path × command × display name, twelve times). Adding a controller is four constant declarations plus a dispatch branch plus a SKILL.md write plus a reference file copy plus an install-script update. The friction causes drift.

### 2.8 Outliers

- **`code-review`** uses the arm mechanism for "hook-backed invocation" only — a mode that is barely documented and does not fit the loop model. Smells like an afterthought bolted onto the shared runner.
- **`arch-loop`** adds a whole external Codex evaluator to decide the verdict. That is a real architectural variation, not a quirk. It is the only skill that does this. It should either become the template (all controllers use external evaluators) or be isolated as a deliberate divergence.

### 2.9 Installation legacy handling is silent

`upsert_codex_stop_hook.py` and `upsert_claude_stop_hook.py` include a `LEGACY_HOOK_SCRIPT_NAMES` set that collapses old per-skill hook scripts (`implement_loop_stop_hook.py`, `audit_loop_stop_hook.py`) into the single shared runner. This is good behavior — but no SKILL.md or README tells users that `make install` will silently rewrite their hooks on upgrade.

---

## 3. Quoted evidence

### 3.1 arch-step auto-plan — arm first, disarm only via Stop hook

`skills/arch-step/SKILL.md:173-190`:

```
`auto-plan` is a bounded planning controller in Codex and Claude Code. `DOC_PATH` is always
the planning ledger. The armed controller state lives under `.codex/` in Codex and under
`.claude/arch_skill/` in Claude Code. On a fresh doc, the initial `auto-plan` pass arms state,
runs only `research` against the same `DOC_PATH`, then ends its turn naturally. On reruns,
the parent pass re-arms state against the same `DOC_PATH` and lets the installed Stop hook
continue from the first incomplete stage already visible in the doc.
...
- the initial `auto-plan` pass must run only `research`, then end the turn
- keep the runtime-local controller state armed for the live run and treat `DOC_PATH`
  as the progress ledger
- if a stage stops early after controller state is armed, stop honestly and let the Stop
  hook clear the matching state
```

### 3.2 arch-step implement-loop — arm before work, do not clear yourself

`skills/arch-step/SKILL.md:207-212`:

```
- arm runtime-local implement-loop state before implementation work so the live loop cannot
  be forgotten mid-run
- do not hand control back to audit until the current full ordered implementation frontier
  is done or genuinely blocked, and its phase claims have credible proof
- keep the runtime-local implement-loop state aligned with the live run
- do not clear that state from the implementation side before fresh `audit-implementation`
  has run, even if the pass believes the work is done
- do not let the parent implementation pass stand in for the clean auditor by writing the
  authoritative audit block or the `Use $arch-docs` handoff
```

### 3.3 audit-loop auto — arm before first run, Stop hook deletes on terminal verdict

`skills/audit-loop/references/auto.md:35-60`:

```
## State file contract

Create the host-aware state path before the first `run` pass:

- Codex: derive `SESSION_ID` from `CODEX_THREAD_ID`, then create `.codex/audit-loop-state.<SESSION_ID>.json`
- Claude Code: prefer `.claude/arch_skill/audit-loop-state.<SESSION_ID>.json` when the session id
  is available before the first Stop-hook turn; otherwise create `.claude/arch_skill/audit-loop-state.json`
  only as a legacy single-slot fallback and let the first Stop-hook turn claim it into the
  session-scoped path

Lifecycle:

- create or refresh it after preflight and before the first `run`
- keep it armed while verdicts are `CONTINUE`
- the Stop hook deletes it before stopping on `BLOCKED`
- the Stop hook deletes it on `CLEAN` before removing the ledger and `.gitignore` entry
```

### 3.4 delay-poll — conditional arm (do not arm if already ready)

`skills/delay-poll/SKILL.md:59-62`:

```
- Run one immediate grounded read-only check against the literal `check_prompt`.
- If the condition is already true, continue immediately from the current turn with the
  `resume_prompt` plus the latest summary and do not arm state.
- If the condition is not yet true, arm the host-aware `delay-poll` controller state
  described in `references/arm.md` and keep it aligned with the live wait.
- Once the controller is armed, end the turn naturally. The installed Stop hook now owns
  sleeping, re-checking, timeout handling, and continuation.
```

### 3.5 wait — arm-first, parse-first, fail-loud

`skills/wait/SKILL.md:47-55`:

```
### Default arm mode

- Resolve the literal `resume_prompt`. If the user did not supply one explicitly, ask. Never invent a prompt.
- Parse the duration into `duration_seconds` using the grammar documented in `references/arm.md`.
- If `duration_seconds` is 0 or negative, or exceeds 24 hours without an explicit cap override
  from the user, refuse to arm and say why.
- Compute `armed_at = current_epoch_seconds()` and `deadline_at = armed_at + duration_seconds`.
- Write the state JSON from `references/arm.md` to the host-aware path and confirm it is the
  only `arch_skill` controller state currently armed for this session.
- Tell the user plainly to end the turn and let the installed Stop hook own the wait.
```

### 3.6 arch-loop — arm before work pass, external evaluator owns verdict

`skills/arch-loop/SKILL.md:59-75`:

```
- Write the runtime-specific `arch-loop` state file before any work pass starts so the loop
  cannot be forgotten mid-turn.
- Do one bounded work pass toward the requirements, or one immediate grounded check when the
  request is cadence/check-only.
- Run the requested named audits inside that pass and update their evidence in state.
- Update `last_work_summary` and `last_verification_summary`.
- End the turn naturally. The installed Stop hook now owns continuation.

### 2) Hook-owned continuation

The installed Stop hook is the only actor that may launch the external evaluator and decide
whether the loop continues. The shared runner:

- validates the state and session,
- enforces `deadline_at` and the installed hook timeout against the requested cadence,
- launches the fresh Codex `gpt-5.4` `xhigh` evaluator with the prompt at `references/evaluator-prompt.md`,
- parses the structured verdict, and
- transitions state per the contract in `references/controller-contract.md`.

`clean` and `blocked` clear state. `continue` with `parent_work` keeps state armed and blocks
with a continuation prompt that names `$arch-loop` plus the next concrete task. `continue` with
`wait_recheck` keeps state armed, sleeps until the next due time, and reruns the evaluator
without waking the parent thread.
```

### 3.7 Concurrent runner conflict gate

`skills/wait/references/arm.md:92`:

```
If any other `arch_skill` controller state is already armed for this session (for example,
`delay-poll`, `auto-plan`, `implement-loop`), the shared runner's conflict gate
(`block_when_multiple_controller_states_armed`) halts the next turn with a conflict message
listing both state files. Do not arm `wait` alongside another kind; resolve the conflict first.
```

`README.md:70-71`:

```
Within one session, only one auto controller kind may be armed at a time: the installed Stop
hook runs a conflict gate before dispatch, and if two or more controller state files are armed
for the same session, the turn halts with a conflict message naming both paths and the user
must clear the stale state manually.
```

### 3.8 Session-scoped paths and the legacy fallback

`skills/arch-step/SKILL.md:216-217`:

```
- Codex should derive `<SESSION_ID>` from `CODEX_THREAD_ID` and arm the session-scoped
  `.codex/...<SESSION_ID>.json` path for the current session.
- Claude Code should arm `.claude/arch_skill/...` for the active controller. When Claude
  exposes session id before the first Stop-hook turn, use the session-scoped path there too.
  Otherwise the unsuffixed runtime-local path is only a legacy single-slot fallback; the
  first Stop-hook turn must claim it into the session-scoped path.
```

---

## 4. The recommended clean pattern

### 4.1 Principles

1. **Armed-by-default via structural position.** The arm instruction is always the first numbered step of the workflow, with the same opening words every time.
2. **Stop-hook-exclusive disarm, stated universally.** A single doctrine line, lifted into every SKILL.md verbatim, that says parent turns never delete state.
3. **One shared reference.** All loop skills point at `skills/_shared/controller-contract.md` for the state contract, lifecycle, preflight, and recovery. Skill-local references describe only what is unique to that controller (state schema, verdict source, continuation semantics).
4. **Session-scoped only.** Remove the legacy Claude unsuffixed fallback if session IDs are now available at arm time. If they are not, guard the fallback with an OS-level `fcntl.flock` to make the race safe.
5. **Registry-driven runner.** Replace the twelve hardcoded constants with a single `CONTROLLERS` dict; adding a controller becomes one entry plus one dispatch function.
6. **Documented recovery.** Every loop skill links to one canonical "manual recovery" section with exact commands.

### 4.2 The one-paragraph doctrine that belongs in every loop SKILL.md

```
Arm first, disarm never. This skill is hook-owned. The very first step of
every invocation writes a session-scoped controller state file; the very
last step of the parent turn is to end the turn. Parent turns do not run
the Stop hook, do not delete state, and do not "clean up early" — the
Stop hook is the only process that clears state, and it does so only on
CLEAN, BLOCKED, or deadline. If you believe the loop is done, end your
turn; the Stop hook will verify and clean up. If the loop needs to stop
for a reason only you know, say so plainly in the turn text and still end
the turn — do not delete state. Recovery: see
skills/_shared/controller-contract.md § Manual recovery.
```

This paragraph should appear in every loop SKILL.md, by copy or by reference. Every deviation (arch-loop's external evaluator, delay-poll's conditional arm, wait's one-shot) is a footnote beneath this paragraph, not a replacement for it.

### 4.3 Workflow shape for every loop skill

```
## Workflow

1. Arm: preflight → write session-scoped state → end turn.
2. (Hook-owned, not your problem) Stop hook runs the body.
3. (Hook-owned, not your problem) Stop hook clears state on terminal verdict.
```

Three lines. Every loop skill. The skill-specific reference file fills in what "body" and "terminal verdict" mean for that controller.

### 4.4 Concurrent runner contract

| Case | Behavior |
|---|---|
| Two arms of same kind, same session | Latest arm overwrites. Documented. |
| Two arms of different kinds, same session | Conflict gate fires; turn halts; message names both state files and links recovery doc. |
| Two arms, different sessions, same working dir | Session-scoped paths keep them isolated. No collision. |
| Missing session id at arm (legacy Claude) | Guard the unsuffixed path with `fcntl.flock`. If lock held, fail loud: "another session holds arch_skill state in this repo — rerun from a session that exposes its id, or use recovery." |
| Terminal dies mid-loop | State file persists. On next session, shared runner's first action is a staleness check (last-mtime vs `deadline_at`). Stale state → move to `.codex/_stale/` or `.claude/arch_skill/_stale/` with timestamp; do not auto-resume; emit one-line user message pointing at recovery. |

The flock guard and staleness check are new — neither exists today.

### 4.5 Registry-driven runner (code sketch)

Replace `arch_controller_stop_hook.py:24-77` with:

```python
@dataclass(frozen=True)
class Controller:
    state_file: str
    dispatch: Callable[[ResolvedControllerState], int]
    display: str

CONTROLLERS = {
    "auto-plan": Controller(
        state_file="auto-plan-state.json",
        dispatch=dispatch_auto_plan,
        display="auto-plan",
    ),
    "implement-loop": Controller(
        state_file="implement-loop-state.json",
        dispatch=dispatch_implement_loop,
        display="implement-loop",
    ),
    # ... one entry per controller
}
```

Adding a controller becomes one-line-plus-one-function, not four constants plus a branch. This also enables tooling: `--list-controllers`, `--disarm <name>` for recovery, `--doctor` for install verification.

### 4.6 Reference file consolidation

Target layout:

```
skills/_shared/controller-contract.md    ← preflight, state lifecycle, manual recovery, conflict gate
skills/<skill>/references/controller.md  ← ONLY this controller's state schema, verdict source, continuation rule
```

Files to merge into the shared doc:

- `skills/audit-loop/references/auto.md`
- `skills/comment-loop/references/auto.md`
- `skills/audit-loop-sim/references/auto.md`
- `skills/arch-docs/references/auto.md`
- `skills/wait/references/arm.md`
- `skills/delay-poll/references/arm.md`

Each skill keeps only a small delta file describing what is unique to it.

### 4.7 Manual recovery procedure

Add to README and the shared reference:

```
## Manual recovery

If a loop left stale state on disk (terminal died, user force-stopped,
conflict gate fired), clear it manually:

# Codex
rm .codex/<controller>-state.<SESSION_ID>.json

# Claude
rm .claude/arch_skill/<controller>-state.<SESSION_ID>.json

To clear every stale arch_skill state in this repo:
~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --disarm-all

The --disarm-all flag is additive (it only removes state files, never
source code or plans).
```

Today nothing like `--disarm-all` exists. It should.

---

## 5. Migration plan

Each step is small enough to land, verify (`npx skills check`, `make verify_install`), and review independently.

1. **Create `skills/_shared/controller-contract.md`.** Merge the best prose from the four `auto.md` and two `arm.md` files into one canonical doc: preflight, state lifecycle, "arm first, disarm never" doctrine paragraph, conflict gate, manual recovery. No behavior change — prose only.
2. **Insert the doctrine paragraph into every loop SKILL.md.** Identical wording across arch-step, miniarch-step, audit-loop, comment-loop, audit-loop-sim, arch-docs, arch-loop, wait, delay-poll, (optionally) code-review. No behavior change.
3. **Normalize workflow structure.** Move the arm instruction to position 1 in each skill's workflow section, using the three-line shape in §4.3. arch-step's paragraph prose gets restructured into numbered steps.
4. **Refactor the runner to a `CONTROLLERS` registry.** Pure refactor — same behavior, same state files, same dispatch. Adds a test harness for the dispatch table. Largest single diff; best as its own PR.
5. **Add `--disarm-all` and `--doctor` flags to the runner.** User-facing recovery. Document in README and shared reference.
6. **Add staleness sweep on runner startup.** First thing the Stop hook does on any turn: scan for state files whose `deadline_at` is long past or whose session is gone; move to `_stale/`. Document the behavior.
7. **Guard the Claude unsuffixed fallback with `fcntl.flock`.** Or, if Claude now exposes session id at arm time, delete the fallback entirely — the cleaner path.
8. **Collapse `references/auto.md` across audit-loop/comment-loop/audit-loop-sim/arch-docs into per-skill deltas** pointing at the shared contract. Same for the two `arm.md` files — rename to `wait/references/wait-controller.md` and `delay-poll/references/delay-poll-controller.md` to kill the name collision.
9. **Decide on `code-review`'s hook mode.** Either promote it to a first-class controller with the same doctrine, or remove hook-backed invocation and make it direct-only. Right now it is a bolted-on third mode of a skill that mostly is not a loop.
10. **Decide on `arch-loop`'s external evaluator.** Is this the future template (all controllers evaluated by a fresh Codex child) or a deliberate one-off? The doctrine should name which.

---

## 6. Open questions

1. **Claude session IDs at arm time.** Does Claude Code now expose the session id before the first Stop-hook turn? If yes, the legacy unsuffixed fallback can die. If no, the flock guard is required. Cannot be determined from the repo alone.
2. **`code-review` hook mode usage.** Is it used in practice, or added speculatively? If nobody uses hook-backed code-review, cut it.
3. **`arch-loop` external evaluator direction.** Intentional one-off, or should the rest of the suite migrate to the same pattern? This is the single biggest doctrine fork.
4. **Gemini.** The Makefile filters Gemini out of loop skills, but the doctrine never explicitly says "loop skills are Codex+Claude only." Should that be stated?
5. **Recovery UX shape.** Want `--disarm-all` (nuke all state), `--disarm <controller>` (nuke one), or both? Default recommendation: both, but `--disarm-all` alone is simpler.
6. **`delay-poll`'s conditional arm.** Keep as-is (intentional optimization) or move the pre-check into the Stop hook (so the arm step is pure and unconditional like the others)? Moving it makes arm-first truly universal.

---

## 7. Smallest first move

Steps 1 + 2: create the shared contract doc, insert the identical doctrine paragraph across loop SKILL.md files. Pure docs change, verifiable with `npx skills check`, and immediately fixes the "feels different across skills" complaint without touching any runner code. Steps 3-10 can then land individually.
