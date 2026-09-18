# Plan: issue-to-pr and epic-to-prs default to native subagents

Date: 2026-09-18. Status: plan only. No skill file has been edited.

## The guidance to add

> Astra and Fable parents have their own rules. If you are not one of them, or
> you are not sure, use your own native subagents on your own model for every
> worker, reviewer, and seat except Pro. Do not start an external agent unless
> the user asks for one.

That is the whole change. It goes in three places.

## The three edits

1. `skills/issue-to-pr/references/primary-and-final.md`, section "Reaching
   another model" (`:55-67`). Put the guidance at the top. Mark the two existing
   bullets (external Claude process, external Codex process) as the Fable and
   Astra rules.
2. `skills/issue-to-pr/SKILL.md:166-168`. Replace "Any other model as a clean
   native child or an external process through `$agent-delegate` at the exact
   model and effort named" with the guidance.
3. `skills/epic-to-prs/SKILL.md:136-139`. Same sentence, same replacement.

No other file changes. `delegated-implementation` and the shared orchestration
policy already say this for workers (commit `3724c69`). Seats were the gap.

About 15 minutes, written under `$skill-authoring`.

## Verify

1. `npx skills check`
2. `make install`, so `~/.agents/skills/` gets the change.
3. Rerun the same prompt in Codex on the DeepSeek preset. Pass: the primary seat
   is a `spawn_agent` call and there are zero `codex exec` calls.

## Why: notes from session `01a0b699-3932-7fb3-b460-57428c61f8dc`

Source: `~/.codex/sessions/2026/09/18/rollout-2026-09-18T17-18-10-01a0b699-3932-7fb3-b460-57428c61f8dc.jsonl`

- The parent was DeepSeek v4.1 Flash through OpenRouter, inside Codex. Amir
  asked for `$issue-to-pr` with a Sol xhigh primary and a Pro final.
- It launched the primary seat as an external `codex exec` process. Its
  reasoning quotes the line that decided it, `primary-and-final.md:64-67`: a
  Codex-model seat "is an external Codex process through `$agent-delegate`."
  That line has no native option and applies to every parent.
- It was also not sure which model it was. It read `~/.codex/config.toml` and
  decided "I'm an Astra parent." That is why the guidance says "or you are not
  sure."
- Amir's correction: "No, use your own native subagents. Don't use
  Codex-invoked subagents. Don't use external Codex subagents."
- Cost: 15 minutes and one discarded external Sol xhigh run.

Other sessions: of 40 Codex sessions in the last week that loaded `issue-to-pr`
or `epic-to-prs`, this is the only one that named a seat, and the only one that
went external unasked. A second DeepSeek session (`01a0a4e3-ca6c`, 2026-09-15)
tried to pin `gpt-5.6-sol` on a native child, was rejected, and weighed going
external before staying native. Workers already go native.

## Separately

After that session switched to native, 8 of 9 child replies said the task body
arrived empty. That is a Codex harness bug with non-OpenAI providers, not a skill
problem. It needs its own look.
