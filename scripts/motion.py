#!/usr/bin/env python3
"""
/motion — Animation Design Intelligence Engine v1.0
Phase 4.1 of the God-Level Roadmap

Disney's 12 principles applied to UI. Duration science.
Easing curve library. Framer Motion snippet generator.

Usage:
  python3 motion.py --component hero --style entrance
  python3 motion.py --component card --style hover
  python3 motion.py --duration hover
  python3 motion.py --easing entrance
  python3 motion.py --audit src/components/Hero.tsx
  python3 motion.py --principles
  python3 motion.py --snippets framer
"""

import sys, re, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# ═══════════════════════════════════════════════════════════════════════
# DISNEY 12 PRINCIPLES APPLIED TO UI
# ═══════════════════════════════════════════════════════════════════════

DISNEY_PRINCIPLES = [
    {
        "number": 1, "name": "Squash and Stretch",
        "original": "Objects deform to convey weight and flexibility.",
        "ui_application": "Scale transforms that feel physical — button press scales down slightly, modal entrance scales up from 0.95.",
        "example": "Button: scale(0.97) on :active. Modal: scale(0.95)→scale(1) on open.",
        "framer": "whileTap={{ scale: 0.97 }}  |  initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}",
        "when_to_use": "Interactive elements (buttons, cards) and overlay entrances.",
    },
    {
        "number": 2, "name": "Anticipation",
        "original": "A small preparatory action before the main action.",
        "ui_application": "Drawer peeks before opening. Button slightly compresses before submit animation. List item nudges before expanding.",
        "example": "Drawer: translateX(-4px) then full open. Submit: scale(0.98) then loading spinner.",
        "framer": "Use keyframes: [null, -4, 0] for nudge anticipation.",
        "when_to_use": "Any action with significant consequence — form submit, destructive actions, important reveals.",
    },
    {
        "number": 3, "name": "Staging",
        "original": "Direct attention to the most important element.",
        "ui_application": "Blur or dim secondary content when primary action is focused. Hero animation runs first, everything else follows.",
        "example": "Dialog opens: background blurs (backdrop-filter). Hero H1 animates first, then sub-text, then CTA.",
        "framer": "Staggered entrance: heading delay:0, body delay:0.15, CTA delay:0.3",
        "when_to_use": "Landing page entrances, modal opens, onboarding steps.",
    },
    {
        "number": 4, "name": "Straight Ahead / Pose to Pose",
        "original": "Frame-by-frame vs keyframe animation approaches.",
        "ui_application": "UI uses Pose to Pose (keyframes between defined states). Spring physics adds natural motion between poses.",
        "example": "Define from-state and to-state. Let spring physics interpolate naturally.",
        "framer": "Use variants: { hidden: {opacity:0, y:20}, visible: {opacity:1, y:0} }",
        "when_to_use": "Always use keyframes/variants for UI. Springs for physical motion.",
    },
    {
        "number": 5, "name": "Follow Through and Overlapping Action",
        "original": "Not all parts of an object stop at the same time.",
        "ui_application": "Stagger list items so later items are still entering as earlier ones settle. Accordion header settles before content fades in.",
        "example": "List: items enter at 50ms stagger intervals. Drawer: handle arrives then content fades in 100ms later.",
        "framer": "staggerChildren: 0.05 in parent variants. Separate variants for container and children.",
        "when_to_use": "Any list, grid, or multi-part reveal. Accordion opens.",
    },
    {
        "number": 6, "name": "Slow In / Slow Out (Easing)",
        "original": "Motion starts and ends slowly, is fastest in the middle.",
        "ui_application": "NEVER linear easing for UI. ease-out for elements entering (fast start, slow settle). ease-in for exits.",
        "example": "Enter: cubic-bezier(0.16, 1, 0.3, 1). Exit: cubic-bezier(0.5, 0, 1, 1).",
        "framer": "ease: [0.16, 1, 0.3, 1] for entrance. type:'spring' for physical.",
        "when_to_use": "Every single animation. Linear only for continuous loops (spinners).",
    },
    {
        "number": 7, "name": "Arcs",
        "original": "Natural objects move in arcs, not straight lines.",
        "ui_application": "Tooltips appear slightly above and translate down-in. Toast notifications slide in along an arc. Cards can rotate slightly on hover.",
        "example": "Tooltip: translateY(-8px)→translateY(0) + scaleY(0.9)→1 creates arc feel.",
        "framer": "Combine translateY and scale for arc-like motion.",
        "when_to_use": "Tooltips, popovers, small UI overlays, card hover effects.",
    },
    {
        "number": 8, "name": "Secondary Action",
        "original": "A supporting action that adds richness to the main action.",
        "ui_application": "Icon subtly wiggles when button is hovered. Checkmark draws in after form submit. Border glows while input is focused.",
        "example": "Save button: text says 'Saving...' + spinner simultaneously. Focus: ring animates in + border color transitions.",
        "framer": "AnimatePresence for icon swap. useAnimationControls for triggered secondary animations.",
        "when_to_use": "CTA hover states, form focus, success/error states.",
    },
    {
        "number": 9, "name": "Timing",
        "original": "The number of frames gives an action weight and feeling.",
        "ui_application": "Duration communicates importance. Fast (100-150ms) = instant, responsive. Slow (400-600ms) = important, dramatic.",
        "example": "See duration table. Never use arbitrary durations — pick from the scale.",
        "framer": "duration: 0.15 (fast) | 0.25 (normal) | 0.4 (slow) | 0.6 (dramatic)",
        "when_to_use": "Every animation needs intentional timing from the duration scale.",
    },
    {
        "number": 10, "name": "Exaggeration",
        "original": "Amplify reality slightly for appeal and clarity.",
        "ui_application": "Magnetic button moves slightly more than cursor. Spring slightly overshoots. Bounce on successful save.",
        "example": "Magnetic button: 0.4× cursor offset (not 1:1). Success state: scale(1.05) before settling at scale(1).",
        "framer": "spring with stiffness:200, damping:10 for playful overshoot.",
        "when_to_use": "Delightful moments — success states, completion animations, playful UI.",
    },
    {
        "number": 11, "name": "Solid Drawing",
        "original": "Maintain 3D feel and weight in 2D animations.",
        "ui_application": "3D card tilts preserve perspective. Shadows update during drag. Z-axis depth in stacked cards.",
        "example": "TiltedCard: perspective(1000px) rotateX() rotateY(). Shadow intensifies on tilt axis.",
        "framer": "style={{ perspective: 1000 }}. rotateX/Y with useMotionValue.",
        "when_to_use": "Tilt cards, drag interactions, 3D product showcases.",
    },
    {
        "number": 12, "name": "Appeal",
        "original": "Characters that are interesting and magnetic.",
        "ui_application": "The one animation that makes you stop and smile. Cursor effects, particle trails, magnetic buttons. One per page — restraint is the rule.",
        "example": "ImageTrail on creative portfolio. Spotlight cursor on dark hero. Aurora background on AI SaaS.",
        "framer": "useMotionValue + useSpring for cursor tracking. AnimatePresence for dramatic reveals.",
        "when_to_use": "ONE statement animation per page. The delight moment. Never more than one.",
    },
]

# ═══════════════════════════════════════════════════════════════════════
# DURATION SCIENCE TABLE
# ═══════════════════════════════════════════════════════════════════════

DURATION_TABLE = {
    "instant":   {"ms": (0, 100),    "use": "Imperceptible — background color on hover, opacity micro-changes",
                  "framer": "duration: 0.08", "tailwind": "duration-75 duration-100"},
    "fast":      {"ms": (100, 200),  "use": "Hover states, focus rings, tooltip show/hide, icon swaps",
                  "framer": "duration: 0.15", "tailwind": "duration-150"},
    "normal":    {"ms": (200, 300),  "use": "Dropdown open/close, state transitions, badge updates",
                  "framer": "duration: 0.25", "tailwind": "duration-200 duration-300"},
    "deliberate":{"ms": (300, 400),  "use": "Dialog open, drawer slide, accordion expand, tab switch",
                  "framer": "duration: 0.35", "tailwind": "duration-300 duration-[350ms]"},
    "slow":      {"ms": (400, 500),  "use": "Page section entrances, card stagger reveals, hero text",
                  "framer": "duration: 0.4",  "tailwind": "duration-400 duration-[400ms]"},
    "cinematic": {"ms": (500, 700),  "use": "Full-page transitions, dramatic hero entrances, first load",
                  "framer": "duration: 0.6",  "tailwind": "duration-500 duration-[600ms]"},
    "too-slow":  {"ms": (700, 9999), "use": "❌ Avoid for UI — feels broken, not polished",
                  "framer": "N/A",             "tailwind": "N/A"},
}

COMPONENT_DURATIONS = {
    "button-hover":     "fast (150ms)",
    "button-press":     "instant (80ms)",
    "input-focus":      "fast (150ms)",
    "tooltip":          "fast (150ms)",
    "dropdown":         "normal (200ms)",
    "badge-update":     "normal (250ms)",
    "modal-open":       "deliberate (300ms)",
    "drawer-slide":     "deliberate (350ms)",
    "accordion":        "deliberate (300ms)",
    "page-transition":  "slow (400ms)",
    "hero-entrance":    "cinematic (500-600ms)",
    "stagger-list":     "slow (400ms total, 50ms per item)",
    "success-state":    "normal (250ms)",
    "skeleton-shimmer": "cinematic (1500ms loop)",
    "spinner":          "cinematic (700ms loop, linear)",
}

# ═══════════════════════════════════════════════════════════════════════
# EASING CURVE LIBRARY
# ═══════════════════════════════════════════════════════════════════════

EASING_CURVES = {
    "entrance":        {"css": "cubic-bezier(0.16, 1, 0.3, 1)",  "framer": "[0.16, 1, 0.3, 1]",
                        "use": "Elements entering — fast start, gentle settle. The most natural UI easing."},
    "exit":            {"css": "cubic-bezier(0.5, 0, 1, 1)",     "framer": "[0.5, 0, 1, 1]",
                        "use": "Elements leaving — accelerates out, no lingering."},
    "spring":          {"css": "N/A (requires JS spring physics)", "framer": "type: 'spring', stiffness: 300, damping: 30",
                        "use": "Physical, bouncy motion. Modal open, card hover, magnetic effects."},
    "spring-gentle":   {"css": "N/A", "framer": "type: 'spring', stiffness: 120, damping: 14",
                        "use": "Gentle spring for lists and panels. Some overshoot, not playful."},
    "spring-bouncy":   {"css": "N/A", "framer": "type: 'spring', stiffness: 200, damping: 10",
                        "use": "Playful bounce for success states, notifications, delight moments."},
    "ease-out":        {"css": "cubic-bezier(0, 0, 0.2, 1)",     "framer": "[0, 0, 0.2, 1]",
                        "use": "Standard ease-out. Good default for most UI animations."},
    "ease-in":         {"css": "cubic-bezier(0.4, 0, 1, 1)",     "framer": "[0.4, 0, 1, 1]",
                        "use": "Standard ease-in. Use for exits and elements leaving viewport."},
    "linear":          {"css": "linear",                          "framer": "'linear'",
                        "use": "ONLY for continuous loops: spinners, shimmer, progress bars."},
    "smooth-expand":   {"css": "cubic-bezier(0.4, 0, 0.2, 1)",   "framer": "[0.4, 0, 0.2, 1]",
                        "use": "Accordion expand, height transitions, panel reveals."},
    "overshoot":       {"css": "cubic-bezier(0.34, 1.56, 0.64, 1)", "framer": "[0.34, 1.56, 0.64, 1]",
                        "use": "Slight overshoot without full spring. Buttons, success badges."},
}

# ═══════════════════════════════════════════════════════════════════════
# FRAMER MOTION SNIPPET LIBRARY
# ═══════════════════════════════════════════════════════════════════════

FRAMER_SNIPPETS = {
    "fade-in-up": {
        "desc": "Fade + translate up — most common entrance for sections and cards",
        "code": """const fadeInUp = {
  hidden:  { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0,
    transition: { duration: 0.4, ease: [0.16, 1, 0.3, 1] }
  }
}
// Usage:
<motion.div variants={fadeInUp} initial="hidden" animate="visible">"""
    },
    "stagger-list": {
        "desc": "Staggered list — items enter sequentially with overlap",
        "code": """const listVariants = {
  hidden:  { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.05, delayChildren: 0.1 } }
}
const itemVariants = {
  hidden:  { opacity: 0, y: 12 },
  visible: { opacity: 1, y: 0,
    transition: { duration: 0.35, ease: [0.16, 1, 0.3, 1] }
  }
}
// Usage:
<motion.ul variants={listVariants} initial="hidden" animate="visible">
  {items.map(item => (
    <motion.li key={item.id} variants={itemVariants}>{item.name}</motion.li>
  ))}
</motion.ul>"""
    },
    "modal-entrance": {
        "desc": "Modal/Dialog — scale + fade with backdrop",
        "code": """// Wrap in AnimatePresence:
const modalVariants = {
  hidden: { opacity: 0, scale: 0.95, y: 8 },
  visible: {
    opacity: 1, scale: 1, y: 0,
    transition: { duration: 0.3, ease: [0.16, 1, 0.3, 1] }
  },
  exit: {
    opacity: 0, scale: 0.95, y: 4,
    transition: { duration: 0.2, ease: [0.4, 0, 1, 1] }
  }
}
const backdropVariants = {
  hidden:  { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.2 } },
  exit:    { opacity: 0, transition: { duration: 0.2 } }
}
<AnimatePresence>
  {isOpen && (
    <>
      <motion.div variants={backdropVariants} initial="hidden" animate="visible" exit="exit"
        className="fixed inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} />
      <motion.div variants={modalVariants} initial="hidden" animate="visible" exit="exit"
        className="fixed ... your-modal-classes" >
        {children}
      </motion.div>
    </>
  )}
</AnimatePresence>"""
    },
    "magnetic-button": {
        "desc": "Magnetic cursor button — pulls toward mouse",
        "code": """"use client"
import { useRef, useState } from 'react'
import { motion } from 'framer-motion'

export function MagneticButton({ children, className, ...props }) {
  const ref = useRef(null)
  const [pos, setPos] = useState({ x: 0, y: 0 })

  const handleMouseMove = (e) => {
    const rect = ref.current.getBoundingClientRect()
    const cx   = rect.left + rect.width  / 2
    const cy   = rect.top  + rect.height / 2
    setPos({ x: (e.clientX - cx) * 0.35, y: (e.clientY - cy) * 0.35 })
  }
  const handleMouseLeave = () => setPos({ x: 0, y: 0 })

  return (
    <motion.button
      ref={ref}
      animate={{ x: pos.x, y: pos.y }}
      transition={{ type: 'spring', stiffness: 200, damping: 18, mass: 0.5 }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      whileTap={{ scale: 0.97 }}
      className={className}
      {...props}
    >
      {children}
    </motion.button>
  )
}"""
    },
    "scroll-reveal": {
        "desc": "Reveal on scroll — uses whileInView for scroll-triggered entrance",
        "code": """// No need for IntersectionObserver — Framer handles it
<motion.div
  initial={{ opacity: 0, y: 32 }}
  whileInView={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
  viewport={{ once: true, margin: '-80px' }}
>
  {/* Content revealed on scroll */}
</motion.div>

// For a grid of cards with stagger:
<motion.div
  initial="hidden"
  whileInView="visible"
  viewport={{ once: true, margin: '-60px' }}
  variants={{ visible: { transition: { staggerChildren: 0.07 } } }}
>
  {cards.map(card => (
    <motion.div key={card.id}
      variants={{ hidden: { opacity: 0, y: 24 }, visible: { opacity: 1, y: 0 } }}
      transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
    >
      <Card {...card} />
    </motion.div>
  ))}
</motion.div>"""
    },
    "page-transition": {
        "desc": "Next.js App Router page transition",
        "code": """"use client"
// In your layout or page:
import { motion, AnimatePresence } from 'framer-motion'

const pageVariants = {
  initial: { opacity: 0, y: 8 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.35, ease: [0.16, 1, 0.3, 1] } },
  exit:    { opacity: 0, y: -8, transition: { duration: 0.2, ease: [0.4, 0, 1, 1] } },
}

export function PageWrapper({ children }: { children: React.ReactNode }) {
  return (
    <motion.main
      variants={pageVariants}
      initial="initial"
      animate="animate"
      exit="exit"
    >
      {children}
    </motion.main>
  )
}"""
    },
    "counter-animation": {
        "desc": "Number counter animation (for stats sections)",
        "code": """"use client"
import { useEffect, useRef, useState } from 'react'
import { useInView, useMotionValue, useSpring, animate } from 'framer-motion'

export function Counter({ target, suffix = '' }: { target: number; suffix?: string }) {
  const ref    = useRef<HTMLSpanElement>(null)
  const inView = useInView(ref, { once: true })
  const count  = useMotionValue(0)
  const spring = useSpring(count, { stiffness: 80, damping: 20 })

  useEffect(() => {
    if (inView) count.set(target)
  }, [inView, target, count])

  useEffect(() => {
    return spring.on('change', (v) => {
      if (ref.current) ref.current.textContent = Math.round(v).toLocaleString() + suffix
    })
  }, [spring, suffix])

  return <span ref={ref}>0{suffix}</span>
}"""
    },
    "reduced-motion": {
        "desc": "prefers-reduced-motion — always wrap animations with this",
        "code": """import { useReducedMotion } from 'framer-motion'

// In your component:
const prefersReduced = useReducedMotion()

// Use as condition:
const variants = {
  hidden:  { opacity: 0, y: prefersReduced ? 0 : 20 },
  visible: { opacity: 1, y: 0 }
}

// Or globally in your root layout (globals.css):
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}"""
    },
}

# ═══════════════════════════════════════════════════════════════════════
# MOTION AUDIT — check files for animation anti-patterns
# ═══════════════════════════════════════════════════════════════════════

MOTION_ANTI_PATTERNS = [
    {"id":"MT001","sev":"Critical","pattern":r"animate-(?!none)[a-z-]+(?![^\n]*motion-reduce)",
     "msg":"Animation without prefers-reduced-motion. Add motion-reduce:animate-none."},
    {"id":"MT002","sev":"High",    "pattern":r"duration-\[(?:7[0-9][0-9]|[89][0-9][0-9]|[1-9][0-9]{3})ms\]",
     "msg":"Animation duration >700ms feels sluggish for UI. Max 600ms for dramatic, 400ms for normal."},
    {"id":"MT003","sev":"High",    "pattern":r"<motion\.[a-z]+(?![^>]*key=)[^>]*>(?=\s*\{[^}]*&&)",
     "msg":"Conditional motion element may need AnimatePresence for exit animations."},
    {"id":"MT004","sev":"Medium",  "pattern":r"transition:\s*[\"']?all\s",
     "msg":"transition:all is expensive. Specify only changed properties: transition-colors, transition-transform."},
    {"id":"MT005","sev":"Medium",  "pattern":r"linear\b(?!-gradient|\s*\()",
     "msg":"Linear easing detected. Use ease-out for entrances, ease-in for exits. Linear only for spinners."},
    {"id":"MT006","sev":"High",    "pattern":r"<AnimatePresence>(?![\s\S]{0,200}key=)",
     "msg":"AnimatePresence children need a key prop for exit animations to work."},
    {"id":"MT007","sev":"Medium",  "pattern":r"transition\s*=\s*\{\{[^}]*duration:\s*0\.[7-9]",
     "msg":"Framer duration > 0.7s is too slow for UI interactions. Keep to 0.6s max."},
]


def audit_motion(filepath: str) -> list:
    path = Path(filepath)
    if not path.exists():
        return []
    code    = path.read_text(errors="ignore")
    issues  = []
    for rule in MOTION_ANTI_PATTERNS:
        if re.search(rule["pattern"], code, re.IGNORECASE | re.MULTILINE):
            issues.append(rule)
    return issues


# ═══════════════════════════════════════════════════════════════════════
# OUTPUT FORMATTERS
# ═══════════════════════════════════════════════════════════════════════

def print_principles():
    print(f"\n  ─── Disney's 12 Principles → UI Application ────────────")
    for p in DISNEY_PRINCIPLES:
        print(f"\n  [{p['number']:02d}] {p['name']}")
        print(f"  UI:      {p['ui_application'][:70]}")
        print(f"  Example: {p['example'][:70]}")
        print(f"  Use:     {p['when_to_use'][:70]}")
    print()


def print_duration_table():
    print(f"\n  ─── Duration Science ─────────────────────────────────────")
    print(f"\n  {'Tier':<12} {'Range':>12}  Use case")
    print(f"  {'─'*60}")
    for tier, data in DURATION_TABLE.items():
        ms = f"{data['ms'][0]}–{data['ms'][1]}ms"
        print(f"  {tier:<12} {ms:>12}  {data['use'][:45]}")
    print(f"\n  Component reference:")
    for comp, dur in COMPONENT_DURATIONS.items():
        print(f"  {comp.replace('-',' '):<24} {dur}")
    print()


def print_easing(filter_key: str = None):
    print(f"\n  ─── Easing Curve Library ────────────────────────────────")
    for key, data in EASING_CURVES.items():
        if filter_key and filter_key not in key:
            continue
        print(f"\n  [{key}]")
        print(f"  CSS:    {data['css']}")
        print(f"  Framer: {data['framer']}")
        print(f"  Use:    {data['use']}")
    print()


def print_snippet(name: str):
    snip = FRAMER_SNIPPETS.get(name)
    if not snip:
        print(f"\n  Unknown snippet: {name}")
        print(f"  Available: {', '.join(FRAMER_SNIPPETS.keys())}")
        return
    print(f"\n  ─── {name} ──────────────────────────────────────────────")
    print(f"  {snip['desc']}\n")
    print(snip['code'])
    print()


def print_component_motion(component: str, style: str):
    comp = component.lower()
    style_l = style.lower()
    print(f"\n  ─── Motion for {component} ({style}) ─────────────────────")

    if "hover" in style_l:
        print(f"\n  Hover animation for {component}:")
        if "card" in comp:
            print(f"  whileHover={{ scale: 1.02, y: -4 }}")
            print(f"  transition={{ type: 'spring', stiffness: 300, damping: 20 }}")
            print(f"  ⚠️  Add overflow-hidden on parent to prevent layout shift")
        elif "button" in comp:
            print(f"  whileHover={{ y: -1 }}")
            print(f"  whileTap={{ scale: 0.97, y: 0 }}")
            print(f"  transition={{ duration: 0.15, ease: [0.16, 1, 0.3, 1] }}")
        else:
            print(f"  whileHover={{ opacity: 0.85 }}")
            print(f"  transition={{ duration: 0.15 }}")

    elif "entrance" in style_l:
        print(f"\n  Entrance animation for {component}:")
        print(f"  initial={{ opacity: 0, y: 20 }}")
        print(f"  animate={{ opacity: 1, y: 0 }}")
        print(f"  transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}")
        if "hero" in comp:
            print(f"\n  For hero: use SplitText from React Bits for staggered headline.")
            print(f"  Sub-text: BlurText from React Bits for blur→sharp reveal.")
            print(f"  CTA: delay 0.5s entrance so headline is read first.")
        elif "list" in comp:
            print(f"\n  For list: staggerChildren: 0.05 in parent variants.")
            print_snippet("stagger-list")

    elif "scroll" in style_l:
        print_snippet("scroll-reveal")

    elif "exit" in style_l:
        print(f"\n  Exit animation for {component}:")
        print(f"  exit={{ opacity: 0, y: -8, scale: 0.98 }}")
        print(f"  transition={{ duration: 0.2, ease: [0.4, 0, 1, 1] }}")
        print(f"  ⚠️  Must be wrapped in <AnimatePresence> with key prop")
    print()


def main():
    parser = argparse.ArgumentParser(description="/motion — Animation Intelligence Engine")
    parser.add_argument("--component", "-c", help="Component to animate (hero, card, button, list, modal)")
    parser.add_argument("--style",     "-s", default="entrance", help="Animation style: entrance|hover|exit|scroll")
    parser.add_argument("--duration",  "-d", help="Duration recommendations for a context")
    parser.add_argument("--easing",    "-e", help="Easing curve recommendations (filter by keyword)")
    parser.add_argument("--audit",     "-a", help="Audit a file for motion anti-patterns")
    parser.add_argument("--principles",      action="store_true", help="Show Disney 12 principles")
    parser.add_argument("--snippets",        help="Show Framer Motion snippets (name or 'all')")
    args = parser.parse_args()

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║        /motion — Animation Intelligence Engine      ║")
    print("╚══════════════════════════════════════════════════════╝")

    if args.principles:
        print_principles()

    elif args.duration:
        print_duration_table()

    elif args.easing:
        print_easing(args.easing if args.easing != "all" else None)

    elif args.snippets:
        if args.snippets == "all":
            for name in FRAMER_SNIPPETS:
                print_snippet(name)
        else:
            print_snippet(args.snippets)

    elif args.audit:
        issues = audit_motion(args.audit)
        if not issues:
            print(f"\n  ✅ No motion issues found in {args.audit}\n")
        else:
            print(f"\n  Motion issues in {args.audit} ({len(issues)}):")
            for i in issues:
                icon = "🔴" if i["sev"]=="Critical" else "🟠" if i["sev"]=="High" else "🟡"
                print(f"  {icon} [{i['id']}] {i['msg']}")
            print()

    elif args.component:
        print_component_motion(args.component, args.style)

    else:
        print(f"\n  ─── Commands ────────────────────────────────────────")
        print(f"  --principles                     Disney 12 → UI")
        print(f"  --duration                       Duration science table")
        print(f"  --easing [keyword]               Easing curve library")
        print(f"  --snippets [name|all]            Framer Motion snippets")
        print(f"  --component hero --style entrance Component motion")
        print(f"  --audit src/Hero.tsx             Motion anti-pattern check")
        print(f"\n  Snippet names: {', '.join(FRAMER_SNIPPETS.keys())}\n")


if __name__ == "__main__":
    main()
