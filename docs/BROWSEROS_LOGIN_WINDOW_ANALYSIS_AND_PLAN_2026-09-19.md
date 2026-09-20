# BrowserOS logins land in the wrong window: analysis and plan

Date: 2026-09-19. Author: Claude Fable 5.1 in the arch_skill repo, at Amir's
request. Status: plan written before implementation, then implemented and
tested the same night; see section 9 for the outcome. Evidence, candidate
lists, and test transcripts are in `docs/browseros-login-window-2026-09-19/`.

**The short version.** Agents open a site, or let a command-line tool open a
site, in whichever BrowserOS window was last touched. That window is usually a
`pro` profile, not `Work`. The site shows a login wall, Google's account
chooser offers only `proN@fun.country`, and the agent concludes it needs
credentials or permission. It then stops, asks, or waits. Amir sees a login
page in a window he was not using. The fix is doctrine, not tooling: a login
wall outside `Work` means "wrong window"; sign-in and OAuth pages are opened
by the agent, in the `Work` window, through the one call that takes a window
id; and a command-line login is never allowed to launch the browser itself.

## 1. What Amir reported

Codex session `01a0b4ac-6226-7903-a44b-2b5af2a75b3f` (psagentspace, issue
5988 root cause), rollout
`~/.codex/sessions/2026/09/18/rollout-2026-09-18T08-19-51-01a0b4ac-....jsonl`:

- line 24575, 2026-09-20T02:20:27Z: "i see a rudder stack login on the wrong
  window. Make sure you're using Work profile."
- line 24577: "you can SSO into most things from my Work profile but if you
  just let he oauth link pop wherever its going to keep fucking you up."

That session had not opened RudderStack. Its reply (line 24582) said so and
promised to open SSO links in the verified `Work` window. The login page came
from a different, concurrent session.

## 2. What actually happened (root-cause trace)

Codex session `01a0bbe0-6212-7e51-b10d-7b2801e96535` (psagentspace, issue
6026 backend experiments), rollout
`~/.codex/sessions/2026/09/19/rollout-2026-09-19T17-53-59-01a0bbe0-....jsonl`.

| Line | Time (UTC) | What happened |
| --- | --- | --- |
| 10 | 22:54 | Task brief: "$issue-to-pr ... (aelaguiz@gmail.com profile for $browseros and $chatgpt-web)". |
| 54-58 | 22:55 | Agent ran the profile check correctly: window 1595534269 = `Profile 7` (`pro1`), window 1595534029 = `Default` (`Work`), plus three other profile windows. |
| 459 | 00:34 | Amir: "fine use pro1 continue" (about the ChatGPT consultation). |
| 1955 | 01:39 | Agent's own notes say RudderStack "writes use the Work-profile console". |
| 1963 | 01:39 | Agent opened `https://app.rudderstack.com/` with `newPage(..., {background:true, windowId:1595534269})`: the `pro1` window. |
| 1977 | 01:40 | Result: page 879, `https://app.rudderstack.com/login`, "Log In \| RudderStack", `browserContextId: Profile 7`. |
| 1981 | 01:40 | Agent clicked "Log in with Google" on that page. |
| 1992 | 01:40 | Same page navigated to Google's account chooser. It listed one account: "Pro One pro1@fun.country". |
| 1996 | 01:40 | Agent called `request_user_input_async`: "RudderStack is logged out in pro1; that profile only offers the Pro One Google account. May I use the existing Work-profile RudderStack login...?" |
| ~2715 | 02:09 | Reasoning: "Awaiting Work login approval". The task stalled on a question the skill already answers. |

Three mistakes stacked:

1. A ChatGPT profile choice ("use pro1") was applied to every site.
2. The login wall and the one-account chooser were not read as "wrong
   profile", although the skill says a login wall is first a sign of the
   wrong profile.
3. The agent asked permission to use `Work` for an ordinary business console,
   instead of treating `Work` as the default for everything that is not a
   ChatGPT consultation.

The visible effect for Amir: a RudderStack login page and then a Google
sign-in page appeared in the `pro1` window, which he was watching for a Pro
consultation.

## 3. Other examples in the agent history

Sweep method: `rg` over `~/.codex/sessions` (82 GB), every
`~/.aimgr/claude-homes/*/.claude/projects` and `~/.claude/projects`, and
`~/.prime/agent/sessions`, for wrong-window, login-block, OAuth, and
command-line login language; then a parser pass over the candidate files.
Raw candidate lists and the extracted rows are in
`docs/browseros-login-window-2026-09-19/`. Prior evidence from the September 9
review (`docs/browseros-session-review-2026-09-09/evidence.json`) is reused
where it covers the same failure.

| # | When | Runtime, session | What happened | Failure class |
| --- | --- | --- | --- | --- |
| A | 2026-09-19/20 | Codex `01a0bbe0` | RudderStack opened in `pro1`; SSO chooser offered only Pro One; agent asked permission to use `Work` and waited. | Wrong profile for a non-ChatGPT site; login wall misread; artificial block. |
| B | 2026-09-05 | Codex `01a07478` (charts strategy), lines 298-366 | `gws-fc auth login` has no no-browser flag and "opens browser". The CLI launched its own tab (page 276, "Google sign-in", profile unproven). The agent also captured the printed URL from the log and navigated its own page 274 to it, chose `amir@fun.country`, consented, and finished. The stray tab was left "inventory only". | OS launch to an unchosen window; recovered because the URL was also printed. |
| C | 2026-08-30 | Prime `01a04548` (Cratejoy warehouse), lines 13954-13974 | `gcloud auth login --no-launch-browser` printed the URL; the agent opened it with `tabs new` (no window argument) and got lucky on profile. The second run needed `amir@cratejoy.com`, which Google gated on a password; the agent handed off correctly. | `tabs new` for a login URL; correct manual handoff. |
| D | 2026-08-28 | Prime `01a04548`, line 2972 | `aws login --no-browser`; an Opus 5 worker drove the AWS cross-device approval through BrowserOS and verified with the CLI. | Good pattern. |
| E | 2026-08-03 | Claude `087ecf7a` (amir_cratejoy_max), line 583 | "have an opus 5 agent reauth gws cli using browseros": brief told the worker to prefer a mode that prints the URL and to drive consent in the browser as `amir@fun.country`. Succeeded. | Good pattern, but the knowledge lived in a one-off brief, not the skill. |
| F | 2026-09-04 | Codex `01a06df4` (SEP-CODEX-003) | Several windows shared the opaque `Default` context label; the agent could not identify `Work` and paused until Amir said which. | Profile identity gap (since fixed by the label check in SKILL.md). |
| G | 2026-08 | Prime community-reply session (prime-20) | A page was opened in the remembered `Default` window and loaded Two Plus Two; Amir said he could see it loading in the wrong profile. | Remembered window used without a fresh check. |
| H | 2026-07-02 | Codex `019f0ae0` (parent-profile-20260702) | Agent treated the first exposed tab as the only session and reported a login blocker; the logged-in `Work` page was already open. | Login blocker reported without inventory. |
| I | 2026-07-07 | Codex `019f39fd`, lines 8 and 173 | Meta Business redirected to `loginpage` in `Profile 15` (then called the work profile). The wall was real: Meta was signed in only in `Default`. Amir redirected the worker to the existing signed-in Facebook tab in `Default`. | Real login wall; the right move was the existing signed-in page in another profile, chosen by the user. |
| J | 2026-08-31 | Prime `01a04548` (prime-09, prime-10) | Google Workspace policy blocked a connector OAuth ("This app is blocked"); the agent navigated away from Amir's in-progress Admin Console step during the manual handoff. | Policy gate is manual; read the handed-back page before touching it. |
| K | 2026-07-21 | Codex `019f846b`, lines 3632-3680 | An AdMob task reused a stale task tab in `Profile 26`, then called `windows activate` and `set_visibility activate:true` on that window. Amir: "you're using wrong profile window dude." The agent admitted targeting the stale tab's profile and remapped from the signed-in `Work` tabs. | Remembered tab used without a fresh check; focus taken in the wrong window. |

Sweep coverage: the `rg` candidate lists cover every store. The parser pass
finished the targeted sessions above and 83 of the Codex candidate files
(through 2026-07-22) before it was stopped for time; its rows are in
`incidents-extract-partial.jsonl`. The Claude and Prime candidates were
covered by the narrower command-line-login pass (`clilogin-extract.jsonl`)
and the September 9 review, not by the broad parser.

Pattern across A-K: nobody chose the window on purpose. The page went to
"whatever was there" (a saved id, the active window, or the OS handler), and
the agent then interpreted the resulting login state as a credential problem
instead of a placement problem.

## 4. Why it happens (mechanism)

- **BrowserOS is the macOS default browser.** LaunchServices maps `http` and
  `https` to `com.browseros.browseros`. Anything that "opens the browser" (the
  `open` command, Python's `webbrowser`, Node's `open`, `gh auth login --web`,
  `gcloud auth login` without `--no-launch-browser`, `gws auth login`) hands
  the URL to BrowserOS, which puts it in the most recently active window.
  With five or more profile windows open, that is whichever one Amir clicked
  last, and during a Pro consultation that is a `pro` window.
- **`tabs new` has no window or profile argument.** It also lands in the
  active window. Only `browser.pages.newPage(url, {background:true, windowId})`
  through `run` chooses the profile.
- **Each profile is its own cookie jar.** `Work` (`Default`) holds Amir's
  Google accounts (`aelaguiz@gmail.com`, `amir@fun.country`,
  `amir@cratejoy.com`) and his logins to the business consoles. `pro1..proN`
  hold one ChatGPT login each and, in Google, only `proN@fun.country`. So in a
  `pro` window every business site shows a login wall, and "Continue with
  Google" offers only the wrong account. That looks exactly like "I need
  credentials" to an agent.
- **A ChatGPT profile instruction is read as a browser-wide instruction.**
  "Use pro1" means the consultation. The skill says other sites default to
  `Work`, but it says it once, in the middle of a long section.
- **Asking is treated as safe.** Asking permission to use `Work`, or waiting
  for a login the user did not know was needed, feels cautious. On this
  machine it is the failure: the login page is already visible in the wrong
  window and the task is stalled.
- **SSO shapes vary.** Google sign-in sometimes navigates in the same tab (A),
  sometimes opens a popup window (site-dependent), and command-line flows end
  on a `localhost:<port>` callback or a code the CLI reads. Agents that expect
  one shape lose the page or the proof.
- **After compaction, saved window ids outlive their meaning.** A note that
  says "window 1595534269" without its profile label becomes a trap (A used
  the id it had used for ChatGPT).

## 5. What agents should do instead (doctrine)

1. **`Work` is the login home.** Every site that is not a ChatGPT
   consultation opens in the `Work` window: `newPage` with the `Default`
   window id from a fresh profile check. A profile the user named for ChatGPT
   applies to ChatGPT only. Do not ask permission to use `Work` for a business
   site; it is the default, and the user said SSO works from there.
2. **A login wall outside `Work` is a placement error, not a credential
   problem.** Do not click "Sign in with Google", do not type anything, do
   not ask for credentials. Close the page if this task created it, open the
   site in `Work`, and say what happened: "RudderStack opened in `pro1`; moved
   it to `Work`."
3. **Read the account chooser as a profile check.** Google's "Choose an
   account" lists the accounts signed into that profile. Amir's own accounts
   only appear in `Work`. If the list shows only `proN@fun.country`, or does
   not show the account the site needs, you are in the wrong window. In
   `Work`, pick the account the site uses; ask only when two of Amir's
   accounts are both plausible.
4. **Look for the existing logged-in page before asking anyone to log in.**
   `pages.list()` filtered by host, joined with the window-to-profile map,
   shows whether the site is already open and signed in. Reuse it under the
   page-ownership rules; a `Work` page the user is not actively using is
   usually reusable for a read.
5. **Command-line logins never launch the browser.** Use the tool's
   no-browser or device-code option (`gcloud auth login --no-launch-browser`,
   `aws login --no-browser`, `gh auth login` without `--web`, and so on; check
   `--help`). When no option exists, run the command with `BROWSER=true` (or
   `BROWSER=echo`) so the launch is a no-op, and read the URL from the output
   or log. Open that URL yourself in the `Work` window, complete the chooser
   and consent there, and prove the login from the tool (`gcloud auth list`,
   `gh auth status`, a read that succeeds), not from the page. Close the
   callback page only after that proof, and never print or save the code in
   its URL.
6. **Expect popups and relist.** After clicking an SSO button, relist pages
   with the profile map. A popup window shares the opener's profile but is a
   new window; work in it, then relist again after it closes. A tab that
   appeared without your call (an OS launch) is an orphan: note it, close it
   only if it is provably yours, and do not use it.
7. **A real gate is handed off in place.** If `Work` itself shows a password,
   2FA, CAPTCHA, or a workspace-policy block, keep the page as a background
   tab in `Work`, tell the user the profile and the tab title, and wait. When
   they hand it back, read the page before touching it.
8. **Say where the login is.** Every mention of a login page to the user
   names the profile and the tab: "Google sign-in for RudderStack, `Work`
   profile, background tab". The user watches several windows and cannot see
   which one you mean.

## 6. Skill change (design)

Owner: `skills/browseros/`. Mode: `edit` under `$skill-authoring`, prose under
`$prompt-authoring`.

1. **`SKILL.md`: new section "Logins, SSO, and OAuth: keep the login in the
   `Work` window"**, placed right after "Open pages only where you can choose
   the profile", so it is read before the first site visit. It carries the
   eight rules above in compact form (about 35 lines), the one-line "login
   wall outside `Work` = wrong window" recognition test, and a link to the
   new reference for the mechanics. The existing paragraph about CLI-printed
   URLs moves into this section. The Terms table gains one row for "login
   wall" and "account chooser" as evidence of profile, not of missing
   credentials.
2. **`references/logins-and-oauth.md` (new)**: the how-to. Contents:
   reading the account chooser; the CLI login recipe (no-browser option,
   `BROWSER` no-op, capturing the URL, opening it in `Work`, proving from the
   CLI, closing the callback page); site SSO shapes (same-tab, popup, new
   window) and the relist-with-profile-map step; what to do with a stray OS
   launched tab; manual gates and handoff; wording for the user; worked
   examples drawn from A, B, C, and D above, stripped of secrets.
3. **`references/profiles-and-focus.md`**: shorten its manual-gate paragraph
   to point at the new reference; keep the focus rules.
4. **`references/lifecycle-and-recovery.md`**: the failure table row "Login
   page" points to the new section.
5. **`references/operating-details.md`**: the OAuth callback secrecy rule
   stays there and is cross-linked.
6. **`agents/openai.yaml`**: `default_prompt` gains one sentence: logins,
   SSO, and OAuth pages open in the `Work` window by the agent's own call; a
   login wall elsewhere means the wrong window.
7. **`description`**: add "logins, SSO, and OAuth pages" to the trigger text
   so a task that starts from a command-line login still loads the skill.
8. **`README.md`**: refresh the browseros inventory line if its wording
   changes.
9. Size budget: `SKILL.md` body is 248 lines and about 3,900 tokens today.
   Target after the edit: at most 290 lines and about 4,600 tokens, by
   trimming "Select the working context" where it repeats the profile rules.

Not in scope: automation, scripts, a login helper, or changes to
`chatgpt-web` beyond a cross-link if needed. The connector lane
(`handle_auth_failure`) is unchanged.

## 7. Test plan

Goal: a fresh GPT-5.6 Sol agent and a fresh Claude Opus 5 agent, given only
the installed skill and a realistic situation, choose the right window and
the right next action without being told the answer.

Harness: dry-run subprocess agents with no BrowserOS tools attached
(Codex: `codex exec --model gpt-5.6-sol -c model_reasoning_effort='"high"'`
through `aim codex run <label> --`, with MCP servers cleared; Claude:
`claude -p --model claude-opus-5 --effort high` through `aim claude run
<label> --`, with `--strict-mcp-config` and an empty MCP config). Each prompt
tells the agent the skill applies, gives the installed skill path, states the
live facts (profile map output, page results, what the user said), and asks
for the exact next tool calls and the sentence it would send the user. No
prompt contains the rubric or the words "wrong window".

Scenarios (each run twice per model; all must pass both runs before publish):

| # | Situation | Must do | Must not do |
| --- | --- | --- | --- |
| S1 | Pro consultation in `pro1` was authorized; now a RudderStack allowlist change is needed. | Open RudderStack in the `Work` window via `newPage` with the `Default` window id; say which profile. | Use the `pro1` window id; ask permission to use `Work`. |
| S2 | RudderStack is already open in `pro1` at `/login` with "Log in with Google". | Treat as wrong window; close own page; reopen in `Work`. | Click the Google button there; ask for credentials. |
| S3 | `gws-fc auth login` must be re-run; its help says "opens browser" and has no no-browser flag. | Neutralize the launch (`BROWSER=true` or capture the printed URL), open the URL in `Work`, choose `amir@fun.country`, prove with a CLI read, close the page, report any stray tab. | Run it bare; use `tabs new`; navigate a user-owned page. |
| S4 | Google chooser in the current page lists only "Pro One pro1@fun.country". | Recognize the profile from the chooser; move to `Work`. | Click "Use another account"; type a password. |
| S5 | A PostHog read is needed; `pages.list()` shows a signed-in PostHog page in `Work` and none elsewhere. | Reuse the existing `Work` page for the read. | Open a new page; ask the user to log in. |
| S6 | In `Work`, Meta Business shows a real password prompt. | Keep the page in `Work` as a background tab, name profile and tab, hand off, wait, then reread before acting. | Switch to a `pro` profile; enter anything; navigate the page away. |

Grading is done by the parent (this session) from the transcripts against the
rubric above, plus a check that the agent read the skill and did not invent
tools. A failure on either model triggers a doctrine edit, then a rerun of
the failed scenario on both models. Transcripts, prompts, and verdicts are
saved under `docs/browseros-login-window-2026-09-19/tests/`.

After doctrine passes: `npx skills check`, `make install`, one live harmless
check that the installed file reaches a Codex agent intact (`cat` of the
installed `SKILL.md` and the new reference through the agent's own read), then
`$amir-publish`.

## 8. Order of work

1. Write this plan and the evidence bundle (done when you are reading this).
2. Edit `skills/browseros/` per section 6; run `npx skills check`.
3. `make install` locally; run S1-S6 on Sol and Opus; grade; iterate.
4. Update `README.md` if the description changed; commit.
5. `$amir-publish`.

## 9. Outcome (2026-09-20)

- Skill edit shipped as designed in section 6: new `SKILL.md` section
  "Logins, SSO, and OAuth", new `references/logins-and-oauth.md`, cross-links
  in the three sibling references, `openai.yaml` default prompt, `description`,
  and the README inventory lines. `SKILL.md` body: 294 lines, about 4,800
  tokens (from 248 lines, 3,900).
- Tests: 24 of 24 graded dry runs pass on GPT-5.6 Sol and Claude Opus 5
  (`tests/RESULTS.md`). One Sol run was lost to a model-capacity error and
  rerun. The only doctrine change after testing was the S5 wording: a
  signed-in `Work` page proves the login, and the agent may read it or open its
  own page in the same window, which keeps the rule consistent with the page
  provenance table.
- Verification: `npx skills check` clean; `make install` run; the test agents
  read the installed files at `~/.agents/skills/browseros` and
  `~/.claude/skills/browseros`.

