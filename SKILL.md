---
name: ui-design-intelligence  
description: >
  World-class UI/UX design intelligence — Tvastar v4.0.
  TRIGGER on: /design /preview /approved /apply /review /ship /component /heal
  /tokens /dark /a11y /cro /color /typography /motion /extract /storybook,
  build page, build component, landing page, hero section, dashboard, nav, card,
  animation, dark mode, layout, color palette, typography, redesign, make it look
  better, add animations, style this, improve UI, add polish, professional look,
  modern design, review my code, check before deploy, is this ready to ship.
---

# UI Design Intelligence — Tvastar v4.0
**18 libraries · 24 styles · 86 lint rules · 14 intelligent slots · March 2026**

---

## The /design Workflow — 7 Steps (follow in exact order)

### Step 1 — Scan the stack
```bash
python3 .claude/skills/ui-design-intelligence/scripts/detect_stack.py
```
Detects: framework, Tailwind v3/v4, all 18 libraries (React Bits, Aceternity, Magic UI,
Tremor, Animata, Motion Primitives, Cult UI, Eldora UI, Kibo UI, Origin UI, etc.)

**READ NOW based on detection:**
- `has_react_bits: true` → read `references/react-bits-catalog.md`
- Any new 2026 lib detected → read `references/component-library-catalog.md`
- Next.js detected → read `references/nextjs-guidelines.md` (Next.js 15 + React 19)
- shadcn/tailwind detected → read `references/shadcn-tailwind-guidelines.md`
- Vue/Nuxt detected → read `references/vue-svelte-guidelines.md`

### Step 2 — Understand the request
Extract: **What** (page/component), **Aesthetic** (style keywords), **Constraints**, **Existing colors**.
Ask ONE clarifying question only if completely blocked. Never ask multiple questions.

### Step 3 — Live Research (always run)
**READ NOW:** `references/resources-blogs.md` — full search routing brain with 2026-updated sources.

Run at minimum 2 web searches:
```
1. "[product type] design inspiration 2026 site:dribbble.com"
2. "[aesthetic] UI site:godly.website OR site:awwwards.com"
3. (if new library needed) "[library name] component examples site:github.com"
```
Extract from results: dominant visual treatment, typography scale, ONE unexpected interaction.

### Step 4 — Generate design system
```bash
python3 .claude/skills/ui-design-intelligence/scripts/design_system.py \
  --product "[type]" --style "[keywords]" [--dark] [--persist] \
  --page landing|dashboard|auth|pricing|portfolio|feature
```

The output contains ALL of these — read every section:
- **PALETTE + COLOR SCIENCE** — WCAG ratios, failing colors with suggested fixes
- **TYPOGRAPHY** — pairing + Fontshare/Google URL + weights
- **TYPE SCALE** — display→caption with exact px/rem values
- **ANIMATION TOKENS + MOTION DURATION TABLE** — exact ms + easing per context
- **STYLE PROFILE** — effects to use, anti-patterns to avoid
- **COMPONENT LIBRARY SELECTIONS** — 14 slots, each mapped to the RIGHT library:
  - background, hero_text, sub_text, cta_button, feature_cards, stats
  - testimonials, logos, borders, mobile_menu, navigation
  - delight (cursor/wow effect), forms (if form present), charts/kpi_cards (if dashboard)
  - advanced_ui (kanban/datepicker if enterprise)
- **INSTALL COMMANDS** — exact npx/npm/copy commands per library
- **INSPIRATION BENCHMARKS** — product-type-specific reference sites
- **SENIOR DESIGNER EYE TEST** — 8-point quality checklist
- **GESTALT CHECKS** — 7 principles applied to this specific palette
- **REACT BITS INSTALL** — TS+TW variants for TypeScript
- **PSYCHOLOGY LAWS** — 3 UX laws applied to this product
- **PAGE PATTERN** — section-by-section layout blueprint
- **CHART TYPE GUIDANCE** — appears for dashboard/analytics
- **PRE-DELIVERY CHECKLIST** — 15 must-pass gates

**READ NOW (framework-specific):**
- Next.js → `references/nextjs-guidelines.md` (Next.js 15, React 19, Turbopack, PPR, params awaiting)
- shadcn/Tailwind → `references/shadcn-tailwind-guidelines.md`
- React/Vite → `references/react-guidelines.md`
- Vue/Nuxt → `references/vue-svelte-guidelines.md`
- SwiftUI/Flutter → `references/native-guidelines.md`

### Step 5 — Design plan (WAIT for approval — never skip this)
Show this exact format:
```
╔══ TVASTAR DESIGN PLAN ═════════════════════════════════════════╗
║ Building:        [what exactly]                                 ║
║ Style:           [name + 1-line why it fits]                    ║
║ Research:        [2 sites studied + key insight from each]      ║
║                                                                 ║
║ PALETTE          Primary — CTA — Bg   [WCAG ratios]            ║
║ TYPOGRAPHY       [Heading] / [Body]   [scale name]             ║
║                                                                 ║
║ STATEMENT PIECE  [lib: component] — the one wow moment         ║
║ SUPPORTING       [slot: lib/component] × 4-5 key slots         ║
║                                                                 ║
║ UX LAWS          [law 1 + how applied]                         ║
║                  [law 2 + how applied]                         ║
║ GESTALT          [principle + application]                      ║
║                                                                 ║
║ MISSING LIBS?    [install commands if anything not installed]   ║
╚═════════════════════════════════════════════════════════════════╝
Build with this plan? (yes / change [what])
```

### Step 6 — Build production code
Output order: globals.css/`@theme` → install commands → component code.

**READ NOW during code generation:**
- Page patterns → `references/page-patterns.md` (section order, mobile-first, empty states)
- Icons/charts → `references/charts-icons-reference.md` (chart matrix, Lucide lookup)
- Animations → `references/motion-principles.md` (library-specific patterns, duration table)
- UX laws → `references/ux-principles.md` (Gestalt, psychology laws)

**Cover every state:**
default → hover → focus → active → loading → disabled → error → empty state

**2026 code standards:**
- Next.js 15: `await params` and `await searchParams` — they are Promises
- React 19: `useActionState` not `useFormState` | `use()` hook for async | `useFormStatus`
- Tailwind v4: `@theme {}` not `tailwind.config.ts` extend | `bg-linear-to-r` not gradient
- Framer Motion: `useReducedMotion()` on EVERY animation component
- React Bits: TS+TW variant — `https://reactbits.dev/r/ComponentName-TS-TW`
- No raw `<img>` in Next.js — always `next/image`
- No `key={index}` — always `key={item.id}` or stable string
- All `<button>` and icon-only elements have `aria-label`
- `focus-visible:ring-2 ring-primary` on every interactive element

### Step 7 — Lint + heal
```bash
python3 scripts/framework_lint.py [file] --stack-check   # 86 rules, auto-detects all frameworks
python3 scripts/heal.py [file]                           # auto-fix Critical+High
```
Fix ALL 🔴 High immediately. Report 🟡 Medium with specific fixes.

---

## 18-Library Tier System

### Tier 1 — Foundation (always present)
**shadcn/ui** + **Tailwind CSS** — accessible base, keyboard navigation, theming

### Tier 2 — Statement Visual WOW (1-2 per design, chosen by style)
| Library | Best For | When to Use |
|---------|----------|-------------|
| **React Bits** | Hero backgrounds, text animations, scroll effects | Dark premium, editorial, portfolio |
| **Aceternity UI** | Cinematic heroes, 3D cards, editorial reveals | Luxury, gaming, 3D immersive |
| **Magic UI** | SaaS CTAs, border effects, bento grids, marquee | SaaS, minimal, dark premium |
| **Animata** | Cursor delight, liquid effects, number morphing | Y2K, social, portfolio |
| **Motion Primitives** | Morphing dialogs, magnetic, polished transitions | Luxury, editorial, portfolio |
| **Cult UI** | Direction-aware hover, Dynamic Island | Social, Y2K, portfolio |

### Tier 3 — Structural Sections
| Library | Best For |
|---------|----------|
| **Eldora UI** | Complete pre-built landing page sections |
| **MVPBlocks** | Rapid MVP scaffolding |
| **shadcn/ui Blocks** | Dashboard layouts, auth flows |
| **Skiper UI** | Bold navigation, unique hero |

### Tier 4 — Data & Forms
| Library | Best For |
|---------|----------|
| **Tremor** | Charts, KPI metrics, dashboards |
| **Kibo UI** | DateRangePicker, MultiSelect, Kanban |
| **Origin UI** | Production form inputs (OTP, phone, tags) |
| **Flowbite** | Admin panels, table-heavy dashboards |

### Tier 5 — Framework-Specific
| Library | Stack |
|---------|-------|
| **Stunning UI** | Vue/Nuxt only |
| **Chakra UI** | React with theming system |
| **NextUI/HeroUI** | Clean Next.js components |

---

## Intelligence Rules (select_components logic)

The `select_components()` function in `core.py` reads:
1. **Style profile** — each style has specific library arrays (rb, ace, mu, etc.)
2. **Product keywords** — y2k/cyber/dashboard/editorial/portfolio detected, route accordingly
3. **14 slots** — each slot has contextual logic, not hardcoded defaults

**Never suggest Aurora for light backgrounds.** Aurora is dark-only.
**Never repeat the same library for background + hero + sub-text.** Variation is the goal.
**Delight slot is mandatory** — every design gets one unexpected wow element.
**Dashboard/analytics gets Tremor** for charts and KPI slots — not Recharts from scratch.

---

## Reference File READ Triggers

| File | READ When | Contains |
|------|-----------|---------|
| `resources-blogs.md` | **Step 3 always** | 2026 search routing, 8 new library search strategies |
| `inspiration.md` | **Step 5** — design plan | 2026 trends: chrome, direction-aware, morphing dialogs, bento grids |
| `react-bits-catalog.md` | **Step 1** if `has_react_bits` | Full 50+ component catalog with TS+TW install variants |
| `component-library-catalog.md` | **Step 4** | Decision tree for all 18 libraries + new Tremor/Animata/Cult UI sections |
| `page-patterns.md` | **Step 6** | Landing/dashboard/auth/pricing layouts, mobile rules |
| `charts-icons-reference.md` | **Step 6** if dashboard | Chart matrix, Recharts code, Lucide icon table |
| `motion-principles.md` | **Step 6** if animations | Duration table, easing library, library-specific patterns |
| `ux-principles.md` | **Step 5** | 18 UX laws, 7 Gestalt principles |
| `nextjs-guidelines.md` | **Step 6** if Next.js | Next.js 15, React 19, Turbopack, PPR, params→Promise |
| `shadcn-tailwind-guidelines.md` | **Step 6** if shadcn/Tailwind | Dialog/Form/Table, v4 syntax |
| `react-guidelines.md` | **Step 6** if React/Vite | Hooks, cleanup, performance |
| `vue-svelte-guidelines.md` | **Step 6** if Vue/Nuxt/Svelte | Reactivity, pinia, sveltekit |
| `native-guidelines.md` | **Step 6** if SwiftUI/Flutter | Platform conventions |

---

## Quality Gates — Zero Tolerance

```
❌ NEVER (from 86 lint rules — auto-checked by framework_lint.py):

CODE:
  key={index} in .map()                 → always key={item.id}
  <img> in Next.js                      → always next/image
  params.id without await               → Next.js 15 breaking change
  useFormState                          → React 19 renamed to useActionState
  useState in Server Component          → crashes in production
  fetch() without cache option          → Next.js 15 behavior changed
  Server Action without auth check      → security vulnerability
  Aurora on light background            → component is invisible
  3+ statement components per section   → visual chaos
  focus:outline-none without ring       → keyboard users locked out
  animate-* without motion-reduce       → violates accessibility
  Linear easing on discrete UI          → violates motion principles
  duration > 600ms on UI elements       → feels broken/slow
  Hex in className                      → hardcoded, breaks theming
  Aceternity without framer-motion      → runtime crash
  SplashCursor without pointer-events-none → blocks all clicks

DESIGN:
  Emoji as icons                        → broken rendering across OS
  Placeholder text in production code  → unprofessional
  Missing cursor-pointer on clickable  → usability failure
  No focus states                      → WCAG failure
  WCAG AA contrast failure on text     → legal and ethical issue
  Icon button without aria-label       → screen reader failure
  Touch targets < 44px                 → mobile usability failure
  No loading states                    → janky perceived performance
  No error states                      → silent failures confuse users

✅ MUST-HAVE (every design):
  cubic-bezier(0.16,1,0.3,1) entrance easing
  useReducedMotion() on every animation
  focus-visible:ring-2 ring-primary on every interactive element
  min-h-[44px] on every button and link
  AnimatePresence wrapping conditional Framer renders
  All states: default→hover→focus→active→loading→disabled→error→empty
  TS+TW React Bits variant for TypeScript projects
  @theme {} for Tailwind v4 (not tailwind.config.ts extend)
  await params / await searchParams in Next.js 15 pages
```

---

## Motion System (from motion-principles.md)

| Interaction | Duration | Easing |
|-------------|----------|--------|
| Hover color/bg | 150ms | ease-out |
| Tooltip | 150ms | ease-out |
| Dropdown | 200ms | ease-out |
| Badge/state | 250ms | ease-out |
| Modal open | 300ms | spring s:300 d:30 |
| Drawer | 350ms | cubic-bezier(0.16,1,0.3,1) |
| Section entrance | 400ms | cubic-bezier(0.16,1,0.3,1) |
| Hero reveal | 500-600ms | cubic-bezier(0.16,1,0.3,1) |
| Exit | 200ms | cubic-bezier(0.5,0,1,1) |
| Loop/shimmer | 700ms+ | linear ONLY |

**RULE:** NEVER linear for discrete UI. Spring for bouncy elements.  
**RULE:** `useReducedMotion()` check on EVERY Framer Motion component.

---

## Design Philosophy (the 6 principles that separate world-class from good)

1. **One star per section.** The delight slot exists for this reason. Not three wow components — one perfect one.

2. **Whitespace is not empty.** Section padding on award-winning sites is 96-128px. When unsure: double it.

3. **Typography does 80% of the work.** H1 to body ratio of 3:1 minimum. The type scale commitment IS the design.

4. **Motion communicates state, not decoration.** Every animation answers: Did this appear? Did my action succeed? Where did it go? No answer = cut it.

5. **Restraint is harder than maximalism.** Knowing which component NOT to use — Aurora on light bg, three statement pieces stacked — separates senior designers from everyone else.

6. **Accessibility is not a checklist.** 44px targets, visible focus, reduced motion — not box-checking. The design breaks for real people without these.
