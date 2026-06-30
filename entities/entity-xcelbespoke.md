---
title: "Xcel Bespoke — Fornitore divise corrieri Stuart"
summary: "Fornitore UK che gestisce il negozio WooCommerce per le divise dei corrieri Stuart: pick/pack/delivery a £7.15 per articolo, con contratto da rinegoziare per una discrepanza strutturale."
tags: [entities, vendor, operations, uniforms]
status: active
created: 2026-06-26
updated: 2026-06-26
related: ["[[entity-stuart]]", "[[persona-yohann-bensadoun]]", "[[persona-sonia-gastelum]]"]
---

## Chi sono

Xcel Bespoke (parte di Xcel Concepts Ltd) è il fornitore UK che gestisce la piattaforma WooCommerce attraverso cui i corrieri di [[entity-stuart]] ordinano le proprie divise. Referenti: **Wayne Gilholm** (Owner/Director, wayne@xcelconcepts.co.uk) e **Gabriel White** (Account Manager, gabriel@xcelbespoke.co.uk).

## Struttura dei costi attuale

| Flusso | Chi paga | A chi | Importo |
|---|---|---|---|
| Pick/Pack/Delivery per articolo | Stuart | Xcel Bespoke | £7.15 / articolo |
| Delivery fee per ordine | Corriere | Stuart (Stripe) | £7.62 / ordine |

Il modello era stato impostato assumendo **un articolo per ordine**. In quel regime Stuart incassava £7.62 e pagava £7.15, con un margine di £0.47 per ordine.

## Il problema scoperto (giugno 2026)

Sotto la gestione di Nico Guiraud (poi uscito da Stuart), il negozio è stato aperto agli ordini **multi-articolo**. Il prezzo lato corriere è rimasto £7.62 per ordine — flat, indipendentemente dal numero di articoli. Xcel continua invece a fatturare £7.15 per articolo.

**Esempio con ordine da 3 articoli:**
- Stuart incassa dal corriere: £7.62
- Stuart paga a Xcel: £7.15 × 3 = £21.45
- Perdita netta per Stuart: £13.83 su quell'ordine

Oltre a questo, Nico aveva organizzato ordini omaggio (giveaway) in cui il corriere non veniva addebitato (£0 su Stripe), ma Xcel fatturava comunque £7.15 per articolo. Questi ordini sono stati confermati internamente da Enora Pierron.

## Stato al 2026-06-26

- Fattura **BPSI14778** (e probabilmente BPSI14783 e BPSI14779) in sospeso — importo complessivo circa **£63k**
- [[persona-yohann-bensadoun]] (Operations) sta cercando di riconciliare Stripe con le fatture Xcel
- L'export dalla piattaforma WooCommerce non è affidabile perché include gli ordini omaggio a prezzo facciale, ma non incassati
- La fonte di verità corretta è **Stripe** (lato Stuart)
- [[persona-mateo-noceti]] e Yohann coinvolti nel follow-up operativo; [[persona-sonia-gastelum]] informata

## Punti da rinegoziare nel nuovo contratto

1. **Prezzo per ordine vs per articolo** — il pricing Xcel deve allinearsi alla struttura reale degli ordini (multi-articolo)
2. **Gestione degli omaggi** — definire chi sostiene il costo Xcel per ordini a £0 lato corriere
3. **Meccanismo di riconciliazione** — Xcel non ha accesso a Stripe; serve un processo di data sharing per evitare discrepanze future
4. **Retroattività** — chiarire se e come la £63k viene ripartita tenendo conto degli ordini omaggio e multi-articolo

## Vedi anche

[[area-fp-and-a]] — [[entity-stuart]] — [[persona-sonia-gastelum]]
