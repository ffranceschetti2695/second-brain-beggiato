---
title: "Segmentazione Clienti Stuart"
summary: "Mappa cliente -> segmento -> barra del waterfall, con i top account per paese, usata negli actuals di performance."
tags: [data, stuart, reporting, fpa]
status: active
created: 2026-06-25
updated: 2026-06-25
related: ["[[entity-stuart]]", "[[concetto-bridge-waterfall]]", "[[data-fc3-baseline-2026]]", "[[progetto-france-task-force]]"]
---

# Segmentazione Clienti Stuart

Mappa di come i clienti di [[entity-stuart]] si aggregano nelle 7 barre del [[concetto-bridge-waterfall]]. La sorgente actuals e' il DWH: il campo `client_forecast_group_adj` (da `mart_finance.inputs_client_grouping`) viene rimappato sulla barra finale.

## Mapping gruppo DWH -> barra

| Barra | Gruppi DWH inclusi |
|---|---|
| **Tesco** | Tesco - UK |
| **UK Top Accounts** | Zapp, Pizza Hut (PH), Iceland |
| **FR Top Accounts** | Carrefour, Sushi Shop, Intermarche, SYSTEME-U |
| **PL Top Accounts** | AmRest, Just Eat (JET) |
| **Mid-Market** | UK MM (+TradeKart), FR MM (+Franprix, +Cote Sushi), PL MM, *-Churned |
| **SMB** | UK SMB, FR SMB, PL SMB |
| **Pipeline ENT** | solo ENT Pipeline (zero negli actuals) |

## Note di mapping

- **Carrefour** resta cliente a se' (`Client_FR Carrefour`) -> FR Top, non confluisce in FR MM.
- **Franprix** e **Cote Sushi** confluiscono in **FR MM** gia' nel grouping DWH.
- **TradeKart** confluisce in **UK MM**.
- **Intermarche** nel sorgente e' bundled in FR Existing MM: estratto verso FR Top e nettato da FR MM.
- Le voci **`*-Churned`** cadono nel Mid-Market del rispettivo paese.

## Peso (riferimento maggio 2026, volume)

- **Tesco** ~437k ordini, da solo circa il 63% del volume totale (696k).
- **PL Top** (AmRest + Just Eat) ~105k, secondo blocco per volume.
- **FR SMB** e **FR MM** i segmenti francesi piu' pesanti; UK Top trainato da Zapp.
- Top account per paese: UK = Zapp, FR = Carrefour + Sushi Shop, PL = AmRest + Just Eat.

I valori puntuali per cliente e mese vivono in [[data-fc3-baseline-2026]] (baseline FC3) e si rileggono dal DWH per gli actuals.
