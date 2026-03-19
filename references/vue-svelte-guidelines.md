# Vue & Svelte Guidelines Reference

> Auto-loaded by `/design` when framework = vue, nuxt, svelte, or sveltekit.

---

# Vue 3 Guidelines

## 🔴 High Severity

### Never Use v-if + v-for on Same Element
```html
<!-- ✅ Use template wrapper -->
<template v-for="item in items" :key="item.id">
  <div v-if="item.visible">{{ item.name }}</div>
</template>

<!-- ❌ v-if priority is higher than v-for, causes bugs -->
<div v-for="item in items" v-if="item.visible" :key="item.id">
```

### Always Key v-for
```html
<!-- ✅ Stable ID as key -->
<div v-for="item in items" :key="item.id">

<!-- ❌ Index as key breaks animations and state -->
<div v-for="(item, i) in items" :key="i">
```

### Never Mutate Props
```vue
<script setup>
// ✅ Emit to parent
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()
const handleChange = (val: string) => emit('update:modelValue', val)

// ❌ Direct mutation crashes at runtime in strict mode
props.modelValue = newValue
</script>
```

### storeToRefs for Pinia
```ts
import { storeToRefs } from 'pinia'
const store = useCounterStore()

// ✅ Maintains reactivity
const { count, name } = storeToRefs(store)
const { increment } = store // actions don't need storeToRefs

// ❌ Loses reactivity — count is a plain number
const { count } = store
```

### Cleanup in onUnmounted
```ts
// ✅ Always clean up
onMounted(() => {
  window.addEventListener('resize', handleResize)
})
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
```

---

## 🟡 Medium Severity

### Composition API with script setup
```vue
<script setup lang="ts">
// Props with TypeScript
const props = defineProps<{
  title: string
  count?: number
}>()

// With defaults
const props = withDefaults(defineProps<{ count?: number }>(), { count: 0 })

// Emits
const emit = defineEmits<{
  change: [id: number]
  close: []
}>()

// Computed
const doubled = computed(() => props.count * 2)

// Watchers
watch(() => props.title, (newTitle) => {
  document.title = newTitle
})
</script>
```

### Composables (Custom Hooks)
```ts
// ✅ Always prefix with 'use'
export function useFetch<T>(url: string) {
  const data = ref<T | null>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)

  onMounted(async () => {
    loading.value = true
    try {
      const res = await fetch(url)
      data.value = await res.json()
    } catch (e) {
      error.value = e as Error
    } finally {
      loading.value = false
    }
  })

  return { data, loading, error } // return refs for reactive destructuring
}
```

### Pinia Store (Composition Style)
```ts
export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const isLoggedIn = computed(() => !!user.value)

  async function login(credentials: Credentials) {
    user.value = await authService.login(credentials)
  }

  function logout() {
    user.value = null
  }

  return { user, isLoggedIn, login, logout }
})
```

### Vue Router (Composition API)
```ts
const router = useRouter()
const route = useRoute()

// Lazy loaded routes
const routes = [
  {
    path: '/dashboard',
    component: () => import('./views/Dashboard.vue')
  }
]

// Navigation guard
router.beforeEach((to) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    return { name: 'Login' }
  }
})
```

---

# Svelte Guidelines

## 🔴 High Severity

### Reassign to Trigger Reactivity
```svelte
<script>
  let items = []

  // ✅ Reassignment triggers update
  function addItem(item) {
    items = [...items, item]
  }

  function removeItem(id) {
    items = items.filter(i => i.id !== id)
  }

  // ❌ Mutation does NOT trigger update
  function addItemWrong(item) {
    items.push(item)  // Svelte won't detect this!
  }
</script>
```

### Keys in {#each}
```svelte
<!-- ✅ Key by stable ID -->
{#each items as item (item.id)}
  <ItemCard {item} />
{/each}

<!-- ❌ No key or index key breaks animations/state -->
{#each items as item}
{#each items as item, i (i)}
```

### Auto-subscribe with $ prefix
```svelte
<script>
  import { count } from './stores'
  // ✅ $count auto-subscribes and unsubscribes
</script>

{$count}  <!-- auto-subscribed -->

<!-- ❌ Manual subscription requires manual cleanup -->
<script>
  let value
  count.subscribe(v => value = v) // memory leak if not unsubscribed!
</script>
```

### SvelteKit: load() not onMount()
```ts
// +page.js ✅ Server-side load
export async function load({ fetch, params }) {
  const res = await fetch(`/api/posts/${params.id}`)
  return { post: await res.json() }
}

// +page.svelte ❌ onMount is client-only, causes flash
import { onMount } from 'svelte'
onMount(async () => {
  data = await fetch('/api/posts').then(r => r.json())
})
```

---

## 🟡 Medium Severity

### Svelte 5 Runes
```svelte
<script>
  // Svelte 5: use runes
  let count = $state(0)
  let doubled = $derived(count * 2)

  $effect(() => {
    console.log('count changed:', count)
    return () => console.log('cleanup') // cleanup
  })

  // Props
  let { name, age = 0 } = $props()
</script>
```

### Stores
```ts
import { writable, readable, derived } from 'svelte/store'

// Writable for shared mutable state
export const user = writable<User | null>(null)

// Derived for computed values
export const isLoggedIn = derived(user, $user => !!$user)

// Readable for external data
export const time = readable(new Date(), (set) => {
  const interval = setInterval(() => set(new Date()), 1000)
  return () => clearInterval(interval) // cleanup
})
```

### SvelteKit Form Actions
```ts
// +page.server.ts ✅ Server-side form handling
export const actions = {
  default: async ({ request }) => {
    const data = await request.formData()
    const email = data.get('email')
    // validate + save
    return { success: true }
  }
}
```

```svelte
<!-- +page.svelte -->
<form method="POST">
  <input name="email" type="email" />
  <button>Submit</button>
</form>
```

### Transitions
```svelte
<script>
  import { fade, fly, slide } from 'svelte/transition'
  let visible = false
</script>

<!-- ✅ Built-in transitions -->
{#if visible}
  <div transition:fade={{ duration: 200 }}>Content</div>
{/if}

<!-- Different in/out -->
<div in:fly={{ y: -20 }} out:fade>Content</div>
```

---

## Docs
- [Vue Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [Pinia](https://pinia.vuejs.org/)
- [Svelte Reactivity](https://svelte.dev/docs/svelte-components#script-2-assignments-are-reactive)
- [SvelteKit Routing](https://kit.svelte.dev/docs/routing)
