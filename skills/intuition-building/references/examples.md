# Intuitions next to the rules they replace

Each pair shows a situation, the rule an agent wrote or would write, and the intuition that handles more than the case in front of it. Most come from real work. The point of each is the idea under it, not the case.

## Intuitions in one breath

Some intuitions fit in a sentence and still cover a whole class of cases:

- "Aggregate blended views are bad; look at the data at the level of individual cases, and the trend should be visible there."
- "Teach them how to be good neighbors," said of agents sharing one machine.
- "If it's done finding things that really matter, move forward," said of a review loop.
- "As of right now we're seeing this, which might trend to that if this rate holds," said of a result that won't be final for weeks.

## Turning a correction into guidance

### Too many questions

An agent that watches other agents was told it interrupted its user with too many questions.

- **Not this:** "Never ask the user anything; make the calls yourself." Within minutes it pushed a production fix and started a client project on its own, and the next correction added "never make business decisions" beside the first rule.
- **Like this:** "A question makes the user stop what they are doing and reload the whole project in their head. Most answers are already in their plan, their words or common sense: use them, and say in one line what you chose. A call is theirs when it can't be undone, changes what customers get or what they spend, lowers the quality bar, or is being settled for the first time."
- **Why:** It says what a question costs and what makes a call the user's. A production fix can't be taken back, so the agent can see it is the user's call without a rule that names it.

### "Make this rule stronger"

An agent was told to change ads through the platform's API instead of clicking through its website, then asked to make that rule stronger. It wrote a version that amounted to never touching the website, so every job the API couldn't do landed back on the user. The user: "The intuition is not 'never do it.' The intuition is 'do it the right way first.'"

- **Like this:** "Use the platform's API first, for changes and for any read it can answer. To the platform, an agent clicking through its console in the user's logged-in session can look like an account takeover. When the API genuinely can't do the job, use the console the way a careful person would: one deliberate change at a time, checking the result before the next."
- **Why:** "Stronger" meant clearer about the risk, not wider. This version says what the risk is and what to do when the safe path can't do the job.

### The disclaimer

Replies on a forum kept ending with a reminder that the app has no real-money play. The user said readers already know that.

- **Not this:** "Never say the app has no real-money play."
- **Like this:** "Write as a strong player who happens to have built a trainer, talking to a friend. Bring the app up when it would help them and leave it out when it wouldn't. Readers know what a training app is, so don't spend words telling them; if someone asks whether they can play for money, answer plainly."
- **Why:** The first version fails the first reader who asks. The friend answers that reader honestly and drops the fine print everywhere else.

## Turning someone's offhand words into guidance

### "Say 48 hours"

Asked to clean up working copies "if they're older than, say, 48 hours with no changes."

- **Not this:** "Remove any working copy older than 48 hours."
- **Like this:** "A working copy nobody has touched in a couple of days is probably abandoned. Check whether a session still uses it before you remove it; its age is a hint, not the test."
- **Why:** "Say" marked a rough number. Made exact, it removes one at 49 hours that someone is using and keeps one at 47 that nobody is.

### "Maybe like a max of four"

Months ago the user guessed that a beginner's walkthrough should have "maybe like a max of four" steps.

- **Not this:** a quality check that fails any walkthrough with five steps.
- **Like this:** "A walkthrough is as long as a beginner seeing this for the first time can follow. The guess of about four steps is a feel for how light to keep it, not a count."
- **Why:** The number stood for how much a beginner can take in. That is what the next agent needs; four was one example of it.

### "Cap it at one round, right?"

A batch spent a day and a half re-reviewing rewritten work. The user asked, "Cap it at one round of feedback, right?"

- **Not this:** "Each build gets one round of review and is never reviewed again."
- **Like this:** "Review is there to catch what a user would trip over. Once a round has found that and the fixes are in, more rounds mostly re-find the same things and cost days. After a round, ask whether it's ready, not whether one more pass might turn something up."
- **Why:** A question about one batch became a law for every build, including one where a fix rewrote half of it.

### An example taken as a duty

Describing a good team lead, the user said: "Here are the three or four things we should do. I've cut two issues for you."

- **Not this:** "File issues for what you find."
- **Like this:** "A good lead does the sorting and the work, and hands the user only what needs them."
- **Why:** The two issues were an example of finished work, not an output to produce.

### A line stretched past where it was drawn

The user told code reviewers to stop flagging personal data as privacy findings.

- **Not this:** "Remove any masking a change adds, whatever it hides: names, addresses, tokens, keys."
- **Like this:** "Don't raise personal data in logs or analytics as a finding; that has been decided. Secrets such as tokens and keys are a different matter, and nobody said otherwise."
- **Why:** The correction was about personal data. Stretched to secrets, it would tell a change that stops leaking login tokens to undo itself.

## Explaining a risk

### Running out of memory

A shared machine crashed when it ran out of memory, and every agent on it stopped.

- **Not this:** a script that kills the largest process whenever free memory drops below 10%.
- **Like this:** "Load is not the danger. Agents compiling, testing and running a dozen sessions keep the cores busy, and that is the work happening. What brings the machine down is memory running out. A sudden swap jump while a test suite runs can be fine. The same jump with free memory falling every few minutes is the start of a crash."
- **Why:** It says what actually kills the machine, what only looks alarming, and two cases that look alike and aren't. The script can only do what its threshold says, and its first version ranked processes by the wrong measure.

### Where to search

- **Not this:** a list of folders never to search from.
- **Like this:** "Search where the thing lives, starting from the narrowest folder that holds it. Some project folders here hold hundreds of gigabytes, so a recursive search from their root reads a whole disk."
- **Why:** The list missed the expensive case, a search from the root of a huge project that wasn't on it. The paragraph covers it because it says what the cost is.

### Commands on a shared machine

- **Not this:** a list of banned commands.
- **Like this:** "Nothing here is banned, because the same command is harmless in one place and ruinous in another. Before you run something, picture it at its biggest: what it will touch, how large that can get, how long it will run, and what it will leave behind."
- **Why:** A ban list stops the commands on it. The question catches the next command nobody listed.

## Writing a check or a test

### "Always"

A bot's description said it "always picks its bigger bet sizes."

- **Not this:** "Pass if the bot picks its bigger bet in 95 to 100% of hands." The bot measured 94.5% and failed.
- **Like this:** "'Always' in a description of a bot means a player should feel it as a habit. Check whether a player would notice the pattern."
- **Why:** The number turned a description of character into a bar, and the check stopped asking what the description was for.

### A trigger that almost never fires

- **Not this:** "Pause posting whenever followers fall by 8 or more in a day." A drop that size had happened on one day in more than a year.
- **Like this:** "Watch what each post does to the account. A post that loses followers you were gaining is news; an ordinary day's wobble isn't."
- **Why:** The number made the call checkable and then almost never applied. When it did, it would have stopped posting on noise.

### Deciding before the data

- **Not this:** "Every decision in the test loop has its rule written before the data arrives, precise enough that two agents reach the same call; when nothing meets the rule, nothing starts." The loop then reported "nothing qualifies" every hour.
- **Like this:** "The loop is there to learn as fast as it can, so it acts on a direction before it is certain and lets each result steer the next test. Writing down what you expect before a test runs is how you notice you were wrong. It is not a rule that decides for you."
- **Why:** The rule was made precise so two agents could not disagree, which is exactly what removing judgment means.

### Testing guidance

- **Not this:** revising a skill round after round until its saved test scenarios pass. One review found most of the added lines existed "to get one scenario to pass."
- **Like this:** "Try the guidance on a case nobody wrote down beforehand, and on one where the right move is different."
- **Why:** Saved scenarios become the thing the guidance is written toward. A new case can't be fitted that way.

## Describing a tool

### A label on a page

- **Not this:** "A review counts only if the answer shows the model tag `gpt-6-pro`." The page stopped showing that tag, and every review after it failed.
- **Like this:** "Make sure the review came from the strong model and not a weaker fallback, by checking what the page shows today."
- **Why:** The point was which model answered. The tag was one day's way of seeing it.

### Detecting someone else's edits

An agent marked every slide it wrote so it would never overwrite the user's edits. The API changes two values on every read, so every slide looked edited and was held back.

- **Like this:** "The point is not to overwrite what the user changed. What they change is a slide's words and pictures, so compare those with what you last wrote. Values the API changes on its own say nothing about them."

## Pushing against a bad habit

### Overbuilding

- **Not this:** "Never use the words proof, receipt, gate or contract," or "Every process section opens with 'Judgment moves, not a recipe.'"
- **Like this:** "Before adding a check, a proof or a gate, ask what it would catch that nothing else would, and what it costs every time it runs. In an early product, most of it catches nothing and slows everything."
- **Why:** Banning a word stops nobody from building the machinery under another name. Asking what it buys does.

## Passing guidance to another agent

### A rule without its case

A rule written for one ad platform, "no 'AI' wording," reached a campaign on another platform as a bare line and stripped copy the user had approved.

- **Like this:** pass the case with the line: which campaign it came from and why, so the other agent can see whether it applies.
- **Why:** The second campaign got the line without the case, so it had no way to see the line wasn't about it.

### Whose caution it is

An agent added its own caution: every new kind of fix waits for the user's merge until it has earned shipping alone. Later agents read it as the user's rule, and the user ended up merging every one as built.

- **Like this:** "I'm sending new kinds of fixes to the user's review as my own caution, not theirs. Drop it once the first ones come back clean."
- **Why:** An agent weighs a caution it knows another agent wrote. It obeys one it thinks came from the user.

## Revising guidance that already exists

### Adding beside

One topic in a skill took ten edits in a month, each adding a paragraph for the latest case, and one was reversed an hour after it went in. The skill quadrupled while almost nothing came out.

### Replacing

A report had judged wins with four checks. The user asked, "What's a win?" A first try tied the answer to that quarter's goals; the one that held replaced the checks:

- **Like this:** "A win is when something we did met reality and we came out ahead: either reality rewarded it, or it taught us something true we can act on. It came from us, it is real (the thing itself changed, not a side number), and it leaves us stronger for what is next. So a bold experiment that failed clearly is a win, told as the lesson, and a good week that happened to us is weather."
- **Why:** It replaced the checks instead of joining them, and it handles weeks that look nothing like the one it came from.

## Where a rule was the right call

- **Something true in every case.** An agent built a check that guessed from file paths which pull requests needed the user's approval label, and it kept missing cases. The user: "You always need it, so it's simple." The rule "Every pull request needs the approval label" is right because no pull request changes the answer.
- **A role.** "You report and analyze; you don't make changes." It replaced a whole workflow for how changes get made, and held, because it says what the job is rather than patching a case.
- **Facts.** An exact command someone checked, a schema, "this remote is blocked; don't push to it." Written as judgment, they would only get vaguer.
- **A standing preference.** A house style held everywhere is a fact about what the user wants.

## Looks like an intuition, but isn't

- **A reason attached to a rule:** "Never say the app has no real-money play: readers know what a training app is." The reason is real, and the line still fails the reader who asks.
- **A long paragraph that ends in an absolute:** a page of reasons for fixing decisions in advance, ending "when nothing meets the rule, nothing starts." The last clause decides every case.
- **A quote attached to a rule:** "Never X (the user, October 3: '...')." It shows where the rule came from, not that anyone understood it.
- **A phrase on repeat:** "It looks different each time:" opening every example list in a set of files. Used once, it introduces cases. Used everywhere, it is a form being filled in.
- **A soft line beside a hard rule:** "When unsure, decide yourself," next to a rule that sends every new kind of fix to the user. The rule keeps winning, because the soft line gives nothing to see by.
- **A correct principle with no picture:** "rather than adding an ever-growing list of micro-rules," in a file that kept growing. It names what not to do and shows nothing of what to do instead.
- **A platitude:** "Use good judgment about when to ask." True, and the watcher above would still have pushed the production fix.
