# issue-to-pr lanes: a primary and a final

Written 2026-09-17. Owner: Amir. Status: implemented and published 2026-09-17 after two cold Opus 5 reads.

## The ask

Amir wants to say, at invocation: "issue-to-pr on #N. Your primary is Sol
xhigh (or Fable 5.1 xhigh). Your final is Pro." The run has the notion of a
primary and a final. The primary is the collaborator for the whole job: it
writes the plan with the coordinator, takes the early review rounds, and
answers blockers, where most of the work is ordinary and does not need Pro.
The final is the ultimate check: it reads the written-up plan once before
anyone builds, and reviews the PR once at the end when it is already clean.
The goal is speed: fewer Pro rounds, no waiting on Pro for work a cheaper
model does just as well.

Canonical asks the change has to serve:

1. "issue-to-pr on #5963, primary Sol xhigh, final Pro."
2. "epic-to-prs on the Missions epic. Primary Fable xhigh, final Pro."
3. "issue-to-pr on #4938." No lanes named: today's behavior, Pro throughout.

## Recommendation: one skill, two roles, not a variant

Keep `issue-to-pr` as the one skill and give it two named roles, primary and
final, that Amir assigns at invocation and that apply to the whole lifecycle:
planning, review, and blockers. Do not fork a
`issue-to-pr-fast` or add a router. The reasons are the ones Amir's own review
questions ask:

- A variant would copy 220 lines of delivery contract, cadence, delegation,
  and reporting, and the two would drift. That is two owners for one workflow.
- The only thing that changes is which model sits in which seat for each
  family: D and the early A and B rounds go to the primary, C and the final A
  go to the final. The briefs are the same family templates either way; the
  transport differs. That is one new concept, not a new lifecycle.
- `epic-to-prs` inherits whatever `issue-to-pr` does. One change point
  serves both.
- Amir names the reviewers in plain language. Skill-authoring's rule is to
  infer from natural language, not to add a formal parameter or a second
  skill name to remember.

Nearest lookalikes, and why they are not this: `fresh-consult` is a strict
pass/fail read-only arbiter the user selects for one verdict; `codex-review-yolo`
is the exact-profile Codex review lane with a `VERDICT:` footer;
`delegated-implementation` owns workers who write code. The primary
here is a collaborator inside the issue-to-pr lifecycle, briefed with the
family templates, whose plan the coordinator carries and whose findings the
coordinator judges and repairs. It borrows
`agent-delegate`'s transport when the reviewer is an external model, and
nothing else.

## What the two roles mean

- **Primary.** The model Amir names, as the collaborator for the job. It
  writes the plan with the coordinator in family D, going back and forth
  until the seven parts are solid. It gets every early PR round: the first
  review (A), the after-fixes round (B), and any restart after a fix changed
  the basis of the review, until it finds nothing material. It answers the
  unblocker's major-blocker consults and the on-track checks (E). It does not
  clear the plan or the PR.
- **Final.** Pro by default, or whatever Amir names, as the ultimate check.
  It reads the written-up plan once against the code before anyone builds
  (family C), with the primary's planning exchange attached. It reviews the
  PR once after the primary is clean (family A), with the primary's findings
  and the fixes attached so it sees the lineage. Its findings get fixed and
  one B round; then CI, last.
- **Same seat twice.** If Amir names the same model for both, or names no
  lanes, the run is today's behavior: one model plans and reviews, one
  planning and final pair plus judgment.
- **Epic.** The primary writes the epic plan and reviews batches; the final
  checks the epic plan once and reviews the stack once.

The brief is identical for either reviewer: the family templates in
`chatgpt-web/references/consultation-templates.md`, in Amir's voice, sources
whole, no verdict token, no cap, no fence, no SHA. Only the handover of
sources differs: Pro gets `@GitHub` and attachments through the composer; a
native or external reviewer gets the worktree path, `gh pr diff`, and the same
files by path.

## Where each piece goes

| Piece | File | Change |
|---|---|---|
| Two roles, which family goes to which seat, defaults | `skills/issue-to-pr/SKILL.md` | "Pro cadence" becomes "Primary and final"; "Consulting Pro" becomes "Consulting the primary or the final"; workflow steps 1, 4, and 5 name the seats; report names both with exact model and effort |
| Seat resolution: how each named model is reached, briefed, and read | `skills/issue-to-pr/references/primary-and-final.md` (new) | Pro through `$chatgpt-web`; Fable xhigh as a clean native child on a Claude host, otherwise external through `$agent-delegate`; Sol xhigh as an external Codex process through `$agent-delegate` with the exact model and effort; a planning collaborator keeps one continuing session for the D back-and-forth; a reviewer gets a clean context per round; each gets the family template with sources by path; return is prose the coordinator judges; receipt records exact model, effort, what it was shown, what it said |
| Shared seats across an epic; the primary plans and reviews batches, the final checks the plan and the stack | `skills/epic-to-prs/SKILL.md` | "Shared Pro cadence" becomes "Shared primary and final"; workflow steps 1 and 4 |
| The unblocker consults the primary | `skills/unblocker/SKILL.md`, `references/charter-template.md` | One clause each |
| Templates serve any seat; how to hand sources to a model without connectors | `skills/chatgpt-web/references/consultation-templates.md` | One paragraph in the shape section; the families say "the reviewer" or "you" where the mechanics differ |
| Invocation grammar and examples | `README.md`, `docs/arch_skill_usage_guide.md`, both `agents/openai.yaml` default prompts | "primary X, final Pro" as the recognized phrasing; defaults stated |
| Amir's ruling, verbatim | `skills/issue-to-pr/references/dispatch-evidence.md`, `skills/epic-to-prs/references/epic-dispatch-evidence.md` | Appended in the existing format |

Not touched: `fresh-consult`, `codex-review-yolo`, `delegated-implementation`
(workers are not reviewers), `agent-delegate` (already owns external
transport), `prompt-authoring` (its consult-brief rule already names a Fable
or Sol audit brief).

## How skill-authoring is applied

- **Job:** `edit` of `issue-to-pr` and `epic-to-prs`, plus one new reference.
  Not `author`; the leverage claim is one new concept inside an existing
  lifecycle.
- **Mechanism:** skill, because the workflow repeats across runs and travels
  between repos and hosts. No script, runner, or parameter schema: Amir names
  reviewers in a sentence and the coordinator reads it.
- **Generalize from intent:** the durable move is "a collaborator for the
  work, an ultimate check at the gates." Encode seats, not model names. Sol
  xhigh and Fable xhigh are examples in the reference, not branches in the
  entry file.
- **Preserve judgment:** the coordinator decides when the plan is fully
  formed, when the primary is clean, and when a fix changed the basis of the
  review. No round caps, no scoring. The B rule already in the templates
  holds: one after-fixes round, then a fresh A if the basis moved.
- **Orchestration policy:** dispatching a seat is an agent dispatch. The
  reference points at `../_shared/agent-orchestration-policy.md` for native
  versus external, continuing versus clean context, and the return contract,
  and keeps only the role-local rules: which family, which seat, what comes
  back.
- **Peer boundaries:** the entry file names `fresh-consult` and
  `codex-review-yolo` as the lanes that keep a verdict footer by design, so a
  primary is never confused with them.
- **Entry file size:** `issue-to-pr/SKILL.md` is 223 lines. The seats add
  about 30 lines to the entry and move resolution detail to the reference.
  Measure lines and tokens after the edit; stay well under 500 lines and
  about 5,000 tokens.
- **Metadata:** both `agents/openai.yaml` default prompts name the seats and
  the default. Descriptions gain one clause: "a primary and a final Amir
  names at invocation."
- **No wording tests.** Validation is `npx skills check`, a full re-read of
  both entry files plus the new reference as one invocation load, and the
  representative run below.

## Sequence

1. Write `references/primary-and-final.md` and edit `issue-to-pr/SKILL.md`.
   About 1.5 hours.
2. Edit `epic-to-prs/SKILL.md`, the unblocker clause, the templates
   paragraph, README, usage guide, both `openai.yaml`, both evidence files.
   About 1 hour.
3. `npx skills check`, re-read, measure, `$amir-publish`. About 20 minutes.
4. Representative run: `issue-to-pr` on one small real issue with "primary
   Fable xhigh, final Pro". Record how many planning turns and findings the
   primary took, what Pro changed at the plan check and the final review,
   and wall-clock versus the last Pro-only run of a similar issue. Pro's time
   plus about 30 minutes.

## Decisions Amir owns

1. Default when no seats are named: Pro throughout (today), or a standing
   default primary. Default in this plan: Pro throughout.
2. Whether the final sees the primary's planning exchange and review findings
   (recommended, so it can judge the lineage) or a clean brief.
3. Sol xhigh transport: external Codex through `$agent-delegate` with the
   exact model and effort, or the `codex-review-yolo` profile. Default:
   `$agent-delegate`, because yolo's `VERDICT:` footer is the anti-pattern the
   templates remove.

## Out of scope

A new skill name, a router, per-round caps, changing how Pro accounts and
profiles are selected, and any change to `fresh-consult` or
`codex-review-yolo`.
