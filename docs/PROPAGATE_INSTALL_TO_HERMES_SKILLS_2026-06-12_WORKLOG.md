# Worklog — Propagate make install to Hermes Agent skill roots

## 2026-06-12 — Phase 1 implementation + proof

- Makefile: added `HERMES_HOME ?=`, `HERMES_SKILLS_SUBDIR := arch_skill`, `NO_HERMES` gate (`INSTALL_HERMES`/`VERIFY_HERMES`), `hermes_install_skill`, `verify_hermes_install`; wired into `install` and `verify_install`; `.PHONY` updated. Targets reuse `SKILLS`/`REMOVED_SKILLS`/`LOCAL_SKILLS`/`VENDORED_SKILLS`/`SHARED_DIRS` directly (no parallel inventory).
- Docs: README.md Install/Verify sections and docs/arch_skill_usage_guide.md Install section document Hermes propagation paths and `NO_HERMES=1`.
- Tests: new `tests/test_hermes_install.py` — 6 tests: install/verify wiring, inventory reuse + prune commands, `NO_HERMES=1` gating via `make -n`, functional fake-home install repairing pre-seeded stale state (removed skills + stray hook script) across default + profile roots, missing-home skip path, fail-loud verify on stale root.
- Proof:
  - `python3 -m pytest tests/ -q` → 49 passed, 3 subtests (43 baseline + 6 new).
  - Real `make install` → `OK: Hermes skills installed to /Users/blake/.hermes/skills/arch_skill`.
  - Real `make verify_install` → all surfaces OK including `OK: Hermes skills verified at /Users/blake/.hermes/skills/arch_skill`.
  - Live root before: contained `arch-loop delay-poll wait code-review`, missing 12 active skills, shipped `arch_controller_stop_hook.py` + 3 `upsert_*hook.py`. After: removed skills gone, all 41 active skills + `_shared` present, only `arch_stage_gate.py` remains under arch-step/scripts.
