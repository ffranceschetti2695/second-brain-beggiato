---
title: "Sessione 2026-06-29-c"
summary: "OPS Dashboard: bridge GM allineato al foglio, FC3 2026 mensile per paese estratto e verificato, dati reali caricati; nota di handoff e CLAUDE.md arricchito."
tags: [workspace, type/session]
status: done
created: 2026-06-29
updated: 2026-06-29
related: ["[[stato-stream-ai]]", "[[progetto-ops-dashboard]]", "[[data-fc3-2026-mensile]]", "[[progetto-company-brain]]", "[[entity-stuart]]"]
---

## Fatto

- Review della OPS GM Dashboard e caccia al disallineamento numeri vs Google Sheet: due cause trovate — convenzione di scomposizione del bridge diversa dal foglio, e dati demo invece dei reali. Allineato il motore (`gm-engine.decompose`) alla convenzione del foglio in TDD (volume effect al margine actual, rate effect al volume target).
- Assimilata la logica target mensile→settimanale (`target-derivation.ts`) e l'inverso ISO data→settimana (`isoWeekYearFromDate`).
- Estratto dall'export FC3 March 2026 il **mensile per paese** (Volume/GM/GR → RPO/CPO) sommando clienti + segmenti + pipeline → paese → globale. Riconciliato contro la riga TOTAL del file: maggio €1.069.957 e volume 756.105 esatti, 11/12 mesi a ±€3. Salvato in [[data-fc3-2026-mensile]].
- Caricati i dati reali nella dashboard (`prisma/load-real.ts`): actuals daily→settimana + target FC3; actuals DB = somma diretta del CSV (esatti). [Lavoro proseguito il 28/6 con la vista mensile su mese di calendario.]
- Creata la nota di handoff [[stato-stream-ai]] (tre stream + next steps) e arricchito `.claude/CLAUDE.md` con le convenzioni di navigazione/manutenzione del vault (entry point `llms.txt`, aggiorna index di cartella, rigenera con `generate_llms.py`, skill journal a inizio/fine, stile).

## Deciso

- La convenzione del bridge è quella del foglio (volume@margine-actual, rate@volume-target): riconcilia uguale ma è l'unica che combacia con lo split del Tracker.
- I target FC3 a livello paese sono sufficienti per la dashboard (niente estrazione GR per cliente per ora).
- CLAUDE.md tiene solo convenzioni di lavoro durature, non dati di dominio (che restano nelle note e in memoria). La preferenza "xCel non azionabile" resta in memoria.
- La priorità tecnica che sblocca gli stream reporting/dashboard è la feature "periodo in corso".

## Aperto

### Stuart

- Feature "periodo in corso": far inserire agli operation manager le assunzioni per settimana/mese in corso → forecast (fix definitivo del bug actual parziale / W26), poi estendere i dati oltre maggio.
- Riconciliare dashboard ↔ slide `performance` sulla stessa baseline FC3.

### Progetto AI / Monetizzazione

- ops-dashboard: review finale whole-branch + triage Minor → chiudere il branch; poi Fase 4 (multi-tenancy, mercati/metriche configurabili, report Slack).
- Company Brain: roadmap step 2 (ChromaDB locale + embedding note), poi step 3 (script ingestion Notion/Drive) verso il primo pilota.
- (Futuro) ingest actuals dal DWH via MCP gateway Superset invece del CSV manuale.
