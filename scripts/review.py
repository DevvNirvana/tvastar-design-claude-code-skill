#!/usr/bin/env python3
"""
/review — Deep UI/UX + Code Quality Auditor v1.0
Runs 5 audit layers on any file, component, or full project:
  1. Design Quality   — hierarchy, whitespace, typography, color, motion
  2. Code Lint        — framework-specific anti-patterns (re-uses framework_lint)
  3. Accessibility    — WCAG 2.1 AA, ARIA, keyboard, focus, contrast signals
  4. Performance      — bundle signals, image handling, lazy loading, layout shift
  5. Consistency      — design token usage, spacing system, naming conventions

Usage:
  python3 review.py                          # review entire project
  python3 review.py src/components/Hero.tsx  # review one file
  python3 review.py src/components/          # review a directory
  python3 review.py --design-only            # skip code lint, design audit only
  python3 review.py --score                  # output numeric score (for CI)
"""

import sys, re, json, argparse, subprocess
from pathlib import Path
from datetime import datetime

# ─── Add scripts dir so we can import sibling modules ────────────────
sys.path.insert(0, str(Path(__file__).parent))
from framework_lint import lint_code, LINT_RULES

# ─── Scoring weights ─────────────────────────────────────────────────
CATEGORY_WEIGHTS = {
    "design":        25,
    "accessibility": 25,
    "code":          25,
    "performance":   15,
    "consistency":   10,
}

# ─── Design quality rules ────────────────────────────────────────────
DESIGN_RULES = [
    # Typography
    {"id":"DQ001","sev":"Critical","cat":"design","layer":"Typography",
     "pattern":r'className=["\'][^"\']*(?:text-xs|text-sm)\s+font-bold',
     "msg":"Small bold text — use font-semibold at small sizes. Bold at <14px is illegible.",
     "fix":"Replace font-bold with font-semibold on text-xs/text-sm elements"},
    {"id":"DQ002","sev":"High","cat":"design","layer":"Typography",
     "pattern":r'style=\{[^}]*fontFamily\s*:',
     "msg":"Inline fontFamily style detected — use CSS variable or Tailwind font-* class.",
     "fix":"Use className='font-heading' or 'font-body' from your design system"},
    {"id":"DQ003","sev":"High","cat":"design","layer":"Typography",
     "pattern":r'text-\[(?:1[3-9]|[2-9]\d)px\]',
     "msg":"Non-system font size — use the type scale (text-sm, text-base, text-lg, etc.).",
     "fix":"Map to nearest type scale value: 14px→text-sm, 16px→text-base, 18px→text-lg"},
    # Color
    {"id":"DQ004","sev":"Critical","cat":"design","layer":"Color",
     "pattern":r'(?:bg|text|border)-\[#[0-9A-Fa-f]{6}\]',
     "msg":"Hardcoded hex color in Tailwind class — breaks design token system.",
     "fix":"Use CSS variable: bg-[var(--color-primary)] or add token to tailwind.config"},
    {"id":"DQ005","sev":"High","cat":"design","layer":"Color",
     "pattern":r'(?:text-gray-[3-4]00|text-slate-[3-4]00)\s',
     "msg":"Gray-300/400 text on white background fails WCAG AA contrast (4.5:1).",
     "fix":"Use text-gray-500 minimum on white. Verify with https://webaim.org/resources/contrastchecker/"},
    {"id":"DQ006","sev":"Medium","cat":"design","layer":"Color",
     "pattern":r'bg-white.*dark:|dark:.*bg-black[^-]',
     "msg":"Pure black (#000) or white (#fff) in dark mode — use near-black (#09090B) for dark bg.",
     "fix":"Replace bg-black with bg-zinc-950 or bg-[#09090B] for premium dark aesthetics"},
    # Spacing
    {"id":"DQ007","sev":"High","cat":"design","layer":"Spacing",
     "pattern":r'(?:p|m|gap|space-[xy])-\[(?:3|5|7|9|11|13|15|17|19|21|23)px\]',
     "msg":"Non-8px-grid spacing value — breaks spatial rhythm.",
     "fix":"Stick to 8px grid: 4, 8, 12, 16, 24, 32, 48, 64px (p-1, p-2, p-3, p-4, p-6, p-8, p-12, p-16)"},
    {"id":"DQ008","sev":"Medium","cat":"design","layer":"Spacing",
     "pattern":r'<section[^>]*className=["\'][^"\']*py-(?:2|3|4)\b',
     "msg":"Section vertical padding too tight (py-2/3/4 = 8-16px). Sections need breathing room.",
     "fix":"Sections need py-16 (64px) minimum on mobile, py-24+ on desktop"},
    # Interaction
    {"id":"DQ009","sev":"Critical","cat":"design","layer":"Interaction",
     "pattern":r'<(?:button|a)\b[^>]*className=["\'][^"\']*(?<!cursor-pointer)["\'](?!\s*cursor)',
     "msg":"Interactive element missing cursor-pointer.",
     "fix":"Add cursor-pointer to all <button> and <a> elements"},
    {"id":"DQ010","sev":"High","cat":"design","layer":"Interaction",
     "pattern":r'hover:[a-z-]+(?![^\n]*transition)',
     "msg":"Hover state without transition — creates jarring instant color jump.",
     "fix":"Add transition-colors duration-150 or transition-all duration-200"},
    {"id":"DQ011","sev":"High","cat":"design","layer":"Interaction",
     "pattern":r'hover:scale-1(?:0[5-9]|[1-9]\d)',
     "msg":"scale on hover shifts layout neighbors. Use transform-gpu and overflow-hidden on parent.",
     "fix":"Wrap in overflow-hidden, add transform-gpu to the scaled element"},
    # Motion
    {"id":"DQ012","sev":"Critical","cat":"design","layer":"Motion",
     "pattern":r'animate-(?!none)[a-z-]+(?![^\n]*motion-reduce)',
     "msg":"Animation without prefers-reduced-motion support — fails WCAG 2.3.3.",
     "fix":"Add motion-reduce:animate-none alongside every animate-* class"},
    {"id":"DQ013","sev":"Medium","cat":"design","layer":"Motion",
     "pattern":r'duration-(?:700|800|900|1000)',
     "msg":"Animation duration >600ms feels sluggish for UI interactions.",
     "fix":"Keep UI animations ≤400ms. Use 600ms only for dramatic page entrances."},
    # Visual debt
    {"id":"DQ014","sev":"High","cat":"design","layer":"Polish",
     "pattern":r'🎉|🚀|✅|❌|🔥|💡|⚡|👋|🎨|🛠',
     "msg":"Emoji used as UI icon — inconsistent rendering across OS, no a11y.",
     "fix":"Replace with SVG icon: Lucide, Heroicons, Phosphor, or Radix Icons"},
    {"id":"DQ015","sev":"Critical","cat":"design","layer":"Polish",
     "pattern":r'(?:Lorem ipsum|placeholder text|TODO|FIXME|Insert here|Coming soon\.\.\.|TBD)',
     "msg":"Placeholder content in component — never ship placeholder text.",
     "fix":"Replace with real content or a realistic content stub"},
    {"id":"DQ016","sev":"Medium","cat":"design","layer":"Responsive",
     "pattern":r'w-\[(?:[4-9]\d\d|[1-9]\d{3})px\]',
     "msg":"Fixed pixel width >400px — will overflow on mobile.",
     "fix":"Use max-w-* or w-full with responsive overrides: md:w-[500px]"},
]

# ─── Accessibility rules ──────────────────────────────────────────────
A11Y_RULES = [
    {"id":"A11Y001","sev":"Critical","cat":"accessibility",
     "pattern":r'<(?:img|Image)\b(?![^>]*alt=)',
     "msg":"Image without alt text — screen readers cannot describe it.",
     "fix":"Add alt='' for decorative images, alt='descriptive text' for meaningful ones"},
    {"id":"A11Y002","sev":"Critical","cat":"accessibility",
     "pattern":r'<(?:input|textarea|select)\b(?![^>]*(?:aria-label|aria-labelledby|id=))',
     "msg":"Form input without label — screen readers cannot identify the field.",
     "fix":"Add <label htmlFor='id'> or aria-label='...' to every input"},
    {"id":"A11Y003","sev":"Critical","cat":"accessibility",
     "pattern":r'<button[^>]*>\s*<(?:svg|Lucide|Icon|[A-Z][a-zA-Z]+Icon)\b',
     "msg":"Icon-only button without aria-label — screen readers say 'button' with no context.",
     "fix":"Add aria-label='Delete item' (or descriptive action) to icon-only buttons"},
    {"id":"A11Y004","sev":"Critical","cat":"accessibility",
     "pattern":r'focus:outline-none(?![^\n]*focus:ring)',
     "msg":"Focus outline removed without replacement — keyboard users cannot navigate.",
     "fix":"Add focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2"},
    {"id":"A11Y005","sev":"High","cat":"accessibility",
     "pattern":r'<div[^>]*(?:onClick|onKeyDown)[^>]*>(?!.*role=)',
     "msg":"Clickable div without role= — not keyboard accessible, no semantics.",
     "fix":"Use <button> for actions, <a> for navigation, or add role='button' tabIndex={0}"},
    {"id":"A11Y006","sev":"High","cat":"accessibility",
     "pattern":r'<h[1-6][^>]*>.*<\/h[1-6]>.*<h[1-6][^>]*>',
     "msg":"Multiple heading levels detected — ensure logical heading hierarchy (h1→h2→h3).",
     "fix":"One h1 per page. h2 for sections, h3 for subsections. Never skip levels."},
    {"id":"A11Y007","sev":"High","cat":"accessibility",
     "pattern":r'(?:color|colour)\s*:\s*(?:red|green|blue|yellow)(?![^;]*(?:background|bg))',
     "msg":"Color alone used to convey meaning — colorblind users miss the signal.",
     "fix":"Add an icon or text label alongside color indicators"},
    {"id":"A11Y008","sev":"Medium","cat":"accessibility",
     "pattern":r'<(?:section|article|aside|main|nav|header|footer)[^>]*>(?!.*aria-label)',
     "msg":"Landmark element without aria-label — screen readers list unnamed landmarks.",
     "fix":"Add aria-label='Main navigation' or aria-labelledby='section-heading-id'"},
    {"id":"A11Y009","sev":"Medium","cat":"accessibility",
     "pattern":r'tabIndex=\{-1\}',
     "msg":"tabIndex={-1} removes element from tab order — ensure this is intentional.",
     "fix":"Only use tabIndex={-1} on programmatically focused elements, not permanent UI"},
    {"id":"A11Y010","sev":"High","cat":"accessibility",
     "pattern":r'<(?:Dialog|Modal|Sheet|Drawer)[^>]*>(?![\s\S]{0,300}(?:DialogTitle|aria-label))',
     "msg":"Dialog/Modal without title — screen reader users have no context when it opens.",
     "fix":"Add <DialogTitle> inside <DialogContent>, or aria-label on the dialog element"},
]

# ─── Performance rules ────────────────────────────────────────────────
PERF_RULES = [
    {"id":"PF001","sev":"Critical","cat":"performance",
     "pattern":r'<img\s',
     "msg":"Raw <img> tag — no optimization, no lazy loading, causes layout shift.",
     "fix":"Use next/image (Next.js) or add loading='lazy' width={} height={} attributes"},
    {"id":"PF002","sev":"High","cat":"performance",
     "pattern":r"@import url\(.+fonts\.googleapis",
     "msg":"Google Fonts @import — blocks render, causes FOUT, zero caching benefit.",
     "fix":"Use next/font/google (Next.js) or @fontsource package (Vite/React)"},
    {"id":"PF003","sev":"High","cat":"performance",
     "pattern":r"import \* as .+ from ['\"](?!react|framer|three)[a-z@][^'\"]+['\"]",
     "msg":"Namespace import (import * as X) — prevents tree-shaking, bloats bundle.",
     "fix":"Use named imports: import { ComponentA, ComponentB } from 'library'"},
    {"id":"PF004","sev":"Medium","cat":"performance",
     "pattern":r'useEffect\(\s*\(\s*\)\s*=>\s*\{[^}]*fetch\(',
     "msg":"Data fetching in useEffect — causes request waterfall. Fetch in Server Component instead.",
     "fix":"Move fetch to a Server Component (Next.js) or React Query/SWR for client data"},
    {"id":"PF005","sev":"Medium","cat":"performance",
     "pattern":r'\.map\([^)]+\)[^.]*\.filter\(',
     "msg":".map() then .filter() — runs twice. .filter() first reduces iterations.",
     "fix":"Reverse order: array.filter(...).map(...) — filter first, then map"},
    {"id":"PF006","sev":"Medium","cat":"performance",
     "pattern":r'<video[^>]*src=(?![^>]*preload)',
     "msg":"Video element without preload attribute — browser may preload entire video.",
     "fix":"Add preload='none' (lazy) or preload='metadata' (load duration only)"},
    {"id":"PF007","sev":"Low","cat":"performance",
     "pattern":r'const \w+ = \([^)]*\) =>[^;]+;\s*(?:return|const)',
     "msg":"Inline function definition inside render — new function reference every render.",
     "fix":"Move handler outside component or wrap in useCallback if passed as prop"},
    {"id":"PF008","sev":"High","cat":"performance",
     "pattern":r'import .+ from ["\'](?:lodash|moment|date-fns)["\'](?!\s*/)',
     "msg":"Full library import (lodash/moment/date-fns) — massive bundle cost.",
     "fix":"Use specific imports: import debounce from 'lodash/debounce' or use native alternatives"},
]

# ─── Consistency rules ────────────────────────────────────────────────
CONSISTENCY_RULES = [
    {"id":"CN001","sev":"High","cat":"consistency",
     "pattern":r'rounded-(?:sm|md|lg|xl|2xl|full)',
     "msg":"Multiple border-radius values detected — define one radius scale and stick to it.",
     "fix":"Define --radius in CSS vars. Cards: rounded-xl. Buttons: rounded-lg. Inputs: rounded-md."},
    {"id":"CN002","sev":"Medium","cat":"consistency",
     "pattern":r'shadow-(?:sm|md|lg|xl|2xl)',
     "msg":"Ensure shadow scale matches elevation system (sm=content, md=card, lg=dropdown, xl=modal).",
     "fix":"Audit shadow usage — same elevation type should always use same shadow class"},
    {"id":"CN003","sev":"High","cat":"consistency",
     "pattern":r'font-(?:sans|serif|mono)\b',
     "msg":"Generic Tailwind font-sans/serif/mono used instead of design system font variable.",
     "fix":"Use font-heading and font-body from your Tailwind config theme extension"},
    {"id":"CN004","sev":"Medium","cat":"consistency",
     "pattern":r'text-(?:blue|red|green|yellow|purple|pink|orange)-\d00\b',
     "msg":"Raw Tailwind color scale used instead of semantic design token.",
     "fix":"Use semantic tokens: text-primary, text-cta, text-muted, text-destructive"},
    {"id":"CN005","sev":"High","cat":"consistency",
     "pattern":r'(?:w|h)-\[(?:3[68]|4[024]|5[26]|6[04]|7[28]|8[048])px\]',
     "msg":"Arbitrary pixel size close to a Tailwind scale value — use the scale.",
     "fix":"Use Tailwind scale: 36px→9, 40px→10, 44px→11, 48px→12, 64px→16, 80px→20"},
]


def run_rules(code: str, rules: list) -> list:
    issues = []
    for rule in rules:
        if re.search(rule["pattern"], code, re.MULTILINE | re.IGNORECASE):
            issues.append(rule)
    return issues


def score_issues(issues: list) -> int:
    """Convert issue list to 0-100 score. Fewer/lower-severity issues = higher score."""
    deductions = {"Critical": 15, "High": 8, "Medium": 3, "Low": 1}
    total_deducted = sum(deductions.get(i["sev"], 0) for i in issues)
    return max(0, 100 - total_deducted)


def grade(score: int) -> tuple:
    if score >= 95: return "A+", "🟢"
    if score >= 90: return "A",  "🟢"
    if score >= 80: return "B",  "🟡"
    if score >= 70: return "C",  "🟠"
    if score >= 60: return "D",  "🔴"
    return "F", "🔴"


def review_code(code: str, filename: str = "", frameworks: list = None) -> dict:
    """Run all 5 audit layers on a code string."""
    if frameworks is None:
        frameworks = ["react", "tailwind", "general"]

    design_issues    = run_rules(code, DESIGN_RULES)
    a11y_issues      = run_rules(code, A11Y_RULES)
    perf_issues      = run_rules(code, PERF_RULES)
    consistency_issues = run_rules(code, CONSISTENCY_RULES)

    # Re-use framework_lint for code issues
    code_issues_raw = lint_code(code, frameworks)
    code_issues = [{"id": i["id"], "sev": i["severity"], "cat": "code",
                    "msg": i["message"], "fix": i.get("fix",""), "rule": i["rule"]}
                   for i in code_issues_raw]

    all_issues = (
        [{"id":i["id"],"sev":i["sev"],"cat":i["cat"],"layer":i.get("layer",""),
          "msg":i["msg"],"fix":i["fix"]} for i in design_issues] +
        [{"id":i["id"],"sev":i["sev"],"cat":i["cat"],"layer":"",
          "msg":i["msg"],"fix":i["fix"]} for i in a11y_issues] +
        code_issues +
        [{"id":i["id"],"sev":i["sev"],"cat":i["cat"],"layer":"",
          "msg":i["msg"],"fix":i["fix"]} for i in perf_issues] +
        [{"id":i["id"],"sev":i["sev"],"cat":i["cat"],"layer":"",
          "msg":i["msg"],"fix":i["fix"]} for i in consistency_issues]
    )

    # Score each category
    scores = {}
    for cat in CATEGORY_WEIGHTS:
        cat_issues = [i for i in all_issues if i["cat"] == cat]
        scores[cat] = score_issues(cat_issues)

    # Weighted overall
    overall = sum(scores[c] * CATEGORY_WEIGHTS[c] / 100 for c in CATEGORY_WEIGHTS)

    return {
        "filename": filename,
        "issues": all_issues,
        "scores": scores,
        "overall": round(overall),
        "counts": {
            "critical": len([i for i in all_issues if i["sev"] == "Critical"]),
            "high":     len([i for i in all_issues if i["sev"] == "High"]),
            "medium":   len([i for i in all_issues if i["sev"] == "Medium"]),
            "low":      len([i for i in all_issues if i["sev"] == "Low"]),
        }
    }


def print_review(result: dict, verbose: bool = True):
    W = 60
    fn = result["filename"] or "project"
    overall = result["overall"]
    g, icon = grade(overall)
    counts = result["counts"]

    print(f"\n{'═'*W}")
    print(f"  /review — UI/UX + Code Quality Report")
    print(f"  File: {fn}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'═'*W}\n")

    # Overall score
    bar_fill = int(overall / 5)
    bar = "█" * bar_fill + "░" * (20 - bar_fill)
    print(f"  OVERALL SCORE   {icon} {overall}/100  [{bar}]  Grade: {g}\n")

    # Category breakdown
    print(f"  {'Category':<16} {'Score':>6}  {'Weight':>7}  Bar")
    print(f"  {'─'*55}")
    for cat, weight in CATEGORY_WEIGHTS.items():
        s = result["scores"][cat]
        g2, ic = grade(s)
        mini_bar = "█" * int(s/10) + "░" * (10 - int(s/10))
        print(f"  {cat.capitalize():<16} {s:>5}/100  {str(weight)+'%':>7}  {ic} [{mini_bar}]")

    print(f"\n  Issues: 🔴 {counts['critical']} Critical  "
          f"🟠 {counts['high']} High  "
          f"🟡 {counts['medium']} Medium  "
          f"⚪ {counts['low']} Low\n")

    if not result["issues"]:
        print("  ✅ No issues found. Ship-ready.\n")
        return

    # Group and print issues by severity
    for sev, icon2 in [("Critical","🔴"), ("High","🟠"), ("Medium","🟡"), ("Low","⚪")]:
        issues = [i for i in result["issues"] if i["sev"] == sev]
        if not issues:
            continue
        print(f"  {icon2} {sev.upper()} ({len(issues)})")
        print(f"  {'─'*55}")
        for issue in issues:
            layer = f" [{issue['layer']}]" if issue.get("layer") else ""
            print(f"  [{issue['id']}]{layer} {issue['msg']}")
            if issue.get("fix") and verbose:
                print(f"  {'':8}→ Fix: {issue['fix']}")
            print()

    # Recommendations
    if counts["critical"] > 0:
        print(f"  ⛔ {counts['critical']} Critical issue(s) must be fixed before /ship.")
    elif counts["high"] > 0:
        print(f"  ⚠️  {counts['high']} High issue(s) — strongly recommended to fix before ship.")
    elif overall >= 80:
        print(f"  ✅ Looking good. Fix Medium issues for a clean ship.")
    print()


def detect_frameworks_from_file(filepath: str) -> list:
    """Guess frameworks from file content + path."""
    path = Path(filepath)
    code = path.read_text(errors="ignore") if path.exists() else ""
    frameworks = ["general"]
    if ".tsx" in filepath or ".ts" in filepath or ".jsx" in filepath:
        frameworks.append("react")
        if "next" in code or "from 'next" in code:
            frameworks.append("nextjs")
        if "framer-motion" in code or "from 'motion" in code:
            frameworks.append("framer")
    if "tailwind" in code or "className=" in code:
        frameworks.append("tailwind")
    if "shadcn" in code or "@/components/ui" in code:
        frameworks.append("shadcn")
    if ".vue" in filepath:
        frameworks.append("vue")
    if ".svelte" in filepath:
        frameworks.append("svelte")
    return list(set(frameworks))


def review_directory(dirpath: str, frameworks: list) -> list:
    """Review all component files in a directory."""
    exts = {".tsx", ".ts", ".jsx", ".js", ".svelte", ".vue"}
    results = []
    root = Path(dirpath)
    for ext in exts:
        for f in root.rglob(f"*{ext}"):
            if any(skip in str(f) for skip in ["node_modules", ".next", "__pycache__", ".git"]):
                continue
            try:
                code = f.read_text(errors="ignore")
                fw = detect_frameworks_from_file(str(f))
                result = review_code(code, str(f.name), fw)
                if result["issues"]:
                    results.append(result)
            except Exception:
                pass
    return results


def main():
    parser = argparse.ArgumentParser(description="/review — UI/UX + Code Quality Auditor")
    parser.add_argument("target", nargs="?", default=".", help="File or directory to review")
    parser.add_argument("--framework", "-f", help="Frameworks: nextjs,react,shadcn,tailwind")
    parser.add_argument("--design-only", action="store_true", help="Only run design quality checks")
    parser.add_argument("--score", action="store_true", help="Output numeric score only (for CI)")
    parser.add_argument("--quiet", "-q", action="store_true", help="Show issues without fix hints")
    args = parser.parse_args()

    target = Path(args.target)

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║        /review — UI/UX + Code Quality Auditor       ║")
    print("╚══════════════════════════════════════════════════════╝")

    # Auto-detect frameworks
    if args.framework:
        frameworks = [f.strip() for f in args.framework.split(",")]
    else:
        try:
            result = subprocess.run(
                ["python3", str(Path(__file__).parent / "detect_stack.py")],
                capture_output=True, text=True, cwd=Path.cwd()
            )
            frameworks = ["react", "tailwind", "general"]
            for line in result.stdout.split("\n"):
                if line.startswith("STACK_JSON:"):
                    stack = json.loads(line[11:])
                    frameworks = stack.get("guidelines", frameworks)
                    if stack.get("has_framer"): frameworks.append("framer")
                    if stack.get("has_shadcn"): frameworks.append("shadcn")
        except Exception:
            frameworks = ["react", "tailwind", "general"]

    # Single file
    if target.is_file():
        code = target.read_text(errors="ignore")
        fw = detect_frameworks_from_file(str(target))
        result = review_code(code, target.name, fw)
        if args.score:
            print(result["overall"])
            return
        print_review(result, verbose=not args.quiet)
        sys.exit(1 if result["counts"]["critical"] > 0 else 0)

    # Directory
    elif target.is_dir():
        results = review_directory(str(target), frameworks)
        if not results:
            print("\n  ✅ No issues found across project.\n")
            return

        # Aggregate
        all_issues = [i for r in results for i in r["issues"]]
        total_critical = len([i for i in all_issues if i["sev"] == "Critical"])
        total_high     = len([i for i in all_issues if i["sev"] == "High"])
        avg_score      = round(sum(r["overall"] for r in results) / len(results))
        g, icon        = grade(avg_score)

        print(f"\n  Project Review — {len(results)} files with issues")
        print(f"  Overall: {icon} {avg_score}/100 (Grade {g})")
        print(f"  Total:   🔴 {total_critical} Critical  🟠 {total_high} High  "
              f"🟡 {len([i for i in all_issues if i['sev']=='Medium'])} Medium\n")

        if args.score:
            print(avg_score)
            return

        for r in sorted(results, key=lambda x: x["overall"]):
            if r["counts"]["critical"] > 0 or r["counts"]["high"] > 0:
                print_review(r, verbose=not args.quiet)

        if total_critical > 0:
            print(f"  ⛔ {total_critical} Critical issues must be fixed before /ship")
            sys.exit(1)
    else:
        print(f"\n  ⚠️  Target not found: {target}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
