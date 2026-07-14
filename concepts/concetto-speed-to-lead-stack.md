---
title: "Stack tecnico — Speed to Lead"
summary: "Perché ogni layer dello stack dell'agente vocale Speed to Lead esiste e come si incastrano tra loro"
tags: [concepts, ai]
status: active
created: 2026-07-14
updated: 2026-07-14
related: ["[[progetto-speed-to-lead]]", "[[concetto-claude-code-vs-api-billing]]"]
---

# Stack tecnico — Speed to Lead

Cinque servizi esterni più un server Node, ognuno responsabile di un solo pezzo della catena "form compilato → lead qualificato → chiamata prenotata". Nessuno di questi sostituisce un altro: sono scelti perché coprono capacità che gli altri non hanno.

## I layer e il perché

- **Node.js + Express** — il server che riceve il webhook Typeform e orchestra la sequenza. Scelto per semplicità: nessun bisogno di un framework più pesante per un flusso lineare webhook → scoring → chiamata → log.
- **Claude (Anthropic SDK)** — legge i dati grezzi del lead (nome, problema, servizio richiesto) e restituisce un giudizio strutturato: score 1-10, tier (Hot/Warm/Cold), urgenza, valore stimato del lavoro. È il layer di ragionamento: gli altri servizi eseguono azioni, Claude decide se e come agire. Consuma crediti API a parte, non l'abbonamento Claude Code — vedi [[concetto-claude-code-vs-api-billing]].
- **Twilio** — telefonia: piazza la chiamata in uscita e gestisce il flusso `<Gather>` (raccolta di risposte vocali step-by-step). È l'unico layer che sa parlare con la rete telefonica reale.
- **ElevenLabs** — sintesi vocale di qualità (text-to-speech) per rendere la voce naturale invece del `<Say>` robotico di Twilio. Con fallback su Twilio `<Say>` quando ElevenLabs fallisce (es. restrizioni di piano sulle voci Library).
- **Cal.com (API v2)** — booking: controlla disponibilità e crea l'evento quando il lead conferma. Scelto perché espone un'API di scheduling già pronta, senza dover costruire una logica di calendario custom.
- **Google Sheets (service account)** — log persistente e leggibile da umani di ogni lead processato (15 colonne: score, tier, esito chiamata, prenotazione, ecc.). Serve da audit trail e da posto dove l'amico può controllare i risultati senza toccare codice.

## Perché non un solo provider "tutto in uno"

Nessuno dei provider vocali all-in-one (es. Vapi, Bland) è stato usato: lo stack è composto manualmente layer per layer. Questo dà controllo granulare su ogni step (in particolare sul prompt di scoring e sulla logica di booking), al costo di dover integrare e debuggare ogni pezzo separatamente — la maggior parte dei bug trovati in [[progetto-speed-to-lead]] nasce proprio dalle giunture tra un layer e l'altro (parsing risposte Cal.com, ordine argomenti Twilio, blocchi "thinking" di Claude).

## Deploy

Il server Node gira in un container Docker su una VPS Hostinger, dietro Traefik come reverse proxy, condividendo l'host con un'istanza del prodotto "Hermes agent". Il container clona il repo a ogni riavvio invece di usare un'immagine pre-buildata — dettaglio operativo, non parte dello stack applicativo in sé.

## Vedi anche

[[progetto-speed-to-lead]] — [[concetto-claude-code-vs-api-billing]]
