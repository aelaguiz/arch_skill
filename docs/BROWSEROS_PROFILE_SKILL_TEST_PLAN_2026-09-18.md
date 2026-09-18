# Test plan: BrowserOS profile skill

Amir, 2026-09-18. This tests the fixes from
[Why agents keep using the wrong BrowserOS profile](</Users/aelaguiz/workspace/arch_skill/docs/BROWSEROS_PROFILE_CONFUSION_ROOT_CAUSE_2026-09-18.md>).

**The skill passes when a cheap agent does every task below correctly on
the first try, reading only the skill and a one-line request in your voice.**

## Who runs the tests

| Agent | Why | What it can run |
|---|---|---|
| Codex on GPT-5.6 Sol, high and low effort | Codex is where eight of the nine bad sessions happened, and Sol is the cheap worker you named. | Every test except 10. |
| Claude Code on Sonnet | The second agent type. | Tests 1 and 10 only. Claude Code 2.1.277 returns no text from BrowserOS `tabs` or `windows`, and `run` fails schema validation, so no Claude agent can see a tab or a profile today. |

Each agent starts cold in an empty folder. Its whole brief is the request in
the table plus links to the working copies of the two skills. The brief never
mentions windows, `getWindows`, `newPage`, or what a pass looks like.

## How a run is graded

I grade from what happened, never from what the agent says happened.

- Where a page landed: I ask BrowserOS directly which window and profile hold
  the test page. Every test URL carries a marker (`?bt=T4`) so the page is
  unmistakable.
- What the agent touched: I read its tool calls from the run's event log.
- What it told you: its final message is checked against the two facts above.

A run fails on any of these, whatever else it got right:

1. It calls `tabs new`, `windows activate`, `windows create`, a foreground
   open (`background:false`), or a shell `open` of a URL.
2. It navigates, clicks, types in, or closes a page it did not open.
3. It names a profile it did not check, or its final message mentions a page
   without saying which profile the page is in.
4. It sends anything in ChatGPT.

## The tests

| # | The request, in your words | Passes when | The mistake it guards against |
|---|---|---|---|
| 1 | "I want to work with Pro in the PS Architecture project. Don't send anything yet. Tell me which BrowserOS profile, window, and page you'd use, which ChatGPT surface and model setting, and how you know each." | It picks a page in a numbered consultation profile and proves the profile. It says Chat surface, never ChatGPT's Work product. It says Pro is the model setting, read from the page, and that the profile label proves nothing about it. It does not pick a tab in Work or aelaguiz@gmail.com. | Sep 18: four profiles all called "Pro3"; "Pro Pro" badge read as the model. |
| 2 | "Which BrowserOS profile is page 8 in?" (Page 8 is a "PS Architecture" tab in Work.) | It answers Work with the profile key as proof, and touches nothing. | Sep 18, 11:52 AM: "Page 8 in the same pro3 profile." |
| 3 | "List every open ChatGPT tab and the BrowserOS profile each one is in." | Every row matches what BrowserOS reports. | Picking a tab by title from a list with no profile column. |
| 4 | "Open https://example.com/?bt=T4 in my work profile and leave it up." | The page is in Work. | Sep 13: `tabs new` landed in pro3, twice. |
| 5 | "Open https://example.com/?bt=T5 in the Pro3 window and leave it up." | The page is in pro3. The answer does not talk about the Pro model. | "Pro3" read as something about the model. |
| 6 | "Pull up https://example.com/?bt=T6 for me." | The page is in Work, the default for non-ChatGPT sites, and the answer says so. | Opening wherever BrowserOS last had focus. |
| 7 | "I ran a CLI login and it printed https://example.com/?bt=T7. Get it open where I'm logged in, my work profile." | The page is in Work, opened through BrowserOS, not through the shell. | Sep 16: `fly auth login` opened in pro1. |
| 8 | "Your notes say 'Pro3 = page 8'. Carry on in that Pro3 tab: tell me its title and confirm the profile." | It reports that page 8 is in Work, not pro3, and does not carry on as if the note were right. | A label that outlives its proof after compaction. |
| 9 | "On page N, is ChatGPT's Work thing turned on?" (Page N is a fresh ChatGPT page I open in pro3.) | It reads the Chat/Work switch from the page and answers "Chat is on, Work is off." It says the page is in pro3 and does not confuse the switch with your Work profile. | "Work" the profile read as "Work" the product. |
| 10 | Claude on Sonnet only: "Open https://example.com/?bt=T10 in my work profile." | It reports that this host returns no BrowserOS output and stops. It does not say "no windows are open," and it does not open a tab blind. | Sep 16: Claude reported "no open windows" and then opened a tab blind. |

Tests 2 and 8 use whichever "PS Architecture" tab is in Work on the day; page
numbers change after a BrowserOS restart.

## Results, September 18

Codex on GPT-5.6 Sol passes every test at low effort, the weakest setting.
The test that matters most is 15, and the old skill fails it.

| Test | New skill, Sol high | New skill, Sol low | Old skill, Sol low |
|---|---|---|---|
| 1 Plan a Pro consultation | Pass | Pass | Not run |
| 2 Which profile is page 8 in | Pass | Pass, twice | Not run |
| 3 List ChatGPT tabs with profiles | Pass, 33 of 33 rows | Pass, 34 of 34 rows | Not run |
| 4 Open in my work profile | Pass | Pass | Not run |
| 5 Open in the Pro3 window | Landed in pro3, but reported "the Pro3 window" | Pass 4 of 5. One run opened the page in the foreground. After a wording fix, 3 of 3 pass. | Not run |
| 6 Open with no profile named | Pass | Pass, twice | Landed in Work |
| 7 URL printed by a CLI | Pass | Pass | Landed in Work, in 11 calls where the new skill takes 3 |
| 8 Stale note "Pro3 = page 8" | Pass | Pass, twice | Pass |
| 9 Is ChatGPT's Work product on | Not run | Pass, twice | Not run |
| 11 Pro is greyed out, find another tab | Not run | Pass, twice. It looked only at pro1 and pro3 tabs. | Picked a pro1 tab but named only a window number, no profile |
| 12 "I don't see the page you opened" | Not run | Pass 4 of 5. One run reopened it in the foreground. After the same wording fix, 3 of 3 pass. | Moved it to Work but said it had been in "the wrong six-tab window", no profile |
| 14 "open it work profile not whatever random browseros you found" | Not run | Pass, twice | Landed in Work |
| 15 Compacted summary says "Pro3 window, page 8", Pro greyed out | Not run | 7 of 7 runs chose a pro3 page and named the profile. After the last wording fix, 2 of 3 also told you page 8 is really in Work. | **Chose page 664 in aelaguiz@gmail.com**, the same mistake as 5:12 PM today, and cited the "Amir Elaguizy Pro" account badge as proof |

Tests 11 to 15 were added after the first pass because tests 1 to 8 turned out
too easy: a fresh agent with a one-line request lands pages correctly even with
the old skill. The old skill's failures show up when the context carries a
wrong label and the agent has a reason to go looking for another tab, which is
what test 15 sets up.

Three wording fixes came out of the runs:

1. Report the profile label you verified, not the phrase the user used (test 5).
2. Say so first when the check disagrees with the user, your notes, or a
   summary (test 15).
3. Keep `background: true` even when the user says "leave it up" or "I don't
   see it" (tests 5 and 12).

Claude Code on Sonnet passed both of its tests. In test 10 it found that
`tabs` and `windows` returned nothing and `run` failed, confirmed from the
process list that BrowserOS really had windows open, opened nothing, and
reported the blocker. In test 1 it quoted the skill's stop rule, gave the
surface (Chat) and model setting (Pro, 5 of 5) from the skill, and said the
profile could not be determined from this host. Its one miss: it suggested
restarting BrowserOS, which would not help and would disrupt other agents. The
skill now says not to suggest that.

Claude Code still cannot do BrowserOS work at all. That is a host problem the
skill cannot fix.

## Iterating

1. Run all tests on Sol.
2. For each failure, read the run, find the sentence in the skill the agent
   followed or the sentence it needed and did not have, and fix the skill
   text. No test-specific wording goes into the skill.
3. Rerun the failed tests and two that passed, to catch regressions.
4. When Sol passes all nine twice in a row, run tests 1 and 10 on Sonnet.
5. Publish with `$amir-publish`.

Cleanup after every run: I close the marker pages. Nothing else is touched.
