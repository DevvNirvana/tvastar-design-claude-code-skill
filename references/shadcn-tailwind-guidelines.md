# shadcn/ui & Tailwind CSS Guidelines Reference

> Auto-loaded by `/design` when has_shadcn=true or tailwind=true.

---

# shadcn/ui Guidelines

## Setup
```bash
# Always init first
npx shadcn@latest init

# Then add components individually
npx shadcn@latest add button card dialog form table sidebar
npx shadcn@latest add "https://reactbits.dev/r/AnimatedList-TS-TW"  # React Bits
```

## 🔴 High Severity

### CSS Variables for Theming (Never Hardcode Colors)
```css
/* globals.css — define both light and dark */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --destructive: 0 84.2% 60.2%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
  }
}
```

### Complete Dialog Structure
```tsx
// ✅ Required: DialogTitle for accessibility
<Dialog open={open} onOpenChange={setOpen}>
  <DialogTrigger asChild>
    <Button>Open</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Edit Profile</DialogTitle>          {/* required! */}
      <DialogDescription>                              {/* recommended */}
        Make changes to your profile here.
      </DialogDescription>
    </DialogHeader>
    {/* content */}
    <DialogFooter>
      <Button type="submit">Save changes</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>

// ❌ Missing DialogTitle — screen readers have no context
<DialogContent>
  <p>Edit your profile below</p>
</DialogContent>
```

### Form with React Hook Form + Zod
```tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Min 8 characters'),
})

export function LoginForm() {
  const form = useForm<z.infer<typeof schema>>({
    resolver: zodResolver(schema),
    defaultValues: { email: '', password: '' },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" {...field} />
              </FormControl>
              <FormMessage />  {/* shows validation error */}
            </FormItem>
          )}
        />
        <Button type="submit">Sign In</Button>
      </form>
    </Form>
  )
}
```

### Toaster in Root Layout
```tsx
// ✅ app/layout.tsx — once, at root
import { Toaster } from '@/components/ui/sonner'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Toaster />  {/* here, not in pages */}
      </body>
    </html>
  )
}

// Usage anywhere:
import { toast } from 'sonner'
toast.success('Saved!')
toast.error('Something went wrong')
```

---

## Component Patterns

### Cards
```tsx
<Card>
  <CardHeader>
    <CardTitle>Job Match</CardTitle>
    <CardDescription>87% match score</CardDescription>
  </CardHeader>
  <CardContent>
    {/* main content */}
  </CardContent>
  <CardFooter className="flex justify-between">
    <Button variant="outline">Save</Button>
    <Button>Apply Now</Button>
  </CardFooter>
</Card>
```

### Data Table
```tsx
// shadcn DataTable = Table + TanStack Table
import {
  useReactTable, getCoreRowModel, getSortedRowModel,
  getFilteredRowModel, flexRender,
} from '@tanstack/react-table'

// Full example: https://ui.shadcn.com/docs/components/data-table
```

### Sidebar (App Layout)
```tsx
// Must wrap in SidebarProvider
<SidebarProvider>
  <AppSidebar />
  <main>
    <SidebarTrigger />  {/* mobile toggle */}
    {children}
  </main>
</SidebarProvider>
```

### asChild Composition
```tsx
// ✅ Button as Link (NextJS)
<Button asChild>
  <Link href="/dashboard">Go to Dashboard</Link>
</Button>

// ❌ Nested button/anchor — invalid HTML
<Button>
  <Link href="/dashboard">Go to Dashboard</Link>
</Button>
```

---

# Tailwind CSS Guidelines

## 🔴 High Severity

### Focus States — Never Remove Without Replacement
```html
<!-- ✅ Replace outline with ring -->
<button class="focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2">

<!-- ❌ Removes focus entirely — keyboard users cannot navigate -->
<button class="focus:outline-none">
```

### Touch Targets — Minimum 44px
```html
<!-- ✅ Mobile-friendly -->
<button class="min-h-[44px] min-w-[44px] px-4">

<!-- ❌ Too small on mobile (32px) -->
<button class="h-8 w-8">
```

### Reduced Motion
```html
<!-- ✅ Respect user preference -->
<div class="animate-pulse motion-reduce:animate-none">

<!-- ❌ Ignores prefers-reduced-motion -->
<div class="animate-pulse">
```

### SVGs Need Explicit Dimensions
```html
<!-- ✅ Prevents layout shift before CSS loads -->
<svg class="size-6" width="24" height="24" viewBox="0 0 24 24">

<!-- ❌ Can cause layout shift -->
<svg class="size-6" viewBox="0 0 24 24">
```

---

## Layout Patterns

### Responsive Container
```html
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  {/* content */}
</div>
```

### Card Grid
```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```

### Centered Loading
```html
<div class="flex items-center justify-center min-h-[400px]">
  <Loader class="animate-spin text-muted-foreground size-8" />
</div>
```

---

## Typography Scale
```html
<h1 class="text-4xl font-bold tracking-tight lg:text-5xl">Page Title</h1>
<h2 class="text-2xl font-semibold tracking-tight">Section Heading</h2>
<h3 class="text-xl font-semibold">Subsection</h3>
<p class="text-base leading-relaxed text-muted-foreground">Body text</p>
<p class="text-sm text-muted-foreground">Caption / metadata</p>
```

## Tailwind v4 Changes
```css
/* v4: Use @theme instead of tailwind.config.js */
@theme {
  --color-primary: #4F46E5;
  --color-primary-foreground: #FFFFFF;
  --font-heading: 'Outfit', sans-serif;
}

/* v4: New gradient syntax */
/* ✅ */ bg-linear-to-r from-blue-500 to-purple-500
/* ❌ */ bg-gradient-to-r from-blue-500 to-purple-500
```

---

## Docs
- [shadcn/ui](https://ui.shadcn.com/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [React Hook Form](https://react-hook-form.com/)
- [Zod](https://zod.dev/)
