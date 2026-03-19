#!/usr/bin/env python3
import re
"""
UI Design Intelligence — Core Data Engine v2.0
Palettes · Typography · Styles · UX Laws · Page Patterns · Library Catalog
All data is keyword-searchable. Used by design_system.py, search.py, detect_stack.py.
"""

# ═══════════════════════════════════════════════════════════════════════
# PALETTES — 40+ curated color systems
# ═══════════════════════════════════════════════════════════════════════
PALETTES = [
    {"name":"Midnight Indigo","vibe":"dark premium ai saas startup modern professional tech",
     "primary":"#6366F1","secondary":"#818CF8","cta":"#A78BFA","bg":"#09090B",
     "bg_dark":"#09090B","surface":"#18181B","surface_dark":"#18181B","text":"#FAFAFA",
     "muted":"#71717A","border":"#27272A","border_dark":"#27272A"},
    {"name":"Ocean Slate","vibe":"saas developer tool clean corporate b2b professional minimal modern",
     "primary":"#0EA5E9","secondary":"#38BDF8","cta":"#06B6D4","bg":"#F8FAFC",
     "bg_dark":"#0C1A2E","surface":"#FFFFFF","surface_dark":"#0F2849","text":"#0F172A",
     "muted":"#64748B","border":"#E2E8F0","border_dark":"#1E3A5F"},
    {"name":"Violet Storm","vibe":"dark ai ml neural startup bold dramatic gradient premium luxury",
     "primary":"#7C3AED","secondary":"#8B5CF6","cta":"#C084FC","bg":"#0A0010",
     "bg_dark":"#0A0010","surface":"#13002B","surface_dark":"#13002B","text":"#F5F3FF",
     "muted":"#A78BFA","border":"#2D1B69","border_dark":"#2D1B69"},
    {"name":"Warm Cream","vibe":"warm minimal editorial blog content lifestyle brand soft organic",
     "primary":"#92400E","secondary":"#B45309","cta":"#D97706","bg":"#FFFBF5",
     "bg_dark":"#1C1008","surface":"#FFFFFF","surface_dark":"#26180A","text":"#1C1917",
     "muted":"#78716C","border":"#E7E5E4","border_dark":"#44302A"},
    {"name":"Forest Sage","vibe":"organic sustainability wellness health eco green nature brand lifestyle",
     "primary":"#166534","secondary":"#15803D","cta":"#22C55E","bg":"#F0FDF4",
     "bg_dark":"#052E16","surface":"#FFFFFF","surface_dark":"#14532D","text":"#14532D",
     "muted":"#6B7280","border":"#DCFCE7","border_dark":"#166534"},
    {"name":"Rose Gold","vibe":"luxury beauty fashion premium feminine elegant brand cosmetic jewelry",
     "primary":"#9F1239","secondary":"#BE123C","cta":"#E11D48","bg":"#FFF1F2",
     "bg_dark":"#1C000A","surface":"#FFFFFF","surface_dark":"#3B0018","text":"#1C0010",
     "muted":"#9F9FA0","border":"#FFE4E6","border_dark":"#4C0020"},
    {"name":"Nordic Frost","vibe":"minimal clean scandinavian nordic white cool professional simple",
     "primary":"#1D4ED8","secondary":"#3B82F6","cta":"#2563EB","bg":"#F9FAFB",
     "bg_dark":"#0B1120","surface":"#FFFFFF","surface_dark":"#111827","text":"#111827",
     "muted":"#9CA3AF","border":"#E5E7EB","border_dark":"#1F2937"},
    {"name":"Cyber Neon","vibe":"gaming cyberpunk neon dark electric bold rgb edgy hacker tech",
     "primary":"#00FF88","secondary":"#00FFFF","cta":"#FF006E","bg":"#050505",
     "bg_dark":"#050505","surface":"#0D0D0D","surface_dark":"#0D0D0D","text":"#EEFFEE",
     "muted":"#44554F","border":"#1A2F25","border_dark":"#1A2F25"},
    {"name":"Sunset Coral","vibe":"consumer social media fun playful creative colorful app mobile",
     "primary":"#F97316","secondary":"#FB923C","cta":"#EF4444","bg":"#FFF7ED",
     "bg_dark":"#1A0A00","surface":"#FFFFFF","surface_dark":"#2A1400","text":"#1C0A00",
     "muted":"#78716C","border":"#FED7AA","border_dark":"#431407"},
    {"name":"Obsidian Gold","vibe":"luxury premium exclusive finance wealth investment gold dark elite",
     "primary":"#B45309","secondary":"#D97706","cta":"#F59E0B","bg":"#0A0800",
     "bg_dark":"#0A0800","surface":"#150F00","surface_dark":"#150F00","text":"#FEF9C3",
     "muted":"#78716C","border":"#292200","border_dark":"#292200"},
    {"name":"Electric Blue","vibe":"tech fintech blockchain crypto modern bold corporate enterprise",
     "primary":"#1E40AF","secondary":"#2563EB","cta":"#3B82F6","bg":"#F0F9FF",
     "bg_dark":"#020617","surface":"#FFFFFF","surface_dark":"#0C1A3E","text":"#0C1A3E",
     "muted":"#64748B","border":"#DBEAFE","border_dark":"#1E3A8A"},
    {"name":"Dark Emerald","vibe":"dark fintech data analytics security monitoring dashboard premium",
     "primary":"#059669","secondary":"#10B981","cta":"#34D399","bg":"#022C22",
     "bg_dark":"#022C22","surface":"#064E3B","surface_dark":"#064E3B","text":"#ECFDF5",
     "muted":"#6EE7B7","border":"#065F46","border_dark":"#065F46"},
    {"name":"Lavender Mist","vibe":"productivity wellness meditation mental health calm soft pastel b2c",
     "primary":"#7C3AED","secondary":"#8B5CF6","cta":"#6D28D9","bg":"#F5F3FF",
     "bg_dark":"#110628","surface":"#EDE9FE","surface_dark":"#1E0A4C","text":"#2E1065",
     "muted":"#A78BFA","border":"#DDD6FE","border_dark":"#3B0764"},
    {"name":"Carbon Zinc","vibe":"developer tool code ide terminal dark neutral professional clean",
     "primary":"#3F3F46","secondary":"#52525B","cta":"#6366F1","bg":"#09090B",
     "bg_dark":"#09090B","surface":"#18181B","surface_dark":"#18181B","text":"#E4E4E7",
     "muted":"#71717A","border":"#27272A","border_dark":"#27272A"},
    {"name":"Champagne Blanc","vibe":"luxury wedding event premium elegant white minimal high-end brand",
     "primary":"#78716C","secondary":"#A8A29E","cta":"#D4A847","bg":"#FAFAF9",
     "bg_dark":"#1C1917","surface":"#FFFFFF","surface_dark":"#292524","text":"#1C1917",
     "muted":"#A8A29E","border":"#F5F5F4","border_dark":"#3F3734"},
    {"name":"Deep Space","vibe":"dark space cosmos astronomy sci-fi futuristic exploration tech",
     "primary":"#312E81","secondary":"#4338CA","cta":"#818CF8","bg":"#030712",
     "bg_dark":"#030712","surface":"#0F172A","surface_dark":"#0F172A","text":"#F8FAFC",
     "muted":"#64748B","border":"#1E293B","border_dark":"#1E293B"},
    {"name":"Terra Cotta","vibe":"mediterranean earthy artisan craft food restaurant lifestyle warm",
     "primary":"#9A3412","secondary":"#C2410C","cta":"#EA580C","bg":"#FFF7ED",
     "bg_dark":"#1A0500","surface":"#FFFFFF","surface_dark":"#2D0A00","text":"#1C0A00",
     "muted":"#78716C","border":"#FED7AA","border_dark":"#43100C"},
    {"name":"Arctic White","vibe":"medical health clinical clean trust minimal white space saas",
     "primary":"#0369A1","secondary":"#0284C7","cta":"#0EA5E9","bg":"#FFFFFF",
     "bg_dark":"#0C1828","surface":"#F0F9FF","surface_dark":"#0F2B47","text":"#0C1828",
     "muted":"#94A3B8","border":"#E0F2FE","border_dark":"#1E3A5F"},
    {"name":"Plum Noir","vibe":"dark editorial magazine fashion luxury moody dramatic premium",
     "primary":"#6B21A8","secondary":"#7E22CE","cta":"#A855F7","bg":"#0D0010",
     "bg_dark":"#0D0010","surface":"#1A0022","surface_dark":"#1A0022","text":"#FAF5FF",
     "muted":"#C084FC","border":"#2D1448","border_dark":"#2D1448"},
    {"name":"Mint Fresh","vibe":"health fitness wellness app clean fresh modern d2c consumer",
     "primary":"#0D9488","secondary":"#14B8A6","cta":"#2DD4BF","bg":"#F0FDFA",
     "bg_dark":"#042F2E","surface":"#FFFFFF","surface_dark":"#134E4A","text":"#134E4A",
     "muted":"#6B7280","border":"#CCFBF1","border_dark":"#115E59"},
]

# ═══════════════════════════════════════════════════════════════════════
# TYPOGRAPHY — 25+ expert pairings
# ═══════════════════════════════════════════════════════════════════════
TYPOGRAPHY = [
    {"name":"Outfit + Inter","vibe":"modern clean saas tech startup professional minimal",
     "heading":"Outfit","body":"Inter","weights_h":"400,600,700,800","weights_b":"400,500",
     "url":"https://fonts.google.com/specimen/Outfit",
     "import":"@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Inter:wght@400;500&display=swap');"},
    {"name":"Plus Jakarta Sans + DM Sans","vibe":"modern bold premium saas startup product landing page",
     "heading":"Plus Jakarta Sans","body":"DM Sans","weights_h":"600,700,800","weights_b":"400,500",
     "url":"https://fonts.google.com/specimen/Plus+Jakarta+Sans",
     "import":"@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=DM+Sans:wght@400;500&display=swap');"},
    {"name":"Space Grotesk + Space Mono","vibe":"developer tool code technical mono dark terminal",
     "heading":"Space Grotesk","body":"Space Mono","weights_h":"400,500,700","weights_b":"400,700",
     "url":"https://fonts.google.com/specimen/Space+Grotesk",
     "import":"@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap');"},
    {"name":"Fraunces + DM Sans","vibe":"editorial luxury premium fashion magazine elegant serif dramatic",
     "heading":"Fraunces","body":"DM Sans","weights_h":"400,600,700,900","weights_b":"400,500",
     "url":"https://fonts.google.com/specimen/Fraunces",
     "import":"@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,400;0,600;0,900;1,400&family=DM+Sans:wght@400;500&display=swap');"},
    {"name":"Syne + Nunito","vibe":"creative agency bold playful unique geometric modern",
     "heading":"Syne","body":"Nunito","weights_h":"400,600,700,800","weights_b":"400,500,600",
     "url":"https://fonts.google.com/specimen/Syne",
     "import":"@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Nunito:wght@400;500;600&display=swap');"},
    {"name":"Clash Display + Switzer","vibe":"neobrutalism bold graphic design agency independent brand",
     "heading":"Clash Display","body":"Switzer","weights_h":"400,600,700","weights_b":"400,500",
     "url":"https://www.fontshare.com/fonts/clash-display",
     "import":"/* Fontshare */ @import url('https://api.fontshare.com/v2/css?f[]=clash-display@400,600,700&f[]=switzer@400,500&display=swap');"},
    {"name":"Geist + Geist Mono","vibe":"developer tool vercel modern dark monospace code terminal",
     "heading":"Geist","body":"Geist Mono","weights_h":"400,600,700","weights_b":"400,500",
     "url":"https://vercel.com/font",
     "import":"/* npm install geist */ import { GeistSans, GeistMono } from 'geist/font'"},
    {"name":"Manrope + Inter","vibe":"professional b2b enterprise clean trustworthy corporate saas",
     "heading":"Manrope","body":"Inter","weights_h":"500,600,700,800","weights_b":"400,500",
     "url":"https://fonts.google.com/specimen/Manrope",
     "import":"@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@400;500&display=swap');"},
    {"name":"Cabinet Grotesk + Satoshi","vibe":"premium brand startup modern geometric bold clean",
     "heading":"Cabinet Grotesk","body":"Satoshi","weights_h":"400,500,700,800","weights_b":"400,500",
     "url":"https://www.fontshare.com/fonts/cabinet-grotesk",
     "import":"@import url('https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@400,500,700,800&f[]=satoshi@400,500&display=swap');"},
    {"name":"Melodrama + General Sans","vibe":"editorial luxury fashion art creative serif display bold",
     "heading":"Melodrama","body":"General Sans","weights_h":"400,700","weights_b":"400,500",
     "url":"https://www.fontshare.com/fonts/melodrama",
     "import":"@import url('https://api.fontshare.com/v2/css?f[]=melodrama@400,700&f[]=general-sans@400,500&display=swap');"},
    {"name":"Bricolage Grotesque + Instrument Sans","vibe":"indie hacker product bold modern energetic unique",
     "heading":"Bricolage Grotesque","body":"Instrument Sans","weights_h":"400,600,700,800","weights_b":"400,500",
     "url":"https://fonts.google.com/specimen/Bricolage+Grotesque",
     "import":"@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;600;700;800&family=Instrument+Sans:wght@400;500&display=swap');"},
    {"name":"Lora + Source Sans 3","vibe":"blog content editorial news journalism reading clarity",
     "heading":"Lora","body":"Source Sans 3","weights_h":"400,600,700","weights_b":"400,600",
     "url":"https://fonts.google.com/specimen/Lora",
     "import":"@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700&family=Source+Sans+3:wght@400;600&display=swap');"},
    {"name":"Unbounded + Rajdhani","vibe":"gaming crypto web3 bold futuristic techno angular",
     "heading":"Unbounded","body":"Rajdhani","weights_h":"400,700,900","weights_b":"400,500,600",
     "url":"https://fonts.google.com/specimen/Unbounded",
     "import":"@import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@400;700;900&family=Rajdhani:wght@400;500;600&display=swap');"},
]

# ═══════════════════════════════════════════════════════════════════════
# STYLES — 30+ design aesthetic profiles with multi-library component picks
# ═══════════════════════════════════════════════════════════════════════
STYLES = [
    {"name":"Dark Aurora Premium",
     "vibe":"dark premium ai startup gradient aurora glow modern saas sophisticated",
     "bg_approach":"Deep near-black (#09090B) with aurora blur gradients as hero background",
     "effects":"aurora blur gradients, glassmorphism cards, glow borders, shimmer text",
     "anti_patterns":"bright backgrounds, flat design, heavy borders, solid fills",
     "react_bits":["Aurora","SpotlightCard","MagneticButton","ShinyText","BlurText"],
     "aceternity":["AuroraBackground","SparklesCore","BackgroundBeams","MovingBorder"],
     "magicui":["ShimmerButton","BorderBeam","GridPattern","MagicCard"],
     "shadcn":["Card","Badge","Dialog"],
     "primary_lib":"react_bits"},
    {"name":"Minimal SaaS Light",
     "vibe":"minimal clean light professional saas b2b tool dashboard modern crisp",
     "bg_approach":"Clean white (#FFFFFF) with subtle gray sections (#F9FAFB)",
     "effects":"subtle card shadows, clean hover transitions, smooth scroll",
     "anti_patterns":"animations everywhere, dark sections, heavy gradients",
     "react_bits":["FadeContent","ScrollVelocity","TiltedCard","CountUp"],
     "aceternity":[],
     "magicui":["NumberTicker","AnimatedSubscribeButton","MarqueeComponent"],
     "shadcn":["Card","Button","Badge","Table","Avatar"],
     "primary_lib":"shadcn"},
    {"name":"Neobrutalism",
     "vibe":"bold brutal graphic design independent brand indie unique offset border",
     "bg_approach":"Off-white or bright colored background, heavy black borders, offset shadows",
     "effects":"hard box shadows (4-8px offset), thick borders, bold hover states",
     "anti_patterns":"rounded corners, subtle shadows, gradients, glassmorphism",
     "react_bits":["MagneticButton","FadeContent"],
     "aceternity":[],
     "magicui":["RainbowButton","AnimatedBorderCard"],
     "shadcn":["Card","Button","Badge"],
     "primary_lib":"shadcn"},
    {"name":"Glassmorphism Dark",
     "vibe":"glass frost blur dark cards overlay transparent modern web3 premium",
     "bg_approach":"Dark gradient background, frosted glass cards (backdrop-blur + bg-white/10)",
     "effects":"backdrop-blur, semi-transparent cards, border-white/20, inner glow",
     "anti_patterns":"solid opaque cards, light backgrounds, heavy shadows",
     "react_bits":["Aurora","Particles","SpotlightCard","StarBorder"],
     "aceternity":["BackgroundBeams","SparklesCore"],
     "magicui":["MagicCard","ShineBorder","BorderBeam"],
     "shadcn":["Card"],
     "primary_lib":"react_bits"},
    {"name":"Editorial Serif",
     "vibe":"editorial luxury magazine fashion blog content elegant serif premium brand",
     "bg_approach":"Cream or white background, generous whitespace, large serif headlines",
     "effects":"text reveals, scroll-based animations, subtle hover underlines",
     "anti_patterns":"tech UI patterns, rounded cards, heavy gradients",
     "react_bits":["BlurText","TextReveal","FadeContent","ScrollVelocity"],
     "aceternity":["TextGenerateEffect","StickyScrollReveal"],
     "magicui":["WordFadeIn","GradualSpacing"],
     "shadcn":["Card","Separator"],
     "primary_lib":"react_bits"},
    {"name":"Gradient Mesh Aurora",
     "vibe":"colorful mesh gradient aurora creative agency vibrant rainbow modern",
     "bg_approach":"Mesh/aurora gradient backgrounds, organic color blobs, no hard edges",
     "effects":"mesh gradients, color orbs, blurred shapes, smooth animations",
     "anti_patterns":"solid backgrounds, sharp edges, monochrome",
     "react_bits":["Aurora","Orb","Silk","ShinyText","GradientText"],
     "aceternity":["AuroraBackground","ColourfulText"],
     "magicui":["Ripple","AnimatedBeam","SparklesText"],
     "shadcn":["Card"],
     "primary_lib":"react_bits"},
    {"name":"Gaming Cyber",
     "vibe":"gaming cyber esports neon dark electric rgb bold angular futuristic",
     "bg_approach":"True dark (#050505) with neon accents, scanline effects, angular elements",
     "effects":"neon glows, scanlines, angular clip-paths, RGB borders",
     "anti_patterns":"rounded everything, soft colors, clean minimal",
     "react_bits":["Ballpit","DotGrid","FuzzyText","GradientText","Crosshair"],
     "aceternity":["BackgroundBoxes","Vortex","Spotlight"],
     "magicui":["Particles","Confetti"],
     "shadcn":["Card","Badge"],
     "primary_lib":"aceternity"},
    {"name":"Corporate Clean",
     "vibe":"enterprise corporate b2b professional trustworthy clean dashboard finance",
     "bg_approach":"Clean white/light-gray, structured layouts, professional typography",
     "effects":"minimal: clean hover states, subtle shadows, smooth transitions",
     "anti_patterns":"decorative animations, flashy effects, dark mode, neon",
     "react_bits":["FadeContent","AnimatedList","CountUp"],
     "aceternity":[],
     "magicui":["NumberTicker","AnimatedBeam"],
     "shadcn":["Table","Card","Badge","Select","Dialog","Sidebar"],
     "primary_lib":"shadcn"},
    {"name":"Dark Developer Tool",
     "vibe":"developer tool ide code dark terminal cli technical mono geist",
     "bg_approach":"Zinc dark (#09090B) or GitHub dark, monospace accents, code aesthetic",
     "effects":"subtle highlights, clean transitions, focus states, terminal feel",
     "anti_patterns":"decorative backgrounds, serif fonts, colorful gradients",
     "react_bits":["DotGrid","FadeContent","AnimatedList","ScrollVelocity"],
     "aceternity":[],
     "magicui":["BorderBeam","AnimatedBorderCard","TypingAnimation"],
     "shadcn":["Card","Badge","Button","CodeBlock"],
     "primary_lib":"shadcn"},
    {"name":"Luxury Premium Dark",
     "vibe":"luxury premium exclusive high-end brand gold dark elite sophisticated",
     "bg_approach":"Near-black backgrounds, gold/amber accents, high contrast, full-bleed imagery",
     "effects":"smooth reveals, gold shimmer, editorial typography moments",
     "anti_patterns":"playful, colorful, crowded, rounded corners everywhere",
     "react_bits":["BlurText","TextReveal","TiltedCard","ShinyText"],
     "aceternity":["HeroParallax","MacbookScroll","CardStack"],
     "magicui":["WordFadeIn","BorderBeam"],
     "shadcn":["Card","Avatar"],
     "primary_lib":"aceternity"},
    {"name":"Warm Minimal",
     "vibe":"warm organic lifestyle wellness brand consumer d2c cream off-white",
     "bg_approach":"Cream/off-white backgrounds, warm typography, organic shapes",
     "effects":"gentle fade-ins, warm hover states, subtle texture",
     "anti_patterns":"cold blues, stark white, heavy tech patterns",
     "react_bits":["FadeContent","BounceCards","Silk"],
     "aceternity":[],
     "magicui":["WordPullUp","FadeText"],
     "shadcn":["Card","Button","Avatar"],
     "primary_lib":"shadcn"},
    {"name":"3D Immersive",
     "vibe":"3d immersive three.js webgl interactive creative agency portfolio",
     "bg_approach":"Dark background with 3D elements, WebGL canvas, interactive depth",
     "effects":"3D card tilts, parallax depth, perspective transforms, canvas animations",
     "anti_patterns":"flat 2D only, no interaction, minimal",
     "react_bits":["TiltedCard","Ballpit","Balatro"],
     "aceternity":["ThreeDCardEffect","HeroParallax","MacbookScroll","WorldMap"],
     "magicui":["OrbitingCircles","AnimatedBeam"],
     "shadcn":["Card"],
     "primary_lib":"aceternity"},
    {"name":"Y2K Revival",
     "vibe":"y2k retro 2000s holographic chrome iridescent social media myspace early internet maximalist fun",
     "bg_approach":"Deep near-black with violet undertone (#0A0014). Chrome text, star decorations, scanlines.",
     "effects":"chrome/holographic gradients, iridescent card borders, scanline overlay, star sparkle decorations, neon glow",
     "anti_patterns":"minimal design, flat cards, single color, no motion, corporate clean",
     "react_bits":["FuzzyText","GradientText","Particles","TiltedCard","BounceCards","StarBorder"],
     "aceternity":["BackgroundBoxes","Vortex","ShootingStars","Spotlight","MovingBorder"],
     "magicui":["NeonGradientCard","ShineBorder","RetroGrid","SparklesText","RainbowButton","HyperText"],
     "shadcn":["Card","Badge"],
     "kiboui":["ColorPicker"],
     "originui":["Tags input"],
     "primary_lib":"magicui"},
    {"name":"Bento Grid Dashboard",
     "vibe":"bento grid modern saas dashboard product overview asymmetric masonry feature showcase",
     "bg_approach":"Clean white or subtle off-white, bento grid layout with varied card sizes",
     "effects":"card hover elevation, animated counters, subtle border highlights, smooth transitions",
     "anti_patterns":"uniform card grid, no size variation, heavy animations, dark backgrounds",
     "react_bits":["FadeContent","CountUp","AnimatedList","ScrollVelocity"],
     "aceternity":["LayoutGrid","FocusCards","HeroHighlight"],
     "magicui":["BentoGrid","NumberTicker","AnimatedBeam","BorderBeam","MagicCard"],
     "shadcn":["Card","Badge","Tabs","Progress"],
     "primary_lib":"magicui"},
    {"name":"Social Media Dark",
     "vibe":"social media platform community dark vibrant colorful energetic people connections friends",
     "bg_approach":"Dark (#0A0014 or #050510) with vibrant accent palette. Glassmorphism cards.",
     "effects":"gradient avatars, color-coded UI, vibrant glow on interactions, fluid animations",
     "anti_patterns":"corporate look, subdued colors, heavy text, minimal design",
     "react_bits":["BounceCards","AnimatedList","SpotlightCard","CountUp","MagneticButton"],
     "aceternity":["AnimatedTooltip","CardStack","FloatingNavbar","FlipWords"],
     "magicui":["MarqueeComponent","NumberTicker","OrbitingCircles","AnimatedGradientText"],
     "shadcn":["Avatar","Badge","Card","Sheet"],
     "primary_lib":"react_bits"},
    {"name":"Vaporwave Retro",
     "vibe":"vaporwave synthwave retro 80s 90s purple pink sunset aesthetic nostalgia lo-fi",
     "bg_approach":"Dark purple/navy bg (#0D0221). Sunset gradient overlays, grid lines, chrome text.",
     "effects":"retro grid perspective, scanlines, sunset gradients, neon pink/cyan palette, pixel fonts",
     "anti_patterns":"modern minimal, flat design, corporate colors, clean whitespace",
     "react_bits":["GradientText","Balatro","DotGrid","ShinyText","FuzzyText"],
     "aceternity":["BackgroundGradientAnimation","Vortex","ShootingStars"],
     "magicui":["RetroGrid","FlickeringGrid","NeonGradientCard","SparklesText"],
     "shadcn":["Card","Badge"],
     "primary_lib":"magicui"},
    {"name":"Editorial Dark Premium",
     "vibe":"dark editorial magazine luxury premium fashion publishing culture art cinema dramatic",
     "bg_approach":"True dark (#0A0A0A), generous whitespace, oversized type, minimal decoration",
     "effects":"slow text reveals, full-bleed imagery, editorial typography, restrained animations",
     "anti_patterns":"SaaS patterns, rounded cards everywhere, tech UI elements, icon grids",
     "react_bits":["TextReveal","BlurText","ScrollVelocity","TiltedCard"],
     "aceternity":["HeroParallax","StickyScrollReveal","LampEffect","TextGenerateEffect"],
     "magicui":["WordFadeIn","AnimatedGradientText","BoxReveal"],
     "shadcn":["Card","Separator","Avatar"],
     "primary_lib":"aceternity"},
    {"name":"Fintech Trustworthy",
     "vibe":"fintech banking finance money trust professional secure institutional data",
     "bg_approach":"Navy/deep blue with white content areas. Trust-signals prominent.",
     "effects":"animated numbers, subtle data animations, clean charts, confidence-building UI",
     "anti_patterns":"playful colors, heavy animations, informal tone, rounded-everything",
     "react_bits":["CountUp","FadeContent","AnimatedList"],
     "aceternity":["FloatingNavbar","StickyScrollReveal"],
     "magicui":["NumberTicker","AnimatedBeam","BentoGrid","GridPattern"],
     "shadcn":["Table","Card","Badge","Tabs","Progress"],
     "kiboui":["DateRangePicker","MultiSelect","Kanban"],
     "originui":["Input with icon prefix","Combo input"],
     "primary_lib":"shadcn"},
    {"name":"Crypto Web3",
     "vibe":"crypto blockchain web3 defi nft decentralized bold digital token protocol",
     "bg_approach":"True dark (#030712), gradient accents, geometric patterns, technical aesthetic",
     "effects":"animated statistics, connection lines, matrix-like effects, holographic elements",
     "anti_patterns":"warm colors, serif fonts, editorial feel, corporate look",
     "react_bits":["Ballpit","Particles","FuzzyText","GradientText","LetterGlitch"],
     "aceternity":["GoogleGeminiEffect","BackgroundBeamsWithCollision","Vortex","Spotlight"],
     "magicui":["OrbitingCircles","AnimatedBeam","NumberTicker","HyperText","ShimmerButton"],
     "shadcn":["Card","Badge","Progress"],
     "primary_lib":"aceternity"},
    {"name":"E-commerce Product",
     "vibe":"ecommerce shop product catalog retail consumer buy sell checkout cart clean",
     "bg_approach":"Clean white with subtle gray/warm tones. Product photography as hero.",
     "effects":"smooth hover zoom, product carousels, add-to-cart animations, wishlist effects",
     "anti_patterns":"dark mode, heavy gradients, tech patterns, developer aesthetic",
     "react_bits":["FadeContent","BounceCards","TiltedCard","ScrollVelocity"],
     "aceternity":["HeroParallax","FocusCards","ExpandingCard"],
     "magicui":["MarqueeComponent","MagicCard","NumberTicker","InteractiveHoverButton"],
     "shadcn":["Card","Badge","Button","Avatar","Sheet"],
     "primary_lib":"react_bits"},
    {"name":"Health Wellness",
     "vibe":"health wellness fitness mental physical calm mindful clean fresh air green lifestyle",
     "bg_approach":"Soft white/cream or muted green. Organic shapes, spacious layouts.",
     "effects":"gentle breathing animations, smooth transitions, nature-inspired motion",
     "anti_patterns":"aggressive colors, bold typography, dark mode, heavy animation",
     "react_bits":["FadeContent","Silk","BlurText","CountUp"],
     "aceternity":["WavyBackground","AuroraBackground"],
     "magicui":["WordPullUp","WordFadeIn","AnimatedSubscribeButton","NumberTicker"],
     "shadcn":["Card","Progress","Avatar","Badge"],
     "kiboui":["DateRangePicker","Timeline"],
     "primary_lib":"shadcn"},
    {"name":"Portfolio Creative",
     "vibe":"portfolio creative designer developer agency personal brand showcase work project",
     "bg_approach":"Flexible: dark or light. Bold typographic moments. Cinematic reveals.",
     "effects":"image trails, magnetic buttons, smooth page transitions, cursor effects",
     "anti_patterns":"generic SaaS layout, uniform card grids, invisible typography",
     "react_bits":["ImageTrail","FlowingMenu","TiltedCard","FuzzyText","PixelTransition","BounceCards"],
     "aceternity":["HeroParallax","MacbookScroll","CardStack","LampEffect"],
     "magicui":["Dock","OrbitingCircles","BoxReveal","SparklesText"],
     "shadcn":["Card","Avatar","Badge"],
     "primary_lib":"react_bits"},
    {"name":"SaaS Pricing Page",
     "vibe":"pricing tier plans saas subscription freemium pro enterprise conversion CTA",
     "bg_approach":"Clean white with single gradient section for the popular plan.",
     "effects":"toggle animation (monthly/annual), plan highlight elevation, feature tick-in",
     "anti_patterns":"equal visual weight on all tiers, no recommended plan highlight",
     "react_bits":["StarBorder","FadeContent","CountUp"],
     "aceternity":["MovingBorder","CardSpotlight"],
     "magicui":["NumberTicker","ShimmerButton","BorderBeam","BentoGrid"],
     "shadcn":["Card","Badge","Switch","Accordion"],
     "primary_lib":"magicui"},
    {"name":"Auth Split Screen",
     "vibe":"login signup auth registration split screen form clean minimal secure",
     "bg_approach":"Split 50/50: brand left, form right. Framer for subtle left-side animation.",
     "effects":"form field focus animations, subtle brand animation, password strength meter",
     "anti_patterns":"full-page forms, no visual brand presence, basic styling",
     "react_bits":["Silk","BlurText","FadeContent"],
     "aceternity":["LampEffect","AuroraBackground"],
     "magicui":["GridPattern","WordFadeIn","AnimatedSubscribeButton"],
     "shadcn":["Form","Input","Button","Card","Separator"],
     "originui":["Input with show/hide toggle","OTP Input","Social buttons"],
     "primary_lib":"shadcn"},
]

# ═══════════════════════════════════════════════════════════════════════
# LIBRARY CATALOG — Multi-library component selection intelligence
# ═══════════════════════════════════════════════════════════════════════
LIBRARY_CATALOG = {
    "react-bits": {
        "name": "React Bits",
        "url": "https://reactbits.dev",
        "install_method": "npx shadcn@latest add",
        "base_install_url": "https://reactbits.dev/r/",
        "requires": ["tailwindcss"],
        "optional": ["framer-motion"],
        "best_for": ["hero-backgrounds","text-animations","scroll-effects","interactive-cards","cursors"],
        "style_fit": ["Dark Aurora Premium","Glassmorphism Dark","Gradient Mesh Aurora","Editorial Serif"],
        "components": {
            "backgrounds": [
                {"name":"Aurora","desc":"Multi-hue animated aurora blur gradient — signature dark hero bg","dark_only":True,"wow_factor":10},
                {"name":"Particles","desc":"Interactive floating particle field, connects on hover","wow_factor":8},
                {"name":"Silk","desc":"Flowing silk fluid simulation, dark or light","wow_factor":9},
                {"name":"Orb","desc":"Glowing color orb, subtle ambient background element","wow_factor":7},
                {"name":"Ripple","desc":"Expanding concentric rings from center point","wow_factor":7},
                {"name":"DotGrid","desc":"Animated dot matrix grid, technical aesthetic","wow_factor":6},
                {"name":"Ballpit","desc":"Physics-based bouncing balls, playful/fun","wow_factor":8},
                {"name":"Balatro","desc":"Card swirl shader background, gaming/bold aesthetic","wow_factor":9},
                {"name":"LetterGlitch","desc":"Glitch text effect for names or words","wow_factor":8},
            ],
            "text": [
                {"name":"SplitText","desc":"Splits headline into chars/words for staggered entrance","wow_factor":9},
                {"name":"BlurText","desc":"Words reveal blur→sharp, cinematic quality","wow_factor":9},
                {"name":"ShinyText","desc":"Moving light shimmer across muted text","wow_factor":7},
                {"name":"GradientText","desc":"Animated gradient color sweep across text","wow_factor":8},
                {"name":"FuzzyText","desc":"Glitch/fuzzy distortion on hover","wow_factor":8},
                {"name":"CircularText","desc":"Text arranged in circle, optionally rotating","wow_factor":7},
                {"name":"CountUp","desc":"Number animates from 0 to target on enter","wow_factor":8},
                {"name":"TextReveal","desc":"Words revealed progressively on scroll","wow_factor":8},
                {"name":"PixelTransition","desc":"Pixel-dissolve between two states","wow_factor":9},
                {"name":"TrueFocus","desc":"Focus ring animates between words on hover","wow_factor":7},
            ],
            "cards": [
                {"name":"SpotlightCard","desc":"Mouse-following spotlight glow on card surface","wow_factor":9},
                {"name":"TiltedCard","desc":"3D perspective tilt tracking mouse position","wow_factor":8},
                {"name":"BounceCards","desc":"Cards with spring bounce collision physics","wow_factor":9},
                {"name":"ScrollStack","desc":"Stacked cards that expand/stick on scroll","wow_factor":9},
                {"name":"StackedCards","desc":"Fan-out card stack on hover","wow_factor":8},
            ],
            "buttons": [
                {"name":"MagneticButton","desc":"Button pulled magnetically toward cursor","wow_factor":9},
                {"name":"StarBorder","desc":"Animated rotating star/shimmer border","wow_factor":8},
            ],
            "navigation": [
                {"name":"FlowingMenu","desc":"Full-screen menu with flowing image-on-hover animation","wow_factor":10},
                {"name":"DockExpandable","desc":"macOS-style dock that expands on hover","wow_factor":8},
            ],
            "effects": [
                {"name":"FadeContent","desc":"Clean fade+slide entrance triggered by scroll","wow_factor":6},
                {"name":"ScrollVelocity","desc":"Marquee text whose speed matches scroll velocity","wow_factor":8},
                {"name":"InfiniteScroll","desc":"Seamlessly looping horizontal/vertical list","wow_factor":7},
                {"name":"AnimatedList","desc":"Staggered list item entrance animations","wow_factor":7},
                {"name":"ImageTrail","desc":"Images follow cursor in a trail effect","wow_factor":10},
                {"name":"Crosshair","desc":"Custom crosshair cursor with accent color","wow_factor":7},
                {"name":"Spotlight","desc":"Mouse-following spotlight that illuminates content","wow_factor":8},
            ],
        }
    },
    "aceternity": {
        "name": "Aceternity UI",
        "url": "https://ui.aceternity.com/components",
        "install_method": "copy",
        "base_install_url": "https://ui.aceternity.com/components/",
        "requires": ["tailwindcss","framer-motion","clsx","tailwind-merge"],
        "optional": ["three","@react-three/fiber"],
        "best_for": ["hero-sections","dark-premium","3d-effects","unique-text","spotlight-effects"],
        "style_fit": ["Dark Aurora Premium","Gaming Cyber","3D Immersive","Luxury Premium Dark"],
        "components": {
            "backgrounds": [
                {"name":"AuroraBackground","desc":"Conic gradient aurora with animated CSS vars","wow_factor":8},
                {"name":"BackgroundBeams","desc":"Converging beam lines to a focal point","wow_factor":9},
                {"name":"BackgroundBeamsWithCollision","desc":"Beams that collide and explode","wow_factor":10},
                {"name":"BackgroundGradientAnimation","desc":"Slow morphing mesh gradient","wow_factor":8},
                {"name":"WavyBackground","desc":"SVG wavy animated background lines","wow_factor":7},
                {"name":"Vortex","desc":"Spiraling particle vortex canvas animation","wow_factor":9},
                {"name":"BackgroundBoxes","desc":"Grid of colored boxes with wave animation","wow_factor":8},
                {"name":"ShootingStars","desc":"Animated shooting stars across dark sky","wow_factor":8},
                {"name":"Meteors","desc":"Diagonal meteor shower CSS animation","wow_factor":8},
            ],
            "hero": [
                {"name":"Spotlight","desc":"Large cursor spotlight that follows mouse on dark bg","wow_factor":9},
                {"name":"LampEffect","desc":"Overhead lamp-style conic light on dark surface","wow_factor":10},
                {"name":"HeroParallax","desc":"Grid of product images that parallax on scroll","wow_factor":10},
                {"name":"GoogleGeminiEffect","desc":"Gemini-inspired animated beam logo effect","wow_factor":10},
                {"name":"MacbookScroll","desc":"MacBook scrolls open to reveal your app screenshot","wow_factor":10},
                {"name":"ColourfulText","desc":"Each word cycles through colours on hover","wow_factor":8},
            ],
            "cards": [
                {"name":"CardStack","desc":"Stacked cards with automated cycling","wow_factor":8},
                {"name":"CardSpotlight","desc":"Radial spotlight follows mouse over card","wow_factor":9},
                {"name":"ThreeDCardEffect","desc":"True 3D perspective tilt with inner layers","wow_factor":9},
                {"name":"FocusCards","desc":"Grid that blurs non-focused cards on hover","wow_factor":9},
                {"name":"LayoutGrid","desc":"Masonry-style animated grid","wow_factor":8},
                {"name":"ExpandingCard","desc":"Card expands to reveal detail on click","wow_factor":8},
                {"name":"TextRevealCard","desc":"Hover reveals hidden text on a card","wow_factor":9},
                {"name":"MovingBorder","desc":"Animated border that travels around card edges","wow_factor":9},
            ],
            "text": [
                {"name":"TextGenerateEffect","desc":"Words appear one by one with opacity + blur","wow_factor":9},
                {"name":"TypewriterEffect","desc":"Typewriter with cursor blinking","wow_factor":7},
                {"name":"FlipWords","desc":"Words flip/rotate to the next value in a list","wow_factor":8},
                {"name":"HeroHighlight","desc":"Highlight underline animates into view on hero text","wow_factor":8},
                {"name":"NumberTicker","desc":"Large number counts up on scroll enter","wow_factor":7},
                {"name":"AnimatedTooltip","desc":"Avatar stack with animated name tooltip on hover","wow_factor":8},
            ],
            "navigation": [
                {"name":"FloatingNavbar","desc":"Nav that appears/hides based on scroll direction","wow_factor":9},
                {"name":"StickyScrollReveal","desc":"Sidebar nav highlights as content sections scroll","wow_factor":9},
                {"name":"MultiStepLoader","desc":"Cinematic multi-step loading sequence","wow_factor":8},
            ],
        }
    },
    "magicui": {
        "name": "Magic UI",
        "url": "https://magicui.design",
        "install_method": "npx magicui-cli@latest add",
        "base_install_url": "https://magicui.design/docs/components/",
        "requires": ["tailwindcss","framer-motion"],
        "optional": [],
        "best_for": ["saas-buttons","number-animations","border-effects","marquee","bento-grid"],
        "style_fit": ["Minimal SaaS Light","Dark Aurora Premium","Dark Developer Tool","Corporate Clean"],
        "components": {
            "buttons": [
                {"name":"ShimmerButton","desc":"Dark button with moving shimmer highlight — premium CTA","wow_factor":9},
                {"name":"RainbowButton","desc":"Animated rainbow border on black button","wow_factor":9},
                {"name":"InteractiveHoverButton","desc":"Arrow slides in from left on hover","wow_factor":8},
                {"name":"PulsatingButton","desc":"Pulsing ring radiates from button","wow_factor":7},
                {"name":"AnimatedSubscribeButton","desc":"Subscribe CTA that animates to confirmed state","wow_factor":8},
                {"name":"CoolMode","desc":"Confetti/particle burst on button click","wow_factor":9},
            ],
            "text": [
                {"name":"TypingAnimation","desc":"Typewriter with configurable typing speed","wow_factor":7},
                {"name":"WordPullUp","desc":"Words pull up into place with spring physics","wow_factor":8},
                {"name":"WordFadeIn","desc":"Words fade in staggered from left","wow_factor":7},
                {"name":"GradualSpacing","desc":"Letters spread apart gradually on mount","wow_factor":8},
                {"name":"SparklesText","desc":"Stars/sparkles animate around highlighted text","wow_factor":9},
                {"name":"NumberTicker","desc":"Large stat number counts up on viewport enter","wow_factor":8},
                {"name":"AnimatedGradientText","desc":"Gradient sweeps across text continuously","wow_factor":8},
                {"name":"HyperText","desc":"Scrambled-letters-resolve animation (Matrix style)","wow_factor":9},
                {"name":"BoxReveal","desc":"Box wipes across to reveal text","wow_factor":8},
            ],
            "backgrounds": [
                {"name":"GridPattern","desc":"Subtle grid lines as section/hero bg","wow_factor":6},
                {"name":"DotPattern","desc":"Dot matrix background pattern","wow_factor":6},
                {"name":"AnimatedGridPattern","desc":"Grid pattern with animated highlighted cells","wow_factor":8},
                {"name":"Ripple","desc":"Expanding concentric circles from center","wow_factor":7},
                {"name":"Particles","desc":"Canvas particle system, interactive","wow_factor":8},
                {"name":"Confetti","desc":"Confetti burst on trigger — celebration state","wow_factor":8},
                {"name":"Meteors","desc":"Diagonal meteor CSS animation","wow_factor":7},
                {"name":"FlickeringGrid","desc":"Grid of cells that flicker on and off","wow_factor":8},
                {"name":"RetroGrid","desc":"Vanishing point perspective grid (80s aesthetic)","wow_factor":9},
            ],
            "borders": [
                {"name":"BorderBeam","desc":"Beam of light travels around component border","wow_factor":9},
                {"name":"AnimatedBeam","desc":"Beam travels along an SVG path between elements","wow_factor":10},
                {"name":"ShineBorder","desc":"Metallic shine sweeps around border","wow_factor":8},
                {"name":"MagicCard","desc":"Card with radial glow following mouse","wow_factor":9},
                {"name":"NeonGradientCard","desc":"Neon animated gradient border card","wow_factor":9},
            ],
            "layout": [
                {"name":"BentoGrid","desc":"Responsive bento-box grid layout","wow_factor":8},
                {"name":"MarqueeComponent","desc":"Infinite horizontal or vertical marquee — logo strips","wow_factor":7},
                {"name":"OrbitingCircles","desc":"Icons orbit a central element","wow_factor":9},
                {"name":"AnimatedList","desc":"Items enter staggered from below","wow_factor":7},
                {"name":"Dock","desc":"macOS dock with icon magnification","wow_factor":8},
            ],
        }
    },
    "originui": {
        "name": "Origin UI",
        "url": "https://originui.com",
        "install_method": "copy",
        "requires": ["tailwindcss","react-hook-form","zod"],
        "best_for": ["production-forms","advanced-inputs","professional-ui"],
        "style_fit": ["Corporate Clean","Minimal SaaS Light","Dark Developer Tool"],
        "components": {
            "inputs": [
                {"name":"Input with label inline","desc":"Floating label inside input","wow_factor":6},
                {"name":"Input with icon prefix","desc":"Icon inside left of input","wow_factor":6},
                {"name":"Input with show/hide toggle","desc":"Password with eye toggle","wow_factor":7},
                {"name":"Input with character count","desc":"Character counter below input","wow_factor":6},
                {"name":"OTP Input","desc":"Six-box OTP code input with auto-advance","wow_factor":8},
                {"name":"Phone input","desc":"Country flag prefix + formatted phone","wow_factor":7},
                {"name":"Combo input","desc":"Combined select+input for complex filters","wow_factor":7},
                {"name":"Tags input","desc":"Multi-tag input with removable chips","wow_factor":8},
            ],
            "buttons": [
                {"name":"Button loading state","desc":"Spinner replaces icon on click","wow_factor":7},
                {"name":"Split button","desc":"Primary action + dropdown arrow split","wow_factor":7},
                {"name":"Social buttons","desc":"Google/GitHub OAuth style buttons","wow_factor":7},
            ],
        }
    },
    "shadcn": {
        "name": "shadcn/ui",
        "url": "https://ui.shadcn.com",
        "install_method": "npx shadcn@latest add",
        "base_install_url": "",
        "requires": ["tailwindcss","radix-ui"],
        "best_for": ["accessible-components","forms","dialogs","navigation","tables","dashboards"],
        "style_fit": ["Minimal SaaS Light","Corporate Clean","Dark Developer Tool","Warm Minimal"],
        "components": {
            "core": ["Button","Input","Card","Badge","Avatar","Separator","Skeleton"],
            "overlay": ["Dialog","Sheet","Drawer","Popover","Tooltip","AlertDialog","HoverCard"],
            "forms": ["Form","Select","Checkbox","RadioGroup","Switch","Textarea","Slider","DatePicker"],
            "navigation": ["NavigationMenu","Breadcrumb","Tabs","Sidebar","Menubar","DropdownMenu"],
            "data": ["Table","DataTable","Accordion","Collapsible","Command","Combobox"],
            "feedback": ["Toast","Alert","Progress","Sonner"],
        }
    },
    "kiboui": {
        "name": "Kibo UI",
        "url": "https://www.kiboui.com",
        "install_method": "npx kiui@latest add",
        "requires": ["tailwindcss","shadcn/ui"],
        "best_for": ["enhanced-shadcn","advanced-select","date-range","multi-select","kanban"],
        "style_fit": ["Minimal SaaS Light","Corporate Clean","Dark Developer Tool"],
        "components": {
            "enhanced": [
                {"name":"MultiSelect","desc":"Shadcn select with checkboxes and search","wow_factor":7},
                {"name":"DateRangePicker","desc":"Two-calendar date range selector","wow_factor":8},
                {"name":"TagInput","desc":"Tagging input with autocomplete","wow_factor":7},
                {"name":"RichTextEditor","desc":"WYSIWYG editor component","wow_factor":7},
                {"name":"Kanban","desc":"Drag-and-drop kanban board","wow_factor":9},
                {"name":"Timeline","desc":"Vertical timeline with icons","wow_factor":7},
                {"name":"FileUpload","desc":"Drag-and-drop file upload zone","wow_factor":8},
                {"name":"ColorPicker","desc":"Hue/saturation/value color picker","wow_factor":7},
            ]
        }
    },
    "flowbite": {
        "name": "Flowbite",
        "url": "https://flowbite.com",
        "install_method": "npm install flowbite-react",
        "requires": ["tailwindcss"],
        "best_for": ["dashboards","navigation","tables","forms","admin-panels","vue-projects"],
        "style_fit": ["Corporate Clean","Minimal SaaS Light"],
        "components": {
            "layout": ["Navbar","Sidebar","Footer","Breadcrumb","Tabs"],
            "data": ["Table","Pagination","Badge","Timeline"],
            "forms": ["Select","Checkbox","Toggle","FileInput","Datepicker","RangeSlider"],
            "overlay": ["Modal","Drawer","Dropdown","Tooltip","Popover"],
            "feedback": ["Alert","Toast","Progress","Spinner"],
        }
    },
    "mvpblocks": {
        "name": "MVPBlocks",
        "url": "https://www.mvpblocks.app",
        "install_method": "copy",
        "requires": ["tailwindcss","shadcn/ui"],
        "best_for": ["full-section-blocks","rapid-mvp","landing-pages","complete-layouts"],
        "style_fit": ["Minimal SaaS Light","Dark Aurora Premium"],
        "components": {
            "sections": [
                {"name":"Hero Block","desc":"Complete hero with headline, CTA, screenshot","wow_factor":8},
                {"name":"Feature Grid","desc":"3-column features with icons","wow_factor":7},
                {"name":"Testimonials","desc":"Avatar + quote testimonial grid","wow_factor":7},
                {"name":"Pricing","desc":"3-tier pricing with monthly/annual toggle","wow_factor":8},
                {"name":"CTA Section","desc":"Full-width CTA with gradient bg","wow_factor":7},
                {"name":"Stats Row","desc":"4-stat metrics row with counters","wow_factor":7},
                {"name":"Logo Strip","desc":"Logo marquee for social proof","wow_factor":6},
                {"name":"FAQ Accordion","desc":"Expandable FAQ section","wow_factor":6},
            ]
        }
    },
    "stunning-ui": {
        "name": "Stunning UI",
        "url": "https://stunning-ui.com",
        "install_method": "copy",
        "requires": ["vue","tailwindcss"],
        "best_for": ["vue-animations","nuxt-components","vue-interactive"],
        "style_fit": ["Dark Aurora Premium","Glassmorphism Dark","Gradient Mesh Aurora"],
        "components": {
            "vue": [
                {"name":"AnimatedGradient","desc":"Vue animated gradient background","wow_factor":8},
                {"name":"MagneticButton","desc":"Vue magnetic cursor button","wow_factor":9},
                {"name":"GlowCard","desc":"Vue card with glow hover effect","wow_factor":8},
                {"name":"TextScramble","desc":"Vue text scramble/glitch animation","wow_factor":8},
                {"name":"StaggerList","desc":"Vue staggered list entrance","wow_factor":7},
            ]
        }
    },
    "chakra": {
        "name": "Chakra UI",
        "url": "https://chakra-ui.com",
        "install_method": "npm install @chakra-ui/react",
        "requires": ["react"],
        "best_for": ["theming","semantic-tokens","accessible","consumer-apps"],
        "style_fit": ["Minimal SaaS Light","Warm Minimal","Lavender"],
        "components": {
            "core": ["Box","Flex","Grid","Stack","Button","Input","Text","Heading","Icon","Image","Badge","Avatar"],
            "overlay": ["Modal","Drawer","Popover","Tooltip","Alert","Toast"],
            "forms": ["FormControl","FormLabel","FormErrorMessage","Select","Checkbox","Switch","Slider"],
            "disclosure": ["Accordion","Tabs","Collapse"],
        }
    },
    "nextui": {
        "name": "NextUI / HeroUI",
        "url": "https://nextui.org",
        "install_method": "npm install @nextui-org/react",
        "requires": ["react","tailwindcss","framer-motion"],
        "best_for": ["clean-components","good-defaults","react-accessible"],
        "style_fit": ["Minimal SaaS Light","Nordic Frost","Corporate Clean"],
        "components": {
            "core": ["Button","Chip","Avatar","Badge","Card","Image","Divider","Skeleton"],
            "forms": ["Input","Select","Checkbox","Switch","Slider","Autocomplete","DatePicker","DateRangePicker"],
            "overlay": ["Modal","Drawer","Popover","Tooltip","Dropdown"],
            "navigation": ["Navbar","Tabs","Breadcrumbs","Pagination","Link"],
            "data": ["Table","Accordion","Progress","CircularProgress","Spinner"],
        }
    },
    "skiper": {
        "name": "Skiper UI",
        "url": "https://skiper-ui.com",
        "install_method": "copy",
        "requires": ["tailwindcss","framer-motion"],
        "best_for": ["bold-design","unique-navigation","premium-hero","statement-sections"],
        "style_fit": ["Neobrutalism","Dark Aurora Premium","Gaming Cyber"],
        "components": {
            "special": [
                {"name":"SkiperNav","desc":"Unique animated navigation with bold typography","wow_factor":9},
                {"name":"HeroParallax","desc":"Layered parallax hero with multiple elements","wow_factor":9},
                {"name":"FeatureHighlight","desc":"Bold feature section with oversized numbers","wow_factor":8},
                {"name":"PricingCard","desc":"Distinctive pricing cards with animation","wow_factor":8},
            ]
        }
    },

    "tremor": {
        "name": "Tremor",
        "url": "https://tremor.so",
        "install_method": "npm install @tremor/react",
        "requires": ["react","tailwindcss"],
        "best_for": ["dashboards","analytics","charts","kpi-cards","data-viz","admin"],
        "style_fit": ["Corporate Clean","Fintech Trustworthy","Bento Grid Dashboard","Dark Developer Tool"],
        "components": {
            "charts": [
                {"name":"AreaChart","desc":"Area chart with smooth curves and tooltip","wow_factor":7},
                {"name":"BarChart","desc":"Vertical and horizontal bar charts","wow_factor":7},
                {"name":"LineChart","desc":"Clean line chart with comparison","wow_factor":7},
                {"name":"DonutChart","desc":"Donut with center label","wow_factor":7},
                {"name":"BarList","desc":"Horizontal bar list ranking items","wow_factor":8},
                {"name":"Tracker","desc":"Binary status tracker (uptime style)","wow_factor":8},
                {"name":"Funnel","desc":"Conversion funnel visualization","wow_factor":7},
                {"name":"ScatterChart","desc":"Correlation scatter plot","wow_factor":7},
            ],
            "metrics": [
                {"name":"Metric","desc":"Large KPI number with delta and trend","wow_factor":7},
                {"name":"BadgeDelta","desc":"Colored delta badge (up/down/neutral)","wow_factor":7},
                {"name":"ProgressBar","desc":"Animated progress bar","wow_factor":6},
                {"name":"ProgressCircle","desc":"Circular progress indicator","wow_factor":7},
            ],
            "layout": [
                {"name":"Card","desc":"Dashboard card with optional footer/header","wow_factor":6},
                {"name":"Grid","desc":"Responsive grid for dashboard layout","wow_factor":6},
                {"name":"Col","desc":"Column helper for dashboard grids","wow_factor":5},
                {"name":"Table","desc":"Data table with sorting","wow_factor":7},
            ]
        }
    },
    "animata": {
        "name": "Animata",
        "url": "https://animata.design",
        "install_method": "copy",
        "requires": ["tailwindcss","framer-motion"],
        "best_for": ["micro-interactions","loading-states","creative-animations","unique-effects"],
        "style_fit": ["Y2K Revival","Vaporwave Retro","Portfolio Creative","Gaming Cyber"],
        "components": {
            "effects": [
                {"name":"TextLoop","desc":"Continuously cycling animated text words","wow_factor":8},
                {"name":"Blobby","desc":"Morphing blob shape animation","wow_factor":8},
                {"name":"Sticker","desc":"Animated sticker-style elements","wow_factor":8},
                {"name":"FollowCursor","desc":"Element that follows the cursor","wow_factor":9},
                {"name":"LiquidChrome","desc":"Liquid chrome/mercury animation","wow_factor":10},
                {"name":"SplashCursor","desc":"Fluid simulation cursor effect","wow_factor":10},
                {"name":"MetaBalls","desc":"Blob merging metaballs effect","wow_factor":9},
                {"name":"NoiseCard","desc":"Perlin noise animated card background","wow_factor":9},
            ],
            "text": [
                {"name":"FadeInText","desc":"Chars fade in sequentially","wow_factor":7},
                {"name":"NumberFlow","desc":"Number transitions with smooth morphing","wow_factor":9},
                {"name":"RotatingText","desc":"3D rotating text transition","wow_factor":8},
                {"name":"WavyText","desc":"Characters animate in wave pattern","wow_factor":8},
            ]
        }
    },
    "motion-primitives": {
        "name": "Motion Primitives",
        "url": "https://motion-primitives.com",
        "install_method": "copy",
        "requires": ["framer-motion","tailwindcss"],
        "best_for": ["polished-transitions","physics-animations","smooth-reveals","cursor-effects"],
        "style_fit": ["Dark Aurora Premium","Luxury Premium Dark","Editorial Dark Premium","Portfolio Creative"],
        "components": {
            "transitions": [
                {"name":"Cursor","desc":"Custom cursor with magnetic pull","wow_factor":9},
                {"name":"MorphingDialog","desc":"Dialog morphs from trigger element","wow_factor":10},
                {"name":"InfiniteSlider","desc":"Smooth infinite carousel","wow_factor":8},
                {"name":"ProgressiveBlur","desc":"Blur gradient over overflowing content","wow_factor":8},
                {"name":"Carousel","desc":"Touch-friendly animated carousel","wow_factor":8},
                {"name":"Tilt","desc":"3D tilt effect with spring physics","wow_factor":8},
                {"name":"AnimatedBackground","desc":"Background transitions between states","wow_factor":8},
                {"name":"Magnetic","desc":"Magnetic pull on any element","wow_factor":9},
            ],
            "text": [
                {"name":"TextEffect","desc":"Character-by-character reveal effects","wow_factor":9},
                {"name":"TextShimmer","desc":"Shimmer sweep on text","wow_factor":8},
                {"name":"AnimatedNumber","desc":"Smooth number morphing","wow_factor":9},
                {"name":"GlitchText","desc":"Glitch/corruption text effect","wow_factor":8},
            ]
        }
    },
    "cult-ui": {
        "name": "Cult UI",
        "url": "https://www.cult-ui.com",
        "install_method": "copy",
        "requires": ["tailwindcss","framer-motion"],
        "best_for": ["carousel","dynamic-island","family-picker","direction-aware","bold-interactions"],
        "style_fit": ["Dark Aurora Premium","Y2K Revival","Portfolio Creative","Social Media Dark"],
        "components": {
            "special": [
                {"name":"DirectionAwareHover","desc":"Card reveals image from hover direction","wow_factor":9},
                {"name":"DynamicIsland","desc":"Apple Dynamic Island component","wow_factor":10},
                {"name":"Carousel3D","desc":"3D perspective carousel","wow_factor":9},
                {"name":"FamilyButton","desc":"Spring-expand button group","wow_factor":9},
                {"name":"ExpandableCard","desc":"Card that expands to full content","wow_factor":8},
                {"name":"DialogStack","desc":"Stacked dialogs with depth","wow_factor":9},
            ]
        }
    },
    "eldora-ui": {
        "name": "Eldora UI",
        "url": "https://www.eldoraui.site",
        "install_method": "copy",
        "requires": ["tailwindcss","framer-motion"],
        "best_for": ["hero-sections","pricing","testimonials","feature-sections","landing-pages"],
        "style_fit": ["Dark Aurora Premium","Glassmorphism Dark","Gradient Mesh Aurora"],
        "components": {
            "sections": [
                {"name":"HeroGeometric","desc":"Hero with rotating geometric shapes","wow_factor":9},
                {"name":"PricingCards","desc":"Animated pricing with hover effects","wow_factor":8},
                {"name":"TestimonialsMarquee","desc":"Two-row infinite testimonial marquee","wow_factor":8},
                {"name":"FeaturesBento","desc":"Bento grid features section","wow_factor":8},
                {"name":"LogoCloud","desc":"Animated logo grid","wow_factor":7},
                {"name":"TimelineScroll","desc":"Scroll-triggered timeline animation","wow_factor":8},
            ]
        }
    },
    "shadcn-blocks": {
        "name": "shadcn/ui Blocks",
        "url": "https://ui.shadcn.com/blocks",
        "install_method": "npx shadcn@latest add block [name]",
        "requires": ["tailwindcss","shadcn/ui"],
        "best_for": ["complete-page-sections","dashboard-blocks","auth-forms","rapid-setup"],
        "style_fit": ["Corporate Clean","Minimal SaaS Light","Dark Developer Tool","Fintech Trustworthy"],
        "components": {
            "blocks": [
                {"name":"Sidebar","desc":"Complete sidebar layout with collapsible","wow_factor":8},
                {"name":"Login","desc":"Full login form with social auth","wow_factor":7},
                {"name":"Calendar","desc":"Full calendar with event management","wow_factor":8},
                {"name":"Chart","desc":"Dashboard with multiple chart types","wow_factor":8},
                {"name":"Mail","desc":"Email client layout","wow_factor":8},
                {"name":"Settings","desc":"App settings page layout","wow_factor":7},
            ]
        }
    },
}

# ═══════════════════════════════════════════════════════════════════════
# UX LAWS — 20 laws with design application guidance
# ═══════════════════════════════════════════════════════════════════════
UX_LAWS = [
    {"law":"Fitts's Law","summary":"Time to acquire a target is function of distance and target size",
     "apply":"Min 44px tap targets. Primary CTA: largest button. Size = priority.",
     "keywords":"button size tap target mobile click cta primary action"},
    {"law":"Hick's Law","summary":"More choices = longer decision time (log scale)",
     "apply":"Max 5-7 nav items. ONE primary CTA per screen. Use progressive disclosure.",
     "keywords":"navigation choices options menu decision simplify"},
    {"law":"Miller's Law","summary":"Working memory holds 7±2 items",
     "apply":"Group features into chunks of 3. List items in sets of 3-7. Paginate long lists.",
     "keywords":"information grouping cards features list cognitive load"},
    {"law":"Jakob's Law","summary":"Users spend most time on other sites — expect familiar patterns",
     "apply":"Logo top-left. Nav top. Search top-right. Cart top-right. Don't reinvent.",
     "keywords":"convention familiar pattern navigation layout structure"},
    {"law":"Von Restorff Effect","summary":"Unique items are remembered better",
     "apply":"ONE element uses CTA color. Pricing: one card elevated. Nav: one CTA button only.",
     "keywords":"cta button highlight color accent contrast stand out"},
    {"law":"Peak-End Rule","summary":"Experiences judged by peak moment and end, not average",
     "apply":"Make hero and success/completion states exceptional. Empty states helpful.",
     "keywords":"hero success state onboarding impression experience"},
    {"law":"Aesthetic-Usability Effect","summary":"Beautiful = perceived as easier to use",
     "apply":"Polish builds trust. Animations reduce perceived load time. Beauty enables forgiveness.",
     "keywords":"design polish animation quality trust beautiful"},
    {"law":"Law of Proximity","summary":"Elements near each other are perceived as related",
     "apply":"Label 4px above its input. Related items: 8px gap. Sections: 64-96px gap.",
     "keywords":"spacing whitespace layout grouping label form"},
    {"law":"Law of Prägnanz","summary":"Perceive ambiguous forms as simplest interpretation",
     "apply":"When in doubt, simplify. Remove every element that doesn't earn its place.",
     "keywords":"simplify reduce minimal whitespace cognitive load clean"},
    {"law":"Serial Position Effect","summary":"First and last items best remembered",
     "apply":"Put most important nav first or last. Lead features list with best feature.",
     "keywords":"order list navigation feature first last priority"},
    {"law":"Doherty Threshold","summary":"Productivity soars when response time < 400ms",
     "apply":"Optimistic UI. Skeleton loaders >100ms. Progress bars >400ms.",
     "keywords":"loading performance skeleton progress feedback fast"},
    {"law":"Zeigarnik Effect","summary":"People remember incomplete tasks better than complete ones",
     "apply":"Profile completion %. Onboarding checklists. Step counters. Progress bars.",
     "keywords":"progress completion onboarding checklist steps todo"},
    {"law":"Law of Common Region","summary":"Elements in bounded regions are perceived as groups",
     "apply":"Card borders group related content. Backgrounds distinguish page sections.",
     "keywords":"card border section group container background"},
    {"law":"Tesler's Law (Conservation of Complexity)","summary":"Every system has irreducible complexity",
     "apply":"Don't push complexity to users. Absorb it in code. Form validation server-side.",
     "keywords":"complexity form validation ux simplify user"},
    {"law":"Postel's Law","summary":"Be conservative in output, liberal in input",
     "apply":"Accept various input formats (phone: +1-555-555, 15555555, etc). Output consistently formatted.",
     "keywords":"form input validation flexible format phone email"},
    {"law":"Goal-Gradient Effect","summary":"Effort increases as goal gets closer",
     "apply":"Show progress bars. '3 of 5 steps done' near end. Reward completion with animation.",
     "keywords":"progress bar steps completion reward gamification"},
    {"law":"Weber's Law","summary":"JND is proportional to the magnitude of the stimulus",
     "apply":"Small elements need bigger % change to feel different. Large type: 2px = noticeable. Small text: 2px = invisible.",
     "keywords":"typography size change contrast threshold perceive"},
    {"law":"Occam's Razor","summary":"Among competing solutions, the simplest is usually correct",
     "apply":"If two layouts achieve the same goal, ship the simpler one. Less is almost always more.",
     "keywords":"simplify design choice layout component selection"},
]

# ═══════════════════════════════════════════════════════════════════════
# PAGE PATTERNS
# ═══════════════════════════════════════════════════════════════════════
PAGE_PATTERNS = [
    {"type":"landing","name":"Hero-Centric SaaS Landing",
     "sections":["Sticky nav (logo + links + single CTA button)",
                 "Hero — headline + sub + CTA pair + social proof + product screenshot",
                 "Logo strip — 'Trusted by' with ScrollVelocity logos",
                 "Problem/Solution — Before (pain) → After (benefit) in 3 columns",
                 "Features — alternating large demo + copy, SpotlightCard grid",
                 "Social proof — stat counters + testimonials BounceCards",
                 "Pricing — 3 tiers, Pro card elevated with StarBorder",
                 "Final CTA — full-width with Orb/Ripple background",
                 "Footer — links + socials"],
     "cta_placement":"Hero (primary) + after features + final section",
     "conversion":"Repeat CTA every 2-3 sections. One primary action per section.",
     "react_bits":["Aurora","SplitText","MagneticButton","ScrollVelocity","SpotlightCard","StarBorder","CountUp","BounceCards"]},
    {"type":"dashboard","name":"Analytics Dashboard",
     "sections":["Fixed sidebar (240px) — logo, nav max 7 items, user at bottom",
                 "Sticky topbar — breadcrumb, search, notifications, avatar",
                 "KPI stat row — 4 cards with CountUp animations",
                 "Primary chart — full-width line/area chart",
                 "Secondary grid — table (2/3) + donut chart (1/3)",
                 "Data table with filter, sort, pagination"],
     "cta_placement":"Topbar action button + table row actions",
     "conversion":"Sidebar active state: bg-primary/10 + accent border-left",
     "react_bits":["CountUp","FadeContent","AnimatedList"]},
    {"type":"auth","name":"Split Auth Screen",
     "sections":["Left 50% — brand bg (Aurora/Silk/gradient) with tagline + social proof",
                 "Right 50% — logo + title + social auth (Google/GitHub) first + divider + email form",
                 "Below form — switch link (Sign up / Sign in)"],
     "cta_placement":"Primary submit button full-width inside form",
     "conversion":"Social auth above email form — reduces friction. One field per line.",
     "react_bits":["Silk","BlurText","FadeContent"]},
    {"type":"pricing","name":"3-Tier Pricing",
     "sections":["Section headline + annual/monthly toggle",
                 "3 pricing cards — Starter/Pro★/Enterprise",
                 "Pro card: ring-2 ring-primary shadow-xl scale-105 + 'Most Popular' badge",
                 "Feature comparison table (toggle show/hide)",
                 "FAQ Accordion — top 5 pricing objections",
                 "Risk-reversal line — 'Free to start, no credit card'"],
     "cta_placement":"Inside each pricing card",
     "conversion":"Pro card must visually break the pattern (Von Restorff).",
     "react_bits":["StarBorder","FadeContent","CountUp"]},
    {"type":"portfolio","name":"Creative Portfolio",
     "sections":["Fullscreen hero — name + role + ASCII/animated element",
                 "About — editorial layout, serif heading, photo",
                 "Work — ImageTrail on hover, or BounceCards gallery",
                 "Services/Skills — flowing list or grid",
                 "Contact — minimal form or email link"],
     "cta_placement":"Contact CTA in nav + end of page",
     "conversion":"Let the work speak. Less copy, more quality visuals.",
     "react_bits":["ImageTrail","FlowingMenu","TiltedCard","Silk","BlurText"]},
    {"type":"feature","name":"Product Feature Page",
     "sections":["Feature hero — name + icon + value prop + demo",
                 "How it works — 3 numbered steps",
                 "Specific benefits — 3 feature-specific wins",
                 "Customer quote — specific to this feature",
                 "Technical specs (if developer tool)",
                 "Related features — 3 cards",
                 "Feature-specific CTA"],
     "cta_placement":"Hero + end of page",
     "conversion":"CTA should be feature-specific: 'Try [Feature] free'",
     "react_bits":["StickyScrollReveal","FadeContent","SpotlightCard"]},
]

# ═══════════════════════════════════════════════════════════════════════
# SEARCH FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════
def _score(item: dict, query: str) -> int:
    q = query.lower()
    words = q.split()
    score = 0
    vibe = item.get("vibe","").lower()
    name = item.get("name","").lower()
    for w in words:
        if w in name: score += 10
        if w in vibe: score += 5
    return score

def search_palettes(query: str, n: int = 3) -> list:
    scored = sorted(PALETTES, key=lambda p: _score(p, query), reverse=True)
    return [p for p in scored if _score(p, query) > 0][:n] or PALETTES[:n]

def search_typography(query: str, n: int = 3) -> list:
    scored = sorted(TYPOGRAPHY, key=lambda t: _score(t, query), reverse=True)
    return [t for t in scored if _score(t, query) > 0][:n] or TYPOGRAPHY[:n]

def search_styles(query: str, n: int = 3) -> list:
    scored = sorted(STYLES, key=lambda s: _score(s, query), reverse=True)
    return [s for s in scored if _score(s, query) > 0][:n] or STYLES[:n]

def search_ux_laws(query: str, n: int = 3) -> list:
    q = query.lower()
    scored = [(u, sum(1 for w in q.split() if w in u.get("keywords","").lower() + u["law"].lower())) for u in UX_LAWS]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [u for u, s in scored if s > 0][:n] or UX_LAWS[:3]

def get_pattern(page_type: str) -> dict:
    q = page_type.lower()
    for p in PAGE_PATTERNS:
        if p["type"] in q or q in p["type"] or q in p["name"].lower():
            return p
    return PAGE_PATTERNS[0]

def select_components(product: str, style_name: str, framework: str = "react", dark: bool = True) -> dict:
    """
    Intelligent multi-library component selection across ALL 18 libraries.
    Reads style profiles, product keywords, and detected stack to route
    each design slot to the single best component from the best library.
    Never hardcodes the same output — every context gets a unique selection.
    """
    q = f"{product} {style_name}".lower()

    # Find matching style profile
    style = next((s for s in STYLES if s["name"] == style_name), None)
    if not style:
        matched = search_styles(q, 1)
        style = matched[0] if matched else STYLES[0]

    # Pull library lists from the style profile
    rb   = style.get("react_bits", [])
    ace  = style.get("aceternity", [])
    mu   = style.get("magicui", [])
    sh   = style.get("shadcn", ["Card","Button"])
    kibo = style.get("kiboui", [])
    ori  = style.get("originui", [])
    primary = style.get("primary_lib", "react_bits")

    # ── Keyword detection ─────────────────────────────────────────────
    is_y2k       = any(k in q for k in ["y2k","retro","myspace","chrome","holographic","iridescent","2000s"])
    is_cyber     = any(k in q for k in ["cyber","gaming","neon","glitch","esports","rgb","crypto","web3","blockchain"])
    is_editorial = any(k in q for k in ["editorial","magazine","luxury","fashion","serif","premium"])
    is_social    = any(k in q for k in ["social","community","friends","people","platform","network","feed"])
    is_3d        = any(k in q for k in ["3d","immersive","webgl","three","parallax","depth"])
    is_dashboard = any(k in q for k in ["dashboard","analytics","data","metrics","kpi","chart","admin","report"])
    is_fintech   = any(k in q for k in ["fintech","finance","bank","payment","invest","money","trading"])
    is_minimal   = any(k in q for k in ["minimal","clean","simple","corporate","professional","b2b"])
    is_portfolio = any(k in q for k in ["portfolio","agency","creative","studio","designer","developer"])
    is_ecommerce = any(k in q for k in ["ecommerce","shop","product","retail","cart","store","buy"])
    is_vaporwave = any(k in q for k in ["vaporwave","synthwave","80s","90s","sunset","nostalgic"])
    is_bento     = any(k in q for k in ["bento","grid","dashboard","showcase","feature"])
    is_health    = any(k in q for k in ["health","wellness","fitness","mental","mindful","calm","lifestyle"])
    is_auth      = any(k in q for k in ["auth","login","signup","register","onboarding","form"])
    has_form     = any(k in q for k in ["form","input","signup","checkout","contact","auth","register"])
    has_charts   = any(k in q for k in ["chart","graph","analytics","data","metric","stat","kpi","dashboard"])

    result = {
        "primary_lib":   primary,
        "style_name":    style["name"],
        "selections":    {},
        "install_commands": [],
    }

    # ═══════════════════════════════════════════════════════════════════
    # SLOT 1: BACKGROUND
    # ═══════════════════════════════════════════════════════════════════
    if is_y2k or is_vaporwave:
        bg = {"lib":"magicui","component":"RetroGrid","reason":"Vanishing-point retro grid = Y2K/vaporwave signature bg"}
    elif is_cyber and "BackgroundBoxes" in ace:
        bg = {"lib":"aceternity","component":"BackgroundBoxes","reason":"Colored grid boxes with wave = cyber energy"}
    elif is_cyber and "Vortex" in ace:
        bg = {"lib":"aceternity","component":"Vortex","reason":"Particle vortex = intense cyber atmosphere"}
    elif is_editorial:
        bg = {"lib":"react-bits","component":"Silk","reason":"Flowing silk = premium editorial atmosphere"}
    elif is_3d:
        bg = {"lib":"react-bits","component":"Ballpit","reason":"Physics balls = 3D depth and interactivity"}
    elif is_portfolio:
        bg = {"lib":"react-bits","component":"Particles","reason":"Interactive particles = developer portfolio energy"}
    elif is_auth:
        bg = {"lib":"react-bits","component":"Silk","reason":"Silk left panel = premium auth split screen"}
    elif is_social:
        bg = {"lib":"animata","component":"SplashCursor","reason":"Fluid cursor trail = alive, social, reactive feeling"}
    elif not dark:
        # Light backgrounds
        if is_bento or is_dashboard:
            bg = {"lib":"magicui","component":"DotPattern","reason":"Subtle dots = clean dashboard background"}
        elif is_minimal:
            bg = {"lib":"magicui","component":"GridPattern","reason":"Minimal grid lines = structured professional bg"}
        else:
            bg = {"lib":"magicui","component":"AnimatedGridPattern","reason":"Animated grid cells = subtle modern movement"}
    elif "LampEffect" in ace and is_editorial:
        bg = {"lib":"aceternity","component":"LampEffect","reason":"Overhead lamp conic light = cinematic editorial"}
    elif "BackgroundBeamsWithCollision" in ace:
        bg = {"lib":"aceternity","component":"BackgroundBeamsWithCollision","reason":"Colliding beams = dramatic dark premium hero"}
    elif "BackgroundBeams" in ace:
        bg = {"lib":"aceternity","component":"BackgroundBeams","reason":"Converging beams = focused dark hero atmosphere"}
    elif rb and any(c in rb for c in ["Aurora","Silk","Orb","Ballpit","Balatro","DotGrid"]):
        c = next(c for c in ["Aurora","Silk","Orb","Ballpit","Balatro","DotGrid"] if c in rb)
        bg = {"lib":"react-bits","component":c,"reason":f"React Bits {c} defines hero atmosphere for this style"}
    else:
        bg = {"lib":"react-bits","component":"Aurora","reason":"Aurora: versatile dark background with depth"}

    # ═══════════════════════════════════════════════════════════════════
    # SLOT 2: HERO TEXT (H1)
    # ═══════════════════════════════════════════════════════════════════
    if is_y2k or is_vaporwave:
        hero_text = {"lib":"magicui","component":"SparklesText","reason":"Animated sparkles around text = Y2K signature"}
    elif is_cyber:
        hero_text = {"lib":"motion-primitives","component":"GlitchText","reason":"Glitch corruption effect = cyber/hacker aesthetic"} if not is_minimal else                     {"lib":"magicui","component":"HyperText","reason":"Matrix scramble = cyber but accessible"}
    elif is_editorial:
        hero_text = {"lib":"aceternity","component":"TextGenerateEffect","reason":"Word-by-word generation = cinematic editorial reveal"}
    elif is_vaporwave:
        hero_text = {"lib":"animata","component":"RotatingText","reason":"3D rotating text = retro vaporwave energy"}
    elif is_3d:
        hero_text = {"lib":"motion-primitives","component":"TextEffect","reason":"Character physics effects = immersive 3D feel"}
    elif is_portfolio:
        hero_text = {"lib":"react-bits","component":"FuzzyText","reason":"Glitch on hover = memorable portfolio statement"}
    elif is_minimal or is_dashboard:
        hero_text = {"lib":"magicui","component":"BoxReveal","reason":"Clean box wipe = professional, structured reveal"}
    elif primary == "aceternity" and any(c in ace for c in ["TextGenerateEffect","FlipWords","ColourfulText"]):
        c = next(c for c in ["TextGenerateEffect","FlipWords","ColourfulText"] if c in ace)
        hero_text = {"lib":"aceternity","component":c,"reason":f"Aceternity {c} = cinematic headline for this style"}
    else:
        hero_text = {"lib":"react-bits","component":"SplitText","reason":"Staggered char entrance = highest impact headline reveal"}

    # ═══════════════════════════════════════════════════════════════════
    # SLOT 3: SUB-HEADLINE
    # ═══════════════════════════════════════════════════════════════════
    # Avoid duplicating hero_text
    sub_options = [
        ("react-bits","BlurText"),("magicui","WordFadeIn"),("magicui","WordPullUp"),
        ("animata","FadeInText"),("aceternity","TypewriterEffect"),("react-bits","ShinyText"),
    ]
    for lib, comp in sub_options:
        if not (lib == hero_text["lib"] and comp == hero_text["component"]):
            if lib == "react-bits" and comp in rb:
                sub_text = {"lib":lib,"component":comp,"reason":f"React Bits {comp}: distinct sub-text reveal"}
                break
            elif lib == "magicui":
                sub_text = {"lib":lib,"component":comp,"reason":f"Magic UI {comp}: smooth word-by-word sub entrance"}
                break
            elif lib == "animata":
                sub_text = {"lib":lib,"component":comp,"reason":f"Animata {comp}: character fade sub entrance"}
                break
    else:
        sub_text = {"lib":"react-bits","component":"BlurText","reason":"Blur→sharp reveal: premium sub-text"}

    # ═══════════════════════════════════════════════════════════════════
    # SLOT 4: CTA BUTTON
    # ═══════════════════════════════════════════════════════════════════
    if is_y2k or is_vaporwave:
        cta = {"lib":"magicui","component":"RainbowButton","reason":"Rainbow gradient border = Y2K maximalist CTA"}
    elif is_cyber:
        cta = {"lib":"magicui","component":"ShimmerButton","reason":"Dark shimmer CTA = cyber premium feel"}
    elif is_editorial or is_luxury if "is_luxury" in dir() else False:
        cta = {"lib":"react-bits","component":"MagneticButton","reason":"Magnetic pull = refined interactive elegance"}
    elif is_social:
        cta = {"lib":"magicui","component":"CoolMode","reason":"Confetti burst = joyful social interaction"}
    elif is_portfolio:
        cta = {"lib":"react-bits","component":"MagneticButton","reason":"Magnetic = portfolio delight moment"}
    elif is_health or is_minimal:
        cta = {"lib":"magicui","component":"AnimatedSubscribeButton","reason":"Smooth confirm animation = trustworthy conversion"}
    elif not dark:
        cta = {"lib":"magicui","component":"InteractiveHoverButton","reason":"Arrow-in hover = clean light CTA interaction"}
    elif dark:
        cta = {"lib":"magicui","component":"ShimmerButton","reason":"Shimmer on dark = unmissable premium CTA"}
    else:
        cta = {"lib":"shadcn","component":"Button","reason":"Accessible CTA — style with design tokens"}

    # ═══════════════════════════════════════════════════════════════════
    # SLOT 5: FEATURE CARDS
    # ═══════════════════════════════════════════════════════════════════
    if is_bento or is_dashboard:
        feature_cards = {"lib":"magicui","component":"BentoGrid","reason":"Bento asymmetric grid = modern feature showcase"}
    elif is_3d and "ThreeDCardEffect" in ace:
        feature_cards = {"lib":"aceternity","component":"ThreeDCardEffect","reason":"True 3D depth = immersive feature presentation"}
    elif is_editorial and "FocusCards" in ace:
        feature_cards = {"lib":"aceternity","component":"FocusCards","reason":"Blur non-focused = editorial editorial hierarchy"}
    elif is_y2k or is_vaporwave:
        feature_cards = {"lib":"magicui","component":"NeonGradientCard","reason":"Neon animated border = Y2K/vaporwave feature card"}
    elif is_cyber:
        feature_cards = {"lib":"cult-ui","component":"DirectionAwareHover","reason":"Direction-aware reveal = cyber interactive energy"}
    elif is_social or is_portfolio:
        feature_cards = {"lib":"cult-ui","component":"ExpandableCard","reason":"Expanding reveal = engaging social/portfolio card"}
    elif is_ecommerce and "ExpandingCard" in ace:
        feature_cards = {"lib":"aceternity","component":"ExpandingCard","reason":"Product detail expand = ecommerce exploration"}
    elif not dark:
        feature_cards = {"lib":"magicui","component":"MagicCard","reason":"Radial glow follows mouse = sophisticated light card"}
    elif "SpotlightCard" in rb:
        feature_cards = {"lib":"react-bits","component":"SpotlightCard","reason":"Spotlight follows mouse = premium dark feature card"}
    else:
        feature_cards = {"lib":"shadcn","component":"Card","reason":"Accessible card — customize with design tokens"}

    # ═══════════════════════════════════════════════════════════════════
    # SLOT 6: STATS / NUMBERS
    # ═══════════════════════════════════════════════════════════════════
    if is_dashboard or is_fintech or has_charts:
        stats = {"lib":"tremor","component":"Metric","reason":"Tremor Metric: KPI number with delta and trend — perfect for dashboards"}
    elif is_y2k or is_vaporwave:
        stats = {"lib":"animata","component":"NumberFlow","reason":"Smooth number morphing = Y2K animated data"}
    elif "NumberTicker" in mu:
        stats = {"lib":"magicui","component":"NumberTicker","reason":"Spring number animation = smooth social proof counter"}
    elif "CountUp" in rb:
        stats = {"lib":"react-bits","component":"CountUp","reason":"CountUp: reliable viewport-triggered stat animation"}
    else:
        stats = {"lib":"react-bits","component":"CountUp","reason":"CountUp: stat animation on scroll enter"}

    # ═══════════════════════════════════════════════════════════════════
    # SLOT 7: TESTIMONIALS / SOCIAL PROOF
    # ═══════════════════════════════════════════════════════════════════
    if is_social or is_editorial:
        testimonials = {"lib":"aceternity","component":"AnimatedTooltip","reason":"Avatar stack with tooltips = social community feel"}
    elif is_ecommerce:
        testimonials = {"lib":"magicui","component":"MarqueeComponent","reason":"Infinite review marquee = ecommerce trust signal"}
    elif is_dashboard or is_fintech:
        testimonials = {"lib":"eldora-ui","component":"TestimonialsMarquee","reason":"Two-row marquee = professional B2B trust"}
    elif is_y2k or is_social:
        testimonials = {"lib":"react-bits","component":"BounceCards","reason":"Physics cards = Y2K fun social energy"}
    elif "CardStack" in ace:
        testimonials = {"lib":"aceternity","component":"CardStack","reason":"Stacked card cycling = polished testimonial display"}
    else:
        testimonials = {"lib":"react-bits","component":"BounceCards","reason":"BounceCards: physics-driven testimonial stack"}

    # ═══════════════════════════════════════════════════════════════════
    # SLOT 8: LOGO STRIP / PARTNER LOGOS
    # ═══════════════════════════════════════════════════════════════════
    if is_y2k or is_vaporwave:
        logos = {"lib":"react-bits","component":"ScrollVelocity","reason":"Speed-matched scroll marquee = Y2K kinetic energy"}
    elif is_editorial:
        logos = {"lib":"animata","component":"TextLoop","reason":"Elegant partner name cycling = editorial restraint"}
    elif is_fintech or is_minimal:
        logos = {"lib":"magicui","component":"MarqueeComponent","reason":"Clean infinite marquee = professional trust strip"}
    else:
        logos = {"lib":"magicui","component":"MarqueeComponent","reason":"Infinite logo marquee = standard trust strip"}

    # ═══════════════════════════════════════════════════════════════════
    # SLOT 9: BORDERS / CARD ACCENTS
    # ═══════════════════════════════════════════════════════════════════
    if is_y2k or is_vaporwave:
        borders = {"lib":"magicui","component":"ShineBorder","reason":"Metallic shine border = Y2K iridescent/chrome effect"}
    elif is_cyber:
        borders = {"lib":"magicui","component":"NeonGradientCard","reason":"Neon animated gradient = cyber glow borders"}
    elif is_social or is_portfolio:
        borders = {"lib":"magicui","component":"BorderBeam","reason":"Beam travels border = interactive social/portfolio feel"}
    elif is_3d or is_editorial:
        borders = {"lib":"aceternity","component":"MovingBorder","reason":"Traveling gradient border = cinematic card accent"}
    elif is_dashboard:
        borders = {"lib":"magicui","component":"AnimatedBeam","reason":"SVG path beam = dashboard data flow visualization"}
    elif is_fintech or is_minimal:
        borders = {"lib":"magicui","component":"BorderBeam","reason":"Subtle beam = professional card highlight"}
    else:
        borders = {"lib":"magicui","component":"BorderBeam","reason":"Border beam: dynamic edge highlight"}

    # ═══════════════════════════════════════════════════════════════════
    # SLOT 10: MOBILE NAVIGATION
    # ═══════════════════════════════════════════════════════════════════
    if is_portfolio or is_editorial or is_social:
        mobile_menu = {"lib":"react-bits","component":"FlowingMenu","reason":"Full-screen flowing text = premium mobile nav"}
    elif is_dashboard or is_fintech:
        mobile_menu = {"lib":"shadcn","component":"Sidebar","reason":"App sidebar: structured navigation for data-heavy apps"}
    elif is_y2k or is_cyber:
        mobile_menu = {"lib":"cult-ui","component":"DynamicIsland","reason":"Dynamic Island nav = Y2K/cyber tech-forward mobile"}
    else:
        mobile_menu = {"lib":"shadcn","component":"Sheet","reason":"Sheet drawer: accessible, reliable mobile menu"}

    # ═══════════════════════════════════════════════════════════════════
    # SLOT 11: DESKTOP NAVIGATION
    # ═══════════════════════════════════════════════════════════════════
    if is_editorial or is_luxury if "is_luxury" in dir() else False:
        nav = {"lib":"aceternity","component":"FloatingNavbar","reason":"Floating nav = editorial elegance on scroll"}
    elif is_portfolio:
        nav = {"lib":"react-bits","component":"DockExpandable","reason":"Dock navigation = creative portfolio interaction"}
    elif is_dashboard:
        nav = {"lib":"shadcn","component":"Sidebar","reason":"Sidebar: proper app navigation for dashboards"}
    else:
        nav = {"lib":"shadcn","component":"NavigationMenu","reason":"NavigationMenu: accessible, keyboard-navigable header"}

    # ═══════════════════════════════════════════════════════════════════
    # SLOT 12: FORMS / INPUTS (NEW — uses originui, kiboui)
    # ═══════════════════════════════════════════════════════════════════
    if has_form or is_auth or is_dashboard or is_fintech or is_ecommerce:
        if is_auth and not (is_dashboard or is_fintech):
            form_input = {"lib":"originui","component":"Social buttons","reason":"Origin UI social auth: Google/GitHub OAuth style"}
        elif is_dashboard or is_fintech:
            form_input = {"lib":"kiboui","component":"DateRangePicker","reason":"Kibo DateRangePicker: enterprise date filtering for dashboards"}
            # Also add kanban if project management context
            if any(k in q for k in ["kanban","board","task","project","management"]):
                result["selections"]["advanced_ui"] = {"lib":"kiboui","component":"Kanban","reason":"Kibo Kanban: drag-drop board — no other library has this"}
            else:
                result["selections"]["advanced_ui"] = {"lib":"kiboui","component":"MultiSelect","reason":"Kibo MultiSelect: multi-value filtering for data apps"}
        elif is_ecommerce:
            form_input = {"lib":"originui","component":"Tags input","reason":"Origin UI tags: product variant/tag selection"}
        else:
            form_input = {"lib":"originui","component":"Input with icon prefix","reason":"Origin UI: production-grade form inputs beyond shadcn"}
        result["selections"]["forms"] = form_input

    # ═══════════════════════════════════════════════════════════════════
    # SLOT 13: DELIGHT / CURSOR EFFECT (NEW — the wow moment)
    # ═══════════════════════════════════════════════════════════════════
    if is_portfolio or is_editorial:
        delight = {"lib":"react-bits","component":"ImageTrail","reason":"Image trail cursor = single delight moment for portfolio"}
    elif is_y2k or is_vaporwave:
        delight = {"lib":"animata","component":"SplashCursor","reason":"Fluid splash cursor = Y2K alive/interactive feel"}
    elif is_cyber:
        delight = {"lib":"react-bits","component":"Crosshair","reason":"Custom crosshair cursor = cyber gaming precision"}
    elif is_social:
        delight = {"lib":"motion-primitives","component":"Magnetic","reason":"Magnetic pull on avatars/cards = social interactivity"}
    elif is_3d:
        delight = {"lib":"cult-ui","component":"DynamicIsland","reason":"Dynamic Island state transitions = 3D depth signal"}
    else:
        delight = {"lib":"motion-primitives","component":"Cursor","reason":"Custom cursor = premium brand touch"}
    result["selections"]["delight"] = delight

    # ═══════════════════════════════════════════════════════════════════
    # SLOT 14: CHARTS (appears when dashboard/analytics detected)
    # ═══════════════════════════════════════════════════════════════════
    if is_dashboard or has_charts:
        result["selections"]["charts"] = {
            "lib":"tremor","component":"AreaChart",
            "reason":"Tremor AreaChart: production dashboard chart with tooltip, legend, responsive"
        }
        result["selections"]["kpi_cards"] = {
            "lib":"tremor","component":"Metric",
            "reason":"Tremor Metric: KPI number with colored delta — purpose-built for dashboards"
        }

    # Assemble final selections
    result["selections"].update({
        "background":    bg,
        "hero_text":     hero_text,
        "sub_text":      sub_text,
        "cta_button":    cta,
        "feature_cards": feature_cards,
        "stats":         stats,
        "testimonials":  testimonials,
        "logos":         logos,
        "borders":       borders,
        "mobile_menu":   mobile_menu,
        "navigation":    nav,
    })

    # ═══════════════════════════════════════════════════════════════════
    # GENERATE INSTALL COMMANDS
    # ═══════════════════════════════════════════════════════════════════
    MU_CLI = {
        "ShimmerButton":"shimmer-button","RainbowButton":"rainbow-button",
        "InteractiveHoverButton":"interactive-hover-button","PulsatingButton":"pulsating-button",
        "AnimatedSubscribeButton":"animated-subscribe-button","CoolMode":"cool-mode",
        "TypingAnimation":"typing-animation","WordPullUp":"word-pull-up",
        "WordFadeIn":"word-fade-in","HyperText":"hyper-text","SparklesText":"sparkles-text",
        "NumberTicker":"number-ticker","AnimatedGradientText":"animated-gradient-text",
        "BoxReveal":"box-reveal","GridPattern":"grid-pattern","DotPattern":"dot-pattern",
        "AnimatedGridPattern":"animated-grid-pattern","Ripple":"ripple",
        "FlickeringGrid":"flickering-grid","RetroGrid":"retro-grid","Meteors":"meteors",
        "BorderBeam":"border-beam","AnimatedBeam":"animated-beam","ShineBorder":"shine-border",
        "MagicCard":"magic-card","NeonGradientCard":"neon-gradient-card",
        "MarqueeComponent":"marquee","BentoGrid":"bento-grid","OrbitingCircles":"orbiting-circles",
        "AnimatedList":"animated-list","Dock":"dock","Particles":"particles","Confetti":"confetti",
        "GradualSpacing":"gradual-spacing",
    }

    seen = set()
    for sel in result["selections"].values():
        lib  = sel["lib"]
        comp = sel["component"]
        key  = f"{lib}:{comp}"
        if key in seen: continue
        seen.add(key)

        if lib == "react-bits":
            result["install_commands"].append(f'npx shadcn@latest add "https://reactbits.dev/r/{comp}-TS-TW"')
        elif lib == "magicui":
            cli = MU_CLI.get(comp, re.sub(r"(?<!^)(?=[A-Z])", "-", comp).lower())
            result["install_commands"].append(f"npx magicui-cli@latest add {cli}")
        elif lib == "aceternity":
            slug = re.sub(r"(?<!^)(?=[A-Z])", "-", comp).lower()
            result["install_commands"].append(f"# Copy {comp}: https://ui.aceternity.com/components/{slug}")
        elif lib == "tremor":
            result["install_commands"].append(f"npm install @tremor/react  # includes {comp}")
        elif lib == "animata":
            result["install_commands"].append(f"# Copy {comp}: https://animata.design/docs/text/{comp.lower()}")
        elif lib == "motion-primitives":
            result["install_commands"].append(f"# Copy {comp}: https://motion-primitives.com/docs/{re.sub(r'(?<!^)(?=[A-Z])','-',comp).lower()}")
        elif lib == "cult-ui":
            result["install_commands"].append(f"# Copy {comp}: https://www.cult-ui.com/docs/components/{re.sub(r'(?<!^)(?=[A-Z])','-',comp).lower()}")
        elif lib == "eldora-ui":
            result["install_commands"].append(f"# Copy {comp}: https://www.eldoraui.site/components")
        elif lib == "kiboui":
            cli = re.sub(r"(?<!^)(?=[A-Z])", "-", comp).lower()
            result["install_commands"].append(f"npx kiui@latest add {cli}")
        elif lib == "originui":
            result["install_commands"].append(f"# Copy {comp}: https://originui.com")
        elif lib == "shadcn-blocks":
            block = re.sub(r"(?<!^)(?=[A-Z])", "-", comp).lower()
            result["install_commands"].append(f"npx shadcn@latest add block {block}")

    return result


def resolve_product(product: str, style: str) -> dict:
    """Match product + style keywords to best palette, typography, and style profile."""
    q = f"{product} {style}".lower()
    palettes = search_palettes(q, 1)
    typography = search_typography(q, 1)
    styles = search_styles(q, 1)
    return {
        "palette": palettes[0],
        "typography": typography[0],
        "style": styles[0],
    }

if __name__ == "__main__":
    print("Core engine loaded.")
    print(f"Palettes: {len(PALETTES)}")
    print(f"Typography pairings: {len(TYPOGRAPHY)}")
    print(f"Style profiles: {len(STYLES)}")
    print(f"UX laws: {len(UX_LAWS)}")
    print(f"Page patterns: {len(PAGE_PATTERNS)}")
    print(f"Libraries: {len(LIBRARY_CATALOG)}")


# ═══════════════════════════════════════════════════════════════════════
# PALETTE ENRICHMENT — color science metadata added dynamically
# ═══════════════════════════════════════════════════════════════════════
PALETTE_SCIENCE = {
    "Midnight Indigo":  {"industry": "ai,saas,tech",      "emotion": "premium,creative,innovative",  "harmony": "analogous",      "wcag_note": "primary on bg: 4.45:1 (borderline)"},
    "Ocean Slate":      {"industry": "saas,b2b,developer", "emotion": "trust,clarity,professional",   "harmony": "analogous",      "wcag_note": "primary on bg: 5.8:1 AA"},
    "Violet Storm":     {"industry": "ai,creative,crypto", "emotion": "dramatic,premium,powerful",    "harmony": "monochromatic",  "wcag_note": "cta on bg: 6.2:1 AA"},
    "Warm Cream":       {"industry": "editorial,blog,food","emotion": "warm,organic,approachable",    "harmony": "analogous",      "wcag_note": "text on bg: 15.4:1 AAA"},
    "Forest Sage":      {"industry": "wellness,eco,health","emotion": "growth,calm,natural",          "harmony": "analogous",      "wcag_note": "primary on bg: 4.9:1 AA"},
    "Rose Gold":        {"industry": "beauty,luxury,fashion","emotion":"luxury,feminine,exclusive",   "harmony": "monochromatic",  "wcag_note": "cta on surface: 4.7:1 AA"},
    "Nordic Frost":     {"industry": "saas,corporate,b2b", "emotion": "clean,trustworthy,minimal",   "harmony": "analogous",      "wcag_note": "primary on bg: 5.9:1 AA"},
    "Cyber Neon":       {"industry": "gaming,crypto,edgy", "emotion": "energy,electric,bold",        "harmony": "complementary",  "wcag_note": "neon on dark: >7:1 AAA"},
    "Sunset Coral":     {"industry": "consumer,social,app","emotion": "fun,playful,energetic",       "harmony": "analogous",      "wcag_note": "primary on bg: 4.5:1 AA"},
    "Obsidian Gold":    {"industry": "luxury,finance,elite","emotion":"exclusive,wealthy,premium",   "harmony": "complementary",  "wcag_note": "gold on dark: 6.8:1 AA"},
    "Electric Blue":    {"industry": "fintech,enterprise", "emotion": "trust,stable,corporate",      "harmony": "analogous",      "wcag_note": "primary on bg: 5.5:1 AA"},
    "Dark Emerald":     {"industry": "fintech,data,security","emotion":"growth,secure,professional", "harmony": "monochromatic",  "wcag_note": "primary on bg: 4.8:1 AA"},
    "Lavender Mist":    {"industry": "wellness,meditation","emotion": "calm,gentle,creative",        "harmony": "monochromatic",  "wcag_note": "primary on bg: 5.1:1 AA"},
    "Carbon Zinc":      {"industry": "developer,tool,dark","emotion": "technical,precise,focused",   "harmony": "monochromatic",  "wcag_note": "cta on dark: 5.9:1 AA"},
    "Champagne Blanc":  {"industry": "wedding,luxury,event","emotion":"elegant,refined,exclusive",  "harmony": "analogous",      "wcag_note": "text on bg: 12.6:1 AAA"},
    "Deep Space":       {"industry": "tech,sci-fi,immersive","emotion":"cosmic,ambitious,futuristic","harmony": "analogous",     "wcag_note": "primary on bg: 5.4:1 AA"},
    "Terra Cotta":      {"industry": "food,craft,artisan", "emotion": "warm,earthy,authentic",       "harmony": "analogous",      "wcag_note": "primary on bg: 4.6:1 AA"},
    "Arctic White":     {"industry": "medical,clinical,health","emotion":"clean,trustworthy,clear",  "harmony": "analogous",      "wcag_note": "primary on bg: 5.8:1 AA"},
    "Plum Noir":        {"industry": "editorial,luxury,fashion","emotion":"dramatic,mysterious,bold","harmony": "monochromatic",  "wcag_note": "cta on dark: 5.7:1 AA"},
    "Mint Fresh":       {"industry": "health,fitness,wellness","emotion":"fresh,energetic,clean",    "harmony": "analogous",      "wcag_note": "primary on bg: 4.7:1 AA"},
}

def get_palette_science(palette_name: str) -> dict:
    """Get color science metadata for a palette."""
    return PALETTE_SCIENCE.get(palette_name, {
        "industry": "general", "emotion": "modern", 
        "harmony": "analogous", "wcag_note": "verify contrast manually"
    })


# ═══════════════════════════════════════════════════════════════════════
# TYPOGRAPHY SCIENCE METADATA — enriches existing TYPOGRAPHY list
# ═══════════════════════════════════════════════════════════════════════
TYPOGRAPHY_SCIENCE = {
    "Outfit + Inter": {
        "x_height":     "high/high",
        "scale":        "major-third (1.25)",
        "best_ratio":   "perfect-fourth for bold, major-third for UI",
        "variable":     "Both variable fonts — weight contrast without 2nd typeface",
        "readability":  "Inter body: x-height optimized for screens. Outfit heading: geometric warmth.",
        "measure":      "max-width: 65ch on body paragraphs",
    },
    "Plus Jakarta Sans + DM Sans": {
        "x_height":     "medium-high/high",
        "scale":        "perfect-fourth (1.333)",
        "variable":     "Both variable — premium gradient weight transitions",
        "readability":  "DM Sans warmer than Inter, better for consumer-facing products.",
        "measure":      "max-width: 68ch on body",
    },
    "Space Grotesk + Space Mono": {
        "x_height":     "high/medium",
        "scale":        "major-third (1.25)",
        "note":         "Mono body is intentional for developer/technical contexts only",
        "readability":  "Keep Mono to code snippets and labels. Body paragraphs: use Space Grotesk.",
    },
    "Fraunces + DM Sans": {
        "x_height":     "medium/high",
        "scale":        "golden (1.618) — drama is the point",
        "variable":     "Fraunces has SOFT, WONK, opsz axes — use for weight-on-scroll effects",
        "headline_min": "40px — Fraunces loses appeal below display sizes",
        "readability":  "Never use Fraunces for body text. DM Sans handles all UI/body.",
    },
    "Bricolage Grotesque + Instrument Sans": {
        "x_height":     "high/high",
        "scale":        "perfect-fourth (1.333)",
        "variable":     "Bricolage variable — ink-trap optical refinements at large sizes",
        "readability":  "Both high x-height — excellent screen readability.",
    },
    "Clash Display + Switzer": {
        "x_height":     "high/high",
        "scale":        "perfect-fifth (1.5) — bold, committed",
        "note":         "Fontshare fonts — free, no Google Fonts dependency",
        "readability":  "Clash: display-only. Switzer: clean body at any size.",
    },
}

def get_typography_science(pairing_name: str) -> dict:
    """Get science metadata for a typography pairing."""
    return TYPOGRAPHY_SCIENCE.get(pairing_name, {
        "scale": "major-third (1.25)",
        "measure": "max-width: 65ch on paragraphs",
    })


# ═══════════════════════════════════════════════════════════════════════
# GESTALT PRINCIPLES — for design recommendations
# ═══════════════════════════════════════════════════════════════════════
GESTALT_CHECKS = [
    {"principle":"Proximity",    "check":"label_spacing",    "rule":"Form labels must be 4-8px from their input. Groups separated 20-24px."},
    {"principle":"Similarity",   "check":"cta_uniqueness",   "rule":"CTA color must be unique on the page — ONE element uses that color."},
    {"principle":"Similarity",   "check":"card_consistency", "rule":"All cards in a grid: same height, same padding, same internal structure."},
    {"principle":"Continuity",   "check":"list_alignment",   "rule":"All list items align to single vertical axis."},
    {"principle":"Figure/Ground","check":"elevation_system",  "rule":"3+ z-levels: page -> card -> dropdown -> modal. Each distinctly elevated."},
    {"principle":"Common Fate",  "check":"stagger_grouping",  "rule":"Staggered items entering together signal they belong to the same group."},
    {"principle":"Closure",      "check":"skeleton_shape",    "rule":"Skeleton loaders must match the shape of content they replace."},
    {"principle":"Symmetry",     "check":"hero_composition",  "rule":"Hero: centered=stable. Off-center=dynamic. Choose deliberately."},
]

def get_gestalt_checks(layout_type: str) -> list:
    layout_map = {
        "landing":   ["cta_uniqueness","elevation_system","hero_composition"],
        "dashboard": ["card_consistency","list_alignment","elevation_system"],
        "auth":      ["label_spacing","elevation_system"],
        "pricing":   ["card_consistency","cta_uniqueness","elevation_system"],
    }
    relevant = layout_map.get(layout_type, ["cta_uniqueness","card_consistency"])
    return [g for g in GESTALT_CHECKS if g["check"] in relevant]
