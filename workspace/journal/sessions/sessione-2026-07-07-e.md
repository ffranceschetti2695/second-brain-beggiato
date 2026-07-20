---
title: "Sessione 2026-07-07-e"
summary: "Ingestion filtrata Confluence TOM e completamento della copertura Slack (group DM leadership + war room UK) nello stuart-brain"
tags: [workspace, type/session]
status: done
created: 2026-07-07
updated: 2026-07-07
related: ["[[progetto-company-brain]]", "[[doc-company-brain-ingestion-horizons]]"]
---

## Fatto

Applicato il filtro concordato a Confluence TOM (504 pagine → 90 giorni + keyword strategia/decisione → 40 candidate) e canonizzate in 28 note atomiche nello stuart-vault via 4 agent paralleli, con dedup di documenti duplicati (3 versioni Tesco Strategy, 2 Vendor Management Concentrix, 3 SteerCo mensili, 3 SOP di automazione) e 5 file scartati (template vuoti, status thin).

Individuati e ingeriti 4 group DM Slack di leadership (90 giorni, non ancora coperti nonostante i DM 1:1 lo fossero già): FR Task Force (Ricardo/Sonia/Dimitrij/Francesco), Finance leadership con Cornelia Raportaru, UK War Room (Mark Jones/Ricardo/Luxsanan/Dimitrij/Francesco), Cornelia/Sonia/Francesco. Creata la prima nota persona per Cornelia Raportaru e due nuovi framework di governance (escalation ladder generico, soglia di autorizzazione spesa CPO weekend). Corretta la nota hub "Pre-weekend CPO Governance", che dichiarava erroneamente chiuso il rito del venerdì ad aprile: in realtà è continuato fino a giugno, spostato in DM di leadership prima del canale pubblico.

Completata la lista canali Slack ingerendo `#uk_ops-commercial` e `#uk-summer-war-room` (90 giorni). Il primo è ad altissimo volume di status operativo quotidiano, da cui è stato estratto un solo framework durevole (RAG di valutazione store Tesco a rischio rimozione). Il secondo è ricco di recap settimanali strutturati, canonizzato in un hub con log cronologico giugno-luglio e un framework di governance heatwave (search ratio RAG + PLI dedicato).

stuart-vault passato da 424 a 459 note atomiche in giornata. Aggiornati indici (concepts/docs/projects/entities), `.ingestion_state.json` e `llms.txt` a ogni batch.

## Deciso

- Lookback standard per tutte le nuove ingestion Slack (group DM leadership, uk_ops-commercial, uk-summer-war-room): 90 giorni, coerente con la convenzione già adottata per TOM e Drive.
- TOM formalmente segnato come "Fatto" in `doc-company-brain-ingestion-horizons`; corretta anche la lista canali Slack mancanti che era già stale (operations/revenue/mbr risultavano ancora da fare pur essendo già stati ingeriti in sessione precedente).
- Per canali ad alto rumore operativo (`#uk_ops-commercial`) si estrae solo il framework/decisione riutilizzabile, non lo status quotidiano — coerente con la regola del vault contro le note su dati numerici ri-derivabili.

## Aperto

Nessun nuovo item: il prossimo passo (DWH connector) era già tracciato in `open-items.md` ed è il naturale successore di questa sessione.
