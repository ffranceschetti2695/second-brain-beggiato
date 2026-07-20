---
title: "Sessione 2026-07-13"
summary: "Costruita la skill mbr-finance-section end-to-end e corretta la metodologia YTD per escludere i mesi pre-freeze del piano"
tags: [workspace, type/session]
status: done
created: 2026-07-13
updated: 2026-07-13
related: ["[[entity-stuart]]", "[[concetto-bridge-waterfall]]", "[[doc-stuart-design-system]]"]
---

## Fatto

Costruita da zero la skill `mbr-finance-section`: contenuto (Next steps, GM overview con chip cliente per paese, bridge mese, bridge YTD a doppio grafico GR+GM, weekly pacing del mese in corso), stile visivo brand Stuart (colori fill vs testo, tipografia, regole anti-dead-space sui bridge chart), e un prompt autosufficiente per generare le slide con un tool AI (es. Claude Design). Verificato il file OPS Tracker aggiornato dall'utente per il pacing di luglio, con distinzione tra settimane Actual/Current/Forecast.

## Deciso

Scoperta e corretta una regola metodologica importante: il bridge YTD non deve includere i mesi precedenti al congelamento del piano usato come baseline, perché le colonne di quei mesi nel piano sono solo actual noti al momento del freeze, non vere previsioni — confrontarli misura rumore di restatement, non varianza reale. Verificato caso concreto (FC3, giugno 2026): PL Top e SMB avevano anomalie di riconciliazione isolate a gennaio/febbraio che distorcevano la lettura YTD (PL Top passava da miss apparente a beat reale una volta escluso gennaio). Generalizzata la regola nella skill: FC3 congelato a marzo → escludi gen-feb; FC6 congelato a giugno → escludi gen-mag; per altri piani, verificare il mese di freeze prima di assumere.

## Aperto

- Slide 8 (Provisional P&L / accounting) resta fuori scope finché il connettore NetSuite non è collegato.
