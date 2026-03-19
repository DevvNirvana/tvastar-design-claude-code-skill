#!/usr/bin/env python3
"""
/a11y — Full WCAG 2.1 AA Accessibility Auditor v1.0 (Phase 10.1)
Deeper than /review. Full contrast math, heading hierarchy, ARIA validation.
Usage:
  python3 a11y.py src/components/Hero.tsx
  python3 a11y.py --contrast #6366F1 --bg #09090B
  python3 a11y.py --wcag             # full WCAG 2.1 checklist
  python3 a11y.py --report src/      # save full report
"""
import sys, re, argparse, json
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).parent))
from color_science import contrast_ratio, wcag_grade

WCAG_CRITERIA = [
    {"id":"1.1.1","level":"A", "name":"Non-text Content",       "check":"Images have alt text"},
    {"id":"1.3.1","level":"A", "name":"Info and Relationships",  "check":"Semantic HTML used correctly"},
    {"id":"1.3.2","level":"A", "name":"Meaningful Sequence",     "check":"Reading order makes sense"},
    {"id":"1.3.3","level":"A", "name":"Sensory Characteristics", "check":"Instructions not color-only"},
    {"id":"1.4.1","level":"A", "name":"Use of Color",            "check":"Color not sole distinguisher"},
    {"id":"1.4.3","level":"AA","name":"Contrast (Minimum)",      "check":"Normal text: 4.5:1, Large: 3:1"},
    {"id":"1.4.4","level":"AA","name":"Resize Text",             "check":"Text resizable to 200% no loss"},
    {"id":"1.4.10","level":"AA","name":"Reflow",                 "check":"No horizontal scroll at 320px"},
    {"id":"1.4.11","level":"AA","name":"Non-text Contrast",      "check":"UI components 3:1 contrast"},
    {"id":"1.4.12","level":"AA","name":"Text Spacing",           "check":"No loss with spacing overrides"},
    {"id":"2.1.1","level":"A", "name":"Keyboard",                "check":"All functionality keyboard accessible"},
    {"id":"2.1.2","level":"A", "name":"No Keyboard Trap",        "check":"Focus not trapped unexpectedly"},
    {"id":"2.4.1","level":"A", "name":"Bypass Blocks",           "check":"Skip navigation link present"},
    {"id":"2.4.2","level":"A", "name":"Page Titled",             "check":"Descriptive page title"},
    {"id":"2.4.3","level":"A", "name":"Focus Order",             "check":"Focus order logical"},
    {"id":"2.4.6","level":"AA","name":"Headings and Labels",     "check":"Descriptive headings/labels"},
    {"id":"2.4.7","level":"AA","name":"Focus Visible",           "check":"Keyboard focus indicator visible"},
    {"id":"3.1.1","level":"A", "name":"Language of Page",        "check":"lang attribute on html"},
    {"id":"3.2.1","level":"A", "name":"On Focus",                "check":"No context change on focus"},
    {"id":"3.3.1","level":"A", "name":"Error Identification",    "check":"Errors identified in text"},
    {"id":"3.3.2","level":"A", "name":"Labels or Instructions",  "check":"Labels for all form inputs"},
    {"id":"4.1.1","level":"A", "name":"Parsing",                 "check":"Valid, well-formed HTML"},
    {"id":"4.1.2","level":"A", "name":"Name, Role, Value",       "check":"UI components have accessible names"},
    {"id":"4.1.3","level":"AA","name":"Status Messages",         "check":"Status changes announced"},
]

A11Y_RULES = [
    {"id":"AX001","sev":"Critical","pattern":r'<(?:img|Image)\s(?![^>]*alt=)',
     "msg":"Image missing alt attribute","fix":"Add alt='' for decorative, alt='description' for meaningful"},
    {"id":"AX002","sev":"Critical","pattern":r'<(?:input|textarea|select)\b(?![^>]*(?:aria-label|aria-labelledby|id=))',
     "msg":"Form input without accessible label","fix":"Add <label htmlFor='id'> or aria-label"},
    {"id":"AX003","sev":"Critical","pattern":r'<button[^>]*>\s*<(?:svg|[A-Z][a-zA-Z]+Icon)(?![^<]*aria-label)',
     "msg":"Icon-only button may lack aria-label","fix":"Add aria-label='Action description' to icon-only buttons"},
    {"id":"AX004","sev":"Critical","pattern":r'focus:outline-none(?!\s+focus(?:-visible)?:ring)',
     "msg":"Focus removed without replacement","fix":"Add focus-visible:ring-2 focus-visible:ring-[var(--color-primary)]"},
    {"id":"AX005","sev":"High","pattern":r'<div[^>]*(?:onClick|onKeyDown)[^>]*>(?!.*role=)',
     "msg":"Clickable div without role","fix":"Use <button>, or add role='button' tabIndex={0}"},
    {"id":"AX006","sev":"High","pattern":r'<h[1-6][^>]*>.*</h[1-6]>[\s\S]{0,500}<h[1-6]',
     "msg":"Check heading hierarchy — ensure no levels skipped","fix":"h1 → h2 → h3, never skip"},
    {"id":"AX007","sev":"High","pattern":r'<(?:Dialog|Modal|AlertDialog)[^>]*>(?![\s\S]{0,300}(?:DialogTitle|aria-label))',
     "msg":"Dialog without accessible title","fix":"Add <DialogTitle> inside <DialogContent>"},
    {"id":"AX008","sev":"Medium","pattern":r'<(?:section|article|nav|aside|main|header|footer)[^>]*>(?!.*aria-label)',
     "msg":"Landmark without aria-label","fix":"Add aria-label='Section purpose' to landmark elements"},
    {"id":"AX009","sev":"Medium","pattern":r'tabIndex=\{-1\}',
     "msg":"tabIndex={-1} removes from tab order — verify intentional","fix":"Only on programmatically focused elements"},
    {"id":"AX010","sev":"High","pattern":r'<(?:Progress|progress)[^>]*>(?!.*aria-)',
     "msg":"Progress bar without ARIA attributes","fix":"Add role='progressbar' aria-valuenow aria-valuemin aria-valuemax"},
    {"id":"AX011","sev":"Medium","pattern":r'animate-(?!none)[a-z-]+(?!.*motion-reduce)',
     "msg":"Animation without motion-reduce support","fix":"Add motion-reduce:animate-none"},
    {"id":"AX012","sev":"High","pattern":r'placeholder=',
     "msg":"Verify placeholder is not the only label","fix":"Always have visible label OR aria-label in addition to placeholder"},
]

def audit_file(filepath: str) -> dict:
    path = Path(filepath)
    if not path.exists(): return {"error": f"Not found: {filepath}"}
    code = path.read_text(errors="ignore")
    issues = []
    for rule in A11Y_RULES:
        matches = list(re.finditer(rule["pattern"], code, re.IGNORECASE | re.MULTILINE))
        if matches:
            issues.append({**rule, "count": len(matches)})
    issues.sort(key=lambda x: {"Critical":0,"High":1,"Medium":2}[x["sev"]])
    score = max(0, 100 - sum({"Critical":20,"High":10,"Medium":5}[i["sev"]] * min(i["count"],2) for i in issues))
    return {"file": filepath, "issues": issues, "score": score,
            "counts": {"critical": len([i for i in issues if i["sev"]=="Critical"]),
                       "high":     len([i for i in issues if i["sev"]=="High"]),
                       "medium":   len([i for i in issues if i["sev"]=="Medium"])}}

def main():
    parser = argparse.ArgumentParser(description="/a11y — WCAG 2.1 AA Auditor")
    parser.add_argument("file",    nargs="?", help="File to audit")
    parser.add_argument("--contrast", help="Check contrast: --contrast #FG --bg #BG")
    parser.add_argument("--bg",       help="Background for contrast check")
    parser.add_argument("--wcag",     action="store_true", help="WCAG 2.1 AA checklist")
    parser.add_argument("--report",   help="Audit directory and save report")
    args = parser.parse_args()

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║        /a11y — WCAG 2.1 AA Auditor                 ║")
    print("╚══════════════════════════════════════════════════════╝\n")

    if args.contrast:
        bg = args.bg or "#FFFFFF"
        ratio = contrast_ratio(args.contrast, bg)
        aa_n, aaa_n, grade_n = wcag_grade(ratio, False)
        aa_l, aaa_l, grade_l = wcag_grade(ratio, True)
        print(f"  Foreground: {args.contrast}  Background: {bg}")
        print(f"  Ratio: {ratio}:1\n")
        print(f"  Normal text  (≥4.5:1): {grade_n}")
        print(f"  Large text   (≥3.0:1): {grade_l}")
        print(f"  UI elements  (≥3.0:1): {grade_l}")
        if not aa_n:
            from color_science import suggest_accessible_color
            sug = suggest_accessible_color(args.contrast, bg)
            sug_ratio = contrast_ratio(sug, bg)
            print(f"\n  Suggestion: {sug} ({sug_ratio}:1) ✅")
        print()
        return

    if args.wcag:
        print(f"  WCAG 2.1 AA Checklist ({len(WCAG_CRITERIA)} criteria)\n")
        current_group = ""
        for c in WCAG_CRITERIA:
            group = c["id"].split(".")[0]
            if group != current_group:
                groups = {"1":"1 — Perceivable","2":"2 — Operable","3":"3 — Understandable","4":"4 — Robust"}
                print(f"\n  Principle {groups.get(group, group)}")
                current_group = group
            lvl = "🔴" if c["level"]=="A" else "🟡"
            print(f"  [ ] {lvl} {c['id']} {c['name']:<30} {c['check']}")
        print()
        return

    if args.report:
        root = Path(args.report)
        all_issues = []
        files_checked = 0
        for ext in [".tsx",".ts",".jsx",".js"]:
            for f in root.rglob(f"*{ext}"):
                if "node_modules" in str(f) or ".next" in str(f): continue
                result = audit_file(str(f))
                if result.get("issues"):
                    all_issues.extend([(str(f.name), i) for i in result["issues"]])
                files_checked += 1
        report_path = Path.cwd()/"a11y-report.md"
        with open(report_path,"w") as rf:
            rf.write(f"# Accessibility Report\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            rf.write(f"Files checked: {files_checked} | Issues: {len(all_issues)}\n\n")
            for fname, issue in all_issues:
                rf.write(f"## {fname}\n**[{issue['id']}]** {issue['sev']}: {issue['msg']}\n\nFix: {issue['fix']}\n\n")
        print(f"  Report saved → a11y-report.md")
        print(f"  Files: {files_checked}  Issues: {len(all_issues)}\n")
        return

    if args.file:
        result = audit_file(args.file)
        if "error" in result: print(f"  ⚠  {result['error']}\n"); return
        c = result["counts"]
        print(f"  File: {args.file}")
        print(f"  Score: {result['score']}/100  🔴 {c['critical']} Critical  🟠 {c['high']} High  🟡 {c['medium']} Medium\n")
        for issue in result["issues"]:
            icon = {"Critical":"🔴","High":"🟠","Medium":"🟡"}[issue["sev"]]
            print(f"  {icon} [{issue['id']}] {issue['msg']}")
            print(f"       Fix: {issue['fix']}\n")
        if not result["issues"]: print("  ✅ No accessibility issues detected\n")
        return

    print("  Commands:")
    print("  python3 a11y.py src/Hero.tsx")
    print("  python3 a11y.py --contrast #6366F1 --bg #09090B")
    print("  python3 a11y.py --wcag")
    print("  python3 a11y.py --report src/\n")

if __name__ == "__main__":
    main()
