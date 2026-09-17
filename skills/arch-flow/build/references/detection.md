# Arch Flow Detection

Flow-family detection and artifact sanity checks. Detect what kind of doc you are reading before you build the checklist.

## Detection order

- Treat a doc as `lilarch` when it has lilarch-specific blocks such as `lilarch:block:requirements` or `lilarch:block:plan_audit`.
- Treat a doc as `arch-mini-plan` follow-through when it has the canonical arch blocks and phase plan, but no evidence that full-arch implementation has started and the artifact still reads like a one-pass handoff doc.
- Treat a doc as `miniarch-step` when it has the canonical arch blocks and mini full-arch execution has started or the artifact clearly lacks the broader `arch-step` helper surface.
- Otherwise treat it as a full-arch doc governed by `arch-step`.

## Sanity checks

- If `DOC_PATH` is missing, say so directly.
- If the doc is structurally non-canonical, still classify it as best you can, then recommend the repair move.
- Do not invent a fourth family because the artifact is messy.
