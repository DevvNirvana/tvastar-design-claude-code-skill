#!/usr/bin/env python3
"""
/extract — Brand Extraction Engine v1.0
Phase 12.1 — God-Level Roadmap

User gives a URL → Claude reverse-engineers the brand into a full design system.
Extracts: dominant colors, fonts, spacing units, border-radius, shadows.
Outputs: design-system/MASTER.md + tokens.json

Usage:
  python3 brand_extractor.py --url https://linear.app
  python3 brand_extractor.py --url https://vercel.com --apply
  python3 brand_extractor.py --css /path/to/styles.css
  python3 brand_extractor.py --analyze  # analyze current project's CSS
"""

import sys, re, json, argparse
from pathlib import Path
from datetime import datetime
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent))

# ═══════════════════════════════════════════════════════════════════════
# CSS PARSER — extracts design tokens from raw CSS
# ═══════════════════════════════════════════════════════════════════════

def extract_colors(css: str) -> dict:
    """Extract most-used colors from CSS content."""
    # Find all hex colors
    hex_colors = re.findall(r'#([0-9A-Fa-f]{6})\b', css)
    hex_3digit = re.findall(r'#([0-9A-Fa-f]{3})\b', css)
    # Expand 3-digit hex
    hex_3_expanded = [c[0]*2 + c[1]*2 + c[2]*2 for c in hex_3digit]
    
    # Find rgb/rgba colors
    rgb_colors = re.findall(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', css)
    rgb_hex = [f"{int(r):02X}{int(g):02X}{int(b):02X}" for r,g,b in rgb_colors]
    
    # Find CSS custom properties (design token values)
    css_vars = {}
    for match in re.finditer(r'--(color|bg|background|text|primary|secondary|accent|brand)[^:]*:\s*(#[0-9A-Fa-f]{3,6}|rgb[^;]+)', css, re.IGNORECASE):
        name = match.group(1).lower()
        val  = match.group(2).strip()
        css_vars[name] = val

    # Count frequency
    all_colors = hex_colors + hex_3_expanded + rgb_hex
    counted = Counter(c.upper() for c in all_colors)
    
    # Filter out identical/trivial colors but keep darks (important for mode detection)
    filtered = {}
    dark_set  = {}
    for k, v in counted.items():
        val = int(k, 16)
        if val > 0xF5F5F5:  # too light (near-white noise)
            continue
        if val < 0x303030:  # near-black — track separately for dark mode
            if v >= 1:
                dark_set[k] = v
        elif v >= 2:  # mid-range colors need 2+ uses
            filtered[k] = v
    # Include top darks
    for k, v in sorted(dark_set.items(), key=lambda x: -x[1])[:3]:
        filtered[k] = v
    
    return {
        "all_counted": dict(sorted(filtered.items(), key=lambda x: -x[1])[:20]),
        "css_vars":    css_vars,
        "top_10":      [f"#{k}" for k, v in sorted(filtered.items(), key=lambda x: -x[1])[:10]],
    }


def extract_fonts(css: str) -> dict:
    """Extract font families from CSS."""
    # font-family declarations
    families = re.findall(r'font-family\s*:\s*([^;}{]+)', css, re.IGNORECASE)
    all_fonts = []
    for fam in families:
        # Split by comma, clean each
        for f in fam.split(','):
            cleaned = f.strip().strip("'\"").strip()
            if cleaned and cleaned not in ('inherit','initial','unset','sans-serif','serif','monospace','system-ui'):
                all_fonts.append(cleaned)
    
    counted = Counter(all_fonts)
    top = [f for f, _ in counted.most_common(5)]
    
    # Google Fonts imports
    gf_imports = re.findall(r'fonts\.googleapis\.com/css[^"\']+family=([^&"\']+)', css)
    
    # @font-face declarations
    face_fonts = re.findall(r"@font-face\s*\{[^}]*font-family\s*:\s*['\"]?([^;'\"]+)['\"]?", css, re.IGNORECASE)
    
    return {
        "top_families": top[:4],
        "google_fonts":  [gf.replace('+', ' ').split(':')[0] for gf in gf_imports[:3]],
        "custom_fonts":  list(set(face_fonts))[:3],
        "heading_guess": top[0] if top else "Inter",
        "body_guess":    top[1] if len(top) > 1 else "Inter",
    }


def extract_spacing(css: str) -> dict:
    """Extract spacing units — find the most common increment."""
    px_values = re.findall(r':\s*(\d+)px\b', css)
    counts = Counter(int(v) for v in px_values if 2 <= int(v) <= 128)
    
    # Find the base unit (most common small value that divides others)
    candidates = [4, 8, 6, 5, 10]
    base_unit = 8  # default
    for c in candidates:
        multiples = sum(1 for v in counts if v % c == 0 and v > 0)
        if multiples > len(counts) * 0.6:
            base_unit = c
            break
    
    return {
        "base_unit": base_unit,
        "common_values": [v for v, _ in counts.most_common(8)],
        "scale_guess": f"{base_unit}px grid — found {len(counts)} unique spacing values",
    }


def extract_radius(css: str) -> dict:
    """Extract border-radius values."""
    values = re.findall(r'border-radius\s*:\s*([\d.]+)(?:px|rem|em)', css, re.IGNORECASE)
    counted = Counter(float(v) for v in values)
    top = [int(v) if v == int(v) else v for v, _ in counted.most_common(5)]
    
    # Classify system
    if not top:
        return {"values": [], "system": "none detected"}
    
    max_r = max(top) if top else 0
    system = "fully rounded (pill style)" if max_r > 20 else \
             "medium radius (card style)" if max_r > 10 else \
             "subtle radius (professional)" if max_r > 4 else \
             "sharp / minimal radius"
    
    return {
        "values": [f"{v}px" for v in top[:5]],
        "max": f"{max_r}px",
        "system": system,
    }


def extract_shadows(css: str) -> dict:
    """Extract box-shadow patterns."""
    shadows = re.findall(r'box-shadow\s*:\s*([^;}{]+)', css, re.IGNORECASE)
    cleaned = [s.strip() for s in shadows if 'none' not in s.lower() and len(s.strip()) > 4]
    
    style = "flat (no shadows)" if not cleaned else \
            "glassmorphism (opacity-based)" if any('rgba' in s for s in cleaned) else \
            "traditional (opaque)"
    
    return {
        "samples": cleaned[:3],
        "count":   len(cleaned),
        "style":   style,
    }


def classify_design_style(colors: dict, fonts: dict, radius: dict) -> dict:
    """Classify the overall design style from extracted tokens."""
    top = colors.get("top_10", [])
    r   = radius.get("max", "0px")
    max_r = float(re.search(r"[\d.]+", r).group()) if r and re.search(r"[\d.]+", r) else 0
    
    # Dark mode: any near-black color (#000000-#303030) in top colors
    dark_colors = [c for c in top if c and len(c) == 7 and int(c[1:], 16) < 0x303030]
    # Also check css_vars for dark backgrounds
    css_vars = colors.get("css_vars", {})
    has_dark_var = any(
        len(str(v)) == 7 and str(v).startswith("#") and int(str(v)[1:], 16) < 0x303030
        for v in css_vars.values() if str(v).startswith("#")
    )
    mode = "dark" if (len(dark_colors) > 0 or has_dark_var) else "light"
    
    if max_r > 20:
        border_style = "pill / very rounded"
    elif max_r > 10:
        border_style = "rounded (modern SaaS)"
    elif max_r > 4:
        border_style = "subtle radius (professional)"
    else:
        border_style = "sharp / geometric"
    
    heading = fonts.get("heading_guess", "")
    category = "developer tool" if heading in ("Space Grotesk","Geist","Fira Code") else \
               "editorial/luxury" if heading in ("Fraunces","Playfair Display","Melodrama") else \
               "SaaS/startup" if heading in ("Outfit","Plus Jakarta Sans","Inter") else \
               "modern product"
    
    return {
        "mode":         mode,
        "border_style": border_style,
        "category":     category,
        "confidence":   "high" if len(top) >= 5 else "medium" if len(top) >= 3 else "low",
    }


def build_design_system_from_extract(
    colors: dict, fonts: dict, spacing: dict,
    radius: dict, shadows: dict, style: dict,
    source_url: str = ""
) -> dict:
    """Build a design system dict from extracted data."""
    top = colors.get("top_10", [])
    css_vars = colors.get("css_vars", {})
    
    # Smart color assignment — CSS vars take priority over frequency
    primary   = css_vars.get("primary") or css_vars.get("brand") or css_vars.get("color")
    # From top colors: skip near-black/near-white, use first mid-range color
    mid_colors = [c for c in top if 0x303030 < int(c[1:],16) < 0xF0F0F0]
    if not primary:
        primary = mid_colors[0] if mid_colors else "#6366F1"
    secondary = css_vars.get("secondary") or (mid_colors[1] if len(mid_colors)>1 else "#818CF8")
    cta       = css_vars.get("accent") or css_vars.get("cta") or (mid_colors[2] if len(mid_colors)>2 else primary)
    
    is_dark = style.get("mode") == "dark"
    bg      = "#09090B" if is_dark else "#FFFFFF"
    surface = "#18181B" if is_dark else "#F9FAFB"
    text    = "#FAFAFA" if is_dark else "#0F172A"
    muted   = "#71717A" if is_dark else "#64748B"
    border  = "#27272A" if is_dark else "#E5E7EB"
    
    # Override with detected values if available
    for c in top:
        lum = int(c[1:], 16)
        if is_dark and lum < 0x303030 and bg == "#09090B":
            bg = c
        elif not is_dark and lum > 0xF0F0F0 and bg == "#FFFFFF":
            bg = c
    
    return {
        "source": source_url,
        "extracted_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "style": style,
        "tokens": {
            "primary":      primary,
            "secondary":    secondary,
            "cta":          cta,
            "bg":           bg,
            "surface":      surface,
            "text":         text,
            "muted":        muted,
            "border":       border,
            "font_heading": fonts.get("heading_guess", "Inter"),
            "font_body":    fonts.get("body_guess", "Inter"),
            "base_spacing": spacing.get("base_unit", 8),
            "border_radius":radius.get("max", "8px"),
        },
        "all_colors_found": colors.get("top_10", []),
        "all_fonts_found":  fonts.get("top_families", []),
        "spacing_system":   spacing.get("scale_guess", "8px grid"),
        "shadow_style":     shadows.get("style", "unknown"),
        "gaps": [],  # filled in by save_master
    }


def detect_gaps(ds: dict) -> list:
    """Find what couldn't be detected and needs manual input."""
    gaps = []
    t = ds.get("tokens", {})
    
    if not ds.get("all_colors_found"):
        gaps.append("No colors extracted — CSS may be in modules or inline styles")
    if t.get("font_heading") == t.get("font_body") == "Inter":
        gaps.append("Font detection uncertain — verify heading/body font pairing")
    if t.get("border_radius") == "8px":
        gaps.append("Border radius defaulted — check actual values in dev tools")
    if ds.get("shadow_style") == "unknown":
        gaps.append("Shadow style unknown — inspect card/dropdown shadows manually")
    if ds.get("style",{}).get("confidence") == "low":
        gaps.append("Low confidence extraction — CSS sample may be incomplete")
    
    return gaps


def save_extracted_system(ds: dict, root: Path):
    """Save extracted design system to MASTER.md and tokens.json."""
    ds_dir = root / "design-system"
    ds_dir.mkdir(exist_ok=True)
    
    t = ds["tokens"]
    source = ds.get("source","")
    style  = ds.get("style",{})
    gaps   = detect_gaps(ds)
    
    # Save tokens.json
    tokens_data = {
        "color": {
            "primary":   {"$value": t["primary"],   "$type": "color"},
            "secondary": {"$value": t["secondary"], "$type": "color"},
            "cta":       {"$value": t["cta"],       "$type": "color"},
            "bg":        {"$value": t["bg"],        "$type": "color"},
            "surface":   {"$value": t["surface"],   "$type": "color"},
            "text":      {"$value": t["text"],      "$type": "color"},
            "muted":     {"$value": t["muted"],     "$type": "color"},
            "border":    {"$value": t["border"],    "$type": "color"},
        },
        "typography": {
            "fontFamily": {
                "heading": {"$value": t["font_heading"], "$type": "fontFamily"},
                "body":    {"$value": t["font_body"],    "$type": "fontFamily"},
            }
        }
    }
    (ds_dir / "tokens.json").write_text(json.dumps(tokens_data, indent=2))
    
    # Build MASTER.md content
    gap_section = ""
    if gaps:
        gap_section = "\n## Extraction Gaps (needs manual verification)\n"
        for g in gaps:
            gap_section += f"- ⚠️  {g}\n"
    
    colors_found = "\n".join(f"  {c}" for c in ds.get("all_colors_found",[]))
    fonts_found  = ", ".join(ds.get("all_fonts_found",[]))
    
    master_content = f"""# Extracted Design System
Source: {source or 'CSS file / project'}
Extracted: {ds['extracted_at']}
Mode: {style.get('mode','unknown')} | Style: {style.get('border_style','?')} | Confidence: {style.get('confidence','?')}

> Generated by /extract — verify all values against the actual site in DevTools.

---

## Design Tokens

:root {{
  --color-primary:   {t['primary']};
  --color-secondary: {t['secondary']};
  --color-cta:       {t['cta']};
  --color-bg:        {t['bg']};
  --color-surface:   {t['surface']};
  --color-text:      {t['text']};
  --color-muted:     {t['muted']};
  --color-border:    {t['border']};
  --font-heading:    '{t['font_heading']}', sans-serif;
  --font-body:       '{t['font_body']}', sans-serif;
}}

## Extracted Data

Colors found (by frequency):
{colors_found}

Fonts found: {fonts_found}
Spacing system: {ds.get('spacing_system','?')}
Shadow style: {ds.get('shadow_style','?')}
Border radius: {t.get('border_radius','?')}
{gap_section}
---

## Next Steps

1. Verify colors in browser DevTools (Inspect → Computed → color)
2. Check font names in DevTools (Computed → font-family)
3. Run /design to generate a full design system matching this brand
4. Run /preview to see the extracted system rendered
"""
    (ds_dir / "MASTER.md").write_text(master_content)
    return gaps


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def process_css(css_content: str, source: str = "") -> dict:
    """Process CSS content and return full extraction result."""
    colors  = extract_colors(css_content)
    fonts   = extract_fonts(css_content)
    spacing = extract_spacing(css_content)
    radius  = extract_radius(css_content)
    shadows = extract_shadows(css_content)
    style   = classify_design_style(colors, fonts, radius)
    
    return build_design_system_from_extract(
        colors, fonts, spacing, radius, shadows, style, source
    )


def print_extraction_result(ds: dict):
    """Print a formatted extraction summary."""
    t     = ds["tokens"]
    style = ds.get("style", {})
    gaps  = detect_gaps(ds)
    
    print(f"\n  ─── Extraction Results ──────────────────────────────")
    print(f"  Source:    {ds.get('source','CSS file')}")
    print(f"  Mode:      {style.get('mode','?')} | {style.get('border_style','?')}")
    print(f"  Category:  {style.get('category','?')} | Confidence: {style.get('confidence','?')}")
    
    print(f"\n  Extracted tokens:")
    print(f"  Primary:    {t['primary']}")
    print(f"  Secondary:  {t['secondary']}")
    print(f"  CTA/Accent: {t['cta']}")
    print(f"  BG:         {t['bg']}")
    print(f"  Heading:    {t['font_heading']}")
    print(f"  Body:       {t['font_body']}")
    print(f"  Radius:     {t['border_radius']}")
    print(f"  Spacing:    {t['base_spacing']}px base unit")
    
    if ds.get("all_colors_found"):
        print(f"\n  All colors found ({len(ds['all_colors_found'])}):")
        for c in ds["all_colors_found"][:8]:
            print(f"    {c}")
    
    if gaps:
        print(f"\n  ⚠️  Gaps ({len(gaps)}) — verify manually:")
        for g in gaps:
            print(f"    {g}")
    
    print()


def main():
    parser = argparse.ArgumentParser(description="/extract — Brand Extraction Engine")
    parser.add_argument("--url",     help="URL to extract from (requires Claude's web_fetch)")
    parser.add_argument("--css",     help="Local CSS file to extract from")
    parser.add_argument("--analyze", action="store_true", help="Analyze current project's CSS")
    parser.add_argument("--apply",   action="store_true", help="Save to design-system/ directory")
    parser.add_argument("--raw",     help="Raw CSS string to analyze")
    args = parser.parse_args()

    root = Path.cwd()

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║        /extract — Brand Extraction Engine           ║")
    print("╚══════════════════════════════════════════════════════╝\n")

    css_content = ""
    source      = ""

    if args.url:
        print(f"  Extracting from: {args.url}")
        print(f"  ℹ  Note: This requires Claude's web_fetch tool to fetch the URL.")
        print(f"  ℹ  In Claude Code, type: /extract --url {args.url}")
        print(f"     Claude will fetch the page, extract all stylesheets, and run this tool.")
        print(f"\n  Simulating extraction with placeholder — paste CSS manually:")
        print(f"  python3 brand_extractor.py --css /path/to/downloaded-styles.css\n")
        return

    elif args.css:
        css_path = Path(args.css)
        if not css_path.exists():
            print(f"  ⚠  CSS file not found: {args.css}\n")
            return
        css_content = css_path.read_text(errors="ignore")
        source      = str(css_path)
        print(f"  Reading CSS: {args.css} ({len(css_content):,} chars)")

    elif args.raw:
        css_content = args.raw
        source      = "raw CSS input"

    elif args.analyze:
        # Find all CSS in current project
        css_files = []
        for pattern in ["*.css", "*.scss", "*.sass"]:
            for f in root.rglob(pattern):
                if "node_modules" not in str(f) and ".next" not in str(f):
                    css_files.append(f)
        
        if not css_files:
            print("  ⚠  No CSS files found in project.\n")
            return
        
        css_content = "\n".join(f.read_text(errors="ignore") for f in css_files[:5])
        source      = f"{root.name} project ({len(css_files)} CSS files)"
        print(f"  Analyzing {len(css_files)} CSS files in {root.name}")

    else:
        print("  Usage:")
        print("  python3 brand_extractor.py --url https://linear.app")
        print("  python3 brand_extractor.py --css styles.css")
        print("  python3 brand_extractor.py --analyze  (current project)")
        print("  python3 brand_extractor.py --raw ':root { --color-primary: #6366F1; }'")
        print()
        print("  In Claude Code, /extract will automatically fetch the URL and")
        print("  pass the CSS through this extractor.\n")
        return

    if not css_content:
        print("  ⚠  No CSS content to analyze.\n")
        return

    ds   = process_css(css_content, source)
    gaps = detect_gaps(ds)
    print_extraction_result(ds)

    if args.apply:
        saved_gaps = save_extracted_system(ds, root)
        print(f"  ✅ Saved to design-system/MASTER.md")
        print(f"  ✅ Saved to design-system/tokens.json")
        if saved_gaps:
            print(f"  ⚠️  {len(saved_gaps)} gaps noted in MASTER.md — verify manually")
        print(f"\n  Next: run /preview to see the extracted design rendered\n")
    else:
        print(f"  Add --apply to save to design-system/\n")


if __name__ == "__main__":
    main()
