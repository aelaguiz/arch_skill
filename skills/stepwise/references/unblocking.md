# Known-unblock doctrine

`$stepwise` should not halt just because something unexpected happened. Halt
only when the current role cannot name a safe, bounded repair inside its
authority.

## Core rule

When a blocker has a known, safe, bounded repair inside the current role's
authority, do the repair before escalating.

Ask or halt only when at least one of these is true:

- The repair is unknown after reasonable inspection.
- The repair would edit target-repo work products from orchestrator or critic
  context.
- The repair would skip, weaken, or reinterpret the confirmed manifest.
- The repair contradicts target doctrine, user instructions, or a hard runtime
  constraint.
- The repair is destructive or cannot be bounded to the current run artifact.
- The relevant retry or recovery budget is exhausted.

This is not a license to improvise work. It is a license to unblock the
orchestration machinery and the current step's own retry path when the right
move is already clear.

## Authority by role

### Orchestrator

The orchestrator may repair orchestration artifacts and subprocess wiring:

- Regenerate malformed prompts, schemas, descriptors, or command files in the
  run directory.
- Normalize schema shape for the selected runtime when the semantics are
  unchanged.
- Retry a subprocess after fixing a prompt/rendering/schema/flag problem.
- Switch to a documented fallback mode when the primary runtime wrapper fails
  but the fallback preserves the same output contract.
- Record the repair in the run directory and continue.

The orchestrator may not edit target-repo work products, substitute its own
answer for a failed step, or silently change the confirmed manifest's meaning.

### Critic

The critic should inspect before abstaining when the missing evidence is
inspectable:

- If a transcript path, artifact path, or doctrine path is present, read it.
- If the descriptor gives a read-only predicate, run the predicate.
- If a worker claims a tool or command was unavailable and the command is easy
  to check safely, inspect the available help or transcript evidence before
  accepting the claim.

When the critic knows how the worker can recover, it returns `verdict=fail`
with an operational `resume_hint`. It abstains only when the evidence needed
for judgment is missing, corrupted, or outside read-only reach.

### Worker

The worker should try the obvious safe discovery step before declaring a
blocker:

- Read the declared doctrine path before acting.
- If a required path is missing, show the exact missing path.
- If a required command or primitive is unclear, run the safe help/list command
  or inspect the owning skill before saying it is unavailable.
- If the owner path is genuinely unavailable, stop with the exact command,
  path, or help output that proves it.

The worker still must not jump to another step, invoke unrelated workflows, or
write outside its target repo.

## Recovery posture by blocker type

- Runtime schema drift: normalize the schema or use the canonical schema, retry
  the critic, then validate the returned verdict semantically.
- Prompt rendering error: rewrite the run-directory prompt from the confirmed
  descriptor and retry the same subprocess.
- Session-id capture drift: inspect the raw stream for the session/thread id
  shape, patch the parser if the shape is known, and retry or resume using the
  captured id.
- Missing process evidence: fail the step with a concrete resume checklist that
  creates the missing evidence on the next attempt.
- Tool/command availability claim: require the worker to prove the claim with a
  read/help/list command or use the declared owner path.
- Target doctrine contradiction: surface the contradiction. Do not pick one side
  silently; this is not a known unblock.

## Anti-patterns

- Do not turn "strict" into "stop at first infrastructure wrinkle." Strict means
  stronger checks and less retry budget, not lower agency.
- Do not hand-roll target work in the orchestrator to keep the run moving.
- Do not route around a critic by pretending a missing verdict is a pass.
- Do not silently ignore an explicit user preference or hard doctrine because
  repairing it takes another subprocess call.
- Do not write vague repair prompts when the failure is operational. If the fix
  is "read this skill, run this command, remove this false claim," say that.

## Recognition test

Before asking the user for help, answer these questions:

1. Do I know what broke?
2. Do I know a bounded repair that preserves the manifest and role boundaries?
3. Can I perform that repair without editing target work from the wrong role?
4. Have I recorded enough evidence that an auditor can see what I did?

If all four are yes, repair and continue. If any answer is no, halt or ask with
the specific missing decision.
