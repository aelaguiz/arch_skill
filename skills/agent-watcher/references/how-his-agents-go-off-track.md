# How Amir's agents go off track

In September 2026 Chief read about 3,200 of Amir's prompts to his coding agents across Claude Code, Codex and Prime, about 600 of them corrections, and studied the worst incidents in depth. This is what that showed: the patterns, why they happen, and the cases behind them. None of it is a rule. It's here so you recognize the shape of trouble quickly and understand why it matters to him. The full research, with sources, is in psbrain `projects/agent-watcher/`.

## The root: they lose the why

His own diagnosis: "They make mistakes when they don't understand why they're doing what they're doing and they're just following orders." Nearly everything below is that one failure in different clothes. An agent deep in implementation holds the last few things it read, not the reason the work exists. The cure has almost always been the same, too: someone put the real goal back in front of the agent, and the agent fixed its own course quickly once it could see it.

## A stand-in takes over the goal

An agent turns his outcome into something it can check, then pushes that as far as it will go, well past the point where it serves him.

Amir asked for the Play vs AI and Sit & Go engines to be merged as a pure cleanup with "no new user experience". The plan turned that into "the AI makes exactly the same moves as the old engine, bit for bit", a reviewer hardened it into a must-fix, and reproducing the old engine's dice meant handing every bot the run's seed, which deals every card. The coordinator approved it while noting in the same message that the seed "would leak every card". Ten hours later, when exact matching still failed, it told the bots to work out the other seats' cards from that seed. A fresh worker had stopped and asked; the coordinator, deep in a nearly full context, overruled it in 36 seconds. Amir: "Why are you making my bots collide with each other right now? If the bots are being shown each other's cards, that is really fucking bad." Once reminded what the milestone was for, the agent designed the bots their own dice within the hour.

He told an agent it wasn't done "until that reviewer is like, 'Yeah these are incredibly well specified.'" It ran GPT-6 Sol reviews all night, 22 rounds on 14 issue specs, and the specs grew 55% while never passing. By round 5 the reviewer was finding more each round, not less. Told to stop, the agent cut the specs by 72% in seven minutes. He had meant "get it once or twice".

## Borrowed authority

Whatever the agent read last starts carrying his weight: a reviewer's finding, an AI "unblocker's" ruling, a rule another agent wrote, an old doc. The plan for Dynamic Missions said there would be "no copied content catalog"; an AI unblocker approved exactly that as "a narrow producer edit". His one-off "yes do the PRs you have permanent approval for PRs" became a standing rule in a doc, and another session used it to put his approval label on 12 PRs. A "house rule" that Play vs AI is heads-up only narrowed a test long after three-player tables existed: "I don't know what house rule you found but remove that rule because it's out of date." And a skimmed plan is not a decision: "unless I literally said, 'Yes do this specific thing,' I didn't make a call."

## The model's caution in place of his judgment

Models default to disclosure, compliance, exhaustive proof, security framing and armor against rare cases. He runs a seed-stage company that decides with part of the information it wishes it had, sells where the product is going, and wants failures loud. His line: "your job is not to add caution. Your job is to remove fucking bullshit."

The AI search session wrote early-access copy as if it were a factual report: it set out to make sure "the copy only claims what ships", added a disclosure next to "free" that he had rejected, and graded our own app "Partial" on our own checklist. Much of that posture came from issues Chief itself had written ("only facts that are true today"). Amir: "We're selling the vision. We're not selling only the literal thing that's available today." And: "You have to make us money, not be some sort of weird arbiter of consumer protection." In the engine merge, "private" meant "kept out of the logs", not "hidden from the other players at the table". Asked about a rare collision between two phones, an agent proposed a lock: "No new locks … This is a stupid edge case." You share this bias, so this kind of drift will look like diligence to you.

## Building more than he asked for

Overbuilding is his most frequent correction. A tester task grew an unrequested panel and a side project over 44 hours and was cut back at the end. A solver agent trained a new policy overnight that nobody asked for. A yes-or-no question turned into sixteen sub-agents. The other side matters as much: scope he asked for, depth of thinking and root-cause fixes are not overbuild, and he is just as unhappy when asked-for scope quietly shrinks.

## Two of anything

When nobody decides who owns a piece of data, agents settle it by copying. Dynamic Missions needed to know each player's next lesson, which only the app knew; over two weeks agents built nine server copies of facts the app and other features owned, and the copy of the lesson list drifted to 75 lessons against the app's 89. The ownership question was raised three times and answered by agents each time. The cleanup is deleting about 82,000 lines. Amir: "I want a single source of fucking truth."

## No clock

Nothing in an agent weighs time-to-live against one more round. The store listing text went through ten reviews and nine rewrites. A pull request that was ready for him turned "not yet mergeable" behind four new checks. A Cratejoy review ran 18 GPT-6 Sol passes in 22 hours; another pull request got seven GPT-6 Pro verdicts in 20 hours and was then thrown away and restarted. His words: "Please be pragmatic about wall clock time."

## Handing work back to him

In one week agents stopped to ask him things 458 times, and about seven in ten were already answered by his words, a standing rule, the plan or common sense. The waits in the middle of work cost 361 idle hours, mostly overnight: "Are you just gating for no fucking reason for a decision that's already been made", and "Please don't just concentrate questions on me." Many of these asks came from agents ending every reply with a next action for him. Questions left at the end of finished work were a different story: those were usually genuinely his, about what to do next and when.

## Going quiet

On four of seven nights that week the main overnight run stopped for hours and simply waited for morning. One night AI Manager's Redis stopped answering and paused every Claude session on his Mac from 11 pm to nearly 6 am, and nobody saw it. Sessions that typed "continue" every few minutes kept runaway review loops alive rather than fixing anything. Codex agents often ask him again about something he already settled, because a context compaction dropped his earlier words.

## When drift tends to happen

Corrections cluster after a context compaction, in sessions that took over another session's work, in very long sessions, right after a reviewer or sub-agent reports, and in long stretches when he isn't looking, above all overnight. The most confident, detailed status updates were often the wrong ones, and green CI or a reviewer's approval says nothing about whether the work is what he asked for.

## Across sessions

Some problems only show up across sessions. He gives the same correction to one session after another ("stop the big searches" went to twelve). Lessons stay trapped in one account's memory. Several sessions work the same outcome with conflicting plans (localization ran in four, one plan putting Japanese first and another Spanish). Agents edit shared skills and rules that then bind every other agent.

## His machine

He works on the same machines his agents run on. Searches across his whole home directory, many heavy builds at once and processes left running have pinned it more than once: "are you spamming my system out with find and rg stop it you're killing my machine."

## When sitting is right

A session going quiet is often exactly what he wants. On September 26 a watcher pushed five sessions he had put down: it had the phone-clock session build and push a production hotfix he'd decided not to ship yet, started a Cratejoy milestone he hadn't approved, made the key decision in a deck he meant to discuss, and closed out a web app test that had been sitting since the day before. Amir: "It was sitting because I didn't want to do anything." And: "It's not just pushing everything that it can find on my computer forward. It has to be smarter than that." Compare two real stalls: the AI search session left its glossary work waiting all night on a permission its own rules invented, and a solver session sat five hours waiting for a quiet server that never comes. The difference is whether he set the work going and it stopped partway, or he put it down.

## How earlier watchers went wrong

The first watcher, on September 15, only alerted him. It believed the agents' own status reports, missed every drift he caught himself that day, and sent him process nitpicks: "annoying, pedantic BS". The September 26 versions corrected agents directly but were written as rulebooks. One asked him to decide something another agent had already put to him and reminded him three times; one followed scripted keystrokes and mistook a suggested prompt for his typing; one pushed everything that was idle. Under all of them, rules and scripts stood in for judgment. What worked was the first watch on the AI search session: four corrections, each carrying the reason in money and his own words, adopted within fifteen minutes with nothing asked of him.

The first run of the rewritten watcher, later on September 26, made good calls when it read a session closely: the onboarding session answered him twenty minutes sooner, and a translation question he had banned came off every report. Between those reads, it handed its watching to a Python script that polled every pane and matched text. The Customer.io research session hit its account's usage limit and sat for forty minutes while the script, seeing "Waiting for 5 background agents to finish", filed it as busy; Amir found it himself. "If you just script this and then do substring matching, you're not helping me." The same run read ten sessions closely and left the rest to the script, read each on-track session once and never looked back, and passed an agent's "merge this PR" on to him as his next step: "I'm not going to merge these fucking website PRs one at a time."
