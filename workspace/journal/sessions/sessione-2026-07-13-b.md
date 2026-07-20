---
title: "Sessione 2026-07-13-b"
summary: "Raccolta credenziali Speed to Lead, scaffold iniziale dell'app e primo deploy su VPS Hostinger con debug del routing"
tags: [workspace, type/session]
status: done
created: 2026-07-13
updated: 2026-07-13
related: ["[[progetto-speed-to-lead]]"]
---

## Fatto

Raccolte le credenziali del progetto Speed to Lead in `~/Desktop/credenziali.md` (Hermes, Claude API, Twilio, ElevenLabs, Cal.com, Typeform, Google service account, GitHub PAT). Costruito da zero lo scaffold Node.js/Express dell'app (webhook Typeform, scoring Claude, chiamata Twilio, voce ElevenLabs, booking Cal.com, log Google Sheets), testato in locale e pushato su `github.com/ffranceschetti2695/speed-to-lead`. Fatto il primo deploy su VPS Hostinger via Docker Compose, con debug end-to-end fino all'health check pubblico funzionante.

## Deciso

- Codice fuori dal vault, in `~/Projects/speed-to-lead`; nota atomica in `projects/progetto-speed-to-lead.md`.
- Repo GitHub privato: il clone nel deploy richiede un `GITHUB_TOKEN` passato via URL, letto da un file `.env` separato accanto al `docker-compose.yml` sul VPS (l'interpolazione Compose non legge la sezione `environment:` del container).
- Il file locale `~/Desktop/speed-to-lead-docker-compose.yml`, con tutte le credenziali reali in chiaro, resta fuori da git e dal vault.
- Il dominio corretto del VPS è `srv1822279` (non `srv1629360`, refuso ereditato dal template di partenza) — fix applicato e verificato dall'utente.

## Aperto

Nessun nuovo step: l'unico emerso in sessione (fix del server ID nel compose) è stato risolto e verificato prima della chiusura. Restano validi gli item già presenti in `open-items.md` sotto "Speed to Lead" (rotazione credenziali, decisione ElevenLabs, log di debug da rimuovere, test booking end-to-end, verifica esposizione codice su repo terzo).
