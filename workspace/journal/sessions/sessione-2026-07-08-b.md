---
title: "Sessione 2026-07-08-b"
summary: "Creati due output di sintesi sul Company Brain: retrospettiva delle decisioni e manuale tecnico dell'app dedotto dal codice"
tags: [workspace, type/session]
status: done
created: 2026-07-08
updated: 2026-07-08
related: ["[[output-company-brain-retrospettiva]]", "[[output-company-brain-manuale-tecnico]]", "[[progetto-company-brain]]", "[[concetto-company-brain]]"]
---

## Fatto

Creati due documenti di sintesi sul progetto Company Brain, richiesti per fissare le logiche del prodotto e come base per future demo cliente:

1. [[output-company-brain-retrospettiva]] — sintesi cronologica delle decisioni prese (perché Stuart è palestra e non prodotto, evoluzione del modello Opus→Sonnet→agenti in sessione, criteri di ingestion per fonte, problemi reali e soluzioni), costruita analizzando tutte le sessioni di journal pertinenti tramite un agente di ricerca dedicato.
2. [[output-company-brain-manuale-tecnico]] — manuale di riferimento tecnico (stack, pipeline canonizer a due fasi, schema del vault, tabella dei 7 connettori con credenziali/filtri/lookback, strumenti di manutenzione quality_gate/dedupe_check/reindex/workspace_log, cheat sheet comandi, limiti attuali), dedotto leggendo direttamente tutto il codice sorgente di `company-brain-app` (14 file, ~2600 righe).

Aggiornato l'indice `outputs/index-outputs.md` e rigenerato `llms.txt` (73 note).

## Deciso

I due documenti sono stati tenuti separati per scopo: la retrospettiva copre il *perché* (decisioni e rationale, utile per demo e per capire la storia del prodotto), il manuale tecnico copre il *come funziona oggi* (stack e architettura, dedotto dal codice, utile come riferimento rapido per non doverselo ricordare a memoria).

## Aperto

Nessun nuovo step aperto emerso in questa sessione.
