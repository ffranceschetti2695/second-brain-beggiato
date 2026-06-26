---
title: "Additional RPO"
summary: "Componente di ricavo aggiuntivo che spiega perche' GR e GM di alcuni clienti divergono tra la dashboard e il DWH."
tags: [concepts, stuart, fpa, metriche]
status: active
created: 2026-06-25
updated: 2026-06-25
related: ["[[concetto-rpo-cpo-slo]]", "[[concetto-bridge-waterfall]]", "[[entity-stuart]]", "[[data-fc3-baseline-2026]]"]
---

# Additional RPO

L'**additional RPO** e' una quota di ricavo per ordine non catturata dalla conversione standard del DWH. Si manifesta come una differenza tra il Gross Revenue (e quindi il Gross Margin) riportato dalla **dashboard** e quello che si ottiene interrogando il **DWH** (`metrics_core.delivery_finance`), a parita' di volume.

## Quando emerge

Tipicamente sui clienti **polacchi** (AmRest, Just Eat): il volume e' identico tra le due fonti (stessi ordini), ma il ricavo convertito in EUR differisce. Il **costo e' identico**, quindi lo scarto su GR e GM e' lo stesso importo (riga a costo zero, puro margine).

## Punti chiave

- **Non e' un bug ne' un errore di grouping**: il grouping e il volume quadrano al 100%.
- **Lo scarto non e' fisso**: varia ogni mese (a maggio 2026 netto circa -4.944 EUR, con AmRest sotto e Just Eat sopra rispetto alla dashboard).
- **Non e' un FX uniforme**: clienti diversi si muovono in direzioni opposte, quindi non e' un singolo tasso di cambio.
- **Regola operativa**: il flusso mensile usa **sempre i valori del DWH**. La divergenza con la dashboard e' attesa e accettata.

Lega le metriche operative di [[concetto-rpo-cpo-slo]] alla pratica del [[concetto-bridge-waterfall]], dove la barra PL Top Accounts assorbe questo scarto. La baseline di confronto su cui si misura la divergenza è quella di [[data-fc3-baseline-2026]].
