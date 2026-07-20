---
title: "Sessione 2026-07-07-f"
summary: "Riallineamento stato Company Brain, ingestion DWH via connettore corretto, nota KPI last-mile benchmark per Stuart"
tags: [workspace, type/session]
status: done
created: 2026-07-07
updated: 2026-07-07
related: ["[[progetto-company-brain]]"]
---

## Fatto

Riallineati `progetto-company-brain.md` (Personal Brain) e `CLAUDE.md` (company-brain-app) allo stato reale del stuart-brain, che erano rimasti indietro rispetto alle sessioni precedenti della giornata (dichiaravano ancora 354 note e fonti "da fare" gia' ingerite). Corretto `connectors/dwh.py`, che interrogava colonne inventate: riscritta la query contro lo schema reale di `metrics_core.delivery_finance`, validata via Superset MCP ed estratto Volume/GR/GM mensile per mercato (UK/FR/PL) gennaio-giugno 2026, cross-validato contro la baseline FC3 esistente (volume maggio 696.055 al 100%). Creata la nota `data-financial-context-2026-h1-dwh` nello stuart-vault.

Delegato a un agent la ricerca di un framework KPI di riferimento per il settore last-mile (Deliveroo, DoorDash, Uber Delivery, Glovo) e il calcolo di RPO/CPO/GM% per Stuart per paese e per cliente (top 12 globali per volume). Creata la nota `concetto-kpi-last-mile-delivery-stuart`; corretto un wikilink orfano (`entity-stuart`, non esistente nel stuart-vault) trovato in revisione.

Stuart-brain a 461 note atomiche. Roadmap step 3 (dogfood Stuart) segnato Fatto, con solo il blocco Google Meet transcript come eccezione nota (limite lato Google, non del connettore).

## Deciso

- Query DWH per KPI unit economics: RPO = gross_revenue_eur / delivery fatturate, CPO = total_costs_eur / delivery fatturate, aggregazione cliente su `parent_client_name` diretto (senza il dedup `client_forecast_group_adj` della query FC3 canonica) — semplificazione accettabile per uno snapshot KPI, non per forecast/budget.
- Prossimo passo del progetto Company Brain: coherence check tra tutte le fonti ora coperte (Slack/Confluence/Drive/Gmail/DWH), da fare in una sessione dedicata separata.

## Aperto

Nessun nuovo step: gli open item restano quelli gia' tracciati in `open-items.md` (coherence check in testa alla lista AI / Company Brain).
