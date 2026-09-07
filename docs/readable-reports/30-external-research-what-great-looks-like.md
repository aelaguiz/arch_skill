# What great looks like: external research on writing a smart, busy reader can understand at a glance

Purpose: evidence and practice for a skill that will govern how AI agents write status reports, morning priority reports, audits, and summaries for one reader: a CEO who is also the engineer who built most of what the reports describe. This file collects what the research and the best writing cultures say, with worked examples. It does not diagnose the sample report in depth; that is a sibling document.

The trigger, in the reader's words (Amir, 2026-09-06, quoted verbatim from the parent task prompt for this research; session id not available to this worker):

> "I'm looking at this and it says, 'checkout route now, clean, children blocked.' I don't know what the fuck that means. I could parse it if I had to. I could be like, 'Okay we're talking about something about the checkout.' I don't know what we're talking about, but I know there are checkout issues. What's the root? Does it mean the root PR, like children issues, right? It's just fucking confusing, dude, and it's sort of the standard of the writing I get back from these agents."

> "It either treats me like a child or it writes it in a way that requires full concentration to even figure out what the fuck they're saying, right?"

The bar, in his words: "a really smart engineering-focused executive could read this at a glance and understand it without having to drop everything and fully focus on every single fucking word."

The line he was reading is in `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/20260906-morning-priorities.txt` and reads, verbatim: "Checkout root now clean, children blocked." Its source is line 59 of `/Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06.md`. Line 71 of the same file has the second form: "Checkout root #5001 now clean; #5056–#5059 blocked."

Conventions in this file: quotes from sources are verbatim except that dashes inside quoted sentences are replaced with commas or colons (words unchanged). Anything marked "(inference)" is this worker's reasoning, not a source claim. Anything marked "(constructed)" is an example built to a source's rule, not quoted from the source. Full URLs are in the Sources section at the end.

## Findings

1. Smart readers scan before they read, so the first two words of every heading and line must carry the point. In Nielsen Norman Group's studies 79% of users scanned any new page and users read at most 20 to 28% of the words, on samples of above-average intelligence; adding headings to a nine-paragraph message doubled clicks on its lower half (Rogers and Lasky-Fink, n = 46,648). Sources: NN/g "How Users Read on the Web" and "How Little Do Users Read?"; Rogers and Lasky-Fink 2023.

2. Experts prefer plain language more than lay readers do, and the preference rises with education. Trudeau's survey found plain versions chosen by 76.5% of readers without a bachelor's degree, rising to 86% of readers with a law degree; Kimble's surveys of 1,462 judges and lawyers preferred plain versions "by margins running from 80% to 86%". GOV.UK's guidance rule is "Write clearly for specialists too". Sources: GOV.UK "Use clear language" (citing Trudeau 2012); Kimble, "The Straight Skinny on Better Judicial Opinions".

3. Telegraphic compression does not save the reader time and raises ambiguity. Martin 1974 (468 readers) found deleting up to 60% of articles and conjunctions left reading time flat (13.06 versus 13.35 minutes for about 25% fewer words); the ASD-STE100 standard bans it outright: "Do not omit words or use contractions to make your sentences shorter... your sentence will be shorter, but it will not be easier to read"; copy-editing doctrine says "As the word count drops, the likelihood of ambiguity increases". Sources: Martin 1974; ASD-STE100 Issue 9 Rule 4.2; Russial quoted by Zimmer 2010.

4. Working memory holds about four novel chunks, and expertise lifts that limit only for material the reader already owns. So a new label ("checkout root"), an internal code ("#5056"), or an undefined referent ("children") costs an expert as much as it costs anyone. Sources: Cowan 2001; Kirschner, Sweller, Kirschner and Zambrano 2018 ("those limits only apply to novel information and not to familiar information retrieved from long-term memory").

5. A stated cause is read faster and remembered better than a bare verdict. Causal and contrastive connectives ("because", "but") sped reading and improved comprehension in eye-tracking and large-sample studies, and "The direction of the effect did not vary between reading proficiency or readers' educational level"; problem-solution relations are recalled better than lists. A label such as "Aligned; blocked" states two verdicts and no relation. Sources: Kleijn et al. 2019 (n = 794); van Silfhout et al. 2015; Sanders and Noordman 2000.

6. Bullets and label-lines strip out actors and causes; full sentences restore them. Tufte on NASA slides: bullets are "base-touching grunts, which show effects without causes, actions without actors, verbs without subjects, and nouns without predicates." The Columbia accident board found the one number that mattered (debris 640 times larger than the test data) buried at the bottom of a slide whose title said the opposite. Bezos banned slides because narrative "forces better thought and better understanding of what's more important than what, and how things are related" and said bullets in Word "would be just as bad". Sources: Tufte; CAIB Report Vol. 1 p. 191; Bezos 2004 email.

7. Lead with the answer, then the support. The US Army standard defines effective writing as "understood by the reader in a single rapid reading" with the main point first; Minto: "The clearest sequence is always to give the summarizing idea before you give the individual ideas being summarized"; Kimble's lawyers ranked "It has a summary at the beginning" second among reasons to prefer the plain opinion; 262 naval officers read bottom-line-first memos faster with better comprehension. Sources: AR 25-50 (2020) 1-38; Minto via Larson; Kimble; Suchan and Colucci 1989 via Smeltzer 1994.

8. Shorter gets more action even from professionals, and writers cannot predict it. A 49-word email to 7,002 school board members got a 4.8% response against 2.7% for the 127-word version; 93% of people shown both predicted the long one would win. Source: Rogers and Lasky-Fink 2023.

9. Explaining basics to an expert backfires. Cognitive load theory calls it the expertise reversal effect: "Instructional techniques that are highly effective with inexperienced learners can lose their effectiveness and even have negative consequences when used with more experienced learners." NN/g's expert study: "you do not need to explain basic terminology or concepts for experts. In fact, doing so may work against you". Sources: Kalyuga, Ayres, Chandler and Sweller 2003; NN/g "Writing Digital Copy for Domain Experts".

10. Needless complexity makes the writer look less able, and jargon slows readers even when defined. Oppenheimer's five experiments: "needless complexity leads to negative evaluations", mediated by processing fluency; Shulman et al. 2020 (N = 650): jargon "disrupts people's ability to fluently process scientific information, even when definitions for the jargon terms are provided". Sources: Oppenheimer 2006; Shulman et al. 2020.

11. Tables cut load for compare-and-decide tasks when each cell is a complete claim. In a randomized trial with Cochrane methodologists, a summary-of-findings table raised correct answers from 44% to 93% and cut the time to find the main results from 4 minutes to 90 seconds; a later trial's gain came from adding a plain-language "What happens" column. Fragment cells recreate the Columbia slide. Sources: Rosenbaum, Glenton and Oxman 2010; Carrasco-Labra et al. 2016.

12. AI-written summaries have measured failure modes that match this reader's complaint. LLM summaries were nearly five times more likely than human ones to over-generalize (OR = 4.85); instruction-tuned models use nominalizations at 1.5 to 2 times and present-participial clauses at 2 to 5 times the human rate, "a particular informationally dense, noun-heavy style"; expert assessors scored AI summaries 47% against 81% for human ones and called them "waffly, wordy" with "limited ability to pick-up the nuance or context". Sources: Peters and Chin-Yee 2025; Reinhart et al. 2025; ASIC 2024.

## Two failures, one cause

The reader named two opposite failures: writing that "requires full concentration" and writing that "treats me like a child". Cognitive load theory names both. Extraneous load is load caused by how information is presented, and it is the writer's to remove. Its two best-documented forms are the split-attention effect (the reader must combine two sources to understand one thing) and the redundancy effect (the reader is given the same information again in another form, or information they already own). Telegraphic label-writing produces split attention: the reader must fetch the missing subject, verb, and relation from memory or from another document. Over-explanation produces redundancy. (Mapping of the two effects onto the two failures is inference; the effects themselves are from Sweller, van Merrienboer and Paas 1998 as quoted by NSW CESE 2017.)

Pinker gives the common root: the curse of knowledge. "It simply doesn't occur to them that their readers don't know what they know." His mechanism is chunking: "An adult mind that is brimming with chunks is a powerful engine of reason, but it comes at a cost: a failure to communicate with other minds that have not mastered the same chunks. The amount of abstraction a writer can get away with depends on the expertise of his readership." An agent that has spent an hour inside pull-request stacks has chunked "checkout root" and "children"; the reader opening the report at breakfast has not. The same blind spot, pointed the other way, produces the tutorial paragraph about what a pull request is. (Application to agents is inference.)

The practical split that follows from findings 4 and 9: domain terms the reader owns (CI, pull request, p95, attribution) are free; project-specific names, internal codes, and yesterday's referents are not, and must be named in passing on first use. Never explain the field; always name the thing.

## Mechanisms of cognitive burden

Each row: the mechanism, why it costs, the evidence, a before example, an after example. Before examples marked "(sample)" are verbatim from the sample morning report at `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/20260906-morning-priorities.txt`. Rewrites are constructed to the cited rule.

| Mechanism | Why it costs | Evidence | Before | After |
|---|---|---|---|---|
| Telegraphic ellipsis: dropped articles, subjects, verbs, and connectives | The reader must reconstruct the sentence before reading it; the omitted words are the ones that fix who did what; ambiguity rises as words drop; reading time does not fall. | ASD-STE100 Rule 4.2: "Do not omit verbs because the reader will not understand the action... Do not omit the subject... omitted articles can cause ambiguity"; Martin 1974 (reading time flat with 25% fewer words); Zimmer 2010 on crash blossoms ("As the word count drops, the likelihood of ambiguity increases"). | (sample) "Checkout root now clean, children blocked." | "The base pull request of the checkout repair stack (psmobile #5001) passed review and CI. The four pull requests stacked on top of it (#5056 to #5059) cannot merge until #5001 merges." |
| Noun stacks and ad-hoc compounds | Each adjacent noun pair forces the reader to pick a relation; ad-hoc compounds have no stored relation, so the reader computes one per pair and guesses the grouping. | Gagne and Shoben 1997 (relation selection); Schmidtke et al. 2016 (more competing relations, slower recognition); plainlanguage.gov: "Once you get past three, the string becomes unbearable"; ASD-STE100 Rule 2.1 (multi-word nouns of no more than three words). | (sample) "purchase-terminal repair merged" and "Home/report-card metrics" | "The repair to the purchase terminal screen is merged." and "the metrics for the Home tab report cards" |
| Undefined referents and anaphora without an antecedent | Every definite reference makes the reader search for what it points to; when the antecedent is only implied the reader must build a bridge (about 180 ms per sentence in the lab); when there is nothing to bridge from, the sentence fails silently. | Haviland and Clark 1974 (835 ms with a direct antecedent, 1016 ms without); Clark and Haviland's Maxim of Antecedence: "one and only direct antecedent for any given information". | (sample) "children blocked" (no earlier mention of children, stack, or base) | "The four pull requests stacked on top of #5001 cannot merge until it merges." |
| Status label without mechanism | A verdict ("Aligned", "blocked", "Amber") gives the reader a conclusion with no relation to attach it to; relations are what is processed faster and remembered; bare colors invite optimistic bias. | Kleijn et al. 2019; van Silfhout et al. 2015; Sanders and Noordman 2000; Iacovou et al. 2009 (optimistic biasing degrades status reports, 561 project managers); Amazon defines each status color in writing. | (sample) "Aligned; finish delivery." and "Aligned; event delivery blocked." | "This work matches the acquisition priority. Next: merge #5001 so the stacked fixes can merge, then build the release candidate." and "Natasha's lifecycle work matches the LTV priority. It is blocked because the events her journeys depend on have not been delivered; the backend agent and Natasha own that handoff." |
| Nominalization (hidden verbs, "zombie nouns") | Turning the verb into a noun deletes the actor and adds a weak verb; the reader must re-derive who did what. | Pinker 2014 ("embalms it into a lifeless noun"); Sword 2012 (nominalized sentences "fail to tell us who is doing what"); plainlanguage.gov "avoid hidden verbs". | "Completion of the token rotation resulted in restoration of API access." (constructed) | "We rotated the token, so API access works again." |
| Agentless passive | Readers use a first-noun-is-agent heuristic; passives are misread 15% of the time by adult native speakers, and an agentless passive gives the heuristic nothing to work with. | Ferreira 2003 (96% correct on actives, 85% on passives, 74% on implausible passives); AR 25-50 1-38b names active voice as one of two essentials. | "The release was blocked." (constructed) | "Sentry blocked the release because the crash rate crossed 1%." |
| Hedge stacks and vague quantity words | Hedges lower perceived authority and hide magnitude; "significant" carried five different meanings on one NASA slide, from "detectable" to "everyone dies". | Pinker 2014 ("their hedging is a choice, not a tic"; give "the magnitude of the effect and the degree of certainty explicitly"); Tufte in CAIB p. 191 on "significant"; Hosman 1989. | "Latency seems to be somewhat improved, possibly." (constructed) | "Median latency fell from 420 ms to 310 ms in one run. I have not repeated the run yet." |
| Abbreviations, internal codes, and bare IDs | Each one is a lookup; even experts in their own field defined only 32% of the abbreviations in their own charts; 79% of acronyms in 24 million paper titles appeared fewer than 10 times. | Jayatilake et al. 2023; Barnett and Doubleday 2020; Brunetti et al. 2007 (4.7% of 643,151 medication errors from abbreviations); Pinker: "the few seconds they add to their own lives come at the cost of many minutes stolen from their readers". | (sample) "#4792/#4807 open at 15:40, same code since September 2" | "The two lifecycle pull requests (#4792 and #4807) are still open and have not changed since September 2." |
| Arrows and symbols standing in for words | An arrow or slash leaves the relation unstated (causes? then? becomes? or?), so the reader supplies it; connectives are exactly what the reading studies show helps. | Kleijn et al. 2019 and van Silfhout et al. 2015 on connectives (application to arrows is inference; no controlled study on arrows in prose was found). | (sample) "Profitable acquisition → campaign and signal recovery" and "Home/report cards" | "Profitable acquisition, through campaign and signal recovery" and "the Home tab and its report cards" |
| Mixed units, clocks, and time zones | The reader converts in their head; conversion is a second source to combine (split attention); missing units are Tufte's "dequantification". | Split-attention effect (Sweller 1998 via NSW CESE 2017); Tufte on "a general absence of units of measurement". (Application to time zones is inference.) | (sample) "Main reads: September 6, 09:51–10:05 Chicago" in the summary, while "Refresh timestamps in this detailed table are UTC" and "#4792/#4807 open at 15:40" with no zone | One clock for the whole report, stated once: "All times are Chicago." |
| Buried lead and process narcissism | The reader wants the world, not the writer's day; describing your process before your result is Pinker's "professional narcissism" and the Economist's "clearing your throat". | Pinker 2014; Economist Style Guide ("Do not spend several sentences clearing your throat, setting the scene or sketching in the background"); Minto; AR 25-50 BLUF. | (sample) The report opens with a six-step table of the agent's own process ("1 · Refresh... Pull Telegram, Slack, GP...") before any priority. | Open with the one-paragraph answer: what changed, what needs a decision, what is next. Move the method to an appendix. |
| Elegant variation and drifting names | Renaming one thing ("worktree", "child", "subprocess") reads as a different thing; consistent terms let the reader chunk. | ASD-STE100 Rule 6.2 ("do not change them in your text") and Rule 1.11; Wikipedia "Signs of AI writing" on synonym-swapping from repetition penalties. | "The search service... the retrieval layer... the query subsystem..." for one component (constructed) | Use one name, "the search service", every time. |
| Over-compression of compound facts | Merging several claims into one short line drops the qualifier that made a claim true. | Apple Intelligence notification summaries (BBC, December 2024: a merged summary falsely said a suspect "had shot himself"); Peters and Chin-Yee 2025 (LLM summaries over-generalize about five times more often). | "Auth migration done, rollback tested, incidents zero." (constructed) | "Auth migration is done for the web app. Rollback was tested on staging only. There were no incidents in the 48 hours since." |
| Over-explanation and tutorial tone | Explaining what the expert already owns is redundant load and a signal that the text is not for them. | Kalyuga et al. 2003 (expertise reversal); NN/g domain experts study ("doing so may work against you"); Economist ("Do not be too didactic"). | "A pull request, or PR, is a proposal to merge code into the main branch. Our PR #412 has passed CI, which is the automated test suite, and is ready." (constructed) | "Pull request #412 passed CI and is ready to merge." |
| Fragment cells in tables and bold-header bullet lists | A grid of fragments is the Columbia slide again: hierarchy without sentences; the trial gain for tables came from adding a sentence-like "What happens" cell. | CAIB p. 191 ("These levels prioritized information that was already contained in 11 simple sentences"); Carrasco-Labra et al. 2016; Wikipedia "Signs of AI writing" on inline-header lists. | "- Status: on track. - Risk: medium. - Next: continue." (constructed) | "The API rewrite is on track for May 3. The one risk is the vendor SDK; if their fix slips past Friday we lose a week." |
| Headings that name a topic instead of stating the message | Scanners see about two words per line; a topic heading gives them nothing to act on. | NN/g "First 2 Words" (35% of tested links could not be understood from their first 11 characters); GOV.UK headings must be "frontloaded" and "removable"; Zelazny and Cracked It!: "A message title is like a headline in a magazine, not an item in a table of contents." | (sample) "Where everyone’s work stands" | "Two blocks need attention: lifecycle events and the checkout stack" |

## What great looks like

Eight short passages, quoted from the sources or built to their rules, each with the technique it shows.

1. Summary first, decision then cause. Kimble's rewrite of a judicial opinion opens: "Summary: Robert Wills was injured when someone drove by him and fired shots toward his car... We disagree and reverse. We do not find a substantial physical nexus between the two cars, because the bullets were not projected by the unidentified car itself." The original opened with procedural history. Technique: the first word is "Summary", the decision comes before the reasoning, and the reason is attached with "because". Of the 251 lawyers who responded, 61% preferred the rewrite, and "It has a summary at the beginning" was their second most chosen reason. (Kimble, "The Straight Skinny on Better Judicial Opinions".)

2. The reader's stake in the first sentence. The US Army's own example of its standard: "The time you spent in training last year entitles you to jump pay." Technique: 13 words, active voice, the actor and the consequence for the reader both present, nothing to decode. AR 25-50 pairs this with two numbers worth keeping as ceilings, not targets: sentences averaging about 15 words and paragraphs of no more than 10 lines. (AR 25-50, 2020, 1-38b and 1-39b.)

3. One line that stands alone. Google's rule for the first line of a change description: "a complete sentence, written as though it were an order" that "should stand alone, allowing readers to skim". Its good example: "RPC: Remove size limit on RPC server message freelist." followed by one sentence on why. Its bad examples: "Fix bug", "Fix build", "Phase 1". Technique: subject, verb, object, and scope in one sentence; the why on the next line. This is the pattern for every status line. (Google Engineering Practices, "Writing good CL descriptions".)

4. Mechanism, not label. Google's example postmortem states the root cause as a sentence, not a category: "Cascading failure due to combination of exceptionally high load and a resource leak when searches failed due to terms not being in the Shakespeare corpus. The newly discovered sonnet used a word that had never before appeared in one of Shakespeare's works, which happened to be the term users searched for." Its action items carry an owner, a tracking bug, a state, and "a verifiable end state (e.g., 'Add an alert when more than X% of our machines have been taken away from us')". The SRE Workbook's list of what makes a postmortem bad is the same list of what makes a status line bad: missing context, summaries without numbers, and vague verbs like "Improve" and "Make better". (Google SRE Book, example postmortem; SRE Workbook, postmortem culture.)

5. Magnitude and certainty instead of hedges. Pinker's model sentence: "During the 20th century, democracies were half as likely to go to war with one another as autocracies were." Technique: the size of the effect ("half as likely") and its scope ("20th century", "with one another") are in the sentence, so no "somewhat", "arguably", or "may" is needed. "It's not that good writers never hedge their claims. It's that their hedging is a choice, not a tic." (Pinker, "Why Academics Stink at Writing".)

6. The headline states the finding that changes the decision. The Boeing slide shown to NASA managers during Columbia's flight was titled "Review of Test Data Indicates Conservatism for Tile Penetration"; the fact that the debris was 640 times larger than anything in the test data sat in the last sub-bullet. Tufte's replacement headline: "Review of Test Data Indicates Irrelevance of Two Models". Technique: put the number that changes the decision, or its consequence, in the first line, and never let a reassuring word describe the model when the reader will read it as describing the risk. (CAIB Report Vol. 1, p. 191.)

7. Number, consequence, full sentences. Axios's own example of Smart Brevity done right: "We stunned the Board of Directors Wednesday with our 12% Q3 revenue jump, which puts us 90% to goal for H2. Why it matters: Higher revenue than ever means we can invest in growth areas that will speed up our go-to-market plan by months." Technique: the first sentence carries the number and its meaning; the "why it matters" is one sentence naming the consequence. What to keep from Smart Brevity is this example. What to drop is its word caps ("six or fewer strong words", "Keep words to one syllable when possible"), which the New Yorker and corporate critics found produce exactly the fragments and lost context this reader complains about. For this reader, "why it matters" should be a clause, not a paragraph (inference). (Axios HQ; Malone, New Yorker 2022.)

8. All items visible, prose only for exceptions, unknown allowed. Amazon's Weekly Business Review shows every metric; for routine variation the owner says "nothing to see here", and for an exception the owner either explains it or says they do not know and are investigating, with a follow-up recorded. Built to that pattern (constructed): "Deploy success rate 98.7%, normal variation, nothing to report." and "p95 latency is up 40% since Tuesday. Cause unknown; Dana is investigating and will report Friday." Technique: the reader can trust silence, and an honest unknown is written as a sentence with an owner and a date instead of a color. (Bryar and Carr, Working Backwards, via Commoncog.)

### The sample row, rewritten to these rules

The row for Amir in the sample report reads, verbatim: "Comparison worksheets delivered; repair stacks moving. Checkout root now clean, children blocked. Aligned; finish delivery." Rewritten with the facts supplied for this task and the sample's own timestamps (constructed):

> Amir: purchase and attribution repairs (acquisition priority). The comparison worksheets are delivered. The base pull request of the checkout repair stack (psmobile #5001) passed review and CI as of the 10:40 Chicago check. The four pull requests stacked on top of it (#5056 to #5059) cannot merge until #5001 merges. This work matches the priority. Next: merge #5001, merge the four stacked fixes, then build the release candidate that contains them.

What changed: every noun has an article, every clause has a verb, the two internal codes are named in plain English on first use, "children" became "the four pull requests stacked on top of it", "blocked" became "cannot merge until #5001 merges", "Aligned" became "matches the priority", and the next action is a sentence with an object. It is 71 words against the original 15, and it can be read once.

## Principles that survive contact with a smart reader

### Rules that hold for expert readers, with the evidence

1. Answer first; the reader can stop at any line and still have the point. Minto ("a reader, no matter how intelligent he is, has only a limited amount of mental energy"); AR 25-50; Kimble's lawyers; Suchan and Colucci's naval officers; Will Larson: "Particularly when writing for executives, I've found that it's most useful to state your conclusion immediately, which allows folks who agree with your conclusion to stop reading."
2. Every status line is a complete sentence with an actor, a verb, and, where there is a state, a cause. ASD-STE100 Rule 4.2; Google's stand-alone first line; Tufte's "grunts"; CAIB naming "sentence fragments, passive voice, multiple meanings of 'significant'" as the failure for senior NASA managers. Rogers and Lasky-Fink, who argue for fewer words, still say "Proper grammar and punctuation, full sentences, and appropriate word choice are almost always useful."
3. Name things once, consistently, and never as a bare code. Define a project-specific name in passing on first use ("the base pull request of the checkout repair stack (psmobile #5001)"), then reuse the same words. ASD-STE100 Rules 1.11 and 6.2; Economist on abbreviations ("you will end up irritating readers rather than informing them"); Jayatilake 2023.
4. Give the cause or write "unknown", never a verdict alone. Connective studies (Kleijn 2019; van Silfhout 2015); Amazon WBR; SRE Workbook ("a well-informed estimate is better than no data at all").
5. Keep numbers, units, exact dates, and one clock. Experts want data and "can see through hype" (NN/g); Tufte on dequantification; NN/g "objective" language alone improved usability 27%.
6. Short sentences as a ceiling, not a count: about 25 words (GOV.UK, ASD-STE100), 15 to 20 for expert web readers (NN/g), one idea each. Rogers refused a hard cap on the record; Orwell's Ecclesiastes test shows a 38-word parody carrying less meaning than the 49-word original. Measure clarity, not words.
7. Structure for scanning: headings that state the message in their first two words, priority order, one bolded line per section at most. NN/g "First 2 Words"; GOV.UK headings "frontloaded" and "removable"; Rogers (headings doubled clicks on the lower half; bolding one line makes nearly everyone read it, bolding many cancels it); AR 25-50 1-32 ("Do not overuse this method for emphasis").
8. Cut what the reader does not need for the decision, starting with the writer's own process. Kimble's top reason for preferring the plain version was "It leaves out a lot of unnecessary detail"; Pinker's "professional narcissism"; Economist "clearing your throat"; Rogers "Include fewer ideas".
9. State what changed since last time, what is next, and who owns it. Orosz's weekly emails ("Risks and delays would explicitly be called out, along with plans to mitigate"); SRE action items with owner and verifiable end state; Basecamp: status is "what's unknown and what's solved", not task counts.
10. Keep the domain terms the reader owns; explain them nowhere. NN/g: shared vocabulary is a shortcut and is more precise; Kimble: "use a longer, less familiar word if you think it's more precise or accurate"; Orwell's rule v bans jargon only "if you can think of an everyday English equivalent".
11. Narrative when relations matter, a table when comparison matters, and sentences in both. Bezos on bullets; Cochrane trials on tables with claim-like cells; NN/g data-tables tasks (find, compare, act).

### Rules that apply mainly to lay readers, or reverse for experts

1. Reading-grade targets and vocabulary simplification. NN/g moves the target from 6th to 8th grade (public) to 10th to 12th grade (experts) and no further; a 30,000-headline field experiment found the public preferred simpler headlines but "a sample of professional writers, including journalists, did not show this pattern". For this reader the transferable rules are structural (verb present, actor present, relation present, referent defined), not lexical (inference).
2. Defining core terms, tutorial background, and "as you may recall". Expertise reversal (Kalyuga 2003); NN/g's oceanographer: "This is for the general public, I don't need that"; Shakespeare experts given line-by-line explanations reported higher load because they "were unable to avoid cross-checking the accuracy and validity of the explanations" (Oksa et al. 2010, via Kalyuga).
3. Previews, restated summaries, and metadiscourse. Pinker: metadiscourse "is there to help the writer, not the reader"; GOV.UK: "Do not repeat the summary in the first paragraph."
4. "Why it matters" as a paragraph. For a newsletter reader it supplies missing context; for this reader it is one clause naming the consequence or the decision, or it becomes the condescension failure (inference from the Smart Brevity critiques).
5. Word and syllable caps. Axios's six-word teases and one-syllable preference, and any rule that makes writers drop verbs and articles, produce the label-writing failure. Keep the ceilings in rule 6 above and nothing tighter.
6. "Let the expert fill the gaps." The reverse cohesion effect (high-knowledge readers learning more from low-cohesion text) held only for less-skilled, high-knowledge readers (O'Reilly and McNamara 2007; Gouravajhala et al. 2025), and all of those studies measure learning from a text studied with full attention. A morning report is read for decisions without full attention, which is the opposite condition (inference).

## Gaps in the evidence

- No controlled study tests telegraphic fragments against full sentences on expert readers. The closest evidence is Martin 1974 (students), ASD-STE100's rule and reasons, and the Columbia case.
- No study tests fragment cells against sentence cells in status tables; the Cochrane "What happens" column is the nearest.
- No study measures executives reading AI-written status reports or dashboards. ASIC's assessors were regulators reading AI summaries of public submissions; Peters and Chin-Yee measured science summaries.
- Sentence-length comprehension percentages often quoted with GOV.UK's 25-word rule (about 90% understood at 14 words, under 10% at 43) are second-hand from the American Press Institute via Ann Wylie; the primary study was not found.
- Trudeau's education gradient was read from the Michigan Bar Journal's report of his data, not the SSRN paper (blocked). Oppenheimer's raters were undergraduates, not executives.
- Suchan and Colucci 1989 and Vessey 1991 were verified from a meta-analysis and abstracts, not full text.
- Amazon's "so what" test, the "under 30 words" rule, and the weasel-word list circulate as social posts; no Amazon primary source was found. The Working Backwards passages and the 2004 and 2017 Bezos texts are sourced.

## Sources

Cognitive science of reading

- Sweller 1988, "Cognitive load during problem solving", original paper: https://mrbartonmaths.com/resourcesnew/8.%20Research/Explicit%20Instruction/Cognitive%20Load%20during%20problem%20solving.pdf
- Sweller, van Merrienboer and Paas 2019, "Cognitive architecture and instructional design: 20 years later", abstract: https://cris.maastrichtuniversity.nl/en/publications/cognitive-architecture-and-instructional-design-20years-later
- Kirschner, Sweller, Kirschner and Zambrano 2018, cognitive load theory principles (open access; novel versus familiar information): https://pmc.ncbi.nlm.nih.gov/articles/PMC6435105/
- NSW CESE 2017 review of cognitive load theory, quoting Sweller 1998 on split attention and redundancy: https://education.nsw.gov.au/content/dam/main-education/about-us/educational-data/cese/2017-cognitive-load-theory.pdf
- Cowan 2001, working memory limit of about four chunks: https://pubmed.ncbi.nlm.nih.gov/11515286/
- Miller 1956, "The magical number seven", full text: http://www.musanim.com/miller1956/
- Kalyuga, Ayres, Chandler and Sweller 2003, the expertise reversal effect: https://doi.org/10.1207/S15326985EP3801_4
- Kalyuga's own summary of expertise reversal (includes Oksa et al. 2010 Shakespeare study): https://my.chartered.college/impact_article/expertise-reversal-effect-and-its-instructional-implications/
- Martin 1974, telegraphic prose deletion experiments, full report: https://files.eric.ed.gov/fulltext/ED098932.pdf
- Zimmer 2010, "Crash Blossoms", New York Times (Wayback copy): https://web.archive.org/web/2020/https://www.nytimes.com/2010/01/31/magazine/31FOB-onlanguage-t.html
- Zimmer 2009, Language Log on headline garden paths: https://languagelog.ldc.upenn.edu/nll/?p=1693
- Christianson et al. 2001, garden-path misreadings persist: https://pubmed.ncbi.nlm.nih.gov/11368528/
- Slattery et al. 2013, lingering misinterpretations, eye tracking: https://eprints.bournemouth.ac.uk/22639/3/SlatteryetalJML3final.docx.pdf
- Ferreira 2003, passives misinterpreted by adults, full paper: https://tallinzen.net/media/readings/ferreira_2003.pdf
- Clark and Haviland 1977, the given-new contract and bridging cost: http://www.web.stanford.edu/~clark/1970s/Clark,%20H.H.%20_%20Haviland,%20S.E.%20_Comprehension%20and%20the%20given-new%20contract_%201977.pdf
- Gagne and Shoben 1997, relation selection in noun compounds: https://doi.org/10.1037/0278-7393.23.1.71
- Schmidtke, Kuperman, Gagne and Spalding 2016, relational competition slows compounds: https://doi.org/10.3758/s13423-015-0926-0
- van Silfhout, Evers-Vermeul and Sanders 2015, connectives as processing signals: https://research-portal.uu.nl/en/publications/connectives-as-processing-signals-how-students-benefit-in-process/
- Kleijn et al. 2019, connectives and comprehension across 794 readers: https://doi.org/10.1080/0163853x.2019.1605257
- Sanders and Noordman 2000, coherence relations and recall: https://doi.org/10.1207/s15326950dp2901_3
- Marchal et al. 2025, connectives across relations and languages: https://www.frontiersin.org/journals/language-sciences/articles/10.3389/flang.2025.1721510/full
- McNamara et al. 1996, reverse cohesion effect: https://asu.elsevierpure.com/en/publications/are-good-texts-always-better-interactions-of-text-coherence-backg/
- O'Reilly and McNamara 2007, reversing the reverse cohesion effect: https://doi.org/10.1080/01638530709336895
- Gouravajhala et al. 2025, low cohesion is not a desirable difficulty: https://doi.org/10.1016/j.lindif.2025.102720
- Science Advances 2024, readers prefer simpler headlines, professional writers do not: https://doi.org/10.1126/sciadv.adn2555
- Hosman 1989, hedges lower perceived authority: https://doi.org/10.1111/j.1468-2958.1989.tb00190.x
- Barnett and Doubleday 2020, growth of acronyms in science, eLife: https://elifesciences.org/articles/60080
- Brunetti, Santell and Hicks 2007, abbreviations and medication errors: https://www.qualityhealth.org/downloads/wpsc/Brunetti_JCJQPS_2007.pdf
- Jayatilake et al. 2023, clinicians define 32% of chart abbreviations: https://pubmed.ncbi.nlm.nih.gov/37674765/
- Bullock et al. 2019, jargon impairs processing: https://pubmed.ncbi.nlm.nih.gov/31354058/
- Shulman et al. 2020, jargon hurts fluency even when defined: https://doi.org/10.1177/0261927x20902177
- Oppenheimer 2006, "Consequences of Erudite Vernacular Utilized Irrespective of Necessity", full text: https://emilkirkegaard.dk/en/wp-content/uploads/Consequences-of-Erudite-Vernacular-Utilized-Irrespective-of-Necessity-Problems-with-Using-Long-Words-Needlessly.pdf
- Martinez and Mammola 2021, jargon in titles and abstracts reduces citations: https://pubmed.ncbi.nlm.nih.gov/33823673/

Pinker, Sword, Orwell, Strunk

- Pinker 2014, "Why Academics Stink at Writing", Chronicle of Higher Education: https://www.chronicle.com/article/why-academics-stink-at-writing/ (PDF reprint: https://chronicle.brightspotcdn.com/08/6f/ac1fe70fb853dc70e254f7303c60/chronfocus-academicwriting-i.pdf)
- Sword 2012, "Zombie Nouns", New York Times: https://archive.nytimes.com/opinionator.blogs.nytimes.com/2012/07/23/zombie-nouns/
- Orwell 1946, "Politics and the English Language": https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/politics-and-the-english-language/
- Strunk 1920, The Elements of Style, Project Gutenberg: https://www.gutenberg.org/files/37134/37134-h/37134-h.htm
- Pullum 2009, "50 Years of Stupid Grammar Advice": https://www.chronicle.com/article/50-years-of-stupid-grammar-advice/

Plain-language standards and expert-reader evidence

- Plain Writing Act of 2010, definition: https://digital.gov/resources/plain-writing-act
- Federal plain language principles ("dumb down" myth): https://digital.gov/guides/plain-language/principles
- Federal plain language style (noun strings, abbreviations): https://digital.gov/guides/plain-language/writing/style
- Archived plainlanguage.gov guidelines (audience, short sentences, paragraphs, main idea first, topic sentences, jargon, noun strings, hidden verbs, definitions, lists, tables): https://raw.githubusercontent.com/GSA/plainlanguage.gov/main/_pages/guidelines/audience/index.md and sibling pages under https://raw.githubusercontent.com/GSA/plainlanguage.gov/main/_pages/guidelines/
- OPM plain language page (15 to 20 word average, complete sentences, not talking down): https://www.opm.gov/information-management/plain-language/
- GOV.UK "Use clear language" (25 words, 5 sentences, write clearly for specialists too): https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/
- GOV.UK "Create a clear structure" (frontloading, headings, 20 to 28% read): https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-structure/
- GOV.UK A to Z style guide (words to avoid, bullets, numbers): https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/
- GDS 2014, "Sentence length: why 25 words is our limit": https://insidegovuk.blog.gov.uk/2014/08/04/sentence-length-why-25-words-is-our-limit/
- GDS 2014, Mark Morris, "Clarity is king" (reports Trudeau and Ipsos MORI): https://gds.blog.gov.uk/2014/02/17/guest-post-clarity-is-king-the-evidence-that-reveals-the-desperate-need-to-re-think-the-way-we-write/
- Trudeau 2012, "The Public Speaks", SSRN (blocked to this worker): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1843415
- Michigan Bar Journal report of Trudeau's education gradient: https://www.michbar.org/journal/Details/A-legal-writing-carol?ArticleID=5210
- Kimble, "The Straight Skinny on Better Judicial Opinions" (judges and lawyers studies): https://scribes.org/wp-content/uploads/2022/12/Scribes_vol9_04_The_Straight_Skinny.pdf
- Kimble 2024 column on precision and sentence length: https://www.michbar.org/journal/Details/Flimsy-claims-for-legalese-and-false-criticisms-of-plain-language-A-30-year-collection-Part-2?ArticleID=4989
- Bernoff 2016, HBR survey of 547 business readers (reprint): https://www.conference-board.org/research/human-capital-briefs/blg-00-1-5321
- ASD-STE100 Simplified Technical English, Issue 9 (2025), full standard: https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf (site: https://www.asd-ste100.org/)

Nielsen Norman Group

- "How Users Read on the Web" (1997; 79% scan; 124% usability experiment): https://www.nngroup.com/articles/how-users-read-on-the-web/
- "How Little Do Users Read?" (2008; 20 to 28% of words): https://www.nngroup.com/articles/how-little-do-users-read/
- "F-Shaped Pattern: Misunderstood, But Still Relevant" (2017): https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/
- "First 2 Words: A Signal for the Scanning Eye" (2009): https://www.nngroup.com/articles/first-2-words-a-signal-for-scanning/
- "Inverted Pyramid" (2018): https://www.nngroup.com/articles/inverted-pyramid/
- "How People Read Online: New and Old Findings" (2020): https://www.nngroup.com/articles/how-people-read-online/
- "Chunking" (2016): https://www.nngroup.com/articles/chunking/
- "Plain Language Is for Everyone, Even Experts" (2017): https://www.nngroup.com/articles/plain-language-experts/
- "Writing Digital Copy for Domain Experts" (2017): https://www.nngroup.com/articles/writing-domain-experts/
- "Data Tables" (four user tasks): https://www.nngroup.com/articles/data-tables/

Writing for Busy Readers (Rogers and Lasky-Fink)

- Official six-principles checklist: https://writingforbusyreaders.com/wp-content/uploads/2023/10/Writing-for-Busy-Readers-Checklist.pdf
- Behavioral Scientist excerpt (school board email experiment): https://behavioralscientist.org/when-writing-for-busy-readers-less-is-more/
- Next Big Idea Club (headings experiment, n = 46,648): https://nextbigideaclub.com/magazine/writing-busy-readers-communicate-effectively-real-world-bookbite/45483/
- Book introduction excerpt ("full sentences... almost always useful"): https://penguinrandomhousehighereducation.com/2023/09/20/writing-for-busy-readers-excerpt/
- Annie Duke Q&A with Rogers (93% prediction failure, bolding tradeoff): https://www.annieduke.com/qa-with-todd-rogers-harvard-behavioral-scientist-and-coauthor-of-writing-for-busy-readers-communicate-more-effectively-in-the-real-world/
- Rogers podcast transcript (no hard caps; highlighting experiments): https://awesomeatyourjob.com/916-six-principles-for-writing-to-busy-readers-with-todd-rogers/
- Lasky-Fink, Robinson, Chang and Rogers 2021, truancy notices RCT (N = 131,312): https://edworkingpapers.com/sites/default/files/Improving%20School%20Administrative%20Communications-Final%28Mar2021%29.pdf
- Bergman, Lasky-Fink and Rogers 2020, decision makers misjudge friction: https://ideas.repec.org/a/eee/jobhdp/v158y2020icp66-79.html

Executive writing systems

- US Army AR 25-50 (10 October 2020), Section IV Army writing style: https://www.maine.gov/dvem/policies/documents/AR%2025-50%20(10%20October%202020).pdf (2013 edition: https://corpslakes.erdc.dren.mil/employees/pdfs/AR25-50.pdf)
- Barbara Minto, official site: https://www.barbaraminto.com/
- Will Larson's notes on The Pyramid Principle, with direct quotes: https://lethain.com/pyramid-principle/
- StrategyU review of Minto, with evidence critique: https://strategyu.co/pyramid-principle-partone/
- Bezos 2004 email banning PowerPoint (reproductions): https://alexnixon.github.io/2019/12/10/writing.html and https://www.worldbuilders.ai/p/welcome-jungle
- Bezos 2017 shareholder letter (six-page narratives): https://www.aboutamazon.com/news/company-news/2017-letter-to-shareholders
- Working Backwards passages on six-pagers: https://manassaloi.com/booksummaries/2022/06/24/working-backwards-bryar-carr.html
- Amazon Weekly Business Review mechanics (Commoncog, citing Working Backwards): https://commoncog.com/the-amazon-weekly-business-review/
- Brad Porter 2015, "The Beauty of Amazon's 6-Pager": https://www.linkedin.com/pulse/beauty-amazons-6-pager-brad-porter
- Axios HQ, Smart Brevity official description and example: https://www.axioshq.com/smart-brevity
- Chapter notes quoting Smart Brevity: https://www.mickmel.com/notes-from-smart-brevity-from-jim-vandehei-mike-allen-and-roy-schwartz/
- Malone 2022, "The Dubious Wisdom of Smart Brevity", New Yorker: https://www.newyorker.com/news/annals-of-communications/the-dubious-wisdom-of-smart-brevity
- Swenson 2024, critique of Smart Brevity in corporate communications: https://shannonswenson.com/2024/11/a-critique-of-smart-brevity-in-corporate-communications/
- Francescato 2023, "When brevity isn't smart": https://flowerchild.substack.com/p/when-brevity-isnt-smart
- McKinsey dot-dash storyline: http://workingwithmckinsey.blogspot.com/2013/07/McKinsey-storyline-dot-dash.html
- Cracked It! (Garrette, Phelps, Sibony) on action titles: https://principus.si/2022/02/13/bernard-garrete-corvey-phelps-olivier-sibony-cracked-it/
- The Economist Style Guide, 2015 edition (introduction): https://moodle2.units.it/pluginfile.php/395439/mod_folder/content/0/Economist_Style_Guide_2015.pdf?forcedownload=1 (short-words entry quoted at https://christopherberry.ca/the-economist-style-guide/)

Engineering organizations, tables, status

- CAIB Report Vol. 1, Part 2 (PowerPoint slide analysis, p. 191): https://s3.amazonaws.com/akamai.netstorage/anon.nasa-global/CAIB/CAIB_medres_part2.pdf
- Tufte, "PowerPoint does rocket science" (bullets as grunts; summary matrix advice): https://www.edwardtufte.com/notebook/powerpoint-does-rocket-science-and-better-techniques-for-technical-reports/
- Tufte, rhetorical ploys in evidence presentations: https://www.edwardtufte.com/notebook/rhetorical-ploys-in-evidence-presentations/
- Tufte on tables (Visual Display p. 178, page-cited excerpt): https://qahiccupps.blogspot.com/2018/08/tufte-visual-display-of-quantitative.html
- Google Engineering Practices, writing good CL descriptions: https://google.github.io/eng-practices/review/developer/cl-descriptions.html
- Google Technical Writing One, documents (scope, main points first): https://developers.google.com/tech-writing/one/documents
- Malte Ubl, "Design Docs at Google": https://www.industrialempathy.com/posts/design-docs-at-google/
- Google SRE Book, example postmortem: https://sre.google/sre-book/example-postmortem/
- Google SRE Workbook, postmortem culture (good versus bad postmortems): https://sre.google/workbook/postmortem-culture/
- Stripe writing culture interview (Collison's footnoted emails): https://slab.com/blog/stripe-writing-culture/
- Wolfson, "What I miss about working at Stripe": https://every.to/p/what-i-miss-about-working-at-stripe
- 37signals, "How we communicate" (heartbeats, kickoffs): https://basecamp.com/guides/how-we-communicate
- Shape Up chapter 13, "Show Progress": https://basecamp.com/shapeup/3.4-chapter-13
- Will Larson, "Presenting to executives": https://lethain.com/present-to-executives/
- Gergely Orosz, weekly written status emails: https://blog.pragmaticengineer.com/a-team-where-everyone-is-a-leader/
- Smeltzer 1994 meta-analysis reporting Suchan and Colucci 1989 (naval officers): https://core.ac.uk/download/36739120.pdf
- Rosenbaum, Glenton and Oxman 2010, summary-of-findings table RCT: https://pubmed.ncbi.nlm.nih.gov/20434024/
- Carrasco-Labra et al. 2016, improved table format RCT: https://pubmed.ncbi.nlm.nih.gov/26791430/ (protocol describing the "What happens" column: https://link.springer.com/article/10.1186/s13063-015-0649-6)
- Vessey 1991, cognitive fit theory: https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-5915.1991.tb00344.x
- GOV.UK Design System, table component: https://design-system.service.gov.uk/components/table/
- Iacovou, Thompson and Smith 2009, selective status reporting, MIS Quarterly: https://aisel.aisnet.org/misq/vol33/iss4/11/
- Chabik, "Fifty Shades of Green", IEEE Software (abstract): https://csdl.computer.org/csdl/magazine/so/5555/01/11036548/27vOW8ccawU

AI-generated text

- Peters and Chin-Yee 2025, generalization bias in LLM summaries of science: https://arxiv.org/abs/2504.00025
- ASIC 2024, AI summarisation proof of concept (tabled to the Australian Senate): https://www.aph.gov.au/DocumentStore.ashx?id=b4fd6043-6626-4cbe-b8ee-a5c7319e94a0
- Reinhart et al. 2025, "Do LLMs write like humans?" (Biber features; nominalizations and participles): https://arxiv.org/html/2410.16107v1
- Wikipedia, "Signs of AI writing": https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- Zhou et al. 2024, language models are reluctant to express uncertainty: https://arxiv.org/abs/2401.06730
- BBC, December 2024, Apple Intelligence false notification summary: https://www.bbc.com/news/articles/cd0elzk24dno
- Markowitz 2024, simple GPT summaries aid lay comprehension: https://pubmed.ncbi.nlm.nih.gov/39290437/
- Melumad and Yun 2025, shallower knowledge from LLM summaries: https://pubmed.ncbi.nlm.nih.gov/41163786/

Local files referenced

- Sample report (text): `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/20260906-morning-priorities.txt`
- Sample report (HTML): `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/samples/20260906-morning-priorities.html`
- Report source markdown: `/Users/aelaguiz/workspace/psagentspace/roadmaps/company/morning-priorities/runs/2026-09-06.md`
