# What each model is weak at

Read November 5, 2026. This is a dated record, and `$model-eval` updates it. Each row names the version it was seen on, because a version is its own model and a weakness doesn't carry to the next one by itself. Always run the newest version; a newer one starts from its row until it has been measured.

How firm each row is matters, so the last column says what stands behind it. "Field" means the judgment of the person who has watched these models build for months. It's strong evidence and it isn't a measurement.

| Model | Weak at | How it shows up | What to do about it | What stands behind it |
|---|---|---|---|---|
| Sol 6.1 | Overbuilding and pedantic scope creep, the worst of these | Three more things to guard against, every time; a simple feature grows into thousands of lines of checks; a fixed number becomes a formula | The brief names the plainest version. Someone from another maker reads the whole diff for what it doesn't need. Its findings are proposals | Field, and one case where guards were about a third of a change |
| Astra 6.0 | The same lean, much less | Smart findings mixed with pedantic, myopic ones that add complexity | A good cross-check on Opus 5.5, because it's smart. Weigh each finding: would a user here meet it? | Field |
| Terra 6.1 | Not known yet | | | Not tested for this |
| Opus 5.5 | Adds much less than Sol 6.1 or Astra 6.0. Its own weak side isn't written down yet | At low, it drops rules of a brief; at medium, it can skip a check the brief asked for | Keep it at medium or above on long briefs | Back-test for the levels; field for adding |
| Sonnet 5.5 | Losing its grip on a long brief | Skipped rules; a read-only review that wrote files | Use it where a check proves the work | Back-test |
| Haiku 5.5 | Losing its grip on a long brief, more than Sonnet 5.5 | Misled on about half of real helper tasks | Keep it to work with no judgment in it | Back-test |
