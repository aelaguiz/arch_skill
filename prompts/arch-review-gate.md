---
description: "09) Review gate: external idiomatic+completeness check."
argument-hint: DOC_PATH=<path> (optional)
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
If DOC_PATH is not provided, locate the most relevant architecture doc by semantic match to $ARGUMENTS and the current conversation; prefer the doc that explicitly matches the topic and is most recently updated among relevant candidates. If you cannot determine a clear winner, ask the user to choose from the top 2–3 candidates.
Request reviews from opus/gemini with the explicit question:
“Is this idiomatic and complete relative to the plan?”
Provide any files they request. Integrate feedback you agree with.
Update $DOC_PATH before moving to the next phase.
Write the Review Gate block into $DOC_PATH (append near the phase progress section). Do not paste the full block to the console.

DOCUMENT INSERT FORMAT:
## Review Gate
- Reviewers: <opus|gemini>
- Question asked: “Is this idiomatic and complete relative to the plan?”
- Feedback summary:
  - <item>
- Integrated changes:
  - <item>
- Decision: proceed to next phase? (yes/no)

CONSOLE OUTPUT FORMAT (summary + open questions only):
Summary:
- <bullet>
Open questions:
- Proceed to next phase? (yes/no)
