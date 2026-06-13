# Figma Audit Toolkit

Use this reference when the task is to review, audit, triage, or plan repairs
for a Figma file, page, node, component, screenshot board, evidence board, or
app/source fidelity claim.

This is a toolkit, not a fixed workflow. Start from whatever the user supplied,
choose the lenses that fit the task, and state the confidence boundary when
evidence is incomplete.

## Intake

Accept partial, vague, or mixed inputs. A useful audit can start from:

- a Figma URL, file key, page, node, component name, screenshot, or export
- an app route, source file, token, asset, runtime state, or bug report
- a broad complaint such as "this file is messy" or "these screens overlap"
- a desired repair such as "make this clean enough for implementation"

First classify what is knowable:

- target identity: file, page, section, frame, component set, component,
  instance, screenshot board, evidence board, source map, sandbox, or archive
- artifact role: canonical, evidence, approximate, stale, draft/exploration,
  research/reference, out of scope, blocked, or not inspected
- confidence source: Figma structure, app/source files, screenshots, runtime
  state, tokens/assets, Code Connect/Dev Resources, or user-provided intent
- blocked evidence: what is missing and how that limits the verdict

Ask only when missing information blocks the requested confidence level. If the
task can proceed at a lower confidence, proceed and name the boundary.

## Target And App Matching

For app/source fidelity tasks, build a candidate match set before judging
correctness.

Target resolution signals:

- Figma URL, file key, page name, node ID, selected node, page/parent context
- node type, component-set membership, variant properties, descriptions, Dev
  Resources, Code Connect context, and component names
- visible labels, screenshot captions, route text, state names, and source
  annotations
- nearby evidence boards, source-map notes, screenshots, and `Index` links

App/source candidate signals:

- route, screen, page, story, component, widget, view, or template names
- source paths, token files, theme modes, asset manifests, and icon registries
- screenshot or golden names, test fixtures, snapshot state, and deeplink state
- Code Connect mappings, Dev Resources, Storybook links, ticket links, or handoff
  docs

Report ambiguity instead of choosing by taste. When multiple candidates remain,
state what separates them and what evidence would disambiguate the match.

## Evidence Tiers

Use the strongest available evidence and do not overclaim weaker evidence.

1. Explicit bidirectional source/design link: Code Connect, Dev Resource, source
   map, component description, or repo manifest that names both sides.
2. Component or source map: production component, token, asset, or route mapped
   to a Figma node or component.
3. Screenshot or capture manifest: runtime route/state and Figma node are both
   named with capture context.
4. Semantic/runtime snapshot: state, props, theme, locale, entitlement, or data
   fixture proves what was rendered.
5. Screenshot label or visible source hint: useful evidence, not source truth.
6. Visual similarity: triage signal only.
7. Name-only guess: weak candidate, never a pass.

When the evidence tier is weak, downgrade the verdict or mark the item
`Evidence only`, `Blocked`, or `Not inspected`.

## Verdicts

Use verdicts that match the evidence:

- `Pass`: required evidence is present and supports the claim.
- `Partial`: some claim surfaces are correct, but important coverage or proof is
  missing.
- `Fail`: the artifact contradicts source, runtime evidence, file-craft rules,
  or the requested standard.
- `Evidence only`: useful reference material exists, but it is not canonical or
  not sufficient for a pass.
- `Blocked`: the requested confidence cannot be reached with available access or
  artifacts.
- `Not inspected`: the surface was in scope but not reached.
- `Out of scope`: intentionally excluded from the current task.

Do not use `Pass` for metadata-only inspection, screenshot resemblance, local
component existence, tool success, or name similarity.

`Partial` is not approval. It must name the missing proof or missing artifact
work before the requested confidence can be reached. If the user asks whether a
file, component, parity claim, or handoff surface is ready, map `Partial` to not
ready unless the user asked only for triage.

## Severity

- `P0`: cannot be used as a reference or causes false implementation/parity
  claims.
- `P1`: high-confidence app/Figma/source drift or missing critical coverage.
- `P2`: important durability, componentization, naming, token, accessibility, or
  handoff issue.
- `P3`: cleanup, metadata, organization, or low-risk maintainability issue.
- `Info`: correct explicit exception or useful future improvement.

Severity is about downstream risk, not how annoying the file looks.

## App-Fidelity Match Surface

Use these categories as a menu. Do not require every category for every task.

- Comparison identity: app, platform, viewport, route, state, build, locale,
  theme, capture context, and Figma target.
- Route/flow coverage: screen coverage, state coverage, exception handling, and
  intentionally omitted flows.
- Geometry: size, spacing, position, crop, safe area, responsive behavior, and
  constraints.
- Color and effects: fill, stroke, opacity, gradient, shadow, blur, masks,
  clipping, border, radius, and platform rendering differences.
- Typography: family, weight, size, line height, casing, wrapping, truncation,
  platform text rendering, and text-style usage.
- Tokens and variables: Figma variables/styles, app tokens, modes, aliases,
  one-off values, and promotion/deprecation recommendations.
- Component identity: reuse, variants, properties, slots, wrappers, forks,
  source component ownership, and duplicate primitives.
- File placement: page/section/frame placement, lifecycle state, archive/stale
  labeling, `Index` accuracy, and no report dumping.
- Copy and data: exact copy, fixtures, dynamic values, localization, empty/error
  content, placeholders, and realistic content length.
- State and edge cases: loading, empty, error, disabled, selected, focus,
  entitlement, platform, edge content, and variant completeness.
- Interaction and motion: prototype/runtime differences, press/hover/focus,
  gesture, feedback, animation timing, and unsupported behavior boundaries.
- Accessibility and semantics: contrast, hit targets, focus order, labels,
  semantics, and usability exceptions.
- Native/platform behavior: OS chrome, density, status/navigation bars, native
  widgets, platform conventions, and safe-area treatment.
- Source usage: app component render path, token source, asset source, primitive
  bypasses, hardcoded values, and source-map validation.
- Screenshot evidence: screenshot boards, golden/baseline evidence, exact image
  identity, capture context, and evidence limits.
- Metadata and handoff: names, aliases, descriptions, searchability, Dev Mode,
  Ready for Dev, Code Connect, Make/MCP readiness, Dev Resources, source links,
  component descriptions, and handoff notes.
- Mess and drift: duplicates, stale artifacts, lookalikes, orphan screenshots,
  loose frames, section overlap, long text blobs, and source/doc drift.

## Duplicate, Stale, And Lookalike Review

Duplicates are not all defects. Classify first.

Signals:

- exact identity: same node, component key, asset hash, or source link
- normalized names: same intent after removing dates, status tags, copy suffixes,
  and generated prefixes
- structure signatures: same component set, variant surface, layer tree, bounds,
  text, and token usage
- app-side duplication: multiple source components or routes implementing the
  same concept
- screenshot evidence duplication: repeated captures, stale golden references,
  or duplicate image fills
- stale artifacts: contradicted by current source, app screenshots, `Index`,
  component descriptions, Dev Resources, or product intent

Legitimate repeats:

- variants, instances, responsive examples, platform differences, state samples,
  wrappers around a canonical inner component, screenshot contact sheets, and
  evidence boards

Finding fields:

- duplicate group or stale artifact
- artifact role
- source or Figma evidence
- legitimate-reuse explanation, if any
- risk
- recommended action: keep, label, move to evidence/archive, replace, merge, or
  delete

## Figma Cleanliness

Figma is a visual reference and design-system surface. It is not the long-form
audit report.

Allowed in Figma:

- visual references and compact labels
- component names, component descriptions, properties, and Dev Resources
- short Dev Mode annotations tied to design objects
- `Index` as the file-native map and convention contract
- evidence screenshots and source anchors when they remain visual and bounded

Keep outside Figma:

- audit reports
- duplicate indexes
- raw source maps
- acceptance matrices
- worklogs
- large tables
- long historical narratives
- generated proof dumps

If a note needs more than two short lines, a list of evidence, or a matrix, put
it in a repo doc and link it from `Index`, a component description, or a Dev
Resource.

## Audit Write Boundary

Audits are read-heavy by default. Do not mutate Figma during an audit unless the
user asks for authoring or repair.

When the user does ask for writes:

- inspect before writing
- keep writes scoped to the requested file/page/node
- preserve or update `Index` and file conventions
- verify returned node IDs, parentage, structure, bounds, fills, styles,
  variables, component properties, screenshots, and source links as applicable
- report any blocked verification instead of claiming success

## Output Contracts

Choose the smallest output shape that fits the task.

Findings:

- severity
- verdict
- Figma target
- app/source target, when relevant
- evidence
- impact
- recommended fix

Compliance checklist:

- requirement or expected standard
- Figma target
- app/source target, when relevant
- status
- evidence
- blocker, exception, or follow-up repair

Coverage ledger:

- surface
- expected source/app state
- Figma target
- status
- evidence
- blocker or exception

App-fidelity match ledger:

- comparison identity
- route/component/state
- source anchors
- screenshot/render anchors
- visual evidence
- source evidence
- verdict

Authorship ledger:

- artifact
- apparent source or creator signal
- current role: canonical, evidence, approximate, stale, draft, or blocked
- source ownership evidence
- reuse or deletion risk
- action

Handoff-readiness ledger:

- Figma target
- intended consumer
- Ready for Dev or handoff status
- component, variable, style, or source-link evidence
- missing metadata, annotation, Dev Resource, Code Connect, or source anchor
- blocking issue or recommended handoff repair

Style-guide gap ledger:

- style-guide surface
- expected token, component, variable, style, pattern, or naming rule
- observed Figma usage
- app/source evidence, when relevant
- gap type: missing, duplicated, hardcoded, stale, approximate, or blocked
- recommended promotion, repair, deprecation, or documentation action

Duplicate/stale ledger:

- group
- artifacts
- source or visual evidence
- classification
- risk
- action

Verification receipts:

- command, tool, or readback source
- target node/source path
- observed result
- confidence boundary
- blocked evidence

Repair plan:

- keep
- relabel
- move to evidence/archive
- replace with source-backed component
- merge/delete duplicate
- add or update token/component/style
- update `Index`, descriptions, Dev Resources, or handoff notes

## Acceptance Checks

For focused audits, the output should answer:

- What exactly was inspected?
- What role does the Figma artifact have?
- What source or runtime target owns the claim?
- Which evidence tier supports the verdict?
- Which duplicates, stale artifacts, or evidence-only surfaces were found?
- What is blocked, not inspected, or out of scope?
- Where should long proof live outside Figma?

For broad sweeps, also include:

- coverage boundaries
- skipped or blocked pages/nodes
- duplicate/stale groups
- source-map gaps
- handoff and metadata gaps
- repair priorities
