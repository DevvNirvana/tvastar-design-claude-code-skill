#!/usr/bin/env python3
"""
Framework Lint v3.0 — checks generated code against framework + library guidelines.
Covers: Next.js, React, shadcn, Tailwind, Vue, Svelte, Framer Motion,
        Aceternity, Magic UI, React Bits. 76 rules total.
Sources: nextjs-guidelines.md, react-guidelines.md, shadcn-tailwind-guidelines.md,
         vue-svelte-guidelines.md, motion-principles.md, react-bits-catalog.md
"""
import sys, re, json, argparse, subprocess
from pathlib import Path

LINT_RULES = {
"nextjs": [
    {"id":"NX001","severity":"High",  "rule":"Use next/image not <img>","pattern":r"<img\s","message":"Use <Image> from 'next/image' for optimization + LCP","good":"<Image src={url} alt='Description' width={400} height={300} />"},
    {"id":"NX002","severity":"High",  "rule":"use client for hooks/events","pattern":r"(useState|useEffect|onClick|useRef|useCallback|useMemo)\b","message":"Add 'use client' directive at top when using React hooks or events","good":"'use client'  ← line 1 of file"},
    {"id":"NX003","severity":"High",  "rule":"No server env in client","pattern":r"process\.env\.(?!NEXT_PUBLIC_)\w+","message":"Non-NEXT_PUBLIC_ env vars must never appear in client components","good":"NEXT_PUBLIC_API_URL for client-accessible vars"},
    {"id":"NX004","severity":"Medium","rule":"Use next/link not <a href>","pattern":r'<a\s+href=["\']/',"message":"Use <Link> from 'next/link' for internal navigation + prefetch","good":"<Link href='/dashboard'>"},
    {"id":"NX005","severity":"Medium","rule":"Use next/font not @import","pattern":r"@import url\(.+fonts\.googleapis","message":"Use 'next/font/google' instead of @import — eliminates FOUT","good":"import { Inter } from 'next/font/google'"},
    {"id":"NX006","severity":"High",  "rule":"Explicit cache on fetch","pattern":r"fetch\(['\"][^'\"]+['\"],\s*\{(?![^}]*cache:)","message":"Next.js 15 defaults to uncached — always set cache explicitly","good":"fetch(url, { cache: 'force-cache' }) or { next: { revalidate: 3600 } }"},
    {"id":"NX007","severity":"High",  "rule":"Validate Server Actions","pattern":r"'use server'[\s\S]{0,200}async function","message":"Server Actions must validate input with Zod before processing","good":"const data = schema.parse(formData) before any DB operation"},
    {"id":"NX008","severity":"High",  "rule":"Sanitize dangerouslySetInnerHTML","pattern":r"dangerouslySetInnerHTML=\{\{\s*__html:\s*\w","message":"Sanitize user content with DOMPurify to prevent XSS","good":"__html: DOMPurify.sanitize(userContent)"},
    {"id":"NX009","severity":"High",  "rule":"Auth check in Server Actions","pattern":r"'use server'[\s\S]{0,300}(?:delete|update|create)\s","message":"Verify auth/session before mutating data in Server Actions"},
    {"id":"NX010","severity":"Medium","rule":"revalidatePath after mutation","pattern":r"'use server'[\s\S]{0,400}(?:create|update|delete)\s(?![\s\S]{0,100}revalidatePath|revalidateTag|redirect)","message":"Call revalidatePath() or redirect() after Server Action mutations"},
    {"id":"NX011","severity":"High",  "rule":"loading.tsx for async pages","pattern":r"export default async function \w+Page","message":"Create loading.tsx for async pages — enables Suspense streaming","good":"app/dashboard/loading.tsx with skeleton component"},
    {"id":"NX013","severity":"High",  "rule":"Await params in Next.js 15","pattern":r"params\.\w+(?!.*await)","message":"Next.js 15: params and searchParams are Promises — must await them","good":"const { id } = await params"},
    {"id":"NX014","severity":"High",  "rule":"useActionState not useFormState","pattern":r"useFormState","message":"React 19: useFormState renamed to useActionState — update import","good":"import { useActionState } from 'react'"},
    {"id":"NX015","severity":"Medium","rule":"after() for post-response work","pattern":r"(?:analytics|logPageView|tracking)\((?![\s\S]{0,200}after\()","message":"Use next/server after() for analytics/logging — runs after response sent","good":"import { after } from 'next/server'; after(() => logPageView())"},
    {"id":"NX012","severity":"Medium","rule":"error.tsx for error boundary","pattern":r"export default function \w+Page","message":"Create error.tsx alongside each page for error boundaries","good":"app/dashboard/error.tsx with 'use client' + reset() handler"},
],
"react": [
    {"id":"RC001","severity":"High",  "rule":"Keys in list renders","pattern":r"\.map\([^)]+\)\s*=>\s*<(?![^>]*key=)","message":"Missing key prop — causes reconciliation bugs and broken animations","good":"key={item.id} — never key={index}"},
    {"id":"RC002","severity":"High",  "rule":"No immediate event call","pattern":r"on\w+=\{[a-zA-Z_]\w*\(\)","message":"onClick={fn()} calls fn immediately on render — remove the ()","good":"onClick={fn} or onClick={() => fn(arg)}"},
    {"id":"RC003","severity":"High",  "rule":"Semantic HTML for clicks","pattern":r"<div[^>]+onClick","message":"Use <button> for clickable elements — <div onClick> breaks a11y and keyboard","good":"<button onClick={...}>"},
    {"id":"RC004","severity":"High",  "rule":"No hooks in conditions","pattern":r"if\s*\([^)]+\)\s*\{[^}]*(useState|useEffect|useRef|useCallback)","message":"Hooks inside conditions violate Rules of Hooks — always call unconditionally","good":"Move hooks to top of component body"},
    {"id":"RC005","severity":"Medium","rule":"Memoize context values","pattern":r"value=\{\{[^}]+\}\}","message":"Inline object as context value causes all consumers to re-render every time","good":"value={useMemo(() => ({...}), [deps])}"},
    {"id":"RC006","severity":"Medium","rule":"Effect cleanup for listeners","pattern":r"window\.addEventListener\((?![\s\S]{0,300}return\s*\(\)\s*=>)","message":"Add cleanup function in useEffect to remove event listeners","good":"return () => window.removeEventListener(...)"},
    {"id":"RC007","severity":"High",  "rule":"Alt text on images","pattern":r"<(?:img|Image)\s(?![^>]*alt=)","message":"All images need alt text — required for WCAG 2.1 AA"},
    {"id":"RC008","severity":"High",  "rule":"Cleanup subscriptions in useEffect","pattern":r"useEffect\([\s\S]{0,400}subscribe\((?![\s\S]{0,300}return\s*\(\)\s*=>)","message":"Subscriptions need cleanup to prevent memory leaks","good":"return () => subscription.unsubscribe()"},
    {"id":"RC009","severity":"Medium","rule":"No async useEffect callback","pattern":r"useEffect\(async","message":"useEffect callback cannot be async — use inner async function","good":"useEffect(() => { const fn = async () => {...}; fn() }, [])"},
    {"id":"RC010","severity":"Medium","rule":"Stable callbacks with useCallback","pattern":r"on\w+=\{\([^)]*\)\s*=>","message":"Inline arrow functions in props cause child re-renders on every render","good":"const handleClick = useCallback(() => {...}, [deps])"},
    {"id":"RC011","severity":"High",  "rule":"Never key={index} in lists","pattern":r"key=\{(?:i|index|idx)\}","message":"key={index} breaks animations and React reconciliation","good":"key={item.id} — always use a stable unique identifier"},
],
"shadcn": [
    {"id":"SC001","severity":"High",  "rule":"DialogTitle required","pattern":r"<DialogContent(?![\s\S]{0,500}DialogTitle)","message":"DialogContent needs DialogTitle — screen readers have no context without it","good":"<DialogTitle>Edit Profile</DialogTitle> inside <DialogHeader>"},
    {"id":"SC002","severity":"High",  "rule":"TooltipProvider at root","pattern":r"<Tooltip[^P]","message":"Wrap app root in <TooltipProvider> — add to app/layout.tsx","good":"<TooltipProvider> in root layout, wrapping children"},
    {"id":"SC003","severity":"High",  "rule":"Toaster in layout not page","pattern":r"export default function.*Page[\s\S]{0,500}<Toaster","message":"<Toaster> belongs in root layout, not individual pages"},
    {"id":"SC004","severity":"Medium","rule":"Use variant not conditional className","pattern":r'<Button className=\{[^}]*\?[^}]*:[^}]*\}',"message":"Use variant='destructive' not conditional className","good":"<Button variant='destructive'>"},
    {"id":"SC005","severity":"High",  "rule":"FormMessage after FormControl","pattern":r"<FormControl>[\s\S]{0,200}</FormControl>(?![\s\S]{0,50}<FormMessage)","message":"<FormMessage /> must follow <FormControl> to display Zod validation errors"},
    {"id":"SC006","severity":"High",  "rule":"asChild for Button-as-Link","pattern":r"<Button[^>]*>[^<]*<(?:Link|a)\s","message":"Nested button/anchor is invalid HTML — use asChild","good":"<Button asChild><Link href='/'>Go</Link></Button>"},
    {"id":"SC007","severity":"Medium","rule":"SelectItem needs value prop","pattern":r"<SelectItem[^>]*>(?![^<]*value=)","message":"<SelectItem> requires value prop for form binding to work"},
    {"id":"SC008","severity":"High",  "rule":"Table needs accessible label","pattern":r"<Table>(?![\s\S]{0,200}caption|aria-label)","message":"Add aria-label to <Table> for screen reader context"},
    {"id":"SC009","severity":"Medium","rule":"Sheet needs SheetTitle","pattern":r"<SheetContent(?![\s\S]{0,300}SheetTitle)","message":"<SheetContent> needs <SheetTitle> for screen reader context"},
    {"id":"SC010","severity":"High",  "rule":"Zod resolver for forms","pattern":r"<Form\s(?![\s\S]{0,300}zodResolver)","message":"shadcn Form must use zodResolver for validation","good":"resolver: zodResolver(schema) in useForm()"},
],
"tailwind": [
    {"id":"TW001","severity":"High",  "rule":"No hardcoded hex in className","pattern":r'className=["\'][^"\']*#[0-9A-Fa-f]{6}',"message":"Use CSS variables or Tailwind tokens — never hex in className","good":"bg-[var(--color-primary)] or bg-primary"},
    {"id":"TW002","severity":"High",  "rule":"Focus state replacement","pattern":r"focus:outline-none(?![\s\S]{0,60}focus:ring)","message":"Never remove focus outline without adding focus:ring replacement","good":"focus:outline-none focus-visible:ring-2 focus-visible:ring-primary"},
    {"id":"TW003","severity":"High",  "rule":"Reduced motion required","pattern":r"animate-(?!none)[a-z-]+(?![^\n]*motion-reduce)","message":"Add motion-reduce:animate-none alongside all animation classes","good":"animate-pulse motion-reduce:animate-none"},
    {"id":"TW004","severity":"Medium","rule":"Tailwind v4 gradient syntax","pattern":r"bg-gradient-to-","message":"Tailwind v4: use bg-linear-to-r/l/t/b instead of bg-gradient-to-*","good":"bg-linear-to-r from-blue-500 to-purple-500"},
    {"id":"TW005","severity":"High",  "rule":"Min 44px touch targets","pattern":r"(?:h-6|h-7|h-8|h-\[2\d+px\])\s+(?:w-6|w-7|w-8)","message":"Interactive elements need min 44px height for mobile accessibility","good":"min-h-[44px] min-w-[44px] on all buttons and links"},
    {"id":"TW006","severity":"Medium","rule":"Transition on hover states","pattern":r"hover:(?:bg|text|border|opacity)-[a-z0-9-]+(?![^\n]*transition)","message":"Add transition class when using hover color changes","good":"transition-colors duration-150 alongside hover: classes"},
    {"id":"TW007","severity":"Medium","rule":"cursor-pointer on clickable","pattern":r'<(?:button|a|div[^>]*onClick)[^>]+className=["\'][^"\']*(?<!cursor-pointer)["\']',"message":"Add cursor-pointer to all clickable elements"},
    {"id":"TW008","severity":"High",  "rule":"@theme not tailwind.config in v4","pattern":r"tailwind\.config\.(js|ts).*theme\.extend","message":"Tailwind v4: use @theme {} in globals.css, not tailwind.config.ts extend","good":"@theme { --color-primary: #6366F1; } in globals.css"},
    {"id":"TW009","severity":"Medium","rule":"CSS vars not raw color scale","pattern":r"(?:bg|text|border)-(?:zinc|gray|slate)-\d{3}(?![^\n]*var)","message":"Prefer CSS token variables over raw Tailwind color scale for theming","good":"bg-[var(--color-surface)] instead of bg-zinc-900"},
    {"id":"TW010","severity":"Medium","rule":"font-heading for display text","pattern":r"font-sans(?=[^\n]*(?:h1|h2|heading|display|font-bold))","message":"Use font-heading class for headings, font-body for body text","good":"<h1 className='font-heading font-bold'>"},
    {"id":"TW011","severity":"High",  "rule":"overflow-hidden on scale transforms","pattern":r"(?:hover:scale|group-hover:scale)(?![\s\S]{0,100}overflow-hidden)","message":"Scale transforms need overflow-hidden on parent to prevent layout bleed","good":"<div class='overflow-hidden'><Card class='hover:scale-[1.02]'>"},
    {"id":"TW012","severity":"Medium","rule":"8px spacing system","pattern":r"(?:p|m|gap|space)-\[(?:3|5|7|9|11|13|15|17|19|21|22|23|25|26)px\]","message":"Use 8px grid: 4,8,12,16,24,32,48,64px — odd values break rhythm","good":"p-4 (16px) p-6 (24px) p-8 (32px) — consistent spatial rhythm"},
],
"vue": [
    {"id":"VU001","severity":"High",  "rule":"No v-if + v-for same element","pattern":r"v-for.*v-if|v-if.*v-for","message":"v-if has higher priority than v-for — use <template v-for>","good":"<template v-for='item in items'><div v-if='item.visible'>"},
    {"id":"VU002","severity":"High",  "rule":"Key with v-for","pattern":r"v-for(?![\s\S]{0,100}:key=)","message":"Always provide :key when using v-for","good":":key='item.id'"},
    {"id":"VU003","severity":"High",  "rule":"No prop mutation","pattern":r"props\.\w+\s*=","message":"Never mutate props directly — emit events to parent","good":"emit('update:modelValue', newVal)"},
    {"id":"VU004","severity":"High",  "rule":"storeToRefs for Pinia","pattern":r"const \{ \w+ \} = use\w+Store\(\)(?![\s\S]{0,200}storeToRefs)","message":"Use storeToRefs() when destructuring Pinia store to preserve reactivity"},
    {"id":"VU005","severity":"High",  "rule":"onUnmounted cleanup","pattern":r"(window\.addEventListener|setInterval|subscribe)\((?![\s\S]{0,500}onUnmounted)","message":"Add onUnmounted cleanup for listeners and subscriptions"},
    {"id":"VU006","severity":"High",  "rule":"Suspense for async components","pattern":r"defineAsyncComponent\((?![\s\S]{0,300}Suspense)","message":"Wrap async components with <Suspense> in Nuxt","good":"<Suspense><AsyncComponent /></Suspense>"},
    {"id":"VU007","severity":"Medium","rule":"useHead for Nuxt SEO","pattern":r"export default defineComponent(?![\s\S]{0,300}useHead|useSeoMeta)","message":"Use useHead() or useSeoMeta() for page-level meta in Nuxt","good":"useHead({ title: 'Page Title' })"},
    {"id":"VU008","severity":"High",  "rule":"watch deep option for objects","pattern":r"watch\(\s*\w+,(?![\s\S]{0,100}deep:\s*true)[^)]+\)","message":"Watching reactive objects needs deep: true or use watchEffect","good":"watch(obj, handler, { deep: true })"},
],
"svelte": [
    {"id":"SV001","severity":"High",  "rule":"Reassign arrays not mutate","pattern":r"\w+\.push\(|\w+\.splice\(","message":"Mutation doesn't trigger Svelte reactivity — reassign the array","good":"items = [...items, newItem]"},
    {"id":"SV002","severity":"High",  "rule":"Keys in {#each}","pattern":r"\{#each \w+ as \w+\}(?!\s*\()","message":"Always provide key in {#each} blocks","good":"{#each items as item (item.id)}"},
    {"id":"SV003","severity":"High",  "rule":"SvelteKit: load not onMount","pattern":r"onMount.*fetch\(","message":"Use load() in +page.js/+page.server.js for data fetching","good":"export const load = async ({ fetch }) => ({ data: await fetch(...) })"},
    {"id":"SV004","severity":"High",  "rule":"Reactive declarations for derived","pattern":r"let \w+ = (?!\$:)[^\n]+(?:\w+\.\w+|\+|-|\*)","message":"Derived values need $: reactive declaration","good":"$: total = price * quantity"},
    {"id":"SV005","severity":"High",  "rule":"SvelteKit form actions","pattern":r"<form[^>]+method=[^>]*POST(?![\s\S]{0,300}use:enhance)","message":"Add use:enhance to SvelteKit forms for progressive enhancement","good":"<form method='POST' use:enhance>"},
],
"framer": [
    {"id":"FM001","severity":"High",  "rule":"AnimatePresence for conditional","pattern":r"\{[^}]+&&\s*<motion\.","message":"Wrap conditional motion elements in <AnimatePresence> for exit animations","good":"<AnimatePresence>{show && <motion.div key='modal'>}"},
    {"id":"FM002","severity":"Medium","rule":"layout prop for size changes","pattern":r"<motion\.[a-z]+(?![^>]*layout)[^>]*(?:className|style)=[^>]*(?:h-|w-|height|width)","message":"Add layout prop to motion elements that change size/position","good":"<motion.div layout>"},
    {"id":"FM003","severity":"High",  "rule":"Key on AnimatePresence child","pattern":r"<AnimatePresence>[\s\S]{0,100}<motion\.[a-z]+(?![^>]*key=)","message":"AnimatePresence children need unique key prop for exit animation to work","good":"<motion.div key={modalId}>"},
    {"id":"FM004","severity":"High",  "rule":"Reduced motion support","pattern":r"<motion\.[a-z]+(?![^>]*useReducedMotion|motion-reduce)","message":"Add useReducedMotion() check or CSS prefers-reduced-motion fallback","good":"const prefersReduced = useReducedMotion(); y: prefersReduced ? 0 : 20"},
    {"id":"FM005","severity":"Medium","rule":"No linear easing for discrete","pattern":r"ease:\s*linear\b(?![\s\S]{0,80}(?:spin|pulse|loop|continuous|infinite))","message":"Never linear easing for discrete UI — use ease-out minimum","good":"ease: [0.16, 1, 0.3, 1] for entrances, [0.5, 0, 1, 1] for exits"},
    {"id":"FM006","severity":"Medium","rule":"Duration over 600ms for UI","pattern":r"duration:\s*0\.[7-9]|duration:\s*[1-9]\d*\.","message":"UI animation >700ms feels sluggish — max 600ms for cinematic hero","good":"duration: 0.4 (normal) | 0.15 (hover) | 0.6 (hero cinematic max)"},
    {"id":"FM007","severity":"High",  "rule":"Use variants for staggered lists","pattern":r"staggerChildren(?![\s\S]{0,200}variants)","message":"Define parent + child variants when using staggerChildren","good":"variants={{ container: { visible: { staggerChildren: 0.05 } } }}"},
],
"aceternity": [
    {"id":"AC001","severity":"High",  "rule":"framer-motion required","pattern":r'from ["\'].*aceternity|components/aceternity',"message":"Aceternity components require framer-motion — npm install framer-motion"},
    {"id":"AC002","severity":"Medium","rule":"cn() utility required","pattern":r'from ["\'].*aceternity',"message":"Ensure cn() utility (clsx + tailwind-merge) exists at @/lib/utils","good":"import { cn } from '@/lib/utils'"},
],
"magicui": [
    {"id":"MU001","severity":"Medium","rule":"framer-motion required","pattern":r'from ["\'].*magicui|@/components/magicui',"message":"Most Magic UI components require framer-motion","good":"npm install framer-motion"},
    {"id":"MU002","severity":"High",  "rule":"ShimmerButton on dark only","pattern":r"<ShimmerButton(?![\s\S]{0,200}dark|bg-\[#0|bg-zinc)","message":"ShimmerButton is designed for dark backgrounds — use RainbowButton for light","good":"Use RainbowButton on light backgrounds instead"},
],
"react_bits": [
    {"id":"RB001","severity":"High",  "rule":"Aurora dark background only","pattern":r"<Aurora(?![\s\S]{0,200}dark|bg-\[#0|bg-zinc-9)","message":"Aurora is invisible on light backgrounds — dark bg required","good":"Only use Aurora on backgrounds like #09090B"},
    {"id":"RB002","severity":"Medium","rule":"Wrap sections with FadeContent","pattern":r"<(?:section|article)[^>]*>(?![\s\S]{0,200}FadeContent)","message":"Wrap sections in <FadeContent> for consistent scroll-triggered entrances"},
    {"id":"RB003","severity":"High",  "rule":"One statement component per section","pattern":r"(?:<Aurora|<Particles|<Silk)[\s\S]{0,500}(?:<Aurora|<Particles|<Silk)","message":"Multiple hero background components compete and cancel each other out","good":"One statement bg per section — Aurora OR Particles OR Silk, not all"},
    {"id":"RB004","severity":"Medium","rule":"TS+TW variant for Next.js","pattern":r'reactbits\.dev/r/[A-Za-z]+-(?!TS)',"message":"Use TS+TW variant for TypeScript + Tailwind projects","good":"npx shadcn@latest add 'https://reactbits.dev/r/Aurora-TS-TW'"},
],
"tremor": [
    {"id":"TR001","severity":"High",  "rule":"Tremor chart needs ResponsiveContainer","pattern":r"<(?:AreaChart|BarChart|LineChart|DonutChart)(?![^>]*className)","message":"Wrap Tremor charts in a sized container div","good":"<div className='h-72'><AreaChart ... /></div>"},
    {"id":"TR002","severity":"Medium","rule":"Tremor: always provide categories","pattern":r"<AreaChart(?![^>]*categories)","message":"Tremor charts require categories prop for multi-series data"},
],
"animata": [
    {"id":"AN001","severity":"High",  "rule":"SplashCursor needs pointer-events-none parent","pattern":r"<SplashCursor(?![\s\S]{0,200}pointer-events-none)","message":"SplashCursor must be in a pointer-events-none container to avoid blocking clicks","good":"<div className='pointer-events-none fixed inset-0'><SplashCursor /></div>"},
    {"id":"AN002","severity":"High",  "rule":"ImageTrail needs overflow-hidden","pattern":r"<ImageTrail(?![\s\S]{0,200}overflow-hidden)","message":"Wrap ImageTrail in overflow-hidden container to prevent page overflow"},
    {"id":"MP001","severity":"Medium","rule":"MorphingDialog needs shared layoutId","pattern":r"<MorphingDialog(?![\s\S]{0,300}layoutId)","message":"MorphingDialog requires matching layoutId on trigger and dialog for morph animation"},
],
"general": [
    {"id":"GN001","severity":"High",  "rule":"No console.log in production","pattern":r"console\.log\(","message":"Remove all console.log statements before shipping"},
    {"id":"GN002","severity":"Medium","rule":"No TODO/FIXME in shipped code","pattern":r"//\s*(TODO|FIXME|HACK|XXX)","message":"Resolve all TODOs before shipping to production"},
    {"id":"GN003","severity":"High",  "rule":"No hardcoded secrets","pattern":r'(?:password|secret|api[_-]?key|token)\s*[=:]\s*["\'][^"\']{8,}',"message":"Never hardcode secrets in source code — use environment variables"},
    {"id":"GN004","severity":"High",  "rule":"ARIA labels on icon buttons","pattern":r"<button[^>]*>[\s\n]*<(?:svg|Lucide|Icon)(?![^>]*aria)","message":"Icon-only buttons need aria-label for screen readers","good":"<button aria-label='Delete item'>"},
    {"id":"GN005","severity":"Medium","rule":"Avoid layout-shifting hover","pattern":r"hover:scale-(?:105|110)\s+(?!.*[^h])","message":"scale-105 on block elements causes layout shift — use overflow-hidden on parent"},
],
}

def lint_code(code, frameworks):
    issues = []
    rule_sets = list(set(frameworks + ["general"]))
    for fw in rule_sets:
        for rule in LINT_RULES.get(fw, []):
            if re.search(rule["pattern"], code, re.IGNORECASE | re.MULTILINE):
                issues.append({
                    "id": rule["id"], "framework": fw,
                    "severity": rule["severity"],
                    "rule": rule["rule"],
                    "message": rule["message"],
                    "fix": rule.get("good","")
                })
    return sorted(issues, key=lambda x: {"High":0,"Medium":1,"Low":2}[x["severity"]])

def lint_file(filepath, frameworks):
    path = Path(filepath)
    if not path.exists():
        print(f"  Warning: File not found: {filepath}")
        return []
    return lint_code(path.read_text(errors="ignore"), frameworks)

def detect_frameworks_from_file(filepath):
    """Auto-detect frameworks from file content."""
    try:
        code = Path(filepath).read_text(errors="ignore")
        frameworks = ["react", "general"]
        if "next/" in code or "from 'next" in code:  frameworks.append("nextjs")
        if "shadcn" in code or "@/components/ui" in code: frameworks.append("shadcn")
        if "tailwind" in code.lower() or "className=" in code: frameworks.append("tailwind")
        if "framer-motion" in code or "from 'motion'" in code: frameworks.append("framer")
        if "aceternity" in code: frameworks.append("aceternity")
        if "magicui" in code: frameworks.append("magicui")
        if "reactbits" in code: frameworks.append("react_bits")
        if "defineComponent" in code or "v-for" in code: frameworks.append("vue")
        if "{#each" in code: frameworks.append("svelte")
        return list(set(frameworks))
    except Exception:
        return ["react", "general"]

def print_issues(issues, filename=""):
    if not issues:
        print(f"  ✅ No issues{' in '+filename if filename else ''}")
        return
    high = [i for i in issues if i["severity"]=="High"]
    med  = [i for i in issues if i["severity"]=="Medium"]
    label = f" in {filename}" if filename else ""
    print(f"\n  Found {len(issues)} issue(s){label}:")
    print(f"  🔴 High: {len(high)}  🟡 Medium: {len(med)}\n")
    for issue in issues:
        icon = {"High":"🔴","Medium":"🟡","Low":"🔵"}[issue["severity"]]
        print(f"  {icon} [{issue['id']}] [{issue['framework']}] {issue['rule']}")
        print(f"     {issue['message']}")
        if issue.get("fix"):
            print(f"     ✓ Fix: {issue['fix']}")
        print()

def main():
    parser = argparse.ArgumentParser(description="Framework Lint v3.0")
    parser.add_argument("file",          nargs="?",       help="File to lint")
    parser.add_argument("--framework",   "-f",            help="Comma-separated frameworks")
    parser.add_argument("--stack-check", action="store_true", help="Scan entire project")
    parser.add_argument("--code",        "-c",            help="Lint raw code string")
    args = parser.parse_args()

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║        FRAMEWORK LINT CHECK v3.0                   ║")
    print("╚══════════════════════════════════════════════════════╝\n")

    # Determine frameworks
    if args.framework:
        frameworks = [f.strip() for f in args.framework.split(",")]
    elif args.stack_check or args.file:
        try:
            result = subprocess.run(
                ["python3", str(Path(__file__).parent/"detect_stack.py")],
                capture_output=True, text=True, cwd=Path.cwd())
            frameworks = ["react","general"]
            for line in result.stdout.split("\n"):
                if line.startswith("STACK_JSON:"):
                    stack = json.loads(line[11:])
                    frameworks = stack.get("guidelines", ["react"])
                    if stack.get("has_framer"):     frameworks.append("framer")
                    if stack.get("has_aceternity"): frameworks.append("aceternity")
                    if stack.get("has_magicui"):    frameworks.append("magicui")
                    if stack.get("has_react_bits"): frameworks.append("react_bits")
                    break
        except Exception:
            frameworks = ["react","general"]
        if args.file:
            frameworks = list(set(frameworks + detect_frameworks_from_file(args.file)))
    else:
        frameworks = ["react","general"]

    if args.code:
        print_issues(lint_code(args.code, frameworks))

    elif args.file:
        print(f"  File: {args.file}")
        print(f"  Frameworks: {', '.join(frameworks)}\n")
        print_issues(lint_file(args.file, frameworks), args.file)

    elif args.stack_check:
        root = Path.cwd()
        exts = {".tsx",".ts",".jsx",".js",".svelte",".vue"}
        all_issues = []
        checked = 0
        for src in ["src","app","components","pages","lib"]:
            sp = root/src
            if not sp.exists(): continue
            for ext in exts:
                for f in sp.rglob(f"*{ext}"):
                    if "node_modules" in str(f) or ".next" in str(f): continue
                    fw = list(set(frameworks + detect_frameworks_from_file(str(f))))
                    issues = lint_file(str(f), fw)
                    if issues:
                        print(f"  📄 {f.relative_to(root)}")
                        print_issues(issues, str(f.relative_to(root)))
                        all_issues.extend(issues)
                    checked += 1
        high_count = len([i for i in all_issues if i["severity"]=="High"])
        print(f"  ═══════════════════════════════════════════════════")
        print(f"  Files: {checked}  |  Total issues: {len(all_issues)}  |  🔴 High: {high_count}")
        if not high_count:
            print("  ✅ No high-severity issues found")
    else:
        total = sum(len(v) for v in LINT_RULES.values())
        print(f"  {total} rules across {len(LINT_RULES)} frameworks\n")
        print("  Usage:")
        print("  python3 framework_lint.py MyComponent.tsx")
        print("  python3 framework_lint.py --stack-check")
        print("  python3 framework_lint.py --code '<img src=x>' --framework nextjs")
        print(f"\n  Frameworks: {', '.join(LINT_RULES.keys())}")

if __name__ == "__main__":
    main()
