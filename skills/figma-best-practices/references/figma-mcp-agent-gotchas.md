# Figma MCP Agent Gotchas

Use this reference when an agent is inspecting, creating, repairing, exporting,
or uploading Figma artifacts through MCP, plugin API scripts, or another
tool-mediated Figma runtime.

This file does not replace `figma-file-craft.md`. It covers the operational
failure modes that make otherwise sound Figma file-craft work appear complete
when the file is actually broken, blank, overlapped, unbound, or unusable by
Dev Mode and model consumers.

## Ground Truth

Successful tool output is not the same as successful Figma state. Treat every
write, upload, import, and export as provisional until the target artifact is
read back and visually checked.

Strong proof usually combines:

- returned node IDs for created or changed objects
- structure reads from the actual target page or node
- variable, style, component, property, fill, and bounds reads where relevant
- screenshots of the real frame, component set, or documentation board
- source-of-truth checks against code, tokens, assets, or a product decision

If a parity task depends on exact Figma values, cite the frame or node IDs and
measure them. If MCP quota or file access prevents measurement, stop the exact
parity claim instead of inventing values.

## Before Writing

Inspect before changing the file:

- pages and top-level page bounds
- the target node type; Figma URLs can point at a page, frame, component, or
  ordinary layer
- existing local components, component sets, variables, styles, sections, and
  published library references
- nearby top-level section bounds so new work does not overlap existing work
- the production source of truth when the Figma artifact maps to shipped code

Screenshots and exported Figma code are evidence, not automatically the source
of truth for reusable system artifacts. Use code, tokens, and app-owned assets
for exact implementation values when the task is building a durable library or
handoff surface.

When a file has both generated local components and imported or published
library components, label the generated work as evidence or repair work unless
inspection proves it is the canonical source.

## Script Runtime Rules

Prefer small scripts that inspect, create, or repair one coherent artifact and
return structured data. Return created node IDs, mutated node IDs, counts,
artifact names, and verification facts. Do not rely on console logs.

Start each script by finding and loading the intended page:

```js
const page = figma.root.children.find((node) => node.name === "Components");
await figma.setCurrentPageAsync(page);
```

Page context can reset between calls. Do not assume the currently visible page
is still the page your next script will mutate.

Use top-level `await` and `return` when the runtime supports it. Avoid wrapping
the whole script in an async IIFE unless the tool explicitly requires that
shape.

Failed plugin scripts are often atomic in MCP runtimes. If a script errors,
read the error, repair the cause, and retry from the intended start state
rather than assuming a partial canvas mutation landed.

Unsupported API calls should be treated as runtime facts, not mysteries to
work around blindly. Common examples in restricted MCP runtimes include
notification APIs, private plugin data APIs, and text inspection APIs that are
available in some contexts but not others. Use returned node IDs, shared plugin
data where supported, explicit page traversal, and concrete font reads instead.

## Node API Traps

Not every property exists on every node type. Page nodes do not behave like
frames, and variant children do not expose the same APIs as standalone
components or component sets. Guard optional reads by property existence or
node type.

Set parent-dependent properties only after the node is inside the right parent:

- Append text into the component before assigning component property
  references.
- Append children to an Auto Layout parent before setting absolute positioning
  that depends on that parent.
- Set fill or sizing values after the node is in the structure when the runtime
  rejects unattached edits.

Use component property definitions from a component set or non-variant
component. Do not read them from variant children as if they were standalone
component definitions.

Name-based audits can lie because instances can share component names. Filter
by both name and node type, and prefer stable parent context when layer names
can repeat.

Figma color channels are `0..1` floats, not `0..255` integers. Fills and
strokes are effectively replace-by-value in many plugin operations, so clone
and reassign arrays instead of mutating them in place.

## Fonts And Text

Load fonts before creating or changing text, text styles, text wrapping,
characters, or auto-resize settings. Treat layout edits on text as font-touching
operations.

Font family and style names are runtime-specific:

- Flutter or CSS names may not exist in Figma.
- Figma style names can differ by family, such as spaced `Semi Bold` versus
  unspaced `SemiBold`.
- A product font declared in app assets may still be unavailable in the Figma
  file.

When a font is unavailable, document the substitute in the Figma artifact and
avoid making that substitute look like production truth.

For notes and documentation frames, make text fill the available width and use
height auto-resize. A structurally rich board can still be useless if evidence
notes render as clipped one-line text.

## Components And Variants

After creating a component set or calling `combineAsVariants`, inspect and lay
out the variant children. Variants can overlap even when the component set was
created successfully.

Resize component sets from actual child bounds. Wide sets, imported examples,
and generated documentation cards can overflow or overlap the section even when
each child component looks correct in isolation.

Keep icons as standalone components, not icon variants. When SVG imports create
wrapper frames, flatten finalized wrappers where appropriate, clear fills on
non-vector containers, and bind color only to vector-like nodes. A root fill on
an icon instance can render as a square even when vector children are correct.

For instance-swap repairs, do not rely only on a slot layer name. After a swap,
the layer may display the swapped component name. Find the slot by parent
structure, position, or the swapped main component.

Use screenshots as part of component verification. Metadata can look green
while the rendered component shows square icons, clipped labels, blank fills,
or stacked variants.

## Images, Uploads, And Screenshots

Treat asset upload as a transport step. An upload can return HTTP success and
an image hash while the target rectangle still has its old fill or a solid
placeholder. Read the target node's `fills` after upload.

When readback does not show the intended image fill, bind the returned hash
explicitly:

```js
const image = figma.createImage(imageHash);
slot.fills = [{ type: "IMAGE", scaleMode: "FIT", imageHash: image.hash }];
```

Use `scaleMode: "FIT"` for visual reference slots unless the intended crop is
part of the artifact. Verify that every expected slot has an image fill and the
expected scale mode.

Large screenshot boards can exceed upload or renderer comfort even when they
are technically valid images. Batch uploads, slice large boards, or convert
risky 16-bit PNGs into 8-bit PNG32 copies when a client or MCP renderer shows
blank output.

Re-uploading the same bytes is a useful diagnostic. If Figma returns the same
image hash, the node may already point at the intended asset and the problem is
more likely render compatibility, stale client cache, or a missing explicit
fill binding.

Do not treat `get_metadata` as visual proof. It reports names, structure, and
geometry, not whether an image hash renders. Pair metadata with screenshot and
fill inspection.

A screenshot of a Section is not proof that separately appended frames live
inside that section. Capture the actual component set, frame, or documentation
board that must be readable.

## Layout And Page Organization

Create the page or wrapper frame first, then append sections and cards inside
it. New top-level nodes often begin at `(0, 0)`, so a valid component family can
still be sitting on top of another section.

Audit direct child bounds after major writes:

- no top-level section overlap
- no component set overflow outside its section
- no documentation-card collision
- no horizontal row fixed-height clipping after text expands
- no blank section screenshots caused by frames living beside, not inside, the
  section

For large visual inventories, use manifest-backed contact sheets instead of
placing hundreds or thousands of individual image nodes. The manifest proves
exact paths and source files; the Figma page provides a reviewable visual
surface.

## Source Truth And Handoff

Figma exports and MCP asset URLs are reference artifacts unless explicitly
promoted into the product asset pipeline. Never put short-lived MCP asset URLs
or generated reference code into runtime code.

Map Figma values into app-owned tokens, generated assets, and component APIs.
When exact parity depends on an exported layer, record the Figma node, the
measured value, and the app owner path that should receive the implementation.

Visible exports beat hidden or clipped layer guesses. If a hidden text layer,
off-canvas label, or mock-only helper conflicts with the visible frame, do not
render it as product UI without an explicit product decision.

Product intent can override the current mock, but the override must be recorded
near the handoff or parity plan. Otherwise future audits will keep repairing
the implementation back to the stale mock.

## Completion Checks

Before calling MCP-mediated Figma work done, verify the relevant checks:

- The intended page or frame was inspected after the write.
- Created or changed nodes are returned and still exist.
- Component sets have expected variants and no stacked children.
- Text uses loaded fonts and does not clip.
- Variables are scoped and bound to supported fields.
- Uploaded image slots have real image fills and expected scale modes.
- Screenshots of target artifacts are nonblank and readable.
- Top-level sections and wide component sets do not overlap or overflow.
- Component descriptions or documentation notes name the source code, token, or
  asset truth when the artifact maps to production.
- Reference exports remain out of runtime code unless they have been promoted
  through the product's normal asset pipeline.
