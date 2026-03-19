#!/usr/bin/env python3
"""
/cro — Conversion Rate Optimization Engine v1.0 (Phase 9.1)
Eye tracking patterns, CRO placement rules, copy frameworks.
Usage:
  python3 cro.py --page landing
  python3 cro.py --page pricing
  python3 cro.py --audit src/app/page.tsx
  python3 cro.py --patterns
"""
import sys, re, argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

EYE_PATTERNS = {
    "F-pattern": {
        "desc": "Text-heavy pages. Eyes scan 2 horizontal bands then vertical left strip.",
        "use":  "Blogs, docs, news, long copy pages.",
        "rules":["Put most important content in first 2 horizontal bands",
                 "Don't rely on right column for critical info",
                 "Front-load value in headlines and first sentence",
                 "Use subheadings every 3-5 paragraphs to re-anchor F"],
    },
    "Z-pattern": {
        "desc": "Sparse pages. Eyes follow Z diagonal: top-left → top-right → bottom-left → bottom-right.",
        "use":  "Landing pages, ads, homepages with few elements.",
        "rules":["Logo top-left (start of Z)",
                 "Nav/trust signals top-right",
                 "Value prop or key image center-diagonal",
                 "CTA bottom-right (terminal area of Z)"],
    },
    "Gutenberg": {
        "desc": "Primary optical area (top-left) + terminal area (bottom-right) get most attention.",
        "use":  "Long-form landing pages, articles, dashboards.",
        "rules":["Primary CTA: top-left OR bottom-right only",
                 "Strongest content: primary optical area",
                 "Avoid weak follow area (bottom-left) for key content",
                 "Use strong fallow areas (top-right, bottom-left) for supporting elements"],
    },
    "Layer-cake": {
        "desc": "Eyes jump between headings, skipping body text entirely on first scan.",
        "use":  "Feature pages, dashboards, data-heavy layouts.",
        "rules":["Every section heading must stand alone — convey value even if body skipped",
                 "Use headings as CTA triggers (make them compelling)",
                 "Body text elaborates on heading — never contradicts it",
                 "3-word summary rule: each heading = value in 3 words max"],
    },
}

ABOVE_FOLD_RULES = [
    "1. Product/brand name visible at top-left (logo)",
    "2. Primary value proposition: WHAT you do for WHO in 7 words or less",
    "3. ONE primary CTA button — visually dominant, specific verb",
    "4. Social proof: number, review stars, or logo strip",
    "5. No navigation that competes with the CTA (Hick's Law)",
    "6. Test at 1280px, 768px, 375px — all 3 must show CTA above fold",
]

CTA_SCIENCE = {
    "copy_rules": [
        "Use verb + outcome: 'Start building' not 'Get started'",
        "Specific beats generic: 'Try free for 14 days' not 'Sign up free'",
        "First person wins: 'Start my free trial' > 'Start your free trial' (+90% in some tests)",
        "Under 4 words for primary CTA. Under 6 for secondary.",
        "Never two CTAs of equal visual weight — one must dominate",
    ],
    "color_rules": [
        "CTA color must be UNIQUE on the page (Von Restorff effect)",
        "High contrast between CTA and its background",
        "Green and orange historically outperform blue for CTA (in tested contexts)",
        "But: use YOUR brand's accent color for CTA — consistency builds recognition",
    ],
    "size_rules": [
        "Minimum 44px height (Fitts's Law — tap target)",
        "CTA should be noticeably larger than secondary actions",
        "Full-width on mobile (reduces decision friction)",
        "16px+ font in CTA — never below 14px",
    ],
    "placement_rules": [
        "Hero CTA: above fold, high contrast position",
        "Repeat CTA every 2-3 sections on long pages",
        "Float CTA after testimonials/social proof (earned the click)",
        "Bottom of page: always end with CTA (no dead ends)",
        "Sidebar CTA: only if user scrolls and doesn't click inline",
    ],
    "micro_copy": [
        "Below primary CTA: remove objections: 'No credit card · Cancel anytime'",
        "Trust indicators: '10,000+ teams', '4.9★ rating', 'SOC2 compliant'",
        "Risk reversal: '14-day free trial' or '30-day money back guarantee'",
        "Scarcity only if real: 'Only 3 spots left this month' (never fake)",
    ],
}

SOCIAL_PROOF_RULES = [
    {"placement":"Below hero headline","type":"Number stat + avatar stack","why":"Immediate credibility"},
    {"placement":"Before pricing section","type":"3 testimonials with specifics","why":"Earned the price reveal"},
    {"placement":"Below CTA button",     "type":"Logo strip or review score","why":"Last objection removal"},
    {"placement":"FAQ section",          "type":"Real common objections","why":"Shows you understand hesitation"},
]

PAGE_CRO_PLAYBOOKS = {
    "landing": {
        "pattern": "Z-pattern",
        "checklist": [
            "[ ] Value prop in first 7 words of H1",
            "[ ] Primary CTA: verb + outcome, unique color",
            "[ ] Micro-copy below CTA: removes top 2 objections",
            "[ ] Social proof: number or logo strip in hero",
            "[ ] Logo strip after hero (trust bar)",
            "[ ] Features: 3 not 12 (Miller's Law)",
            "[ ] Testimonials with specific outcomes not vague praise",
            "[ ] Pricing: show value BEFORE price (earn the reveal)",
            "[ ] Final CTA section: last chance, no dead end",
            "[ ] Mobile: CTA full-width, large enough to tap",
        ],
        "conversion_killers": [
            "CTA says 'Learn more' — not specific enough",
            "No social proof above the fold",
            "More than 7 navigation items (Hick's Law)",
            "Two equal-weight CTA buttons competing",
            "Price revealed before value demonstrated",
            "No risk reversal near CTA",
        ],
    },
    "pricing": {
        "pattern": "Layer-cake",
        "checklist": [
            "[ ] One clearly recommended plan (Most Popular)",
            "[ ] Annual/monthly toggle with savings % visible",
            "[ ] Pro card visually elevated (scale-105 + ring)",
            "[ ] Feature list: customer outcomes not feature names",
            "[ ] Risk reversal below plans: 'Free trial, no card'",
            "[ ] FAQ addresses top 5 pricing objections",
            "[ ] Comparison table for enterprise evaluation",
            "[ ] CTA inside each card: specific to that plan",
        ],
        "conversion_killers": [
            "All plans look equal weight — no recommended option",
            "Feature names are internal jargon not customer outcomes",
            "No annual discount or billing toggle",
            "No risk reversal near CTA",
            "Pricing revealed before problem/solution section",
        ],
    },
    "auth": {
        "pattern": "Gutenberg",
        "checklist": [
            "[ ] Social auth (Google/GitHub) ABOVE email form",
            "[ ] 'Or continue with email' divider clearly separates",
            "[ ] Single column form (never side-by-side fields)",
            "[ ] Auto-focus on first field on mount",
            "[ ] Password strength indicator on signup only",
            "[ ] Forgot password link: right-aligned, below password",
            "[ ] Submit button: full-width, 48px min height",
            "[ ] Sign up / Sign in switch link clearly visible",
        ],
        "conversion_killers": [
            "Email form before social auth (friction order wrong)",
            "Multiple fields per row on mobile",
            "No error message specificity (just 'Invalid input')",
            "Slow validation (>500ms feedback feels broken)",
        ],
    },
    "dashboard": {
        "pattern": "Layer-cake",
        "checklist": [
            "[ ] KPI cards in first visible row: 4 max",
            "[ ] Most important metric: top-left KPI (primary optical area)",
            "[ ] Primary action button: top-right of content area",
            "[ ] Empty states: specific action to fill them",
            "[ ] Progressive disclosure: overview then detail on click",
            "[ ] Loading states: skeleton not spinner for data-heavy views",
        ],
        "conversion_killers": [
            "KPI cards buried below the fold",
            "No empty state action (just shows blank space)",
            "Too many metrics without hierarchy",
        ],
    },
}

CRO_AUDIT_RULES = [
    {"id":"CRO001","sev":"High",
     "pattern":r'(?:Get started|Learn more|Click here|Submit|Button)\b',
     "msg":"Weak CTA copy. Use verb + outcome: 'Start building', 'Try free', 'View pricing'"},
    {"id":"CRO002","sev":"High",
     "pattern":r'<(?:button|a)[^>]*>\s*(?:Get started|Learn more|Submit)\s*</(?:button|a)>',
     "msg":"Generic CTA text detected. Replace with specific outcome."},
    {"id":"CRO003","sev":"Medium",
     "pattern":r'<(?:nav|header)[^>]*>(?:(?!<li|<a|<Link).){0,500}(?:<li|<a|<Link>[^<]*</){8,}',
     "msg":"Possible 8+ nav items (Hick's Law). Max 7 items to reduce decision paralysis."},
    {"id":"CRO004","sev":"Medium",
     "pattern":r'TODO.*(?:testimonial|social proof|review|trust)',
     "msg":"Missing social proof (TODO found). Testimonials increase conversion 10-34%."},
]

def audit_cro(code: str) -> list:
    issues = []
    for rule in CRO_AUDIT_RULES:
        if re.search(rule["pattern"], code, re.IGNORECASE):
            issues.append(rule)
    return issues

def main():
    parser = argparse.ArgumentParser(description="/cro — Conversion Rate Optimization Engine")
    parser.add_argument("--page","-p", help="Page playbook: landing|pricing|auth|dashboard")
    parser.add_argument("--audit","-a", help="Audit a file for CRO issues")
    parser.add_argument("--patterns",   action="store_true", help="Show eye tracking patterns")
    parser.add_argument("--cta",        action="store_true", help="Show CTA science")
    args = parser.parse_args()

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║        /cro — Conversion Rate Optimization          ║")
    print("╚══════════════════════════════════════════════════════╝\n")

    if args.patterns:
        for name, data in EYE_PATTERNS.items():
            print(f"  [{name}]  {data['use']}")
            print(f"  {data['desc']}")
            for rule in data["rules"]: print(f"    → {rule}")
            print()
        return

    if args.cta:
        for section, rules in CTA_SCIENCE.items():
            print(f"  [{section.replace('_',' ').upper()}]")
            for r in rules: print(f"    • {r}")
            print()
        return

    if args.audit:
        path = Path(args.audit)
        if not path.exists(): print(f"  ⚠  Not found: {args.audit}\n"); return
        code = path.read_text(errors="ignore")
        issues = audit_cro(code)
        print(f"  CRO audit: {args.audit}  |  {len(issues)} issues\n")
        for i in issues:
            icon = "🟠" if i["sev"]=="High" else "🟡"
            print(f"  {icon} [{i['id']}] {i['msg']}")
        if not issues: print("  ✅ No CRO issues detected")
        print()
        return

    if args.page:
        playbook = PAGE_CRO_PLAYBOOKS.get(args.page.lower())
        if not playbook:
            print(f"  Unknown page. Available: {', '.join(PAGE_CRO_PLAYBOOKS.keys())}\n"); return
        print(f"  CRO Playbook: {args.page.title()}")
        print(f"  Eye pattern:  {playbook['pattern']}\n")
        ep = EYE_PATTERNS.get(playbook["pattern"],{})
        if ep:
            print(f"  Pattern rule: {ep['desc']}")
            for r in ep["rules"]: print(f"    → {r}")
            print()
        print(f"  Conversion Checklist:")
        for item in playbook["checklist"]: print(f"  {item}")
        print(f"\n  Conversion Killers:")
        for k in playbook["conversion_killers"]: print(f"  ✗ {k}")
        print()
        return

    # Default: above fold rules + CTA rules
    print("  Above the Fold Rules:")
    for r in ABOVE_FOLD_RULES: print(f"  {r}")
    print()
    print("  CTA Copy Rules:")
    for r in CTA_SCIENCE["copy_rules"]: print(f"  • {r}")
    print()
    print("  Commands:")
    print("  --page landing|pricing|auth|dashboard")
    print("  --patterns   Eye tracking patterns")
    print("  --cta        CTA science")
    print("  --audit [file]\n")

if __name__ == "__main__":
    main()
