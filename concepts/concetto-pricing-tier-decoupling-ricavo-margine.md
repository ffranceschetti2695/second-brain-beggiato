---
title: "Pricing a tier: quando Ricavo e Gross Margin si disaccoppiano"
summary: "Con un pricing a soglie di volume, un aumento di volume può ridurre il margine anche se il ricavo sale: superare una soglia (tier) abbassa la tariffa netta su tutto il volume di quel mese."
tags: [concepts, fp-and-a, pricing, forecasting]
status: active
created: 2026-07-14
updated: 2026-07-14
related: ["[[entity-stuart]]", "[[concetto-rpo-cpo-slo]]", "[[data-tesco-pricing-tiers-fc6]]", "[[concetto-stuart-modelli-revenue]]"]
---

# Pricing a tier: quando Ricavo e Gross Margin si disaccoppiano

## Il meccanismo

Quando un cliente ha un contratto **a tier di volume** (es. [[data-tesco-pricing-tiers-fc6]]: sotto una soglia mensile di consegne si applica un RPO più alto, sopra una soglia più alta si applica un RPO più basso), un'ipotesi di crescita del volume non è semplicemente "più consegne allo stesso prezzo". Se la crescita fa scavalcare una soglia di tier, **tutto il volume di quel mese** ricade sulla tariffa netta più bassa, non solo l'incremento marginale.

Questo produce un effetto controintuitivo: **una crescita di volume moderata può generare meno ricavo (o meno margine) di una crescita nulla o di una crescita forte**, perché la crescita moderata è proprio quella che rischia di far scattare il tier peggiore senza guadagnare abbastanza volume da compensare la tariffa più bassa. Una crescita forte, che supera abbondantemente la soglia, o un volume piatto che resta sotto, possono entrambi risultare in un esito migliore della via di mezzo.

## Perché il Ricavo può salire mentre il Gross Margin scende

Il Gross Margin per consegna è `RPO − CPO` ([[concetto-rpo-cpo-slo]]). Se il CPO (costo per consegna) è già vicino o sopra l'RPO ri-tierizzato in un dato mese, aggiungere volume a quel margine unitario sottile o negativo **peggiora il Gross Margin anche se il Ricavo aggregato aumenta** (più consegne × RPO più alto in valore assoluto, ma margine per consegna più basso o negativo). Un'ipotesi di crescita valutata solo sul Ricavo può quindi nascondere un impatto opposto sul margine.

## Applicazione pratica

Quando si modella un'ipotesi di crescita volume su un cliente con pricing a tier:
1. **Non applicare mai una % piatta al ricavo** — va applicata al volume, poi il nuovo volume aggregato va ri-tierizzato contro la tabella tariffaria reale.
2. **Verificare mese per mese se la soglia viene scavalcata**, non solo il totale annuo — l'effetto tier-cliff è mensile.
3. **Controllare sempre l'impatto su Gross Margin separatamente dal Ricavo** — non assumere che vadano nella stessa direzione.

## Esempio osservato

Nel reforecast FC6 2026 di Tesco UK, un'ipotesi di +4% di volume in H2 ha fatto scavalcare la soglia dei tier in più mesi. A settembre, il +4% di volume ha effettivamente *ridotto* il ricavo del mese, perché il volume è passato dalla fascia sotto-soglia (tariffa più alta) alla fascia successiva (tariffa più bassa) senza guadagnare abbastanza volume da compensare. Sull'intero H2, l'aggiustamento ha aggiunto ricavo ma **ridotto il Gross Margin complessivo** del cliente, perché diversi mesi avevano già un CPO superiore all'RPO ri-tierizzato.

## Vedi anche

[[entity-stuart]] — [[concetto-stuart-modelli-revenue]]
