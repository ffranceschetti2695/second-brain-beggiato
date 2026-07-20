---
title: "Ancorare un'assumption di forecast al gap forecast-vs-actual, non a un tasso YoY"
summary: "Per giustificare un aggiustamento su un forecast già esistente, confrontare il forecast stesso con l'actual dello stesso periodo evita il doppio conteggio che si crea confrontando invece con un tasso di crescita YoY sull'anno precedente"
tags: [concepts, fp-and-a, forecasting]
status: active
created: 2026-07-14
updated: 2026-07-14
related: ["[[concetto-fpa]]", "[[concetto-forecast-adjustment-baked-in-vs-bolt-on]]", "[[progetto-fc6-topline-proposal]]"]
---

# Ancorare un'assumption di forecast al gap forecast-vs-actual, non a un tasso YoY

## Il problema

Quando si vuole giustificare un aggiustamento percentuale su un forecast già modellato (es. "+4% di volume H2"), è tentante ancorarlo a un tasso di crescita year-over-year osservato nel DWH (es. "il mese scorso è cresciuto +3.7% vs lo stesso mese dell'anno precedente"). Questo ragionamento sembra solido ma nasconde un **rischio di doppio conteggio**: se il forecast originale *già* incorpora una crescita simile rispetto all'anno precedente (cosa comune, perché i forecast di solito assumono un trend YoY), applicare un ulteriore +X% YoY sopra quel forecast significa sommare due volte la stessa crescita, arrivando a un'assunzione implicita di crescita doppia (es. +8% invece di +4%) senza che nessuno l'abbia deciso esplicitamente.

## La soluzione: confrontare il forecast con l'actual dello stesso periodo

Invece di confrontare "actual di quest'anno vs actual dell'anno scorso" (YoY), il confronto corretto per decidere se e quanto correggere un forecast è **il forecast stesso vs l'actual/run-rate dello stesso mese**: quel forecast, per quel mese, sta sovra- o sotto-stimando quello che sta davvero succedendo? Questo isola la domanda giusta (il forecast è sbagliato?) da una domanda diversa (quest'anno cresce rispetto al precedente?), che può essere vera in entrambi i casi senza dire nulla sulla bontà del forecast.

## Esempio osservato

Nel [[progetto-fc6-topline-proposal]] (FC6 2026, Tesco UK), la prima bozza giustificava un +4% di volume H2 citando che giugno 2026 actual era +3.7% YoY vs giugno 2025. Verificando i dati, il forecast FC6 originale per Tesco H2 (luglio-dicembre) già incorporava circa +3.9% di crescita YoY rispetto al 2025 — quasi identico al dato citato. Applicare un ulteriore +4% sopra quel forecast avrebbe quindi implicitamente assunto un'accelerazione a ~+8% YoY, senza alcuna giustificazione per l'accelerazione in sé.

La correzione: confrontare il forecast di luglio di FC6 (13.340 consegne/giorno) con l'actual dei primi 12 giorni di luglio (14.891 consegne/giorno) — un gap di +11.6% *sul forecast stesso*, non sul 2025. Il +4% finale è stato mantenuto come frazione conservativa di quel gap, non come ulteriore crescita YoY. Lo stesso approccio applicato a Zapp UK ha rivelato un gap ancora più ampio (+25.6%) contro cui il +2% già usato risultava ancora più conservativo del previsto.

## Quando applicarlo

Ogni volta che un'assumption di forecast viene giustificata citando un tasso di crescita esterno (YoY, benchmark di settore, ecc.), controllare prima se il forecast di partenza già incorpora quel tasso. Se sì, il confronto rilevante è forecast-vs-actual dello stesso periodo, non actual-vs-actual tra anni.

## Vedi anche

[[concetto-fpa]] — [[concetto-forecast-adjustment-baked-in-vs-bolt-on]] — [[progetto-fc6-topline-proposal]]
