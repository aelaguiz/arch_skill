# Examples And Anti-Examples

These are adapted from real failures already seen in this repo, but rewritten as portable prompt-authoring patterns. Use them to teach the principle, not to cargo-cult the wording.

## Table of contents

- Case 1: commander's intent collapsed into procedure
- Case 2: one acceptable local move was mistaken for the completion line
- Case 3: examples hardened into a hidden action menu
- Case 4: wrong-layer edits flattened the prompt
- Case 5: phantom context
- Case 6: refactor deleted the useful magic
- Case 7: system context existed in name only
- Case 8: quality bar was too generic to guide judgment
- Case 9: output contract named fields but not validity
- Case 10: prompt-type diagnosis leaked to the user
- Case 11: outcome-first prompt got buried under process
- Case 12: creative drafting invented unsupported claims
- Case 13: validation was requested but not made real
- Case 14: goal prompt became a form or competing source of truth
- Case 15: execution goal softened into a non-completion report
- Case 16: the agent's restatement replaced the source
- Case 17: verdict token, SHA pin, and scope fence made the review narrow
- How to use these examples safely

## Case 1: commander’s intent collapsed into procedure

Real failure pattern:
- the prompt tried to make commander’s intent own the exact interaction script instead of the outcome

Bad shape:
- "Always summarize the request, ask two clarifying questions, propose the plan, and end with next steps."

Better shape:
- "Help the user leave with a clearer decision, a stronger prompt, or a sharper diagnosis. Use judgment about how to get there; the process details belong lower in the prompt."

Why the better shape works:
- the mission stays high-level
- specific behaviors can still live lower in success/failure, process, or examples

Transferable principle:
- commander’s intent should describe the improved world state, not the menu of moves

## Case 2: one acceptable local move was mistaken for the completion line

Real failure pattern:
- the prompt rewarded the first locally correct move even when one more obvious in-scope improvement was still left

Bad shape:
- "Once you produce a correct answer, finish."

Better shape:
- "After the first acceptable move, ask whether one more obvious in-scope improvement would materially strengthen the result before returning."

Why the better shape works:
- it preserves autonomy
- it teaches completion-line judgment instead of a brittle finish rule

Transferable principle:
- prompts should teach what done means, not just how to start

## Case 3: examples hardened into a hidden action menu

Real failure pattern:
- examples started functioning like the actual rulebook instead of illustrations

Bad shape:
- "Choose from these response types: summarize, escalate, defer, reject."

Better shape:
- "Use examples only to show what smart action can look like. The real rule is the recognition test and the desired outcome."

Why the better shape works:
- new cases can still be handled correctly
- examples stay illustrative rather than exhaustive

Transferable principle:
- examples should illuminate judgment, not replace it

## Case 4: wrong-layer edits flattened the prompt

Real failure pattern:
- the same shared wording was pasted everywhere, washing out role identity and section ownership

Bad shape:
- one generic block tries to carry mission, process, and role-specific rules for every surface

Better shape:
- shared mission stays high-level
- role identity stays in identity and system-context sections
- process and examples stay lower

Why the better shape works:
- each section owns one kind of reasoning
- the prompt keeps both coherence and personality

Transferable principle:
- fix the highest section that owns the problem before rewriting the lower ones

## Case 5: phantom context

Real failure pattern:
- prompts referenced files or docs the runtime could not actually access

Bad shape:
- "Use the design doc, the meeting notes, and the internal write-up when deciding."

Better shape:
- "Bundle the needed doctrine into the skill or paste the binding context into the prompt."

Why the better shape works:
- the prompt becomes portable
- the model is not asked to rely on invisible context

Transferable principle:
- never make a prompt depend on context that is not actually present

## Case 6: refactor deleted the useful magic

Real failure pattern:
- a refactor replaced a vivid, effective prompt with a generic template and lost the behavior that made the original work

Bad shape:
- "Replace the whole prompt with the standard template so everything is uniform."

Better shape:
- "Keep the useful behavior, extract the principle that makes it work, and relocate brittle wording into examples, rationale, or litmus tests instead of deleting it."

Why the better shape works:
- it preserves the prompt's strengths
- it upgrades structure without flattening tone or judgment

Transferable principle:
- refactoring should preserve durable behavior while removing brittle expression

## Case 7: system context existed in name only

Real failure pattern:
- the prompt had a section named `System context`, but it did not explain what the output becomes or why quality matters

Bad shape:
- "This prompt supports the review workflow."

Better shape:
- "This output becomes the brief users read before making a decision. They will use it under time pressure. If it hides the key tradeoff or invents certainty, the next decision goes wrong."

Why the better shape works:
- it ties the work to a real user or downstream moment
- it gives the model a reason to care about quality beyond formatting

Transferable principle:
- system context should create stakes, not just name the surrounding system

## Case 8: quality bar was too generic to guide judgment

Real failure pattern:
- the prompt asked for high quality but never defined what strong output looks like or what weak output does wrong

Bad shape:
- "Be clear, concise, and useful."

Better shape:
- "Strong output names the real decision, cites the strongest available evidence, and surfaces the main uncertainty without padding. Weak output is generic, overconfident, or technically correct but not decision-useful."

Why the better shape works:
- it gives the model a contrastive target
- it makes quality downstream-useful rather than ornamental

Transferable principle:
- quality bars should describe the real win condition and the real failure mode

## Case 9: output contract named fields but not validity

Real failure pattern:
- the prompt listed fields to return, but never explained how to validate them or when to reject

Bad shape:
- "Return title, summary, recommendation, and confidence."

Better shape:
- "Return `title`, `summary`, `recommendation`, and `confidence`. `recommendation` must be one clear action. `confidence` must match the evidence quality. Reject only when the core artifact required for a responsible answer is missing; ordinary uncertainty belongs inside the answer."

Why the better shape works:
- it distinguishes formatting from correctness
- it prevents the prompt from turning ordinary ambiguity into a false failure

Transferable principle:
- output contracts should define validity and reject semantics, not just field names

## Case 10: prompt-type diagnosis leaked to the user

Real failure pattern:
- the author made the user choose a prompt type before writing the prompt

Bad shape:
- "Which mode should I use: personality, retrieval, drafting, validation, or workflow?"

Better shape:
- "Infer the needed shape from the brief. If the user asks for a friendly assistant that searches docs and cites sources, write one prompt that blends collaboration style, retrieval rules, citation behavior, and completion conditions."

Why the better shape works:
- the taxonomy stays internal
- casual prompt-writing asks keep moving
- mixed prompts get the useful parts of several lenses

Transferable principle:
- prompt types are diagnostic lenses, not gates the user must pass through

## Case 11: outcome-first prompt got buried under process

Real failure pattern:
- a simple task prompt became a long sequence of steps that narrowed the model's judgment

Bad shape:
- "First inspect every input, then list all possible actions, then compare each option, then choose, then write a summary, then verify the summary."

Better shape:
- "Resolve the user's issue end to end. Success means the decision is made from available evidence, allowed actions are completed, missing required facts are requested narrowly, and the final answer states what was done and what evidence supports it."

Why the better shape works:
- it defines done-ness instead of activity
- it leaves room for the model to choose an efficient path
- it still gives concrete success criteria

Transferable principle:
- prompt the destination unless the route is genuinely fragile

## Case 12: creative drafting invented unsupported claims

Real failure pattern:
- a copywriting prompt encouraged polish but did not protect factual claims

Bad shape:
- "Write a punchy launch blurb that makes the product sound like the market leader."

Better shape:
- "Write a concise launch blurb using only provided facts for product capabilities, customer claims, metrics, roadmap status, and competitive comparisons. You may make the language vivid, but use placeholders or labeled assumptions for missing specifics."

Why the better shape works:
- it separates creative phrasing from evidence-backed claims
- it prevents stronger-sounding but unsupported facts

Transferable principle:
- drafting prompts need factual boundaries when the prose can create false confidence

## Case 13: validation was requested but not made real

Real failure pattern:
- the prompt asked the model to check its work without saying what checking means

Bad shape:
- "Make sure the implementation is correct before answering."

Better shape:
- "After changing code, run the most relevant available validation: targeted tests for changed behavior, type checks or lint when applicable, and a build check if the affected package has one. If the obvious validation path is unavailable, use the next best evidence."

Why the better shape works:
- the model has a real check path
- failures and missing validation become visible instead of hand-waved

Transferable principle:
- validation prompts should name concrete checks or recognition tests, not just ask for confidence

## Case 14: goal prompt became a form or competing source of truth

Real failure pattern:
- a Codex `/goal` prompt was rewritten into a fixed field list, so the future
  agent followed labels without understanding the desired world state
- or a rich plan/source doc was copied into the goal, so the goal became a
  second source of truth that could drift from the real plan

Bad shape:
- "Outcome: fix it. Source: repo. Workflow: use skills. Evidence: tests. Done:
  reviewer signs off."
- a Markdown prompt file or 4,000-character paste-sized goal that pastes the
  whole plan doc, every thought exercise, the reviewer prompt, and the detailed
  test list

Better shape:
- "Fix the current lesson issue through the owning workflow, not by patching
  around it. The learner-facing behavior should be actually correct, the skill
  architecture should remain intact, and the fix should survive quality review.
  Use owner skill readbacks and live surfaces as source truth; stale reports are
  context only. Do not use heuristic backfills or fake receipts. Done requires
  the original failure, owner-path fix, validation receipt, and any required
  blind review."
- "Implement the work described in `docs/PLAN.md`. That doc is controlling
  source truth for doctrine, examples, fixtures, and validation details; do not
  restate it or create a second plan. Done requires the implementation,
  validation against the named fixtures, non-leading signoff, and a final report
  with changed files, commands, artifacts, signoff result, and risks."

Why the better shape works:
- the mission is visible before mechanics
- the quality bar teaches judgment
- source truth, forbidden shortcuts, evidence, and signoff still exist, but
  they serve the outcome instead of becoming a checklist
- rich docs stay authoritative instead of being copied into a brittle goal
- rich goals can live in Markdown prompt files, while paste-sized `/goal` text
  stays inside the 4,000-character hard cap and usually closer to the
  2,000-3,000 character working range

Transferable principle:
- goal prompts should be adaptive mission briefs; use structure only where it
  makes the goal easier to pursue
- when a source doc exists, the goal should point to it and define acceptance,
  not duplicate it

## Case 15: execution goal softened into a non-completion report

Real failure pattern:
- a user asked for a system to work, but the prompt author added language that
  made a diagnosis, refusal, disagreement, or obstacle summary look like a valid
  ending
- review or model consensus was framed as a way to certify non-completion rather
  than a way to choose the next experiment or repair

Bad shape:
- "Diagnose why RTS fails and finish if the issue is rare, hard to reproduce, or
  reviewers disagree."
- "Done means either the work is fixed or the final report names a precise
  non-completion reason."

Better shape:
- "Make RTS work on this class of hands. H0050 is the probe, not the prize. Use
  source truth, whole-hand replay, theory-disproving tests, instrumentation,
  paper-aligned algorithm checks, and model consensus to choose the next repair.
  A refusal, rarity claim, narrow diagnosis, or reviewer objection is not done;
  it becomes the next evidence packet. Done means the production path is
  repaired, focused tests pass, and reviewers agree the engine-quality fix
  satisfies the goal."

Why the better shape works:
- the desired world state stays operational
- uncertainty creates the next action instead of an ending
- review and consensus drive the search instead of narrowing it up front
- the proof gate requires the system to work, not just the report to sound
  precise

Transferable principle:
- execution goals should make non-completion language hard to use. If the user
  wants the system working, done means the system works and the evidence proves
  it.

## Case 16: the agent's restatement replaced the source

Real failure pattern:
- an agent held the full planning workbook and the plan, then sent the
  expert reviewer a 25KB brief that pasted the issue body verbatim plus its
  own test output, and asked it to assess "on that accepted scope"
- the reviewer answered well about the issue and said so: "the verdict
  applies only to the RED-suite deliverable"; the user reran the same review
  with the workbook attached and got a different answer
- the agent's pre-send check was a dispatch-dimension checklist ("original
  user correction quoted; same architect/thread"), which the brief passed

Bad shape:
- "Final review of PR #5970 against the accepted scope in the attached
  issue. Judge the PR against that scope. Test output attached."
- a brief with `Goal`, `Context`, `Instructions`, and `Output` headings whose
  context section is the agent's summary of the sources

Better shape:
- "We're working on Dynamic Missions; the sheet we've been working out of is
  attached, full export, and the plan is attached. I've been working out of
  branch X; here's PR #5970, @GitHub, read the latest. The
  issue I picked up was #5949. What I did: ... I think I'm done. Where I'm
  least sure: ... What I'm looking for: did I implement the intent right, and
  is this the cleanest, most pragmatic way to do it? Read the plan and the
  sheet first, then the PR."

Why the better shape works:
- the reviewer reads the source the user reads, so its answer can match his
- the status is a belief the reviewer can overturn
- the question is about intent, so an issue that got the intent wrong is in
  reach
- the moves are sentences, so the brief reads like a colleague, not a form

Transferable principle:
- narrowing the work never narrows what the reviewer sees. Attach the
  canonical source whole; the agent's restatement is not evidence.

## Case 17: verdict token, SHA pin, and scope fence made the review narrow

Real failure pattern:
- across a 621-prompt corpus, six in ten review briefs asked for a verdict
  token, one in three capped the answer, one in four fenced what the reviewer
  could conclude, and nearly all pinned a commit SHA
- the reviewer produced the token, the cap, and the fence, and the agent
  reported "Pro passed it" while the user's own review of the same PR found
  real problems

Bad shape:
- "Review PR 4734 at exact head 57eb43e4 against the approved plan. Return
  APPROVED only if this exact head is correct, complete, minimal, and
  merge-ready; otherwise return CHANGES REQUIRED with only blocking in-scope
  defects. Do not require RustAI, Patrol, Flutter work, or any other adjacent
  milestone scope."
- "Judge only whether each of the five findings is now resolved. First line
  PASS or CHANGES REQUIRED, then one line per finding."

Better shape:
- "Here's the PR; read the latest. Where am I introducing risk that really
  wasn't necessary? Where did I overbuild around edge cases? Where did I
  create new patterns where there were existing clean ones, split brain, or
  a web of individual calls instead of one clear abstraction? Where am I
  working around an architectural limitation I should tackle first? If the
  issue itself got the intent wrong, say so. Whatever you find, I'll fix and
  bring back."

Why the better shape works:
- the reviewer reads the whole PR as it is, not a frozen head
- the reviewer decides what matters; the agent writes the verdict afterward
- the question names the kinds of problems the user actually finds, so the
  answer covers them
- nothing forbids the reviewer from saying the scope is wrong

Transferable principle:
- a token, a cap, a fence, or a pin each trades a real review for an easy
  summary. The agent owns the summary; the reviewer owns the review.

## How to use these examples safely

- Prefer the principle over the wording.
- If you borrow an example, say why it works.
- If the example starts feeling like a lookup table, extract the higher-level rule instead.
