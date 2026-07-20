---
title: "Progetto — Speed to Lead"
summary: "Demo di agente vocale per la qualifica lead di un'azienda di ispezioni immobiliari: da form Typeform a chiamata automatica con booking, costruita per un amico."
tags: [projects, ai]
status: active
created: 2026-07-11
updated: 2026-07-20
related: ["[[progetto-ops-dashboard]]", "[[progetto-company-brain]]", "[[concetto-claude-code-vs-api-billing]]"]
---

# Progetto — Speed to Lead

Demo/lab, non un progetto Stuart: agente per la qualifica automatica dei lead di un'azienda di ispezioni immobiliari (home inspection), costruito per un amico. Riceve un form compilato, valuta il lead con Claude e, se promettente, chiama la persona al telefono per fissare un appuntamento.

## Dove vive il codice

Il codice NON sta nel vault. Vive in:

```
/Users/f.franceschetti/Projects/speed-to-lead
```

Repo GitHub: https://github.com/ffranceschetti2695/speed-to-lead

Per avviarlo:

```
cd /Users/f.franceschetti/Projects/speed-to-lead
npm install
node src/index.js   # legge PORT da .env, default 3000
```

Le credenziali reali (Twilio, ElevenLabs, Cal.com, Claude, Google service account) vanno in un file `.env` locale, mai committato (vedi `.env.example` per le chiavi richieste).

## Flusso

1. **Webhook** — `POST /webhook/typeform` riceve il form (name, phone, email, serviceNeeded, problem).
2. **Scoring** — il lead viene inviato a Claude, che restituisce score 1-10, tier (Hot/Warm/Cold), urgency, valore stimato del lavoro, segnali chiave, nota di follow-up.
3. **Chiamata** — se il tier è Hot o Warm ed esiste un telefono, parte una chiamata Twilio in uscita.
4. **Conversazione vocale** — 4 step con `<Gather>` di Twilio: saluto e domanda sul problema → salvataggio problema e richiesta giorno/ora → controllo disponibilità su Cal.com e proposta slot più vicino → conferma e prenotazione.
5. **Voce** — sintesi con ElevenLabs (eleven_turbo_v2), fallback su `<Say>` di Twilio se la sintesi fallisce.
6. **Registrazione** — ogni lead viene loggato su Google Sheets con 15 colonne (score, tier, esito chiamata, prenotazione, ecc.).

## Stack

| Layer | Tecnologia |
|---|---|
| Server | Node.js + Express (CommonJS) |
| Scoring lead | Claude (Anthropic SDK) |
| Telefonia | Twilio (chiamata + `<Gather>`) |
| Voce | ElevenLabs (text-to-speech) |
| Booking | Cal.com API v2 |
| Log | Google Sheets (service account) |

## Deploy (VPS Hostinger)

L'app gira in produzione su un VPS Hostinger tramite il prodotto "Hermes agent" (dominio `hermes-agent-7ie1.srv1822279.hstgr.cloud`), non su Vercel/Railway. Il `docker-compose.yml` vive sul VPS in `/docker/lead-app/` e clona il repo GitHub ad ogni avvio del container (non è un'immagine pre-buildata).

Una copia locale del compose file, con **tutte le credenziali reali in chiaro** (Twilio, ElevenLabs, Cal.com, Anthropic, Google service account, più un GitHub PAT), vive in `~/Desktop/speed-to-lead-docker-compose.yml` — fuori dal vault e fuori da git, stesso trattamento del file `credenziali.md` sul Desktop.

**Gotcha da ricordare per prossimi deploy simili**: il repo GitHub è privato, quindi il clone nel `command:` del compose richiede un token nell'URL (`https://${GITHUB_TOKEN}@github.com/...`). Ma l'interpolazione `${GITHUB_TOKEN}` dentro `command:`/`labels` viene risolta da **Docker Compose leggendo l'host** (variabili di shell o un file `.env` accanto al `docker-compose.yml`), **non** dalla sezione `environment:` del container — quella è visibile solo dentro il container a runtime, troppo tardi per l'interpolazione del file YAML. Il fix è stato creare un secondo file `.env` in `/docker/lead-app/.env` sul VPS con `GITHUB_TOKEN=...`, poi `docker compose up -d --force-recreate`. Senza quel file, il container entra in loop di restart con `fatal: could not read Password for 'https://github.com'`.

## Stato (2026-07-13)

Deploy reale su VPS Hostinger (Docker + Hermes agent + Traefik come reverse proxy), non più solo locale. Flusso end-to-end funzionante: webhook → scoring Claude → chiamata Twilio → conversazione vocale in italiano → tentativo di prenotazione Cal.com. Testato sia via Typeform reale sia via `curl` diretto al webhook (fallback già previsto nel codice per bypassare il limite mensile di risposte gratuite di Typeform).

### Bug trovati e corretti in questa sessione (tutti pushati su GitHub, repo privato)

- **Traefik**: label di routing sul VPS puntava a un server ID sbagliato (`srv1629360` invece di `srv1822279`) → 302 verso login di Hermes invece di raggiungere l'app. Corretto direttamente nel `docker-compose.yml` sul VPS.
- **leadScorer.js**: assumeva `message.content[0]` sempre di tipo testo, ma Claude a volte restituisce prima un blocco "thinking" → crash su `.trim()`. Corretto cercando il blocco `type === 'text'`, più pulizia dei fence markdown attorno al JSON.
- **webhook.js — matching campi**: confrontava il titolo della domanda per uguaglianza esatta con alias brevi, ma i titoli reali di Typeform sono frasi intere → nessun campo mai estratto. Corretto con matching a sottostringa.
- **webhook.js — bug più a monte**: il codice leggeva `answer.field.title`, che in Typeform **non esiste** nell'array `answers[]` (il titolo vive solo in `definition.fields[]`, collegato tramite `ref`). Corretto costruendo una mappa `ref → title`.
- **Numero di telefono non normalizzato**: Twilio interpretava un numero italiano senza `+39` come numero USA (`+1...`), risultando "non verificato". Aggiunta normalizzazione E.164, poi estesa anche al percorso di test manuale via `curl` (inizialmente applicata solo al percorso Typeform).
- **twiml.say() ordine argomenti sbagliato**: `say(testo, attributi)` invece di `say(attributi, testo)` — la lingua `it-IT` veniva ignorata, da cui la voce inglese che leggeva testo italiano. Corretto; testi del flusso vocale tradotti in italiano; regex di conferma aggiornata da "yes" a "sì".
- **Cal.com `/slots`**: parametri sbagliati (`startTime` invece di `start`+`end`, entrambi obbligatori), header `cal-api-version` sbagliato per questo endpoint specifico (serve `2024-09-04`, diverso da quello per `/bookings` che resta `2024-08-13`), e parsing della risposta sbagliato (il codice si aspettava un array flat `slots[]`, la risposta reale è raggruppata per data sotto `data{}`). Tutti corretti verificando la documentazione ufficiale Cal.com.
- **ElevenLabs 402 (diagnosticato, non risolvibile via codice)**: confermato dal body dell'errore — `"Free users cannot use library voices via the API"`. Le voci prese dalla Voice Library richiedono un piano a pagamento, indipendentemente dai crediti disponibili. Nel frattempo il fallback su `<Say>` di Twilio (ora corretto in italiano) copre la demo.

### Note di sicurezza emerse

Diverse credenziali reali sono finite in chiaro in screenshot durante il debug (GitHub PAT, Anthropic API key, Twilio SID/Auth Token, ElevenLabs key, Cal.com key, chiave privata service account Google) → **da ruotare tutte se non ancora fatto**, e aggiornare il `docker-compose.yml` sul VPS di conseguenza.

## Aperto

- **Decisione ElevenLabs**: upgrade del piano per sbloccare le voci Library via API, oppure trovare una voce non-Library nell'account (My Voices, non Voice Library), oppure accettare il fallback Twilio `<Say>` per questa demo.
- **Log di debug da rimuovere**: `webhook.js` contiene ancora `console.log` temporanei (`DEBUG lead/scoring/shouldCall/call placed/failed`) aggiunti per diagnosi — da ripulire quando il flusso sarà considerato stabile.
- **Preferenza giorno/orario del chiamante non usata**: la domanda vocale "che giorno e orario preferisce?" viene fatta ma la risposta non è mai usata — il sistema propone sempre il primo slot Cal.com disponibile, ignorando la preferenza. Comportamento voluto dal prompt originale, ma da rivalutare se serve un'esperienza più realistica.
- **Booking end-to-end non ancora confermato con successo** dopo i fix Cal.com: manca un test completo fino alla conferma vocale "sì" con verifica dell'evento su Cal.com Bookings / Google Calendar (`f.franceschetti@stuart.com`).
- **Limite mensile Typeform raggiunto**: da qui in avanti i test si fanno via `curl` diretto al webhook (fallback già presente nel codice), non serve upgrade Typeform per continuare a testare.
- Nessuna validazione della firma webhook su `/webhook/typeform` o `/voice/*` — accettabile per demo, da aggiungere se questo diventa produzione reale.

## Vedi anche

[[progetto-ops-dashboard]] — [[progetto-company-brain]] — [[concetto-claude-code-vs-api-billing]]
