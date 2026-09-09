---
name: eline
description: "Answer, explain, or rewrite in ELINE style (Explain Like I'm a New Engineer): brief a competent engineer who is new to this system and short on time, the way a subsystem's owner explains it to a peer on another team. Assume college-level CS and common industry vocabulary; never define or metaphor-ize standard concepts. Gloss system-specific names by engineering role, collapse off-path components to their interface, and layer depth: thesis, high-level setup, then the problem area with its critical evidence. Add exact identifiers only when the ask calls for that depth; otherwise close with the questions the reader would ask next. Use for `$eline`, 'explain it like I'm new to the team', engineer-level summaries of bugs, incidents, decisions, PRs, or plans, or 'give me the gist and I'll dig in'. Not for non-engineer plain English with analogies (use `eli10`) or report artifacts like weekly reports (use `readable-reports`), and not the task owner: it shapes the answer; the underlying work owns the substance."
metadata:
  short-description: "Brief a peer engineer who is new to the system"
---

# ELINE: The Peer Briefing

Use this skill as a response style for the user's current ask. It shapes how
the answer is written. It does not change which skill, workflow, tool, or
safety rule owns the underlying work.

## Mission

Write the way the engineer who owns a subsystem explains it, in a hallway, to a
strong engineer from the next team over. That reader has the vocabulary but not
the map. They will follow up on whatever matters to them, so the first answer
has to make the whole thing parsable at a glance, put the problem area in
focus, and keep the fine detail ready rather than front-loaded.

Great ELINE output:

- states the thesis and its mechanism in the first one or two sentences
- sets up the system in engineering-category words, so the reader can place
  every component without a glossary
- spends most of its length on the problem area, with the few pieces of
  evidence that make the thesis falsifiable
- gives exact identifiers and edge-case nuance only when the ask calls for
  that depth
- ends with the questions the reader would ask next, so the follow-up is one
  line away
- keeps every number, name, and failure mode true

Weak ELINE output:

- explains what a token, a retry, a cache, or a race condition is
- introduces a cast, characters, or a metaphor to stand in for components
  ("the errand-runner", "a stage crew")
- opens with file paths, class names, PR numbers, or house codenames before
  the reader knows what the system does
- dumps identifiers and config values on a reader who asked for the gist, or
  withholds the one detail that makes the thesis believable
- pads with process history, hedges, or a plan nobody asked for

## The Reader

Write for one person: a competent software engineer who does not work on this
system and has a few minutes.

- They know college-level CS and common industry practice: data structures,
  concurrency, networking, HTTP, auth flows, databases and migrations, caching,
  queues, retries and backoff, feature flags, CI, observability. Do not explain
  these. Do not replace them with analogies.
- They do not know this codebase, this product's domain terms, this team's
  acronyms, or which of ten similar-sounding services does what. Gloss those
  once, by engineering role.
- They are not junior. "New engineer" means new to the system, not new to
  engineering.
- They will ask follow-ups. Design the first answer so the follow-ups are
  obvious and cheap.

## When To Use

- The user asks for `$eline`, ELINE, "explain it like I'm new to the team",
  "engineer-level summary", "the gist", "what would you tell a new hire",
  "brief me", or "assume I can code but don't know this repo".
- The user wants a bug, incident, root cause, design decision, tradeoff, PR,
  plan, or status explained to someone who has to act on it without studying
  it.
- The user wants prose rewritten so an engineer outside the system can parse
  it in one read.
- The user is reacting to an explanation that was either too simplified
  (analogies, defined basics) or too specific (repo trivia up front).

## When Not To Use

- The reader is not an engineer, or the user asked for `eli10`, ELI10, ELI16,
  or "plain English". That lane defines jargon and may use analogies; this one
  assumes the vocabulary.
- The deliverable is a report artifact: a morning, weekly, delivery, or audit
  report, a deck, or sheet notes. `readable-reports` owns that form; ELINE can
  shape an explanatory section inside it.
- The answer must be exact code, JSON, YAML, config, a schema, or quoted
  output. Keep exact material exact and use ELINE prose only around it.
- The user asked for the exhaustive or audit-grade version. Coverage skills own
  that; ELINE is the compression, not the audit.
- The substance is not resolved yet. Do the investigation, review, or
  implementation first, under whatever skill owns it, then write the answer in
  this style.

## Non-Negotiables

- Resolve the substance before shaping it. Never let the layering hide that a
  fact is unknown; say "not established" and what would establish it.
- Keep exact truth exact: numbers that carry the argument, names, dates,
  versions, and failure modes must survive compression. Round only what does
  not carry weight.
- Hold the vocabulary floor. Standard CS and industry terms are assumed.
  System-specific names get one role gloss on first use, then the real name.
  No cast lists, no metaphors, no "think of it as".
- Collapse, don't narrate. Components off the problem's path are named by
  their interface ("the backend validates the token and returns the puzzle"),
  not explained.
- Layer the depth. Thesis, setup, problem area. Identifiers, paths, and config
  values appear only when the ask calls for that depth, and then only for the
  piece the reader must trust.
- Put evidence after the claim it supports, and keep it to what makes the
  thesis falsifiable. A timestamp pair, a count, one log line, or one code fact
  beats a citation wall.
- Mark confidence in plain words: confirmed, inferred, or unknown. Do not
  upgrade an inference by phrasing.
- End with dig handles, not next steps. Name what the reader could ask next
  and what is behind each question. Add a plan or action only when the user
  asked for one.
- Do not pretend to remember earlier sessions or hidden preferences. Use the
  current conversation and inspected artifacts.

## The Vocabulary Floor

Three buckets. Decide each term's bucket before writing.

- **Assumed.** Standard CS and industry vocabulary. Use it plainly: race
  condition, idempotent, backoff, TTL, JWT, p95, cache invalidation, cron,
  pub/sub, migration, feature flag, kill switch, circuit breaker, 429, OAuth,
  WebSocket, ORM.
- **Glossed.** Anything the reader could not look up: service names, package
  names, product-domain terms, team acronyms, internal codenames. Pattern: real
  name, then its engineering role and the one contract fact that matters here.
  "RustAI, the Rust service that returns the AI's action for a hand; stateless
  HTTP, one call per decision." After the gloss, keep the real name.
- **Collapsed.** Internals on the periphery of the problem. Replace the chain
  with the role of the whole: "our auth gateway" for the wrapper, its cache,
  and its refresh scheduler. Expand only if the reader digs there.

If a sentence in the setup would make a strong outside engineer ask "what is
that", it needs a gloss. If it would make them think "I know what a retry is",
it needs cutting.

`references/vocabulary-floor.md` has fuller lists, gloss patterns, and the
acronym and product-domain rules.

## The Depth Ladder

Every ELINE answer moves through the first three layers in order. The fourth
is conditional. Proportion matters more than exact length; the first three
layers should fit on one screen.

- **L0, thesis.** One or two sentences: what is true or decided, and the
  mechanism in one clause. This is the sentence the reader will repeat to
  someone else.
- **L1, setup.** The system in engineering-category words: what it is for, the
  two to four components on the problem's path with the contract between them,
  and the normal flow. Everything else is collapsed. No paths, class names, PR
  numbers, or codenames here.
- **L2, problem area.** Most of the answer. Which contract broke, or which
  constraint forces the decision, at the level of interfaces, state, ordering,
  ownership, and timing. Then the critical evidence, placed after the claim,
  with confidence marked. This is where the reader should feel the mechanism
  click.
- **L3, narrow nuance, only when the ask calls for it.** Exact identifiers,
  config values, file or function names, and edge branches, for the one piece
  the reader must trust. Include it when the user asks what exactly changed,
  which setting, which file or line, or for the code path; when the reader
  will act on the identifier, such as a reviewer checking a diff or an on-call
  flipping a flag; or when the question is already at that depth, such as a
  follow-up that names a component. Otherwise omit L3 entirely. A number that
  carries the argument is L2 evidence, not L3.
- **Dig handles.** Two to four lines: the questions the reader would ask next,
  each with a one-line pointer to what the answer contains. When L3 was
  omitted, the handles are where the reader learns it exists. Not next steps.

`references/worked-examples.md` shows one incident written as cast-and-metaphor,
as repo soup, and as ELINE, with the layers labeled and the L3 decision shown.

## Follow-Ups: Descend, Don't Restart

When the reader digs in, go one layer deeper on the piece they asked about and
nothing else.

- Do not repeat the setup. Reference it in half a sentence if needed.
- Keep the floor. New proper nouns still get their role gloss.
- Bring the L3 material for that piece: the identifier, the config value, the
  exact branch, the exact log line. A follow-up is the usual way L3 arrives.
- If the answer is not established, say so and name the evidence that would
  settle it.
- If the question reveals the thesis was wrong, say that first, then re-layer.

## Writing Moves

Compact readability rules this skill relies on. They are the same craft as any
good technical writing; the floor and the ladder are what make it ELINE.

- The first sentence carries the answer, not the windup.
- Name the actor: which component did what to which.
- Prefer verbs to nominalizations: "the gateway times out", not "a timeout
  occurs at the gateway layer".
- Two-noun compounds are fine. Three or more stacked nouns get unpacked with a
  relation word or split.
- Start sentences with what the reader already has; end with the new point.
- Cut hedges without a measurement and minimizers like "just" and "simply".
- Numbers appear only where they carry the argument, and then they are exact.
- No emoji markers. Plain paragraphs by default; short bold labels or headings
  for the layers only when the answer runs past a screen. Bullets for parallel
  items. Tables only for compact grids.

## Shape By Ask

- **Bug or incident.** L0 is cause plus mechanism. L1 is the system on the
  failure path. L2 is the broken contract and the timeline evidence. L3, when
  the ask names the fix or the gate, is the specific setting or line. Handles
  cover what it does not explain and how it is proven.
- **Design decision or tradeoff.** L0 is the decision and the constraint that
  forces it. L1 is the systems it touches. L2 is the tradeoff with evidence and
  a recommendation stated, not hedged. L3, when asked, is the mechanism of the
  chosen option.
- **PR or handoff for an outside reviewer.** L0 is what changes for callers or
  users. L1 is which components. L2 is the non-obvious part the reviewer must
  check and how it is proven. L3 is usually warranted here, because the
  reviewer acts on the diff.
- **Status.** L0 is the state now and the blocker. Skip L1 unless the reader
  is new to the work. L2 is what is proven versus assumed. Handles instead of
  a plan.
- **"What is this system".** L0 is its purpose. L1 is components and
  contracts. L2 is the part that surprises people. No L3 unless asked.
- **Decision the user must make.** Recommendation first, then each option with
  its one real tradeoff in the same layered style. No scoring template.

## Workflow

1. Resolve the substance under whatever skill or work owns it. ELINE shapes
   the answer; it does not replace investigation.
2. Name the reader's map gap: which components and contracts they need to
   place the problem, and nothing more.
3. Trace the problem's path through the system. Everything on the path gets a
   role; everything off it is collapsed.
4. Sort every term into assumed, glossed, or collapsed.
5. Decide whether the ask calls for L3. If it does not, plan to omit it.
6. Write L0, then L1, then L2 with evidence and confidence, then L3 only if
   step 5 said so.
7. Write the dig handles from the questions a strong outside engineer would
   actually ask.
8. Run the self-check, then cut anything the reader does not need in order to
   act.

## Self-Check Before Emitting

- [ ] The first two sentences state the thesis and its mechanism.
- [ ] A strong engineer from another company could read L0 and L1 without
      asking what a word means, and without being told what a retry, token,
      cache, or flag is.
- [ ] No analogy, cast, character, or "think of it as" anywhere.
- [ ] L1 contains no file path, class name, PR number, or house codename.
- [ ] Every component off the problem's path is collapsed to its interface.
- [ ] The evidence in L2 is enough to falsify the thesis and no more, and
      confidence is marked.
- [ ] L3 appears only because the ask called for it; otherwise it is omitted
      and the handles cover it.
- [ ] Numbers, names, dates, and failure modes are exact.
- [ ] The answer ends with handles, not a plan, unless a plan was requested.

## Output Expectations

- `answer` or `explain`: the layered briefing above.
- `rewrite`: preserve every fact in the source; re-sort terms into the three
  buckets; re-layer; strip analogies and front-loaded identifiers.
- `handoff` or `pr summary`: the briefing shaped for an outside reviewer,
  usually with L3; the owning skill still publishes.
- `status`: state now, blocker, proven versus assumed, handles.
- `decision`: recommendation first, options with one real tradeoff each, same
  layers.

## Reference Map

- `references/vocabulary-floor.md`: assumed, glossed, and collapsed term
  lists; gloss patterns; acronym and product-domain rules; the two failure
  directions.
- `references/worked-examples.md`: one incident written three ways with layers
  labeled and the L3 decision shown; a follow-up exchange; a rewrite from repo
  soup; a design decision.

Load references when the answer is high-friction, the user asks for a rewrite,
or the previous explanation missed the floor in either direction.
