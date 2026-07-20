---
title: "Sessione 2026-07-01-d"
summary: "Costruito il stuart-brain end-to-end: 21 fonti Slack estratte via MCP, canonizzate in 303 note atomiche con Sonnet, vector store operativo."
tags: [workspace, type/session]
status: done
created: 2026-07-01
updated: 2026-07-01
related: ["[[progetto-company-brain]]", "[[area-ai-business]]", "[[entity-stuart]]"]
---

## Fatto

Costruito il stuart-brain end-to-end. Estratte 21 fonti Slack via MCP (canali privati FC6, finance, strategia Mutares, FR task force, e DM diretti con Sonia Gastelum, Ricardo Amorim, Mateo Noceti, Dimitrij Phoursa, Mark Jones, Antoine Wiecek, Gaspard RC). Canonizzate con Sonnet in 303 note atomiche strutturate nel vault `~/Desktop/company-brain-app/stuart-vault/`. Vector store ChromaDB operativo, ricerca semantica testata e funzionante. Scritti i 4 connettori real-code (slack.py, confluence.py, drive.py, dwh.py) per uso futuro senza MCP.

## Deciso

- Stuart è tutto in inglese: embedding multilingue non necessario, rimosso dalla roadmap.
- Modello canonizzazione: Sonnet (non Opus) per il rapporto qualità/costo; Opus consuma troppo credito su fonti grandi.
- Connettori scritti come codice reale per il prodotto futuro; oggi la pipeline usa MCP come shortcut.
- API key dell'app: usa il `.env` locale con la key Anthropic personale di Francesco.
- Stuart = palestra e proof of concept, non asset da vendere. Il prodotto è l'IP generica.

## Aperto

- Add remaining Slack sources to stuart-brain via MCP (#operations, #revenue, #monthly-business-review, group DM leadership)
- Build Confluence ingestion for stuart-brain via MCP (Financial Data Pipeline, OKR, SteerCo)
- Build Drive ingestion for stuart-brain via MCP (transcript Meet, FC/MBR reports)
- Evaluate DWHMcpConnector for weekly financial context snapshot
- Test Financial Update automation on top of the stuart-brain
