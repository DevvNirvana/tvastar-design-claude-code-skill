#!/usr/bin/env python3
"""
/heal — Auto-Fix Engine v1.0
Phase 6.1 — God-Level Roadmap

Reads /review output and auto-fixes known Critical and High issues.
Shows before/after score. Reports what it fixed vs what needs human review.

Usage:
  python3 heal.py src/components/Hero.tsx
  python3 heal.py src/components/Hero.tsx --dry-run
  python3 heal.py --all                      # heal all files in src/
  python3 heal.py --score                    # show improvement score only
"""

import sys, re, argparse, shutil
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from review import review_code, grade, detect_frameworks_from_file

# ═══════════════════════════════════════════════════════════════════════
# AUTO-FIX RULES — safe, mechanical transformations
# ═══════════════════════════════════════════════════════════════════════

def fix_cursor_pointer(code: str) -> tuple[str, int]:
    """Add cursor-pointer to <button> and <a> missing it."""
    count = 0
    # Match <button className="..." without cursor-pointer
    def add_cursor(m):
        nonlocal count
        tag = m.group(0)
        if 'cursor-' not in tag:
            count += 1
            return tag.replace('className="', 'className="cursor-pointer ').replace("className='", "className='cursor-pointer ")
        return tag
    code = re.sub(r'<(?:button|a)\s[^>]*className=["\'][^"\']*["\']', add_cursor, code)
    return code, count


def fix_motion_reduce(code: str) -> tuple[str, int]:
    """Add motion-reduce:animate-none alongside animate-* classes."""
    count = 0
    def add_reduce(m):
        nonlocal count
        cls = m.group(0)
        if 'motion-reduce' not in cls:
            count += 1
            anim_class = m.group(1)
            return cls.replace(anim_class, f'{anim_class} motion-reduce:animate-none')
        return cls
    code = re.sub(r'(animate-(?!none)[a-z-]+)', add_reduce, code)
    return code, count


def fix_focus_outline(code: str) -> tuple[str, int]:
    """Replace focus:outline-none with focus:outline-none + focus-visible:ring-2."""
    count = 0
    pattern = r'focus:outline-none(?!\s+focus[-:])'
    replacement = 'focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-primary)] focus-visible:ring-offset-2'
    new_code, n = re.subn(pattern, replacement, code)
    return new_code, n


def fix_console_logs(code: str) -> tuple[str, int]:
    """Remove console.log/warn/debug statements."""
    pattern = r'\n?\s*console\.(log|warn|debug)\([^)]*\);?\n?'
    new_code, count = re.subn(pattern, '\n', code)
    return new_code, count


def fix_img_alt(code: str) -> tuple[str, int]:
    """Add alt="" to <img> and <Image> missing alt attribute."""
    count = 0
    def add_alt(m):
        nonlocal count
        tag = m.group(0)
        if 'alt=' not in tag:
            count += 1
            # Add alt="" before the closing > or />
            return re.sub(r'(\s*\/?>)$', r' alt="" /* TODO: add descriptive alt text */\1', tag.rstrip())
        return tag
    code = re.sub(r'<(?:img|Image)\s[^>]*>', add_alt, code)
    return code, count


def fix_key_prop(code: str) -> tuple[str, int]:
    """Add key={index} fallback where .map() renders JSX without key."""
    count = 0
    # Match .map((item, i) => <SomeComponent without key=
    def add_key(m):
        nonlocal count
        mapping = m.group(0)
        if 'key=' not in mapping:
            count += 1
            # Add key={i} to the first JSX element in the map
            return re.sub(r'(<[A-Za-z][A-Za-z0-9]*)', r'\1 key={i} /* TODO: use stable id */', mapping, count=1)
        return mapping
    code = re.sub(r'\.map\(\([^)]+,\s*i\)\s*=>\s*<[^>]+', add_key, code)
    return code, count


def fix_hardcoded_hex(code: str) -> tuple[str, int]:
    """Convert hardcoded hex in className to CSS variable hints."""
    count = 0
    def replace_hex(m):
        nonlocal count
        hex_val = m.group(1)
        count += 1
        return f'bg-[var(--color-primary)] /* was: #{hex_val} — use CSS var */'
    # Only fix hex in bg- and text- classes
    code = re.sub(r'\bbg-\[#([0-9A-Fa-f]{6})\]', replace_hex, code)
    return code, count


def fix_transition_all(code: str) -> tuple[str, int]:
    """Replace transition-all with transition-colors where hover color changes."""
    count = 0
    # Only replace when near hover:bg or hover:text
    pattern = r'transition-all\s+duration-(\d+)(?=.*hover:(?:bg|text|border)-)'
    def replace(m):
        nonlocal count
        count += 1
        return f'transition-colors duration-{m.group(1)}'
    code = re.sub(pattern, replace, code)
    return code, count


def fix_todo_placeholders(code: str) -> tuple[str, int]:
    """Flag lorem ipsum and placeholder text (can't auto-fix, just count)."""
    pattern = r'Lorem ipsum|placeholder text|Coming soon\.\.\.|Insert here'
    matches = re.findall(pattern, code, re.IGNORECASE)
    return code, len(matches)  # Return unchanged — needs human


# ═══════════════════════════════════════════════════════════════════════
# FIX REGISTRY
# ═══════════════════════════════════════════════════════════════════════

AUTO_FIXES = [
    {"id": "F001", "name": "Add motion-reduce:animate-none",   "fn": fix_motion_reduce,  "safe": True},
    {"id": "F002", "name": "Fix focus:outline-none → ring",    "fn": fix_focus_outline,  "safe": True},
    {"id": "F003", "name": "Remove console.log statements",    "fn": fix_console_logs,   "safe": True},
    {"id": "F004", "name": "Add alt='' to images",             "fn": fix_img_alt,        "safe": True},
    {"id": "F005", "name": "Convert transition-all → specific","fn": fix_transition_all, "safe": True},
    {"id": "F006", "name": "Flag hardcoded hex in className",  "fn": fix_hardcoded_hex,  "safe": True},
]

HUMAN_REQUIRED = [
    {"id": "H001", "pattern": r"<div[^>]+onClick", "name": "div onClick → use <button>",
     "reason": "Requires HTML restructuring — Claude must rewrite the element."},
    {"id": "H002", "pattern": r"Lorem ipsum|placeholder text|TBD\b", "name": "Placeholder content",
     "reason": "Requires real copy — only a human or /design workflow can supply it."},
    {"id": "H003", "pattern": r"#[0-9A-Fa-f]{6}.*contrast|contrast.*fail", "name": "Color contrast failure",
     "reason": "Requires design decision — run /color --check [fg] --bg [bg] for suggestion."},
]


def heal_file(filepath: str, dry_run: bool = False) -> dict:
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}

    original = path.read_text(errors="ignore")
    frameworks = detect_frameworks_from_file(filepath)

    # Score before
    before_result = review_code(original, path.name, frameworks)
    before_score  = before_result["overall"]

    # Apply all auto-fixes
    code   = original
    fixes_applied = []

    for fix in AUTO_FIXES:
        new_code, count = fix["fn"](code)
        if count > 0:
            fixes_applied.append({"id": fix["id"], "name": fix["name"], "count": count})
            code = new_code

    # Find human-required issues
    human_issues = []
    for h in HUMAN_REQUIRED:
        if re.search(h["pattern"], original, re.IGNORECASE):
            human_issues.append(h)

    # Score after
    after_result = review_code(code, path.name, frameworks)
    after_score  = after_result["overall"]
    improvement  = after_score - before_score

    if not dry_run and fixes_applied:
        # Backup original
        backup_path = path.with_suffix(f".pre-heal{path.suffix}")
        shutil.copy2(path, backup_path)
        # Write healed file
        path.write_text(code)

    return {
        "file":          filepath,
        "before_score":  before_score,
        "after_score":   after_score,
        "improvement":   improvement,
        "fixes_applied": fixes_applied,
        "human_issues":  human_issues,
        "dry_run":       dry_run,
        "backup":        str(path.with_suffix(f".pre-heal{path.suffix}")) if not dry_run and fixes_applied else None,
    }


def print_heal_result(r: dict):
    if "error" in r:
        print(f"  ⚠  {r['error']}")
        return

    g_before, _ = grade(r["before_score"])
    g_after,  _ = grade(r["after_score"])
    arrow = "→" if r["improvement"] > 0 else "="

    print(f"\n  File: {r['file']}")
    print(f"  Score: {r['before_score']}/100 (Grade {g_before}) {arrow} {r['after_score']}/100 (Grade {g_after})", end="")
    if r["improvement"] > 0:
        print(f"  [+{r['improvement']} pts]")
    else:
        print(" [no change]")

    if r["fixes_applied"]:
        print(f"\n  ✅ Auto-fixed ({len(r['fixes_applied'])} categories):")
        for fix in r["fixes_applied"]:
            print(f"     [{fix['id']}] {fix['name']} ({fix['count']} instances)")

    if r["human_issues"]:
        print(f"\n  ⚠️  Requires human review ({len(r['human_issues'])} issues):")
        for h in r["human_issues"]:
            print(f"     [{h['id']}] {h['name']}")
            print(f"            → {h['reason']}")

    if r["dry_run"]:
        print(f"\n  [DRY RUN] No files changed.")
    elif r["backup"]:
        print(f"\n  Backup: {r['backup']}")
    elif not r["fixes_applied"]:
        print(f"\n  ✅ No auto-fixable issues found.")
    print()


def main():
    parser = argparse.ArgumentParser(description="/heal — Auto-Fix Engine")
    parser.add_argument("file",       nargs="?", help="File to heal")
    parser.add_argument("--all",      action="store_true", help="Heal all source files")
    parser.add_argument("--dry-run",  action="store_true", help="Show changes without applying")
    parser.add_argument("--score",    action="store_true", help="Show score improvement only")
    args = parser.parse_args()

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║        /heal — Auto-Fix Engine                      ║")
    print("╚══════════════════════════════════════════════════════╝")

    if args.file:
        result = heal_file(args.file, dry_run=args.dry_run)
        if args.score:
            print(f"\n  {result.get('before_score',0)} → {result.get('after_score',0)} "
                  f"(+{result.get('improvement',0)} pts)\n")
        else:
            print_heal_result(result)

    elif args.all:
        root = Path.cwd()
        exts = {".tsx", ".ts", ".jsx", ".js"}
        files = []
        for src in ["src","app","components","pages"]:
            sp = root/src
            if not sp.exists(): continue
            for ext in exts:
                for f in sp.rglob(f"*{ext}"):
                    if not any(skip in str(f) for skip in ["node_modules",".next","__pycache__"]):
                        files.append(str(f))

        if not files:
            print("\n  No source files found.\n")
            return

        total_before = total_after = 0
        total_fixes  = 0
        print(f"\n  Healing {len(files)} files{'(dry run)' if args.dry_run else ''}...\n")

        for f in files:
            result = heal_file(f, dry_run=args.dry_run)
            if "error" not in result:
                total_before += result["before_score"]
                total_after  += result["after_score"]
                total_fixes  += sum(fx["count"] for fx in result["fixes_applied"])
                if result["fixes_applied"] or result["human_issues"]:
                    print_heal_result(result)

        avg_before = round(total_before / max(len(files),1))
        avg_after  = round(total_after  / max(len(files),1))
        print(f"  ═══════════════════════════════════════════════════")
        print(f"  Files healed:   {len(files)}")
        print(f"  Avg score:      {avg_before}/100 → {avg_after}/100  (+{avg_after-avg_before} pts)")
        print(f"  Total fixes:    {total_fixes} instances auto-corrected")
        print()

    else:
        print("\n  Usage:")
        print("  python3 heal.py src/components/Hero.tsx")
        print("  python3 heal.py src/components/Hero.tsx --dry-run")
        print("  python3 heal.py --all")
        print("  python3 heal.py src/Hero.tsx --score\n")


if __name__ == "__main__":
    main()
