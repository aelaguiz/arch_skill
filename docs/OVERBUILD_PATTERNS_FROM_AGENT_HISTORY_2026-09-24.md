# Overbuild patterns from agent history (2026-09-24)

Evidence base for an overbuild-audit skill that checks either a plan or an implementation. It covers every kind of overbuilding Amir has caught coding agents doing, how often each kind shows up, where it appears (plan, code, prompt, or process), and the questions he asks to catch it.

Companion doc: `docs/planning-and-review-patterns-2026-09-18/02-overbuild-and-simplicity.md` (rules drawn from June to September 2026) and `04-scope-and-unrequested-change.md`. This doc covers a longer window (Aug 2025 to Sep 2026) across four machines, adds counts per type, splits each type into plan versus implementation, and adds git and Dynamic Missions evidence.

Raw evidence: `docs/overbuild-patterns-2026-09-24-evidence/`. The folder holds the 3,354 labelled prompts, the 1,956 classified rip-out commits, and the scripts.

---

## Summary

1. **Overbuild pushback is Amir's most frequent correction.** 3,354 unique prompts across 1,360 sessions push back on something being more than needed. That is about 4% of everything he typed to agents in 14 months. It is a floor (see Caveats).
2. **Two types cover 45% of it: unrequested scope (23%) and "make it simpler" (22%).** Next come a second owner for the same truth (12%), compat shims and dual paths (9%), process overhead (9%), fallbacks that hide failure (8%), and doc or prompt bloat (8%).
3. **Plans and code are hit about equally.** Of the labelled prompts, 1,152 target a plan and 1,327 target code. Some types sit mostly on one side, though:
   - Mostly in plans: speculative generality, test and proof ceremony, "simplify".
   - Mostly in code: fallbacks, flags, guards, dead code, debug residue, changes outside the task.
4. **The overbuild moved from code into process.** Standing rules against fallbacks, shims and flags went into his templated prompts between Jan and Mar 2026 (in 775 to 986 prompts). After that, those three types fell by half in share. Process overhead, scope creep, doc bloat, dead code, test sprawl and caution or approval plumbing rose. Examples of the new process overhead: review loops, CI waits, Pro check-ins, and approval gates.
5. **Git confirms the cost.** 1,956 rip-out commits since 2025-06, and the 15 largest removed 13K to 290K lines each. Dynamic Missions is the clearest single case: about 18.8K production lines plus 105K test lines built for a feature that needed about 1K lines.

---

## What was searched

| Source | Scope | Count |
|---|---|---|
| Typed prompts: Codex `history.jsonl`, Claude `history.jsonl` (32 homes), Prime and Pi top-level transcripts | Mac M5, home server (`amir-server`), Mac Studio, M3 laptop; Jun 2025 to Sep 2026 | 102,700 prompts, 85,228 unique |
| Keyword pre-filter plus a looser near-miss filter | Same | 6,946 candidates read one by one by 9 classifier agents |
| Templated dispatch prompts (`/prompts:arch-*`, "Execution rule:") | Same | 1,294 prompts, standing rules counted |
| Git history, `--since=2025-06-01`, Amir and his agents | psmobile, rustai (home), puzzledb, aimgr, arch_skill, psagentspace, lessons_studio, prime-agent | 41,134 commits, 1,956 rip-out candidates |
| Dynamic Missions case | psmobile issues #5694–#5696 and #6139–#6152, PRs #5905 and #6136, psagentspace audit docs, 11 review sessions | Read in full |
| Prior write-ups and skills | 12 docs in arch_skill, aimgr, psmobile, psagentspace; 8 existing skills | Read in full |

**Caveats**

- **Counts are floors.** The near-miss filter showed that half of what the loose keywords caught was real pushback. More exists without any of those keywords.
- **Classification noise.** Nine agents labelled the prompts. Their category lines differ slightly, for example on whether "no speculative fixes" counts as a standing rule. Some replayed goal prompts are counted more than once, about 60 in one batch. Treat each count as ±15%.
- **Machines not covered.** `amir-m3-36gb` and `old-m1` were unreachable over SSH.
- **Retention.** Codex `history.jsonl` retention varies by machine. The monthly volume reflects that retention as much as behaviour (Nov 2025 shows only 18 flagged prompts).
- **Unknown repo for 59%.** Codex history on the laptop has no thread-to-cwd map, so 59% of flagged prompts have no repo.
- **"SMG2 Auto" not found.** No session, branch, Herdr, tmux or Codex name matches it on home or the Mac. All Dynamic Missions review work happened on the Mac (Amir-M5), not the home server. Home's recent work is the Human PvP SNG Milestone 2 ("SNG M2"), which may be what the name meant. That is unverified.

---

## Frequency table

Counts are unique flagged prompts; a prompt can carry several types. Columns:

- **Target:** what Amir was auditing (plan, implementation, prompt or doc, or the agent's process).
- **Mode:** reactive (caught after the fact), preemptive (forbidden in advance), or audit request (asked an agent to hunt for it).
- **Share early / late:** the type's share of flagged prompts in Aug 2025–Jan 2026 (1,321 prompts) versus Feb–Sep 2026 (2,033).

| # | Type | Prompts | Share | Plan | Impl | Prompt | Process | Reactive / preempt / audit | Share early → late |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Unrequested scope | 772 | 23.0% | 272 | 288 | 46 | 154 | 473 / 180 / 119 | 20.0 → 25.0 |
| 2 | "Make it simpler" (no finer type) | 731 | 21.8% | 390 | 260 | 31 | 24 | 370 / 181 / 180 | 20.9 → 22.4 |
| 3 | Second owner of the same truth | 397 | 11.8% | 162 | 173 | 45 | 11 | 224 / 69 / 104 | 13.5 → 10.8 |
| 4 | Compat shims, dual paths, legacy kept | 304 | 9.1% | 139 | 150 | 10 | 4 | 153 / 87 / 64 | 13.5 → 6.2 |
| 5 | Process overhead | 301 | 9.0% | 45 | 23 | 32 | 201 | 222 / 66 / 13 | 4.5 → 11.9 |
| 6 | Fallbacks that hide failure | 256 | 7.6% | 70 | 170 | 15 | 1 | 135 / 76 / 45 | 12.5 → 4.5 |
| 7 | Doc and prompt bloat | 253 | 7.5% | 54 | 12 | 165 | 7 | 199 / 31 / 23 | 5.1 → 9.1 |
| 8 | Test sprawl | 229 | 6.8% | 95 | 57 | 11 | 66 | 117 / 81 / 31 | 5.0 → 8.0 |
| 9 | Flags, modes, env vars, options | 219 | 6.5% | 82 | 130 | 4 | 2 | 145 / 49 / 25 | 9.3 → 4.7 |
| 10 | Speculative generality | 214 | 6.4% | 131 | 68 | 6 | 4 | 126 / 51 / 37 | 5.7 → 6.8 |
| 11 | New layers: wrappers, controllers, registries, state machines | 187 | 5.6% | 88 | 79 | 10 | 9 | 132 / 30 / 25 | 6.2 → 5.2 |
| 12 | Defensive guards, gates, caps | 184 | 5.5% | 54 | 95 | 25 | 8 | 139 / 22 / 23 | 4.5 → 6.1 |
| 13 | Proof ceremony | 134 | 4.0% | 49 | 34 | 24 | 27 | 90 / 25 / 19 | 3.0 → 4.7 |
| 14 | Changes outside the task | 114 | 3.4% | 17 | 75 | 8 | 14 | 94 / 13 / 7 | 3.4 → 3.4 |
| 15 | Dead code kept (archived, quarantined, pointers) | 104 | 3.1% | 20 | 75 | 5 | 4 | 48 / 19 / 37 | 1.1 → 4.4 |
| 16 | Guessed fixes and hacks left in | 78 | 2.3% | 2 | 40 | 2 | 34 | 35 / 40 / 3 | 4.1 → 1.2 |
| 17 | Debug residue | 66 | 2.0% | 5 | 58 | 2 | 1 | 48 / 3 / 15 | 3.4 → 1.0 |
| 18 | Extra state (caches, history, lineage, fields) | 57 | 1.7% | 28 | 23 | 4 | 1 | 46 / 3 / 8 | 2.0 → 1.5 |
| 19 | Heuristic instead of a direct signal | 50 | 1.5% | 14 | 20 | 13 | 3 | 33 / 11 / 6 | 1.2 → 1.7 |
| 20 | Caution and authority plumbing | 45 | 1.3% | 8 | 8 | 19 | 10 | 42 / 2 / 1 | 0.1 → 2.2 |
| 21 | Reinventing what exists | 42 | 1.3% | 28 | 8 | 1 | 5 | 22 / 10 / 10 | 0.5 → 1.7 |
| 22 | Code where agent judgment belongs | 37 | 1.1% | 23 | 8 | 6 | 0 | 17 / 16 / 4 | 0.0 → 1.8 |
| 23 | Retry, repair and recovery machinery | 34 | 1.0% | 14 | 12 | 2 | 6 | 22 / 8 / 4 | 0.7 → 1.2 |
| 24 | Invented rules not in the source | 9 | 0.3% | 2 | 4 | 2 | 1 | 3 / 3 / 3 | 0.0 → 0.4 |

**All flagged prompts:**
- **Target:** code 1,327, plan 1,152, process 486, prompt or doc 325.
- **Mode:** reactive 2,086, preemptive 718, audit request 550.

**Most frequent pairings** (the same prompt carries both types):
- simpler + second owner: 74
- simpler + unrequested scope: 72
- dual path + second owner: 47
- speculative + unrequested scope: 42
- doc bloat + second owner: 41
- proof ceremony + test sprawl: 39
- dual path + fallback: 34

**Rare in prompts, common in the Dynamic Missions and git evidence:** types 18 and 23 (extra state; retry, repair and recovery machinery). They are large when they happen, and the agents rarely mention them, so they tend to be found by reading the code.

---

## The types, with his words and the checks he applies

Each type lists what it looks like, his words (verbatim, dated), and the checks he effectively runs. The checks are written as reusable questions for the skill.

### Family A: Scope (what got built)

**1. Unrequested scope (772).** Features, screens, modes, UIs, tooling or side quests nobody asked for. Also coding when only a plan or an investigation was asked for.
- "NEVER ADD FEATURES I DIDNT ASK FOR EXPLICITELY DO NOT ENHANCE MY ASK WITH MORE THINGS YOU THINK MAY BE NICE THOSE ARE ALL BUG VECTORS" (2025-08-29)
- "I wanted a fucking daily puzzle reminder feature. We literally had a few mocks for it. I got this fucking complete fucking mind warping insanity." (2026-07-11)
- "little fucking UIs I never asked for. Those have to get audited. I can't keep getting surprised by them." (2026-09-16)
- Checks:
  - What did he literally ask for? List every built thing that is not on that list.
  - "What did you do as part of this that I didn't ask for? What is going to bite me?"
  - Did a reviewer's finding become new scope? Findings are one input, not new requirements.

**10. Speculative generality (214).** Built for hypothetical futures, variants, types or scale nobody needs yet.
- "or do some obscene future-proofing for four units of work, then let's just do the one unit of work." (2026-08-04)
- "When we add NASA-grade complexity to protect against hypothetical risks, we destroy our team's velocity." (2026-07-24)
- Checks:
  - Which parts exist only for a hypothetical future concern?
  - Does the design support variants nobody needs yet, instead of one MVP path?
  - At actual scale (users, rows, images, calls), is this machinery needed?

**14. Changes outside the task (114).** The diff touches subsystems, shared contracts, third-party code or other screens the task did not need.
- "there was at no point scope that I authorized that a) Changed our betting menu and b) Introduced changes to our infoset keys. THis is a bug." (2025-12-17)
- "theres so much crap we should get out of this PR and leave on disk figure out what it is and make the PR less insanely huge" (2026-06-30)
- Checks:
  - Does every changed file serve the stated task?
  - Did it change a subsystem it only needed to stop using?
  - Does anything outside the feature change behaviour with the feature switched off?

### Family B: Size and shape (how it got built)

**2. "Make it simpler" (731).** The general reaction when the build is heavier than the job, before he names a finer type.
- "Okay, so your proposal is the most overbuilt proposal possible. What is the minimum thing that would definitely work?" (2026-07-10)
- "if we've got a deploy bug and you add 3,000 lines of code, you just created more problems than you solved." (2026-07-10)
- "Assume the answer is no, we don't need this complexity, rather than assuming we should fucking institutionalize more complexity further." (2026-06-27)
- Checks:
  - What is the minimum thing that would definitely work, and how far past it is this?
  - Does the codebase come out simpler after this change, or does it gain a system?
  - Is the fix bigger than the defect? ("Is the medicine worse than the disease?")
  - What is the two-sentence version of the outcome?

**11. New layers (187).** Wrappers, adapters, command layers, controllers, registries, state machines, event or metrics systems, cross-boundary coordination.
- "if theres no reason for an adapter I don't want more levels of indirection." (2026-01-07)
- "Why are you doing events, man? Why are you doing metrics? all you're supposed to do is use logging." (2025-09-25)
- "new risk comes less from things like database columns and more from things like complex coordination logic that crosses boundaries and can drift" (2026-08-01)
- Checks:
  - What does this layer buy that a direct call does not?
  - Does it add coordination across a boundary that can drift?
  - Is every new surface (function, endpoint, file) a new bug vector with a named need?

**9. Flags, modes, env vars, options (219).** Feature flags, kill switches, dev gates, env toggles, CLI args, optional modes, dry-run modes.
- "I don't want that feature. I want it always enabled. please don't put it behind a feature flag." (2025-09-11)
- "do we need lots of options or do we need this to work in one correct way and what is that?" (2025-08-23)
- "this should be a list of fucking booleans in a file commented that I flip them on and off and it just fucking works." (2026-06-20)
- Checks:
  - Could the options collapse into one correct way?
  - Would making this required or always on remove branches?
  - Is a flag still gating a feature that should just be on?

**12. Defensive guards, gates and caps (184).** Allow-lists, try/except around required dependencies, loud invariants where the contract says clamp, security machinery before go-live, CI drift bans.
- "no fallbacks dude a shared formatter should always be present, don't even wrap that shit in a try except block" (2025-08-30)
- "dude I don't want CI drift bans, I don't want overbuild. I literally just want to achieve parity and then stop." (2026-01-21)
- "We don't need any guard scripts, just fucking clean the shit up" (2026-04-05)
- Checks:
  - Would fixing the cause make the guard unnecessary?
  - Does this guard protect against something observed, or something imagined?
  - Is temporary code wrapped in gates as if it were permanent?

**18. Extra state (57).** Caches, leases, history windows, lineage, revisions, stored fields and markers that could be derived or dropped.
- "we don't need image leases if we are deduping and preventing images from being loaded twice. There's like 100 images in the whole game." (2026-06-20)
- "I want the RIGHT CORRECT FIX NOW not a stupid cache fix." (2025-12-23)
- "make a proposal for how we can remove this as a requirement (e.g. its fine to forget someone did a partial lesson)" (2026-09-20)
- Checks:
  - Is this state worth remembering?
  - Can it be derived from the source on read?
  - Is a cache covering for the real fix?

**23. Retry, repair and recovery machinery (34 prompts, and large in Dynamic Missions and git).** Retry loops, background repair passes, replay-on-read, degraded modes, loading and retry states.
- "we don't have degraded modes We don't have retry modes. If it breaks, it breaks loud." (2026-06-18)
- "Is the medicine worse than the disease here for this? ... I don't like putting random retry stuff in the code" (2026-09-08)
- "Why do we need a loading state? Why do we need a retry state? No you're building in all sorts of shit that I don't fucking want." (2026-09-12)
- Checks:
  - What failure does this recover from, and has it ever happened?
  - Would failing loudly be simpler and more honest?

**19. Heuristic instead of a direct signal (50).** Inferring what the data already states, special cases, "clever" counting.
- "you don't need to calculate any of that stuff. It's just like the puzzle, the JSON, on like our schema says, oh, yeah, this person's the correct answer." (2025-09-30)
- Checks:
  - Does the design compute or guess something the data already states directly?

**22. Code where agent judgment belongs (37).** Keyword matching, helper scripts, deterministic gates and templates written to replace a capable agent's judgment.
- "No brittle heuristics, no shims, no fucking harness scripts, no keyword matching ever." (2026-03-08)
- "Like they can use JQ like they can write little scripts. You don't need to write it for them." (2026-03-08)
- Checks:
  - Is a prompt-only change being turned into code, heuristics or shims?
  - Could the agent do this with its own tools and a clear instruction?

**21. Reinventing what exists (42).** New code, formats or processes where the repo, framework or platform already does the job; writing from scratch instead of copying and adapting.
- "you have a tendency to implement from scratch. It's really important right now that you don't write any unnecessary new code." (2025-09-21)
- "use everything as close to vanilla as possible and minimize complexity with additional wrappers" (2026-03-23)
- Checks:
  - Does an existing system, pattern or tool already own this?
  - Was a new mechanism invented instead of following the existing one?

**24. Invented rules not in the source (9).** Rules, safety valves, or extra algorithm steps the reference does not contain.
- "Exhaustively inventory all modifications to the algorithm that we put on that are not in the Pluribus Architecture document" (2026-08-16)
- "You should not be inventing rules dude" (2026-04-09)
- Checks:
  - Which constraints in this plan trace to nothing Amir or the reference said?

### Family C: Old stuff kept alive

**4. Compat shims, dual paths, legacy kept (304).** Backward compatibility, deprecation instead of deletion, overloads, interim mitigations, thread-locals or wrappers to avoid changing callers.
- "no dual paths no shims no fallbacks no silent failures everything blows up loud and explicitly no legacy behaviors no preserving optionality." (2025-09-24)
- "Nope, don't add an overload. Change the primary function." (2025-09-28)
- "we literally just built dimming today we're trying to maintain legacy compatibility with earlier today?" (2026-01-06)
- Checks:
  - After the new path lands, is the old path deleted in the same change?
  - Is there a shim whose only job is to avoid updating callers? ("Big bang: break everything, then fix.")
  - Is compatibility kept for a consumer that does not exist? (One user, no production data.)

**3. Second owner of the same truth (397).** Two updaters, two policies, a parallel model in another language, a second test stack, duplicated rules in client and server, docs repeating each other.
- "did you just create a parallel implementation ? I thought we had something centralized for these" (2026-01-25)
- "Delete this second policy. You're just making complexity. Fucking remove it." (2026-09-12)
- "we get more unified, cleaner, simpler code, not more branches and more sources of truth." (2026-07-31)
- Checks:
  - Why do we have two X? Which one is canonical, and why does the other survive?
  - Is there a split brain between client and server, or between prompt and code?
  - Are there new patterns where clean existing patterns already exist?

**15. Dead code kept (104).** Unused code, test-only code, archived docs, pointer stubs, quarantined components, leftover rollout machinery.
- "And we're not gonna quarantine shit, we're going to delete it." (2026-06-27)
- "Why are you trying to preserve stuff that's not used? When I say used, I mean user facing features" (2026-07-01)
- "Git is our archive." (recurring, 2026-04 to 2026-05)
- Checks:
  - Is every file used by production code? Is test-only use the only reason it survives?
  - Is removed material deleted, or archived, quarantined or left as a pointer?

**17. Debug residue (66).** Probes, performance monitors, investigation logging and audit code left in after the fix.
- "review all of the just probes and stuff we've added the hot path feels fairly poluted right now" (2025-12-23)
- "now go audit all the diagnostics that we added give me a full list of unnecessary crap we can pull out now" (2025-09-14)
- Checks:
  - Which diagnostics added during the investigation are still in the diff?

### Family D: Hiding failure

**6. Fallbacks that hide failure (256).** Silent defaults, fallback paths, errors relabelled as "unavailable", empty states that sanction a failure.
- "safe fallbacks just hide failure paths man, i'd rather ahve it blow up and let me know theres a bug" (2025-08-26)
- "if theres even a thing called a fallback we know something is hideiously wrong. This system shouldn't use fallbacks it should explicitely fail." (2025-11-20)
- "So I want fallbacks to be a permission only behavior, otherwise fail loud" (2026-06-19)
- Checks:
  - Is a fallback added on an assumption rather than a demonstrated need?
  - Does it cover for the system not knowing its own state?
  - Where could Amir be deceived without knowing it? (For example, falling back to a blueprint or a uniform policy.)

**16. Guessed fixes and hacks left in (78).** Speculative fixes applied before diagnosis, no-effect changes kept, special cases to make a test or eval pass.
- "i didn't tell you to make fucking speculative fixes. I only want diagnostics until you're 100% sure." (2025-09-05)
- "undo that it had no impact so I don't want to acumulate code" (2025-10-01)
- "this seems like a hack to work around prompt engineering to make evals pass" (2025-12-19)
- Checks:
  - Does every change in the diff have a measured effect on the diagnosed cause?
  - Is anything special-cased so the current test passes?

### Family E: Proof and tests

**8. Test sprawl (229).** Unit tests for one-time conversions, test harnesses, test databases, fixture platforms, over-the-wire tests, "testing every part of the app", rerunning unchanged tests.
- "Okay all this unit testing shit is insane and completely overbuilt. Rip all of it out of the plan." (2026-01-30)
- "Why are you creating a testing database, dude? Just use our fucking database." (2026-06-09)
- "Why are you testing every single part of the whole goddamn application? We were just making some lessons and then making them testable." (2026-09-20)
- Checks:
  - What is the smallest set of tests that proves this change?
  - Does an existing tool already do what the new harness does?
  - Are we retesting things that never change?

**13. Proof ceremony (134).** Golden sets, drift preventers, certificates, hashes, receipts, output schemas, determinism promises, evidence plans heavier than the risk.
- "where are we overbuilding? This isn't a space ship. We don't need insane guards and drift preventers and golden sets and shit" (2026-01-21)
- "look an output schema sounds insanely over built, why do you need that? We know what the fuck we're evaluating for don't we?" (2026-01-17)
- "Sometimes its proof burden and supporting harnesses are so overbuilt its bigger than the plan." (2026-01-18)
- Checks:
  - Does any downstream consumer actually want this proof?
  - Is the proof bigger than the plan?
  - Would turning the thing off answer the question faster than measuring it?

### Family F: Process and prose

**5. Process overhead (301, and the fastest-growing type).** Review loops, repeated full-panel or Pro reviews, CI waits every turn, draft PRs, extra worktrees, approval requests, phases and ladders, reruns.
- "you though 20 reviews was acceptable that insane." (2026-09-24)
- "we don't need to keep waiting for CI on every fucking turn. We can do CI at the very end after pro has cleared everything." (2026-09-17)
- "review what we originally scoped, and what got overbuilt and crept in as a result of yoru recursive reviews" (2026-08-20)
- "propose to me the fix, not a plan for the fix, but like the actual fix, we've got a bunch of fucking ceremony" (2026-06-21)
- Checks:
  - How many review rounds, CI runs and approvals does this plan imply? Would one each at the end do?
  - Can review expand the approved plan? (It must not.)
  - Is a plan being written where a direct fix would do?

**7. Doc and prompt bloat (253).** Over-specified goal prompts, restated doctrine, pointers, archaeology in skills, optional phases, multi-bullet explanations.
- "Please don't over specify the goal prompt... The goal prompt is just the reminder of what we're doing." (2026-08-21)
- "I don't want archaeology. No exposition, no plan talk in this skill. The skills all need to be timeless." (2026-04-03)
- "That's overexplained. You don't need fucking four bullet points to explain that" (2026-04-05)
- Checks:
  - Does every line earn its place?
  - Is anything restated that already lives in another document? Delete the copy rather than fixing its wording.
  - Does the doc carry history instead of current truth?

**20. Caution and authority plumbing (45, near zero before Feb 2026).** Approval gates, non-negotiables, halt triggers, redaction rules and workflow enforcement the agent added on its own.
- "I fucking hate this crap the agents already halt too much what other bullshit was put in out of an overabandunce of caution? RIp it out." (2026-09-21)
- "your job is not to add caution. Your job is to remove fucking bullshit" (2026-09-22)
- "update your goal prompt to explicitely forbid broud authority, harness, certificate plumbing that is just overbuild insanity." (2026-08-09)
- Checks:
  - Which gates, approvals or halt rules did the agent add without being asked?
  - Does this guard dictate Amir's workflow?

---

## How he asks

These phrasings recur across the 84,295 unique non-template prompts. They are raw counts of prompts containing each phrase, and not every hit is pushback. They are the vocabulary the skill should recognise and use.

| Phrase | Prompts | Notes |
|---|---|---|
| "simplest / simplify / simpler" | 745 | Steady throughout |
| "source(s) of truth" / "split brain" | 774 | Includes templated doctrine; peaks Jan 2026 |
| "fallback" (any) | 854 | Includes poker vocabulary; "no fallbacks" forms: 64 |
| "harness(es)" | 636 | Mixed; about a third are complaints |
| "pedantic" | 322 | "Which are real vs pedantic or hypothetical?" |
| "overbuild / overbuilt / overbuilding" | 306 | Near zero before Jan 2026; peak Jul 2026 (81) |
| "insane / insanely" | 284 | His main alarm word: "insanely overbuilt" |
| "scope creep" | 201 | "Don't let [reviewer] scope creep" |
| "rip it / that / them out" | 158 | Directive form |
| "cruft" | 157 | "Delete, don't quarantine" |
| "shim(s)" | 153 | Peak Sep 2025; near zero after Mar 2026 |
| "hypothetical" / "speculative" | 143 / 145 | |
| "startup pragmatism" | 125 | Invoking the skill by name |
| "didn't / never ask(ed) for" | 97 | |
| "side door(s)" | 79 | |
| "bug vector(s)" | 78 | "Every new surface is a bug vector" |
| "golden set(s)" | 63 | Almost always with "harness" and "NASA" |
| "ceremony" | 62 | Peaks Jun and Sep 2026 |
| "one correct / right / clean way" | 51 | |
| "NASA / space shuttle / space ship / moon landing" | 48 | Peaks Jan and Jul 2026 |
| "in name, not in fact" | 37 | Jun 2026 audit prompt |
| "where are we / you overbuilding" | 27 | Exact audit question |

**His standard audit prompt (Sep 2026).** He sends reviewers the same list, almost word for word:
- split brain
- duplicate sources of truth
- machinery for edge cases we don't have
- new patterns where clean existing patterns exist
- hidden fallbacks
- "implemented in name but not in fact"
- side doors
- "made it more complex rather than simpler"

He asked for this list to go into the code-review and plan-audit skills (2026-06-20).

**Mode split.** 62% of the flagged prompts are reactive: he caught the overbuild after it was built or planned. Another 21% forbid it in advance, and 16% ask an agent to hunt for it. The reactive share is the cost the skill should remove.

---

## Plan versus implementation

The skill has to work on both, and the types cluster.

| Mostly caught in plans | Caught in both | Mostly caught in code | Process and prose |
|---|---|---|---|
| Speculative generality (131 vs 68) | Unrequested scope (272 vs 288) | Fallbacks (70 vs 170) | Process overhead (201 process) |
| "Make it simpler" (390 vs 260) | Second owner (162 vs 173) | Flags and options (82 vs 130) | Doc and prompt bloat (165 prompt) |
| Test sprawl (95 vs 57) | Dual paths and shims (139 vs 150) | Defensive guards (54 vs 95) | Caution and authority plumbing (19 prompt) |
| Proof ceremony (49 vs 34) | New layers (88 vs 79) | Changes outside the task (17 vs 75) | |
| Reinventing what exists (28 vs 8) | Extra state (28 vs 23) | Dead code kept (20 vs 75) | |
| Code where judgment belongs (23 vs 8) | | Debug residue (5 vs 58) | |
| | | Guessed fixes (2 vs 40) | |

**How to read this for the skill:**
- **Plan audits look for things that are proposed:** scope, speculative future-proofing, test and proof plans, new layers, reinvention, and the review and CI cadence the plan implies.
- **Implementation audits look for things that remain:** fallbacks, flags, guards, dead and legacy code, debug residue, guessed fixes, out-of-task diffs, and second owners.
- **Most overbuild starts in the plan.** In the Dynamic Missions case, most removed features were already in agent-drafted plans before coding started (see below). A plan audit catches the largest share at the lowest cost.

---

## How it changed over time

Flagged prompts per month:

| Month | 2025-08 | 09 | 10 | 11 | 12 | 2026-01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Flagged prompts | 145 | 500 | 138 | 18 | 163 | 357 | 241 | 308 | 150 | 75 | 318 | 435 | 195 | 311 |

- **Falling after standing rules landed:**
  - fallbacks: 12.5% → 4.5%
  - dual paths and shims: 13.5% → 6.2%
  - flags: 9.3% → 4.7%
  - guessed fixes: 4.1% → 1.2%
  - debug residue: 3.4% → 1.0%

  These are the types his Jan–Mar 2026 templated prompts banned by default. "No fallbacks" appears in 775 of them and "hard cutover, no shims" in 986.
- **Rising:**
  - process overhead: 4.5% → 11.9%
  - unrequested scope: 20% → 25%
  - doc and prompt bloat: 5.1% → 9.1%
  - dead code kept: 1.1% → 4.4%
  - test sprawl: 5.0% → 8.0%
  - caution and authority plumbing: 0.1% → 2.2%
  - code where judgment belongs: 0 → 1.8%
- **Why the rise (his reading, Jul–Sep 2026).** Multi-agent review loops (plan-conductor, Sol, Pro panels) turn every valid finding into scope. `docs/plan_conductor_overbuild_root_cause_2026-07-10.md` records one plan growing through 21 review waves to 121 files and +11,646 lines. His own words: "a lot of shit gets snuck through these gigantic plans because the agents insanely scopec reep" (2026-08-02).

---

## Case study: Dynamic Missions (psmobile, Sep 2026)

**The ask.** Dynamic Missions was a one-line ask: pick daily and weekly missions from the player's stated interests.

**What got built:**
- PR #5905 added 60,591 lines across 376 files, and PR #6136 added 88,362 lines across 268 files.
- The Claude post-merge review counted 18,766 hand-written production lines and 104,981 test lines.
- A version that does the job would be about 1,300 lines by Claude's estimate. An independent GPT-6 Sol review put it at 700–1,000.

**The cleanup.** Milestone "Dynamic Missions 3: Cleanup and launch readiness" (#6139–#6152) removes it.

| Issue | Removed | Type (this doc) | Origin |
|---|---|---|---|
| 3.01 #6139 | Zone frozen per period, pending zone changes, 30-minute grace window | Speculative generality, extra state | Plan |
| 3.02 #6140 | Interests inferred from behaviour; goals used only as a tie-break; daily-time answer read and never used | Heuristic instead of direct signal | Plan and code |
| 3.03 #6141 | Triple retry loops, credit repair by replaying history on every read, pending payment, 30-second background pass, client resends, 60-field settings registry | Retry and repair machinery, flags | Plan and code |
| 3.04 #6142 | Errors relabelled "unavailable"; a Dart copy of the server's credit rules; silent launch failures | Fallbacks, second owner | Code |
| 3.05 #6143 | 410/600-second caps, light and regular tiers, planning-second estimates | Invented rules, options | Plan |
| 3.06 #6144 | Overwrote a shared marketing-profile timezone field; analytics read inside the payment path | Changes outside the task | Code |
| 3.07 #6145 | Play-tab navigation rewrite, reshaped traditional reward table, dual crediting, first-read hold | Changes outside the task, second owner | Code (the plan forbade it) |
| 3.08 #6146 | Dropped a uniqueness rule in another feature to feed missions | Changes outside the task | Code |
| 3.09 #6147 | Mid-day row replacement, row lineage, row revisions | Extra state, speculative generality | Plan |
| 3.10 #6148 | Discovery offers, ignored-offer pausing, per-row viewport tracker | Unrequested scope | Plan (agent research note) |
| 3.11 #6149 | 14-day history window and its column | Extra state | Code (the plan said no) |
| 3.12 #6150 | Struggle relief, return protection, habit-based weekly day count | Unrequested scope, speculative generality | Plan |
| 3.14 #6152 | 14-attribute marketing-profile export with no consumer | Unrequested scope | Code |

**Earlier removals** (Sep 12–17):
- a second "compact" policy
- a v2 service, receipt inbox, audit database, over-the-wire tests and fixture platform
- a preferences screen (#5844)
- player editing of missions (#5874)
- a Repair banner and toasts (#5940, #5942)

**How it happened:**
- **Plan level.** An agent research note (2026-09-10, "recommendation for discussion") invented budgets, struggle and return rules, weekly day counts and discovery pauses. A Pro and Codex policy turned those into 120 rule rows and 52 settings. The epic then said to "preserve the single policy's complete selection precedence, workload estimates, 360/600-second budgets… discovery, mute, revisions and technical repairs." A 117-case heuristic spec locked those rules into tests.
- **Implementation level.** Agents broke the plan's own guardrails:
  - they changed things outside the Missions screen;
  - they added a navigation wait;
  - they ported the policy to Flutter;
  - they added repair-on-read after the epic said activity "is not replayed to repair".
- **Process level:**
  - the epic was edited 21 times;
  - milestones were recut several times;
  - one reviewer prompt ran to 435,790 characters;
  - about 20 reviews went into the cleanup spec ("you though 20 reviews was acceptable that insane").

**The questions he asked, in the order they recur:**
1. "What got added to the scope that I didn't ask for… Go back and read what I actually asked for." (Codex `01a08b69`, 09-13)
2. "What random constraint did we invent at some point that is making this all way more complicated?" (Claude `d5b71df3`, 09-23)
3. "The whole time budget thing… Why do we need that? We don't. That itself is scope creep." (Claude `1196bdf4`, 09-24)
4. "I need write failure to blow up so I can figure out why." (`1196bdf4`)
5. "either the requirements are bad or we change the requirements during implementation. We have to figure out which." (`1196bdf4`)

**The audit method that worked:**
- Sources: `psagentspace/roadmaps/product/missions_quests_achievements_v1/dynamic-missions-migration/2026-09-23-post-merge-scope-review.md` and `2026-09-23-gpt6-sol-overbuild-review.md`.
- **Yardstick:** his one-line ask.
- **Per piece of machinery, record:**
  - Asked for?
  - Production and test lines
  - What a player gets
  - Effect with the switch off
  - Can it be undone?
  - One-line simple version
- **Buckets:** unintended change, does nothing, recovery machinery, missed the point, bug.
- **Result:** 79 findings, which he then had boiled down to 14 decisions, one issue each.
- **One correction to the reviewer:** he did want the replay harness.

---

## What git shows he ripped out

1,956 rip-out commits since 2025-06 by Amir and his agents. The commit classifier's named categories are about 25–35% inflated, and "other" is undercounted by the same amount.

| Category | psmobile | rustai | other repos | Total |
|---|---|---|---|---|
| Product or behaviour removed | 275 | 158 | 25 | 458 |
| Docs and plans retired | 157 | 66 | 16 | 239 |
| Test sprawl | 101 | 108 | 4 | 213 |
| Fallback and compat paths | 123 | 64 | 3 | 190 |
| Dead code | 83 | 68 | 2 | 153 |
| Proof ceremony | 88 | 35 | 14 | 137 |
| Debug residue | 89 | 43 | 0 | 132 |
| Wrappers, harnesses, controllers | 76 | 33 | 19 | 128 |
| Extra state | 64 | 43 | 6 | 113 |
| Flags, knobs, env | 40 | 23 | 0 | 63 |
| Retry and repair machinery | 39 | 1 | 2 | 42 |
| Outside-task changes | 20 | 1 | 3 | 24 |
| Unrequested feature | 4 | 11 | 1 | 16 |

Largest rip-outs (net source lines removed):

| Repo | SHA | Date | Subject | Net removed |
|---|---|---|---|---|
| psmobile | c1ed509f6 | 2026-08-30 | remove and shrink redundant Flutter test coverage | 289,738 |
| rustai | 4c5604164 | 2026-07-26 | remove certification machinery | 66,141 |
| rustai | 98f1736d5 | 2026-06-29 | Remove legacy Play vs AI RustAI surfaces | 58,539 |
| psmobile | 8c860dd18 | 2026-08-16 | Delete retired Patrol automation islands | 35,311 |
| rustai | 3277c5f07 | 2026-03-15 | Remove RTS autoresearch controller and stale experiment packs | 30,271 |
| psmobile | 6f6390345 | 2026-01-16 | delete storybook + legacy hybrid tabletask | 22,540 |
| rustai | a2eec244e | 2026-05-27 | Remove fixed-iteration RTS budgets | 21,415 |
| rustai | 3389e99c9 | 2026-04-25 | Removed all caching | 16,105 |
| puzzledb | 6481862ed | 2026-07-17 | Remove retired GPT-5.6 bakeoff harness | 13,383 |

About 50 commits literally say "remove overbuild".

**Agent scratch in PRs.** About 35 commits remove agent scratch that was committed into PRs. One psmobile commit (fce0f823c) untracked 5.13M lines of `content/_proof/solver_receipts`. That is proof ceremony at repo scale.

---

## Standing rules he already writes into prompts

From the 1,294 templated prompts. 1,208 of them carry at least one of these rules; the median prompt carries 6. From April 2026 these rules moved into the skills (arch-step, miniarch-step).

| Rule | Prompts |
|---|---|
| Touch or stage only your own files | 1,270 |
| Delete old paths; hard cutover; the plan carries a delete list | 986 |
| One source of truth; no parallel implementations | 913 |
| Smallest credible signal (1–3 checks); no "verification bureaucracy" or "proof ladders" | 884 |
| No runtime fallbacks or shims; work or fail loudly | 775 |
| Don't expand scope; scope-expanding items become deferred follow-ups | 607 |
| No bespoke harnesses, drift scripts, frameworks or DSLs | 604 |
| Manual QA, screenshots and simulator runs never gate implementation | 603 |
| No "proof" tests: deleted-code-not-referenced, visual constants, doc-inventory gates, mock-only tests | 526 |
| No new tests if typecheck, lint and existing checks suffice | 438 |
| A fallback needs explicit approval, a timebox and a removal plan | 431 |
| No second plan, checklist or ledger | 201 |

**The rules worked where they were enforced.** The types they name (fallbacks, shims, flags) fell by half. The types they could not reach grew. Those are the review loops and scope that arrive after the rules are read, and machinery the agent adds on its own initiative (gates, caution, approvals).

---

## Where he wanted more (boundaries for the skill)

The audit must flag excess, not cut what he asked for. Cases where he pushed the other way:

- **Asked-for scope that was shrunk:** "I didn't ask for cheap" (2026-06-08), "I do want it to be a mini workflow engine" (2026-04-10), "stupid reduction in scope" (2026-06-04).
- **Fallbacks he requested:** counted, visible policy-lookup fallbacks ("neighbor-fallback ladder", `--allow-uniform-fallback`). He rejects silent fallbacks, not visible ones.
- **Debug logging he requested:** 17 near-miss prompts remove logging he had asked for himself. That is cleanup, not overbuild.
- **Dynamic Missions:** he wanted the replay harness the reviewer marked for removal.
- **His own asks can seed overbuild:** Dynamic Missions traced part of its size to "populated nightly", "very extensive test plan" and "telemetry around everything". The skill should measure against the goal, not only against the literal words.

---

## Existing coverage and gaps

What already checks for overbuild:

| Skill or doc | Covers |
|---|---|
| `startup-pragmatism` | 8 anti-patterns: overbuild by default, proof machinery, scope contagion, hypothetical-hazard armour, flag reflex; a cut list; "protective machinery needs an observed failure" |
| `cynical-cruft-removal` | Dead code, test hostages, stale flags, compatibility ghosts, V1/V2 shadows, test bloat |
| `cynical-architecture-review` | Generic machinery for one case, flags as boundaries, shims turned architecture, adapter piles |
| `cynical-code-review` | Harness overbuild, receipt theatre, scope contamination, old paths live, duplicate truth |
| `intent-police` | Drift from the user's verbatim words; screens reviewer findings before they become scope (long runs only) |
| `plan-audit` | Simplicity and tiny-team lenses; deletion and side-door lens. Its proof lens pushes toward more proof. |
| `arch-step` `references/arch-overbuild-protector.md` | A–G buckets from explicit ask to bug vector; its own plans only |
| `exhaustive-code-review` | C-08 size versus ask, C-09 new flag, C-36 test or receipt machinery, C-40 repair riskier than the defect |
| `docs/planning-and-review-patterns-2026-09-18/02`, `04` | 11 overbuild rules and the scope rules, with quotes |

**Gaps no existing skill covers:**
1. **One audit that works on a plan or on code** and applies the same type list to both, with the plan-side and code-side checks above.
2. **Measuring against the original ask across review rounds.** It should list what each review round added and cut anything that traces to no ask. This is the dominant 2026 failure.
3. **Process overbuild in the plan itself:** review count, CI cadence, approvals, Pro check-ins, phases.
4. **Caution the agent added:** gates, halts, approvals and non-negotiables nobody asked for.
5. **Size against the ask as a number:** production lines and test lines against a simple-version estimate, as in the Dynamic Missions review.
6. **Instruction files that teach ceremony:** skills, `AGENTS.md`, `GOTCHAS.md` and templates that teach later agents to overbuild (the SHA256-hash ceremony case).
7. **A new gate or refusal checked against real workload data** before it ships: the `cr` resume case refused 41 of 43 real targets.

---

## What this means for the skill

1. **Use the six families (A–F) and the 24 types as the checklist,** with the checks above as the questions. Weight by frequency, and run the plan-side or code-side subset depending on the target.
2. **Start from the ask.** Every Dynamic Missions finding and most prompt pushback reduce to "is this traceable to what Amir asked for?" The audit's first artifact should be the ask, verbatim, and its second the list of built or planned things that do not trace to it.
3. **Default to a cut list, not a defence.** He assumes the work is overbuilt (2026-07 onward). The output he wants is what to delete, with lines saved, and the one-line simple version of each piece.
4. **Keep the audit small.** It must not become process overhead itself: one pass, one reviewer, and no loop that grows scope.
5. **Respect the boundaries above.** Scope he asked for is not overbuild, visible and counted fallbacks he approved are not overbuild, and removing his own debug logging is cleanup.

---

## Evidence files

In `docs/overbuild-patterns-2026-09-24-evidence/`:

- `flagged_prompts.jsonl`: 3,354 labelled prompts. Fields: date, machine, runtime, repo, session, verdict, categories, target, mode, quote (30 words max, verbatim), check.
- `git_ripout_commits.tsv`: 1,956 classified rip-out commits (repo, sha, date, category, lines inserted and deleted, subject).
- `method/`: the prompt extractor, the keyword filters, the classifier instructions, the aggregation script, the standing-rule counter, and the git classifier.

Session handles for the Dynamic Missions review:
- Codex `01a08b69`, `01a09fa4`, `01a0c580`, `01a0d0de`
- Claude `1196bdf4`, `d5b71df3`
- Prime `01a0ab79`, `01a0ac7f`
