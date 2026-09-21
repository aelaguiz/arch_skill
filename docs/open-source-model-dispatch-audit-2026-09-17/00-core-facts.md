# Core facts (root agent, verified 2026-09-17)

## Session reality
- This Prime Agent session's parent model: `openrouter/deepseek/deepseek-v4.1-flash` (OpenRouter, provider routed to Together/Phala/Makora).
- Unpinned native children inherited exactly that model: 4 audit children all admitted with model `openrouter/deepseek/deepseek-v4.1-flash`.

## Prime Agent catalog facts (live, via `rlm.find_models`)
- `~/.prime/agent/models.json` registers custom: anthropic/claude-fable-5-1; openrouter stealth/union-alpha, z-ai/glm-5.3, deepseek/deepseek-v4.1-flash; sakana fugu-max, fugu-ultra-v2.0 (baseUrl https://api.sakana.ai/v1).
- thinkingLevelMap for the OSS models is PARTIAL:
  - deepseek/deepseek-v4.1-flash: low, high, xhigh (medium + max are null)
  - z-ai/glm-5.3: low, high, max (medium + xhigh null)
  - fugu-max / fugu-ultra-v2.0: high, xhigh, max only
- PROOF of hard failure: spawn with model=openrouter/deepseek/deepseek-v4.1-flash, thinking='medium' ->
  RuntimeError: Requested thinking level "medium" is not supported by model "openrouter/deepseek/deepseek-v4.1-flash"; supported levels: low, high, xhigh
- Cross-provider native child FROM an OSS parent WORKS in this install:
  - openai-codex/gpt-5.6-luna admitted (model field confirmed)
  - sakana/fugu-max admitted (model field confirmed)
- `gpt-6-astra` DOES NOT EXIST in this Prime catalog: find_models('astra')=0, find_models('gpt-6')=0.
  Prime openai-codex models available: gpt-5.5, gpt-5.6-luna, gpt-5.6-sol, gpt-5.6-sol-1m, gpt-5.6-terra.
  Also prime-inference/openai/gpt-5.6-sol|sol-pro|luna|luna-pro|terra|terra-pro, openrouter/openai/gpt-5.6-*.
- So: Codex vocab `gpt-6-astra`/`xhigh` default is unreachable from Prime; Sol/Luna/Terra/Fable/Opus/GLM/DeepSeek/Fugu/Kimi/Grok are reachable.

## Repo facts
- Live skill surface: skills/<slug>/{SKILL.md,references/}. Many skills also have a stale-looking skills/<slug>/build/ copy (skills/agent-delegate/build/, arch-docs/build/, etc.) with OLDER model doctrine (e.g. build/references/model-and-invocation.md names haiku/sonnet/opus only). Makefile installs the live surface, not build/.
- Makefile SKILLS list == install surface for ~/.agents/skills and ~/.codex/skills; CLAUDE_SKILLS ~ same; shared doctrine dir `_shared` ships alongside.
- Key container-skill text:
  - skills/delegated-implementation/SKILL.md: "An Astra parent assigns implementation and verification to GPT-5.6 Sol (`gpt-5.6-sol`) at `high`. A Fable parent assigns them to Opus 5 ... For another parent model, use the worker choice supplied by the user or calling workflow."  <- undefined fallback when nobody supplied one
  - skills/issue-to-pr/SKILL.md: "For an Astra or Fable coordinator, apply `$delegated-implementation` ... For other dispatches, read the installed `../_shared/agent-orchestration-policy.md` and apply `$prompt-authoring`" <- no worker-profile guidance for OSS parents
  - skills/epic-to-prs/SKILL.md: same fork; hard external dependency on GPT-6 Astra Pro via $chatgpt-web (host-independent, OK).
  - skills/conductor/SKILL.md: ALREADY generic: inherits-or-pin doctrine, "never route bulk work to an unpinned native child", but its fleet default is Codex `gpt-6-astra` at `xhigh` (unreachable in Prime).
  - skills/miniarch-step/SKILL.md:85 ALREADY has the guard pattern: "prefer `gpt-5.4-mini` with `xhigh` ... only when the active native tool schema can select and confirm both. Otherwise use the inherited native capability and do not claim the child used an unconfirmed model or effort."
- skills/_shared/native-child-capabilities.md is the facts file (Prime/Codex/Claude matrix). It says Prime pin = `model="provider/id"`, exact selector, hard fail when not in catalog; unsupported thinking level = hard spawn failure when set explicitly, inherited level silently clamped.
