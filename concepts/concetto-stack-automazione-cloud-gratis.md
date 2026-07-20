---
title: "Stack: automazione personale always-on su cloud gratis"
summary: "Pattern riusabile per un'automazione personale che gira a orario fisso indipendentemente dai miei dispositivi: prendi dati, elabora, genera report, notifica, eseguita su CI cloud gratuita e sempre accesa."
tags: [concepts, automation, architettura, cloud]
status: active
created: 2026-06-30
updated: 2026-06-30
related: ["[[progetto-finance-dashboard]]", "[[concetto-automazione-local-first]]", "[[concetto-core-adapters-presentation]]", "[[doc-accesso-dati-bancari]]", "[[doc-launchd-automazioni-mac]]"]
---

# Stack: automazione personale always-on su cloud gratis

Pattern riusabile per un'automazione personale che deve girare a orario fisso a prescindere dai miei dispositivi (es. l'email finanziaria mattutina): **prendi dati, elabora, genera report, notifica**, eseguita su CI cloud gratuita e sempre accesa. È l'evoluzione di [[concetto-automazione-local-first]]: quel principio dice "esegui dove ci sono rete e secret"; GitHub Actions ha entrambi, quindi il cloud diventa la sede naturale quando non voglio dipendere dal laptop acceso.

## I pezzi e a cosa servono

- **GitHub Actions** — il motore sempre acceso che esegue il programma sui computer di GitHub, non sul Mac. È il cuore: rende la consegna indipendente dallo stato del laptop.
- **cron** — la sveglia: la riga che dice "esegui ogni giorno alle 07:50".
- **Python** — il linguaggio in cui è scritta tutta la logica (fetch dati, calcoli, costruzione dell'email).
- **API della fonte (Enable Banking per Illimity)** — il ponte verso i dati: un programma chiede i dati a un altro. Gira headless con chiave + sessione salvata, senza browser.
- **Relay dal Mac + GitHub contents API** — per le fonti irraggiungibili dal cloud (AMEX blocca il login automatizzato): un dispositivo che controllo carica il file nel repo nel momento in cui sono io a scaricarlo.
- **Playwright + Chromium headless** — un browser invisibile che apre la dashboard e cattura gli screenshot da incollare nell'email.
- **Gmail SMTP** — il postino che spedisce davvero l'email.
- **GitHub Secrets + Keychain** — la cassaforte: chiavi e password mai nel codice, passate al programma solo a runtime.

## Perché questa combo

Gratis, sempre attiva, nessun server da gestire o aggiornare, secret gestiti dal provider. Si appoggia bene alla struttura a strati di [[concetto-core-adapters-presentation]]: il `core` resta riusabile e cambia solo lo strato di accesso dati quando si passa da locale a cloud.

## Cosa migliorare / sapere la prossima volta

- **Il cron di GitHub è best-effort, non preciso al minuto.** Una schedule appena creata non parte se manca lead time: una aggiunta ~20 min prima dell'orario non è scattata affatto. Evitare gli slot di picco (:00 e :30 a metà giornata UTC). Per un timing garantito serve un trigger esterno (es. un cron service gratuito che chiama l'API di GitHub).
- **Resilienza agli errori a monte (rate limit / down dell'API).** Tenere uno snapshot "last known good" come fallback, così la notifica parte comunque; aggiungere retry/backoff. Nel caso reale il 429 di Enable Banking avrebbe bloccato tutto senza il fallback.
- **Decidere consapevolmente quali dati vivono nel repo (privacy).** Screenshot, template della dashboard e snapshot di transazioni sono dati finanziari a riposo sul provider. Repo privato + scelta esplicita, non per inerzia.
- **Secret solo nel secret store del provider**, mai nel codice o nel repo.
- **Alcune fonti non si raggiungono dal cloud** (login anti-bot come AMEX): usare come relay un dispositivo che controllo, sfruttando il momento in cui ci sono comunque io.

Caso reale e stato del progetto: [[progetto-finance-dashboard]]. Nodo accesso dati bancari: [[doc-accesso-dati-bancari]]. Alternativa di scheduling locale: [[doc-launchd-automazioni-mac]].
