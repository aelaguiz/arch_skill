# Agent History Failure Examples Pack

Date: 2026-06-25

This doc pack preserves the concrete Codex-history examples used by:

- `../AGENT_HISTORY_RECURRING_FAILURE_PATTERNS_2026-06-25.md`

It exists so `~/.codex` can be cleaned later without losing the important
evidence.

## Files

- `COPIED_EXAMPLES.md` - copied, human-readable transcript excerpts for each
  failure pattern.

## Preservation Level

This is a curated evidence pack, not a raw transcript mirror.

Copied:

- timestamps,
- session ids,
- original local transcript paths,
- line numbers,
- user corrections,
- assistant completion or acknowledgement snippets,
- why each example matters.

Not copied:

- base64 images,
- encrypted reasoning blobs,
- token-count events,
- full developer/system prompts,
- giant tool outputs,
- unrelated surrounding transcript.

That keeps the durable examples useful after Codex cleanup without turning the
repo into a full private transcript dump.

## Pattern Catalog

| Id | Pattern | Example |
| --- | --- | --- |
| E01 | False completion / authority drift | Marked complete, then user forced adversarial audit. |
| E02 | Surface completion challenged | User demanded line-by-line plan audit after another done claim. |
| E03 | Docs/status substituted for code | User redirected from doc hygiene to literal code requirements. |
| E04 | Plan reread not treated as gate | User identified missing plan reread and weak reviewer gating. |
| E05 | Goal prompt became source truth risk | User said not to copy plan content into prompt files. |
| E06 | Implemented in name, not in fact | User requested audit doctrine for name-only implementations. |
| E07 | Source-truth cataloging became doctrine | User requested explicit source/pattern cataloging phases. |
| E08 | Scratch output instead of durable docs | Agent saved analysis to `/tmp`; user demanded docs dir. |
| E09 | Names/comments not accepted as proof | User told agent to trace through and assume duplicate truth. |
| E10 | Historical split rationalized | Agent leaned on current names/classes; user forced first principles. |
| E11 | Emerged code patterns treated as design | User rejected accidental implementation splits as architecture. |
| E12 | Branch/live-process confusion | Agent edited one checkout while live Flutter run came from another. |
| E13 | Hidden automation over user-facing proof | User required real user-facing controls and visible checkpoints. |
| E14 | Harness overbuild | User corrected a permanent framework impulse into fast diagnostics. |
| E15 | Traps/logs over harnesses | User asked for aggressive throws/logs, not big harnesses. |
| E16 | Tiny visual fix became policy | Shader z-order tweak became a larger policy. |
| E17 | Product workflow missed | Audio editor changed options but could not assign sound to silence. |
| E18 | Visual evidence discounted | Agent trusted crop math until screenshot proof forced correction. |
| E19 | Scope contamination | Chip-stack label work accidentally changed action ribbons. |
| E20 | Fake readiness receipts | Agent claimed six ready plans after implausibly short process. |
| E21 | Process receipt theater repeated | Agent again claimed deep planning stages in implausible time. |
| E22 | Parallel-agent evidence mishandled | Parent stopped another agent before its evidence was saved. |
| E23 | Wrong skill / wrong execution mode | User corrected wrong skill routing and "do the audit" failure. |

## Use

When updating skills, prompts, review gates, or goal templates, use this pack
as a concrete failure corpus. The useful question is:

> Which of these examples would the new instruction have prevented?
