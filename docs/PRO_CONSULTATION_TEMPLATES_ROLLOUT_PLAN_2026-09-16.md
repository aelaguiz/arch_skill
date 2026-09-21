# Pro consultation templates: rollout plan

Written 2026-09-16. Owner: Amir. Status: in progress (steps 1 to 4 implemented 2026-09-16).

## What this delivers

Every prompt an agent sends to GPT-6 Astra Pro (and every audit brief it hands a
Fable or Sol reviewer) is written the way Amir would say it to a colleague: it
opens with what we are building and what the finished thing will contain, hands
over the sources whole, offers the agent's status as a belief, and asks one
question about intent with a flavor of what to look for. Wherever something is
being authored (a plan, a design, a diagnosis, an issue set) Pro writes it and
the agent asks the questions, then carries the agreed result into the artifact
verbatim. No verdict tokens, no answer caps, no scope fences, no SHA pins.

The reviewed draft of the templates is the share page
[Pro prompt templates](https://share.fun.country/20260916-c62a297f69c0/index.html),
with its markdown source at
`/Users/aelaguiz/workspace/psagentspace/_artifacts/2026-09-16-pro-consultation-templates/report.md`.
The evidence behind it is the 621-prompt inventory (`gpt6-pro-prompt-inventory-2026-09.md`
and `.jsonl` in this repo root) and the Dynamic Missions Codex session
`01a0abbe-a311-75f0-9b87-ed006b673ccb` (2026-09-16).

## Lessons the templates encode

1. Open with the picture of the finished thing, never a generic ask.
2. Pro writes; the agent asks. The agent never writes a thing and asks Pro to check it.
3. Reviews say what to look for, in Amir's words: unnecessary risk, overbuilt edge
   cases, new patterns beside clean existing ones, split brain, a web of calls,
   working around an architectural limitation that should be fixed first, and
   the bugs we have actually shipped.
4. Hand over the sources whole and let Pro read the latest: full sheet export,
   the plan, Amir's words, raw output, the branch or PR with the connector. No
   SHA pins, no pasting the issue in place of the source, no narrowing what Pro
   sees because the work got narrowed.
5. Amir's phrasing beats the prompt-authoring scaffold. Section moves are his:
   here's where I'm at, what I did, where I'm least sure, what I'm looking for,
   outline it for me.
6. Every template ships with its anti-patterns, one real example of what agents
   send today, and the attach list.
7. The agent watches for Pro to return, not Amir. Sending is not done. The
   agent does not end its turn with "read Pro's review when it lands" or
   "stopping at merge-ready for you"; it waits, reads the whole answer, and
   acts on it. Amir's ruling, 2026-09-16: "No, don't tell me too, dude. You
   have to watch for it."
8. The brief goes into the composer as written, with a synthetic paste in page
   context (verified 2026-09-17 on a 540-word Template A brief): paragraphs
   and bullets survive, nothing sends mid-entry, and a literal `@GitHub` or
   `@BigQuery` becomes the connector pill. Never `fill` or `type` the brief,
   and never move the ask into a file; that workaround produced the ask-file
   plus competing one-line prompt Amir flagged on 2026-09-17.

## Where every Pro prompt comes from today

The inventory attributes 610 sent prompts to these callers, and every one of
them went through `chatgpt-web` for transport and was supposed to apply
`prompt-authoring` to the brief:

| Caller | Prompts | What it asks Pro for |
|---|---|---|
| `epic-to-prs` | 303 | plan gates, PR reviews, fix verification, on-track checks, failover threads |
| `issue-to-pr` | 84 | plan gates, PR reviews, fix verification |
| ad-hoc `$chatgpt-web` consults | 89 | design rounds, diagnoses, audits, architecture reviews |
| `gh-issue-filing` (not from this repo) | 10 | issue-set design |
| `bugs-flow`, `bq-telemetry` | 3 | diagnosis, data questions |

Audit briefs for Fable and Sol reviewers come from `delegated-implementation`
and `fresh-consult`, built ad hoc per run. The `unblocker` consults the run's
Pro thread for blockers. So the hub is `chatgpt-web`; the workflow skills only
need to point at it and stop asking for verdicts.

## Where each piece goes

| Piece | File | Change |
|---|---|---|
| Templates A to J, anti-patterns, attach lists, base shape, voice check | `skills/chatgpt-web/references/consultation-templates.md` (new) | The page content, moved verbatim into a reference with a read condition |
| Pick the family, write in Amir's voice, voice check, no SHA, Pro writes, the agent watches for Pro's answer, receipt records what Pro was shown | `skills/chatgpt-web/SKILL.md` | "Wait for the requested review" rule, "Prepare the consultation" and "Return the result" rewritten |
| Attach mechanics: full sheet export through gws, plan doc, Amir's words file, raw output, packing within the 10-attachment cap | `skills/chatgpt-web/references/composer-and-attachments.md` | New section |
| Planning is D, plan check is C, PR review is A, fixes are B once, on-track is E, failover is J, retry is I; report carries what Pro was shown and said plus the coordinator's own judgment | `skills/issue-to-pr/SKILL.md`, `skills/epic-to-prs/SKILL.md` | "Pro cadence", "Consulting Pro" / "Shared Pro cadence", "Pro thread and receipts", report step |
| Amir's 2026-09-16 rulings, verbatim | `skills/issue-to-pr/references/dispatch-evidence.md`, `skills/epic-to-prs/references/epic-dispatch-evidence.md` | Appended in the existing owner-direction format |
| Phrasing beats scaffold for consult and reviewer briefs; two anti-example cases | `skills/prompt-authoring/SKILL.md`, `skills/prompt-authoring/references/examples-and-anti-examples.md` | One non-negotiable; Case 16 (the #5949 brief) and Case 17 (SHA pin, verdict token, scope fence) |
| Fable and Sol audit briefs carry the same sources and review questions as Template A | `skills/delegated-implementation/SKILL.md` | "Brief and parallelize" |
| One pointer line each | `skills/_shared/agent-orchestration-policy.md` ("Preserve independent judgment"), `skills/unblocker/SKILL.md` (Pro consult bullet) | Point at the templates reference |
| Bugs we have actually shipped | stays in `psmobile/.github/claude/repo_review_policy.md` and `partials/incident_rules.md` | Template A attaches them when the repo has them; the reference keeps only the cross-repo subset |
| Inventory line for `chatgpt-web` | `README.md` | Names the templates reference |
| `default_prompt` for `chatgpt-web` | `skills/chatgpt-web/agents/openai.yaml` | Says to pick the family template and run the voice check |

Not touched: `fresh-consult` (a strict yes/no arbiter by explicit user
selection; decision 1 below), `codex-review-yolo` (exact-profile receipt lane),
the cynical review skills (host-side review lanes, already the source of the
lenses), and `gh-issue-filing` / `bq-telemetry` (installed from elsewhere; they
inherit the templates through `chatgpt-web`).

## How skill-authoring is applied

Each edit below runs through `$skill-authoring` as an `edit` job (or `refactor`
for `chatgpt-web`), with `$prompt-authoring` applied to the prose. The concrete
rules from that skill that bind here:

- **Read the contract first.** `skills/skill-authoring/references/skill-pattern-contract.md`
  before any edit; `references/packaging-trigger-and-validation.md` for the
  `chatgpt-web` restructure, because it changes package layout.
- **Entry file size.** `chatgpt-web/SKILL.md` is 239 lines today. The
  templates go into a reference, not the entry file, so the entry stays well
  under 500 lines and about 5,000 tokens. Measure both after the edit.
- **Selective reading with a clear condition.** `SKILL.md` links the templates
  reference with the condition "before writing any submission, read the family
  that matches the ask." The rules that hold on every invocation (no verdict
  token, no cap, no fence, no SHA pin, sources attached whole, Pro writes) stay
  in the entry file; only the templates and examples move to the reference.
- **One owning place per instruction.** The templates live in `chatgpt-web`
  only. `issue-to-pr`, `epic-to-prs`, `delegated-implementation`,
  `unblocker`, and the shared policy point at them by path and name the family;
  they do not restate them. `prompt-authoring` keeps the general prompt
  doctrine and gains one rule that defers to the templates for consult briefs.
- **Trigger boundaries against peers.** `chatgpt-web`'s description already
  separates it from API work and generic browser automation. The edit adds one
  sentence naming `fresh-consult` and `codex-review-yolo` as the lanes that keep
  a verdict footer by design, so the no-verdict rule is not read as applying to
  them.
- **Co-edit runtime metadata.** `chatgpt-web/agents/openai.yaml`
  `default_prompt` changes with the visible contract. The other edited skills
  keep their metadata unless their default prompt names the old verdict
  behavior; check each `agents/openai.yaml` and change only where it drifts.
- **No scripts, no tests on wording.** This is prompt-only doctrine. No lint
  script for anti-patterns, no runner, and no unit test that greps `SKILL.md`
  for phrases (`AGENTS.md` red line). Validation is `npx skills check`, a
  complete re-read of each edited entry file plus its normal invocation load,
  and the representative-task check below.
- **Amir's words as evidence, not rules.** His verbatim rulings go into the
  two `dispatch-evidence.md` references in the format those files already use.
  The runtime contract in `SKILL.md` states the rule in plain English and does
  not quote him; the reference carries provenance.
- **Generalize from intent.** The templates encode the pattern (situate, hand
  over sources, state belief, one intent question, Pro writes), not the
  Missions incident. The Missions brief appears only as an anti-example in
  `prompt-authoring`.

## Sequence

1. **Hub.** Create `chatgpt-web/references/consultation-templates.md` from the
   page's `report.md` (drop the page-only lede; keep A to J, the bugs subset,
   and add the base shape and voice check). Rewrite "Prepare the consultation"
   and "Return the result" in `chatgpt-web/SKILL.md`. Add the attach section to
   `composer-and-attachments.md`. Update `agents/openai.yaml`. Measure the entry
   file. Run `npx skills check`. About 2 hours.
2. **Workflows.** Edit `issue-to-pr/SKILL.md` and `epic-to-prs/SKILL.md`
   cadence, consulting, and report sections; append the rulings to both
   evidence references. The plan on disk is Pro's plan from D, carried over by
   the agent; the delivery contract wording changes to say so. About 2 hours.
3. **Doctrine.** One non-negotiable in `prompt-authoring/SKILL.md`; Cases 16
   and 17 in its examples reference; one line in the shared policy;
   `delegated-implementation` brief section; `unblocker` pointer. About 1 hour.
4. **README and inventory.** Update the `chatgpt-web` inventory line and the
   usage guide entry if it names the old behavior. About 20 minutes.
5. **Install and publish.** `make install`, `make verify_install`, then
   `$amir-publish` to the other machines. About 30 minutes.
6. **Validate on a real task.** Re-run the #5949 PR review with Template A in a
   fresh Pro thread, with the workbook export, the plan, the issue, and Amir's
   words attached, and compare with the agent's original two-round review. Then,
   after a week of runs, re-run the inventory counts (`$agent-history` on new
   sessions) and check that the verdict-token, cap, fence, and SHA-pin shares
   fall from 60%, 33%, 23%, and near-universal toward zero. Pro's time plus about
   1 hour.
7. **Retire the draft.** Regenerate the share page from the skill reference or
   mark it superseded; update its `SHARES.md` row; mark
   `psagentspace/factory/workflows/external-review-gpt-pro.md` superseded where
   it describes the old prompt shape.

Steps 1 to 4 are one PR on this repo; steps 5 to 7 follow the merge.

## Verification

- `npx skills check` passes.
- Every edited `SKILL.md` re-read in full after editing; entry body under 500
  lines and about 5,000 tokens; the normal invocation load (entry plus the one
  templates reference) fits a single read.
- `make verify_install` passes after `make install`.
- The #5949 A/B in step 6 is recorded beside this plan with both Pro answers.
- No new script, runner, or wording test was added.

## Decisions Amir owns

1. `fresh-consult` keeps its yes/no VERDICT footer as the one explicit token
   lane, or aligns with the templates. Default: keep it.
2. rustai, cratejoy, and website have no `.github/claude/repo_review_policy.md`.
   Add one per repo, or let Template A run there without a bug list. Default:
   no new policy files in this rollout.
3. The share page: regenerate from the skill reference after step 1 so there is
   one source, or retire it. Default: regenerate.

## Out of scope

Changing the PR-Agent policy in psmobile, adding review policy files to other
repos, editing `gh-issue-filing` or `bq-telemetry`, and any change to how Pro
accounts, profiles, or the Chat surface are selected.
