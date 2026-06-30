---
title: "Stuart Design System — brand e UI"
summary: "Token di brand Stuart (colori, GT Walsheim, spaziature, componenti) per UI e presentazioni on-brand."
tags: [docs, stuart, design, brand]
status: active
created: 2026-06-28
updated: 2026-06-28
related: ["[[entity-stuart]]", "[[progetto-ops-dashboard]]", "[[doc-flusso-performance-mensile]]"]
---

# Stuart Design System — brand e UI

Riferimento sintetico del design system Stuart (Brand Guidelines, ott 2025), per costruire UI e
**presentazioni** on-brand. Fonte completa (CSS + font GT Walsheim) archiviata in
`docs/assets/stuart-design-system/`. Applicato la prima volta alla [[progetto-ops-dashboard]].

## Colori

**Primari (fanno il 90% del lavoro):**

| Token | Hex | Uso |
|---|---|---|
| Dark blue | `#00249c` | Testo, pannelli profondi, bottone primario |
| Stuart blue | `#0192ff` | Superficie firma, hover CTA, link, chrome |
| Stuart green | `#27e2a5` | Accento — **con parsimonia**, quasi sempre un dot / success |

**Secondari (illustrazione / accento, mai flood di sfondo):**
yellow `#ffcc36` · magenta `#ff4d73` · purple `#4755ff` · light-blue `#87eaff`

**Neutro:** solo bianco `#ffffff`. **Regola brand: mai ridurre l'opacità dei colori brand** — tutto
il tono viene dai colori a piena intensità.

**Status:** success → green · positive → yellow · attention → magenta · info → blue/dark-blue.
Nota: **il brand non ha il rosso**. Per dati finanziari positivo/negativo uso green (accento) /
magenta (attention).

## Tipografia

- **Font:** **GT Walsheim** ovunque (sans geometrico, terminali circolari). Fallback **Poppins**
  (mai mischiare i due). Pesi: Regular 400, Medium 500, Bold 700, Black 900 (+ obliques).
- **Scala (px):** display 88 · h1 56 · h2 40 · h3 28 · h4 20 · body-lg 18 · body 16 · body-sm 14 · caption 12.
- **Line-height:** tight 1.05 · snug 1.2 · normal 1.5 · relaxed 1.65.
- **Tracking:** tight -0.02em · normal 0 · wide 0.04em.
- **Gerarchia:** titoli Black/Bold, tracking stretto. Corpo Medium/Regular. Annotazioni Regular **corsivo**. Bottoni Medium, uppercase, tracking 0.06em.

## Spaziature, raggi, ombre

- **Spacing** (griglia 4/8 px): 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128.
- **Raggi:** solo due in UI — `8px` (container/input), `999px` pill (bottoni, chip). Marketing: card 20px, hero 28px, blob 40px.
- **Ombre** (blu-fredde, mai nere): xs `0 1px 2px rgba(10,20,60,.06)` · sm `0 4px 12px rgba(10,20,60,.08)` · md `0 10px 24px rgba(10,20,60,.10)` · lg `0 24px 48px rgba(10,20,60,.14)`.
- **Motion:** ease-out `cubic-bezier(.2,.8,.2,1)`, durate 120/200/360ms. Calmo e corto.

## Il dot 🟢 (elemento firma)

Un cerchio pieno Stuart Green a destra del wordmark "stuart". Ricorre come pin mappa, indicatore
nav attivo, marker di checkpoint, conferma di success. *Nel dubbio, aggiungi un dot.*

## Componenti

- **Card:** bianca, raggio 8px, ombra sm, padding 24px; hover = lift 2px + ombra md.
- **Button:** pill, uppercase, tracking 0.06em. Primario = fill dark-blue → **hover schiarisce a Stuart Blue** (non scurisce). Active scale(.98). Focus ring blu 3px @40%.
- **Input:** bordo blu 1.5px, raggio 8px, hover→bordo dark-blue, focus→bordo dark-blue + glow blu.
- **Chip / Badge:** pill, uppercase, bold.
- **Blob:** forma organica firma (`border-radius: 60% 40% 55% 45% / 50% 55% 45% 50%`).

## Sfondi (uno per superficie)

1. Flood Stuart Blue `#0192ff` edge-to-edge — marketing/hero.
2. Bianco con blob organici Stuart Blue.
3. **Dashboard grigio chiaro `#f4f5f5`** + card bianche con ombra soft — **prodotto interno**.

**Niente gradienti, texture, grana, stock-photo.**

## Voce e regole contenuti

- Tono: confident, warm, operational. Partner B2B logistico, non app consumer.
- **Sentence case ovunque** (titoli, bottoni, label). ALL-CAPS solo su didascalie mappa stampate.
- CTA = verbi ("Get started", "Book a delivery"). Numerico e specifico quando aiuta.
- **No emoji, no glifi unicode come icone.** Icone utility in UI: Lucide (stroke 2px). Icone brand: tile circolare + line art bianca + dot verde.

## Layout

Griglia 12 colonne. Max width 1280px marketing / 1440px dashboard. Top nav 64px bianca, ombra xs.
Ritmo verticale generoso (96-128px tra sezioni marketing). Mobile single column, gutter 16px.

## Vedi anche

[[entity-stuart]] — [[progetto-ops-dashboard]] — [[doc-flusso-performance-mensile]]
