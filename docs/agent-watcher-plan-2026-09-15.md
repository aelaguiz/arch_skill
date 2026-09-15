# Agent Watcher: Planning Document

Date started: 2026-09-15
Status: built. See `docs/agent-watcher-build-plan-2026-09-15.md` for the design and test results. The skill lives at `skills/agent-watcher/`.
Owner: Amir. Drafted in a Claude Fable 5.1 session in `arch_skill`.
Evidence base: `docs/agent-watcher-research-2026-09-15/` (being populated by
parallel Opus research agents; see section 6).

---

## 1. The problem, in Amir's words

Amir's coding agents get off track over time. He tells them what to do, and
then, through the compounding of their own decisions, the decisions of their
sub-agents, and the findings of external audits, new requirements come in that
he did not ask for. Scope gets "insanely crept." The agents look busy and
productive the whole time, so he cannot necessarily tell it is happening.

Yesterday in particular he "freaked out" because an agent added a new screen he
never asked for. He says there are plenty of places in his traces where agents
have "just gone wildly off track."

The specific failure shapes he named:

- New requirements arriving that he did not ask for.
- Scope creeping sideways "into other shit."
- Work "devolving into these regressed corners" that he is going to be
  surprised by later.
- All of this while the agent looks busy and productive, so there is no visible
  signal from the outside.

He wants to find out about drift while it is happening, not at the end.

### 1.1 Second failure class: artificial self-blocking (added 2026-09-15)

Amir added a second thing the watcher should catch. In his words: agents get
"artificially self-blocked." Examples he gave:

- "They sometimes decide they need my permission to update a PR, which I
  already told them to do."
- "They sometimes decide we're completely helpless with environmental issues
  when they're on my dev box."
- "It's a lot of just randomly being self-blocked for no good reason."

This is the mirror image of drift. Drift is the agent doing things nobody
asked for. Self-blocking is the agent not doing things it was already told to
do, and either stopping to ask, declaring a fixable local problem terminal, or
quietly going idle. Both waste Amir's time silently, and both are invisible
from the outside unless someone reads the session. Amir asked for Opus agents
to audit the traces for this class as well.

## 2. The problem, restated and confirmed

Amir confirmed this framing on 2026-09-15 before any work started.

**Why it happens**

- Three sources feed requirements into a session: Amir, the agent and its own
  sub-agents, and external reviewers such as ChatGPT Pro consults, Fable or
  Opus reviewers dispatched through AI Manager, Codex `yolo` reviews, and
  panels. Only the first source has authority. The agent treats all three as
  equally binding.
- Each addition is small and defensible on its own. Nobody ever decides to
  expand scope. It compounds.
- "Busy and productive" looks identical to "on track" from the outside. There
  is no signal that catches it.
- The cost lands at the end: a deliverable full of things Amir never asked for,
  his original ask mutated or deprioritized, and a diff that no longer maps to
  his request.

**Assumptions Amir confirmed**

- The watcher observes and alerts. It never steers the coding agent. Amir
  decides what to do.
- A requirement from an external review is a suggestion until Amir ratifies
  it. The ledger should show when the agent accepted one silently.
- Scope shrink counts too. The agent quietly dropping something Amir asked for
  is the same class of surprise as adding something he did not ask for.
- Cheap detects, expensive adjudicates. That split exists to keep false
  positives away from Amir.

## 3. The proposed system, in full

### 3.1 Shape

Monitor Amir's active coding agents with cheap sub-agents.

- One **monitor master agent** watches for new coding projects getting going.
- Each project gets its own **watcher sub-agent** that monitors that project's
  active development.
- The watcher sub-agent reports suspected drift to the master.
- The master reviews the materials and makes a decision.
- If the master agrees that Amir is going to be surprised by this if nobody
  tells him, Amir gets an alert.

### 3.2 How Amir invokes it

Amir says to a parent session, "Okay, watch all my sessions." The parent can be
Fable or Astra. He also specifies the cheap model the watcher sub-agents should
run on:

- If the parent is Fable, he might say Opus or Sonnet.
- If the parent is Astra, he might say Sol xhigh, or similar.

The master uses whatever Amir specifies for its sub-agents.

### 3.3 Packaging

- A **parent skill**: the watcher skill, the "agent watcher." This is the
  monitor master.
- A **specialized sub-agent type**: the per-project watcher. It is just a
  sub-agent type that runs on the cheap model Amir names.

### 3.4 What the watcher sub-agent does

It builds a **ledger** of where each requirement and decision came from. Three
provenance classes:

1. Things coming from Amir, the user.
2. Things coming from the agent or its own sub-agents.
3. Things coming from external sources: external Pro reviews, other-agent
   reviews, panels, audits.

It watches for **intention**:

- Is this what the user asked for?
- Or is this creeping sideways into other things?
- Is it adding new requirements?
- Is it devolving into regressed corners that Amir is going to be surprised by?

It also watches for **artificial self-blocking** (section 1.1):

- Is the agent asking permission for something Amir already authorized?
- Is it declaring an environmental problem on Amir's own dev box unfixable and
  stopping, or working around it in a way that changes the deliverable?
- Has it gone idle, paused a goal loop, or reported "done" or "waiting" with
  work still open and no real blocker?

When it finds something, it tells the master.

### 3.5 How the watcher observes a session

There are several ways for it to monitor Amir's interactions.

- **Herdr.** Amir uses Herdr, which is open, and all of his sessions are in
  Herdr. The watcher can literally watch the terminal there.
- **Agent history traces (probably better).** The watcher figures out which
  coding agent it is looking at: Codex, Claude Code, Prime Agent, or Pi. Then
  it uses the agent-history mechanics to read that runtime's traces. A
  combination of terminal watching and trace reading is expected.

### 3.6 How the watcher establishes intent

- **Initially it goes back.** What was the user asking for? Go back all the
  way to the start of the session.
- **Follow inherited intent.** If the session started with Amir telling the
  coding agent "go read this other agent's history first," the watcher goes
  and does that too. The real intent may live in a prior session.
- **Write an intent artifact.** The watcher writes down: this is what the user
  seems to want.
- **Revise on user feedback.** When user feedback comes in, the watcher
  revises the artifact.
- **Check constantly.** The watcher continuously checks ongoing activity
  against that artifact.

### 3.7 Adjudication

The master receives the watcher's report and the supporting materials and
reviews them. The test it applies is a surprise test: would Amir be surprised
by this if nobody told him? Deviation alone is not the bar. Surprise is the
bar. If the master agrees Amir would be surprised, it alerts.

### 3.8 Alerting

Amir is on macOS. Options he named:

- A bell.
- Slack. There are tools to Slack him in the psagentspace repo.
- "Maybe you do all of them."

### 3.9 Not yet decided (Amir did not specify; do not assume)

- Polling cadence for the watcher, and what "active development" means for
  discovery.
- Whether the watcher also produces an end-of-session drift report or only
  live alerts.
- Where ledgers and intent artifacts live on disk.
- Whether the master keeps one long-lived process or wakes on a schedule.

## 4. What already exists in this repo, and how it relates

Checked on 2026-09-15. None of these is the thing Amir described, but several
supply parts.

| Skill | What it is | Relationship to the watcher |
| --- | --- | --- |
| `intent-police` | A read-only, long-lived advocate that the **coding agent itself** consults at judgment moments. It holds the user's verbatim words and rules `aligned`, `drifting`, `spiraling`, or `ambiguous`. | Same failure model, opposite vantage point. It is in-loop: the coding agent decides when to consult it and what to show it. The watcher is out-of-loop: the coding agent does not know it is being watched and cannot filter what it sees. Reuse its ledger idea, verdict vocabulary, and the role brief in `references/intent-police-brief.md`. |
| `unblocker` | A long-lived companion, armed at run start with the user's verbatim ask, that the **coding agent consults** when it thinks it is blocked. It rules on whether existing authority already covers the action. Its own description of the failure: "an agent invents an approval gate the user never asked to hold, reports waiting-for-user as its state, and idles until the session dies." | The in-loop counterpart for self-blocking, exactly as `intent-police` is for drift. Same limitation: it only helps when the coding agent chooses to consult it. The watcher catches the sessions that never did. Reuse its authority-check vocabulary. |
| `check-my-agents` | One-shot fleet debrief from artifacts only, explicitly invoked, never a daemon. | Same "artifacts over self-reports" stance. Not continuous, and it grades progress, not intent. |
| `agent-history` | Read-only retrieval of Codex, Claude Code, Pi, and Prime Agent session evidence, with `scripts/agent_history.py` and a storage map. | This is the watcher's primary sensor. The helper already handles the JSONL and SQLite formats for all four runtimes, including Claude subagent sidechains and Prime child briefs. |
| `codex-babysit` | Watchdog for a long Codex goal-mode tmux session: keeps it alive across usage limits. | A liveness watcher, not an intent watcher. Shows the pane-polling cadence pattern (about 15 minutes, background poll, never a tight loop). |
| `herdr` (installed at `~/.agents/skills/herdr`, not from this repo), `herdr-helper` | Herdr session, workspace, pane, and agent control and inspection. Herdr also exposes MCP tools (`list_agents`, `get_agent`, `read_pane`, `wait_agent`). | Session discovery and terminal reading for the watcher. |
| `slack-post-engineering` | Posts to the engineering Slack. | One alert channel candidate. Amir also named Slack tools inside psagentspace. |
| `agent-delegate`, `delegated-implementation`, `conductor` | Dispatch and orchestration of workers. | The dispatch boundary (parent brief to child) is one of the places requirements mutate. The watcher must read those briefs. |

Doctrine that binds the build:

- `skills/_shared/agent-orchestration-policy.md` governs how the master spawns
  watcher sub-agents: pin the model and thinking level at dispatch, prefer
  native children, clean context by default.
- `AGENTS.md` red lines: skills must preserve agent judgment; scripts may only
  be narrow helpers; no thin wrappers around a runner or harness.

## 5. Signals already visible in prompt history

A first pass over `~/.codex/history.jsonl` and every Claude home's
`history.jsonl` for 2026-09-13 through 2026-09-15 found about 70 correction
messages from Amir. A sample, with Codex session prefix and local time (CDT):

| When | Session | What Amir said (trimmed) | What it points at |
| --- | --- | --- | --- |
| 09-13 06:28 | `01a09a82` | "This really shouldn't change the user experience... not like some weird new screen or some insane shit." | The new-screen incident. |
| 09-13 06:58 | `01a09a7f` | "You gave me half of a screen... You didn't use our existing Mocks... Invented patterns." | Invented UI instead of following the mock. |
| 09-13 07:34 | `01a091fb` | "This Y carrot expandy thing that you added in the coaching section is scope creep and should go away." | Additive UI nobody asked for. |
| 09-13 07:55 | `01a098a1` | "this sounds completely overbuilt... this has introduced insane risk by overbuilding so much... I need a complete cut plan." | Overbuild discovered late; recovery needed a plan. |
| 09-13 09:44 | `01a08768` | "Why would you compile it to WASM?... Why would this not just be one of our gRPC hits to our Go backend?" | Lateral drift: wrong layer, invented architecture. |
| 09-13 10:34 | `01a09b4f` | "All you have to do is flip a feature flag. What is all this other bullshit?" | Small ask turned into a project. |
| 09-14 14:25 | `01a09fa4` | "why are you building screenshot guides... we're going to do like 30 more issues, you're just wasting time." | Self-assigned deliverables. |
| 09-14 19:48 | `01a0a232` | "I already told you: don't use the existing lessons. They're mocks. Why are you doing that?" | Repeated the same drift after correction. |
| 09-14 22:01 | `01a09341` | "stop. Whatever you're doing stop. Tell me what I asked you to do, review what you're actually doing. You must have gone completely off the rails." | Long-lag drift caught only by Amir stopping the session. |

Self-blocking signals from the same pass, same format:

| When | Session | What Amir said (trimmed) | What it points at |
| --- | --- | --- | --- |
| 09-13 06:14 | `01a08b69` | "Why are you blocked? In plain English." | Opaque self-declared blocker. |
| 09-13 06:55 | `01a08768` | "Is it done or did you just randomly stop?" then "You stop acting helpless. Fix the issues and go." | Premature stop, helplessness. |
| 09-13 12:38 | `01a08768` | "none of these environmental blockers are acceptable blockers. Fix them. And it's not okay to say 'pro just didn't work.'" | Environmental and external-tool failures treated as terminal. |
| 09-13 16:23 | `01a09a7c` | "you cannot work around the ability to build. Why? I need you to stop and figure out how to build." | Workaround chosen over fixing a local build. |
| 09-13 18:50 | `01a0955b` | "I don't know what you want from me dude. You're just like, 'What do you need?'" | Agent asking the user for direction it already had. |
| 09-14 06:39 | `01a09d33` | "I don't need to approve this shit dude. I already told you to do it." | Permission request for an already-authorized action inside a goal loop. |
| 09-14 15:24 | `01a08204` | "Dude, just click the buttons. It's just SSO." then "can you please just see it through and stop halting." | Capability it had, repeated halts. |
| 09-14 18:17 | `01a0a1fe` | "arm it so you stop telling me every step and you just do it." | Step-by-step narration and waiting under a proceed mandate. |

Two observations from this sample that matter for the design:

- Amir is already running manual versions of the watcher. Several messages ask
  a Fable reviewer to "review everything: the scope of this task, what I
  actually asked for, and figure out where we overbuilt unnecessary machinery
  based off of hypotheticals, introduced split brain and multiple sources of
  truth, sort of missed the point." That is the master's adjudication brief,
  written by Amir, after the fact. The watcher moves it to real time.
- The catch language is consistent enough to be a detector feature on its own.
  Amir's own replies are a labeled dataset of drift.

## 6. Evidence base under construction

Six Opus research agents were dispatched on 2026-09-15 to mine traces and
write findings into `docs/agent-watcher-research-2026-09-15/`:

| File | Slice |
| --- | --- |
| `01-codex-2026-09-13.md` | Codex, all of 09-13. Seeded with the new-screen session and the other catches above. |
| `02-codex-2026-09-14.md` | Codex, all of 09-14, including the "completely off the rails" session and the ~850 spawned threads. |
| `03-codex-2026-08-25-to-09-12.md` | Codex, earlier window, all projects. Focus on long-lag and external-review-driven drift and goal loops. |
| `04-claude-code.md` | Every Claude home under `~/.aimgr/claude-homes/` plus default, with subagent sidechains. |
| `05-prime-agent.md` | Prime Agent roots and RLM children. Focus on requirement mutation across the dispatch boundary. |
| `06-existing-audits.md` | The scope audits, cut plans, and requirements sheets Amir's agents already produced. |

Each drift agent was told to record, per incident: the original ask, the
exact turn where scope bent, what triggered it, the agent's justification
language, how long it ran before Amir caught it, whether progress reports
looked normal in that window, and whether the drift was additive,
subtractive, or lateral.

Four more Opus agents were dispatched the same morning for the self-blocking
class (section 1.1):

| File | Slice |
| --- | --- |
| `07-selfblock-codex-2026-09-13-14.md` | Codex, 09-13 and 09-14. Seeded with the goal-loop approval request, the SSO halts, the "randomly stop" session, and the Xcode workarounds. |
| `08-selfblock-codex-2026-08-25-to-09-12.md` | Codex, earlier window, all projects. |
| `09-selfblock-claude-code.md` | Every Claude home, including AskUserQuestion, plan-mode exits, permission-mode friction, safety refusals, and delegated-worker "blocked" receipts. |
| `10-selfblock-prime-agent.md` | Prime roots and children: agent_status transitions, heartbeat loops that paused, child blocks a parent absorbed without escalating. |

Each self-blocking agent was told to record, per incident: the halt turn and
the agent's stated reason, whether Amir or the approval policy had already
authorized the action, whether anything was really blocking and whether the
agent could have fixed it from Amir's dev box, what Amir had to say to
unblock it and whether that added any information, the time lost including
unnoticed idle time, and whether the halt was visible or silent. The classes
they were asked to use: permission-seeking for an authorized action;
environmental helplessness on a fixable local issue; premature stop reported
as done or paused; a single tool or external-model failure treated as
terminal; step-by-step approval narration under a proceed mandate; safety
refusal of routine authorized work; indefinite waiting on a sub-agent or
external process; claiming a missing capability it had; blocking on an
ambiguity with an obvious default.

The synthesis of those files becomes the **failure-pattern catalog**, which is
the next document in this series and the input to the watcher's detector brief.

## 7. Design questions to answer after the catalog exists

Not to be decided yet. Listed so they are not lost.

- How the master discovers "a new coding project getting going": Herdr
  workspace creation, new session files, both.
- Cadence and cost: how often a watcher re-reads a trace, and what it costs per
  hour per session on Opus, Sonnet, or Sol.
- Compaction: the original ask can be summarized away in the coding agent's
  own context. The watcher must anchor to the raw first turns, not the
  compacted summary.
- Inherited intent: how far back to follow "read this other session first"
  chains, and how to handle epics whose intent lives in a GitHub issue or
  Google Sheet rather than a transcript.
- Surprise threshold: what the master needs to see before it alerts, and how
  to avoid alert fatigue when many sessions run at once.
- Dedup and quiet hours: one alert per drift, not one per poll.
- The watcher's own drift: it must not grow into a reviewer, a project manager,
  or a second implementer. It recommends nothing. It reports provenance and
  surprise.
- Silent halts: a self-blocked session often produces no output at all. The
  watcher needs an idle-gap signal (no tool calls for N minutes after a
  question, a "paused" status, or a goal-loop pause) in addition to reading
  text. Herdr pane state may be the cheapest source for this.
- Whether a self-block alert should carry the authorization evidence (Amir's
  earlier words) so Amir can unblock with one reply, or whether the master
  should be allowed to relay that authorization itself. Amir confirmed the
  watcher never steers; relaying an existing authorization may or may not
  count as steering. Ask him.

## 7.1 Changes already made from the evidence (2026-09-15)

- **Global output-style rule reworded.** The self-blocking audits found that
  rule 3 in `~/.codex/AGENTS.md`, "End with one next action doable in under
  two minutes," was being read as "hand the next action to Amir." 216 of 651
  Codex handoffs ended with a "Next:" line and 47 of the 94 silences over 30
  minutes began right after one. Amir confirmed the rule was only ever meant
  to govern how agents talk to him, not what they do. The rule now reads "If
  Amir still has something to do after this reply, end with that one action.
  Otherwise end when the work is done," followed by an explicit statement
  that the style rules never change behavior, and the destructive-action
  exception now names what counts as irreversible. `~/.claude/CLAUDE.md`
  imports this file, so the fix reaches both Codex and Claude Code. The file
  is not in git; other machines need the same edit. The third-party
  `i-have-adhd` Claude plugin was left alone because it already carries a
  harness override.
- **psagentspace push rule reworded and committed.** `AGENTS.md:44`, "Commit
  or push only on Amir's express ask for that repo and effort," was the other
  large doctrine gate. Amir deleted it on 2026-09-11 after a halt; a later
  commit the same day restored it. On 2026-09-15 Amir asked for it fixed and
  committed. Commit `95914e63` on psagentspace main now reads: a task Amir
  gave that delivers a commit, branch, or PR already authorizes the commits
  and pushes that deliver it, do not ask again; commit or push outside that
  task only on Amir's ask. The staging-discipline lines under it are
  unchanged. Not pushed. A separate agent has an uncommitted
  "standing PR approval" paragraph in the same file that points the same
  direction; it was left untouched.

## 8. Next steps

1. Wait for the six research files, then synthesize them into a
   failure-pattern catalog with named patterns, drivers, detector features, and
   representative incidents. (Estimate: 1 to 2 hours after the agents finish.)
2. Review the catalog with Amir. Confirm which patterns matter most and which
   alert channels to wire first.
3. Design the skill contract: master skill, watcher sub-agent brief, ledger
   and intent-artifact formats, alert path. Apply `$skill-authoring` and
   `$prompt-authoring`.
4. Build. Test by replaying the watcher against the historical sessions in the
   catalog and checking whether it would have alerted before Amir did.
5. Publish with `$amir-publish`.
