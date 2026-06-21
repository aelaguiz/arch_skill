# Review Catalog

Use this catalog to decide what to look for once the target is mapped. It is
review doctrine, not a rule system. Apply judgment and cite real evidence.

For every pattern:

- name the concept the change touches
- identify the canonical owner, or say there is no clear owner yet
- search for old and alternate paths that can still express the same concept
- read representative callers, readers, writers, tests, docs, prompts, schemas,
  generated artifacts, config, and examples when they matter
- decide whether the change converges the system or leaves two ways to be right
- flag only changed-code or changed-scope risks with concrete evidence

## Split-Brain Or Bifurcated Abstraction

Flag when the system has two live ways to express, mutate, validate, render,
serialize, route, prompt, or configure the same concept.

Common signs:

- old service and new service both callable
- old command path and new command path both registered
- two schemas describe the same contract
- one feature reads from the central store while another reads a local copy
- docs or examples teach an old path that still works
- direct mutation bypasses the intended owner
- two generated artifacts can drift

Read:

- new owner and old owner
- public entrypoints that reach either owner
- representative internal callers
- tests and fixtures that instantiate either model
- docs, examples, prompts, schemas, and generated artifacts that name either
  model

Block when both paths remain live and can affect real behavior, callers can
choose between models, the bridge is implicit, or docs/tests still make the old
path look supported.

Do not block when the old path is unreachable, the two paths intentionally
serve different products or versions, or there is a short explicit migration
shim with no new callers and a deletion point.

Example:

```markdown
### [BLOCKING] New session writer bypasses the canonical save service

- File: src/editor/ToolbarSaveButton.tsx
- Symbol / line: `handleSave`
- Risk: The button now calls `writeSessionDraft` directly while the rest of the
  editor saves through `EditorSessionService.save`. That creates two live save
  paths with different validation and retry behavior.
- Evidence: `ToolbarSaveButton.tsx` calls `writeSessionDraft`; existing callers
  in `src/editor/session/` use `EditorSessionService.save`.
- Repair target: Route toolbar save through the canonical session service or
  move the new validation into that owner and migrate callers.
- Review pattern: split-brain abstraction
```

## Missed Centralized Owner

Flag when local code repeats behavior that belongs in an existing service,
schema, helper, adapter, prompt reference, config owner, or domain model.

Common signs:

- caller repeats validation instead of using the owner
- one package knows internals of another package
- UI reaches around state/session/persistence owner
- script reimplements runtime behavior
- tests encode production rules instead of calling canonical behavior
- skill or prompt copies policy that should live in a shared reference

Read:

- existing owner that appears to own the concept
- new local copies of validation, normalization, parsing, routing, or policy
- callers that can now choose between central and local behavior
- tests that may have copied the rule instead of exercising the owner

Block when local code repeats a rule with one obvious owner, callers must know
an ordering convention, the helper exists because the owner was inconvenient, or
tests can pass while production behavior diverges from the owner.

Do not block when the local rule is truly presentation-only, ordinary adapter
glue, or the supposed central owner does not own the changed concept after
reading the code.

Example:

```markdown
### [BLOCKING] Form validation duplicates the account schema

- File: src/account/AccountForm.tsx
- Symbol / line: `validateLocalAccount`
- Risk: The form reimplements account-name validation instead of using
  `accountSchema`. The API and UI can now disagree on valid names.
- Evidence: `validateLocalAccount` checks length and character rules locally;
  `src/account/accountSchema.ts` already owns the same contract.
- Repair target: Route form validation through the canonical schema or extract
  the shared rule into the schema owner.
- Review pattern: missed centralized owner
```

## Partial Migration

Flag when one route, caller, feature, command, or artifact moved to the new
model while adjacent same-contract paths still use the old model.

Common signs:

- one UI action uses the new service while a sibling action still calls the old
  writer
- one route accepts the new schema while a sibling route accepts the old shape
- one generated file is updated but another generated consumer is stale
- one command family moved to a new registry but aliases still point at the old
  registry
- feature flag keeps both paths selectable after migration is claimed

Read adjacent routes, commands, jobs, components, prompts, scripts, API methods,
old aliases, compatibility flags, fallback readers, direct mutation paths, docs,
examples, and migration notes when present.

Block when user-visible behavior can still enter through the old path, both
data shapes remain accepted without one adapter boundary, or branch/plan intent
promised migration, centralization, or deletion that did not happen.

Do not block when scope explicitly migrates only one isolated caller and leaves
a named follow-up with no shared invariant broken, or compatibility normalizes
immediately through one adapter.

Example:

```markdown
### [BLOCKING] CLI migrated to the new config loader but scheduled jobs did not

- File: src/jobs/nightlyImport.ts
- Symbol / line: `loadImportConfig`
- Risk: The CLI now uses `ConfigService`, but nightly jobs still read env vars
  directly. The same import can run with different defaults by entrypoint.
- Evidence: `src/cli/import.ts` calls `ConfigService.loadImportConfig`;
  `nightlyImport.ts` still reads `process.env.IMPORT_BATCH_SIZE`.
- Repair target: Move the job to `ConfigService.loadImportConfig` or add a
  single adapter that both entrypoints use.
- Review pattern: partial migration
```

## Name-Only Completion Or False Simplification

Flag when a change looks complete at the naming, convention, wrapper, checklist,
or phase-label level, but the old behavior or complexity remains live
underneath.

Common signs:

- a new "canonical" owner exists but callers still use the old owner
- a wrapper or facade has the right name but forwards to old behavior unchanged
- a "unified" path covers only one happy path while siblings stay split
- a simplification adds a layer without deleting an older concept
- a plan or completion note says migrated/deleted/centralized, but code still
  exposes the old route, command, prompt, fixture, config, or generated artifact
- tests assert the new label or wrapper instead of the intended outcome

Read the actual control flow, data flow, callers, old entrypoints, side doors,
tests, docs, prompts, examples, and generated artifacts. Treat names and phase
status as claims to verify against runtime behavior, not proof.

Block when apparent completion can coexist with the old behavior, two truths,
side doors, or extra complexity the change was supposed to remove.

Do not block when the old path is unreachable, the wrapper now owns a real
invariant, or the plan explicitly scoped a temporary bridge with a deletion
point.

Example:

```markdown
### [BLOCKING] `UnifiedImportService` leaves the old import path live

- File: src/import/UnifiedImportService.ts
- Symbol / line: `runImport`
- Risk: The new service gives the migration a unified name, but scheduled jobs
  still call `legacyImport`. The same import behavior now has two live owners.
- Evidence: `UnifiedImportService.runImport` handles the CLI path;
  `src/jobs/nightlyImport.ts` still calls `legacyImport` directly.
- Repair target: Route the job through the unified service or delete the old
  path if it is no longer supported.
- Review pattern: name-only completion
```

## Wrong-Layer Logic

Flag feature-specific logic in shared layers, transport details in domain
logic, persistence details in UI, product judgment in low-level utilities, or
agent workflow policy hidden in scripts.

Common signs:

- shared helper knows a specific feature name
- UI component directly writes persistence state
- domain model knows HTTP or GraphQL response details
- script decides product, workflow, or agent-review policy instead of narrow
  mechanics
- prompt or skill hardcodes repo-local workflow policy that belongs elsewhere

Read package boundaries, new imports, nearby ownership names, existing adapters,
service boundaries, and tests that now need internal knowledge.

Block when dependency direction is wrong, callers must understand internal
lifecycle details, future features are likely to copy the wrong layer, or a
script/generated artifact now owns reasoning that should stay in code or agent
judgment.

Do not block when the code is a true adapter and immediately normalizes the
shape across layers.

Example:

```markdown
### [BLOCKING] Shared renderer imports lesson-specific QA types

- File: src/ui/playable_surface/renderSurface.ts
- Symbol / line: `renderSurfaceControls`
- Risk: The shared renderer imports lesson QA command types, which leaks
  feature-specific QA behavior into the shared rendering layer.
- Evidence: `renderSurface.ts` imports `LessonQaCommand`; nearby shared surface
  files depend only on surface interfaces.
- Repair target: Move lesson command mapping behind a lesson-owned adapter or
  pass only the shared command interface into the renderer.
- Review pattern: wrong-layer logic
```

## Thin Or Fake Abstraction

Flag wrappers and helpers that add a live concept without removing real
complexity, naming a real domain concept, hiding a dangerous boundary, reducing
caller burden, or making invalid use harder.

Common signs:

- manager/facade only forwards arguments unchanged
- helper exists for one call site and has no domain name
- abstraction accepts a bag of flags instead of owning a state model
- wrapper makes tests mock the wrapper instead of behavior
- new layer has the same method names as the wrapped layer
- "future flexibility" is the only reason it exists

Read call sites before and after, repeated logic the abstraction claims to
remove, invariants it claims to own, and tests that now mock it.

Block when the abstraction removes no meaningful complexity, hides a dangerous
boundary, creates a second API, or weakens behavior proof.

Do not block when the wrapper names a real domain concept, hides a risky
boundary, reduces caller burden, or is needed to split a large file into a clear
owned unit.

Example:

```markdown
### [BLOCKING] `CommandExecutionFacade` is a second command API

- File: src/commands/CommandExecutionFacade.ts
- Symbol / line: `execute`
- Risk: The facade forwards to `CommandService.execute` with the same
  arguments. It gives callers two equivalent APIs and no new invariant.
- Evidence: New callers import the facade while existing callers use
  `CommandService`.
- Repair target: Delete the facade or move a real invariant into the canonical
  command service.
- Review pattern: thin abstraction
```

## Drift-Prone Proof

Flag tests and proof that pass while the real behavior can still be wrong.

Common signs:

- test repeats the same conditional as production code
- test asserts a helper was called but not the behavior that matters
- integration behavior is tested only through mocked adapters
- deletion is tested by grep or absence without proving old behavior is
  unreachable
- fixture builds impossible states production cannot produce
- snapshot blesses a stale contract without semantic assertion

Read changed tests, fixtures, production behavior under test, existing
higher-level tests, and the bug or obligation the proof is supposed to protect.

Block when risky behavior changed without behavior-boundary proof, tests prove
mocks or duplicated rules, fixtures make impossible states look valid, or
claimed deletion leaves old behavior reachable.

Do not block when the change is low-risk and already covered by typecheck,
build, or existing tests, or when a unit test is the correct proof for a truly
isolated shared owner.

Example:

```markdown
### [BLOCKING] Test repeats the permission rule instead of exercising it

- File: tests/admin/deleteUser.test.ts
- Symbol / line: `canDeleteFixture`
- Risk: The test duplicates the admin permission conditional in fixture setup.
  If production permission logic changes, the test can still pass.
- Evidence: `canDeleteFixture` checks role and org status locally; production
  permission lives in `src/auth/permissions.ts`.
- Repair target: Build the test through the production permission API or add an
  integration assertion that reaches it.
- Review pattern: drift-prone proof
```

## Stale Truth Surface

Flag docs, comments, examples, prompt references, generated files, telemetry
names, stable IDs, and install commands that now teach the wrong thing.

Common signs:

- README command uses old CLI, env var, or API
- examples instantiate old APIs
- prompt instructions name archived workflows as live behavior
- generated artifact was not regenerated after schema changes
- telemetry event names still imply old behavior
- comments explain a retired invariant

Read touched docs plus docs/examples/prompts/generated artifacts that mention
changed symbols, commands, routes, schemas, env vars, public APIs, or install
surfaces.

Block when a future developer or agent would copy stale instructions and
reintroduce the old path, generated artifacts contradict runtime code, or public
commands/install behavior changed while live docs teach the old contract.

Do not block historical docs clearly marked historical, internal changes with
no live truth surface, or stale surfaces unrelated to changed behavior.

Example:

```markdown
### [BLOCKING] README still teaches direct writer usage

- File: README.md
- Symbol / line: `Saving drafts`
- Risk: Code migrates draft writes behind `DraftService`, but the README still
  shows callers importing `writeDraft` directly.
- Evidence: README example imports `writeDraft`; changed production code routes
  through `DraftService.save`.
- Repair target: Update the live example to use `DraftService` or remove it.
- Review pattern: stale truth surface
```

## Boundary, Lifecycle, And Error Gap

Flag changed code that crosses a platform, SDK, network, auth, storage,
process, filesystem, UI lifecycle, or other external boundary without carrying
the boundary's failure modes and cleanup obligations.

Common signs:

- network call assumes success or ignores partial failure
- filesystem write is non-atomic where partial state matters
- async work has no cancellation or stale-result guard
- listener, timer, or handle is not cleaned up
- retry hides permanent failure
- error handling logs sensitive data or swallows the only diagnostic

Read boundary wrappers, nearby error conventions, caller expectations on
failure, tests/telemetry/messages for failure paths, and primary docs only when
current platform behavior matters.

Block when reachable failure corrupts state, hides data loss, leaks data,
leaves resources alive, or moves lifecycle cleanup into caller memory.

Do not block when the canonical boundary already owns the failure mode and the
changed code uses it correctly.

Example:

```markdown
### [BLOCKING] Import job can leave half-applied state on API failure

- File: src/jobs/importCustomers.ts
- Symbol / line: `runImport`
- Risk: Customers are saved before the remote cursor update succeeds. If cursor
  update fails, the next run can import the same page again.
- Evidence: `saveCustomers(page.items)` runs before `updateCursor(page.next)`;
  the update error is logged but does not roll back or make the write
  idempotent.
- Repair target: Put customer writes and cursor update behind one transaction
  or make import idempotent through the canonical service.
- Review pattern: boundary lifecycle error
```

## Caller Contract And Invariant Leak

Flag APIs where correct use depends on caller memory instead of type shape,
ownership, routing, or fail-loud enforcement.

Common signs:

- boolean flags select incompatible modes
- nullable fields allow impossible combinations
- caller must call methods in a hidden order
- caller must pass matching arrays, indexes, or IDs by convention
- caller chooses between old and new APIs
- error-prone sequence is repeated across call sites

Read public signatures, changed call sites, representative existing call sites,
type definitions, runtime guards, and tests that prove invalid states fail.

Block when a new impossible state exists, callers can misuse the API without
immediate failure, or an invariant moved from the owner into caller convention.

Do not block when the API is private to one file and all callers are visible
and safe, or a stronger type/parser/schema/runtime guard prevents the state.

Example:

```markdown
### [BLOCKING] Nullable state allows saved-but-unvalidated sessions

- File: src/session/sessionState.ts
- Symbol / line: `SessionState`
- Risk: `validatedAt?: Date` lets callers create a saved session with no
  validation timestamp, while downstream code treats saved sessions as
  validated.
- Evidence: `saveSession` accepts `SessionState`; `renderSessionBadge` checks
  only `state.saved`.
- Repair target: Represent draft, validated, and saved states as distinct
  variants or make `saveSession` own validation.
- Review pattern: invariant leak
```

## Agent, Prompt, Or Skill Surface Regression

Flag instruction-bearing changes that make agents less capable, less truthful,
or more likely to bypass judgment.

Common signs:

- skill prose depends on hidden history instead of runtime context
- script owns workflow judgment rather than narrow mechanics
- prompt replaces reasoning with keyword rules or brittle checklists
- agent-facing doc names archived commands as live behavior
- multiple skills claim the same lane with no peer boundary
- generated skill output and source doctrine can drift
- install docs, runtime metadata, and README disagree

Read changed `SKILL.md`, `AGENTS.md`, `CLAUDE.md`, prompt files, `agents/*.yaml`,
generated outputs, install docs, Makefile targets, and sibling skills with
overlapping descriptions.

Block when a shipped skill depends on archived runtime files, judgment moves
into a runner without deterministic need, trigger metadata overlaps a peer, or
source/generated/install surfaces disagree.

Do not block when a checklist is a judgment aid and the agent still owns
synthesis, or a script performs narrow mechanics with bounded output.

Example:

```markdown
### [BLOCKING] Skill trigger overlaps `plan-audit`

- File: skills/example-review/SKILL.md
- Symbol / line: `description`
- Risk: The description claims both generic branch review and plan-backed
  implementation review, making routing ambiguous with `plan-audit`.
- Evidence: Description says "review any branch or plan implementation";
  `plan-audit` already owns plan-backed implementation review.
- Repair target: Narrow the trigger to the actual lane and add a handoff line.
- Review pattern: agent prompt skill surface
```

## Security And Trust Boundary Regression

Flag only reachable security risks introduced or worsened by the reviewed
change. Do not emit generic security warnings.

Common signs:

- user input reaches command execution, SQL, shell, filesystem paths, HTML,
  templates, deserialization, or network requests
- auth or authorization moves from owner to caller
- logs include secrets, tokens, credentials, PII, or request bodies
- dependency or infrastructure trust changes without pinning or validation
- file upload, archive extraction, or path handling lacks normalization
- tenant, account, org, or workspace boundary assumptions changed

Read the changed trust boundary, validation/escaping/logging/auth owners, paths
from input source to sink, and authoritative external security docs only when
the claim depends on current external behavior.

Block when untrusted input reaches a dangerous sink, authorization becomes
caller memory, sensitive data can leak, or tenant/account/org/workspace
isolation can be bypassed.

Do not block when the value is not attacker-controlled and the reviewer can
cite why, or the canonical boundary validates the value and all changed paths
use that boundary.

Example:

```markdown
### [BLOCKING] Export path trusts user-controlled filenames

- File: src/export/writeExport.ts
- Symbol / line: `writeExport`
- Risk: The export path joins a user-provided filename directly into the output
  path. A crafted filename can write outside the export directory.
- Evidence: `path.join(exportDir, request.filename)` is used without basename
  or normalization checks; `request.filename` comes from the API body.
- Repair target: Normalize and validate filenames at the export boundary, or
  generate server-owned filenames.
- Review pattern: security trust boundary
```
