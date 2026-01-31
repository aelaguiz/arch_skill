# Pragmatic Flutter testing: knowing when NOT to test

**The most valuable testing skill is restraint.** An experienced engineer doesn't maximize test coverage—they maximize the ratio of bugs caught to maintenance cost incurred. This guide provides authoritative, value-driven guidance on Flutter testing with equal emphasis on what to test and what to leave alone. The bias throughout is pragmatic: test the right things in the right way, and ruthlessly avoid tests that cost more than they're worth.

The frustration with AI-generated pointless tests—verifying a deleted file isn't used, checking an image's expected color—reflects a deeper problem: **coverage-driven testing** rather than **value-driven testing**. The solution isn't better AI; it's better judgment about what deserves a test in the first place.

---

## The Flutter test pyramid and official guidance

Flutter officially recognizes three test types, each with distinct trade-offs that determine when to use them:

| Test Type | Confidence | Maintenance Cost | Speed | Best For |
|-----------|------------|------------------|-------|----------|
| **Unit** | Low | Low | Quick | Business logic, data transformations, isolated functions |
| **Widget** | Higher | Higher | Quick | UI components, user interactions, state responses |
| **Integration** | Highest | Highest | Slow | Critical user journeys, end-to-end flows |

Google's recommended distribution is **70% unit tests, 20% integration tests, and 10% end-to-end tests**—the classic pyramid shape. Flutter's official docs state: "A well-tested app has **many unit and widget tests**, tracked by code coverage, plus **enough integration tests** to cover all the important use cases."

The key word is "enough." Not comprehensive. Not exhaustive. Enough.

Google's 2024 **SMURF framework** provides a more nuanced lens: Speed, Maintainability, Utilization, Reliability, and Fidelity. These dimensions are in tension—unit tests excel at speed and maintainability but lack fidelity to real conditions; integration tests offer high fidelity but sacrifice speed and reliability. The art is balancing these trade-offs for your specific codebase.

---

## When tests become liabilities: the negative value test

A **negative value test** costs more to maintain than the bugs it catches. These tests actively harm velocity by breaking on unrelated changes, requiring constant updates, and giving false confidence. Google's Software Engineering book warns: "If a team regularly writes brittle tests, test maintenance will inevitably consume a larger and larger proportion of the team's time."

Here are the canonical patterns of tests that should never be written:

**Testing implementation details rather than behavior.** If a test breaks when you refactor internal code without changing external behavior, it's testing the wrong thing. Kent Beck's Test Desiderata explicitly requires tests be "structure-insensitive"—they shouldn't break when code structure changes. A test that verifies `PaymentProcessor.process()` was called is implementation-coupled; a test that verifies the user's cart is empty after checkout is behavior-coupled.

**Testing framework or library code.** You are not responsible for verifying that Flutter's `Text` widget renders text, that Dart's `List.add()` works, or that your HTTP client library makes requests correctly. If you're explicitly testing third-party behavior, either delete the test (not your responsibility) or contribute it upstream.

**Testing trivial code.** Simple getters, setters, constructors, and constants have no logic to verify. A test asserting `user.email` returns the email you set is testing that Dart assignment works. These tests can never meaningfully fail.

**Testing generated code.** Code generators and build systems are responsible for their output. Very Good Ventures explicitly excludes generated code from coverage requirements.

**Tests that verify mocks work, not your code.** When a test's primary assertions are `verify(mock.method()).called(1)`, you're testing that your mock setup is correct, not that your system behaves correctly. Over-mocked tests routinely pass while the real system fails.

---

## The seven deadly sins of Flutter testing

**Sin 1: Testing that deleted code isn't used.** The compiler already enforces this. A test verifying an import doesn't exist or a removed function isn't called is pure noise.

**Sin 2: Testing visual constants.** Asserting an image has expected dimensions, a color value equals `0xFF0000FF`, or a widget has a specific margin provides zero regression protection. These "tests" break whenever design changes and catch nothing.

**Sin 3: Testing data model existence.** "Customer object has email field" is not a test—it's a type system check. TypeScript, Dart's null safety, and static analysis handle this.

**Sin 4: Snapshot testing internal state.** Any snapshot that captures implementation details rather than public behavior will break on every refactor.

**Sin 5: Golden tests on unstable UI.** Golden tests provide value only when UI is locked down. Running pixel-perfect comparisons on screens still being designed creates an avalanche of false failures. eBay Motors' guidance: "Minimize full-screen goldens and reserve them for high-level visual integration tests. Often, we only have **one multiScreenGolden() test per screen**."

**Sin 6: Tests requiring artificial delays.** If a test needs `await Future.delayed()` to work, it's testing timing rather than behavior and will be flaky.

**Sin 7: Order-dependent tests.** Tests that pass only when run in sequence indicate shared mutable state—a maintenance nightmare.

---

## What actually deserves automated tests

Focus automated testing where it provides asymmetric value: **high bug risk, high user impact, low maintenance cost**.

**Business logic and data transformations** are the highest-value test targets. Pure functions that calculate prices, validate inputs, transform data structures, or make decisions have clear inputs and outputs, no dependencies, and high regression risk. These should have extensive unit tests covering normal cases, edge cases, and error conditions.

**State management code** (BLoC, Riverpod, Provider) represents critical application behavior. Test state transitions thoroughly using packages like `bloc_test`:

```dart
blocTest<CartBloc, CartState>(
  'adds item and recalculates total',
  build: () => CartBloc(),
  act: (bloc) => bloc.add(AddItem(product)),
  expect: () => [CartState(items: [product], total: 29.99)],
);
```

**User-facing behavior at integration points** deserves widget tests. Does tapping "Submit" disable the button and show a loading indicator? Does an empty state message appear when the list is empty? These behaviors matter to users.

**Critical paths through the application** warrant integration tests: authentication flows, checkout processes, core feature workflows. As Google notes, integration tests verify "all the widgets and services being tested work together as expected."

**Bugs that escaped to production** must be captured with regression tests. Martin Fowler's rule: "Before fixing a bug exposed by a high level test, replicate the bug with a unit test." This ensures the same bug never recurs.

---

## The philosophy of restraint: thought leaders on testing limits

The most valuable testing wisdom comes from practitioners who've seen over-testing destroy velocity.

**DHH's "TDD is Dead" critique** targets **test-induced design damage**: "Changes to your code that facilitate easier testing but harm the clarity of the code through needless indirection and conceptual overhead." His position: "You do not let your tests drive your design, you let your design drive your tests!" When testability demands contorting architecture, the tests are wrong, not the architecture.

**Guillermo Rauch's mantra**—"Write tests. Not too many. Mostly integration"—became a touchstone for pragmatic testing. Kent C. Dodds elaborated: "You get diminishing returns on tests as coverage increases much beyond 70%... When you strive for 100% all the time, you find yourself spending time testing things that really don't need to be tested."

**Kent Beck's Test Desiderata** lists twelve properties of valuable tests, acknowledging trade-offs: "Not all tests need to exhibit all properties. However, no property should be given up without receiving a property of greater value in return." The critical properties are **behavioral** (sensitive to behavior changes, not structure) and **structure-insensitive** (survives refactoring).

**Justin Searls** offers perhaps the most honest assessment: "People love debating what percentage of which type of tests to write, but it's a distraction. Nearly zero teams write expressive tests that establish clear boundaries, run quickly & reliably, and only fail for useful reasons. **Focus on that instead.**"

---

## Fixtures, mocks, and fakes: choosing the right test double

Mockito's own documentation states the hierarchy clearly: "Testing with real objects is preferred over testing with mocks—if you can construct a real instance for your tests, you should!"

**Use real objects** when constructible and deterministic. A pure function calculating discounts needs no mocking—pass real inputs, assert real outputs.

**Use fakes** (simplified implementations) when you need full interface compatibility across many tests. A `FakeUserRepository` that stores users in a `Map<String, User>` is reusable, readable, and behavior-preserving:

```dart
class FakeUserRepository implements UserRepository {
  final _users = <String, User>{};
  
  @override
  Future<User?> getUser(String id) async => _users[id];
  
  @override
  Future<void> saveUser(User user) async => _users[user.id] = user;
}
```

**Use mocks** (Mocktail/Mockito) when verifying interactions matters or when simulating specific error conditions. Mocks excel at testing "did we call the analytics service?" or "what happens when the API returns a 500?"

**Heavy mocking is a code smell.** Philippe Bourgau's observation: "I was losing a lot of time maintaining the mock setup code in line with the real classes." When tests require mocking four-plus dependencies with complex stubbing, the system under test likely has too many responsibilities.

---

## Manual testing: when automation isn't the answer

Very Good Ventures states plainly: "Automated tests don't solve all of the problems—there are always some behaviors or integrations which are best tested with real world users on physical devices."

**Visual and aesthetic verification** cannot be automated meaningfully. Does the animation feel smooth? Is the color scheme pleasant? Does the layout look balanced? These are human judgments.

**Exploratory testing** discovers unexpected behaviors that scripted tests miss by definition. A skilled tester trying to break the app finds edge cases no specification anticipated.

**Performance and "feel"** require human perception. Automated tests can measure frame rates; they cannot perceive jank. They can time API responses; they cannot feel sluggishness.

**Third-party integrations** with real backends, payment processors, or hardware often resist reliable automation. The cost of maintaining flaky integration tests against external services frequently exceeds manual verification.

**Just before release** is the appropriate time for comprehensive manual testing on real devices. After code freeze, human verification catches what automation missed.

Before deciding to rely on manual testing, always ask: "Can this be automated **cost-effectively**?" Manual testing doesn't scale, is inconsistent, and doesn't prevent regression. But for subjective quality and exploratory discovery, it's irreplaceable.

---

## Golden tests: high value or high noise?

Golden tests compare rendered widgets pixel-by-pixel against reference images. They sound appealing but carry significant maintenance burden.

**Golden tests are valuable for**: custom painters, charts, design system components with locked specifications, and catching unintended visual regressions.

**Golden tests become noise when**: UI is still in flux, tests run cross-platform (font rendering differs between macOS, Linux, Windows), or full-screen goldens capture components with many reasons to change.

**Best practice from eBay Motors**: Reserve full-screen goldens for high-level visual integration tests—often just one per screen. For variations and edge cases, use smaller widgets with fewer reasons to change. The Alchemist package (from VGV) addresses CI flakiness and provides a declarative API that reduces maintenance burden.

---

## Test maintenance: designing for longevity

Tests become liabilities when they're **brittle**—failing due to unrelated changes rather than actual bugs. Brittle tests have four sensitivities to manage:

- **Interface sensitivity**: Breaks when method signatures change
- **Behavior sensitivity**: Breaks on behavioral changes it shouldn't verify
- **Data sensitivity**: Breaks on unrelated data changes
- **Context sensitivity**: Breaks due to environment or timing

**Design refactoring-resistant tests** by testing through public APIs only, focusing on observable outcomes, using centralized test setup helpers, and asserting behaviors rather than method calls. "Customer can complete checkout" survives refactoring; "CartService.processPayment() was called with exact arguments" does not.

Google's engineering playbook: "Tests using only public APIs are, by definition, accessing the system under test in the same manner that its users would."

---

## Conclusion: the pragmatist's testing checklist

Before writing any test, ask these questions:

1. **Will this test fail for the right reasons?** It should fail when user-facing behavior breaks, not when internal structure changes.

2. **Does this test survive refactoring?** If changing implementation without changing behavior breaks the test, don't write it.

3. **Would a real user care if this fails?** Tests should protect what matters to users.

4. **Is this cheaper to test than to fix when it breaks?** Some code is so trivial or so stable that the maintenance cost of testing exceeds the cost of occasional manual fixes.

5. **Am I testing my code or someone else's?** Don't verify frameworks, libraries, or languages.

The goal is not maximum coverage. The goal is **maximum confidence per maintenance hour**. Kent Beck worked at Facebook when they had zero unit tests in 2011—and the system worked because developers took responsibility for their code. Tests are one tool for building confidence, not the only tool, and not always the right tool.

Write tests. Not too many. Mostly integration. And delete the ones that aren't paying rent.
