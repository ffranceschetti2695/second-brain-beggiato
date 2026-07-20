---
title: Follow-up mensile next steps MBR
summary: "Procedura ripetibile: chiedere update agli owner dei next steps dell'MBR precedente, prima della prossima MBR"
tags: [docs, mbr, slack, procedura]
status: active
created: 2026-07-08
updated: 2026-07-08
related: ["[[doc-flusso-performance-mensile]]"]
---

# Follow-up mensile next steps MBR

Ogni mese, prima della Monthly Business Review, Francesco chiede agli owner dei next steps dell'MBR precedente un aggiornamento sullo stato. Il processo è automatizzato dalla skill Claude Code `stuart-mbr-next-steps-followup` (`.claude/commands/stuart-mbr-next-steps-followup.md`).

## Come funziona

1. Trova nel canale privato `#monthly_business_review` l'ultimo messaggio di recap "next steps" postato da Francesco (elenco numerato con Sponsor/Owner).
2. Assegna ogni punto al **primo owner elencato** (escluso Francesco). Se Francesco è l'unico owner o lo ha già gestito, il punto viene saltato.
3. Raggruppa i punti per destinatario: Slack permette **una sola bozza per DM**, quindi più next steps per la stessa persona finiscono in un unico messaggio.
4. Ogni messaggio riporta il next step **per intero** (contesto + riga "Next step:"), mai una parafrasi.
5. Crea le bozze su Slack (mai invio diretto) — Francesco le rivede e le manda lui.

## Limiti noti

- Non è possibile allegare uno screenshot o un'immagine a una bozza Slack via tool — solo testo/markdown.
- Non è possibile creare un nuovo gruppo DM via tool: si può scrivere una bozza solo in un gruppo DM già esistente. Se non esiste, va chiesto a Francesco se preferisce messaggi individuali o vuole indicare il gruppo giusto.

## Vedi anche

[[doc-flusso-performance-mensile]] — [[entity-stuart]] — [[self-stuart-achievements]]
