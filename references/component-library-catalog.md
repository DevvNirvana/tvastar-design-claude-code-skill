# Component Library Catalog v2.0
Master reference for all 12+ UI libraries.

---

## Library Decision Tree — Which Library for What?

HERO SECTION:
  Dark premium  → React Bits: Aurora + SplitText + MagneticButton
  Cinematic dark → Aceternity: LampEffect + TextGenerateEffect
  Light SaaS    → Magic UI: GridPattern + WordPullUp + ShimmerButton
  Editorial     → React Bits: Silk + BlurText

FEATURE CARDS:
  Dark bg   → React Bits: SpotlightCard   wow:9
  Light bg  → Magic UI: MagicCard         wow:9
  3D wow    → Aceternity: ThreeDCardEffect wow:9
  Simple    → shadcn: Card

CTA BUTTON (most important element — use ONE per section):
  Dark premium → Magic UI: ShimmerButton      wow:9
  Bold/brand   → Magic UI: RainbowButton      wow:9
  Magnetic     → React Bits: MagneticButton   wow:9
  Standard     → shadcn: Button (primary)

TEXT EFFECTS:
  Hero H1 stagger  → React Bits: SplitText         wow:9
  Sub-headline     → React Bits: BlurText           wow:9
  Tech typewriter  → Magic UI: HyperText            wow:9
  Scroll reveal    → Aceternity: TextGenerateEffect wow:9
  Stats numbers    → Magic UI: NumberTicker         wow:8
  Marquee          → Magic UI: MarqueeComponent

BACKGROUNDS:
  Dark aurora  → React Bits: Aurora          (dark only!)
  Dark beams   → Aceternity: BackgroundBeams
  Grid (light) → Magic UI: GridPattern
  Dots (light) → Magic UI: DotPattern
  Retro grid   → Magic UI: RetroGrid

NAVIGATION:
  Desktop sticky   → Aceternity: FloatingNavbar
  Mobile menu      → React Bits: FlowingMenu   wow:10
  App sidebar      → shadcn: Sidebar
  Scroll highlight → Aceternity: StickyScrollReveal

FORMS / INPUTS → Origin UI (16+ variants) + shadcn (structure)
ADVANCED COMPONENTS → Kibo UI (kanban, date range, file upload)
VUE/NUXT projects → Stunning UI (Vue-native equivalents)

---

## React Bits Install Commands
Install: npx shadcn@latest add "https://reactbits.dev/r/[ComponentName]"
Requires: Tailwind CSS (some: framer-motion)

BACKGROUNDS:
  Aurora         → dark-only multi-hue animated aurora                WOW:10
  Particles      → interactive particle field                         WOW:8
  Silk           → flowing silk fluid simulation                      WOW:9
  Orb            → glowing ambient orb                                WOW:7
  Ripple         → expanding concentric rings                         WOW:7
  DotGrid        → animated dot matrix                                WOW:6
  Ballpit        → physics bouncing balls                             WOW:8
  Balatro        → card swirl shader                                  WOW:9

TEXT:
  SplitText      → staggered char/word entrance                       WOW:9
  BlurText       → blur-to-sharp word reveal                          WOW:9
  ShinyText      → moving shimmer highlight                           WOW:7
  GradientText   → animated color sweep                               WOW:8
  FuzzyText      → glitch distortion on hover                         WOW:8
  CountUp        → number count from 0 to target                      WOW:8
  TextReveal     → words reveal on scroll position                    WOW:8
  ScrollVelocity → marquee speed matches scroll                       WOW:8
  CircularText   → text arranged in circle                            WOW:7

CARDS:
  SpotlightCard  → mouse-tracking spotlight glow on card              WOW:9
  TiltedCard     → 3D perspective tilt tracking mouse                 WOW:8
  BounceCards    → spring-physics card stack                          WOW:9
  ScrollStack    → cards expand as you scroll                         WOW:9
  StackedCards   → fan-out on hover                                   WOW:8

BUTTONS & EFFECTS:
  MagneticButton → button pulled magnetically toward cursor           WOW:9
  StarBorder     → rotating star shimmer border                       WOW:8
  FadeContent    → clean fade+slide on scroll enter                   WOW:6
  AnimatedList   → staggered list item entrance                       WOW:7
  ImageTrail     → images follow cursor in trail                      WOW:10
  InfiniteScroll → seamlessly looping list                            WOW:7

NAVIGATION:
  FlowingMenu    → full-screen menu, flowing text animation           WOW:10
  DockExpandable → macOS dock with magnification                      WOW:8

---

## Aceternity UI Install
Setup: npm install framer-motion clsx tailwind-merge
       Ensure cn() at @/lib/utils.ts
Copy from: https://ui.aceternity.com/components/[slug]

HERO/ATMOSPHERE:
  lamp                              → LampEffect                WOW:10
  spotlight                         → Spotlight                 WOW:9
  aurora-background                 → AuroraBackground          WOW:8
  background-beams                  → BackgroundBeams           WOW:9
  background-beams-with-collision   → BeamsWithCollision        WOW:10
  vortex                            → Vortex                    WOW:9
  shooting-stars                    → ShootingStars             WOW:8
  meteors                           → Meteors                   WOW:8
  macbook-scroll                    → MacbookScroll             WOW:10
  hero-parallax                     → HeroParallax              WOW:10
  google-gemini-effect              → GoogleGeminiEffect        WOW:10

CARDS:
  3d-card-effect                    → ThreeDCardEffect          WOW:9
  card-spotlight                    → CardSpotlight             WOW:9
  card-stack                        → CardStack                 WOW:8
  focus-cards                       → FocusCards                WOW:9
  text-reveal-card                  → TextRevealCard            WOW:9
  moving-border                     → MovingBorder              WOW:9
  expanding-card                    → ExpandingCard             WOW:8

TEXT:
  text-generate-effect              → TextGenerateEffect        WOW:9
  typewriter-effect                 → TypewriterEffect          WOW:7
  flip-words                        → FlipWords                 WOW:8
  hero-highlight                    → HeroHighlight             WOW:8
  colourful-text                    → ColourfulText             WOW:8

NAVIGATION:
  floating-navbar                   → FloatingNavbar            WOW:9
  sticky-scroll-reveal              → StickyScrollReveal        WOW:9

---

## Magic UI Install
CLI: npx magicui-cli@latest add [name]
Requires: framer-motion

BUTTONS:
  shimmer-button                → ShimmerButton dark CTA       WOW:9
  rainbow-button                → RainbowButton bold CTA       WOW:9
  interactive-hover-button      → arrow slides in              WOW:8
  pulsating-button              → radiate pulse ring           WOW:7
  cool-mode                     → confetti on click            WOW:9

TEXT:
  number-ticker                 → NumberTicker stats           WOW:8
  word-pull-up                  → words spring up              WOW:8
  word-fade-in                  → staggered fade               WOW:7
  hyper-text                    → Matrix scramble              WOW:9
  sparkles-text                 → sparkles around text         WOW:9
  animated-gradient-text        → gradient sweep               WOW:8
  box-reveal                    → box wipe reveal              WOW:8
  gradual-spacing               → letters spread apart         WOW:8

BACKGROUNDS:
  grid-pattern                  → subtle grid lines            WOW:6
  dot-pattern                   → dot matrix                   WOW:6
  animated-grid-pattern         → highlighted cells            WOW:8
  retro-grid                    → perspective vanishing grid   WOW:9
  flickering-grid               → flicker on/off cells         WOW:8
  ripple                        → concentric rings             WOW:7

BORDERS:
  border-beam                   → beam travels around border   WOW:9
  animated-beam                 → beam along SVG path          WOW:10
  shine-border                  → metallic shine               WOW:8
  magic-card                    → radial glow follows mouse    WOW:9
  neon-gradient-card            → neon animated border         WOW:9

LAYOUT:
  marquee                       → infinite logo strip          WOW:7
  bento-grid                    → feature grid layout          WOW:8
  orbiting-circles              → icons orbit center           WOW:9
  dock                          → macOS icon dock              WOW:8

---

## Origin UI
Copy from: https://originui.com
Input variants: floating-label, icon-prefix, icon-suffix, character-count,
show-hide-toggle, inline-validation, OTP (6-box), phone (flag+format),
tags (chips+autocomplete), combo (select+input)

---

## Kibo UI
CLI: npx kiui@latest add [component]
Requires: shadcn/ui

  multi-select        → checkboxes + search in select
  date-range-picker   → two-calendar range selector
  kanban              → drag-drop board
  file-upload         → drag-drop with preview
  rich-text-editor    → WYSIWYG
  color-picker        → HSV picker
  tag-input           → autocomplete tagging
  timeline            → vertical timeline

---

## Stunning UI (Vue/Nuxt only)
Copy from: https://stunning-ui.com
Requires: Vue 3, Tailwind CSS

  AnimatedGradient  ≈ React Bits: Aurora
  MagneticButton    ≈ React Bits: MagneticButton
  GlowCard          ≈ React Bits: SpotlightCard
  TextScramble      ≈ React Bits: FuzzyText
  StaggerList       ≈ React Bits: AnimatedList
  ParticleField     ≈ React Bits: Particles

---


---

## Tremor (Dashboards & Data Viz)
Install: `npm install @tremor/react`
Requires: React, Tailwind CSS
Best for: Any project with metrics, charts, or data

CHARTS:
  AreaChart        → trend over time, smooth curves          WOW:7
  BarChart         → compare categories                      WOW:7
  LineChart        → multi-series comparison                 WOW:7
  DonutChart       → part-to-whole (≤6 categories)          WOW:7
  BarList          → horizontal ranked list                  WOW:8
  Tracker          → binary uptime/status tracker            WOW:8
  ScatterChart     → correlation between variables           WOW:7

METRICS:
  Metric           → large KPI number + delta + trend        WOW:7
  BadgeDelta       → colored up/down/neutral badge           WOW:7
  ProgressBar      → percentage completion bar               WOW:6
  ProgressCircle   → circular progress indicator             WOW:7

DECISION: Default chart library for any dashboard. Replaces raw Recharts setup.

---

## Animata (Micro-interactions & WOW Effects)
Copy from: https://animata.design
Requires: Tailwind CSS, framer-motion

CURSOR / ATMOSPHERE:
  SplashCursor     → fluid simulation cursor trail           WOW:10
  LiquidChrome     → liquid mercury animation                WOW:10
  MetaBalls        → blob merging metaballs                  WOW:9
  FollowCursor     → element follows cursor                  WOW:9

TEXT:
  NumberFlow       → smooth morphing number transitions      WOW:9
  RotatingText     → 3D rotating word transitions            WOW:8
  WavyText         → characters wave on mount                WOW:8
  FadeInText       → sequential character fade               WOW:7

DECISION: Use for the ONE delight moment per page that nobody expects.

---

## Motion Primitives (Polished Framer Transitions)
Copy from: https://motion-primitives.com
Requires: framer-motion, Tailwind CSS

INTERACTIONS:
  MorphingDialog   → dialog morphs from its trigger element  WOW:10
  Cursor           → custom cursor with magnetic pull        WOW:9
  Magnetic         → magnetic pull effect on any element     WOW:9
  Tilt             → 3D tilt with spring physics             WOW:8
  InfiniteSlider   → smooth infinite carousel                WOW:8

TEXT:
  TextEffect       → character-by-character physics reveals  WOW:9
  TextShimmer      → shimmer sweep on text                   WOW:8
  AnimatedNumber   → smooth morphing between numbers         WOW:9
  GlitchText       → glitch/corruption text effect           WOW:8

DECISION: When Framer Motion alone feels too raw but Aceternity is too heavy.

---

## Cult UI (Unique High-Impact Components)
Copy from: https://www.cult-ui.com
Requires: framer-motion, Tailwind CSS

SPECIAL:
  DirectionAwareHover → card reveals image from cursor direction  WOW:9
  DynamicIsland       → Apple Dynamic Island component            WOW:10
  Carousel3D          → 3D perspective carousel                   WOW:9
  FamilyButton        → spring-expand button group                WOW:9
  ExpandableCard      → card expands to full content              WOW:8
  DialogStack         → stacked dialogs with depth                WOW:9

DECISION: Use for the single most interactive card on the page. One per design.

---

## Eldora UI (Landing Page Section Blocks)
Copy from: https://www.eldoraui.site
Requires: framer-motion, Tailwind CSS

SECTIONS:
  HeroGeometric    → rotating geometric shapes hero           WOW:9
  TestimonialsMarquee → two-row infinite testimonial strip    WOW:8
  FeaturesBento    → bento grid features section              WOW:8
  PricingCards     → animated pricing with hover effects      WOW:8
  LogoCloud        → animated logo grid                       WOW:7
  TimelineScroll   → scroll-triggered timeline                WOW:8

DECISION: Use when you need a battle-tested complete section block.

---

## Library Decision Matrix (Updated March 2026)

| Need | Best Library | Runner-Up |
|------|-------------|-----------|
| Dashboard charts | Tremor | Recharts (shadcn chart wrapper) |
| KPI metrics | Tremor Metric | Magic UI NumberTicker |
| Cursor delight | Animata SplashCursor | Motion Primitives Cursor |
| Number morphing | Animata NumberFlow | Motion Primitives AnimatedNumber |
| Dialog wow | Motion Primitives MorphingDialog | Cult UI DialogStack |
| Card wow interaction | Cult UI DirectionAwareHover | React Bits SpotlightCard |
| Dynamic Island | Cult UI DynamicIsland | custom |
| Complete section | Eldora UI | MVPBlocks |
| Enterprise forms | Kibo UI | Origin UI |
| Advanced inputs | Origin UI | shadcn/ui |

## Critical Anti-Patterns

  Aurora on white bg       → invisible, dark-only component
  Aceternity without FM    → hard crash
  ShimmerButton light bg   → washed out, use RainbowButton instead
  3+ statement pieces/sec  → chaos, they cancel each other
  Flowbite for landing     → admin-panel look, wrong context
  MUI + shadcn together    → conflicts, huge bundle
  key={index} in .map()    → breaks animations + React reconciliation
  No AnimatePresence       → Framer exit animations never play
