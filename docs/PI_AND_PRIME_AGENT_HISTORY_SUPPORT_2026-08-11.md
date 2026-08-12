---
title: "Pi and Prime Agent History Support for `agent-history` — Implementation Plan"
date: 2026-08-11
status: complete
owners: [aelaguiz]
doc_type: skill_extension
related:
  - skills/agent-history/SKILL.md
  - skills/agent-history/references/storage-map.md
  - skills/agent-history/references/helper-script.md
  - skills/agent-history/scripts/agent_history.py
  - skills/agent-history/scripts/test_agent_history.py
  - docs/PRIME_AGENT_VIA_AIM_DISPATCH_SUPPORT_FOR_AGENT_SKILLS_2026-08-11.md
  - ~/.pi/agent (Pi local home)
  - ~/.prime/agent (Prime Agent local home)
---

# TL;DR

- **Outcome:** `$agent-history` gains two more searchable runtimes — `pi` and `prime` — so
  "what did I ask Prime last night", "which prime session touched psagentspace today", and
  "what did the child agent report back" are answerable from local session stores, with the
  same evidence/confidence contract the skill already uses for Codex and Claude Code.
- **Problem:** The skill is hard-wired to two runtimes. `--runtime` accepts only
  `codex|claude` (`scripts/agent_history.py:1068`), dispatch has exactly two branches
  (`:977-982`), and `references/storage-map.md` documents only those two stores. Meanwhile
  this machine holds **319 Prime sessions** and **78 Pi sessions** that no skill can read,
  including 165 Prime roots with child-agent transcripts.
- **Approach:** One shared parser for both, because Pi and Prime write the **same
  `version: 3` session-event schema**; they differ only in on-disk layout and in Prime's
  extra child-agent artifacts. Add two layout adapters, two CLI runtimes, two home flags,
  deterministic tests, and the reference/doctrine updates. **No new commands, no new
  dependencies, no new skill package, no install changes.**
- **Skill authoring contract:** Every edit under `skills/agent-history/` runs through
  `$skill-authoring`, then `npx skills check`. Helper behavior is proven by unit tests, not
  by doctrine-wording assertions (repo red line).
- **Ground truth:** Store layouts, event schemas, session counts, and the absent stores were
  probe-verified live on this machine on 2026-08-11 and are recorded below. Two facts drive
  most of the design: **neither runtime has a `history.jsonl` or SQLite store**, and **Prime
  session files reach 21 MB**, so a cheap first-line prefilter is mandatory.

# North Star

A user in any host can say "what was I doing in prime today", "find where the prime child
agent pushed back", or "what prompt did I give pi in lessons_studio in June", and the skill
resolves runtime → scope → window, runs the bundled helper against the right home, and
answers with session ids, timestamps, cwd, source paths, short evidence, and honest
confidence labels — including saying plainly when a compaction ate the turns being asked about.

Success looks like:

- `agent_history.py sessions --runtime prime --since 24h` lists today's Prime sessions for
  the current project, scoped by the header `cwd`, in under a few seconds despite multi-MB
  transcripts.
- `agent_history.py prompts --runtime pi --scope all-projects --since 2026-05-01` returns Pi
  user prompts across the per-project session directories, ignoring extension debug files.
- `agent_history.py search --runtime prime --include-sidechains "worktree"` reaches child
  (`sub-*`) transcripts and the parent's `agent_message` relays.
- `goals --runtime prime` returns an honest `NO_MATCH` naming the searched stores, because no
  goal store exists — not a silent empty result.
- Codex and Claude behavior is byte-for-byte unchanged; the existing 4 tests still pass.

# Verified ground truth (2026-08-11, this machine)

## Shared session-event schema (Pi and Prime are the same format)

Both write newline-delimited JSON, one event per line, `type` as the discriminator, with
events chained by `id` / `parentId`.

Header (always line 1, verified on all 319 Prime files and the Pi samples):

```json
{"type":"session","version":3,"id":"<uuid>","timestamp":"<ISO8601>","cwd":"<abs path>","rlmDepth":0,"git":{"repoUrl":"...","commit":"...","branch":"..."}}
```

`rlmDepth` and `git` are **Prime-only extras** — the Pi headers observed carry only
`type`, `version`, `id`, `timestamp`, `cwd`. Treat both as optional.

Event `type` values observed, with counts from one live 21 MB Prime session:

| `type` | count | evidence value |
| --- | --- | --- |
| `message` | 1996 | the transcript. `message.role` ∈ `user` \| `assistant` \| `toolResult`; `message.content` blocks ∈ `text` \| `thinking` \| `toolCall` \| `image`; `message.timestamp` is epoch ms |
| `child_usage_attributed` | 923 | token/cost accounting for child agents — noise, not evidence |
| `custom_message` | 41 | `customType: "agent_message"` — agent-to-agent relay carrying `[from child:<name>]`, source/target session ids, and the child's verdict text |
| `agent_status` | 24 | `status.taskState` (e.g. `needs_input`), `summary`, `basedOnMessageCount` |
| `compaction` | 6 | `summary` replacing earlier turns — proof that context was dropped |
| `custom` | 4 | `customType` + `data`; observed `aimgr.session-identity` (auto title, color), extension state, and per the dispatch plan `aimgr_credential_binding_v1` (provider + account label) |
| `session_info` | 1 | `name` — the auto title |
| `model_change` | 1 | `provider`, `modelId` (observed `openai-codex` / `gpt-5.6-sol`) |
| `thinking_level_change` | 1 | `thinkingLevel` |
| `service_tier_change` | 1 | `serviceTier` |
| `session_state` | 1 | `state.status` |

Note the schema difference from Claude Code: **`toolResult` is a message *role*, not a
content block**, and `thinking` / `toolCall` are content blocks. The existing
`content_to_text` helper (`agent_history.py:225`) must be extended rather than reused as-is.

## Prime store (`~/.prime/agent/`)

- `sessions/<uuid>.jsonl` — **flat**, 319 files, 0 subdirectories. Every first line parsed
  as a valid `type: session` header; all `version: 3`; `rlmDepth` 0 on 312 files and 1 on 7.
- File sizes reach **21 MB** (largest observed). Full-scanning every file per query is not
  viable.
- Header `cwd` distribution confirms project scoping works: `psagentspace` 233,
  `aimgr` 41, `logan` 8, `arch_skill` 5, `puzzledb` 5.
- `session-artifacts/<root-session-id>/` — 324 directories. Contains:
  - `rlm-subagents.jsonl` (present in **165** roots) — the child index. One line per child:

    ```json
    {"type":"rlm_subagent","childId":"sub-39fd0823","sessionName":"impl-wait-onboarding-plan-lo","sessionDir":"…/sub-39fd0823","sessionFile":"…/sub-39fd0823/<child-uuid>.jsonl","parentSessionId":"<root-uuid>","parentSessionFile":"~/.prime/agent/sessions/<root-uuid>.jsonl","rlmDepth":1,"rlmMaxDepth":1,"rlmParentNodeId":"sub-39fd0823","prompt":"Role: You own the implementation and test pass for …"}
    ```

  - `sub-<childId>/<child-uuid>.jsonl` — the child transcript, same schema.
  - `kernel-state.json`, `kernel-state.dill` (38 MB), `scheduled-jobs.json`, `harness/`,
    and a **nested** `session-artifacts/` directory (162 entries observed).
- `logs/` — 517 entries: `agent.jsonl`, `daemon.sock.<hash>.log`,
  `worker-<id>-<id>.sock.<hash>.log`.
- `session-leases/<sha256>.lock` — 177 entries. `daemon-workers/` — 31 entries.
- Config/credentials: `auth.json`, `settings.json`, `telemetry.json`,
  `prime-inference-private-models.json`, plus `skills/`, `extensions/`, `harness/`,
  `kernel-venv/`.

## Pi store (`~/.pi/agent/`)

- `sessions/--<encoded-abs-cwd>--/<ISO-basic>_<uuid>.jsonl` — **per-project directories**,
  70 of them, 0 flat files, 78 session files, spanning 2026-03-26 → 2026-08-09.
  - Example: `/Users/aelaguiz/workspace/lessons_studio` →
    `--Users-aelaguiz-workspace-lessons_studio--`; leading and trailing `--`, `/` → `-`,
    underscores preserved. The encoding is **lossy** (a literal `-` in a path collides), so
    the directory name is a hint and the header `cwd` is truth — the same rule the skill
    already applies to Claude project keys.
  - Filename carries a second timestamp and a second uuid:
    `2026-06-12T20-46-27-706Z_019ebd96-0b79-74a1-a46f-b2ce2ec9e674.jsonl`.
- **Noise lives in the same directories.** Extension artifacts `<name>-debug.jsonl` (984 KB
  observed) and `<name>-state.json` sit beside real sessions. The debug JSONL is keyed
  `event` / `at` / `diagnosticVersion` — no `type` field at all. A naive `*.jsonl` glob
  ingests ~556 junk records per file. A parallel fallback store exists at
  `~/.pi/agent/<extension-name>-diagnostics/--<encoded-cwd>--.jsonl`.
- No `session-artifacts/`, no `logs/`, no daemon directories → **no child-agent transcripts
  exist in the Pi home**.
- Config: `auth.json`, `settings.json`, `mcp.json`, `mcp-cache.json`, `skills/`,
  `extensions/`, `git/`.

## What is absent in both (drives the doctrine)

- **No `history.jsonl`** — verified missing at `~/.pi/agent/history.jsonl` and
  `~/.prime/agent/history.jsonl`. There is no global submitted-prompt recall and no
  cross-project shortcut. Prompts come only from transcript `message` records.
- **No SQLite store** — no Codex-style `state_5.sqlite` equivalent.
- **No goal store observed** — nothing analogous to `thread_goals`.
- **No separate slash-command journal** — slash text appears inline in user message text
  (observed: a user message whose text contains `/skill:revenue-product-tech-panel`).

## Current helper baseline

- `python3 skills/agent-history/scripts/test_agent_history.py` → **Ran 4 tests, OK** (0.31 s).
- `skills/agent-history/` ships `SKILL.md`, three references, and two scripts. **There is no
  `agents/openai.yaml`**, so no runtime-metadata co-edit is required — but the frontmatter
  `description` in `SKILL.md` *is* trigger logic and must be updated.
- Install surface already lists `agent-history` in `Makefile` `SKILLS` and `CLAUDE_SKILLS`;
  no install change is needed.

# Scope

## In scope

### A. Helper script — `skills/agent-history/scripts/agent_history.py`

Exact anchors in the current file:

1. `RunContext` (`:44`) — add `pi_home: Path` and `prime_home: Path`.
2. `add_common_options` (`:1067`) — `--runtime` choices become
   `("codex", "claude", "pi", "prime")`; add `--pi-home` (default `~/.pi`) and
   `--prime-home` (default `~/.prime`) beside the existing home flags.
3. `context_from_args` (`:1004`) — populate the two new homes.
4. `execute_search_command` (`:977-982`) — two new dispatch branches; the error message
   becomes `--runtime must be codex, claude, pi, or prime`.
5. `rebuild_args_for_next_page` (`:991`) — carry non-default home flags into the next-page
   hint so pagination stays correct under `--pi-home` / `--prime-home`.
6. **New collector family**, mirroring the shape of `collect_claude_project_records`
   (`:818`):
   - `pi_session_files(home, ...)` — walk `sessions/*/` one level deep, accept only
     `<ISO>_<uuid>.jsonl`.
   - `prime_session_files(home, include_sidechains, ...)` — glob `sessions/*.jsonl`; when
     sidechains are on, read each relevant root's `session-artifacts/<id>/rlm-subagents.jsonl`
     and follow its `sessionFile` pointers (bounded depth, see decision 7).
   - `collect_session_records(...)` — one shared record walker for the `version: 3` schema,
     used by both, emitting the existing result fields (`id`, `runtime`, `kind`, `source`,
     `confidence`, `timestamp`, `session_id`, `cwd`, `path`, `line`, `role`, `preview`,
     `text_capped`, `context`).
   - `collect_pi(ctx, mode, matcher)` / `collect_prime(ctx, mode, matcher)` — thin wrappers
     that pick the layout adapter and set `runtime`.
7. **Content extraction** — extend `content_to_text` (`:225`) for the block vocabulary
   `text` / `thinking` / `toolCall` / `image` and for `toolResult` as a role.
8. **Mode mapping** for the five existing commands:
   - `sessions` — header line only: session id, timestamp, cwd, `rlmDepth`, git branch,
     plus `session_info.name` and `model_change` when cheaply reachable.
   - `prompts` — `message.role == "user"` text blocks. Confidence `exact`.
   - `commands` — user text whose first non-space character is `/`. Confidence `exact`;
     the reference states there is no separate command journal.
   - `goals` — no store; emit `NO_MATCH` naming the searched sources. Confidence
     `not_found_after_search`.
   - `search` — all message text, `custom_message` content, `compaction` summaries,
     `agent_status` summaries, and `custom` data strings.
9. **New evidence kinds:** `agent_message` (from `custom_message`) and `compaction`.
   Sessions containing compactions must surface that fact so "not found" is reported as
   `best_effort` inside the compacted range rather than as a clean absence.

### B. Tests — `skills/agent-history/scripts/test_agent_history.py`

Add `make_pi_home` / `make_prime_home` builders in the existing
`AgentHistoryScriptTests` style (synthetic homes under a temp root, driven through
`run_tool`). New deterministic tests:

1. Prime `prompts` + `show` drill-down from a flat `<uuid>.jsonl`.
2. Pi `sessions` + `prompts` from a per-project directory, asserting that the **header
   `cwd`**, not the encoded directory name, decides `--scope current-project`.
3. Pi noise exclusion: a `<name>-debug.jsonl` with `event`-keyed lines in the same directory
   produces zero results and zero fatal errors.
4. Prime `--include-sidechains` surfaces a `sub-*` child transcript via
   `rlm-subagents.jsonl`, and does not surface it when the flag is off.
5. Prime `search` finds `custom_message` agent-to-agent text.
6. A malformed line lands in `errors.jsonl` as a recoverable error, not an abort.
7. Regression: `child_usage_attributed` lines never appear in results.

### C. References

- `references/storage-map.md` — new `## Pi` and `## Prime Agent` sections carrying the
  verified ground truth above: layouts, the shared `version: 3` schema table, the encoded
  directory hint rule, the noise-file trap, the child-agent index, the adjacent stores
  (logs, leases, kernel state) marked best-effort, and an explicit "no `history.jsonl`,
  no SQLite, no goal store" subsection so absence is documented, not rediscovered.
- `references/helper-script.md` — `--runtime pi|prime`, the two new home flags, the extended
  `--include-sidechains` meaning, and the new evidence kinds.

### D. `SKILL.md`

- Frontmatter `description` (trigger logic): extend "Codex or Claude Code" to name Pi and
  Prime Agent, and accept the natural-language aliases users will actually say
  (`prime`, `prime agent`, `prime-agent`, `pi`). Keep the field under the 1024-character
  runtime cap.
- Body: runtime defaulting rule gains two answers; When To Use / When Not To Use mention the
  new runtimes; Non-Negotiables gain the read-only credential red line (never read
  `auth.json`, never touch the Prime daemon or its leases).
- Reference Map unchanged in shape.

### E. Repo enumerations

- `README.md:65` and `README.md:281` — the `agent-history` inventory lines say "Codex or
  Claude Code local history"; both gain Pi and Prime.
- `AGENTS.md` — add a Skill Routing line for `$agent-history` if one is still absent at edit
  time (there is none today); otherwise update it.
- `docs/arch_skill_usage_guide.md` — same inventory wording where `agent-history` is
  described.

### F. Verification

`npx skills check`, the unit tests, and a live smoke against the real homes (Phase 5).

## Out of scope (with rationale)

- **Parsing Prime daemon logs, `kernel-state.*`, `scheduled-jobs.json`, and
  `session-leases/`.** Named in the storage map as best-effort adjacent stores so an agent
  knows they exist, but no parser in v1: they are operational state, not conversation
  evidence, and `kernel-state.dill` is a 38 MB pickle.
- **`--runtime all` / cross-runtime unified search.** Genuinely useful and genuinely a
  separate feature — it changes the result schema, dedup rules, and the summary line. Add it
  when someone actually asks a cross-runtime question.
- **Pi child-agent support.** No `session-artifacts/` exists in the Pi home; building for it
  would be speculative. The shared collector makes it a small addition if Pi ever grows one.
- **Any change to `~/workspace/prime-agent`, `~/workspace/pi-mono`, or `~/workspace/aimgr`.**
  The skill reads shipped on-disk formats only.
- **`Makefile` / install changes.** `agent-history` is already installed on the agents/Codex
  and Claude Code surfaces; no new package is created.
- **Doctrine-wording tests.** Red-lined by `AGENTS.md`; `npx skills check` plus review is the
  doctrine gate.
- **Runtime auto-detection inside the helper script.** Host detection is the agent's
  judgment call under `SKILL.md`, not script logic; `--runtime` stays required.

# Phase 0 results (2026-08-11)

All five probes ran. Three changed the design.

1. **Host detection markers — negative result.** Neither Pi nor Prime exports an
   identifying environment variable to child shells (`rg` over
   `prime-agent/packages/coding-agent/src` finds only `PRIME_AGENT_*` build and
   kernel flags; `AI_AGENT=claude-code_2-1-227_agent` here comes from the Claude
   wrapper, not from a shell profile). **Design change:** `SKILL.md` states the
   honest rule instead of a fake env check — the running agent knows its own
   runtime; when genuinely ambiguous, pick the store with recent activity for
   this project and say which was assumed.
2. **Slash commands — better source found.** Only one user message across 141
   sampled sessions began with `/`. The real store is a `custom_message` event
   with `customType: "session_slash_command"`, carrying
   `details.command.{name,args,text}` (plus a `session_slash_command_result`
   sibling). **Design change:** `commands` reads that event *and* user text
   starting with `/`.
3. **Goal-like custom events — none.** Sweep of all `customType` values found no
   goal store, confirming the absence. But `/goal ...` text does appear as
   command evidence, so **design change:** `goals` returns that text (kind
   `goal`) and records "no goal store in this runtime" in `sources.jsonl`,
   rather than the planned bare `NO_MATCH`. The first implementation shipped the
   bare NO_MATCH and was caught by a live smoke that showed `commands` finding
   `/goal` lines the `goals` command denied existed.
4. **Nesting depth — bounded at 2.** Child transcripts sit exactly at
   `session-artifacts/<root>/sub-*/*.jsonl` (2268 files on this machine). Max
   relative depth is 4 but nothing deeper holds a transcript, so a fixed glob
   replaced the planned recursive walk with a depth cap.
5. **Read cost — cheap, but volume is not.** First-line scan of all 324 Prime
   files takes 0.07 s; a full parse of the largest 38 MB file also takes 0.07 s.
   The prefilter stays (it is what makes a scoped query instant), but the real
   hazard turned out to be **output**, not input: one broad
   `search --include-sidechains --since 2d` matched 34,432 records and wrote a
   **110 MB** `results.jsonl`. **Design addition:** a `--max-results` cap
   (default 2000), newest-session-first scan order, and loud reporting when the
   cap bites.

Also catalogued for the storage map: `agent_message`, `heartbeat_prompt`,
`rlm_child_terminal_notice`, `compaction_outcome`, `aimgr_credential_binding_v1`
(provider + account label), `aimgr.session-identity`, and `ipython_state`.

# Phase plan

All edits under `skills/agent-history/` run through `$skill-authoring`. Doc-only edits
(this file, README, AGENTS.md, usage guide) are ordinary edits, re-read after writing.

## Phase 0 — Pin the remaining ground truth (probes only, no edits) — ~30 min

Five bounded probes; everything else is already verified above.

1. **Host detection markers.** This shell reports `AI_AGENT=claude-code_2-1-227_agent` plus
   `CLAUDECODE` / `CLAUDE_CODE_*`. Capture the equivalent markers inside a running Pi and
   Prime session so `SKILL.md` can state a real default-runtime rule instead of a guess.
2. **Slash-command persistence.** Confirm across a sample of sessions that typed slash
   commands survive verbatim in `message.role == "user"` text, and note any that do not.
3. **Goal-like `custom` events.** Sweep `customType` values across all 319 Prime and 78 Pi
   sessions; if a goal-ish custom event exists, `goals` maps to it instead of returning
   `NO_MATCH`.
4. **Nested `session-artifacts/` depth.** Measure the real maximum nesting to set the
   sidechain traversal cap (decision 7).
5. **Read cost.** Time a first-line-only scan of all 319 Prime sessions and a full scan of
   the 21 MB file, to confirm the prefilter design and pick a sane byte cap.

Exit: results appended to this doc under "Phase 0 results".

## Phase 1 — Helper script — ~2-3 hours

Apply section A. Exit: `--runtime pi` and `--runtime prime` work against the real homes;
Codex and Claude paths untouched; the existing 4 tests still pass.

## Phase 2 — Tests — ~1-1.5 hours

Apply section B. Exit: `python3 skills/agent-history/scripts/test_agent_history.py` passes
with the new cases; every new test fails if its guard is removed.

## Phase 3 — References — ~1 hour

Apply section C with `$skill-authoring`. Exit: `npx skills check` passes; the storage map
matches Phase 0 and the verified ground truth verbatim, including the absent stores.

## Phase 4 — `SKILL.md` and enumerations — ~45 min

Apply sections D and E with `$skill-authoring` for the skill package. Exit:
`npx skills check` passes; `rg -n "Codex or Claude Code" README.md AGENTS.md docs/ skills/`
shows every live surface updated or on the out-of-scope list; the frontmatter `description`
is under 1024 characters.

## Phase 5 — End-to-end verification — ~30 min

1. `npx skills check`.
2. `python3 skills/agent-history/scripts/test_agent_history.py`.
3. Live smoke against the real homes:

   ```bash
   python3 skills/agent-history/scripts/agent_history.py sessions --runtime prime --since 24h
   python3 skills/agent-history/scripts/agent_history.py prompts  --runtime prime --scope all-projects --since 7d
   python3 skills/agent-history/scripts/agent_history.py search   --runtime prime --include-sidechains --since 7d worktree
   python3 skills/agent-history/scripts/agent_history.py prompts  --runtime pi --scope all-projects --since 2026-05-01
   python3 skills/agent-history/scripts/agent_history.py goals    --runtime prime --since 7d
   ```

   Expected: real sessions for `psagentspace`/`arch_skill`; Pi prompts from
   `lessons_studio`; child transcripts only with the sidechain flag; `goals` returns a clear
   `NO_MATCH` naming the searched sources.
4. Confirm no run touched `auth.json`, the daemon, or any lease file.
5. Record results in this doc under "Implementation result" and "Verification" before status
   flips to `complete`.

# Design decisions locked

1. **Runtime tokens are `pi` and `prime`** — short, and `prime` matches the dispatch plan's
   `runtime=prime`. `prime-agent` / `prime agent` are natural-language aliases the agent maps
   to `--runtime prime`; the CLI does not add alias choices.
2. **One shared record walker, two layout adapters.** The schemas are identical; only file
   discovery differs. Two copies would drift.
3. **The header `cwd` is project truth.** Pi's encoded directory name is a hint only, because
   the encoding is lossy. This matches the existing Claude project-key rule.
4. **First-line prefilter before any full scan.** Read line 1 of each candidate file, filter
   by `cwd` and time window, and only then walk the body. Non-negotiable given 21 MB files
   and 319 of them.
5. **A file is a session only if the name matches (`<ISO>_<uuid>.jsonl` for Pi,
   `<uuid>.jsonl` for Prime) *and* line 1 parses as `type: "session"`.** Everything else in
   those directories is extension noise and is skipped as an absent/ignored source, not an
   error.
6. **`child_usage_attributed` is excluded from results by default.** It is accounting, 923
   records in a single session, and never answers a history question.
7. **`--include-sidechains` extends to Prime children**, off by default, resolved through
   `rlm-subagents.jsonl` rather than by globbing `session-artifacts/`, with a traversal depth
   cap set by Phase 0 probe 4. The index carries the dispatch `prompt`, which is itself
   high-value evidence.
8. **`custom_message` is a first-class evidence kind (`agent_message`).** Agent-to-agent
   relay is unique to this runtime family and is exactly what "what did the child report"
   asks for.
9. **Compaction is surfaced, never hidden.** A session with `compaction` events downgrades
   absence claims in that range from `not_found_after_search` to `best_effort`.
10. **`goals` returns an honest `NO_MATCH`** naming the searched stores unless Phase 0 probe 3
    finds a goal-like custom event.
11. **Stdlib only, no new commands.** The helper stays a single self-contained Python file
    with the same six commands and the same bounded output contract.
12. **Read-only, credential-blind, daemon-safe.** Never read `auth.json`, never write inside
    `~/.pi` or `~/.prime`, never touch `session-leases/`, `daemon-workers/`, or any
    `prime-agent` lifecycle verb. AIM account labels found inside `custom` events are
    non-secret and may be quoted; tokens never appear anywhere.

# Risks and open questions

- **Read cost on live sessions.** The largest observed Prime transcript is 21 MB and files
  are appended while being read. Mitigations: first-line prefilter (decision 4), a byte cap
  on full scans, and tolerating a truncated final line as a recoverable error. Phase 0 probe
  5 sizes this before implementation.
- **Pi may be dormant.** Last Pi session is 2026-08-09 and the layout is the older
  per-project shape. If Pi is retired, this lane ages out — but it shares the Prime collector,
  so the marginal cost is a file-discovery function and two tests. Accepted.
- **Prime's flat vs Pi's nested layout could converge later.** A future Prime build could
  adopt per-project directories or Pi could adopt flat. Both adapters run off the same
  walker, so convergence is a discovery-function edit, not a rewrite.
- **Headless Prime sessions have filename ≠ header id** (documented in the dispatch plan).
  Results must report the header `id` as the session id and the file path separately, so
  `aim`-side selectors (which match filenames) remain usable.
- **Nested `session-artifacts/<id>/session-artifacts/`** could recurse deeply; the depth cap
  from Phase 0 probe 4 is the guard.
- **Open: host detection for default runtime.** Unverified until Phase 0 probe 1. If no clean
  marker exists, `SKILL.md` states the fallback plainly: infer from which local store has
  recent activity for the current cwd, and say which runtime was assumed.
- **Privacy surface grows.** Prime transcripts embed child dispatch prompts, tool output, and
  images. The skill's existing "quote short, relevant snippets only" rule already covers this
  and is restated in the new storage-map sections.

# Implementation result (2026-08-11)

Shipped. `--runtime pi` and `--runtime prime` work against the real homes.

Changes to `skills/agent-history/scripts/agent_history.py`:

- `RunContext` gained `pi_home`, `prime_home`, `max_results`, and `truncated`;
  new `SessionCandidate` dataclass carries a transcript plus its header, source,
  child label, and parent id.
- New collector family: `session_home`, `session_message_text`,
  `read_session_header`, `file_mtime`, `session_overlaps_window`,
  `pi_session_files`, `prime_session_files`, `prime_subagent_files`,
  `pi_prime_candidates`, `collect_pi_prime_records`, `collect_pi_prime`.
- `session_message_text` is a **new** helper rather than an extension of
  `content_to_text` as originally planned — the block vocabulary
  (`text`/`thinking`/`toolCall`/`image`) and the `toolResult` role differ enough
  from Codex/Claude that sharing the function would have risked a regression in
  two working runtimes for no gain.
- CLI: `--runtime` choices, `--pi-home`, `--prime-home`, `--max-results`;
  dispatch branch; next-page hints now carry non-default home flags.
- Two bounded-output fixes that apply to **all** runtimes: `print_summary`
  dedupes source names (a 300-file no-match line used to print 300 names), and
  the result cap truncates the artifact while saying so.

Tests: `test_agent_history.py` grew from 4 to 12 tests, adding
`make_prime_home` / `make_pi_home` builders and cases for prompts+show, session
metadata (name/model/AIM account/compactions), opt-in sidechains, slash-command
and goal extraction, `agent_message` search, usage-record exclusion, the result
cap, Pi header-cwd-over-directory-name truth, Pi extension-noise exclusion, Pi
scope filtering, and malformed-line recovery.

Docs: `references/storage-map.md` gained a combined Pi/Prime section (layouts,
schema, absent stores, reading traps); `references/helper-script.md` gained the
new runtimes, flags, and runtime notes; `references/retrieval-playbook.md`
gained evidence ordering, example commands, and a Prime child-agent section;
`SKILL.md` gained the runtime triggers, the ambiguity rule, the
no-prompt-store/no-goal-store caveat, and a never-read-`auth.json` red line;
`README.md` and `AGENTS.md` enumerations updated.

Two live-data corrections during implementation, both caught by smoking against
the real homes rather than by the plan:

1. `goals` denied evidence that `commands` was finding (fixed as Phase 0
   item 3).
2. The result cap was silent when it bit mid-file, so a truncated scan looked
   complete. Now the candidate reports truncation upward and the summary says
   `capped at <n>`.

# Verification

Ran 2026-08-11, all passing:

- `python3 skills/agent-history/scripts/test_agent_history.py` → **Ran 12 tests,
  OK** (was 4 before this work; the original 4 still pass unchanged).
- `npx skills check` → `✓ All global skills are up to date`.
- `SKILL.md` frontmatter description: 622 characters, under the 1024 cap.
- Live smoke against the real homes:
  - `sessions --runtime prime --since today` → 2 real sessions with names,
    message counts, model, and AIM account labels (`cfo`, `product_growth`).
  - `prompts --runtime prime --since 24h` → 5 real prompts with file:line.
  - `commands --runtime prime --scope all-projects --since 7d` → 21 hits,
    mixing `/compact` slash events and `/goal` user text.
  - `goals --runtime prime --scope all-projects --since 7d` → 12 `/goal` hits.
  - `search --runtime prime --include-sidechains --since 2d` → reaches child
    transcripts under `session-artifacts/*/sub-*/`; 1113 child sessions
    discovered and labelled from `rlm-subagents.jsonl` (e.g.
    `3538-impl-initial-external`).
  - `sessions --runtime pi --scope all-projects --since 90d` → 58 Pi sessions.
  - `--runtime bogus` → rejected with `choose from codex, claude, pi, prime`.
- Bounded output confirmed: the broad sidechain search that wrote **110 MB**
  before the cap now writes **11 MB** and runs in **0.6 s** instead of 7 s.
- No run read `auth.json`, touched the Prime daemon, or wrote inside `~/.pi` or
  `~/.prime`.

Original plan checks retained:

- After each skill-package phase: `npx skills check`.
- After Phases 1-2: `python3 skills/agent-history/scripts/test_agent_history.py`
  (baseline today: 4 tests, OK).
- Enumeration sweep: `rg -n "Codex or Claude Code|codex or claude" README.md AGENTS.md docs/ skills/`
  and confirm each hit is updated or listed as out of scope.
- Phase 5 live smoke with the five commands above against the real `~/.pi` and `~/.prime`
  homes.
- This doc updated with "Phase 0 results", "Implementation result", and "Verification"
  records before status flips to `complete`.

# References

- `skills/agent-history/scripts/agent_history.py` — current two-runtime helper; edit anchors
  cited by line in section A.
- `skills/agent-history/references/storage-map.md` — the Codex/Claude format precedent the
  new sections mirror.
- `docs/PRIME_AGENT_VIA_AIM_DISPATCH_SUPPORT_FOR_AGENT_SKILLS_2026-08-11.md` — Prime session
  header shape, the filename-vs-header-id quirk, AIM binding receipts, and daemon safety
  rules reused here.
- Probe evidence (2026-08-11, this machine): `~/.prime/agent/sessions/` (319 files,
  all `version: 3`), `~/.prime/agent/session-artifacts/` (324 dirs, 165 with
  `rlm-subagents.jsonl`), `~/.pi/agent/sessions/` (70 project dirs, 78 session files,
  2026-03-26 → 2026-08-09).
