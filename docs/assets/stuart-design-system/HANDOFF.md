# Stuart Design System — Claude Code handoff

This file describes the **Stuart** brand + UI design system so you can build pixel-accurate
Stuart-branded UI in any codebase (React, Vue, SwiftUI, plain HTML, etc.).

**Stuart** is a European last-mile delivery platform. Businesses connect a shop, warehouse or
restaurant to Stuart's network of couriers (bike, moped, car, van, cargo-bike) to deliver goods
A→B in under an hour, or same-day / scheduled. Markets: UK, France, Poland, Spain, other EU.

> **How to use this bundle.** `css/` holds the production stylesheets — link `css/styles.css`
> and you get every token + component class below. `fonts/` holds the GT Walsheim family. The
> token values and component specs are also written out in full here so you can port them to
> Tailwind config, CSS-in-JS, design tokens, native styles, etc. **Recreate** these in the
> target codebase's own patterns — don't ship the raw CSS if the project has its own system.

---

## 1. Brand voice & content rules

- **Voice:** confident, warm, operational. B2B logistics partner — reliable, fast, network-scale,
  but friendly. Not a consumer food-delivery app.
- **Person:** "you" to merchants; "we / our" as Stuart. Never first-person singular.
- **Casing:** **sentence case for everything** — headings, buttons, nav, labels. ("Sign up to
  start shipping", "Get started", "Already have an account? Log in".) ALL-CAPS only on map captions
  stamped on imagery and physical courier kit — never in UI.
- **CTAs are verbs:** "Get started", "Log in", "Book a delivery".
- **Numeric & specific** when it helps ("60 min instant delivery", "7am–12pm, 7 days a week").
  Avoid superlatives and startup clichés.
- **No emoji. No unicode glyphs as icons.** Stuart's expressive vocabulary is its **branded
  circular icons** and the **green dot**.

### The dot 🟢 (most distinctive brand element)
A solid Stuart Green circle sits to the right of the "stuart" wordmark. It recurs as map pins,
active-nav indicators, checkpoint markers, success confirmations. *When in doubt, add a dot.*

---

## 2. Design tokens

All tokens are CSS custom properties in `css/colors_and_type.css`. Raw values below.

### Color — primaries (do 90% of the work)
| Token | Hex | Use |
|---|---|---|
| `--stuart-dark-blue` | `#00249c` | Headings, deep panels, primary button |
| `--stuart-blue` | `#0192ff` | Signature surface, CTA hover, links, chrome |
| `--stuart-green` | `#27e2a5` | Accent — **sparingly**, almost always a dot / success |

### Color — secondaries (illustration & internal/courier comms only — never background floods)
| Token | Hex |
|---|---|
| `--stuart-yellow` | `#ffcc36` |
| `--stuart-magenta` | `#ff4d73` |
| `--stuart-purple` | `#4755ff` |
| `--stuart-light-blue` | `#87eaff` |

### Color — neutral & semantic
- `--stuart-white: #ffffff` — the only neutral. **Brand rule: never reduce the opacity of any
  brand color.** All tone comes from brand colors at 100%.
- Surfaces: `--surface-page #fff`, `--surface-inverse → dark-blue`, `--surface-brand → blue`.
- Foreground: `--fg-1 → dark-blue` (primary text), `--fg-2 → blue` (secondary/links),
  `--fg-on-brand #fff`, `--fg-link → blue`.
- Borders: `--border-subtle → blue`, `--border-strong → dark-blue`.
- Status: `--success → green`, `--positive → yellow`, `--attention → magenta`,
  `--info → blue`, `--info-alt → dark-blue`.

### Typography
- **Family:** **GT Walsheim** everywhere (geometric sans, circular terminals, warm). Tokens:
  `--font-display`, `--font-body`. Files in `fonts/` (Thin 100 → Black 900, + obliques).
- **Fallback:** `--font-fallback: "Poppins", ui-sans-serif, system-ui, sans-serif`. Poppins is the
  substitute when GT Walsheim isn't available (Google Slides, 3rd-party). **Never mix the two.**
- **Weights:** `--fw-regular 400`, `--fw-medium 500`, `--fw-bold 700`, `--fw-black 900`.
- **Type scale (px):** `--fs-display 88`, `--fs-h1 56`, `--fs-h2 40`, `--fs-h3 28`, `--fs-h4 20`,
  `--fs-body-lg 18`, `--fs-body 16`, `--fs-body-sm 14`, `--fs-caption 12`.
- **Line-height:** `--lh-tight 1.05`, `--lh-snug 1.2`, `--lh-normal 1.5`, `--lh-relaxed 1.65`.
- **Tracking:** `--tracking-tight -0.02em`, `--tracking-normal 0`, `--tracking-wide 0.04em`.
- **Hierarchy:** Headline = Black/Bold, tight tracking + leading. Subline = Bold/Medium.
  Body = Medium/Regular. Annotation = Regular **Oblique** (italic). Button = Medium.

### Spacing — 4 / 8 grid
`--sp-1 4` · `--sp-2 8` · `--sp-3 12` · `--sp-4 16` · `--sp-5 24` · `--sp-6 32` · `--sp-7 48` ·
`--sp-8 64` · `--sp-9 96` · `--sp-10 128` (all px).

### Radii — Stuart uses only two in UI
- `--radius-sm: 8px` (containers, inputs) · `--radius-pill: 999px` (buttons, chips, lockups).
- Marketing/hero shapes go larger: cards `20px`, hero panels `28px`, hero blobs `40px`.

### Shadows — cool blue-tinted, never black
- `--shadow-xs: 0 1px 2px rgba(10,20,60,.06)`
- `--shadow-sm: 0 4px 12px rgba(10,20,60,.08)`
- `--shadow-md: 0 10px 24px rgba(10,20,60,.10)`
- `--shadow-lg: 0 24px 48px rgba(10,20,60,.14)`
- Hover brand-lift: `0 12px 28px rgba(1,146,255,.28)`. No inner shadows.

### Motion
- `--ease-out: cubic-bezier(.2,.8,.2,1)` · `--ease-spring: cubic-bezier(.34,1.35,.64,1)`.
- `--dur-fast 120ms` · `--dur-base 200ms` · `--dur-slow 360ms`.
- Calm & short. `200ms` ease-out for state changes; spring for feedback (green dot pop, button
  settle). No parallax, no long scroll animations, no aggressive bounces.

---

## 3. Components (classes in `css/components.css`)

**Button** `.btn` + `.btn--primary | --secondary | --ghost`, sizes `.btn--sm | --lg`, `[disabled]`.
Pill-shaped, uppercase, `0.06em` tracking, Medium/Bold weight. Primary = dark-blue fill →
**hover lightens to Stuart Blue** (note: hover gets *lighter*, not darker). Active `scale(.98)`.
Focus = 3px blue ring at 40% alpha, 2px offset.

**Input** `.field` > `.field__label` (uppercase, bold, dark-blue) + `.input`/`.field__input` +
`.field__hint` (italic). Input: 1.5px blue border, `8px` radius, hover→dark-blue border,
focus→dark-blue border + 3px blue glow. Validation hints sit under the field in Regular-Oblique.

**Chip** `.chip` + `--dark | --green | --outline`, optional `.chip__dot`. Pill, uppercase, bold.

**Badge** `.badge` + `--success | --info | --info-alt | --attention`. Pill, caption size, uppercase.

**Card** `.card` + `--hoverable | --brand | --dark`. White, `8px` radius, `--shadow-sm`, `24px`
padding. Hoverable lifts 2px to `--shadow-md`.

**Icon tile** `.icon-tile` + `--dark | --green`. 64px circle, brand fill, white line art inside.

**Blob** `.blob` (organic `border-radius: 60% 40% 55% 45% / 50% 55% 45% 50%`) / `.blob--pill`.
Signature organic shape framing photography / illustration.

### States (apply consistently)
- Hover primary button: lighten to Stuart Blue + blue shadow, no movement.
- Hover card: lift 2px, strengthen shadow.
- Press: `scale(0.98)`, shadow flattens.
- Focus: 3px Stuart Blue ring @30% alpha, 2px offset.
- Disabled: 40% opacity, no pointer.
- Active nav: Stuart Blue label + 2px green dot to its right.

---

## 4. Backgrounds (pick ONE per surface)
1. **Flat Stuart Blue flood** `#0192ff` edge-to-edge, white type, white-line circular icons —
   dominant marketing/hero.
2. **White with color blobs** — white base + organic Stuart-Blue blobs framing photo/illustration.
3. **Light grey dashboard** `#f4f5f5` page, white cards with soft shadow — internal product.

**No gradients, no textures, no grain, no stock-photo backgrounds.**

---

## 5. Imagery & iconography
- **Photography:** outdoor/urban daylight, couriers in bright-blue kit, clean cut-outs on color
  blobs. Saturated, warm skin, cool sky — never desaturated or b&w.
- **Isometric illustrations** (signature): blue flood, 2–3px white strokes, green fills as the one
  accent. Marketing/corporate only.
- **Character illustrations** (cartoon couriers): internal & courier comms only, never client UI.
- **Branded icon set:** circular tile (blue or dark-blue) + flat white line art + a green dot;
  high-res PNG. Use for feature grids, list bullets, empty states.
- **In-UI utility icons** (16/20/24px in buttons, menus, rows): use **Lucide** (2px stroke,
  rounded caps) — the branded PNGs are too heavy at small sizes. This is a substitution; commission
  a custom utility set if you want one.

---

## 6. Layout
- 12-column grid. Max content `1280px` marketing / `1440px` dashboard.
- Fixed top nav 64px, white, `--shadow-xs`.
- Generous vertical rhythm — 96–128px between marketing sections.
- Mobile: single column, 16px gutters, hero stacks illustration-first.
- Transparency/blur is rare — only the glass address cards over maps
  (`rgba(255,255,255,.96)` + `backdrop-filter: blur(8px)`).

---

## 7. Files in this bundle
```
stuart_design_handoff/
├── CLAUDE.md                  this doc (Claude Code auto-reads it)
├── css/
│   ├── styles.css             entry — @imports the two below
│   ├── colors_and_type.css    tokens, @font-face, semantic type styles
│   └── components.css         button / input / chip / badge / card / icon-tile / blob
└── fonts/                     GT Walsheim family (OTF)
```
Link `css/styles.css` once, or port the tokens in §2 into the project's own token system.
