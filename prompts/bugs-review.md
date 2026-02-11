---
description: "External review (cross-tool): audit bug fix against the bug doc via the other agent CLI, then apply feedback you agree with."
argument-hint: "<Required: docs/bugs/<...>.md bug doc path. Optional: scope notes (perf/security/only suggest, no code changes).>"
---
# /prompts:bugs-review — $ARGUMENTS
# COMMUNICATING WITH DEV (IMPORTANT)
- Start console output with a 1 line reminder of our Bug North Star.
- Then give the punch line in plain English.
- Then give a short update in natural English (bullets optional; only if they help).
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Keep console output high-signal; long logs go in a file.

Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately.
$ARGUMENTS is freeform steering. Infer what you can.

Hard constraints:
- DO NOT USE PAL MCP (this is a command-line action).
- Detect which agent you're running in and use the OTHER tool for the review:
  - If `CLAUDECODE=1` is set (you are Claude Code): use Codex CLI
    `echo "<prompt>" | codex exec --dangerously-bypass-approvals-and-sandbox`
  - Otherwise (you are Codex or other): use Claude Code CLI
    `echo "<prompt>" | claude -p --dangerously-skip-permissions`
- NEVER pass the prompt as a positional argument — it hangs in nested sessions.
- ALWAYS use print/exec mode so the reviewer exits after responding.

Question policy (strict):
- You MUST answer anything discoverable from code/tests/docs or by running repo tooling; do not ask me.
- Allowed questions only:
  - Missing access/permissions (e.g., `claude` not installed / not authenticated)
  - Doc-path ambiguity (pick from top 2–3 candidates)
  - A real product/UX decision not encoded anywhere

Goal:
Get an external, high-signal code review of the bug fix relative to the bug doc, then integrate the feedback you agree with (you do not have to accept everything).

## 0) Resolve DOC_PATH
- If $ARGUMENTS contains a docs/bugs/<...>.md path, use it as DOC_PATH.
- Otherwise infer DOC_PATH from the repo (recent bug docs). If ambiguous, ask the user to choose from the top 2–3 candidates.

## 1) Run external review (this may take ~5 minutes — don't be antsy)
- Print one short line like: "Running external code review (can take ~5 minutes)…", then run the command and wait for completion (no chatty progress spam).
- CRITICAL: You must **pipe the prompt** to the reviewer, not pass it as a positional argument. Positional args hang when invoked from inside another agent session.
- Detect the reviewer CLI and run:
  ```bash
  # Detect reviewer CLI
  if [ "$CLAUDECODE" = "1" ]; then
    REVIEWER="codex exec --dangerously-bypass-approvals-and-sandbox"
  else
    REVIEWER="claude -p --dangerously-skip-permissions"
  fi

  cat <<'REVIEW_EOF' | $REVIEWER
  <PROMPT>
  REVIEW_EOF
  ```

Where `<PROMPT>` is a single, well-formed instruction that includes DOC_PATH and asks Claude to do an evidence-anchored audit relative to the bug doc.
Use this prompt template (fill in DOC_PATH and any scope hints from $ARGUMENTS):

Claude prompt:
`Use parallel agents to exhaustively review my implementation relative to DOC_PATH=<DOC_PATH>, looking for anything missing or incorrect vs the bug doc. Read the relevant files and the diff vs main. Focus on correctness, edge cases, regressions, and whether the fix truly addresses the stated root cause. Explicitly verify the fix aligns with the Evidence section and that the evidence supports the chosen root cause/fix. Call out any missing call sites, partial migrations, or SSOT violations. Do not recommend negative-value tests (deleted-code proofs, visual-constant/golden noise, doc-driven inventory gates, mock-only interaction tests). Provide evidence anchors (file paths / symbols). Output: (1) Top risks (ranked), (2) Specific fixes with file anchors, (3) Tests to add or run (targeted only), (4) Anything over-scoped or unrelated.`

## 2) Process feedback (apply what we agree with)
- Summarize Claude’s feedback into three buckets:
  - “Will do now” (high-confidence, in-scope)
  - “Disagree / won’t do” (with a short rationale)
  - “Follow-ups” (good ideas but out-of-scope)
- For “Will do now” items: implement fixes and keep changes minimal/targeted.
- Run the smallest relevant checks to validate the changes (don’t run the full suite unless requested or clearly required).
- If the bug doc needs a quick update (Decision Log / risks), update DOC_PATH accordingly (keep it short).

Commit policy:
- Do NOT commit by default.
- If $ARGUMENTS explicitly asks to commit, do so (stage only files you touched).

OUTPUT FORMAT (console only; Dev-style):
This is the information it should contain but you should communicate it naturally in english not as a bulleted list that is hard to parse for the user.
Include:
- Bug North Star reminder (1 line)
- Punchline (1 line)
- What the reviewer found (short, practical summary)
- What you accepted vs declined (and why, briefly)
- What you changed (if anything) + what checks you ran
- Pointers (DOC_PATH + any file where you saved the raw Claude output, if you saved it)
