# agent-watcher v2 — independent prompt audit

Against the pattern contract, the 23 audit questions, and the seven dispatch dimensions.

**1. A correction still becomes alignment, one tick later.** `watcher-brief.md` §Process
(later check, 2-4): the watcher logs `MISS`, correctly leaves `intent.md` alone, then reads the
next window with `work --cursor <saved>`. That window holds only the redo, which now has an
ancestor in his words → `ALIGNED`. The drifted artifact sits *before* the cursor and is never
re-examined; nothing carries an open finding forward, so `MISS` reads as discharged. Today's
failure, one tick later. Fix in §Process and §Output contract: a correction re-opens that
artifact until the inventory shows it gone, and an open item forbids `ALIGNED`.

**2. The headline question is a four-item menu missing today's case.** `SKILL.md` §What this is
for: "who asked for this," "why are there two," "why is it running that," "why did it stop" —
additive, duplication, machine, self-block. Lateral drift (rebuilt instead of reused) and
subtraction fit none, and the rebuild is the case the quality bar is built from. Make intent the
outcome — would he recognise this as what he asked for, and is it all of it — and let the
recognitions carry the shapes. Same in the brief's §Identity.

**3. "Did it build the thing" has doctrine but no step and no instrument.** The reviewer line is
drawn well, but §Process and §Inputs give only `session_events.py` over the transcript: every
step reads calls, never the produced artifact. Recognition 5 ("find where each imperative clause
landed") is not executable from a call inventory. A Sonnet watcher follows the process and
reports that work exists, not that it is the thing. Fix in §Process: one step that opens the
deliverable; §Inputs: list it as an instrument.

**4. Phantom context: the output formats are not in the dispatch.** §Dispatching hands over the
brief, `recognition.md`, session facts, and script paths — never `state-and-ledger.md`, cited
three times by the brief for the intent, ledger, packet, dedup-key, and return formats. The
whole output contract sits behind an unhanded path.

**5. Evidence truncates silently; child inventory is Codex-only.** Verified against `--help`:
`session_events.py` prints `--limit` 80 rows, pages under `--max-bytes`, and `--full-args` keeps
full arguments **only in the page file** it writes. So the central rule — read the call, not
the description — needs a page-file read no section instructs, and a large session silently
yields a partial inventory. `--children-of` is Codex-only; Claude
workers need `discover_sessions.py --include-children`, never named, so recognition 6 has no
instrument there. Fix in §Inputs and §Error handling: name the page file; a truncated page is
unverified, not clean.

**6. The master must arm, pin, and report facts it is told not to read.** §Before the first tick
requires the policy, `recognition.md`, `state-and-ledger.md`. Wake mechanisms, the host matrix,
and "Claude Code cannot pin effort per call" live in `runtime-notes.md`, gated by §Reference map
behind "under a new host" — so "Say plainly when effort inherits" is unsatisfiable from the
assigned reading. There is also no error handling: nothing for discovery failing, a watcher
erroring or never returning, an unpinnable model, or an invalid return (the brief defines
invalidity; the master never checks it). That is where "never ask him a question" breaks: an
unresolvable setup with no fallback is when a model asks.

**7. Rejected packets travel as authority the brief cannot receive.** §Dispatching passes
rejected packets "with your one-line reason"; the brief has no section that receives one. The
policy requires parent judgment to arrive challengeable. As written, "rejected: he doesn't care
about that" reads as binding and will suppress a correct re-escalation with better evidence.
Mark it non-binding; give §Inputs a re-raise rule.

**8. Brief and recognition restate each other (~1,200 words).** Brief principles 1,3,4,5,6,7 =
recognitions 1,5,3,6,7,2; the miss doctrine appears four times. First contact runs ~3,500 words
before a tool call for a Sonnet child, and the copies already diverge. Let recognition own the
tests, the brief own role, process, and return.

**9. Recognition's lower half is the residual keyword list.** §His corrections are the metric
ends in eight dated shapes ("today"); §Suppression is ten non-findings with no principle above
them — both in the decay zone, both inviting matching. Put the principle over suppression (he
cares what exists and what stopped, not how the work was conducted) and subordinate the eight
shapes to it.

**10. Two dispatch dimensions implicit.** **Continuation** is unstated: a watcher is a fresh
child at every check (hence `cursor.json`), but the text says only "never a fork of you," a
context choice. **Isolation** is a no-edit sentence with no parent check, against live repos;
the master also accepts a packet without confirming the quoted call exists.

## Strong — preserve verbatim

- `SKILL.md` opening: "...swearing. Your job is for him to find out from you first, with his own
  words next to the agent's, so one reply fixes it."
- "Compliance with his latest instruction is not the question; an agent that just got caught
  complies beautifully." And "The reviewer boundary excludes how well the thing was built, never
  whether it was the thing."
- All of `watcher-brief.md` §Quality bar — the Figma timeline, strong 11:52 return against weak
  11:59 `ALIGNED`. The most load-bearing passage in the package.
- The invalidity clause: "invalid if it cites the agent's own status as its evidence, if it
  grades the agent's response to a correction, or if it asks a question."
- The silence rule; "Do not add your theory of what he wants; the watcher derives it from his
  words."; `recognition.md` §What carries no signal; and "Read-only... does not mean you avert
  your eyes from the artifact."
