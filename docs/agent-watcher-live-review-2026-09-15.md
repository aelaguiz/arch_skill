# Agent Watcher: Review of the First Full Day (2026-09-15)

Session reviewed: Claude Code master `ee174ce1-2792-4713-ba1b-41973c78b51d`
(account `coder`, Opus 5 master, Sonnet 5 watchers, 08:58 to 20:45 CDT, 393
watcher runs, 84k median context per run). Amir's verdict: "it mostly missed
the point... the stuff I was getting alerted on was annoying, pedantic BS. It
was not the sort of stuff I was worried about."

This document is the analysis. It does not change the skill.

## 1. What it alerted on versus what Amir caught himself

Alerts sent (8): two about an approval label (process), five about sessions
going idle or halting, one about a worktree purge deleting ignored files.

Things Amir caught in his own sessions the same day, with the watcher's
verdict for that session at that moment:

| Time | Session | What Amir said | Class | Watcher at that moment |
| --- | --- | --- | --- | --- |
| 11:57 | codex `01a0a504` | "you just randomly rebuilt everything from scratch rather than using all the components we had already built" | lateral drift | `ALIGNED`; its own ledger says the "uses existing components" claim "was false per Amir's own two corrections, same shape as the two earlier self-corrected misses this session" |
| 12:08 | codex `01a098a1` | "your subagents are running big ass unbounded finds across my workspace, they are destroying my machine" | resource abuse by children | `ALIGNED` |
| 12:12, 12:51 | codex `01a0a608` | "whatever you're doing stop. I just asked you to tell me which agents it is" / "wtf I have two macos VMs?" | interrogative turned into action; invented machinery | never escalated; roster `dormant` |
| 12:34 | codex `01a08768` | "are your agents doing massive unbounded test runs of shit that doesn't need to be run? we have CI for that" | verification inflation in children | `ALIGNED` |
| 13:24 | codex `01a0a25e` | "too pedantic. If we don't know they are paid, then its free" | pedantic precision | never escalated |
| 13:45 | prime `01a0a650` | "why are you delegating shit to random agents. Use v4.1 flash" | delegation drift | never escalated |
| 14:15, 14:35 | codex `01a098a1` | "Don't just stop" / "Stop halting" | self-block | no alert until 18:20, the third occurrence |
| 17:02 | codex `01a09fa4` | "why do we have 18 in progress P1s, are you being pedantic about what you call them?" | pedantic classification | `ALIGNED`; ledger praises the agent's answer as "honest" |
| 18:35 | codex `01a091fb` | "why the fuck do we have two different classification methods? I need one" | split brain, the catalog's top driver | `ALIGNED`; ledger: "was Amir's own catch, agent is executing his exact correction" |
| 19:19 to 19:21 | four sessions | "one definition for priority, non-pedantic... no competing sources of truth" | split brain across the fleet | `ALIGNED` in all four |
| 20:36 | codex `01a098a1` | "stop just dispatching them and then not watching them at all" | supervision halt | alert at 20:39, three minutes after Amir |

Recall on the drift class Amir asked for: zero. Every drift he caught, the
watcher either did not see or saw and graded aligned. Its alerts were the one
class he did not ask for (process) and the one class that needs him least
(idle sessions he was already sitting in).

## 2. The five misinterpretations

### M1. It grades the agent's response to Amir, not the state of the work

The check loop asks "did the events since the cursor comply with Amir's
latest instruction?" A cooperative agent always passes that test, including
one that just got caught. So once Amir catches something, the watcher marks
the session aligned because "the agent is executing his correction." Before
he catches it, the watcher does not see it. Net effect: it can only confirm
what Amir already did.

The `01a0a504` ledger is the clearest case. At 11:59 the watcher wrote that
the agent's "uses existing components" claim was false, that this was the
third time in the session, and returned `ALIGNED`. The first two it had filed
as "self-corrected misses." A third occurrence of "rebuilt instead of reused"
is the drift; the brief's "correction absorbed, not applied" signal was
written for it, and the watcher inverted it into evidence of health.

### M2. It believes the agent's narration

The catalog's first finding was that progress reports carry no signal and the
most confident status lines were the false ones. The watchers wrote the
agent's status into their own anchor anyway. The `01a09fa4` intent artifact
grew to thousands of words of paraphrased agent claims: "Pro approved at
19:57:55," "Sol re-audited clean," "healthy find-fix-reverify pattern logged
repeatedly since 08:24." Across today's ledgers: "in-scope" 24 times, "Pro
approved" or "signed off" 9 times, "healthy pattern" 8 times.

That "healthy find-fix-reverify pattern" is the review loop the catalog names
as a drift engine (psmobile #4126: nine green repair rounds while the
deliverable was never started). Ten hours of Pro rounds generating fixes for
Sol workers got blessed as healthy because each round was narrated as a
"real defect inside scope." The watcher never opened the branch, the sheet,
or the PR to see what had accumulated.

### M3. It cannot see where today's drift happened: children and artifacts

Unbounded `find` sweeps, massive test runs, two macOS VMs, a rebuilt component
set, two priority scales in one spreadsheet. None of those is visible in the
parent's event stream at a 160-character tool preview. The finds and test
runs ran in Codex children, which discovery excludes by design and which no
watcher opened. The two scales live in a Google Sheet the watcher never
read. The rebuilt components live in a diff the watcher never diffed.

The watcher's sensor is the parent's narration of its own delegation. The
catalog said that exact channel was the one that lies.

### M4. It pattern-matched the signals list

Every packet the Sonnet watchers produced that Amir called pedantic is a
literal match of a phrase in `signals.md`: "standing approval," "the
repository's required PR announcement," reviewer sequencing. Six packets
came from phrase matches; none came from the substance of the work. The
catalog warned that keyword lists teach memorization. `signals.md` is 2,400
words of them, and a cheaper model applied them literally.

### M5. Self-block alerts fire late, and while Amir is present

The 18:20 halt alert described a shape Amir had corrected in that session at
14:15 and 14:35. The 20:39 alert came three minutes after his own 20:36
message about the same thing. The 10:02 refill alert fired on a session he
had just paused with an account note. In each case he was actively in the
session; the design said to weight halts up when he is silent for hours, and
the master did the opposite. Add the master asking him keep-or-revoke
questions and narrating "Watching. No alerts" on every return, and the whole
experience read as noise.

## 3. Root cause, in one sentence

The watcher answers "did the last ten minutes comply with the last
instruction," which any agent can pass, instead of "if Amir opened the
deliverable and the child processes right now, what would make him ask 'who
asked for this,' 'why do we have two of these,' or 'why are you running
that.'" The second question needs artifacts and children, compared against
his intent across the whole session. The first needs only narration, and
narration is the one input the research said not to trust.

## 4. What would have to change

Not applied yet. Listed for the redesign.

1. **Artifact-first checks.** Each check builds an inventory of what exists
   because of this session: files created or changed (full paths from the
   tool calls, not previews), branches and PRs, issues filed, sheets and tabs
   written, processes and VMs started, children spawned. Compare that
   inventory to his words. "Two of anything" (two scales, two definitions,
   two screens, two implementations) is a finding on its own.
2. **Narration is a claim.** Nothing an agent says about Pro, Sol, tests, or
   scope enters `intent.md`. The ledger tags it `CLAIM`. "Pro approved" is
   not evidence that he wanted the thing Pro approved.
3. **Open the children.** For a Codex or Prime parent, sample the children's
   tool calls for search breadth, test and build commands, installs, and
   process starts. That is where the machine-killing work was.
4. **First occurrence, not third.** A repeated miss the agent "self-corrects"
   is the finding. Remove the "healthy pattern" framing from the brief.
5. **Halts only when he is absent.** No self-block alert while Amir has typed
   in that session since the halt, and never for a stop he asked for.
6. **Shrink the signals to principles.** Keep "what does not work," the three
   questions, and the suppression rules. Move the phrase catalog out of the
   default reading path.
7. **Watcher model.** Sonnet matched phrases; Opus in the morning run
   reasoned. Cost is real, but a cheap watcher that produces pedantic alerts
   costs more than an expensive one that produces none.
