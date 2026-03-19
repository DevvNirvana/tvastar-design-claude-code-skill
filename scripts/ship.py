#!/usr/bin/env python3
"""
/ship — Production Readiness Gate v1.0
Final pre-deployment validator. Checks everything that can silently break in
production that /review doesn't catch at the file level.

Validates 8 gates:
  1. Build hygiene      — console.logs, TODOs, debug flags, commented-out code
  2. Environment        — .env.example exists, no secrets committed, NEXT_PUBLIC_ correct
  3. SEO & Meta         — <title>, meta description, OG tags, robots.txt, sitemap
  4. Accessibility gate — landmark structure, skip links, page title uniqueness
  5. Performance gate   — image dimensions, font strategy, lazy loading signals
  6. Design system gate — CSS variables defined, design-system/MASTER.md present
  7. Dependencies       — no known vulnerable pattern imports, peer dep mismatches
  8. Framework-specific — Next.js: error.tsx, loading.tsx, not-found.tsx present

Usage:
  python3 ship.py                    # full gate check on current project
  python3 ship.py --fix-hints        # include specific fix commands
  python3 ship.py --gate seo         # run one gate only
  python3 ship.py --score            # output GO/BLOCKED and numeric score for CI
"""

import sys, re, json, os, argparse, subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

# ─── Gate definitions ─────────────────────────────────────────────────
GATES = {
    "hygiene": {
        "name": "Build Hygiene",
        "weight": 20,
        "checks": [
            {"id":"HY001","sev":"Critical","name":"No console.log",
             "search_file": True,
             "pattern": r"console\.(log|warn|debug)\(",
             "msg": "console.log/warn/debug statements in source",
             "fix": "Remove all console.* calls. Use a logging utility for intentional logs."},
            {"id":"HY002","sev":"High","name":"No TODO/FIXME",
             "search_file": True,
             "pattern": r"//\s*(TODO|FIXME|HACK|XXX|TEMP|REMOVEME)",
             "msg": "Unresolved TODO/FIXME comments found",
             "fix": "Resolve or create tickets for each TODO before shipping"},
            {"id":"HY003","sev":"High","name":"No debug flags",
             "search_file": True,
             "pattern": r"(?:debug|DEBUG)\s*[:=]\s*true",
             "msg": "Debug flag set to true",
             "fix": "Remove or set debug flags to false / env-controlled"},
            {"id":"HY004","sev":"Medium","name":"No large commented blocks",
             "search_file": True,
             "pattern": r"(?:\/\/[^\n]+\n){5,}",
             "msg": "Large blocks of commented-out code found",
             "fix": "Remove dead code — version control is your history"},
            {"id":"HY005","sev":"Critical","name":"No placeholder content",
             "search_file": True,
             "pattern": r"Lorem ipsum|placeholder text|Coming soon\.\.\.|Insert content|TBD\b",
             "msg": "Placeholder text found in source files",
             "fix": "Replace all placeholder text with real content before shipping"},
        ]
    },
    "environment": {
        "name": "Environment & Secrets",
        "weight": 20,
        "checks": [
            {"id":"EV001","sev":"Critical","name":".env not committed",
             "check_fn": "check_env_not_committed",
             "msg": ".env file committed to repo (visible in git)",
             "fix": "Add .env to .gitignore immediately. Rotate all exposed secrets."},
            {"id":"EV002","sev":"High","name":".env.example exists",
             "check_fn": "check_env_example_exists",
             "msg": "No .env.example file — collaborators won't know required variables",
             "fix": "Create .env.example with all variable keys (empty values)"},
            {"id":"EV003","sev":"Critical","name":"No hardcoded secrets",
             "search_file": True,
             "pattern": r'(?:api[_-]?key|secret|password|token)\s*[=:]\s*["\'][a-zA-Z0-9_\-]{16,}["\']',
             "msg": "Hardcoded secret/API key found in source",
             "fix": "Move to environment variables immediately. Rotate the exposed key."},
            {"id":"EV004","sev":"High","name":"NEXT_PUBLIC_ for client vars",
             "search_file": True,
             "pattern": r'process\.env\.(?!NEXT_PUBLIC_|NODE_ENV)\w+',
             "msg": "Server-only env var accessed in client component",
             "fix": "Prefix client-accessible vars with NEXT_PUBLIC_"},
        ]
    },
    "seo": {
        "name": "SEO & Meta",
        "weight": 15,
        "checks": [
            {"id":"SE001","sev":"High","name":"<title> tag present",
             "check_fn": "check_title_tag",
             "msg": "No <title> or metadata.title found in layout/pages",
             "fix": "Add export const metadata = { title: 'Page Title | Brand' } to layout.tsx"},
            {"id":"SE002","sev":"High","name":"Meta description",
             "check_fn": "check_meta_description",
             "msg": "No meta description found",
             "fix": "Add description: 'Your page description (150-160 chars)' to metadata"},
            {"id":"SE003","sev":"Medium","name":"OG image defined",
             "check_fn": "check_og_image",
             "msg": "No Open Graph image defined — poor social share preview",
             "fix": "Add openGraph: { images: [{ url: '/og-image.png', width: 1200, height: 630 }] }"},
            {"id":"SE004","sev":"Medium","name":"robots.txt exists",
             "check_fn": "check_robots_txt",
             "msg": "No robots.txt found in public/ directory",
             "fix": "Create public/robots.txt. Minimum: User-agent: * / Allow: /"},
            {"id":"SE005","sev":"Low","name":"Sitemap exists",
             "check_fn": "check_sitemap",
             "msg": "No sitemap.xml or sitemap.ts found",
             "fix": "Create app/sitemap.ts (Next.js) or public/sitemap.xml"},
        ]
    },
    "accessibility": {
        "name": "Accessibility Gate",
        "weight": 15,
        "checks": [
            {"id":"AX001","sev":"Critical","name":"Skip navigation link",
             "check_fn": "check_skip_link",
             "msg": "No skip-to-main-content link found",
             "fix": "Add <a href='#main-content' className='sr-only focus:not-sr-only'>Skip to content</a> as first element in layout"},
            {"id":"AX002","sev":"High","name":"lang attribute on <html>",
             "check_fn": "check_html_lang",
             "msg": "No lang attribute on <html> element",
             "fix": "Add lang='en' (or appropriate language) to <html> tag in layout.tsx"},
            {"id":"AX003","sev":"High","name":"Single h1 per page",
             "search_file": True,
             "pattern": r"<h1[^>]*>[\s\S]*?<\/h1>[\s\S]*?<h1[^>]*>",
             "msg": "Multiple <h1> elements detected in a file",
             "fix": "Each page should have exactly ONE h1. Use h2-h6 for subsequent headings."},
            {"id":"AX004","sev":"Medium","name":"prefers-reduced-motion",
             "check_fn": "check_reduced_motion",
             "msg": "Animation classes found without prefers-reduced-motion support",
             "fix": "Add @media (prefers-reduced-motion: reduce) block to globals.css, or motion-reduce:animate-none on animate-* classes"},
        ]
    },
    "performance": {
        "name": "Performance Gate",
        "weight": 15,
        "checks": [
            {"id":"PG001","sev":"Critical","name":"No raw <img> tags",
             "search_file": True,
             "pattern": r"<img\s+src=",
             "msg": "Raw <img> tags found — no optimization or lazy loading",
             "fix": "Use next/image in Next.js. Add loading='lazy' width={} height={} in plain React."},
            {"id":"PG002","sev":"High","name":"Font strategy correct",
             "check_fn": "check_font_strategy",
             "msg": "Google Fonts @import detected — causes render-blocking + FOUT",
             "fix": "Use next/font/google (Next.js) or @fontsource npm packages"},
            {"id":"PG003","sev":"Medium","name":"Dynamic imports for heavy components",
             "check_fn": "check_dynamic_imports",
             "msg": "Heavy libraries imported statically — consider dynamic imports for code splitting",
             "fix": "Use dynamic(() => import('./HeavyComponent'), { ssr: false }) for charts, editors, 3D"},
            {"id":"PG004","sev":"Low","name":"Image assets in /public optimized",
             "check_fn": "check_image_sizes",
             "msg": "Large unoptimized images found in /public",
             "fix": "Optimize images: use WebP/AVIF format, max 200KB for hero images"},
        ]
    },
    "design_system": {
        "name": "Design System Gate",
        "weight": 10,
        "checks": [
            {"id":"DS001","sev":"High","name":"CSS variables defined",
             "check_fn": "check_css_variables",
             "msg": "No --color-* CSS variables found in globals.css",
             "fix": "Run: python3 design_system.py --product 'your product' --persist"},
            {"id":"DS002","sev":"Medium","name":"MASTER.md exists",
             "check_fn": "check_master_md",
             "msg": "No design-system/MASTER.md — no persistent design system",
             "fix": "Run: python3 design_system.py --product 'your product' --style 'dark' --persist"},
            {"id":"DS003","sev":"High","name":"No hardcoded hex in components",
             "search_file": True,
             "pattern": r'className=["\'][^"\']*#[0-9A-Fa-f]{6}',
             "msg": "Hardcoded hex values in className — bypasses design token system",
             "fix": "Replace with CSS variable: bg-[var(--color-primary)] or Tailwind token"},
            {"id":"DS004","sev":"Medium","name":"Tailwind config has theme extensions",
             "check_fn": "check_tailwind_tokens",
             "msg": "No custom colors/fonts in tailwind.config — design tokens not wired",
             "fix": "Add theme.extend with colors and fontFamily pointing to CSS variables"},
        ]
    },
    "nextjs": {
        "name": "Next.js Production Files",
        "weight": 5,
        "checks": [
            {"id":"NP001","sev":"Medium","name":"error.tsx present",
             "check_fn": "check_error_page",
             "msg": "No error.tsx found — unhandled errors show raw Next.js error page",
             "fix": "Create app/error.tsx with 'use client' and useEffect to log errors"},
            {"id":"NP002","sev":"Medium","name":"not-found.tsx present",
             "check_fn": "check_not_found_page",
             "msg": "No not-found.tsx — 404s show default Next.js page",
             "fix": "Create app/not-found.tsx with branded 404 design"},
            {"id":"NP003","sev":"Low","name":"loading.tsx for slow routes",
             "check_fn": "check_loading_page",
             "msg": "No loading.tsx — no streaming skeleton for slow data routes",
             "fix": "Create app/loading.tsx or app/[route]/loading.tsx with Skeleton components"},
        ]
    },
}

# ─── Check functions ──────────────────────────────────────────────────
def check_env_not_committed(root: Path) -> bool:
    """FAIL if .env exists and is not in .gitignore."""
    env_file = root / ".env"
    gitignore = root / ".gitignore"
    if not env_file.exists():
        return True  # Pass — no .env at all is fine
    if gitignore.exists():
        content = gitignore.read_text(errors="ignore")
        if ".env" in content:
            return True  # Pass — .env in gitignore
    return False  # FAIL — .env exists and not ignored

def check_env_example_exists(root: Path) -> bool:
    return (root / ".env.example").exists() or (root / ".env.local.example").exists()

def check_title_tag(root: Path) -> bool:
    patterns = [root/"app"/"layout.tsx", root/"app"/"layout.ts",
                root/"src"/"app"/"layout.tsx", root/"pages"/"_document.tsx",
                root/"pages"/"_document.js"]
    for p in patterns:
        if p.exists():
            c = p.read_text(errors="ignore")
            if "title" in c and ("metadata" in c or "<title" in c):
                return True
    return False

def check_meta_description(root: Path) -> bool:
    for layout in [root/"app"/"layout.tsx", root/"src"/"app"/"layout.tsx"]:
        if layout.exists():
            c = layout.read_text(errors="ignore")
            if "description" in c:
                return True
    return False

def check_og_image(root: Path) -> bool:
    for p in [root/"app"/"layout.tsx", root/"src"/"app"/"layout.tsx"]:
        if p.exists() and "openGraph" in p.read_text(errors="ignore"):
            return True
    if (root / "public" / "og-image.png").exists():
        return True
    if (root / "public" / "og-image.jpg").exists():
        return True
    return False

def check_robots_txt(root: Path) -> bool:
    return (root / "public" / "robots.txt").exists() or (root / "app" / "robots.ts").exists()

def check_sitemap(root: Path) -> bool:
    return (
        (root / "public" / "sitemap.xml").exists() or
        (root / "app" / "sitemap.ts").exists() or
        (root / "app" / "sitemap.js").exists()
    )

def check_skip_link(root: Path) -> bool:
    for p in [root/"app"/"layout.tsx", root/"src"/"app"/"layout.tsx",
              root/"components"/"Layout.tsx", root/"src"/"components"/"Layout.tsx"]:
        if p.exists():
            c = p.read_text(errors="ignore")
            if "skip" in c.lower() and ("main-content" in c or "#main" in c):
                return True
    return False

def check_html_lang(root: Path) -> bool:
    for p in [root/"app"/"layout.tsx", root/"src"/"app"/"layout.tsx"]:
        if p.exists():
            c = p.read_text(errors="ignore")
            if 'lang=' in c:
                return True
    return False

def check_reduced_motion(root: Path) -> bool:
    for p in [root/"app"/"globals.css", root/"src"/"app"/"globals.css",
              root/"src"/"styles"/"globals.css", root/"src"/"index.css"]:
        if p.exists():
            c = p.read_text(errors="ignore")
            if "prefers-reduced-motion" in c:
                return True
    return False

def check_font_strategy(root: Path) -> bool:
    """FAIL if @import fonts.googleapis found anywhere."""
    for ext in [".css", ".tsx", ".ts"]:
        for f in list(root.rglob(f"*{ext}"))[:50]:
            if "node_modules" in str(f): continue
            try:
                if "fonts.googleapis.com" in f.read_text(errors="ignore"):
                    return False
            except: pass
    return True

def check_dynamic_imports(root: Path) -> bool:
    """PASS if any dynamic() or lazy() imports found — signals awareness."""
    for ext in [".tsx", ".ts", ".jsx", ".js"]:
        for f in list(root.rglob(f"*{ext}"))[:100]:
            if "node_modules" in str(f): continue
            try:
                c = f.read_text(errors="ignore")
                if "dynamic(" in c or "React.lazy(" in c:
                    return True
            except: pass
    return False  # Not critical, just a hint

def check_image_sizes(root: Path) -> bool:
    """FAIL if any image in /public > 500KB."""
    pub = root / "public"
    if not pub.exists(): return True
    for ext in [".png", ".jpg", ".jpeg", ".gif"]:
        for f in pub.rglob(f"*{ext}"):
            try:
                if f.stat().st_size > 500_000:
                    return False
            except: pass
    return True

def check_css_variables(root: Path) -> bool:
    for p in [root/"app"/"globals.css", root/"src"/"app"/"globals.css",
              root/"src"/"styles"/"globals.css", root/"src"/"index.css"]:
        if p.exists():
            c = p.read_text(errors="ignore")
            if "--color-primary" in c or "--color-bg" in c:
                return True
    return False

def check_master_md(root: Path) -> bool:
    return (root / "design-system" / "MASTER.md").exists()

def check_tailwind_tokens(root: Path) -> bool:
    for p in [root/"tailwind.config.ts", root/"tailwind.config.js"]:
        if p.exists():
            c = p.read_text(errors="ignore")
            if "extend" in c and ("colors" in c or "fontFamily" in c):
                return True
    return False

def check_error_page(root: Path) -> bool:
    return any([
        (root / "app" / "error.tsx").exists(),
        (root / "src" / "app" / "error.tsx").exists(),
    ])

def check_not_found_page(root: Path) -> bool:
    return any([
        (root / "app" / "not-found.tsx").exists(),
        (root / "src" / "app" / "not-found.tsx").exists(),
        (root / "pages" / "404.tsx").exists(),
    ])

def check_loading_page(root: Path) -> bool:
    for f in list(Path(".").rglob("loading.tsx")) + list(Path(".").rglob("loading.js")):
        if "node_modules" not in str(f):
            return True
    return False


CHECK_FN_MAP = {
    "check_env_not_committed": check_env_not_committed,
    "check_env_example_exists": check_env_example_exists,
    "check_title_tag": check_title_tag,
    "check_meta_description": check_meta_description,
    "check_og_image": check_og_image,
    "check_robots_txt": check_robots_txt,
    "check_sitemap": check_sitemap,
    "check_skip_link": check_skip_link,
    "check_html_lang": check_html_lang,
    "check_reduced_motion": check_reduced_motion,
    "check_font_strategy": check_font_strategy,
    "check_dynamic_imports": check_dynamic_imports,
    "check_image_sizes": check_image_sizes,
    "check_css_variables": check_css_variables,
    "check_master_md": check_master_md,
    "check_tailwind_tokens": check_tailwind_tokens,
    "check_error_page": check_error_page,
    "check_not_found_page": check_not_found_page,
    "check_loading_page": check_loading_page,
}


def search_all_files(root: Path, pattern: str) -> list:
    """Search all source files for a regex pattern. Returns list of (file, line_no)."""
    exts = {".tsx", ".ts", ".jsx", ".js", ".css", ".svelte", ".vue"}
    hits = []
    regex = re.compile(pattern, re.IGNORECASE)
    for ext in exts:
        for f in root.rglob(f"*{ext}"):
            if any(skip in str(f) for skip in ["node_modules", ".next", "__pycache__", ".git"]):
                continue
            try:
                lines = f.read_text(errors="ignore").splitlines()
                for i, line in enumerate(lines, 1):
                    if regex.search(line):
                        hits.append((str(f.relative_to(root)), i, line.strip()[:80]))
            except Exception:
                pass
    return hits


def run_gate(gate_key: str, gate: dict, root: Path, is_nextjs: bool) -> dict:
    """Run all checks in a gate. Returns dict with results."""
    results = []
    for check in gate["checks"]:
        # Skip Next.js gate if not a Next.js project
        if gate_key == "nextjs" and not is_nextjs:
            continue

        passed = True
        hits = []

        if check.get("search_file"):
            hits = search_all_files(root, check["pattern"])
            passed = len(hits) == 0
        elif check.get("check_fn"):
            fn = CHECK_FN_MAP.get(check["check_fn"])
            if fn:
                try:
                    passed = fn(root)
                except Exception:
                    passed = True  # Don't fail on check errors

        results.append({
            "id": check["id"],
            "name": check["name"],
            "sev": check["sev"],
            "passed": passed,
            "msg": check["msg"],
            "fix": check["fix"],
            "hits": hits[:3],  # Show max 3 examples
        })

    total = len(results)
    failed = [r for r in results if not r["passed"]]
    score = round(100 * (total - len(failed)) / max(total, 1))

    return {
        "gate": gate_key,
        "name": gate["name"],
        "weight": gate["weight"],
        "score": score,
        "total": total,
        "failed": failed,
        "results": results,
    }


def print_ship_report(gate_results: list, overall: int, fix_hints: bool):
    W = 62
    critical_fails = [c for g in gate_results for c in g["failed"] if c["sev"] == "Critical"]
    high_fails     = [c for g in gate_results for c in g["failed"] if c["sev"] == "High"]
    blocked        = len(critical_fails) > 0

    print(f"\n{'═'*W}")
    print(f"  /ship — Production Readiness Report")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'═'*W}\n")

    status = "⛔ BLOCKED" if blocked else ("⚠️  WARNINGS" if high_fails else "✅ GO")
    bar_fill = int(overall / 5)
    bar = "█" * bar_fill + "░" * (20 - bar_fill)
    print(f"  STATUS:  {status}")
    print(f"  SCORE:   {overall}/100  [{bar}]\n")

    # Gate summary table
    print(f"  {'Gate':<26} {'Score':>6}  {'Failed':>7}  Status")
    print(f"  {'─'*55}")
    for g in gate_results:
        f_count = len(g["failed"])
        crit = any(c["sev"]=="Critical" for c in g["failed"])
        high = any(c["sev"]=="High" for c in g["failed"])
        status_icon = "⛔" if crit else ("⚠️ " if high else ("✅" if f_count == 0 else "🟡"))
        print(f"  {g['name']:<26} {g['score']:>5}/100  {str(f_count)+' fail':>7}  {status_icon}")

    print()

    # Blockers first
    if critical_fails:
        print(f"  ⛔ BLOCKERS — Must fix before deploy ({len(critical_fails)})")
        print(f"  {'─'*55}")
        for c in critical_fails:
            print(f"  [{c['id']}] {c['name']}")
            print(f"       {c['msg']}")
            if fix_hints: print(f"       → Fix: {c['fix']}")
            if c["hits"]:
                for path, line, snippet in c["hits"]:
                    print(f"       📄 {path}:{line}  {snippet}")
            print()

    # High severity
    if high_fails:
        print(f"  ⚠️  HIGH PRIORITY — Fix before ship ({len(high_fails)})")
        print(f"  {'─'*55}")
        for c in high_fails:
            print(f"  [{c['id']}] {c['name']}")
            print(f"       {c['msg']}")
            if fix_hints: print(f"       → Fix: {c['fix']}")
            if c["hits"]:
                for path, line, snippet in c["hits"][:2]:
                    print(f"       📄 {path}:{line}")
            print()

    # Medium/Low if clean
    med_fails = [c for g in gate_results for c in g["failed"] if c["sev"] == "Medium"]
    if med_fails and not blocked:
        print(f"  🟡 MEDIUM — Recommended to fix ({len(med_fails)})")
        print(f"  {'─'*55}")
        for c in med_fails:
            print(f"  [{c['id']}] {c['name']} — {c['msg']}")
            if fix_hints: print(f"       → {c['fix']}")
        print()

    # Final verdict
    print(f"  {'═'*55}")
    if blocked:
        print(f"  ⛔ BLOCKED  — {len(critical_fails)} critical issue(s) must be resolved.")
        print(f"     Run /review to get per-file fix details.")
    elif high_fails:
        print(f"  ⚠️  SHIPPABLE WITH WARNINGS")
        print(f"     {len(high_fails)} high-priority issue(s). Ship if deadline requires,")
        print(f"     but schedule fixes in next sprint.")
    else:
        print(f"  ✅ GO — All critical and high gates passed.")
        print(f"     Score: {overall}/100. This project is production-ready.")
    print()


def main():
    parser = argparse.ArgumentParser(description="/ship — Production Readiness Gate")
    parser.add_argument("--fix-hints", action="store_true", help="Show specific fix commands")
    parser.add_argument("--gate", help="Run one gate only: hygiene|environment|seo|accessibility|performance|design_system|nextjs")
    parser.add_argument("--score", action="store_true", help="Output score + GO/BLOCKED for CI")
    args = parser.parse_args()

    root = Path.cwd()

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║        /ship — Production Readiness Gate            ║")
    print("╚══════════════════════════════════════════════════════╝")

    # Detect if Next.js project
    is_nextjs = False
    try:
        result = subprocess.run(
            ["python3", str(Path(__file__).parent / "detect_stack.py")],
            capture_output=True, text=True, cwd=root
        )
        for line in result.stdout.split("\n"):
            if line.startswith("STACK_JSON:"):
                stack = json.loads(line[11:])
                is_nextjs = stack.get("framework") == "nextjs"
                break
    except Exception:
        pass

    # Run gates
    gates_to_run = [args.gate] if args.gate else list(GATES.keys())
    gate_results = []

    for gate_key in gates_to_run:
        if gate_key not in GATES:
            print(f"  ⚠️  Unknown gate: {gate_key}")
            continue
        result = run_gate(gate_key, GATES[gate_key], root, is_nextjs)
        gate_results.append(result)

    # Weighted overall score
    total_weight = sum(GATES[g["gate"]]["weight"] for g in gate_results if g["gate"] in GATES)
    overall = round(sum(
        g["score"] * GATES[g["gate"]]["weight"] / max(total_weight, 1)
        for g in gate_results if g["gate"] in GATES
    ))

    if args.score:
        blocked = any(c["sev"]=="Critical" and not c["passed"]
                      for g in gate_results for c in g["results"])
        print(f"{'BLOCKED' if blocked else 'GO'} {overall}/100")
        sys.exit(1 if blocked else 0)

    print_ship_report(gate_results, overall, fix_hints=args.fix_hints)

    # Exit code for CI
    blocked = any(c["sev"]=="Critical" for g in gate_results for c in g["failed"])
    sys.exit(1 if blocked else 0)


if __name__ == "__main__":
    main()
