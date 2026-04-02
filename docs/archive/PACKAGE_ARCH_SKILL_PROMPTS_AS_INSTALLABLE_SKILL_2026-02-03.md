---
title: "arch_skill — Package prompts as installable Codex skill — Architecture Plan"
date: 2026-02-03
status: draft
owners: [Amir]
reviewers: []
doc_type: phased_refactor
related:
  - docs/WRITING_SKILLS.md
  - docs/custom_prompts.md
  - docs/arch_skill_usage_guide.md
  - Makefile
---

# TL;DR

- **Outcome:** Running `make install` (and `make remote_install HOST=...`) consistently installs arch_skill prompts/templates **and** a Codex skill that routes to prompt markdown on demand (no duplication), with a clear verification checklist.
- **Problem:** Today, arch_skill is distributed primarily as `/prompts:*` markdown copied into `~/.codex/prompts/`; there’s no installable Codex skill “router” layer, and the current remote install flow is easy to drift because it depends on what’s already in `~/.codex/` on the source machine.
- **Approach:** Add a minimal `skills/<skill>/SKILL.md` that encodes routing + invariants (progressive disclosure), keep prompt bodies as SSOT, update Make targets (local + remote) to sync from the repo, and document the contract (including how `$ARGUMENTS` behaves when reading prompt files directly).
- **Plan:** (1) Define skill contract + prompt index, (2) add skill directory + resources, (3) update Makefile install/remote_install, (4) add docs + verification steps, (5) dry-run locally + on a remote host.
- **Non-negotiables:**
  - Prompts remain the **single source of truth**; no copy/paste duplication of prompt bodies into `SKILL.md`.
  - Skill is a **router + invariants layer**, not a replacement for `/prompts:*`.
  - If the skill reads prompt files directly, it must define a clear placeholder-binding contract (no magical `$ARGUMENTS` expansion).
  - `make install` and `make remote_install` must be **idempotent** and sync from this repo (not from whatever happens to be in `~/.codex/`).

---

<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: done 2026-02-03
external_research_grounding: not started
deep_dive_pass_2: not started
recommended_flow: deep dive -> external research grounding -> deep dive again -> phase plan -> implement
note: This is a warn-first checklist only. It should not hard-block execution.
-->
<!-- arch_skill:block:planning_passes:end -->

---

# 0) Holistic North Star

## 0.1 The claim (falsifiable)
> If we package arch_skill as (a) installable prompts/templates and (b) an installable Codex skill that routes to prompt markdown on demand, then a developer can set up (or sync) a machine with a single `make install`/`make remote_install` and reliably get the same `/prompts:*` catalog plus the “router” behavior — validated by Codex showing the prompts after restart and the skill being present under `~/.codex/skills/`, without duplicating prompt bodies.

## 0.2 In scope
- UX surfaces (what users will see change):
  - Codex CLI/IDE: `/prompts:*` commands continue to show up and behave the same after install.
  - Codex behavior: an optional “arch-skill” router skill exists to guide users toward the right prompt/workflow.
- Technical scope (what code will change):
  - Add a skill directory in-repo (e.g., `skills/arch-skill/` with `SKILL.md` + `resources/`).
  - Update `Makefile` to install/sync the skill alongside prompts and templates (local + remote).
  - Update documentation in `README.md` and/or `docs/arch_skill_usage_guide.md` explaining prompts vs skill and the routing contract.

## 0.3 Out of scope
- UX surfaces (what users must NOT see change):
  - No breaking changes to existing prompt names (e.g. `arch-new`, `arch-implement`, `arch-qa-autotest`).
  - No new workflow bureaucracy; the “arch flow” remains prompt-driven.
- Technical scope (explicit exclusions):
  - No rewrite of prompt content (beyond small safety/clarity edits if needed).
  - No new external tooling/packaging system unless required (keep it Makefile + filesystem copies).
  - No changes to Codex CLI itself; we only change what we install under `~/.codex/`.

## 0.4 Definition of done (acceptance evidence)
- Local install:
  - Running `make install` installs:
    - prompts → `~/.codex/prompts/`
    - templates → `~/.codex/templates/arch_skill/`
    - skill → `~/.codex/skills/<skill-name>/`
  - After restarting Codex, `/prompts:arch-*` commands appear as before.
- Remote install:
  - Running `make remote_install HOST=<user@host>` installs the same three buckets on the remote host, syncing from this repo (not relying on pre-existing `~/.codex/*` on the source machine).
- Skill contract is explicit and documented:
  - If the skill reads prompt markdown directly, it defines how to interpret placeholders like `$ARGUMENTS` (no assumption of Codex prompt expansion unless invoked via `/prompts:*`).

Evidence plan (common-sense; non-blocking):
  - Primary signal: manual checklist in docs + spot-check file presence (`ls ~/.codex/prompts`, `ls ~/.codex/skills/<skill>`) and prompt visibility after restart.
  - Optional second signal: a `make verify_install` target that checks expected files exist after install.

## 0.5 Key invariants (fix immediately if violated)
- **No duplication:** `SKILL.md` must not embed full prompt bodies; prompts remain SSOT.
- **Explicit binding:** if the skill reads prompt files directly, it must specify how `$ARGUMENTS`/named args are interpreted.
- **Idempotent installs:** both local and remote installs should overwrite/update cleanly and avoid stale shadow copies.
- **Predictable sync source:** remote install must sync from repo paths (not from “whatever is installed locally”).

---

# 1) Key Design Considerations (what matters most)

## 1.1 Priorities (ranked)
1) Zero duplication + low drift (prompts remain SSOT; skill is routing only)
2) Installation reliability (local + remote; sync from repo)
3) Minimal cognitive overhead (keep current `/prompts:*` UX; skill is optional)

## 1.2 Constraints
- Correctness: prompt behavior must not regress; avoid silent mismatch between local/remote installs.
- Performance: keep SKILL.md small; leverage progressive disclosure (load resources only when needed).
- Compatibility / migration: preserve existing prompt names and installed paths.
- Operational / observability: install should be debuggable by checking filesystem paths.

## 1.3 Architectural principles (rules we will enforce)
- Prefer **composition** (skill routes to prompt markdown) over embedding/re-encoding workflows.
- Prefer **one canonical source** for instructions (prompts) and keep the skill as a small index + guardrails.

## 1.4 Known tradeoffs (explicit)
- Routing via reading markdown files directly is more autonomous, but lacks Codex’s automatic `$ARGUMENTS` expansion; we’ll mitigate by defining a binding contract.
- For remote install, syncing from repo is more deterministic than syncing from `~/.codex/`, but requires the repo to be available on the source machine (which is already true for `make remote_install` usage).

---

# 2) Problem Statement (existing architecture + why change)

## 2.1 What exists today
- This repo is primarily a **prompt library** (`prompts/*.md`) plus a small HTML template (`templates/*.html`).
- Install path today:
  - `make install` copies prompts → `~/.codex/prompts/` and templates → `~/.codex/templates/arch_skill/`.
  - `make remote_install HOST=<user@host>` SSHes to the host and SCPs prompts/templates, but currently sources prompt files from the local machine’s `~/.codex/prompts/` (not directly from this repo).
- Usage is intentionally prompt-driven:
  - Users invoke `/prompts:arch-*` and follow the regular/mini flow described in `docs/arch_skill_usage_guide.md`.

## 2.2 What’s broken / missing (concrete)
- There is no installable Codex skill that encodes the “router + invariants” layer (SSOT doc, question policy, flow selection).
- Remote install is drift-prone:
  - It depends on what prompt files happen to already exist under local `~/.codex/prompts/` rather than syncing from the repo sources.
- There’s no documented “binding contract” for using prompt markdown *as a procedure*:
  - Codex placeholder expansion (`$ARGUMENTS`, named args) happens when invoking `/prompts:*`, not when reading a `.md` file directly.
  - If the skill is expected to “load prompt markdown dynamically”, we must explicitly define how that binding works to avoid confusion.

## 2.3 Constraints implied by the problem
- Prompts must continue to be installed “as-is” and invoked the same way (this is a parallel mechanism, not a replacement).
- The skill must remain minimal and avoid prompt duplication (prompts remain SSOT).
- The installation mechanism must be deterministic and easy to debug by checking filesystem paths.

---

<!-- arch_skill:block:research_grounding:start -->
# 3) Research Grounding (external + internal “ground truth”)

## 3.1 External anchors (papers, systems, prior art)
- `docs/custom_prompts.md` (OpenAI Codex docs copy) — **adopt**: prompts live under `~/.codex/prompts/` and require explicit invocation; “if you want to share a prompt (or want Codex to implicitly invoke it), use skills” — this is the core motivation for adding a skill.
- `docs/WRITING_SKILLS.md` — **adopt**: skills are small, high-signal, and rely on progressive disclosure; Codex CLI skill location: `.codex/skills/` (project) and `~/.codex/skills/` (user) — informs where `make install` should copy.
- Agent Skills spec (referenced in `docs/WRITING_SKILLS.md`) — **adopt**: `SKILL.md` frontmatter + optional `resources/` / `scripts/` layout; use the skill as an index/router rather than embedding large bodies.

## 3.2 Internal ground truth (code as spec)
- Authoritative behavior anchors (do not reinvent):
  - `Makefile` — defines current local install (`make install`) and remote install (`make remote_install`) behavior, including current drift risks (remote copies from local `~/.codex/prompts/*` globs).
  - `prompts/` — authoritative prompt content; this remains the single source of truth for the prompt “procedures”.
  - `templates/arch_doc_template.html` — the only template currently installed; prompts depend on `~/.codex/templates/arch_skill/`.
- Existing patterns to reuse:
  - Local Codex skill layout examples (e.g. `~/.codex/skills/terminal-context/`) — minimal `SKILL.md` plus optional `scripts/` and `references/` (analogous to `resources/` in the writing guide).
  - Prompt taxonomy conventions in this repo (`arch-*`, `*-agent`, `north-star-*`, `maestro-*`, `qa-*`) — use the same naming scheme in the skill’s prompt index/router.

## 3.3 Open questions (evidence-based)
- Should the skill assume prompts are installed under `~/.codex/prompts/` (recommended, since prompts are still installed in parallel) or embed/copy prompt files under the skill (self-contained but higher drift risk)?
  - Evidence: current workflow explicitly installs prompts; “parallel mechanism” requirement suggests we can safely depend on prompts being present.
- What is the binding contract when the skill “loads prompt markdown on demand”?
  - Option A: skill routes users to invoke `/prompts:<name>` (Codex expands `$ARGUMENTS` automatically).
  - Option B: skill reads prompt files directly and defines: `$ARGUMENTS = user’s current request text`, ignore YAML frontmatter, and treat named placeholders as “ask if missing”.
- Should `make remote_install` sync from repo sources (`prompts/*.md`, `templates/*.html`, `skills/...`) rather than from local `~/.codex/*` state?
  - Evidence: current `remote_install` globs local installed prompts, which can be stale or incomplete if `make install` wasn’t run first.
<!-- arch_skill:block:research_grounding:end -->

---

<!-- arch_skill:block:current_architecture:start -->
# 4) Current Architecture (as-is)

## 4.1 On-disk structure
```text
arch_skill/
  Makefile
  prompts/
    arch-*.md
    north-star-*.md
    maestro-*.md
    qa-*.md
  templates/
    arch_doc_template.html
  docs/
    arch_skill_usage_guide.md
    WRITING_SKILLS.md
    custom_prompts.md
```

## 4.2 Control paths (runtime)
- Local install:
  - `make install` → copies `prompts/*.md` to `~/.codex/prompts/` and `templates/*.html` to `~/.codex/templates/arch_skill/`.
- Remote install:
  - `make remote_install HOST=...` → ensures dirs exist on remote, then SCPs prompt files and templates.
  - Current source of truth for remote prompts is the local machine’s `~/.codex/prompts/*` (not the repo), which creates drift.

## 4.3 Object model + key abstractions
- Artifacts:
  - “Prompts” (`~/.codex/prompts/*.md`) — explicitly invoked via `/prompts:*` and support placeholder expansion (`$ARGUMENTS`, named args) at invocation time.
  - “Templates” (`~/.codex/templates/arch_skill/*.html`) — consumed by some prompts for HTML output.
- Naming schema (implicit contract):
  - `arch-*` are the primary workflow prompts; `*-agent` variants bias toward subagents/parallelism.

## 4.4 Observability + failure behavior today
- Primary failure mode: a machine’s `~/.codex/prompts/` is stale (prompt content diverges between machines).
- Remote install can appear “successful” while silently copying an incomplete set if the local `~/.codex/prompts/` was never updated from this repo.

## 4.5 UI surfaces (ASCII mockups, if UI work)
N/A (this is a distribution/installation change, not a UI change).
<!-- arch_skill:block:current_architecture:end -->

---

<!-- arch_skill:block:target_architecture:start -->
# 5) Target Architecture (to-be)

## 5.1 On-disk structure (future)
```text
arch_skill/
  Makefile
  prompts/                      # unchanged (SSOT for procedures)
  templates/                    # unchanged
  skills/
    arch-skill/
      SKILL.md                  # router + invariants (small)
      resources/
        PROMPT_INDEX.md         # mapping + usage notes (no duplication)
        BINDING_CONTRACT.md     # how "$ARGUMENTS" works when reading prompt files
  docs/                         # updated to explain prompts vs skill
```

## 5.2 Control paths (future)
- Local install (idempotent):
  - `make install` installs prompts + templates (as-is) **and** installs the skill to `~/.codex/skills/arch-skill/`.
- Remote install (deterministic):
  - `make remote_install HOST=...` SCPs prompts/templates/skill **from the repo sources**, not from local `~/.codex/*`.
- Optional verification:
  - `make verify_install` checks expected installed files exist.

## 5.3 Object model + abstractions (future)
- New artifact: “Router skill”
  - Purpose: encode the invariant workflow rules and route users/agent to the right prompt procedure on demand.
  - Mechanism: open/read the relevant prompt markdown (or instruct `/prompts:<name>`), without duplicating prompt bodies.
- Explicit contracts:
  - Prompts remain SSOT; the skill references them by name/path.
  - Binding contract is explicit when reading prompt markdown directly (no assumption of Codex prompt expansion).

## 5.4 Invariants and boundaries
- Fail-loud boundaries:
  - If the skill is asked to “follow a prompt procedure” but the prompt file is missing, it should explicitly say the prompts aren’t installed and point to `make install`.
- Single source of truth:
  - Prompt bodies live only in `prompts/` (and installed copy under `~/.codex/prompts/`); skill only indexes/routes.
- Installation determinism:
  - Remote install must sync from repo, not from local installed state.

## 5.5 UI surfaces (ASCII mockups, if UI work)
N/A.
<!-- arch_skill:block:target_architecture:end -->

---

<!-- arch_skill:block:call_site_audit:start -->
# 6) Call-Site Audit (exhaustive change inventory)

## 6.1 Change map (table)
| Area | File | Symbol / Call site | Current behavior | Required change | Why | New API / contract | Tests impacted |
| ---- | ---- | ------------------ | ---------------- | --------------- | --- | ------------------ | -------------- |
| Install | `Makefile` | `install` target | Copies prompts + templates only | Add `install_skill` and make `install` call it (parallel mechanism) | Skill must be installable via Makefile | `~/.codex/skills/arch-skill/` is installed | N/A |
| Remote install | `Makefile` | `remote_install` target | Copies prompts from local `~/.codex/prompts/*` globs | Copy from repo `prompts/*.md` and add skill sync | Deterministic, no drift | Remote host matches repo | N/A |
| Skill | `skills/arch-skill/SKILL.md` | new | N/A | Add router + invariants (small) | Enable progressive disclosure + implicit routing | Defines routing + binding contract | N/A |
| Skill resources | `skills/arch-skill/resources/PROMPT_INDEX.md` | new | N/A | Index prompt families + intended use | Avoid duplicating prompt bodies in SKILL.md | “Where to go next” mapping | N/A |
| Skill resources | `skills/arch-skill/resources/BINDING_CONTRACT.md` | new | N/A | Define `$ARGUMENTS`/named args behavior when reading prompt files | Prevent ambiguity/confusion | Explicit placeholder-binding rules | N/A |
| Docs | `README.md` | Install section | Mentions prompts/templates only | Document prompts + templates + skill install (parallel) | Reduce setup confusion | “prompts vs skill” explanation | N/A |
| Docs | `docs/arch_skill_usage_guide.md` | Setup section | Prompt-centric setup | Add short note about optional router skill | Keep the primary workflow prompt-driven | Skill is guidance layer | N/A |

## 6.2 Migration notes
- Deprecated APIs: N/A (new packaging only)
- Compatibility shims: N/A (skill is additive; prompts unchanged)
- Delete list: none (do not delete or rename prompts)

## 6.3 Pattern Consolidation Sweep (anti-blinders; scoped by plan)
| Area | File / Symbol | Pattern to adopt | Why (drift prevented) | Proposed scope (include/defer/exclude) |
| ---- | ------------- | ---------------- | ---------------------- | ------------------------------------- |
| Remote sync | `Makefile:remote_install` | “sync from repo sources” | Avoids local-state drift | include |
| Local install | `Makefile` | split into `install_prompts`, `install_templates`, `install_skill` | Clear install contract; easier verify | include |
| Safety | `prompts/arch-new.md` | guard for empty `$ARGUMENTS` (ask + stop) | Prevents empty-intent runs | defer (nice-to-have) |
<!-- arch_skill:block:call_site_audit:end -->
