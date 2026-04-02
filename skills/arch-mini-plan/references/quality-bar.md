# Arch Mini Plan Quality Bar

## Research grounding

- Strong:
  - names the files or symbols that actually control the change
  - captures existing patterns worth reusing
  - calls out real constraints
- Weak:
  - generic repo tour
  - no file anchors
  - "we should probably" language without evidence

## Current and target architecture

- Strong:
  - explain where the behavior lives now
  - explain what changes after the work lands
  - make data flow and ownership obvious
- Weak:
  - paraphrase the ticket
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
  - explicit follow-ups separated from ship-blocking work
- Weak:
  - pseudo-chronological task dump
  - optional ideas mixed into required work
  - no verification bar

## Ready verdict

- Ready:
  - the implementer can start with `arch-step implement` and does not need to invent architecture
- Not ready:
  - open architecture questions still control the plan
  - the doc needs full-arch restructuring first
