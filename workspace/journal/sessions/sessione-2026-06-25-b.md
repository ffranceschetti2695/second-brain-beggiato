---
title: "Sessione 2026-06-25-b"
summary: "Validato il flusso actuals dal DWH e costruita la skill performance per i bridge Actual vs FC3, collaudata su maggio."
tags: [workspace, type/session]
status: done
created: 2026-06-25
updated: 2026-06-25
related: ["[[data-fc3-baseline-2026]]", "[[code-query-actuals-dwh]]", "[[doc-flusso-performance-mensile]]", "[[doc-dwh-finance-schema]]", "[[data-stuart-segmentazione-clienti]]", "[[concetto-bridge-waterfall]]", "[[concetto-additional-rpo]]", "[[entity-stuart]]"]
---

## Fatto

Chiuso il cerchio sul flusso actuals e trasformato in skill riutilizzabile. Collegato l'MCP "agent gateway prod", eseguita la query actuals sul DWH (`metrics_core.delivery_finance` + `mart_finance.inputs_client_grouping`) e **validata contro la dashboard**: Volume (696.055) e Tesco (437.532) tornano all'unita', e tutti i 16 gruppi del bridge Volume combaciano. Isolato lo scarto GR/GM di ~€4.944: e' tutto e solo sui clienti PL (AmRest/JET) = additional RPO, atteso e variabile, quindi si usano sempre i valori DWH.

Arricchito il vault con 6 note atomiche: Tier 2 di contesto ([[concetto-bridge-waterfall]], [[concetto-additional-rpo]], [[data-stuart-segmentazione-clienti]]) e Tier 1 di riferimento ([[code-query-actuals-dwh]], [[doc-dwh-finance-schema]], [[doc-flusso-performance-mensile]]). Aggiornati gli index di concepts/data/code/docs e rigenerato `llms.txt` (49 note, 9 cartelle). Aggiornata anche la nota [[data-fc3-baseline-2026]] per marcare il DWH come fonte canonica e ricalcolare i bridge di maggio con gli actuals DWH.

Creata la skill `performance` (`.claude/commands/performance.md`), in stile `journal`, che orchestra il flusso end-to-end. **Collaudata su maggio 2026**: i 3 bridge (Volume, GR, GM) quadrano tutti (check = 0) e combaciano col waterfall ufficiale, con la sola barra PL Top che assorbe l'additional RPO dov'e' atteso.

## Deciso

- **Fonte actuals = DWH, sempre** (non piu' la sheet dashboard). Lo scarto su PL e' fisiologico e variabile, non si hardcoda.
- Struttura della conoscenza a due livelli: note di contesto (concetti) + materiali di riferimento (codice, schema, procedura), cosi' la skill ci si appoggia invece di contenere tutto.
- La skill `performance` e' un **mattone**, non il fine: il goal ultimo del progetto e' la **presentazione automatizzata**, che annidera' performance con altre skill (YTD, rendering, orchestratrice).
- Il collaudo su un mese gia' validato (maggio) e' il criterio di affidabilita': se i bridge quadrano e combaciano, la skill e' solida.

## Aperto

- **Slide YTD**: servono gli actuals dei mesi Jan-Apr (stessa query su range) per le viste cumulate.
- **Skill di rendering**: trasformare i bridge in HTML/deck.
- **Skill orchestratrice**: chiamare le skill in sequenza e assemblare la presentazione end-to-end.
- Output di maggio lasciato solo come collaudo, non salvato in `outputs/` per scelta.
