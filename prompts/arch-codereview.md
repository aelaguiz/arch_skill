---
description: "13) Code review (Claude CLI): run an external review via `claude`, then apply the feedback you agree with."
argument-hint: "<Required: docs/<...>.md plan doc path. Optional: scope notes like 'security', 'perf', 'only suggest, no code changes'.>"
---
# /prompts:arch-codereview — $ARGUMENTS
# COMMUNICATING WITH USERNAME (IMPORTANT)
- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give a short update in natural English (bullets optional; only if they help).
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Keep console output high-signal; long logs go in a file.

Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately.
$ARGUMENTS is freeform steering. Infer what you can.

Hard constraints:
- DO NOT USE PAL MCP (this is a command-line action).
- Use the Claude CLI exactly like: `claude --dangerously-skip-permissions "<prompt>"`

Question policy (strict):
- You MUST answer anything discoverable from code/tests/docs or by running repo tooling; do not ask me.
- Allowed questions only:
  - Missing access/permissions (e.g., `claude` not installed / not authenticated)
  - Doc-path ambiguity (pick from top 2–3 candidates)
  - A real product/UX decision not encoded anywhere

Goal:
Get an external, high-signal code review of the implementation relative to the plan doc, then integrate the feedback you agree with (you do not have to accept everything).

## 0) Resolve DOC_PATH
- If $ARGUMENTS contains a `docs/<...>.md` path, use it as DOC_PATH.
- Otherwise infer DOC_PATH from the repo (recent docs, or the most relevant plan doc). If ambiguous, ask the user to choose from the top 2–3 candidates.

## 1) Run Claude review (this may take ~5 minutes — don’t be antsy)
- Print one short line like: “Running Claude code review (can take ~5 minutes)…”, then run the command and wait for completion (no chatty progress spam).
- Run:
  - `claude --dangerously-skip-permissions "<PROMPT>"`

Where `<PROMPT>` is a single, well-formed instruction that includes DOC_PATH and asks Claude to use “parallel agents” (multiple reviewer perspectives) and produce actionable, evidence-anchored feedback.
Use this prompt template (fill in DOC_PATH and any scope hints from $ARGUMENTS):

Claude prompt (single string):
`Use parallel agents to exhaustively, line by line, code review my implementation relative to DOC_PATH=<DOC_PATH>, looking for every single element of our plan doc vs any ground truths referenced. Literally read every single file that was part of the plan or adjacent to the plan, read the actual diff vs main, and find anything we did we weren't supposed to as well as anything we did not do that we were supposed to. DO NOT AUDIT FOR SECURITY OR PII CONCERNS THAT IS OUT OF SCOPE. Also: do not recommend negative-value tests (deleted-code proofs, visual-constant/golden noise, doc-driven inventory gates, mock-only interaction tests). Also: call out any missing high-leverage code comments/doc comments for new SSOTs/contracts or tricky gotchas; avoid comment spam. Review for correctness vs the plan, edge cases, performance, maintainability, and test coverage. Point to concrete evidence (file paths / symbols). Output: (1) Top risks (ranked), (2) Specific suggested fixes with file anchors, (3) Tests to add or run (relevant only, not full-suite), (4) Anything that looks over-scoped. Be direct.`

## 2) Process feedback (apply what we agree with)
- Summarize Claude’s feedback into three buckets:
  - “Will do now” (high-confidence, in-scope)
  - “Disagree / won’t do” (with a short rationale)
  - “Follow-ups” (good ideas but out-of-scope for this PR)
- For “Will do now” items: implement fixes and keep changes minimal/targeted.
- Run the smallest relevant checks to validate the changes (don’t run the full suite unless requested or clearly required).
- If the plan doc needs a quick update (Decision Log / risks), update DOC_PATH accordingly (keep it short).

Commit policy:
- Do NOT commit by default; leave changes ready for `/prompts:arch-open-pr`.
- If $ARGUMENTS explicitly asks to commit, do so (stage only files you touched).

OUTPUT FORMAT (console only; USERNAME-style):
This is the information it should contain but you should communicate it naturally in english not as a bulleted list that is hard to parse for the user.
Include:
- North Star reminder (1 line)
- Punchline (1 line)
- What Claude found (short, practical summary)
- What you accepted vs declined (and why, briefly)
- What you changed (if anything) + what checks you ran
- Pointers (DOC_PATH + any file where you saved the raw Claude output, if you saved it)
