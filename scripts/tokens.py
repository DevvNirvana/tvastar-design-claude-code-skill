#!/usr/bin/env python3
"""
/tokens — W3C Design Token Generator v1.0 (Phase 7.1)
Generates tokens.json (W3C spec), tokens.css, tokens.ts, tokens.tailwind.ts
Usage:
  python3 tokens.py                        # generate all formats
  python3 tokens.py --format w3c           # W3C only
  python3 tokens.py --format css|ts|figma|tailwind
"""
import sys, json, argparse
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).parent))

def load_tokens(root: Path) -> dict:
    master = root / "design-system" / "MASTER.md"
    t = {}
    if master.exists():
        for line in master.read_text(errors="ignore").splitlines():
            line = line.strip()
            for css, key in [("--color-primary:","primary"),("--color-secondary:","secondary"),
                              ("--color-cta:","cta"),("--color-bg:","bg"),("--color-surface:","surface"),
                              ("--color-text:","text"),("--color-muted:","muted"),("--color-border:","border")]:
                if line.startswith(css): t[key] = line.split(":",1)[1].strip().rstrip(";")
            if line.startswith("--font-heading:"):
                t["font_heading"] = line.split(":",1)[1].strip().rstrip(";").split(",")[0].strip().strip("'\"")
            if line.startswith("--font-body:"):
                t["font_body"] = line.split(":",1)[1].strip().rstrip(";").split(",")[0].strip().strip("'\"")
    if not t:
        t = {"primary":"#6366F1","secondary":"#818CF8","cta":"#A78BFA","bg":"#09090B","surface":"#18181B",
             "text":"#FAFAFA","muted":"#71717A","border":"#27272A","font_heading":"Outfit","font_body":"Inter"}
    return t

def gen_w3c(t: dict) -> str:
    ts = datetime.now().strftime("%Y-%m-%d")
    data = {
        "$metadata": {"tokenSetOrder": ["color","typography","spacing","radius","shadow","animation"]},
        "color": {
            "primary":   {"$value": t.get("primary","#6366F1"),   "$type": "color"},
            "secondary": {"$value": t.get("secondary","#818CF8"), "$type": "color"},
            "cta":       {"$value": t.get("cta","#A78BFA"),       "$type": "color"},
            "bg":        {"$value": t.get("bg","#09090B"),        "$type": "color"},
            "surface":   {"$value": t.get("surface","#18181B"),   "$type": "color"},
            "text":      {"$value": t.get("text","#FAFAFA"),      "$type": "color"},
            "muted":     {"$value": t.get("muted","#71717A"),     "$type": "color"},
            "border":    {"$value": t.get("border","#27272A"),    "$type": "color"},
        },
        "typography": {
            "fontFamily": {
                "heading": {"$value": t.get("font_heading","Outfit"), "$type": "fontFamily"},
                "body":    {"$value": t.get("font_body","Inter"),     "$type": "fontFamily"},
            },
            "fontSize": {
                "caption": {"$value":"12px","$type":"dimension"},
                "sm":      {"$value":"14px","$type":"dimension"},
                "base":    {"$value":"16px","$type":"dimension"},
                "lg":      {"$value":"18px","$type":"dimension"},
                "xl":      {"$value":"20px","$type":"dimension"},
                "2xl":     {"$value":"24px","$type":"dimension"},
                "3xl":     {"$value":"30px","$type":"dimension"},
                "4xl":     {"$value":"36px","$type":"dimension"},
                "5xl":     {"$value":"48px","$type":"dimension"},
                "6xl":     {"$value":"60px","$type":"dimension"},
                "7xl":     {"$value":"72px","$type":"dimension"},
            },
        },
        "spacing": {
            "1": {"$value":"4px","$type":"dimension"},
            "2": {"$value":"8px","$type":"dimension"},
            "3": {"$value":"12px","$type":"dimension"},
            "4": {"$value":"16px","$type":"dimension"},
            "6": {"$value":"24px","$type":"dimension"},
            "8": {"$value":"32px","$type":"dimension"},
            "12":{"$value":"48px","$type":"dimension"},
            "16":{"$value":"64px","$type":"dimension"},
            "24":{"$value":"96px","$type":"dimension"},
        },
        "borderRadius": {
            "sm": {"$value":"6px","$type":"dimension"},
            "md": {"$value":"10px","$type":"dimension"},
            "lg": {"$value":"16px","$type":"dimension"},
            "xl": {"$value":"24px","$type":"dimension"},
            "full":{"$value":"9999px","$type":"dimension"},
        },
        "shadow": {
            "sm": {"$value":"0 1px 2px rgba(0,0,0,.05)","$type":"shadow"},
            "md": {"$value":"0 4px 16px rgba(0,0,0,.10)","$type":"shadow"},
            "lg": {"$value":"0 12px 40px rgba(0,0,0,.15)","$type":"shadow"},
        },
        "animation": {
            "duration": {
                "fast":   {"$value":"150ms","$type":"duration"},
                "normal": {"$value":"250ms","$type":"duration"},
                "slow":   {"$value":"400ms","$type":"duration"},
                "spring": {"$value":"600ms","$type":"duration"},
            },
            "easing": {
                "entrance": {"$value":"cubic-bezier(0.16,1,0.3,1)","$type":"cubicBezier"},
                "exit":     {"$value":"cubic-bezier(0.5,0,1,1)","$type":"cubicBezier"},
                "standard": {"$value":"cubic-bezier(0.4,0,0.2,1)","$type":"cubicBezier"},
            },
        },
    }
    return json.dumps(data, indent=2)

def gen_css(t: dict) -> str:
    return f"""/* Design Tokens — W3C compatible CSS custom properties
 * Generated: {datetime.now().strftime('%Y-%m-%d')}
 * Source: design-system/tokens.json
 */
:root {{
  /* Color */
  --color-primary:   {t.get('primary','#6366F1')};
  --color-secondary: {t.get('secondary','#818CF8')};
  --color-cta:       {t.get('cta','#A78BFA')};
  --color-bg:        {t.get('bg','#09090B')};
  --color-surface:   {t.get('surface','#18181B')};
  --color-text:      {t.get('text','#FAFAFA')};
  --color-muted:     {t.get('muted','#71717A')};
  --color-border:    {t.get('border','#27272A')};

  /* Typography */
  --font-heading:    '{t.get('font_heading','Outfit')}', sans-serif;
  --font-body:       '{t.get('font_body','Inter')}', sans-serif;

  /* Spacing (8px grid) */
  --space-1: 4px;  --space-2: 8px;  --space-3: 12px; --space-4: 16px;
  --space-6: 24px; --space-8: 32px; --space-12: 48px; --space-16: 64px; --space-24: 96px;

  /* Border radius */
  --radius-sm: 6px;  --radius-md: 10px; --radius-lg: 16px;
  --radius-xl: 24px; --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,.05);
  --shadow-md: 0 4px 16px rgba(0,0,0,.10);
  --shadow-lg: 0 12px 40px rgba(0,0,0,.15);

  /* Animation */
  --duration-fast:   150ms;
  --duration-normal: 250ms;
  --duration-slow:   400ms;
  --duration-spring: 600ms;
  --ease-entrance: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-exit:     cubic-bezier(0.5, 0, 1, 1);
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
}}

@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }}
}}
"""

def gen_ts(t: dict) -> str:
    return f"""// Design Tokens — TypeScript
// Generated: {datetime.now().strftime('%Y-%m-%d')}
// Usage: import {{ tokens }} from '@/design-system/tokens'

export const tokens = {{
  color: {{
    primary:   '{t.get('primary','#6366F1')}',
    secondary: '{t.get('secondary','#818CF8')}',
    cta:       '{t.get('cta','#A78BFA')}',
    bg:        '{t.get('bg','#09090B')}',
    surface:   '{t.get('surface','#18181B')}',
    text:      '{t.get('text','#FAFAFA')}',
    muted:     '{t.get('muted','#71717A')}',
    border:    '{t.get('border','#27272A')}',
  }},
  font: {{
    heading: "'{t.get('font_heading','Outfit')}', sans-serif",
    body:    "'{t.get('font_body','Inter')}', sans-serif",
  }},
  spacing: {{
    '1': '4px', '2': '8px',  '3': '12px', '4': '16px',
    '6': '24px','8': '32px', '12':'48px', '16':'64px', '24':'96px',
  }},
  radius: {{ sm:'6px', md:'10px', lg:'16px', xl:'24px', full:'9999px' }},
  shadow: {{
    sm: '0 1px 2px rgba(0,0,0,.05)',
    md: '0 4px 16px rgba(0,0,0,.10)',
    lg: '0 12px 40px rgba(0,0,0,.15)',
  }},
  duration: {{ fast:'150ms', normal:'250ms', slow:'400ms', spring:'600ms' }},
  ease: {{
    entrance: 'cubic-bezier(0.16,1,0.3,1)',
    exit:     'cubic-bezier(0.5,0,1,1)',
    standard: 'cubic-bezier(0.4,0,0.2,1)',
  }},
}} as const

export type DesignToken = typeof tokens
export type ColorToken  = keyof typeof tokens.color
"""

def gen_tailwind(t: dict) -> str:
    fh = t.get('font_heading','Outfit')
    fb = t.get('font_body','Inter')
    return f"""// tailwind.config.ts — Generated from design tokens
// Generated: {datetime.now().strftime('%Y-%m-%d')}
import type {{ Config }} from 'tailwindcss'

const config: Config = {{
  content: ['./src/**/*.{{ts,tsx}}', './app/**/*.{{ts,tsx}}'],
  darkMode: 'class',
  theme: {{
    extend: {{
      fontFamily: {{
        heading: ['{fh}', 'sans-serif'],
        body:    ['{fb}', 'sans-serif'],
      }},
      colors: {{
        primary:   'var(--color-primary)',
        secondary: 'var(--color-secondary)',
        cta:       'var(--color-cta)',
        bg:        'var(--color-bg)',
        surface:   'var(--color-surface)',
        muted:     'var(--color-muted)',
        border:    'var(--color-border)',
      }},
      spacing: {{
        '18': '72px', '22': '88px', '26': '104px',
      }},
      borderRadius: {{
        sm: '6px', md: '10px', lg: '16px', xl: '24px',
      }},
      boxShadow: {{
        'glow-sm': '0 0 12px var(--color-primary)/20',
        'glow-md': '0 0 24px var(--color-primary)/30',
        'glow-lg': '0 0 48px var(--color-primary)/40',
      }},
      animation: {{
        'fade-in':   'fadeIn 400ms cubic-bezier(0.16,1,0.3,1)',
        'slide-up':  'slideUp 400ms cubic-bezier(0.16,1,0.3,1)',
        'slide-down':'slideDown 400ms cubic-bezier(0.16,1,0.3,1)',
        'scale-in':  'scaleIn 300ms cubic-bezier(0.16,1,0.3,1)',
      }},
      keyframes: {{
        fadeIn:    {{ from: {{ opacity:'0' }}, to: {{ opacity:'1' }} }},
        slideUp:   {{ from: {{ opacity:'0',transform:'translateY(16px)' }},to:{{ opacity:'1',transform:'translateY(0)' }} }},
        slideDown: {{ from: {{ opacity:'0',transform:'translateY(-16px)' }},to:{{ opacity:'1',transform:'translateY(0)' }} }},
        scaleIn:   {{ from: {{ opacity:'0',transform:'scale(0.95)' }},to:{{ opacity:'1',transform:'scale(1)' }} }},
      }},
    }},
  }},
  plugins: [],
}}
export default config
"""

def main():
    parser = argparse.ArgumentParser(description="/tokens — Design Token Generator")
    parser.add_argument("--format","-f", default="all",
                        choices=["all","w3c","css","ts","tailwind","figma"])
    args = parser.parse_args()
    root = Path.cwd()
    t = load_tokens(root)
    out_dir = root/"design-system"; out_dir.mkdir(exist_ok=True)

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║        /tokens — W3C Design Token Generator         ║")
    print("╚══════════════════════════════════════════════════════╝\n")

    outputs = {
        "w3c": ("tokens.json", gen_w3c),
        "css": ("tokens.css",  gen_css),
        "ts":  ("tokens.ts",   gen_ts),
        "tailwind": ("tailwind.config.ts", gen_tailwind),
    }

    formats = list(outputs.keys()) if args.format == "all" else [args.format]
    for fmt in formats:
        if fmt == "figma":
            print("  ℹ  Figma Variables: import tokens.json into Figma via Variables Import plugin.")
            continue
        fname, gen_fn = outputs[fmt]
        content = gen_fn(t)
        path = out_dir/fname
        path.write_text(content)
        print(f"  ✓ {fname} → design-system/{fname}")
    print(f"\n  Tokens: {t.get('primary')} primary · {t.get('font_heading')} heading\n")

if __name__ == "__main__":
    main()
