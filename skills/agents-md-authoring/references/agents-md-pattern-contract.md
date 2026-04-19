# AGENTS.md Pattern Contract

Use this file when deciding what a strong repo `AGENTS.md` must contain, what it must not do, and where each class of guidance belongs.

## Table of contents

- Start from cold-start failure modes
- What a great AGENTS.md must do
- Ownership by layer
- Fatal anti-patterns
- Symptom-to-fix map
- Final self-check

## Start from cold-start failure modes

Write `AGENTS.md` from the perspective of a fresh coding agent that has not yet built a repo mental model.

That agent needs repo truth, not author narration. Do not spend budget on how the file was planned, why the writer chose this structure, or what a future cleanup pass might do.

That agent needs to learn, quickly:

- what command proves the repo is healthy
- what command proves the changed area is healthy
- which paths or systems are dangerous
- what "done" means here
- when to stop and escalate instead of improvising
- how to answer without making a human decode repo jargon
- where deeper docs live

If the file does not improve those first-run decisions, it is probably carrying the wrong content.

## What a great AGENTS.md must do

High-signal `AGENTS.md` files usually do seven things well:

1. **Make the first action obvious**
   - install, bootstrap, or discovery commands
2. **Put verification before preference**
   - build, lint, test, typecheck, and file-scoped variants
3. **Define completion clearly**
   - what must pass before claiming success
4. **Define blocked-state behavior**
   - when to ask, when to stop, and what never to do
5. **Point to durable truth**
   - source-of-truth paths, docs indexes, or specialized skills
6. **Keep human communication legible**
   - plain English, answer-first wording, and immediate translation of repo shorthand
7. **Stay cheap enough to carry every run**
   - concise, non-inferable, and scoped

If you cannot answer those seven questions quickly after reading the file, the file is not doing its main job.

## Ownership by layer

Use the smallest layer that can honestly own the rule:

- **Root `AGENTS.md`**
  - cross-cutting commands, global safety rails, repo-wide definition of done, doc map, skill triggers, and the default communication invariant
- **Path-local `AGENTS.md`**
  - subtree-specific commands, ownership boundaries, dangerous exceptions, service-local truth surfaces, or local jargon rules that genuinely differ from root
- **`AGENTS.override.md`**
  - replacement rules for exceptional conditions where inheritance would be actively misleading
- **Linked docs or compressed docs indexes**
  - deeper architectural or domain reference that should not ride in every prompt
- **Skills**
  - larger reusable procedures that should load on demand instead of living in always-on context

If a rule belongs to a deeper layer but sits in root, the root file will sprawl. If a cross-cutting rule lives only in a deep file, fresh agents will miss it.

## Fatal anti-patterns

Avoid these failure modes aggressively:

- **Prose without commands**
  - values, aspirations, and style opinions that never tell the agent what to run
- **Inferable filler**
  - directory structures, framework defaults, or conventions already enforced by tooling or obvious from the repo
- **Architecture mirrors**
  - long summaries of the codebase instead of pointers to truth surfaces
- **Stale path assertions**
  - exact file locations that are likely to drift and are not backed by a search command or docs map
- **Contradictory priorities**
  - "move fast" alongside "run everything" with no ordering or stop rule
- **Auto-generated prompt sludge**
  - giant files filled with generic guidance that burns budget every turn
- **Authoring-process leakage**
  - notes about what the writer plans to add, why the file was drafted this way, or what happened in a previous edit
- **Self-referential skill chatter**
  - instructions about using `agents-md-authoring` or explaining the AGENTS workflow instead of routing real repo work
- **Workflow-lab jargon**
  - replies that say `phase plan`, `review-gate`, `cutover`, `follow-through`, or similar abstractions when the real answer is `plan`, `review`, `switch`, `finish`, `install`, or `uninstall`
- **Shorthand without translation**
  - terms like `host-local` or internal labels that are not explained in normal English right away
- **One giant file for every service**
  - no scope control, no local ownership, no hierarchy
- **Vague danger rules**
  - "be careful" instead of "ask before running migrations" or "never delete generated snapshots to make tests pass"

## Symptom-to-fix map

If the problem is:

- **the file feels long but still unhelpful**
  - move inferable or deep content into linked docs and leave only the routing rules
- **the agent keeps missing required checks**
  - move exact commands and definition-of-done rules nearer the top
- **agents break local services or risky paths**
  - add explicit red lines, approvals, and local-path instructions in the owning layer
- **different teams read the same root file and get conflicting guidance**
  - split path-local files or add an override where replacement is safer than inheritance
- **the file reads like a style guide**
  - keep only non-standard conventions tied to a command, example path, or failure mode
- **the file sounds like a plan, memo, or author note**
  - rewrite it in present-tense repo facts and delete sentences about the drafting process, future intentions, or self-reference
- **agents keep answering in jargon or evasive abstractions**
  - add or tighten a short communication invariant with concrete say-this-not-that examples such as `I installed it on this machine` instead of `I completed the host-local cutover`
- **agents do not know where to find deeper truth**
  - add a compact docs index or pointers to the right specialized docs or skills

## Final self-check

- Would a fresh coding agent know what to run first?
- Is the definition of done concrete and verifiable?
- Are blocked states and red lines explicit?
- Does the file contain mostly non-inferable repo truths?
- Does every sentence speak about the repo as it is now rather than the process of writing the file?
- Would a frustrated human understand the first sentence without decoding shorthand or workflow jargon?
- Is each rule owned by the right layer: root, path-local, override, docs, or skill?
- Could 20-30 percent of the file be deleted without losing real value?
  - If yes, it is probably still carrying filler.

## Source notes

Derived from:

- OpenAI Codex `AGENTS.md` guidance and prompting guidance
- the `openai/agents.md` examples repository
- Vercel's compressed-docs-index AGENTS patterns
- ETH Zurich AGENTbench findings on concise human-written context outperforming generated context
