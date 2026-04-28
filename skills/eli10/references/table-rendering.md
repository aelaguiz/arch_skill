# ELI10 Renderer-Aware Tables

Use this reference when an ELI10 answer has compact grid-shaped information and
the renderer matters.

Tables are not proof of clarity. A table helps only when the cells stay short
and the reader can scan the whole row without reconstructing wrapped text.

## Renderer Split

- **Claude / Claude Code:** use native Markdown tables for compact tables.
  Claude renders Markdown tables cleanly.
- **Codex:** avoid Markdown pipe tables for important information. Generate a
  Unicode table with `scripts/render_codex_table.py` and place it in a fenced
  `text` block.
- **Unknown renderer:** default to bullets, key/value blocks, or short labeled
  sections.

Do not use the Codex Unicode renderer in Claude unless the user explicitly asks
for Codex-compatible output.

## Codex Helper

Preferred command:

```bash
uv --quiet run --script skills/eli10/scripts/render_codex_table.py
```

Direct command:

```bash
python3 skills/eli10/scripts/render_codex_table.py
```

The direct command re-execs through `uv --quiet run --script` when `rich` is
not importable in the active Python environment.

Example input:

```json
{
  "title": "Metric Snapshot",
  "columns": [
    {"key": "metric", "label": "Metric"},
    {"key": "value", "label": "Value", "justify": "right", "kind": "number"},
    {"key": "meaning", "label": "Meaning"}
  ],
  "rows": [
    {"metric": "AIVAT lift", "value": "+3.2", "meaning": "RTS won after noise reduction"},
    {"metric": "CI width", "value": "8.4", "meaning": "Evidence is still noisy"}
  ]
}
```

Codex output:

```text
                   Metric Snapshot
╭────────────┬───────┬───────────────────────────────╮
│ Metric     │ Value │ Meaning                       │
├────────────┼───────┼───────────────────────────────┤
│ AIVAT lift │  +3.2 │ RTS won after noise reduction │
│ CI width   │   8.4 │ Evidence is still noisy       │
╰────────────┴───────┴───────────────────────────────╯
```

If the script returns `NO_TABLE:`, respect it. The rejection means the table is
likely to make the answer harder to read.

## Good Table Uses

Use tables for compact, repeated shapes:

- option comparisons with short labels
- metric snapshots with numeric values
- before/after differences
- small status grids
- short good/bad contrasts

### Good: Claude Native Markdown

Use this in Claude:

```markdown
| Choice | Best For | Risk |
|---|---|---|
| Markdown table | Claude answers | Bad in Codex |
| Rich Unicode | Codex answers | Only for short cells |
| Bullets | Long explanations | Less compact |
```

### Good: Codex Unicode Table

Use this in Codex:

```text
                         Option Fit
╭────────────────┬───────────────────┬──────────────────────╮
│ Choice         │ Best For          │ Risk                 │
├────────────────┼───────────────────┼──────────────────────┤
│ Markdown table │ Claude answers    │ Bad in Codex         │
│ Rich Unicode   │ Codex answers     │ Only for short cells │
│ Bullets        │ Long explanations │ Less compact         │
╰────────────────┴───────────────────┴──────────────────────╯
```

### Good: Split Logical Tables

When there are two separate meanings, split them.

Good:

```text
✅ Keep
- Metrics: short repeated values.
- Status: one-word states.

⚠️ Avoid
- Long explanations: they wrap.
- Proof paths: they belong after the meaning.
```

Also acceptable in Codex when each table stays small:

```json
{
  "tables": [
    {
      "title": "Keep",
      "columns": ["Case", "Why"],
      "rows": [["Metrics", "Short repeated values"]]
    },
    {
      "title": "Avoid",
      "columns": ["Case", "Why"],
      "rows": [["Long prose", "Wraps into unreadable blocks"]]
    }
  ]
}
```

## Bad Table Uses

Bad tables usually fail because the apparent structure is visual, not mental.
The table looks organized, but the reader still has to untangle wrapped prose.

### Bad: Dense Audit Matrix

This is the canonical bad case:

```text
| Area | File / Symbol | Pattern to adopt | Why (drift prevented) | Proposed scope (include/defer/exclude/blocker question) |
|---|---|---|---|---|
| Shared per-kind doctrine | shared/prompts/playable_kind_selection_contract/AGENTS.prompt | One shared contract emitted into every kind skill | Prevents 32 packages from drifting on evidence posture, label-shim language, and "not good for" semantics | include |
```

Why it fails:

- five dense columns
- long path-like cells
- long prose cells
- rationale and decision state crammed into the same row
- Codex wrapping destroys the row boundary
- the user has to reconstruct the meaning from broken visual layout

Better ELI10 shape:

```text
Pattern Consolidation Sweep

✅ Include now
- Shared per-kind doctrine: emit one shared contract into every kind skill.
  Why: prevents 32 packages from drifting on evidence posture and label-shim language.

- Existing hard-kind skills: add selection-fit sections without changing proof-owner flow.
  Why: prevents duplicate selection packages from competing with proof specialists.

⚠️ Defer
- MCP playable-author contexts: read as adjacent evidence only.
  Why: useful for contradictions, but too wide for this pass.

❌ Exclude unless factual drift is found
- Runtime schemas/renderers: preserve runtime truth.
  Why: prompt work should not smuggle product changes.

Proof:
- Put long paths here, after the meaning.
```

If a table is still useful, split it by decision:

```text
Include Now
╭──────────────────────────┬──────────────────────────────╮
│ Area                     │ Move                         │
├──────────────────────────┼──────────────────────────────┤
│ Shared per-kind doctrine │ Emit one shared contract     │
│ Hard-kind skills         │ Add selection-fit sections   │
╰──────────────────────────┴──────────────────────────────╯
```

Then keep paths and long rationale outside the table.

### Bad: Root Cause Forced Into A Table

Bad:

```markdown
| Symptom | Cause | Fix |
|---|---|---|
| It restarted Android | Readiness check mismatch | Change check |
```

Why it fails:

- the user asked why, not for a compressed ticket
- the system belief is the important part
- the fix is unsolicited if the user only asked for explanation

Better:

```text
It did not think Android was missing. It thought its own readiness check had not passed.

🧠 Mechanism:
The simulator window can be visible before the worker sees the exact "booted and reachable" signal it waits for.

Net: the visible symptom was Android opening; the root cause was the worker's readiness check.
```

### Bad: Long Commands In Cells

Bad:

```markdown
| Step | Command | Why |
|---|---|---|
| Verify | uv --quiet run --script skills/eli10/scripts/render_codex_table.py --self-test | Confirms renderer setup |
```

Better:

Verify the renderer:

```bash
uv --quiet run --script skills/eli10/scripts/render_codex_table.py --self-test
```

Why: confirms `uv` can install `rich` and the table renderer works.

### Bad: Path Wall Table

Bad:

```markdown
| File | Meaning | Action |
|---|---|---|
| skills/eli10/scripts/render_codex_table.py | Owns Codex-safe rendering and uv bootstrap | Edit |
| skills/eli10/references/table-rendering.md | Owns examples and anti-examples | Edit |
```

Better:

```text
The split is simple:

✅ Runtime helper:
`skills/eli10/scripts/render_codex_table.py` owns Codex-safe rendering.

✅ Teaching reference:
`skills/eli10/references/table-rendering.md` owns examples and anti-examples.
```

Use path tables only when the paths are short and the table has no prose-heavy
cells.

## Rejection Rules To Remember

For Codex, the helper rejects:

- more than five columns
- columns that would become too narrow
- cells with newlines
- cells that behave like paragraphs
- cells that would wrap beyond two lines
- more than twelve rows in one table
- Markdown pipe-table input
- dense audit matrices

These are not arbitrary style rules. They are there because a bad table makes
the user read the formatting instead of the idea.

## Final Check

Before using a table, ask:

- Can the reader understand each row in one glance?
- Are the cells short labels, values, or phrases?
- Is this a real comparison, not an explanation pretending to be a comparison?
- Would bullets be clearer?
- Is the renderer Claude, Codex, or unknown?

Net: if the table makes the answer feel clever but harder to read, do not use
the table.
