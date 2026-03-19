# Page Patterns Reference
Proven layouts from Awwwards, Lapa.ninja, SiteInspire, and Dribbble research.
Each pattern is a battle-tested conversion or UX structure.

---

## LANDING PAGES

### Pattern 1: Hero-Centric SaaS (Most Common, Highest Conversion)
**Best for:** SaaS, tools, productivity apps, B2B
**Awwwards inspiration:** Linear.app, Vercel, Supabase, Raycast

```
[STICKY NAVIGATION]  logo · links · CTA button (Von Restorff: only colored element in nav)

[HERO — Full viewport]
  ┌─────────────────────────────────────────────┐
  │  [Announcement pill] "New: AI features →"   │  ← ShinyText / pill badge
  │                                             │
  │  H1: Bold 56px headline (SplitText)         │  ← Primary value proposition
  │  Subhead: 18px description (BlurText)       │  ← What it does for who
  │                                             │
  │  [CTA Primary] [CTA Secondary]              │  ← MagneticButton (primary only)
  │                                             │
  │  "Join 10,000+ teams" + avatar stack        │  ← Counter + social proof
  │                                             │
  │  Product screenshot/mockup (3D tilt)        │  ← TiltedCard
  └─────────────────────────────────────────────┘
  BACKGROUND: Aurora or Particles (dark) or subtle gradient

[LOGO STRIP]  "Trusted by teams at..."  [ScrollVelocity logos]

[PROBLEM → SOLUTION]
  "Before" pain points (3 columns, red/warning icons)
  → Arrow or visual transition →
  "After" benefits (3 columns, green/checkmark icons)

[FEATURES]  (FadeContent entrance on scroll)
  Large feature demo on left | Feature list on right (alternating)
  OR
  Feature grid: 3 columns × 2 rows, SpotlightCard for each

[SOCIAL PROOF]
  Stats row: [Counter 10,000+] [Counter $2M] [Counter 99.9%]
  Testimonials: BounceCards or Masonry grid

[PRICING]  (See Pricing Pattern)

[FINAL CTA SECTION]
  Full-width section with Orb/Ripple background
  "Ready to [benefit]?" + big CTA

[FOOTER]
```

---

### Pattern 2: Visual-First Landing (Creative/Agency/Consumer)
**Best for:** Creative agencies, consumer apps, visual products
**Awwwards inspiration:** Dribbble, Craft, Lottiefiles

```
[HERO — Fullscreen, edge-to-edge]
  Background: Silk or Aurora (full viewport)
  Text minimal and large over background
  One CTA, centered

[SCROLL → next sections reveal cinematic ally]
  ScrollStack for "how it works" sections
  Each section full viewport height

[Gallery] Masonry or ImageTrail interaction

[About/Philosophy] Editorial layout, large serif type (Fraunces)

[CTA] Understated, confident
```

---

### Pattern 3: Conversion-Maximized Landing (E-Commerce / SaaS Trial)
**Best for:** Free trial, product launch, App Store redirect
**Lapa.ninja reference:** Shopify Landing, Duolingo Plus

```
Above fold MUST have:
  1. Product name + what it does (7 words max)
  2. ONE primary CTA with micro-copy below ("No credit card · Cancel anytime")
  3. Social proof number ("4.8★ rated by 50,000 users")
  4. Product screenshot or 15s demo video

Key conversion elements:
  - CTA repeated every 2-3 sections (not just hero)
  - Objection-busting section ("Is it secure? Is it worth it?")
  - Guarantee/risk-reversal (money back, free tier, etc.)
  - Urgency/scarcity if real (not fake)
```

---

## DASHBOARDS

### Pattern 1: Analytics Dashboard
**Best for:** Data products, reporting tools, admin panels

```
[SIDEBAR — fixed, 240px wide]
  Logo
  Primary navigation (max 7 items)
  Active state: bg-primary/10 + primary text color + left accent border
  User avatar + name at bottom

[TOP BAR — sticky]
  Page title + breadcrumb
  Search
  Notifications icon + count badge
  User avatar dropdown

[MAIN CONTENT AREA]
  ┌──────────────────────────────────────────┐
  │  Page header + date range picker + filter│
  ├──────┬──────┬──────┬──────────────────────┤
  │ KPI  │ KPI  │ KPI  │ KPI (Counter anim)  │  ← 4 stat cards
  ├──────┴──────┴──────┴──────────────────────┤
  │  PRIMARY CHART  (full width or 2/3)       │  ← Line/area chart
  ├───────────────────────┬───────────────────┤
  │  TABLE with filters   │  Secondary chart  │
  └───────────────────────┴───────────────────┘

Spacing: 24px between sections, 16px between elements in sections
```

**Tailwind layout:**
```tsx
<div className="flex h-screen overflow-hidden bg-bg">
  <Sidebar />  {/* w-60 flex-shrink-0 */}
  <div className="flex flex-1 flex-col overflow-hidden">
    <TopBar />  {/* h-16 flex-shrink-0 border-b */}
    <main className="flex-1 overflow-y-auto p-6">
      <StatsRow />
      <div className="mt-6 grid grid-cols-3 gap-6">
        <MainChart className="col-span-2" />
        <SecondaryChart />
      </div>
      <DataTable className="mt-6" />
    </main>
  </div>
</div>
```

---

### Pattern 2: App Dashboard (User-Facing Product)
**Best for:** SaaS product main view, user home screen

```
[TOP NAV — horizontal]  (no sidebar needed for simple products)
  Logo · Navigation · Search · User menu

[PAGE BODY — max-w-7xl centered]
  Welcome message + quick actions
  Content area: varies by product
  Activity feed or recent items
```

---

## AUTHENTICATION PAGES

### Pattern 1: Split Screen (Recommended for Marketing Value)
```
┌─────────────────────────┬─────────────────────────┐
│                         │                         │
│  BRAND SIDE (50%)       │  FORM SIDE (50%)         │
│                         │                         │
│  Background: Silk /     │  Logo                   │
│  Aurora / Image         │  "Welcome back"         │
│                         │                         │
│  Brand tagline          │  [Social Auth Buttons]  │
│  Value proposition      │  ─── or ───             │
│  1-2 testimonial quotes │  Email input            │
│                         │  Password input         │
│                         │  Forgot password link   │
│                         │  [Sign In] button       │
│                         │  "No account? Sign up"  │
│                         │                         │
└─────────────────────────┴─────────────────────────┘
```

**Rules:**
- Social auth (Google, GitHub) ALWAYS above email form — reduces friction
- Divider "or continue with email" below social buttons
- Single field per line — never side-by-side on auth
- Password strength indicator on sign-up only
- Auto-focus first field on mount

---

### Pattern 2: Centered Card (Minimal, Clean)
```
[Full page background: gradient or subtle bg-surface]
  ┌──────────────────────────┐
  │  Logo (centered)         │
  │  "Sign in to Product"    │
  │                          │
  │  [Google] [GitHub]       │
  │  ────── or ──────        │
  │  [Email input]           │
  │  [Password input]        │
  │  [Sign In button]        │
  │                          │
  │  "Don't have an account? │
  │   Sign up"               │
  └──────────────────────────┘
```

---

## PRICING PAGES

### The 3-Tier Pricing Pattern
```
[Section header]  "Simple, transparent pricing"
                  Toggle: [Monthly] [Annual (save 20%)]

[3 Pricing Cards]
  ┌──────────┬──────────────────┬──────────┐
  │  Starter │  Pro ★★★        │  Ent.    │
  │          │  (elevated card) │          │
  │  $0/mo   │  $49/mo         │  Custom  │
  │          │                  │          │
  │  Feature │  Feature        │  Feature │
  │  Feature │  Feature        │  Feature │
  │  Feature │  Feature        │  Feature │
  │          │  Feature [+4]   │  Feature │
  │  [Start] │  [Get Pro]      │  [Talk]  │
  └──────────┴──────────────────┴──────────┘
         ↑
  StarBorder on Pro card + "Most Popular" badge
  Pro card: `ring-2 ring-primary shadow-xl scale-105`

[Feature comparison table]  (toggle: show/hide)

[FAQ Accordion]  Top 5 pricing objections answered

[Final CTA]  "Start for free, upgrade when you're ready"
```

---

## FEATURE DETAIL PAGES

```
[HERO — specific feature]
  Feature name + icon
  "What if you could [key benefit]?"  ← Problem framing
  Screenshot/video of feature in action

[HOW IT WORKS]
  3 numbered steps (ScrollStack or horizontal row)
  Step 1: Setup (< 5 min) · Step 2: Configure · Step 3: Results

[SPECIFIC BENEFITS]
  3 benefits specific to this feature (not generic)
  Real customer quote related to this feature

[TECHNICAL SPECS]  (if needed — developer tools, API, etc.)

[RELATED FEATURES]  3 feature cards leading to other pages

[CTA]  Specific: "Try [Feature Name] free for 14 days"
```

---

## EMPTY STATES

**The 4 components of a great empty state:**
1. **Illustration or icon** — friendly, not generic
2. **Headline** — what's missing and why this is a good thing to set up
3. **Subtext** — one clear sentence about what to do
4. **Primary action** — specific, not generic ("Connect your first account" not "Get started")

**Examples of good empty states:**
- GitHub: "This repository is empty — Push your first commit"
- Linear: "No issues · Create your first issue to track work"
- Notion: "Start writing, or press / for commands"

**React Bits for empty states:**
```tsx
<FadeContent>
  <div className="flex flex-col items-center py-24 text-center">
    <Orb size={200} className="opacity-20 mb-8" />
    <h3 className="font-heading text-xl font-semibold">No matches found</h3>
    <p className="text-muted mt-2 max-w-sm">Try adjusting your filters or search terms</p>
    <button className="btn-primary mt-6">Clear filters</button>
  </div>
</FadeContent>
```

---

## MOBILE-FIRST DESIGN RULES

### Breakpoint strategy:
```
Default (mobile): 375px — single column, large touch targets
sm: 640px  — still mobile-focused
md: 768px  — tablet, 2 columns start
lg: 1024px — desktop begins, sidebar appears
xl: 1280px — wide desktop
2xl: 1536px — cap max-width, center content
```

### Mobile-specific patterns:
- Bottom navigation for 4-5 primary actions (not sidebar)
- Sticky CTA bar at bottom for conversion pages
- Hamburger → full-screen menu (FlowingMenu)
- Cards stack to single column, reduce padding to 16px
- Hero text drops to 36-40px max on mobile (not 72px)
- No hover-only interactions — always have a tap/focus equivalent

```tsx
{/* Mobile-first responsive example */}
<section className="
  px-4 py-16           /* mobile */
  md:px-8 md:py-24    /* tablet */
  lg:px-16 lg:py-32  /* desktop */
">
  <div className="
    grid grid-cols-1 gap-6
    md:grid-cols-2
    lg:grid-cols-3
  ">
    {features.map(f => <FeatureCard key={f.id} {...f} />)}
  </div>
</section>
```
