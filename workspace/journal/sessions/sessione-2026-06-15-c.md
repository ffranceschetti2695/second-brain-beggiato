---
title: "Sessione 2026-06-15-c"
summary: "Esplorazione degli script Python del vault e apertura della questione automazione."
tags: [workspace, type/session]
status: done
created: 2026-06-15
updated: 2026-06-15
related: ["[[index-self]]"]
---

## Fatto
Esaminati i tre script Python del vault: `quality_gate.py` (auditor su 6 regole di integrità), `generate_llms.py` (rigeneratore dell'indice AI `llms.txt`), `generate_showcase.py` (fotografia statistica del vault). Chiarito che tutti e tre si lanciano manualmente da terminale e non c'è automazione attiva.

## Deciso
Nessuna decisione presa. La questione dell'automazione è stata aperta ma non affrontata.

## Aperto
Valutare se introdurre un'automazione per gli script Python: hook git pre-commit, Makefile, o plugin Obsidian (Shell Commands / Templater).
