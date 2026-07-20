---
title: "Sessione 2026-07-07-c"
summary: "Completato setup MCP Gmail locale: OAuth, test lettura email Notes by Gemini, verifica accesso attachment."
tags: [workspace, type/session]
status: done
created: 2026-07-07
updated: 2026-07-07
related: ["[[doc-company-brain-ingestion-horizons]]"]
---

## Fatto

Registrato correttamente l'MCP Gmail locale (`claude mcp add`), che nella sessione precedente era rimasto configurato solo a metà (credenziali scaricate ma server mai registrato). Completato il flow OAuth: liberata temporaneamente la porta 3000 (occupata dal dev server di ops-dashboard, poi riavviato), autenticato l'app con l'account f.franceschetti@stuart.com. Verificato che l'MCP legge correttamente le email, in particolare quelle di `gemini-notes@google.com` con oggetto `Notes: "<titolo riunione>" <data>`, che contengono riassunto e next steps generati da AI direttamente nel corpo dell'email. Verificato inoltre che il tool di download attachment funziona in generale (test su `has:attachment`), ma che le email Gemini Notes non hanno mai allegati: il transcript completo vive solo come Google Doc collegato, non come file nell'email.

## Deciso

- La porta 3000 hardcoded nel tool Gmail MCP (`@gongrzhe/server-gmail-autoauth-mcp`) va liberata a mano ogni volta che serve rifare l'OAuth (nessuna configurazione alternativa disponibile nel pacchetto).
- Per il transcript completo delle riunioni serve il Drive MCP (documento collegato), non l'email: l'email Gmail MCP basta per riassunto e next steps.

## Aperto

- Ingestion sistematica delle note riunioni (email "Notes by Gemini") nello stuart-brain via MCP Gmail locale
