#!/usr/bin/env python3
"""
/approved — Design approval recorder v1.0
Stamps the current design into design-system/MASTER.md and creates
a timestamped approval snapshot. Unlocks /apply.

Usage:
  python3 approved.py                          # approve current design
  python3 approved.py --message "Dark landing approved after client review"
  python3 approved.py --page pricing           # approve a specific page
  python3 approved.py --list                   # list past approvals
"""

import sys, json, argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from core import resolve_product

def main():
    parser = argparse.ArgumentParser(description="/approved — Design Approval Recorder")
    parser.add_argument("--message","-m", default="", help="Approval note")
    parser.add_argument("--page",   "-p", default="all", help="Page type being approved")
    parser.add_argument("--list",   "-l", action="store_true", help="List past approvals")
    args = parser.parse_args()

    root      = Path.cwd()
    ds_dir    = root / "design-system"
    approved_dir = ds_dir / "approved"
    approved_dir.mkdir(parents=True, exist_ok=True)

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║        /approved — Design Approval Recorder         ║")
    print("╚══════════════════════════════════════════════════════╝\n")

    if args.list:
        snapshots = sorted(approved_dir.glob("*.json"), reverse=True)
        if not snapshots:
            print("  No approvals recorded yet.\n")
            return
        print(f"  Past approvals ({len(snapshots)}):\n")
        for snap in snapshots[:10]:
            d = json.loads(snap.read_text())
            print(f"  [{d['timestamp']}] {d['page']} — {d.get('message','(no note)')}")
        print()
        return

    # Read current design system state
    master = ds_dir / "MASTER.md"
    tokens = {}
    if master.exists():
        content = master.read_text(errors="ignore")
        for line in content.splitlines():
            line = line.strip()
            for css, key in [
                ("--color-primary:", "primary"), ("--color-secondary:", "secondary"),
                ("--color-cta:", "cta"), ("--color-bg:", "bg"), ("--color-surface:", "surface"),
                ("--color-text:", "text"), ("--color-muted:", "muted"), ("--color-border:", "border"),
            ]:
                if line.startswith(css):
                    tokens[key] = line.split(":", 1)[1].strip().rstrip(";")
            if line.startswith("--font-heading:"):
                raw = line.split(":", 1)[1].strip().rstrip(";")
                tokens["font_heading"] = raw.split(",")[0].strip().strip("'\"")
            if line.startswith("--font-body:"):
                raw = line.split(":", 1)[1].strip().rstrip(";")
                tokens["font_body"] = raw.split(",")[0].strip().strip("'\"")
    else:
        print("  ⚠  No design-system/MASTER.md found.")
        print("  Run /design first, then /preview to review, then /approved.\n")
        sys.exit(1)

    if not tokens:
        print("  ⚠  No design tokens found in MASTER.md.")
        print("  Run /design --persist to generate the design system first.\n")
        sys.exit(1)

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ts_file = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create approval snapshot
    snapshot = {
        "timestamp": ts,
        "page": args.page,
        "message": args.message or f"Design approved via /approved command",
        "tokens": tokens,
        "status": "approved",
    }
    snap_path = approved_dir / f"{ts_file}_{args.page}.json"
    snap_path.write_text(json.dumps(snapshot, indent=2))

    # Append approval record to MASTER.md
    approval_block = f"""
---
## Approval Record
**Approved:** {ts}
**Page:** {args.page}
**Note:** {args.message or '(no note)'}
**Status:** ✅ APPROVED — Ready for /apply

Tokens approved:
```
Primary:  {tokens.get('primary', '—')}
CTA:      {tokens.get('cta', '—')}
BG:       {tokens.get('bg', '—')}
Heading:  {tokens.get('font_heading', '—')}
Body:     {tokens.get('font_body', '—')}
```
"""
    with open(master, "a") as f:
        f.write(approval_block)

    print(f"  ✅ Design approved!")
    print(f"  Timestamp:  {ts}")
    print(f"  Page:       {args.page}")
    if args.message:
        print(f"  Note:       {args.message}")
    print(f"\n  Snapshot saved → design-system/approved/{snap_path.name}")
    print(f"  MASTER.md updated with approval record\n")
    print(f"  ─────────────────────────────────────────────────")
    print(f"  Approved tokens:")
    for k, v in tokens.items():
        if k not in ("font_heading", "font_body"):
            print(f"  {k+':':12} {v}")
    print(f"  Heading font: {tokens.get('font_heading','—')}")
    print(f"  Body font:    {tokens.get('font_body','—')}")
    print(f"\n  Next step → run /apply to generate production code:")
    print(f"  python3 .claude/skills/ui-design-intelligence/scripts/apply.py")
    print(f"  python3 .claude/skills/ui-design-intelligence/scripts/apply.py --page {args.page}")
    print()

if __name__ == "__main__":
    main()
