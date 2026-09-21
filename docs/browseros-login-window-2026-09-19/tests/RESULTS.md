# Dry-run results: can Sol and Opus place a login correctly from the skill alone?

Run 2026-09-20 02:44-02:53 UTC against the installed skill after the edit in
`docs/BROWSEROS_LOGIN_WINDOW_ANALYSIS_AND_PLAN_2026-09-19.md`. Harness:
`run_one.sh` (Codex `gpt-5.6-sol` high, read-only sandbox, MCP servers
cleared; Claude `claude-opus-5` high, hooks off, empty strict MCP config,
tools limited to Read/Glob/Grep). Prompts in `prompts/`, one folder per run in
`runs/` with the prompt's answer (`final.txt`) and the files the agent read
(`trace.txt`). Grading per `RUBRIC.md`, by the parent session.

| Scenario | Opus r1 | Opus r2 | Sol r1 | Sol r2 |
| --- | --- | --- | --- | --- |
| S1 console after "use pro1" | pass | pass | pass | pass |
| S2 login wall in pro1 | pass | pass | pass | pass |
| S3 CLI login that opens the browser | pass | pass | pass | pass |
| S4 chooser shows only pro1 | pass | pass | pass | pass |
| S5 signed-in page already in Work | pass* | pass* | r1 lost to "model at capacity"; r3 pass* | pass |
| S6 real gate in Work | pass | pass | pass | pass |

What every passing run did: opened or reopened the site in the `Default`
(`Work`) window with `newPage` and a window id, verified the placement with
the window map, refused to click the Google controls in `pro1`, did not ask
permission to use `Work`, named the profile and tab in its message to Amir,
and (S3) neutralized the CLI's browser launch with `BROWSER=true` or a
printing mode, opened the printed URL in `Work`, and proved the login from
the tool.

\* S5: both Opus runs and the Sol run opened their own background page in the
`Work` window instead of reading the pre-existing page 402, because the
provenance table treats a page of unknown ownership as inventory-only. That
is consistent with the skill and achieves the login lesson (no login asked,
right window), so the rubric was amended and the rule in `SKILL.md` now says
a signed-in `Work` page proves the login and the agent may read it or open its
own page in the same window.

Sol S5 r1 failed with "Selected model is at capacity" before answering
(infrastructure, not doctrine); r3 replaced it and passed. Final: 24 of 24
graded runs pass, no doctrine iteration was needed beyond the S5 wording fix.

Things the runs asked Amir for that are not login questions: the two exact
event names for the RudderStack allowlist (S1/S2), and the ad account id (S6).
Those are task inputs the scenario left out on purpose.

Not tested live: an actual OAuth round trip. The dry runs prove the decision
and the calls; the mechanics (`newPage` with `windowId`, the window map, the
`BROWSER` no-op) were verified separately on this machine and in the
September 5 and August 28-30 sessions cited in the plan.
