---
title: "Sessione 2026-07-07-b"
summary: "Investigazione transcript Google Meet e setup Gmail MCP locale per accesso email Stuart."
tags: [workspace, type/session]
status: done
created: 2026-07-07
updated: 2026-07-07
related: ["[[progetto-company-brain]]", "[[doc-company-brain-ingestion-horizons]]"]
---

## Fatto

- Creata nota `doc-company-brain-ingestion-horizons` con lookback per ogni fonte del stuart-brain (Confluence per spazio, Slack/Drive/DWH da definire).
- Confermato che Drive MCP legge transcript Google Docs senza problemi di permessi, ma i transcript Meet recenti di Stuart non sono nel Drive di Francesco — sono nel Drive dell'organizzatore delle call.
- Scoperto che l'MCP claude.ai per Gmail espone solo tool di autenticazione, non di lettura (a differenza di Drive e Calendar che hanno tool completi).
- Setup completo Gmail MCP locale: Google Cloud project `claude-mcp-personal` (account Google personale — Stuart blocca creazione GCP projects agli utenti standard), Gmail API abilitata, OAuth consent screen External con test user f.franceschetti@stuart.com, credenziali scaricate in `~/.claude/gmail/credentials.json`, `@gongrzhe/server-gmail-autoauth-mcp` installato in `~/.npm-global`, `.mcp.json` configurato in `~/.claude/`.

## Deciso

- Usare account Google personale per il GCP project (Stuart non permette la creazione di progetti GCP agli utenti standard).
- Gmail MCP locale come soluzione per leggere email con transcript Meet, in attesa che claude.ai aggiunga tool di lettura Gmail nativamente.

## Aperto

- Riavviare Claude Code e completare OAuth flow Gmail (selezionare account Stuart nel browser), poi testare lettura email transcript Meet
