# Review Output Contract

This file defines exactly two output shapes:

1. **Lens output** — one per parallel `codex exec` subprocess review agent.
2. **Final synthesis** — one final Codex invocation consuming the lens outputs.

Both shapes are findings-first, sparse, and evidence-backed. Placeholder sections and "None." filler are forbidden. Empty findings are a valid, useful outcome; the shapes below have explicit no-findings states.

## Finding schema (shared)

Every finding — blocking or non-blocking — MUST use this shape:

```markdown
### [BLOCKING|NON-BLOCKING] <short title>

- File: <repo-relative path>
- Symbol / line: <symbol name or L<line> or L<start>-L<end>>
- Risk: <one-to-three sentences of concrete risk in plain language>
- Fix touches: <what the fix should touch, without writing the fix>
- Evidence: <diff hunk excerpt, test output excerpt, external-source citation, or "see file" when the risk is self-evident from the cited location>
```

Rules:

- `File` paths MUST exist on disk; spot-check with `ls` before citing.
- `Evidence` MUST be real. No paraphrase of what "could" be there.
- External sources, when cited, use primary/authoritative references (official docs, OWASP, CERT, RFCs). Name the source.
- Do not include a "suggested patch" block. The skill is review-only.

## Lens output shape

Each lens subprocess MUST emit exactly this shape and nothing else:

```markdown
## Lens: <lens-name>

<findings section — see below>

## Coverage notes

- Inspected: <what this lens inspected (files, symbols, ranges, or "the full diff")>
- Skipped: <what this lens did NOT inspect and why (e.g., "security lens: no security-adjacent surface touched by this change")>
- External sources consulted: <list of source URLs, or "none">
- Agent-linter: <"invoked" | "not applicable" | "coverage failure: <why>">  # only present on the agent-linter lens
```

### Lens findings section — three valid states

**State A: one or more findings**

```markdown
## Findings

### [BLOCKING] <title>
- File: ...
- Symbol / line: ...
- Risk: ...
- Fix touches: ...
- Evidence: ...

### [NON-BLOCKING] <title>
- File: ...
- Symbol / line: ...
- Risk: ...
- Fix touches: ...
- Evidence: ...
```

**State B: no findings**

```markdown
## Findings

No findings for this lens.
```

**State C: coverage failure**

```markdown
## Coverage failure

- Reason: <specific reason — e.g., "target diff was empty", "agent-linter not installed", "required convention source missing: AGENTS.md">
- What the synthesis should do: <"treat this lens as not-run" | "block final verdict on coverage">
```

If a lens emits State C, it MUST NOT also emit findings. State C means the lens could not do its job.

## Final synthesis shape (`ReviewVerdict`)

The synthesis subprocess MUST emit exactly this shape and nothing else:

```markdown
# ReviewVerdict

VERDICT: <approve | approve-with-notes | not-approved>

## Blocking findings

<one or more findings in the shared finding schema, OR the literal line "No blocking findings.">

## Non-blocking findings

<one or more findings in the shared finding schema, OR the literal line "No non-blocking findings.">

## Coverage notes

- Lenses run: <comma-separated list of lens names that completed successfully>
- Lenses with coverage failures: <list, or "none">
- Docs/contract drift inspected: <yes | no — with one-line justification>
- External research consulted: <list of source URLs, or "none">
- Agent-linter: <"invoked" | "not applicable" | "coverage failure: <why>">
- Repo-local convention sources consulted: <list of paths, or "none found">

## Reviewer notes

<optional, at most one paragraph — used only for honest context the caller needs to act on the verdict; omit the section entirely if there is nothing to add>
```

### `VERDICT` decision rules

- `approve` — no blocking findings AND no lens emitted a trust-breaking coverage failure.
- `approve-with-notes` — no blocking findings AND non-blocking findings exist OR lens coverage failures exist that the synthesizer judges do not break trust.
- `not-approved` — at least one blocking finding OR a lens coverage failure prevents a trustworthy review (e.g., required agent-linter unavailable on an agent-surface target).

When a coverage failure drives `not-approved`, the top blocking finding MUST be the coverage failure itself, cited as a finding with `File`/`Symbol` replaced by the missing lens name and `Risk` stating what the failure prevents.

## Malformed output handling

The runner MUST reject any lens or synthesis output that:

- omits the required sections for its shape
- emits findings without the required fields
- claims agent-linter coverage when `$agent-linter` did not run
- includes a "suggested patch" or similar fix-writing block

When the runner detects malformed output, it MUST fail loud, preserve the raw output under the run directory, and name the offending file in its error message. Do NOT hand-write a verdict on the reviewer's behalf.

## No-findings is a first-class outcome

If the synthesis concludes the change is clean within the scope the lenses covered, it MUST emit:

- `VERDICT: approve`
- `No blocking findings.`
- `No non-blocking findings.`
- honest coverage notes

Do NOT manufacture a finding to justify the review running.
