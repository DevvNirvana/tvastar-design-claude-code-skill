# Next.js Guidelines Reference
> Auto-loaded by `/design` when framework = nextjs.  
> Covers **Next.js 15** (App Router) + **React 19** — current as of March 2026.

---

## ⚡ What's New in 2025-2026 (Critical)

| Change | Impact |
|--------|--------|
| **Turbopack is now default** `next dev --turbo` | Faster HMR, some plugins incompatible |
| **React 19 ships by default** | `use()` hook, `useOptimistic`, `useFormStatus`, `useActionState` |
| **`fetch()` uncached by default** (Next.js 15) | Must explicitly set `cache: 'force-cache'` or `next: {revalidate}` |
| **`params` and `searchParams` are now Promises** | Must `await params` in page components |
| **PPR (Partial Prerendering) stable** | Static shell + dynamic holes in same route |
| **`after()` API for post-response work** | Analytics, logging after response sent |
| **`connection()` for dynamic data** | Replaces `noStore()` from next/cache |
| **`forbidden()` / `unauthorized()`** | New navigation functions for auth errors |

---

## 🔴 High Severity — Always Apply

### Rendering Model
```tsx
// ✅ Server Components by default (no 'use client')
// ✅ React 19: async params/searchParams are Promises
export default async function Page({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>
  searchParams: Promise<{ q: string }>
}) {
  const { id } = await params          // ← must await in Next.js 15
  const { q } = await searchParams     // ← must await in Next.js 15
  const data = await fetchData(id)
  return <div>{data.title}</div>
}

// ❌ Old pattern — params not awaited (breaks in Next.js 15)
export default function Page({ params }: { params: { id: string } }) {
  const { id } = params  // Type error in Next.js 15
}
```

### Images — Always next/image
```tsx
import Image from 'next/image'

// ✅ Sized image
<Image src={url} alt="Description" width={400} height={300} />

// ✅ Fill layout
<Image src={hero} alt="Hero" fill className="object-cover" priority />

// ❌ Raw <img> — no optimization, causes LCP regression
<img src={url} />
```

### Data Fetching (Next.js 15: no default cache)
```tsx
// ✅ Static — cached forever (ISR)
const data = await fetch(url, { cache: 'force-cache' })

// ✅ Revalidate every hour
const data = await fetch(url, { next: { revalidate: 3600 } })

// ✅ Always fresh
const data = await fetch(url, { cache: 'no-store' })

// ❌ Next.js 15: bare fetch() = uncached (was cached in Next.js 14)
const data = await fetch(url)  // No cache behavior — dangerous!
```

### Server Actions — React 19 Pattern
```tsx
// ✅ React 19: useActionState (replaces useFormState)
import { useActionState } from 'react'

function CreateForm() {
  const [state, action, isPending] = useActionState(createPost, null)
  return (
    <form action={action}>
      <input name="title" />
      <button disabled={isPending}>
        {isPending ? 'Creating...' : 'Create'}
      </button>
    </form>
  )
}

// ✅ Server Action with validation + revalidation
async function createPost(prevState: unknown, formData: FormData) {
  'use server'
  const body = schema.parse(Object.fromEntries(formData))
  // Always: auth check before mutation
  const session = await getSession()
  if (!session) throw new Error('Unauthorized')
  await db.post.create({ data: body })
  revalidatePath('/posts')
}

// ❌ Never trust Server Action input without Zod validation
// ❌ Never mutate without checking auth/session first
```

### Environment Variables
```bash
# ✅ Client-accessible
NEXT_PUBLIC_API_URL=https://api.example.com

# ✅ Server-only (never expose)
DATABASE_URL=postgres://...
AUTH_SECRET=...

# ❌ Server-only var in 'use client' file = runtime crash
```

### Security
```tsx
// ✅ Sanitize before dangerouslySetInnerHTML
import DOMPurify from 'isomorphic-dompurify'
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(content) }} />

// ✅ React 19: forbidden() for auth errors
import { forbidden, unauthorized } from 'next/navigation'
if (!session) unauthorized()        // 401
if (!hasPermission) forbidden()     // 403
```

---

## 🟡 Medium Severity — Best Practice

### Fonts — Always next/font (zero layout shift)
```tsx
import { Outfit, DM_Sans } from 'next/font/google'
const heading = Outfit({ subsets: ['latin'], weight: ['600','700','800'], variable: '--font-heading' })
const body    = DM_Sans({ subsets: ['latin'], weight: ['400','500'], variable: '--font-body' })

// layout.tsx
<body className={`${heading.variable} ${body.variable}`}>

// globals.css
@theme {
  --font-heading: var(--font-heading);
  --font-body:    var(--font-body);
}

// ❌ External Google Fonts link causes FOUT + layout shift
```

### Route Structure with PPR
```
app/
├── (marketing)/
│   ├── page.tsx           ← static shell
│   └── pricing/page.tsx
├── (app)/
│   ├── dashboard/
│   │   ├── page.tsx       ← PPR: static shell + dynamic data
│   │   ├── loading.tsx    ← streaming skeleton (always create)
│   │   └── error.tsx      ← error boundary (always create)
│   └── settings/page.tsx
└── layout.tsx
```

### Partial Prerendering (PPR) — 2025 stable
```tsx
// next.config.ts
export default {
  experimental: { ppr: 'incremental' }
}

// page.tsx — static shell with dynamic holes
import { unstable_noStore as noStore } from 'next/cache'
import { Suspense } from 'react'

export default function Page() {
  return (
    <main>
      <StaticHero />                    {/* prerendered */}
      <Suspense fallback={<Skeleton />}>
        <DynamicFeed />                 {/* streams in */}
      </Suspense>
    </main>
  )
}
```

### `after()` — Post-Response Work
```tsx
import { after } from 'next/server'

export default async function Page() {
  after(() => {
    // Runs AFTER response sent — perfect for analytics
    logPageView()
    updateCache()
  })
  return <div>Page content</div>
}
```

### API Routes (App Router)
```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'

const schema = z.object({ name: z.string().min(1) })

export async function POST(request: NextRequest) {
  const body = schema.parse(await request.json())
  return NextResponse.json({ success: true }, { status: 201 })
}
```

### Dynamic Imports for Bundle Splitting
```tsx
import dynamic from 'next/dynamic'

// Heavy animation/chart components — always dynamic
const HeavyChart = dynamic(() => import('./Chart'), {
  ssr: false,
  loading: () => <Skeleton className="h-48 w-full" />,
})

// Framer Motion — only load on client
const MotionDiv = dynamic(() => import('framer-motion').then(m => m.motion.div), {
  ssr: false,
})
```

### Middleware
```ts
// middleware.ts
import { NextResponse } from 'next/server'
export function middleware(request) {
  const token = request.cookies.get('auth-token')
  if (!token) return NextResponse.redirect(new URL('/login', request.url))
  return NextResponse.next()
}
export const config = {
  matcher: ['/dashboard/:path*', '/settings/:path*'],
}
```

---

## React 19 New APIs (ships with Next.js 15)

```tsx
// use() — read resources in render
import { use } from 'react'
function Comments({ commentsPromise }: { commentsPromise: Promise<Comment[]> }) {
  const comments = use(commentsPromise)  // Suspense-integrated
  return comments.map(c => <p key={c.id}>{c.text}</p>)
}

// useOptimistic — instant UI while server updates
import { useOptimistic } from 'react'
const [optimisticLikes, addOptimisticLike] = useOptimistic(
  likes,
  (state, newLike) => [...state, newLike]
)

// useFormStatus — read parent form state
import { useFormStatus } from 'react-dom'
function SubmitButton() {
  const { pending } = useFormStatus()
  return <button disabled={pending}>{pending ? 'Saving...' : 'Save'}</button>
}
```

---

## Turbopack Notes (2025-2026)

Turbopack is the default dev bundler in Next.js 15. Key differences:
- **Faster HMR**: 10× faster than Webpack for large projects
- **Plugin incompatibility**: Some webpack plugins won't work. Check before adding.
- **CSS Modules**: Full support, including `composes`
- **SWC transforms**: All SWC transforms supported
- **Babel**: If you need custom Babel config, Turbopack won't run — falls back to Webpack

```bash
# Default in Next.js 15
next dev          # Uses Turbopack
next dev --no-turbo  # Force Webpack if plugin issues
```

---

## Docs (March 2026)
- [Next.js 15 Docs](https://nextjs.org/docs)
- [React 19 Release Notes](https://react.dev/blog/2024/12/05/react-19)
- [PPR Docs](https://nextjs.org/docs/app/building-your-application/rendering/partial-prerendering)
- [Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)
- [next/image](https://nextjs.org/docs/app/building-your-application/optimizing/images)
- [next/font](https://nextjs.org/docs/app/building-your-application/optimizing/fonts)
