# Examples

Examples illustrate the single protocol. They are not a routing table. In each
case, Stepwise follows the same shape: observe, diagnose, talk to the relevant
session, repair at root cause, then rejudge.

## Example 1 - Local timeline-sensitive copy failure

User asks Stepwise to finish a lesson section with strict skill-order
adherence. The manifest includes a bounded copy cleanup step. The worker
removes placeholders and the artifact verifies, but the transcript shows the
worker edited learner-facing copy before loading the owner-declared copy
baseline and grounding support.

### Critic output

The critic returns observation only:

```json
{
  "step_n": 6,
  "verdict": "fail",
  "checks": [
    {
      "name": "skill_order_adherence",
      "status": "fail",
      "evidence": "stream.log shows manifest write before owner-declared baseline reads"
    },
    {
      "name": "artifact_exists",
      "status": "pass",
      "evidence": "placeholder scan returned 0 and verify exited 0"
    }
  ],
  "observed_breach": "The attempt changed learner-facing copy before the owner-declared copy gate was evidenced.",
  "evidence_pointers": [
    "steps/6/try-1/stream.log: manifest write event precedes baseline reads",
    "steps/6/try-1/stdout.final.json: final proof claims clean copy cleanup"
  ],
  "contract_clauses_implicated": [
    "manifest step 6 owner instruction: follow $lesson-copy-discipline",
    "$lesson-copy-discipline: load copy baseline before learner-facing write"
  ],
  "summary": "The artifact is clean, but the attempt skipped pre-write copy provenance.",
  "abstain_reason": null
}
```

The critic does not say how to repair, does not say "do not redo," and does not
route upstream.

### Diagnostic intake

Stepwise writes `diagnostic/intake.md`:

- Artifact state is green.
- Contract evidence is not green.
- The suspect break is between owner skill requirements and worker action.
- The old repair instinct "preserve the good edit and patch proof" would be
  dishonest because the requirement is timeline-sensitive.

### Diagnostic conversation

Stepwise resumes the step-6 worker read-only:

```text
Diagnostic conversation only. Do not modify files. Do not run commands beyond
safe reads explicitly allowed below. Do not attempt repair.

## What the transcript already shows

- Tool calls during this attempt: manifest read, manifest write, placeholder scan, verify
- Owner runbook paths you read or did not read: $lesson-copy-discipline read after the write
- Artifact state after the attempt: placeholders 0, verify pass
- Contract clauses this attempt is being judged against: copy baseline before learner-facing copy write

## Questions

1. What did you believe this step was asking, and which owner-runbook line made
   you believe it?
2. Which of your actions in this attempt supports that belief, and which of
   them contradicts it?
3. What evidence does the owner contract actually require here?
4. Where did each input to this step come from? Did any of those inputs look
   wrong to you at the time?

End with exactly one line:
CONFIRMATION: <one sentence naming what you now understand about the issue,
citing the owner-runbook clause that implies the correct behavior>.
```

The worker says it treated placeholder cleanup as reuse of existing copy, not a
copy-lane write. It confirms that this was not an owner-doctrine exception.

If the worker overcorrects and says every support skill must emit a receipt id,
Stepwise asks the same conversation's follow-up:

```text
Continue diagnostic conversation only. You stated: "every support skill must
emit a receipt id". Where does the owner runbook or declared support say that?
If it is not in the owner doctrine, what is the owner-doctrine rule you are
actually trying to honor?
```

The worker corrects itself: lenses need invocation and visible application;
grounding primitives need real receipts where their runbook requires them.

### Repair prompt

Stepwise authors an operational repair prompt with source tags:

```text
Your prior attempt on this step did not honor its contract. We have diagnosed
the issue.

Execute the repair below. Do not add constraints beyond the user prompt,
manifest, owner runbook, and confirmed repair.

## Confirmed issue

The artifact is currently clean, but the original copy write happened before
the owner-declared copy gate. The recovery must not claim the original write
was pre-gated; it must either reapply the copy under the gate or record an
honest post-gate audit if the owner primitive performs an idempotent write.

## Repair steps

1. Load the owner copy baseline and declared support before any recovery write. [source: owner runbook]
2. Ground the learner-visible headline through the owner-declared grounding primitive and record the returned evidence. [source: owner runbook]
3. Use the owner-declared read/write primitive to reapply or audit the four headline fields. [source: manifest]
4. Rewrite the proof note so it states the true timeline: the first write was not pre-gated; this repair is the compliant recovery event. [source: confirmed diagnosis]

## Evidence to leave

- baseline/support reads,
- grounding receipt or explicit owner-supported no-receipt evidence,
- owner primitive readback/writeback,
- placeholder scan,
- lesson verify result,
- truthful proof note.

## Stop instead of finishing if

- the owner primitive is unavailable and no owner-documented substitute exists,
- the only way to pass would be to claim the original write was pre-gated.
```

### Rejudge

A new clean critic judges the repaired attempt. If the worker left honest evidence
and did not fabricate the original timeline, the step can pass.

## Example 2 - Upstream input is the real root cause

Step 5 creates learner-facing copy from a stage descriptor produced by step 3.
Step 5 fails because its output references the wrong stage. The step-5 worker
says in diagnostic conversation that it used the stage text it received from
step 3.

Stepwise does not hammer step 5 with local rewrite instructions. It reads the
manifest, sees step 3 produced the stage descriptor consumed by step 5, and
resumes the step-3 session read-only with the same diagnostic prompt shape.

If step 3 confirms it picked the wrong stage from its own owner runbook, root
cause is step 3. Stepwise authors a source-tagged repair prompt for step 3,
repairs step 3, runs the step-3 critic, then starts new clean replacements for
steps 4 and 5. Those downstream tries are marked
`origin.kind = "respawn-after-upstream"` so the run record shows they used
clean context after an upstream fix, not repairs of the downstream worker's
own attempt.

Why clean replacement matters: step 5's session history was built around the
wrong stage. Resuming it after step 3 changes would carry poisoned context
forward.

## Example 3 - Mechanical missing artifact

Step 2 claims it wrote `outline.md`; the critic sees the file is missing.

Even this simple failure enters the same protocol:

1. Intake names the broken link: worker claim to artifact evidence.
2. Diagnostic prompt asks the worker what it believed it produced and what
   evidence supports it.
3. Worker confirms it wrote notes to the wrong path.
4. Stepwise authors a source-tagged repair prompt: write the expected artifact
   at the manifest path or stop with evidence that the path is impossible.
5. A new clean critic rejudges.

Simple failures converge quickly. They do not need a separate shortcut path.

## Example 4 - Doctrine ambiguity

The critic fails a step because support evidence appears missing. Diagnostic
conversation shows the owner runbook names two incompatible support paths, and
neither one clearly dominates.

Stepwise halts and asks the user. It does not invent a tie-breaker, and it does
not prompt the worker to choose whichever support path seems plausible.
