---
title: "Aggiustamenti di forecast: baked-in vs bolt-on"
summary: "Per correggere un forecast, modificare direttamente gli input del modello (Volume/RPO) è più coerente che aggiungere una colonna di overlay: i costi e il margine si ricalcolano da soli e non rischiano di disallinearsi."
tags: [concepts, fp-and-a, forecasting, excel]
status: active
created: 2026-07-14
updated: 2026-07-14
related: ["[[concetto-fpa]]", "[[concetto-pricing-tier-decoupling-ricavo-margine]]", "[[concetto-rpo-cpo-slo]]", "[[progetto-fc6-topline-proposal]]"]
---

# Aggiustamenti di forecast: baked-in vs bolt-on

## I due approcci

Quando si vuole correggere o proporre un aggiustamento a un numero di forecast già modellato in un file (es. Excel), ci sono due modi:

1. **Bolt-on (overlay)**: si lascia il numero originale intatto e si aggiunge una colonna/cella separata con `= originale + aggiustamento`. Il modello di base non viene toccato.
2. **Baked-in (incorporato)**: si modificano direttamente le celle di input che alimentano il numero (es. Volume o RPO/prezzo), lasciando che le formule esistenti (Ricavo, Costi, Margine) si ricalcolino da sole.

## Perché baked-in è preferibile quando il modello lo permette

Se un foglio ha già le formule corrette e collegate (es. `Ricavo = Volume × RPO`, `Costi = Volume × CPO`, `Margine = Ricavo + Costi`), modificare solo gli input mantiene tutto **automaticamente coerente**: cambiare il Volume aggiorna da solo Ricavo, Costi e Margine, senza bisogno di ricalcolare a mano ogni riga collegata.

L'approccio bolt-on invece rischia di **disallinearsi**: il Ricavo "proposto" sale nella colonna di overlay, ma i Costi e il Margine nel resto del foglio restano ancorati al Volume originale — l'aggiustamento non si propaga a valle, e chi legge il file può facilmente prendere per buono un Margine che non riflette l'aggiustamento di Ricavo.

## Quando il bolt-on resta necessario

Se il driver dell'aggiustamento non è chiaramente riconducibile a un input esistente del modello (es. un ricavo ancillary che vive su una riga/tab separata, non collegata al Volume del cliente), forzarlo dentro Volume o RPO lo classificherebbe in modo scorretto. In quel caso l'overlay bolt-on — o meglio, una riga dedicata nella sezione corretta del modello — resta la scelta giusta.

## Esempio osservato

Nel [[progetto-fc6-topline-proposal]] (FC6 2026), un primo giro di aggiustamenti (Tesco, Zapp, Sushi Shop) era stato costruito come overlay bolt-on, mentre solo un quarto (FR Existing SMB, correzione RPO) era stato incorporato direttamente nell'input. Dopo revisione, tutti e quattro sono stati convertiti allo stesso trattamento baked-in, per garantire che Excel e il documento di analisi restassero sempre coerenti tra loro senza rischio di disallineamento.

## Vedi anche

[[concetto-fpa]] — [[concetto-pricing-tier-decoupling-ricavo-margine]] — [[concetto-rpo-cpo-slo]]
