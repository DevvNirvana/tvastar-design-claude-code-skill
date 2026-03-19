#!/usr/bin/env python3
"""
UI Design Intelligence — Search CLI v2.0
Usage:
  python3 search.py "AI startup" --domain palette
  python3 search.py "dark luxury" --domain typography
  python3 search.py "landing page SaaS" --domain pattern
  python3 search.py "dark gradient" --design-system --product "SaaS" --persist --dark
  python3 search.py "background hero dark" --domain library
  python3 search.py "button cta" --domain library
"""
import argparse, sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from core import (search_palettes, search_typography, search_styles, search_ux_laws,
                  resolve_product, get_pattern, select_components,
                  PALETTES, TYPOGRAPHY, STYLES, UX_LAWS, PAGE_PATTERNS, LIBRARY_CATALOG)

def print_palette(p):
    print(f"\n  [{p['name']}]")
    print(f"  Vibe:    {p['vibe'][:65]}")
    print(f"  Primary: {p['primary']}  Secondary: {p['secondary']}  CTA: {p['cta']}")
    print(f"  BG:      {p['bg']}  Text: {p['text']}  Muted: {p['muted']}")

def print_typo(t):
    print(f"\n  [{t['name']}]")
    print(f"  Vibe:    {t['vibe'][:65]}")
    print(f"  Heading: {t['heading']} ({t['weights_h']})")
    print(f"  Body:    {t['body']} ({t['weights_b']})")

def print_style(s):
    print(f"\n  [{s['name']}]")
    print(f"  Vibe:    {s['vibe'][:65]}")
    print(f"  Effects: {s['effects']}")
    for lib, comps in [("React Bits", s.get("react_bits",[])), ("Aceternity", s.get("aceternity",[])), ("Magic UI", s.get("magicui",[]))]:
        if comps: print(f"  {lib+':':12} {', '.join(comps)}")

def print_law(u):
    print(f"\n  [{u['law']}]")
    print(f"  Rule:  {u['summary']}")
    print(f"  Apply: {u['apply']}")

def print_pattern(p):
    print(f"\n  [{p['name']}]  type={p['type']}")
    for i,s in enumerate(p['sections'],1): print(f"    {i:2}. {s}")
    print(f"  CTA:  {p['cta_placement']}")
    print(f"  Note: {p['conversion']}")

def search_library(query):
    """Find components across all libraries matching a query."""
    q = query.lower()
    results = []
    for lib_key, lib in LIBRARY_CATALOG.items():
        for cat, items in lib.get("components",{}).items():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        score = sum(1 for w in q.split() if w in item.get("name","").lower() or w in item.get("desc","").lower() or w in cat.lower())
                        if score > 0:
                            results.append({"lib": lib["name"], "lib_key": lib_key, "category": cat,
                                            "component": item["name"], "desc": item["desc"],
                                            "wow": item.get("wow_factor",5), "score": score})
    results.sort(key=lambda x: (-x["score"], -x["wow"]))
    return results[:8]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("--domain","-d", choices=["palette","typography","style","ux","pattern","library","all"], default=None)
    parser.add_argument("--design-system","-ds", action="store_true")
    parser.add_argument("--product","-p", default=None)
    parser.add_argument("--style",  "-s", default="")
    parser.add_argument("--dark",   action="store_true")
    parser.add_argument("--persist",action="store_true")
    parser.add_argument("--page",   default="landing")
    parser.add_argument("-n","--max-results", type=int, default=3)
    args = parser.parse_args()

    query = args.query or args.product or ""

    if args.design_system:
        from design_system import generate
        generate(args.product or query, args.style or query, args.dark, args.persist, args.page)
        sys.exit(0)

    domain = args.domain or "all"
    n = args.max_results

    print(f"\n  ─── UI Design Intelligence Search v2.0 ────────────")
    print(f"  Query: '{query}'  |  Domain: {domain}")

    if domain in ("palette","all"):
        print("\n  PALETTES:")
        for p in (search_palettes(query, n) or PALETTES[:n]): print_palette(p)

    if domain in ("typography","all"):
        print("\n  TYPOGRAPHY:")
        for t in (search_typography(query, n) or TYPOGRAPHY[:n]): print_typo(t)

    if domain in ("style","all"):
        print("\n  STYLES:")
        for s in (search_styles(query, n) or STYLES[:n]): print_style(s)

    if domain in ("ux","all"):
        print("\n  UX LAWS:")
        for u in search_ux_laws(query, n): print_law(u)

    if domain == "pattern":
        print("\n  PAGE PATTERNS:")
        print_pattern(get_pattern(query))

    if domain == "library" or (domain == "all" and query):
        print("\n  LIBRARY COMPONENTS:")
        results = search_library(query)
        if results:
            for r in results:
                install = LIBRARY_CATALOG[r["lib_key"]].get("install_method","copy")
                base_url = LIBRARY_CATALOG[r["lib_key"]].get("base_install_url","")
                if "npx shadcn" in install:
                    cmd = f'npx shadcn@latest add "{base_url}{r["component"]}"'
                elif "npx magicui" in install:
                    cmd = f'npx magicui-cli@latest add {r["component"].lower().replace(" ","-")}'
                elif "npm install" in install:
                    cmd = install
                else:
                    cmd = f"Copy from: {base_url}{r['component'].lower().replace(' ','-')}"
                print(f"\n  ★{'★'*r['wow']}{'☆'*(10-r['wow'])} [{r['lib']}] {r['component']}")
                print(f"  Category: {r['category']}  |  {r['desc']}")
                print(f"  Install:  {cmd}")
        else:
            print("  No components found. Try: 'background hero', 'button cta', 'card feature', 'text animation'")

    print()
