# Intent Pack Contract

The Intent Pack is the skill's output artifact: the authorization-anchor
source that downstream planning skills plan from and executors run from
without re-asking the user.

## Layout

One directory per effort, in the target repo:

```
docs/<SLUG>_INTENT/
  INTENT.md        # the single authoritative document
  research/        # education evidence: facts briefings, journey
                   # inventories, key-file maps, prior-research pointers,
                   # visual references
```

`INTENT.md` is the only authority; `research/` files are evidence it cites.
For quick-lane work the whole pack may be one quarter-page `INTENT.md`.

## INTENT.md sections

Sections map 1:1 to the must-always-know list (see `must-know-list.md`):
what and why, success signals, project type, UX delta (journey maps,
stay-dead list, vocabulary freeze, visual references), numbered
requirements, non-goals and deferral ledger, architecture requirements,
test grid and proof obligations, definition of done, execution policy,
autonomy contract, open decisions and assumptions.

Two additional sections:

- **Decision log** — every question asked and the answer given, in order;
  proxy answers marked `[PROXY-<model>]`; rejected alternatives with the
  one-line reason; every agent-made derivation flagged as such with its
  approval. This log is what makes the pack auditable: any decision in the
  pack traces to a line here.
- **Approval and freeze** — who approved the decision table and when, the
  chosen plan step from gate 2, and the freeze statement, carrying seven
  fields the downstream planning skill consumes directly:
  - *authorized outcome and anchors* — what the user asked for, pointing at
    the decision-log lines where they said it;
  - *smallest sufficient solution* — the least work that satisfies it;
  - *convergence-closure candidates* — adjacent same-contract paths
    education found that planning may need to migrate or delete so one
    owner remains (candidates only; the planning skill decides, the user
    approves);
  - *freeze boundary* — what is in and out as of approval;
  - *enough proof* — the approved grid and artifacts;
  - *do-not-build boundary* — the non-goals and rejected machinery;
  - *accepted residual risk* — what stays imperfect on purpose.

## The blank template

Education produces the template with every section header present and every
body empty except evidence-free scaffolding (e.g. the standing-doctrine
defaults, clearly marked as unconfirmed). Pre-filling any elicited section
before the user has spoken is the presumptive-drafter failure — the pack
would then contain decisions the user never made, formatted for
rubber-stamping.

## Writing rules

- Answers are written into the pack immediately as they land, replacing
  any contradicted text; the decision log keeps the raw question-and-answer
  record separately.
- Plain language throughout: requirements stated in words and referred to
  by name; no invented shorthand; no code symbols in any user-facing line.
- Target under ~300 lines for `INTENT.md`. The pack records intent,
  boundaries, and proof — not designs, not implementation recipes. If it
  is growing past that, detail is leaking in that belongs to the downstream
  plan or to `research/`.

## Freeze rules

- The pack freezes when gate 1 feedback is folded in and gate 2 chooses
  the plan step. After freeze, changes are human decisions recorded in the
  decision log — the pack is never silently edited to match what got built.
- Nothing in the frozen pack says "coming later" except items the user
  explicitly parked (recorded with where they land, e.g. "copy rides with
  the mock round").
- Downstream skills must not re-ask what the pack answers; the handoff
  says so. A genuinely new fork discovered during planning or execution
  comes back as a question, not as scope.

## Acceptance bar

The No Prior Knowledge Test: an agent with zero repo familiarity, given
only this pack and repo access, could produce the implementation plan and
execute it without asking the user anything — because every must-know line
is present, every decision is owned, and every proof obligation is stated.
