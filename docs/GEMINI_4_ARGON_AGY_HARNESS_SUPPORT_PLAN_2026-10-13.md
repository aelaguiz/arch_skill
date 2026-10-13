---
title: "Gemini 4 Argon on the Antigravity CLI (agy): Harness Support Plan"
date: 2026-10-13
status: complete
completed: 2026-10-13
fallback_policy: forbidden
owners: [aelaguiz]
doc_type: new_system
related:
  - docs/KIMI_K3_PROVIDER_SUPPORT_FOR_AGENT_SKILLS_2026-07-17.md
  - skills/_shared/model_resolution.py
  - skills/_shared/agent-orchestration-policy.md
  - skills/_shared/native-child-capabilities.md
  - skills/agent-delegate/references/model-and-invocation.md
  - skills/fresh-consult/references/model-and-invocation.md
  - skills/model-consensus/references/model-and-invocation.md
  - skills/arch-epic/scripts/run_arch_epic.py
  - skills/stepwise/scripts/run_stepwise.py
  - Makefile
---

# TL;DR

Two separate jobs, both needed for "Argon is supported":

1. **Argon as a worker, consultant, or reviewer from any session.** Add a sixth
   external runtime, `agy`, next to Claude, Codex, Cursor Agent, Grok, and Kimi.
   A user can then say "argon high", "gemini", or "agy" to `$agent-delegate`,
   `$fresh-consult`, `$model-consensus`, `$stepwise`, or `$arch-epic`, and the
   skill runs Gemini 4 Argon through `agy` with an exact, resumable session.
   This follows the Kimi K3 change of 2026-07-18 file for file: one shared
   resolver, three invocation references, two runner scripts, the doctrine
   lists, and tests. 46 live files list the current five runtimes, and every
   one of them needs the sixth.
2. **agy as a place our skills run.** Today an `agy` session sees none of our
   skills. It loads only its own built-ins. Its global skill folder is
   `~/.gemini/config/skills/`. It also scans the `~/.gemini/skills/` folder that
   `make install` fills for the Gemini CLI, but rejects every skill there,
   because that copy has its frontmatter stripped and agy requires it. This
   needs a new install target, plus an
   `agy` column in the native-child facts so our delegation rules work when
   Argon is the parent.

Herdr already supports `agy` (`herdr agent start --kind agy`, integration
`antigravity-cli`), so the watcher and Herdr skills need no change.
Reading agy history in `$agent-history` and pooling Google accounts in AIMgr
are real gaps, but they are separate features and are left out of this plan.

# What we support today

| Harness (executable) | Models our skills route to it | How skills use it |
|---|---|---|
| Codex CLI (`codex`) | `gpt-6.1-sol` (default, `xhigh`), `gpt-6-astra`, `gpt-6-sol`, `gpt-6-luna`, `gpt-5.6-terra`, Fugu / Fugu Ultra profiles; `gpt-5.4` and `gpt-5.5` blocked | Host for skills (`~/.agents/skills`); native children; external lane through AIMgr; `-p yolo` review lane |
| Claude Code (`claude`) | Fable, Opus, Sonnet, Haiku families (e.g. `claude-opus-5-5`, `claude-fable-5-1`) | Host (`~/.claude/skills`); native subagents; external lane through AIMgr |
| Cursor Agent (`agent`) | `composer-2.5-fast` only | External lane only |
| Grok CLI (`grok`) | `grok-4.6` for natural phrases; exact `grok-*` slugs preserved | External lane; Prime can run Grok through AIMgr |
| Kimi Code (`kimi`) | `kimi-code/k3`, default `max` | External lane |
| Prime Agent | Any provider the installation is signed in to | Host with cross-provider native children; launched by `aim prime run` |
| Gemini CLI (`gemini`) | none routed | Install target only (`~/.gemini/skills`) |
| Hermes Agent | none routed | Install target only (existing Hermes roots) |
| ChatGPT web (BrowserOS) | GPT-6 Astra Pro | `$chatgpt-web` consultations |
| **Antigravity CLI (`agy`)** | **none today** | **not an install target, not a runtime** |

Routing rule in `skills/_shared/model_resolution.py`: each provider's models run
only through that provider's harness, and a phrase that mixes two providers
fails instead of guessing.

# What was verified live (2026-10-13, agy 1.3.4)

All probes ran in a scratch folder outside this repo with
`--model gemini-4-argon --effort low`.

- **Catalog.** `agy models` lists `gemini-4-argon-{low,medium,high}`,
  `gemini-3.8-flash-{low,medium,high}`, `claude-opus-5-5-*`,
  `claude-sonnet-5-5-*`, and `gpt-oss-120b-medium`. The first line is
  `Fetching available models...`; each model line is `<id>\t<display name>`.
- **Efforts.** Argon accepts `low`, `medium`, `high`. `--effort xhigh` and
  `--effort max` exit 1 with `gemini-4-argon has no "xhigh" effort (available:
  low, medium, high)`. A baked id such as `--model gemini-4-argon-high` also
  works. Amir's own agy setting is `Gemini 4 Argon (High)`.
- **Fresh headless run.** `agy -p "<prompt>" --model gemini-4-argon --effort low
  --output-format stream-json > events.jsonl` exits 0 with output redirected to
  a file, so the old v1.0.0 empty-stdout bug no longer applies. Events:
  - `{"event":"init","conversation_id":"<uuid>","init":{"model":...,"cwd":...,"tools":[...],"permission_mode":...}}`
    is the first line, so the session id is known before any work happens.
  - `{"event":"step_update","step_update":{...,"text_delta":"..."}}` streams progress.
  - `{"event":"result","result":{"conversation_id":...,"status":"SUCCESS","response":"...","num_turns":N,"usage":{...}}}`
    is the last line. On failure, `status` is `ERROR` with an `error` string.
- **Exact resume.** `agy --conversation <id> -p "<prompt>" ...` answered from the
  earlier turn ("MANGO"). It also worked from a different folder. `-c/--continue`
  picks the latest conversation and must never be used.
- **Structured verdicts.** `--json-schema <path>` with `--output-format json`
  returns the parsed object in `structured_output`. The `response` text in the
  same envelope carried extra keys (`toolAction`, `toolSummary`), so parsers must
  read `structured_output`, not `response`.
- **Prompt delivery.** The prompt is one argv value after `-p`. Piped stdin with
  `--input-format stream-json` exists, but it rejected two guessed message
  shapes (`stream input message is missing the "event" field`), and the shape is
  undocumented. Do not use it.
- **Timing field.** `duration_seconds` on a resumed turn read 400 seconds for a
  run that finished inside a 150-second timeout. It appears to count from the
  conversation's previous activity. Receipts must measure wall-clock themselves.
- **Plan mode.** `--mode plan` writes an `implementation_plan.md` artifact and
  waits for approval instead of answering. It is not a read-only review mode.
- **Permissions.** Print mode ran with `permission_mode: always-proceed` because
  Amir's `~/.gemini/antigravity-cli/settings.json` sets `toolPermission` to
  `always-proceed`. The shipped default is `request-review`, which a headless run
  cannot answer. Editful workers must pass `--dangerously-skip-permissions`
  explicitly so behavior does not depend on each machine's settings.
- **Skills.** In a plain folder, agy listed only its built-ins
  (`agy-customizations`, `antigravity-guide`). In a folder whose
  `.agents/skills.json` registered `~/.agents/skills`, it listed 110 skills,
  including `agent-delegate`, `fresh-consult`, `model-consensus`, `stepwise`, and
  `arch-step`, and it resolved `../_shared/agent-orchestration-policy.md`.
  Bundled docs (`builtin/skills/agy-customizations`) name `~/.gemini/config/`
  as the global discovery root, with skills at `skills/<name>/SKILL.md`, the
  same layout our skills already use.
- **Native subagents** (from the tool schemas agy exposes to the model):
  `invoke_subagent` takes `Model` as a tier enum `inherit | flash_lite | flash |
  pro` (no exact model id, no effort), and `Workspace` as `inherit | branch |
  share` (`branch` is an isolated copy, `share` is worktree-like). A child starts
  from its definition's `system_prompt` plus the `Prompt`, so it starts clean.
  It is resumed through `send_message` to its `conversationId`. Its own fan-out
  is off unless the definition sets `enable_subagent_tools`. `manage_subagents`
  lists and kills children. The concurrency cap is unknown.
- **No equivalents found** for Kimi's no-auto-update variable or Claude's
  hook-disable setting. agy subprocesses run the user's global hooks in
  `~/.gemini/config/hooks.json` (currently the Orca status hook) and may
  self-update between runs.

Outside reports: Google began rolling Argon out on 2026-10-13 to Google AI Ultra
subscribers in the Antigravity desktop app and CLI. AI Pro subscribers get Argon
in the Gemini app but not in Antigravity. A machine signed in to a non-Ultra
Google account will not list Argon.

# Part 1: Argon as an external runtime (`agy`)

## Decisions

- **Runtime name `agy`**, after the executable, the way `kimi`, `grok`, and
  `agent` are named. Phrase triggers: `agy`, `antigravity`, `gemini`, `argon`.
- **Default model `gemini-4-argon`.** Bare `agy`, `antigravity`, `gemini`, or
  `argon` resolves to it. `gemini flash` or `gemini-3.8-flash` resolves to
  `gemini-3.8-flash`, and only when named. A natural version that is not in the
  catalog, such as "gemini 4.5 argon", fails. It is never rewritten.
- **Efforts `low | medium | high`.** An omitted effort resolves to `high` with
  `effort_source="preference_default"`, the label Codex's `xhigh` default uses.
  `high` is Amir's own agy setting and Argon's top level. `xhigh`, `max`, and
  `ultra` fail in the resolver, before agy rejects them. A baked suffix
  (`gemini-4-argon-high`) is read as model plus effort.
- **Only Gemini models go through agy.** agy also lists Claude Opus 5.5, Sonnet
  5.5, and GPT-OSS. Under the existing routing rule, Opus stays on Claude Code,
  and "agy opus" fails as a mixed-provider phrase.
- **Collision with Cursor's bare `agent`.** `_infer_runtime` treats bare
  `agent` as Cursor Agent today, so "antigravity agent" would trip both
  providers. When an agy keyword is present, only `cursor`, `cursor-agent`, or
  `cursor agent` counts as Cursor. "Cursor agent argon" still fails as mixed.
- **Invocation.** Run from `work_root`; agy has no `-C` flag. Use
  `agy --print=<prompt> --model <model> --effort <effort> --output-format stream-json --print-timeout 0 --dangerously-skip-permissions`.
  - The attached `--print=` form keeps a prompt that looks like a flag from
    being read as one; agy's own error message recommends it. Shared helpers
    `agy_prompt_arg()` and `agy_model_args()` in `model_resolution.py` build
    those pieces.
  - `--print-timeout 0` pins "wait for the turn": the installed help says the
    default is 0, but older builds documented 5 minutes, which would kill long
    worker turns.
  - Every headless run, critics and consults included, passes
    `--dangerously-skip-permissions`. A headless run cannot answer a permission
    prompt, so without the flag a machine on the shipped `request-review`
    default would silently refuse tools. The read-only guard for critics and
    consults is the no-edit contract plus the parent's diff check, which is how
    the Grok (`bypassPermissions`) and Kimi (print-mode auto-approve) lanes
    already work.
  - Critics with a structured verdict add `--json-schema <schema path>` and
    read `structured_output`. This is native structured output, unlike Grok and
    Kimi, which take the schema inside the prompt.
- **Receipts.** The session id is `init.conversation_id`, cross-checked against
  `result.conversation_id`. The final text is `result.response` when
  `result.status == "SUCCESS"`. A zero exit with no `result` event, an `ERROR`
  status, or empty text counts as malformed: keep the run folder, report it
  loudly, and never fall back. Record `agy --version` in the receipt, because
  agy can update itself between runs.
- **Resume** is `agy --conversation <exact id>` only, from the same `work_root`.
  agy does not fail on an id it does not know: it starts a new conversation,
  exits 0 with `SUCCESS` under a new id, and only warns on stderr
  (`warning: conversation "..." not found`). Every resume therefore compares
  the returned conversation id with the requested one, and treats a mismatch
  as a failed resume that keeps the run folder, never as success.
  `-c/--continue` is banned, matching the existing bans on Claude `--continue`
  and Codex `--last`.
- **Discovery.** `discover_agy_models()` runs `agy models`, skips lines without a
  tab, strips a trailing `-(low|medium|high)` to get base ids, and keeps the
  effort set per base id. It returns empty if the command fails or the output
  shape changes, like `discover_kimi_models()`. If the catalog is non-empty and
  lacks the requested model, the run fails and the error names the account and
  plan, because Argon needs Ultra.
- **No new runner, registry, or provider framework.** agy joins as a peer of
  Kimi in each existing switch, which is the same minimal-diff rule the Kimi
  change used.

## Files to change

The 46 live files that mention Kimi today are the complete list. A search for
files that name Grok but not Kimi came back empty, so no other runtime lists
exist.

**A. Shared resolver:** `skills/_shared/model_resolution.py`
- Add `"agy"` to `VALID_RUNTIMES`, and add `PREFERRED_AGY_MODEL`,
  `PREFERRED_AGY_EFFORT`, `_AGY_EFFORTS`, the agy model regex, `discover_agy_models()`,
  `_resolve_agy_model()`, `_validate_agy_effort()`, and
  `agy_model_args(model, effort)` returning `["--model", model, "--effort", effort]`.
- Add `has_agy` and the "Gemini" family to `_infer_runtime`, and apply the bare
  `agent` rule above.
- Add the `agy` branches and an `agy_models` parameter to
  `resolve_execution_phrase` and `resolve_role_execution_policy`. Update the
  unresolved-runtime message, the module docstring, and the examples.

**B. The three invocation references** (each keeps its own full copy):
- `skills/agent-delegate/references/model-and-invocation.md`: `## agy Fresh` and
  `## agy Resume` after the Kimi pair; the required-values enum; runtime
  inference; phrase resolution with examples (`argon high`, `gemini`,
  `gemini flash medium`, `agy opus` failing); effort resolution; final-text and
  session-id rules under the run-folder section; failure behavior.
- `skills/fresh-consult/references/model-and-invocation.md` and
  `skills/model-consensus/references/model-and-invocation.md`: the same block,
  adapted to each file's section names and receipt layout. Argon gives
  `$model-consensus` a Google participant for provider diversity.
- `skills/agent-delegate/references/delegate-prompt-and-output.md` and
  `skills/model-consensus/references/workflow-contract.md`: the runtime mentions.

**C. Runner scripts:**
- `skills/arch-epic/scripts/run_arch_epic.py`: `_agy_argv`, `_agy_worker_argv`,
  `_agy_critic_argv` (with `--json-schema`), `_parse_agy_final_json`, and
  `_parse_agy_session_id`; `agy` branches at each Kimi dispatch point (worker
  run, auto-critic spawn, critic spawn, worker and critic finalize); add `agy`
  to the `--runtime` choices.
- `skills/stepwise/scripts/run_stepwise.py`: the same builders and parsers;
  `agy` branches in step spawn, resume, diagnose, and critic spawn, and in session
  capture with the existing `UNRECOVERABLE` exit-4 rule; add `agy` to all four
  `--runtime` choices.

**D. Doctrine and metadata lists** (add agy wherever Kimi is listed; no new
rules):
- `skills/_shared/agent-orchestration-policy.md`: the external-runtime list in
  "A child must not spawn external agents".
- arch-epic: `SKILL.md`, `references/{model-and-effort,critic-contract,critic-prompt,epic-doc-contract,resume-semantics,workflow-contract}.md`.
- stepwise: `SKILL.md`, `references/{model-and-effort,session-resume,critic-contract,critic-prompt,execution-routing,manifest-schema,run-directory-layout,session-prompt-contracts}.md`.
  Update `session-resume.md` first, because it holds the CLI mechanics: add a
  "Verified against agy 1.3.4" note, sections for a fresh resumable step, a step
  resume, and a fresh critic with schema, plus three smoke commands.
- conductor: `SKILL.md`, `references/{delegation-and-monitoring,worker-prompt-contract}.md`.
- `SKILL.md` descriptions and routing blocks for `agent-delegate`,
  `fresh-consult`, `model-consensus`, and `stepwise`, plus their
  `agents/openai.yaml` provider lists. Keep each description under its length
  cap.
- The "do not start provider CLIs yourself" lines in `plan-implement` (SKILL.md
  and four references), `plan-audit` (two references), and
  `cynical-{code-review,architecture-review,cruft-removal}/SKILL.md`. These are
  wording changes only.
- `README.md`, `AGENTS.md`, `docs/arch_skill_usage_guide.md`: the provider
  inventory and routing sentence. All three files have uncommitted edits by
  Amir. Patch only the provider paragraphs and keep his edits.

**E. Tests**
- `tests/test_arch_epic_auto.py`: phrase cases (`argon` → agy /
  `gemini-4-argon` / `high` / `preference_default`; `gemini 4 argon low`;
  `gemini-4-argon-medium`; `gemini flash high` → `gemini-3.8-flash`; `agy`;
  `antigravity agent argon high` → agy). Failure cases: `argon xhigh`,
  `argon max`, `agy opus high`, `cursor agent argon`, `gemini 4.5 argon`, two
  effort words. Also discovery fixtures (real `agy models` text, a failed
  command, changed output), `agy_model_args`, a role policy with `same as`, and
  the arch-epic argv and parser cases against captured events (success, ERROR
  result, missing result, empty response, schema `structured_output`).
- `skills/stepwise/scripts/test_run_stepwise.py`: an `AgyInvocationFlags` class
  for spawn, resume, diagnose, and critic argv, plus agy parse tests.

# Part 2: agy as a place our skills run

- **Install target.** Add `AGY_SKILLS_DIR ?= $(HOME)/.gemini/config/skills`
  with `agy_install_skill`, `verify_agy_install`, and a `NO_AGY=1` opt-out wired
  into `install` and `verify_install`. Copy the same skill set as Gemini CLI
  (`GEMINI_SKILLS`, which leaves out `pr-review-followthrough` and
  `agent-history`) plus `_shared`, and strip build internals, the way the Gemini
  target does. Following the Hermes rule, install only where agy already exists
  (`~/.gemini/antigravity-cli/` is present) and print `SKIP` elsewhere, so
  machines without agy are untouched.
  - The other option is to write `~/.gemini/config/skills.json` pointing at
    `~/.agents/skills`. It worked in the probe with no copying, but it would
    also load every other package in that folder (110 skills), and it means the
    Makefile edits a config file Amir owns. I chose the copy because every other
    target works that way and `verify_*` can check it.
  - Before shipping, confirm the global root with one skill: copy it into
    `~/.gemini/config/skills/`, run `agy -p` from a plain folder, and check that
    the skill is listed. The probe proved discovery at workspace level, and the
    global path comes from agy's bundled docs, not from a run.
- **Tests:** add `tests/test_agy_install.py`, modeled on
  `tests/test_hermes_install.py` (a temp HOME with and without the agy folder),
  and add the agy target to the loops in `tests/test_shared_policy_install.py`
  and `tests/test_vendored_skill_install_inventory.py`.
- **Native-child facts:** add an "Antigravity CLI" column to the matrix in
  `skills/_shared/native-child-capabilities.md`, with a provenance line:
  - Pin model: tier only (`inherit | flash_lite | flash | pro`), no exact id.
    An exact model therefore needs the external lane.
  - Pin effort: not offered.
  - Cross-provider child: no.
  - Starting context: clean.
  - Resume: `send_message` to the child's `conversationId`.
  - Isolation: `Workspace` `inherit | branch | share`.
  - Child fan-out: off unless `enable_subagent_tools` is set.
  - Concurrency: verify on a real spawn before recording a number.
- **Orchestration policy:** add a short agy paragraph to "Map context to the
  active host" in `skills/_shared/agent-orchestration-policy.md`. A native child
  is `invoke_subagent` with `Model: inherit`, which is the default dispatch for
  an Argon parent. A tier pin is not an exact-model pin. `branch` or `share`
  gives real isolation for editful children. Resume goes to the same
  `conversationId`.
- **Docs:** README line 3 and the install section ("Codex CLI, Claude Code, and
  Gemini CLI") gain the Antigravity CLI and its install folder. AGENTS.md's
  install sentence gains it too. Keep Amir's uncommitted edits.

# Order of work

1. **Resolver and its tests** (Part 1 A, plus the resolver half of E). Done
   when `python3 -m unittest tests/test_arch_epic_auto.py` passes.
2. **Runner scripts and their tests** (C, plus the script half of E). Done when
   `python3 skills/stepwise/scripts/test_run_stepwise.py` and the arch-epic
   tests pass, and `python3 -m py_compile` passes on both scripts.
3. **Invocation references** (B): `agent-delegate` first, then
   `fresh-consult` and `model-consensus`.
4. **Doctrine and metadata lists** (D). Done when searching for "Kimi" in live
   files finds no runtime list that lacks agy, and each `openai.yaml` matches
   its `SKILL.md`.
5. **agy as a host** (Part 2): the one-skill global-root check, then the
   Makefile target, install tests, native-child column, policy paragraph, and
   docs.
6. **Verification.** Run `python3 -m unittest discover -s tests`, `npx skills
   check`, `make install` and then `make verify_install` (required this time,
   because install behavior changes), and `git diff --check`. Run live smoke
   tests from a scratch folder: one fresh Argon run, one exact resume, one
   critic with `--json-schema`, one `$fresh-consult` with "argon high" from
   Claude Code, and one `agy -p` session that lists our skills. Then a read-only
   review of the diff against this plan.
7. **Rollout** to the other machines with `$amir-publish`. That pushes to the
   public repo, so it waits for Amir's go-ahead.

# Risks

- **One Google account per machine, and Argon needs Ultra.** No AIMgr pooling
  exists for Google accounts, so heavy Argon fan-out can exhaust that account's
  quota. A quota error has to surface as a failed run. Never fall back to Flash
  or to another provider.
- **agy updates itself.** No no-auto-update switch was found. Recording
  `agy --version` per run makes drift visible. The parsers should fail loudly on
  unknown event shapes rather than guess.
- **User hooks run inside agy workers.** The global Orca status hook fires on
  every agy subprocess. That is acceptable, and it is documented the same way as
  for Kimi.
- **Long prompts ride argv.** This is the same operating-system limit as Kimi.
  Add stdin delivery only after the stream-json input shape is documented or
  verified.

# Left for later

- **`$agent-history` for agy.** Conversations are SQLite files under
  `~/.gemini/antigravity-cli/conversations/` whose step payloads are protobuf
  blobs, and prompts are in `history.jsonl`. Reading them needs a decoder, so it
  is its own feature.
- **AIMgr Google accounts.** This belongs in the aimgr repo, not here.
- **Herdr and `$agent-watcher`.** No work: Herdr already knows `agy`.
- **Gemini CLI install.** Unchanged. It keeps `~/.gemini/skills`.

# Implementation result (2026-10-13)

Built as planned, with these changes from review and live runs:

- **Exact resume needs an id check.** `agy --conversation <unknown id>` starts a
  new conversation and still reports `SUCCESS`. Both runners exit 4
  (`UNRECOVERABLE`) when a resumed turn reports any other conversation id, and
  the three invocation references tell the agent to treat that as a failed
  resume. A stepwise diagnostic turn that lands in another conversation writes
  no answer file.
- **A signed-out agy opens a browser.** A headless run on a signed-out agy opens
  the Google sign-in page in the default browser. `discover_agy_models()` now
  fails when `agy models` asks for a sign-in, `check_agy_ready(model)` also
  fails when the catalog lacks the model, and both runners call it before every
  agy launch. The invocation references tell the agent to run `agy models`
  first and stop if it asks for a sign-in.
- **Every headless run skips permission prompts**, critics and consults
  included, matching the Grok and Kimi lanes. The fixed flags live once in
  `AGY_HEADLESS_ARGS`.
- **Resolver hardening.** A version written after the name (`argon 4.5`), other
  Gemini names (`gemini pro`, `flash lite`, `nano`), `composer`, and effort
  words agy does not offer (`minimal`, `none`, `off`) all fail instead of
  quietly running Argon at `high`.
- **Receipts** record `agy --version`, because agy updates itself.
- **Native children.** One Argon parent launched five `flash`-tier children in
  a single call with no queueing; each reported running Gemini 3.8 Flash.

Not changed: `gpt-oss-120b` phrases still resolve to Codex `gpt-6.1-sol`. That
rewrite predates this change; the docs now say only that GPT-OSS never runs
through agy.

# Verification

- `python3 -m unittest discover -s tests`: passed.
- `python3 skills/stepwise/scripts/test_run_stepwise.py`: 56 passed.
- `npx skills check`: passed.
- Live Argon runs at `low` through both runners and the documented commands:
  fresh runs, exact resumes, unknown-id resumes, critics with the real
  StepVerdict and EpicVerdict schemas, and one subagent fan-out.
- Global skill root: a probe skill in `~/.gemini/config/skills/` was listed by
  `agy` from a plain folder before the real install.
- A clean read-only review of the whole change found no failure in the runner
  argv, parsing, resume checks, or exit codes; its resolver, sign-in, and
  diagnostic findings are the fixes listed above.

# Sources

- [Gemini 4 Argon in Google Antigravity](https://antigravity.google/blog/gemini-4-argon-in-google-antigravity/)
- [9to5Google: Gemini app rolling out Gemini 4 Argon](https://9to5google.com/2026/10/13/gemini-app-4-argon/)
- [Android Developers Blog: Argon in the Antigravity CLI](https://android-developers.googleblog.com/2026/10/bringing-gemini-4-argon-to-android-agentic-engineering-antigravity-cli.html)
- [Antigravity CLI features](https://antigravity.google/docs/cli/features)
- [Antigravity CLI cheat sheet (third party)](https://computingforgeeks.com/antigravity-cli-cheat-sheet/)
- [antigravity-cli issue #76: print mode with piped stdout](https://github.com/google-antigravity/antigravity-cli/issues/76)
- Local: `agy --help`, `agy models`, `agy changelog` (1.3.4), bundled docs in
  `~/.gemini/antigravity-cli/builtin/skills/agy-customizations/`, and the probe
  runs described above.
