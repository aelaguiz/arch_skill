# How to write technical explanations engineers can actually read

**Clear technical writing is the byproduct of one decision made over and over: spend your reader's working memory on ideas, not on parsing.** Most confusing engineering prose isn't confusing because the topic is hard. It's confusing because the writer made the reader do unnecessary work — guess where a sentence is heading, hold five unattached modifiers in mind, infer who is doing what, decode an acronym that appears once. Every technique below — short sentences, active verbs, unstacked noun phrases, concrete examples, defined jargon — is a way of paying that tax instead of charging it. The cognitive science is unanimous (Cowan's working-memory limit of about four items; Gibson's dependency-locality theory; Paivio's dual-coding effect): readers have a tiny buffer, and they spend it on whatever you make them spend it on. The guide below is organized around the highest-leverage moves, with concrete before/after rewrites for each. The aim is not "simple writing." The aim is *dense* writing whose density is in the ideas, not the syntax.

## Lead with the answer; cut the throat-clearing

The first sentence is your most valuable real estate. Use it for the conclusion, the recommendation, the surprising finding, the thing the reader needs to do. This is the **BLUF** principle ("bottom line up front") borrowed from US military memos and now standard in design docs at Amazon, Google, and most serious engineering organizations. Knuth's first rule in *Mathematical Writing* says the same thing: "the opening paragraph should be your best paragraph, and its first sentence should be your best sentence."

The reader's attention is highest at the start and decays fast. Sean Goedecke puts it bluntly: readers read sentence one, skim sentence two, and either skim the rest or stop. If you spend a paragraph setting up context, half your audience is gone before you say anything.

**Before:** *In the modern distributed systems landscape, ensuring data integrity across multiple nodes has become an increasingly important consideration. There are many factors that affect this. In this document, we will discuss the trade-offs we considered and ultimately the approach we have decided to take.*

**After:** *We're switching the order service from strong to eventual consistency. The latency win (p99 drops from 240ms to 35ms) is worth the 1–2 second window where reads can be stale. Details below.*

The "before" version says nothing in 47 words. The "after" version answers *what, why, what's the cost, where to read more* in 36. Throat-clearing phrases to delete on sight: *In this document we will discuss…, It is important to note that…, Over the years…, As we all know…, Recently there has been growing interest in….* If the paragraph still works after you delete sentence one, sentence one was throat-clearing.

A specific corollary: **bury the lede only when the lede is meaningless without prerequisites.** If "we should migrate to microservices" requires architectural background to make sense, the prerequisite is the lede — give the reader the framing fact, then the recommendation. But default to BLUF.

## Unstack noun phrases — the single highest-leverage fix

This is the most common defect in engineering writing and the hardest to see in your own prose. A noun stack is a string of three or more nouns and noun-like modifiers crammed in front of a single head noun: *failed password security question answer attempts limit* (a real Microsoft example), *cross-region database failover latency*, *live-vs-replay solver consistency*. Each one is parseable in principle. Each one forces the reader to do work the writer should have done.

**Why noun stacks fail.** English puts the head noun *last*. Until it arrives, every preceding word is an unattached fragment the reader holds in working memory. With three modifiers, the reader must also guess the bracketing (*[user account] [verification email] template* or *[user] [account verification email] template*?) and the implicit relation between every pair (template *for* emails *that perform* verification *of* user accounts). English deletes those relational prepositions when it stacks, so the reader reconstructs them from world knowledge — which is fine if the reader already knows what the phrase means, and a disaster if they don't. Geoff Pullum coined **nerdview** for the resulting failure: the writer is so embedded in the domain that the implicit connectors feel obvious; to anyone outside, the phrase is opaque. "Live-vs-replay solver consistency" is textbook nerdview. The author *knows* it means "the solver gives the same answer on live data as on replay." A reader has to invent that.

**The threshold rule.** Two-noun compounds are usually fine because readers have stored them as single units: *load balancer, garbage collection, race condition, stack trace, thread pool, type system, build server, queue depth*. **Three is risky** unless one of the three pairs is itself a frozen compound (*load-balancer health-check timeout* survives because both *load balancer* and *health check* are lexicalized). **Four is almost always a defect.** If you would need two hyphens to disambiguate the bracketing, rewrite.

**The unstacking moves.** Apply them in order:

1. **Drag the head noun to the front and convert leading modifiers into a prepositional phrase** (using *of, for, on, in, by, between, against, with*). This is the workhorse fix.
2. **Un-bury the verb.** Any noun ending in *-tion, -ment, -ance, -ity, -al, -ing* used as the action — turn it back into a verb. Helen Sword calls these "zombie nouns"; Bryan Garner calls them "buried verbs." They almost always shorten and clarify because the verb's subject and object snap into natural order.
3. **Promote a modifier to a relative clause** (*the template that verifies a user's account*).
4. **Replace a vague head noun** (*system, framework, mechanism, layer, context, infrastructure, approach*) with the concrete object it actually refers to.
5. **Break into two sentences.** Often the cleanest fix. The phrase wasn't one idea; it was three.

A wide spread of rewrites, drawn from real and realistic engineering contexts:

| Stacked | Unstacked |
|---|---|
| live-vs-replay solver consistency | whether the solver gives the same answer on live data as it does when replayed on recorded data |
| user account verification email template | the email template we send to verify a user's account |
| request rate limit exceeded handler | the handler that runs when a request exceeds the rate limit |
| cross-region database failover latency | how long it takes to fail a database over to another region |
| stale replica read fallback policy | the policy that decides whether to read from a stale replica when the primary is unreachable |
| write-ahead log segment compaction worker | the worker that compacts segments of the write-ahead log |
| secondary index update propagation lag metric | how far behind secondary indexes are when propagating updates |
| TCP retransmission timeout backoff multiplier | the factor we multiply the timeout by after each TCP retransmission |
| build server cache invalidation race condition | a race condition in how the build server invalidates its cache |
| deployment rollback failure notification escalation path | who gets paged, and in what order, when a rollback fails |
| failed password security question answer attempts limit | the maximum number of wrong answers to a password-reset question before lockout |
| AWS IAM role assumption policy condition key | a condition key in the policy that controls who can assume this IAM role |
| OAuth token refresh grant flow callback handler | the handler for the callback in the OAuth refresh-token flow |
| flash memory wear leveling block reassignment | reassigning flash blocks as part of wear leveling |
| configuration file parser error reporting subsystem | the part of the config parser that reports errors |
| training data pipeline schema drift detection | detecting schema drift in the training-data pipeline |
| feature store online serving fan-out latency | how long the feature store takes to fan a request out to its online-serving replicas |
| event-driven cross-platform real-time data-streaming pipeline | a real-time streaming pipeline, driven by events, that runs on every platform |

**A specific anti-pattern: variable-name leakage.** Engineers paste `failedPasswordSecurityQuestionAnswerAttemptsLimit` straight from code into prose. Identifiers must be unbroken strings; prose must not. Translate every identifier into a phrase before it enters a sentence.

**Another anti-pattern: the acronym-stack chimera.** *AWS IAM SCP policy boundary evaluation order* hides six prepositions in eight words. Each acronym carries an undefined noun. Either expand them and unstack normally, or split the explanation into two sentences: *"AWS evaluates two kinds of policy when deciding whether an action is allowed: SCPs (organization-wide) and permission boundaries (account-wide). The order is …"*

**When stacks earn their keep.** Sometimes a compound *is* the name of a thing — *Linux kernel memory management subsystem, polymerase chain reaction, hypertext transfer protocol*. These are proper or near-proper names; readers store them as single nodes. The test: does the phrase identify a specific, agreed-on entity in the field, or is it a description the writer composed for this document? The first earns a pass. The second needs unstacking.

## Hunt zombie nouns; verbs do real work

A nominalization is a verb (or adjective) jammed into a noun: *decide → decision, fail → failure, implement → implementation, analyze → analysis, careless → carelessness*. Helen Sword's term "zombie nouns" captures the pathology: they cannibalize the verb of the sentence and force a vague helper verb (*occur, take place, perform, conduct, make*) to do the actual work. Bryan Garner's diagnostic suffixes: *-tion, -sion, -ment, -ance, -ence, -ity, -ing*.

The cost is double. First, a nominalization deletes the actor — *"the deletion was performed"* by whom? Second, it forces stacked prepositions, because the verb's old object has to be reattached with *of*: *"the implementation of the optimization of the storage layer."*

| Zombie | Live |
|---|---|
| make a determination | determine |
| conduct an investigation of | investigate |
| provide assistance to | help |
| perform an analysis of | analyze |
| reach a settlement | settle |
| has the ability to | can |
| is in possession of | has |
| in the event that | if |
| due to the fact that | because |
| at this point in time | now |
| the implementation of the optimization | optimizing |
| the configuration of the parameters of the request of the client | the client's request parameters (or: configuring the client's request) |
| the prosecutor's expectation was that defense counsel would make an objection | the prosecutor expected defense counsel to object |

Joseph Williams' rule, the one engineers should tattoo on their forearms: **make the main characters the subjects, and their important actions the verbs.** When the grammar (subject-verb-object) lines up with the story (who-does-what-to-whom), readers parse without effort. When it doesn't, they feel the prose as "gummy." Williams' diagnostic: scan the first seven or eight words of each sentence. If the subject is abstract and the verb is *is, has, makes, performs, conducts*, you have a zombie problem.

## Be concrete; descend the ladder of abstraction

Concrete words activate two memory systems (Paivio's dual-coding theory), get read faster (Sadoski & Paivio 2001), and are retained longer (Fliessbach et al. 2006). Abstract words activate only the verbal system. The cost compounds: a paragraph of abstractions demands the reader build an example for every sentence just to follow along.

**Before (Strunk & White's example):** *A period of unfavorable weather set in.*
**After:** *It rained every day for a week.*

**Before:** *The system exhibits suboptimal performance characteristics under high-concurrency conditions.*
**After:** *Past 200 concurrent users, p95 latency jumps from 80ms to 2 seconds.*

**Before:** *Improvements were made to the caching layer.*
**After:** *We added a 30-second TTL to user-profile lookups, which cut database load by 60%.*

The "before" sentences are technically true and contain zero information. The "after" sentences locate the claim in something the reader can picture and check. Hayakawa's ladder of abstraction is the underlying frame: any topic can be discussed at many levels (*Bessie* → *cow* → *livestock* → *farm asset* → *asset* → *wealth*), and effective writing moves up and down it. Engineers default to the upper rungs. The fix is to push down — to the specific number, the specific user, the specific request, the specific failure mode.

Pinker calls the failure mode "functional fixity": experts think of objects by their *role* rather than what they look like, so they write *"conditions of good acoustic isolation"* when they mean *"a quiet room."* The signal you've fallen into it: most of your nouns are *process, capability, framework, mechanism, configuration, infrastructure*. None of them can be drawn.

A complementary technique from Julia Evans: **start every explanation with a concrete example, then generalize.** Her famous opening — *"Have you used `kill`? You've used signals!"* — replaces the standard Wikipedia opener (*"Signals are a limited form of inter-process communication, an asynchronous notification…"*) with something the reader's hands have already done. Knuth's *Mathematical Writing* point 24 says the same: avoid "an X is Y" openings; lead with the X itself doing something.

## Keep sentences short by keeping dependencies short

The folk rule "use short sentences" is approximately right for the wrong reason. Length per se isn't the killer — *unresolved dependencies* are. Edward Gibson's dependency-locality theory predicts (and eye-tracking confirms) that processing cost scales with how long a syntactic dependency stays open while the reader holds intervening material in working memory. A right-branching forty-word sentence reads more easily than a center-embedded twenty-word one.

Practical consequences:

**Don't separate subject from verb with long modifiers.** *"The new caching layer, which was introduced in Q3 after a six-month effort by the platform team and replaces the previous Redis-based implementation that had been in production since 2019, is faster."* By the time *is* arrives, the reader has lost the subject. Split: *"The new caching layer is faster. We introduced it in Q3 after a six-month effort. It replaces the Redis implementation we'd run since 2019."*

**Don't center-embed.** *"The packets the router the team rewrote dropped triggered the retry."* Single embedding is fine. Double is hard. Triple is essentially unparseable even when grammatical (Miller & Chomsky 1963). Use relative pronouns (*that, which, who*) to mark structure, and prefer right-branching: extend at the *end* of the sentence, not the middle.

**Avoid garden paths.** Reading is left-to-right and committed; when a sentence forces re-parsing, comprehension breaks. Common engineering triggers: *"Build runtime checks system reliability"* (is *checks* a verb or a noun?), *"The packets dropped by the router triggered the retry"* (initial parse: *packets dropped* as main clause). Insert *that* or *which* to disambiguate: *"The packets that the router dropped…"*

**Match sentence shape to thought shape.** Dan Luu's pushback against Strunk-and-Whiteification is worth taking seriously: when the underlying logic is genuinely conditional or quantified, splitting it into staccato sentences can lose the dependency. The goal is not minimum length; it's minimum unresolved structure per moment of reading. A long sentence whose dependencies all close on the right is fine. A short sentence with a triple-nested subject is not.

The rule of thumb most plain-language guides converge on: average around 15–20 words; cap individual sentences near 30; if a sentence wants to go past 30, ask whether it's actually two ideas.

## Use active voice when you have an actor; use passive when you don't

The "always use active voice" rule is wrong. Linguists have been pointing this out since Pullum's critique of Strunk and White. Williams, Pinker, and the Google Developer Style Guide all agree: passive voice is correct when (a) the patient is the topic, (b) the agent is unknown or irrelevant, or (c) you need new information at the end of the sentence to chain into the next one.

The honest reason engineers should default to active is different: passive voice **lets writers hide the actor** — and in engineering writing, hiding the actor is usually evasion. *"Mistakes were made."* *"It was decided that the migration would be deferred."* *"The database was purged."* Each of these answers the wrong question. Who? Who decided? Who purged?

| Hiding | Honest |
|---|---|
| Mistakes were made in the rollout. | We rolled out without a canary. |
| It was determined that the API contract would need to change. | The platform team decided to change the API contract. |
| Latency improvements have been observed. | p99 latency dropped from 240ms to 80ms after the cache change. |
| The service is queried, and an acknowledgment is sent. | Send a query to the service; the server sends back an acknowledgment. |

When passive earns its place: *"The database was purged in January"* (when nobody cares who; the event is the topic). *"Over 50 conflicts were found in the file"* (when *you* found them but blaming the reader is harsh). The principle: choose voice based on *which noun is the topic*, not on a blanket rule.

## Introduce jargon deliberately, or don't use it

Jargon is not the enemy. Specialized vocabulary lets experts pack a paragraph of meaning into one word — *idempotent, quorum, mutex, checksum, serialization, eventual consistency*. Banning it would make engineering writing longer and less precise. The actual problems are (1) using jargon the audience doesn't share, (2) introducing jargon without grounding it, and (3) using jargon as a status signal where a plain word would do.

**The two questions to ask** (Kate Moran, Nielsen Norman Group): *How many of my readers know this term? How important is the term?* If most readers know it, use it bare. If the term is essential and some readers don't know it, define it the first time. If a plain word works, use the plain word.

**A reliable four-move pattern for introducing a term**: define in one concrete sentence, give an example the reader can picture, contrast with what it isn't, *then* name the term — bolded, at the end of the buildup, as the result of the explanation rather than its starting point.

**Bad:** *We use eventual consistency for the replica set.*

**Mediocre:** *We use eventual consistency, a model in which replicas converge to the same value over time, for the replica set.*

**Good:** *When you write a value to one replica, the other replicas don't see it immediately — they catch up after a short delay, usually under a second. A read right after a write may return the old value. This is different from strong consistency, where every read is guaranteed to see the latest write. We call this model **eventual consistency**.*

The good version costs three more sentences. It saves the reader from googling.

**A complementary move: "show, don't define."** Sometimes a worked example beats any definition. To explain *idempotent*: don't write "an operation that produces the same result when applied multiple times." Write: *"Calling `DELETE /users/42` once deletes the user. Calling it again returns 404 but doesn't break anything. That's what we mean by idempotent."* The concept is now hooked to a memory the reader can replay.

**Anti-patterns to watch for.** *Restating jargon instead of explaining it* — calling Git "a content-addressable filesystem" and then "a simple key-value store" without ever saying that the key is a hash of the content (Julia Evans' diagnosis of the Git book). *Circular definitions* — explaining "cryptographically secure" by saying it's "secure against cryptographic attack." *Shibboleth jargon* — using *leverage, holistic, paradigm, first-class citizen, blast radius, ingest, off-the-shelf* when *use, whole, model, primary, affected area, import, ready-made* would communicate better. The Google developer guide explicitly flags these.

## Spell out acronyms — usually

Default rule: spell out on first use, parenthesize the acronym, then use the acronym thereafter. *"The Border Gateway Protocol (BGP) controls inter-AS routing. BGP sessions…"* Reverse the order if the acronym is more recognizable than the expansion (*"ETF (exchange-traded fund)"*). Don't expand acronyms that have effectively become words (*laser, radar, scuba*) or that any plausible reader will know in context (HTTP, URL, API, CPU, RAM, JSON, SQL, USB). And don't define an acronym you're only going to use twice — just spell it out both times.

Acronyms that *always* need expansion: anything specific to your team or product (the canonical anti-example is an API doc that uses an undefined `DEG` everywhere, leaving the reader to guess); anything with multiple common expansions (ATM, CRM, SLA); anything in a doc that may be read non-linearly — re-expand at the start of each major section.

The Federal Plain Language Guidelines impose a hard limit: no more than two or three acronyms per document. Beyond that, you've offloaded a lookup table to the reader's working memory.

## Use analogies sparingly, and never as load-bearing structure

Analogies bootstrap intuition cheaply. They also mislead — sometimes badly — when they're stretched. Feynman's articulation of when analogy fails is the best one available. Asked to explain magnetic attraction, he refused to use rubber bands, saying: *"if I said the magnets attract like as if they were connected by rubber bands, I would be cheating you. Because they're not connected by rubber bands… and if you were curious enough, you'd ask me why rubber bands tend to pull back together again, and I would end up explaining that in terms of electrical forces, which are the very things that I'm trying to use the rubber bands to explain."*

The principle: an analogy works when it shares an *underlying mechanism* with the target. It fails when the reader can ask "why" of the analogy and the answer is the same phenomenon you're trying to explain. *"A monad is like a burrito"* fails because the burrito has none of the structure that makes a monad a monad. *"Backpressure in a stream is like a traffic jam — slow consumers cause the queue ahead of them to fill up"* works because the underlying mechanism (a slow node propagates congestion upstream) is genuinely shared.

Heuristics: **one analogy per concept, used once, then dropped.** If you find yourself elaborating the analogy ("the database is like a city, the queries are tourists, the indexes are subway maps…"), the reader is now learning your analogy instead of the target. Cut it.

## Cut the hedges, the weasels, and the gaslighters

Three families of small words make engineering prose look careful but read worse:

**Hedges that mean nothing.** *somewhat, fairly, quite, rather, basically, essentially, arguably, perhaps, possibly, in some sense.* Used once, fine. Stacked, they signal that the writer doesn't want to be wrong: *"This may possibly be somewhat slower in certain cases."* Either you measured it and it's slower, or you didn't and you don't know. Move uncertainty into a number with a confidence interval, or into a footnote with the data, not into a fog of qualifiers.

**Weasel words that fake authority.** *experts say, it is widely believed, evidence suggests, many engineers prefer, it has been argued.* Replace with the actual source or the actual count. If you can't, drop the claim.

**Minimizers that gaslight.** *obviously, simply, just, of course, clearly, trivially.* These tell a reader who is struggling that they shouldn't be. They almost always signal curse-of-knowledge: the writer learned it long ago and now finds it self-evident. Delete them. *"Just SSH into the box and edit the config"* loses nothing by becoming *"SSH into the box and edit the config"* — and stops insulting readers who haven't done it before.

**False rigor.** Six decimal places when "about half" would do. Type signatures in prose when the reader doesn't need them. Long Greek-letter formulas where two sentences would communicate the same idea. Knuth's rule on this: every symbol should earn its place; sentences should still flow when formulas are mentally replaced by "blah."

**"It depends" without elaboration.** A non-answer disguised as an answer. If it depends, on *what* does it depend, and which direction does each dependency push? If you genuinely don't know, say so and give the case from your own experience. A specific anecdote beats a generic refusal to commit.

## Information order: old before new, topic before stress

Joseph Williams' contribution that engineers most often miss: sentences flow when each one starts with information the reader already has and ends with information that's new. The new at the end of sentence N becomes the old at the start of sentence N+1, building a chain. This is the **given-new contract** (Haviland & Clark 1974), and it explains why some technically correct paragraphs feel choppy while others glide.

**Choppy:**
> *Eventual consistency is what our replica set uses. The ability for replicas to diverge briefly under load is created by this. Higher write throughput is the reason we accept this trade-off.*

**Smooth:**
> *Our replica set uses eventual consistency. That means replicas can diverge briefly under load — which is the price we pay for higher write throughput.*

Each sentence in the smooth version starts with what the previous one ended on. The reader never has to look up a fresh subject mid-paragraph. This is also the strongest legitimate use of passive voice: passive lets you reorder so the topic comes first and the new information lands at the end. Williams calls this the "stress position" — the most emphatic slot in any sentence is its end. Put the thing you want the reader to remember there.

## Code examples: real, minimal, and contrasted

Code clarifies when it shows the *one* thing being explained, in code the reader could plausibly write themselves, with visible behavior. Code muddies when it's a toy ontology (`class Bicycle extends Vehicle`), when boilerplate dominates the meaningful line, or when multiple new concepts appear in a single snippet.

Julia Evans' rule for examples: **start with real code.** To explain Python's `lambda`, don't show `lambda x: x*x`; show `sorted(children, key=lambda x: x['age'])`, because that's how `lambda` actually gets used. To explain header files, don't describe their purpose in the abstract; show a `gcc` command failing without `#include <stdio.h>` and succeeding with it.

Kernighan and Plauger's structural move in *The Elements of Programming Style*: every rule has a "bad" example from real published code, followed by a rewrite. The pedagogical force is in the contrast, not the rule. The same move works in prose explanations of code: show the wrong way, show the right way, name what changed.

A specific code-comment anti-pattern: comments that echo the code (*`i++; // increment i`*). Comments earn their place by explaining *intent* the code can't show: *why* we're incrementing, *what invariant* this maintains, *what happens* if it overflows. If the comment is redundant, the comment is wrong.

## The curse of knowledge is what's actually wrong with your draft

Steven Pinker calls the curse of knowledge "the single best explanation I know of why good people write bad prose." Once you understand something, you can't accurately model not understanding it. Experts compress concepts into single chunks (*"backpressure," "eventual consistency," "live-vs-replay solver consistency"*) that novices have to unpack with chunks they don't possess.

The signals that you've fallen in:

- You introduce a term and never define it, because *of course* the reader knows it.
- Your nouns are mostly abstract — *process, capability, framework, mechanism, paradigm.*
- You skip intermediate steps because they "go without saying."
- You name things by their role rather than what they do (*"the orchestration layer"* rather than *"the thing that decides which worker runs each job"*).
- You use noun stacks the team uses verbally — *"the live-vs-replay solver consistency thing"* — and forget that the phrase only parses inside the team.

The fix isn't more hedging; hedging makes the curse worse by adding insulation without adding clarity. The fix is concrete examples, defined terms, and named actors. Specifically: when a draft feels right but a fresh reader is lost, you have not failed at writing — you have failed at modeling them. Replace one abstraction with one specific instance and watch the paragraph come alive.

## Naming: choose names that explain themselves

Names that describe what a thing *does* outperform names that are clever, mythological, or cute. *PaymentProcessor* beats *Hermes*. *RetryQueue* beats *Persephone*. The cleverness tax is paid by every future reader who has to learn what *Hermes* refers to in this codebase — and the tax compounds because cute names rarely come alone.

Kernighan and Pike's rule from *The Practice of Programming*: names should describe purpose; consistency matters more than brevity; mnemonic names beat compressed ones. Inside a small scope a single letter is fine (`i` in a loop). At module or service boundaries, names are documentation that runs first.

A specific anti-pattern: **the name that is itself a noun stack** (`failedPasswordSecurityQuestionAnswerAttemptsLimit`). Inside code, identifiers must be unbroken strings, so noun stacks are the natural form. The mistake is letting the identifier escape into prose. Translate before quoting.

## A short cheat sheet

The moves that matter most, in priority order:

1. **First sentence carries the answer**, not the windup.
2. **Three or more stacked nouns means rewrite.** Drag the head to the front; relocate modifiers behind it with prepositions or relative clauses.
3. **Nominalizations ending in *-tion, -ment, -ance* are usually a buried verb.** Un-bury it.
4. **Name the actor.** If the sentence doesn't say who, the sentence is hiding.
5. **One concrete example before any abstraction.**
6. **Define jargon the first time** — define, exemplify, contrast, then name.
7. **Old information starts the sentence; new information ends it.** Chain the new of one sentence to the old of the next.
8. **Cut hedges, weasels, and minimizers** (*basically, somewhat, obviously, just*).
9. **Sentences end where their dependencies close.** No center-embedding past one level.
10. **Read it aloud.** The ear catches what the eye doesn't (Knuth, Kernighan, Graham all converge on this).

## What changes when you do this

The reader's working memory is no longer occupied by syntactic bookkeeping — by held-open subjects waiting for verbs, by stacks of unattached modifiers waiting for a head, by undefined acronyms waiting to be looked up, by hedged claims waiting to be evaluated. That memory is now available for the actual content. The same paragraph, rewritten this way, doesn't get *simpler*; it gets *denser in ideas* per unit of cognitive effort. Pinker's framing is the cleanest: clear prose is a window onto the world, and the world is what the reader is trying to see. Every technique above moves another smudge off the glass.

The deeper lesson — the one Paul Graham repeats and Dan Luu demonstrates — is that this kind of writing is mostly an act of cutting. The first draft buries the answer, stacks the modifiers, hides the actor, and names the actor with a god's name. The work is finding what the sentence is actually saying and letting it say that.
