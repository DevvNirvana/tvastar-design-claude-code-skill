# SwiftUI & Flutter Guidelines Reference

> Auto-loaded by `/design` when platform = ios (SwiftUI) or cross-platform (Flutter).

---

# SwiftUI Guidelines

## 🔴 High Severity

### Correct Property Wrapper Usage
```swift
// @State — view-local primitive state
struct Counter: View {
    @State private var count = 0  // ✅ private, owned by this view
    var body: some View {
        Button("\(count)") { count += 1 }
    }
}

// @StateObject — view CREATES the object
struct ProfileView: View {
    @StateObject private var vm = ProfileViewModel()  // ✅ view owns it

// @ObservedObject — object INJECTED from parent
struct ProfileCard: View {
    @ObservedObject var vm: ProfileViewModel  // ✅ passed in

// ❌ Using @StateObject for injected objects resets on re-render
struct ProfileCard: View {
    @StateObject var vm = ProfileViewModel()  // recreated on every render!
```

### Modifier Order Matters
```swift
// ✅ Background then padding — background fills padded area
Text("Hello")
    .padding()
    .background(Color.blue)  // background includes padding area

// ❌ Padding then background — background only behind text
Text("Hello")
    .background(Color.blue)  // only text-sized
    .padding()
```

### LazyVStack for Long Lists
```swift
// ✅ Lazy — only renders visible items
ScrollView {
    LazyVStack(spacing: 12) {
        ForEach(items) { item in
            ItemRow(item: item)
        }
    }
}

// ❌ VStack renders ALL items immediately
ScrollView {
    VStack { // 1000 items = 1000 views at once
        ForEach(items) { item in ItemRow(item: item) }
    }
}
```

### Accessibility Labels
```swift
// ✅ Clear label for screen readers
Button(action: deleteItem) {
    Image(systemName: "trash")
}
.accessibilityLabel("Delete item")

// ❌ Icon-only button with no accessibility label
Button(action: deleteItem) {
    Image(systemName: "trash")
}
```

---

## 🟡 Medium Severity

### @Observable (iOS 17+) vs ObservableObject
```swift
// ✅ Modern: @Observable macro (iOS 17+)
@Observable
class ViewModel {
    var items: [Item] = []
    var isLoading = false

    func loadItems() async {
        isLoading = true
        items = await apiService.fetchItems()
        isLoading = false
    }
}

// In view — @Bindable for two-way binding
struct ContentView: View {
    @State private var vm = ViewModel()

    var body: some View {
        List(vm.items) { item in ItemRow(item: item) }
            .task { await vm.loadItems() }
    }
}
```

### .task for Async Work
```swift
// ✅ .task — auto-cancels when view disappears
struct UserProfile: View {
    @State private var user: User?

    var body: some View {
        VStack {
            if let user { UserCard(user: user) }
            else { ProgressView() }
        }
        .task {
            user = await fetchUser()  // auto-cancelled on disappear
        }
    }
}

// ❌ onAppear Task — requires manual cancellation
.onAppear { Task { user = await fetchUser() } }
```

### NavigationStack (iOS 16+)
```swift
// ✅ Type-safe navigation
NavigationStack {
    ContentView()
        .navigationDestination(for: Item.self) { item in
            ItemDetailView(item: item)
        }
}

// In child view
NavigationLink(value: item) { ItemRow(item: item) }

// ❌ Deprecated
NavigationView { ... }
NavigationLink(destination: ItemDetailView(item: item)) { ... }
```

### Reduced Motion
```swift
// ✅ Respect accessibility
struct AnimatedView: View {
    @Environment(\.accessibilityReduceMotion) var reduceMotion

    var body: some View {
        content
            .animation(reduceMotion ? .none : .spring(), value: isExpanded)
    }
}
```

### Custom ViewModifiers
```swift
// ✅ Reusable modifier instead of repeating code
struct CardStyle: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(Color(.systemBackground))
            .cornerRadius(12)
            .shadow(radius: 4, y: 2)
    }
}

extension View {
    func cardStyle() -> some View { modifier(CardStyle()) }
}

// Usage
UserCard().cardStyle()
```

---

# Flutter Guidelines

## 🔴 High Severity

### const for Static Widgets
```dart
// ✅ const = zero runtime cost, widget reuse
const Text('Hello World')
const SizedBox(height: 16)
const Icon(Icons.home)

// ❌ Recreated every build — unnecessary allocation
Text('Hello World')  // no const
```

### ListView.builder for Long Lists
```dart
// ✅ Lazy — only builds visible items
ListView.builder(
  itemCount: items.length,
  itemExtent: 72.0,  // set if all items same height = faster scroll
  itemBuilder: (context, index) => ItemTile(item: items[index]),
)

// ❌ Builds all items at once
ListView(children: items.map((i) => ItemTile(item: i)).toList())
```

### Dispose Resources
```dart
class MyWidget extends StatefulWidget {
  @override
  State<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late StreamSubscription _subscription;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: const Duration(ms: 300));
    _subscription = stream.listen(handleEvent);
  }

  @override
  void dispose() {
    _controller.dispose()    // ✅ Always dispose
    _subscription.cancel()   // ✅ Always cancel
    super.dispose()
  }
}
```

### PopScope not WillPopScope
```dart
// ✅ Modern API (Flutter 3.12+)
PopScope(
  canPop: false,
  onPopInvoked: (didPop) {
    if (didPop) return;
    // Show confirmation dialog
    showExitDialog(context);
  },
  child: Scaffold(...)
)

// ❌ Deprecated
WillPopScope(onWillPop: () async { ... }, child: ...)
```

### Handle All Async States
```dart
// ✅ Handle loading, error, and data states
FutureBuilder<List<Item>>(
  future: fetchItems(),
  builder: (context, snapshot) {
    if (snapshot.connectionState == ConnectionState.waiting) {
      return const CircularProgressIndicator();
    }
    if (snapshot.hasError) {
      return ErrorView(error: snapshot.error);
    }
    if (!snapshot.hasData || snapshot.data!.isEmpty) {
      return const EmptyState();
    }
    return ItemList(items: snapshot.data!);
  },
)
```

---

## 🟡 Medium Severity

### Riverpod for State Management
```dart
// ✅ Provider definition
@riverpod
Future<List<Item>> items(ItemsRef ref) async {
  return await itemRepository.fetchAll();
}

// ✅ In widget
class ItemsScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final itemsAsync = ref.watch(itemsProvider);
    return itemsAsync.when(
      data: (items) => ItemList(items: items),
      loading: () => const LoadingView(),
      error: (e, _) => ErrorView(error: e),
    );
  }
}
```

### GoRouter Navigation
```dart
// ✅ Declarative routing
final router = GoRouter(
  routes: [
    GoRoute(path: '/', builder: (ctx, state) => const HomeScreen()),
    GoRoute(
      path: '/items/:id',
      builder: (ctx, state) => ItemScreen(id: state.pathParameters['id']!),
    ),
  ],
)

// Navigate
context.go('/items/$id')
context.push('/settings')
```

### Material 3 Theming
```dart
// ✅ ColorScheme.fromSeed — generates complete Material 3 palette
MaterialApp(
  theme: ThemeData(
    colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF4F46E5)),
    useMaterial3: true,
  ),
  darkTheme: ThemeData(
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF4F46E5),
      brightness: Brightness.dark,
    ),
    useMaterial3: true,
  ),
)
```

---

## Docs
- [SwiftUI Documentation](https://developer.apple.com/documentation/swiftui)
- [Flutter Widget Catalog](https://docs.flutter.dev/ui/widgets)
- [Riverpod](https://riverpod.dev/)
- [GoRouter](https://pub.dev/packages/go_router)
