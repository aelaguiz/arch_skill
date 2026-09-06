# Amir's writing rules and voice corpus

Evidence file for a later "readable reports" skill. Built 2026-09-06 from Amir's workspace at `/Users/aelaguiz/workspace/psagentspace`, his global agent instructions, and the `prime-adhd` package. Every Amir quote is verbatim with a source path or session and a date. Anything that is my reading of the evidence is labeled **inference**.

The trigger: the report at `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/20260906-morning-priorities.txt` (source markdown `/Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06.md`) contains the line "Checkout root now clean, children blocked." Amir, 2026-09-06 (session prompt, relayed by the parent task):

> "I'm looking at this and it says, 'checkout route now, clean, children blocked.' I don't know what the fuck that means. I could parse it if I had to. I could be like, 'Okay we're talking about something about the checkout.' I don't know what we're talking about, but I know there are checkout issues. What's the root? Does it mean the root PR, like children issues, right? It's just fucking confusing, dude, and it's sort of the standard of the writing I get back from these agents. I need it to not create so much cognitive burden to try to parse these things. I need it to be simple and easy to understand, and when I try to do this half the time I get something that goes into this: 'Oh he's an idiot.' I'll say, 'Computers are like brains.' It either treats me like a child or it writes it in a way that requires full concentration to even figure out what the fuck they're saying, right?"

His target bar, same session: "a really smart engineering-focused executive could read this at a glance and understand it without having to drop everything and fully focus on every single fucking word."

## Findings (what a skill author should act on)

1. **The readability bar already exists in writing, but only for other readers.** Two documents state a measured bar: the Monday investor email (`/Users/aelaguiz/workspace/psagentspace/skills/weekly-ops-report/SKILL.md`, "box density law": one point per bullet, median about 100 characters, hard ceiling about 250, "no house vocabulary a first-time reader cannot parse") and player coaching copy (`/Users/aelaguiz/workspace/psagentspace/docs/COACHING_STYLE_GUIDE.md`: fifth-grade readability, "One idea per message, point first, short", a headline must be "Meaningful standing alone, never a cryptic label"). No document applies a measured bar to reports written for Amir himself; the closest are chat-reply rules (the prime-adhd contract and the "Writing And Replies" section of `/Users/aelaguiz/workspace/arch_skill/AGENTS.md`). The skill should port those bars to Amir-facing reports.

2. **His hard rules are mostly naming rules, and the sample line breaks two of them.** Plain English, never bare codes (name the thing on every mention; the code goes in parentheses after the name); every PR or issue is a labeled hyperlink; absolute paths always; never the word "receipt"; no invented personas. "Checkout root now clean, children blocked." names nothing: no PR numbers, no link, and "clean" and "blocked" are GitHub's raw merge-state values leaked into prose (see Gaps).

3. **He rejects two opposite failures with the same force: padding and over-compression.** Padding: "don't write a fucking book", "make 1 less flowery and overly verbose". Over-compression: "I can't even understand what the fuck you're saying. It's so confusing", on a 54-word post that passed every gate. Short is not the goal; one-pass parse is. The community ledger's repair rule fits reports too: "when a draft only fits the band by fusing sentences, the fix is cutting a claim, never fusing."

4. **Verdict first, then mechanism, then evidence.** This shape shows up in his own writing (Telegram 2026-07-18: "theres 3 issues:" then a numbered list, then "the answer for 3 is..."), in the contract he installed for his own agents (rule 1: "Lead with the answer or next action"), in the investor email ("If you read nothing else:" on its own line), and in the coaching guide ("point first"). A status cell should open with the state and the next action, not with history.

5. **A term the reader has not met never leads a sentence.** The "M concept" verdicts (2026-08-15): the draft opened with a named concept and defined it afterward; Amir: "what the FUCK is the M cooncpet thats what is so confusing". The approved repair said the idea in plain words and dropped the term. For Amir the exact technical term should still be available afterward: when an agent explained a build in plain words he asked back "are you saying its a reverse incompatible build?" (Slack, 2026-08-05). That matches the standing pattern "the paywall copy test (C35)", never "C35".

6. **Every claim carries its provenance, but evidence follows the point, never leads it.** He reads every sentence as a claim: "Where the fuck did this come from, dude? This all just seems like gibberish." (2026-08-15). Rules require source links, dates, and his own words for anything in his voice. And yet: "I don't care about receipts. I care about good headlines and good copy." (2026-08-23, as quoted in the coaching guide; the raw ledger version has one more word) and the ledger rule "receipts follow the OP and draft, never lead them". Link the source at the end of the sentence; do not open with it.

7. **Structure rules he has ruled on: one point per bullet, labeled short blocks, bullets whenever a passage carries more than one point, tables newest first, one row per item in sheets.** Template labels are fine in a report and wrong in a personal post ("Workaround:" / "Affects:" labels read as an incident report, 2026-08-10). Mechanical length checks are accepted for measurable things (the box density check "runs as code"), but a harness for taste is not: "Don't build some fucking harness... Just update the skill."

8. **Voice he approves: first person where a person acts, active voice with the actor in the sentence, verbs not noun stacks, no hedging on clear calls.** He kills agentless passives ("It's sort of passive voice, right?"), nominalizations ("you tend to make the thing they are doing an object 'the study' thats not how people talk"), signage ("They should be me, the founder, not fucking signage"), and program furniture for people ("We call them people, not seats"). In a report for him the analog is: say who is blocked, on what, and who acts next.

9. **AI tells are a closed, measured list with one canonical home.** Banned outright: em dashes, the 27-word Pew vocabulary list, negative parallelism ("it's not just X, it's Y"), the default Oxford comma, stacked hyphenated compounds in personal-voice channels. Structural tells (polished emptiness, triads, reveal bridges, recap loops, interface residue, uniform cadence) are judgment calls documented with repairs. The skill should point at `/Users/aelaguiz/workspace/psagentspace/skills/fc-authored-copy/references/editorial-judgment.md` and not copy it; Amir's rule is "one boss file per surface".

10. **Do not nag, re-surface, or report on the report.** Merged means done (rule text: Never re-raise "it hasn't shipped / it's in no release cut yet" as a status update); unanswered drafts expire ("please don't remind me about it forever"); do not quote his corrections back at him on the page; "No third-person self-reference ('agents build this page') and no report-about-itself exposition anywhere." Anything put in front of him must be decidable from that one message alone: full quote, reception tag before the quote, evidence links after the point rather than before it.

## Amir's explicit writing rules

Verbatim quotes. "Amir" in the quote column means his own words; "rule text" means the doctrine text that records his ruling (the ruling is his, the wording is the agent's). Dates are the ruling dates recorded in the source.

| Rule | Exact quote | Source path | Date |
|---|---|---|---|
| Never the word "receipt" in anything a human reads | Rule text: "Never use the word "receipt" (or "receipts") in anything written for a human to read: decks, reports, docs, chat answers, PR bodies, sheet cells, copy. Say "source", "proof", or "evidence" instead, or name the actual thing (the query, table, dashboard, ledger row)." | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` (Writing Rule: Never Use The Word "Receipt") | 2026-08-31 |
| Never em dashes | Rule text: "in anything written for a human to read: emails, store review replies, website and store copy, lifecycle messages, docs, sheet cells, PR bodies, chat answers. Use a comma, a period, a colon, or parentheses instead. Restructure the sentence if none of those fit. Em dashes are a known AI tell and Amir has ruled them out unconditionally." (The rule's last sentence tells the writer to search the draft for the character and remove every one; the character itself is omitted here.) | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` (Writing Rule: Never Use Em Dashes) | 2026-07-08 |
| Plain English, never bare codes | Rule text: "Never refer to anything by an internal code, label, or ID alone ("C35", "MW-004", "cluster 7", "variant B") in anything Amir reads: chat answers, reports, docs, sheet cells, Slack, PR bodies. Assume he has no idea what the code means. Name the thing in plain English on every mention, not just the first; a code defined 40 lines earlier is still a bare code here. When the exact code is genuinely needed as a receipt or lookup key, put it in parentheses after the plain-English name: "the paywall copy test (C35)", never "C35"." | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` (Plain English, Never Bare Codes) | 2026-08-21 |
| PR and issue mentions are hyperlinks | Rule text: "Every PR or issue mentioned in anything Amir reads (chat answers, reports, PR bodies, Slack, docs) is written as a clickable hyperlink to it, labeled with the repo and number or title ... Never a bare number like "PR #4290" that he has to go find. On surfaces where Markdown links do not render, paste the full URL next to the number." | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` (PR And Issue Mentions Are Hyperlinks) | 2026-08-21 |
| File paths are always absolute | Rule text: "always give the full absolute path on disk (`/Users/aelaguiz/workspace/...`), never a repo-relative path. He should never have to ask "where is that on disk."" | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` (File Paths Are Always Absolute) | 2026-08-24 |
| No invented personas | Rule text: "Never invent named fictional users ("Mina", "Theo", "Priya") to narrate journeys, specs, reports, or plans: describe the situation itself ("player who misses one day", "player already at the cap")." | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` (No Invented Personas) | 2026-07-24 |
| Merged means done; never re-raise "not shipped" | Rule text: "Once a fix or feature is merged to the shared repo's main, treat it as DONE in all conversation with Amir. Never re-raise "it hasn't shipped / it's in no release cut yet" as a status update, a recommendation lead, or a repeated caveat. ... Why: the agent repeatedly told Amir a merged fix "was in no release" while recommending next work, which reads as nagging him about something he just fixed." | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` (Merged Means Done) | 2026-07-08 |
| No engineering-time estimates in recommendations | Rule text: "Never produce engineering-time estimates or let estimated engineering time influence any recommendation, priority, scope, or decision." | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` (Startup Reality) | added 2026-08-27 (git history) |
| "Receipt" means a ledger line, never software | Rule text: ""Receipt" in this repo means a dated `LOG.md` or ledger line, never new software." | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` (Startup Reality) | added 2026-07-26 (git history) |
| One living report per workstream, updated in place | Rule text: "Amir was getting a pile of little report files and links to track per investigation; that is the failure mode this rule kills." | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` (Update The Owning Report, Don't Multiply Report Files) | 2026-07-18 |
| Working documents are markdown; shares are renderings | Rule text: "Every working document lives as a markdown file on disk in this repo, edited in place; the markdown is the single source of truth. A cf-share is only a read-only rendering of a markdown source" | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` (Working Documents Are Markdown) | 2026-08-21 |
| Web reports use the house style kit | Rule text: "Do not improvise CSS, pull a different framework, or invent chart colors." Amir: "we have a literal format we've defined" | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` (Web Reports Use The Report Style Kit); Amir quote in `/Users/aelaguiz/workspace/psagentspace/skills/weekly-ops-report/SKILL.md` | 2026-07-17; quote 2026-08-02 |
| Charts left to right, tables newest first | Rule text: "Every chart ordered by time, date, release, or app version flows from left to right. ... Vertical tables, cohort views, release lists, and other top-to-bottom displays remain newest-first by default, with the newest row at the top." | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` (Charts Flow Left To Right; Tables Stay Newest First) | 2026-07-20 |
| Sheets: one row per item, never paragraph cells | Rule text: "one row per item, never paragraph cells; text longer than a line spans merged cells" | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` (Spreadsheets Follow The Sheet Guide) | 2026-08-03 |
| QA steps a non-engineer can run | Rule text: "numbered steps a non-engineer can run with expected results, the named setup lane that puts a tester in the right state" | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` (User-Facing Changes Are Never A Surprise) | 2026-08-02 |
| No text walls | Amir: "don't write a fucking book" (2026-08-02); "that whole box needs to be way simpler... If you only read one thing, then it's fucking a wall of text" (2026-08-17). Rule text: "A paragraph carries ONE point in at most two to three short sentences; a passage carrying multiple points becomes bullets, with sub-bullets when a point has parts. ... Simple and easy to understand beats comprehensive-sounding; if a skimmer cannot pull the points out in seconds, the writing failed regardless of accuracy." | `/Users/aelaguiz/workspace/psagentspace/skills/weekly-ops-report/SKILL.md` (No text walls) | 2026-08-02, escalated 2026-08-17 |
| Box density law | Rule text: "One point per bullet. A bullet with two clauses doing separate jobs is two bullets. Plain short sentences at plain reading level. Target median around 100 characters per bullet; HARD CEILING around 250. A bullet over the ceiling gets rewritten, never trimmed at the margin. No multi-clause paragraph anywhere inside the box. ... Internal-ledger jargon is translated before it may enter the box: no verifier family names, no "pre-registered rule" without saying what the rule does in plain words, no house vocabulary a first-time reader cannot parse." | `/Users/aelaguiz/workspace/psagentspace/skills/weekly-ops-report/SKILL.md` (The box density law) | 2026-08-17 |
| Never "close rate" for checkout completion | Rule text: "NEVER call checkout completion a "close rate" anywhere (it reads as closing the paywall dialog, a real bug class we shipped); say "checkout conversion rate"." | `/Users/aelaguiz/workspace/psagentspace/skills/weekly-ops-report/SKILL.md` (living block, VOCABULARY) | 2026-08-24 |
| Nothing in Amir's voice without his words | Rule text: "Never write a rule, decision, threshold, plan, or intention in Amir's voice ("my rule", "my call", "I will", "predeclared") unless it traces to words Amir actually said, with the receipt". Amir, on the invented rule: "I'm not doing this. I'm not even considering this. I'm fucking debugging things and the last thing I'm going to do is stop spend so I get less data." | `/Users/aelaguiz/workspace/psagentspace/skills/weekly-ops-report/SKILL.md`; quote in `/Users/aelaguiz/workspace/psagentspace/_artifacts/2026-08-17-monday-update/RECEIPTS.md` | 2026-08-17 |
| Do not quote his corrections back on the page | Rule text: "Internalize the framing; do not quote Amir's own correction back on the page." | `/Users/aelaguiz/workspace/psagentspace/skills/weekly-ops-report/SKILL.md` (Framing rule) | 2026-08-31 |
| No self-reference or report-about-itself | Rule text: "No third-person self-reference ("agents build this page") and no report-about-itself exposition anywhere." | `/Users/aelaguiz/workspace/psagentspace/skills/weekly-ops-report/SKILL.md` (The overlay) | 2026-07-27 |
| The email lead is the message, not the damage | Rule text: "the "If you read nothing else:" line carries the week's MESSAGE ... and the bad numbers enter afterward as the priced cost of that story, stated plainly but never as the headline. Opening with the damage reads as panic" | `/Users/aelaguiz/workspace/psagentspace/skills/weekly-ops-report/SKILL.md` | 2026-08-02 |
| Fifth-grade readability for player copy | Ledger: Amir asked for the plain-language review "with fifth-grade readability as the target and 'Correct the decision directly' as a known bad example." Guide: "Target register is a sharp friend at a home game, readable by a fifth grader." | `/Users/aelaguiz/workspace/psagentspace/research/2026-08-22-coaching-style-guide/worker-corrections-ledger.md` (rule 2.11); `/Users/aelaguiz/workspace/psagentspace/docs/COACHING_STYLE_GUIDE.md` (G4) | 2026-08-14 |
| Active voice, actor named, actionable | Amir: "It's sort of passive voice, right? It should be like, 'You should have raised preflop. You should have folded preflop,' something like that, giving them actual actionable feedback." | `/Users/aelaguiz/workspace/psagentspace/docs/COACHING_STYLE_GUIDE.md` (G2) | 2026-08-21 |
| Simplify; no internal concept names in reader-facing text | Amir: "Who the fuck is the greater? We have no user-facing concept called a fucking greater." and "Just say 'you shouldn't have folded.' Simplify." and "Another one is this passive voice: 'The flop fold is the one to look back.' No that's confusing. ... 'You probably shouldn't have folded the flop' is a much better way of fucking saying that, right?" | `/Users/aelaguiz/workspace/psagentspace/research/2026-08-23-voice-guide-playbook/worker-prime-sessions.md` (Episode 3; Prime session 01a0169f-a0ce-77d8-ae33-b90888b1ef1b) | 2026-08-18 |
| Headlines must mean something alone | Amir: "this shit 'The offer' and 'The price' it dominates the screen its bolded and pink and literally means nothing. the headlines have to be less cryptic and more meaningful... mean something on their own and still be short and punc and non duplicative with the coaching text." | `/Users/aelaguiz/workspace/psagentspace/research/2026-08-22-coaching-style-guide/worker-corrections-ledger.md` (A.1) | 2026-08-22 |
| A headline is an executable thought | Amir: "Its not just that they are short poekr statements its that they tell you what to do if you actually think about them. Do the math, Thin value, they fucking clearly imply that if you do what they say or read them you should fold. Its more than just some random statement. Say it back to me." | `/Users/aelaguiz/workspace/psagentspace/research/2026-08-23-voice-guide-playbook/worker-prime-sessions.md` | 2026-08-22 |
| Direct phrasing over convoluted phrasing | Amir: "It's confusingly worded. I would just say 'almost never fold to this raise'." | `/Users/aelaguiz/workspace/psagentspace/research/2026-08-22-coaching-style-guide/worker-corrections-ledger.md` (rule 2.13) | 2026-08-21 |
| Sources are means, not the deliverable | Amir: "I don't care about receipts motherfucker. I care about good headlines and good copy." | `/Users/aelaguiz/workspace/psagentspace/research/2026-08-22-coaching-style-guide/worker-corrections-ledger.md` (A.6) | 2026-08-23 |
| No internal jargon in anything Amir reads about a program | Ledger paraphrase: "No internal jargon in anything Amir reads about this program (plain-English workstream names, no probe numbers)." | `/Users/aelaguiz/workspace/psagentspace/research/2026-08-22-coaching-style-guide/worker-corrections-ledger.md` (rule 8.6) | 2026-08-21 |
| Unparseable prose is a rejection, even when short and true | Amir: "Two, I can't even understand what the fuck you're saying. It's so confusing, what you're saying." | `/Users/aelaguiz/workspace/psagentspace/research/2026-07-18-amir-ai-expert-x-strategy/amir-draft-verdicts.md` | 2026-08-15 |
| Never lead with a term the reader has not met | Amir: "what the FUCK is the M cooncpet thats what is so confusing"; then on the plain-words rewrite: "yeah v3 is good post it" | same file | 2026-08-15 |
| Anything he must decide on is decidable from that one message | Amir: "Dude, I don't know the fucking original post. Why do you keep doing this? How am I supposed to respond?" | same file | 2026-08-15 |
| Every sentence is a claim with a provenance question | Amir: "What the fuck is this assertion that big pots deep are mostly flush over flush? Where the fuck did this come from, dude? This all just seems like gibberish. Did you make all of this up without following our protocols?" | same file | 2026-08-15 |
| Do not explain what the reader already knows | Amir: "Dude, you're literally defining a fucking wheel. ... Do you have any idea how bad it makes me look when you're explaining the cards it takes to make a nut straight as the wheel?" | same file | 2026-08-15 |
| Not a calculator; not formulaic | Amir: "Hold on, dude. Does part of our process involve looking at all of our recent posts and being less formulaic? Your responses are so heavily like, 'Here's the exact pot odds.' It's almost like you're being a fucking calculator." and "Do you see the formulaic nature of your posts? Are you seeing how it's becoming repetitive?" | same file (2026-08-11); `/Users/aelaguiz/workspace/psagentspace/roadmaps/growth/2026-07-12-community-ua-strategy/LEARNINGS.md` (2026-08-08) | 2026-08-08, 2026-08-11 |
| Less flowery, less verbose | Amir: "make 1 less flowery and overly verbose match go re-read our ledger and style guide." | `/Users/aelaguiz/workspace/psagentspace/research/2026-07-18-amir-ai-expert-x-strategy/amir-draft-verdicts.md` | 2026-08-23 |
| Positional references that do not hold for the reader are banned | Amir: "stop referring to posts on reddit as above or below. They are dynamically ordered and it make sno sense. Update your materials to reflect that and then try again" | same file | 2026-09-05 |
| Tag the valence before the quote | Amir: "indicate whether it's bad about us, good about us, or just conversational engagement... so that I don't have to try to parse it out without context." | `/Users/aelaguiz/workspace/psagentspace/roadmaps/growth/2026-07-12-community-ua-strategy/LEARNINGS.md` | 2026-08-13 |
| No nominalizing the activity | Amir: "you tend to make the thing they are doing an object 'the study' thats not how people talk." | same file | 2026-08-30 |
| Do not re-surface unanswered items | Amir: "If I haven't responded to you about a post in like 24 hours, please don't remind me about it forever. All right? Like a day, two days, then stop." | same file | 2026-08-04 |
| Personable, first person, not signage | Amir: "Our posts and our subreddit should be personable. They should be me, the founder, not fucking signage. That's the worst thing." Verdicts on two drafts: "it's not personable." and "you're writing mechanically". | `/Users/aelaguiz/workspace/psagentspace/skills/pokerskill-subreddit-posts/references/voice-and-framing.md` (rule 0); `/Users/aelaguiz/workspace/psagentspace/research/2026-07-29-owned-subreddit-decision/POST_LEDGER.md` | 2026-08-04; 2026-08-10 |
| People are people, not program furniture | Amir: "It's so weird. The Release Crew is like 50 people I picked by hand. We call them people, not seats." | `/Users/aelaguiz/workspace/psagentspace/skills/pokerskill-subreddit-posts/references/voice-and-framing.md` | 2026-08-04 |
| A correction to a template is not a new template | Amir: "lol you made 3 even more fucking formulaic." and "Don't build some fucking harness, you fucking idiot. Just update the skill." | `/Users/aelaguiz/workspace/psagentspace/docs/VOICE_GUIDE_PLAYBOOK.md` (section 10) | 2026-08-09 |
| Not every correction is a rule | Amir: "i didn't say change a rule. I just said this one dashboard." | `/Users/aelaguiz/workspace/psagentspace/docs/VOICE_GUIDE_PLAYBOOK.md` (section 7) | undated in source |
| Hyphenated coinages sound like AI | Amir: "Do not say bluff or better hyphenated like that it sounds like AI. Rewrite for me" | `/Users/aelaguiz/workspace/psagentspace/docs/VOICE_GUIDE_PLAYBOOK.md` (section 10) | 2026-08-22 |
| Save his feedback verbatim | Amir: "Make sure you're saving out the feedback I give you on these things so you're building a corpus of information." | `/Users/aelaguiz/workspace/psagentspace/research/2026-07-18-amir-ai-expert-x-strategy/amir-draft-verdicts.md` | 2026-08-01 |
| Simple plain English is a standing instruction to models | Amir (to Andrew, about GPT): "with gpt  I still have to reinforce like SIMPLE PLAIN ENGLISH" then "otherwise I just get spammed" | `/Users/aelaguiz/workspace/psagentspace/research/2026-08-11-andrew-telegram-backfill/telegram-fc3-2026-01-01_to_2026-05-01.md` | 2026-04-25 |
| He asks for plain English and then for the exact term | Amir: "what does that mean in plain english this pair thing" then "are you saying its a reverse incompatible build?"; and "@Ops what merged into main since our last staging cut? Tell me in plain english the impact of each" | `/Users/aelaguiz/workspace/psagentspace/research/2026-08-10-weekly-comms/slack-2026-08-03_to_2026-08-10.md` | 2026-08-05; 2026-08-06 |
| Lead with the answer; number steps; no preamble (his own agent contract) | Rule text (installed by Amir for every agent run): "1. Lead with the answer or next action: command, path, or snippet first. 2. Number multi-step work; one bounded action per step. 3. End with one next action doable in under two minutes. 4. Finish the current issue before raising a new one. 5. Restate progress each turn ("step 3 of 5 done"). 6. Give time estimates in concrete units, never "a bit". 7. After a change, show what now works. 8. Errors: state location, cause, and fix. No drama. 9. Cap lists at 5 items. 10. No preamble, no recaps, no closers." | `/Users/aelaguiz/.codex/AGENTS.md` (Output style); longer wording of the same ten rules in `/Users/aelaguiz/workspace/prime-adhd/rules/ADHD_OUTPUT.md` | 2026-08-13 (prime-adhd commit date) |
| Lead with the concrete outcome | Rule text: "Lead with the concrete outcome in plain English and name what changed." | `/Users/aelaguiz/.codex/AGENTS.md` (Communication) | undated |
| Write for a human first; plain English; lead with the concrete thing | Rule text: "Write for a human reader first. Use plain English. Do not make the reader decode house jargon, compressed labels, or pseudo-technical wording. Lead with the concrete thing in 1-3 sentences: what changed, what to run, what happens next, or what the blocker is. If the real answer is a path, command, setting, or skill name, name that exact thing first. Prefer simple action language over doctrine language. If the rule is simple, write the simple rule." | `/Users/aelaguiz/workspace/arch_skill/AGENTS.md` (Writing And Replies) | added 2026-04-02 (git history) |
| Public copy serves the reader, never the writer | Rule text: "Who is this sentence speaking to, and about what?" and "If it speaks about the page itself, where its content came from, how it was assembled, or how it relates to other surfaces ... writer-rationale, not copy, and does not save." | `/Users/aelaguiz/workspace/website/AGENTS.md` (Public copy is for the reader) | undated (stable since April 2026 per the playbook) |

## What Amir-approved readable writing looks like

Five excerpts. Each is either his own text or text he approved or sent. One line under each says why it reads easily.

### 1. His own Reddit release opener (2026-08-10)

Amir rejected the agent's draft ("it's not personable.") and supplied this opener himself:

> "Alright, 2.1.3.7 is live, guys. It's mostly bug fixes, but don't worry, we got some big features coming. If you've been having issues with your streaks, this should repair it. If you think you got a dead streak that you want us to resurrect, send me a message."

Source: `/Users/aelaguiz/workspace/psagentspace/research/2026-07-29-owned-subreddit-decision/POST_LEDGER.md` ("Read this before drafting anything: Amir's own words, 2026-08-10").

Why it reads easily: the state comes first ("is live"), the size of the change is stated honestly in plain words, each fix is aimed at the person it affects ("If you've been having issues with your streaks"), and it ends with the next action.

### 2. His own bug-post rewrite (2026-08-10)

The agent's draft used `Workaround:` / `Affects:` / `Where it sits:` labels. Amir: "you're writing mechanically". What he would have written:

> "Hey, if you get a button that says "Critical Update Ready," I know it's on iOS. I know it's confusing. The button does nothing. You have to close the app and restart it."

Source: same file.

Why it reads easily: one symptom the reader recognizes, then three short facts in the order the reader needs them (it is known, it does nothing, do this). No label scaffolding; every obligation lives inside a sentence.

### 3. His own explanation of a problem to Andrew Sheppard of Transcend Fund, his board-side operating partner (Telegram, 2026-07-18)

> "theres 3 issues:
>
> 1. Fix them and yes get that benefit
> 2. How do we prevent this from ever regressing again
> 3. How did our analysis not surface these sooner"

> "the answer for 3 is that we weren't slicing by app version enough. In some places we did, but mostly were looking at blended."

> "Most of this shit jumps off screen when sliced by version after you give it any reasonable amount of time to settle"

> "on blended it just looks like one long slow decline that feels bad but is hard to pin point"

Source: `/Users/aelaguiz/workspace/psagentspace/research/2026-07-18-fc3-ops-accountability-chat/TRANSCRIPT.md` (5:38 to 5:39 AM).

Why it reads easily: he numbers the issues before discussing any of them, answers one at a time by number, gives the mechanism in one sentence, and then the contrast case in one sentence. Every sentence has an actor ("we weren't slicing"). No term is introduced before the idea.

### 4. The Monday investor email he sent (2026-08-17)

Amir reviewed and sent this body verbatim after asking for the takeaway box to be "way simpler". Opening and first block:

> "If you read nothing else: we found the quarter's biggest revenue lever. The paygate changes we made to survive July's App Review emergency halved our checkout close rate on both stores, and the working version is already going back in.
>
> The halving, receipted:
>
> - Checkout-to-purchase completion: 58 to 66% in May and June, 49% in July, 26% on the current build (40 of 153).
> - The review-safe presentation is the mechanism. iOS needed it. Putting it on the Play Store too was my own unforced error, made mid-emergency, and it erased the control group that would have exposed this in days.
> - The way back: the original presentation is already the Android 2.1.38 default, the puzzle paywalls are back after four months dark, and hosted paygates behind feature flags come next, Android first. If it closes like it used to, that is roughly a doubling of checkout completion at unchanged traffic."

Source: `/Users/aelaguiz/workspace/psagentspace/_artifacts/2026-08-17-monday-update/SENT_EMAIL_2026-08-17.md`. Note: two words in this sent text were banned afterward ("close rate" on 2026-08-24, "receipt" on 2026-08-31); the shape is what to copy, not those two words.

Why it reads easily: the one-line message comes first, then a labeled block, then one point per bullet with the number, the mechanism, and the next step each in its own bullet. A skimmer who stops after the first line still has the story.

### 5. The coaching headline table he approved (2026-08-22)

| Killed (fielded) | Approved replacement |
|---|---|
| "The offer" | "Priced in?" |
| "The price" | "A good investment?" |
| "Break-even" | "Know the numbers" |
| "Board check" | "Miss the flop?" |
| "Showdown value" | "No more drawing" |

Source: `/Users/aelaguiz/workspace/psagentspace/docs/COACHING_STYLE_GUIDE.md` (H2, "Meaningful standing alone, never a cryptic label").

Why it reads easily: every approved line is a thought the reader can act on without the body text. Every killed line is a category label that only makes sense to the person who built the categories. **Inference:** "Checkout root now clean, children blocked." is a category label of the same kind: it names the writer's mental model (a stacked set of pull requests with a root and children) instead of the reader's question (what is done, what is stuck, what happens next).

### Also: the store reply guide's graded pair

`/Users/aelaguiz/workspace/psagentspace/skills/store-review-reply-writing/references/APP_STORE_REVIEW_REPLY_VOICE_GUIDE.md` (revised after an operator review loop, 2026-03-08). North star: "Sounds like Amir. Period." Its method: "examples beat abstractions", "operator rewrites beat principles", "if a draft sounds like generic app support, it failed", and "Content can be right and still be too dry." One graded pair from the review loop (guide text, shapes Amir graded, not his own sentences):

> Dry: "Thanks for the feedback. If you couldn't even get through signup, that's not at all how it's supposed to work."
>
> Better: "That's a brutal way to hit the app for the first time. If signup is failing, that's a miss on our side. We've been putting a lot of work into login stability lately, and I think you'd find Poker Skill in a much better spot now."

Why the better one reads easily: it names the reader's experience first, owns the problem in one short sentence, then says what changed and what to do. Same shape as his own release opener.

### Also approved: the Voice Guide Playbook itself

`/Users/aelaguiz/workspace/psagentspace/docs/VOICE_GUIDE_PLAYBOOK.md` opens: "Put your taste in one Markdown file. Make every tool read it. Fold every correction back in. That is the whole method." Its structure is the readable-document template in this workspace: the whole idea in 30 seconds (five numbered steps), then "How do I start? Do this today.", real prompts before rules, every rule with a dated quote, every ban with its repair, one-line "why" under each example, and printable checklists at the end. Its sentences are short, second person, and concrete ("A file nobody reads is a wish.").

## How Amir himself writes

He types from the hip, usually by voice-to-text, so typos stay ("cooncpet", "poekr", "ownersihp"). Claim first, mechanism second, no hedge. First person, present tense, active verbs. He names the actor and the consequence in the same sentence and stops when the point lands; there is no closing line. He numbers things when there are several ("theres 3 issues:"), uses real numbers when he has them, and coins a plain name for a pattern rather than reaching for a technical term ("death by a thousand cuts", "slicing by version"). He addresses the reader directly ("dude", "guys", "man") and asks for a readback when he wants to know he was understood ("Say it back to me"). Swearing is emphasis, not anger. When he wants precision he asks for the exact term after the plain version ("are you saying its a reverse incompatible build?"). Corpus facts from his X posts: median 148 characters, 53% carry a concrete number, 9% questions, 3% lists, zero em dashes, zero hashtags (`/Users/aelaguiz/workspace/psagentspace/research/2026-07-18-amir-ai-expert-x-strategy/amirpc-voice-analysis-2026-07-18.md`).

Three verbatim samples of him explaining something:

1. Telegram, the FC 3.0 group with Andrew Sheppard, 2026-08-27: "2.1.40 is live but don't expect much for a few days every time I launch a new monetization feature set that affects entitlements it takes me half a week to get it perfect. Its just a complex orchestration between third parties which makes testing of limited value." (`/Users/aelaguiz/workspace/psagentspace/research/2026-08-31-weekly-comms/telegram-fc3-2026-08-24_to_2026-08-31.md`, 12:40 UTC)

2. Slack, #engineering, 2026-08-26: "I'm going to flip this live for all PRs on github. You guys will see this one "buildkite/psmobile-shadow-ci" runner as a new action. My intent is that this replaces our slow github CI for all testing and is way faster. For now I will run it in parallel, but our hand may be forced by how flakey github actions has been" (`/Users/aelaguiz/workspace/psagentspace/research/2026-08-31-weekly-comms/slack-2026-08-24_to_2026-08-31.md`, 19:50 UTC)

3. Slack, #growth-team, to Natasha, 2026-08-27 (the line before it: "@Natasha Johnson the critical thing is install cohorts by week, not blended over time only. You need to see that each new week worth of installs has a slightly better experience over time."): "these aggregate views are mostly always going to look good, its really like if you take a week of installs from a month ago vs a week of installs now are we giving those players a better experienc ecompared side by side" (same Slack file, 11:52 UTC)

**Inference:** the common shape is state, then why, then what it means for the reader, in three or four plain sentences, with the exact technical name quoted where it will appear on screen ("buildkite/psmobile-shadow-ci").

## What he rejects

### The canonical banned list

One file owns the AI-tell list and every other skill points at it: `/Users/aelaguiz/workspace/psagentspace/skills/fc-authored-copy/references/editorial-judgment.md`. The rule for using it (from `/Users/aelaguiz/workspace/psagentspace/skills/fc-authored-copy/SKILL.md`, non-negotiable 8): "Remove a banned word by repairing the sentence, never by swapping a synonym, and drop the Oxford comma unless removing it changes the meaning of the list."

The four measured tells, banned outright (Pew Research Center count across 490,000 web pages, cited in that file):

1. Em dash. "Never use U+2014 under this local skill contract."
2. The 27 AI-vocabulary words: "additionally, align with, boasts, bolstered, crucial, delve, emphasizing, enduring, enhance, essential, fostering, garner, highlight, interplay, intricate, key, landscape, meticulous, perfectly, pivotal, showcase, significant, tapestry, testament, underscore, valuable, vibrant". Three narrow exemptions (a quotation or product name, a domain term with no substitute, mirroring a user's own wording).
3. Negative parallelism: "it's not just X, it's Y".
4. The default Oxford comma: "Drop it by default in Fun Country public prose. Keep it only where removing it changes the meaning of the list".

Plus, in personal-voice channels: "do not stack hyphenated compound modifiers ... never use more than one hyphenated compound per short post" (Amir ruling 2026-07-24, recorded in the same SKILL.md).

### The 15 items from that file most relevant to reports

Quoted from `/Users/aelaguiz/workspace/psagentspace/skills/fc-authored-copy/references/editorial-judgment.md`. Items 1 to 5 and 8 are table rows quoted as "signal: why it matters"; an ellipsis marks omitted text.

1. "Interface leakage: Chatbot greetings, progress narration, offers to continue, and model disclaimers do not belong in finished copy" (very high severity).
2. "Unsupported or vague grounding: Unnamed experts, invented-looking quotations, source-free numbers, and frictionless certainty create factual and stylistic risk" (very high).
3. "Polished low-information prose: The writing sounds complete but adds little evidence, mechanism, consequence, or judgment" (high). The test: "Replace the main company, product, or topic nouns with unrelated nouns. Ask whether most of the paragraph still sounds plausible."
4. "Repeated rhetorical geometry: Several contrast frames, triads, balanced clauses, or dramatic pivots reveal a reusable template" (high).
5. "Templated macrostructure: Generic context, exhaustive middle, recap, caveat, and optimistic close make unrelated pieces share one skeleton" (high).
6. "Participial tails and abstract packaging: Repeated endings such as "ensuring" or "highlighting" often simulate analysis without adding a causal link".
7. "Nominalization and noun-heavy packaging ... implementation of, development of, facilitation of ... restore the actor and action."
8. "Weak indexical detail: Few names, dates, quantities, constraints, local references, or situation-specific decisions make the prose interchangeable".
9. "Reveal bridges ... "Here is the real issue." "What matters most is..." "The deeper point..."".
10. "Maximum-abstraction openers ... Start with the event, answer, disagreement, surprising detail, or consequence."
11. "Generic setup ... restating the prompt before answering; announcing "Here is a breakdown"; defining an obvious term; offering context the intended reader already has".
12. "Exhaustive-looking middle: Models often cover every plausible angle at equal weight. Human experts select."
13. "Recap loops ... State the point once, then develop or qualify it. A conclusion should advance, land, or stop."
14. "Elegant but false causality: Words such as "thereby," "ensuring," "ultimately," and "in turn" can make sequence look like causation."
15. "Abstract significance: Phrases such as "underscores the importance," "serves as a testament," "reflects a broader shift," and "marks a pivotal moment" tell readers how much something matters without showing why."

Its closing checklist is worth copying into any report gate: "1. The reader gets the answer or point quickly. 2. Every important claim has a source, observation, or clearly marked inference. 3. Rhetorical patterns serve meaning and do not stack into a template. 4. Sentence and paragraph rhythm follow the ideas. 5. The copy contains no assistant residue or ceremonial conclusion. ... 8. There is no U+2014 character."

Secondary lists (same bans, longer tables, do not treat as canonical): `/Users/aelaguiz/workspace/psagentspace/skills/human-writing/SKILL.md` (hedging words "typically, often, sometimes, potentially, usually, rather"; filler phrases "it's important to note", "in order to", "serves as a"; sentence starters "This document/guide...") and `/Users/aelaguiz/workspace/psagentspace/skills/humanizer/SKILL.md` (the Wikipedia "Signs of AI writing" list with the Fun Country bans on top).

### Structural patterns Amir has ruled out, with the source

Short source names in this table: "corrections ledger" is `/Users/aelaguiz/workspace/psagentspace/research/2026-08-22-coaching-style-guide/worker-corrections-ledger.md`; "draft verdicts" is `/Users/aelaguiz/workspace/psagentspace/research/2026-07-18-amir-ai-expert-x-strategy/amir-draft-verdicts.md`; "community LEARNINGS" is `/Users/aelaguiz/workspace/psagentspace/roadmaps/growth/2026-07-12-community-ua-strategy/LEARNINGS.md`; "POST_LEDGER" is `/Users/aelaguiz/workspace/psagentspace/research/2026-07-29-owned-subreddit-decision/POST_LEDGER.md`; "coaching guide" is `/Users/aelaguiz/workspace/psagentspace/docs/COACHING_STYLE_GUIDE.md`; "RECEIPTS.md" is `/Users/aelaguiz/workspace/psagentspace/_artifacts/2026-08-17-monday-update/RECEIPTS.md`; "VOICE_GUIDE_PLAYBOOK.md" is `/Users/aelaguiz/workspace/psagentspace/docs/VOICE_GUIDE_PLAYBOOK.md`; "subreddit voice-and-framing.md" is `/Users/aelaguiz/workspace/psagentspace/skills/pokerskill-subreddit-posts/references/voice-and-framing.md`; "weekly-ops-report SKILL.md" is `/Users/aelaguiz/workspace/psagentspace/skills/weekly-ops-report/SKILL.md`.

| Pattern | Amir's words or the ruling | Source |
|---|---|---|
| Walls of text; multi-clause paragraphs carrying several points | "don't write a fucking book"; "If you only read one thing, then it's fucking a wall of text" | `/Users/aelaguiz/workspace/psagentspace/skills/weekly-ops-report/SKILL.md` |
| Bare codes and IDs ("C35", "MW-004", "cluster 7", "variant B") | "Assume he has no idea what the code means." | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` |
| Bare PR or issue numbers | "Never a bare number like "PR #4290" that he has to go find." | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` |
| Cryptic labels as headings | "it dominates the screen its bolded and pink and literally means nothing" | corrections ledger A.1 |
| Leading with an unmet term | "what the FUCK is the M cooncpet thats what is so confusing" | draft verdicts, 2026-08-15 |
| Appositive chains that rename one thing three ways | "I can't even understand what the fuck you're saying." | draft verdicts, 2026-08-15 |
| Explaining what the reader already knows | "you're literally defining a fucking wheel" | draft verdicts, 2026-08-15 |
| Agentless passive; judgment attached to the thing instead of the actor | "It's sort of passive voice, right?"; "Preflop was a mistake." killed | coaching guide G2, G3 |
| Nominalized activity | "thats not how people talk" | community LEARNINGS, 2026-08-30 |
| Template labels on a personal surface (`Workaround:` / `Affects:`) | "you're writing mechanically" | POST_LEDGER, 2026-08-10 |
| Accurate changelog with no reader addressed | "it's not personable." | POST_LEDGER, 2026-08-10 |
| Hedging a clear call ("probably right" on a 100% spot) | "No fake-humble hedging" [Amir, 2026-08-21] | coaching guide G8 |
| Invented difficulty or invented calm | "No invented difficulty ("tough spot" on a trivial one) and no invented cleanliness" | coaching guide G8 |
| Alarm framing on a planned, expected cost | "Alarm framing on an anticipated cost reads as panic and misses the point" | weekly-ops-report SKILL.md, 2026-08-02 |
| Re-raising a merged fix as "not shipped yet" | "reads as nagging him about something he just fixed" | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` |
| Re-surfacing an unanswered item every run | "please don't remind me about it forever" | community LEARNINGS, 2026-08-04 |
| Writing in his voice without his words | "I'm not doing this. I'm not even considering this." | RECEIPTS.md 2026-08-17 |
| The report talking about itself | "No third-person self-reference ("agents build this page") and no report-about-itself exposition anywhere." | weekly-ops-report SKILL.md |
| Positional references that depend on the reader's view ("the reply above") | "They are dynamically ordered and it make sno sense." | draft verdicts, 2026-09-05 |
| Formula and rotation as a fix for formula | "you made 3 even more fucking formulaic." | VOICE_GUIDE_PLAYBOOK.md |
| Invented personas in reports | "describe the situation itself" | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` |
| The word "receipt" in prose | "Say "source", "proof", or "evidence" instead, or name the actual thing" | `/Users/aelaguiz/workspace/psagentspace/AGENTS.md` |
| Enthusiasm, certification words, kicker closes | "Enthusiasm is scarce currency"; "Do not certify authenticity"; "End on the last fact or the ask." and "Never a kicker, punchline, or moralized sign-off." | subreddit voice-and-framing.md rules 2 to 4 |

## Gaps: what the corpus does not cover, and the report problem needs

Everything below is my reading of the evidence (**inference**), with the nearest existing rule named so the skill author can extend rather than invent.

### 1. No rule says how to expand a compressed status phrase

The sample line, with the source data behind it (`/Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06/sources/github/final-status.json`, collected 2026-09-06 15:40 UTC):

- "Checkout root now clean, children blocked."
- The data: [psmobile #5001](https://github.com/funcountry/psmobile/pull/5001) "Explain Android checkout cancellations with bounded attempt evidence" has GitHub merge state `CLEAN`. Four pull requests stacked on it, [#5056](https://github.com/funcountry/psmobile/pull/5056) "release confirmed access while storage settlement waits", [#5057](https://github.com/funcountry/psmobile/pull/5057) "retain checkout-initiating app version on subscription commits", [#5058](https://github.com/funcountry/psmobile/pull/5058) "preserve current subscription identity before plan changes", and [#5059](https://github.com/funcountry/psmobile/pull/5059) "settle original subscription transactions after renewal", have merge state `BLOCKED`.
- What went wrong in the writing: "root" and "children" are the writer's stacked-PR vocabulary, not the reader's; "clean" and "blocked" are GitHub's `mergeStateStatus` enum values pasted into prose; no PR is named or linked; the reader cannot tell what is done, what is stuck, why, or who acts.
- A plain-English version, as one candidate for the skill's worked example: "Your checkout-fix stack: the base pull request ([psmobile #5001](https://github.com/funcountry/psmobile/pull/5001), Android checkout cancellation evidence) passes checks and can merge. The four fixes stacked on top of it ([#5056](https://github.com/funcountry/psmobile/pull/5056) to [#5059](https://github.com/funcountry/psmobile/pull/5059)) show as blocked on GitHub, which in psmobile usually means a required review or the `ufc-approved` label is missing. Next: merge the base, then clear the four." The exact cause of `BLOCKED` was not read from the PRs during this research; the writer of the report should have read it.

Nearest existing rules: "Plain English, Never Bare Codes" (name the thing on every mention) and "PR And Issue Mentions Are Hyperlinks". Neither says that tool states (`CLEAN`, `BLOCKED`, `UNSTABLE`, `draft`, "merged but not in the release branch") need a plain sentence, or that the reader's model of the work, not the writer's data model, chooses the nouns.

### 2. No rule about verdict labels in table cells

Fifteen cells in the sample report carry three or more semicolon-joined clauses ("Reset running September 2/4; audience rebuilt; SDK finding and 8 ASO assets September 5. **Aligned; historical comparison unresolved.**"). The bold verdicts ("Aligned; finish delivery.") are compressed labels of the kind the coaching guide bans for headlines ("Meaningful standing alone, never a cryptic label"), but that rule is written for player copy. The spreadsheet rule ("one row per item, never paragraph cells") is the nearest rule for cells and it is written for Google Sheets. No rule covers markdown or HTML report tables. A candidate rule: a table cell holds one state or one fact in one sentence; a cell that needs semicolons is a list and gets its own rows or a bullet list.

### 3. No rule against telegraphic compression

The sample drops articles, verbs, and subjects ("Reset running September 2/4; audience rebuilt", "Friday: Home/report-card metrics", "Media bodies and final handoff unverified"). Amir's verdicts show he rejects this as hard as padding ("I can't even understand what the fuck you're saying" was on a 54-word post). The community ledger has the closest rule: "when a draft only fits the band by fusing sentences, the fix is cutting a claim, never fusing." No report-level rule says: write full sentences with a subject and a verb; if the cell is too long, cut a fact, do not cut the grammar.

### 4. No calibration rule for a smart engineering executive

Amir's complaint names both failure directions: "It either treats me like a child or it writes it in a way that requires full concentration". The corpus has the child-facing end (fifth-grade readability for players) and the tool-facing end (the bare-code ban), but no statement of who the report reader is. Evidence for the middle register: he asks "what does that mean in plain english" and then "are you saying its a reverse incompatible build?", so he wants the plain sentence and the precise term, in that order. He also rejects being told what he knows ("you're literally defining a fucking wheel"). A candidate rule: assume the reader is a senior engineer who has not been in this codebase or thread today; plain sentence first, exact term or identifier in parentheses, never a definition of anything an engineer already knows (pull request, CI, staging), always a definition of anything house-specific (a workbook name, an internal code, a verifier).

### 5. No acronym policy

The sample uses `GP` ten times and never expands it (it is the team's planning workbook in Google Sheets; the morning-priorities README calls it "GP workbook" and never spells out the letters either). Also unexpanded: `LTV` (customer lifetime value), `SNG` (sit-and-go tournament), `PvAI` (Play vs AI), `ASO` (app store optimization), `SDK` (software development kit), `D30` (day 30 after install), `OTA` (over-the-air update), `GSC` (Google Search Console), `UA` (user acquisition). The bare-code rule covers "internal code, label, or ID"; the box density law bans "house vocabulary a first-time reader cannot parse" but only for the investor email. No rule says which acronyms count as plain English for Amir and which must be spelled out on first use in every report.

### 6. No "reader's question first" rule for status writing

The Monday email has "If you read nothing else:" and the coaching guide has "point first", both for their own surfaces. No rule says a status entry answers, in order: what is the state, what is blocking, who acts next, by when (or "no date"). The prime-adhd contract says this for chat replies ("Lead with the answer or next action"), not for reports.

### 7. Vague attributions of people's words

"Amir's later assessment credits their partnership" is an example: no quote, no date, no link. The weekly-ops rule "First-person commitments require Amir's own words" covers his voice on an investor page; nothing covers third-person summaries of what someone said in an Amir-facing report. Candidate rule: when a report says someone said or decided something, quote the words or link the message with its date.

### 8. Two tensions the skill author must resolve, not paper over

- The prime-adhd contract says "Give time estimates in concrete units, never 'a bit'" (about the agent's own next action). Psagentspace says "Never produce engineering-time estimates or let estimated engineering time influence any recommendation". Read together: time estimates for the agent's own immediate work are wanted; engineering effort estimates in recommendations are banned. The skill should say both.
- The word "receipt" is banned in anything a human reads (2026-08-31), yet most doctrine in this workspace still uses it, including quotes in this file. A skill that copies phrasing from older skills will re-introduce it.

### 9. No rule about what a report is for versus what it records

The morning-priorities README (`/Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/README.md`) specifies sources, steps, and tables, and has no readability contract at all; the weekly-ops report has one. The sample report also spends its second half on coverage tables (21 source groups, refresh timestamps). Amir's rule for the investor page, "no report-about-itself exposition", and the box density law's "The dense versions live in the body and appendix, never the box." suggest a candidate rule: the report body is the judgment; how the report was built goes in an appendix or a separate working file.

### 10. No rule for the sentence-level "one-pass parse" test

The community ledger has one, written for forum posts: "the check is a cold read aloud asking 'could a non-native reader resolve every that/the rest/the part on first pass'". The coaching guide has "The seven tests, pocket form". Nothing equivalent exists for report sentences. Candidate test for the skill: read the sentence once, cold; can you say who did what to what, and what happens next, without looking anywhere else on the page?

## Sources read for this file

All under `/Users/aelaguiz/workspace/psagentspace` unless stated.

- `AGENTS.md` (all writing rules and writing-adjacent hard rules)
- `docs/VOICE_GUIDE_PLAYBOOK.md`
- `docs/COACHING_STYLE_GUIDE.md`
- `docs/copy-authoring/README.md`, `docs/copy-authoring/brand-voice-and-vision.md`
- `skills/fc-authored-copy/SKILL.md` and `references/editorial-judgment.md`
- `skills/human-writing/SKILL.md`, `skills/humanizer/SKILL.md`
- `skills/store-review-reply-writing/SKILL.md` and `references/APP_STORE_REVIEW_REPLY_VOICE_GUIDE.md`
- `skills/pokerskill-subreddit-posts/SKILL.md`, `references/voice-and-framing.md`, `references/release-post-log.md`, `references/exemplars-map.md`
- `skills/weekly-ops-report/SKILL.md`, `references/critic-amir.md`, `references/monday-email.md`
- `skills/client-report-narratives/SKILL.md`, `skills/report-pdf-template/SKILL.md`, `skills/pokerskill-report-theme/SKILL.md`
- `research/2026-07-18-amir-ai-expert-x-strategy/amir-draft-verdicts.md` and `amirpc-voice-analysis-2026-07-18.md`
- `research/2026-08-22-coaching-style-guide/worker-corrections-ledger.md`
- `research/2026-08-23-voice-guide-playbook/worker-prime-sessions.md`
- `research/2026-07-18-fc3-ops-accountability-chat/TRANSCRIPT.md`
- `research/2026-07-29-owned-subreddit-decision/POST_LEDGER.md`
- `roadmaps/growth/2026-07-12-community-ua-strategy/LEARNINGS.md`
- `research/2026-08-31-weekly-comms/`, `research/2026-08-24-weekly-comms/`, `research/2026-08-17-weekly-comms/`, `research/2026-08-10-weekly-comms/` (Slack and Telegram exports), `research/2026-08-11-andrew-telegram-backfill/`
- `_artifacts/2026-08-17-monday-update/RECEIPTS.md` and `SENT_EMAIL_2026-08-17.md`
- `roadmaps/company/morning-priorities/README.md`, `runs/2026-09-06.md`, `runs/2026-09-06/sources/github/final-status.json`
- `/Users/aelaguiz/workspace/prime-adhd/rules/ADHD_OUTPUT.md`, `README.md`, `docs/aelaguiz/PRIME_ADHD_ALWAYS_ON_EXTENSION_2026-08-13.md`
- `/Users/aelaguiz/.codex/AGENTS.md`, `/Users/aelaguiz/.claude/CLAUDE.md`
- `/Users/aelaguiz/workspace/arch_skill/AGENTS.md` (Writing And Replies)
- `/Users/aelaguiz/workspace/website/AGENTS.md` (Public copy is for the reader)
- `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/20260906-morning-priorities.txt`
