#!/usr/bin/env python3
"""
/preview — Self-contained HTML design preview generator v1.0
Generates a zero-dependency .html file that renders the full design instantly.
No npm, no CDN, no React — just open in browser or Claude artifact panel.

Usage:
  python3 preview.py                        # landing page preview
  python3 preview.py --page dashboard       # dashboard layout
  python3 preview.py --page auth            # auth screen
  python3 preview.py --page pricing         # pricing page
  python3 preview.py --page portfolio       # portfolio
  python3 preview.py --dark                 # force dark mode
  python3 preview.py --open                 # open in browser after generating
  python3 preview.py --output preview.html  # custom output path
"""

import sys, argparse, webbrowser, os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from core import resolve_product


# ── Load existing design system tokens from MASTER.md ────────────────
def load_design_system(root: Path) -> dict:
    master = root / "design-system" / "MASTER.md"
    if not master.exists():
        return {}
    content = master.read_text(errors="ignore")
    tokens = {}
    for line in content.splitlines():
        line = line.strip()
        pairs = {
            "--color-primary:":   "primary",
            "--color-secondary:": "secondary",
            "--color-cta:":       "cta",
            "--color-bg:":        "bg",
            "--color-surface:":   "surface",
            "--color-text:":      "text",
            "--color-muted:":     "muted",
            "--color-border:":    "border",
        }
        for css_var, key in pairs.items():
            if line.startswith(css_var):
                tokens[key] = line.split(":", 1)[1].strip().rstrip(";")
        if line.startswith("--font-heading:"):
            raw = line.split(":", 1)[1].strip().rstrip(";")
            tokens["font_heading"] = raw.split(",")[0].strip().strip("'\"")
        if line.startswith("--font-body:"):
            raw = line.split(":", 1)[1].strip().rstrip(";")
            tokens["font_body"] = raw.split(",")[0].strip().strip("'\"")
    return tokens


def default_tokens(product: str, style: str, dark: bool) -> dict:
    resolved = resolve_product(product, style)
    p = resolved["palette"]
    t = resolved["typography"]
    return {
        "primary":      p["primary"],
        "secondary":    p["secondary"],
        "cta":          p["cta"],
        "bg":           p["bg"] if dark else "#FFFFFF",
        "surface":      p.get("surface_dark", "#18181B") if dark else p.get("surface", "#F9FAFB"),
        "text":         p["text"] if dark else "#0F172A",
        "muted":        p["muted"],
        "border":       p.get("border_dark", "#27272A") if dark else p.get("border", "#E2E8F0"),
        "font_heading": t["heading"],
        "font_body":    t["body"],
    }


# ── Base CSS ─────────────────────────────────────────────────────────
def base_css(T: dict) -> str:
    p = T["primary"]
    return f"""
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --color-primary:   {T["primary"]};
  --color-secondary: {T["secondary"]};
  --color-cta:       {T["cta"]};
  --color-bg:        {T["bg"]};
  --color-surface:   {T["surface"]};
  --color-text:      {T["text"]};
  --color-muted:     {T["muted"]};
  --color-border:    {T["border"]};
  --font-heading: '{T["font_heading"]}', sans-serif;
  --font-body:    '{T["font_body"]}', sans-serif;
  --radius-sm: 6px; --radius-md: 10px; --radius-lg: 16px; --radius-xl: 24px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,.05);
  --shadow-md: 0 4px 16px rgba(0,0,0,.10);
  --shadow-lg: 0 12px 40px rgba(0,0,0,.15);
}}
html {{ background: var(--color-bg); color: var(--color-text); scroll-behavior: smooth; }}
body {{ font-family: var(--font-body); font-size: 16px; line-height: 1.6; background: var(--color-bg); }}
h1,h2,h3,h4 {{ font-family: var(--font-heading); line-height: 1.15; font-weight: 700; }}
a {{ color: var(--color-primary); text-decoration: none; cursor: pointer; }}
.btn-primary {{
  display: inline-flex; align-items: center; gap: 8px;
  background: {p}; color: #fff; padding: 12px 28px;
  border-radius: var(--radius-md); font-family: var(--font-body);
  font-size: 15px; font-weight: 600; border: none; cursor: pointer;
  transition: transform .15s, box-shadow .15s, background .15s;
}}
.btn-primary:hover {{ background: {p}dd; transform: translateY(-1px); box-shadow: 0 4px 20px {p}50; }}
.btn-secondary {{
  display: inline-flex; align-items: center; gap: 8px;
  background: transparent; color: {T["text"]}; padding: 12px 28px;
  border-radius: var(--radius-md); font-family: var(--font-body);
  font-size: 15px; font-weight: 600; border: 1px solid {T["border"]}; cursor: pointer;
  transition: background .15s, border-color .15s;
}}
.btn-secondary:hover {{ background: {T["surface"]}; border-color: {p}; }}
.badge {{
  display: inline-flex; align-items: center; gap: 6px;
  background: {p}18; color: {p}; border: 1px solid {p}30;
  padding: 4px 14px; border-radius: 999px; font-size: 13px; font-weight: 600;
}}
.card {{
  background: {T["surface"]}; border: 1px solid {T["border"]};
  border-radius: var(--radius-lg); padding: 28px;
  box-shadow: var(--shadow-sm); transition: box-shadow .2s, border-color .2s;
}}
.card:hover {{ box-shadow: var(--shadow-md); border-color: {p}40; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; }}
.section {{ padding: 96px 0; }}
.grid-3 {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 24px; }}
.grid-2 {{ display: grid; grid-template-columns: repeat(2,1fr); gap: 32px; }}
@media (max-width: 768px) {{
  .grid-3, .grid-2 {{ grid-template-columns: 1fr; }}
  .section {{ padding: 64px 0; }}
  #preview-banner .status {{ display: none; }}
}}
#preview-banner {{
  position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
  background: {p}; color: #fff; padding: 8px 16px;
  display: flex; align-items: center; justify-content: space-between;
  font-family: var(--font-body); font-size: 13px; font-weight: 500;
  box-shadow: 0 2px 12px {p}60;
}}
#preview-banner .actions {{ display: flex; gap: 8px; }}
#preview-banner button {{
  background: rgba(255,255,255,.2); border: 1px solid rgba(255,255,255,.3);
  color: #fff; padding: 5px 14px; border-radius: 6px; cursor: pointer;
  font-size: 12px; font-weight: 600; transition: background .15s; white-space: nowrap;
}}
#preview-banner button:hover {{ background: rgba(255,255,255,.35); }}
#preview-banner .approve-btn {{ background: rgba(255,255,255,.35); font-weight: 700; }}
#token-sidebar {{
  position: fixed; right: 0; top: 40px; bottom: 0; width: 240px; z-index: 9998;
  background: {T["surface"]}; border-left: 1px solid {T["border"]};
  overflow-y: auto; padding: 16px 12px; transform: translateX(100%);
  transition: transform .25s ease; font-family: var(--font-body);
  box-shadow: -4px 0 24px rgba(0,0,0,.12);
}}
#token-sidebar.open {{ transform: translateX(0); }}
#token-sidebar h3 {{
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: .1em; color: {T["muted"]}; margin: 16px 0 10px;
  font-family: var(--font-body);
}}
#token-sidebar h3:first-child {{ margin-top: 0; }}
.token-row {{ display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }}
.swatch {{ width: 26px; height: 26px; border-radius: 6px; flex-shrink: 0; border: 1px solid {T["border"]}; }}
.token-name {{ font-size: 12px; font-weight: 600; color: {T["text"]}; }}
.token-value {{ font-size: 11px; color: {T["muted"]}; font-family: monospace; }}
#preview-content {{ padding-top: 40px; transition: margin-right .25s; }}
#preview-content.sidebar-open {{ margin-right: 240px; }}
"""


# ── Token sidebar HTML ────────────────────────────────────────────────
def token_sidebar(T: dict) -> str:
    color_rows = ""
    for name, val in [
        ("primary", T["primary"]), ("secondary", T["secondary"]), ("cta", T["cta"]),
        ("bg", T["bg"]), ("surface", T["surface"]),
        ("text", T["text"]), ("muted", T["muted"]), ("border", T["border"]),
    ]:
        color_rows += f'''<div class="token-row">
  <div class="swatch" style="background:{val}"></div>
  <div><div class="token-name">{name}</div><div class="token-value">{val}</div></div>
</div>\n'''

    spacing_rows = ""
    for name, val in [("xs","4px"),("sm","8px"),("md","16px"),("lg","24px"),
                       ("xl","32px"),("2xl","48px"),("3xl","64px"),("4xl","96px")]:
        spacing_rows += f'<div class="token-row"><div style="width:26px;height:6px;background:{T["primary"]}60;border-radius:3px;"></div><div><div class="token-name">{name}</div><div class="token-value">{val}</div></div></div>\n'

    return f"""<div id="token-sidebar">
  <h3>Colors</h3>
  {color_rows}
  <h3>Typography</h3>
  <div class="token-row"><div><div class="token-name">Heading</div><div class="token-value">{T["font_heading"]}</div></div></div>
  <div class="token-row"><div><div class="token-name">Body</div><div class="token-value">{T["font_body"]}</div></div></div>
  <h3>Spacing (8px grid)</h3>
  {spacing_rows}
</div>"""


# ── Page builders ─────────────────────────────────────────────────────
def page_landing(T: dict) -> str:
    p = T["primary"]; s = T["secondary"]; bg = T["bg"]
    surface = T["surface"]; text = T["text"]; muted = T["muted"]; border = T["border"]

    nav_links = "".join(
        f'<a href="#" style="color:{muted};font-size:14px;font-weight:500;">{lbl}</a>'
        for lbl in ["Features", "Pricing", "Docs", "Blog"]
    )

    feat_cards = ""
    for icon, title, desc in [
        ("⚡", "AI Design System", "Generate complete design tokens, type scales, and component selections in seconds."),
        ("🎯", "12+ Libraries", "Best component for every slot — React Bits, Aceternity, Magic UI, and 9 more."),
        ("🚀", "Ship-Ready Code", "Framework-correct, accessible, and performance-optimized. Every time."),
    ]:
        feat_cards += f'''<div class="card">
  <div style="width:44px;height:44px;border-radius:10px;background:{p}15;display:flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:20px;">{icon}</div>
  <h3 style="font-size:18px;margin-bottom:10px;">{title}</h3>
  <p style="color:{muted};font-size:14px;line-height:1.7;">{desc}</p>
</div>\n'''

    testimonials = ""
    for quote, name, role in [
        ("Saved us weeks of design work. The component selection is exactly right.", "Sarah Chen", "Lead Engineer, Vercel"),
        ("The /preview workflow is genius. Design and dev finally in sync.", "Marcus Rivera", "CTO, Linear"),
        ("Design to production in 2 days. That used to take 3 weeks.", "Priya Patel", "Head of Product, Notion"),
    ]:
        initial = name[0]
        testimonials += f'''<div class="card">
  <div style="display:flex;gap:3px;margin-bottom:16px;color:{p};font-size:14px;">★★★★★</div>
  <p style="font-size:14px;line-height:1.7;margin-bottom:20px;">"{quote}"</p>
  <div style="display:flex;align-items:center;gap:12px;">
    <div style="width:36px;height:36px;border-radius:50%;background:{p}25;display:flex;align-items:center;justify-content:center;font-weight:700;color:{p};font-size:13px;">{initial}</div>
    <div><div style="font-weight:600;font-size:14px;">{name}</div><div style="font-size:12px;color:{muted};">{role}</div></div>
  </div>
</div>\n'''

    logos = "".join(
        f'<span style="font-family:var(--font-heading);font-weight:700;font-size:17px;color:{text};">{n}</span>'
        for n in ["Stripe", "Vercel", "Linear", "Notion", "Figma", "Supabase"]
    )

    return f"""<nav style="border-bottom:1px solid {border};background:{bg};position:sticky;top:40px;z-index:100;">
  <div class="container" style="display:flex;align-items:center;justify-content:space-between;height:64px;">
    <div style="font-family:var(--font-heading);font-weight:800;font-size:20px;color:{p};">YourBrand</div>
    <div style="display:flex;gap:32px;">{nav_links}</div>
    <button class="btn-primary" style="padding:9px 20px;font-size:14px;">Get Started →</button>
  </div>
</nav>

<section style="min-height:88vh;display:flex;align-items:center;background:linear-gradient(160deg,{bg} 0%,{surface} 100%);position:relative;overflow:hidden;">
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 70% 50%,{p}18 0%,transparent 65%);pointer-events:none;"></div>
  <div class="container" style="text-align:center;position:relative;z-index:1;">
    <div class="badge" style="margin:0 auto 28px;">✨ New — /preview + /approved + /apply workflow</div>
    <h1 style="font-size:clamp(42px,7vw,88px);font-weight:800;letter-spacing:-.04em;margin-bottom:28px;line-height:1.0;">
      Design at the speed<br>of <span style="color:{p};">thought</span>
    </h1>
    <p style="font-size:19px;color:{muted};max-width:540px;margin:0 auto 44px;line-height:1.7;">
      The complete design-to-code platform. From idea to production-ready components in minutes.
    </p>
    <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;">
      <button class="btn-primary" style="font-size:16px;padding:14px 32px;">Start building free →</button>
      <button class="btn-secondary" style="font-size:16px;padding:14px 32px;">Watch demo ▶</button>
    </div>
    <p style="color:{muted};font-size:13px;margin-top:18px;">No credit card · Free 14 days · Cancel anytime</p>
    <div style="display:flex;align-items:center;justify-content:center;gap:8px;margin-top:40px;font-size:14px;color:{muted};">
      <span style="color:{p};">★★★★★</span>
      <strong style="color:{text};">4.9/5</strong>
      <span>from 2,400+ developers</span>
    </div>
  </div>
</section>

<section style="padding:28px 0;border-top:1px solid {border};border-bottom:1px solid {border};background:{surface};">
  <div class="container">
    <p style="text-align:center;color:{muted};font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin-bottom:20px;">Trusted by teams at</p>
    <div style="display:flex;gap:48px;justify-content:center;align-items:center;flex-wrap:wrap;opacity:.45;">{logos}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div style="text-align:center;margin-bottom:64px;">
      <h2 style="font-size:clamp(28px,4vw,48px);font-weight:800;letter-spacing:-.025em;margin-bottom:16px;">Everything you need to ship</h2>
      <p style="color:{muted};font-size:18px;max-width:460px;margin:0 auto;">Three capabilities that replace your entire design workflow.</p>
    </div>
    <div class="grid-3">{feat_cards}</div>
  </div>
</section>

<section class="section" style="background:{surface};border-top:1px solid {border};border-bottom:1px solid {border};">
  <div class="container">
    <div style="text-align:center;margin-bottom:64px;">
      <h2 style="font-size:clamp(28px,4vw,48px);font-weight:800;letter-spacing:-.025em;margin-bottom:16px;">Loved by teams who ship</h2>
    </div>
    <div class="grid-3">{testimonials}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div style="background:linear-gradient(135deg,{p},{s});border-radius:24px;padding:80px 48px;text-align:center;position:relative;overflow:hidden;">
      <div style="position:absolute;top:-60px;right:-60px;width:240px;height:240px;border-radius:50%;background:rgba(255,255,255,.07);"></div>
      <div style="position:absolute;bottom:-40px;left:-40px;width:180px;height:180px;border-radius:50%;background:rgba(255,255,255,.05);"></div>
      <h2 style="font-size:clamp(28px,4vw,48px);font-weight:800;color:#fff;margin-bottom:16px;letter-spacing:-.025em;position:relative;">Ready to build something beautiful?</h2>
      <p style="color:rgba(255,255,255,.8);font-size:18px;margin-bottom:40px;position:relative;">Join 12,000+ developers shipping faster.</p>
      <button style="background:#fff;color:{p};padding:14px 40px;border-radius:var(--radius-md);font-weight:700;font-size:16px;border:none;cursor:pointer;box-shadow:0 4px 24px rgba(0,0,0,.25);position:relative;">Start building free →</button>
    </div>
  </div>
</section>

<footer style="border-top:1px solid {border};padding:40px 0;">
  <div class="container" style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
    <div style="font-family:var(--font-heading);font-weight:800;font-size:17px;color:{p};">YourBrand</div>
    <div style="display:flex;gap:24px;">
      {"".join(f'<a href="#" style="color:{muted};font-size:13px;">{lbl}</a>' for lbl in ["Privacy","Terms","Blog","Docs"])}
    </div>
    <p style="font-size:12px;color:{muted};">© 2025 YourBrand. All rights reserved.</p>
  </div>
</footer>"""


def page_dashboard(T: dict) -> str:
    p = T["primary"]; text = T["text"]; muted = T["muted"]
    border = T["border"]; surface = T["surface"]; bg = T["bg"]

    nav_items = ""
    for icon, label, active in [
        ("📊","Overview",True),("📈","Analytics",False),("👥","Users",False),
        ("💳","Revenue",False),("⚙️","Settings",False)
    ]:
        style = f"background:{p}12;color:{p};border-left:3px solid {p};" if active else f"color:{muted};"
        nav_items += f'<a href="#" style="display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:8px;font-size:14px;font-weight:500;margin-bottom:2px;{style}text-decoration:none;">{icon} {label}</a>\n'

    kpi_cards = ""
    for label, value, change, positive in [
        ("Total Revenue","$48,234","+12.5% vs last month",True),
        ("Active Users","3,842","+8.2% this week",True),
        ("Conversion Rate","4.6%","+0.3% vs last month",True),
        ("Avg Session","2m 34s","-0.12s vs last week",False),
    ]:
        color = "#22C55E" if positive else "#EF4444"
        kpi_cards += f'''<div class="card" style="padding:20px;">
  <p style="font-size:11px;color:{muted};font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:10px;">{label}</p>
  <p style="font-size:30px;font-weight:800;font-family:var(--font-heading);color:{text};margin-bottom:6px;">{value}</p>
  <p style="font-size:12px;color:{color};">{"↑" if positive else "↓"} {change}</p>
</div>\n'''

    bars = "".join(
        f'<div style="flex:1;background:{p};border-radius:3px 3px 0 0;height:{h}%;opacity:.75;min-width:0;transition:opacity .15s;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.75"></div>'
        for h in [40,58,35,72,88,60,78,92,65,82,95,72,85,60,78]
    )

    channels = ""
    for ch, pct in [("Organic Search",42),("Direct",28),("Social Media",18),("Email",12)]:
        channels += f'''<div style="margin-bottom:16px;">
  <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px;">
    <span style="color:{text};">{ch}</span><span style="font-weight:700;">{pct}%</span>
  </div>
  <div style="height:6px;background:{border};border-radius:3px;">
    <div style="height:6px;background:{p};border-radius:3px;width:{pct}%;transition:width .3s;"></div>
  </div>
</div>\n'''

    table_rows = ""
    for name, email, role, status in [
        ("Sarah Chen","sarah@example.com","Admin","Active"),
        ("Marcus Rivera","marcus@example.com","Editor","Active"),
        ("Priya Patel","priya@example.com","Viewer","Away"),
        ("James Wilson","james@example.com","Editor","Inactive"),
    ]:
        sc = "#22C55E" if status=="Active" else ("#F59E0B" if status=="Away" else "#EF4444")
        table_rows += f'''<tr style="border-bottom:1px solid {border};">
  <td style="padding:12px 16px;font-size:13px;font-weight:600;">{name}</td>
  <td style="padding:12px 16px;font-size:13px;color:{muted};">{email}</td>
  <td style="padding:12px 16px;font-size:13px;">{role}</td>
  <td style="padding:12px 16px;">
    <span style="background:{sc}20;color:{sc};padding:3px 10px;border-radius:999px;font-size:11px;font-weight:700;">{status}</span>
  </td>
</tr>\n'''

    return f'''<div style="display:flex;height:calc(100vh - 40px);overflow:hidden;">
  <aside style="width:240px;background:{surface};border-right:1px solid {border};display:flex;flex-direction:column;flex-shrink:0;overflow-y:auto;">
    <div style="padding:20px;border-bottom:1px solid {border};">
      <div style="font-family:var(--font-heading);font-weight:800;font-size:18px;color:{p};">Dashboard</div>
    </div>
    <nav style="padding:12px;flex:1;">{nav_items}</nav>
    <div style="padding:16px;border-top:1px solid {border};">
      <div style="display:flex;align-items:center;gap:10px;">
        <div style="width:32px;height:32px;border-radius:50%;background:{p}25;display:flex;align-items:center;justify-content:center;font-weight:800;color:{p};font-size:13px;">A</div>
        <div><div style="font-size:13px;font-weight:600;color:{text};">Admin User</div><div style="font-size:11px;color:{muted};">admin@example.com</div></div>
      </div>
    </div>
  </aside>
  <div style="flex:1;overflow-y:auto;display:flex;flex-direction:column;">
    <header style="height:56px;border-bottom:1px solid {border};background:{bg};display:flex;align-items:center;justify-content:space-between;padding:0 24px;flex-shrink:0;">
      <div style="font-size:13px;"><span style="color:{muted};">Dashboard</span> <span style="color:{muted};">/</span> <span style="font-weight:600;color:{text};">Overview</span></div>
      <button class="btn-primary" style="padding:7px 16px;font-size:13px;">+ New Report</button>
    </header>
    <main style="padding:24px;flex:1;overflow-y:auto;">
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px;">{kpi_cards}</div>
      <div style="display:grid;grid-template-columns:2fr 1fr;gap:20px;margin-bottom:24px;">
        <div class="card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
            <h3 style="font-size:15px;">Revenue Over Time</h3>
            <select style="font-size:12px;border:1px solid {border};border-radius:6px;padding:5px 8px;background:{surface};color:{text};cursor:pointer;"><option>Last 30 days</option></select>
          </div>
          <div style="height:180px;display:flex;align-items:flex-end;gap:6px;padding-bottom:8px;position:relative;border-bottom:1px solid {border};">
            {bars}
          </div>
          <div style="display:flex;justify-content:space-between;margin-top:8px;font-size:11px;color:{muted};">
            <span>Mar 1</span><span>Mar 8</span><span>Mar 15</span><span>Mar 22</span><span>Mar 30</span>
          </div>
        </div>
        <div class="card"><h3 style="font-size:15px;margin-bottom:20px;">Traffic Channels</h3>{channels}</div>
      </div>
      <div class="card" style="padding:0;overflow:hidden;">
        <div style="padding:16px 20px;border-bottom:1px solid {border};display:flex;justify-content:space-between;align-items:center;">
          <h3 style="font-size:15px;">Recent Users</h3>
          <button class="btn-secondary" style="padding:6px 14px;font-size:12px;">View all</button>
        </div>
        <table style="width:100%;border-collapse:collapse;">
          <thead><tr style="background:{surface};">
            {"".join(f'<th style="padding:10px 16px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.07em;color:{muted};text-align:left;">{h}</th>' for h in ["Name","Email","Role","Status"])}
          </tr></thead>
          <tbody>{table_rows}</tbody>
        </table>
      </div>
    </main>
  </div>
</div>'''


def page_auth(T: dict) -> str:
    p = T["primary"]; s = T["secondary"]
    text = T["text"]; muted = T["muted"]; border = T["border"]
    surface = T["surface"]; bg = T["bg"]

    perks = ""
    for icon, title, desc in [
        ("⚡","AI-powered design","Generate complete design systems and production code in seconds"),
        ("🎯","12+ component libraries","Every slot gets the best component from the best library"),
        ("✅","Ship with confidence","Built-in review, a11y, and deployment gates ensure quality"),
    ]:
        perks += f'''<div style="display:flex;align-items:flex-start;gap:14px;margin-bottom:22px;">
  <div style="width:30px;height:30px;border-radius:50%;background:rgba(255,255,255,.18);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:14px;">{icon}</div>
  <div><p style="color:#fff;font-size:14px;font-weight:600;margin-bottom:3px;">{title}</p><p style="color:rgba(255,255,255,.72);font-size:13px;line-height:1.5;">{desc}</p></div>
</div>\n'''

    social_btns = ""
    for icon, label in [("G","Google"), ("⌥","GitHub")]:
        social_btns += f'<button style="flex:1;padding:11px;border:1px solid {border};border-radius:var(--radius-md);background:{surface};color:{text};font-size:14px;font-weight:500;cursor:pointer;">{icon} {label}</button>\n'

    fields = ""
    for label, type_, ph in [("Email address","email","you@example.com"),("Password","password","••••••••")]:
        fields += f'''<div style="margin-bottom:16px;">
  <label style="display:block;font-size:13px;font-weight:600;margin-bottom:6px;color:{text};">{label}</label>
  <input type="{type_}" placeholder="{ph}" style="width:100%;padding:11px 14px;border:1px solid {border};border-radius:var(--radius-md);background:{surface};color:{text};font-size:14px;outline:none;font-family:var(--font-body);transition:border-color .15s;">
</div>\n'''

    return f'''<div style="min-height:calc(100vh - 40px);display:grid;grid-template-columns:1fr 1fr;">
  <div style="background:linear-gradient(145deg,{p},{s});display:flex;flex-direction:column;justify-content:center;padding:64px;position:relative;overflow:hidden;">
    <div style="position:absolute;top:-80px;right:-80px;width:320px;height:320px;border-radius:50%;background:rgba(255,255,255,.07);pointer-events:none;"></div>
    <div style="position:absolute;bottom:-60px;left:-60px;width:240px;height:240px;border-radius:50%;background:rgba(255,255,255,.05);pointer-events:none;"></div>
    <div style="position:relative;z-index:1;">
      <div style="font-family:var(--font-heading);font-size:26px;font-weight:800;color:#fff;margin-bottom:48px;">YourBrand</div>
      <h2 style="font-family:var(--font-heading);font-size:34px;font-weight:700;color:#fff;margin-bottom:14px;line-height:1.2;">Design at the<br>speed of thought</h2>
      <p style="color:rgba(255,255,255,.78);font-size:16px;line-height:1.65;margin-bottom:44px;">Join 12,000+ developers and designers building beautiful products faster than ever.</p>
      {perks}
    </div>
  </div>
  <div style="background:{bg};display:flex;align-items:center;justify-content:center;padding:48px;">
    <div style="width:100%;max-width:400px;">
      <h1 style="font-size:28px;font-weight:700;margin-bottom:8px;color:{text};">Welcome back</h1>
      <p style="color:{muted};font-size:15px;margin-bottom:32px;">Sign in to your account to continue</p>
      <div style="display:flex;gap:12px;margin-bottom:24px;">{social_btns}</div>
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:24px;">
        <div style="flex:1;height:1px;background:{border};"></div>
        <span style="font-size:12px;color:{muted};">or continue with email</span>
        <div style="flex:1;height:1px;background:{border};"></div>
      </div>
      {fields}
      <div style="display:flex;justify-content:flex-end;margin-bottom:24px;">
        <a href="#" style="font-size:13px;color:{p};font-weight:500;">Forgot password?</a>
      </div>
      <button class="btn-primary" style="width:100%;justify-content:center;padding:13px;font-size:15px;">Sign in →</button>
      <p style="text-align:center;font-size:13px;color:{muted};margin-top:24px;">
        Don't have an account? <a href="#" style="color:{p};font-weight:600;">Sign up free</a>
      </p>
    </div>
  </div>
</div>'''


def page_pricing(T: dict) -> str:
    p = T["primary"]; text = T["text"]; muted = T["muted"]
    border = T["border"]; surface = T["surface"]; bg = T["bg"]

    plans = [
        ("Starter", "Free", "/month", "Perfect for individuals", [
            "5 projects", "Basic components", "Community support", "HTML export"
        ], False),
        ("Pro", "$49", "/month", "For teams shipping products", [
            "Unlimited projects", "All 12+ libraries", "Priority support",
            "All export formats", "Team collaboration", "Design system sync",
        ], True),
        ("Enterprise", "Custom", "", "For organizations at scale", [
            "Everything in Pro", "SSO & SAML", "SLA guarantee",
            "Dedicated support", "Custom contracts", "Audit logs",
        ], False),
    ]

    plan_cards = ""
    for i, (name, price, period, desc, features, is_pro) in enumerate(plans):
        border_s = f"border:2px solid {p};box-shadow:0 24px 64px {p}28;transform:translateY(-8px);" if is_pro else ""
        price_color = p if is_pro else text
        btn_style = f"background:{p};color:#fff;border:none;" if is_pro else f"background:transparent;color:{text};border:1px solid {border};"
        btn_label = "Get Pro →" if is_pro else "Get started"
        badge = f"<div style='position:absolute;top:-14px;left:50%;transform:translateX(-50%);background:{p};color:#fff;padding:4px 20px;border-radius:999px;font-size:12px;font-weight:700;white-space:nowrap;'>Most Popular</div>" if is_pro else ""
        feats = "".join(
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:11px;font-size:14px;"><span style="color:#22C55E;">✓</span><span style="color:{text};">{feat}</span></div>'
            for feat in features
        )
        plan_cards += f'''<div class="card" style="padding:32px;position:relative;{border_s}">
  {badge}
  <h3 style="font-size:18px;font-weight:700;margin-bottom:10px;color:{text};">{name}</h3>
  <div style="display:flex;align-items:baseline;gap:4px;margin-bottom:8px;">
    <span style="font-size:38px;font-weight:800;font-family:var(--font-heading);color:{price_color};">{price}</span>
    <span style="font-size:14px;color:{muted};">{period}</span>
  </div>
  <p style="font-size:14px;color:{muted};margin-bottom:24px;">{desc}</p>
  <button style="width:100%;padding:12px;border-radius:var(--radius-md);font-size:14px;font-weight:600;cursor:pointer;margin-bottom:24px;{btn_style}">{btn_label}</button>
  {feats}
</div>\n'''

    return f'''<section class="section">
  <div class="container">
    <div style="text-align:center;margin-bottom:64px;">
      <h1 style="font-size:clamp(32px,5vw,58px);font-weight:800;letter-spacing:-.03em;margin-bottom:16px;color:{text};">Simple, transparent pricing</h1>
      <p style="color:{muted};font-size:18px;max-width:440px;margin:0 auto 36px;">Start free. Scale when ready. No surprises, no lock-in.</p>
      <div style="display:inline-flex;background:{surface};border:1px solid {border};border-radius:999px;padding:4px;gap:0;">
        <button style="padding:9px 28px;border-radius:999px;background:{p};color:#fff;border:none;font-size:14px;font-weight:600;cursor:pointer;">Monthly</button>
        <button style="padding:9px 28px;border-radius:999px;background:transparent;color:{muted};border:none;font-size:14px;font-weight:500;cursor:pointer;">Annual <span style="background:{p}20;color:{p};padding:2px 8px;border-radius:999px;font-size:11px;font-weight:700;margin-left:6px;">Save 20%</span></button>
      </div>
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px;align-items:start;padding:12px 0;">
      {plan_cards}
    </div>
    <div style="text-align:center;margin-top:48px;padding:32px;background:{surface};border-radius:var(--radius-xl);border:1px solid {border};">
      <p style="font-size:15px;font-weight:600;margin-bottom:6px;color:{text};">100% satisfaction guarantee</p>
      <p style="font-size:14px;color:{muted};">Try Pro free for 14 days. No credit card required. Cancel anytime with one click.</p>
    </div>
  </div>
</section>'''


def page_portfolio(T: dict) -> str:
    p = T["primary"]; s = T["secondary"]; cta = T["cta"]
    text = T["text"]; muted = T["muted"]; border = T["border"]
    surface = T["surface"]; bg = T["bg"]

    stats = "".join(
        f'<div><p style="font-size:38px;font-weight:800;font-family:var(--font-heading);color:{p};">{num}</p><p style="font-size:13px;color:{muted};">{label}</p></div>'
        for num, label in [("8+","Years exp."),("40+","Products"),("M+","Users")]
    )

    work_cards = ""
    for icon, title, desc, tags, c1, c2 in [
        ("🎨","Design System — Acme Corp","Complete design system used by 40+ engineers.",["Figma","React","Storybook"],p+"50",s+"50"),
        ("📱","Mobile App — FinTech","Onboarding redesign increased completion by 34%.",["iOS","UX Research","Swift"],cta+"50",p+"50"),
        ("🛒","E-commerce Platform","Checkout redesign reduced abandonment by 28%.",["Next.js","A/B Tests","Analytics"],s+"50",cta+"50"),
        ("📊","Analytics Dashboard","Real-time viz for 50k+ daily active users.",["D3.js","React","WebSockets"],p+"40",s+"40"),
    ]:
        tag_html = "".join(f'<span class="badge" style="font-size:11px;padding:3px 10px;">{t}</span>' for t in tags)
        work_cards += f'''<div class="card" style="padding:0;overflow:hidden;">
  <div style="height:200px;background:linear-gradient(135deg,{c1},{c2});display:flex;align-items:center;justify-content:center;font-size:52px;">{icon}</div>
  <div style="padding:24px;">
    <h3 style="font-size:17px;font-weight:700;margin-bottom:8px;color:{text};">{title}</h3>
    <p style="font-size:14px;color:{muted};margin-bottom:16px;">{desc}</p>
    <div style="display:flex;gap:8px;flex-wrap:wrap;">{tag_html}</div>
  </div>
</div>\n'''

    return f'''<nav style="position:sticky;top:40px;z-index:100;padding:0 48px;height:64px;display:flex;align-items:center;justify-content:space-between;background:{bg}f0;backdrop-filter:blur(12px);border-bottom:1px solid {border}20;">
  <div style="font-family:var(--font-heading);font-weight:800;font-size:18px;color:{text};">Alex Designer</div>
  <div style="display:flex;gap:32px;">
    {"".join(f'<a href="#" style="color:{""+p+";font-weight:600;" if active else muted+";"}font-size:14px;font-weight:500;">{lbl}</a>' for lbl,active in [("Work",False),("About",False),("Process",False),("Hire me",True)])}
  </div>
</nav>
<section style="min-height:88vh;display:flex;align-items:center;padding:0 48px;max-width:900px;">
  <div>
    <div class="badge" style="margin-bottom:28px;">✅ Available for work · Starting June 2025</div>
    <h1 style="font-size:clamp(48px,7vw,100px);font-weight:800;letter-spacing:-.04em;line-height:.98;margin-bottom:32px;color:{text};">
      Senior<br>Product<br><span style="color:{p};">Designer</span>
    </h1>
    <p style="font-size:18px;color:{muted};max-width:480px;line-height:1.7;margin-bottom:48px;">
      I design and build interfaces that people love. 8 years shipping products used by millions.
    </p>
    <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:64px;">
      <button class="btn-primary">View my work ↓</button>
      <button class="btn-secondary">Download CV</button>
    </div>
    <div style="display:flex;gap:56px;">{stats}</div>
  </div>
</section>
<section class="section" style="padding-top:0;">
  <div class="container">
    <h2 style="font-size:32px;font-weight:700;margin-bottom:48px;color:{text};">Selected work</h2>
    <div class="grid-2">{work_cards}</div>
  </div>
</section>'''


# ── Page router ───────────────────────────────────────────────────────
PAGE_BUILDERS = {
    "landing":   page_landing,
    "dashboard": page_dashboard,
    "auth":      page_auth,
    "pricing":   page_pricing,
    "portfolio": page_portfolio,
}


def build_html(page_type: str, T: dict, dark: bool) -> str:
    ts    = datetime.now().strftime("%Y-%m-%d %H:%M")
    mode  = "Dark" if dark else "Light"
    fn    = T["font_heading"]
    fb    = T["font_body"]
    gf    = f"https://fonts.googleapis.com/css2?family={fn.replace(' ','+')}:wght@400;600;700;800&family={fb.replace(' ','+')}:wght@400;500&display=swap"
    build = PAGE_BUILDERS.get(page_type, page_landing)
    body  = build(T)
    css   = base_css(T)
    tok   = token_sidebar(T)
    p     = T["primary"]

    # Sidebar token data for JS
    color_js = str({k: T[k] for k in ["primary","secondary","cta","bg","surface","text","muted","border"]})

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>/preview — {page_type.capitalize()} · {mode} · {ts}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{gf}" rel="stylesheet">
<style>{css}</style>
</head>
<body>

<div id="preview-banner">
  <span class="status">⚡ /preview — {page_type.capitalize()} · {mode} · {ts}</span>
  <div class="actions">
    <button onclick="toggleSidebar()">🎨 Tokens</button>
    <button onclick="alert('Open preview-{page_type}.html in your browser to toggle modes.')">
      {'☀️ Light' if dark else '🌙 Dark'}
    </button>
    <button class="approve-btn" onclick="showApproveMsg()">✅ /approved</button>
  </div>
</div>

{tok}

<div id="preview-content">
{body}
</div>

<script>
function toggleSidebar() {{
  document.getElementById('token-sidebar').classList.toggle('open');
  document.getElementById('preview-content').classList.toggle('sidebar-open');
}}
function showApproveMsg() {{
  const msg = [
    "Design approved! ✅",
    "",
    "Run in your terminal:",
    "python3 .claude/skills/ui-design-intelligence/scripts/approved.py",
    "",
    "This will:",
    "  • Lock these design tokens into design-system/MASTER.md",
    "  • Create a timestamped approval snapshot",
    "  • Enable /apply to generate production-ready code",
    "",
    "Or type /approved in Claude Code to approve directly.",
  ].join("\\n");
  alert(msg);
}}
</script>
</body>
</html>"""


# ── Main ──────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="/preview — Design Preview Generator")
    parser.add_argument("--page", "-p", default="landing",
                        choices=["landing","dashboard","auth","pricing","portfolio"])
    parser.add_argument("--product", default="Your Product")
    parser.add_argument("--style",   default="dark premium")
    parser.add_argument("--dark",    action="store_true")
    parser.add_argument("--open",    action="store_true")
    parser.add_argument("--output",  default="")
    args = parser.parse_args()

    root   = Path.cwd()
    tokens = load_design_system(root)

    if not tokens:
        tokens = default_tokens(args.product, args.style, args.dark)
        print("  ℹ  No design-system/MASTER.md found — using auto-generated defaults.")
        print("  ℹ  Run /design first to use your custom palette.\n")

    dark = args.dark or (tokens.get("bg","#fff") not in ("#FFFFFF","#ffffff","#fff","#F9FAFB","#FAFAFA"))
    html = build_html(args.page, tokens, dark)

    out_path = args.output or f"preview-{args.page}.html"
    Path(out_path).write_text(html, encoding="utf-8")

    print(f"\n  ✅ Preview generated → {out_path}")
    print(f"  Page:    {args.page}  |  Mode: {'Dark' if dark else 'Light'}")
    print(f"  Colors:  {tokens.get('primary')} primary  |  Fonts: {tokens.get('font_heading')} / {tokens.get('font_body')}")
    print(f"\n  📋 Next steps:")
    print(f"  1. Open {out_path} in your browser to review the design")
    print(f"  2. Click '✅ /approved' in the banner — or run:")
    print(f"     python3 .claude/skills/ui-design-intelligence/scripts/approved.py")
    print(f"  3. Then run /apply to generate production-ready component code\n")

    if args.open:
        webbrowser.open(f"file://{os.path.abspath(out_path)}")


if __name__ == "__main__":
    main()
