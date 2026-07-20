---
title: "Sessione 2026-07-07-d"
summary: "Ingestion completa email Notes by Gemini (ultimo anno) nello stuart-brain: 77 email, 44 note atomiche, log di dedup manuale."
tags: [workspace, type/session]
status: done
created: 2026-07-07
updated: 2026-07-07
related: ["[[doc-company-brain-ingestion-horizons]]", "[[progetto-company-brain-app]]"]
---

## Fatto

Avviata l'ingestion sistematica delle email "Notes by Gemini" (gemini-notes@google.com) via MCP Gmail locale, lookback 365 giorni (2025-07-07 → 2026-07-07), senza filtro: 77 email trovate e recuperate come raw source in `stuart-vault/sources/gmail/`. Canonizzate in 44 note atomiche nello stuart-vault, organizzate in 6 gruppi tematici: ritmo operativo (Weekly Ops & Sustainability, Pre-weekend CPO Governance), ritmo revenue/MBR (Global Revenue Bi-Weekly, Monthly Business Review), ciclo forecast FC3/FC6, 1:1 e Finance LT, ops/finance ad-hoc, iniziative strategiche/training. Le serie ricorrenti sono confluite in note-hub con log cronologico invece che una nota per istanza, per evitare duplicazione; i meeting one-off hanno note dedicate. Verificato che tutte le 44 note nuove risolvono correttamente i wikilink (zero link dangling), rigenerato llms.txt (424 note totali).

## Deciso

- Ingest tutto il corpus di 77 email senza filtro segnale/rumore, a differenza di TOM/Slack (le note atomiche deduplicano naturalmente i concetti ricorrenti nelle note-hub).
- Target di scrittura: stuart-brain (company-brain-app/stuart-vault), non il Personal Brain, essendo contenuto aziendale.
- Creata `doc-gmail-notes-gemini-ingestion-log` come stato manuale di dedup per Gmail (elenco delle 77 email con message_id e nota di destinazione), in assenza di un connector Python con state file come per Slack/Confluence/Drive.

## Aperto

- Gmail Notes by Gemini: trovare un modo per fare ingestion solo incrementali in futuro (nessun connector/stato di dedup automatico) — riferimento nel log `doc-gmail-notes-gemini-ingestion-log`
