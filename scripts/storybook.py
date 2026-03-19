#!/usr/bin/env python3
"""
/storybook — Storybook Story Auto-Generator v1.0
Phase 13.1 — God-Level Roadmap

Generates .stories.tsx files for any component file.
Creates: default, all variants, dark mode, mobile, loading/error/empty states.

Usage:
  python3 storybook.py src/components/PricingCard.tsx
  python3 storybook.py --all                      # all components in src/
  python3 storybook.py --init                     # setup .storybook/ config
  python3 storybook.py src/components/KPICard.tsx --open
"""

import sys, re, argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))


# ═══════════════════════════════════════════════════════════════════════
# COMPONENT ANALYZER — extracts props from TypeScript interface
# ═══════════════════════════════════════════════════════════════════════

def extract_component_info(code: str) -> dict:
    """Extract component name, props, and variants from TypeScript source."""
    info = {
        "name":        "",
        "props":       {},
        "has_loading": False,
        "has_error":   False,
        "has_variant": False,
        "variants":    [],
        "description": "",
    }

    # Component name — from export default function Name or export default function
    name_match = re.search(r'export default function\s+(\w+)', code)
    if name_match:
        info["name"] = name_match.group(1)
    elif re.search(r'export default', code):
        info["name"] = "Component"

    # Description from JSDoc comment
    doc_match = re.search(r'/\*\*\s*\n\s*\*\s*([^\n*]+)', code)
    if doc_match:
        info["description"] = doc_match.group(1).strip()

    # Props from interface — handles single-line and multi-line interfaces
    iface_match = re.search(r'interface\s+\w+Props\s*\{([^}]+)\}', code, re.DOTALL)
    if iface_match:
        props_str = iface_match.group(1)
        # Split on ; or newline to handle both formats
        segments = re.split(r';|\n', props_str)
        for seg in segments:
            seg = seg.strip().strip(",")
            if not seg or seg.startswith("//"):
                continue
            prop_match = re.match(r'^(\w+)\??\s*:\s*(.+)$', seg)
            if prop_match:
                pname = prop_match.group(1).strip()
                ptype = prop_match.group(2).strip()
                if pname and ptype and pname not in ('interface','export','type','function'):
                    info["props"][pname] = ptype

    # Detect loading/error/empty props
    info["has_loading"] = "loading" in info["props"] or "isLoading" in code
    info["has_error"]   = "error" in info["props"] or "isError" in code

    # Extract variant union type
    variant_match = re.search(r"variant\??:\s*'([^']+)'(?:\s*\|\s*'([^']+)')*", code)
    if variant_match:
        all_variants = re.findall(r"'([^']+)'", code[variant_match.start():variant_match.end()+100])
        info["variants"]    = all_variants[:6]
        info["has_variant"] = True

    return info


# ═══════════════════════════════════════════════════════════════════════
# STORY GENERATORS
# ═══════════════════════════════════════════════════════════════════════

def gen_prop_default(pname: str, ptype: str, component_name: str) -> str:
    """Generate a sensible default value for a prop based on its type."""
    t = ptype.lower().strip()
    
    # Special cases by prop name
    name_defaults = {
        "label":       '"Button label"',
        "title":       f'"{component_name} title"',
        "description": '"A description for this component"',
        "heading":     '"Section heading"',
        "headline":    '"Your compelling headline here"',
        "subheadline": '"Supporting text that explains the value"',
        "name":        '"John Doe"',
        "email":       '"user@example.com"',
        "role":        '"Product Designer"',
        "price":       '"$49"',
        "period":      '"/month"',
        "value":       "42000",
        "change":      "12.5",
        "ctaLabel":    '"Get started →"',
        "ctaPrimary":  '"Start building free"',
        "ctaSecondary":'"Watch demo"',
        "badge":       '"New feature"',
        "href":        '"#"',
        "src":         '"/placeholder-image.jpg"',
        "alt":         '"Descriptive alt text"',
        "message":     '"This is an alert message with important information."',
        "actionLabel": '"Take action"',
        "confirmLabel":'"Confirm"',
        "cancelLabel": '"Cancel"',
    }
    
    if pname in name_defaults:
        return name_defaults[pname]
    
    # By type
    if "boolean" in t:
        return "false"
    if "number" in t:
        return "0"
    if "string" in t:
        return f'"{pname}"'
    if "string[]" in t or "array" in t:
        return "[]"
    if "() =>" in t or "function" in t:
        return "() => {}"
    if "LucideIcon" in ptype:
        return "Star"
    if "ReactNode" in ptype or "React.ReactNode" in ptype:
        return 'null'
    
    return "undefined"


def generate_story_file(component_path: str, info: dict) -> str:
    """Generate a complete Storybook stories file."""
    name = info["name"]
    desc = info.get("description", f"{name} component")
    
    # Import icon if needed
    has_icon_prop = any("LucideIcon" in t for t in info["props"].values())
    icon_import   = "\nimport { Star, AlertCircle, Package } from 'lucide-react'" if has_icon_prop else ""
    
    # Build default args
    default_args = {}
    for pname, ptype in info["props"].items():
        if pname == "className":
            continue
        val = gen_prop_default(pname, ptype, name)
        if val not in ("undefined", "null", "[]", "() => {}"):
            default_args[pname] = val
    
    args_str = "\n    ".join(f"{k}: {v}," for k, v in default_args.items())
    
    # Build variant stories
    variant_stories = ""
    if info["variants"]:
        for v in info["variants"]:
            story_name = v.replace("-", " ").title().replace(" ", "")
            variant_stories += f"""
export const {story_name}: Story = {{
  args: {{
    ...Default.args,
    variant: '{v}',
  }},
}}
"""

    # Loading story
    loading_story = ""
    if info["has_loading"]:
        loading_story = f"""
export const Loading: Story = {{
  args: {{
    ...Default.args,
    loading: true,
  }},
  parameters: {{
    docs: {{ description: {{ story: 'Loading state — shows skeleton while data fetches.' }} }},
  }},
}}
"""

    # Error story
    error_story = ""
    if info["has_error"]:
        error_story = f"""
export const WithError: Story = {{
  args: {{
    ...Default.args,
    error: true,
  }},
  parameters: {{
    docs: {{ description: {{ story: 'Error state — shown when data fetch fails.' }} }},
  }},
}}
"""

    # Dark mode story
    dark_story = f"""
export const DarkMode: Story = {{
  args: {{ ...Default.args }},
  parameters: {{
    backgrounds: {{ default: 'dark' }},
  }},
  decorators: [
    (Story) => (
      <div className="dark" style={{{{ background: '#09090B', padding: '32px', minHeight: '200px' }}}}>
        <Story />
      </div>
    ),
  ],
}}
"""

    # Mobile viewport story
    mobile_story = f"""
export const Mobile: Story = {{
  args: {{ ...Default.args }},
  parameters: {{
    viewport: {{ defaultViewport: 'mobile1' }},
  }},
}}
"""

    ts = datetime.now().strftime("%Y-%m-%d")
    component_rel = component_path.replace("\\", "/")

    return f"""/**
 * {name} Stories — Generated by /storybook {ts}
 * Run: npx storybook dev
 */
import type {{ Meta, StoryObj }} from '@storybook/react'
import {{ {name} }} from './{Path(component_path).stem}'{icon_import}

type Story = StoryObj<typeof {name}>

const meta: Meta<typeof {name}> = {{
  title: 'Components/{name}',
  component: {name},
  parameters: {{
    layout: 'centered',
    docs: {{
      description: {{
        component: '{desc}',
      }},
    }},
  }},
  tags: ['autodocs'],
  argTypes: {{
{_build_arg_types(info['props'])}
  }},
}}

export default meta

// ── Default Story ─────────────────────────────────────────────────────
export const Default: Story = {{
  args: {{
    {args_str}
  }},
}}
{variant_stories}{loading_story}{error_story}{dark_story}{mobile_story}
// ── All Variants Overview ──────────────────────────────────────────────
{"export const AllVariants: Story = {" if info["variants"] else ""}
{"  render: () => (" if info["variants"] else ""}
{"    <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>" if info["variants"] else ""}
{chr(10).join(f"      <{name} {{...Default.args}} variant='{v}' />" for v in info["variants"]) if info["variants"] else ""}
{"    </div>" if info["variants"] else ""}
{"  )," if info["variants"] else ""}
{"}" if info["variants"] else ""}
"""


def _build_arg_types(props: dict) -> str:
    """Build argTypes configuration for Storybook controls."""
    lines = []
    for pname, ptype in props.items():
        if pname == "className":
            continue
        if "boolean" in ptype.lower():
            lines.append(f"    {pname}: {{ control: 'boolean' }},")
        elif "number" in ptype.lower():
            lines.append(f"    {pname}: {{ control: {{ type: 'number' }} }},")
        elif "string[]" in ptype.lower():
            lines.append(f"    {pname}: {{ control: 'object' }},")
        elif re.search(r"'[^']+'\s*\|", ptype):
            options = re.findall(r"'([^']+)'", ptype)
            opts_str = str(options).replace('"', "'")
            lines.append(f"    {pname}: {{ control: 'select', options: {opts_str} }},")
        elif "() =>" in ptype or "function" in ptype.lower():
            lines.append(f"    {pname}: {{ action: '{pname}' }},")
        elif "string" in ptype.lower():
            lines.append(f"    {pname}: {{ control: 'text' }},")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════
# STORYBOOK CONFIG GENERATOR
# ═══════════════════════════════════════════════════════════════════════

STORYBOOK_MAIN = '''import type { StorybookConfig } from '@storybook/nextjs'

const config: StorybookConfig = {
  stories: ['../src/**/*.stories.@(js|jsx|ts|tsx|mdx)'],
  addons: [
    '@storybook/addon-onboarding',
    '@storybook/addon-essentials',
    '@chromatic-com/storybook',
    '@storybook/addon-interactions',
    '@storybook/addon-a11y',
  ],
  framework: {
    name: '@storybook/nextjs',
    options: {},
  },
  staticDirs: ['../public'],
}

export default config
'''

STORYBOOK_PREVIEW = '''import type { Preview } from '@storybook/react'
import '../src/app/globals.css'  // Your design system tokens

const preview: Preview = {
  parameters: {
    controls:    { matchers: { color: /(background|color)$/i, date: /Date$/i } },
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#FFFFFF' },
        { name: 'dark',  value: '#09090B' },
        { name: 'surface', value: '#F9FAFB' },
      ],
    },
    viewport: {
      viewports: {
        mobile:  { name: 'Mobile',  styles: { width: '375px',  height: '812px' } },
        tablet:  { name: 'Tablet',  styles: { width: '768px',  height: '1024px' } },
        desktop: { name: 'Desktop', styles: { width: '1280px', height: '900px' } },
      },
    },
  },
}

export default preview
'''


def generate_storybook_config(root: Path):
    """Generate .storybook/main.ts and preview.ts."""
    sb_dir = root / ".storybook"
    sb_dir.mkdir(exist_ok=True)

    (sb_dir / "main.ts").write_text(STORYBOOK_MAIN)
    (sb_dir / "preview.ts").write_text(STORYBOOK_PREVIEW)

    print(f"  ✓ .storybook/main.ts")
    print(f"  ✓ .storybook/preview.ts")
    print(f"\n  Install Storybook:")
    print(f"  npx storybook@latest init")
    print(f"  npm install @storybook/addon-a11y")
    print(f"\n  Run Storybook:")
    print(f"  npx storybook dev")
    print()


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def process_component(filepath: str, out_dir: str = "") -> str | None:
    """Process a component file and generate its story."""
    path = Path(filepath)
    if not path.exists():
        print(f"  ⚠  Not found: {filepath}")
        return None

    code = path.read_text(errors="ignore")
    info = extract_component_info(code)

    if not info["name"]:
        print(f"  ⚠  No exported component found in {path.name}")
        return None

    story_code = generate_story_file(filepath, info)

    # Output path
    if out_dir:
        out_path = Path(out_dir) / f"{path.stem}.stories.tsx"
    else:
        out_path = path.parent / f"{path.stem}.stories.tsx"

    out_path.write_text(story_code)
    return str(out_path)


def main():
    parser = argparse.ArgumentParser(description="/storybook — Story Auto-Generator")
    parser.add_argument("file",    nargs="?", help="Component file to generate stories for")
    parser.add_argument("--all",   action="store_true", help="Generate stories for all components")
    parser.add_argument("--init",  action="store_true", help="Setup .storybook/ config files")
    parser.add_argument("--out",   default="",         help="Output directory for stories")
    parser.add_argument("--open",  action="store_true", help="Run storybook after generating")
    args = parser.parse_args()

    root = Path.cwd()

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║        /storybook — Story Auto-Generator            ║")
    print("╚══════════════════════════════════════════════════════╝\n")

    if args.init:
        generate_storybook_config(root)
        return

    if args.file:
        out = process_component(args.file, args.out)
        if out:
            code = Path(args.file).read_text(errors="ignore")
            info = extract_component_info(code)
            print(f"  ✓ Generated: {out}")
            print(f"  Component:  {info['name']}")
            print(f"  Props:      {', '.join(info['props'].keys())}")
            variants_found = info['variants'] or []
            extra_stories = (
                (["Loading"] if info["has_loading"] else []) +
                (["WithError"] if info["has_error"] else []) +
                (["DarkMode", "Mobile"]) +
                (["AllVariants"] if variants_found else [])
            )
            print(f"  Stories:    Default, {', '.join(extra_stories)}")
            if args.open:
                import subprocess
                subprocess.Popen(["npx", "storybook", "dev"], cwd=root)
            print()
        return

    if args.all:
        components_dir = root / "src" / "components"
        if not components_dir.exists():
            components_dir = root / "components"
        if not components_dir.exists():
            print("  ⚠  No components directory found. Create src/components/ first.\n")
            return

        generated = 0
        for tsx in components_dir.rglob("*.tsx"):
            # Skip existing stories and non-component files
            if ".stories." in tsx.name or tsx.name.startswith("_"):
                continue
            code = tsx.read_text(errors="ignore")
            if "export default function" not in code:
                continue
            out = process_component(str(tsx), args.out)
            if out:
                info = extract_component_info(code)
                print(f"  ✓ {info['name']:<25} → {Path(out).name}")
                generated += 1

        print(f"\n  Generated {generated} story files")
        print(f"  Run: npx storybook dev\n")
        return

    print("  Usage:")
    print("  python3 storybook.py src/components/PricingCard.tsx")
    print("  python3 storybook.py --all")
    print("  python3 storybook.py --init   (setup .storybook/)\n")


if __name__ == "__main__":
    main()
