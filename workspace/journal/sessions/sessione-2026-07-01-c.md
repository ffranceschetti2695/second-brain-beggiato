---
title: "Sessione 2026-07-01"
summary: "Migliorato il workflow della skill journal: open-items.md come fonte di verità degli step aperti"
tags: [workspace, type/session]
status: done
created: 2026-07-01
updated: 2026-07-01
related: ["[[progetto-company-brain]]", "[[area-ai-business]]"]
---

## Fatto

Rivisto e migliorato il workflow della skill `journal`. Adottato `open-items.md` come fonte di verità degli step aperti, in sostituzione della lettura dell'ultima sessione. Estratto e ripulito gli open items da tutte le sessioni passate (20 note), rimossi gli item già completati, organizzato in 5 workstream (Stuart, AI / Company Brain, Finance Dashboard, AI Frontiera, Vault / Tooling). Creato il file `workspace/journal/open-items.md` e aggiornata la skill per leggerlo all'inizio sessione e aggiornarlo alla chiusura con un diff leggero.

## Deciso

- `open-items.md` è la fonte di verità: la skill non legge più l'ultima sessione ma questo file.
- Alla chiusura sessione la skill mostra un diff compatto (rimuovo / aggiungo) e chiede conferma solo se ci sono modifiche. Se non ci sono cambiamenti, chiude senza chiedere.
- 5 workstream fissi: Stuart, AI / Company Brain, Finance Dashboard, AI Frontiera, Vault / Tooling.
- ops-dashboard e Financial Update automation rientrano in Stuart (non in Company Brain), perché sono strumenti per il lavoro, non per il business personale.

## Aperto

(nessun nuovo step emerso in questa sessione)
