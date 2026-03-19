# UX Principles Reference
Distilled from: Refactoring UI · Laws of UX · Design of Everyday Things · Don't Make Me Think
· 100 Things Every Designer Needs to Know About People · About Face · Designing Interfaces

---

## The 12 Psychology Laws (Jon Yablonski — Laws of UX)

### 1. Fitts's Law
**"Time to acquire a target is a function of distance and size."**
- Make primary CTAs large — minimum 44×44px tap target (Apple HIG)
- Size communicates importance. Small = secondary. Large = primary.
- Place primary actions where hands naturally rest (bottom of screen on mobile)
- Don't make users travel far to reach important actions

```css
/* Minimum tap target */
.btn-primary { min-height: 44px; min-width: 44px; padding: 12px 24px; }
```

### 2. Hick's Law
**"More choices = longer decision time."**
- Max 5-7 navigation items (Miller's Law applies here too)
- ONE primary CTA per screen — never two equal-weight actions
- Use progressive disclosure — hide advanced options until needed
- Reduce checkout steps ruthlessly (each step = decision = drop-off)

### 3. Miller's Law
**"Working memory holds 7±2 items."**
- Group navigation into categories of 3-7
- Break feature lists into chunks of 3 — never 12 in a row
- Pagination over infinite scroll for complex content
- Visual separators between content groups

### 4. Jakob's Law
**"Users spend most time on OTHER websites."**
- Logo top-left, links to home ✓
- Navigation at top ✓
- Search top-right or prominent ✓
- Cart icon top-right on e-commerce ✓
- Don't reinvent breadcrumbs, tabs, accordions — users know these patterns

### 5. Von Restorff Effect (Isolation Effect)
**"Unique items are remembered better."**
- The CTA button MUST be the only element using your CTA color on the page
- If everything is bold, nothing is bold
- Use accent color for ONE thing — the most important action
- The "recommended" pricing tier breaks the visual pattern

```tsx
// Von Restorff applied:
// - Pricing cards: all gray borders except "Pro" which gets a violet border + "Most Popular" badge
// - Nav: all links same weight except the single "Get Started" CTA button
// - Features: all text except one number stat in accent color
```

### 6. Peak-End Rule
**"People judge experiences by peak + end, not average quality."**
- **Peak moment** = the hero impression + the "aha" moment inside product
- **End moment** = success state after signup/purchase
- Make onboarding success screen genuinely delightful
- Make empty states helpful, not sad
- First impression (hero) and final impression (thank you page) are disproportionately important

### 7. Aesthetic-Usability Effect
**"Aesthetic interfaces are perceived as easier to use."**
- Users forgive minor UX issues if the design is beautiful
- Polish is not vanity — it builds trust and reduces perceived friction
- A loading state that looks good feels faster
- Skeleton loaders > spinners because they preview shape

### 8. Law of Proximity
**"Objects near each other are perceived as related."**
- Label directly above/left of its input field — not centered between two fields
- Related items: 4-8px gap. Unrelated items: 24-48px gap. Sections: 64-96px gap.
- This is why design tokens for spacing matter — consistency creates grouping

```css
/* Proximity in forms */
.form-group { display: flex; flex-direction: column; gap: 6px; } /* label + input tight */
.form-group + .form-group { margin-top: 20px; } /* fields separated */
```

### 9. Law of Prägnanz (Simplicity)
**"People perceive ambiguous forms as their simplest interpretation."**
- When in doubt, simplify
- Users scan before they read — hierarchy before decoration
- Remove every element that doesn't serve a purpose
- Negative space is as important as positive space

### 10. Serial Position Effect
**"People remember first and last items best."**
- Put your most important nav item first or last
- In a feature list, lead with the most compelling feature
- End CTAs/testimonial sections with your strongest testimonial

### 11. Doherty Threshold
**"Productivity soars when response < 400ms."**
- Optimistic UI: update immediately, roll back on failure
- Skeleton loaders for anything > 100ms
- Progress indicators for anything > 400ms
- Perceived performance > actual performance

### 12. Zeigarnik Effect
**"People remember incomplete tasks better."**
- Profile completion percentages (LinkedIn model)
- Onboarding checklists — "3 of 5 steps complete"
- Progress bars in multi-step forms
- "You're 70% set up" beats "Finish setup"

---

## Refactoring UI — Core Principles (Wathan & Schoger)

### Hierarchy is everything
- **Size, weight, color** = the three tools of visual hierarchy
- Use all three consistently: primary=large+bold+dark, secondary=medium+normal+medium, tertiary=small+normal+light
- De-emphasize secondary info more than you think you need to

### Start with too much whitespace
- Every design starts with too little whitespace
- When a design "doesn't feel right," add more padding first
- Component padding should feel extravagant

### Not every text needs a label
- "johndoe@example.com" doesn't need a "Email:" label — it's obviously an email
- Remove redundant labels in cards and list items
- User cards: name is bold, job title is muted below — no "Name:" label needed

### Avoid implicit semantics
- Don't rely on color alone to communicate (accessibility)
- Use icons + color, not color alone, for status indicators
- Status "green" needs a checkmark icon too

### Shadows define elevation, not decoration
- sm shadow = content level
- md shadow = raised card
- lg shadow = dropdown/modal
- Don't mix shadow styles randomly

```css
/* Elevation system */
--shadow-sm:  0 1px 2px rgb(0 0 0 / 5%);
--shadow-md:  0 4px 6px -1px rgb(0 0 0 / 10%), 0 2px 4px -2px rgb(0 0 0 / 10%);
--shadow-lg:  0 10px 15px -3px rgb(0 0 0 / 10%), 0 4px 6px -4px rgb(0 0 0 / 10%);
--shadow-xl:  0 20px 25px -5px rgb(0 0 0 / 10%), 0 8px 10px -6px rgb(0 0 0 / 10%);
--shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 25%);
```

### Color opacity instead of value
- Use transparent colors for layered UI (glass effects, hover states)
- `bg-violet-500/10` > picking a custom lighter violet hex
- Consistent opacity scale: /5, /10, /15, /20, /30, /40, /50

### The "1000 calorie diet" for spacing
- Define 8 spacing values and use only those: 4, 8, 12, 16, 24, 32, 48, 64
- Never use "I'll just do 13px here" — stick to your scale

---

## Don Norman — Design of Everyday Things

### Affordances
- An element should communicate how it's used through its appearance
- Buttons look pressable (rounded, elevated, clear label)
- Input fields look fillable (bordered, placeholder, label above)
- Clickable text needs visual differentiation (color, underline, or context)

### Signifiers
- Tell users what to do: "Click here", hover states, directional arrows
- Don't assume affordances are obvious — add signifiers

### Feedback
- Every action needs immediate feedback
- Form submit: loading state → success state → next step
- Button click: press state → loading → result
- No silent failures — if something doesn't work, say why

### Conceptual Models
- Build on users' existing mental models
- Shopping cart = basket (metaphor users already understand)
- Trash/delete = recycle bin metaphor
- Settings = gear icon (universal convention — Jakob's Law)

---

## Accessibility Fundamentals (WCAG 2.1 AA)

### Contrast ratios
- Normal text: **4.5:1 minimum**
- Large text (18px+): **3:1 minimum**
- UI components and graphics: **3:1 minimum**
- Don't fail on placeholder text — it's often too light

### Focus management
```css
/* Never remove focus — enhance it */
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
  border-radius: 4px;
}
/* The above is better than removing outline entirely */
```

### Motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Touch targets
- Minimum 44×44px for all interactive elements (Apple HIG)
- On mobile: 48×48dp (Material Design)
- Never make tap targets smaller to fit more — reduce content instead

### Semantic HTML
```tsx
// Correct semantic structure
<header role="banner">
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>
<main id="main-content">
  <h1>Page Title</h1> {/* Only ONE h1 per page */}
  <section aria-labelledby="features-heading">
    <h2 id="features-heading">Features</h2>
  </section>
</main>
<footer role="contentinfo">...</footer>
```

---

## Micro-Interaction Checklist

Every interactive state needs a design:
- `default` — base state
- `hover` — cursor over (desktop only)
- `focus` — keyboard focus (for accessibility)
- `active` / `pressed` — during click/tap
- `loading` — async operation in progress
- `disabled` — unavailable (explain why when possible)
- `error` — something went wrong (specific message, not "error")
- `success` — operation completed

```tsx
// Complete button states example
<button
  className={cn(
    // Default
    "inline-flex items-center gap-2 rounded-lg px-6 py-3 text-sm font-semibold transition-all",
    "bg-primary text-white cursor-pointer",
    // Hover
    "hover:bg-primary/90 hover:-translate-y-0.5 hover:shadow-lg",
    // Focus
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2",
    // Active
    "active:translate-y-0 active:shadow-none",
    // Disabled
    "disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0",
    // Loading
    isLoading && "cursor-wait"
  )}
  disabled={isDisabled || isLoading}
>
  {isLoading ? <Spinner className="h-4 w-4 animate-spin" /> : <Icon />}
  {isLoading ? "Processing..." : label}
</button>
```

---

## Anti-Patterns Reference

### The 10 Most Common Professional UI Mistakes

1. **Multiple CTAs with equal visual weight** — violates Von Restorff, kills conversion
2. **Using `outline: none` without replacement** — breaks keyboard accessibility
3. **Emoji as icons** — inconsistent rendering across OS, wrong size, no a11y
4. **Placeholder text as labels** — disappears on type, WCAG failure
5. **Layout-shifting hover effects** — `transform: scale(1.05)` on block elements shifts siblings
6. **Low contrast muted text in light mode** — gray-400 on white is a WCAG fail
7. **Dark mode with pure #000000 background** — use #0A0A0A or #09090B instead
8. **Missing loading states** — users think broken, they click again
9. **Tight touch targets on mobile** — buttons under 44px cause mis-taps
10. **Inconsistent border-radius** — `rounded` on cards, `rounded-full` on buttons, no system


---

## Gestalt Principles — The Science of Visual Grouping

> Gestalt psychology explains why layouts feel right or broken.
> Apply all 7 to every design. The best designs layer multiple simultaneously.

### 1. Proximity — Objects near each other appear related
- Label 4-6px ABOVE its input (not 16px — that breaks the group)
- Related items: 4-8px gap. Siblings: 16-24px. Sections: 64-96px.
- Card padding creates a proximity group — everything inside = related
- CSS: .form-group gap: 6px; .form-group + .form-group margin-top: 20px

### 2. Similarity — Shared visual traits signal same type
- All nav links same size/weight — they're the same category
- All primary CTAs same color — same importance level
- Violation: two buttons, same size, different colors = user thinks different function

### 3. Continuity — Eyes follow smooth paths naturally
- Progress steps left-to-right suggest a path to follow
- Alternating feature sections create a Z-path the eye follows
- Lists must be truly aligned — 1px misalignment breaks the line

### 4. Closure — Mind completes incomplete shapes
- Skeleton loaders: mind completes the shape (match content shape exactly)
- Partially visible carousel cards = signal more content exists
- Avatar stacks: overlapping circles = mind sees related group

### 5. Common Fate — Moving together = belonging together
- Stagger animations: items entering together = same group
- Hover: ALL cards dim EXCEPT hovered one = they're peers
- Micro-interaction: form error icon + text shake together = same event

### 6. Figure/Ground — Mind separates foreground from background
- Modal + backdrop blur: modal = figure, rest = ground
- Use shadow, opacity, blur to establish z-axis depth
- Mistake: card on card on card with no clear foreground hierarchy

### 7. Symmetry — Symmetric = stable. Asymmetric = dynamic
- Symmetric: pricing cards, feature grids, testimonial rows
- Asymmetric: hero text-left + image-right creates tension and direction
- Choose deliberately based on brand tone

---

## Gestalt Application by Layout

| Layout | Primary Principle | Application |
|--------|------------------|-------------|
| Nav bar | Proximity + Similarity | Links grouped left, CTA right, same text size |
| Feature grid | Similarity | Equal cards, equal spacing, equal icon size |
| Form | Proximity + Continuity | Labels 4-6px above, one column, visual flow |
| Pricing | Figure/Ground | Pro card elevated = figure, others = ground |
| Dashboard | Similarity + Proximity | KPI cards grouped, same chart style throughout |

---

## Gestalt Quick Audit
- [ ] Related items have smaller gaps than unrelated items (Proximity)
- [ ] CTA color appears ONLY on CTAs (Similarity — Von Restorff)
- [ ] Eye has a clear path to follow (Continuity)
- [ ] Foreground elements are distinctly elevated (Figure/Ground)
- [ ] Animated elements that enter together tell a story (Common Fate)
