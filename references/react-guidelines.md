# React Guidelines Reference

> Auto-loaded by `/design` when framework = react/nextjs/vite. Modern React 18+ patterns.

---

## 🔴 High Severity — Always Apply

### Keys in Lists
```tsx
// ✅ Stable unique key
{items.map(item => <Card key={item.id} {...item} />)}

// ❌ Index as key — breaks animations, state, focus
{items.map((item, i) => <Card key={i} {...item} />)}
```

### Pass Handlers, Not Invocations
```tsx
// ✅ Reference
<Button onClick={handleClick}>Submit</Button>

// ❌ Immediate call (runs on every render!)
<Button onClick={handleClick()}>Submit</Button>
```

### Rules of Hooks
```tsx
// ✅ Always at top level
function Component() {
  const [open, setOpen] = useState(false)
  const data = useFetch('/api/data')
  // ...
}

// ❌ Hooks in conditions crash React
function Component() {
  if (loading) {
    const [x, setX] = useState(false) // CRASH
  }
}
```

### Semantic HTML
```tsx
// ✅ Button for actions
<button onClick={handleDelete} className="...">Delete</button>

// ❌ Div with onClick — not keyboard accessible, no semantics
<div onClick={handleDelete} className="...">Delete</div>
```

### Effect Cleanup
```tsx
// ✅ Always return cleanup for subscriptions
useEffect(() => {
  const sub = store.subscribe(handler)
  return () => sub.unsubscribe()
}, [store])

// ❌ Memory leak — subscription never cleaned
useEffect(() => {
  store.subscribe(handler)
}, [store])
```

---

## 🟡 Medium Severity — Best Practice

### State Design
```tsx
// ✅ Derive, don't store
function Cart({ items }) {
  const total = items.reduce((sum, i) => sum + i.price, 0) // computed

  // ❌ Derived state causes sync bugs
  const [total, setTotal] = useState(0)
  useEffect(() => setTotal(items.reduce(...)), [items])
}
```

### Memoization
```tsx
// useMemo — expensive calculations
const sortedList = useMemo(
  () => [...items].sort((a, b) => a.name.localeCompare(b.name)),
  [items]
)

// useCallback — stable handlers for memoized children
const handleSelect = useCallback(
  (id: string) => setSelected(id),
  [] // no deps = stable forever
)

// React.memo — pure components
const UserCard = memo(({ user }: { user: User }) => (
  <Card>...</Card>
))
```

### Context — Memoize Values
```tsx
// ✅ Memoized context — no unnecessary re-renders
const AuthContext = createContext<AuthCtx | null>(null)

function AuthProvider({ children }) {
  const [user, setUser] = useState<User | null>(null)
  const value = useMemo(() => ({ user, setUser }), [user])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

// ❌ New object every render — all consumers re-render
<AuthContext.Provider value={{ user, setUser }}>
```

### Avoid Unnecessary Effects
```tsx
// ✅ Compute during render
function FilteredList({ items, query }) {
  const filtered = items.filter(i => i.name.includes(query)) // no effect needed!
  return <ul>{filtered.map(...)}</ul>
}

// ❌ Pointless effect for derived state
function FilteredList({ items, query }) {
  const [filtered, setFiltered] = useState([])
  useEffect(() => {
    setFiltered(items.filter(i => i.name.includes(query)))
  }, [items, query]) // extra render, same result
}
```

### Code Splitting
```tsx
import { lazy, Suspense } from 'react'

// Lazy load heavy components
const DataTable = lazy(() => import('./DataTable'))
const ChartView = lazy(() => import('./ChartView'))

function Dashboard() {
  return (
    <Suspense fallback={<Skeleton className="h-48" />}>
      <DataTable />
    </Suspense>
  )
}
```

---

## Performance Checklist

| Check | Pattern |
|-------|---------|
| Long lists | Use `react-window` or `react-virtual` for 100+ items |
| Error boundaries | Wrap major sections in `<ErrorBoundary>` |
| Profiler | Use React DevTools Profiler before optimizing |
| Batch updates | React 18 auto-batches — avoid `flushSync` |
| Transitions | `startTransition` for non-urgent UI updates |

---

## TypeScript Patterns
```tsx
// Component props
interface ButtonProps {
  label: string
  onClick: () => void
  variant?: 'primary' | 'secondary' | 'destructive'
  disabled?: boolean
}

// Event handlers
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value)
}

// Generic list component
function List<T extends { id: string }>({ items, renderItem }: {
  items: T[]
  renderItem: (item: T) => React.ReactNode
}) {
  return <ul>{items.map(item => <li key={item.id}>{renderItem(item)}</li>)}</ul>
}
```

---

## Docs
- [React Hooks Reference](https://react.dev/reference/react)
- [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)
- [Choosing State Structure](https://react.dev/learn/choosing-the-state-structure)
