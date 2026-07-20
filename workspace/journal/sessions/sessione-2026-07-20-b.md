---
title: "Sessione 2026-07-20-b"
summary: "Gross margin di giugno 2026 dal DWH e refresh della Budget Plan view con il nuovo FC6"
tags: [workspace, type/session]
status: done
created: 2026-07-20
updated: 2026-07-20
related: ["[[doc-dwh-finance-schema]]"]
---

## Fatto

Estratto dal DWH (`metrics_core.delivery_finance`, filtro `is_invoiced = TRUE`, conversione EUR) il gross margin di giugno 2026 per mercato: UK 470.728€, FR 263.580€, PL 132.348€, totale 866.656€.

Rigenerata la Budget Plan view (skill `budget-plan-view`) usando `OPS - GM Tracker  (3).xlsx` e il file `Revenue to GM - FC6 - June 2026 (4).xlsx` scaricato da Francesco. Output salvato in `~/Desktop/budget-plan-monthly-2026.csv`.

## Deciso

- Cutover confermato a luglio 2026 in poi (mese successivo al file FC6 di giugno).
- I valori di luglio nel Plan sheet erano disallineati rispetto al nuovo FC6 (es. Global GM luglio 1.069.958€ → 760.126,85€) nonostante il tag `FC6` fosse già presente: sovrascritti con i dati del file appena scaricato, seguendo la logica della skill (cutover mese = fonte di verità, non il tag già presente).
- CPO normalizzato a positivo (il file FC6 lo storicizza negativo).
- EBITDA e Contribution Margin globali lasciati a FC3: nessuna riga equivalente nel file FC6.

## Aperto

Nessun nuovo step aperto da questa sessione.
