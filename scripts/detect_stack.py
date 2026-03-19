#!/usr/bin/env python3
"""
Stack Detector v2.0 — detects framework + ALL UI libraries including
React Bits, Aceternity, Magic UI, Origin UI, NextUI, Chakra, DaisyUI,
Flowbite, Headless UI, Radix UI, Stunning UI, Kibo UI, Skiper UI.
Run from project root: python3 detect_stack.py
"""
import json, os, re, sys
from pathlib import Path

def detect():
    root = Path.cwd()
    r = {
        "framework":"unknown","platform":"web","router":None,"language":"javascript",
        # CSS / utility
        "tailwind":False,"tailwind_version":None,
        # Foundation libs
        "has_shadcn":False,"has_radix":False,"has_headlessui":False,
        # Animation
        "has_framer":False,"has_gsap":False,"has_react_spring":False,"has_three":False,
        # Statement libs
        "has_react_bits":False,"has_aceternity":False,"has_magicui":False,
        # Component libs
        "has_nextui":False,"has_chakra":False,"has_daisy":False,
        "has_flowbite":False,"has_mantine":False,"has_mui":False,
        "has_nextui":False,"has_chakra":False,
        # Vue-specific
        "has_pinia":False,"has_vuex":False,"has_nuxt":False,"has_sveltekit":False,
        "has_stunningui":False,
        # Advanced
        "has_kiboui":False,"has_originui":False,
        # Meta
        "components":[],"src_dir":None,"globals_css":None,
        "has_design_tokens":False,"existing_colors":[],"guidelines":[],
    }

    # ── Flutter ───────────────────────────────────────────────────────
    if (root / "pubspec.yaml").exists():
        content = (root / "pubspec.yaml").read_text(errors="ignore")
        r.update({"framework":"flutter","platform":"cross-platform","language":"dart","guidelines":["flutter"]})
        for pkg in ["flutter_riverpod","riverpod","go_router","get_it","bloc","mobx"]:
            if pkg in content: r["components"].append(pkg)
        _print_results(r); return r

    # ── SwiftUI ───────────────────────────────────────────────────────
    if list(root.glob("*.xcodeproj")) or list(root.glob("*.xcworkspace")) or list(root.rglob("*.swift"))[:1]:
        r.update({"framework":"swiftui","platform":"ios","language":"swift","guidelines":["swiftui"]})
        _print_results(r); return r

    # ── package.json ──────────────────────────────────────────────────
    pkg_path = root / "package.json"
    if not pkg_path.exists():
        if list(root.rglob("*.vue"))[:1]: r.update({"framework":"vue","guidelines":["vue","tailwind"]})
        elif list(root.rglob("*.svelte"))[:1]: r.update({"framework":"svelte","guidelines":["svelte","tailwind"]})
        else: print("⚠  No package.json found.\nSTACK_UNKNOWN"); sys.exit(0)
        _print_results(r); return r

    with open(pkg_path) as f: pkg = json.load(f)
    deps = {**pkg.get("dependencies",{}), **pkg.get("devDependencies",{})}
    dep_str = json.dumps(deps).lower()

    # ── Framework ────────────────────────────────────────────────────
    if "next" in deps:
        app_dirs = [root/"app", root/"src"/"app"]
        r.update({"framework":"nextjs","router":"app-router" if any(d.exists() for d in app_dirs) else "pages-router","guidelines":["nextjs","react","tailwind"]})
    elif any(k in deps for k in ["nuxt","@nuxt/core"]):
        r.update({"framework":"nuxt","has_nuxt":True,"guidelines":["vue","tailwind"]})
    elif "vue" in deps:
        r.update({"framework":"vue","guidelines":["vue","tailwind"]})
    elif "@sveltejs/kit" in deps:
        r.update({"framework":"sveltekit","has_sveltekit":True,"guidelines":["svelte","tailwind"]})
    elif "svelte" in deps:
        r.update({"framework":"svelte","guidelines":["svelte","tailwind"]})
    elif "vite" in deps:
        r.update({"framework":"vite-react","guidelines":["react","tailwind"]})
    elif "gatsby" in deps:
        r.update({"framework":"gatsby","guidelines":["react","tailwind"]})
    elif "react" in deps:
        r.update({"framework":"react-cra","guidelines":["react","tailwind"]})

    # ── Language ─────────────────────────────────────────────────────
    if "typescript" in deps or (root/"tsconfig.json").exists(): r["language"] = "typescript"

    # ── Tailwind ─────────────────────────────────────────────────────
    if "tailwindcss" in deps:
        ver = deps.get("tailwindcss","").lstrip("^~>=")
        r.update({"tailwind":True,"tailwind_version":ver[0] if ver else "3"})
        if "tailwind" not in r["guidelines"]: r["guidelines"].append("tailwind")

    # ── shadcn ───────────────────────────────────────────────────────
    if (root/"components.json").exists():
        r.update({"has_shadcn":True})
        r["components"].append("shadcn/ui")
        if "shadcn" not in r["guidelines"]: r["guidelines"].append("shadcn")

    # ── Animation libs ───────────────────────────────────────────────
    if "framer-motion" in deps or "motion" in deps: r["has_framer"] = True
    if "gsap" in deps: r["has_gsap"] = True
    if "@react-spring/web" in deps or "react-spring" in deps: r["has_react_spring"] = True
    if "three" in deps: r["has_three"] = True

    # ── Statement component libs ─────────────────────────────────────
    # React Bits — detect by checking src dir for aurora/spotlightcard imports
    src_dirs_to_check = ["src","app","components","lib"]
    rb_indicators = ["reactbits","aurora","spotlightcard","splittext","blurtext","magneticbutton"]
    ac_indicators = ["aceternity","aurorabackground","sparklescore","heroparallax","movingborder"]
    mu_indicators = ["magicui","shimmerbutton","rainbowbutton","borderbeam","numberticker","magiccard"]
    ou_indicators = ["originui"]
    sk_indicators = ["skiper"]
    kb_indicators = ["kiboui","kibo"]

    def _scan_imports(indicators):
        for sd in src_dirs_to_check:
            sp = root / sd
            if not sp.exists(): continue
            for ext in [".tsx",".ts",".jsx",".js",".svelte",".vue"]:
                for f in list(sp.rglob(f"*{ext}"))[:30]:  # limit for speed
                    try:
                        ct = f.read_text(errors="ignore").lower()
                        if any(ind in ct for ind in indicators): return True
                    except: pass
        return False

    r["has_react_bits"] = _scan_imports(rb_indicators)
    r["has_aceternity"] = _scan_imports(ac_indicators)
    r["has_magicui"] = _scan_imports(mu_indicators)

    # ── Component framework detection ────────────────────────────────
    if any(k.startswith("@nextui-org") or k.startswith("@heroui") for k in deps):
        r["has_nextui"] = True; r["components"].append("nextui")
    if any(k.startswith("@chakra-ui") for k in deps):
        r["has_chakra"] = True; r["components"].append("chakra-ui")
    if "daisyui" in deps:
        r["has_daisy"] = True; r["components"].append("daisyui")
    if "flowbite" in deps or "flowbite-react" in deps:
        r["has_flowbite"] = True; r["components"].append("flowbite")
    if any(k.startswith("@mantine") for k in deps):
        r["has_mantine"] = True; r["components"].append("mantine")
    if any(k.startswith("@mui") or k.startswith("@material-ui") for k in deps):
        r["has_mui"] = True; r["components"].append("material-ui")
    if any(k.startswith("@headlessui") for k in deps):
        r["has_headlessui"] = True; r["components"].append("headlessui")
    if any(k.startswith("@radix-ui") for k in deps):
        r["has_radix"] = True
        if "radix-ui" not in r["components"]: r["components"].append("radix-ui")
    if "pinia" in deps: r["has_pinia"] = True; r["components"].append("pinia")
    if "vuex" in deps: r["has_vuex"] = True; r["components"].append("vuex")
    if "vue-router" in deps: r["components"].append("vue-router")

    # ── Vue-specific statement libs
    r["has_stunningui"] = _scan_imports(["stunning-ui","stunningui"])
    r["has_kiboui"] = _scan_imports(kb_indicators) or "kiboui" in dep_str
    r["has_originui"] = _scan_imports(ou_indicators)

    # ── CSS + tokens ─────────────────────────────────────────────────
    for d in ["src","app","pages","components"]:
        if (root/d).exists(): r["src_dir"] = d; break

    css_paths = [root/"src"/"app"/"globals.css", root/"app"/"globals.css",
                 root/"src"/"styles"/"globals.css", root/"src"/"index.css",
                 root/"src"/"style.css", root/"styles"/"globals.css"]
    for g in css_paths:
        if g.exists():
            r["globals_css"] = str(g.relative_to(root))
            ct = g.read_text(errors="ignore")
            if "--color" in ct or "--primary" in ct: r["has_design_tokens"] = True
            r["existing_colors"] = list(set(re.findall(r'#[0-9A-Fa-f]{6}',ct)))[:5]
            break

    if (root/"design-system").exists(): r["has_design_tokens"] = True

    _print_results(r)
    return r


def _print_results(r):
    fw = r["framework"]
    router = f" ({r['router']})" if r.get("router") else ""
    platform = f" [{r['platform']}]" if r.get("platform","web") != "web" else ""
    W = 54

    print(f"\n╔{'═'*W}╗")
    print(f"║{'CODEBASE STACK ANALYSIS v2.0'.center(W)}║")
    print(f"╚{'═'*W}╝\n")
    print(f"  Framework:     {fw}{router}{platform}")
    print(f"  Language:      {r['language']}")

    if fw not in ("flutter","swiftui"):
        tw = f"✓ v{r['tailwind_version']}" if r["tailwind"] else "✗ not found"
        print(f"  Tailwind:      {tw}")
        print(f"\n  ── Foundation ──────────────────────────────────────")
        print(f"  shadcn/ui:     {'✓' if r['has_shadcn'] else '✗  → npx shadcn@latest init'}")
        print(f"  Radix UI:      {'✓' if r['has_radix'] else '✗'}")
        print(f"  Headless UI:   {'✓' if r['has_headlessui'] else '✗'}")

        print(f"\n  ── Animation ───────────────────────────────────────")
        print(f"  Framer Motion: {'✓' if r['has_framer'] else '✗  → npm i framer-motion'}")
        print(f"  GSAP:          {'✓' if r['has_gsap'] else '✗'}")
        print(f"  React Spring:  {'✓' if r['has_react_spring'] else '✗'}")
        print(f"  Three.js:      {'✓' if r['has_three'] else '✗'}")

        print(f"\n  ── Statement Libraries (visual wow) ────────────────")
        print(f"  React Bits:    {'✓ detected' if r['has_react_bits'] else '✗  → npx shadcn@latest add [url]'}")
        print(f"  Aceternity UI: {'✓ detected' if r['has_aceternity'] else '✗  → copy from ui.aceternity.com'}")
        print(f"  Magic UI:      {'✓ detected' if r['has_magicui'] else '✗  → npx magicui-cli@latest add [c]'}")

        print(f"\n  ── Component Frameworks ────────────────────────────")
        print(f"  NextUI:        {'✓' if r.get('has_nextui') else '✗'}")
        print(f"  Chakra UI:     {'✓' if r.get('has_chakra') else '✗'}")
        print(f"  DaisyUI:       {'✓' if r.get('has_daisy') else '✗'}")
        print(f"  Flowbite:      {'✓' if r.get('has_flowbite') else '✗'}")
        print(f"  MUI:           {'✓' if r.get('has_mui') else '✗'}")
        print(f"  Mantine:       {'✓' if r.get('has_mantine') else '✗'}")

        print(f"\n  ── Enhanced Components ─────────────────────────────")
        print(f"  Kibo UI:       {'✓' if r.get('has_kiboui') else '✗  → npx kiui@latest add [c]'}")
        print(f"  Origin UI:     {'✓' if r.get('has_originui') else '✗  → copy from originui.com'}")

    if fw in ("vue","nuxt"):
        print(f"\n  ── Vue State ───────────────────────────────────────")
        print(f"  Pinia:         {'✓' if r['has_pinia'] else '✗  → npm install pinia'}")
        print(f"  Vuex:          {'✓' if r['has_vuex'] else '✗'}")
        print(f"  Stunning UI:   {'✓' if r.get('has_stunningui') else '✗  → copy from stunning-ui.com'}")

    if fw not in ("flutter","swiftui"):
        print(f"\n  ── Project ─────────────────────────────────────────")
        print(f"  Source dir:    {r.get('src_dir') or 'root'}")
        print(f"  globals.css:   {r.get('globals_css') or 'not found'}")
        print(f"  Design tokens: {'✓ found' if r['has_design_tokens'] else '✗ will create'}")
        if r.get("existing_colors"):
            print(f"  Existing hex:  {', '.join(r['existing_colors'][:3])}")
        if r["components"]:
            print(f"  Other libs:    {', '.join(r['components'])}")
        print(f"\n  Active guidelines: {', '.join(r['guidelines'])}")

    # Recommendations
    recs = []
    if fw in ("nextjs","vite-react","react-cra"):
        if not r["has_framer"]: recs.append("npm install framer-motion  # required for Aceternity + Magic UI")
        if not r["has_shadcn"]: recs.append("npx shadcn@latest init  # foundation for React Bits + Kibo UI")
        if r.get("tailwind_version") == "4":
            recs.append("⚠  Tailwind v4: use @theme{} in CSS, bg-linear-to-r not bg-gradient-to-r")
        if not r["has_react_bits"] and not r["has_aceternity"] and not r["has_magicui"]:
            recs.append("No statement lib detected — add React Bits, Magic UI, or Aceternity for wow factor")
    if fw in ("vue","nuxt") and not r["has_pinia"]:
        recs.append("npm install pinia  # recommended state management")
    if fw == "flutter" and "riverpod" not in r.get("components",[]):
        recs.append("flutter pub add flutter_riverpod")

    if recs:
        print(f"\n  RECOMMENDATIONS:")
        for rec in recs: print(f"  → {rec}")

    print()
    print("STACK_JSON:" + json.dumps(r))


if __name__ == "__main__":
    detect()
