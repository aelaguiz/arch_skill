---
name: eline
description: "Answer, explain, summarize, or rewrite in ELINE style (Explain Like I'm a New Engineer): brief a strong engineer who is new to this system and short on time, the way a subsystem's owner explains it to a peer on another team. Assume standard CS and industry vocabulary; define nothing standard and use no metaphors. Gloss system-specific names by engineering role, collapse off-path components to their interface, and layer depth: thesis, setup, then the problem area with its critical evidence. Add exact identifiers only when the reader will act on them; otherwise close with the questions they would ask next. Use for `$eline`, 'explain it like I'm new to the team', 'assume I can code but don't know this repo', 'onboard me to X', 'TL;DR this for an engineer', and engineer-level summaries of bugs, incidents, decisions, plans, or PRs for an outside reviewer. Not for non-engineer plain English (use `eli10`) or status and delivery reports to be posted (use `readable-reports`); a response style, not the task owner."
metadata:
  short-description: "Brief a strong engineer who is new to the system"
---

# ELINE: The Peer Briefing

Use this skill as a response style for the user's current ask, and keep it in
force for the rest of the conversation unless the user asks for a different
style. It shapes how the answer is written. It does not change which skill,
workflow, tool, or safety rule owns the underlying work.

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
- is much shorter than its source material
- ends with the questions the reader would ask next, so the follow-up is one
  line away

Weak ELINE output:

- explains what a token, a retry, a cache, or a race condition is
- introduces a cast, characters, or a metaphor to stand in for components
  ("the errand-runner", "a stage crew")
- opens with file paths, class names, PR numbers, or house codenames before
  the reader knows what the system does
- dumps column names, log labels, and config paths on a reader who asked for
  the gist, or withholds the one detail that makes the thesis believable
- runs as long as the document it was supposed to compress

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
  "assume I can code but don't know this repo", "onboard me to X", "TL;DR this
  for an engineer", "what do I need to know before I touch X", "brief me", or
  "give me the gist and I'll dig in".
- The user wants a bug, incident, root cause, design decision, tradeoff, PR,
  plan, or status explained to an engineer who has to act on it without
  studying it, including a PR summary for a reviewer on another team.
- The user wants prose rewritten so an engineer outside the system can parse
  it in one read.
- The user is reacting to an explanation that was either too simplified
  (analogies, defined basics) or too specific (repo trivia up front).

## When Not To Use

- The reader is not an engineer, or the user asked for `eli10`, ELI10, ELI16,
  or "plain English". That lane defines jargon and may use analogies; this one
  assumes the vocabulary.
- The deliverable is a status or delivery report to be posted: a morning,
  weekly, or delivery report, an audit summary, a deck, or sheet notes.
  `readable-reports` owns that form. A status or incident explained in
  conversation, or an incident write-up for engineers, is ELINE.
- The answer must be exact code, JSON, YAML, config, a schema, or quoted
  output. Keep exact material exact and use ELINE prose only around it.
- The user asked for the exhaustive or audit-grade version. A coverage skill
  such as `exhaustive-code-review` owns that; ELINE is the compression, not
  the audit.
- The substance is not resolved yet. Do the investigation, review, or
  implementation first, under whatever skill owns it, then write the answer in
  this style.

## Non-Negotiables

- Resolve the substance before shaping it. Never let the layering hide that a
  fact is unknown; say "not established" and what would establish it.
- Keep exact truth exact: names, dates, versions, and failure modes survive
  compression. Numbers that carry the argument are exact; other numbers are
  rounded or dropped.
- Hold the vocabulary floor below. No cast lists, no metaphors, no "think of
  it as".
- Collapse, don't narrate. Components off the problem's path are named by
  their interface ("the backend validates the token and returns the puzzle"),
  not explained.
- Put evidence after the claim it supports, state it as facts, and keep it to
  what makes the thesis falsifiable. Mark confidence in plain words:
  confirmed, inferred, or not established. Do not upgrade an inference by
  phrasing.
- End with dig handles, not next steps. Add a plan or action only when the
  user asked for one.
- No emoji markers, no layer names shown to the reader, plain paragraphs by
  default. Short bold labels or headings only past about 400 words; bullets
  for parallel items; tables only for compact grids.

## The Vocabulary Floor

Three buckets. Decide each term's bucket before writing.

- **Assumed.** Standard CS and industry vocabulary. Use it plainly: race
  condition, idempotent, backoff, TTL, JWT, p95, cache invalidation, cron,
  pub/sub, migration, feature flag, kill switch, circuit breaker, 429, OAuth,
  WebSocket, ORM.
- **Glossed.** Anything the reader could not look up: service names, package
  names, product-domain terms, team acronyms, internal codenames. Pattern: real
  name, then its engineering role and the one contract fact that matters here.
  "`ledger-svc`, the Go service that owns account balances; every debit is one
  gRPC call to it." After the gloss, keep the real name.
- **Collapsed.** Internals on the periphery of the problem. Replace the chain
  with the role of the whole: "our auth gateway" for the wrapper, its cache,
  and its refresh scheduler. Expand only if the reader digs there.

If a sentence in the setup would make a strong outside engineer ask "what is
that", it needs a gloss. If it would make them think "I know what a retry is",
it needs cutting.

`references/vocabulary-floor.md` has fuller lists, gloss patterns, and the
acronym and product-domain rules.

## The Depth Ladder

An ELINE answer moves through the first three layers in order unless Shape By
Ask or Follow-Ups says to skip one. The fourth is conditional. The layer
names are for you; the reader never sees "L0" or "L3".

- **L0, thesis.** One or two sentences: what is true or decided, and the
  mechanism in one clause. This is the sentence the reader will repeat to
  someone else.
- **L1, setup.** The system in engineering-category words: what it is for, the
  two to four components on the problem's path with the contract between them,
  and the normal flow. Everything else is collapsed. Glossed component names
  belong here; identifiers do not: no paths, class or function names,
  columns, log labels, config keys, commit hashes, or PR numbers.
- **L2, problem area.** Most of the answer. Which contract broke, or which
  constraint forces the decision, at the level of interfaces, state, ordering,
  ownership, and timing, naming which component did what to which. Then the
  critical evidence, placed after the claim,
  with confidence marked. Evidence is stated as facts: a count, a timestamp
  pair, a status code, what a test asserts. The column, file, log label, or
  test name that carries the fact belongs in L3.
- **L3, narrow nuance.** Exact identifiers, config values, file or function
  names, and edge branches, for the one piece the reader must trust. Include
  L3 when the reader will act on the identifier. The ask's wording tells you
  (what exactly changed, which setting, which file or line, the code path), or
  its shape does (a reviewer checking a diff, an on-call flipping a flag, a
  follow-up that names a component). Otherwise omit it entirely. A number that
  carries the argument is L2 evidence, not L3.
- **Dig handles.** Two to four lines: the questions the reader would ask next,
  each with a one-line pointer to what the answer contains. When L3 was
  omitted, the handles are where the reader learns it exists. Not next steps.

Budget: L0 through L2 in roughly 250 to 400 words. A reader who says they have
no time gets the low end. Past that, every sentence must buy believability,
not completeness. The answer should be far shorter than the material it
compresses; if it is not, the setup is narrating or L2 is carrying L3.

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

## Shape By Ask

- **Bug or incident.** L0 is cause plus mechanism. L1 is the system on the
  failure path. L2 is the broken contract and the timeline evidence. Handles
  cover what it does not explain and how it was proven.
- **Design decision, made or under analysis.** L0 is the decision and the constraint that
  forces it. L1 is the systems it touches. L2 is the tradeoff with evidence and
  a recommendation stated, not hedged.
- **PR or handoff for an outside reviewer.** L0 is what changes for callers or
  users. L1 is which components. L2 is the non-obvious part the reviewer must
  check and how it is proven. L3 is usually warranted, because the reviewer
  acts on the diff. The owning skill still publishes.
- **Status.** L0 is the state now and the blocker. Skip L1 unless the reader
  is new to the work. L2 is what is proven versus assumed. Handles instead of
  a plan.
- **"What is this system".** L0 is its purpose. L1 is components and
  contracts. L2 is the part that surprises people.
- **Rewrite.** Preserve every fact in the source; re-sort terms into the three
  buckets; re-layer; strip analogies and front-loaded identifiers.
- **Decision the user must make now.** Recommendation first, then each option with
  its one real tradeoff, in the same layers. No scoring template.

## Workflow

1. Resolve the substance under whatever skill or work owns it. ELINE shapes
   the answer; it does not replace investigation.
2. Name the reader's map gap: which components and contracts they need to
   place the problem, and nothing more.
3. Trace the problem's path through the system. Everything on the path gets a
   role; everything off it is collapsed.
4. Sort every term into assumed, glossed, or collapsed.
5. Decide L3 with the one test: will the reader act on the identifier?
6. Write L0, then L1, then L2 with evidence and confidence, then L3 only if
   step 5 said yes. Then the dig handles.
7. Cut to budget. Remove anything the reader does not need in order to act.

## Self-Check Before Emitting

- [ ] A strong engineer from another company could read L0 and L1 without
      asking what a word means and without being told what a retry, token,
      cache, or flag is. No analogy, cast, or "think of it as" anywhere.
- [ ] No identifier (path, class or function name, column, log label, config
      key, hash, PR number) outside L3, and L3 is present only because the
      reader will act on it. Glossed component names are not identifiers.
- [ ] L0 through L2 fit the budget and are far shorter than the source.
- [ ] Evidence is the falsifying minimum, stated as facts, with confidence
      marked.
- [ ] The answer ends with handles, not a plan, unless a plan was requested.

## Reference Map

- `references/vocabulary-floor.md`: assumed, glossed, and collapsed term
  lists; gloss patterns; acronym and product-domain rules; the two failure
  directions.
- `references/worked-examples.md`: one incident written three ways with layers
  labeled and the L3 decision shown; a follow-up exchange; a rewrite from repo
  soup; a design decision.

SKILL.md is sufficient on its own. Load a reference when a self-check item
fails, the user asks for a rewrite, or the previous explanation missed the
floor in either direction.
