---
title: "Automazione local-first (rete + secret)"
summary: "Un'automazione che chiama API esterne usando credenziali va eseguita dove ci sono rete e secret (il Mac), non in una sandbox cloud che le blocca."
tags: [concepts, automation, architettura]
status: active
created: 2026-06-30
updated: 2026-06-30
related: ["[[progetto-finance-dashboard]]", "[[doc-launchd-automazioni-mac]]", "[[doc-accesso-dati-bancari]]"]
---

# Automazione local-first (rete + secret)

Principio emerso costruendo la [[progetto-finance-dashboard]]. Quando un'automazione deve (a) chiamare API
esterne e (b) usare credenziali/secret, va ancorata **dove rete e secret esistono davvero**.

Le sandbox cloud degli assistenti (es. Claude Cowork) hanno **rete in uscita ristretta**: le
chiamate verso API esterne (banche, ecc.) tornano 403. Quindi un task schedulato in cloud non può
fare il fetch dei dati. La soluzione non è "insistere col cloud" ma spostare l'esecuzione **in
locale sul Mac** (cron/launchd, o Claude Code che gira nativo), dove la rete funziona e i secret
stanno nel Keychain. Il cloud, semmai, resta solo per pezzi senza rete (hosting di un artifact).

**Corollario anti-bot (login):** se il sito di origine blocca attivamente l'automazione del login
(fingerprinting anti-bot, es. American Express, vedi [[doc-accesso-dati-bancari]]), non combatterlo
— rischi il blocco account. Sposta
il punto di automazione **a valle del login**: l'utente fa login a mano e scarica il file, e
l'automazione parte da lì (vedi pattern auto-ingest da Downloads in [[doc-launchd-automazioni-mac]]).

**Regola pratica:** decidi prima DOVE gira ogni pezzo (rete? secret? scheduler affidabile?), poi
scrivi il codice. Vedi anche [[concetto-core-adapters-presentation]] per come strutturarlo.
