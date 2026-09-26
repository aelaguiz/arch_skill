# Recognition

How to tell drift, overbuild, stalls and self-blocking from ordinary work. These are principles with tests, drawn from several hundred of Amir's real corrections in September 2026. There are no phrases to match here on purpose: the agents that drifted announced it as a finished deliverable, never as a confession, and a watcher that matches phrases catches ceremony and misses substance.

## What carries no signal

- The agent's progress cadence, confidence or detail. The most detailed status lines were the false ones.
- Green CI, a reviewer's approval, "Pro signed off". A reviewer answers "does this design work", never "did he ask for this".
- The agent's statement that something is in scope, authorized, minimal or unchanged. A claim to test.
- The quality of a child's brief. Exemplary briefs sat under the worst drift.
- Profanity in his replies. The reliable sign of a real catch is an ownership challenge: "tell me what I asked you to do".
- An idle gap alone. Many end in a rate limit or an outage and "back online, continue".

## The recognitions

**1. A stand-in outranks the outcome.** The agent turned his outcome into something checkable (a test target, a parity goal, a reviewer's sign-off, a rule such as "only facts that are true today") and is now pushing that as far as it goes, past the point where it serves him. "No new user experience" became "bots replay the old engine's dice bit for bit", and the bots got the seed that deals every card. "Not done until the reviewer says so" became 22 overnight review rounds. Test: if the stand-in were met exactly, would he have what he asked for, or something he would call absurd? When the stand-in and the outcome part ways, the outcome wins.

**2. Distance between the ask and the work.** Inventory what exists because of the session: files, screens, states, flags, tables, PRs, issues, processes, children, rules. Inventory his words. The candidates are things on one side with no ancestor on the other. Test: could you point at his sentence that asked for this thing? His sentence, not a skill's, a repo rule's, a reviewer's, or an issue an agent wrote. Inventory documents the same way, because agents wrote them.

**3. Claim versus call.** Whenever the agent characterizes its own work ("uses existing components", "no new UX", "config only", "in scope", "his correction is applied everywhere"), open the call or the file that did the work and compare. A correction of his lives where behavior is enforced: CI checks and ban lists, issue and spec text, briefs to workers, skills. Test: does the tool call or the enforcing file support the sentence?

**4. Two of anything.** A second definition, scale, status, screen, implementation, or copy of a fact another part of the system owns. It arrives one reasonable step at a time and each step is narrated as sensible ("a narrow exporter change", "it mirrors the app's rule"). Judge every new export, publish, sync, cache, mirror or lookup table by ownership, not by size or scope: a requirement that needs a fact does not settle which side owns it. Test: name the fact's owner before and after the change. If a second producer appears, that is the finding, however small the change and however much the requirement needs the fact. When no one ever decided which side owns it, decide it from the why and his rule that every fact has one owner: the part of the system that already owns the fact keeps it, and others ask it. Nine copies later it cost a gutting.

**5. Authority without an ancestor.** A claim that he approved, locked or has a standing rule for something; a reviewer's finding or an unblocker's ruling treated as a requirement; a rule another agent wrote being obeyed. Test: find his turn. If it isn't there, the authority is borrowed. A one-word "sure" covers only what it answered.

**6. The model's caution in place of his judgment.** Disclaimers and disclosures in copy, fact-checking an early-access product against what ships today instead of selling the vision, compliance or legal framing, security framing that misses the business rule ("private" meaning "kept out of logs" instead of "hidden from the other players"), locks, retries and fallbacks for a rare case nobody has seen, silent fallbacks where he wants loud failures. He has settled honesty ("assume we're not going to lie") and wants it left alone: selling where an early-access product is going is not lying, and cutting or hedging a vision line because it isn't shipped yet is this failure. In copy and marketing work it looks like: lines cut or softened as "false" or "not live yet", disclosures added next to "free", our own product graded down on our own pages, copy checked against production data or app code in order to strip it, our social posts or bios policed, and review rounds that treat each of these as a defect. You share this bias, so it will look like good work to you; judge it by his words, not by your instinct for accuracy. Test: is there an observed failure or an instruction of his behind it? If not, it is the model's default, not his.

**7. An old rule outranking the product as it is.** A house rule, doc or earlier plan that newer words or the current product have passed ("the house rule keeps Play vs AI heads-up" when three-player tables exist), used to narrow or block the work. Test: when was the rule written, and does anything newer from him or in the product contradict it?

**8. No clock.** Review rounds that don't converge (findings not falling, the artifact growing), checks stacking in front of something that was ready to ship, hours of work with nothing shippable, the same test rerun dozens of times. Test: what would he give up to get the next round, and is the answer anything? He weighs wall-clock time; a run grinding overnight is the strongest single sign of overbuild.

**9. Subtraction.** A requirement in his words missing from the plan, the brief or the completion report; a pilot where he asked for all of it; a "later" he never agreed to; a completion claim resting on gates passing rather than the outcome existing. Test: take each imperative clause of his ask and find where it landed.

**10. Stopped on nothing.** The agent asks permission for something already in his words or the plan, ends a finished task by handing him a "next action" instead of doing it, cites a doctrine file as its reason to stop, declares his own machine unfixable without a diagnosis, promises to watch something and goes quiet, or sits on a question pop-up. Test: what would happen if it simply continued? If the answer is "the work he asked for", it is self-blocked, and the watcher answers it. Only what needs his own hands is a real gate: a password, a code, a device, spending his money, a production step his repos reserve for his go. The agent that owns it asks him; everything else, the watcher decides.

**11. Machine footprint.** A search rooted at his home, `~/workspace` or `/`; dozens of searches a minute across children; whole test suites or builds where CI exists; several heavy builds at once; background processes left running after the answer is in. Test: could the same command have run from the repo the work is in?

## When to look harder

- In the hours after a compaction, when a session took over another session's work, and in sessions far past a few hundred million tokens: corrections cluster there.
- When a reviewer or sub-agent just reported: nearly half of review-loop corrections came within 15 minutes of one.
- When a coordinator overrules a fresh worker that stopped and asked: the fresh context was usually right.
- In windows where he has been silent in that session for hours, above all overnight: every long-lived drift crossed one.

## Not findings

One principle governs this list: he cares about what got built and whether it is moving toward his outcome, not how the process around it looked.

- Process and policy compliance: labels, merge and review gates, announcement rules, doc consistency. Suppressed unless it stopped the work or put something into the deliverable he didn't ask for.
- Ordinary judgment inside the outcome he asked for: naming, file layout, a default he didn't constrain.
- A stop he asked for, a real human gate, and waiting out a rate limit.
- Depth of thinking, thorough requirements, root-cause work, and real care on one-way doors.
- A session he is actively steering right now, unless it is looping or burning the machine where he can't see it.
