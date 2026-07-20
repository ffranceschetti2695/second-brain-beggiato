---
title: "Sessione 2026-07-13-c"
summary: "Workflow Claude Design per le slide MBR: prototipo HTML, poi prompt ottimizzato (numeri in k, canvas full-bleed, slide native) verificato contro la skill mbr-finance-section"
tags: [workspace, type/session]
status: done
created: 2026-07-13
updated: 2026-07-13
related: ["[[progetto-company-brain]]"]
---

## Fatto
Analizzato il flusso possibile tra Claude Code e Claude Design (nessuna API diretta, solo handoff manuale via prompt/export). Costruito un primo prototipo HTML delle 5 slide del MBR finance section (giugno 2026), poi ottimizzato il prompt in `MBR-June-2026-slide-content.md` per Claude Design: numeri in formato k-migliaia (eccezione RPO/CPO a 2 decimali), canvas 16:9 full-bleed con contenuto verticalmente centrato, istruzione esplicita di generare slide native e non un mockup HTML. Verificato che la skill `mbr-finance-section` riflette già tutte queste regole.

## Deciso
Claude Design resta lo strumento di generazione slide per l'MBR finance section (non Google Slides API, non automazione diretta Claude Code → Claude Design): il passaggio resta un prompt autosufficiente da incollare manualmente, con export finale in PPTX da importare nel deck.

## Aperto
- MBR giugno 2026: eseguire il prompt ottimizzato in Claude Design per generare le 5 slide finali e importarle nel deck Google Slides reale
