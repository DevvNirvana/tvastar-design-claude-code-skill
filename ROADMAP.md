# UI Design Intelligence — God-Level Upgrade Roadmap
# Version: 3.0
# Created: 2026-03-18
# Status legend: [ ] Pending  [x] Complete  [~] In Progress  [!] Blocked
#
# RULE: Never mark [x] unless the file exists, tests pass, and SKILL.md is updated.
# ─────────────────────────────────────────────────────────────────────────────────

---

## PHASE 1 — Preview / Approval / Apply Loop
**Goal:** Transform from code generator → design collaboration workflow.
**Why first:** Closes the biggest gap. Professionals never ship code without visual approval.

### 1.1 [x] preview.py — Self-contained HTML preview generator
- Generates a single .html file with EVERYTHING inlined (CSS, fonts, JS, SVGs)
- Zero external dependencies — opens in any browser instantly
- Renders full page with real typography, real colors, realistic content
- Includes dark/light toggle button in preview
- Shows design token sidebar: colors, fonts, spacing used
- Works as a Claude artifact (renders inline in Claude Code panel)
- Command: /preview [page-type] [--dark] [--open]

### 1.2 [x] approved.py — Design approval recorder
- Stamps the approved design into design-system/MASTER.md
- Records: approved palette, fonts, component selections, layout decisions
- Creates design-system/approved/[timestamp]-[page].json snapshot
- Generates a diff if approving over a previous approval (what changed)
- Locks design tokens so /apply uses exact approved values
- Command: /approved [--message "reason for approval"]

### 1.3 [x] apply.py — Approval-to-production code executor
- Reads from approved design-system snapshot
- Generates production-ready framework-correct component files
- Auto-runs /review on every generated file
- Auto-fixes Critical and High issues before delivery
- Only outputs files after review score >= 80
- Command: /apply [--component Hero] [--page landing] [--all]

### 1.4 [x] SKILL.md update — Document the /preview /approved /apply workflow
- Add to trigger description
- Add workflow diagram showing the 3-stage process
- Add to reference table

---

## PHASE 2 — Color Science & Psychology Engine
**Goal:** Make color choices defensible with psychology, science, and WCAG math.
**Why:** Any LLM picks colors. God-level knows WHY each color works.

### 2.1 [x] color_science.py — Color intelligence engine
- Color psychology by industry:
  * Finance/Healthcare: blues (trust, stability, #0EA5E9, #0369A1)
  * AI/Tech/Premium: violet-indigo (#6366F1, #7C3AED) — but warn of overuse
  * Energy/Urgency/Food: orange-red (#F97316, #EF4444)
  * Growth/Sustainability/Health: greens (#22C55E, #059669)
  * Luxury/Exclusive: near-black + gold, or deep plum
  * Creative/Agency: high-contrast, unexpected combinations
- Color harmony algorithms:
  * Complementary (opposite on wheel): highest contrast, use for CTA only
  * Analogous (adjacent): harmonious, use for primary + secondary
  * Triadic (120° apart): vibrant, use for accent systems
  * Split-complementary: balanced tension, good for brands
  * Monochromatic: sophisticated, use for minimal luxury
- WCAG contrast calculator:
  * Given foreground + background hex → outputs ratio
  * Auto-suggests accessible alternative if failing
  * Checks: normal text (4.5:1), large text (3:1), UI components (3:1)
- Color temperature analysis: warm vs cool for emotional response
- Dark mode color relationships: different hue shifts needed, not just lightness
- Command: /color [hex] --check-contrast [bg-hex]
          /color --palette [industry] [style]
          /color --harmony [hex] [type]

### 2.2 [x] Update core.py — Embed color science into palette data
- Add industry_fit field to every palette
- Add harmony_type field
- Add wcag_score (pre-calculated contrast ratios)
- Add emotional_response field (what this palette communicates)
- Add dark_mode_notes (what changes in dark version)

### 2.3 [x] Update design_system.py — Output WCAG ratios in design system
- Show contrast ratio for primary text on bg
- Show contrast ratio for muted text on bg  
- Flag any failing combinations immediately
- Add color psychology explanation for chosen palette

---

## PHASE 3 — Typography Science Engine
**Goal:** Understand typography at the level of a type director, not just font picker.
**Why:** Typography does 80% of design work. Current system picks pairs but not science.

### 3.1 [x] typography_science.py — Type intelligence engine
- Modular scale calculator:
  * Ratios: Minor Second 1.067, Major Second 1.125, Minor Third 1.200,
            Major Third 1.250, Perfect Fourth 1.333, Augmented Fourth 1.414,
            Perfect Fifth 1.500, Golden Ratio 1.618
  * Given base size (16px) + ratio → full type scale
  * Recommend ratio by product type (SaaS: 1.25, Editorial: 1.414, Bold: 1.618)
- Readability science:
  * Optimal line length: 45-75 characters (Bringhurst's Elements of Typographic Style)
  * Optimal line-height: 1.4-1.6 for body, 1.1-1.2 for headings
  * x-height analysis: high x-height = better screen readability
  * Letter-spacing: tighten headings (-0.02em to -0.04em), loosen all-caps (+0.1em)
- Font classification intelligence:
  * Geometric sans (Outfit, Plus Jakarta): modern, neutral, tech-forward
  * Humanist sans (Inter, DM Sans): warm, readable, UI-optimal
  * Grotesque (Space Grotesk, Bricolage): editorial, character, personality
  * Display serif (Fraunces, Melodrama): luxury, editorial, drama
  * Slab serif: strong, stable, editorial tech
  * Monospace (Geist Mono, Space Mono): code, technical, intentional
- Pairing rules:
  * Contrast is the rule: serif + sans, display + neutral
  * Never: two geometric sans, two serifs, two display fonts
  * Maximum: 2 typefaces per design (heading + body)
  * Variable fonts: weight axis for scroll-reactive headlines
- Command: /typography --product [type] --style [keywords]
          /typography --scale [base] [ratio]
          /typography --check [font-name]

### 3.2 [x] Update core.py TYPOGRAPHY — Add science metadata
- Add x_height_rating (high/medium/low)
- Add best_for classification
- Add pairing_reason explanation
- Add modular_scale_recommendation
- Add variable_font flag
- Add google_fonts_performance (font-display, subset options)

---

## PHASE 4 — Motion Design Principles Engine
**Goal:** Animations that communicate state and delight, not just decorate.
**Why:** Motion is currently scattered. Needs its own science and principle system.

### 4.1 [x] motion.py — Animation intelligence engine
- Disney's 12 principles applied to UI:
  1. Squash and Stretch → scale transforms that feel physical
  2. Anticipation → slight move before action (button press)
  3. Staging → direct attention before revealing content
  4. Straight Ahead / Pose to Pose → keyframe vs spring animation
  5. Follow Through → element overshoots slightly then settles (spring)
  6. Slow In, Slow Out → ease-in-out, never linear for UI
  7. Arc → natural curved paths (toast notification path)
  8. Secondary Action → subtle supporting motion (icon wiggle on hover)
  9. Timing → duration science table
  10. Exaggeration → slightly more than real for delight
  11. Solid Drawing → preserve 3D feel in 2D animations
  12. Appeal → motion that feels alive and intentional
- Duration science table:
  * 0-100ms: instant (imperceptible delay — hover bg color)
  * 100-150ms: fast (hover state transitions)
  * 200-300ms: normal (show/hide, dropdowns, tooltips)
  * 300-400ms: deliberate (page entrances, modals)
  * 400-600ms: cinematic (hero reveals, dramatic entrances)
  * 600ms+: too slow for UI (only for creative/portfolio)
- Easing curve library:
  * ease-out: most natural for UI (fast start, slow end)
  * ease-in: exits, elements leaving screen
  * ease-in-out: elements moving between positions
  * spring (0.16, 1, 0.3, 1): bouncy entrance, feels physical
  * linear: only for continuous loops (spinners, progress)
- Stagger patterns:
  * List items: 30-50ms apart
  * Grid cards: 50-80ms apart
  * Characters (SplitText): 20-40ms apart
  * Max stagger: 8 items (after 8, first item already finished)
- Framer Motion snippet library: variants, AnimatePresence patterns, layout animations
- Reduced motion strategy: what to replace with (instant, opacity-only, scale-only)
- Command: /motion --component [type] --style [entrance|exit|hover|scroll]
          /motion --audit [file] (checks animation decisions)

### 4.2 [x] references/motion-principles.md — Reference file
- Disney 12 principles with UI application examples
- Duration table with use case mapping
- Easing curve visual descriptions
- Framer Motion snippet library
- Library-specific animation patterns (React Bits, Aceternity, Magic UI)
- When NOT to animate: checklist

---

## PHASE 5 — /component Command
**Goal:** Generate any single component on demand with full design system + review cycle.
**Why:** Most design requests are for ONE component, not full pages.

### 5.1 [x] component.py — Isolated component generator
- Takes component type + style + framework
- Runs full design system generation (scoped)
- Selects best library components for each slot
- Generates complete, isolated, production-ready component file
- Auto-runs /review on output
- Auto-fixes Critical issues before delivery
- Examples:
  * /component PricingCard --style dark-premium --framework nextjs
  * /component TestimonialCarousel --style minimal-light
  * /component AuthForm --style split-screen
  * /component HeroSection --style aurora-dark
  * /component DataTable --columns "name,email,role,status,date"
  * /component NavBar --style sticky-blur --links "home,features,pricing,docs"
- Component library (40+ templates):
  * Marketing: HeroSection, FeatureGrid, TestimonialGrid, PricingTable,
               LogoStrip, CTASection, StatsRow, FAQAccordion, TeamGrid
  * App UI: NavBar, Sidebar, DataTable, KPICard, AnalyticsChart,
            EmptyState, LoadingState, ErrorState, SearchBar
  * Forms: LoginForm, SignupForm, ContactForm, CheckoutForm, SettingsForm,
           MultiStepForm, OnboardingFlow
  * Feedback: ToastNotification, AlertBanner, ProgressBar, SkeletonLoader,
              ConfirmDialog, NotificationCenter
  * Cards: ProductCard, ProfileCard, ArticleCard, BlogCard,
           PricingCard, FeatureCard, JobCard, EventCard

### 5.2 [x] references/component-templates.md — Component spec library
- Each component: description, required props, design notes, library picks
- Variant matrix (style × framework × dark/light)
- Anti-patterns for each component type
- Accessibility checklist per component

---

## PHASE 6 — Self-Healing Review Cycle
**Goal:** /review finds issues → Claude autonomously fixes them → re-runs → confirms.
**Why:** Removes the human repair step. True autonomous quality loop.

### 6.1 [x] heal.py — Auto-fix engine
- Reads /review output
- For each Critical and High issue: applies known safe auto-fix
- Auto-fixable issues (can fix programmatically):
  * Missing cursor-pointer → adds to className
  * Missing motion-reduce:animate-none → adds alongside animate-*
  * Raw <img> → converts to <Image> (Next.js) with width/height
  * Missing alt text → adds alt="" with TODO comment for real text
  * Missing key prop → adds key={item.id} with index fallback
  * console.log → removes
  * Hardcoded hex in className → converts to CSS variable
  * focus:outline-none without ring → adds focus-visible:ring-2
  * Missing aria-label on icon button → adds placeholder, flags for real text
- Issues that require human: flags clearly, does NOT auto-fix
  * Semantic HTML restructuring (div→button)
  * Color contrast failures (need design decision)
  * Missing content (empty states, error states)
- After healing: runs /review again, shows before/after score
- Command: /heal [file] — fix one file
          /heal --all — fix all files in src/
          /heal --dry-run — show what would be changed without changing

### 6.2 [x] Update review.py — Add --fix flag
- --fix flag calls heal.py on the reviewed file automatically
- Shows score before and after healing
- Reports: "Fixed 4 of 6 issues automatically. 2 require human review."

---

## PHASE 7 — W3C Design Tokens Standard
**Goal:** Generate tokens.json compliant with W3C Design Tokens spec (stable Oct 2025).
**Why:** Interoperability with Figma, Style Dictionary, and AI design tools.

### 7.1 [x] tokens.py — W3C-compliant token generator
- Generates tokens.json in W3C format:
  {
    "color": {
      "primary": { "$value": "#6366F1", "$type": "color" },
      "background": { "$value": "#09090B", "$type": "color" }
    },
    "fontFamily": {
      "heading": { "$value": "Plus Jakarta Sans", "$type": "fontFamily" }
    },
    "spacing": {
      "sm": { "$value": "8px", "$type": "dimension" }
    }
  }
- Also generates: tokens.css (CSS custom properties), tokens.ts (TypeScript)
- Style Dictionary config for multi-platform output
- Figma Variables JSON format export
- Tailwind config auto-generated from tokens
- Command: /tokens --format w3c|css|ts|figma|tailwind
          /tokens --all (outputs all formats)

### 7.2 [x] Update design_system.py — Output tokens.json alongside MASTER.md
- Every /design run now also saves design-system/tokens.json
- design-system/tokens.css auto-generated
- design-system/tokens.ts auto-generated with typed exports

---

## PHASE 8 — /dark Command
**Goal:** Convert any existing design to proper dark mode (not just adding dark: prefixes).
**Why:** Dark mode is requested constantly and done poorly almost universally.

### 8.1 [x] dark.py — Dark mode conversion engine
- Reads existing CSS variables or Tailwind classes from a file/directory
- Applies dark mode color science:
  * Background: never pure black, use zinc-950 (#09090B) or zinc-900 (#18181B)
  * Surfaces: 2-4 levels of lightness (bg, surface, elevated, overlay)
  * Text: never pure white, use zinc-50 (#FAFAFA) max
  * Borders: reduce contrast (white/10 to white/20 range)
  * Shadows: flip to glow (outset shadows become inner glows or border glows)
  * Colors: desaturate slightly in dark (pure #6366F1 can feel harsh)
  * Images: add slight dim (brightness-90) to avoid eye strain
- Adds .dark {} CSS variable overrides to globals.css
- Adds dark: Tailwind prefixes to component className strings
- Tests: verifies contrast ratios in dark mode too
- Adds DarkModeToggle component automatically
- Command: /dark [file|directory] — convert to dark mode
          /dark --audit — check if dark mode is properly implemented
          /dark --toggle — add dark mode toggle component

---

## PHASE 9 — Eye Tracking & CRO Patterns
**Goal:** Place elements where eyes naturally go. Optimize for conversion.
**Why:** Beautiful design that doesn't convert is decoration, not design.

### 9.1 [x] cro.py — Conversion Rate Optimization engine
- Reading pattern awareness:
  * F-Pattern: text-heavy pages (blogs, docs) — eyes scan horizontal then vertical left
  * Z-Pattern: sparse pages (landing, ads) — eyes follow Z diagonal
  * Gutenberg Diagram: long-form — primary optical area (top-left), terminal area (bottom-right)
  * Layer Cake: dashboard/scan — eyes jump between headings ignoring body
- Eye tracking placement rules:
  * CTA placement: terminal area (bottom-right of Z) or primary optical area (top-left)
  * Most important content: top 600px of viewport — 80% attention above fold
  * Logo: top-left (always, per Jakob's Law)
  * Trust signals (logos, testimonials): just BEFORE the CTA
  * Pricing: after value prop (never before you've earned attention)
- CRO copywriting principles:
  * Headline: problem → solution (not feature → feature)
  * CTA copy: verb + specific outcome ("Start building" not "Get started")
  * Social proof placement: 3 positions — hero, before pricing, below CTA
  * Urgency: only use if real ("Offer ends Friday" not "Limited time")
  * Risk reversal: "Free trial, no credit card" immediately below CTA
- Above-fold audit: checks if CTA, value prop, and social proof all visible at 768px
- Command: /cro [page-type] — get CRO recommendations for page type
          /cro --audit [file] — audit existing page for CRO issues

### 9.2 [x] references/cro-patterns.md — CRO reference file
- Eye tracking patterns with descriptions
- Conversion optimization checklist per page type
- Copy frameworks (AIDA, PAS, BAB)
- Social proof patterns and placement
- Pricing page psychology
- Dark patterns to avoid (ethical CRO only)

---

## PHASE 10 — /a11y Command (Deep Accessibility)
**Goal:** Dedicated accessibility audit deeper than /review covers.
**Why:** Accessibility is law in many countries. /review covers basics. /a11y goes full WCAG.

### 10.1 [x] a11y.py — Full WCAG 2.1 AA auditor
- Contrast ratio calculator (WCAG 1.4.3 / 1.4.11):
  * Calculates actual luminance ratios from hex values
  * Checks: normal text 4.5:1, large text 3:1, UI components 3:1
  * Reports exact ratio and pass/fail for every color combination found
- Reading level analysis:
  * Flesch-Kincaid score for button labels, headings, CTAs
  * Flags overly complex microcopy
- Touch target measurement (WCAG 2.5.5):
  * Flags any interactive element with h/w class implying < 44px
- ARIA role validation:
  * Checks role usage against allowed children
  * Flags role="button" without tabIndex={0}
  * Flags aria-label on non-interactive elements
- Heading hierarchy checker:
  * Maps h1→h2→h3 sequence
  * Flags skipped levels (h1→h3)
  * Flags multiple h1s
- Focus order analysis:
  * Checks tabIndex sequence is logical
  * Flags tabIndex > 0 (anti-pattern)
- Form accessibility:
  * Every input has label
  * Error messages associated with fields
  * Required fields marked with aria-required
- Color independence check:
  * Flags status indicators using only color (no icon/text)
- WCAG 2.1 checklist output (all 50 AA criteria)
- Command: /a11y [file|directory]
          /a11y --contrast [hex] [bg-hex]
          /a11y --wcag (full criteria checklist)
          /a11y --report (save full report to a11y-report.md)

---

## PHASE 11 — Gestalt Principles Engine
**Goal:** Apply all 7 Gestalt laws scientifically to every layout decision.
**Why:** Gestalt explains WHY layouts feel right or wrong. Missing from current system.

### 11.1 [x] Update references/ux-principles.md — Add Gestalt section
- Law of Proximity: related items closer than unrelated (spacing as grouping signal)
- Law of Similarity: same style = same group (consistent card heights, icon sizes)
- Law of Continuity: eyes follow lines and curves (navigation flow)
- Law of Closure: incomplete shapes perceived as complete (skeleton loaders)
- Law of Common Fate: moving together = belonging together (animation grouping)
- Law of Figure/Ground: foreground vs background separation (shadow, blur, z-index)
- Law of Symmetry: symmetric = stable, asymmetric = dynamic tension
- Practical application rules per UI pattern type
- Gestalt audit checklist

### 11.2 [x] Update core.py — Embed Gestalt checks in design recommendations
- After palette/typography selection, output Gestalt application notes
- Flag when spacing doesn't respect proximity grouping
- Flag when inconsistent styling breaks similarity law

---

## PHASE 12 — Brand Extraction (URL → Design System)
**Goal:** User gives a URL, Claude reverse-engineers the brand into a design system.
**Why:** The fastest way to match an existing brand is to extract it automatically.

### 12.1 [x] brand_extractor.py — URL-to-design-system converter
- Fetches URL content (works with Claude's web_fetch tool)
- Extracts from CSS and HTML:
  * Color values (background-color, color, border-color — top 10 most used)
  * Font families (font-family declarations)
  * Font sizes (most common heading and body sizes)
  * Border-radius values
  * Shadow definitions
  * Spacing units (most common padding/margin values)
- Builds design-system/MASTER.md from extracted values
- Flags gaps (things it couldn't detect)
- Suggests complementary additions
- Command: /extract [url] — extract design system from URL
          /extract [url] --apply — extract + generate tokens immediately

---

## PHASE 13 — Storybook Auto-Generation
**Goal:** Every component gets a Storybook story automatically.
**Why:** Components become machine-readable, testable, and documentable.

### 13.1 [x] storybook.py — Storybook story generator
- For any component file: generates ComponentName.stories.tsx
- Creates stories for:
  * Default state
  * All prop variants
  * Dark mode variant
  * Mobile viewport story
  * Loading/error/empty states
- Generates: .storybook/main.ts config if not present
- Generates: decorators for dark mode, responsive testing
- Command: /storybook [file] — generate stories for component
          /storybook --all — generate for all components in src/components/

---

## PHASE 14 — Final Integration & SKILL.md v3.0
**Goal:** All commands unified, documented, and working together as one system.
**Why:** Each command should reference others. The system is greater than the parts.

### 14.1 [x] Final SKILL.md v3.0 — Complete rewrite
- All commands documented: /design /preview /approved /apply /review /ship
  /component /heal /tokens /dark /a11y /cro /extract /storybook /motion /color /typography
- Command interaction diagram (which commands call which)
- Complete reference table (all 14 reference files)
- God-level design philosophy section
- Version history

### 14.2 [x] README.md — Public-facing documentation
- Installation (3 commands)
- Quick start guide
- Command reference table
- Example outputs
- Contributing guide

### 14.3 [x] Final test suite
- test_all.py: runs integration tests for every command
- test_review.py: 20+ specific review rule tests
- test_ship.py: 8-gate ship tests
- All tests must pass before marking Phase 14 complete

---

## COMPLETION TRACKING

Phase 1  — Preview/Approval/Apply:    [x] 1.1  [x] 1.2  [x] 1.3  [x] 1.4
Phase 2  — Color Science:             [x] 2.1  [x] 2.2  [x] 2.3
Phase 3  — Typography Science:        [x] 3.1  [x] 3.2
Phase 4  — Motion Design:             [x] 4.1  [x] 4.2
Phase 5  — /component Command:        [x] 5.1  [x] 5.2
Phase 6  — Self-Healing Review:       [x] 6.1  [x] 6.2
Phase 7  — W3C Design Tokens:         [x] 7.1  [x] 7.2
Phase 8  — /dark Command:             [x] 8.1
Phase 9  — Eye Tracking & CRO:        [x] 9.1  [x] 9.2
Phase 10 — /a11y Command:             [x] 10.1
Phase 11 — Gestalt Principles:        [x] 11.1  [x] 11.2
Phase 12 — Brand Extraction:          [x] 12.1
Phase 13 — Storybook Auto-Gen:        [x] 13.1
Phase 14 — Final Integration:         [x] 14.1  [x] 14.2  [x] 14.3

TOTAL TASKS: 30
COMPLETED:    30
PROGRESS:     100% 🏁

---

## FILE MANIFEST (when complete)
scripts/
  core.py              ✓ exists
  design_system.py     ✓ exists
  detect_stack.py      ✓ exists
  framework_lint.py    ✓ exists
  review.py            ✓ exists
  search.py            ✓ exists
  ship.py              ✓ exists
  preview.py           [x] Phase 1.1
  approved.py          [x] Phase 1.2
  apply.py             [x] Phase 1.3
  color_science.py     [x] Phase 2.1
  typography_science.py [x] Phase 3.1
  motion.py            [x] Phase 4.1
  component.py         [x] Phase 5.1
  heal.py              [x] Phase 6.1
  tokens.py            [x] Phase 7.1
  dark.py              [x] Phase 8.1
  cro.py               [x] Phase 9.1
  a11y.py              [x] Phase 10.1
  brand_extractor.py   [x] Phase 12.1
  storybook.py         [x] Phase 13.1
  test_all.py          [x] Phase 14.3

references/
  charts-icons-reference.md      ✓ exists
  component-library-catalog.md   ✓ exists
  component-templates.md         [ ] Phase 5.2
  cro-patterns.md                [ ] Phase 9.2
  inspiration.md                 ✓ exists
  motion-principles.md           [ ] Phase 4.2
  native-guidelines.md           ✓ exists
  nextjs-guidelines.md           ✓ exists
  page-patterns.md               ✓ exists
  react-bits-catalog.md          ✓ exists
  react-guidelines.md            ✓ exists
  resources-blogs.md             ✓ exists
  shadcn-tailwind-guidelines.md  ✓ exists
  ux-principles.md               ✓ exists (update Phase 11)
  vue-svelte-guidelines.md       ✓ exists

root/
  SKILL.md             ✓ exists (update Phase 1.4, 14.1)
  install.sh           ✓ exists
  README.md            [x] Phase 14.2
