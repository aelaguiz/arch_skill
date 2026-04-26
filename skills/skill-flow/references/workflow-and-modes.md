# Workflow And Modes

Use this reference after you classify the job as `design`, `audit`, or `repair`.

## Design mode

Use design mode when the flow does not exist yet or the author is still deciding what the skills should be.

1. Capture 2-3 real user asks and one nearby anti-case.
2. Write the leverage claim for the flow as a whole.
3. Draft the default path in plain English before naming folders.
4. For each proposed skill, write:
   - job
   - input
   - output or blocker
   - nearest lookalike
   - specialist skill to use, if any
5. Remove stages that only restate another stage's job.
6. Add handoff artifacts where the next skill would otherwise depend on memory.
7. Validate with one representative case and one anti-case.

Design output should be a compact brief, not a full implementation plan unless the user asked for one.

## Audit mode

Use audit mode when the skills or drafts already exist.

1. Lock the inspected frontier. Name the skills, prompt files, Doctrine sources, emitted packages, or docs you actually inspected.
2. Read the whole visible flow before deciding findings.
3. Build a flow map: skill, job, input, output, handoff, nearest peer.
4. Look for the strongest flow failures first:
   - two skills own the same job
   - one skill owns several unrelated jobs
   - a handoff depends on hidden context
   - examples act like a router
   - scripts encode judgment instead of utility
   - individual skill or prompt quality should be sent to a specialist
   - Doctrine-specific audit should go to `agent-linter` when available
5. Return findings first with exact evidence and the smallest credible fix.

Do not claim a full-flow audit if you only inspected one skill. Say what is missing.

### Audit (DAG-grounded sub-mode)

Use this sub-mode when the user wants to audit a skill suite that is too large
for one-pass reasoning (typically 10+ skills, designed for 30+ skill suites).
Trigger phrases include "audit every skill in this project", "audit the skills
for flow F1 in lessons_studio", or an explicit slug list with audit intent.

This sub-mode is **audit-only and read-only against the target**. It writes a
DAG substrate document for the agent's reasoning surface, then emits findings
using the existing audit-finding template. It does not edit any file in the
target skill suite, and it does not invoke any other skill at runtime to act
on findings.

#### Reads (in this order)

1. `references/dag-substrate-format.md` — substrate format spec and closed enums.
2. `references/parallel-walk-protocol.md` — sub-agent evidence schema, fanout
   sizing, scope resolution rules, code-block whitelist.
3. `references/waste-pattern-catalog.md` — recognition tests for the audit
   reasoning step.
4. `references/lessons-studio-worked-example.md` — only when the boundary or
   pattern is still fuzzy. The audit prompt itself does NOT name the worked
   example case.

#### Workflow

1. **Resolve scope from the user's plain-language phrase.** Per
   `parallel-walk-protocol.md` scope-resolution rules. Print the resolved
   skill list (count + slugs) before fanout. Ask an exact blocker question if
   the phrase is genuinely ambiguous.
2. **Spawn parallel sub-agents to walk the resolved scope.** Fanout sizing per
   `parallel-walk-protocol.md`. Each sub-agent returns the per-skill evidence
   schema verbatim.
3. **Aggregate sub-agent evidence into the DAG substrate.** Write the
   substrate at `<doc-dir>/<doc-slug>_DAG.md` per `dag-substrate-format.md`
   (mermaid graph + edge table + unresolved-reference list, in that order).
4. **Read the substrate back. Apply the recognition tests** from
   `waste-pattern-catalog.md`. The substrate is exhaustive grounding; the
   verdict is prompt-driven judgment.
5. **Emit findings using the existing 6-field audit-finding template** below.
   `Owner` field names affected SKILL.md / reference paths only — never names
   another skill to invoke.
6. **(On request only)** Invoke `scripts/render_dag_d2.py <substrate.md>
   <out.d2> <out.svg>` to produce a d2 render of the substrate. Fail loudly
   if `d2` binary is not on PATH.

#### Fail-loud boundaries

Each of these stops the run with a named error:

- Missing `d2` binary on PATH (only when render was requested).
- Missing target `skills/` directory.
- Unreadable SKILL.md (file missing, malformed, permission denied).
- Unresolvable scope phrase that the in-prompt resolver cannot disambiguate
  after one blocker question.

No silent fallbacks. No cached SVG. No "lite" substrate when fanout fails.
The substrate is regenerated from a fresh parallel walk every audit run.

## Repair mode

Use repair mode when the flow has a known issue and the owning surfaces are available.

1. Choose the smallest owner:
   - flow-level boundary or handoff goes in the flow docs or guide
   - one skill's trigger or package shape goes through `skill-authoring`
   - one prompt contract goes through `prompt-authoring`
   - Doctrine construct choice goes through `doctrine-learn` when available
   - Doctrine authoring lint goes through `agent-linter` when available
2. Preserve useful behavior. Extract the durable principle before deleting a vivid example or working prompt pattern.
3. Patch only the surfaces that own the issue.
4. Re-run the representative case and nearby anti-case.

## Specialist skill use

Do not run peers as a ritual pipeline. Use them when their question is active.

- Use `skill-authoring` when a specific skill package needs trigger, scope, packaging, references, or validation repair.
- Use `prompt-authoring` when the problem is commander's intent, section placement, examples, anti-heuristic wording, or prompt output contracts.
- Use `doctrine-learn` when the author is choosing or learning a Doctrine construct.
- Use `agent-linter` when a Doctrine-authored package, prompt, or flow needs an evidence-based authoring audit and the skill is available.

If a preferred peer is not installed, keep the local `skill-flow` judgment useful. Name the missing preferred lever and continue with the evidence available.

## Markdown and Doctrine surfaces

For pure Markdown skill packages, inspect:

- `SKILL.md`
- `references/`
- `agents/openai.yaml` or other runtime metadata when present
- install docs when the package makes install or runtime claims

For Doctrine-authored packages, inspect:

- the `.prompt` source that owns the package
- bundled references or emitted documents when they change behavior
- emitted `SKILL.md` when drift or runtime shape matters
- typed contracts when exact truth is involved

Do not punish a Doctrine source for using comments that do not emit into runtime text.
Do not trust emitted Markdown alone when the authored source is the requested surface.

## Output shapes

Design brief:

```markdown
Intent spine:
Canonical asks:
Anti-case:
Flow:
| Step | Skill | Job | Input | Output or blocker | Next handoff |
Peer boundaries:
Validation:
Open questions:
```

Audit finding:

```markdown
Finding:
Severity:
Evidence:
Why it matters:
Smallest fix:
Owner:
```

Repair summary:

```markdown
Changed:
Why:
Verification:
Remaining risk:
```
