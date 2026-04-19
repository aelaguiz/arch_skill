# Examples And Anti-Examples

Use this file when you need concrete patterns for writing or auditing repo `AGENTS.md` files.

## Table of contents

- Example: strong root-file shape
- Example: strong path-local file
- Example: override done right
- Example: rule quality
- Example: docs index versus doc dump
- Example: repo truth versus author narration
- Example: plain English versus workflow jargon
- Example: findings-first audit

## Example: strong root-file shape

Good:

```md
# AGENTS.md

## Build and verify
- Install: `pnpm install`
- Lint: `pnpm lint`
- Test: `pnpm test`
- Typecheck: `pnpm typecheck`
- File test: `pnpm vitest run path/to/file.test.ts`

## Definition of done
- The relevant lint, test, and typecheck commands pass.
- Changed files stay within the requested scope.
- If behavior changed, tests or explicit proof changed with it.

## When blocked
- Ask before adding dependencies.
- Ask before running migrations or deleting files.
- Stop and report the exact failing command after repeated retries.

## Plain Speak
- Write in plain natural English.
- Lead with the concrete answer in 1-3 sentences.
- Say `I installed it on this machine`, not `I completed the host-local cutover`.
- Translate repo shorthand immediately if it must appear.

## Docs map
- Release docs: `docs/release/index.md`
- Auth docs: `docs/backend/auth.md`
```

Why it works:

- commands first
- explicit done rules
- explicit blocked-state behavior
- plain-English communication rule that prevents jargon-heavy replies
- compact pointers to deeper truth

Weaker:

```md
# AGENTS.md

We believe in clean, thoughtful engineering. Follow existing patterns and be careful with risky changes.
```

Why it fails:

- no commands
- no definition of done
- no local truth surfaces
- no real operational guidance

## Example: strong path-local file

Good:

```md
# AGENTS.md

## Local verify
- API tests: `cargo test -p payments-api`
- Contract checks: `make test-payments-contracts`

## Local red lines
- Never rotate payment secrets from this workspace.
- Ask before editing settlement or ledger migrations.

## Local docs
- Settlement flow: `docs/payments/settlement.md`
- Retry rules: `docs/payments/retries.md`
```

Why it works:

- only local deviations
- no restatement of the entire root doctrine
- fast to scan under pressure

Bad:

- copying the whole root file and adding three local lines at the bottom

Why it fails:

- duplicate budget
- conflicting local edits become harder to maintain

## Example: override done right

Good use case:

- a release-freeze or incident-response directory where normal commands and autonomy rules would be actively wrong

Good file shape:

```md
# AGENTS.override.md

## Mode
- Freeze mode. Do not ship normal feature work from this directory.

## Local verify
- `make freeze-check`
- `make incident-smoke`

## Red lines
- No dependency updates.
- No schema changes.
- No config edits without human approval.
```

Why it works:

- clearly replaces, not extends, the normal local behavior
- states the mode at the top
- fully restates the local verify path

Bad use case:

- using an override just to emphasize stylistic preference

## Example: rule quality

Strong:

- "Run `pnpm vitest run path/to/file.test.ts` before touching snapshot baselines."
- "If a command fails three times for the same reason, stop and report the output."
- "Do not edit generated SDK files directly; regenerate with `pnpm generate:sdk`."

Weak:

- "Be careful with tests."
- "Use your best judgment with generated files."
- "Optimize for quality."

Strong rules:

- have a trigger
- describe an action
- are anchored to a command, path, or stop condition

Weak rules:

- sound wise but do not change behavior

## Example: docs index versus doc dump

Better:

```text
[Docs Index] root: ./docs/agent
| deploy/: {overview.md, rollback.md}
| data/: {schema.md, migrations.md}
| frontend/: {tokens.md, testing.md}
```

Worse:

- copying the contents of `schema.md`, `rollback.md`, and `tokens.md` straight into root `AGENTS.md`

Why the index wins:

- cheaper always-on context
- easier maintenance
- clearer retrieval path

## Example: repo truth versus author narration

Better:

```md
## Verify
- `pnpm lint`
- `pnpm test path/to/file.test.ts`

## When blocked
- Ask before editing migrations under `db/migrations`.
```

Worse:

```md
This file was created to help agents think through the repo.
We may split it later once the architecture settles.
Use `$agents-md-authoring` when updating this file.
```

Why the worse version fails:

- talks about the file instead of the repo
- leaks planning and retrospective commentary
- adds self-referential skill chatter instead of operational guidance
- gives the agent no commands, stop rules, or truth surfaces

## Example: plain English versus workflow jargon

Better:

```md
## Plain Speak
- Lead with the concrete answer.
- Use short plain-English sentences.
- Say `I didn't uninstall it`, not `I did not roll back the host-local setup`.
- Avoid workflow labels like `arch-step`, `North Star`, `phase plan`, or `review-gate` unless the user asked for them. Even then, give the plain-English answer first.
```

Worse:

```md
## Communication
- Preserve boundary clarity across the follow-through surface.
- Explain whether the host-local cutover was rolled back to its prior state.
- Use workflow labels to anchor the answer.
```

Why the worse version fails:

- makes the user translate the answer
- prefers internal process language over the concrete action
- buries simple facts like `installed`, `uninstalled`, or `updated`
- teaches the exact tone the repo owner is trying to stop

## Example: findings-first audit

Good audit finding:

- **Missing file-scoped verification commands**
  - Why it matters: the file only lists full-repo checks, so agents may skip targeted local validation or overrun expensive global commands.
  - Change: add file-scoped examples near the top-level verify section or link to the test-selection doc.

- **Root file contains inferable architecture summary**
  - Why it matters: always-on context is being spent on facts the agent can discover from the repo or docs.
  - Change: cut the summary and replace it with a compact docs map.

- **Local payments instructions should be an override**
  - Why it matters: the current child file partially contradicts the inherited local rules, which leaves dangerous ambiguity.
  - Change: replace the child file with `AGENTS.override.md` and restate the mode-specific verify path.

Weak audit finding:

- "Could be clearer."

Why it fails:

- no concrete issue
- no performance consequence
- no owning file or section
