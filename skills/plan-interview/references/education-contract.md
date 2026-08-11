# Education Contract

Education is how the skill earns the right to interview: it burns its own
tokens learning what the repo, history, and docs already know so the user is
never asked something evidence could answer. It returns **facts and a blank
template — zero decisions**.

## When education runs

- **Up front**, after orienting: the main ramp before the first real
  interview question.
- **Mid-interview, repeatedly**: the investigate-and-return loop. Any
  answer whose implications you cannot resolve from what you've read sends
  you back here. Say what you're going to find out, go, write findings into
  the pack, return with the questions they raise.

## Researcher dispatch

Apply `../../_shared/agent-orchestration-policy.md`; apply
`$prompt-authoring` to each populated brief. Clean read-only native
children, non-overlapping lenses, their own native sub-agents allowed and
no external agents, compact returns with file and symbol anchors plus the
5–10 key files that matter. The parent
reads the key files itself and owns synthesis.

Lenses to cover (merge or drop by judgment for small work):

1. **Similar features and reusable patterns** — what already exists that
   does something like this; how the last comparable change was made.
2. **Authority paths and current architecture** of the touched area — who
   owns the contract today, competing writers/readers, side doors.
3. **User journeys actually touched** — the current screens/flows and how a
   user reaches them; raw material for journey maps.
4. **Git and PR history of the area** — how it got this way, what was
   recently changed or reverted, intentional deletions (stay-dead
   candidates).
5. **Docs, prior research, and the facts inventory** — settled decisions,
   credentials and setup locations, prior investigations — collected so
   the interview (and later the executing run) searches these before
   asking the user.
6. **Test and automation surface** — what proof already exists at what
   altitude, what the default suite covers, where the gaps are.
7. **The user's past asks in similar situations** — their own phrasing and
   standing preferences, used later as question framing ("you usually ask
   for…").

## Output

- `research/` files in the pack directory: one compact file per lens that
  produced anything, facts with anchors, no recommendations dressed as
  facts.
- A **facts briefing** for the user: what was found, stated as evidence
  ("the intro blocks on a content fetch plus two image decodes; measured
  1.9–3.1s"), explicitly flagging noted-but-not-included adjacencies.
- The **blank Intent Pack template** per `intent-pack-contract.md`: every
  section header present, every elicited section empty, standing defaults
  scaffolded and marked unconfirmed.

## The facts-not-decisions rule

Education never decides. It does not classify the project type (that is a
derivation presented for approval), does not pick bars or thresholds, does
not write requirements, does not include adjacent surfaces it found — it
notes them for the interview to raise as scope questions. If a finding
makes an answer obvious, the interview still asks the question; the framing
may carry the evidence, the user carries the decision.
