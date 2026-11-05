# Where each kind of work starts

Read November 5, 2026, from the evidence in [evidence.md](evidence.md). This is a dated reading, and `$model-eval` updates it. The teaching stays in `SKILL.md`, so a new result changes a row here and nothing there.

Each row gives the setting to start on from each family. Without a mark, it's the cheapest setting that held up on that kind of work, and "held" means neither judge saw the score fall by much against the level above it. A * marks a setting that was never run on that kind: a starting guess from field use or the levels around it, tested by nothing yet. Rows rest on 3 to 6 tasks, so each is a direction. Each setting names the version it was measured on. Always run the family's newest version: a newer one starts from its row until it has been measured. A level you or your team has named wins over a row, as "Whose pick wins" says.

The rows run from work where the material carries the answer to work where the thinking is the job.

| Kind of work | For example | Claude | Codex | What has been measured |
|---|---|---|---|---|
| Mechanical work | Rebase, run the tests and report what failed | Sonnet 5.5 medium | Terra 6.1 xhigh | Two small jobs ending in a test, all right. Sonnet 5.5 at medium was quickest and Terra 6.1 at xhigh cheapest |
| Fix a well-defined bug | Cause known, one or two files, one part of a full spec | Sonnet 5.5 medium | Terra 6.1 xhigh | The same two jobs, nothing larger. In field use, no Terra 6.1 xhigh build from a full spec needed redoing |
| Bring text in line with the facts | PR text, docs after a change | Opus 5.5 medium | Terra 6.1 xhigh | 3 documents: Opus held at medium, and Sol from high down to low. Terra 6.1 at xhigh matched Sol 6.1 at high on one |
| Research a question | From documents, email or the web | Opus 5.5 medium | Sol 6.1 low | 5 tasks: Sol stayed level from high to low. Opus fell at low |
| Judge images or frames against a standard | "Does each screenshot follow the style guide?" | Opus 5.5 medium | Sol 6.1 low | 5 tasks: Sol stayed level down to low. Opus fell at low |
| Work out a problem with one right answer | "Which of these three options is correct, and why?" | Opus 5.5 medium | Sol 6.1 low | 4 tasks: Sol stayed level down to low. Opus 5.5 at medium and low came out about even |
| Read a document cold | As the reader it was written for | Opus 5.5 medium | Terra 6.1 xhigh | 4 tasks, noisy: on the 3 first run on Opus, Opus 5.5 at medium scored below both that setting and Opus 5.5 at low. Sol stayed level down to low. Terra 6.1 at xhigh about matched Sol 6.1 at high on two |
| Analyze a dataset | "How did last week's sign-ups compare with the week before?" | Opus 5.5 medium | Sol 6.1 medium | 5 tasks: Sol held at medium and slipped at low. Opus fell at low |
| Check facts against their sources | Numbers, quotes, records | Opus 5.5 medium | Sol 6.1 medium | 6 tasks: Sol 6.1 at medium and low came out level, below high on one judge. On the 4 first run on Opus, Opus 5.5 at medium sat most of a point below that setting and fell hard at low |
| Label items by a codebook | "Tag these tickets with the categories in this list" | Opus 5.5 medium | Sol 6.1 medium | 5 tasks: on the 2 first run on Opus, Opus 5.5 at medium held and slipped at low. Sol slipped a little at medium and more at low |
| Check in on running work | "Is this session still doing what it was asked?" | Opus 5.5 medium | Sol 6.1 high | 4 tasks: Sol stayed level from high to low, and Opus slipped at medium and low. But on 20 real timed looks, Sol 6.1 at high missed 37 to 42% of what Astra 6.0 at xhigh had caught, on 16 of them Sol 6.1 at xhigh caught no more, and Astra 6.0 at high matched Sol 6.1 at high at six times the cost, so "Which reviews need deep thinking" decides this one |
| Write short copy people read | Scripts, ad copy, the product's own lines | Opus 5.5 high* | Sol 6.1 medium | 5 tasks: Sol held at medium and fell hard at low. On the 4 first run on Opus, Opus 5.5 at medium sat about a point below that setting |
| Plan or design | An implementation plan and its test plan | Opus 5.5 high* | Sol 6.1 high | 5 tasks: Sol 6.1 at medium lost a little on one judge and took the same time as high. On the 2 first run on Opus, Opus 5.5 at medium sat a point below that setting. Opus 5.5 at high matched Opus 5.5 at medium on one later task |
| Explain how code behaves | "Which file decides when this request is retried?" | Opus 5.5 medium | Sol 6.1 high | 4 tasks: Opus held at medium and collapsed at low. Sol fell at medium on one judge |
| Judge writing against a standard | Copy or content against a style guide | Opus 5.5 medium | Sol 6.1 high | 5 tasks: Sol fell more than a point at medium on both judges. Opus held at medium and fell at low |
| Review code or a plan against its spec | "Did this build do what the spec says?" | Opus 5.5 high* | Sol 6.1 high | 5 tasks: on the 4 first run on Sol 6.1 at xhigh, Sol 6.1 at high matched that and Sol 6.1 at medium fell. Only one first ran on Opus, too few to place a level |
| Second opinion, once | A plan or PR, looking for what you missed | Opus 5.5 high* | Astra 6.0 xhigh | From a maker other than the one that made the work. Astra 6.0 at xhigh is a setting people named. On reviewer looks Astra 6.0 at high kept up with it in about half the time, on 5 looks |
| Find a bug's cause | Reproduce it and name the cause, a red CI job nobody has read | Opus 5.5 medium* | Sol 6.1 xhigh* | Not measured. Field use, next to "Explain how code behaves" |
| Build across several parts from a spec | App and backend, several screens | Opus 5.5 medium* | Sol 6.1 xhigh* | Not measured: the back-test stopped before its code-writing tasks ran. Field use |
| New feature with algorithmic changes | A new game rule, a ratings change, a spec with open design calls | Opus 5.5 high* | Sol 6.1 xhigh* | Not measured. Field use |
| Walk a test plan on a device | Capture each screen and compare it with what was decided | Opus 5.5 high* | Terra 6.1 xhigh* | Not measured: it can't be rerun in a back-test. Field use |
| Build a content item through its steps | A long authoring process with checks at each step | Opus 5.5 high* | Sol 6.1 xhigh* | 6 tasks: every setting run below what the tasks first ran on misled on at least one, on either family |
| Translate text | Under a glossary, a length limit and a check script | Opus 5.5 xhigh | Sol 6.1 xhigh* | 5 tasks, all first run on Opus 5.5 at xhigh or max: Opus 5.5 at medium sat most of a point below that. Sol misled on 2 of 5 at high, medium and low |

Terra 6.1 at xhigh has been run on only a few of these kinds. It cost about a third of Sol 6.1 at high and matched it on the three documents where they could be compared, so where a row says Sol at a low level and the job is cheap to check, Terra 6.1 at xhigh is worth trying.
