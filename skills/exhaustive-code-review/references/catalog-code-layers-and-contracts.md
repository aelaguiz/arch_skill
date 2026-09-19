# Catalog Slice: Layers And Contracts

Applies when the change moves logic across a module or package boundary, adds an
import between layers, or changes a signature, a type, or a calling convention.
Needs the diff, the repository at head for the boundaries and the existing
adapters, and the call sites of every changed interface.

Both checks ask where knowledge sits. C-38 asks whether the logic is in the layer
that owns it. C-39 asks whether correct use of a boundary now depends on what the
caller remembers. Report each defect once, under the check whose comparison found
it.

## C-38 Logic placed in the wrong layer

Question: Does this change put feature-specific or lower-level knowledge in a
layer that should not hold it?

Needs: the diff; the module and package boundaries at head; the imports the
change adds; the existing adapters; tests that now reach across a boundary.

Read: Follow the new imports and the direction of the dependency. A shared
helper that now knows one feature's name, an interface component that writes
persistence state directly, a domain model that knows transport or response
details, a low-level utility that makes a product judgment, and a script or
generated artifact that decides workflow or review policy instead of narrow
mechanics are the same defect: knowledge sitting beside or below the owner that
should hold it. Read what sibling files in that directory are allowed to depend
on, and what the layer's existing adapters already normalize. A test that now
needs another layer's internals shows the boundary moved. Ask what the next
feature will copy from this file.

Block when: the dependency direction is wrong, callers must understand another
layer's internal lifecycle, the next feature is likely to copy the misplacement,
or a script or generated artifact now owns reasoning that belongs in code or in
the agent's judgment.

Do not block when: the code is a true adapter and normalizes the shape across
the boundary immediately; the layer genuinely owns the concept once you read it;
the file is private to one feature and no shared layer is affected. Repeating a
rule an existing owner already holds is C-04; an interface that makes callers
remember an ordering or a pairing is C-39. When the misplaced reasoning sits on a
prompt, skill, or agent instruction surface, report it under C-41.

Examples:

- **[REQUIRED REPAIR] The shared renderer imports one feature's command
  types.** The rendering path every surface uses now imports a lesson-specific
  command type, so feature behavior lives in shared code. Compared the new
  import with what sibling files in the shared directory depend on. Repair
  target: map the feature's commands behind a feature-owned adapter and pass
  only the shared interface into the renderer.
- **[OBSERVATION] An import that looks like a leak is adapter glue.** The new
  module imports the transport's response type, converts it to the domain record
  in the same function, and exposes nothing else across the boundary.

## C-39 A caller must remember an invariant the boundary should enforce

Question: Can a caller of this changed interface get it wrong without failing
immediately?

Needs: the diff; the changed signatures and type definitions; the changed call
sites and representative existing ones; the runtime guards; tests that prove
invalid use fails.

Read: Read the new signature as a caller who has not read the implementation.
Ask what combinations the types admit that the code cannot handle: a nullable
field permitting a state downstream code treats as impossible, a boolean that
selects incompatible modes, parallel collections or identifiers matched by
position or convention, a required call order the types do not express, an
error-prone sequence repeated at every call site, or a choice between the old
and the new interface. Then check what misuse does: fail at once, or produce a
wrong result later. Compare the change against the call sites that existed
before — an invariant the owner used to enforce that now lives in a comment, a
naming convention, or the caller's memory has leaked.

Block when: the change creates a state the types permit and the code cannot
handle, callers can misuse the interface without immediate failure, or an
invariant moved out of the owner into caller convention.

Do not block when: the interface is private to one file and every caller is
visible and safe; a type, parser, schema, or runtime guard already makes the
invalid state unreachable; the shape is the surrounding code's existing
convention and this change does not widen it. Whether a new control surface
should exist at all is C-09; a second interface for work an owner already does
is C-02; one field or one state carrying two meanings at once is C-29, and the
two checks meet where an overloaded field is also what a caller has to decode —
report the contract half here and the two meanings there.

Examples:

- **[REQUIRED REPAIR] A nullable timestamp allows a saved but unvalidated
  session.** The state record lets a session be saved with no validation
  timestamp while downstream code treats every saved session as validated.
  Compared what the type admits with what its readers assume. Repair target:
  make draft, validated, and saved distinct variants, or have the save path own
  validation.
- **[REQUIRED REPAIR] Two collections that must line up by position.** The new
  call takes the items in one list and their results in another and pairs them
  by index; filtering one and not the other produces mismatched results with no
  error. Compared the signature with what each call site has to remember. Repair
  target: pass one collection of paired records.
