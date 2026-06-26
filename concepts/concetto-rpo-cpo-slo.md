---
title: "RPO, CPO e SLO — Metriche Last-Mile Delivery"
summary: "Le tre metriche operative chiave di Stuart: Revenue Per Order, Cost Per Order e Service Level Objective."
tags: [concepts, last-mile, metriche, delivery]
status: active
created: 2026-06-18
updated: 2026-06-18
related: ["[[entity-stuart]]", "[[area-fp-and-a]]", "[[concetto-fpa]]"]
---

# RPO, CPO e SLO

## Formula base

**RPO − CPO = GM/ordine**

## Definizioni

| Metrica | Definizione |
|---|---|
| **RPO** (Revenue Per Order) | Revenue per consegna, pagata dal cliente retailer. Varia per cliente, mercato e soglie di volume. |
| **CPO** (Cost Per Order) | Costo operativo per consegna (corrieri, incentivi, trasporto). Split: Instant vs Scheduled. |
| **SLO** (Service Level Objective) | Target qualitativo — es. 95% consegne entro 60 min. Negoziato per cliente. Sub-metrica: undelivered rate. |

## Tensione strutturale

Alzare RPO rischia di degradare SLO. L'overspend CPO è usato per "comprare" SLO. Questo trade-off è il tema centrale di ogni reforecast e negoziazione cliente.

## Contesto operativo

- Tracciati per linea di prodotto (Instant / Scheduled / LTT), per mercato (UK, FR, PL) e per cliente
- Input principali del ciclo MBR e dei reforecast (FC3, FC6, FC9)
- Formula estesa: RPO − CPO = GM/ordine → aggregato = Gross Margin totale

## Note collegate

Queste tre metriche sono la base di calcolo del [[concetto-bridge-waterfall]] (Actual vs FC3) e dei valori per cliente congelati in [[data-fc3-baseline-2026]]. Lo scarto di conversione del ricavo che non emerge dal RPO standard è trattato in [[concetto-additional-rpo]].
