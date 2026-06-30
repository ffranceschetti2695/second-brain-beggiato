---
title: "Sessione 2026-06-26-c"
summary: "Costruito l'MVP della web app OPS GM Dashboard partendo dal GM OPS Tracker, con nota di progetto dedicata nel vault."
tags: [workspace, type/session]
status: done
created: 2026-06-26
updated: 2026-06-26
related: ["[[progetto-ops-dashboard]]", "[[progetto-company-brain]]", "[[entity-stuart]]", "[[doc-flusso-performance-mensile]]", "[[concetto-bridge-waterfall]]"]
---

## Fatto

- Brainstorming sulla fattibilità di trasformare il GM OPS Tracker (Google Sheet) in una web app vendibile ad altre aziende last-mile. Esito: fattibile e più robusto del foglio.
- Costruito l'MVP completo di ops-dashboard in `/Users/f.franceschetti/Projects/ops-dashboard` (Next.js + TypeScript + Tailwind + Prisma/SQLite): schema DB, motore di GM decomposition con invariante di riconciliazione, import CSV con API route, dashboard con week selector + headline + market card + vista MTD, e waterfall chart. 80 test verdi, build OK, 6 commit.
- Creata la nota [[progetto-ops-dashboard]] nel vault come ponte tra il Personal Brain e il codice che vive fuori dal vault.

## Deciso

- Import dati via CSV (export da Superset) invece di connessione diretta al DWH Redshift: Francesco non è admin e non vuole chiedere accessi IT. Vantaggio collaterale: il prodotto diventa indipendente dal DWH del cliente, quindi più vendibile.
- Il codice dell'app sta fuori dal vault (è un progetto software, non note markdown); il vault traccia il progetto tramite la nota dedicata che punta al path e allo stato.

## Aperto

### Stuart

- (niente di aperto)

### Progetto AI / Monetizzazione

- ops-dashboard: eseguire la review finale whole-branch dell'MVP (non ancora fatta).
- Triage dei Minor accumulati: query DB duplicate (12 vs 9), campi latenti MTD, mutazione array nel dedup CSV.
- Poi chiudere il branch di sviluppo (finishing-a-development-branch).
- A seguire, Fase 4 del piano: multi-tenancy, mercati configurabili, report Slack.
