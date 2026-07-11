---
name: model-consensus
description: "Orchestrate a prompt-only dialogue between two selected Claude, Codex, Cursor Agent, or Grok participants until they converge on a lean plan, architecture, debugging strategy, investigation, design, or concept. Resolve transport independently per participant: use separate clean native children for same-host participants when native model capability suffices, and external sessions for cross-provider or unavailable exact-model/profile needs. Resume each exact participant between rounds; relay through the parent by default. Not for one-shot cold opinions, ordinary code review, ordered implementation loops, or broad idea tournaments."
metadata:
  short-description: "Two-participant consensus with per-role transport"
---

# Model Consensus

Use this skill when the user wants two selected model participants to think
together until they converge on the best answer. The parent agent orchestrates
the dialogue, preserves the goal, resolves transport independently for each
participant, relays evidence, checks for agreement, and reports the result.
Do not add or depend on a deterministic runner, script, controller, state
machine, or harness.

Same-host participants use separate clean native children when the active host
can actually supply the requested model capability. Cross-provider participants
or load-bearing exact models/profiles unavailable through the native child
surface use resumable external sessions. Every later round resumes the exact
participant that produced the earlier position, regardless of transport.

The work is not "ask two models and concatenate the answers." It is a
disciplined conversation that removes weaker ideas, preserves independent
evidence discovery for investigations, converges on existing repo patterns for
architecture, and avoids kitchen-sink plans.

## Use When

- The user wants two Claude, Codex, Cursor Agent, or Grok participants to
  iterate on a plan, architecture, design, migration, debugging strategy,
  investigation, or concept.
- The value comes from independent first passes, critique, and convergence
  rather than one reviewer answering once.
- One participant should challenge assumptions, propose simpler alternatives,
  or argue against overbuilt choices.
- Repo-backed work should minimize new pathways by adopting canonical owner
  modules, tests, and conventions.
- The final answer needs explicit agreement, explicit non-agreement, or a small
  set of remaining decisions.

## Do Not Use When

- The user wants one cold second opinion without dialogue: use
  `$fresh-consult`.
- The user wants ordinary code review findings: use the host agent's normal
  review response.
- The user wants ordered implementation or epic execution: use `$stepwise` or
  `$arch-epic`.
- The user wants broad idea generation across many options: use an ideation
  skill instead.
- The user only wants the current agent's own answer.

## Non-Negotiables

- Apply `../_shared/agent-orchestration-policy.md`. Keep each participant's
  role, transport, starting context, continuation, capabilities/isolation,
  topology, and return contract explicit without reducing the choice to a
  rigid dispatch form.
- Resolve transport independently. Prefer a native child for a same-host
  participant when it can honor the requested capability. Use an external
  session when a different provider, load-bearing exact model/profile,
  lifecycle, isolation, automation surface, or structured receipt provides a
  concrete benefit. These are recognition examples, not a closed allowlist or
  approval gate.
- For each new Codex-native participant, set `fork_turns: "none"`. A positive
  count carries bounded recent turns and `"all"` carries full parent context;
  neither is the independent-first-pass default. Resume later rounds through
  that participant's exact child handle. Do not omit `fork_turns` or claim an
  exact native model override unless the active tool schema confirms it.
- In Claude Code, start each same-host participant as its own clean named or
  custom subagent. An explicit conversation fork carries the parent
  conversation and is not an independent first pass. A skill with
  `context: fork` runs in an isolated clean subagent context; it is not a full
  conversation fork. Resume later rounds through the exact subagent. Use
  background agents only for a real lifecycle need.
- Parent relay is the default topology. Do not create a Claude agent team or
  another peer-messaging topology merely because there are two participants.
  Use direct participant messaging only when the user genuinely requested that
  method and explain why it improves the dialogue.
- The parent owns fanout, the concurrency budget, round sequencing, evidence
  relay, and final integration. Participant prompts prohibit child-created
  fanout and delegation/consult skills unless the parent explicitly assigns a
  bounded nested scope and budget.
- Context is separate from permissions, filesystem sharing, and worktree
  isolation. Participants are read-only collaborators. Prefer enforced
  read-only capability where available, include no-edit/no-write guidance, and
  have the parent check workspace status or diff before accepting the run.
- On a Codex host, an external Codex participant adds another operating-system
  process and may contend on shared Codex SQLite/WAL state; on some hosts that
  has caused system-wide stalls. Weigh that real cost without turning it into a
  ban, approval gate, or fixed process-count limit.
- Preserve exact participant model resolution. Codex runs GPT/GBT/OpenAI model
  ids and Fugu profiles; Claude Code runs supported Claude models; Cursor Agent
  runs `composer-2.5-fast`; Grok runs `grok-build` or
  `grok-composer-2.5-fast`. An omitted Codex participant model defaults to
  `gpt-5.6-sol`. Never silently substitute model family/version or cross
  runtimes.
- Keep the runner intelligent. The parent may tighten a round, require missing
  evidence, or stop on genuine agreement. It must not reduce the work to
  mechanical alternation or solve the problem itself.
- Preserve the user's raw goal. Build a faithful goal brief that clarifies
  success without injecting the parent's diagnosis, preferred solution, or
  investigation map.
- Preserve child discovery freedom. Start both participants from the same raw
  goal, exact user-named inputs, constraints, and evidence obligations. Do not
  reveal either first pass to the other before both have formed independent
  views.
- For repo-backed work, both participants must read real evidence before they
  recommend or agree. Investigation participants choose and cite their own
  evidence trails. Architecture participants identify canonical owner paths
  and existing patterns before proposing new ones.
- Agreement is not accumulation. Push toward the smallest answer that covers
  every hard requirement; a new abstraction or pathway requires evidence that
  the existing owner cannot absorb the work.
- Every dialogue round resumes the exact participant. If independence is needed
  again, such as a later cold gate, start a new clean child instead of reusing
  participant history.

## First Move

Read these references before dispatching participants:

- `../_shared/agent-orchestration-policy.md`
- `references/workflow-contract.md`
- `references/prompt-contracts.md`
- `references/model-and-invocation.md`
- `references/repo-grounding.md` when a repo, codebase, or local project is
  involved
- `references/convergence-and-synthesis.md`

Then:

1. Capture the raw user goal and whether one participant is adversarial.
2. Build a faithful goal brief with the goal, hard constraints, desired output,
   and exact user-named inputs, without adding the caller's theory or file map.
3. Resolve both participant provider/model/profile/effort choices exactly. Use
   the omitted-Codex-model default, then ask one concise question if another
   load-bearing participant choice remains ambiguous.
4. Inspect the active host's native child capabilities and choose transport for
   each participant separately. Record the concrete reason for any external
   participant and do not promise native model selection the host cannot
   confirm.
5. Set new native starting context explicitly: Codex
   `fork_turns: "none"`; Claude clean named/custom subagent. New external
   sessions start clean from the prompt. Preserve each exact child/session
   handle for later rounds.
6. Create a per-run artifact directory by hand, for example
   `.arch_skill/model-consensus/<slug>-<timestamp>/`, and store participant
   mapping, prompts, replies, receipts, and a short index. Do not create a
   script.
7. If repo-backed, require both participants to inspect real evidence. Before
   dispatch, reread each prompt and remove parent-written diagnosis or a
   parent-selected investigation map not present in the user's ask.

## Workflow

1. **Start two independent first passes.** Dispatch separate clean participants
   with the same faithful goal brief and mode-specific evidence obligations.
   For native Codex use `fork_turns: "none"`; for native Claude use separate
   clean named/custom subagents; for external participants use fresh resumable
   sessions. Prohibit nested fanout unless explicitly budgeted.
2. **Collect both views before relay.** Do not let either participant see the
   other's answer before it has formed its own position.
3. **Relay through the parent.** Send Model A's pass to Model B for critique and
   simplification, then send Model B's critique and proposal back to Model A.
   In adversarial mode, require constructive opposition and evidence-backed
   simpler alternatives.
4. **Resume exact participants.** Every critique, revision, and signoff returns
   to the same native child handle or external session id. Do not use a latest
   session, replace one participant silently, or cross runtimes on resume.
5. **Continue only purposeful rounds.** Stop when both participants explicitly
   accept the same lean answer and evidence obligations are satisfied. Continue
   when a reply is ungrounded, overbuilt, contradictory, or drops a hard user
   requirement. Most runs need one to four rounds.
6. **Synthesize only agreed material.** If they do not converge, report the
   smallest unresolved decision, each side's evidence, and the user decision
   that would unblock it. Do not invent a third unreviewed architecture.
7. **Verify and leave handles.** Inspect workspace status/diff for unexpected
   writes, preserve native/external participant handles and artifact receipts,
   and return the artifact directory without pasting long transcripts.

## Output

Final responses should include:

- each participant's provider/model/effort/role, transport, clean-start
  mechanism, exact continuation handle, and concrete external benefit when used
- whether the run converged
- the lean consensus plan or concept
- repo evidence that shaped the result when applicable
- rejected alternatives and why they were rejected
- unresolved decisions, if any
- parent read-only/status check
- artifact directory path

## Reference Map

- `workflow-contract.md` - parent-owned transport selection, independent first
  passes, exact-participant rounds, relay topology, and long-run posture
- `prompt-contracts.md` - first-pass, critique, adversarial, revision, and
  signoff prompt shapes with parent-owned fanout
- `model-and-invocation.md` - per-participant native/external resolution, exact
  model mapping, native child semantics, external command shapes, session
  resume, and receipts
- `repo-grounding.md` - required repo reading, open-investigation evidence
  discovery, and single-path architecture pressure
- `convergence-and-synthesis.md` - agreement versus accumulation and honest
  no-consensus reporting
- `examples.md` - representative transport and dialogue patterns
