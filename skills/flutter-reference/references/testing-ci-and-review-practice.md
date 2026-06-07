# Testing, CI, And Review Practice

Use this reference when designing tests, CI lanes, performance scenarios, leak checks, code review standards, anti-pattern fixes, sample review comments, or acceptance criteria for Flutter work.

## Testing Strategy And CI/CD

### Testing, delivery, and performance

Flutter’s testing guidance is unusually clear: **unit tests** validate a single function/method/class, **widget tests** validate a widget in a controlled Flutter test environment, and **integration tests** validate a complete app or large slice of it. Flutter also says a well-tested app usually has **many unit and widget tests** plus **enough integration tests** for important use cases, because the trade-off is confidence versus speed and maintenance cost.

#### Testing strategy

The most effective Flutter testing portfolio is usually:

* **Unit tests** for repositories, mappers, validation, formatters, and state reducers.
* **Widget tests** for screen-state rendering, interaction, navigation triggers, responsive layout, and error states.
* **Golden tests** for design-system components and heavily visual widgets.
* **Integration tests** for the few highest-value end-to-end flows: auth, checkout, onboarding, offline recovery, deep link entry, and crash-prone native interactions.

| Tool | Purpose | Strengths | Caveats |
|---|---|---|---|
| `package:test` | Base Dart unit testing | Fast, pure Dart, ideal for business logic | No widget lifecycle |
| `flutter_test` | Widget and Flutter-aware tests | `WidgetTester`, `Finder`, `testWidgets`, golden support | Still not a full device environment |
| `integration_test` | End-to-end app testing | Runs app flows closer to reality; can verify performance | Slower, more setup, higher maintenance |
| Golden tests | Pixel/screenshot regression checks | Excellent for design systems and visual stability | Platform/font/rendering drift must be controlled |
| Mockito | Generated mocks, rich verification | Mature, official Dart publisher | More ceremony than hand-written fakes or mocktail |
| Mocktail | Null-safe mocking without code generation | Lightweight and ergonomic | Some teams prefer stricter/generated mocks |
| Patrol | Native UI automation on top of Flutter testing stack | Valuable for system dialogs and true native interactions | Extra setup and CLI requirements |

#### CI/CD

Flutter’s deployment guidance recommends automating continuous build and release workflows so apps reach beta testers frequently without manual steps. The official docs list several all-in-one CI/CD options with Flutter support and also document fastlane/Xcode Cloud paths, but the core pipeline is vendor-neutral. Flutter’s build-modes docs are also explicit: use **debug** during development, **profile** to analyze performance, and **release** for shipping artifacts.

A strong PR pipeline for Flutter should do this, in this order:

1. `dart pub get --enforce-lockfile`
2. `dart format --output=none --set-exit-if-changed .`
3. `flutter analyze`
4. Unit tests
5. Widget tests
6. Golden tests when visible UI changed
7. Integration tests for affected critical flows on at least one Android and one iOS lane before release branches merge

Release pipelines should additionally build signed release artifacts, push iOS builds to TestFlight and Android builds to an internal/beta Play track, and inject environment variables through CI secret storage and `--dart-define` rather than hard-coding values into source. Flutter’s deployment docs explicitly note that CI systems generally support encrypted environment variables and that Flutter supports passing them with `--dart-define`.

## Anti-Patterns And Review Practice

### Anti-patterns and review practice

The anti-patterns below are the ones to flag most aggressively in code review because they degrade readability, testability, performance, or future change cost fastest.

#### Business logic and side effects in `build`

`build` is supposed to describe UI for current state. Flutter’s UI model is reactive and builders are expected to be pure; Bloc’s docs state this explicitly for `BlocBuilder`. Recreating async work or mutating state inside `build` produces duplicate requests, hidden state transitions, and hard-to-test screens.

**Bad**

```dart
class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final future = ApiClient().fetchProfile(); // recreated every build

    return FutureBuilder<Profile>(
      future: future,
      builder: (context, snapshot) {
        if (!snapshot.hasData) return const CircularProgressIndicator();
        return Text(snapshot.data!.name);
      },
    );
  }
}
```

**Better**

```dart
class ProfileViewModel extends ChangeNotifier {
  ProfileViewModel(this._repo);

  final ProfileRepository _repo;

  ViewStatus<Profile> state = const ViewStatus.loading();

  Future<void> load() async {
    try {
      state = const ViewStatus.loading();
      notifyListeners();

      final profile = await _repo.fetchProfile();
      state = ViewStatus.data(profile);
    } catch (e, st) {
      state = ViewStatus.error(AppFailure.from(e, st));
    }
    notifyListeners();
  }
}
```

```dart
class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  late final ProfileViewModel vm;

  @override
  void initState() {
    super.initState();
    vm = context.read<ProfileViewModel>()..load();
  }

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: vm,
      builder: (context, _) => switch (vm.state) {
        Loading<Profile>() => const CircularProgressIndicator(),
        Data<Profile>(value: final profile) => Text(profile.name),
        Error<Profile>(failure: final failure) => Text(failure.message),
      },
    );
  }
}
```

#### Mutable state leaking across boundaries

The official simple state-management example exposes an **unmodifiable view** for the cart instead of the mutable backing list. That is exactly the right instinct. Exposing mutable collections makes bugs non-local and tests flaky.

**Bad**

```dart
class CartState {
  CartState(this.items);
  final List<Item> items; // mutable reference leaks
}
```

**Better**

```dart
import 'dart:collection';

final class CartState {
  CartState(List<Item> items) : items = UnmodifiableListView(items);

  final UnmodifiableListView<Item> items;

  int get totalItems => items.length;
}
```

#### Blocking the UI isolate with heavy parsing or transforms

Flutter’s isolate guidance is explicit: large computations that would otherwise cause UI jank should be moved to helper isolates, since Flutter apps otherwise do their work on a single main isolate. The `compute` API is designed for this on native platforms.

**Bad**

```dart
Future<List<Order>> loadOrders(String rawJson) async {
  final decoded = jsonDecode(rawJson) as List<dynamic>;
  return decoded.map(Order.fromJson).toList();
}
```

**Better**

```dart
Future<List<Order>> loadOrders(String rawJson) {
  return compute(_parseOrders, rawJson);
}

List<Order> _parseOrders(String rawJson) {
  final decoded = jsonDecode(rawJson) as List<dynamic>;
  return decoded
      .cast<Map<String, dynamic>>()
      .map(Order.fromJson)
      .toList(growable: false);
}
```

#### Eager list construction and expensive paint operations

Flutter’s docs explicitly say to use `ListView.builder` for long/infinite lists and to avoid `Opacity` in animations when alternatives like `AnimatedOpacity` or direct semitransparent drawing will do. Costly operations such as `saveLayer`, `Opacity`, and some clipping modes routinely show up in real app traces.

**Bad**

```dart
ListView(
  children: items
      .map((item) => Opacity(
            opacity: item.isDimmed ? 0.5 : 1,
            child: ProductTile(item: item),
          ))
      .toList(),
)
```

**Better**

```dart
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    final item = items[index];
    return AnimatedOpacity(
      opacity: item.isDimmed ? 0.5 : 1,
      duration: const Duration(milliseconds: 150),
      child: ProductTile(item: item),
    );
  },
)
```

#### Stringly typed platform channels mixed into UI code

Flutter’s platform-integration docs explicitly recommend Pigeon for type-safe platform code generation, and the platform-channels guide also emphasizes thread constraints. Hand-written string channel names sprinkled through widgets invite breakage and make reviews much harder. Keep platform interop in a package or service boundary, not in UI code.

**Bad**

```dart
class CameraButton extends StatelessWidget {
  static const channel = MethodChannel('camera_magic');

  const CameraButton({super.key});

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: () async {
        final result = await channel.invokeMethod('capturePhoto');
        debugPrint('$result');
      },
      child: const Text('Capture'),
    );
  }
}
```

**Better**

```dart
abstract interface class CameraGateway {
  Future<PhotoResult> capturePhoto();
}

final class NativeCameraGateway implements CameraGateway {
  NativeCameraGateway(this._api);

  final CameraApi _api; // generated by Pigeon

  @override
  Future<PhotoResult> capturePhoto() async {
    final dto = await _api.capturePhoto();
    return PhotoResult(path: dto.path, width: dto.width, height: dto.height);
  }
}
```

#### Importing another package’s `src` or leaving dependency overrides around

Effective Dart says not to import libraries inside another package’s `src`, because those internals may change without a breaking-version bump. The same mindset applies to `dependency_overrides`: they are a temporary development tool and are dangerous as long-lived project state.

**Bad**

```dart
import 'package:some_package/src/private_mapper.dart';
```

**Better**

```dart
import 'package:some_package/some_package.dart';

// or wrap the external package behind your own adapter interface
```

#### Storing secrets in the app and calling it “secured”

Flutter’s own docs explicitly warn that putting secrets in the app is poor security practice, and that obfuscation only obscures symbol names. Store user/device tokens with the platform’s secure storage primitives where necessary, but keep real secrets server-side.

**Bad**

```dart
const stripeSecretKey = 'sk_live_...';
const internalAdminApiKey = 'prod-...';
```

**Better**

```dart
// client gets a short-lived token or signed request from backend
final publishableKey = const String.fromEnvironment('STRIPE_PUBLISHABLE_KEY');
```

#### Code review checklist

Treat this as a synthesis checklist derived from the Flutter, Dart, Android, and Apple guidance in this reference.

| Area | Review questions |
|---|---|
| Architecture | Is responsibility clear? Is IO below the UI layer? Is state owned in one obvious place? |
| State | Is the chosen state manager appropriate for actual complexity, or is it overbuilt? |
| Widgets | Are builders pure? Are widgets small enough to review locally? Are unnecessary rebuilds avoided? |
| API design | Are public APIs typed? Are names explicit and intention-revealing? Are class modifiers used where appropriate? |
| Collections and state objects | Are view-state models immutable? Do collections avoid leaking mutability? |
| Imports and packaging | Any import into another package’s `src`? Any package boundary violation? |
| Dependencies | Is every new dependency justified? Is `pubspec.lock` updated intentionally? Any lingering `dependency_overrides`? |
| Async and errors | Are loading/error/success states explicit? Are raw exceptions translated at boundaries? |
| Testing | Are unit/widget tests present where logic/UI changed? Are integration/golden tests added when risk justifies it? |
| Performance | Was this profiled on real devices in profile mode? Are long lists lazy? Is heavy compute off the UI isolate? Any `Opacity`/`saveLayer`/clipping traps? |
| Accessibility | Are semantics/labels complete? Large text and screen readers covered? Touch targets reasonable? |
| Localization | Any hard-coded user strings? Any English-specific layout assumptions? |
| Security | Any embedded secrets? HTTPS/network policy correct? Secure storage and signing handled correctly? |

#### Sample review comments

These are high-signal, low-drama examples for real reviews.

| Scenario | Sample comment |
|---|---|
| Business logic in widget | “This widget is doing request orchestration and state mutation in `build`. Please move that into a feature controller/view model so the widget becomes a pure state-to-UI mapping.” |
| Overbuilt architecture | “This flow has one async request and three UI states. A full event/state graph here feels heavier than the problem. Can we collapse to a thinner notifier/view model?” |
| Mutable state leak | “`items` is exposed as a mutable `List`. Please return an unmodifiable view or copy so downstream code can’t mutate state behind our back.” |
| Performance risk | “This list eagerly builds all children. Please switch to `ListView.builder`; otherwise offscreen items will still incur build cost.” |
| Paint cost | “This animation wraps each row in `Opacity`. Can we avoid raster cost here with `AnimatedOpacity` or a direct color approach?” |
| Interop boundary | “Native channel strings in the widget make this hard to test and easy to break. Please move channel usage behind a gateway/service and prefer Pigeon-generated types if possible.” |
| Dependency hygiene | “This PR introduces a `dependency_overrides` entry. Is it temporary for local work, or are we accidentally baking an override into the app?” |
| A11y | “This custom control renders fine visually, but I don’t see semantics/labels. How will TalkBack/VoiceOver describe it?” |
| Localization | “This string is user-visible and hard-coded in the widget. Please move it into localization resources before the copy spreads further.” |
| Security | “This key appears to be a credential, not a public identifier. We should not ship it in the app binary.” |

### Open questions and limitations

No authoritative, current official benchmark data compares Riverpod, Bloc, Provider, and other state managers in a way that should drive architecture by runtime performance alone. The real determinants of app performance are usually rebuild scope, list virtualization, expensive paint/layout work, main-isolate blocking, and startup/rendering discipline. Where this reference compares state managers, it compares **ergonomics, structure, reviewability, and complexity cost**, not benchmark supremacy.

Some recommendation branches depend on details that were unspecified: whether the app is add-to-app, whether a separate domain/use-case layer is already organizational policy, whether the app is plugin/native-heavy, whether the team is two people or twenty, and whether regulated compliance or fraud-resistance requirements are in scope. Those constraints can reasonably push the choice toward thinner local-state patterns, more explicit Bloc-style modeling, or stronger package boundaries. Flutter’s own architecture docs explicitly say recommendations should be adapted to the app’s unique requirements rather than treated as rules.

## Testing, Profiling, CI, And Review Checklists

### Testing, profiling, continuous integration, and code review checklists

Flutter’s testing model spans unit tests, widget tests, and integration tests. The official testing overview explicitly distinguishes them, and the app architecture case study goes further by recommending that view-model logic be unit tested independently of Flutter widgets. That is the correct test pyramid for maintainability: most logic in pure Dart tests, widget tests for composition and lifecycle behavior, integration tests for end-to-end correctness and performance.

#### What to test

Unit tests should cover repositories, use cases, reducers, commands, and feature controllers without Flutter dependencies. Widget tests should cover key lifecycle and presentation invariants: does a controller get disposed, does a key change remount, does a loading future restart accidentally, does a modal appear with the correct semantics, does a gesture route correctly. Integration tests should cover native/plugin behavior, platform channels, platform views, heavy scrolling, app startup, and game session flows on real devices or simulators/emulators. Flutter’s integration-test docs also explicitly note that integration tests can be used to verify performance.

If the app or game is memory-sensitive, add leak tracking to tests. Flutter’s ecosystem now includes `leak_tracker` and `leak_tracker_flutter_testing`, and the Flutter framework itself has integrated leak tracking work across tests. DevTools Memory plus leak-tracking packages is a strong combination for stubborn retained-object bugs.

#### What to profile

Use the Performance Overlay for fast visual diagnosis and DevTools Performance view for actual analysis. Flutter’s performance docs describe the frame charts, frame analysis, timeline viewer, and the ability to track widget builds, layouts, and paints. Recent DevTools release notes also add widget build counts in frame analysis and rebuild stats views, which is ideal for catching rebuild storms that look harmless in code review.

Use the Memory view for heap and external memory, especially after scene transitions, repeated gameplay sessions, asset-heavy screens, or camera/video flows. Use the inspector for tree shape and selection. In IntelliJ or Android Studio, the Flutter Performance window can expose widget rebuild information directly.

#### The code review checklist

The checklist below is **author synthesis** grounded in the official docs covered throughout this reference.

| Review question | Pass condition |
|---|---|
| Is widget identity stable? | Keys reflect semantic identity, not incidental state |
| Is `build()` pure? | No subscriptions, async starts, controller creation, or animation starts inside `build()` |
| Are async tasks owned outside builders? | Futures/streams/controllers created in lifecycle or provider boundaries |
| Is mutable state at the right level? | Local view state local; feature state feature-scoped; simulation state off widget tree |
| Are rebuild scopes narrow? | Hot paths use `const`, small widgets, listenable child caching, selectors, or projections |
| Are lifecycle resources cleaned up? | Controllers, subscriptions, focus nodes, notifiers, and game disposables are disposed |
| Are animations identity-safe? | No accidental key churn; `didUpdateWidget()` handles config changes cleanly |
| Is the render path sane? | No gratuitous `Opacity`, clipping, `saveLayer`, intrinsic passes, or eager giant lists |
| Is native integration chosen deliberately? | Channels for API calls, FFI for native libs, textures/views only with composition trade-offs understood |
| Is game code loop-safe? | No per-frame `setState()`, per-frame allocations minimized, simulation decoupled from shell |

#### The CI checklist

A sane mobile Flutter CI lane should at minimum run `dart format --set-exit-if-changed`, `flutter analyze`, fast unit/widget tests, and a smaller set of targeted integration tests. For performance-sensitive apps or games, add one profile-mode scroll/perf scenario and one memory-sensitive scenario that exercises heavy images, video/textures, or a full gameplay loop. Flutter’s continuous-delivery and performance testing docs support exactly this direction.

A lean but effective CI matrix is:

- static checks and formatting
- unit tests for pure state/data logic
- widget tests for lifecycle/remount/rebuild behavior
- integration tests for iOS and Android critical flows
- one profile/perf benchmark scenario
- one memory/leak scenario for asset-heavy or game-heavy screens

#### Open questions and limitations

A few areas remain less crisply documented in official Flutter sources than others. Low-latency audio strategy on mobile is still largely package- and workload-dependent; the official docs are thinner there than they are for rendering or architecture. Similarly, exact determinism guarantees for cross-platform physics/game loops depend on the engine, packages, and floating-point behavior more than on Flutter itself. Those are areas where package-level benchmarks and production profiling matter more than generic rules.
