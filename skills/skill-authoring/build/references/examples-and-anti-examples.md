# Examples And Anti-Examples

Use this file when you need concrete patterns for framing, packaging, or auditing a skill.

## Example: strong use-case framing

Good: "Write, edit, refactor, or audit agent skills so they are leverage-first, self-contained, and anti-heuristic."
Why it works: names the verbs; names the artifact; names the quality bar; signals that the skill supports more than greenfield authoring.
Weaker: "Help create better skills and best practices."
Why it fails: too vague to trigger reliably; does not say what the runtime work actually is; sounds like generic advice, not a concrete workflow.

## Example: strong `When not to use`

Good: "The right artifact is repo-local `AGENTS.md` guidance, a project plan, or a one-shot prompt rather than a reusable skill."
Why it works: names the nearby alternatives explicitly; prevents umbrella-skill drift; teaches the mechanism choice, not just the prohibition.
Weaker: "Do not use this skill for unrelated tasks."
Why it fails: says almost nothing; gives no help with boundary decisions.

## Example: lean entrypoint with deeper references

Good pattern: `SKILL.md` teaches scope, workflow, and routing; `references/` carries detailed doctrine, examples, and validation; `agents/openai.yaml` exists only if UI metadata or policy matters.
Why it works: keeps the default context lean; loads detail only when the task truly needs it; makes the package easier to maintain.
Anti-pattern: a 600-line `SKILL.md` with every example, edge case, and policy embedded inline.
Why it fails: bloats context; makes audits harder; usually signals missing structure rather than genuine complexity.

## Example: description as trigger, not slogan

Good: "Self-contained project planning and finalization workflow for non-trivial work..."
Why it works: identifies a workflow; implies entry criteria; distinguishes itself from generic planning advice.
Bad: "World-class project excellence for fast-moving teams."
Why it fails: pure positioning language; impossible to route reliably.

## Example: coordinator versus specialist

Good coordinator shape: "Recommend the right skill in this suite and explain the nearest boundary. Not for running the underlying workflow."
Good specialist shape: "Write or review one learner-facing feedback object after the answer contract is stable. Not for option labels, answer truth, or route selection."
Why it works: the coordinator owns selection and handoff; the specialist owns one artifact and one entry condition; both can share a domain without competing for the same user ask; the boundary is visible from compact trigger text before the full body loads.
Weaker: "Use this skill for curriculum quality improvements." / "Use this skill for detailed curriculum quality improvements."
Why it fails: both descriptions claim the same domain; "detailed" is not an ownership boundary; the model has to guess whether to route, coordinate, write, review, or mutate.

## Example: OpenClaw metadata is operational, not decorative

Good: keep OpenClaw-specific load-time behavior in frontmatter, such as quoted `description`, explicit invocation keys, and single-line `metadata.openclaw` JSON.
Why it works: the runtime can actually gate and route the skill correctly; machine behavior is not hidden in prose the loader never reads; OpenClaw-only rules stay bundled in a dedicated reference instead of leaking into generic sections.
Bad: describe gating, slash-command, or secret expectations only in the body while leaving frontmatter vague or malformed.
Why it fails: the loader cannot infer the real behavior; the skill may overtrigger, undertrigger, or silently fail eligibility; authors end up blaming the prose for what is really a schema problem.

## Example: preserve the principle, not the checklist

Bad refactor instinct: remove a messy but useful section and replace it with bland generic guidance.
Better refactor: ask what problem the messy section was solving; extract that durable lesson upward; keep the old concrete detail as an example, litmus test, or reference note if it still teaches something real.
This is how you avoid deleting the skill's real value while still removing heuristics.

## Example: prompt-first runbook

Bad: The user says, "Run the lesson I specify from beginning to end." The skill becomes a runner with flags, target schemas, route recovery rules, hard blockers for missing artifacts, and a script that mostly enforces the same order a prompt could have stated.
Why it fails: it treats natural language as an API problem; it overfits one repair incident into runtime behavior; it removes the agent's ability to use common sense about the named target; it blocks on normal start states the skill was supposed to handle.
Better: "Use when the author names one lesson and wants it authored end to end." "Assume the section is ready unless the owning controller or skill proves otherwise." "Run the owner skills in this order; stop only for real owner blockers, failed validation, or ambiguity."
Why it works: the skill is a reusable prompt the user no longer has to type; the sequence is clear without pretending every branch is knowable up front; ownership boundaries stay visible without becoming a second harness.

## Example: script discipline

Good: add a validator script only after repeated packaging or format failures justify deterministic help.
Bad: add scripts preemptively because code feels more serious than prose.
Why this matters: skills are primarily workflow and knowledge packages; scripts are support beams, not the main building.
