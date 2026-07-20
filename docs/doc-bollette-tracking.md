---
title: "Tracking bollette personali (skill /bills)"
summary: "Dove vivono lo storico delle bollette (CSV) e la skill che lo aggiorna, per rispondere a domande come 'quanto pago di luce' o 'media di aprile'"
tags: [docs, finance, reference]
status: active
created: 2026-07-15
updated: 2026-07-15
related: ["[[progetto-finance-dashboard]]"]
---

# Tracking bollette personali

Storico mensile delle spese fisse e variabili di casa (Madrazo 32, Barcelona): affitto, palestra,
telefono, luce, gas, acqua. Nato da una sessione di pulizia della seconda casella Gmail
(`francesco.franceschetti2695@gmail.com`), dove arrivano le fatture.

## Dove vivono i dati

I numeri **non stanno nel vault** (sono dati numerici riderivabili dalla fonte, sotto la soglia di
creazione nota di `CLAUDE.md`). Vivono in:

```
~/Documents/Bank Accounts/bills-history.csv
```

Una riga per bolletta: `date,category,amount,period_start,period_end,period_days,month,notes`.
`category` è una di: `rent`, `electricity`, `gas`, `water`, `movistar`, `fitness_park`.

## Come si aggiorna

Skill `/bills` (in `.claude/commands/bills.md`, in questo vault). Cerca solo le fatture arrivate
dopo l'ultima data già registrata per categoria (non "dall'inizio del mese corrente"), quindi
recupera automaticamente eventuali mesi saltati. Per luce e gas l'importo è dentro un grafico
generato dinamicamente da Endesa (non testo, non un PDF semplice): la skill scarica l'immagine e la
legge via vision. Affitto (€1.340) e palestra Fitness Park (€27) sono costanti fisse, nessuna email.

Ogni run stampa in chat una tabella riassuntiva (Bills + Rent + Fitness Park + Totale per mese), una
tabella dettagliata per categoria con due medie (con/senza mesi a zero), e un breve commento sul
mese appena chiuso vs la media.

## Come interrogarlo

Per domande dirette ("quanto pago di acqua", "qual è la media di aprile", "quanto ho pagato di luce
a marzo"), leggere direttamente `bills-history.csv` invece di lanciare `/bills` per intero — la
skill serve per aggiungere nuovi mesi, non per ogni singola domanda di lettura.

## Vedi anche

[[progetto-finance-dashboard]] — [[doc-accesso-dati-bancari]] — [[self-franceschetti]]
