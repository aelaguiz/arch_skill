# Why agents keep using the wrong BrowserOS profile

Amir, 2026-09-18. All times are Central.

**Agents do not know which profile they are in, and they name one anyway.**
Nothing an agent normally looks at shows the profile: not the tab list, not
the window list, not the page. Finding out takes two sources joined by hand,
about 15 calls when the agent has forgotten how. So agents go by a tab's
title, by ChatGPT's account badge, or by the label you gave them at the start
of the task. In all eight real mistakes below, the agent stated a profile it
had not checked. One wrote "in the correct Work profile" twice while sitting
in pro3.

They land in the wrong place three ways, most common first:

1. Reusing a tab that was already open, picked by its title.
2. `tabs new`, which has no window argument and opens wherever BrowserOS last
   had focus.
3. A URL opened by a command-line login such as `fly auth login`, which macOS
   hands to whichever BrowserOS profile was used last. This happened once in
   the sessions I read.

`browser.pages.newPage(url, {windowId})` is the only call that knows about
profiles. It landed correctly every time an agent used it, including 45 out of
45 times in one session. The skill's entry file describes path 2, recommends
path 1, says nothing about path 3, and names the safe call only in a reference
file.

Three things make it worse. Agents lose their window-to-profile map at every
context compaction but keep the word "Pro3". psagentspace carries a September 6
copy of the skill with none of the profile rules, and 44 of your 49 prompts
link to it. And both of your profile labels are ChatGPT's own words: "Work" is
also a ChatGPT product, and "Pro" is also the model and the account badge.

You asked whether the instructions are confusing. Yes, in four specific ways,
listed under Cause 2. The agent in the session you named told you "the
instructions are clear." The traces do not support that.

## I read thirteen corrections. Eight were real targeting mistakes.

| When | Session | What you said | What had happened |
|---|---|---|---|
| Sep 18, 5:13 PM | [01a0b4c0, Android CPI](</Users/aelaguiz/.codex/sessions/2026/09/18/rollout-2026-09-18T08-41-45-01a0b4c0-6f61-7531-9653-bb762e741875.jsonl>) | "now you're in the Elaguizy browser OS profile" | Reused tabs. Four wrong profiles in one day. Details in the next section. |
| Sep 18, 1:58 PM | [01a0b41b](</Users/aelaguiz/.codex/sessions/2026/09/18/rollout-2026-09-18T05-41-39-01a0b41b-8b6c-7273-bece-1019a0bdc2c9.jsonl>) | "use a diff browseros window if you must but pro is available in some of them" | `tabs new` twice, both landed in Work. The agent believed the MCP `session` handle picks the profile. It found pro1 rate limited and stopped, although its own tab sweep showed 6 Pro in pro2 and pro3. The sign-off it finally got came from aelaguiz@gmail.com. |
| Sep 18, 10:15 AM | [01a0b4ac](</Users/aelaguiz/.codex/sessions/2026/09/18/rollout-2026-09-18T08-19-51-01a0b4ac-6226-7903-a44b-2b5af2a75b3f.jsonl>) | "you're just getting confused by the browser OS profile name versus the GPT-6 Astra 6 Pro model" | It chose its window because ChatGPT's account button read "Pro Pro", sent on the wrong model once, then declared every profile Pro-disabled without opening pro2. 42 minutes and 151 tool calls passed between your two corrections. |
| Sep 16, 3:49 PM | [01a0aa04](</Users/aelaguiz/.codex/sessions/2026/09/16/rollout-2026-09-16T06-40-34-01a0aa04-c448-7741-9b63-45c8553b9601.jsonl>) | "you keep popping it up in the wrong fucking Browser OS profile" | It read "work profile" as a Google Chrome profile and launched Chrome. Then `fly auth login` opened its URL in the pro1 window. |
| Sep 16, 3:47 PM | same session | "open it work profile not whatever random browseros you found" | The tab was in Work, by luck. The agent had navigated your first tab without checking it and told you "sign in to Fly in BrowserOS tab 1" with no profile name. |
| Sep 13, 7:11 PM | [01a0955b, Cratejoy CircleCI](</Users/aelaguiz/.codex/sessions/2026/09/12/rollout-2026-09-12T06-23-24-01a0955b-9d77-74a0-95a0-20684c721df2.jsonl>) | "you keep opening stuff in the wrong browser OS window. I'm using the work profile." | Same `tabs new` mistake as 24 minutes earlier, after a compaction. It landed in pro3, clicked "Log in with GitHub" there, wrote "in the correct Work profile" twice, and asked you to log in. |
| Sep 13, 6:47 PM | same session | "I think you're opening it in the wrong profile" | `tabs new` with `background:false` landed in pro3. The day before, this agent had used `newPage` with the Work window correctly. After 35 compactions it had switched to `tabs new`. |
| Sep 9, 6:36 AM | [01a06dd9, Cratejoy](</Users/aelaguiz/.codex/sessions/2026/09/04/rollout-2026-09-04T14-16-32-01a06dd9-e9b4-7fa3-affd-82bda773cb27.jsonl>) | "You're using a rate-limited Pro 1 account." | It knew it was in pro1. It had reused one page by number for 15 hours and sent with the model pill reading "Medium", treating the "Pro Pro" account badge as the model. Your broadcast about Pro2 never reached this session. |

Five corrections were not targeting mistakes:

| When | Session | What happened |
|---|---|---|
| Sep 16, 3:55 PM | [Claude Code 64547480](</Users/aelaguiz/.aimgr/claude-homes/pro3/.claude/projects/-Users-aelaguiz-workspace-psagentspace/64547480-df8e-46c4-85af-5d810bd3cc34.jsonl>) | The agent had opened nothing. Claude Code 2.1.273 dropped the text of every BrowserOS result, so `tabs list` came back empty and the agent reported "no open windows." |
| Sep 16, 8:02 AM | [01a09fa4](</Users/aelaguiz/.codex/sessions/2026/09/14/rollout-2026-09-14T06-19-05-01a09fa4-6248-7c03-96ec-921af4bcc3e7.jsonl>) | False alarm. Buildkite was in Work. A sub-agent's 403 came from an API token, and you guessed wrong window. |
| Sep 15, 3:18 PM | same session | The agent ran the review in pro1 on purpose, because the skill bans Work for ChatGPT and you had said "pro1 is open." Your thread lived in Work and you wanted it used. Work then hit its limit at 11:06 PM, and the review stalled seven hours while the agent waited for permission to go back to a numbered profile. |
| Sep 9, 6:56 AM | 01a06dd9 | "Try Pro 2" was an unblock. The agent was already in pro2, refusing to send because the pill said "6 Pro" and not "GPT-6 Astra". |
| Sep 7, 8:08 AM | [01a07858](</Users/aelaguiz/.codex/sessions/2026/09/06/rollout-2026-09-06T15-10-48-01a07858-4ee2-70e1-9c4a-487755718741.jsonl>) | You said "use Pro 2", the agent proved it was in pro2, and you switched it to Pro1. pro2 was a new account with no Google Drive connection. |

## The session you named touched four profiles and called all of them "Pro3"

You told it "Pro3 brower os window is up and is all yours" at 8:44 AM.

| Time | What the agent did | What it said | Profile the tab was really in |
|---|---|---|---|
| 8:53 AM | Mapped windows to profiles correctly, then sent the first brief in page 606. | "attached to the PS Architecture Pro3 chat" | pro3. Correct. |
| 10:36 AM | You said Meta and AppsFlyer are in Work. It opened Events Manager with `newPage` aimed at the Work window. | Nothing about profiles. | Work. Correct. |
| 11:12 AM | Found Pro greyed out in one project composer and sent the brief on Latest, then on GPT-5.6 Sol. | "The Pro choice is disabled in the Pro3 ChatGPT profile" | pro3, but the claim was false. You posted screenshots of 6 Pro working in pro3 at 11:51 AM. |
| 11:52 AM | Opened the model picker and started a new chat in page 8, an existing "PS Architecture" tab. | "Page 8 in the same pro3 profile currently shows 6 Pro active" | **Work.** You did not catch this one. |
| 11:54 AM to 12:08 PM | Sent the 6 Pro rerun from page 451, another existing tab, waited 5 minutes 42 seconds, and filed the chat into that account's PS Architecture project. | "6 Pro is active in the pro3 BrowserOS profile. I reran the analysis using 6 Pro" | **aelaguiz@gmail.com.** You did not catch this one either. |
| 5:10 PM | Drafted the next brief and attached six files in page 113. | "Pro3's current composer is showing GPT-6 Pro disabled" | **pro1.** |
| 5:12 PM | Snapshotted five look-alike tabs, found "6 Pro" on page 664, moved the draft and the six files there. | "checking the other already-open consultation window" | **aelaguiz@gmail.com.** You caught it at 5:13 PM. |

Between 11:51 AM and 12:11 PM the agent made zero profile checks. It chose
pages 8 and 451 from the flat tab list because their titles said "PS
Architecture".

Rebuilding the map after your correction took 3.5 minutes and about 15 calls,
including four passes over the `Local State` file, a process listing, and a
search of the skill for the word `getWindows`. The recipe works. The agent had
forgotten it.

## Cause 1: no list shows the profile, and the tabs look identical

`tabs list` returns page number, URL, title. `windows list` returns window IDs
and tab counts. Neither names a profile. The profile appears only in
`Browser.getWindows` as a directory key such as `Profile 15`, and the label you
typed ("pro3") appears only in the `Local State` file on disk. An agent must
join the two by hand. `pages.getInfo` returns a window ID and no profile.

At 5:11 PM the named session had 78 open pages. 33 were ChatGPT tabs across
five profiles: Work 11, pro1 12, pro2 4, pro3 4, aelaguiz@gmail.com 2.
Fourteen were titled "PS Architecture": six in Work, seven in pro1, one in
aelaguiz@gmail.com, none in pro3. Your standard instruction is "work with Pro
in the PS Architecture project." Searching the tab list for that title lands in
Work or pro1 thirteen times out of fourteen.

You copied the PS Architecture project into each account, so the project IDs
differ (`6a89c1ca` in Work, `6a9816e4` in pro1, `6aaa8463` in
aelaguiz@gmail.com), but no agent knows which ID belongs to which account.

With no profile in the tool output, agents reach for what the page shows. Two
sessions used ChatGPT's account button, which reads "Pro Pro, open profile
menu" in your Pro accounts, as proof of both the profile and the model. It is
neither. One session believed the MCP `session` handle selects the profile.

The BrowserOS server's own instructions push the blind path. They say "Start
with tabs action=list to find page ids" and suggest cloning a tab with
`tabs new`.

## Cause 2: the skill points at the blind calls

These are the four ways the instructions themselves mislead.

**The entry file describes `tabs new`.**
[SKILL.md](</Users/aelaguiz/workspace/arch_skill/skills/browseros/SKILL.md>)
says "request one normal background tab in the verified existing window with
`hidden=false` and `background=true`." Those are `tabs new` flags, and
`tabs new` cannot target a window. `newPage` with a `windowId` is named only in
[profiles-and-focus.md](</Users/aelaguiz/workspace/arch_skill/skills/browseros/references/profiles-and-focus.md>)
line 22. The warning that `tabs new` has no window argument sits at line 153 of
that reference. The same reference lists "`tabs new` with `background=false`"
as an approved foreground route, which is the exact call that put CircleCI in
pro3 twice.

**It prefers reuse and gives reuse no check.** "Reuse one compatible,
current-agent-controlled page" is the first instruction. The warning is a
principle: "Matching titles, project names, or the active window do not
establish the account." There is no call to run. Every wrong-profile event in
the named session was a reused tab.

**It says nothing about URLs opened outside BrowserOS.** `fly auth login`,
OAuth device flows, and `open <url>` all hand the URL to macOS, and BrowserOS
opens it in the last-used profile.

**It names arguments the live tools do not have.** The live `tabs` tool takes
`action`, `url`, `background`, `page`, `session`. There is no `hidden`, and
`windows` has no `set_visibility`. An agent that checks the schema sees the
skill is out of date.

## Cause 3: the map dies at every compaction, the label does not

| Session | Compactions | What was lost |
|---|---|---|
| 01a09fa4 | 66 | It reread `SKILL.md` 45 times and called `Browser.getWindows` 63 times to stay correct. |
| 01a0955b | 35 | The `newPage` habit. Your first correction lasted 24 minutes. |
| Named session | 17 in 8.5 hours | The map was in context at 8:59 AM and gone from the two compactions before the 5:10 PM mistake. The word "Pro3" was in all 17. |
| 01a06dd9 | Skill reread, then compacted 100 seconds later | The rotation rule it had just read. |

The skill says "keep it in the task notes." That is not a file, so after a
compaction there is nothing to reread. Your "yes" and "pro1 is open" replies
survived compaction in session 01a09fa4. The questions they answered did not.

## Cause 4: psagentspace agents read a September 6 copy of the skill

The stale copies described here were deleted on September 18, after this
analysis.

| Path | Lines | Last changed | Profile rules |
|---|---|---|---|
| `~/.agents/skills/browseros` (installed from this repo) | 157 | Sep 18 | Current. |
| `psagentspace/.agents/skills/browseros` | 342 | Sep 6 | "Default to the Work profile." No Pro profiles, no Work ban for ChatGPT, no "label is not the model", no `profiles-and-focus.md`. |
| `psagentspace/skills/browseros` | 342 | Sep 6 | Same file as the row above. |
| `psagentspace/.claude/skills/browseros` | symlink | Sep 6 | Points at the stale copy. |

Every profile rule you asked for landed after September 6. Of your 49 prompts
since August 14 that link a BrowserOS skill file, 44 link the psagentspace copy
and 5 link the installed one. Codex in psagentspace lists two skills named
`browseros`, with descriptions cut to four characters. Four of the six Codex
sessions above had the stale copy injected or read it first.

This is a contributor, not the main cause. Session 01a0955b read the current
skill 20 seconds before it called `tabs new`.

## Cause 5: you cannot see which profile the agent is in

Agents report "page 606", "tab 1", or nothing. In session 01a09fa4 the agent
named "Pro1" in its status lines until September 14 at 9:50 PM, then stopped.
You corrected it the next afternoon by watching the screen, and the morning
after that you guessed wrong about Buildkite. In session 01a0aa04 the tab was
in Work and you still assumed it was random, because the agent asked you to
sign in to "tab 1".

Both agents in that pair also announced "verified Work" without ever reading a
profile key. They inferred it from a window ID.

## Cause 6: your profile labels are ChatGPT's own words

Both labels you typed for browser profiles are also controls inside ChatGPT.

**"Work" is a browser profile and a ChatGPT product.** Every new ChatGPT chat
has a switch named "Select chat surface" with two options, Chat and Work. The
Work surface is a separate ChatGPT product that cannot run the Pro consultation
you want, in any browser profile. Agents read that switch about 1,500 times
across 100 September sessions, and the page snapshot lists both options without
saying which one is on. An agent has to query the page's `aria-checked` value
to find out.

The skills now hold two "never Work" rules with different meanings. The
September 2 ChatGPT web change says never send from the Work surface. The
September 13 change says never use the `Work` browser profile for ChatGPT.
Both are true, and both shorten to "never Work for ChatGPT." Your prompts then
say "work with Pro in this session work profile."

The BrowserOS skill, which owns profiles, never mentions the Work surface. It
does say "ChatGPT work uses only the existing consultation profiles; `Work` is
never a fallback for it," which puts the product's name two words away from
the profile's. Agents copied that phrasing into saved notes on September 8:
"ChatGPT work uses the Pro2 BrowserOS window." One agent's review receipt reads
"Profile/surface: Work, Chat, Latest / 6 Pro", meaning Work profile and Chat
surface. Two later sessions reread that file. Nothing on the line says which
"Work" it is.

On September 16 an agent gave the word a fourth reading. You said "open it
work profile not whatever random browseros you found," and it launched Google
Chrome's work profile.

I found no September session that sent from the Work surface. The September 2
commit says one did before then.

**"Pro" is three things too:** the model ("work with Pro"), the profiles ("Pro3 window"), and the
account badge ("Pro Pro"). Until the September 18 commits the ChatGPT web skill
also described a model picker that does not exist: it told agents to find a
literal "Pro" entry in the model list and said a "5/5" power level "is not
Pro." In the live page Pro is the top Power position and the list entry is
disabled. Two sessions read that disabled entry as "Pro unavailable."

Once an agent believes Pro is unavailable where it stands, it looks for any tab
that shows "6 Pro" and adopts it. That is how the named session reached
aelaguiz@gmail.com twice. The new "no Pro, no send" rule is right, and it gives
agents a stronger reason to do this.

## Cause 7: the skill describes a simpler machine than yours, and the Work rule keeps moving

The skill expects "`Work` and any number of ChatGPT consultation profiles,
labeled `Pro 1`, `Pro2`." BrowserOS has 34 profiles. The labels are lowercase
with no space (`pro1` to `pro17`). `Work` is the directory `Default`. There are
also `aelaguiz@gmail.com`, `amir@fun.country`, `amir.elaguizy@fun.country`,
`amir @ cratejoy`, and one per agent account (`boss`, `coder`, `growth`).

The skill never mentions `aelaguiz@gmail.com`. It has a ChatGPT login, a PS
Architecture project, and 6 Pro, and you have sent agents there on purpose
("use the aelaguiz@gmail.com browseros profile", September 16 and 18). Three
sessions used it today. One of them was the one you objected to.

You have called Work "work profile", "my Browser OS profile", "the root
profile", and "my amir@fun.country browseros profile". A different profile is
literally labeled `amir@fun.country`.

Your rule about Work for ChatGPT changed five times in twelve days:

| Date | What you said |
|---|---|
| Sep 4 | "you can use the Work profile" for ChatGPT. |
| Sep 5 | "you can use work or pro1 either works". |
| Sep 8 | Broadcast to eight sessions: "use the Pro2 browseros window right now for chatgpt, pro1 is rate limited". Same night: the skill should rotate through "(work, pro1, pro2, pro3)". |
| Sep 13 | "stop using my browser OS work profile." The skill now says never. |
| Sep 15 | "work with Pro in this session work profile" with a Work chat URL, in two sessions. |
| Sep 16 | "use browseros and chatgpt-web against the Work profile". |

Each was reasonable on its day. The skill's "never" now contradicts what you
ask for, and that contradiction cost seven hours in session 01a09fa4.

## What would fix it, most effective first

Every fix here is clearer skill text. None is a script, runner, hook, or
validator.

1. **Show agents, in `SKILL.md`, how to answer "which profile is this page
   in?"** A short worked example the agent types into BrowserOS `run` itself,
   with what the answer looks like. Say when to ask: before the first action
   on any page the agent did not open in this task, after every compaction,
   and before every send. Today agents rediscover the method in about 15 calls
   and mostly skip it.
2. **Write the map to a file and name the profile in every status line.**
   "pro3, page 606" instead of "page 606". The file survives compaction, and
   you can see a wrong profile before anything is sent.
3. **Make `newPage` with a window the only way to open a URL, and say so in
   `SKILL.md`.** Ban `tabs new`. Cover command-line logins: copy the URL the
   CLI prints and open it with `newPage` in the right window.
4. **Delete the two stale copies in psagentspace** so `$browseros` resolves to
   the installed skill. Done September 18: `psagentspace/skills/browseros`,
   `psagentspace/.agents/skills/browseros`, and the `.claude/skills/browseros`
   symlink are removed. The tracked copy shows as an uncommitted deletion in
   psagentspace.
5. **Say what each colliding word means, in the skills.** Started September
   18: `skills/browseros/SKILL.md` has a Terms table and
   `skills/chatgpt-web/SKILL.md` opens by splitting "Pro" and "Work". A rename
   would remove the collision at the source: `Work` and `pro1` collide with ChatGPT's Work surface and Pro
   model. Labels such as `amir-main` and `consult1` collide with nothing. The
   skill then lists which labels are consultation profiles, which ones need
   you to name them, and whether a chat URL from you overrides the ban on your
   main profile. Until a rename, the skills should always write "the `Work`
   browser profile" and "ChatGPT's Work surface", never the bare word.

One separate tool problem: Claude Code drops the text of BrowserOS results, so
Claude sessions cannot see tabs at all.

## Appendix: what I read

- Nine sessions with a profile correction from you between September 7 and 18:
  eight Codex, one Claude Code. For each: what you had said, which skill files
  the agent read and when, what profile discovery it ran, the exact call that
  put the page where it landed, what the agent claimed, and the recovery cost.
  The line-level notes for each session are in the run's scratch folder and
  are not kept.
- Your own prompts since August 14 from `~/.codex/history.jsonl` and each
  Claude home's `history.jsonl`: 182 mention BrowserOS or a profile.
- The live `tabs` and `windows` tool schemas, the BrowserOS `Local State`
  profile labels (labels and directory keys only), every installed copy of the
  BrowserOS and ChatGPT web skills, and the git history of both skills.
- [BrowserOS session failure modes, September 9](</Users/aelaguiz/workspace/arch_skill/docs/BROWSEROS_SESSION_FAILURE_MODES_2026-09-09.md>),
  which lists wrong-profile work as one failure among many and concludes the
  rules were already installed. It did not look at the psagentspace copy, at
  tab reuse, or at `tabs new`.
- A count over September's Codex sessions, best effort by text match: 396
  sessions called BrowserOS tools. 269 called `Browser.getWindows` at least
  once and 209 read `Local State` at least once, so at most 209 ever had both
  halves of the map. 106 had neither.
- Two things the traces could not show. Where `tabs new` lands is inferred
  from five observed landings, not from BrowserOS source. Codex reasoning is
  stored as titles only and compaction summaries are encrypted, so agent
  beliefs come from their messages.
