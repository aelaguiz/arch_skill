# Invocation Reference

Two supported invocations:

1. **Direct.** User invokes `$code-review` from Codex or Claude Code. The skill runs the Python runner, which shells out to Codex for every review subprocess.
2. **Hook-backed.** User arms a `code-review` hook state for the current session, then the installed Stop hook drives the runner at each Stop event.

Every review subprocess is **always a fresh Codex process** at `gpt-5.4` `xhigh`, unsandboxed by default. Claude (or any other caller) is never the reviewer.

## Direct invocation

From a repo root:

```bash
python3 skills/code-review/scripts/run_code_review.py \
  --repo-root "$(git rev-parse --show-toplevel)" \
  --target uncommitted-diff \
  --output-root /tmp/code-review
```

Supported `--target` modes:

- `uncommitted-diff` — `git diff HEAD` (and staged) against the worktree.
- `branch-diff --base <ref> --head <ref>` — `git diff <base>...<head>`.
- `commit-range --base <sha> --head <sha>` — `git log -p <base>..<head>`.
- `paths --paths <file> [<file> ...]` — explicit path list; review examines current worktree contents of those paths.
- `completion-claim --claim-doc <path> --claim-phase <n>` — review whether the cited plan phase is really complete; target context is the plan doc plus recent commits.

Common flags:

- `--objective "<free-form user objective>"` — optional; passed to the reviewer as `{objective}`.
- `--output-root <dir>` — where the runner writes namespaced run directories. Default: `/tmp/code-review`.
- `--run-dir <dir>` — explicit run directory; overrides `--output-root`. Useful for hook-driven runs where the dispatcher pre-computes the path.
- `--host-runtime <codex|claude>` — optional; purely informational, recorded in the run manifest. Does NOT change reviewer identity.

## Codex subprocess flags (what the runner actually launches)

Lens subprocess (one per required lens):

```
codex exec \
  --ephemeral \
  --disable codex_hooks \
  --cd <repo_root> \
  --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.4-mini \
  -c model_reasoning_effort="xhigh" \
  -o <run_dir>/lenses/<lens_name>.final.txt \
  < <run_dir>/lenses/<lens_name>.prompt.md
```

Synthesis subprocess:

```
codex exec \
  --ephemeral \
  --disable codex_hooks \
  --cd <repo_root> \
  --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.4 \
  -c model_reasoning_effort="xhigh" \
  -o <run_dir>/synthesis.final.txt \
  < <run_dir>/synthesis.prompt.md
```

Rationale for each flag:

- `--ephemeral` — no session persistence; every review starts with fresh context.
- `--disable codex_hooks` — prevent Stop-hook recursion when a hook-backed run spawns the review subprocess.
- `--cd <repo_root>` — pin working directory to the reviewed repo.
- `--dangerously-bypass-approvals-and-sandbox` — match the repo's existing pattern for fresh review/audit children. Intentionally unsafe outside hardened local environments; do not copy into untrusted contexts.
- `--model` + `-c model_reasoning_effort` — pin exact model and reasoning effort regardless of profile state.
- `-o <final.txt>` — capture the final assistant message. The runner validates this against the output contract.

## Run artifact layout

Each invocation creates one namespaced run directory. Default shape:

```
<output_root>/<YYYYMMDD_HHMMSS>_<short-hash>/
  manifest.json            # target, objective, host runtime, model/effort, repo root, lens list
  target/
    target.json            # structured target spec
    diff.patch             # captured diff (uncommitted-diff / branch-diff / commit-range)
    paths.txt              # path list (paths mode)
  lenses/
    <lens_name>.prompt.md  # prompt fed to the lens subprocess
    <lens_name>.stream.log # stdout/stderr
    <lens_name>.final.txt  # captured final assistant message
  synthesis.prompt.md      # prompt fed to the synthesis subprocess
  synthesis.stream.log
  synthesis.final.txt      # canonical ReviewVerdict
  coverage.json            # lenses completed / failed, agent-linter state, external sources, conventions
  errors.log               # malformed-output or child-failure details (when present)
```

Rules:

- The runner MUST NOT write anywhere outside the run directory.
- The runner MUST NOT modify the reviewed repo.
- `synthesis.final.txt` is the single authoritative review output for that invocation.

## Hook-backed invocation

The shared `skills/arch-step/scripts/arch_controller_stop_hook.py` dispatcher owns `code-review` as one of its controller families. State lives at:

- Codex host: `.codex/code-review-state.<SESSION_ID>.json`
- Claude host: `.claude/arch_skill/code-review-state.<SESSION_ID>.json`

State file shape:

```json
{
  "version": 1,
  "command": "code-review",
  "session_id": "<SESSION_ID>",
  "repo_root": "<absolute path>",
  "target": {
    "mode": "uncommitted-diff | branch-diff | commit-range | paths | completion-claim",
    "base": "<ref or sha>",
    "head": "<ref or sha>",
    "paths": ["<path>", "..."],
    "claim_doc": "<docs/PLAN.md>",
    "claim_phase": <n>
  },
  "objective": "<free-form or empty>",
  "output_root": "<dir>",
  "host_runtime": "codex | claude"
}
```

The dispatcher:

- resolves the state file per host runtime
- validates session ownership
- invokes the runner with the state-file fields as CLI arguments
- forwards the run directory path and a verdict summary back to the Stop-hook JSON

The Claude host case is an intentional exception to the broader native-auto-loop direction: the Stop hook runs under Claude, but the actual review subprocess is Codex. Generic Claude auto-controllers stay Claude-native; `code-review` does not.

## Default model and reasoning effort

- Lens subprocess model: `gpt-5.4-mini`
- Lens reasoning effort: `xhigh`
- Synthesis model: `gpt-5.4`
- Synthesis reasoning effort: `xhigh`

These are runner-enforced defaults. Users do not override them through `SKILL.md`. Changing them would change the review product, not a knob, and must go through plan/Decision-Log review.

## Failure behavior (fail-loud, no silent downgrade)

The runner MUST exit non-zero and preserve artifacts when:

- `codex` is not on PATH.
- The requested `--target` cannot be resolved (empty diff, missing refs, unreadable paths, missing claim doc).
- A required parallel lens subprocess fails to start or exits non-zero.
- A lens subprocess emits malformed output (see `output-contract.md`).
- The synthesis subprocess emits a malformed `ReviewVerdict`.
- Required agent-linter coverage is missing on an agent-surface target.
- Any write leaves the run directory.

The runner MUST NOT:

- Silently drop a lens and declare exhaustive coverage.
- Fall back to caller-model review when Codex is unavailable.
- Modify, format, or "clean up" a malformed output — preserve it verbatim for debugging.
- Retry a failing lens indefinitely; retries are off by default.

## Operational boundary

The unsandboxed Codex invocation is intentionally permissive. It matches the existing repo pattern for fresh review/audit children and trades sandbox isolation for realistic repo access. Run this skill only inside a hardened local environment that you would give a fresh Codex process full access to. Do not adopt this invocation pattern in untrusted environments.
