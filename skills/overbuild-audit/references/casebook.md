# Overbuild Audit Casebook

Read this for a large plan or PR, or when you are unsure where the line sits. Each case gives the ask, what was planned or built, the audit as it should read, and the lesson. The cases teach judgment. They are not templates to match.

## Table of contents

1. A feature that grew fifteen times too large (plan and implementation)
2. A plan that grew through review waves (plan)
3. A safety fix that became a platform (implementation)
4. A rule that refused the real work (implementation)
5. Ceremony taught by instruction files (prompt and skill)
6. Centralization that turned reads into writes (implementation)
7. A lean result (illustrative)
8. When cutting would have been wrong
9. An agent workflow that was the overbuild (process)

---

## 1. A feature that grew fifteen times too large

**Ask.** Pick each player's daily and weekly missions from what they told us: their stated interests, goals and play frequency. Missions appear on the Missions screen, and tapping one launches the activity.

**What was built.** Two PRs added about 149,000 lines across 640 files. Hand-written production code was 18,766 lines and tests were 104,981. Independent estimates put the simple version at 700–1,300 production lines.

**How it happened.**
- **Plan level.**
  - An agent research note marked "recommendation for discussion" proposed time budgets, lighter sets for struggling or returning players, weekly active-day counts and discovery pauses.
  - A policy pass turned the note into 120 rule rows and 52 settings.
  - The epic then said to "preserve" all of it.
  - A 117-case spec locked the rules into tests.
- **Implementation level.** Agents broke the plan's own guardrails:
  - changed things outside the Missions screen;
  - added a navigation wait;
  - copied the policy into the client;
  - added repair-on-read after the plan said activity "is not replayed to repair".

**The audit, as it should read:**

- **Ask:** "missions picked from stated interests, goals and play frequency".
- **Verdict:** `overbuilt`.
- **Size:** 18,766 production and 104,981 test lines, against about 1,000 for the simple version.

| Piece | Type | Why it is not needed | Simple version | Saves |
|---|---|---|---|---|
| Triple retry loops, repair-by-replay on every read, pending payment, 30 s background pass, client resends | Retry and repair | No observed failure; hides write errors | Credit from native records on each read; throw on write failure | Large |
| 60-field settings registry | Flags and options | Nobody tunes these | Constants in code | Large |
| Timezone frozen per period, pending zone changes, 30-minute grace window | Speculative generality, extra state | For travellers; it caused a lockout | Local date from each request | Medium |
| 410/600 s caps, light/regular tiers, planning-second estimates | Invented rules | Came from an agent note, not the ask | No budget | Medium |
| Interests inferred from behavior; stated interests only a tie-break | Heuristic instead of signal | The player stated their interests | Stated answers set the picks | Medium |
| Discovery offers, ignored-offer pausing, per-row viewport tracker | Unrequested scope | Engagement feature nobody asked for | Delete | Medium |
| Mid-day row replacement, lineage, revisions, credit segments | Extra state | A second mode for a rare case | Keep each issued row as issued | Medium |
| Struggle relief, return protection, habit-based weekly day count | Unrequested scope | Barely visible; heavy data model | Delete | Medium |
| 14-day history window and its column | Extra state | Only serves other overbuilt rules | Delete | Small |
| Client copy of the server's credit rules | Second owner | Celebrates before the server answers | Show what the server paid | Medium |
| Errors relabelled "unavailable", silent launch failures | Fallbacks | Hides bugs | Original error to the tracker | Small |
| Play-tab rewrite, reshaped reward table, dropped uniqueness rule elsewhere | Outside the task | Changes behavior with the feature off | Revert everything outside Missions | Medium |
| 14-attribute marketing-profile export with no consumer | Unrequested scope | Nobody reads it | Delete; put completions in the warehouse | Small |
| Over-the-wire tests, fixture platform | Test sprawl | Heavier than the feature | One end-to-end test that pins the rewards | Large |

**Needs the user:** none. Every row traces to an agent artifact, not to the user.

**Lesson.**
- Most of the excess was in the plan before any code existed. A plan audit would have cut it for free.
- Always trace a rule back to its source. An epic that says to preserve something is not the user asking for it.

## 2. A plan that grew through review waves

**Ask.** A focused change to one workflow.

**What happened.** The plan went through 21 review waves. Each wave found real issues, and each finding became an invariant, a test, or a new file. The plan ended at 121 files and +11,646 lines. Reviews are good at catching what is missing and poor at catching what is extra, and the anti-overbuild check ran only after the build.

**The audit, as it should read:**

- **Ask:** the original intake, quoted.
- **Verdict:** `overbuilt`.
- **Size:** one workflow change against 121 files.
- **Cut list:** go wave by wave. For each wave, list what it added, then trace each addition to the original intake. Additions that answer "what if" rather than "what was asked" are cuts. Findings that were real but outside the ask become one-line notes for later, not plan items.

**Lesson.**
- Run the audit on the plan before building, not after.
- Measure against the original intake, not the latest revision.
- A review finding is an input, not a requirement.

## 3. A safety fix that became a platform

**Ask.** When a coordinated network operation fails, kill the process.

**What was built.** Pause machinery built on SIGSTOP, +469 lines. A coordination lease became able to freeze the main process, and a test locked the behavior in.

**The audit, as it should read:**

- **Verdict:** `overbuilt`.

| Piece | Type | Why it is not needed | Simple version | Saves |
|---|---|---|---|---|
| SIGSTOP pause and resume machinery | Heavier than the job; retry and repair | The ask was kill on failure | Kill on failure | ~450 lines |
| Lease that decides whether the main process runs | New layer | A side service now controls the main job | The lease coordinates and never controls | — |
| Test that pins the pause behavior | Test sprawl | Locks the defect in | Delete with the machinery | — |

**Lesson.**
- Check that no helper added along the way can freeze or block the main job: a lease, telemetry, a receipt, a guard.
- A "simplification" that adds state or fences is not a simplification.

## 4. A rule that refused the real work

**Ask.** When continuing a conversation on a different account, give it fresh identifiers so the two accounts are not linked.

**What was built.** Resolution logic that collected as much metadata as it could and refused any target it could not fully prove. It refused 41 of 43 real targets. Its tests ran on toy threads, and review findings had been adopted as defaults. It also closed a small leak while a bigger one stayed open.

**The audit, as it should read:**

- **Verdict:** `overbuilt`.

| Piece | Type | Why it is not needed | Simple version | Saves |
|---|---|---|---|---|
| Refusal paths for every unprovable field | Guards and gates | Refuses 95% of real use | Mint fresh identifiers and continue | Most of the resolver |
| Defaults adopted from review findings | Invented rules | Nobody asked for them | The user's rule only | — |
| Toy-thread tests | Test sprawl | Do not reflect real workloads | One test on a real thread shape | — |

**Lesson.**
- Before a new gate or refusal ships, run it against real workload data and count what it refuses.
- Protection that costs a lot while a bigger risk stays open is not worth it.

## 5. Ceremony taught by instruction files

**Ask.** Agents should commit their work before handing off.

**What was built.** Across hundreds of sessions, agents computed and reported git and file hashes as "proof". The user never asked for one and had to tell agents to stop many times. The habit came from the instruction layer:
- skills seeded hashes of goals and stage gates;
- a repo gotchas file told agents to hash screenshots "as a habit";
- parents passed the habit to children in their briefs.

**The audit, as it should read (target: skills and instruction files):**

- **Verdict:** `overbuilt`.

| Piece | Type | Why it is not needed | Simple version | Saves |
|---|---|---|---|---|
| Hash-as-proof steps in skills and gates | Proof ceremony | Nobody consumes the hashes | "Commit your work before you're done." | Every run |
| Gotchas line teaching screenshot hashing | Doc and prompt bloat | Teaches ceremony to every later agent | Delete the line | — |
| Brief templates that carry receipts to children | Process overhead | Multiplies the ceremony | Drop the receipt fields | — |

**Lesson.**
- When the same overbuild keeps coming back, audit the instructions that produce it: skills, `AGENTS.md`, gotchas files, goal and brief templates.
- The user's words: "I just wanted them to fucking commit their work."

## 6. Centralization that turned reads into writes

**Ask.** Make streak state consistent.

**What was built.** Centralization that made every read a database write, with 45–90 SQL statements per read, plus repair and retry bookkeeping. Locks and check-and-set guards were added for races that had not happened, and the bugs the user actually hit came from the locking.

**The audit, as it should read:**

- **Verdict:** `overbuilt`.

| Piece | Type | Why it is not needed | Simple version | Saves |
|---|---|---|---|---|
| Write-on-read reconciliation | Retry and repair; extra state | Consistency can be derived on read | Compute the streak on read | Most of the SQL |
| Locks and check-and-set guards | Guards and gates | Hypothetical races; the real bugs came from the locks | Last write wins, with a database constraint | — |
| Repair and retry bookkeeping | Retry and repair | Exists to fix what the reconciliation broke | Delete with it | — |

**Lesson.** For a tiny team, prefer constraints, idempotency and derive-on-read over queues, locks and reconciliation.

## 7. A lean result (illustrative)

**Ask.** Add a "copy link" button to the share sheet.

**What was built.** One button, one call to the platform clipboard API, one line of copy, and one widget test that the tap copies the URL. The diff is 41 lines.

**The audit, as it should read:**
- **Ask:** "add a copy link button to the share sheet".
- **Verdict:** `lean`.
- **Size:** 41 lines, against about 40 for the simple version.
- **Cut list:** none.

**Lesson.**
- Report lean when it is lean.
- Do not invent findings: the test is small and covers the change, so it is not test sprawl.

## 8. When cutting would have been wrong

Each of these looked like overbuild on the surface. Each one traced to the ask, so it belongs under "Needs the user" or "Keep", not in the cut list.

- **A mini workflow engine.** The user said, "I do want it to be a mini workflow engine."
  - An agent that shrank it to a script was scolded for a "stupid reduction in scope".
  - **Correct output:** Keep, "the user asked for an engine".
- **"I didn't ask for cheap."** A planner cut a requested capability to save cost. The capability was the ask.
  - **Correct output:** no cut. Name the cost under "Needs the user" if it is large.
- **A replay harness.** A reviewer marked a replay harness for removal. The user had asked for it.
  - **Correct output:** Keep, "asked for".
- **Visible, counted fallbacks.** A policy lookup falls back to a neighbor and logs a counter the user reviews.
  - **Correct output:** Keep. It is visible, counted and approved. The rule is against silent fallbacks.
- **Debug logging the user asked for.** The user asked for heavy logging while chasing a bug.
  - **Correct output:** no finding during the investigation. Remove it after the fix as ordinary cleanup.
- **A deep fix.** A bug's real cause spans three modules. Fixing it properly touches all three.
  - **Correct output:** Keep. A deep fix once is what the user wants. Cut only the machinery around it.
- **A one-way door.** A data migration deletes user records. Its backup step and dry run look like ceremony.
  - **Correct output:** Keep. Production data loss keeps full rigor.

**Needs the user, as it should read (illustrative):**

> The ask says "lessons and puzzles both get daily reminders". The plan builds a shared scheduling layer for both, about 600 lines. Two direct schedulers would be about 150. Keep the shared layer, or build two direct ones? Recommendation: two direct ones. Merge them if a third kind of reminder arrives.

## 9. An agent workflow that was the overbuild

**Ask.** Scheduled routines that produce a morning report.

**What was built.** Five lanes that each reread the same contracts, heartbeat polling that added turns, and runs that took 189–595 minutes.

**The audit, as it should read (target: the process):**

- **Verdict:** `overbuilt`.

| Piece | Type | Why it is not needed | Simple version | Saves |
|---|---|---|---|---|
| Five lanes rereading the same contracts | Process overhead | Same reading, five times | One reader that shares its notes | Hours per run |
| Heartbeat polling | Process overhead | Adds turns, not information | Wake when the work lands | Turns |
| Per-lane review | Process overhead | Review before every step | One review at the end | — |

**Lesson.**
- The process an agent runs can be overbuilt as surely as the code it writes.
- For a plan, also audit the review count, CI cadence, approvals and phases it implies.
