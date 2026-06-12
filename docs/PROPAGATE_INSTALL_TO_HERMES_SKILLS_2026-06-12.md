---
title: "arch_skill - Propagate make install to Hermes Agent skill roots - Architecture Plan"
date: 2026-06-12
status: complete
fallback_policy: forbidden
owners: [blake]
reviewers: [amir]
doc_type: architectural_change
related:
  - Makefile (install/verify surface)
  - tests/test_no_arch_skill_hooks_install.py
  - tests/test_vendored_skill_install_inventory.py
---

# TL;DR

- **Outcome**: `make install` propagates the same live skill surface it installs for Codex/agents, Claude Code, and Gemini to every Hermes Agent skill root that exists on the box (`~/.hermes/skills/` plus each `~/.hermes/profiles/<name>/skills/`), under the existing `arch_skill/` category directory, with the same purge/prune discipline. `make verify_install` validates it.
- **Problem**: Hermes skill installs are manual one-off copies today. The live box already shows the failure mode: `~/.hermes/skills/arch_skill/` contains removed skills (`arch-loop`, `delay-poll`, `wait`, `code-review` — the last colliding with another Hermes skill of the same name), is missing ~12 newer skills, and still ships hook scripts that every other install surface prunes.
- **Approach**: Add a `hermes_install_skill` target (plus `verify_hermes_install`) that discovers Hermes roots dynamically, reuses the existing `SKILLS` / `REMOVED_SKILLS` / `LOCAL_SKILLS` / `VENDORED_SKILLS` / `SHARED_DIRS` inventory variables as the single source of truth, and mirrors the exact copy/purge/prune recipe shape already used by `agents_install_skill` / `claude_install_skill`. Gate with `NO_HERMES=1` for symmetry with `NO_GEMINI=1`; silently no-op (with message) on machines without a Hermes home.
- **Plan**: One phase: Makefile targets + wiring, README + usage-guide install docs, new test module (`tests/test_hermes_install.py`) with Makefile-inventory checks plus a functional `make hermes_install_skill HERMES_HOME=<tmp>` test, then a real on-box `make install` + `make verify_install` proof.
- **Non-negotiables**: No second skill inventory list to drift; no hook scripts installed; removed skills purged; non-Hermes machines unaffected; `remote_install` unchanged.

<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: done 2026-06-12 (Makefile install/verify/remote surface, both test modules, live Hermes root inventory on this box)
external_research_grounding: skipped 2026-06-12 (change is local to this repo's Makefile + local box conventions; no external anchors apply)
deep_dive_pass_2: done 2026-06-12 (recipe shape finalized against agents/claude/gemini targets; profile-glob and no-home edge cases resolved)
recommended_flow: deep dive -> external research grounding -> deep dive again -> phase plan -> implement
note: This block tracks stage order only. It never overrides readiness blockers caused by unresolved decisions.
-->
<!-- arch_skill:block:planning_passes:end -->

# 0) Holistic North Star

## 0.1 The claim (falsifiable)

After `make install` on a box with a Hermes home, every existing Hermes skill root (`$HERMES_HOME/skills` and each `$HERMES_HOME/profiles/<name>/skills`) contains exactly the active arch_skill surface under `arch_skill/`: every skill in `SKILLS` present with `SKILL.md`, every skill in `REMOVED_SKILLS` absent, `_shared/` present, and zero `build/`, `prompts/`, `__pycache__/`, `*.pyc`, `upsert_*hook.py`, or `arch_controller_stop_hook.py` artifacts. `make verify_install` fails if any of that is false. On a box with no Hermes home, `make install` and `make verify_install` succeed unchanged.

## 0.2 In scope

- New `hermes_install_skill` and `verify_hermes_install` Makefile targets wired into `install` / `verify_install`.
- Dynamic Hermes root discovery: default profile root plus named profile roots, existing dirs only.
- `NO_HERMES=1` opt-out gate mirroring `NO_GEMINI=1`.
- `HERMES_HOME ?= $(HOME)/.hermes` override variable (enables hermetic functional tests).
- README + `docs/arch_skill_usage_guide.md` install documentation updates.
- New `tests/test_hermes_install.py` (inventory + functional + skip-path coverage).
- Real on-box `make install` / `make verify_install` run as acceptance evidence.

## 0.3 Out of scope

- `remote_install` Hermes propagation (remote hosts get Hermes coverage by running `make install` locally; extending scp/ssh discovery is not requested and would complicate Amir's remote flow).
- Any change to which skills are in the active surface (`SKILLS` inventory unchanged).
- Hermes-side config, curator, manifest, or `.archive` handling — only the skill package directories are owned by this installer.
- Gemini/Claude/agents/codex install behavior changes.

## 0.4 Definition of done (acceptance evidence)

- `python3 -m pytest tests/ -q` passes including the new module.
- Functional test proves: fresh tmp Hermes home with default root + one profile root gets the full surface; pre-seeded stale `arch-loop`/`code-review` dirs and a stray hook script are purged; verify target passes against the result; missing-home path no-ops successfully.
- Real `make install` on this box repairs the stale `~/.hermes/skills/arch_skill/` (removed skills gone, new skills present, hook scripts gone) and `make verify_install` passes end to end.

## 0.5 Key invariants (fix immediately if violated)

- Single inventory source of truth: Hermes targets consume `SKILLS`/`REMOVED_SKILLS`/`LOCAL_SKILLS`/`VENDORED_SKILLS`/`SHARED_DIRS` directly; no `HERMES_SKILLS` parallel list.
- No hook scripts on any installed surface (existing repo-wide invariant; extends to Hermes).
- Install never creates a Hermes home that does not exist; it only populates roots that are already there (profile roots may gain a `skills/` dir, the profile itself must pre-exist).
- Fail-loud verify: missing skill, surviving removed skill, or surviving internals fail `verify_install` with a named path.
- No fallbacks or runtime shims.

# 1) Key Design Considerations (what matters most)

## 1.1 Priorities (ranked)

1. Zero drift between the agents/Claude surface and the Hermes surface (same inventory variables, same prune set).
2. Safe no-op on machines without Hermes (this PR lands in Amir's upstream; his boxes may not run Hermes).
3. Recipe readability consistent with the existing Makefile idiom (duplicated per-surface shell loops, not clever macros).
4. Hermetic testability (`HERMES_HOME` override).

## 1.2 Constraints

- GNU make + POSIX sh recipes, matching the existing file.
- Hermes skill discovery expects `<root>/<category>/<skill>/SKILL.md`; category dir `arch_skill` is already established on this box and groups the suite cleanly.
- Hermes requires globally unique skill names across categories — purging `REMOVED_SKILLS` (esp. `code-review`) is required correctness, not just tidiness.
- Tests must not touch the real `$HOME` surfaces; functional coverage uses `HERMES_HOME=<tmpdir>` and invokes only the Hermes targets.

## 1.3 Architectural principles (rules we will enforce)

- Reuse the canonical inventory variables; never introduce a second skill list for Hermes.
- Mirror the canonical recipe shape (`purge → copy local → copy vendored → copy shared → prune internals`) exactly as `agents_install_skill` does.
- Gate variables (`INSTALL_HERMES`/`VERIFY_HERMES`) follow the existing `NO_GEMINI` pattern verbatim.

## 1.4 Known tradeoffs (explicit)

- Duplicating the discovery loop between install and verify targets (matches the Makefile's existing duplication idiom; a shared `define` macro would be more DRY but foreign to this file's style and harder for upstream review).
- Default-on Hermes install in `install` (auto-skip makes it free on non-Hermes machines; `NO_HERMES=1` exists for explicit opt-out).
- Frontmatter is kept in Hermes SKILL.md copies (unlike Gemini, Hermes parses YAML frontmatter natively — same as agents/Claude surfaces).

# 2) Problem Statement (existing architecture + why change)

## 2.1 What exists today

`make install` fans out to `agents_install_skill` (→ `~/.agents/skills/`), `claude_install_skill` (→ `~/.claude/skills/`), and `gemini_install` (→ `~/.gemini/skills/`, frontmatter stripped), each purging `REMOVED_SKILLS`, copying `LOCAL_SKILLS` + `VENDORED_SKILLS` + `_shared`, and pruning build internals and hook scripts. `verify_install` validates all three. Hermes Agent on this box reads skills from `~/.hermes/skills/` (category subdirs) and per-profile roots under `~/.hermes/profiles/<name>/skills/`, but no installer target serves them.

## 2.2 What's broken / missing (concrete)

`~/.hermes/skills/arch_skill/` is a stale manual copy: it contains `arch-loop`, `delay-poll`, `wait`, and `code-review` (all in `REMOVED_SKILLS`; `code-review` shadows/collides with the separate `software-development/code-review` Hermes skill), lacks `pr-review-followthrough`, `plan-audit`, `plan-implement`, `plan-swarm`, `agent-history` updates, `contact-sheet-builder`, `exhaustive-code-review`, `chatgpt-web`, `flutter-reference`, `stepwise` updates, `codex-cleanup`, and `thermo-nuclear-code-quality-review`, and still ships `arch_controller_stop_hook.py` + `upsert_*hook.py` under `arch-step/scripts/` contrary to the repo's no-hooks install policy.

## 2.3 Constraints implied by the problem

The fix must be part of the same `make install` muscle-memory command, must repair (not just append to) stale Hermes copies, and must be invisible on machines without Hermes.

# 3) Research Grounding (external + internal "ground truth")

## 3.1 External anchors (papers, systems, prior art)

None applicable — rejected by inspection: this is an in-repo installer extension governed entirely by local conventions. The `NO_GEMINI` gate and `agents_install_skill` recipe are the prior art being followed.

## 3.2 Internal ground truth (code as spec)

- `Makefile:87-100` — per-surface dir variables and the `NO_GEMINI` gate pattern (canonical gate shape to copy).
- `Makefile:151-171` (`agents_install_skill`) — canonical copy/purge/prune recipe; the Hermes target mirrors it per discovered root.
- `Makefile:238-258` (`verify_install`, `verify_agents_install`) — canonical verify shape including internals/hook absence checks.
- `tests/test_no_arch_skill_hooks_install.py`, `tests/test_vendored_skill_install_inventory.py` — Makefile-parsing test idiom (`make_var_words`, substring assertions) the new test module follows.
- Live box: `~/.hermes/skills/` exists with category dirs; `~/.hermes/profiles/` does not exist on this box (the profile loop must therefore be proven via the functional test's fake home).
- Canonical owner path: the `install` aggregate target in `Makefile` owns all local surface propagation; Hermes becomes one more leaf of that target.

## 3.3 Decision gaps that must be resolved before implementation

None. All plan-shaping decisions are resolved and logged in Section 10.

# 4) Current Architecture (as-is)

## 4.1 On-disk structure

```
Makefile                      # install/verify/remote targets; inventory vars
skills/<skill>/               # source packages
vendor/cursor/.../skills/     # vendored thermo-nuclear package
tests/test_*.py               # Makefile-contract tests
~/.agents/skills/<skill>/     # installed (flat)
~/.claude/skills/<skill>/     # installed (flat)
~/.gemini/skills/<skill>/     # installed (flat, frontmatter stripped)
~/.hermes/skills/arch_skill/<skill>/   # STALE manual copy, no installer
```

## 4.2 Control paths (runtime)

`make install` → stale-surface cleanup → hook cleanup → `agents_install_skill` → `clean_codex_skill_mirror` → `claude_install_skill` → `gemini_install`. `make verify_install` → per-surface verify targets. Hermes: no path.

## 4.3 Object model + key abstractions

Inventory variables (`SKILLS`, `CLAUDE_SKILLS`, `GEMINI_SKILLS`, `REMOVED_SKILLS`, `SHARED_DIRS`, `LOCAL_*`/`VENDORED_*` filters) are the single source of truth; per-surface targets are pure consumers.

## 4.4 Observability + failure behavior today

Targets echo `OK:` lines; verify targets exit non-zero with `ERROR:` lines on contract violations. Hermes drift is invisible — nothing checks it.

## 4.5 UI surfaces

N/A (no UI work).

# 5) Target Architecture (to-be)

## 5.1 On-disk structure (future)

```
~/.hermes/skills/arch_skill/<skill>/            # default profile root (if box has Hermes)
~/.hermes/profiles/<name>/skills/arch_skill/<skill>/  # each existing named profile
```

Same package contents as `~/.agents/skills/<skill>/` (frontmatter kept, internals and hook scripts pruned), nested under the `arch_skill` category dir.

## 5.2 Control paths (future)

`install: ... $(INSTALL_GEMINI) $(INSTALL_HERMES)` where `INSTALL_HERMES := hermes_install_skill` unless `NO_HERMES=1`. `verify_install: ... $(VERIFY_GEMINI) $(VERIFY_HERMES)`. Each Hermes target: discover roots (existing dirs only) → per root: purge `REMOVED_SKILLS`+`SKILLS` → copy `LOCAL_SKILLS` → copy `VENDORED_SKILLS` → refresh `SHARED_DIRS` → prune internals/hooks → echo OK. Empty discovery: echo skip line, exit 0.

## 5.3 Object model + abstractions (future)

New variables: `HERMES_HOME ?= $(HOME)/.hermes`, `HERMES_SKILLS_SUBDIR := arch_skill`, gate pair `INSTALL_HERMES`/`VERIFY_HERMES`. No new inventory lists. Hermes consumes the agents-surface inventory (`SKILLS`/`LOCAL_SKILLS`/`VENDORED_SKILLS`) directly.

## 5.4 Invariants and boundaries

- Compatibility posture: **pure addition** — existing targets, variables, and outputs unchanged; `install` on a Hermes-less box behaves byte-identically except one skip line. No bridge needed.
- Fail-loud: verify exits non-zero naming the offending path; install uses `set -e` semantics per recipe line.
- The installer owns only `<root>/arch_skill/` package dirs; it never touches sibling categories, Hermes config, or archives.

## 5.5 UI surfaces

N/A.

# 6) Call-Site Audit (exhaustive change inventory)

## 6.1 Change map (table)

- **Makefile / .PHONY** — add `hermes_install_skill verify_hermes_install` — wiring — new targets must be phony.
- **Makefile / vars block (~L87-100)** — add `HERMES_HOME ?=`, `HERMES_SKILLS_SUBDIR :=`, `NO_HERMES` gate (`INSTALL_HERMES`/`VERIFY_HERMES`) — mirrors `NO_GEMINI` — new contract: `NO_HERMES=1` opt-out, `HERMES_HOME=<path>` override.
- **Makefile / `install` (~L102)** — append `$(INSTALL_HERMES)` — propagation entry point.
- **Makefile / new `hermes_install_skill`** — root discovery + per-root copy/purge/prune mirroring `agents_install_skill` — tests impacted: new functional test.
- **Makefile / `verify_install` (~L238)** — append `$(VERIFY_HERMES)`; update summary echo to mention Hermes — keeps verify honest.
- **Makefile / new `verify_hermes_install`** — per-root presence/absence/internals checks mirroring `verify_agents_install` — tests impacted: functional verify run.
- **README.md / Install + verify sections** — document Hermes propagation, `NO_HERMES=1`, paths — doc truth.
- **docs/arch_skill_usage_guide.md / Install section** — same documentation — doc truth.
- **tests/test_hermes_install.py (new)** — inventory wiring assertions + functional fake-home install/verify/skip tests — proof.

## 6.2 Migration notes

- Canonical owner path: `install` aggregate target; Hermes is a peer leaf of agents/claude/gemini targets.
- Delete list: none in-repo; at install time the purge loop deletes `REMOVED_SKILLS` and re-copies `SKILLS` per root (this is the repair mechanism for the stale box copy).
- Adjacent surfaces: `remote_install` explicitly excluded (Section 0.3, Decision Log 2026-06-12); README/usage guide move with the change in the same phase.
- Compatibility: pure addition; no deprecated APIs.
- Behavior preservation: existing targets untouched; baseline test suite (43 tests) must stay green.

# 7) Depth-First Phased Implementation Plan (authoritative)

> Rule: depth-first implementation protects the full destination while proving the path early. Treat TL;DR, Section 0, Sections 5-6, and approved decisions as the destination map. Phase boundaries are proof gates. No fallbacks/runtime shims — the system must work correctly or fail loudly.

<!-- arch_skill:block:phase_plan:start -->

## Phase 1 — Hermes install/verify surface, docs, and tests

Status: COMPLETE

- **Goal**: `make install` / `make verify_install` own Hermes skill-root propagation end to end, proven hermetically and on the real box.
- **Work**: Add the variables, gate, and two targets to the Makefile mirroring the agents recipe per discovered Hermes root; update README and usage guide install docs; add `tests/test_hermes_install.py` with inventory and functional coverage.
- **Checklist (must all be done)**:
  - [x] `HERMES_HOME ?= $(HOME)/.hermes`, `HERMES_SKILLS_SUBDIR := arch_skill`, `NO_HERMES` gate variables added; `.PHONY` updated.
  - [x] `hermes_install_skill` discovers `$(HERMES_HOME)/skills` + existing `$(HERMES_HOME)/profiles/*/skills`, and per root: purges `REMOVED_SKILLS`+`SKILLS`, copies `LOCAL_SKILLS`+`VENDORED_SKILLS`+`SHARED_DIRS`, prunes `build/`/`prompts/`/`__pycache__`/`*.pyc`/`upsert_*hook.py`/`arch_controller_stop_hook.py`; skips with message when no roots exist.
  - [x] `verify_hermes_install` checks per root: every `SKILLS` member has `SKILL.md`, every `REMOVED_SKILLS` member absent, `_shared` markers present, no internals/bytecode/hook scripts; succeeds with message when no roots exist.
  - [x] `install` and `verify_install` wired via `$(INSTALL_HERMES)` / `$(VERIFY_HERMES)`; `verify_install` summary line mentions Hermes.
  - [x] README.md and docs/arch_skill_usage_guide.md document the Hermes surface, paths, and `NO_HERMES=1`.
  - [x] `tests/test_hermes_install.py` added: Makefile wiring assertions; functional fake-home test (default root + one profile root, pre-seeded stale removed-skill dirs and a stray hook script, asserts purge/copy/prune and verify pass); missing-home skip test; `NO_HERMES=1` gating test.
- **Verification (required proof)**: `python3 -m pytest tests/ -q` green (old + new). Real on-box `make install` then `make verify_install` exit 0, and `~/.hermes/skills/arch_skill/` shows removed skills gone, new skills present, hook scripts absent.
- **Docs/comments (propagation; only if needed)**: README + usage guide (in checklist).
- **Exit criteria (all required)**:
  - [x] Full pytest suite green.
  - [x] Functional test proves repair of a stale fake root (removed skills purged, hook script pruned).
  - [x] Real box: `make verify_install` passes and live `~/.hermes/skills/arch_skill/` matches the active surface.
- **Rollback**: revert the single commit; installed Hermes dirs remain but are inert copies (same state as today's manual copy, minus staleness).

Completed work: All checklist items and exit criteria satisfied 2026-06-12. Full suite 49 passed, 3 subtests. Real `make install` + `make verify_install` exit 0; live `~/.hermes/skills/arch_skill/` repaired (4 stale removed skills purged incl. colliding `code-review`, 12 missing skills added, hook scripts pruned). Evidence detail in WORKLOG.

<!-- arch_skill:block:phase_plan:end -->

<!-- arch_skill:block:implementation_audit:start -->
## Implementation Audit — 2026-06-12 (fresh)

Verdict: CLEAN. Phase 1 checklist and exit criteria all validated against live state, not memory:
- `python3 -m pytest tests/ -q` → 49 passed, 3 subtests (43 baseline + 6 new in `tests/test_hermes_install.py`).
- `make verify_install` exits 0 including `verify_hermes_install` on the real box.
- Live `~/.hermes/skills/arch_skill/`: 41 active skills + `_shared` (42 dirs), all `REMOVED_SKILLS` absent, zero hook scripts / `*.pyc` / internals.
- Functional test proves stale-root repair (pre-seeded `arch-loop`, `code-review`, stray `arch_controller_stop_hook.py`) and profile-root coverage hermetically; missing-home path no-ops; `NO_HERMES=1` drops the targets from the `install` plan.
- Docs (README, usage guide) updated in the same change. No scope cuts; no phases reopened.
<!-- arch_skill:block:implementation_audit:end -->

# 8) Verification Strategy (common-sense; non-blocking)

## 8.1 Unit tests (contracts)

Makefile-parsing assertions in `tests/test_hermes_install.py` (same idiom as existing test modules): gate wiring, inventory reuse, prune commands present.

## 8.2 Integration tests (flows)

Functional subprocess tests invoking `make hermes_install_skill HERMES_HOME=<tmp>` and `make verify_hermes_install HERMES_HOME=<tmp>` against a fabricated Hermes home with a default root and one profile root, pre-seeded with stale state; plus the missing-home skip path and `make -n install NO_HERMES=1` gating.

## 8.3 E2E / device tests (realistic)

One real `make install` + `make verify_install` on this box, with before/after inspection of `~/.hermes/skills/arch_skill/`.

# 9) Rollout / Ops / Telemetry

## 9.1 Rollout plan

Single commit on `main`, pushed to `origin` (rblakemesser fork), PR into `amir/main` (aelaguiz/arch_skill). No migration; next `make install` on any box self-heals Hermes roots.

## 9.2 Telemetry changes

None. Install/verify echo lines are the observability surface.

## 9.3 Operational runbook

- Hermes box: `make install` (default). Non-Hermes box: identical command; target self-skips.
- Opt out: `make install NO_HERMES=1`.
- Hermetic test: `make hermes_install_skill HERMES_HOME=/tmp/fake`.
- Restart Hermes sessions after install so the skill index reloads (same guidance as Codex/Claude/Gemini).

# 10) Decision Log (append-only)

## 2026-06-12 - North Star approval and end-to-end authorization

- Context: Blake requested, in one instruction, the design ("thoughtfully"), tests, real install proof, push to `origin main`, and PR into `amir main`, explicitly invoking the arch-step workflow end to end.
- Options: pause after `new` for confirmation vs. treat the instruction as explicit pre-approval.
- Decision: treat the instruction as North Star confirmation; `status: complete`.
- Consequences: full arc executes in this session; this entry records the approval.

## 2026-06-12 - Intent-derived: profile skill roots included in propagation

- Blocker: whether "any possibly existing hermes agents' skills on the box" covers per-profile roots.
- Consulted: user ask; Hermes profile layout (`~/.hermes/profiles/<name>/skills/`).
- Intent says: "any possibly existing" — propagate to every root that exists.
- Decision: include existing profile roots; never create a profile, only populate `skills/` within existing ones. This box has no `profiles/` dir, so the path is proven via the functional fake-home test.
- Consequences: discovery loop + functional test cover both root kinds.

## 2026-06-12 - Default-on with auto-skip; NO_HERMES gate

- Context: PR lands upstream in Amir's repo; his machines may not run Hermes.
- Options: opt-in target only; default-on with auto-skip + opt-out gate.
- Decision: default-on mirroring `NO_GEMINI` (auto-skip makes it free on non-Hermes boxes).
- Consequences: one extra skip line on non-Hermes boxes; symmetric gate surface.

## 2026-06-12 - remote_install excluded

- Context: ask is box-local; `remote_install` is Amir's multi-host scp flow.
- Decision: leave `remote_install` untouched; remote boxes gain Hermes coverage when they run `make install` locally. Documented in 0.3.
- Consequences: smaller upstream diff; revisit only if Amir asks.

## 2026-06-12 - Hook scripts pruned on Hermes surface; frontmatter kept

- Context: repo policy installs no hooks anywhere; Hermes cannot run Codex/Claude stop hooks. Hermes parses YAML frontmatter natively (unlike Gemini).
- Decision: prune `upsert_*hook.py` + `arch_controller_stop_hook.py` exactly like other surfaces; keep frontmatter (agents/Claude treatment, not Gemini's strip).
- Consequences: consistent policy; fixes the stale box copy that still shipped hooks.

## 2026-06-12 - Category dir `arch_skill/` retained; duplication idiom over make macros

- Context: Hermes skills support category subdirs; `arch_skill/` is already the established category on this box and keeps the 41-skill suite grouped. The Makefile's house style duplicates per-surface shell loops.
- Decision: install under `<root>/arch_skill/`; write discovery/copy loops inline per target (no shared `define`), matching existing style for upstream reviewability. Purging `REMOVED_SKILLS` also resolves the live `code-review` name collision with the `software-development` Hermes category.
- Consequences: slightly more repeated make text; consistent with every other target pair.
