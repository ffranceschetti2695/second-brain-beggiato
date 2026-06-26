---
title: "Flusso Performance Mensile (Stuart)"
summary: "Procedura ripetibile per costruire i bridge Actual vs FC3 mensili: dalla baseline e dalla query DWH ai 7 waterfall, con i check di quadratura."
tags: [docs, stuart, reporting, fpa, procedura]
status: active
created: 2026-06-25
updated: 2026-06-25
related: ["[[data-fc3-baseline-2026]]", "[[code-query-actuals-dwh]]", "[[doc-dwh-finance-schema]]", "[[concetto-bridge-waterfall]]", "[[data-stuart-segmentazione-clienti]]"]
---

# Flusso Performance Mensile

Procedura ripetibile per produrre lo scostamento **Actual vs FC3** delle slide di Company Performance di [[entity-stuart]] (Volume, GR, GM). E' il blueprint operativo della skill mensile. La teoria del bridge e' in [[concetto-bridge-waterfall]].

## Input

- **Mese di lavoro** (es. maggio 2026).
- **Baseline FC3**: colonna del mese da [[data-fc3-baseline-2026]] (per i mesi non congelati si ripesca dall'export FC3).
- **Actuals**: dal DWH via [[code-query-actuals-dwh]].
- **Mapping** gruppo -> barra: [[data-stuart-segmentazione-clienti]].

## Step

1. **FC3 del mese.** Leggi la colonna del mese dalla baseline: Volume / GR / GM per cliente e segmento. Per le 7 barre ricorda lo split pipeline (ENT a se', SMB dentro SMB, MM dentro MM) e l'estrazione di Intermarche.
2. **Actuals dal DWH.** Lancia la query di [[code-query-actuals-dwh]] cambiando `month_end_date` sul mese. Negli actuals la pipeline e' sempre 0.
3. **Applica il mapping.** Collassa `client_forecast_group_adj` nelle 7 barre (Tesco, UK/FR/PL Top, Mid-Market, SMB, Pipeline ENT) secondo [[data-stuart-segmentazione-clienti]].
4. **Check di quadratura (obbligatorio).** Il **volume totale** Actual deve coincidere con la dashboard all'unita'. Se non torna, fermati: il grouping o il mese sono sbagliati.
5. **Costruisci i 3 bridge.** Per ciascuna metrica: barra iniziale FC3, delta per barra (Actual - FC3), barra finale Actual. La somma dei delta deve quadrare (check = 0).
6. **Output.** Tre waterfall + la narrativa del mese (driver del miss/beat, ranking dei segmenti per impatto).

## Note e caveat

- **Fonte actuals = DWH**, sempre. Mai i valori della sheet dashboard.
- **PL AmRest/JET**: GR e GM divergono dalla dashboard per [[concetto-additional-rpo]] (scarto variabile). La barra PL Top assorbe lo scostamento. Il Volume non e' mai impattato.
- **Versione FC3**: tra dashboard ed export di marzo c'e' uno scarto noto su Tesco GM (vedi baseline). Per i valori FC3 della dashboard usare i numeri dashboard.
- **YTD**: per le slide cumulate servono gli actuals dei mesi precedenti (stessa query, mese per mese o range).
