---
name: codex-review-yolo
description: "Invoke the local Codex CLI with the exact external `yolo` profile (gpt-5.6-sol xhigh, fast tier) and captured receipts for an independent review of a substantial artifact or completion state. Use when the user explicitly asks for `codex -p yolo`, an external Codex review, or the profile's exact model/effort/receipt contract. Ordinary same-host Codex reviews should use a clean native child instead. Review-only; requires a concrete artifact or completion target."
metadata:
  short-description: "Request an independent review from codex -p yolo"
---

# codex-review-yolo

Use this skill when the user wants an independent review from the locally
installed `codex` CLI using the exact `yolo` profile. The artifact can be code,
a doc, a plan, a rollout, or a completion state. This is the deliberate
external-profile lane: its value is the pinned profile, clean process context,
and captured final/event artifacts. An ordinary same-host Codex review should
use a clean native child instead.

Read `../_shared/agent-orchestration-policy.md` before dispatch. This skill's
transport is intentionally external and its starting context is intentionally
clean; it does not redefine the suite-wide transport or context policy.

This skill is intentionally narrow in mechanism, not in review subject. It teaches the invocation pattern, the prompt shape that makes codex read the named artifacts directly, and how to consume the verdict. It does not wrap every possible codex use case.

## When to use

- The user says `run codex -p yolo`, names the `yolo` profile, or explicitly
  asks for an external Codex review with its captured receipt shape.
- The user has a substantial artifact or completion target and specifically
  wants the pinned `yolo` model/effort/tier or its external receipt contract
  before the next step.
- The user wants an adversarial external Codex audit and chooses the `yolo`
  profile as the independent reviewer.

## When not to use

- The user wants codex to *write* code, not review it. This skill is review-only.
- The user wants an ordinary same-host Codex review and does not need the exact
  `yolo` profile or external receipts. Use a clean native reviewer under the
  shared policy.
- The user wants a quick yes/no on a one-line change — the setup cost exceeds the value.
- The user has not yet produced a concrete artifact or completion target to
  review. Don't spin up codex on vapor.
- `codex` is not installed on the host — `which codex` returns nothing. Stop and tell the user.

## Non-negotiables

- **Run codex with `-p yolo` explicitly.** The profile carries gpt-5.6-sol + xhigh reasoning + fast service tier + `danger-full-access` sandbox. Any other profile changes the contract.
- **Use `codex exec` (non-interactive), not `codex` (interactive TUI).** You are orchestrating, not babysitting a session.
- **Brief codex like a colleague who just walked in.** It has no memory of your session. Name the review goal, work root, exact user-named artifacts or target paths, hard constraints, and the verdict contract.
- **Require a structured verdict block at the end.** Without it, codex drifts into narrative and you cannot act on the result.
- **Treat the prompt examples as examples.** Adapt the sections to the actual review objective instead of cargo-culting one review mode.
- **Never pass secrets in the prompt.** If codex needs `FIGMA_ACCESS_TOKEN` or similar, source `.env` into the codex env and instruct codex to read it from the environment.
- **Run in the background for non-trivial audits.** Codex at xhigh takes
  minutes. Normal audits often take 5+ minutes, and broad `xhigh` audits can
  reasonably take 20-40 minutes. Kick it off with background execution so you
  can keep working.
- **Namespace every run's files.** Derive one run-specific directory or prefix and keep the prompt, final output, and stream log inside it so concurrent runs on the same machine never clobber each other.
- **Capture output to a file.** The final-message file is the consumable deliverable; the stream log is diagnostic.
- **Trust but verify.** Codex can be wrong. Spot-check any blocking finding by reading the cited file before acting on it.
- **Keep the external cost deliberate.** A separate Codex process adds lifecycle,
  integration, and shared SQLite/WAL contention cost. Do not create parallel
  `yolo` reviewers merely as a speed reflex; choose the fanout that the concrete
  review benefit and current host state justify. This is a cost judgment, not a
  ban or fixed process limit.
- **Keep topology parent-owned.** The review prompt tells Codex not to spawn
  nested agents or invoke delegation/consult skills. The parent verifies and
  integrates the verdict.
- **Verify the review-only boundary from repository state.** The `yolo`
  profile grants `danger-full-access`; a no-edit prompt is guidance, not an
  enforced capability boundary. Record the reviewed repository's status and
  diff before launch, compare them after the process exits, and account for any
  change before trusting or integrating the verdict.

## First move

1. Confirm `codex` exists and the `yolo` profile is defined: `which codex && grep -A2 '^\[profiles.yolo\]' ~/.codex/config.toml`.
2. Identify the exact review objective and user-named artifacts or target paths:
   commit SHA(s), branch, file paths, doc paths, commands to inspect current
   state, or plan phases. Write them down in the prompt.
3. Create a namespaced run directory once and reuse it for every file in that invocation. Example:

   ```bash
   REVIEW_SLUG="phase-b-completion"
   RUN_TS="$(date -u +%Y%m%dT%H%M%SZ)"
   RUN_DIR="$(mktemp -d "/tmp/codex-review-${REVIEW_SLUG}-${RUN_TS}-XXXXXX")"
   PROMPT_PATH="$RUN_DIR/prompt.md"
   FINAL_PATH="$RUN_DIR/final.txt"
   STREAM_PATH="$RUN_DIR/stream.log"
   ```

4. If the review needs API tokens, confirm `.env` has them and plan to `set -a; source .env; set +a` before invoking.
5. Draft the prompt to `$PROMPT_PATH` (never inline — prompts get long and multi-line is inevitable).
6. Note that this dispatch is a new clean external review with no continuation
   handle. Tell the reviewer not to edit or spawn children. Record the current
   repository status and diff before launch; this is required because the
   profile has `danger-full-access` even though the role is review-only.
7. Invoke via `codex exec -p yolo -C <repo-root> --json -o "$FINAL_PATH" < "$PROMPT_PATH" > "$STREAM_PATH" 2>&1`, in background.
8. Continue other work while Codex reasons; when it completes, compare the
   repository status and diff with the pre-launch snapshot, account for any
   change, then read `$FINAL_PATH`, verify important claims, and relay the
   verdict to the user.

## Workflow

### 1. Shape the prompt

A good prompt for codex review has these sections, in this order:

1. **Role + posture.** One line. "You are auditing X. Be skeptical. If the work is wrong, say so plainly."
2. **Review objective and work root.** State what approval means for this review and where codex should run.
3. **User-named artifacts or target paths.** Point codex at the concrete artifacts the user named.
4. **Verdict block requirement.** Demand a specific footer format so the result is machine-ish-readable.

See `references/prompt-template.md` for the full skeleton.

### 2. Invoke codex

Example pattern, adjust the repo root, review slug, and paths:

```bash
REVIEW_SLUG="phase-b-completion"
REPO_ROOT="$(pwd)"
RUN_TS="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_DIR="$(mktemp -d "/tmp/codex-review-${REVIEW_SLUG}-${RUN_TS}-XXXXXX")"
PROMPT_PATH="$RUN_DIR/prompt.md"
FINAL_PATH="$RUN_DIR/final.txt"
STREAM_PATH="$RUN_DIR/stream.log"

# If the audit needs API tokens, source them into the codex environment.
if [ -f "$REPO_ROOT/.env" ]; then set -a; source "$REPO_ROOT/.env"; set +a; fi

codex exec -p yolo \
  -C "$REPO_ROOT" \
  --json \
  -o "$FINAL_PATH" \
  < "$PROMPT_PATH" \
  > "$STREAM_PATH" 2>&1
```

Key flags:

- `-p yolo` — the profile. Non-negotiable.
- `-C <dir>` — the working root. Use the repo root (or the submodule root if that's the reviewed unit).
- `--json` — writes live Codex event JSONL to `stream.log` while the child
  works.
- `-o <file>` — writes the final assistant message to this file. This is what you Read at the end.
- `< prompt.md` — feeds the prompt via stdin. Keeps command lines sane and lets you iterate on prompts in a file.
- `> stream.log 2>&1` — captures the full event stream. Use for diagnosis if codex errored or went sideways.
- `$RUN_DIR/...` — keeps one review invocation's artifacts isolated from every other invocation.

Run via the shell's background support for any audit you expect to take more
than ~30 seconds. Poll `stream.log` and process status every few minutes, not
every few seconds. The final-message file is created when codex exits.

### 3. Consume the verdict

When codex finishes:

1. Compare the reviewed repository's status and diff with the pre-launch
   snapshot. Treat unexplained changes as a failed review-only boundary and do
   not hide, revert, or absorb them silently.
2. Read the run's final output file, e.g. `$FINAL_PATH`.
3. Locate the `VERDICT:` / `REQUIRED REPAIRS:` / `OBSERVATIONS:` footer.
4. Relay findings to the user. Do not blindly trust — spot-check any required
   repair claim against the actual file before acting.
5. If codex found nothing actionable, say so directly. Don't manufacture issues to justify the invocation.

## Output expectations

- A short summary to the user: what codex's verdict was, what blocking issues it found (if any), and whether you agree after verification.
- The full final-output file stays on disk in its namespaced run directory — mention the path so the user can read the full review if they want.
- Never claim codex said something it didn't. If the output is ambiguous, say "codex was ambiguous on X" and ask the user how to proceed.

## Reference map

- `references/prompt-template.md` — full skeleton for the review prompt, plus clearly-labeled examples for diff review, implementation completion, plan review, and cross-repo review
- `references/verdict-contract.md` — the exact footer format and how to parse it
- `references/troubleshooting.md` — common failure modes (no output, rate-limit, truncation, codex can't find files)
