---
title: "Sessione 2026-07-16"
summary: "Actualizzazione completa del file FC6 Topline Proposal (giugno su tutte le tab), rifinitura RPO FR SMB, nota su re-forecast Tesco e messaggio a Mark Jones su RPO/CPO"
tags: [workspace, type/session]
status: done
created: 2026-07-16
updated: 2026-07-16
related: ["[[progetto-fc6-topline-proposal]]", "[[data-tesco-reforecast-luglio-2026-zone-exits]]", "[[data-tesco-pricing-tiers-fc6]]", "[[doc-tone-of-voice]]", "[[entity-stuart]]"]
---

## Fatto

Nel file Excel di lavoro del FC6 Topline Proposal (`~/Desktop/FC6_Topline_Proposal/`), giugno 2026 è stato actualizzato con i dati DWH su tutte e tre le tab (UK/FR/PL), non solo sui 4 item già committed. La RPO di FR Existing SMB è stata rifinita usando `active_client_tier = 'SMB'` (confermato superset di `is_self_sign_up`), e un intero recalculation del workbook (Python `formulas`) ha verificato i nuovi totali contro il DWH, scoprendo e correggendo un arrotondamento errato sulla CPO di Tesco di un round precedente. Creata la nota [[data-tesco-reforecast-luglio-2026-zone-exits]] sul re-forecast Tesco condiviso da Vaibhav Anand, corretta poi per riflettere che l'uscita da alcune zone/città UK è una decisione strategica di Stuart (non profittevoli/performance), non un rifiuto o un ritiro volume da parte del cliente. Craftato e iterato (4 round) un messaggio Slack per Mark Jones sul nesso RPO/CPO di Tesco, usato come spunto per aggiornare [[doc-tone-of-voice]] con due regole nuove: non suonare mai come una giustificazione/difesa, e controllare sempre le DM col destinatario prima di scrivere (per calibrare, non per copiarne lo stile).

## Deciso

- Metodologia SMB unificata su `active_client_tier` per tutte le country tab, sostituendo il proxy `is_self_sign_up` usato in precedenza solo per FR.
- Il Word doc e lo Slack draft del FC6 Topline Proposal NON vengono rigenerati in questa sessione: Francesco ha scelto di fermarsi dopo l'Excel, rimandando la rigenerazione dei ~15 chart e delle sezioni testuali.
- Il landing point revenue 2026 non viene ricalcolato con il vero re-forecast Tesco (volumi in calo per zone exits) in questa sessione.
- Nessun nuovo open item viene aggiunto a `open-items.md`: Francesco ha rifiutato esplicitamente la proposta di tracciare i follow-up sopra (Word doc/Slack draft, ricalcolo landing point, invio messaggio a Mark).

## Aperto

Nessuno (per scelta esplicita di Francesco in chiusura sessione).
