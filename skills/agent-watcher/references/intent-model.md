# Intent Model

The intent model is the watcher's whole advantage over the agents it watches. An agent deep in implementation holds the last few things it read; the model holds what Amir wants and why, built only from his side and kept current. Every judgment the watcher makes is the work compared against this model, so a wrong model makes every later call wrong. Build it before you form any view of the work.

## The four layers, in order of authority

1. **His words, across the session's whole history.** You will rarely arrive at the start of a session, and you do not need to: every transcript keeps its lines from the first message on, including the parts the agent compacted, and restarts, forks and account switches leave a chain back to the first session ([runtime-notes.md](runtime-notes.md) has the markers). Follow the chain to its start and read every message he wrote in each transcript, oldest first: his typed messages and the ones he queued while the agent was busy, leaving out scheduled prompts, relays and summaries ([runtime-notes.md](runtime-notes.md) shows which records are his). His words are small, about 3,000 tokens in a 78 MB transcript, so read all of them. What he pasted inside a message is his: he pastes his own dictation and documents. When he tells a session to "ramp up on" or "read" another session, that session's words are part of this chain.
2. **His decision records for the work.** The documents his words point to or that he approved: the spec sheet's North Star, Intent and Decisions tabs, issues he filed or approved, workbook tabs written for him or by him, and repo rules traceable to his words. A decision row an agent wrote counts only where his words ratify that specific row.
3. **The business why, from psbrain.** His values (`shared/amir-values.md`), his corrections to Chief (`shared/feedback.md`), strategy under `shared/strategy/`, the project's home under `projects/`, intake entries on the topic, and what he said about the same work in other sessions. This layer supplies intent he never typed into this session: that our bots teach players and never cheat them, that early-access copy sells the vision, that every fact has one owner, that a two- or three-person seed company decides at 50 to 70% of the information it wants.
4. **The lessons ledger** (`operations/watcher/ledger.md` in psbrain): the principles his corrections have taught across every session.

Read his voice-to-text for the meaning he intended, not the literal word. When he makes a point with emphasis, find the point he means rather than testing the superlative.

## What never counts as his intent

- The agent's plans, summaries, recorded "decisions", and its restatement of his words.
- Reviewer findings (GPT-6 Pro, Sol, Astra, another Claude), and rulings by an AI "unblocker".
- Rules other agents wrote into `AGENTS.md`, docs, skills, memories or specs, unless you can find the turn where he asked for them.
- Old docs and house rules that his newer words or the product as it is now contradict.
- A one-word "sure" or "ok" to a long proposal, beyond the specific thing it answered. In his words: "unless I literally said, 'Yes do this specific thing,' I didn't make a call."

These are claims. Check them against the model; never add them to it.

## The model file

`operations/watcher/models/<slug>.md` in psbrain, one per piece of work (not per session, since one piece of work outlives several sessions). About one page. Every line cites its source (a quote with the date and session, or a document); anything inferred says what it was inferred from.

- **Work:** its plain name, the Herdr space, the chain of sessions (runtime, id, host, transcript) with the time each transcript was read to, and when the model was last updated.
- **Outcome:** what he wants, in a short paragraph built from his quotes.
- **Why it matters:** the business reason: money, survival, the promise to players.
- **The clock:** the deadline or rhythm he set ("a PR to review in the morning", "before the October 4 read").
- **Decided:** his decisions, quoted and dated; superseded ones marked with what replaced them.
- **Must hold:** the business rules the work may not break, at the scope he set. Never widen a principle of his into a stricter rule: "we're not going to lie" settles honesty and leaves it alone; it is not "claim only what ships today". Rules that Chief or an agent wrote are marked as theirs.
- **Doesn't matter:** what he said is out of scope, not important, or not his concern.
- **Corrected:** each correction he gave, quoted and dated. These lines teach the most.
- **Open:** questions the layers don't settle that would change what gets built or shipped, each with your recommendation.

The test of a good model: someone who never saw the session could read it and predict what Amir would say about the work as it stands now.

## Keeping it current

- Every check starts with his new words since the last check, in this session and anywhere else he talked about the same work, including his messages to you. Newer words win; a correction rewrites the lines it corrects, with its date.
- When the session restarts, forks or moves accounts, extend the chain and keep the model.
- Never revise the model from what the agent is doing. If the work suggests the model is wrong, look for his words. If there are none, it is an open question.

## When the model doesn't settle it

If the question would change what gets built or shipped, look for his words in the other layers first. If they don't settle it, it goes to him as one question with the options, what each changes, and your recommendation; his answer goes into the model, and into the ledger when it is a principle. If the question wouldn't change the outcome, the agent's own judgment stands.
