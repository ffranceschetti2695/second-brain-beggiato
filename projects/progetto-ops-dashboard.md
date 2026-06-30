---
title: "Progetto — OPS GM Dashboard"
summary: "Web app che sostituisce il GM OPS Tracker di Stuart e punta a diventare un prodotto SaaS vendibile ad altre aziende last-mile."
tags: [projects, ai, business, stuart]
status: active
created: 2026-06-26
updated: 2026-06-26
related: ["[[progetto-company-brain]]", "[[entity-stuart]]", "[[doc-flusso-performance-mensile]]", "[[concetto-bridge-waterfall]]", "[[concetto-rpo-cpo-slo]]", "[[doc-modelli-monetizzazione-ai]]"]
---

# Progetto — OPS GM Dashboard

> ⚠️ **Stato aggiornato e next steps in [[stato-stream-ai]]** (questa nota descrive l'MVP iniziale del 26/6; la matematica del bridge, la vista mensile e il caricamento dati reali sono evoluti dopo — vedi la nota di handoff e la memoria `project_ops-dashboard-gm-math`).

Web app che replica e migliora il GM OPS Tracker (oggi un Google Sheet fragile con mirror IMPORTRANGE). Traccia Volume, RPO, CPO e GM Impact per mercato su base settimanale e mensile, con la decomposizione del GM in tre driver (volume, RPO rate, CPO rate). Nasce per uso interno Stuart, con l'obiettivo di diventare un prodotto SaaS per altre aziende last-mile.

## Dove vive il codice

Il codice NON sta nel vault (è un progetto Next.js, non note markdown). Vive in:

```
/Users/f.franceschetti/Projects/ops-dashboard
```

Per avviarlo:

```
cd /Users/f.franceschetti/Projects/ops-dashboard
npm run seed:demo   # carica dati demo (giugno 2026, UK/FR/PL, settimane 23-26)
npm run dev         # dashboard su localhost:3000
```

## Stack

| Layer | Tecnologia |
|---|---|
| Frontend + backend | Next.js (App Router) + TypeScript + Tailwind |
| Database | Prisma + SQLite (locale) |
| Chart | recharts (waterfall bridge) |
| Import dati | CSV upload (export da Superset) — niente connessione diretta al DWH |
| Test | vitest |

Scelta chiave: import via CSV invece di connessione diretta a Redshift, perché Francesco non è admin del DWH e non vuole chiedere accessi IT. Vantaggio collaterale: funziona con qualsiasi DWH (Snowflake, BigQuery, Excel), quindi più universale per la vendita.

## Stato (2026-06-26)

MVP COSTRUITO. Sei task completati con metodo subagent-driven:

1. Scaffold Next.js + TypeScript + Tailwind + Prisma/SQLite
2. Schema DB (Company / Market / Actual / Target) + seed Stuart (UK, FR, PL)
3. Motore GM decomposition con invariante di riconciliazione provato (Volume + RPO + CPO effect = delta GM)
4. Import CSV (parser + API route actuals/targets)
5. Dashboard (week selector, headline globale, 3 market card, vista MTD)
6. Waterfall chart (bridge Target -> Volume -> RPO -> CPO -> Actual, globale + per mercato)

80 test verdi, build OK. Branch `main`, 6 commit puliti. Il ledger di avanzamento è in `ops-dashboard/.superpowers/sdd/progress.md`.

## Aperto

- Review finale whole-branch dell'MVP (non ancora eseguita).
- Triage dei Minor accumulati: query DB duplicate nel data layer (12 vs 9), campi latenti nella vista MTD, mutazione array nel dedup CSV.
- Poi chiudere il branch di sviluppo.
- A seguire la Fase 4 del piano: multi-tenancy, mercati e metriche configurabili, report Slack generato.

## Modello di business

Stesso filone di [[progetto-company-brain]] e [[doc-modelli-monetizzazione-ai]]: prima validazione interna su Stuart, poi prodottizzazione. Prezzo ipotetico SaaS 300-800 euro/mese per azienda. Clienti target: aziende last-mile multi-mercato che oggi fanno questo reporting a mano su fogli di calcolo.

## Vedi anche

[[progetto-company-brain]] — [[entity-stuart]] — [[doc-flusso-performance-mensile]] — [[concetto-bridge-waterfall]]
