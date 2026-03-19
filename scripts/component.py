#!/usr/bin/env python3
"""
/component — Isolated Component Generator v1.0
Phase 5.1 — God-Level Roadmap

Generate any single production-ready component on demand.
Runs the full design system workflow scoped to one component.
Auto-reviews output and reports score.

Usage:
  python3 component.py PricingCard --style dark-premium --framework nextjs
  python3 component.py HeroSection --style minimal-light
  python3 component.py AuthForm --style split-screen --dark
  python3 component.py NavBar --style sticky-blur
  python3 component.py DataTable --framework nextjs
  python3 component.py --list
"""

import sys, json, argparse, subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from core import resolve_product, select_components, search_ux_laws

# ═══════════════════════════════════════════════════════════════════════
# COMPONENT LIBRARY — 40+ templates
# ═══════════════════════════════════════════════════════════════════════

COMPONENT_LIBRARY = {
    # ── MARKETING ───────────────────────────────────────────────────
    "HeroSection": {
        "category": "Marketing",
        "desc": "Full-viewport hero with headline, sub-text, dual CTAs, social proof",
        "required_libs": ["framer-motion"],
        "statement_components": ["Aurora (React Bits)", "SplitText (React Bits)", "BlurText (React Bits)", "ShimmerButton (Magic UI)"],
        "props": ["headline", "subheadline", "ctaPrimary", "ctaSecondary", "badge"],
        "a11y": ["aria-labelledby on section", "role=heading on h1", "aria-label on CTAs"],
        "variants": ["dark-aurora", "light-grid", "editorial-serif", "glassmorphism"],
    },
    "FeatureGrid": {
        "category": "Marketing",
        "desc": "3-column feature grid with icons, titles, descriptions",
        "required_libs": ["framer-motion"],
        "statement_components": ["SpotlightCard (React Bits)", "FadeContent (React Bits)"],
        "props": ["features[]", "columns", "style"],
        "a11y": ["role=list on grid", "aria-label on section"],
    },
    "TestimonialGrid": {
        "category": "Marketing",
        "desc": "Testimonial cards with avatar, quote, name, role",
        "statement_components": ["BounceCards (React Bits)", "MarqueeComponent (Magic UI)"],
        "props": ["testimonials[]", "layout"],
        "a11y": ["blockquote semantics", "cite element for attribution"],
    },
    "PricingTable": {
        "category": "Marketing",
        "desc": "3-tier pricing with monthly/annual toggle, popular badge, feature list",
        "required_libs": ["framer-motion"],
        "statement_components": ["StarBorder (React Bits)"],
        "props": ["plans[]", "billingToggle", "currency"],
        "a11y": ["aria-label on pricing cards", "aria-pressed on toggle"],
    },
    "LogoStrip": {
        "category": "Marketing",
        "desc": "Infinite scrolling logo strip with 'Trusted by' label",
        "statement_components": ["MarqueeComponent (Magic UI)", "ScrollVelocity (React Bits)"],
        "props": ["logos[]", "speed", "label"],
    },
    "CTASection": {
        "category": "Marketing",
        "desc": "Full-width CTA section with gradient background and dual buttons",
        "statement_components": ["Orb (React Bits)", "ShimmerButton (Magic UI)"],
        "props": ["headline", "subtext", "ctaPrimary", "ctaSecondary"],
    },
    "StatsRow": {
        "category": "Marketing",
        "desc": "4-stat metrics row with animated number counters",
        "statement_components": ["CountUp (React Bits)", "NumberTicker (Magic UI)"],
        "props": ["stats[]"],
        "a11y": ["aria-label for each stat", "role=list"],
    },
    "FAQAccordion": {
        "category": "Marketing",
        "desc": "Expandable FAQ accordion with smooth animation",
        "statement_components": ["shadcn: Accordion"],
        "props": ["faqs[]"],
        "a11y": ["aria-expanded", "aria-controls", "role=region"],
    },
    "TeamGrid": {
        "category": "Marketing",
        "desc": "Team member cards with photo, name, role, social links",
        "statement_components": ["TiltedCard (React Bits)"],
        "props": ["members[]", "columns"],
        "a11y": ["img alt text", "aria-label on social links"],
    },
    # ── APP UI ───────────────────────────────────────────────────────
    "NavBar": {
        "category": "App UI",
        "desc": "Sticky top nav with logo, links, mobile menu, CTA button",
        "required_libs": ["framer-motion"],
        "statement_components": ["FlowingMenu (React Bits) for mobile", "FloatingNavbar (Aceternity) for sticky scroll"],
        "props": ["links[]", "ctaLabel", "logo", "sticky"],
        "a11y": ["role=navigation", "aria-label='Main navigation'", "aria-current on active"],
    },
    "Sidebar": {
        "category": "App UI",
        "desc": "Fixed app sidebar with nav items, active state, user profile",
        "statement_components": ["shadcn: Sidebar"],
        "props": ["navItems[]", "user", "collapsed"],
        "a11y": ["role=navigation", "aria-current on active item"],
    },
    "DataTable": {
        "category": "App UI",
        "desc": "Sortable, filterable data table with pagination",
        "required_libs": ["@tanstack/react-table"],
        "statement_components": ["shadcn: DataTable", "Origin UI inputs for filter"],
        "props": ["columns[]", "data[]", "pageSize"],
        "a11y": ["role=table", "aria-sort on sortable columns", "scope=col on headers"],
    },
    "KPICard": {
        "category": "App UI",
        "desc": "Metric card with value, trend indicator, sparkline",
        "statement_components": ["CountUp (React Bits)", "NumberTicker (Magic UI)"],
        "props": ["label", "value", "change", "trend", "unit"],
        "a11y": ["aria-label with full metric description"],
    },
    "EmptyState": {
        "category": "App UI",
        "desc": "Empty state with illustration, headline, description, action",
        "statement_components": ["FadeContent (React Bits)", "Orb (React Bits) as ambient bg"],
        "props": ["icon", "headline", "description", "actionLabel", "onAction"],
        "a11y": ["role=status", "aria-live=polite"],
    },
    "LoadingState": {
        "category": "App UI",
        "desc": "Skeleton loader that previews the content shape",
        "statement_components": ["shadcn: Skeleton"],
        "props": ["variant", "lines", "showAvatar"],
        "a11y": ["role=status", "aria-busy=true", "aria-label='Loading content'"],
    },
    "SearchBar": {
        "category": "App UI",
        "desc": "Search input with icon, keyboard shortcut badge, suggestions",
        "statement_components": ["shadcn: Command", "Origin UI search input"],
        "props": ["placeholder", "shortcut", "onSearch", "suggestions[]"],
        "a11y": ["role=search", "aria-label", "aria-autocomplete"],
    },
    "NotificationCenter": {
        "category": "App UI",
        "desc": "Notification dropdown with unread badge and list",
        "statement_components": ["shadcn: Popover", "AnimatedList (Magic UI)"],
        "props": ["notifications[]", "onMarkRead", "onClearAll"],
        "a11y": ["role=log", "aria-live=polite", "aria-label on bell button"],
    },
    # ── FORMS ────────────────────────────────────────────────────────
    "LoginForm": {
        "category": "Forms",
        "desc": "Email + password login with social auth buttons, validation",
        "required_libs": ["react-hook-form", "zod"],
        "statement_components": ["Origin UI inputs", "shadcn: Form"],
        "props": ["onSubmit", "onSocialAuth", "forgotPasswordHref"],
        "a11y": ["labels on all inputs", "aria-invalid on error", "role=alert for errors"],
    },
    "SignupForm": {
        "category": "Forms",
        "desc": "Registration form with validation and password strength indicator",
        "required_libs": ["react-hook-form", "zod"],
        "statement_components": ["Origin UI inputs", "shadcn: Form"],
        "props": ["onSubmit", "onSocialAuth", "requireTerms"],
        "a11y": ["aria-describedby for requirements", "password strength announcement"],
    },
    "ContactForm": {
        "category": "Forms",
        "desc": "Contact form with name, email, subject, message, submit",
        "required_libs": ["react-hook-form", "zod"],
        "statement_components": ["Origin UI inputs", "shadcn: Form", "AnimatedSubscribeButton (Magic UI)"],
        "props": ["onSubmit", "successMessage"],
        "a11y": ["visible labels", "required field marking", "error summaries"],
    },
    "MultiStepForm": {
        "category": "Forms",
        "desc": "Multi-step wizard with progress indicator and step validation",
        "required_libs": ["react-hook-form", "zod", "framer-motion"],
        "statement_components": ["shadcn: Form", "Zeigarnik progress bar"],
        "props": ["steps[]", "onComplete", "allowBack"],
        "a11y": ["aria-current=step", "progress role", "step announcement on change"],
    },
    # ── FEEDBACK ─────────────────────────────────────────────────────
    "ToastNotification": {
        "category": "Feedback",
        "desc": "Toast notifications for success, error, warning, info",
        "statement_components": ["shadcn: Sonner"],
        "props": ["type", "message", "description", "duration"],
        "a11y": ["role=status", "aria-live=polite for info", "aria-live=assertive for errors"],
    },
    "AlertBanner": {
        "category": "Feedback",
        "desc": "Inline alert banner with icon, message, dismiss button",
        "statement_components": ["shadcn: Alert"],
        "props": ["variant", "title", "message", "dismissible"],
        "a11y": ["role=alert", "aria-live=assertive"],
    },
    "ConfirmDialog": {
        "category": "Feedback",
        "desc": "Confirmation dialog for destructive actions",
        "statement_components": ["shadcn: AlertDialog"],
        "props": ["title", "description", "confirmLabel", "cancelLabel", "onConfirm", "destructive"],
        "a11y": ["DialogTitle required", "role=alertdialog", "focus trap"],
    },
    "ProgressBar": {
        "category": "Feedback",
        "desc": "Animated progress bar with label and percentage",
        "statement_components": ["shadcn: Progress", "BorderBeam (Magic UI) for active"],
        "props": ["value", "max", "label", "showPercent", "animated"],
        "a11y": ["role=progressbar", "aria-valuenow", "aria-valuemin", "aria-valuemax"],
    },
    # ── CARDS ────────────────────────────────────────────────────────
    "ProductCard": {
        "category": "Cards",
        "desc": "E-commerce product card with image, name, price, add to cart",
        "statement_components": ["TiltedCard (React Bits)"],
        "props": ["image", "name", "price", "badge", "onAddToCart"],
        "a11y": ["img alt", "aria-label on button", "price sr-only announcement"],
    },
    "BlogCard": {
        "category": "Cards",
        "desc": "Article card with cover, category tag, title, excerpt, author",
        "statement_components": ["MagicCard (Magic UI)"],
        "props": ["cover", "category", "title", "excerpt", "author", "date", "href"],
        "a11y": ["card as article element", "heading hierarchy", "date as time element"],
    },
    "PricingCard": {
        "category": "Cards",
        "desc": "Single pricing tier card with features list and CTA",
        "statement_components": ["StarBorder (React Bits) for popular", "MovingBorder (Aceternity) for featured"],
        "props": ["name", "price", "period", "description", "features[]", "ctaLabel", "popular"],
        "a11y": ["aria-label with plan name + price", "list semantics for features"],
    },
    "ProfileCard": {
        "category": "Cards",
        "desc": "User profile card with avatar, name, role, stats, actions",
        "statement_components": ["TiltedCard (React Bits)", "AnimatedTooltip (Aceternity)"],
        "props": ["avatar", "name", "role", "stats[]", "actions[]"],
        "a11y": ["img alt", "dl for stats", "aria-label on action buttons"],
    },
    "FeatureCard": {
        "category": "Cards",
        "desc": "Feature highlight card with icon, title, description",
        "statement_components": ["SpotlightCard (React Bits)", "MagicCard (Magic UI)"],
        "props": ["icon", "title", "description", "link", "variant"],
        "a11y": ["icon aria-hidden", "heading in card"],
    },
}

# ═══════════════════════════════════════════════════════════════════════
# CODE GENERATORS — one per component type
# ═══════════════════════════════════════════════════════════════════════

def gen_pricing_card(T: dict, framework: str, style: str) -> str:
    is_next = "next" in framework
    directive = "'use client'\n" if is_next else ""
    p = T.get("primary","#6366F1")
    return f"""{directive}/**
 * PricingCard — Generated by /component {datetime.now().strftime('%Y-%m-%d')}
 * Install: npx shadcn@latest add "https://reactbits.dev/r/StarBorder"
 */
import {{ motion }} from 'framer-motion'
// import StarBorder from '@/components/ui/star-border'

interface Feature {{
  text: string
  included: boolean
}}

interface PricingCardProps {{
  name: string
  price: string
  period?: string
  description: string
  features: Feature[]
  ctaLabel: string
  popular?: boolean
  onSelect?: () => void
}}

export default function PricingCard({{
  name, price, period = '/month', description,
  features, ctaLabel, popular = false, onSelect,
}}: PricingCardProps) {{
  return (
    <motion.div
      initial={{{{ opacity: 0, y: 20 }}}}
      animate={{{{ opacity: 1, y: 0 }}}}
      transition={{{{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}}}
      className={{`relative flex flex-col rounded-2xl border p-8 transition-all duration-200
        ${{popular
          ? 'border-[var(--color-primary)] shadow-[0_0_40px_var(--color-primary)/20] scale-[1.03]'
          : 'border-[var(--color-border)] hover:border-[var(--color-primary)/40]'
        }}`}}
      style={{{{ background: 'var(--color-surface)' }}}}
      aria-label={{`${{name}} plan — ${{price}}${{period}}`}}
    >
      {{popular && (
        <div
          className="absolute -top-3.5 left-1/2 -translate-x-1/2 rounded-full px-4 py-1 text-xs font-bold text-white"
          style={{{{ background: 'var(--color-primary)' }}}}
          aria-label="Most popular plan"
        >
          Most Popular
        </div>
      )}}

      <div className="mb-6">
        <h3 className="font-heading text-lg font-bold" style={{{{ color: 'var(--color-text)' }}}}>
          {{name}}
        </h3>
        <div className="mt-3 flex items-baseline gap-1">
          <span className="font-heading text-4xl font-extrabold" style={{{{ color: popular ? 'var(--color-primary)' : 'var(--color-text)' }}}}>
            {{price}}
          </span>
          {{period && (
            <span className="text-sm font-medium" style={{{{ color: 'var(--color-muted)' }}}}>
              {{period}}
            </span>
          )}}
        </div>
        <p className="mt-2 text-sm leading-relaxed" style={{{{ color: 'var(--color-muted)' }}}}>
          {{description}}
        </p>
      </div>

      <ul className="mb-8 flex-1 space-y-3" role="list" aria-label={{`Features included in ${{name}} plan`}}>
        {{features.map((feature, i) => (
          <li key={{i}} className="flex items-start gap-3 text-sm">
            <span
              className={{`mt-0.5 flex-shrink-0 text-base ${{feature.included ? 'text-green-500' : 'opacity-30'}}`}}
              aria-hidden="true"
            >
              {{feature.included ? '✓' : '✗'}}
            </span>
            <span style={{{{ color: feature.included ? 'var(--color-text)' : 'var(--color-muted)' }}}}>
              {{feature.text}}
              {{!feature.included && <span className="sr-only"> (not included)</span>}}
            </span>
          </li>
        ))}}
      </ul>

      <button
        onClick={{onSelect}}
        className={{`inline-flex min-h-[48px] w-full cursor-pointer items-center justify-center rounded-xl
          px-6 py-3 text-sm font-semibold transition-all duration-150
          focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-primary)] focus-visible:ring-offset-2
          ${{popular
            ? 'bg-[var(--color-primary)] text-white hover:bg-[var(--color-primary)]/90 hover:-translate-y-0.5 hover:shadow-lg motion-reduce:hover:translate-y-0'
            : 'border border-[var(--color-border)] bg-transparent hover:border-[var(--color-primary)] hover:bg-[var(--color-primary)/8]'
          }}`}}
        style={{{{ color: popular ? '#fff' : 'var(--color-text)' }}}}
      >
        {{ctaLabel}}
      </button>
    </motion.div>
  )
}}
"""

def gen_stats_row(T: dict, framework: str, style: str) -> str:
    is_next = "next" in framework
    directive = "'use client'\n" if is_next else ""
    p = T.get("primary","#6366F1")
    return f"""{directive}/**
 * StatsRow — Generated by /component {datetime.now().strftime('%Y-%m-%d')}
 * Install: npx shadcn@latest add "https://reactbits.dev/r/CountUp"
 */
import {{ useRef }} from 'react'
import {{ motion, useInView }} from 'framer-motion'
// import CountUp from '@/components/ui/count-up'

interface Stat {{
  label: string
  value: number
  suffix?: string
  prefix?: string
  description?: string
}}

interface StatsRowProps {{
  stats: Stat[]
  title?: string
}}

function AnimatedStat({{ stat, index }}: {{ stat: Stat; index: number }}) {{
  const ref  = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, {{ once: true, margin: '-80px' }})

  return (
    <motion.div
      ref={{ref}}
      initial={{{{ opacity: 0, y: 16 }}}}
      animate={{{{ opacity: inView ? 1 : 0, y: inView ? 0 : 16 }}}}
      transition={{{{ delay: index * 0.1, duration: 0.5, ease: [0.16, 1, 0.3, 1] }}}}
      className="flex flex-col items-center gap-2 text-center"
      aria-label={{`${{stat.label}}: ${{stat.prefix ?? ''}}${{stat.value.toLocaleString()}}${{stat.suffix ?? ''}}`}}
    >
      <div className="font-heading text-4xl font-extrabold md:text-5xl" style={{{{ color: 'var(--color-primary)' }}}}>
        {{stat.prefix && <span>{{stat.prefix}}</span>}}
        {{/* Replace with: <CountUp end={{stat.value}} suffix={{stat.suffix}} /> */}}
        <motion.span>
          {{inView ? stat.value.toLocaleString() : '0'}}
        </motion.span>
        {{stat.suffix && <span>{{stat.suffix}}</span>}}
      </div>
      <p className="text-sm font-semibold uppercase tracking-widest" style={{{{ color: 'var(--color-muted)' }}}}>
        {{stat.label}}
      </p>
      {{stat.description && (
        <p className="max-w-[140px] text-xs leading-relaxed" style={{{{ color: 'var(--color-muted)' }}}}>
          {{stat.description}}
        </p>
      )}}
    </motion.div>
  )
}}

export default function StatsRow({{ stats, title }}: StatsRowProps) {{
  return (
    <section
      className="py-16 md:py-24"
      aria-label={{title ?? 'Key metrics'}}
    >
      <div className="container mx-auto px-4">
        {{title && (
          <p className="mb-12 text-center text-xs font-bold uppercase tracking-[.12em]"
            style={{{{ color: 'var(--color-muted)' }}}}>
            {{title}}
          </p>
        )}}
        <dl className="grid grid-cols-2 gap-8 md:grid-cols-4">
          {{stats.map((stat, i) => (
            <div key={{i}}>
              <AnimatedStat stat={{stat}} index={{i}} />
            </div>
          ))}}
        </dl>
      </div>
    </section>
  )
}}
"""

def gen_navbar(T: dict, framework: str, style: str) -> str:
    is_next = "next" in framework
    directive = "'use client'\n" if is_next else ""
    link_comp  = "Link"  if is_next else "a"
    link_import = "\nimport Link from 'next/link'" if is_next else ""
    p = T.get("primary","#6366F1")
    return f"""{directive}/**
 * NavBar — Generated by /component {datetime.now().strftime('%Y-%m-%d')}
 * For mobile menu: npx shadcn@latest add "https://reactbits.dev/r/FlowingMenu"
 */
import {{ useState, useEffect }} from 'react'{link_import}
import {{ motion, AnimatePresence }} from 'framer-motion'
import {{ Menu, X }} from 'lucide-react'

interface NavLink {{
  label: string
  href: string
}}

interface NavBarProps {{
  logo?: string
  links?: NavLink[]
  ctaLabel?: string
  ctaHref?: string
}}

export default function NavBar({{
  logo = 'YourBrand',
  links = [
    {{ label: 'Features', href: '#features' }},
    {{ label: 'Pricing',  href: '#pricing'  }},
    {{ label: 'Docs',     href: '/docs'     }},
    {{ label: 'Blog',     href: '/blog'     }},
  ],
  ctaLabel = 'Get Started',
  ctaHref  = '/signup',
}}: NavBarProps) {{
  const [open,     setOpen]     = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {{
    const handler = () => setScrolled(window.scrollY > 16)
    window.addEventListener('scroll', handler, {{ passive: true }})
    return () => window.removeEventListener('scroll', handler)
  }}, [])

  return (
    <header
      className={{`fixed inset-x-0 top-0 z-50 transition-all duration-300
        ${{scrolled
          ? 'border-b border-[var(--color-border)] bg-[var(--color-bg)]/90 backdrop-blur-md shadow-sm'
          : 'bg-transparent'
        }}`}}
      role="banner"
    >
      <div className="container mx-auto flex h-16 items-center justify-between px-4 sm:px-6">

        {{/* Logo */}}
        <{link_comp} href="/" className="font-heading text-xl font-extrabold" style={{{{ color: 'var(--color-primary)' }}}}>
          {{logo}}
        </{link_comp}>

        {{/* Desktop nav */}}
        <nav className="hidden items-center gap-8 md:flex" aria-label="Main navigation">
          {{links.map(link => (
            <{link_comp}
              key={{link.href}}
              href={{link.href}}
              className="text-sm font-medium transition-colors duration-150 hover:text-[var(--color-primary)]"
              style={{{{ color: 'var(--color-muted)' }}}}
            >
              {{link.label}}
            </{link_comp}>
          ))}}
        </nav>

        {{/* Desktop CTA */}}
        <div className="hidden items-center gap-4 md:flex">
          <{link_comp}
            href={{ctaHref}}
            className="inline-flex min-h-[40px] cursor-pointer items-center rounded-[var(--radius-md)]
              px-5 py-2 text-sm font-semibold text-white transition-all duration-150
              hover:-translate-y-px hover:opacity-90 motion-reduce:hover:translate-y-0
              focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-primary)] focus-visible:ring-offset-2"
            style={{{{ background: 'var(--color-primary)' }}}}
          >
            {{ctaLabel}} →
          </{link_comp}>
        </div>

        {{/* Mobile menu button */}}
        <button
          className="flex h-10 w-10 cursor-pointer items-center justify-center rounded-lg
            transition-colors hover:bg-[var(--color-surface)] md:hidden
            focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-primary)]"
          onClick={{() => setOpen(!open)}}
          aria-expanded={{open}}
          aria-controls="mobile-menu"
          aria-label={{open ? 'Close navigation menu' : 'Open navigation menu'}}
        >
          {{open
            ? <X className="size-5" style={{{{ color: 'var(--color-text)' }}}} aria-hidden="true" />
            : <Menu className="size-5" style={{{{ color: 'var(--color-text)' }}}} aria-hidden="true" />
          }}
        </button>
      </div>

      {{/* Mobile menu */}}
      <AnimatePresence>
        {{open && (
          <motion.div
            id="mobile-menu"
            initial={{{{ opacity: 0, height: 0 }}}}
            animate={{{{ opacity: 1, height: 'auto' }}}}
            exit={{{{ opacity: 0, height: 0 }}}}
            transition={{{{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}}}
            className="overflow-hidden border-b border-[var(--color-border)] md:hidden"
            style={{{{ background: 'var(--color-bg)' }}}}
          >
            <nav className="flex flex-col gap-1 p-4" aria-label="Mobile navigation">
              {{links.map(link => (
                <{link_comp}
                  key={{link.href}}
                  href={{link.href}}
                  className="rounded-lg px-4 py-3 text-sm font-medium transition-colors
                    hover:bg-[var(--color-surface)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-primary)]"
                  style={{{{ color: 'var(--color-text)' }}}}
                  onClick={{() => setOpen(false)}}
                >
                  {{link.label}}
                </{link_comp}>
              ))}}
              <{link_comp}
                href={{ctaHref}}
                className="mt-2 inline-flex min-h-[48px] cursor-pointer items-center justify-center rounded-xl
                  text-sm font-bold text-white transition-opacity hover:opacity-90
                  focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-primary)]"
                style={{{{ background: 'var(--color-primary)' }}}}
              >
                {{ctaLabel}} →
              </{link_comp}>
            </nav>
          </motion.div>
        )}}
      </AnimatePresence>
    </header>
  )
}}
"""

def gen_empty_state(T: dict, framework: str, style: str) -> str:
    is_next = "next" in framework
    directive = "'use client'\n" if is_next else ""
    return f"""{directive}/**
 * EmptyState — Generated by /component {datetime.now().strftime('%Y-%m-%d')}
 */
import {{ motion }} from 'framer-motion'
import {{ type LucideIcon }} from 'lucide-react'

interface EmptyStateProps {{
  icon: LucideIcon
  headline: string
  description: string
  actionLabel?: string
  onAction?: () => void
  secondaryLabel?: string
  onSecondary?: () => void
}}

export default function EmptyState({{
  icon: Icon,
  headline,
  description,
  actionLabel,
  onAction,
  secondaryLabel,
  onSecondary,
}}: EmptyStateProps) {{
  return (
    <motion.div
      role="status"
      aria-label={{headline}}
      className="flex flex-col items-center py-24 text-center"
      initial={{{{ opacity: 0, y: 16 }}}}
      animate={{{{ opacity: 1, y: 0 }}}}
      transition={{{{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}}}
    >
      {{/* Icon container with ambient glow */}}
      <div
        className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl"
        style={{{{ background: 'var(--color-primary)/10', border: '1px solid var(--color-primary)/20' }}}}
      >
        <Icon
          className="size-7"
          style={{{{ color: 'var(--color-primary)' }}}}
          aria-hidden="true"
        />
      </div>

      <h3
        className="mb-2 font-heading text-xl font-semibold"
        style={{{{ color: 'var(--color-text)' }}}}
      >
        {{headline}}
      </h3>
      <p
        className="mb-8 max-w-sm text-sm leading-relaxed"
        style={{{{ color: 'var(--color-muted)' }}}}
      >
        {{description}}
      </p>

      {{(actionLabel || secondaryLabel) && (
        <div className="flex flex-wrap items-center justify-center gap-3">
          {{actionLabel && (
            <button
              onClick={{onAction}}
              className="inline-flex min-h-[44px] cursor-pointer items-center gap-2 rounded-[var(--radius-md)]
                px-6 py-2.5 text-sm font-semibold text-white transition-all duration-150
                hover:-translate-y-px hover:opacity-90 motion-reduce:hover:translate-y-0
                focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-primary)] focus-visible:ring-offset-2"
              style={{{{ background: 'var(--color-primary)' }}}}
            >
              {{actionLabel}}
            </button>
          )}}
          {{secondaryLabel && (
            <button
              onClick={{onSecondary}}
              className="inline-flex min-h-[44px] cursor-pointer items-center rounded-[var(--radius-md)]
                border border-[var(--color-border)] bg-transparent px-6 py-2.5 text-sm font-medium
                transition-all duration-150 hover:border-[var(--color-primary)] hover:bg-[var(--color-surface)]
                focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-primary)] focus-visible:ring-offset-2"
              style={{{{ color: 'var(--color-text)' }}}}
            >
              {{secondaryLabel}}
            </button>
          )}}
        </div>
      )}}
    </motion.div>
  )
}}
"""

def gen_kpi_card(T: dict, framework: str, style: str) -> str:
    is_next = "next" in framework
    directive = "'use client'\n" if is_next else ""
    return f"""{directive}/**
 * KPICard — Generated by /component {datetime.now().strftime('%Y-%m-%d')}
 * Install: npx shadcn@latest add "https://reactbits.dev/r/CountUp"
 */
import {{ motion }} from 'framer-motion'
import {{ TrendingUp, TrendingDown, Minus, type LucideIcon }} from 'lucide-react'

interface KPICardProps {{
  label: string
  value: string | number
  change?: number
  changePeriod?: string
  unit?: string
  icon?: LucideIcon
  loading?: boolean
}}

export default function KPICard({{
  label, value, change, changePeriod = 'vs last month',
  unit = '', icon: Icon, loading = false,
}}: KPICardProps) {{
  const isPositive = (change ?? 0) > 0
  const isNeutral  = (change ?? 0) === 0
  const TrendIcon  = isNeutral ? Minus : isPositive ? TrendingUp : TrendingDown
  const trendColor = isNeutral ? 'var(--color-muted)' : isPositive ? '#22C55E' : '#EF4444'

  if (loading) {{
    return (
      <div
        className="animate-pulse rounded-xl border p-5 motion-reduce:animate-none"
        style={{{{ background: 'var(--color-surface)', borderColor: 'var(--color-border)' }}}}
        role="status"
        aria-label="Loading metric"
      >
        <div className="mb-3 h-3 w-24 rounded" style={{{{ background: 'var(--color-border)' }}}} />
        <div className="mb-2 h-8 w-32 rounded" style={{{{ background: 'var(--color-border)' }}}} />
        <div className="h-3 w-20 rounded" style={{{{ background: 'var(--color-border)' }}}} />
      </div>
    )
  }}

  return (
    <motion.div
      className="rounded-xl border p-5 transition-all duration-200 hover:shadow-md"
      style={{{{ background: 'var(--color-surface)', borderColor: 'var(--color-border)' }}}}
      initial={{{{ opacity: 0, y: 12 }}}}
      animate={{{{ opacity: 1, y: 0 }}}}
      transition={{{{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}}}
      aria-label={{`${{label}}: ${{value}}${{unit}}${{change !== undefined ? `, ${{isPositive ? 'up' : 'down'}} ${{Math.abs(change)}}% ${{changePeriod}}` : ''}}`}}
    >
      <div className="mb-3 flex items-center justify-between">
        <p
          className="text-xs font-bold uppercase tracking-widest"
          style={{{{ color: 'var(--color-muted)' }}}}
        >
          {{label}}
        </p>
        {{Icon && (
          <div
            className="flex h-8 w-8 items-center justify-center rounded-lg"
            style={{{{ background: 'var(--color-primary)/12' }}}}
          >
            <Icon className="size-4" style={{{{ color: 'var(--color-primary)' }}}} aria-hidden="true" />
          </div>
        )}}
      </div>

      <p className="mb-2 font-heading text-3xl font-extrabold" style={{{{ color: 'var(--color-text)' }}}}>
        {{typeof value === 'number' ? value.toLocaleString() : value}}
        {{unit && <span className="text-lg font-semibold" style={{{{ color: 'var(--color-muted)' }}}}>{{unit}}</span>}}
      </p>

      {{change !== undefined && (
        <div className="flex items-center gap-1.5 text-xs font-semibold" style={{{{ color: trendColor }}}}>
          <TrendIcon className="size-3.5" aria-hidden="true" />
          <span>
            {{isPositive ? '+' : ''}}{{change}}% {{changePeriod}}
          </span>
        </div>
      )}}
    </motion.div>
  )
}}
"""

def gen_alert_banner(T: dict, framework: str, style: str) -> str:
    is_next = "next" in framework
    directive = "'use client'\n" if is_next else ""
    return f"""{directive}/**
 * AlertBanner — Generated by /component {datetime.now().strftime('%Y-%m-%d')}
 */
import {{ useState }} from 'react'
import {{ motion, AnimatePresence }} from 'framer-motion'
import {{ X, CheckCircle, AlertTriangle, XCircle, Info }} from 'lucide-react'

type AlertVariant = 'success' | 'warning' | 'error' | 'info'

const VARIANTS: Record<AlertVariant, {{ icon: typeof Info; bg: string; border: string; text: string; iconColor: string }}> = {{
  success: {{ icon: CheckCircle, bg: '#F0FDF4', border: '#86EFAC', text: '#14532D', iconColor: '#22C55E' }},
  warning: {{ icon: AlertTriangle, bg: '#FFFBEB', border: '#FCD34D', text: '#78350F', iconColor: '#F59E0B' }},
  error:   {{ icon: XCircle,       bg: '#FEF2F2', border: '#FCA5A5', text: '#7F1D1D', iconColor: '#EF4444' }},
  info:    {{ icon: Info,          bg: '#EFF6FF', border: '#93C5FD', text: '#1E3A8A', iconColor: '#3B82F6' }},
}}

interface AlertBannerProps {{
  variant?: AlertVariant
  title: string
  message?: string
  dismissible?: boolean
  onDismiss?: () => void
}}

export default function AlertBanner({{
  variant = 'info', title, message, dismissible = true, onDismiss,
}}: AlertBannerProps) {{
  const [visible, setVisible] = useState(true)
  const cfg = VARIANTS[variant]
  const Icon = cfg.icon

  const handleDismiss = () => {{
    setVisible(false)
    onDismiss?.()
  }}

  return (
    <AnimatePresence>
      {{visible && (
        <motion.div
          role="alert"
          aria-live={{variant === 'error' ? 'assertive' : 'polite'}}
          initial={{{{ opacity: 0, height: 0, marginBottom: 0 }}}}
          animate={{{{ opacity: 1, height: 'auto', marginBottom: 16 }}}}
          exit={{{{ opacity: 0, height: 0, marginBottom: 0 }}}}
          transition={{{{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}}}
          className="overflow-hidden rounded-[var(--radius-md)] border px-4 py-3"
          style={{{{ background: cfg.bg, borderColor: cfg.border }}}}
        >
          <div className="flex items-start gap-3">
            <Icon
              className="mt-0.5 size-5 flex-shrink-0"
              style={{{{ color: cfg.iconColor }}}}
              aria-hidden="true"
            />
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold" style={{{{ color: cfg.text }}}}>{{title}}</p>
              {{message && (
                <p className="mt-1 text-sm leading-relaxed" style={{{{ color: cfg.text, opacity: 0.8 }}}}>
                  {{message}}
                </p>
              )}}
            </div>
            {{dismissible && (
              <button
                onClick={{handleDismiss}}
                className="flex-shrink-0 rounded p-1 transition-opacity hover:opacity-70
                  focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-current"
                aria-label="Dismiss alert"
              >
                <X className="size-4" style={{{{ color: cfg.text }}}} aria-hidden="true" />
              </button>
            )}}
          </div>
        </motion.div>
      )}}
    </AnimatePresence>
  )
}}
"""

# ── Generator dispatch ───────────────────────────────────────────────
GENERATORS = {
    "PricingCard":   gen_pricing_card,
    "StatsRow":      gen_stats_row,
    "NavBar":        gen_navbar,
    "EmptyState":    gen_empty_state,
    "KPICard":       gen_kpi_card,
    "AlertBanner":   gen_alert_banner,
}

def generate_component(name: str, T: dict, framework: str, style: str) -> tuple[str, str]:
    """Generate code for a component. Returns (filename, code)."""
    gen_fn = GENERATORS.get(name)
    if gen_fn:
        code = gen_fn(T, framework, style)
        return f"{name}.tsx", code

    # Generic fallback for unlisted components
    spec = COMPONENT_LIBRARY.get(name, {})
    cat  = spec.get("category", "Component")
    desc = spec.get("desc", "Generated component")
    libs = ", ".join(spec.get("statement_components", ["shadcn: Card"])[:2])
    a11y = "\n   * ".join(spec.get("a11y", ["Include appropriate ARIA attributes"]))
    props_list = spec.get("props", ["children"])

    is_next = "next" in framework
    directive = "'use client'\n" if is_next else ""

    props_iface = "\n  ".join(f"{p.rstrip('[]')}: {'string' if '[]' not in p else 'any[]'}" for p in props_list[:5])
    props_destr = ", ".join(p.rstrip("[]") for p in props_list[:5])

    code = f"""{directive}/**
 * {name} — Generated by /component {datetime.now().strftime('%Y-%m-%d')}
 * Category: {cat}
 * Description: {desc}
 * Recommended: {libs}
 *
 * Accessibility requirements:
 * {a11y}
 */
import {{ motion }} from 'framer-motion'

interface {name}Props {{
  {props_iface}
  className?: string
}}

export default function {name}({{ {props_destr}, className }}: {name}Props) {{
  return (
    <motion.div
      className={{`rounded-[var(--radius-lg)] border border-[var(--color-border)] p-6 ${{className ?? ''}}`}}
      style={{{{ background: 'var(--color-surface)' }}}}
      initial={{{{ opacity: 0, y: 16 }}}}
      animate={{{{ opacity: 1, y: 0 }}}}
      transition={{{{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}}}
    >
      {{/* TODO: Implement {name} component */}}
      {{/* Recommended libs: {libs} */}}
      <p style={{{{ color: 'var(--color-text)' }}}}>{{name}} component</p>
    </motion.div>
  )
}}
"""
    return f"{name}.tsx", code


def load_tokens(root: Path) -> dict:
    master = root / "design-system" / "MASTER.md"
    tokens = {}
    if master.exists():
        for line in master.read_text(errors="ignore").splitlines():
            line = line.strip()
            for css, key in [("--color-primary:","primary"),("--color-cta:","cta"),
                              ("--color-bg:","bg"),("--color-surface:","surface"),
                              ("--color-text:","text"),("--color-muted:","muted")]:
                if line.startswith(css):
                    tokens[key] = line.split(":",1)[1].strip().rstrip(";")
    if not tokens:
        tokens = {"primary":"#6366F1","cta":"#A78BFA","bg":"#09090B",
                  "surface":"#18181B","text":"#FAFAFA","muted":"#71717A"}
    return tokens


def main():
    parser = argparse.ArgumentParser(description="/component — Component Generator")
    parser.add_argument("name",        nargs="?",   help="Component name")
    parser.add_argument("--style", "-s", default="dark-premium")
    parser.add_argument("--framework","-f", default="")
    parser.add_argument("--out",   "-o", default="")
    parser.add_argument("--list",  "-l", action="store_true")
    args = parser.parse_args()

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║        /component — Component Generator             ║")
    print("╚══════════════════════════════════════════════════════╝\n")

    if args.list:
        cats: dict = {}
        for name, spec in COMPONENT_LIBRARY.items():
            cat = spec["category"]
            cats.setdefault(cat, []).append((name, spec["desc"]))
        for cat, items in sorted(cats.items()):
            print(f"  [{cat}]")
            for name, desc in items:
                has_gen = "✓ full code" if name in GENERATORS else "◦ scaffold"
                print(f"    {name:<24} {has_gen:<14} {desc[:42]}")
        print(f"\n  ✓ = full production code  ◦ = scaffold (add your logic)")
        print(f"\n  Usage: python3 component.py PricingCard --style dark-premium")
        return

    if not args.name:
        print("  Usage: python3 component.py [ComponentName] [--style] [--framework]")
        print("         python3 component.py --list")
        return

    root = Path.cwd()

    # Detect framework
    framework = args.framework
    if not framework:
        try:
            result = subprocess.run(
                ["python3", str(Path(__file__).parent/"detect_stack.py")],
                capture_output=True, text=True, cwd=root)
            for line in result.stdout.split("\n"):
                if line.startswith("STACK_JSON:"):
                    framework = json.loads(line[11:]).get("framework","react")
        except Exception:
            framework = "react"

    tokens = load_tokens(root)

    # Check component exists
    if args.name not in COMPONENT_LIBRARY and args.name not in GENERATORS:
        print(f"  ⚠  '{args.name}' not in library. Generating scaffold...")

    filename, code = generate_component(args.name, tokens, framework, args.style)

    # Write file
    out_dir = Path(args.out) if args.out else root/"src"/"components"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir/filename
    out_path.write_text(code)

    print(f"  ✓ Generated: {out_path}")
    print(f"  Component:  {args.name}  |  Framework: {framework}  |  Style: {args.style}")

    # Quick review
    try:
        from review import review_code, grade
        result = review_code(code, filename, ["react","tailwind","nextjs" if "next" in framework else "react"])
        score = result["overall"]
        g, icon = grade(score)
        print(f"\n  Review: {icon} {score}/100 (Grade {g})  "
              f"Critical: {result['counts']['critical']}  "
              f"High: {result['counts']['high']}")
        if result["counts"]["critical"] > 0:
            print(f"  Run: python3 scripts/review.py {out_path} for details")
    except Exception:
        pass

    spec = COMPONENT_LIBRARY.get(args.name, {})
    if spec.get("required_libs"):
        print(f"\n  Required deps:")
        for lib in spec["required_libs"]:
            print(f"  npm install {lib}")
    if spec.get("statement_components"):
        print(f"\n  Statement components (install):")
        for comp in spec["statement_components"][:3]:
            print(f"  → {comp}")
    print()


if __name__ == "__main__":
    main()
