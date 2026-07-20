---
title: "Sessione 2026-07-20-e"
summary: "Ripresa del progetto Speed to Lead: pulizia open items, nota di stack tecnico committata, spiegazione high-level in inglese (Word) per Francesco"
tags: [workspace, type/session]
status: done
created: 2026-07-20
updated: 2026-07-20
related: ["[[progetto-speed-to-lead]]", "[[concetto-speed-to-lead-stack]]"]
---

## Fatto

Ripreso il progetto Speed to Lead (agente vocale demo per un'azienda di ispezioni immobiliari, costruito per Giovanni Beggiato). Rimosso il punto sulla rotazione credenziali dagli open items del progetto (già confermato risolto). Creata e committata nel vault la nota `concetto-speed-to-lead-stack.md` che spiega perché ogni layer dello stack (Node, Claude, Twilio, ElevenLabs, Cal.com, Google Sheets) esiste. Su richiesta di Francesco, scritta una spiegazione completamente non tecnica del progetto per un pubblico non esperto: prima in italiano, poi rifatta in inglese col nome `PROJECT-OVERVIEW.md` e convertita in un file Word (`Speed to Lead - Project Overview.docx`), entrambi salvati nella cartella del progetto (`~/Projects/speed-to-lead`, fuori dal vault). Il documento include anche una sezione che spiega, file per file, a cosa serve ogni elemento della cartella del progetto, e una sezione dedicata a cosa è stato effettivamente ripreso dal prompt originale di Giovanni Beggiato (via Notion) rispetto a cosa è stato corretto durante il debug. Chiarito a Francesco anche il ruolo di Hermes: solo hosting/routing condiviso sulla VPS (Traefik), nessun ruolo nella logica dell'agente.

## Deciso

Il documento esplicativo per Francesco vive fuori dal vault, nella cartella di progetto, non come nota Obsidian: è materiale di onboarding/riferimento per lui, non knowledge atomica da collegare al grafo. Mantenuta comunque una versione `.md` come sorgente editabile accanto al `.docx` consegnato.

## Aperto

Nessun nuovo step aperto emerso in questa sessione.
