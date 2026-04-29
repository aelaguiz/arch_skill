# Figma File Craft

Use this reference when a Figma file, library, component system, prototype, or
handoff surface needs to be created, reviewed, or repaired. The central rule is
simple: a strong Figma file is a self-describing, structurally honest artifact.
It should be readable not only by a designer on the canvas, but also by Dev
Mode, Code Connect, Figma Make, Sites, Buzz, Slides, and MCP-fed coding agents.

The durable habits are:

- variables instead of raw values
- Auto Layout instead of free-form UI frames
- components instead of duplicated shapes
- sections to scope shippable work
- semantic layer and component names instead of auto-generated labels
- Figma component properties that match code props where code mapping matters

Pixel pushing is the enemy. A static drawing may look correct until text grows,
the locale changes, a theme switches, a developer inspects the file, a model
reads it, or a downstream product tries to publish from it.

## Layout

### Auto Layout is the default for UI

Wrap virtually every UI frame in Auto Layout by default. Auto Layout encodes
the same intent that frontend code will express through flex, grid, gap,
padding, and alignment. It improves Dev Mode output, Code Connect mapping,
Figma Make generation, and resilience to content changes.

Use the stretch test: drag an unfinished component to odd dimensions. If the
content, spacing, and alignment still behave, the structure is probably healthy.

### Hug, Fill, and Fixed

- `Hug` belongs on an Auto Layout parent when the parent should shrink to its
  children plus padding. Use it for buttons, chips, tags, tooltips, and other
  content-driven surfaces.
- `Fill` belongs on a child when it should take available space. Use it for
  inputs, table cells, row labels, and equal columns.
- `Fixed` locks an invariant dimension. Use it for icons, avatars, switches,
  and other fixed-size elements.

Important caveat: if any child is set to `Fill` on an axis, the parent cannot
`Hug` that axis and effectively becomes fixed there. Multiple sibling children
set to `Fill` divide the available space equally, which is the clean way to
make equal-width columns without manually assigning widths.

### Min, max, and wrap

Min/max width and height turn Auto Layout from static arrangement into real
responsive behavior.

- Use min-width on buttons so short labels do not collapse into cramped pills.
- Use max-width on paragraphs to preserve readable line length.
- Use horizontal wrap for tag clouds, filter-chip rows, and responsive card
  grids that reflow from more columns to fewer columns.
- Give wrapped children explicit min-widths. Without child min-widths, Figma
  has no clear break point and wrap appears not to work.
- Bind min/max values, gaps, padding, and spacer dimensions to number variables
  when the same responsive measure belongs to the system.

### Ignore Auto Layout and constraints

Absolute positioning inside Auto Layout is now named `Ignore auto layout`.
Use it when a child should be anchored without pushing siblings:

- notification badges
- tooltips
- sticky bottom panels
- floating action buttons
- decorative overlays on hero images
- scrollbars over menus
- custom z-order avatar stacks

Ignored children pick up constraints inside the Auto Layout parent. Negative
gap is the better tool for simple overlap like avatar groups, with layer order
controlling z-index.

Constraints still matter, but in a smaller role. They govern children of
non-Auto-Layout frames, Auto Layout frames inside non-Auto-Layout parents, and
ignored Auto Layout children. Use them for proportional artwork, anchored
badges, floating elements, centered modals, loaders, and responsive marketing
composition. Avoid `Scale` for normal UI because it distorts text and icons;
use it for proportional artwork. Constraints do not work on groups, so convert
groups to frames.

### Grid Auto Layout and layout guides

Use Grid Auto Layout for true two-dimensional structures: bento grids,
dashboards, galleries, and layouts with real row/column relationships such as
one-third plus two-thirds splits. Do not replace one-dimensional flex flows
with grid. Content that flows in a line and wraps to the next line still belongs
in horizontal Auto Layout wrap.

Known Grid Auto Layout limits to respect:

- no percentage tracks
- no named areas
- no subgrid
- no Hug on rows or columns
- no `minmax()`
- reordering layers changes z-index, not display order

Layout guides are visual overlays. They do not move objects. They remain useful
for page-level rhythm, alignment, legacy responsive flows, and children that
attach to stretch grids through constraints. Use an 8-point base grid for most
UI and 4-point increments for dense surfaces like toolbars and tables.

### Useful Auto Layout recipes

- Auto-spacing divider: one divider layer set to `Fill` width inside a vertical
  Auto Layout card.
- Tooltip tail: component set with a variant per tail position, placed via
  `Ignore auto layout`.
- Equal flex columns: sibling children all set to `Fill`, no manual width.
- Variable-driven spacer: a thin Auto Layout frame with width or height bound
  to a number variable.
- Space-between navbar: horizontal Auto Layout with gap set to `Auto`, matching
  CSS `justify-content: space-between`.

### Layout anti-patterns

- manual eyeballed gaps instead of gap
- fixed widths where children should Fill
- spacer-frame clutter when a number variable on gap or padding would do
- deeply nested unnecessary Auto Layout frames
- fixed-size text boxes that overlap when content grows
- sticky elements as regular Auto Layout children instead of ignored children
- inconsistent group/frame mixing

Auto Layout is not for everything. Do not force it onto free-form
illustrations, expressive hero compositions, deliberately rotated or overlapping
marketing layouts, FigJam diagrams, or Figma Draw work.

## Components

### Make fewer components and expose more

Create a component when the same configuration appears two or three times and
maintenance updates are expected. Do not pre-componentize exploratory work.
Keep exploration on a discovery or sandbox page, promote cross-team work to a
staging library, and graduate stable work to a published global library.

Main components belong in dedicated published library files. Do not keep the
canonical components inside product files where designers can accidentally
instance from the wrong source.

### Variant property or separate component

Use variants when the structure is identical and only state changes:

- size
- hierarchy
- count
- status
- other mutually exclusive enumerated states

Split into separate components when:

- there is a meaningful hierarchy difference
- composition changes substantially across contexts
- the visual style is fundamentally different
- independent versioning matters
- a boolean such as `iconOnly` would warp layout, padding, or dimensions

Example: if a normal button and icon button need different dimensions and
padding, ship `Button` and `IconButton`. If the difference can be expressed
cleanly through an icon-position variant and visibility property, keep one
component.

### Avoid variant explosion

Every new parallel variant property multiplies maintenance. Replace variant
axes with the right property type where possible:

- Use booleans for orthogonal visibility toggles.
- Use instance swap for guarded content replacement.
- Use text properties for repeated strings and labels.
- Use nested instance properties to expose child controls without multiplying
  parent variants.
- Split hierarchy or composition changes into separate components.

Do not build mega-components that try to express every possible card, row,
dialog, or button through variants. Prefer compound components such as
`Card`, `Card.Header`, `Card.Body`, and `Card.Footer` when the design needs
rich composition.

### Never use variants for icons

Each icon should be its own component. Variants are wrong for icon libraries
because variant dropdowns lack useful preview/search behavior, load every
variant into memory, and require manual alphabetization.

Icon components should have:

- slash naming such as `Icon/16/check`, `Icon/24/check`, or `Icon/Format/Bold`
- a standardized frame size
- a flattened inner shape when finalized
- a consistent inner layer name, commonly `Vector`, so color overrides survive
  swapping

### Component property types

- `Variant` properties handle mutually exclusive enumerated states. They pin to
  the top of the property panel and cannot be interleaved with other property
  types.
- `Boolean` properties bind to layer visibility. Use them for `Show icon`,
  `Has divider`, and `Has supporting text`. Phrase them positively so `True`
  reads as visible or present.
- `Instance swap` properties are for guarded single-item replacement with a
  fixed footprint, such as icon slots or avatar slots. Set preferred values and
  provide a real default instance rather than an empty placeholder.
- `Text` properties replace direct text overrides with a single field. They are
  useful when one string drives multiple nested elements, such as a visible
  label and an accessibility label.
- `Nested instance` properties expose a child component's properties at the
  parent level. They can collapse huge variant sets, but exposure is
  all-or-nothing, so keep nested components lean.

### Slots and composition

Use slots for freeform composition. Slots accept text, frames, multiple layers,
and images, and let the recipient resize and rearrange freely. Use preferred
instances as guardrails. Do not expect component properties to bind to layers
inside a slot; that boundary preserves structural integrity.

Decision rule:

- variants for state
- instance swap for guarded single replacement
- slots for freeform composition

Layout primitives such as `Stack`, `Row`, and `Spacer` can be components when
they help designers compose layouts through the system instead of ad-hoc Auto
Layout. Expose direction or density as controlled properties.

### Component naming and descriptions

- Component names use Title Case: `Button`, not `btn`.
- Slash hierarchy creates asset-panel folders: `Button/Primary/Large`.
- Property names use Title Case nouns: `Size`, `Type`, `Hierarchy`, `State`.
- Values may use code-aligned lowercase when mapping one-to-one to code props,
  or Title Case when optimized for designers. Pick one convention and enforce
  it.
- Boolean property names should be positive: `Show icon`, not `Hide icon`.
- Internal atomic components that should not be published directly can be
  prefixed with `_` or `.`.
- Component descriptions appear in asset-panel hover, Dev Mode inspect, and
  instance properties. Treat them as searchable alias fields and include the
  human name plus code identifier where useful.

### Component anti-patterns

- variant explosion
- booleans masquerading as variants, or variants masquerading as booleans
- variants for icons
- mega-components that should be split into subcomponents or slots
- detach-and-modify instead of contributing back to the system
- creating components too early during exploration
- inconsistent names such as `btn-primary`, `Button/Primary`, and
  `primaryButton` in the same system

Prevent detaching by giving designers enough structure: slots, instance swap
properties, and useful subcomponents. Detached instances can be detected through
Design System Analytics on Organization plans or through plugin-based
signature-layer approaches, but prevention is better than cleanup.

## Variables, tokens, and styles

### Three-tier token architecture

Variables are how Figma becomes a token system instead of a collection of magic
values. Use a three-tier model:

1. Hidden `Primitives` collection for raw values, such as `color/blue/500` or
   `space/4`.
2. Published `Semantic` collection for intent, such as `color/bg/surface`,
   `color/text/default`, and `space/inset/md`, with modes for context.
3. Hidden `Component` collection for component-specific overrides, such as
   `button/primary/bg/default`, always aliasing semantics rather than
   primitives.

The payoff:

- re-alias semantics to change a brand
- edit one primitive to change the brand blue
- tune components without polluting the shared semantic vocabulary
- keep component tokens brand-agnostic by referencing semantic intent

Component tokens that reference primitives directly collapse the indirection
that makes theming work.

### Variable capabilities and gaps

- Color variables apply to fills, strokes, gradient stops, shadow colors, and
  as the value inside color styles. A color variable is one value, so it cannot
  itself be a gradient.
- Number variables apply to corner radius, width, height, gap, padding, stroke
  weight, opacity, font size, numeric font weight, line height in px, letter
  spacing, paragraph spacing, and shadow X/Y/blur/spread.
- String variables apply to text content, exact-match font family, font
  style/weight name, and component variant property values used in prototyping.
- Boolean variables apply to layer visibility, component boolean properties,
  and prototype conditionals.

Gaps to respect:

- variable-font axes other than weight cannot bind
- line height and letter spacing accept px, not percent
- image fills cannot be variables
- effect styles are not wholesale variables
- multi-stop gradients remain styles even when stops are variable-bound
- variables cannot store formulas in native Figma variable definitions

### Modes

Use modes when the same variable has different context values:

- light/dark
- density such as comfortable/compact
- brand
- locale through string variables
- device or breakpoint
- high contrast or reduced motion
- subscription tier, validation state, seasonal theming, and other contextual
  product states

Mode values inherit down the frame tree unless overridden. A single canvas can
therefore show Light, Dark, and Brand B frames using the same components.

Mode limits captured here: after the October 28, 2025 mode-limit increase, Pro
supports 10 modes per collection, Organization supports 20, and Enterprise
supports 40. Treat changing plan limits as release-sensitive if a user asks for
current account-specific limits.

### Scoping and publishing visibility

Scope variables aggressively. A border-radius variable should not appear when a
designer is binding font size or X-offset.

Useful scopes include:

- colors: `ALL_FILLS`, `FRAME_FILL`, `SHAPE_FILL`, `TEXT_FILL`,
  `STROKE_COLOR`, `EFFECT_COLOR`
- numbers: `TEXT_CONTENT`, `CORNER_RADIUS`, `WIDTH_HEIGHT`, `GAP`, `OPACITY`,
  `FONT_WEIGHT`, `FONT_SIZE`, `LINE_HEIGHT`, `LETTER_SPACING`,
  `PARAGRAPH_SPACING`, `PARAGRAPH_INDENT`

Hide internals from publishing. Prefix a collection with `_` or `.`, or hide
individual variables from publishing, so consumers see semantic and component
tokens rather than raw primitives.

### Aliasing

Aliases create the token chain. Variable values can reference other variables
with curly braces, such as `{color/blue/500}`. Aliases survive mode switches by
resolving through the referenced collection's current mode.

Cross-collection aliasing is essential for multi-brand systems. Each brand's
semantic collection can alias shared primitives while resolving key intents,
such as `color/action/primary`, differently.

### Token naming

Use slash naming in Figma variables because forward slashes create hierarchy in
the Variables modal. Avoid flat or kebab-only names that collapse navigation.

A robust token name layers ideas like:

`[namespace] / [object] / category / concept / property / variant / state / scale / mode`

Major systems express this differently, but all preserve tiering and consistent
anatomy:

- reference/system/component classes
- descriptive layered tokens
- base/functional/component tiers
- global/alias/component-specific tiers
- paired foreground tokens for surfaces, such as a primary surface and its
  on-primary text

Token naming anti-patterns:

- flat names such as `bg-primary` or `text-color`
- color-named semantics such as `color-text-red` instead of `color/text/error`
- component tokens aliasing primitives directly
- sequential numeric suffixes that leave no room to insert values later
- inconsistent state position across token names
- page-specific tokens such as `card-customer-page-bg` in a shared system

Use 100-step scales when intermediate values may be needed later.

### DTCG, Extended Collections, and computed values

The W3C Design Tokens Format reached a first stable spec on October 28, 2025.
Its JSON shape uses `$value`, `$type`, and `$description`, curly-brace aliases,
and standard token types such as `color`, `dimension`, `transition`, and
`gradient`. Figma APIs align conceptually, but import/export commonly still
goes through plugins such as Tokens Studio.

For multi-brand work on Enterprise, Extended Collections are the preferred
inheritance model where available: a parent collection holds canonical
structure and default values, while child collections override only differences.
This replaces many older duplicate-library or swap-library patterns. Before
Extended Collections, common multi-brand approaches were mode-based theming in
one semantic collection or separate published libraries per brand.

Conditional logic and expressions live in prototyping, not variable
definitions. The `Set variable` value field and `Conditional` if field support
arithmetic, comparison, logical operators, parentheses, and string
concatenation. Native variables themselves do not store formulas. Plugin-layer
systems may compute values before publishing; treat native computed variables
as release-sensitive unless confirmed current.

### Styles still matter

Color styles are mostly superseded by color variables, except for
compatibility, layered fills, and multi-fill compositions.

Styles remain uniquely useful when one decision bundles multiple values:

- Text styles package family, weight, size, line height, letter spacing, and
  paragraph spacing. Individual properties can be variable-bound inside the
  style.
- Effect styles package shadows. X/Y/blur/spread can bind to number variables
  and shadow color can bind to a color variable, but the effect stack is still a
  style.
- Gradient styles remain required for multi-stop gradients, even when stops are
  variable-bound.
- Image fills can only be styles.

Migration path from color styles to variables:

1. Audit existing color styles in Selection Colors view.
2. Build hidden primitives from raw values.
3. Build semantic variables with modes.
4. Edit each existing color style to bind its fill to the semantic variable,
   preserving instance bindings.
5. Deprecate the old style.

Use design-linting tools where available to locate hard-coded values and suggest
token replacements.

## Library architecture and operations

### System of systems

Large systems should usually be a system of systems, not one giant library:

- core libraries owned by the design-system team
- shared or contributor libraries owned by extension teams
- local or staging libraries owned by product teams

Common mature split:

- Foundations/Tokens
- Icons
- Core Components
- Patterns
- platform-specific libraries such as Mobile, Web, or Desktop
- Brand or Illustration libraries

Split when there is a real reason: file performance, memory limits, divergent
ownership, different publishing cadence, or a different audience. Fewer larger
libraries plus branching can be valid when split-library overhead is worse than
performance or ownership pressure.

### Dependencies, deprecation, and curation

Dependency direction should be acyclic in practice:

- Components may depend on Tokens.
- Patterns may depend on Components.
- Components should not depend on Patterns.

Do not rename or remove tokens used downstream without a migration path. Prefer
additive deprecation: prefix with `[Deprecated]`, add a replacement note, and
remove only after consumers migrate.

Curate published libraries aggressively. Org and Enterprise scoping should make
only relevant libraries available to each team, or the library dialog becomes
noise.

### Publishing

- Bundle changes thematically.
- Always fill in the publish description. The auto-generated diff is not enough
  because later acceptors may only see your description.
- Maintain a release-notes page inside the library file with semantic versions.
- Use staged publishing on Org/Enterprise: publish to the design-system team,
  validate in test files, then publish broadly.
- Do not publish at end-of-day Friday.

### Branching and versioning

Use branching for system updates, large refactors across components, and
exploratory sandboxes. Do not use it for one-off tweaks or ordinary daily
product design.

Good branch discipline:

- one branch per meaningful component change
- branch names tied to the issue or change when possible
- pull from main daily
- keep branches short-lived
- update existing components instead of deleting and recreating, which loses
  instance links
- require review before merge
- write a meaningful merge description because it becomes version history
- coordinate on conflicting branches because Figma merge is binary

Use named versions as semantic anchors: `v2.4.0`, `v2.5.0-beta`, and similar.
Map semantic versioning naturally:

- MAJOR for breaking renames or removals
- MINOR for additive components or variants
- PATCH for visual tweaks

Avoid file-name versioning such as `Components v3` unless intentionally forking
a generation. Use version history and named versions instead.

## File structure and naming

### Pages

A library file should read itself at a glance. A strong structure is:

- Cover first, because it controls the thumbnail
- Getting Started or About
- Release Notes
- Foundations or Tokens for visual reference
- Icons, or a separate icon library if large
- Components, organized by category or component family
- Patterns for composed reference layouts
- Sandbox for work in progress
- Archive for deprecated work
- spacer pages such as `---` between phases

Hidden internal pages are prefixed with `_` or `.`.

Cover thumbnails at 1920x1080 should show file name, owner, status, version,
and last update. Use a status indicator color system on the cover and Dev Mode
statuses on sections. Avoid status emoji in page names because page-name churn
can create unnecessary unpublished-change noise.

### Sections, frames, and groups

- Frames are the workhorse for UI canvases, components, cards, anything with
  Auto Layout, constraints, prototyping, clipping, fills, or exports.
- Sections are top-level canvas organization for grouping multiple frames into
  feature flows or contributions. They are the standard Ready for Dev unit.
- Sections cannot live inside frames or components.
- Groups should almost never appear in UI work. Use them only for narrow vector
  art cases where bounds should auto-fit.
- Convert groups created by imports or pasted external material into frames
  immediately.

### Layer naming

Auto-generated names such as `Frame 1234`, `Rectangle 47`, and `Group 12` are a
real structural defect.

Layer names affect:

- Dev Mode element labels
- Code Connect component and property mapping
- Smart Animate matching
- asset-panel search
- Buzz edit-content fields for non-designers
- exported filenames
- MCP context for coding agents

Smart Animate matches child layers by case-sensitive name, hierarchy position,
and layer type. Bad naming can silently break animations.

Use bulk rename when needed, but review AI rename output before handoff.

### Cleanup after external paste

After pasting from external sources:

1. Run Clean Document or equivalent cleanup.
2. Delete hidden layers.
3. Ungroup single-layer groups.
4. Pixel-align.
5. Convert groups to frames.
6. Apply Auto Layout where structure repeats.
7. Replace raw colors with variables.
8. Replace raw text formatting with text styles.
9. Rename meaningful layers.

Flatten decorative finalized vectors for performance. Never flatten functional
UI because it destroys Auto Layout and prototyping links.

## Prototyping

Variables in prototypes can replace many frame-per-state prototypes.

Use `Set variable` actions to change string, number, boolean, or color
variables. Bind variables to text content, dimensions, layer visibility, fills,
strokes, and opacity. This can collapse a login form or validation flow into a
single state-driven frame.

Conditionals evaluate boolean expressions and execute if/else branches. Order
matters because actions run top to bottom. Expressions support arithmetic,
comparison, logical operators, parentheses, and string concatenation.

Limitations:

- no arrays
- no functions
- no loops
- no clean dynamic math without intermediate variables

For mutually exclusive selection such as radio buttons or active navigation,
use a single string variable holding the active item ID instead of many
booleans.

Variable modes in prototypes let `Set variable` target a specific mode value,
which supports dynamic light/dark toggles in one frame.

Smart Animate discipline:

- children must match by case-sensitive layer name
- hierarchy depth must match
- layer type must match
- top-level frame names do not need to match
- implicitly named text layers also need matching text styles
- within a section, matches are sought inside that section
- duplicate frames with Cmd+D when possible to preserve naming

## Dev Mode and Code Connect

Dev Mode prep is file craft, not handoff theater.

- Wrap every shippable unit in a section named after the feature.
- Mark Ready for Dev only when content is locked.
- Keep WIP and exploration on separate pages.
- Remember that unsectioned content is collapsed by default in Dev Mode.
- Use Completed status where the plan supports it.
- Treat yellow drift alerts after edits as real handoff risk.

Use annotations for non-visual requirements:

- accessibility labels
- focus order
- keyboard shortcuts
- interaction behavior
- debounce or polling rules
- conditional logic
- internationalization
- analytics events
- API field mapping

Do not annotate things Dev Mode already shows, such as padding, color, and
font. Put discussion in comments, not annotations. Put long-form docs behind
Dev Resources on the component. Use the property chip to bind annotations to
specific layer properties so they update with design changes. Remember that
annotations may require Full or Dev seats to view.

Code Connect file-side rules:

- Each Figma component should map cleanly to one code component where possible.
- If code splits variants into separate components, use variant restrictions in
  `figma.connect()` to map each Figma variant to the right code component.
- Align Figma property names with code prop names, such as `disabled` to
  `disabled`.
- Use variants for code enums.
- Use booleans for code booleans such as `disabled` or `loading`.
- Use instance swap or slots for JSX children or slottable content.
- Use component-level MCP instructions to inject accessibility rules and prop
  patterns into AI-agent context when available.

## AI, publishing, and downstream products

### Figma Make

Figma Make generates better React/HTML/CSS when the source frame is structurally
honest.

- Auto Layout lets Make infer flex/grid containers, gap, and padding.
- Free-positioned UI becomes absolute-positioned div clutter.
- Real components and instances help Make identify reusable React components.
- Variables become tokens.
- Layer names become code context.
- Make kits are the quality lever: they connect real production components,
  imported variables/styles, and imperative Markdown guidance.
- Without a Make kit, treat output as exploration rather than production code.

### Figma Sites

Sites requires responsive structure.

- Auto Layout is mandatory for responsive behavior.
- A page starts with a Desktop primary breakpoint.
- Edits cascade to Tablet, Mobile, or custom secondary breakpoints and can be
  overridden per breakpoint.
- Responsive components can use variant values that match breakpoint names so
  Sites swaps them automatically.
- Hover interactions do not work on touch; use press/mobile alternatives.
- Set `nav`, `main`, and `footer` accessibility landmarks on top-level frames
  because they affect published HTML and SEO.
- Group/frame mixing and fixed-width top-level sections produce unpredictable
  responsive behavior.

### Figma Buzz

Buzz templates need structure for non-designers.

- Use Auto Layout on every layer so long headlines and swapped images do not
  break alignment.
- Locked layers are omitted from the end-user Edit content panel when users
  start from a published template.
- Name every editable layer semantically because those names become field
  labels.
- Component sets become Template Sets.
- Boolean props become toggle switches.
- Instance swaps become dropdowns.
- Text properties become Edit content fields.
- Variable modes drive multi-theme and multi-locale templates.
- CSV/XLSX bulk create maps columns to layer names, so naming clarity affects
  data mapping.

### Figma Slides

Treat Slides files like design files. Components, styles, and variables carry
over. Variable modes apply per slide. Polls, stamps, Likert scales, and
embedded prototypes are first-class live interactions. Use components, styles,
and variables for templated layouts instead of pasting raw images for every
slide.

### Figma Design AI

- First Draft output is wireframe quality. Apply the real design system after
  generation.
- Make Image output is placeholder material unless licensing and brand usage
  have been cleared.
- Rename Layers is useful only after the design is structurally final and must
  be reviewed because it can break Smart Animate.
- Smart Duplicate is good for content variation, but generated content should
  be replaced before handoff.
- Visual Search helps find icons by appearance rather than exact naming.
- Do not accept AI output unchanged.

### MCP and IDE agents

MCP-fed coding agents read variables, components, layer hierarchy, and names.
The same disciplines that help designers and developers also help models:

- variables
- Auto Layout
- real components and instances
- semantic naming
- Code Connect mappings
- custom component instructions where supported

Sloppy files now damage multiple consumers at once: Dev Mode, Code Connect,
Make, Sites, Buzz, Slides, and MCP.

When an agent is using Figma through MCP, plugin API scripts, upload tools, or
screenshot repair flows, also read `figma-mcp-agent-gotchas.md`. Tool success
does not prove file success; the agent must verify actual node state, image
fills, bounds, component properties, and target screenshots.

Figma exports and MCP asset URLs are reference surfaces unless intentionally
promoted into a product-owned asset pipeline. Map exported values to the
receiving code tokens, assets, or component APIs instead of treating generated
code or short-lived URLs as runtime truth.

## Review checklist

Use this as a recognition test, not as a rote keyword list.

Layout:

- Are UI frames in Auto Layout by default?
- Are Hug, Fill, and Fixed used according to content behavior?
- Are min/max and wrap used where content changes or grids reflow?
- Is Grid Auto Layout used only for real two-dimensional structures?
- Are constraints used only where they own behavior?
- Are groups absent from UI structures?

Components:

- Do components exist only after reuse and maintenance need are real?
- Are variants limited to true enumerated state?
- Are booleans, instance swaps, text properties, nested instance properties,
  and slots used for their proper jobs?
- Are icon libraries built as separate components, not variants?
- Are names, properties, values, and descriptions discoverable and code-aligned
  where needed?
- Are detach-and-modify patterns prevented by better composition?

Variables and styles:

- Does the file use hidden primitives, published semantics, and hidden
  component tokens?
- Do component tokens alias semantics instead of primitives?
- Are variables scoped and hidden from publishing where appropriate?
- Are modes used for real context changes?
- Are names hierarchical and semantic rather than flat, color-bound, or
  page-specific?
- Are text/effect/gradient/image styles retained only where styles still own
  bundled decisions?

Library operations:

- Is the library split justified by ownership, performance, cadence, or
  audience?
- Are dependency directions safe?
- Are breaking changes handled through additive deprecation?
- Are publishes thematic and described?
- Are branches short-lived and reviewed?
- Are versions named in history instead of encoded in file names?

File structure:

- Is the cover first and informative?
- Do pages communicate purpose?
- Are shippable units wrapped in sections?
- Are layers semantically named?
- Has imported material been cleaned, converted, tokenized, and renamed?

Downstream readiness:

- Is Dev Mode scoped to ready sections?
- Are annotations reserved for non-visual requirements?
- Do component properties map to code props where Code Connect matters?
- Will Make, Sites, Buzz, Slides, and MCP see structure rather than a painting?
- If MCP/API tools touched the file, did the agent verify returned node IDs,
  loaded page context, font-loaded text edits, image fills, component property
  placement, bounds/overlap, and screenshots of the actual target artifact?
- If Figma exports informed implementation, are exported code and MCP asset URLs
  kept reference-only unless moved through the product's normal asset pipeline?

## Never do catalog

- manual eyeballed gaps
- fixed widths where Fill belongs
- fixed-size text boxes that overlap when content grows
- spacer-frame clutter when variables on gap/padding would do
- deeply nested unnecessary Auto Layout frames
- sticky elements as normal Auto Layout children
- inconsistent group/frame mixing
- variants for icons
- variant explosion
- booleans masquerading as variants, or variants masquerading as booleans
- mega-components that should be decomposed
- detach-and-modify as a normal workflow
- hardcoded hexes and magic-number spacing
- flat or kebab-only variable names that destroy hierarchy
- color-named semantic tokens
- component tokens referencing primitives directly
- auto-generated layer names
- stray groups from external pastes
- hidden layers left invisible instead of deleted
- single-layer groups
- file-name versioning instead of named versions
- publishing without a real change description
- long-running branches
- status emoji in page names
- pasted raw images for every slide
- fixed-width top-level Sites sections
- accepting AI-generated output without reviewing structure, names, and tokens
- treating MCP/API success, metadata, or upload hashes as proof without reading
  back node state and checking screenshots
- importing Figma export code or short-lived MCP asset URLs into runtime code
