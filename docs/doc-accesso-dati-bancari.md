---
title: "Doc — Accesso programmatico ai dati bancari (Illimity & AMEX)"
summary: "Verdetto su come accedere ai propri dati Illimity e AMEX in Italia da privato senza P.IVA: Enable Banking funziona per Illimity, nessun aggregatore raggiunge AMEX, resta l'export Excel."
tags: [docs, finance, automation]
status: active
created: 2026-06-29
updated: 2026-06-29
related: ["[[progetto-finance-dashboard]]", "[[concetto-automazione-local-first]]", "[[doc-launchd-automazioni-mac]]"]
---

# Doc — Accesso programmatico ai dati bancari (Illimity & AMEX)

Ricerca del 2026-06-29 su come un **privato in Italia senza P.IVA** può accedere ai propri dati
bancari per automazioni. Sapere riusabile (vale anche oltre la [[progetto-finance-dashboard]]).

## Illimity — RISOLTO (Enable Banking)

- **Enable Banking** (aggregatore PSD2) funziona: JWT RS256, sessione OAuth ~89 giorni.
- Verificato: restituisce transazioni day-by-day (`booking_date`, `credit_debit_indicator`
  DBIT/CRDT, importo) + saldo dall'endpoint `/balances` ("Interim booked balance").
- Un privato può partire (sandbox + production iniziale); il modello commerciale pieno presuppone
  KYB aziendale, ma per uso personale funziona.

## AMEX Italia — nessuna via API senza P.IVA

- **Salt Edge**: rifiuta i privati, richiede società/P.IVA registrata. (Rifiuto ricevuto 2026-06-29.)
- **Enable Banking**: American Express NON è nel catalogo ASPSP italiano. In Italia le carte di
  credito sono il buco nero del PSD2.
- **GoCardless / Nordigen**: storicamente la più amichevole per i privati, ma **chiusa ai nuovi
  iscritti da luglio 2025**.
- **PSD2 di AMEX**: l'AIS reale è frammentato per entità nazionale (UK/FR), non esposto per la
  carta personale italiana. Gli aggregatori che "vedono" Amex lo fanno via UK/FR.
- **API personale Amex**: non esiste. Le API developer sono B2B.
- **Email per-transazione**: il servizio "Alert" italiano manda saldo/scadenze, NON una mail per
  ogni acquisto, e non è abilitabile. Via morta per il parsing email.

## Cosa resta per AMEX

- **Export Excel** da americanexpress.it (Conto → Transazioni → download): completo al 100%,
  gratis, senza licenza. È la via adottata.
- **Automazione browser** (Playwright): TESTATA e ABBANDONATA — AMEX blocca il login
  automatizzato via anti-bot (fingerprinting al login). Forzarla rischia il blocco account.
- **Soluzione adottata: auto-ingest da Downloads.** Login manuale normale (no automazione) +
  click "scarica Excel"; un watcher launchd (WatchPaths su ~/Downloads, vedi
  [[doc-launchd-automazioni-mac]]) riconosce il file dal contenuto, lo sposta in `amex-inbox/` e
  rigenera dashboard+email da solo. Affidabile, zero lotta con l'anti-bot, attrito minimo (solo
  login+download quando vuoi dati freschi). Questo è un caso di [[concetto-automazione-local-first]]:
  rete e secret stanno sul Mac, e il punto di automazione è a valle del login anti-bot.

## Conclusione operativa

Illimity = automatico (Enable Banking). AMEX = export Excel periodico. Per una SaaS multi-tenant
servirebbe comunque una società registrata + un aggregatore con licenza.
