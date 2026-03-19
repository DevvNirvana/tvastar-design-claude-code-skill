# Charts & Icons Reference

> Read when building dashboards, data visualization, or any icon usage.

---

# Chart Type Selection Guide

## Quick Decision Matrix

| Your Data | Best Chart | Library | Key Rule |
|-----------|-----------|---------|----------|
| Trend over time | Line / Area | Recharts | Primary #0080FF, distinct colors per series |
| Compare categories | Bar (horizontal if labels long) | Recharts, Chart.js | Sort descending, label bars |
| Part-to-whole (≤6) | Donut | Recharts | Max 6 slices, label largest first |
| Part-to-whole (>6) | Stacked Bar | Recharts | Pie gets unreadable above 6 |
| Correlation | Scatter | Recharts, Plotly | Opacity 0.6-0.8 for density |
| Geo data | Choropleth | D3, Mapbox | Single gradient + legend |
| KPI vs target | Gauge / Bullet | ApexCharts, D3 | Red→Yellow→Green, mark target |
| Conversion funnel | Funnel | Recharts, D3 | Show % per stage |
| Realtime / streaming | Canvas area chart | CanvasJS | Never SVG at 60fps |
| Hierarchy | Treemap / Sunburst | D3 | White 2px borders between items |
| Network / connections | Network Graph | D3-force, Cytoscape | Falls apart >500 nodes |
| Financial OHLC | Candlestick | TradingView Lightweight | Bullish #26A69A / Bearish #EF5350 |

---

## Color Guidance by Chart Type

### Single-series Charts
```
Primary line/bar: #0080FF
Success/positive:  #10B981
Warning:           #F59E0B
Danger/negative:   #EF4444
```

### Multi-series — Distinct Palette
```
Series 1: #2563EB  (blue)
Series 2: #7C3AED  (violet)
Series 3: #059669  (green)
Series 4: #D97706  (amber)
Series 5: #DC2626  (red)
Series 6: #0891B2  (cyan)
```

### Sequential (low → high)
```
Light → Dark of one hue, e.g.:
#DBEAFE → #1E40AF  (blue scale)
#D1FAE5 → #065F46  (green scale)
```

### Diverging (negative ↔ positive)
```
#EF4444 (red) → #F9FAFB (white) → #10B981 (green)
```

---

## Recharts (React — Most Common)

```tsx
import {
  LineChart, Line, BarChart, Bar, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, PieChart, Pie, Cell,
} from 'recharts'

// Line Chart
<ResponsiveContainer width="100%" height={300}>
  <LineChart data={data}>
    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
    <XAxis dataKey="date" tick={{ fontSize: 12, fill: '#6B7280' }} />
    <YAxis tick={{ fontSize: 12, fill: '#6B7280' }} />
    <Tooltip contentStyle={{ borderRadius: '8px' }} />
    <Legend />
    <Line
      type="monotone"
      dataKey="applications"
      stroke="#2563EB"
      strokeWidth={2}
      dot={false}
      activeDot={{ r: 6 }}
    />
  </LineChart>
</ResponsiveContainer>

// Donut Chart
const COLORS = ['#2563EB', '#7C3AED', '#059669', '#D97706', '#DC2626']
<PieChart>
  <Pie
    data={data}
    cx="50%"
    cy="50%"
    innerRadius={60}
    outerRadius={80}
    paddingAngle={4}
    dataKey="value"
  >
    {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
  </Pie>
  <Tooltip />
  <Legend />
</PieChart>
```

## shadcn Chart (Recharts wrapper)
```tsx
import { ChartContainer, ChartTooltip, ChartTooltipContent } from '@/components/ui/chart'

const chartConfig = {
  applications: { label: 'Applications', color: '#2563EB' },
  interviews: { label: 'Interviews', color: '#7C3AED' },
}

<ChartContainer config={chartConfig} className="h-[300px]">
  <BarChart data={data}>
    <Bar dataKey="applications" fill="var(--color-applications)" radius={4} />
    <Bar dataKey="interviews" fill="var(--color-interviews)" radius={4} />
    <ChartTooltip content={<ChartTooltipContent />} />
  </BarChart>
</ChartContainer>
```

---

## Accessibility for Charts

```tsx
// Always provide data table alternative
<div role="img" aria-label="Monthly applications: Jan 45, Feb 62, Mar 58...">
  <BarChart ... />
</div>

// For colorblind users — add patterns or labels
<Bar label={{ position: 'top', fontSize: 11 }} />

// Caption
<figure>
  <BarChart ... />
  <figcaption className="text-sm text-muted-foreground text-center mt-2">
    Application trends over the last 6 months
  </figcaption>
</figure>
```

---

# Icons Reference (Lucide React)

## Installation
```bash
npm install lucide-react  # already included with shadcn
```

## Usage Pattern
```tsx
import { Search, Bell, User, Settings, Plus, Trash2, Edit, ArrowLeft } from 'lucide-react'

// Default sizing
<Search className="size-4" />       // 16px — inside inputs, small UI
<Bell className="size-5" />         // 20px — nav icons
<User className="size-6" />         // 24px — feature icons

// With color
<CheckCircle className="size-5 text-green-500" />
<AlertTriangle className="size-5 text-yellow-500" />
<XCircle className="size-5 text-red-500" />

// Loading spinner
<Loader className="size-5 animate-spin" />

// Icon button — always aria-label!
<button
  onClick={handleDelete}
  aria-label="Delete item"
  className="p-2 rounded-md hover:bg-destructive/10 transition-colors"
>
  <Trash2 className="size-4 text-destructive" />
</button>
```

## Common UI Patterns → Icon

| UI Element | Icon | Import |
|------------|------|--------|
| Mobile nav toggle | Menu | `Menu` |
| Back navigation | Arrow | `ArrowLeft` |
| Close / dismiss | X | `X` |
| Add / create | Plus | `Plus` |
| Delete | Trash | `Trash2` |
| Edit | Pencil | `Edit` or `Pencil` |
| Search | Magnifier | `Search` |
| Filter / sort | Funnel | `Filter` |
| Settings / prefs | Gear | `Settings` |
| Success / done | Check | `Check` or `CheckCircle` |
| Error / fail | X circle | `XCircle` |
| Warning | Triangle | `AlertTriangle` |
| Info | Circle i | `Info` |
| Loading | Spinner | `Loader` (+ `animate-spin`) |
| Notifications | Bell | `Bell` |
| User / account | Person | `User` |
| Team / members | People | `Users` |
| Email | Envelope | `Mail` |
| Chat | Bubble | `MessageCircle` |
| Calendar / date | Calendar | `Calendar` |
| Location | Pin | `MapPin` |
| Link / URL | Chain | `Link` |
| Download | Arrow down | `Download` |
| Upload | Arrow up | `Upload` |
| Copy | Clipboard | `Copy` |
| Show password | Eye | `Eye` / `EyeOff` |
| Lock / secure | Padlock | `Lock` / `Unlock` |
| Analytics | Bar chart | `BarChart2` |
| Trend up | Arrow up | `TrendingUp` |
| Trend down | Arrow down | `TrendingDown` |
| Star / favorite | Star | `Star` |
| Bookmark | Bookmark | `Bookmark` |
| Share | Arrow up-right | `Share2` |
| Refresh | Rotate | `RefreshCw` |
| Undo | Rotate CCW | `RotateCcw` |
| Fullscreen | Expand | `Maximize` |

## Sizing Convention
```tsx
// Consistent size scale
const iconSizes = {
  xs:  'size-3',   // 12px — tiny badges, tight UI
  sm:  'size-4',   // 16px — default for most inline icons
  md:  'size-5',   // 20px — nav bar, action buttons
  lg:  'size-6',   // 24px — feature highlights, empty states
  xl:  'size-8',   // 32px — hero areas, large empty states
  '2xl': 'size-12', // 48px — illustrations
}
```

---

## Docs
- [Lucide Icons](https://lucide.dev/icons/) — searchable catalog
- [Recharts](https://recharts.org/en-US/)
- [shadcn Charts](https://ui.shadcn.com/docs/components/chart)
- [D3.js](https://d3js.org/)
