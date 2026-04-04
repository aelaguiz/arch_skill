# Lilarch Quality Bar

## Requirements block

- Strong:
  - concrete user-visible behavior
  - defaults are explicit
  - when agent-backed, it is clear whether the feature should lean on prompt/capability work versus deterministic code
  - instruction-bearing source content keeps explicit structure when it shapes behavior
  - non-requirements cut off easy overbuild
- Weak:
  - generic wish list
  - agent-backed behavior is under-specified and left to be solved with scaffolding later
  - prompt or agent doctrine was silently compressed while being ported
  - no defaults
  - implied product decisions left unresolved

## Architecture blocks

- Strong:
  - name the real files or modules
  - explain ownership before and after
  - when agent-backed, explain what behavior belongs in prompt/native-capability use versus deterministic code
  - preserve explicit operational structure when instruction-bearing source is re-homed
  - capture the call-site blast radius
- Weak:
  - vague "update UI and backend"
  - jumps to custom scaffolding without a capability-first rationale
  - no call-site view

## Plan audit

- Strong:
  - says why the plan is safe to implement
  - calls out remaining risk directly
  - catches prompt-first or capability-first misses before finish mode
  - catches silent compression of instruction-bearing content before finish mode
  - catches scope creep before finish mode
- Weak:
  - rubber-stamp approval
  - accepts agent-backed tooling without justifying why prompt-first options failed
  - just repeats the phase plan

## Finish-mode audit

- Strong:
  - checks code reality against the compact doc
  - treats unjustified scaffolding around agent-backed behavior as a real miss
  - names missing work if any
- Weak:
  - "looks good"
  - lets finish mode invent wrappers or scripts that the doc never justified
  - equates partial verification with completion
