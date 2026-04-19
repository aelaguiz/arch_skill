# Review Requirements (portable)

The reviewer applies these requirements to every lens and to the final synthesis. They are derived from industry review practice and genericized so the skill is portable across repos, languages, and frameworks. Repo-local conventions (`AGENTS.md`, `CLAUDE.md`, `README.md`, lint/formatter config, nearby idioms) outrank anything here when they disagree.

## Required review lenses

The runner MUST launch one parallel Codex `gpt-5.4-mini` `xhigh` subprocess per required lens. Required lenses:

- `correctness`
- `architecture`
- `proof`
- `docs-drift`
- `security` (risk-triggered; still runs, but emits "no findings for this lens" when the change is outside security surface)
- `agent-linter` (conditional — see below)

The `agent-linter` lens is required only when the target touches agent-building or instruction-bearing surfaces:

- files under `skills/`, `agents/`, `.github/claude/`, `prompts/`
- files named `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `agent.md`, `prompt.md`, or ending in `.prompt.md` / `.skill.md`
- files matching `*agent*`, `*prompt*`, `*skill*` in path or name
- changes to runner scripts that drive agent subprocesses

If `agent-linter` is required and `$agent-linter` is not installed/reachable, the lens MUST emit the coverage-failure shape. The runner MUST NOT silently downgrade coverage.

## Mandatory duplication and drift checks

Flag when the change introduces or worsens:

- A rule, condition, prompt fragment, schema, command string, policy, or runtime contract expressed in multiple places that can drift.
- A parallel path alongside an existing canonical owner path, when the canonical path could have been extended instead.
- A helper that obscures a critical edge case, couples unrelated callers, or adds a generic framework before examples justify it.
- A shim, feature flag, test-only branch, or hypothetical fallback not authorized by the change's plan.

Do NOT flag:

- Similar-looking code when callers have legitimately different reasons to change.
- The first or second similar instance when drift risk is not yet concrete.

## Mandatory boundary and error-handling checks

Flag when changed code touches a platform, SDK, network, auth, storage, process, filesystem, or other external boundary and:

- Does not handle a failure mode the boundary is known to produce.
- Assumes success without inspecting the returned error/result.
- Silently swallows errors that would hide regressions.
- Introduces an unguarded race, lifecycle bug, or resource leak.

## Mandatory name and clarity checks (bounded)

Flag when a changed name, constant, or conditional makes the code materially harder to read, maintain, or reason about — especially in:

- predicates and invariants
- magic constants in control flow
- helper names that describe the wrong thing
- inconsistent use of existing repo vocabulary

Do NOT flag:

- Ordinary style preferences when the existing repo is silent on them.
- Formatting or whitespace handled by a formatter.
- Comment-density opinions when no behavior is obscured.

## Mandatory proof-adequacy checks

Proof scales with changed risk. Flag when:

- A behavior-shaping change ships without any corresponding assertion.
- A refactor lacks a credible behavior-preservation signal (tests, typecheck, build, instrumentation, targeted regression check).
- Tests only prove trivia (deletion, visual constants, mock interactions with no behavior assertion, timing hacks).
- Integration-shaped behavior is covered only by narrow unit mocks.

Do NOT require:

- A full test matrix for small local refactors that are already covered by existing checks.
- New test frameworks when an existing signal (typecheck, lint, build) is enough.

## Mandatory docs and contract drift checks

Flag when the change alters behavior, commands, install paths, APIs, examples, comments, prompts, telemetry names, stable IDs, or user-facing contracts and the corresponding live truth surface is now stale or contradictory. Covered surfaces include:

- `README.md`, `docs/`, inline code comments, docstrings
- install scripts, `Makefile`, CI config that names the changed behavior
- example invocations, snippets, fixtures, generated artifacts
- agent instructions (`AGENTS.md`, `CLAUDE.md`, `SKILL.md`, prompt references)
- telemetry and analytics names
- user-facing error messages and copy

Do NOT flag:

- Ordinary docs cleanup unrelated to the change.
- Perceived documentation gaps in pre-existing code the change did not touch.

## Risk-triggered security checks

Run full security review only when the change touches any of:

- auth / authorization / access control
- input validation at a trust boundary
- crypto, hashing, signing, TLS
- secrets, tokens, credential handling, logging of sensitive data
- deserialization, SSRF, injection, command execution
- file / process / network execution
- privacy / PII handling
- dependency pins or infrastructure boundaries

Emit findings tied to reachable paths and concrete exploit or data-risk reasoning. Cite authoritative sources (OWASP, CERT, vendor docs) only when the claim depends on current best-practice.

Do NOT:

- Run a broad security audit for ordinary changes that do not touch the above surface.
- Emit generic "consider XSS/CSRF/etc." bullets without reachability and changed-code causality.

## External research policy

Consult external sources only when a best-practice, framework, API, security, or runtime claim depends on current authoritative behavior. When cited:

- Prefer primary sources (official docs, language specs, framework maintainers, OWASP, CERT, RFCs).
- Name the source in the finding.
- Let repo truth, user intent, and local contracts win any tiebreaker.

Do NOT:

- Cite opinion pieces or blog posts as authority.
- Import team-process advice (SLA, standup, workflow ceremony) into findings.
- Use external sources to manufacture findings against clean changed code.

## Findings-quality bar (sparse > noisy)

Every blocking finding MUST:

- name file, symbol, and line (or contiguous line range)
- state the concrete risk in plain language
- say what the fix should touch (without writing the fix)

Every non-blocking finding MUST meet the same bar or be dropped. Empty findings are a valid, useful outcome — say so plainly.

DO NOT:

- Restate the review requirements back to the caller.
- Emit "no issues found in this area." placeholder under every heading.
- Block on unrelated pre-existing issues that the change did not introduce or worsen.
- Use `deferred`, `optional`, or `nice-to-have` to downgrade ship-blocking convergence work.
- Fabricate a finding because a review was requested.

## Scope discipline

The reviewer is review-only:

- Never edit the target repo.
- Never instruct the caller model to write the fix for the user.
- Never claim agent-linter coverage when `$agent-linter` did not run.
- Never produce a verdict when coverage requirements failed — emit the coverage-failure shape instead.
