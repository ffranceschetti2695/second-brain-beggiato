---
title: "Open Items"
summary: "Fonte di verità degli step aperti per workstream — aggiornata a ogni chiusura sessione"
tags: [workspace]
status: active
created: 2026-07-01
updated: 2026-07-20
related: []
---

## Stuart

- MBR giugno 2026: eseguire il prompt ottimizzato in Claude Design per generare le 5 slide finali (next steps, GM overview, bridge mese, bridge YTD, weekly pacing) e importarle nel deck Google Slides reale
- Verificare se il Carrefour RFP è deferred a "Q4'26" o "settembre" (fonti in contraddizione)
- Pizza Hut UK: nessuna causa documentata per il calo volume dell'84% a giugno
- Next step 8 MBR (AmRest SLO alignment): nessuna risposta da Maksymilian/Agnieszka
- ops-dashboard: "periodo in corso" feature — OM assumptions → forecast, fix W26 partial actual bug, extend data beyond May
- ops-dashboard: final whole-branch review + Minor triage → close branch → Phase 4 (multi-tenancy, configurable markets, Slack report)
- Reconcile dashboard ↔ performance slides on FC3 baseline
- Read Google Meet transcripts via Drive tool (example link in sessione-2026-07-01-b)
- Slide 8 (Provisional P&L / accounting) resta fuori scope finché il connettore NetSuite non è collegato

## AI / Company Brain

- Company Brain quality audit (2026-07-10): aggiungere FPA/FIN a `SPACES` in `fetch_confluence.py` e rilanciare il fetch, fix semantica `status`/`created` nelle note stuart-vault (data evento non data ingestion), dedup a livello di contenuto sui cluster FC6-CPO/ancillary revenue/chiusura accounting dic-2024, costruire layer di sintesi sistematico in `areas/`/`docs/` seguendo il pattern di `area-accounting-x-fpa.md`
- Gmail Notes by Gemini: trovare un modo per fare ingestion solo incrementali in futuro (oggi nessun connector/stato di dedup come per Slack/Confluence/Drive) — log delle 77 email già ingerite in `doc-gmail-notes-gemini-ingestion-log` nello stuart-brain
- DWH: refresh resta manuale (nessuna credenziale Superset REST in `.env`) — valutare scheduler al primo cliente pilota
- Optional: visual interface (chat/dashboard) on top of vector store
- Coherence check: risolvere i finding media/bassa severità rimasti — refuso anno FC3 lock date, vintage RPO Carrefour FR (FC3 vs FC6) non esplicito, buco operativo su Fnac (zero traccia Slack), 4 note quasi-duplicate ramp-down BPO organico
- Dedupe stuart-vault: valutare `concetto-zapp-test-performance-premium.md` e `concetto-bpo-automazione-contatti-corrieri-2026.md` in un prossimo giro di `dedupe_check.py` (segnalati come probabili duplicati ma lasciati fuori scope)

## Finance Dashboard

- Fix AMEX auto-ingest: switch WatchPaths → launchd StartInterval for reliable detection
- Re-auth Illimity when credentials expire (`docs/REAUTH.md`)
- Optional: link Landing point to live Illimity balance

## Speed to Lead

- Urgente: verificare se il codice è finito esposto pubblicamente su `github.com/ffranceschetti2695/second-brain-beggiato` — discrepanza di sicurezza sul push non risolta
- Decisione ElevenLabs: upgrade piano / voce non-Library / restare sul fallback Twilio `<Say>`
- Rimuovere i log di debug temporanei (`console.log('DEBUG ...')`) in `webhook.js` una volta stabile il flusso
- Test end-to-end completo della prenotazione: conferma vocale "sì" → verifica evento su Cal.com Bookings / Google Calendar Stuart
