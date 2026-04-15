# Arch Mini Plan Quality Bar

## Research grounding

- Strong:
  - names the files or symbols that actually control the change
  - captures existing patterns worth reusing
  - when agent-backed, names prompt surfaces, native capabilities, and capability-first options before blessing tooling
  - when instruction-bearing source exists, keeps explicit structure visible instead of paraphrasing it away
  - calls out real constraints
- Weak:
  - generic repo tour
  - assumes the model lacks capability without grounded evidence
  - silently condenses prompt or agent doctrine into vague summary bullets
  - no file anchors
  - "we should probably" language without evidence

## Current and target architecture

- Strong:
  - explain where the behavior lives now
  - explain what changes after the work lands
  - when agent-backed, explain what belongs in prompt/native-capability use versus deterministic code
  - preserve instruction-bearing operational structure when that content is being ported
  - make data flow and ownership obvious
- Weak:
  - paraphrase the ticket
  - jumps to custom scaffolding without a capability-first rationale
  - list components without relationships
  - describe outcomes but not structure

## Call-site audit

- Strong:
  - concrete files or call-site families
  - notes deletes, migrations, and new ownership
- Weak:
  - "update all usages"
  - no count, no representative sites, no delete story

## Phase plan

- Strong:
  - 1-2 real phases, optionally 3 for cleanup
  - each phase has goal, work, verification, and done bar
  - agent-backed plans prefer prompt, grounding, and native-capability changes before new tooling
  - instruction-bearing imported content is preserved explicitly or escalated rather than silently compressed
  - explicit follow-ups separated from ship-blocking work
- Weak:
  - pseudo-chronological task dump
  - agent-backed tooling is included with no justification against prompt-first options
  - optional ideas mixed into required work
  - no verification bar

## Ready verdict

- Ready:
  - the implementer can start with `miniarch-step implement` and does not need to invent architecture
- Not ready:
  - open architecture questions still control the plan
  - the doc needs full-arch restructuring first
