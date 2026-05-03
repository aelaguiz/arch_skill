# Prompt Types And Selection

Use this file when a prompt-writing ask is broader than a reusable agent,
skill, reviewer, or workflow contract.

Prompt types are internal lenses, not user-facing modes. The user can say
"write me a prompt that does this" and still get a good result. Do not require
them to choose a category, fill out a schema, or approve a taxonomy before you
write the prompt.

## First rule: infer, blend, and move

Most real prompts combine several shapes. A support assistant prompt might need
personality, tool-use rules, evidence rules, and stop conditions. A launch-copy
prompt might need creative drafting guardrails, audience constraints, and
source-backed claim rules.

Use this reference to notice what the prompt needs, then write the smallest
prompt that will work.

Good behavior:
- infer the likely prompt shape from the user's plain-language brief
- combine lenses when several are useful
- ask only when a missing detail materially changes the prompt's purpose,
  audience, safety, evidence policy, or output contract
- state assumptions briefly when they matter
- keep one-shot prompts short unless durability, risk, tools, or reuse calls
  for a heavier contract

Bad behavior:
- asking the user to pick a prompt type before doing useful work
- turning the type list into keyword triggers
- inflating every ask into a full system prompt
- blocking because optional product details are missing
- treating examples as a finite menu of allowed prompt shapes

## Lightweight shape for ordinary prompts

For many asks, a compact prompt is enough:

```markdown
You are [role].

Goal: [the outcome the user wants].

Context: [the facts, audience, sources, or constraints that matter].

Instructions:
- [the few behaviors that change quality]
- [evidence, tool, or safety rules when needed]
- [stop condition when needed]

Output: [format, length, tone, or fields].
```

Use the fuller prompt-pattern contract only when the artifact needs durable
reuse, complex tools, validation, examples, or stronger failure handling.

## 1) Reusable prompt contracts

Use when the prompt will be reused, installed, shared, or treated as a durable
agent/skill/reviewer/workflow contract.

Usually needs:
- mission-level identity and success/failure
- non-goals and boundaries
- inputs and ground truth
- tool rules if tools exist
- process, quality bar, output contract, and reject handling
- examples only when they teach judgment

Common failures:
- commander’s intent collapses into a checklist
- examples become the hidden rulebook
- a local incident becomes a universal rule
- the prompt depends on context the runtime cannot access

Use the full `prompt-pattern-contract.md` section model when this shape is
really needed.

## 2) Assistant personality and collaboration prompts

Use when the prompt shapes how an assistant sounds and works with a user over
time.

Usually needs:
- tone, warmth, formality, directness, humor, and polish level
- collaboration style: when to ask, when to assume, when to act, when to stop
- uncertainty behavior
- correction behavior
- boundaries for empathy, confidence, and proactivity

Common failures:
- personality tries to replace task goals, tool rules, or evidence standards
- the assistant becomes chatty because warmth was underspecified
- collaboration style is missing, so the assistant asks too many questions or
  charges ahead when it should not

Keep this short. Personality shapes experience; it should not carry the whole
job.

## 3) Outcome-first task prompts

Use when the user mainly needs the model to accomplish a job, not follow a
fragile step sequence.

Usually needs:
- the desired end state
- success criteria
- constraints and side-effect limits
- available context or sources
- output shape
- stop rules

Common failures:
- process steps are over-specified and narrow the model's search
- strict words like "always" and "never" are used for judgment calls
- the prompt describes activity but not done-ness
- there is no fallback behavior when evidence is missing

Prefer the destination over the route. Use exact sequences only when the
sequence itself is fragile, safety-critical, or part of the product contract.

Codex `/goal` prompts are a common outcome-first variant. They usually also
need evidence, validation, tool-use, and stop-rule lenses because the goal may
guide many future turns. When writing one, use `codex-goal-prompts.md`; keep it
as a compact mission brief, not a fixed schema or duplicated plan doc. The hard
cap is 4,000 characters, complex goals should usually stay around 2,000-3,000,
and rich source docs should be referenced by path instead of restated.

## 4) Retrieval, citation, and evidence prompts

Use when the answer must be grounded in sources, files, records, search
results, policies, or retrieved context.

Usually needs:
- what claims need support
- what counts as acceptable evidence
- how to cite or refer to sources
- when to retrieve more and when to stop
- what to do when evidence is missing
- a rule against turning absence of evidence into a false negative

Common failures:
- the model searches repeatedly to improve wording instead of evidence
- citations support minor wording but not the main factual claim
- missing evidence becomes an invented answer
- the prompt does not distinguish "not found" from "not true"

Write retrieval budgets as stop rules, not as a fixed number of tool calls.

## 5) Creative drafting prompts

Use for copy, slides, summaries for sharing, talk tracks, launch notes,
leadership blurbs, narratives, or other generative drafting tasks.

Usually needs:
- audience, medium, tone, and length
- which facts must come from sources
- what can be creatively phrased
- what claims must not be invented
- placeholders or labeled assumptions for missing specifics

Common failures:
- unsupported product, customer, metric, roadmap, or competitive claims
- invented names or outcomes added to make the draft sound stronger
- source-backed facts and creative framing are mixed with no boundary
- the prompt over-polishes and changes the genre or structure

Separate factual claims from creative expression. Let the model write, but do
not let it invent the evidence.

## 6) Formatting and audience prompts

Use when the main quality lever is how the answer is shaped for a reader,
surface, or artifact.

Usually needs:
- audience level and decision context
- length target or verbosity
- allowed structure
- tone and genre
- what to preserve during rewriting
- what not to add

Common failures:
- formatting becomes heavier than the content
- the model adds sections, claims, or marketing tone during a polish pass
- the answer ignores the user's requested terseness or structure
- audience guidance is vague, such as "make it clear"

Tell the prompt what to preserve before asking for improvement.

## 7) Tool-use and workflow prompts

Use when the model can inspect files, call tools, mutate state, or perform a
multi-step workflow.

Usually needs:
- available tools and their boundaries
- when to call tools and when not to
- side-effect rules
- evidence needed before action
- intermediate user-visible communication when the work may take time
- final answer and receipt expectations

Common failures:
- tool calls become a rigid script instead of evidence-seeking behavior
- the model acts before it has enough context
- the model keeps looping after it can answer
- the prompt hides side effects in vague language

Make the model accountable for outcomes and side effects, not for following a
decorative sequence.

## 8) Validation and check-your-work prompts

Use when the model can verify its output before finalizing.

Usually needs:
- the checks that matter for the artifact
- when validation is required versus best-effort
- what to do if validation cannot run
- what failure should change before the final answer
- what residual risk to report

Common failures:
- "check your work" is generic and produces no real check
- validation is requested but the model has no tool or evidence path
- failed checks are summarized instead of repaired
- the prompt does not say when enough validation is enough

Name concrete checks when the environment makes them knowable. Otherwise,
describe the recognition test and fallback reporting.

## 9) Runtime communication prompts

Use when the user experience depends on what the assistant says before or
during longer work, streaming, tool calls, or background progress.

Usually needs:
- when to send a short preamble or status update
- how long the update should be
- what it should contain
- what should be reserved for the final answer
- how to preserve runtime-specific message labels if the host requires them

Common failures:
- no visible update before a long tool-heavy task
- updates become verbose process narration
- intermediate text is confused with the final answer
- runtime metadata is described in prose when the host has a machine-readable
  field for it

Keep user-visible updates short and useful. Runtime mechanics belong in the
runtime layer when the host provides one.

## 10) Implementation-plan prompts

Use when the model should produce a plan that another engineer or agent can
execute.

Usually needs:
- requirements and where each is addressed
- affected resources, files, APIs, or systems when known
- data flow or state transitions when relevant
- validation commands or checks
- failure behavior and open questions
- privacy, security, or migration constraints when they matter

Common failures:
- the plan is motivational instead of executable
- it names tasks but leaves decisions to the implementer
- it invents schema, fallback, or rollout policy the request did not establish
- it omits validation and acceptance criteria

Plans should be decision-complete enough for the risk level. Do not invent
ceremony when the implementation is straightforward.

## Combining lenses

When a prompt has multiple needs, compose the minimum useful pieces:

- personality + retrieval: tone and collaboration style plus source and stop
  rules
- creative drafting + evidence: clear factual boundaries plus room for good
  prose
- tool-use + validation: action rules plus concrete checks before finalizing
- Codex `/goal`: compact desired world state plus source truth pointers,
  quality bar, evidence, signoff, and stop rule
- formatting + audience: reader context plus structure and length limits
- reusable contract + examples: durable sections plus examples that teach
  reasoning

Do not list every lens in the prompt. The final prompt should feel purpose-built
for the user's job, not like a taxonomy dump.

## Final self-check

- Did the user have to classify their ask? If yes, simplify.
- Did the prompt include only the structure that changes behavior?
- Are evidence, stop rules, tools, validation, personality, and formatting
  present only where they matter?
- Does the prompt state done-ness, not just activity?
- Are examples and types teaching judgment rather than replacing it?
- Would the prompt still handle a new variant of the task tomorrow?
