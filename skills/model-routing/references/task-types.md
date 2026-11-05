# Where each kind of work starts

Read November 5, 2026, from the evidence in [evidence.md](evidence.md). This is a dated reading, and `$model-eval` updates it. The teaching stays in `SKILL.md`, so a new result changes a row here and nothing there.

Each row gives the setting to start on from each family: the cheapest one that held up on that kind of work in what has been measured. "Held" means neither judge saw the score fall by much against the level above it. Where nothing has been measured, the row says so, and the setting is a starting guess from field use. Rows rest on 3 to 6 tasks, so each is a direction. Names are families, so use the newest version of each. A level you or your team has named wins over a row, as "Whose pick wins" says.

The rows run from work where the material carries the answer to work where the thinking is the job.

| Kind of work | For example | Claude | Codex | What has been measured |
|---|---|---|---|---|
| Mechanical work | Rebase, run the tests and report what failed | Sonnet medium | Terra xhigh | Two small jobs ending in a test, all right. Sonnet at medium was quickest and Terra at xhigh cheapest |
| Fix a well-defined bug | Cause known, one or two files, one part of a full spec | Sonnet medium | Terra xhigh | The same two jobs, nothing larger. In field use, no Terra xhigh build from a full spec needed redoing |
| Bring text in line with the facts | PR text, docs after a change | Opus medium | Terra xhigh | 3 documents: Opus held at medium, and Sol from high down to low. Terra at xhigh matched Sol at high on one |
| Research a question | From documents, email or the web | Opus medium | Sol low | 5 tasks: Sol stayed level from high to low. Opus fell at low |
| Judge images or frames against a standard | "Does each screenshot follow the style guide?" | Opus medium | Sol low | 5 tasks: Sol stayed level down to low. Opus fell at low |
| Work out a problem with one right answer | "Which of these three options is correct, and why?" | Opus medium | Sol low | 4 tasks: Sol stayed level down to low. Opus at medium and low came out about even |
| Read a document cold | As the reader it was written for | Opus medium | Terra xhigh | 4 tasks, noisy: Opus at medium scored below both its top and its low. Sol stayed level down to low. Terra at xhigh about matched Sol at high on two |
| Analyze a dataset | "How did last week's sign-ups compare with the week before?" | Opus medium | Sol medium | 5 tasks: Sol held at medium and slipped at low. Opus fell at low |
| Check facts against their sources | Numbers, quotes, records | Opus medium | Sol medium | 6 tasks: Sol at medium and low came out level, below high on one judge. Opus at medium sat most of a point below its top and fell hard at low |
| Label items by a codebook | "Tag these tickets with the categories in this list" | Opus medium | Sol medium | 5 tasks: Opus at medium beat the top setting and fell at low. Sol slipped a little at medium and more at low |
| Check in on running work | "Is this session still doing what it was asked?" | Opus medium | Sol high | 4 tasks: Sol stayed level from high to low, and Opus slipped at medium and low. But on 20 real timed looks, Sol at high missed 37 to 42% of what Astra at xhigh had caught, so "Which reviews need deep thinking" decides this one |
| Write short copy people read | Scripts, ad copy, the product's own lines | Opus high | Sol medium | 5 tasks: Sol held at medium and fell hard at low. Opus at medium sat about a point below its top. Opus at high hasn't been run on this kind |
| Plan or design | An implementation plan and its test plan | Opus high | Sol high | 5 tasks: Sol at medium lost a little on one judge and took the same time as high. Opus at medium sat about a point below its top |
| Explain how code behaves | "Which file decides when this request is retried?" | Opus medium | Sol high | 4 tasks: Opus held at medium and collapsed at low. Sol fell at medium on one judge |
| Judge writing against a standard | Copy or content against a style guide | Opus medium | Sol high | 5 tasks: Sol fell more than a point at medium on both judges. Opus held at medium and fell at low |
| Review code or a plan against its spec | "Did this build do what the spec says?" | Opus high | Sol high | 5 tasks, mostly first run on Sol at xhigh: Sol at high matched it and fell at medium. Opus at medium scored well under it, across families |
| Second opinion, once | A plan or PR, looking for what you missed | Opus high | Astra xhigh | From a maker other than the one that made the work. Astra has not been run below xhigh, so how far it can drop is unknown |
| Find a bug's cause | Reproduce it and name the cause, a red CI job nobody has read | Opus medium | Sol xhigh | Not measured. A starting guess from field use, next to "Explain how code behaves" |
| Build across several parts from a spec | App and backend, several screens | Opus medium | Sol xhigh | Not measured: the back-test stopped before its code-writing tasks ran. A starting guess from field use |
| New feature with algorithmic changes | A new game rule, a ratings change, a spec with open design calls | Opus high | Sol xhigh | Not measured. A starting guess from field use |
| Walk a test plan on a device | Capture each screen and compare it with what was decided | Opus high | Terra xhigh | Not measured: it can't be rerun in a back-test. A starting guess from field use |
| Build a content item through its steps | A long authoring process with checks at each step | Opus high | Sol xhigh | 6 tasks: every lower setting on either family misled on at least one. Levels above Sol at high weren't run |
| Translate text | Under a glossary, a length limit and a check script | Opus xhigh | Sol xhigh | 5 tasks: Opus at medium sat most of a point below its top. Sol misled on 2 of 5 at high, medium and low, and Sol at xhigh wasn't run |

Terra at xhigh has been run on only a few of these kinds. It cost about a third of Sol at high and matched it on the three documents where they could be compared, so where a row says Sol at a low level and the job is cheap to check, Terra at xhigh is worth trying.
