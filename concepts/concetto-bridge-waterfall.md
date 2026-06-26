---
title: "Bridge Waterfall (Actual vs FC3)"
summary: "Metodologia del waterfall a 7 barre che spiega lo scostamento Actual vs FC3 per Volume, GR e GM nelle slide di performance Stuart."
tags: [concepts, stuart, fpa, reporting]
status: active
created: 2026-06-25
updated: 2026-06-25
related: ["[[concetto-rpo-cpo-slo]]", "[[concetto-fpa]]", "[[entity-stuart]]", "[[data-fc3-baseline-2026]]"]
---

# Bridge Waterfall (Actual vs FC3)

Il **bridge** (o waterfall) e' il grafico a cascata che scompone la differenza tra un valore Actual e la sua baseline (FC3) in contributi per segmento. In [[entity-stuart]] e' lo strumento centrale delle slide di Company Performance mensili: una barra iniziale (FC3), una serie di delta per segmento, una barra finale (Actual). Si costruisce su tre metriche [[concetto-rpo-cpo-slo]]: **Volume, Gross Revenue, Gross Margin**.

## Le 7 barre

1. **Tesco** (standalone, ~60% del volume)
2. **UK Top Accounts** (Zapp, Pizza Hut, Iceland)
3. **FR Top Accounts** (Carrefour, Sushi Shop, Intermarche, SYSTEME-U)
4. **PL Top Accounts** (AmRest, Just Eat)
5. **Mid-Market** (UK/FR/PL MM)
6. **SMB** (UK/FR/PL SMB)
7. **Pipeline ENT**

Dettaglio della membership cliente per barra in [[data-stuart-segmentazione-clienti]].

## Le 3 regole non ovvie

1. **Split della pipeline.** La barra "Pipeline ENT" contiene **solo** la ENT Pipeline. La **SMB Pipeline confluisce in SMB**, la **MM Pipeline in Mid-Market**. Negli Actuals la pipeline e' zero (e' una voce di solo forecast): i clienti che si materializzano finiscono gia' nel loro segmento reale.
2. **Intermarche bundled.** Nel dato sorgente Intermarche e' dentro FR Existing MM: va estratto verso FR Top Accounts e nettato da FR MM.
3. **Riallocazioni hardcoded.** TradeKart va in UK Mid-Market; Franprix e Cote Sushi vanno in FR Mid-Market.

## Lettura del bridge

Il segno del delta dice dove l'Actual ha battuto o mancato la baseline. La somma dei delta per segmento deve **quadrare** con la differenza tra barra iniziale e finale (check = 0). La metrica Volume e' il controllo piu' robusto perche' non risente di FX o additional RPO (vedi [[concetto-additional-rpo]]).
