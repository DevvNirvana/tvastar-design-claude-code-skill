#!/usr/bin/env python3
"""
/color — Color Science & Psychology Engine v1.0
Phase 2.1 of the God-Level Roadmap

Makes every color choice defensible with psychology, WCAG math,
harmony algorithms, and industry-specific knowledge.

Usage:
  python3 color_science.py --industry fintech --style dark
  python3 color_science.py --check #6366F1 --bg #09090B
  python3 color_science.py --harmony #6366F1 --type complementary
  python3 color_science.py --palette "dark AI startup"
  python3 color_science.py --temperature warm
"""

import sys, math, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# ═══════════════════════════════════════════════════════════════════════
# COLOR PSYCHOLOGY DATABASE — industry × emotion × color mapping
# ═══════════════════════════════════════════════════════════════════════

COLOR_PSYCHOLOGY = {
    "trust":       {"colors": ["#0EA5E9","#1D4ED8","#0369A1"], "industries": ["finance","healthcare","b2b","enterprise","legal"],
                    "why": "Blue activates trust pathways. Nielsen Norman: blue links = highest click confidence."},
    "energy":      {"colors": ["#F97316","#EF4444","#DC2626"], "industries": ["fitness","food","gaming","sports","retail"],
                    "why": "Red/orange raises heart rate, creates urgency. Used by Netflix, YouTube, Coca-Cola."},
    "growth":      {"colors": ["#22C55E","#16A34A","#059669"], "industries": ["health","sustainability","fintech","productivity"],
                    "why": "Green = growth, money, go. Primary signal color in Western markets for success/profit."},
    "premium":     {"colors": ["#7C3AED","#6D28D9","#4C1D95"], "industries": ["ai","tech","saas","luxury","crypto"],
                    "why": "Violet = creativity + premium. Overused in AI (2023–25). Consider differentiating if in this space."},
    "luxury":      {"colors": ["#B45309","#D97706","#F59E0B"], "industries": ["luxury","fashion","beauty","jewelry","premium"],
                    "why": "Gold/amber signals exclusivity and wealth. Best on near-black backgrounds (Obsidian Gold palette)."},
    "calm":        {"colors": ["#0D9488","#14B8A6","#0891B2"], "industries": ["wellness","meditation","healthcare","education"],
                    "why": "Teal/cyan creates calm, reduces anxiety. Used by mental health apps, healthcare portals."},
    "bold":        {"colors": ["#EC4899","#DB2777","#BE185D"], "industries": ["beauty","consumer","social","entertainment"],
                    "why": "Pink/magenta = bold, fun, unapologetic. Glossier, Barbie, anti-corporate brand tone."},
    "creative":    {"colors": ["#8B5CF6","#7C3AED","#A855F7"], "industries": ["creative","agency","portfolio","art","design"],
                    "why": "Violet-purple = imagination and creativity. Distinct from AI-violet when used with warm accents."},
    "neutral":     {"colors": ["#78716C","#57534E","#44403C"], "industries": ["editorial","blog","content","news","documentary"],
                    "why": "Warm neutrals let content breathe. Typography-forward designs need color restraint."},
    "innovation":  {"colors": ["#06B6D4","#0EA5E9","#38BDF8"], "industries": ["tech","startup","developer","open-source"],
                    "why": "Cyan-sky = innovation, clarity, digital-native. Supabase, Tailwind, Vercel all use this range."},
}

# Industry → best palette profile mapping
INDUSTRY_PROFILES = {
    "fintech":        {"vibe": "trust dark", "primary": "#1E40AF", "cta": "#3B82F6", "bg_dark": "#020617", "psychology": "trust"},
    "healthcare":     {"vibe": "clean trust", "primary": "#0369A1", "cta": "#0EA5E9", "bg_dark": "#0C1828", "psychology": "trust"},
    "ai":             {"vibe": "dark premium", "primary": "#6366F1", "cta": "#A78BFA", "bg_dark": "#09090B", "psychology": "premium",
                       "warning": "AI-violet is heavily saturated. Consider differentiating with warm accents or teal."},
    "saas":           {"vibe": "professional minimal", "primary": "#4F46E5", "cta": "#6366F1", "bg_dark": "#09090B", "psychology": "premium"},
    "ecommerce":      {"vibe": "warm energy", "primary": "#F97316", "cta": "#EF4444", "bg_dark": "#1A0A00", "psychology": "energy"},
    "fitness":        {"vibe": "bold energy", "primary": "#EF4444", "cta": "#F97316", "bg_dark": "#0A0000", "psychology": "energy"},
    "wellness":       {"vibe": "calm minimal", "primary": "#0D9488", "cta": "#14B8A6", "bg_dark": "#042F2E", "psychology": "calm"},
    "gaming":         {"vibe": "cyber dark", "primary": "#00FF88", "cta": "#FF006E", "bg_dark": "#050505", "psychology": "energy"},
    "luxury":         {"vibe": "dark gold", "primary": "#B45309", "cta": "#D97706", "bg_dark": "#0A0800", "psychology": "luxury"},
    "creative":       {"vibe": "bold creative", "primary": "#7C3AED", "cta": "#EC4899", "bg_dark": "#0D0010", "psychology": "creative"},
    "developer":      {"vibe": "dark neutral", "primary": "#6366F1", "cta": "#3B82F6", "bg_dark": "#09090B", "psychology": "innovation"},
    "startup":        {"vibe": "energetic modern", "primary": "#6366F1", "cta": "#F97316", "bg_dark": "#09090B", "psychology": "premium"},
    "education":      {"vibe": "calm professional", "primary": "#4F46E5", "cta": "#6366F1", "bg_dark": "#0C0C1A", "psychology": "trust"},
    "media":          {"vibe": "editorial bold", "primary": "#EF4444", "cta": "#F97316", "bg_dark": "#0A0000", "psychology": "energy"},
    "social":         {"vibe": "fun bold", "primary": "#EC4899", "cta": "#8B5CF6", "bg_dark": "#0D0018", "psychology": "bold"},
}

# Dark mode color science rules
DARK_MODE_RULES = [
    {"rule": "Never pure black",       "bad": "#000000", "good": "#09090B",
     "why": "Pure black creates harsh contrast and feels flat. Near-black (zinc-950) has subtle warmth."},
    {"rule": "Never pure white text",  "bad": "#FFFFFF", "good": "#FAFAFA",
     "why": "Pure white on dark causes eye strain over time. Off-white #FAFAFA or zinc-50 is easier."},
    {"rule": "Desaturate darks",       "note": "Reduce saturation 10-20% from light version",
     "why": "Fully saturated colors on dark bg are harsh. Slightly muted = more premium feel."},
    {"rule": "Flip shadows to glows",  "note": "Instead of drop-shadow use box-shadow: 0 0 20px primary/30",
     "why": "Dark backgrounds make traditional shadows invisible. Glows create depth instead."},
    {"rule": "Surface hierarchy",      "note": "3-4 surface levels: bg → surface → elevated → overlay",
     "why": "Define bg (#09090B) → surface (#18181B) → elevated (#27272A) → overlay (#3F3F46)"},
    {"rule": "Reduce border contrast", "note": "white/10 to white/20 range",
     "why": "Strong borders in dark mode are jarring. Subtle 10-20% opacity borders are professional."},
    {"rule": "Dim images",             "note": "brightness-90 class on img elements",
     "why": "Unmodified photos appear too bright on dark backgrounds. Slight dim improves integration."},
]

# ═══════════════════════════════════════════════════════════════════════
# COLOR MATH — WCAG contrast, harmony, temperature
# ═══════════════════════════════════════════════════════════════════════

def hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c*2 for c in hex_color)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def relative_luminance(rgb: tuple) -> float:
    """WCAG 2.1 relative luminance calculation."""
    def linearize(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = [linearize(c) for c in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(hex1: str, hex2: str) -> float:
    """Calculate WCAG contrast ratio between two hex colors."""
    l1 = relative_luminance(hex_to_rgb(hex1))
    l2 = relative_luminance(hex_to_rgb(hex2))
    lighter = max(l1, l2)
    darker  = min(l1, l2)
    return round((lighter + 0.05) / (darker + 0.05), 2)


def wcag_grade(ratio: float, large_text: bool = False) -> tuple:
    """Returns (AA_pass, AAA_pass, grade_label)."""
    threshold_aa  = 3.0 if large_text else 4.5
    threshold_aaa = 4.5 if large_text else 7.0
    aa  = ratio >= threshold_aa
    aaa = ratio >= threshold_aaa
    if aaa:   label = "AAA ✅"
    elif aa:  label = "AA ✅"
    else:     label = "FAIL ❌"
    return aa, aaa, label


def suggest_accessible_color(fg: str, bg: str, target_ratio: float = 4.5) -> str:
    """Lighten or darken fg until it meets target contrast with bg."""
    bg_lum = relative_luminance(hex_to_rgb(bg))
    r, g, b = hex_to_rgb(fg)

    # Try lightening
    for step in range(0, 256, 8):
        candidate = f"#{min(r+step,255):02X}{min(g+step,255):02X}{min(b+step,255):02X}"
        if contrast_ratio(candidate, bg) >= target_ratio:
            return candidate

    # Try darkening
    for step in range(0, 256, 8):
        candidate = f"#{max(r-step,0):02X}{max(g-step,0):02X}{max(b-step,0):02X}"
        if contrast_ratio(candidate, bg) >= target_ratio:
            return candidate

    return "#FFFFFF" if bg_lum < 0.5 else "#000000"


def rgb_to_hsl(rgb: tuple) -> tuple:
    r, g, b = [c / 255 for c in rgb]
    cmax = max(r, g, b); cmin = min(r, g, b)
    delta = cmax - cmin
    l = (cmax + cmin) / 2
    s = 0 if delta == 0 else delta / (1 - abs(2*l - 1))
    if delta == 0:   h = 0
    elif cmax == r:  h = 60 * (((g - b) / delta) % 6)
    elif cmax == g:  h = 60 * (((b - r) / delta) + 2)
    else:            h = 60 * (((r - g) / delta) + 4)
    return round(h), round(s * 100), round(l * 100)


def hsl_to_hex(h: float, s: float, l: float) -> str:
    s /= 100; l /= 100
    c = (1 - abs(2*l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c/2
    if   0   <= h < 60:  r,g,b = c,x,0
    elif 60  <= h < 120: r,g,b = x,c,0
    elif 120 <= h < 180: r,g,b = 0,c,x
    elif 180 <= h < 240: r,g,b = 0,x,c
    elif 240 <= h < 300: r,g,b = x,0,c
    else:                r,g,b = c,0,x
    return f"#{int((r+m)*255):02X}{int((g+m)*255):02X}{int((b+m)*255):02X}"


def color_temperature(hex_color: str) -> str:
    """Classify color as warm, cool, or neutral."""
    r, g, b = hex_to_rgb(hex_color)
    h, s, l = rgb_to_hsl((r, g, b))
    if s < 15:   return "neutral (achromatic)"
    if 0 <= h < 30 or h >= 330:   return "warm (red/orange)"
    if 30 <= h < 75:               return "warm (yellow/amber)"
    if 75 <= h < 150:              return "cool-warm (green)"
    if 150 <= h < 210:             return "cool (teal/cyan)"
    if 210 <= h < 270:             return "cool (blue)"
    if 270 <= h < 330:             return "cool-warm (violet/pink)"
    return "neutral"


def generate_harmony(hex_color: str, harmony_type: str) -> dict:
    """Generate a color harmony from a base color."""
    r, g, b = hex_to_rgb(hex_color)
    h, s, l = rgb_to_hsl((r, g, b))

    harmonies = {
        "complementary": {
            "description": "Opposite on color wheel. Maximum contrast. Use for CTA only.",
            "colors": [hex_color, hsl_to_hex((h + 180) % 360, s, l)],
            "use": "Primary + CTA button only. Never use both for large areas.",
        },
        "analogous": {
            "description": "Adjacent colors (±30°). Harmonious, natural. Best for primary + secondary.",
            "colors": [
                hsl_to_hex((h - 30) % 360, s, l),
                hex_color,
                hsl_to_hex((h + 30) % 360, s, l),
            ],
            "use": "Primary brand color + secondary tones. Safe, cohesive.",
        },
        "triadic": {
            "description": "Three equally spaced (120° apart). Vibrant but balanced.",
            "colors": [hex_color, hsl_to_hex((h+120)%360, s, l), hsl_to_hex((h+240)%360, s, l)],
            "use": "Hero accent + feature icons + CTA. One dominant, two supporting.",
        },
        "split-complementary": {
            "description": "Base + two colors adjacent to complement. Tension without harshness.",
            "colors": [hex_color, hsl_to_hex((h+150)%360, s, l), hsl_to_hex((h+210)%360, s, l)],
            "use": "Best for brands needing visual interest without full complementary clash.",
        },
        "monochromatic": {
            "description": "Same hue, varied lightness/saturation. Sophisticated, minimal.",
            "colors": [
                hsl_to_hex(h, s, max(l-30, 10)),
                hsl_to_hex(h, s, max(l-15, 10)),
                hex_color,
                hsl_to_hex(h, s, min(l+15, 90)),
                hsl_to_hex(h, s, min(l+30, 90)),
            ],
            "use": "Luxury, minimal, editorial. One hue done in many lightness levels.",
        },
        "tetradic": {
            "description": "Four colors (90° apart). Rich, complex. Hard to balance.",
            "colors": [hex_color, hsl_to_hex((h+90)%360, s, l),
                       hsl_to_hex((h+180)%360, s, l), hsl_to_hex((h+270)%360, s, l)],
            "use": "Only for illustration/graphic contexts. Too complex for product UI.",
        },
    }
    return harmonies.get(harmony_type, harmonies["analogous"])


def dark_mode_variants(hex_color: str) -> dict:
    """Generate dark mode appropriate variants of a color."""
    r, g, b = hex_to_rgb(hex_color)
    h, s, l = rgb_to_hsl((r, g, b))
    return {
        "original":        hex_color,
        "dark_bg":         hsl_to_hex(h, max(s-5, 0),  max(l-40, 5)),
        "dark_surface":    hsl_to_hex(h, max(s-5, 0),  max(l-30, 10)),
        "dark_elevated":   hsl_to_hex(h, max(s-5, 0),  max(l-20, 15)),
        "dark_text":       hsl_to_hex(h, max(s-20, 5), min(l+40, 92)),
        "dark_muted":      hsl_to_hex(h, max(s-25, 5), min(l+15, 65)),
        "dark_border":     hsl_to_hex(h, max(s-10, 5), max(l-25, 18)),
        "glow":            f"0 0 20px {hex_color}40",
    }


def full_color_audit(fg: str, bg: str) -> dict:
    """Complete WCAG audit of a foreground/background pair."""
    ratio = contrast_ratio(fg, bg)
    aa_normal,  aaa_normal,  grade_normal  = wcag_grade(ratio, large_text=False)
    aa_large,   aaa_large,   grade_large   = wcag_grade(ratio, large_text=True)
    aa_ui,      _,           grade_ui      = wcag_grade(ratio, large_text=True)  # 3:1 for UI

    temp_fg = color_temperature(fg)
    temp_bg = color_temperature(bg)

    suggestion = None if aa_normal else suggest_accessible_color(fg, bg)

    return {
        "fg": fg, "bg": bg,
        "ratio": ratio,
        "normal_text":  {"pass": aa_normal,  "grade": grade_normal,  "threshold": "4.5:1"},
        "large_text":   {"pass": aa_large,   "grade": grade_large,   "threshold": "3.0:1"},
        "ui_components":{"pass": aa_ui,      "grade": grade_ui,      "threshold": "3.0:1"},
        "temperature_fg": temp_fg,
        "temperature_bg": temp_bg,
        "accessible_suggestion": suggestion,
    }


# ═══════════════════════════════════════════════════════════════════════
# OUTPUT FORMATTERS
# ═══════════════════════════════════════════════════════════════════════

def print_audit(audit: dict):
    W = 58
    print(f"\n  ─── WCAG Contrast Audit ─────────────────────────────")
    print(f"  Foreground: {audit['fg']}")
    print(f"  Background: {audit['bg']}")
    print(f"  Ratio:      {audit['ratio']}:1\n")
    for check, data in [("Normal text (≥4.5:1)", audit["normal_text"]),
                        ("Large text  (≥3.0:1)", audit["large_text"]),
                        ("UI elements (≥3.0:1)", audit["ui_components"])]:
        icon = "✅" if data["pass"] else "❌"
        print(f"  {icon}  {check:<24} {data['grade']}")
    print(f"\n  Temp (fg): {audit['temperature_fg']}")
    print(f"  Temp (bg): {audit['temperature_bg']}")
    if audit.get("accessible_suggestion"):
        print(f"\n  ⚠️  Fails normal text. Accessible alternative: {audit['accessible_suggestion']}")
        print(f"     ({contrast_ratio(audit['accessible_suggestion'], audit['bg'])}:1 ratio)")


def print_harmony(base: str, harmony_type: str, harmony: dict):
    print(f"\n  ─── {harmony_type.title()} Harmony ──────────────────────────")
    print(f"  Base:   {base}")
    print(f"  Rule:   {harmony['description']}")
    print(f"  Use:    {harmony['use']}\n")
    for i, color in enumerate(harmony["colors"]):
        label = "BASE" if color == base else f"  {i+1} "
        print(f"  [{label}] {color}")
    print()


def print_industry_palette(industry: str):
    profile = INDUSTRY_PROFILES.get(industry.lower())
    if not profile:
        similar = [k for k in INDUSTRY_PROFILES if industry.lower() in k]
        print(f"\n  Unknown industry: {industry}")
        if similar:
            print(f"  Similar: {', '.join(similar)}")
        return

    psych = COLOR_PSYCHOLOGY.get(profile["psychology"], {})
    print(f"\n  ─── {industry.title()} Color Profile ─────────────────────────")
    print(f"  Vibe:       {profile['vibe']}")
    print(f"  Psychology: {profile['psychology'].upper()}")
    if psych:
        print(f"  Why:        {psych['why']}")
    print(f"\n  Recommended colors:")
    print(f"  Primary:    {profile['primary']}")
    print(f"  CTA:        {profile['cta']}")
    print(f"  Dark BG:    {profile['bg_dark']}")
    if "warning" in profile:
        print(f"\n  ⚠️  {profile['warning']}")

    # WCAG checks for the palette
    print(f"\n  WCAG on dark background:")
    for name, fg in [("Primary on bg", profile["primary"]), ("CTA on bg", profile["cta"])]:
        ratio = contrast_ratio(fg, profile["bg_dark"])
        _, _, grade = wcag_grade(ratio)
        print(f"  {name}: {ratio}:1  {grade}")


def print_dark_mode_variants(hex_color: str):
    variants = dark_mode_variants(hex_color)
    print(f"\n  ─── Dark Mode Variants for {hex_color} ───────────────")
    labels = {
        "original":      "Original color",
        "dark_bg":       "Background (darkest)",
        "dark_surface":  "Surface cards",
        "dark_elevated": "Elevated elements",
        "dark_text":     "Text on dark bg",
        "dark_muted":    "Muted text",
        "dark_border":   "Border color",
        "glow":          "Glow shadow",
    }
    for key, label in labels.items():
        val = variants[key]
        if key != "glow":
            ratio = contrast_ratio(val, variants["dark_bg"]) if key != "dark_bg" else "—"
            print(f"  {label:<22} {val}  (ratio on bg: {ratio})")
        else:
            print(f"  {label:<22} {val}")
    print()


def cmd_palette(query: str):
    """Search for palette by vibe/industry keywords."""
    sys.path.insert(0, str(Path(__file__).parent))
    from core import search_palettes
    results = search_palettes(query, 3)
    print(f"\n  ─── Palettes for '{query}' ──────────────────────────────")
    for p in results:
        print(f"\n  [{p['name']}]")
        print(f"  Primary:  {p['primary']}  Secondary: {p['secondary']}  CTA: {p['cta']}")
        print(f"  BG:       {p['bg']}")
        # WCAG check
        ratio = contrast_ratio(p['text'], p['bg'])
        _, _, grade = wcag_grade(ratio)
        print(f"  Contrast: text on bg = {ratio}:1  {grade}")


def main():
    parser = argparse.ArgumentParser(description="/color — Color Science & Psychology Engine")
    parser.add_argument("--check",      help="Check WCAG contrast: --check #FG --bg #BG")
    parser.add_argument("--bg",         help="Background color for contrast check")
    parser.add_argument("--harmony",    help="Generate color harmony from base hex")
    parser.add_argument("--type",  "-t",default="analogous",
                        choices=["complementary","analogous","triadic","split-complementary","monochromatic","tetradic"])
    parser.add_argument("--industry",   help="Get palette profile for an industry")
    parser.add_argument("--dark-variants", help="Show dark mode variants for a hex color")
    parser.add_argument("--palette",    help="Search for palette by keywords")
    parser.add_argument("--temperature",help="Describe color temperature: warm|cool|neutral")
    parser.add_argument("--psychology", action="store_true", help="Show full psychology database")
    args = parser.parse_args()

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║        /color — Color Science Engine                ║")
    print("╚══════════════════════════════════════════════════════╝")

    if args.check:
        bg = args.bg or "#FFFFFF"
        audit = full_color_audit(args.check, bg)
        print_audit(audit)

    elif args.harmony:
        harmony = generate_harmony(args.harmony, args.type)
        print_harmony(args.harmony, args.type, harmony)

    elif args.industry:
        print_industry_palette(args.industry)

    elif getattr(args, 'dark_variants', None):
        print_dark_mode_variants(args.dark_variants)

    elif args.palette:
        cmd_palette(args.palette)

    elif args.temperature:
        temp = color_temperature(args.temperature)
        print(f"\n  {args.temperature}: {temp}\n")

    elif args.psychology:
        print(f"\n  ─── Color Psychology Database ─────────────────────────")
        for emotion, data in COLOR_PSYCHOLOGY.items():
            print(f"\n  [{emotion.upper()}]")
            print(f"  Colors:     {', '.join(data['colors'])}")
            print(f"  Industries: {', '.join(data['industries'])}")
            print(f"  Why:        {data['why']}")
        print()

    else:
        # Default: show full summary
        print(f"\n  ─── Available Commands ──────────────────────────────")
        print(f"  --check #FG --bg #BG         WCAG contrast audit")
        print(f"  --harmony #HEX --type TYPE   Color harmony generator")
        print(f"  --industry [name]            Industry palette profile")
        print(f"  --dark-variants #HEX         Dark mode color variants")
        print(f"  --palette 'keywords'         Search palettes")
        print(f"  --psychology                 Full psychology database")
        print(f"\n  Industries: {', '.join(INDUSTRY_PROFILES.keys())}")
        print(f"\n  Harmony types: complementary, analogous, triadic,")
        print(f"                 split-complementary, monochromatic, tetradic\n")


if __name__ == "__main__":
    main()
