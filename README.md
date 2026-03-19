<div align="center">

<img src="https://img.shields.io/badge/version-4.0-6366F1?style=for-the-badge&labelColor=09090B" />
<img src="https://img.shields.io/badge/tests-164%20passing-22C55E?style=for-the-badge&labelColor=09090B" />
<img src="https://img.shields.io/badge/libraries-18-A78BFA?style=for-the-badge&labelColor=09090B" />
<img src="https://img.shields.io/badge/styles-24-EC4899?style=for-the-badge&labelColor=09090B" />
<img src="https://img.shields.io/badge/lint_rules-86-F59E0B?style=for-the-badge&labelColor=09090B" />
<img src="https://img.shields.io/github/stars/yourusername/tvastar?style=for-the-badge&labelColor=09090B&color=F59E0B" />

<br/><br/>

# 𝕿𝖛𝖆𝖘𝖙𝖆𝖗

### The World's Most Intelligent Frontend Design Skill for Claude Code

*Named after the Vedic divine craftsman — builder of tools for the gods*

<br/>

**Type `/design landing page for a SaaS product` and watch Tvastar:**  
run color science · pick from 18 libraries · apply Disney motion principles  
validate WCAG · generate production code · lint 86 rules · wait for your approval

<br/>

[**Install in 30 seconds →**](#installation) · [Commands](#commands) · [Libraries](#18-component-libraries) · [Examples](#examples)

</div>

---

## The Problem with AI-Generated UI

Every AI tool produces the same design: Inter font, indigo gradient, three rounded cards, no cursor effects, Aurora everywhere regardless of context. It looks like AI made it because it did — the same defaults for every project.

Tvastar is different. It reads your actual stack, checks contrast ratios, picks different components for a Y2K social app vs a fintech dashboard vs a luxury editorial, and produces code that passes real accessibility audits. It knows that `params` is a Promise in Next.js 15. It knows Aurora doesn't work on light backgrounds. It knows the difference between `ease-out` and `linear` matters.

> *"The gap between what AI produces and what wins awards is one thing: design intelligence. Tvastar is that layer."*

---

## Installation

### One command

```bash
# Clone
git clone https://github.com/yourusername/tvastar.git
cd tvastar

# Install
bash install.sh
```

### Manual

```bash
# Create skills directory
mkdir -p ~/.claude/skills

# Copy skill
cp -r ui-design-intelligence/ ~/.claude/skills/

# Verify
python3 ~/.claude/skills/ui-design-intelligence/scripts/test_all.py
```

### Windows

```powershell
# Set encoding first (required for Unicode output)
$env:PYTHONIOENCODING = "utf-8"

# Then install normally — the install.sh works in Git Bash / WSL
bash install.sh
```

**Requirements:** Python 3.10+ · Claude Code (any version)  
No npm install required. No config files. Works immediately.

---

## Usage

Open Claude Code in your project directory. That's the entire setup.

```bash
# Basic — Tvastar reads your stack and does the rest
/design landing page for a SaaS product

# Specific aesthetic
/design Y2K social media platform

# With page type
/design fintech analytics dashboard

# Targeted commands
/review HeroSection.tsx
/ship
/component PricingCard
/a11y src/components/
```

The `/design` command detects your stack automatically — Tailwind version, which libraries are installed, your existing color tokens — and builds around what you already have.

---

## What happens when you type `/design`

```
1. Stack scan         → Detects Next.js 15, Tailwind v4, React Bits ✓, Magic UI ✗
2. Research           → Searches godly.website + dribbble for your aesthetic
3. Design system      → Generates palette (WCAG checked) + typography + motion tokens
4. Component slots    → Maps 14 slots to the right library from 18 options
5. Design plan        → Shows everything. Waits for your approval.
6. Code generation    → globals.css → tailwind.config → component code
7. Lint + heal        → Runs 86 rules. Auto-fixes Critical issues.
```

You approve the design plan before a single line of code is written.

---

## 18 Component Libraries

Tvastar knows when to use each one. Not just "react-bits or aceternity" — the right component from the right library for each of 14 slots.

### Tier 1 — Foundation
| Library | Best For |
|---------|----------|
| **shadcn/ui** | Accessible base, forms, dialogs, navigation |
| **Tailwind CSS** | Utility styling, design tokens |

### Tier 2 — Visual WOW (1-2 per design)
| Library | Signature Components | When |
|---------|---------------------|------|
| **React Bits** | Aurora, SplitText, ImageTrail, FlowingMenu | Dark premium, portfolio, editorial |
| **Aceternity UI** | LampEffect, BeamsWithCollision, HeroParallax | Cinematic dark, 3D, luxury |
| **Magic UI** | ShimmerButton, RetroGrid, BentoGrid, HyperText | SaaS, Y2K, minimal |
| **Animata** | SplashCursor, LiquidChrome, NumberFlow | Y2K, social, cursor delight |
| **Motion Primitives** | MorphingDialog, Magnetic, GlitchText | Editorial, portfolio, luxury |
| **Cult UI** | DirectionAwareHover, DynamicIsland | Social, gaming, portfolio |

### Tier 3 — Section Blocks
| Library | Best For |
|---------|----------|
| **Eldora UI** | Complete pre-built landing sections |
| **MVPBlocks** | Rapid MVP scaffolding |
| **shadcn/ui Blocks** | Dashboard layouts, auth flows |

### Tier 4 — Data & Forms
| Library | Best For |
|---------|----------|
| **Tremor** | Dashboard charts, KPI metrics (auto-selected) |
| **Kibo UI** | DateRangePicker, MultiSelect, Kanban |
| **Origin UI** | OTP input, phone input, tags input |
| **Flowbite** | Admin panels, data tables |

### Tier 5 — Framework-Specific
| Library | Stack |
|---------|-------|
| **Stunning UI** | Vue/Nuxt only |
| **Chakra UI** | React with theming |
| **NextUI/HeroUI** | Next.js clean components |

---

## 24 Design Style Profiles

Each style has its own component lists, anti-patterns, and selection logic. Tvastar produces completely different output for each:

| Style | Signature Components |
|-------|---------------------|
| Dark Aurora Premium | Aceternity BeamsWithCollision · React Bits SpotlightCard |
| Y2K Revival | Magic UI RetroGrid · Magic UI SparklesText · Animata SplashCursor |
| Minimal SaaS Light | shadcn dominant · Magic UI subtle animations |
| Editorial Dark Premium | Aceternity LampEffect · React Bits TextReveal · Motion Primitives Cursor |
| Fintech Trustworthy | Tremor charts · Kibo DateRangePicker · shadcn forms |
| Portfolio Creative | React Bits ImageTrail · Cult UI DirectionAwareHover |
| Crypto Web3 | Aceternity GoogleGeminiEffect · Magic UI OrbitingCircles |
| Bento Grid Dashboard | Magic UI BentoGrid · Tremor Metric |
| Gaming Cyber | Aceternity Vortex · Cult UI DynamicIsland |
| Vaporwave Retro | Magic UI RetroGrid · Magic UI FlickeringGrid |
| + 14 more... | Auth Split Screen · Health Wellness · Ecommerce · Pricing · etc. |

---

## 17 Commands

| Command | What it does |
|---------|-------------|
| `/design [what]` | Full 7-step workflow: scan → research → system → plan → code → lint |
| `/review [file]` | 5-layer audit: design quality, code lint, a11y, performance, consistency |
| `/ship` | 8-gate production readiness check → GO ✅ or BLOCKED ⛔ |
| `/component [Name]` | Generate any of 30 production-ready components |
| `/heal [file]` | Auto-fix all Critical + High lint issues |
| `/tokens` | Export W3C tokens.json + CSS variables + TypeScript types |
| `/dark` | Convert existing design to dark mode with color science |
| `/a11y [path]` | Full WCAG 2.1 AA audit |
| `/cro [path]` | Eye tracking simulation + conversion rate playbook |
| `/color [hex]` | WCAG math + harmony generation + color psychology |
| `/typography [fonts]` | Modular scale + font pairing score + readability rules |
| `/motion` | Disney principles → Framer Motion snippets |
| `/extract [url/css]` | Reverse-engineer any site's design system |
| `/storybook [component]` | Auto-generate Storybook stories |
| `/preview` | Self-contained HTML preview with token sidebar |
| `/approved` | Stamp design approval, create versioned snapshot |
| `/apply` | Generate production code from approved design |

---

## 86 Lint Rules

Tvastar catches mistakes before they ship. Rules are sourced from the actual documentation of each framework and library — not guesswork.

**Next.js 15 + React 19**
- `params` must be awaited (Next.js 15 breaking change)
- `useFormState` renamed to `useActionState` (React 19)
- `fetch()` requires explicit `cache:` option (Next.js 15)
- Server Actions require auth check before mutation
- Dynamic imports for heavy components

**Design Quality**
- Aurora on light background (invisible — component is dark-only)
- 3+ statement components per section (visual chaos)
- Missing `useReducedMotion()` on Framer Motion
- Linear easing on discrete UI (violates motion principles)
- Duration > 600ms for non-hero animations

**Accessibility**
- Focus states (`focus:outline-none` without ring)
- Touch targets < 44px
- Missing `aria-label` on icon buttons
- `key={index}` in lists

**Code Quality**
- `key={index}` in `.map()` — breaks React reconciliation
- Raw `<img>` in Next.js — use `next/image`
- Hardcoded hex in `className`
- Console.log in production

---

## Design Intelligence

### Color Science
Every palette gets WCAG contrast ratios calculated against the actual background color. Failing colors get suggested fixes that stay true to the hue.

```
#8A2EFF on #0A0014 → 3.83:1 FAIL ❌
Suggestion: #A246FF → 4.75:1 AA ✅
```

### Motion System
Duration × easing × reduced-motion — all three, every animation.

```
hover        150ms  ease-out
modal open   300ms  spring stiffness:300 damping:30
hero reveal  500ms  cubic-bezier(0.16, 1, 0.3, 1)
continuous   700ms  linear (ONLY for spinners/shimmer)
```

### Typography Science
13 expert pairings with pairing scores, modular scales, and Fontshare alternatives to Google Fonts.

### UX Psychology
18 laws applied to every design plan: Fitts, Hick, Miller, Von Restorff, Peak-End Rule, Gestalt principles.

---

## Examples

### Y2K Social Media Platform
```
/design Y2K social media platform
```
Output: RetroGrid background · SparklesText hero · RainbowButton CTA · 
NeonGradientCard features · SplashCursor delight · ShineBorder accents

### Fintech Analytics Dashboard  
```
/design fintech analytics dashboard
```
Output: Tremor AreaChart + Metric KPIs · Kibo DateRangePicker forms · 
Magic UI BentoGrid features · Eldora TestimonialsMarquee

### Creative Portfolio
```
/design creative portfolio dark cinematic
```
Output: React Bits ImageTrail cursor · Aceternity LampEffect hero · 
Cult UI DirectionAwareHover cards · Motion Primitives MorphingDialog

### Everything automatically:
- Scans your package.json — knows what's installed
- Reads your globals.css — knows your existing colors
- Checks WCAG on your colors before generating any code
- Waits for your approval before writing a line

---

## Reference Library

4,077 lines of curated design knowledge:

| File | Contains |
|------|---------|
| `references/resources-blogs.md` | 30+ sources with exact search queries per use case |
| `references/component-library-catalog.md` | Decision tree for all 18 libraries |
| `references/inspiration.md` | 2026 trends, Awwwards formula, senior eye test |
| `references/motion-principles.md` | Duration table, easing library, Disney principles |
| `references/ux-principles.md` | 18 UX laws + 7 Gestalt principles applied |
| `references/react-bits-catalog.md` | 50+ components with TS+TW install variants |
| `references/nextjs-guidelines.md` | Next.js 15 + React 19 + Turbopack + PPR |
| `references/charts-icons-reference.md` | Chart type matrix, Recharts code, Lucide icons |
| `references/page-patterns.md` | Landing, dashboard, auth, pricing layouts |
| + 4 more... | Vue/Svelte · shadcn/Tailwind · native · React |

---

## Architecture

```
ui-design-intelligence/
├── SKILL.md                    ← Claude Code reads this first
├── install.sh                  ← One-command installer
├── scripts/
│   ├── core.py                 ← 1,560 lines: 20 palettes, 24 styles, 18 libraries
│   ├── design_system.py        ← Full design system generator (21 output sections)
│   ├── detect_stack.py         ← Reads package.json, detects 18 libraries
│   ├── framework_lint.py       ← 86 rules across 13 frameworks
│   ├── color_science.py        ← WCAG math, harmony, suggestions
│   ├── typography_science.py   ← Pairing scores, modular scale
│   ├── motion.py               ← Disney principles → Framer snippets
│   ├── component.py            ← 30 production components
│   ├── review.py               ← 5-layer code auditor
│   ├── ship.py                 ← 8-gate production readiness
│   ├── heal.py                 ← Auto-fix Critical + High issues
│   ├── test_all.py             ← 164 tests
│   └── [8 more scripts]
└── references/
    └── [13 markdown files]     ← 4,077 lines of design knowledge
```

---

## 2026 Technology Support

Tvastar is current as of **March 2026**:

- ✅ **Next.js 15** — `params` as Promises, uncached `fetch()`, PPR, `after()`
- ✅ **React 19** — `useActionState`, `use()`, `useFormStatus`, `useOptimistic`
- ✅ **Turbopack** — default in Next.js 15, compatibility notes
- ✅ **Tailwind v4** — `@theme {}` syntax, `bg-linear-to-r`, CSS variables
- ✅ **Framer Motion** — `useReducedMotion()`, `AnimatePresence`, variants
- ✅ **shadcn/ui** — latest components, `zodResolver`, v4 compatibility
- ✅ **Tremor** — dashboard charts and metrics
- ✅ **Animata** — SplashCursor, LiquidChrome, NumberFlow
- ✅ **Motion Primitives** — MorphingDialog, Magnetic, TextEffect
- ✅ **Cult UI** — DirectionAwareHover, DynamicIsland

---

## Contributing

Contributions welcome. The skill improves when new libraries, styles, and rules are added.

**Adding a new library:**
1. Add entry to `LIBRARY_CATALOG` in `scripts/core.py`
2. Add slot logic in `select_components()` in `scripts/core.py`
3. Add rules to `framework_lint.py` if the library has gotchas
4. Add section to `references/component-library-catalog.md`
5. Add search strategy to `references/resources-blogs.md`
6. Run `python3 scripts/test_all.py` — all 164 must pass
7. Submit PR

**Adding a new style:**
1. Add entry to `STYLES` in `scripts/core.py` with vibe, effects, anti_patterns, and library arrays
2. Run tests

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

---

## License

MIT — use freely, contribute back.

---

<div align="center">

Built for Claude Code · Updated March 2026 · [Report a bug](https://github.com/yourusername/tvastar/issues) · [Request a feature](https://github.com/yourusername/tvastar/issues)

*If Tvastar helped you ship something great, a ⭐ means a lot.*

</div>
