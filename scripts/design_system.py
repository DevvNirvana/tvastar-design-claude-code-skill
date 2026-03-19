#!/usr/bin/env python3
"""
Design System Generator v2.0
Produces complete design system with multi-library component selection.
Saves to design-system/MASTER.md for persistent cross-session use.
"""
import argparse, sys, os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from core import resolve_product, search_ux_laws, get_pattern, select_components, UX_LAWS, LIBRARY_CATALOG, get_palette_science
try:
    from color_science import contrast_ratio, wcag_grade, full_color_audit, color_temperature, generate_harmony
    HAS_COLOR_SCIENCE = True
except ImportError:
    HAS_COLOR_SCIENCE = False

def generate(product, style, dark_mode, persist, page_type="landing"):
    resolved = resolve_product(product, style)
    palette  = resolved["palette"]
    typo     = resolved["typography"]
    sty      = resolved["style"]
    pattern  = get_pattern(page_type)
    ux_laws  = search_ux_laws(f"{product} {style} layout navigation CTA", n=3)
    components = select_components(product, sty["name"], dark=dark_mode)

    W = 64
    lines = []
    def box(t): return f"  {t}"
    def div(label=""): pad = max(1, W - len(label) - 7); return f"  {'─'*4} {label} {'─'*pad}"

    lines += [f"╔{'═'*W}╗", f"║  {(product.upper()+' DESIGN SYSTEM').center(W-2)}  ║", f"╚{'═'*W}╝", ""]

    lines += [div("PALETTE"), box(f"Name:       {palette['name']}"),
              box(f"Primary:    {palette['primary']}"), box(f"Secondary:  {palette['secondary']}"),
              box(f"CTA/Accent: {palette['cta']}"),    box(f"Background: {palette['bg']}")]
    if dark_mode:
        lines += [box(f"Surface:    {palette.get('surface_dark','#18181B')}"),
                  box(f"Border:     {palette.get('border_dark','#27272A')}")]
    else:
        lines += [box(f"Surface:    {palette.get('surface','#FFFFFF')}"),
                  box(f"Border:     {palette.get('border','#E5E7EB')}")]
    lines += [box(f"Text:       {palette['text']}"), box(f"Muted:      {palette['muted']}"), ""]

    lines += [div("TYPOGRAPHY"), box(f"Heading:    {typo['heading']}  ({typo['weights_h']})"),
              box(f"Body:       {typo['body']}  ({typo['weights_b']})"),
              box(f"URL:        {typo['url']}"), ""]

    lines += [div("TYPE SCALE"),
              box("display: 72px / 4.5rem  / leading-none   / font-heading  ← hero only"),
              box("h1:      56px / 3.5rem  / leading-tight  / font-heading"),
              box("h2:      40px / 2.5rem  / leading-tight  / font-heading"),
              box("h3:      28px / 1.75rem / leading-snug   / font-heading"),
              box("h4:      22px / 1.375rem/ leading-snug   / font-body w-600"),
              box("body-lg: 18px / 1.125rem/ leading-relaxed/ font-body"),
              box("body:    16px / 1rem    / leading-relaxed/ font-body"),
              box("small:   14px / 0.875rem/ leading-normal / font-body"),
              box("caption: 12px / 0.75rem / leading-normal / font-body"), ""]

    lines += [div("ANIMATION TOKENS"),
              box("fast:     150ms ease-out      ← hover states, micro interactions"),
              box("normal:   250ms ease-out      ← transitions, show/hide"),
              box("slow:     400ms ease-in-out   ← page entrances, reveals"),
              box("spring:   600ms cubic-bezier(0.16, 1, 0.3, 1)  ← bouncy entrance"),
              box("stagger:  50ms delay increment between list items"), ""]

    lines += [div("STYLE PROFILE"), box(f"Name:     {sty['name']}"),
              box(f"Approach: {sty['bg_approach']}"),
              box(f"Effects:  {sty['effects']}"),
              box(f"Avoid:    {sty['anti_patterns']}"), ""]

    # ── Multi-library component selection ────────────────────────────
    lines += [div("COMPONENT LIBRARY SELECTIONS")]
    lines += [box("Each slot → best library + component for this design context:"), ""]
    for slot, sel in components["selections"].items():
        slot_label = slot.replace("_"," ").title().ljust(18)
        lines.append(box(f"  {slot_label} [{sel['lib']}] {sel['component']}"))
        lines.append(box(f"  {'':18}  ↳ {sel['reason']}"))
        lines.append(box(""))
    lines.append("")

    lines += [div("INSTALL COMMANDS")]
    lines.append(box("# Run from project root:"))
    lines.append(box("npm install framer-motion  # required by Aceternity + Magic UI"))
    lines.append(box(""))
    for cmd in components["install_commands"]:
        lines.append(box(cmd))
    lines.append("")


    # ── Color science section ────────────────────────────────────────
    if HAS_COLOR_SCIENCE:
        ps = get_palette_science(palette['name'])
        lines += [div("COLOR SCIENCE")]
        lines.append(box(f"Palette:    {palette['name']}"))
        lines.append(box(f"Industry:   {ps.get('industry','general')}"))
        lines.append(box(f"Emotion:    {ps.get('emotion','modern')}"))
        lines.append(box(f"Harmony:    {ps.get('harmony','analogous')}"))
        lines.append(box(f"WCAG note:  {ps.get('wcag_note','verify contrast')}"))
        lines.append(box(""))
        lines.append(box("Contrast ratios (WCAG 2.1):"))
        bg_color = palette['bg'] if dark_mode else "#FFFFFF"
        for name, fg in [("text on bg",    palette['text']),
                          ("primary on bg", palette['primary']),
                          ("muted on bg",   palette['muted'])]:
            try:
                ratio = contrast_ratio(fg, bg_color)
                _, _, grade = wcag_grade(ratio)
                lines.append(box(f"  {name+':':<18} {ratio}:1  {grade}"))
            except Exception:
                pass
        lines.append(box(""))
        lines.append(box(f"Temperature: {color_temperature(palette['primary'])}"))
        lines.append("")

    lines += [div("CSS VARIABLES  (→ globals.css / app/globals.css)")]
    lines.append(box(":root {"))
    lines += [box(f"  --color-primary:   {palette['primary']};"),
              box(f"  --color-secondary: {palette['secondary']};"),
              box(f"  --color-cta:       {palette['cta']};"),
              box(f"  --color-bg:        {palette['bg']};"),
              box(f"  --color-surface:   {palette.get('surface','#FFFFFF')};"),
              box(f"  --color-text:      {palette['text']};"),
              box(f"  --color-muted:     {palette['muted']};"),
              box(f"  --color-border:    {palette['border']};"),
              box(f"  --font-heading:    '{typo['heading']}', sans-serif;"),
              box(f"  --font-body:       '{typo['body']}', sans-serif;")]
    lines.append(box("}"))
    if dark_mode:
        lines += [box(".dark {"),
                  box(f"  --color-bg:      {palette.get('bg_dark','#09090B')};"),
                  box(f"  --color-surface: {palette.get('surface_dark','#18181B')};"),
                  box(f"  --color-text:    #F8FAFC;"),
                  box(f"  --color-muted:   #71717A;"),
                  box(f"  --color-border:  {palette.get('border_dark','#27272A')};"),
                  box("}")]
    lines.append("")

    lines += [div("FONT IMPORT"), box(typo['import']), ""]

    lines += [div("PAGE PATTERN"), box(f"Type: {pattern['name']}")]
    for i, s in enumerate(pattern['sections'], 1):
        lines.append(box(f"  {i:2}. {s}"))
    lines += [box(f"CTA:  {pattern['cta_placement']}"),
              box(f"Note: {pattern['conversion']}"), ""]

    if ux_laws:
        lines += [div("PSYCHOLOGY LAWS TO APPLY")]
        for law in ux_laws:
            lines += [box(f"[{law['law']}]"), box(f"  → {law['apply']}")]
        lines.append("")


    # ── INSPIRATION BENCHMARKS (from inspiration.md) ─────────────────────
    # Map product/style keywords to real reference sites
    q_low = f"{product} {style}".lower()
    inspo_map = [
        (["saas","b2b","tool","productivity","developer"],
         ["linear.app — type scale, spacing discipline",
          "vercel.com — dark/light toggle, motion quality",
          "raycast.com — dark premium, cursor spotlight"]),
        (["ai","ml","llm","artificial"],
         ["cursor.sh — dark premium, editor screenshot hero",
          "runway.ml — demo-first hero, dark sophistication",
          "perplexity.ai — functional minimal, restrained"]),
        (["ecommerce","shop","product","store"],
         ["allbirds.com — product photography standard",
          "ugmonk.com — product page + typography execution",
          "glossier.com — editorial grid, single-product focus"]),
        (["portfolio","agency","creative","studio"],
         ["obys.agency — fluid layout, typography-forward",
          "cuberto.com — cursor effects, bold motion",
          "fantasy.co — product design, restraint benchmark"]),
        (["dashboard","analytics","admin","data"],
         ["nicelydone.club — data-dense layouts, table design",
          "cal.com — clean open source dashboard quality",
          "clerk.dev — auth UI + clean dark dashboard"]),
        (["social","community","platform","network"],
         ["layers.to — new-gen Dribbble, polished work",
          "dribbble.com/search/social platform UI",
          "mobbin.com — social app UI patterns"]),
    ]
    inspo_refs = []
    for keywords, refs in inspo_map:
        if any(k in q_low for k in keywords):
            inspo_refs = refs
            break
    if not inspo_refs:
        inspo_refs = ["lapa.ninja — filter by product type, study 3 examples",
                      "godly.website — motion reference for the style",
                      "awwwards.com/websites — aspirational quality bar"]
    lines += [div("INSPIRATION BENCHMARKS")]
    lines.append(box("Study these before or during design (15min research protocol):"))
    for ref in inspo_refs:
        lines.append(box(f"  → {ref}"))
    lines += [box(""),
              box("Awwwards formula — what winning sites share:"),
              box("  1. One exceptional typographic moment (H1: 56-96px, committed scale)"),
              box("  2. One unexpected interactive element (cursor, scroll, 3D, trail)"),
              box("  3. Extreme whitespace confidence (96-128px section padding minimum)"),
              box("  4. Complete color discipline (2-3 colors, accent on ONE element only)"),
              box("  5. Motion that communicates state (not decoration)"),
              box(""), ""]

    # ── MOTION DURATION TABLE (from motion-principles.md) ─────────────────
    lines += [div("MOTION DURATION TABLE")]
    motion_rows = [
        ("hover bg/color",     "150ms", "ease-out"),
        ("tooltip show/hide",  "150ms", "ease-out"),
        ("dropdown open",      "200ms", "ease-out"),
        ("badge/state update", "250ms", "ease-out"),
        ("modal open",         "300ms", "spring stiffness:300 damping:30"),
        ("drawer slide",       "350ms", "cubic-bezier(0.16,1,0.3,1)"),
        ("page section enter", "400ms", "cubic-bezier(0.16,1,0.3,1)"),
        ("hero text reveal",   "500-600ms", "cubic-bezier(0.16,1,0.3,1)"),
        ("exit animations",    "200ms", "cubic-bezier(0.5,0,1,1)"),
        ("continuous loops",   "700ms+", "linear — ONLY for spinners/shimmer"),
    ]
    for ctx, dur, ease in motion_rows:
        lines.append(box(f"  {ctx:<24} {dur:<12} {ease}"))
    lines += [box(""),
              box("Entrance easing: cubic-bezier(0.16, 1, 0.3, 1)  ← fast start, soft settle"),
              box("Exit easing:     cubic-bezier(0.5, 0, 1, 1)     ← accelerates out"),
              box("Spring:          type:'spring' stiffness:300 damping:30"),
              box("RULE: NEVER linear for discrete UI. Always ease-out minimum."),
              box("RULE: useReducedMotion() check on ALL Framer Motion components."),
              box(""), ""]

    # ── SENIOR EYE TEST (from inspiration.md) ─────────────────────────────
    lines += [div("SENIOR DESIGNER EYE TEST")]
    eye_tests = [
        ("Scale test",       "H1 and body feel dramatically different — 3:1 minimum ratio"),
        ("Whitespace test",  "Every section breathes. If unsure, double the padding."),
        ("Hierarchy test",   "Cover all text — visual weight alone shows what matters most"),
        ("Color discipline", "CTA color appears ONLY on the CTA. Nowhere else on page."),
        ("Motion purpose",   "Remove any animation — does UX suffer? If no, cut it."),
        ("Mobile test",      "Hero text wraps gracefully at 375px. Tap targets ≥ 44px."),
        ("B&W test",         "Print in grayscale — hierarchy still clear via layout?"),
        ("Von Restorff",     "Is there exactly ONE thing that breaks the visual pattern?"),
    ]
    for test, condition in eye_tests:
        lines.append(box(f"  [ ] {test:<20} {condition}"))
    lines.append("")

    # ── CHART GUIDANCE (from charts-icons-reference.md) ──────────────────
    if any(k in q_low for k in ["dashboard","analytics","data","chart","metric","kpi","report"]):
        lines += [div("CHART TYPE GUIDANCE")]
        chart_rows = [
            ("Trend over time",     "Line / Area",   "Recharts LineChart"),
            ("Compare categories",  "Bar (horiz)",   "Recharts BarChart"),
            ("Part-to-whole ≤6",   "Donut",         "Recharts PieChart inner=60"),
            ("Part-to-whole >6",   "Stacked Bar",   "Recharts BarChart stacked"),
            ("KPI vs target",       "Gauge",         "ApexCharts / D3"),
            ("Correlation",         "Scatter",       "Recharts ScatterChart"),
            ("Funnel/conversion",   "Funnel",        "Recharts FunnelChart"),
            ("Realtime/streaming",  "Canvas area",   "CanvasJS (not SVG at 60fps)"),
        ]
        for data, chart, lib in chart_rows:
            lines.append(box(f"  {data:<24} → {chart:<16} {lib}"))
        lines += [box(""),
                  box("Chart colors: primary=#0080FF success=#10B981 warning=#F59E0B danger=#EF4444"),
                  box("Always: <figure><Chart/><figcaption>Description</figcaption></figure>"),
                  box("A11y: role='img' aria-label='Chart name: data summary' on wrapper"),
                  box(""), ""]

    # ── GESTALT QUICK AUDIT (from ux-principles.md) ───────────────────────
    lines += [div("GESTALT CHECKS FOR THIS LAYOUT")]
    gestalt_checks = [
        ("Proximity",     "Label 4-6px above input. Related items 4-8px. Sections 64-96px."),
        ("Similarity",    f"CTA color ({palette['cta']}) appears on ONLY ONE element."),
        ("Continuity",    "Feature sections alternate → Z-path eye follows naturally."),
        ("Figure/Ground", "Modal/dropdown elevated 3+ levels above page bg."),
        ("Common Fate",   "Staggered items entering together = they belong together."),
        ("Closure",       "Skeleton loaders match the exact shape of content they replace."),
        ("Symmetry",      "Centered layout = stable/authoritative. Off-center = dynamic."),
    ]
    for principle, check in gestalt_checks:
        lines.append(box(f"  [ ] {principle:<16} {check}"))
    lines.append("")

    # ── REACT BITS SELECTION GUIDE (from react-bits-catalog.md) ──────────
    rb_sels = components["selections"]
    rb_used = [v["component"] for v in rb_sels.values() if v["lib"] == "react-bits"]
    if rb_used:
        lines += [div("REACT BITS INSTALL (TS+TW variant for TypeScript projects)")]
        lines.append(box("Use TS+TW variant for Next.js + TypeScript:"))
        for comp in rb_used:
            lines.append(box(f'  npx shadcn@latest add "https://reactbits.dev/r/{comp}-TS-TW"'))
        lines += [box(""),
                  box("React Bits rules (from react-bits-catalog.md):"),
                  box("  • One statement piece per SECTION — FadeContent for everything else"),
                  box("  • Aurora/Particles/Silk: hero backgrounds only, never repeated"),
                  box("  • Counter on ALL numeric social proof — never static numbers"),
                  box("  • SplitText on ONE headline per page — the most important one"),
                  box("  • Always wrap components in FadeContent for scroll entrance"),
                  box(""), ""]

    lines += [div("TAILWIND CONFIG EXTENSIONS")]
    lines.append(box("// tailwind.config.ts → theme.extend:"))
    lines.append(box(f"fontFamily: {{ heading: ['{typo['heading']}', 'sans-serif'], body: ['{typo['body']}', 'sans-serif'] }},"))
    lines.append(box(f"colors: {{ primary: 'var(--color-primary)', cta: 'var(--color-cta)', bg: 'var(--color-bg)', surface: 'var(--color-surface)', muted: 'var(--color-muted)', border: 'var(--color-border)' }},"))
    lines.append("")

    lines += [div("PRE-DELIVERY CHECKLIST")]
    checks = ["[ ] No emojis as icons — SVGs only (Lucide, Heroicons, Phosphor)",
              "[ ] cursor-pointer on ALL clickable elements",
              "[ ] Hover transitions 150-300ms ease on every interactive element",
              "[ ] Light mode contrast 4.5:1 minimum (WCAG AA)",
              "[ ] Focus states visible — focus-visible:ring-2 ring-primary",
              "[ ] prefers-reduced-motion: motion-reduce:animate-none on all animate-*",
              "[ ] Responsive: 375 / 768 / 1024 / 1440px breakpoints",
              "[ ] No horizontal scroll on mobile",
              "[ ] No hardcoded hex values — use CSS variables / design tokens",
              "[ ] AnimatePresence wrapping all conditional Framer Motion renders",
              "[ ] Alt text on every image",
              "[ ] aria-label on every icon-only button",
              "[ ] key={item.id} on every .map() — never key={index}",
              "[ ] 'use client' directive on any Next.js component with hooks/events",
              "[ ] No raw <img> in Next.js — use next/image"]
    for c in checks: lines.append(box(f"  {c}"))
    lines.append("")

    output = "\n".join(lines)
    print(output)
    if persist: _save_master(output, product, style, palette, typo, sty, dark_mode, pattern, components)
    return output


def _save_master(output, product, style, palette, typo, sty, dark_mode, pattern, components):
    out_dir = Path.cwd() / "design-system"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "pages").mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    install_cmds = "\n".join(f"# {c}" if c.startswith("#") else c for c in components["install_commands"])

    content = f"""# Design System Master — {product}
Generated: {ts}  |  Style: {style}  |  Dark: {dark_mode}

> Rule: Check design-system/pages/[page].md first.
> If that file exists, its rules OVERRIDE this Master.
> If not, follow this Master exclusively.

---

## System Output
```
{output}
```

---

## Install Commands
```bash
npm install framer-motion
{install_cmds}
```

---

## Tailwind Config
```typescript
import type {{ Config }} from 'tailwindcss'
const config: Config = {{
  content: ['./src/**/*.{{ts,tsx}}', './app/**/*.{{ts,tsx}}'],
  darkMode: 'class',
  theme: {{
    extend: {{
      fontFamily: {{
        heading: ['{typo['heading']}', 'sans-serif'],
        body:    ['{typo['body']}', 'sans-serif'],
      }},
      colors: {{
        primary: 'var(--color-primary)', cta: 'var(--color-cta)',
        bg: 'var(--color-bg)', surface: 'var(--color-surface)',
        muted: 'var(--color-muted)', border: 'var(--color-border)',
      }},
      animation: {{
        'fade-in':  'fadeIn 400ms cubic-bezier(0.16,1,0.3,1)',
        'slide-up': 'slideUp 400ms cubic-bezier(0.16,1,0.3,1)',
      }},
    }},
  }},
}}
export default config
```

---

## globals.css
```css
:root {{
  --color-primary:   {palette['primary']};
  --color-secondary: {palette['secondary']};
  --color-cta:       {palette['cta']};
  --color-bg:        {palette['bg']};
  --color-surface:   {palette.get('surface','#FFFFFF')};
  --color-text:      {palette['text']};
  --color-muted:     {palette['muted']};
  --color-border:    {palette['border']};
  --font-heading:    '{typo['heading']}', sans-serif;
  --font-body:       '{typo['body']}', sans-serif;
}}
{''.join([chr(10)+".dark {", f"  --color-bg: {palette.get('bg_dark','#09090B')};", f"  --color-surface: {palette.get('surface_dark','#18181B')};", "  --color-text: #F8FAFC;", f"  --color-border: {palette.get('border_dark','#27272A')};", "}"] if dark_mode else [])}
```

---

## Page-Specific Overrides
Create design-system/pages/[page-name].md to override for specific pages.
Only document DEVIATIONS from this Master.
Examples: landing.md, dashboard.md, auth.md, pricing.md
"""
    (out_dir / "MASTER.md").write_text(content, encoding="utf-8")
    print(f"\n  ✓ Saved → design-system/MASTER.md")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--product","-p", default="web app")
    parser.add_argument("--style",  "-s", default="modern minimal")
    parser.add_argument("--dark",   action="store_true")
    parser.add_argument("--persist",action="store_true")
    parser.add_argument("--page",   default="landing")
    args = parser.parse_args()
    generate(args.product, args.style, args.dark, args.persist, args.page)
