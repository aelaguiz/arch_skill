# Overbuild Types And Examples

Read this before your first audit in a session and whenever a piece is borderline. The families and types match `SKILL.md`. Each type gives what it looks like, the questions that catch it, and real examples.

Each example has three parts: what an agent built or planned, the user's reaction in their own words, and the simple version that should have been built. Quotes are verbatim, typos and profanity included, because the heat tells you how much the user cares. The examples teach the pattern; they are not a lookup table. A piece can be overbuilt in a way no example shows, and a piece that looks like an example can be exactly what the user asked for. The ask decides.

## Table of contents

- A. Scope: unrequested scope, speculative generality, outside the task, invented rules
- B. Size and shape: heavier than the job, new layers, flags and modes, guards and gates, extra state, retry and repair, heuristic instead of signal, code where judgment belongs, reinventing
- C. Old stuff kept alive: dual paths and shims, second owner, dead code kept, debug residue
- D. Hiding failure: fallbacks, guessed fixes and hacks
- E. Proof and tests: test sprawl, proof ceremony
- F. Process and prose: process overhead, doc and prompt bloat, caution and authority plumbing
- How the user asks

---

## A. Scope: what got built

### A1. Unrequested scope

**Looks like:** features, screens, settings, modes, operator surfaces, CLIs, scripts, integrations, or side quests nobody asked for. Also doing more than the ask shape allows, such as coding, committing, or opening PRs when only a plan or an investigation was asked for. This is the most common overbuild of all, and it grows during review. A reviewer's finding becomes a requirement, the requirement becomes code, and the code becomes a reason for more findings.

**Questions:**
- What did the user literally ask for? List it, then list what was built. The difference is the cut list.
- "what did you do as part of this that I didn't ask for. like what is going to fucking bite me"
- Did a review finding, a bot comment, or an agent research note become scope?

**Examples:**

- **Built:** a daily puzzle reminder with a conductor log, suppression machinery and extra states. The user had supplied mocks.
  - **User:** "I wanted a fucking daily puzzle reminder feature. We literally had a few mocks for it. I got this fucking complete fucking mind warping insanity."
  - **Simple version:** build the mocks.
- **Built:** a settings screen and player editing for a feature whose ask was "pick missions from the player's stated interests".
  - **User:** "We don't nee da fucking settings screen for this. Insanely stupid, and ugly as fuck."
  - **Simple version:** no settings screen. If QA needs a knob, a QA-only tool.
- **Built:** discovery offers, pausing after ignored offers, and a per-row viewport tracker that writes to the server. All of it came from an agent research note marked "recommendation for discussion".
  - **Simple version:** none of it. The research note was never the ask.
- **Built:** a Rust CLI during a solver task.
  - **User:** "wait you made a RUST cli? WHy? Thats not useful dude."
  - **Simple version:** no CLI.
- **Built:** a `checks.sh` script and a status surface in an agent system.
  - **User:** "what the fuck is the point of checks. SH. It's just scope creep, isn't it?"
  - **User:** "Why do we need a status slash ASA? Like why do you need that? I don't think we need that. I think that's also scope creep."
  - **Simple version:** neither.
- **Built:** CI integration for a simulator automation ask.
  - **User:** "Dude, I didn't ask for a CI and I asked for automation in the simulator. Is this thing trying to put the simulator into our CI?"
  - **Simple version:** simulator automation only.
- **Built:** onboarding steps silently skipped.
  - **User:** "We didn't used to do that, why did you add that? stupid complexity give me a plan to rip that out"
  - **Simple version:** the onboarding flow as it was.
- **Built:** an "RTS snapshots mode" where the user expected the existing arguments.
  - **User:** "what is this RTS snapshots mode? Like, this is not what I expect. ... I've never even used this RTS snapshot thing so I don't know what the fuck this is."
  - **Simple version:** the same arguments the simple solver already takes.
- **Built:** edits to the company website's content during unrelated work.
  - **User:** "Why are you working on the content of our website? Like, I didn't ask you to fucking do that."
- **Built:** perf work in a staging-ops plan.
  - **User:** "I don't need a bunch of perf work here don't scope creep it this is just the initial staging ops plan. Pull it down to somethign for like $250/month"
- **Built:** commits and PRs when the user only wanted to test.
  - **User:** "Why are you committing and opening PRs I didn't tell you to do that. Stop doing that. Just let me know when ready to test"
- **Built:** a reference-algorithm project gathered "safety valves" and extra calculations.
  - **User:** "There's this whole question of extra shit that's not part of RTS that we put on."
  - **Simple version:** the published algorithm, and only it.

**Not overbuild:** the user asked for something big. "I do want it to be a mini workflow engine" means the engine is the ask.

### A2. Speculative generality

**Looks like:** supporting variants, game types, flag types, platforms, scale, offline modes, caching, or future phases before the first one works. Also presuming how the user will use a thing before they have used it once.

**Questions:**
- Which parts exist only for a hypothetical future concern?
- At actual scale (users, rows, images, calls, agents), is this needed?
- What about the spec presumes too much before the user has used it even once?

**Examples:**

- **Built:** a plan to generalize four units of work.
  - **User:** "or do some obscene future-proofing for four units of work, then let's just do the one unit of work."
  - **Simple version:** the one unit.
- **Built:** evaluator hooks that could support games other than the one in use.
  - **User:** "That's like the sort of thing when you don't just want to call a function, right? and it creates complexity. ... We don't need to support games other than nlhe"
  - **Simple version:** call the function.
- **Built:** a "normalized" hand-history format.
  - **User:** "remove the normalized shit I didn't ask for that and its just inviting bugs. ... Just implement our strict subset of OpenHH."
  - **Simple version:** the strict subset.
- **Built:** filtering and compaction of context for a model with a large window.
  - **User:** "the context window on these LLMs is enormous. ... It can handle the full chronological list. You don't need to filter it"
  - **User:** "Why do you need to compact the fucking hand history? Just put the fucking hand history in there."
  - **Simple version:** pass the whole thing.
- **Built:** a design question about what happens when a service goes offline.
  - **User:** "Your question is about what happens when the thing goes offline and you want to build software around that. That's your fucking idea for our startup to focus on right now? ... You really want to add complexity around that hypothetical?"
- **Built:** alerting with tuning machinery before the first alert fired.
  - **User:** "First version can be noisy and we can tune it down from there. Don't preemptively build all sorts of complicated machinery. ... We already have a morning alert system."
  - **Simple version:** add a line to the existing morning alert.
- **Built:** support for tournament and short-deck variants not on the issue's list.
  - **User:** "This doesn't call for short deck, right? Go back to the issue ... and make sure the things that you're saying we should support are on that list."
- **Built:** caching concerns shaping the primary path.
  - **User:** "we can always take the specific OHH and massage it to get better caching performance once we we have the system working end to end."
  - **Simple version:** note the concern and build the path.
- **Built:** a mission day frozen per period, pending zone changes and a 30-minute grace window, all for travellers.
  - **Simple version:** take the local date from each request.
- **Built:** several play modes in a plan.
  - **User:** "the one and only play mode that we intend to support right now, which is heads up, five hand bounded runs ... everything else is cruft"
- **Built:** support for extra flag types.
  - **User:** "I didn't ask for support for additional flag types." And later: "They're all going to be fucking Booleans."

### A3. Outside the task

**Looks like:** the diff touches subsystems, shared contracts, other screens, other repos, prompts, third-party source, or infrastructure the task did not need. This includes changes that alter behavior while the new feature is switched off.

**Questions:**
- Does every changed file serve the stated task?
- Did the change touch a subsystem it only needed to stop using?
- With the feature off, does anything behave differently from before?

**Examples:**

- **Built:** a solver fix that also changed the betting menu and the infoset keys.
  - **User:** "there was at no point scope that I authorized that a) Changed our betting menu and b) Introduced changes to our infoset keys. THis is a bug."
- **Built:** header edits during an achievement fix.
  - **User:** "why the fuck are you workign on the fucking header the whole fucking job was to fucking fix the fucking fire achievement"
- **Built:** edits to the algorithms during unrelated work.
  - **User:** "WHy are you editing the algorithms. That was not supposed to be in scope at all."
- **Built:** a feature switch that also:
  - rewrote Play-tab navigation;
  - reshaped the traditional reward table;
  - paid a traditional day early;
  - overwrote a shared marketing-profile timezone;
  - dropped a uniqueness rule in another feature so it would accept the new flow.

  All of it shipped with the switch off.
  - **Simple version:** revert every change outside the new screen and its launch taps.
- **Built:** a fork of a third-party chat app's source.
  - **User:** "why are you changing the source to librechat I'm not looking to fucking fork librechat"
- **Built:** changes to design files and to onboarding during other work.
  - **User:** "you should not be touching figma at all"
  - **User:** "We are not fucking touching onboarding."
- **Built:** changes to a scripting subsystem the task only needed to stop calling.
  - **User:** "why are you touching the poker scripting stuff stuff, you don't need to touch it. just don't use it please undo do unnecessary changes you made"
- **Built:** a huge PR full of incidental files.
  - **User:** "theres so much crap we should get out of this PR and leave on disk figure out what it is and make the PR less insanely huge"
- **Built:** edits to a stale local checkout instead of the installed tool.
  - **User:** "we use the actual vanilla openclaw installed globally. What is going on why are you editing this old ass clawdbot checkout."

### A4. Invented rules

**Looks like:** budgets, caps, tiers, estimates, exclusion lists, protocols, safety valves, or algorithm steps that trace to nothing the user or the reference said. Agents often invent a plausible rule to make a design feel complete, and then build machinery to enforce it.

**Questions:**
- Where did this constraint come from? Quote the source. If the only source is an agent note, it is a cut.
- "What random constraint did we invent at some point that is making this all way more complicated than it actually needs to be?"

**Examples:**

- **Built:** 410/600-second workload caps, light and regular tiers, planning-second estimates and a lower-work tie-break. All of it came from an agent research note.
  - **User:** "The whole time budget thing… Why do we need that? We don't. That itself is scope creep."
  - **Simple version:** no budget.
- **Built:** changes to a published game-theory algorithm that the reference does not contain: a blueprint fallback, EV calculations, special cases, safety valves hardened into gates.
  - **User:** "Exhaustively inventory all modifications to the algorithm that we put on that are not in the Pluribus Architecture document"
  - **User:** "I'm confused about why we have EV calculations at all ... What is this EV calculation being used for?"
  - **Simple version:** the reference algorithm.
- **Built:** an "action authority" protocol for agents.
  - **User:** "you invented a like plausible protocol, but like it's not really grounded"
  - **Simple version:** delete the protocol and its references.
- **Built:** an exclusion list of entities that could not receive treatments.
  - **User:** "I didn't make those decisions. by default all entities should support all of our treatments. I didn't ask for an exclusion list."
- **Built:** a planner's invented rules.
  - **User:** "You should not be inventing rules dude"
  - **User:** "if it is already fixed just say so dont' invent work."

---

## B. Size and shape: how it got built

### B1. Heavier than the job

**Looks like:** the work is traceable to the ask, but far bigger than the job. The signs are thousands of lines for a small fix, a system where a function would do, a proposal with every option, or a plan that treats an urgent simple goal like a fine-tuned machine.

**Questions:**
- What is the minimum thing that would definitely work, and how far past it is this?
- Is the fix bigger than the bug? "Is the medicine worse than the disease here for this?"
- What is the two-sentence version?
- Would a two-person startup build this?

**Examples:**

- **Built:** a feature whose job was a few hundred lines grew to 18,766 production lines and 104,981 test lines. An independent estimate of the simple version was 700–1,300 lines.
  - **Simple version:** measure the size against the ask before reviewing the details.
- **Built:** thousands of lines to fix a deploy bug.
  - **User:** "if we've got a deploy bug and you add 3,000 lines of code, you just created more problems than you solved."
- **Built:** a proposal with every option.
  - **User:** "Okay, so your proposal is the most overbuilt proposal possible. What is the minimum thing that would definitely work?"
- **Built:** an elaborate internal tool.
  - **User:** "Dude, this is just an internal fucking tool. Why are you making this so fucking complicated? What's the shortest path to get good?"
- **Built:** a configuration system for feature switches.
  - **User:** "this should be a list of fucking booleans in a file commented that I flip them on and off and it just fucking works."
- **Built:** split energy synchronization.
  - **User:** "why do we need to split up energy shit why can't we just synch energy when lesson is over? WHat is the purpose of a more complex solution?"
- **Built:** precise animation coordination.
  - **User:** "I think we just do a JS delay ... it doesn't matter if they aren't perfectly in sync and simplifies the control flow and risk for bugs"
- **Built:** a challenge-scoring model.
  - **User:** "we can do a simpler core which is just like here's a pre-defined set of hands and target BB winning or loses, nothing else for the challenge. Liek 10 hands 1 star = 10BB, 2 stars = 20BB"
- **Built:** layered protections around a bug.
  - **User:** "You're over building, undo that right now. and we're literally just going to put an if statement and a throw."
  - **User:** "why the fuck if we add all these caps and shit, why don't we just fucking set the viewport?"
- **Built:** a wrapper for building an app that is built every day.
  - **User:** "Wait, this is insane dude. I build this app all the time. Why do I suddenly have to have this complex rapper thing?"
- **Built:** agent tooling for a git task.
  - **User:** "Why are you using the fucking agents, the open claw agents? Like this machine is logged in. Just use git."
- **Built:** a file move handled like a migration project.
  - **User:** "this shouldn't be very hard so you must be doing something insanely complicated when it's just a bunch of fucking file moves."
- **Built:** a solver budget with every option exposed.
  - **User:** "dude what is the simplest thing possible. No fucking optiosn AT ALL LITERALLY SIMPLEST POSSIBLE DONT BE SMART DONT FUCKING TRY TO OUTSMART ME"

### B2. New layers

**Looks like:** wrappers, adapters, sanitizers, gateways, command layers, controllers, registries, state machines, event and metrics systems, APIs shaped around one client, or coordination logic that crosses boundaries and can drift.

**Questions:**
- What does this layer buy over a direct call?
- Does it add coordination across a boundary that can drift?
- Every new surface (function, endpoint, file, service) is a new bug vector. Which named need does each one serve?

**Examples:**

- **Built:** a wrapper.
  - **User:** "what the fuck is this wrapper why are we wrapping it and what does it get us?"
- **Built:** an adapter layer.
  - **User:** "if theres no reason for an adapter I don't want more levels of indirection."
- **Built:** an events system and a metrics system in a logging task.
  - **User:** "Why are you doing events, man? Why are you doing metrics? all you're supposed to do is use logging."
- **Built:** sanitizers that pass everything through.
  - **User:** "Dude, why would you put together sanitizers that just pass through? why in what world does that make sense?"
- **Built:** a gateway per agent.
  - **User:** "why are you splitting the fleet into per agent gateways in the first place?"
- **Built:** a Go library compiled to WASM and downloaded to the client.
  - **User:** "which is insane. Did we do that same architecture or did we put this in our Go gRPC server like any sane human would do?"
  - **Simple version:** call the server.
- **Built:** a new card component.
  - **User:** "we don't need new card component for this we just need to change the avatars to use LessonPocketCards"
- **Built:** a conversation fan-out to isolated agent sessions.
  - **User:** "You're the one that invented one conversation fans out to multiple agents with isolated sessions. I didn't say that. ... they're in the fucking room and that's it."
- **Built:** an API shaped like the UI.
  - **User:** "You're overengineering. the API should be a clean API for poker, not like a UI mapped API."
- **Built:** a planned bundle of extras.
  - **User:** "We don't need full heart effect only. We don't need rich transport ... We don't need a general framework. We don't need a bigger CLI operator surface. We don't need extra verification machinery"
- **Built:** a CLI in front of an existing test tool.
  - **User:** "Why do you need a CLI? like we have maestro Right? Explain the need for a CLI."
- **Built:** a command layer beside the owning store.
  - **User:** "Yeah, that command layer seems like bullshit. I like a single source of truth."
- **Built:** a workflow app where a metrics dashboard was asked for.
  - **User:** "This is like some sort of insane workflow thing not a metric dashboard ... Did you even look at our old evidence site"

### B3. Flags, modes and options

**Looks like:**
- feature flags and kill switches;
- env vars and dev gates;
- CLI arguments and optional modes;
- dry-run, preview, or verbose modes;
- "optional" phases;
- a settings registry.

**Questions:**
- Could this be one correct way, always on?
- Would making the value required remove branches?
- Is a flag still gating a feature that should just be on?

**Examples:**

- **Built:** a feature flag on new behavior.
  - **User:** "I don't want that feature. I want it always enabled. please don't put it behind a feature flag."
- **Built:** a toggle on something the user wanted off.
  - **User:** "dude i don't want it behind a fucking toggle I wanted it fucking disdabled"
- **Built:** kill switches in a release plan.
  - **User:** "Dude, why do we need kill switches? I don't fucking get it. The last thing that we regressed, we fixed by updating our app's fire setting."
- **Built:** on/off flags for pipeline stages.
  - **User:** "flags to turn things off/on feel like an overbuild. its bad now. Why not just turn it on?"
- **Built:** optional versus required app updates.
  - **User:** "What if we just make every update required? Just simplify this whole fucking thing. Do we delete a lot of code"
- **Built:** a "policy mode".
  - **User:** "fine what is this policy mode crap?"
- **Built:** a temporary dry-run mode.
  - **User:** "I dont' know what this temp dry run shit is for, its all jsut confusing complexity. We should fix the bugs, cut the unecessary shit"
- **Built:** a monetization flag.
  - **User:** "rip out th emonetizationEnabled feature flag and always have monetization enabled for everyone"
- **Built:** extra arguments on a generator.
  - **User:** "lots of extra args that increase complexity and produce no value. Make it rewrite the whole lesson, in place, update interface to simplify."
- **Built:** a verbose-logging mode and log gates.
  - **User:** "I don't need you to gate chatty logs. ... you trying to predict and add features like verbose logging mode and this sort of stuff just drives me nuts."
- **Built:** a flag proposed as a way to disable something temporarily.
  - **User:** "do not propose some bullshit like fucking feature flags. I mean like fucking commenting shit out."
- **Built:** a 60-field settings registry for a missions feature.
  - **Simple version:** constants in code.
- **Built:** options everywhere.
  - **User:** "do we need lots of options or do we need this to work in one correct way and what is that?"

### B4. Guards and gates

**Looks like:**
- allow-lists and caps;
- try/except around dependencies that are always present;
- loud invariants where the contract says clamp;
- drift bans and CI enforcement against a reference about to be deleted;
- security machinery for a pre-launch or VPN-only tool;
- production code that tolerates a broken staging environment.

**Questions:**
- Would fixing the cause remove the need for the guard?
- Was the risk observed, or imagined?
- Is temporary code wrapped in gates as if it were permanent?

**Examples:**

- **Built:** try/except around a shared formatter.
  - **User:** "a shared formatter should always be present, don't even wrap that shit in a try except block, no safe cases there."
- **Built:** CI drift bans during a port.
  - **User:** "dude I don't want CI drift bans, I don't want overbuild. I literally just want to achieve parity and then stop . RN is being deprecated"
- **Built:** guard scripts.
  - **User:** "We don't need any guard scripts, just fucking clean the shit up"
- **Built:** a loud invariant.
  - **User:** "you don't need a loud invariant just it just stays to the last level If it's off the end, it clamps to the last one. Just make it work."
- **Built:** an allow-list gate.
  - **User:** "lets just remove this alllowed kinds gate, so all kinds are allowed"
- **Built:** production code that tolerates a broken staging environment.
  - **User:** "We don't need to put code in our main that forever handles staging being in a weird state because somebody is doing development testing against it."
  - **Simple version:** fix staging.
- **Built:** security work on a pre-launch prototype.
  - **User:** "I want the simplest, fastest version to get going without any of the security horse shit."
  - **User:** "some of your questions make mea fraid you're moving into nasa grade security and extreme scope creep."
- **Built:** a "too obvious" gate.
  - **User:** "hold on what is this too obvious gate, is it fucking us over? I never wanted it its one of those things that AI just builds and I discover later"
- **Built:** dev gates around debug code.
  - **User:** "We don't need stupid gates, we'll delete the code right after."
- **Built:** a very cautious migration.
  - **User:** "Why are we being so ridiculously cautious about this? Is it really any more dangerous than all of the other migrations and stuff we always do?"
- **Built:** API gating added during a fix.
  - **User:** "Are we accomplishing my goal of removing all the fucking API gating that we just fucking added for no reason ... Are we preemptively putting more safety measures in place"

### B5. Extra state

**Looks like:**
- caches, leases, timers, drafts, sessions;
- history windows, lineage, revisions;
- stored fields, markers, historical references;
- bookkeeping that could be derived or forgotten.

**Questions:**
- Is this state worth remembering?
- Can it be derived from the source on read?
- Is a cache covering for the real fix?

**Examples:**

- **Built:** image leases.
  - **User:** "we don't need image leases if we are deduping and preventing images from being loaded twice. There's like 100 images in the whole game."
- **Built:** an image cache, a canvas cache and an asset bank.
  - **User:** "Why do we need an image cache, an app canvas cache, and a perspective scene asset bank? ... Are you just like naively supporting multiple sources of truth"
- **Built:** several info-state maps.
  - **User:** "I don't even think we need multiple info state maps. Like we can just have one."
- **Built:** a draft mechanism for assignments.
  - **User:** "I hit enter, its assigned. period. Go rip out this draft shit and just make it instantly save"
- **Built:** timers.
  - **User:** "dude literally we don't need these timers, just when they hit it, wipe them and tell them you did it. This isn't so precious."
- **Built:** a drill timing field.
  - **User:** "remove this drill timing field entirely. its brittle and not required."
- **Built:** remembering partly finished lessons.
  - **User:** "make a proposal for how we can remove this as a requirement (e.g. its fine to forget someone did a partial lesson)"
- **Built:** a cache as a fix.
  - **User:** "I want the RIGHT CORRECT FIX NOW not a stupid cache fix."
- **Built:** a 14-day history window and its column, mid-day row replacement, row lineage, row revisions and credit segments.
  - **Simple version:** keep each issued row as issued and compute credit on read.
- **Built:** streak centralization that turned every read into a database write, with 45–90 SQL statements per read plus repair bookkeeping.
  - **Simple version:** read, don't write.
- **Built:** historical owner references in docs.
  - **User:** "When you reference something, you create confusion. So creating historical references is just creating confusion."
- **Built:** required sessions.
  - **User:** "we should simplify this by not requiring sessions, and haveing the persistence just be something we do for debugging"

### B6. Retry, repair and recovery

**Looks like:**
- retry loops and retry buttons;
- background repair passes and replay-on-read;
- pending states and degraded modes;
- rollback lanes and always-on pollers;
- dedupe and rate-limit layers;
- pause machinery.

**Questions:**
- Has this failure actually happened?
- Would failing loudly be simpler and more honest?
- Can the recovery machinery freeze or block the main job?

**Examples:**

- **Built:** degraded modes and retry modes in a plan.
  - **User:** "we don't have degraded modes We don't have retry modes. If it breaks, it breaks loud. and then I fix it"
- **Built:** a retry button.
  - **User:** "look dude if something breaks like it's not going to fucking work to retry it. It's just a worthless retry button."
- **Built:** loading and retry states.
  - **User:** "Why do we need a loading state? Why do we need a retry state? No you're building in all sorts of shit that I don't fucking want."
- **Built:** a rollback path.
  - **User:** "no rollbacks no fallbacks please, remove that from code. ... Don't create dual code paths, don't create hidden bugs by trying to gracefully degrade. Just fail if it fails."
- **Built:** a missions feature with:
  - triple retry loops;
  - credit repair that replayed history on every read;
  - a pending-payment state;
  - a 30-second background pass;
  - client resends.
  - **User:** "I need write failure to blow up so I can figure out why."
  - **Simple version:** credit from native records on each read, and throw on write failure.
- **Built:** a kill-on-failure fix that became SIGSTOP pause machinery (+469 lines). A coordination lease was allowed to decide whether the main process runs.
  - **Simple version:** kill on failure. A side service must never control whether the main job runs.
- **Built:** an agent repair path.
  - **User:** "you're still overbuilding like you don't need to build an agent repair path It's usually the JSON path, over-specified."
- **Built:** retry harnesses for agents.
  - **User:** "the agents using it can interpret the skill instruction and try again in a moment there sno need for harnesses for retries"
- **Built:** an always-on post-release poller.
  - **User:** "this is a LOT of side band architecture for what we ultimately want as a simple feature."
- **Built:** dedupe and rate limits in an error channel.
  - **User:** "I just want fucking errors to go to the work log. I don't want this preempted dedupe rate limit."
- **Built:** a retry-heavy experiment process.
  - **User:** "There's this bias towards retrying on rather than going and resampling. Where is that happening?"
- **Built:** a policy that tries one abstraction, then the other.
  - **User:** "it looks like you built a retry with different abstraction level thing which looks like a hack to me ... a place that's going to obfuscate bugs"

### B7. Heuristic instead of signal

**Looks like:** inferring what the user or the data already states; regexes where a structured output exists; progress guessed from side effects; special cases layered in.

**Questions:**
- Is there a direct signal (a stated answer, a schema field, an explicit input) being ignored?
- Does the design compute something the data already states?

**Examples:**

- **Built:** missions that inferred interests from behavior while the player's stated interests set only a tie-break. Also a "changed direction" signal that could not fire, and a daily-time answer that was read and never used.
  - **Simple version:** stated interests, goals and play frequency set the picks.
- **Built:** a computation of puzzle correctness.
  - **User:** "you don't need to calculate any of that stuff. It's just like the puzzle, the JSON, on like our schema says, oh, yeah, this person's the correct answer."
- **Built:** regexes over model output.
  - **User:** "I didn't realize you were trying to build a heuristic. That will not fucking work. Undo that immediately. I thought what you were doing was using the output of the extractor LLM contract"
- **Built:** a preset developers must type.
  - **User:** "do we really need the devs to type that in? Can't we know that on our own?"
- **Built:** release notes built from "changes since the last build".
  - **User:** "it's just like this heuristic. What was since the last one, but that's not how it works. That's not how we work."
- **Built:** layered special cases.
  - **User:** "weird additional heuristics layered in places like special cases ... just weird fallback conditions, hiding bugs"

### B8. Code where judgment belongs

**Looks like:** Python scripts, keyword matching, deterministic helpers, "healing hints", heuristic cues, or gate scripts written for agents. The intended behavior was an instruction, an example, and the agent's own tools.

**Questions:**
- Is a prompt-only change being turned into code?
- Could a clear instruction plus the agent's own tools do this?
- Does the script remove the agent's judgment?

**Examples:**

- **Built:** harness scripts and keyword matching for agent behavior.
  - **User:** "No brittle heuristics, no shims, no fucking harness scripts, no keyword matching ever."
- **Built:** a Python helper for agents that can already search.
  - **User:** "Like they can use JQ like they can write little scripts. You don't need to write it for them."
- **Built:** a deterministic puzzle generator in a skill.
  - **User:** "I don't want a deterministic fucking puzzle. Fucking delete that. I want in the skill for you to specify, here's what the output looks like."
- **Built:** heuristic scripts from the start.
  - **User:** "Why are you building fucking heuristic scripts into this from the beginning? ... I want intelligent agents. Where the fuck else did you do that?"
- **Built:** code for a prompt tweak.
  - **User:** "DO not turn this into a heuristic or shim or some shit. I'm asking for prompt tweaking"
- **Built:** a "parity helper".
  - **User:** "What is this parody helper? Are you building some sort of fucking shim or script or something?"
- **Built:** a sync shim.
  - **User:** "No, no fucking shims. ... It should be in doctrine. It should be like a list of files we gotta go update and they should all match."
- **Built:** a healing hint to make validation pass.
  - **User:** "No the LLM should heal based on the feedback from the errors from validation. You cannot introduce some new stupid pattern to get the test to pass"
- **Built:** new artifacts for agent behavior.
  - **User:** "We don't need new artifacts...we could literally just give the prompt some tweaking and expose the tools with good docstrings as a start yes?"
- **Built:** a script where self-healing agents were wanted.
  - **User:** "You built a fucking script, didn't you? ... the point is an anti-fragile system that self-heals"

### B9. Reinventing what exists

**Looks like:**
- new code, formats, harnesses, databases, or processes where the repo, framework, platform, or an earlier result already does the job;
- writing from scratch instead of copying and adapting.

**Questions:**
- Does an existing owner, tool, pattern, or result already do this?
- Was a new mechanism invented instead of following the existing one?

**Examples:**

- **Built:** a new benchmark harness.
  - **User:** "You don't need any stupid P80 harness. We have the ability to fucking replay hands."
- **Built:** a test database.
  - **User:** "Why are you creating a testing database, dude? Just use our fucking database."
- **Built:** raw SQL against a service.
  - **User:** "why are you putting SQL rather than using front door db api for grinder"
- **Built:** a new YAML format.
  - **User:** "Why are you doing this in YAML Like you're like inventing your own format for everything. When the lessons pod already shows us how to do this"
- **Built:** a Python model beside a Go backend.
  - **User:** "why did you build a python model though, ourbackend is go and uses ssqlc and grpc to communicate with client."
- **Built:** code from scratch.
  - **User:** "you have a tendency to implement from scratch. It's really important right now that you don't write any unnecessary new code."
  - **User:** "step one can only be created by copying files and editing them, not by writing code from scratch"
- **Built:** sideband processes beside a framework's conventions.
  - **User:** "have we created sideband processes that are unnecessary after you understood paperclip better"
- **Built:** a rerun of finished work.
  - **User:** "fucking kill the re-run and fucking use the shit we already did"
- **Built:** manual bootstrapping.
  - **User:** "why are you manually bootstrapping? you should let the experiment bootstrap"
- **Built:** a new fallback order.
  - **User:** "You should have followed the same fucking fallback waterfall as the NLHE non tournament path. Did you invent some bullshit instead?"
- **Built:** a second heartbeat mechanism.
  - **User:** "Paperclip already has its heartbeat protocol ... What causes us to need this Hermes thing?"

---

## C. Old stuff kept alive

### C1. Dual paths and shims

**Looks like:**
- backward compatibility, deprecation instead of deletion;
- re-exports, overloads, thread-locals, or new constructors added so callers don't have to change;
- legacy paths kept beside new ones;
- "temporary mitigations" in a one-pass change;
- escape hatches.

**Questions:**
- After the new path lands, is the old path deleted in the same change?
- Is there a shim whose only job is to avoid updating callers?
- Is compatibility kept for a consumer that does not exist (one user, no production data)?

**Examples:**

- **Built:** a migration with shims.
  - **User:** "no dual paths no shims no fallbacks no silent failures everything blows up loud and explicitly no legacy behaviors no preserving optionality."
- **Built:** a new overload.
  - **User:** "Nope, don't add an overload. Change the primary function."
- **Built:** compatibility with something built that morning.
  - **User:** "we literally just built dimming today we're trying to maintain legacy compatibility with earlier today?"
- **Built:** re-exports of old names.
  - **User:** "dude you need to get the code into the new naming convention not fucking reexport it don't leave crufty old code around"
- **Built:** disabled legacy code.
  - **User:** "hey don't disable legacy shit, delete it."
- **Built:** deprecation markers.
  - **User:** "Our new fields are the fields, period. Delete, don't deprecate, comment out, etc. JUST REMOVE."
  - **User:** "*DO NOT DEPRECATE AND DO NOT LEAVE FOR FOLLOW ON PASSES FUCKING MARK IT AND DELETE IT AS PART OF THE PLAN NO FUCKING CRUFT"
- **Built:** an interim mitigation.
  - **User:** "remove this "temporary mitigation" we're doing this all in one pass don't create complexity"
- **Built:** options piled on instead of integrating the new approach.
  - **User:** "the thing you do where you just keep fucking piling on more options rather than integrating the new approach fully"
- **Built:** an escape hatch.
  - **User:** "okay delete this escape hatch entirely."
- **Built:** a logging shim over monkey-patching.
  - **User:** "fuck can you just delete this shim thing and instead just stop monkey patching logging?"
- **Built:** thread-local state to avoid changing signatures.
  - **User:** "No dual path. No shims. big bang break everything and then put it back together single point in time"
- **Built:** a legacy product path kept beside its replacement until a 58,539-line rip-out.
  - **Simple version:** delete it when the replacement lands.

### C2. Second owner

**Looks like:**
- two updaters or two policies;
- a client copy of server rules;
- a parallel model in another language, or a second test stack;
- duplicate scripts, competing versions, or documents that repeat each other;
- a prompt restating what code enforces;
- a second auth system beside the first.

**Questions:**
- Why do we have two? Which one is canonical, and why does the other survive?
- Where can two places now answer the same question (split brain)?
- Did we create a new pattern where a clean one existed?

**Examples:**

- **Built:** a parallel queue for deferred gameplay events.
  - **User:** "did you just create a parallel implementation ? I thought we had something centralized for these "queue and do later" during gameplay events?"
- **Built:** a second compact policy.
  - **User:** "Delete this second policy. You're just making complexity. Fucking remove it."
- **Built:** two updaters.
  - **User:** "why are there two updaters? And is one of them now not used and should we delete it?"
- **Built:** a client-side copy of the credit rules that celebrated before the server answered.
  - **Simple version:** the client shows what the server paid.
- **Built:** two baselines.
  - **User:** "Why do you have two bass lines? There's there should only be, in my opinion, the current winner and the comparison candidate."
- **Built:** two files to update.
  - **User:** "I just don't want to have to update two files on disk"
- **Built:** several difficulty measures.
  - **User:** "we don't want multiple ways of measuring difficulty floating around the system."
- **Built:** a prompt telling a model what code already enforces.
  - **User:** "The prompt shouldn't be told this stuff that is enforceable determinsitically"
- **Built:** competing scripts.
  - **User:** "a single script that does everything and get rid of the competing scripts"
- **Built:** a split architecture written into a plan.
  - **User:** "That just seems like unnecessary split architecture that we just memorialized."
- **Built:** version proliferation.
  - **User:** "do we actually need all these competing versions for real, or can it be simplified?"
- **Built:** three overlapping docs.
  - **User:** "I want to stop having three separate documents that are confusing. I want a single markdown document"
- **Built:** a new auth layer.
  - **User:** "Are you saying this is in addition to CLERK?"

### C3. Dead code kept

**Looks like:**
- unused code, or code used only by its own tests;
- archived copies, quarantined components, pointer stubs;
- leftover rollout or experiment machinery;
- stale checkouts;
- widgets nobody can explain.

**Questions:**
- Is this used by a real user-facing path? A test that uses it does not count.
- Is removed material deleted, or archived, quarantined, or left as a pointer?
- Is anything left over from a finished experiment or rollout?

**Examples:**

- **Built:** a quarantine for retired code.
  - **User:** "And we're not gonna quarantine shit, we're going to delete it."
- **Built:** code preserved because a test used it.
  - **User:** "Why are you trying to preserve stuff that's not used? When I say used, I mean user facing features, right? Not just like, "Oh, some test somewhere uses it.""
- **Built:** a stale test quarantined.
  - **User:** "If it's a stale test, deliver product change, just delete it. I don't want quarantine crap. We have everything in Git."
- **Built:** pointers left after consolidating docs.
  - **User:** "no, just delete it once consolidated I don't want fucking pointers laying around"
- **Built:** containment of a low-value component.
  - **User:** "It should not "quarantine" EV rollouts just fucking delete that shit"
- **Built:** leftover experiment enrollment.
  - **User:** "So is there leftover machinery for a rolling in the StreakFreeze experiment?"
- **Built:** a hello-world widget.
  - **User:** "atlas hello world widget seems like we should delete it I don't know what the fuck that is Is it even used?"
- **Built:** dead code removed one piece at a time.
  - **User:** "delete it all stop making me tell you one by one to fucking delete the code that we we don't use anymore."
- **Built:** a warm-start path that did nothing.
  - **User:** "then we can remove the warm start behavior in API.RS, right? because that doesn't actually do anything."
- **Built:** agent configuration left over from weaker models.
  - **User:** "remove all this HZL crap from our hermes agents its cruft ... holdovers from before the models were good enough on there own"

### C4. Debug residue

**Looks like:** probes, performance monitors, investigation logging, audit code, capture systems, event firings, "null comment" leftovers.

**Questions:**
- Which diagnostics added during the investigation are still in the diff?
- Does this instrumentation cost runtime for no ongoing use?

**Examples:**

- **Built:** a custom performance monitor.
  - **User:** "Its just like this sprawling thing that is hurting everything> I want a plan to rip out that crap and instead use react native performacne and skia provided performance metrics"
- **Built:** hot-path probes.
  - **User:** "review all of the just probes and stuff we've added the hot path feels fairly poluted right now"
- **Built:** probe leftovers.
  - **User:** "you remove the E to E probe, but you've left this like null comment thing. What is that? Why do we need that?"
- **Built:** a one-off event.
  - **User:** "literally just remove that event firing. Thats just a useless overboard event, then remove it from the catalog and CLI"
- **Built:** a capture-readiness system.
  - **User:** "delete this whole capture readiness system. like I don't want this in my fucking code base this is insane It's not worth it. It also gives false reads."
- **Built:** more metrics during a readability cleanup.
  - **User:** "if you are adding more metrics or diagnostics you are fucking up bad. The point is to remove them from obscuring the code"
- **Built:** a fix wrapped in scaffolding.
  - **User:** "rip out all that shit except leave the shading fix that we made in simply and comment it ... I don't need any more unit tests. I don't need any harnesses."
- **Built:** debug output with a production cost.
  - **User:** "anything that is likely a point in time debugging or will add production overhead for no benefit"

---

## D. Hiding failure

### D1. Fallbacks

**Looks like:**
- silent defaults and "try A, then B";
- errors relabelled as "unavailable";
- empty states that sanction a failure;
- a fallback to a baseline, a default policy, or bash;
- optional fields where missing data is a bug.

**Questions:**
- Is the fallback added on an assumption rather than a demonstrated need?
- Does it cover for the system not knowing its own state?
- Where could the user be deceived without knowing it?

**Examples:**

- **Built:** "safe" fallbacks.
  - **User:** "safe fallbacks just hide failure paths man, i'd rather ahve it blow up and let me know theres a bug"
- **Built:** a fallback anywhere in a system.
  - **User:** "if theres even a thing called a fallback we know something is hideiously wrong. This system shouldn't use fallbacks it should explicitely fail."
- **Built:** a fallback for one call site.
  - **User:** "hold on, why do we need a fallback? Are you like assuming we do? If it is just in this one place why do we need that?"
- **Built:** a navigation fallback.
  - **User:** "fallbacks because we don't know if we have a root nav during normal usage is lazy as fuck"
- **Built:** UI fallbacks for missing data.
  - **User:** "i consider the fallback behavior  a bug in the UI it shouldn't ever need to fallback"
- **Built:** a plan full of optional rows and fallbacks.
  - **User:** "All the places that you put things is optional or with fallbacks, like this if it doesn't have a row in the blueprint. Like, those are fatal errors."
- **Built:** errors relabelled as "unavailable" and silent launch failures.
  - **Simple version:** every failure reaches the error tracker with its original error, and the player sees only what the server paid.
- **Built:** a fallback to bash when a TTY tool is present.
  - **User:** "I have a TTY, gum is installed, and you're not going to just fall back to bash"
- **Built:** a fallback that hid the real bug.
  - **User:** "I bet our Rust AI server that we're hitting is running a different branch. Undo that fallback"
- **Built:** a fallback instead of the right design.
  - **User:** "Why do we have fallbacks, dude? Why are we not just doing this the one correct way?"
- **Built:** a fallback in a data lookup.
  - **User:** "no fucking fallbacks. Are you telling me you can't find any info in the kib?"

**Not overbuild:** a visible, counted fallback the user approved, such as a neighbor-fallback ladder or an explicit `--allow-uniform-fallback`. The rule is: "I want fallbacks to be a permission only behavior, otherwise fail loud."

### D2. Guessed fixes and hacks

**Looks like:**
- speculative changes made before the cause is known, and left in;
- edits that had no effect;
- special cases so a test or eval passes;
- hacks around a local environment problem.

**Questions:**
- Does each change in the diff have a measured effect on the diagnosed cause?
- Is anything special-cased so the current test passes?

**Examples:**

- **Built:** speculative fixes during debugging.
  - **User:** "i didn't tell you to make fucking speculative fixes. I only want diagnostics until you're 100% sure."
  - **User:** "remove the attempted fixes man I don't want shots in the dark I watn certainty via diagnosis"
- **Built:** an edit with no effect.
  - **User:** "undo that it had no impact so I don't want to acumulate code"
- **Built:** a hack to make evals pass.
  - **User:** "this is absolutely not our pattern and it wouldn't even get through PR this seems like a hack to work around prompt engineering to make evals pass"
- **Built:** a 1px hack.
  - **User:** "this 1px thing was a hack ... I would just assume you'd immediately revert it and figure out what the real fix is"
- **Built:** a tool patched around a shell problem.
  - **User:** "why do you keep fixing it by hacking up aimgr rather than by fixing my shell?"
- **Built:** a shim when a restart was the fix.
  - **User:** "undo that I just neede dto restart codex, now it'll work without the stupid shim"
- **Built:** prompt special cases.
  - **User:** "You're still special casing it. ... it means my first test will pass and then future ones might fail"
- **Built:** a reactive fix.
  - **User:** "It feels like you're being reactive to the error rather than stepping back and saying from first principles ... Do we need this complexity?"
- **Built:** hacks instead of instrumentation.
  - **User:** "why are you fucking hacking at this why are you not fucking just instrumenting at the ground truth source and figuring out the root cause"

---

## E. Proof and tests

### E1. Test sprawl

**Looks like:**
- unit tests for one-time conversions;
- new test harnesses, test databases, fixture platforms, over-the-wire tests;
- test ladders;
- tests that fail by design;
- testing the whole app for a narrow change;
- rerunning unchanged suites;
- a second test stack in another language.

**Questions:**
- What is the smallest set of tests that proves this change?
- Does an existing tool or suite already cover it?
- Are we retesting things that never change?

**Examples:**

- **Built:** a unit-testing plan for a one-time conversion.
  - **User:** "Okay all this unit testing shit is insane and completely overbuilt. Rip all of it out of the plan."
- **Built:** a whole-app test pass.
  - **User:** "Why are you testing every single part of the whole goddamn application? We were just making some lessons and then making them testable."
- **Built:** a smoke-test step.
  - **User:** "why are you smoke testing just fucking run it dude"
- **Built:** a test ladder.
  - **User:** "the plan should not just be a run this ladder plan, which is something that you like to build. It should be a, here's the simplest set of tests"
- **Built:** repeated testing of stable code.
  - **User:** "there have to be some simplifying assumptions some shit just never changes we test it over and over again."
- **Built:** a test that fails by design.
  - **User:** "why do we have a failing test by design idk what the fuck your'e talking about, remove it if its not useful."
- **Built:** holdouts in a simple framework.
  - **User:** "You took my simple framework and you like hacked in as much complexity as you could ... You put you you hacked in holdouts?"
- **Built:** Python tests beside a Rust stack.
  - **User:** "why are you making python tests, we can test in rust against our mcp can't we?"
- **Built:** a missions feature with 104,981 test lines against 18,766 production lines, including over-the-wire tests and a fixture platform.
  - **User:** "over-the-wire tests are fucking nuts."
- **Built:** redundant Flutter test coverage.
  - **Simple version:** a later single commit removed 289,738 lines of it.
- **Built:** files kept only for tests.
  - **User:** "if they're not used or if they're legacy, If they're only used by a test, I want to just remove them."
- **Built:** a test process.
  - **User:** "please do not run unit tests and shit we don't need a fucking bunch of time wasted on that bullshit"

### E2. Proof ceremony

**Looks like:**
- golden sets, drift preventers, certificates, certification systems;
- hashes and receipts;
- output schemas, screenshot baselines;
- determinism promises and seeds, n=3 repeated runs;
- evidence plans heavier than the change.

The vocabulary itself is a tell: proof, receipt, pin, certify, gate.

**Questions:**
- Does any downstream consumer actually want this proof?
- Is the proof bigger than the plan?
- Would turning the thing off answer the question faster than measuring it?

**Examples:**

- **Built:** guards, drift preventers and golden sets in a plan.
  - **User:** "where are we overbuilding? This isn't a space ship. We don't need insane guards and drift preventers and golden sets and shit"
- **Built:** an output schema for an evaluation.
  - **User:** "look an output schema sounds insanely over built, why do you need that? We know what the fuck we're evaluating for don't we?"
- **Built:** proof in general.
  - **User:** "Every time you say the word "proof" you're overbuilding."
- **Built:** repeated runs.
  - **User:** "why do you even need n=3 runs this isn't fucking nasa."
- **Built:** a `--seed` flag promising determinism the system cannot deliver.
  - **User:** "we do not support --seed, rip it out, we don't pretend to have determinism anymore its too hard with multithreading"
- **Built:** certification machinery around a stable system.
  - **User:** "I don't fucking understand what we think we're doing with the certification shit. It just seems like an insane overbuild"
  - **Simple version:** a later rip-out removed 66,141 lines.
- **Built:** git-hash evidence that agents produced constantly, though the user never asked for it.
  - **User:** "I want all the stupid fucking git hash bullshit to go away. It was insane. I just wanted them to fucking commit their work"
- **Built:** screenshot verification.
  - **User:** "remove the idea of having screenshtos to verify against entirely, you won't get those."
- **Built:** quantifying a visual bug.
  - **User:** "There's no point in quantifying the bug, right? ... if I fucking turn it off, does everything look better? Isn't that just the simplest approach?"
- **Built:** a proof burden bigger than the plan.
  - **User:** "Sometimes its proof burden and supporting harnesses are so overbuilt its bigger than the plan."
- **Built:** proof for downstream consumers.
  - **User:** "okay thats insane. What proof may other downstreams actually want go fully audit it. Are there any?"
- **Built:** solver receipts committed to a repo.
  - **Simple version:** a later cleanup untracked 5.13M lines of them.

---

## F. Process and prose

### F1. Process overhead

**Looks like:**
- review rounds that repeat, and the full panel convened for small things;
- CI awaited every turn;
- draft PRs and PR stacks;
- approvals in a worktree;
- careful phase ladders for urgent simple goals;
- reruns;
- extra worktrees;
- plans written where a fix would do.

Review loops are a special danger: every valid finding becomes a requirement.

**Questions:**
- How many review rounds, CI runs, and approvals does this plan imply? Would one of each, at the end, do?
- Can review expand the approved plan? It must not.
- Is a plan being written where a direct fix would do?

**Examples:**

- **Built:** about 20 reviews of a cleanup spec.
  - **User:** "you though 20 reviews was acceptable that insane."
  - **Simple version:** one review, then implement.
- **Built:** CI waits every turn.
  - **User:** "we don't need to keep waiting for CI on every fucking turn. We can do CI at the very end after pro has cleared everything."
- **Built:** draft PRs.
  - **User:** "I don't know why we have draft PRs. What's the fucking point? ... We don't need all this ceremony around these fucking PRs."
- **Built:** a PR stack.
  - **User:** "I hate this PR stack. I just want one branch with all of our work on it."
- **Built:** a plan for a fix.
  - **User:** "propose to me the fix, not a plan for the fix, but like the actual fix, we've got a bunch of fucking ceremony"
- **Built:** recursive reviews that grew the scope.
  - **User:** "review what we originally scoped, and what got overbuilt and crept in as a result of yoru recursive reviews"
- **Built:** a plan that went through 21 review waves and grew to 121 files and +11,646 lines.
  - **Simple version:** freeze the ask, run one review, and reject findings that add scope.
- **Built:** the full panel for every question.
  - **User:** "why are you sending this to all the full panel constantly. Stop doing that. You only need to do that when we hit a real blocker."
- **Built:** approval stops in a worktree.
  - **User:** "You're working in a work tree on a dev machine. You're not gonna do any fucking harm. You don't need fucking approvals."
- **Built:** stop gates mid-build.
  - **User:** "update plan remove all gates that require em to stop and do shit until very end the whole point is you can build autonomously."
- **Built:** long reruns.
  - **User:** "don't just rerun things over and over again. like two and a half fucking hours is fucking insane."
- **Built:** a careful rollout plan for a broken system.
  - **User:** "your plan is assume this is a fine-tuned machine and very carefully land each piece. When what I really want is just to race"
- **Built:** a review for a doc edit.
  - **User:** "you don't need a new review for a fuckign doc change"
- **Built:** extra worktrees.
  - **User:** "wait how many fuckign worktrees are you working out of and why did you make worktrees?"
- **Built:** an epic edited 21 times, milestones recut several times, and a 435,790-character reviewer prompt.
  - **Simple version:** one plan and one review.

### F2. Doc and prompt bloat

**Looks like:**
- over-specified goal prompts;
- restated doctrine and per-agent pointers to shared rules;
- archaeology and plan talk in skills;
- optional phases;
- several bullets where one line would do;
- new docs nobody asked for;
- "second path" alternatives in an authoritative doc;
- query lists for agents that can find their own data.

**Questions:**
- Does every line earn its place?
- Is anything restated that already lives elsewhere? Delete the copy rather than fixing its wording.
- Does the document carry history instead of current truth?

**Examples:**

- **Built:** an over-specified goal prompt.
  - **User:** "Please don't over specify the goal prompt... The goal prompt is just the reminder of what we're doing."
  - **User:** "stop restating shit that's in the fucking documents, in the goal. You're just like muddying everything."
- **Built:** a skill with history in it.
  - **User:** "I don't want archaeology. No exposition, no plan talk in this skill. The skills all need to be timeless."
- **Built:** a four-bullet explanation.
  - **User:** "That's overexplained. You don't need fucking four bullet points to explain that"
- **Built:** a long outcome statement.
  - **User:** "Even simpler. There's like a two sentence version of the outcome I'm looking for."
- **Built:** duplicated wording.
  - **User:** "I would rather things be moved or removed entirely if they are already stated elsewhere rather than try to correct the wording in multiple places."
- **Built:** an optional phase.
  - **User:** "We don't have like phase two optional. what the fuck is that horse shit? ... if it's optional, then let's not have it in our goddamn document."
- **Built:** instructions a runtime already follows.
  - **User:** "remove the instruction on how to run the subagent idiot codex does tihat itself"
- **Built:** query lists for a capable agent.
  - **User:** "remove theo sfucking query lists the whole point is that the agent can read psmobile materials and pull all its own reports"
- **Built:** a new doc mid-audit.
  - **User:** "why the fuck did you just make a random new doc. How is that helping me?"
- **Built:** a second path in an authoritative doc.
  - **User:** "remove the second path from the doc the "if a central router path" so the doc is authoritative"
- **Built:** a detailed spec for something small.
  - **User:** "Nope, you're going way too detailed. Like this can be really simple."
- **Built:** per-agent pointers to shared doctrine.
  - **User:** "Don't you don't need pointers if it's already shared doctrine. Just fucking delete it."

### F3. Caution and authority plumbing

**Looks like:**
- approval gates, halt triggers, "ask the user first" rules;
- non-negotiables over the user;
- redaction and PII checks, security refusals;
- workflow enforcement, default crons, gate checklists;
- agents deciding budgets or doing the user's job.

**Questions:**
- Which gates, approvals, or halt rules did the agent add without being asked?
- Does this guard dictate the user's workflow?
- Is the agent adding caution where the user is trying to remove it?

**Examples:**

- **Built:** caution rules in a skill.
  - **User:** "I fucking hate this crap the agents already halt too much what other bullshit was put in out of an overabandunce of caution? RIp it out."
- **Built:** risk-triggered early checks in a plan.
  - **User:** "this whole thing with earlier checks, when a specific risk requires them, is a place where you're inserting caution that I didn't ask for. ... I'm trying to get you to turn down the caution level and you're just reflexively turning it up."
- **Built:** redaction tests.
  - **User:** "Why are you testing redaction? I fucking told you to stop doing the redaction bullshit. Rip all the redaction tests out"
- **Built:** a Slack approval flow for content edits.
  - **User:** "Just assume that they edit and then it goes live in the database as a new version ... This fucking neat approval thing is overbuilt."
- **Built:** "ask the user first" in agent instructions.
  - **User:** "remove the bullshit that said ask me to do it. THEY DO IT THEMSELVES"
- **Built:** a workflow guard.
  - **User:** "Yeah, I hate that fucking guard. That's your bullshit. ... I do not want you dictating my fucking workflows. Remove that fucking guard."
- **Built:** a plan that did the user's job.
  - **User:** "please remove the parts of this that are you trying to do my job. Like gates, budget decisions, "morning watches"."
- **Built:** self-limiting rules.
  - **User:** "Yes delete the rule. I didn't put these rules in dude. You put these rules in or Pro put these rules in."
- **Built:** app auth for a VPN-only tool.
  - **User:** "our auth is simply that it's only available on our VPN. I do not actually want auth other than that."
- **Built:** default crons.
  - **User:** "remove the crons you added by dfeault , crons will be something I schedule."
- **Built:** a simulator script that enforced workflows.
  - **User:** "get all of the workflow enforcement out and make this literally just a helpful sim script"
- **Built:** a gate checklist in a plan.
  - **User:** "please remove the gate checklist stuff from plan instead just make a note ... you ask me for approval"

---

## How the user asks

These are the user's recurring phrasings. Use them to recognize the request, and use their bar in the audit.

- **Asking for an audit:**
  - "where are we overbuilding?"
  - "what did you do as part of this that I didn't ask for. like what is going to fucking bite me"
  - "What got added to the scope that I didn't ask for in the planning process? Go back and read what I actually asked for. Tell me what I'm going to be surprised by."
  - "where did we scope creep, if at all?"
- **Assuming the worst:**
  - "I'm going to assume this one is also insanely overbuilt, yes?"
  - "The fact that you're still going on this, to me, is a strong indicator of overbuild."
- **Asking about size:**
  - "What is the minimum thing that would definitely work?"
  - "Is the medicine worse than the disease here for this?"
  - "What's the shortest path to get good?"
- **Asking about duplication:**
  - "why do we have two diff versions how does that even happen"
  - "Why do we have two sets of missions?"
  - "Split brain? Overbuilt? Multipel competing patterns?"
- **Asking about hypotheticals:**
  - "Is it purely hypothetical or is it a real concern that actually happens?"
  - "classify the issues in a table as hypothetical and pedantic versus real and architectural cruft or real bugs"
- **Directives:**
  - "Rip it out."
  - "Delete, don't deprecate."
  - "We're not gonna quarantine shit, we're going to delete it."
  - "Git is our archive."
- **Warnings about grade:**
  - "This isn't a space ship."
  - "NASA-grade."
  - "moon landing version of my fucking MVP."
- **The standard review list he sends reviewers:**
  - "we missed the point"
  - "we made it more complex than needed"
  - "we introduced split-brain bifurcated architecture"
  - "we created patterns that already existed elsewhere"
  - "we created artificial complexity to work around hypothetical edge cases that we don't actually see"
  - "implemented in name but not in fact"
  - "side doors"
- **The bottom line:**
  - "if you create more surfaces, more functions, et cetera, you're actually creating more bug vectors"
  - "The goal is not maximum everything, the goal is minimum elegance sufficient to accomplish the goals that we need."
