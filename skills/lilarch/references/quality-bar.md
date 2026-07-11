# Lilarch Quality Bar

## Requirements block

- Strong:
  - concrete user-visible behavior
  - defaults are explicit
  - when agent-backed, it is clear whether the feature should lean on prompt/capability work versus deterministic code
  - instruction-bearing source content keeps explicit structure when it shapes behavior
  - non-requirements cut off easy overbuild
  - the Scope and Simplicity Contract distinguishes human scope from the
    initial closure and names enough proof, residual risk, and what stays unbuilt
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
  - rejects any required item without human or pre-freeze convergence provenance
  - freezes the closure and cannot add scope itself
  - rejects repo-policing heuristics when they are not the user-requested feature
  - when independent mapping or review is delegated, uses clean native
    read-only roles with disjoint lenses, parent synthesis, and repo-state proof
- Weak:
  - rubber-stamp approval
  - accepts agent-backed tooling without justifying why prompt-first options failed
  - accepts docs-audit scripts, stale-term greps, absence checks, or CI cleanliness gates as if they were meaningful feature safety
  - just repeats the phase plan
  - treats a full conversation fork or external process as the default meaning
    of fresh review, or lets a reviewer edit the compact doc

## Finish-mode audit

- Strong:
  - checks code reality against the compact doc
  - checks against the original human anchors and frozen closure, not merely the
    latest edited doc
  - treats unjustified scaffolding around agent-backed behavior as a real miss
  - names missing work if any
  - treats unauthorized built work as subtraction even when it passes
  - returns authorized repair to the exact implementer and uses a new clean
    read-only role for an independent recheck when one is useful
- Weak:
  - "looks good"
  - lets finish mode invent wrappers or scripts that the doc never justified
  - treats missing repo-policing heuristics as missing feature code
  - equates partial verification with completion
  - resumes a prior critic as an allegedly independent recheck or lets child
    edits bypass parent repo-state verification
