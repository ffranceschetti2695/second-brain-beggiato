---
title: "Sessione 2026-06-29"
summary: "Diagnosi e fix dell'accesso MCP al gateway Superset: VPN/DNS, OAuth e porta callback occupata; accesso ottenuto da CLI"
tags: [workspace, type/session]
status: done
created: 2026-06-29
updated: 2026-06-29
related: ["[[doc-dwh-finance-schema]]", "[[doc-flusso-performance-mensile]]"]
---

## Fatto
Diagnosticato perche' la tool MCP `superset-mcp_1_List_Datasets` falliva nella desktop app di Claude con "Failed to call tool". Leggendo i log MCP (`~/Library/Logs/Claude/`) e' emersa una cascata di tre cause, non una sola: (1) fuori VPN, l'host interno `stuart-agentgateway.internal.stuart.com` non si risolveva; (2) token OAuth scaduto, con `UnauthorizedError` ripetuti; (3) porta callback OAuth `127.0.0.1:10863` occupata da processi `mcp-remote` zombie (`EADDRINUSE`), che impediva il salvataggio del token. Risolte tutte e tre: riconnessione VPN, login SSO/Google, kill dei processi `mcp-remote` orfani. Poi ho avviato io `mcp-remote`, completato l'OAuth, e usato il token salvato in `~/.mcp-auth` per chiamare il gateway via HTTP (con timeout) — `initialize`, `notifications/initialized`, `tools/call`. Accesso pieno all'MCP da CLI: elencati i 17 dataset Superset disponibili (incl. id 766 `reporting_finance` baseline FC3 e id 378 Delivery Finance).

## Deciso
Il problema non era ne' Claude ne' la desktop app, ma rete + auth + porta. Verifica DNS corretta: non `nslookup` (interroga il resolver pubblico e da' falsi NXDOMAIN) ma `dscacheutil -q host` o `curl --max-time`. Salvata in memoria la procedura completa di accesso/debug del gateway per riuso futuro, cosi' la prossima volta non si riparte da zero.

## Aperto

### Stuart
- Sfruttare l'MCP ora funzionante per estrarre dati Superset: schema/query sul dataset 766 (`reporting_finance`, baseline FC3) o 378 (Delivery Finance)

### Progetto AI / Monetizzazione
- (nessuno step confermato in questa sessione)
