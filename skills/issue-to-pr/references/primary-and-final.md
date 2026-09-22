# Primary and Final: Reaching the Seats

Read before the first consultation of a run, and again when the user names or
renames a seat mid-run. The entry file says what each seat does; this file
says how to reach it, what context it starts with, how to hand it the
sources, and what to record.

Contents: [who holds which seat](#who-holds-which-seat),
[reaching Pro](#reaching-pro), [reaching another model](#reaching-another-model),
[continuing versus clean context](#continuing-versus-clean-context),
[sources without connectors](#handing-over-sources-without-connectors),
[receipts](#receipts).

## Who holds which seat

The user names seats in plain language at invocation: "primary Sol xhigh,
final Pro", "primary Fable 5.1 xhigh", "final Pro". Read the model and effort
exactly as named; do not upgrade, downgrade, or substitute, and do not treat
a profile name, a power number, or "the best available" as the model. A seat
named at invocation is a deliberate exact choice; a house default such as
Astra xhigh does not override it. If the effort word is not one the named
model offers (xhigh for a Claude model, say), use that model's nearest level
and say so in the receipt; that is reading the name, not substituting. A seat
the user did not name is GPT-6 Astra Pro. A seat renamed mid-run applies from
the next consultation; record the change in the worklog and carry it into
the goal, the unblocker charter, and active briefs. `epic-to-prs` names the
seats once for the epic; child issues inherit them.

## Reaching Pro

Pro is GPT-6 Astra with the literal `Pro` option, power 5 of 5, and Extended
thinking where offered, in ChatGPT's `Chat` surface, reached through
`$chatgpt-web` with `$browseros` applied. Use only the consultation profiles,
the BrowserOS profiles labeled `Pro 1`, `Pro2`, and so on; never the user's
`Work` profile, including as a fallback.

The seat is the model, not the profile. A label such as `Pro 1` is a name the
user typed for a browser profile; a page in it sends to whatever model its
picker holds, which can be ChatGPT's default. A consultation counts for the
Pro seat only when `$chatgpt-web`'s readings prove it: the picker's selected
model and `Pro` option read from the page before Send, and the model named
on the response turn after it. A review that went out on any other model is
not the seat's review, whichever profile it ran in: stop it, select `Pro`,
and resend it whole. When no composer offers Pro, the seat's consultation
waits. A plan, finding, or sign-off from a fallback model never fills the seat,
is never recorded as the seat's, and never makes a PR merge-ready.

Rate limits,
account switching, and delivery verification are `$chatgpt-web`'s rules.
Continue the run's thread for the seat, or the epic's thread when the issue
is inside an epic. When a switch moves the run to another consultation
profile, verify the new page, then close the pages the run created in the
profile it left; the entry file's Browser pages section owns when pages
close. Only after the consultation profiles' accounts are exhausted, report the
observed conditions, pause the blocked consultation, continue independent
work, and wait for the user to say Pro is back.

## Reaching another model

Read `../../_shared/agent-orchestration-policy.md` first; it owns native
versus external transport, starting context, isolation, and the return
contract.

Astra and Fable parents have their own rules, below. If you are not one of
them, or you are not sure, use your own native subagents on your own model
for every worker, reviewer, and seat except Pro, including a seat named for
another model, and say which model it ran on. Do not start an external agent
unless the user asks for an external one.

For an Astra or a Fable parent:

- A Claude model (Fable 5.1, Opus 5) on a Claude host is a native child at
  the named model and effort. On any other host it is an external Claude
  process through `$agent-delegate` at the exact model and effort.
- A Codex model (GPT-6 Sol, or GPT-6 Astra at an effort other than Pro) is
  an external Codex process through `$agent-delegate` at the exact model and
  effort. Not `$codex-review-yolo`: its `VERDICT:` footer is the anti-pattern
  the consultation templates remove.

Whatever the seat and whoever the parent, the brief is the family template
from `../../chatgpt-web/references/consultation-templates.md`, in the user's
voice, with the user's words verbatim and the sources whole. Where the
template says Pro, read the seat. Read the whole answer before acting on it;
the coordinator, not the seat, decides what is material.

## Continuing versus clean context

The primary as planner keeps one continuing session for the D back-and-forth
so the plan grows in one place. A review round (A or B) starts with a clean
context that has not seen the coordinator's reasoning, so it reads the PR
cold. The final's plan check (C) and PR review (A) each start clean, with the
primary's planning exchange or findings attached as files that say what
happened, placed after the ask so the final reads the plan or the PR itself
first, not inherited as conversation. For Pro, continuing means the run's thread and clean means a
new conversation in the same project; when the same Pro thread must carry
both, say in the brief which turn is the fresh read.

## Handing over sources without connectors

A native or external seat has no `@GitHub` or `@BigQuery`. Give it the
worktree path and branch, checked out at the pushed head with a clean tree
(verify the head matches the PR branch on origin before briefing); `gh pr
view` and `gh pr diff` output saved to files; the plan; the canonical requirements export; the issue as filed; the
user's words, dated; raw test output; and the repo's review policy files,
all by absolute path. Tell it to read the latest code in the worktree
itself. For a data question, save the query and its results to files. Never
paste a summary in place of a source.

## Receipts

Each submission's worklog entry names the seat, exact model and effort
(for Pro, quoted from the page readings; the profile label goes under
transport),
transport, purpose, artifact or revision, thread or session handle, and the
running count for that seat. The merge-ready report keeps three things
separate for each seat: what it was shown, what it said, and the
coordinator's own conclusion. A seat's answer is never reported as the
other seat's.
