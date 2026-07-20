---
title: "Sessione 2026-07-17"
summary: "Diagnosi e fix del bug di riconciliazione GM OPS Tracker (RPO stale UK luglio) e formattazione Slack del Financial Update settimanale"
tags: [workspace, type/session]
status: done
created: 2026-07-17
updated: 2026-07-17
related: ["[[progetto-ops-dashboard]]"]
---

## Fatto

Rieseguita `budget-plan-view` con l'ultimo file FC6 scaricato, generando il CSV blend BP26/FC3/FC6 su Desktop. Rieseguita `stuart-financial-update-weekly` per la settimana W29 (13-19 luglio) e il landing di luglio, con base di confronto FC6 invece di BP'26.

Durante la verifica dei numeri, individuato uno scarto reale di circa 66k€ tra la somma dei GM Impact settimanali e il GM Impact mensile del tab Monthly per UK (e di conseguenza Global) nel GM OPS Tracker. Diagnosticata la causa: nel foglio "Pre-weekend monitoring", la cella RPO (riga 60) delle due settimane di luglio già chiuse ("Actual", colonne AR/AS) conteneva un valore hardcoded disallineato dal Gross Revenue pull via SUMIFS da Actuals. Francesco ha confermato che l'RPO hardcoded era quello corretto, quindi la correzione necessaria era sul Gross Revenue (formula `=RPO*Volume` invece del SUMIFS). Francesco ha applicato il fix e scaricato un nuovo file: verificata la riconciliazione perfetta Weekly↔Monthly per tutti i mercati e confermato che il piano FC6 nel tab Plan del tracker è allineato al file standalone Revenue to GM FC6 (differenze solo di arrotondamento a 2 decimali).

Preparato il messaggio Slack del Financial Update (vs FC6) per #operations e per Mark Jones in DM. Dopo un errore iniziale (invio diretto invece di bozza, e formattazione non corretta), è stata identificata la formattazione esatta usata da Francesco nei messaggi precedenti (letta via ricerca Slack raw) e le due bozze sono state ripubblicate correttamente: tre righe in grassetto (titolo, header Weekly, header Monthly) con sintassi markdown a doppio asterisco per i tool Slack MCP, bullet "•" per il breakdown mensile per mercato.

## Deciso

- Il Gross Revenue delle due settimane "Actual" di luglio nel tracker va ricalcolato come RPO×Volume, non pullato via SUMIFS da Actuals, perché in questo caso l'RPO hardcoded da Francesco è la fonte corretta.
- La formattazione Slack del Financial Update settimanale usa doppio asterisco (`**bold**`) nei tool di invio/bozza Slack (che convertono in bold nativo Slack), non singolo asterisco (che rende in corsivo). Corretto lo skill file `stuart-financial-update-weekly.md` e salvata la regola in memoria.
- Le bozze Slack vanno sempre create con lo strumento apposito (draft), mai inviate direttamente, a meno di richiesta esplicita di invio.

## Aperto

Nessun nuovo step aperto emerso in questa sessione.
