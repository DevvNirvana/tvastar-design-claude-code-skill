# React Bits — Complete Component Catalog
Source: https://reactbits.dev | Install via: `npx shadcn@latest add "https://reactbits.dev/r/[ComponentName]"`
All components have 4 variants: JS+CSS, JS+Tailwind, TS+CSS, TS+Tailwind

---

## Install Command Format

```bash
# Standard (TS + Tailwind — use for Next.js + TypeScript projects)
npx shadcn@latest add "https://reactbits.dev/r/[ComponentName]-TS-TW"

# JavaScript + Tailwind
npx shadcn@latest add "https://reactbits.dev/r/[ComponentName]-JS-TW"

# After install, import from your components folder:
import ComponentName from '@/components/ui/ComponentName'
```

---

## TEXT ANIMATIONS

### SplitText
**Use for:** Hero headlines, section titles, statement text
**Effect:** Animates each word or character individually on scroll/mount
**Best moment:** First heading on page, feature section titles
```tsx
import SplitText from '@/components/ui/SplitText'
<SplitText
  text="Build faster, ship smarter"
  className="text-5xl font-heading font-bold"
  delay={100}
  animationFrom={{ opacity: 0, transform: 'translate3d(0,40px,0)' }}
  animationTo={{ opacity: 1, transform: 'translate3d(0,0,0)' }}
  easing="easeOutCubic"
  threshold={0.2}
/>
```
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/SplitText-TS-TW"`

---

### BlurText
**Use for:** Subheadlines, descriptions, secondary headings
**Effect:** Letters blur into focus, creating an elegant reveal
**Best moment:** Paired under a SplitText headline
```tsx
import BlurText from '@/components/ui/BlurText'
<BlurText
  text="The AI-powered recruiting platform"
  delay={200}
  direction="top"
  className="text-xl text-muted"
/>
```
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/BlurText-TS-TW"`

---

### GradientText
**Use for:** Brand names, key terms, pricing numbers, CTAs
**Effect:** Animated gradient applied to text
**Best moment:** Product name in hero, pricing tier name
```tsx
import GradientText from '@/components/ui/GradientText'
<GradientText colors={["#7C3AED", "#EC4899", "#F97316"]} className="text-4xl font-bold">
  Pro Plan
</GradientText>
```
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/GradientText-TS-TW"`

---

### ShinyText
**Use for:** Tags, badges, status indicators, "New" labels
**Effect:** Shimmer passes across text
**Best moment:** "New Feature", "Beta", "Early Access" badges
```tsx
import ShinyText from '@/components/ui/ShinyText'
<ShinyText text="Now in public beta" className="text-sm" speed={3} />
```
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/ShinyText-TS-TW"`

---

### FuzzyText
**Use for:** Bold statements, memorable taglines, hero text
**Effect:** Characters randomize on hover or mount
**Best moment:** Agency/portfolio hero, single statement pages
```tsx
import FuzzyText from '@/components/ui/FuzzyText'
<FuzzyText baseIntensity={0.2} hoverIntensity={0.8} className="text-7xl font-black">
  We build bold
</FuzzyText>
```
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/FuzzyText-TS-TW"`

---

### VariableFontCursor
**Use for:** Portfolio/agency hero sections
**Effect:** Font weight changes based on cursor proximity
**Best moment:** Single large heading on portfolio landing page
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/VariableFontCursor-TS-TW"`

---

### DecryptedText
**Use for:** Terminal/developer aesthetic, reveals, code-like content
**Effect:** Characters "decrypt" from random chars to final text
**Best moment:** Developer tools hero, security product, code highlight
```tsx
import DecryptedText from '@/components/ui/DecryptedText'
<DecryptedText text="ACCESS GRANTED" speed={80} className="text-3xl font-mono" />
```
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/DecryptedText-TS-TW"`

---

### ScrambleText
**Use for:** Tech/AI product text hover effects
**Effect:** Text scrambles through characters on hover before landing
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/ScrambleText-TS-TW"`

---

### TypewriterText  
**Use for:** Loading states, onboarding steps, chat-like interfaces
**Effect:** Types out text character by character
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Typewriter-TS-TW"`

---

### CircularText
**Use for:** Decorative badge elements, rotating labels, "available for work"
**Effect:** Text arranged in a circle, optionally rotating
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/CircularText-TS-TW"`

---

### TextPressure
**Use for:** Interactive hero text, portfolio statement
**Effect:** Variable font weight responds to mouse pressure
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/TextPressure-TS-TW"`

---

### CountUp (Counter)
**Use for:** Statistics sections, KPI dashboards, social proof numbers
**Effect:** Numbers count up from 0 to target
**Best moment:** "10,000+ users", "$2M saved", stat rows
```tsx
import Counter from '@/components/ui/Counter'
<Counter from={0} to={10000} separator="," className="text-5xl font-bold" />
```
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Counter-TS-TW"`

---

### ScrollVelocity
**Use for:** Marquee/ticker sections, logo strips, skill tags
**Effect:** Scrolling text that speeds up/slows based on scroll velocity
**Best moment:** Between sections as a separator, "trusted by" logo strip alternative
```tsx
import ScrollVelocity from '@/components/ui/ScrollVelocity'
<ScrollVelocity velocity={50} className="text-2xl font-bold text-muted">
  React · TypeScript · Next.js · TailwindCSS · Framer Motion ·
</ScrollVelocity>
```
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/ScrollVelocity-TS-TW"`

---

### InfiniteScroll (TextLoop)
**Use for:** Cycling through feature names, use cases, industries
**Effect:** Vertical or horizontal text cycling
**Best moment:** Hero subtitle showing multiple use cases
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/InfiniteScroll-TS-TW"`

---

## ANIMATIONS

### FadeContent
**Use for:** EVERY section entrance — universal, non-distracting
**Effect:** Clean fade + subtle slide up on scroll enter
**Best moment:** Default animation for all sections/cards
```tsx
import FadeContent from '@/components/ui/FadeContent'
<FadeContent blur={true} duration={800} delay={200}>
  <YourContent />
</FadeContent>
```
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/FadeContent-TS-TW"`

---

### BlurIn
**Use for:** Images, screenshots, modals revealing
**Effect:** Element blurs into focus
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/BlurIn-TS-TW"`

---

### GlitchText
**Use for:** Cyberpunk, hacker, gaming aesthetic
**Effect:** Text glitches with color channel separation
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/GlitchText-TS-TW"`

---

### BounceCards
**Use for:** Feature highlights, team members, testimonial cards
**Effect:** Cards stack and bounce into view
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/BounceCards-TS-TW"`

---

### PixelTrail
**Use for:** Interactive hero sections, creative/agency sites
**Effect:** Pixel trail follows cursor
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/PixelTrail-TS-TW"`

---

### StarBorder
**Use for:** Highlighting special cards, pricing recommended tier
**Effect:** Animated star/glitter border around element
**Best moment:** "Most Popular" pricing card border
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/StarBorder-TS-TW"`

---

### MagneticButton
**Use for:** Primary CTA buttons, "Get Started" buttons
**Effect:** Button follows cursor magnetically on hover
**Best moment:** Hero CTA, final CTA section
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/MagneticButton-TS-TW"`

---

### ShimmerButton
**Use for:** Primary CTAs in dark-mode sections
**Effect:** Shimmer light sweeps across button
**Best moment:** Dark hero section primary CTA
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/ShimmerButton-TS-TW"`

---

### RippleButton
**Use for:** Touch-optimized CTAs, mobile-first designs
**Effect:** Ripple effect from click point
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/RippleButton-TS-TW"`

---

### MetaBalls
**Use for:** Liquid/organic decorative accents, creative backgrounds
**Effect:** Liquid blob forms that merge and split
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/MetaBalls-TS-TW"`

---

### ClickSpark
**Use for:** Fun, delightful interactions on any clickable element
**Effect:** Spark particles emit from click point
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/ClickSpark-TS-TW"`

---

### ImageTrail
**Use for:** Portfolio image galleries, team pages, creative project showcases
**Effect:** Images trail behind cursor
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/ImageTrail-TS-TW"`

---

## BACKGROUNDS

### Aurora
**Use for:** Hero sections, full-page backgrounds, CTA sections
**Effect:** Animated colored aurora/northern-lights effect
**Best moment:** THE most impactful React Bits component — use as hero bg
```tsx
import Aurora from '@/components/ui/Aurora'
// As hero background:
<div className="relative min-h-screen overflow-hidden">
  <Aurora
    colorStops={["#7C3AED", "#EC4899", "#3B82F6"]}
    amplitude={1.2}
    blend={0.4}
  />
  <div className="relative z-10">{/* hero content */}</div>
</div>
```
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Aurora-TS-TW"`

---

### Particles
**Use for:** Dark mode hero backgrounds, ambient decoration
**Effect:** Floating particles that connect/disperse
**Best moment:** Dark/tech hero section background
```tsx
import Particles from '@/components/ui/Particles'
<Particles
  quantity={80}
  color="#818CF8"
  className="absolute inset-0"
/>
```
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Particles-TS-TW"`

---

### Meteors
**Use for:** Dark hero sections, cosmic/space/tech aesthetic
**Effect:** Meteor streaks fall across the background
**Best moment:** Dark landing page hero, space/astronomy product
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Meteors-TS-TW"`

---

### Grid
**Use for:** Background texture for dashboards, data products
**Effect:** Subtle grid pattern background
**Best moment:** Dashboard page background, technical/data product bg
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Grid-TS-TW"`

---

### Ripple
**Use for:** CTA section backgrounds, conversion-focused sections
**Effect:** Expanding ripple rings from center
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Ripple-TS-TW"`

---

### Beams
**Use for:** Feature sections, dark backgrounds with depth
**Effect:** Light beams sweep across background
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Beams-TS-TW"`

---

### Silk
**Use for:** Hero backgrounds, auth pages, premium/luxury backgrounds
**Effect:** Flowing silk-like animated gradient
**Best moment:** Auth page split-view left panel, premium product hero
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Silk-TS-TW"`

---

### Orb
**Use for:** Decorative floating accents, CTA sections
**Effect:** Glowing orb/blob that floats
**Best moment:** Float behind a stats number, CTA section accent
```tsx
import Orb from '@/components/ui/Orb'
<div className="relative">
  <Orb size={400} color={["#7C3AED", "#EC4899"]} className="opacity-30" />
  <div className="relative z-10">{/* content */}</div>
</div>
```
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Orb-TS-TW"`

---

### Noise
**Use for:** Background texture overlay, tactile/paper feel
**Effect:** Subtle noise/grain texture overlay
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Noise-TS-TW"`

---

### DotGrid
**Use for:** Technical/developer bg, Notion-like texture
**Effect:** Dot grid pattern, optionally interactive
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/DotGrid-TS-TW"`

---

### WaveBackground
**Use for:** Smooth, flowing section separators, hero backgrounds
**Effect:** Animated wave shapes
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Waves-TS-TW"`

---

### Dither
**Use for:** Artistic/creative retro effect, low-fi aesthetic
**Effect:** WebGL dithering effect applied to background
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Dither-TS-TW"`

---

### MeshGradient
**Use for:** Colorful gradient backgrounds, AI/modern startup
**Effect:** Organic mesh gradient that slowly animates
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/MeshGradient-TS-TW"`

---

## COMPONENTS

### TiltedCard
**Use for:** Feature cards, testimonial cards, product showcases
**Effect:** Card tilts on cursor hover with 3D perspective
**Best moment:** Feature grid, "How it works" step cards
```tsx
import TiltedCard from '@/components/ui/TiltedCard'
<TiltedCard
  imageSrc="/feature-preview.png"
  imageAlt="Feature preview"
  containerHeight="300px"
  containerWidth="100%"
  scaleOnHover={1.05}
  rotateAmplitude={14}
  displayOverlayContent
  overlayContent={<FeatureInfo />}
/>
```
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/TiltedCard-TS-TW"`

---

### SpotlightCard
**Use for:** Feature highlights, pricing cards, premium item showcases
**Effect:** Spotlight follows cursor across card, illuminating surface
**Best moment:** Pricing cards, integration cards, "Why us" cards
```tsx
import SpotlightCard from '@/components/ui/SpotlightCard'
<SpotlightCard className="rounded-2xl border bg-surface p-8" spotlightColor="rgba(124,58,237,0.15)">
  <FeatureContent />
</SpotlightCard>
```
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/SpotlightCard-TS-TW"`

---

### Stack (Card Stack)
**Use for:** Portfolio items, testimonial stack, image galleries
**Effect:** Cards stacked with draggable/interactive physics
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Stack-TS-TW"`

---

### ScrollStack
**Use for:** Feature showcases, "How it works" steps on scroll
**Effect:** Cards pin and stack as user scrolls
**Best moment:** "3 simple steps" section with cinematic feel
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/ScrollStack-TS-TW"`

---

### Masonry
**Use for:** Image galleries, portfolio grids, testimonial walls
**Effect:** Responsive masonry grid with GSAP entrance animations
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Masonry-TS-TW"`

---

### FlowingMenu
**Use for:** Fullscreen navigation overlays, creative menus
**Effect:** Menu items flow with ripple background on hover
**Best moment:** Hamburger menu on creative/agency sites
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/FlowingMenu-TS-TW"`

---

### GooeyNav
**Use for:** Navigation between pages, tab-style navigation
**Effect:** Gooey/liquid transition between nav items
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/GooeyNav-TS-TW"`

---

### StaggeredMenu
**Use for:** Mobile navigation, side drawers
**Effect:** Menu items stagger in with delay
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/StaggeredDropdown-TS-TW"`

---

### Dock
**Use for:** macOS-style tool bars, quick action menus
**Effect:** Magnifying effect like macOS Dock
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Dock-TS-TW"`

---

### GlassIcons
**Use for:** Feature icon lists, integration logos
**Effect:** Glass-morphism icon containers
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/GlassIcons-TS-TW"`

---

### Lanyard
**Use for:** Interactive "about" sections, team cards, fun hero accents
**Effect:** 3D physics-based lanyard/badge that user can grab and swing
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Lanyard-TS-TW"`

---

### PixelCard
**Use for:** Product/feature cards with unique interactive feel
**Effect:** Canvas-based pixel shimmer on hover
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/PixelCard-TS-TW"`

---

### CardSwap
**Use for:** Feature/testimonial carousels, before/after comparisons
**Effect:** Cards swap with smooth 3D flip
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/CardSwap-TS-TW"`

---

### Ribbon
**Use for:** "Featured", "New", "Best Value" corner badges on cards
**Effect:** Folded ribbon in card corner
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Ribbon-TS-TW"`

---

### Ballpit
**Use for:** Whimsical/fun empty states, loading screens, brand moments
**Effect:** Physics-based colored balls bouncing in a container
**Install:** `npx shadcn@latest add "https://reactbits.dev/r/Ballpit-TS-TW"`

---

## COMPONENT SELECTION GUIDE

### By page section:

| Section | React Bits choice |
|---------|------------------|
| Hero headline | `SplitText` (primary) or `BlurText` |
| Hero background | `Aurora` (colorful) · `Silk` (premium) · `Particles` (dark/tech) |
| Hero CTA button | `MagneticButton` or `ShimmerButton` |
| Social proof stat | `Counter` (for numbers) |
| Logo strip / marquee | `ScrollVelocity` |
| Feature cards | `SpotlightCard` · `TiltedCard` |
| Feature grid background | `Grid` or `DotGrid` |
| Testimonials | `BounceCards` · `CardSwap` · `Masonry` |
| Pricing recommended | `StarBorder` on the card |
| CTA section | `Orb` or `Ripple` as background |
| Navigation | `FlowingMenu` (fullscreen) · `GooeyNav` (tab-style) |
| Stats section | `Counter` + `FadeContent` |
| Loading / empty state | `Ballpit` |
| Portfolio/agency hero | `FuzzyText` · `VariableFontCursor` · `ImageTrail` |
| Dark tech hero | `Meteors` · `Beams` |
| Auth page | `Silk` (left panel) |
| Any section entrance | `FadeContent` (universal) |

### By design style:

| Style | Primary React Bits |
|-------|--------------------|
| Clean Minimal | `FadeContent` · `SplitText` · `Counter` |
| Dark Premium | `Aurora` · `Particles` · `ShimmerButton` · `SpotlightCard` |
| Aurora Gradient | `Aurora` · `MeshGradient` · `GradientText` |
| Editorial | `ScrollVelocity` · `BlurText` · `FuzzyText` |
| Typography First | `SplitText` · `VariableFontCursor` · `ScrollVelocity` |
| 3D Interactive | `TiltedCard` · `Lanyard` · `Ballpit` |
| Glassmorphism | `Aurora` (bg) · `SpotlightCard` · `GlassIcons` |
| Neubrutalism | `BounceCards` · `FuzzyText` |

---

## Rules for React Bits Usage

1. **One statement piece per section** — not three. Use `FadeContent` for everything else.
2. **Aurora or Particles for hero backgrounds only** — not repeated on every section.
3. **Counter for all numeric social proof** — never static numbers next to a "trusted by" claim.
4. **SpotlightCard is the default feature card** — elegant, works in any color scheme.
5. **MagneticButton only for primary CTAs** — gives it deserved weight (Von Restorff).
6. **SplitText on the page's single most important headline** — not every heading.
7. **ScrollVelocity between major sections** — good visual separator, shows momentum.
8. **Always wrap with FadeContent** — even React Bits components benefit from an entrance fade.
