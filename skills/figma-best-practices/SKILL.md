---
name: figma-best-practices
description: "Author, review, or repair Figma files, component libraries, variables, handoff surfaces, and source-backed app/Figma fidelity audits using prompt-first file-craft doctrine. Use for Figma organization, components, tokens, Dev Mode/Code Connect/Make/MCP readiness, duplicate/stale cleanup, screenshot/reference handling, and app/source parity evidence. Do not use for generic visual taste critique, implementing frontend code from Figma, operating the Figma UI/tool itself, or deterministic visual-diff automation."
metadata:
  short-description: "Apply Figma file-craft and fidelity audit doctrine"
---

# Figma Best Practices

Use this skill when the work is Figma file craft: creating, reviewing, or
repairing Figma structures so they are readable by designers, developers,
Dev Mode, Code Connect, Figma Make, Sites, Buzz, Slides, and MCP-fed coding
agents.

Use the same skill when the user asks whether Figma accurately reflects an app,
source component, token system, asset set, screenshot, or runtime state. Treat
that as source-backed review work inside this skill, not as a separate mode,
runner, or app-fidelity skill.

This is a prompt-only skill. It ships no scripts, runners, controllers, Figma
API wrappers, browser automation, OCR stacks, fuzzy matchers, or visual-diff
harnesses.

## When to use

- The user wants a Figma design-system plan, file structure, component model,
  variable/token architecture, library split, or publishing workflow.
- The user wants a Figma file, page, component set, screenshot board, evidence
  board, or Dev Mode surface audited for structural quality.
- The user wants source-backed app/Figma fidelity review: target classification,
  app/source matching, screenshot/reference handling, duplicate/stale analysis,
  visual parity evidence, or repair planning.
- The user wants guidance on Auto Layout, Grid Auto Layout, constraints,
  variables, modes, styles, components, variants, slots, Code Connect,
  annotations, Dev Resources, or AI/MCP readiness.
- The user gives an incomplete Figma URL, node, screenshot, source hint, vague
  complaint, or broad cleanup request and needs grounded judgment about what is
  knowable.

## When not to use

- The task is implementing frontend code from a Figma design. Use the relevant
  coding or Figma-implementation workflow instead.
- The task is operating the Figma UI, clicking through a file, or automating
  the Figma app itself. Use the appropriate browser, Figma, or MCP tool skill.
- The task is generic visual taste critique without any Figma file-structure,
  system, token, handoff, parity, or downstream-consumer concern.
- The user needs deterministic visual-diff automation, OCR, parser stacks, or a
  Figma MCP wrapper. This skill can describe evidence expectations, but it does
  not provide tooling.
- The user needs the latest post-source Figma release facts. Verify current
  official docs or release notes before relying on changing limits or feature
  availability.

## Non-negotiables

- Treat a high-quality Figma file as a self-describing artifact, not a static
  picture. The file must survive content changes, team reuse, developer
  inspection, code mapping, and model consumption.
- Accept whatever Figma-related input the user supplies. Classify what is
  knowable, name evidence gaps, and ask only when missing information blocks the
  requested confidence level.
- Preserve the existing `author`, `review`, and `repair` surfaces. App/source
  fidelity audits live inside `review`; do not create a new runtime mode
  selector.
- Use adaptive reference selection. Load the smallest owned reference set that
  fits the task, then compose tools and evidence levels instead of following a
  mandatory workflow.
- Keep Figma clean. Long reports, duplicate indexes, source maps, acceptance
  matrices, and worklogs belong in repo docs or chat, not as canvas text. The
  only text-heavy native Figma page is `Index`, and it is a map, not a report.
- Preserve Figma-native judgment. Do not turn this into a keyword checklist or
  insist on Auto Layout for illustrations, expressive hero art, FigJam, or
  other intentionally free-form work.
- For tool-mediated Figma work, treat successful MCP/API responses as
  provisional. Verify actual file state with returned node IDs, structure
  reads, fill reads, bounds checks, and screenshots of the target artifact.
- For audit work, default to read-heavy inspection. Write to Figma only when
  the user asks for authoring or repair, then verify with readback and visual
  proof.
- Do not treat tool success, `get_metadata`, upload hashes, generated component
  names, local component existence, screenshot resemblance, or name similarity
  as proof by themselves.
- A source-backed claim must name the source component, token source, asset
  source, runtime state, screenshot, product decision, or verification anchor
  that owns the truth. If that evidence is unavailable, use `Evidence only`,
  `Blocked`, or another bounded verdict rather than inventing a pass.
- A pixel-perfect or visual-parity claim requires an explicit source pair,
  render proof, dimensions, normalization, ignored regions, and blocker
  disclosure.
- Keep generated and imported Figma work clearly separated from canonical
  library work. A plausible local component is not canonical until it is
  source-mapped, named, and verified.
- Runtime doctrine must stay self-contained in this skill package. Do not route
  users to planning docs, local source packs, or hidden repo context to
  understand the guidance.

## First Move

1. Start from the user's actual artifact or complaint. Do not reject partial,
   vague, mixed, or indirect inputs up front.
2. Classify the job as `author`, `review`, or `repair`.
3. Classify the artifact role before judging it: canonical, evidence,
   approximate, stale, draft/exploration, research/reference, out of scope,
   blocked, or not inspected.
4. Load references by need:
   - Always read `references/figma-file-craft.md` for detailed Figma guidance.
   - Read `references/figma-mcp-agent-gotchas.md` for MCP/API inspection,
     writes, uploads, exports, screenshots, or tool-mediated repair.
   - Read `references/figma-source-backed-parity.md` when the artifact claims
     production truth from code, tokens, assets, screenshots, or runtime
     behavior.
   - Read `references/figma-audit-toolkit.md` for audits, evidence-ranked
     verdicts, target/app matching, duplicate/stale cleanup, report contracts,
     or broad file sweeps.
   - Read `references/figma-visual-fidelity.md` for source-pair manifests,
     screenshot/reference handling, fast structural scans, exact asset checks,
     deterministic capture expectations, or visual parity claims.
5. Identify the consumers that matter: designers, developers, Code Connect,
   Make, Sites, Buzz, Slides, MCP/IDE agents, or non-designer template users.
6. If a real file, node, screenshot, or source path is available, inspect it
   before prescribing fixes. If no artifact is available, produce a concrete
   structure, audit plan, or evidence boundary instead of inventing file facts.

## Working Posture

For authoring:

- Provide Figma-native structure: pages, `Index`, sections, frames,
  components, variables, modes, component properties, descriptions,
  Dev Resources, and handoff surfaces.
- Keep canvas chrome consistent across the file. Product theme belongs inside
  mockup frames, not in random page backgrounds or section fills.
- Use component descriptions and Dev Resources for compact source truth; use
  external docs for long proof.

For review:

- Lead with prioritized findings and evidence. Distinguish file-craft issues
  from product-design opinions.
- Classify artifacts before reuse. Screenshots, generated components, imported
  boards, and approximate repairs are evidence until source-backed proof
  promotes them.
- Use verdicts that match the evidence: `Pass`, `Partial`, `Fail`, `Evidence
  only`, `Blocked`, `Not inspected`, or `Out of scope`.
- `Partial` is evidence grading, not approval. It must name the missing proof or
  missing artifact work before the requested confidence can be reached. For
  readiness questions, treat `Partial` as not ready unless the user asked only
  for triage.
- For fidelity claims, require source-pair identity and rendered or explicitly
  blocked visual evidence.

For repair:

- Give the smallest ordered repair path that restores structural honesty
  without overbuilding.
- Remove or relabel duplicate, stale, generated, or approximate artifacts that
  would pollute component search or Assets surfaces.
- Update `Index`, descriptions, Dev Resources, component names, and handoff
  notes when the repair changes file conventions or source ownership.

## Output Expectations

- `author`: a concrete Figma structure, naming scheme, variable/component
  architecture, or handoff plan with relevant tradeoffs.
- `review`: findings first, ordered by downstream impact, with file/source
  evidence and explicit blockers.
- `repair`: an ordered fix plan that names what to convert, rename, tokenize,
  componentize, annotate, deprecate, delete, or verify.
- Audit outputs should live in chat or repo docs. Use checklists and ledgers
  only when the task needs them: compliance checklist, coverage, app-fidelity
  match surface, authorship, handoff readiness, style-guide gaps,
  duplicate/stale artifacts, verification receipts, or repair plan.
- Include a short acceptance check that a human or agent can run against the
  Figma artifact or source evidence.

## Reference Map

- `references/figma-file-craft.md` - Figma file-craft doctrine for layout,
  components, variables, styles, libraries, page organization, `Index`,
  Dev Mode, Code Connect, AI surfaces, MCP readiness, and anti-patterns.
- `references/figma-mcp-agent-gotchas.md` - operational gotchas for Figma
  MCP/API work, including page context, fonts, component properties, uploads,
  screenshots, readback, bounds, and source-of-truth checks.
- `references/figma-source-backed-parity.md` - source-truth discipline for
  production-backed Figma components and parity claims, including code, token,
  asset, runtime, and claim-boundary semantics.
- `references/figma-audit-toolkit.md` - audit toolkit for permissive intake,
  artifact roles, evidence tiers, verdicts, severity, target/app matching,
  duplicate/stale review, clean reporting, and repair contracts.
- `references/figma-visual-fidelity.md` - visual-fidelity method for source
  pairs, screenshots, fast structural scans, exact asset checks, deterministic
  captures, normalized comparison, and pixel-parity boundaries.
