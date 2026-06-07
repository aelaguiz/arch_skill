---
name: flutter-reference
description: "Use as a Flutter app-building reference for architecture, code quality, Dart style, state management, lifecycle, performance, rendering, testing, CI, accessibility, localization, security, platform integration, and Flame/game-loop guidance. Use when authoring, reviewing, repairing, or diagnosing Flutter mobile apps or games. Do not use for non-Flutter frontend work, generic visual design, running Flutter tooling, or latest Flutter/Dart facts without checking official docs."
---

# Flutter Reference

Use this skill when the user wants Flutter-specific guidance for building,
reviewing, repairing, or diagnosing production mobile apps or games.

This is a doctrine-only reference skill. It ships no scripts, tests, runners,
controllers, command wrappers, generated build files, or tool automation.

## When to use

- The user wants Flutter architecture, state management, project structure,
  Dart style, API design, dependency policy, or code review guidance.
- The user wants help with Flutter lifecycle, keys, remounts, async ownership,
  animation stability, rebuild scope, rendering, memory, or concurrency.
- The user wants Flutter testing, CI/CD, profiling, accessibility,
  localization, security, platform integration, assets, input, or native
  interop guidance.
- The user wants Flutter game architecture, Flame, HUD/shell boundaries, game
  loops, audio, physics, or per-frame performance guidance.
- The user is authoring or reviewing Flutter code and needs practical
  standards rather than generic frontend advice.

## When not to use

- The task is not about Flutter or Dart.
- The user wants generic visual design critique, product UX critique, or Figma
  file craft without Flutter implementation concerns.
- The user wants you to run Flutter tooling, operate an emulator, publish an
  app, or debug a local build pipeline. Use the repo's normal coding and tool
  workflow, then consult this skill only for Flutter judgment.
- The user asks for latest Flutter, Dart, package, Android, or iOS facts. Check
  current official docs before relying on version-sensitive claims.

## Non-negotiables

- Treat repository code, app behavior, and official docs as source truth when
  they are available. This skill gives defaults and review doctrine, not magic
  facts about an unseen app.
- Prefer the lightest architecture that makes ownership, lifecycle, state, and
  data flow explicit. Do not add layers because the app feels like it should be
  "enterprise."
- Keep `build()` pure. Async work, subscriptions, controllers, platform calls,
  and state mutation belong in lifecycle methods, provider/controller
  boundaries, repositories, services, or game-world systems.
- Make identity explicit. Keys should reflect semantic identity, not incidental
  state that causes accidental remounts.
- Do not claim performance wins without measurement. Use profile mode and real
  devices for meaningful Flutter performance claims.
- For games and high-frequency simulations, keep per-frame world state out of
  the widget tree. Bridge coarse HUD or shell state into Flutter widgets.
- Preserve accessibility, localization, and security as first-class app
  quality, not late cleanup.

## First move

1. Classify the user's request as `author`, `review`, `repair`, or `diagnose`.
2. Inspect the actual Flutter code, app structure, logs, screenshots, or
   failing behavior when the user provides them.
3. Load only the reference files needed for the current problem:
   - architecture/state decisions: `references/architecture-and-state.md`
   - Dart style, structure, APIs, dependencies: `references/dart-style-project-structure-and-api.md`
   - lifecycle, keys, async, animation replay: `references/lifecycle-identity-and-async.md`
   - performance, rendering, memory, isolates: `references/performance-rendering-memory-and-concurrency.md`
   - platform channels, input, assets, textures: `references/platform-integration-input-assets.md`
   - accessibility, localization, security: `references/accessibility-localization-security.md`
   - games, Flame, audio, physics: `references/games-flame-audio-and-physics.md`
   - testing, CI, reviews, anti-patterns: `references/testing-ci-and-review-practice.md`
   - current official docs and source links: `references/source-map.md`
4. If the request depends on current Flutter, Dart, package, Android, or iOS
   behavior, verify current official documentation before giving a
   version-sensitive answer.

## Workflow

1. Start from the app's real shape: small app, medium/large product app,
   package/workspace, add-to-app, plugin-heavy app, or game.
2. Name the ownership boundary first: UI, view model/notifier/bloc, domain
   logic, repository, service/plugin adapter, platform code, or game world.
3. Choose the smallest state and architecture pattern that makes that boundary
   reviewable.
4. Check lifecycle and identity before chasing surface symptoms. Many Flutter
   bugs are remounts, recreated futures/streams/controllers, async gaps, or
   rebuild storms.
5. For performance work, separate UI-isolate work, raster work, memory, image
   cache/external memory, platform-view composition, and game-loop update cost.
6. For review output, lead with the concrete defect or decision, then explain
   the Flutter mechanism and the smallest repair.

## Output expectations

- `author`: give a concrete Flutter architecture, code pattern, file structure,
  test plan, or implementation standard.
- `review`: findings first, with the Flutter mechanism, user-visible risk, and
  the smallest practical fix.
- `repair`: an ordered fix path that moves work to the right ownership layer
  and names the verification that proves it.
- `diagnose`: a short hypothesis list tied to Flutter runtime behavior, plus
  the next evidence to inspect.

## Reference map

- `references/architecture-and-state.md` - architecture defaults, layered app
  design, repositories/services, state-management tradeoffs, and game shell
  boundaries.
- `references/dart-style-project-structure-and-api.md` - Dart style, lints,
  package layout, workspaces, dependency policy, public APIs, immutability,
  null safety, and typed errors.
- `references/lifecycle-identity-and-async.md` - widget identity, keys,
  remounts, lifecycle methods, side-effect placement, animation replay,
  futures/streams, `setState`, mounted guards, and lifecycle tests.
- `references/performance-rendering-memory-and-concurrency.md` - profile-mode
  measurement, frame budgets, rebuild scope, expensive paint/layout work,
  images, textures, memory, isolates, Android/iOS profiling, and renderer
  caveats.
- `references/platform-integration-input-assets.md` - platform channels,
  Pigeon, FFI, platform views, textures, gestures, focus, semantics, assets,
  image variants, and cache discipline.
- `references/accessibility-localization-security.md` - screen readers,
  semantics, large text, RTL, localized strings, secrets, obfuscation limits,
  transport security, secure storage, signing, and attestation.
- `references/games-flame-audio-and-physics.md` - Flutter game architecture,
  Flame, game loops, HUD overlays, ECS/components, per-frame allocation,
  Flame lifecycle, input, audio, and physics.
- `references/testing-ci-and-review-practice.md` - unit/widget/golden/
  integration testing, leak checks, profile scenarios, CI lanes, anti-patterns,
  code review checklist, review comments, and limitations.
- `references/source-map.md` - official docs to verify version-sensitive
  Flutter, Dart, platform, state-package, testing, performance, and Flame facts.
