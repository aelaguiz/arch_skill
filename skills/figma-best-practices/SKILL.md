---
name: figma-best-practices
description: "Author, review, or repair Figma files, component libraries, variables, and handoff prep using research-backed file-craft best practices. Use when an agent is creating a Figma design-system plan, auditing a Figma file for Dev Mode/Code Connect/Make/MCP readiness, or translating design-system intent into Figma structure. Do not use for generic visual design critique, implementing code from a Figma design, or operating the Figma UI/tool itself."
metadata:
  short-description: "Apply modern Figma file-craft doctrine"
---

# Figma Best Practices

Use this skill when the work is Figma file craft: creating, reviewing, or
repairing Figma structures so they are readable by designers, developers,
Dev Mode, Code Connect, Figma Make, Sites, Buzz, Slides, and MCP-fed coding
agents.

This is a prompt-only skill. It ships no scripts, runners, controllers,
Figma API wrappers, browser automation, or MCP automation.

## When to use

- The user wants a Figma design-system plan, file structure, component model,
  variable/token architecture, library split, or publishing workflow.
- The user wants a Figma file, library, page, component set, prototype, or
  Dev Mode surface audited for structural quality.
- The user wants guidance on Auto Layout, Grid Auto Layout, constraints,
  variables, modes, styles, components, variants, slots, Code Connect,
  annotations, or AI/MCP readiness.
- The user wants to turn design-system intent into Figma-native structure
  before humans, developers, or models consume the file.

## When not to use

- The task is implementing frontend code from a Figma design. Use the relevant
  coding or Figma-implementation workflow instead.
- The task is operating the Figma UI, clicking through a file, or automating
  the Figma app itself. Use the appropriate browser, Figma, or MCP tool skill.
- The task is generic visual taste critique without any Figma file-structure,
  system, token, handoff, or downstream-consumer concern.
- The user needs the latest post-source Figma release facts. Verify current
  official docs or release notes before relying on changing limits or feature
  availability.

## Non-negotiables

- Treat a high-quality Figma file as a self-describing artifact, not a static
  picture. The file must survive content changes, team reuse, developer
  inspection, code mapping, and model consumption.
- Read `references/figma-file-craft.md` before giving detailed Figma guidance.
- Optimize for the six durable habits: variables over raw values, Auto Layout
  over free-form UI frames, components over duplicated shapes, sections for
  shippable scope, semantic layer names, and code-aligned component properties.
- Preserve Figma-native judgment. Do not turn this into a keyword checklist or
  insist on Auto Layout for illustrations, expressive hero art, FigJam, or
  other intentionally free-form work.
- Separate file-craft findings from product-design opinions. If the issue is
  visual taste, say so instead of laundering it as a Figma best practice.
- If inspecting a real artifact, ground every finding in visible structure:
  frame hierarchy, Auto Layout settings, variables, styles, components,
  properties, layer names, sections, annotations, branches, or publish state.
- For tool-mediated Figma work, treat successful MCP/API responses as
  provisional. Verify actual file state with returned node IDs, structure
  reads, fill reads, bounds checks, and screenshots of the target artifact.

## First move

1. Read `references/figma-file-craft.md`.
2. If the task involves Figma MCP/API inspection, writes, uploads, exports, or
   screenshot repair, also read `references/figma-mcp-agent-gotchas.md`.
3. Classify the job as `author`, `review`, or `repair`.
4. Identify the artifact being shaped: product file, library file, component
   family, token system, prototype, Dev Mode handoff, Make kit, Sites page,
   Buzz template, Slides deck, or MCP/Code Connect surface.
5. Identify the consumers that matter: designers, developers, Code Connect,
   Make, Sites, Buzz, Slides, MCP/IDE agents, or non-designer template users.
6. If a real file or screenshot is available, inspect it before prescribing
   fixes. If no artifact is available, produce a concrete structure or audit
   rubric instead of inventing file facts.

## Workflow

1. **Anchor the artifact.** State what kind of Figma surface is being created
   or judged, who will consume it, and what would break if the file is only a
   visual drawing.
2. **Check layout structure.** Look for Auto Layout defaults, correct
   Hug/Fill/Fixed use, min/max and wrap, Grid Auto Layout only for real
   two-dimensional layouts, constraints only where they still own behavior,
   and almost no groups in UI work.
3. **Check component architecture.** Prefer fewer, stronger components with
   exposed properties, slots, instance swaps, and subcomponents over
   variant-heavy mega-components or detached local copies.
4. **Check variables and styles.** Require a three-tier token system, scoped
   variables, modes where context changes, semantic naming, aliasing, and
   styles only where bundled multi-property decisions still belong.
5. **Check library and file operations.** Review page structure, naming,
   sections, cover, release notes, branching, publishing descriptions,
   dependency direction, deprecation policy, and versioning.
6. **Check downstream readiness.** Verify the file is prepared for Dev Mode,
   Code Connect, Make, Sites, Buzz, Slides, and MCP where those consumers are
   relevant.
7. **Return actionable judgment.** For reviews, lead with prioritized findings
   and evidence. For authoring, provide the exact Figma-native structure to
   build. For repairs, give the smallest ordered fix sequence that restores
   structural honesty without overbuilding.

## Output expectations

- `author`: a concrete Figma structure, naming scheme, variable/component
  architecture, or handoff plan with the relevant tradeoffs called out.
- `review`: findings first, ordered by downstream impact, with evidence from
  the file or a clear note when the artifact could not be inspected.
- `repair`: an ordered fix plan that names what to convert, rename, tokenize,
  componentize, annotate, deprecate, or publish.
- For all modes, include the relevant anti-patterns to avoid and a short
  acceptance check the user or agent can run against the Figma artifact.

## Reference map

- `references/figma-file-craft.md` - exhaustive Figma file-craft doctrine for
  layout, components, variables, styles, libraries, file structure,
  prototyping, Dev Mode, Code Connect, AI surfaces, MCP readiness, and
  anti-patterns.
- `references/figma-mcp-agent-gotchas.md` - operational gotchas for Figma
  MCP/API work, including page context, fonts, component properties, uploads,
  screenshots, and source-of-truth checks.
