#!/usr/bin/env python3
"""
/typography — Typography Science Engine v1.0
Phase 3.1 of the God-Level Roadmap

Understands typography at the level of a type director.
Modular scales, readability science, pairing rules, font classification.

Usage:
  python3 typography_science.py --scale 16 --ratio golden
  python3 typography_science.py --pair "Outfit" --recommend
  python3 typography_science.py --product "SaaS" --style "minimal dark"
  python3 typography_science.py --check "Outfit" "Inter"
  python3 typography_science.py --readability --measure 65
"""

import sys, math, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# ═══════════════════════════════════════════════════════════════════════
# MODULAR SCALE RATIOS — from Bringhurst / The Elements of Typographic Style
# ═══════════════════════════════════════════════════════════════════════

SCALE_RATIOS = {
    "minor-second":     {"ratio": 1.067, "name": "Minor Second",    "use": "Dense UI, data tables, admin panels — tight but harmonious"},
    "major-second":     {"ratio": 1.125, "name": "Major Second",    "use": "Professional SaaS, dashboards — subtle hierarchy"},
    "minor-third":      {"ratio": 1.200, "name": "Minor Third",     "use": "Corporate, B2B, trustworthy — comfortable progression"},
    "major-third":      {"ratio": 1.250, "name": "Major Third",     "use": "General SaaS, marketing, balanced — most versatile choice"},
    "perfect-fourth":   {"ratio": 1.333, "name": "Perfect Fourth",  "use": "Modern SaaS, landing pages — clear distinct levels"},
    "augmented-fourth": {"ratio": 1.414, "name": "Augmented Fourth","use": "Editorial, blogs, content — dramatic section breaks"},
    "perfect-fifth":    {"ratio": 1.500, "name": "Perfect Fifth",   "use": "Bold brand, portfolio — very dramatic scale"},
    "golden":           {"ratio": 1.618, "name": "Golden Ratio",    "use": "Maximum drama, luxury, editorial, hero moments only"},
}

PRODUCT_SCALE_RECOMMENDATIONS = {
    "dashboard":  "minor-second",
    "data":       "minor-second",
    "admin":      "major-second",
    "saas":       "major-third",
    "landing":    "perfect-fourth",
    "marketing":  "perfect-fourth",
    "blog":       "augmented-fourth",
    "editorial":  "golden",
    "portfolio":  "golden",
    "luxury":     "golden",
    "minimal":    "major-third",
    "dark":       "perfect-fourth",
}

# ═══════════════════════════════════════════════════════════════════════
# FONT CLASSIFICATION DATABASE
# ═══════════════════════════════════════════════════════════════════════

FONT_DATABASE = {
    # Geometric Sans — modern, neutral, tech-forward
    "Outfit": {
        "category": "Geometric Sans", "x_height": "high",
        "weights": [400,600,700,800], "variable": True,
        "personality": "Modern, clean, slightly playful. The current gold standard for SaaS heading fonts.",
        "best_for": ["saas","startup","tech","landing","dashboard"],
        "avoid_for": ["luxury","editorial serif moments","legal"],
        "pair_with": ["Inter","DM Sans","Manrope","Space Grotesk"],
        "avoid_pairing": ["Space Grotesk","Bricolage Grotesque"],
        "performance": "Excellent — variable font, Google Fonts, 4 subset weights",
        "google_url": "Outfit:wght@400;600;700;800",
        "fontsource": "@fontsource/outfit",
    },
    "Plus Jakarta Sans": {
        "category": "Geometric Sans", "x_height": "medium-high",
        "weights": [400,500,600,700,800], "variable": True,
        "personality": "Premium geometric sans. Slightly more personality than Inter, less stylized than Space Grotesk.",
        "best_for": ["saas","fintech","startup","premium product"],
        "pair_with": ["DM Sans","Inter","Manrope"],
        "performance": "Good — variable font available",
        "google_url": "Plus+Jakarta+Sans:wght@400;500;600;700;800",
    },
    "Space Grotesk": {
        "category": "Geometric Grotesque", "x_height": "high",
        "weights": [400,500,700], "variable": True,
        "personality": "Geometric with angular quirks. Technical, editorial, developer-tool aesthetic.",
        "best_for": ["developer-tool","technical","dark","portfolio"],
        "avoid_for": ["corporate B2B","healthcare"],
        "pair_with": ["Space Mono","Inter","DM Sans"],
        "performance": "Good",
        "google_url": "Space+Grotesk:wght@400;500;700",
    },
    "Bricolage Grotesque": {
        "category": "Grotesque Display", "x_height": "high",
        "weights": [400,600,700,800], "variable": True,
        "personality": "Ink-trap grotesque with optical refinements. Distinctive, editorial, premium.",
        "best_for": ["editorial","bold-brand","portfolio","creative","statement-headline"],
        "avoid_for": ["dense body text","admin UI"],
        "pair_with": ["Instrument Sans","DM Sans","Inter"],
        "performance": "Good — variable font",
        "google_url": "Bricolage+Grotesque:wght@400;600;700;800",
    },
    # Humanist Sans — warm, readable, UI-optimal
    "Inter": {
        "category": "Humanist Sans", "x_height": "high",
        "weights": [400,500,600,700], "variable": True,
        "personality": "The UI font standard. Neutral, extremely readable, optimized for screens. Nearly invisible.",
        "best_for": ["body-text","dashboard","admin","any-product-body"],
        "avoid_for": ["headings-only (too neutral)"],
        "pair_with": ["Outfit","Plus Jakarta Sans","Fraunces","Manrope","Bricolage Grotesque"],
        "performance": "Best-in-class — variable, optimized pixel hinting",
        "google_url": "Inter:wght@400;500;600",
        "fontsource": "@fontsource/inter",
    },
    "DM Sans": {
        "category": "Humanist Sans", "x_height": "high",
        "weights": [400,500,700], "variable": True,
        "personality": "Friendly, approachable humanist. Warmer than Inter, less corporate.",
        "best_for": ["consumer-app","wellness","body-text","SaaS-body"],
        "pair_with": ["Plus Jakarta Sans","Outfit","Fraunces"],
        "performance": "Excellent",
        "google_url": "DM+Sans:wght@400;500;700",
        "fontsource": "@fontsource/dm-sans",
    },
    "Manrope": {
        "category": "Humanist Geometric", "x_height": "high",
        "weights": [400,500,600,700,800], "variable": True,
        "personality": "Professional, clean, slightly geometric. Excellent for B2B and enterprise.",
        "best_for": ["b2b","enterprise","corporate","professional"],
        "pair_with": ["Inter","DM Sans"],
        "performance": "Excellent",
        "google_url": "Manrope:wght@400;500;600;700;800",
    },
    # Display Serifs — luxury, editorial, drama
    "Fraunces": {
        "category": "Display Serif (Variable)", "x_height": "medium",
        "weights": [400,600,700,900], "variable": True,
        "personality": "Optical-size serif with softness axis. Expressive, literary, distinctive. Best at large sizes.",
        "best_for": ["editorial","luxury","portfolio","hero-headlines","fashion"],
        "avoid_for": ["body text","small sizes","UI labels"],
        "pair_with": ["DM Sans","Inter","Manrope"],
        "headline_size_min": "40px",
        "performance": "Good — variable with SOFT and WONK axes",
        "google_url": "Fraunces:ital,opsz,wght@0,9..144,100..900;1,9..144,100..900",
    },
    "Melodrama": {
        "category": "Display Serif", "x_height": "medium",
        "weights": [400,700], "variable": False,
        "personality": "High-contrast display serif. Dramatic, fashion-forward, statement-making.",
        "best_for": ["fashion","luxury","editorial","portfolio"],
        "pair_with": ["General Sans","DM Sans"],
        "performance": "Fontshare CDN — free",
        "import_note": "Fontshare: @import url('https://api.fontshare.com/v2/css?f[]=melodrama@400,700')",
    },
    # Monospace — code, technical, intentional
    "Space Mono": {
        "category": "Monospace", "x_height": "medium",
        "weights": [400,700], "variable": False,
        "personality": "Geometric mono with personality. Use intentionally for code or technical contexts.",
        "best_for": ["code-display","developer-tool","technical-accent"],
        "avoid_for": ["body text","UI labels","anything non-technical"],
        "pair_with": ["Space Grotesk"],
        "performance": "Good",
        "google_url": "Space+Mono:wght@400;700",
    },
    "Geist Mono": {
        "category": "Monospace", "x_height": "high",
        "weights": [400,500,700], "variable": False,
        "personality": "Vercel's mono font. Clean, modern, optimized for developer contexts.",
        "best_for": ["developer-tool","code","CLI","terminal"],
        "pair_with": ["Geist"],
        "performance": "npm install geist",
        "import_note": "npm: import { GeistMono } from 'geist/font/mono'",
    },
    # Fontshare fonts
    "Cabinet Grotesk": {
        "category": "Grotesque Display", "x_height": "high",
        "weights": [400,500,700,800], "variable": False,
        "personality": "Tall, confident grotesque. Premium feel, excellent for large headings.",
        "best_for": ["premium-brand","startup","bold-heading"],
        "pair_with": ["Satoshi","DM Sans"],
        "performance": "Fontshare CDN — free",
        "import_note": "Fontshare: @import url('https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@400,500,700,800')",
    },
    "Satoshi": {
        "category": "Geometric Sans", "x_height": "high",
        "weights": [400,500,700,900], "variable": False,
        "personality": "Clean, geometric, highly legible. Popular alternative to Inter for body text.",
        "best_for": ["body-text","product","saas"],
        "pair_with": ["Cabinet Grotesk","Bricolage Grotesque"],
        "performance": "Fontshare CDN — free",
        "import_note": "Fontshare: @import url('https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900')",
    },
    "Clash Display": {
        "category": "Geometric Display", "x_height": "high",
        "weights": [400,600,700], "variable": False,
        "personality": "Bold, confident geometric. Popular for neobrutalist and indie brand aesthetics.",
        "best_for": ["neobrutalism","bold-brand","indie","agency"],
        "pair_with": ["Switzer","Satoshi"],
        "performance": "Fontshare CDN — free",
        "import_note": "Fontshare: @import url('https://api.fontshare.com/v2/css?f[]=clash-display@400,600,700')",
    },
    "Syne": {
        "category": "Display Geometric", "x_height": "medium",
        "weights": [400,600,700,800], "variable": True,
        "personality": "Unique, expressive geometric. Angular terminals give strong personality.",
        "best_for": ["creative","agency","portfolio","unique-brand"],
        "avoid_for": ["conservative brands","healthcare","legal"],
        "pair_with": ["Nunito","DM Sans"],
        "performance": "Good — variable font on Google",
        "google_url": "Syne:wght@400;600;700;800",
    },
}

# ═══════════════════════════════════════════════════════════════════════
# READABILITY SCIENCE (Bringhurst + modern screen research)
# ═══════════════════════════════════════════════════════════════════════

READABILITY_RULES = {
    "measure": {
        "optimal_chars": (45, 75),
        "rule": "Optimal line length: 45–75 characters per line (Bringhurst, 'Elements of Typographic Style').",
        "css_tip": "max-width: 65ch on paragraph elements. Never full-width body text.",
        "too_short": "< 45 chars creates choppy reading rhythm, too many hyphenations.",
        "too_long":  "> 75 chars causes eye tracking errors at line return.",
    },
    "line_height": {
        "body":    {"range": (1.4, 1.6), "recommendation": "1.5 or 1.6 for body text"},
        "heading": {"range": (1.05, 1.2), "recommendation": "1.1–1.2 for large headings, 1.15–1.25 for h2/h3"},
        "rule": "Tighter line-height as font size increases. Looser for small body text.",
    },
    "letter_spacing": {
        "headings":   {"value": "-0.02em to -0.04em", "why": "Large sizes optically appear too loose. Tighten slightly."},
        "body":       {"value": "-0.01em to 0",        "why": "Neutral or barely negative for comfortable reading."},
        "all_caps":   {"value": "+0.08em to +0.12em",  "why": "ALL CAPS needs positive tracking to be legible."},
        "small_text": {"value": "+0.01em to +0.03em",  "why": "Very small text (11-12px) benefits from slight opening."},
    },
    "font_size": {
        "minimum_body": 16,
        "minimum_ui":   14,
        "minimum_label":12,
        "never_below":  11,
        "rule": "Body text must be ≥16px. UI labels ≥14px. Never below 11px for anything readable.",
    },
    "font_weight": {
        "heading_range":   (600, 800),
        "body_normal":     400,
        "body_emphasis":   500,
        "ui_label":        (500, 600),
        "rule": "Body at 400. UI labels at 500-600. Headings 600-800. Avoid 300 (too light) and 900 (too heavy for screen).",
    },
    "pairing_rules": [
        "RULE 1: Maximum 2 typefaces per design. Heading + Body. Never more.",
        "RULE 2: Contrast is the principle — Serif heading + Sans body, or Display + Neutral.",
        "RULE 3: Never pair two fonts of the same category (2 sans, 2 serifs, 2 display).",
        "RULE 4: Size IS contrast — if fonts look too similar, one should be 2-3× the other.",
        "RULE 5: Variable fonts allow weight-based contrast without a second typeface.",
        "RULE 6: Personality contrast — pairing a character font with a neutral body is always safe.",
        "RULE 7: Never use a display font for body text. It's called 'display' for a reason.",
    ],
}

# ═══════════════════════════════════════════════════════════════════════
# MODULAR SCALE CALCULATOR
# ═══════════════════════════════════════════════════════════════════════

def modular_scale(base_px: float, ratio: float, steps: int = 7) -> list:
    """Generate a modular type scale from base size and ratio."""
    scale = []
    for i in range(-2, steps + 1):
        size_px  = round(base_px * (ratio ** i), 2)
        size_rem = round(size_px / 16, 4)
        scale.append({
            "step": i,
            "px":   size_px,
            "rem":  size_rem,
        })
    return scale


def assign_scale_labels(scale: list) -> list:
    """Assign semantic labels to scale steps (body=0, h4=1, h3=2, etc.)."""
    labels = {-2: "caption", -1: "small", 0: "body", 1: "body-lg",
              2: "h4", 3: "h3", 4: "h2", 5: "h1", 6: "display", 7: "display-xl"}
    for step in scale:
        step["label"] = labels.get(step["step"], f"step-{step['step']}")
    return scale


# ═══════════════════════════════════════════════════════════════════════
# FONT PAIRING ENGINE
# ═══════════════════════════════════════════════════════════════════════

def check_pairing(font1: str, font2: str) -> dict:
    """Analyze a font pairing and give a quality score."""
    f1 = FONT_DATABASE.get(font1, {})
    f2 = FONT_DATABASE.get(font2, {})

    issues = []
    score  = 100
    notes  = []

    # Same category check
    if f1.get("category") and f2.get("category"):
        cat1 = f1["category"].split()[0]
        cat2 = f2["category"].split()[0]
        if cat1 == cat2 and "Display" not in f1.get("category",""):
            issues.append("⚠️  Same category — lacks visual contrast")
            score -= 25

    # Explicit avoid-pairing check
    if font2 in f1.get("avoid_pairing", []) or font1 in f2.get("avoid_pairing", []):
        issues.append("❌ These fonts are explicitly listed as incompatible")
        score -= 40

    # Good pairing check
    if font2 in f1.get("pair_with", []) or font1 in f2.get("pair_with", []):
        notes.append("✅ Recommended pairing combination")
        score = min(score + 10, 100)

    # Both display fonts
    if "Display" in f1.get("category","") and "Display" in f2.get("category",""):
        issues.append("❌ Never pair two display fonts — both compete for attention")
        score -= 50

    # One is mono
    if "Mono" in f1.get("category","") or "Mono" in f2.get("category",""):
        if not any("code" in str(f.get("best_for",[])) for f in [f1,f2]):
            issues.append("⚠️  Monospace pair — only works in developer/code contexts")
            score -= 15

    verdict = "Excellent" if score >= 85 else "Good" if score >= 70 else "Fair" if score >= 50 else "Poor"

    return {
        "font1": font1, "font2": font2,
        "score": max(score, 0), "verdict": verdict,
        "issues": issues, "notes": notes,
        "f1_data": f1, "f2_data": f2,
    }


def recommend_pairs(font: str, role: str = "heading") -> list:
    """Recommend body/heading pairs for a given font."""
    f = FONT_DATABASE.get(font)
    if not f:
        return []
    if role == "heading":
        return f.get("pair_with", [])[:4]
    else:
        # Find fonts that list this as a pair
        return [name for name, data in FONT_DATABASE.items()
                if font in data.get("pair_with", []) and name != font][:4]


def product_type_recommendation(product: str, style: str) -> dict:
    """Recommend a font pairing for a product type and style."""
    query = f"{product} {style}".lower()

    # Find best scale ratio
    best_scale = "major-third"
    for keyword, scale_key in PRODUCT_SCALE_RECOMMENDATIONS.items():
        if keyword in query:
            best_scale = scale_key
            break

    # Find best heading font
    heading_scores = {}
    for name, data in FONT_DATABASE.items():
        if "Mono" in data.get("category",""):
            continue
        score = 0
        for best in data.get("best_for", []):
            if best.replace("-"," ") in query:
                score += 10
        heading_scores[name] = score

    heading_font = max(heading_scores, key=heading_scores.get) if heading_scores else "Outfit"

    # Find best body font
    body_font = "Inter"  # default
    paired = recommend_pairs(heading_font, "heading")
    if paired:
        # Prefer humanist sans for body
        for pf in paired:
            if FONT_DATABASE.get(pf, {}).get("category","") in ["Humanist Sans","Humanist Geometric"]:
                body_font = pf
                break
        if body_font == "Inter" and paired:
            body_font = paired[0]

    scale_data = SCALE_RATIOS[best_scale]
    scale = assign_scale_labels(modular_scale(16, scale_data["ratio"]))

    return {
        "heading_font": heading_font,
        "body_font":    body_font,
        "scale_key":    best_scale,
        "scale_ratio":  scale_data["ratio"],
        "scale_name":   scale_data["name"],
        "scale_use":    scale_data["use"],
        "type_scale":   scale,
    }


# ═══════════════════════════════════════════════════════════════════════
# OUTPUT FORMATTERS
# ═══════════════════════════════════════════════════════════════════════

def print_scale(scale: list, heading: str, body: str):
    W = 60
    print(f"\n  ─── Type Scale ──────────────────────────────────────────")
    print(f"  Heading: {heading}  |  Body: {body}")
    print(f"\n  {'Label':<12} {'px':>6}  {'rem':>7}  CSS class")
    print(f"  {'─'*52}")
    class_map = {
        "caption":    "text-xs",
        "small":      "text-sm",
        "body":       "text-base",
        "body-lg":    "text-lg",
        "h4":         "text-xl",
        "h3":         "text-2xl",
        "h2":         "text-3xl / text-4xl",
        "h1":         "text-5xl / text-6xl",
        "display":    "text-7xl",
        "display-xl": "text-8xl / text-9xl",
    }
    for step in scale:
        css = class_map.get(step["label"], "")
        font_ref = "font-heading" if step["label"] not in ("caption","small","body","body-lg") else "font-body"
        print(f"  {step['label']:<12} {step['px']:>5}px  {step['rem']:>6}rem  {css}  {font_ref}")
    print()


def print_pairing(result: dict):
    print(f"\n  ─── Pairing Analysis ────────────────────────────────────")
    print(f"  {result['font1']} + {result['font2']}")
    print(f"  Score:   {result['score']}/100  ({result['verdict']})")
    for n in result["notes"]:   print(f"  {n}")
    for i in result["issues"]:  print(f"  {i}")

    f1 = result["f1_data"]
    f2 = result["f2_data"]
    if f1:
        print(f"\n  {result['font1']}: {f1.get('category','?')}  |  {f1.get('personality','')[:55]}")
    if f2:
        print(f"  {result['font2']}: {f2.get('category','?')}  |  {f2.get('personality','')[:55]}")
    print()


def print_font_info(font_name: str):
    f = FONT_DATABASE.get(font_name)
    if not f:
        print(f"\n  Font '{font_name}' not in database.")
        print(f"  Available: {', '.join(list(FONT_DATABASE.keys())[:8])}...")
        return
    print(f"\n  ─── {font_name} ─────────────────────────────────────────")
    print(f"  Category:    {f['category']}")
    print(f"  x-height:    {f['x_height']}")
    print(f"  Variable:    {'Yes' if f.get('variable') else 'No'}")
    print(f"  Weights:     {', '.join(str(w) for w in f.get('weights',[]))}")
    print(f"\n  Personality: {f.get('personality','')}")
    print(f"\n  Best for:    {', '.join(f.get('best_for',[]))}")
    if f.get("avoid_for"):
        print(f"  Avoid for:   {', '.join(f['avoid_for'])}")
    print(f"\n  Pair with:   {', '.join(f.get('pair_with',[]))}")
    print(f"  Performance: {f.get('performance','')}")
    if f.get("google_url"):
        print(f"  Google URL:  fonts.googleapis.com/css2?family={f['google_url']}&display=swap")
    if f.get("fontsource"):
        print(f"  Fontsource:  npm install {f['fontsource']}")
    if f.get("import_note"):
        print(f"  Import:      {f['import_note']}")
    print()


def print_readability_rules():
    print(f"\n  ─── Readability Science (Bringhurst + Screen Research) ─")
    print(f"\n  MEASURE (line length)")
    m = READABILITY_RULES["measure"]
    print(f"  Optimal: {m['optimal_chars'][0]}–{m['optimal_chars'][1]} characters per line")
    print(f"  CSS tip: {m['css_tip']}")
    print(f"  Too short: {m['too_short']}")
    print(f"  Too long:  {m['too_long']}")

    print(f"\n  LINE HEIGHT")
    lh = READABILITY_RULES["line_height"]
    print(f"  Body text:  {lh['body']['recommendation']}")
    print(f"  Headings:   {lh['heading']['recommendation']}")

    print(f"\n  LETTER SPACING")
    ls = READABILITY_RULES["letter_spacing"]
    for ctx, data in ls.items():
        print(f"  {ctx.replace('_',' ').title():<15} {data['value']:<25} — {data['why']}")

    print(f"\n  FONT SIZE MINIMUMS")
    fs = READABILITY_RULES["font_size"]
    print(f"  Body text: ≥{fs['minimum_body']}px  |  UI labels: ≥{fs['minimum_ui']}px  |  Tiny: ≥{fs['minimum_label']}px")

    print(f"\n  PAIRING RULES")
    for rule in READABILITY_RULES["pairing_rules"]:
        print(f"  {rule}")
    print()


def main():
    parser = argparse.ArgumentParser(description="/typography — Typography Science Engine")
    parser.add_argument("--scale",      type=float, help="Generate scale from base px (e.g. 16)")
    parser.add_argument("--ratio",  "-r",default="major-third",
                        choices=list(SCALE_RATIOS.keys()), help="Scale ratio name")
    parser.add_argument("--check",  "-c",nargs=2,   help="Check font pairing: --check FontA FontB")
    parser.add_argument("--font",       help="Get info about a specific font")
    parser.add_argument("--pair",       help="Get recommended pairs for a font")
    parser.add_argument("--product",    help="Get recommendations for a product type")
    parser.add_argument("--style",      default="modern", help="Product style keywords")
    parser.add_argument("--readability",action="store_true", help="Show readability science rules")
    parser.add_argument("--list",       action="store_true", help="List all fonts in database")
    args = parser.parse_args()

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║        /typography — Type Science Engine            ║")
    print("╚══════════════════════════════════════════════════════╝")

    if args.scale:
        ratio_data = SCALE_RATIOS[args.ratio]
        scale = assign_scale_labels(modular_scale(args.scale, ratio_data["ratio"]))
        print(f"\n  Scale: {ratio_data['name']} ({ratio_data['ratio']}×)")
        print(f"  Use:   {ratio_data['use']}")
        print_scale(scale, "Heading Font", "Body Font")

    elif args.check:
        result = check_pairing(args.check[0], args.check[1])
        print_pairing(result)

    elif args.font:
        print_font_info(args.font)

    elif args.pair:
        pairs = recommend_pairs(args.pair)
        print(f"\n  Recommended pairings for {args.pair}:")
        for p in pairs:
            print(f"  • {p}")
        print()

    elif args.product:
        rec = product_type_recommendation(args.product, args.style)
        print(f"\n  ─── Typography for '{args.product} — {args.style}' ─────────")
        print(f"  Heading: {rec['heading_font']}")
        print(f"  Body:    {rec['body_font']}")
        print(f"  Scale:   {rec['scale_name']} ({rec['scale_ratio']}×)  — {rec['scale_use']}")
        print_scale(rec["type_scale"], rec["heading_font"], rec["body_font"])
        # Check the pairing
        pair_result = check_pairing(rec["heading_font"], rec["body_font"])
        print_pairing(pair_result)

    elif args.readability:
        print_readability_rules()

    elif args.list:
        print(f"\n  Font Database ({len(FONT_DATABASE)} fonts):\n")
        cats = {}
        for name, data in FONT_DATABASE.items():
            cat = data.get("category","Other")
            cats.setdefault(cat, []).append(name)
        for cat, fonts in sorted(cats.items()):
            print(f"  [{cat}]")
            for f in fonts:
                var = " (variable)" if FONT_DATABASE[f].get("variable") else ""
                print(f"    {f}{var}")
        print()

    else:
        print(f"\n  ─── Commands ────────────────────────────────────────")
        print(f"  --scale 16 --ratio major-third     Generate type scale")
        print(f"  --check 'Outfit' 'Inter'            Analyze font pairing")
        print(f"  --font 'Fraunces'                   Font details")
        print(f"  --pair 'Outfit'                     Recommended pairs")
        print(f"  --product 'SaaS' --style 'dark'     Product recommendations")
        print(f"  --readability                        Readability science rules")
        print(f"  --list                               All fonts in database")
        print(f"\n  Scale ratios: {', '.join(SCALE_RATIOS.keys())}\n")


if __name__ == "__main__":
    main()
