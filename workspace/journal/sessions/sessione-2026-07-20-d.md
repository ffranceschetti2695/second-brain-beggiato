---
title: "Sessione 2026-07-20-d"
summary: "Risposte alle domande trimestrali di Accuracy su Tesco/report/pipeline, e creazione della skill /stuart-lookup"
tags: [workspace, type/session]
status: done
created: 2026-07-20
updated: 2026-07-20
related: ["[[entity-stuart]]", "[[persona-mark-jones]]", "[[progetto-company-brain]]"]
---

## Fatto

Risposte alle tre domande della richiesta trimestrale di Accuracy (monitoraggio del rapporto Stuart-Mutares) di competenza di Francesco: scaricati da Drive i report mensili Mutares di aprile/maggio/giugno 2026, ricostruito lo stato della negoziazione Tesco (RFP concluso, nuovi tier RPO) da Stuart Brain vault + Slack, ed estratta la slide di stato pipeline in PDF. Tutto salvato in `~/Desktop/Accuracy/` (fuori dal vault). Il documento Word su Tesco è stato accorciato su richiesta per essere più diretto.

Creata la skill `/stuart-lookup` (`.claude/commands/stuart-lookup.md`): ricerca cross-fonte su qualsiasi argomento Stuart, in ordine Stuart Brain vault → Slack → Google Drive.

## Deciso

- `/stuart-lookup` non va mai auto-invocata: va sempre offerta prima ("vuoi che lanci la skill di lookup?") e lanciata solo dopo conferma; una chiamata esplicita `/stuart-lookup` vale già come conferma.
- I deliverable per Accuracy vivono in `~/Desktop/Accuracy/` sul Mac, non nel vault Obsidian: sono output per una parte esterna, non conoscenza statica del vault.
- Il pattern delle domande trimestrali di Accuracy (naming convention Drive per i report mensili, Tesco via lookup, pipeline via slide del deck) è stato documentato come riutilizzabile per il prossimo giro.

## Aperto

Nessun nuovo step aperto.
