---
title: "Progetto — Personal Finance Dashboard"
summary: "Dashboard finanziaria personale + automazione locale giornaliera (Illimity via Enable Banking, AMEX via export Excel) che controlla la spesa MTD vs forecast. Prototipo verso una futura SaaS."
tags: [projects, finance, automation]
status: active
created: 2026-06-29
updated: 2026-06-29
related: ["[[progetto-ops-dashboard]]", "[[stato-stream-ai]]", "[[concetto-core-adapters-presentation]]", "[[concetto-automazione-local-first]]", "[[doc-accesso-dati-bancari]]", "[[doc-launchd-automazioni-mac]]", "[[doc-stuart-design-system]]"]
---

# Progetto — Personal Finance Dashboard

Dashboard finanziaria personale (HTML autocontenuto + Chart.js) con automazione che ogni mattina
calcola quanto è stato speso il giorno prima e proietta la spesa di fine mese vs un forecast
(check "MTD vs forecast"). Nato come strumento personale, pensato come prototipo/MVP di una futura
SaaS per la gestione finanziaria personale.

## Dove vive il codice

Il codice NON sta nel vault. Vive in:

```
/Users/f.franceschetti/Documents/Bank Accounts
```

Leggere il `CLAUDE.md` di quella cartella a inizio sessione: contiene architettura, file map,
setup e problemi aperti.

## Architettura (v2, locale)

Riprogettato il 2026-06-29 da Cowork (sandbox senza rete → non poteva chiamare le API bancarie)
ad architettura **tutta locale sul Mac**, dove la rete funziona (principio
[[concetto-automazione-local-first]]). Struttura a tre strati, vedi [[concetto-core-adapters-presentation]]:

- `run_daily.py` — entry point unico, lanciato da `launchd` ogni mattina alle 7:50 (vedi
  [[doc-launchd-automazioni-mac]]).
- `core/` — logica pura riusabile (mese finanziario 27→26, categorizzazione, proiezione MTD).
  È il "cuore" già pronto per il salto SaaS: cambia solo lo strato dati.
- `adapters/` — accesso dati per-fonte (Illimity via Enable Banking; AMEX via export Excel).
- `presentation/` — render della dashboard HTML + invio email SMTP (vedi
  [[doc-email-da-script-macos]] e lo snapshot su telefono in [[doc-dashboard-telefono-screenshot-email]]).

## Il nodo dati: AMEX

Vedi [[doc-accesso-dati-bancari]]. In sintesi: **nessun aggregatore PSD2 raggiunge la carta Amex
personale italiana senza P.IVA** (Salt Edge rifiuta i privati, Enable Banking non ha Amex IT,
GoCardless chiuso ai nuovi). Illimity invece è pienamente automatico via Enable Banking. AMEX si
aggiorna droppando l'export Excel di americanexpress.it in `amex-inbox/`.

## Stato attuale (2026-06-29) — cosa funziona

- **Illimity day-by-day + saldo**: ✅ automatico via Enable Banking (verificato dal vivo: 81 txn
  con data/segno/importo + saldo €13.883,72). Era un falso problema il `balance: null` (JSON vecchio).
- **Bug dashboard `NaN`**: ✅ risolto (guard su `balance` null nella tab MTD).
- **Email mattutina**: ✅ funziona davvero (testata, ricevuta). Invio SMTP Gmail + app-password nel
  Keychain (risolto anche un problema di certificati SSL del Python.framework via `certifi`).
  Contiene: dettaglio voce-per-voce delle spese di IERI (Illimity + AMEX), aggregato spese del mese,
  e risparmi del mese = income (3662) − spese MTD. Recapito: francesco.franceschetti2695@gmail.com.
- **Scheduler 7:50**: ✅ attivo (launchd `com.francesco.finance.daily`).
- **AMEX**: ✅ via **auto-ingest da Downloads**. L'automazione browser (Playwright) è stata testata
  ma ABBANDONATA perché AMEX blocca il login automatizzato (anti-bot). Flusso scelto: login manuale
  normale + "scarica Excel" → un watcher launchd (`com.francesco.finance.downloads`, WatchPaths su
  ~/Downloads) riconosce il file, lo sposta in `amex-inbox/` e rigenera dashboard+email da solo.
- **Dashboard da telefono**: ✅ risolto in due modi. (a) **Screenshot inline di ogni tab nell'email
  mattutina** (Playwright cattura le 8 tab → incorporate nell'email): si vede tutto da qualsiasi rete,
  anche dati, senza server. (b) Mini-server locale (launchd, porta 8765) per la WiFi di casa:
  `http://192.168.1.83:8765/dashboard.html`, serve SOLO `public/` (secret mai esposti). Per la visione
  live interattiva fuori casa: opzione Tailscale.
- **Sicurezza**: secret a `chmod 600`, cartella non-git.

## Setup residuo (comandi che attiva Francesco)

I LaunchAgent persistenti li attiva l'utente (il classifier blocca l'installazione automatica). Vedi
i comandi nel `CLAUDE.md` della cartella. In sintesi: attivare i 3 plist (`daily`, `downloads`,
`server`) con `launchctl bootstrap`. App-password Gmail già nel Keychain.

## Direzione futura — SaaS

Il `core/` (categorizzazione, matematica MTD, forecast, mese finanziario) è riutilizzabile tale e
quale. Per una SaaS multi-tenant cambierebbe lo strato di accesso dati (servirebbe un aggregatore
"vero" con società registrata e licenza) e l'hosting cloud. La versione locale di oggi valida il
prodotto su un utente reale (Francesco) prima del salto. Per UI di prodotto o slide/demo on-brand
si può attingere al [[doc-stuart-design-system]].
