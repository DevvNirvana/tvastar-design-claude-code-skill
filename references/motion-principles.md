# Motion Design Principles Reference v1.0
Read when: building animations, selecting motion libraries, reviewing animation code.
Companion to: motion.py (run: python3 scripts/motion.py --principles)

---

## The Core Rule

**Motion communicates state, not decoration.**
Every animation must answer one of these questions:
- Did this element appear, or was it always there?
- Did my action succeed?
- Where did that element go?
- What should I look at next?

If the animation doesn't answer one of these — cut it.

---

## Duration Quick Reference

| Tier | Range | Use |
|------|-------|-----|
| Instant | 0–100ms | bg-color hover, opacity micro |
| Fast | 100–200ms | hover states, focus rings, tooltips |
| Normal | 200–300ms | dropdowns, state transitions |
| Deliberate | 300–400ms | modals, drawers, accordions |
| Slow | 400–500ms | page entrances, card reveals |
| Cinematic | 500–700ms | hero text, full-page transitions |
| ❌ Too slow | 700ms+ | Avoid — feels broken, not polished |

---

## Easing Quick Reference

| Easing | CSS / Framer | Use |
|--------|-------------|-----|
| Entrance | cubic-bezier(0.16,1,0.3,1) | Elements entering — fast start, soft settle |
| Exit | cubic-bezier(0.5,0,1,1) | Elements leaving — accelerates out |
| Spring | stiffness:300, damping:30 | Physical, bouncy — modals, cards |
| Smooth | cubic-bezier(0.4,0,0.2,1) | Accordion height, panel reveals |
| Overshoot | cubic-bezier(0.34,1.56,0.64,1) | Slight bounce for buttons, badges |
| Linear | linear | ONLY continuous loops: spinners, shimmer |

**Rule: Never linear for discrete UI animations. Always ease-out minimum.**

---

## Disney's 12 Principles → UI

1. **Squash & Stretch** — scale(0.97) on button :active. Modal entrance scale(0.95)→(1).
2. **Anticipation** — drawer nudges -4px before opening. Submit compresses before loading.
3. **Staging** — hero H1 animates first. CTA has 0.3s delay. Background blurs on modal.
4. **Pose to Pose** — always keyframes between defined states. Spring interpolates between.
5. **Follow Through** — staggerChildren: 0.05 so items overlap. Accordion content delays 100ms after header.
6. **Slow In/Out** — ease-out for enter. ease-in for exit. NEVER linear.
7. **Arcs** — tooltip translateY(-8px)→(0) + scaleY(0.9)→(1) for arc feel.
8. **Secondary Action** — icon animates with button state. Border glows on focus.
9. **Timing** — use the duration scale. Never arbitrary milliseconds.
10. **Exaggeration** — spring overshoots slightly. Magnetic moves 0.35× cursor (not 1:1).
11. **Solid Drawing** — 3D tilt preserves perspective. Shadow intensifies on tilt axis.
12. **Appeal** — ONE delight moment per page. Cursor effect OR particle trail OR spotlight. Not all three.

---

## Library Motion Patterns

### React Bits
- **Aurora** — CSS animation, 0.4 speed parameter. Slow = premium. Fast = busy.
- **SplitText** — delay parameter between chars (ms). 80ms for headline, 40ms for sub-text.
- **BlurText** — delay between words. 120ms for dramatic reveal, 60ms for fast.
- **SpotlightCard** — mouse-tracking via onMouseMove, requestAnimationFrame for smooth.
- **BounceCards** — spring physics, no configuration needed — defaults are correct.
- **MagneticButton** — 0.3–0.4 cursor multiplier. Spring: stiffness 200, damping 18.

### Aceternity UI
- **LampEffect** — pure CSS conic-gradient animation. No framer needed.
- **BackgroundBeams** — SVG path animation. Slow down via animationDuration.
- **MovingBorder** — border-radius + gradient rotation. Duration controls speed.
- **TextGenerateEffect** — stagger via delay increment. 0.15 per word is readable.

### Magic UI
- **BorderBeam** — CSS animation. Adjust duration (lower = faster beam).
- **AnimatedBeam** — SVG pathLength animation. duration: 2-4s for smooth flow.
- **ShimmerButton** — CSS background-position animation. Linear is correct here (continuous).
- **Ripple** — scale + opacity, ease-out. Delay increments create nested rings.

---

## Anti-Pattern Reference

| Anti-Pattern | Why bad | Fix |
|---|---|---|
| animate-* without motion-reduce | WCAG 2.3.3 failure | Add motion-reduce:animate-none |
| duration > 700ms for UI | Feels broken | Max 600ms for cinematic, 400ms for normal |
| linear easing on discrete UI | Feels robotic | ease-out minimum |
| AnimatePresence without key | Exit never fires | Add key={id} to direct child |
| transition: all | Perf hit | Specify: transition-colors, transition-transform |
| 3+ statement animations per section | Chaos | One delight per section |
| Animation answering no question | Decoration = noise | Cut if no state communication |
| scale on block element without overflow-hidden | Layout shift | Wrap in overflow-hidden container |

---

## Reduced Motion Strategy

Always include. No exceptions.

```css
/* globals.css */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }
}
```

```tsx
// Framer Motion — use useReducedMotion() hook
const prefersReduced = useReducedMotion()
initial={{ opacity: 0, y: prefersReduced ? 0 : 20 }}
```

```html
<!-- Tailwind — alongside every animate-* -->
<div class="animate-pulse motion-reduce:animate-none">
```

**Replacement strategy for reduced motion:**
- Fade-in-up → opacity only (no translateY)
- Scale entrance → opacity only (no scale)
- Continuous loops → pause or instant state
- Scroll reveal → instant appear (no delay)
