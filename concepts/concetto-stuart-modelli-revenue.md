---
title: "Stuart: Modelli di Revenue per Paese"
summary: "Struttura GR→NR per i tre modelli operativi Stuart (Merchant UK, Agent 2.0 FR, Agent 1.0 PL): come si classifica il ricavo e cosa conta come Net Revenue."
tags: [concepts, stuart, fpa, revenue]
status: active
created: 2026-07-02
updated: 2026-07-02
related: ["[[concetto-rpo-cpo-slo]]", "[[data-fc3-2026-mensile]]", "[[doc-dwh-finance-schema]]", "[[entity-stuart]]"]
---

# Stuart: Modelli di Revenue per Paese

Stuart opera con tre modelli commerciali distinti che determinano come si calcola il Net Revenue a partire dal Gross Revenue.

## UK — Merchant

- **GR = NR**: il cliente paga direttamente Stuart per la consegna. Stuart non agisce da agente.
- Tutto il GR va nel Net Revenue senza rettifiche.
- In FC6: GL 4001100 (Delivery Fee diretta).

## FR — Agent 2.0

Stuart agisce da **agente** per conto del corriere: il cliente paga il corriere, Stuart trattiene una fee di servizio.

| Componente | Significato |
|---|---|
| Delivery Fee | Quanto paga il merchant al corriere (pass-through) |
| Service Fee | La fee che Stuart trattiene (revenue reale) |
| VAT Commission | IVA sulla Service Fee (rettifica negativa) |

**Gross Revenue** = Delivery Fee + Service Fee (− VAT Commission in alcune versioni)
**Net Revenue** = Service Fee (− VAT Commission)

In FC3 2026, la Delivery Fee rappresenta ~64–67% del GR.

### Differenza di classificazione FC3 vs FC6

In **FC3**, il GR FR è riportato come somma delle tre componenti (DF + SF − VAT). In **FC6**, il ricavo FR è registrato sotto un'unica voce GL 4001200 che rappresenta l'intero GR senza distinguere DF/SF — quindi il valore "Service Fee" in FC6 = GR FC3. Lo split DF/SF deve essere riapplicato esternamente usando i ratei FC3 (metodo residuale).

## PL — Agent 1.0

Modello precedente ad Agent 2.0, con struttura contrattuale diversa ma stesso schema GR = NR in DWH: il file gsheets non separa DF/SF per PL.

- GR riportato come unico aggregato nel DWH.
- NR ≈ GR (nessuna rettifica visibile nei file di forecast).

## FX per il reporting in EUR

| Paese | Valuta | Conversione |
|---|---|---|
| FR | EUR | 1:1 |
| UK | GBP | ÷ 0.86 |
| PL | PLN | ÷ 4.5 |

Questi tassi sono convenzionali usati nel ciclo di forecast FC6 2026; non sono tassi spot aggiornati.

## Vedi anche

[[concetto-rpo-cpo-slo]] — [[doc-dwh-finance-schema]] — [[entity-stuart]]
