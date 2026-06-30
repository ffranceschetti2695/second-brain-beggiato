---
title: "Stato & Next Steps — Stream AI (reporting, dashboard, company brain)"
summary: "Punto di ripartenza dei tre stream AI di Francesco: automazione reporting mensile, OPS GM Dashboard, Company Brain prodotto. Stato al 2026-06-29 + prossimi passi."
tags: [projects, ai, business, stuart]
status: active
created: 2026-06-29
updated: 2026-06-29
related: ["[[progetto-ops-dashboard]]", "[[progetto-company-brain]]", "[[data-fc3-2026-mensile]]", "[[doc-flusso-performance-mensile]]", "[[entity-stuart]]"]
---

# Stato & Next Steps — Stream AI

Nota di handoff: da qui si riparte. Tre stream aperti, come li vede Francesco.

---

## Stream 1 — Automazione del reporting mensile

**Obiettivo:** automatizzare i deliverable di reporting che Francesco produce a mano. Due artefatti, stessa baseline FC3:
- **Slide Company Performance (All-Hands)** — skill `performance` (`.claude/commands/performance.md`): bridge a 7 barre per segmento, Actual (DWH) vs FC3. Procedura in [[doc-flusso-performance-mensile]], teoria in [[concetto-bridge-waterfall]]. Validata su maggio 2026.
- **OPS GM Dashboard** — la web app (vedi Stream 2): bridge a 3 driver (Volume/RPO/CPO) per mercato, settimanale + mensile.

**Fatto in questo arco di sessioni (26-28 giu):** allineata la matematica del bridge della dashboard alla convenzione esatta del GM OPS Tracker; assimilata la logica target mensile→settimanale; estratto e verificato l'**FC3 2026 mensile per paese** ([[data-fc3-2026-mensile]], riconciliato contro la riga TOTAL del file, maggio €1.069.957 esatto); caricati i dati reali nella dashboard. Dettaglio matematico nella memoria `project_ops-dashboard-gm-math`.

**Next steps:**
- **Feature "settimana/mese in corso"** (la più importante): far inserire agli operation manager le assunzioni per il periodo in corso → forecast, così un actual parziale non sballa più il confronto (è il bug della W26). Sblocca poi l'estensione dei dati oltre maggio.
- Riconciliare dashboard ↔ slide `performance` sulla stessa baseline FC3 (oggi la dashboard è per mercato a 3 driver, le slide per segmento a 7 barre).
- (Futuro) automatizzare l'ingest degli actuals dal DWH via l'MCP gateway Superset ora funzionante (dataset 378 Delivery Finance / 766 reporting_finance) invece dell'export CSV manuale — vedi memoria `reference_agent-gateway-mcp-access`.

---

## Stream 2 — OPS GM Dashboard (stato tecnico)

Codice: `/Users/f.franceschetti/Projects/ops-dashboard` (Next.js + TS + Prisma/SQLite). Avvio: `npm run dev` → `localhost:3000`. Ricarica dati: `npx tsx prisma/load-real.ts`.

**Stato attuale (2026-06-28):**
- **Bridge GM** (`lib/gm-engine.ts`): convenzione del foglio — Volume effect = ΔVol × margine **actual**; RPO/CPO effect × volume **target**. Riconciliazione provata sui test.
- **Vista settimanale** (ISO week): actual vs target settimanale derivato. Validata.
- **Vista mensile** (`lib/monthly-aggregation.ts` + tabelle `MonthlyActual`/`MonthlyTarget` + `getMonthDecomposition`): su **mese di calendario** (non somma di settimane ISO). Validata vs foglio: **maggio 2026 = −€171,4k** (actual 898,5k vs FC3 1.070,0k). Il vecchio MTD-by-ISO-week è stato rimosso.
- **Target FC3**: mensili-per-paese (hardcoded e verificati) → settimanali via `lib/target-derivation.ts`; il mensile usa il target FC3 diretto.
- **Dati caricati**: scope temporaneo **2026, 1 gen → 31 mag** (ultima settimana piena ISO W22) per validare su dati puliti. `LOAD_START_MS`/`LOAD_END_MS` in `load-real.ts`.
- Actuals DB = somma diretta del CSV, esatti (verificato su W25). Suite test verde all'ultimo run.

**Next steps:**
- Allargare `LOAD_END_MS` oltre maggio (giugno+, poi 2024/2025) **dopo** la feature settimana-in-corso.
- Review finale whole-branch + triage Minor residui (query DB duplicate nel data layer, mutazione array dedup CSV) → poi chiudere il branch.
- Fase 4 prodotto: multi-tenancy, mercati/metriche configurabili, report Slack generato.
- Eventuale estrazione GR per cliente (oggi i target sono a livello paese, sufficienti).

---

## Stream 3 — Company Brain (prodotto da vendere)

Stato e architettura in [[progetto-company-brain]]. Il personal brain è il prototipo artigianale; scalarlo = sostituire ogni pezzo manuale con uno automatizzato (ingestion API → note atomiche via Claude API → vault + vector DB → RAG → automazioni).

**Next steps (roadmap):**
- Step 2: ChromaDB locale + script di embedding delle note esistenti (imparare il RAG dall'interno).
- Step 3: script di ingestion da una fonte reale (Notion o Google Drive API).
- Step 4: primo cliente pilota (5-20 persone, Notion+Drive) per imparare il workflow di onboarding.
- La **OPS GM Dashboard** può essere il primo wedge di prodotto vendibile a aziende last-mile (SaaS €300-800/mese), validato internamente su Stuart prima di prodottizzare.

---

## Da dove ripartire

La priorità tecnica che sblocca lo Stream 1/2 è la **feature "periodo in corso"** (assunzioni operation manager → forecast). Tutto il resto (estensione dati, riconciliazione slide↔dashboard, prodottizzazione) viene dopo.
