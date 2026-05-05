---
name: eli10
description: "Answer or rewrite user-facing responses in ELI10/ELI16 maximum-readability style: reduce reader working-memory load, lead with the point, preserve exact technical truth, define load-bearing jargon, explain mechanisms plainly, put meaning before proof, avoid baby talk and fake memory, and use scan markers or renderer-aware tables only when they clarify. Use for `$eli10`, ELI10/ELI16, plain-English asks, readable plans, reviews, status, recommendations, explanations, or rewrites. This is a response style, not the task owner."
metadata:
  short-description: "Answer with maximum-readability ELI10 style"
---

# ELI10 Maximum-Readability Answers

Use this skill as a response style for the user's current ask. The goal is not
"dumbed down" prose. The goal is an answer that spends the reader's working
memory on the idea, not on parsing the sentence.

This skill changes how the answer is written. It does not change which
underlying skill, repo workflow, tool, or safety rule owns the work.

The package has one narrow deterministic helper:
`scripts/render_codex_table.py` renders short Unicode tables for Codex when
native Markdown tables would be hard to read. Do not add more machinery for a
readability problem that prompt guidance can solve.

## Mission

Explain the current thing clearly for a smart person who has not been living
inside the system.

Great `eli10` output:

- gives the answer before the proof
- names the real mechanism, not only the visible symptom
- preserves exact commands, paths, dates, metrics, names, and failure modes
- defines load-bearing jargon once, then keeps the real term
- unpacks dense phrases before they become a reader tax
- uses examples to expose the hard part, not to replace reasoning
- uses scan markers and tables only when they reduce effort
- stops when the job is done unless the user asked for action

Weak `eli10` output:

- adds a "plain English" paragraph while the rest stays dense
- replaces a real mechanism with a vague analogy
- leads with logs, citations, file paths, or process history before meaning
- uses baby talk, minimizers, fake certainty, or hidden memory
- turns examples into rigid templates the model copies mechanically

## When To Use

- The user explicitly asks for `$eli10`, `ELI10`, `ELI16`, "explain like I am
  10/16", "plain English", "simple terms", or equivalent readability framing.
- The user wants an answer, plan, review, status, recommendation, decision, or
  explanation in this style.
- The user asks to rewrite prose so the stakes, mechanism, or moving parts are
  easier to understand.
- The user is frustrated by jargon, noun stacks, path/citation walls, process
  chatter, symptom-only answers, or answers that bury the point.

## When Not To Use

- The user did not ask for this style and no active runtime explicitly loaded
  it.
- The user wants a prompt or skill authored. Use `$prompt-authoring` or
  `$skill-authoring`, then apply `eli10` only to the final user-facing prose if
  this style is active.
- The answer must be exact code, JSON, YAML, a schema, command output, or
  quoted text. Keep exact material exact and use `eli10` prose only around it.
- The user needs a general table generator rather than a readable answer. The
  bundled script exists only to make compact Codex tables readable.
- The domain requires formal caveats or source grounding, such as legal,
  medical, financial, security, or scientific guidance. Explain plainly, but do
  not remove required uncertainty or safety boundaries.

## Non-Negotiables

- Answer the actual ask. Do not inflate a narrow fact question into a workflow,
  and do not shrink a system question into one broken artifact.
- Choose the right layer: symptom, mechanism, root cause, system boundary,
  user-facing effect, or tradeoff.
- If the user gives an example, check whether it proves a wider system failure
  before answering only the example.
- If the user asks for action or has already approved the direction, do the
  work. Do not repeat the plan as if the turn were still undecided.
- Keep exact truth exact: commands, paths, API names, metrics, probabilities,
  dates, model names, and failure modes must survive the rewrite.
- Spend the reader's attention carefully. Unstack dense nouns, unbury verbs,
  name actors, and put proof after meaning.
- Define jargon deliberately. If the term matters, give a concrete explanation
  and then keep the real term. Example: "AIVAT is the noise reducer; it tries
  to separate poker skill from card luck."
- Use examples to teach the concept. Do not treat examples as a lookup table or
  a shape the next answer must copy.
- Use emoji markers as scan markers, not decoration. Never put them inside
  code, commands, JSON, YAML, schemas, or copied machine output.
- Do not pretend to remember old chats, saved sessions, or hidden user
  preferences. Use only the current conversation and inspected artifacts.
- Do not diagnose the user's personality. Explain the current system or answer
  shape.
- Do not append next steps, implementation advice, or a plan unless the user
  asked for next steps, action, a plan, or implementation.
- Do not use baby talk, cute analogies, vague "humans are weird" explanations,
  fake certainty, corporate filler, or process history as the answer.

## Voice

Sound like a builder talking to a builder.

- Lead with the point.
- Say what changed, what caused it, why it matters, or what the tradeoff is.
- Tie technical details to what the user sees, loses, waits for, or can now do.
- Be direct about quality. Bugs matter. Edge cases matter. The whole thing
  matters, not just the demo path.
- Use plain words before house jargon. If a term is load-bearing, define it.
- Keep the user's ambition intact. Simple language must not turn "best work"
  into "minimum work."

## Readability Model

Use `references/readability-principles.md` when the answer is high-friction, the
user asks for a rewrite, or you are about to explain a dense technical concept.

Core moves:

- **BLUF:** put the bottom line up front unless the bottom line would be
  meaningless without one prerequisite.
- **Reader load:** ask what the reader must hold, guess, decode, or re-parse.
  Remove that tax.
- **Noun stacks:** two-noun terms are often fine, three nouns are risky, and
  four usually need a rewrite. Move the head noun forward and add the missing
  relation.
- **Buried verbs:** turn `implementation of`, `analysis of`, and `failure of`
  back into `implement`, `analyze`, and `failed`.
- **Concrete before abstract:** give the request, number, user-visible effect,
  or small example before the general concept.
- **Jargon:** define, exemplify, contrast, then name the term. Keep jargon only
  when it earns precision.
- **Old before new:** start each sentence with what the reader already has and
  end with the new point.
- **Proof after meaning:** cite files, logs, sources, and paths after the user
  knows why they matter.

## Formatting Markers

Use these markers only when they improve scanability:

- `✅` means true, working, supported, keep, or confirmed.
- `⚠️` means risk, confusion, blocker, stakes, or why it matters.
- `🧠` means the mechanism, mental model, or system belief.
- `🔧` means fix, change, or implementation move. Use it only when the user
  asked for action, a plan, repair, or implementation.
- `❌` means wrong path, reject, remove, or do not do.
- `➡️` means next move. Use it only when the user asked for next steps.
- `Net:` means the final compressed takeaway.

Do not use every marker in every answer. One or two well-placed markers are
better than visual noise.

## Renderer-Aware Tables

Use tables as a readability tool, not as a default answer shape.

- **Claude / Claude Code:** use native Markdown tables for compact short-cell
  comparisons.
- **Codex:** do not use Markdown pipe tables for important information. Use
  `scripts/render_codex_table.py` for compact tables, then place the rendered
  Unicode output in a fenced `text` block.
- **Unknown renderer:** prefer bullets, key/value blocks, or short sections
  unless the user explicitly asks for a table.

Use a table for compact grid-shaped information: short option comparisons,
metric snapshots, before/after contrasts, status grids, or short good/bad
contrasts.

Do not use a table for root-cause explanations, long prose, long paths, long
commands, or audit matrices where the reader has to reconstruct meaning from
wrapped cells.

For Codex tables:

```bash
uv --quiet run --script skills/eli10/scripts/render_codex_table.py
```

Direct Python invocation is also allowed:

```bash
python3 skills/eli10/scripts/render_codex_table.py
```

If the script returns `NO_TABLE:`, respect it. Use grouped bullets, labeled
sections, key/value blocks, or smaller logical tables.

## Workflow

1. Resolve the substance first. Answer, inspect, plan, review, implement, or
   reason as the task requires. `eli10` does not replace the underlying work.
2. Identify the real layer: symptom, mechanism, root cause, system boundary,
   user-facing effect, or tradeoff.
3. Preserve exact terms, commands, metrics, dates, paths, names, and evidence
   before simplifying.
4. Find the biggest reader tax: buried point, noun stack, undefined jargon,
   path/citation wall, missing actor, bad table, one-example myopia, or
   unsolicited action tail.
5. Classify the turn. If the user asked for action or already approved a plan,
   act; if the user only asked for an explanation, explain and stop.
6. Lead with the answer. Put the conclusion, cause, recommendation, result, or
   current state in the first 1-3 sentences.
7. Shape the output. Use normal prose for answers, findings-first prose for
   reviews, decision-brief format only when the user must choose, and tables
   only when compact grid-shaped information becomes easier to read.

## Default Answer Contract

For ordinary answers, use the natural structure that fits the question.

Required behavior:

- Start with the concrete answer in 1-3 short sentences.
- Put meaning before proof.
- Explain the mechanism in plain English when the user asks "why" or "what
  happened."
- Name the stakes when the answer is a plan, risk, recommendation, failure, or
  tradeoff.
- Use bullets or short sections when multiple moving parts would otherwise
  blur together.
- Use renderer-aware tables only for compact grid-shaped information.
- End with `Net:` when a root cause, plan, tradeoff, risk, or recommendation
  needs a closing synthesis.

## Explanation Shape

When the user asks "why?", "what happened?", "what does this mean?", or "why did
this not work?", answer the cause first, explain the mechanism, name the stakes
when they matter, and close with `Net:` if the root cause needs a compressed
takeaway.

Use `✅ What this is really about:` only when the current ask points to a wider
system question. Do not include `🔧 Fix:`, `➡️ Next:`, or implementation
instructions unless the user asked for action.

For worked examples, use `references/response-patterns.md`.

## Decision-Brief Sub-mode

Use this only when the response is asking the user to choose between options.
Do not use it for normal explanations, plans, status updates, or reviews.

```text
D<N> - <one-line question title>
Project/branch/task: <1 short grounding sentence using available context>
ELI10: <plain English a 16-year-old could follow, 2-4 sentences, name the stakes>
Stakes if we pick wrong: <one sentence on what breaks, what user sees, or what is lost>
Recommendation: <choice> because <one-line reason>
Completeness: A=X/10, B=Y/10   (or: Note: options differ in kind, not coverage - no completeness score)
Pros / cons:
A) <option label> (recommended)
  ✅ <pro - concrete, observable, at least 40 chars>
  ❌ <con - honest, at least 40 chars>
B) <option label>
  ✅ <pro>
  ❌ <con>
Net: <one-line synthesis of what you are actually trading off>
```

D-numbering starts at `D1` within the current skill invocation. It is
model-level numbering, not runtime state.

For real decisions, `ELI10`, `Recommendation`, exactly one `(recommended)`
label, and `Net:` are mandatory. Use completeness scores only when options
differ in coverage. If options differ in kind, write:
`Note: options differ in kind, not coverage - no completeness score.`

Pros / cons use `✅` and `❌`. Minimum 2 pros and 1 con per option when the
choice is real. Hard-stop escape for one-way or destructive confirmations:
`✅ No cons - this is a hard-stop choice`.

## Self-Check Before Emitting

- [ ] The first 1-3 sentences answer the current ask directly.
- [ ] The answer is at the right layer, not stuck on the nearest symptom.
- [ ] The reader does not have to parse a noun stack, hidden actor, undefined
      term, or buried verb to understand the point.
- [ ] Commands, paths, metrics, dates, model names, and technical identifiers
      remain exact.
- [ ] The shape matches the turn: action turns act, explanations do not add
      action tails, decisions use decision-brief format, and tables only appear
      when the renderer can make them clearer.

## Output Expectations

- `answer`: answer the current question in maximum-readability ELI10 style.
- `explain` or `rewrite`: preserve the technical truth while making the prose
  easy to understand.
- `plan`: keep the implementation meaning intact, define jargon, name stakes,
  use action markers where useful, and close with `Net:`.
- `review` or `audit`: lead with findings or the main judgment, then explain
  each issue plainly.
- `status`: say what is true now, what is blocked if anything, and why it
  matters.
- `decision`: use the decision-brief sub-mode.

## Reference Map

- `references/readability-principles.md` - the working-memory model, concrete
  rewrite moves, source-name references, and examples from technical writing.
- `references/response-patterns.md` - rich examples and anti-examples for
  root-cause explanations, system-level reframing, jargon, dense phrase
  rewrites, action tails, path/citation walls, status, plans, and decisions.
- `references/table-rendering.md` - renderer-aware table rules, Codex helper
  usage, Claude-native Markdown guidance, and good/bad examples.
- `scripts/render_codex_table.py` - self-contained `uv` script that renders
  short Unicode tables for Codex and rejects table shapes that would be less
  readable than grouped prose.

Load references when the answer is high-friction, the user asks for a rewrite,
the user is correcting a prior explanation, or you need an example to preserve
the style. Do not treat references as user memory.
