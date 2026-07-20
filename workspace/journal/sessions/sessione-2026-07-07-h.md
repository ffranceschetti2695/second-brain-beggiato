---
title: "Sessione 2026-07-07-h"
summary: "Costruiti i meccanismi di governance mancanti nello stuart-vault (CLAUDE.md, workspace, index) e due script di manutenzione (dedupe_check.py, reindex.py); risolto un bug di disallineamento vector store e ripulite 12 delle 13 note quasi-duplicate rilevate."
tags: [workspace, type/session]
status: done
created: 2026-07-07
updated: 2026-07-07
related: ["[[progetto-company-brain]]", "[[doc-company-brain-ingestion-horizons]]"]
---

## Fatto

Costruiti nello stuart-vault i meccanismi di governance che mancavano rispetto al Personal Brain: `.claude/CLAUDE.md` vault-specifico, `workspace/canon/` + `workspace/journal/ingestion-log.md` (con `workspace_log.py` agganciato a `pipeline.py` per non scartare più il canon), e `index-stuart-vault.md` come mappa cartelle. Aggiunti a `company-brain-app` due script nuovi: `dedupe_check.py` (candidati duplicati semantici via embedding ChromaDB, sola lettura, con gate di sicurezza che rifiuta di girare se disco e vector store non coincidono) e `reindex.py` (ricostruzione vector store dal disco, nessuna chiamata API).

Il gate di sicurezza di `dedupe_check.py` ha subito trovato un bug reale: 318 embedding su 466 avevano un ID con suffisso `-md` residuo di una versione precedente della pipeline, quindi il vector store era silenziosamente disallineato dal disco. Risolto con `reindex.py`.

Fixati 4 wikilink rotti nello stuart-vault (2 per il bug `-md`, 1 riferimento cross-vault convertito in testo semplice, 1 risolto creando le due note entità mancanti `entity-amrest-poland` ed `entity-just-eat-poland`). Quality gate portato a 0 errori.

Eseguita la pulizia duplicati: 16 coppie candidate raggruppate in 13 cluster indipendenti, processati in parallelo da sub-agent con giudizio caso per caso (non solo similarità embedding). Risultato: 12 cluster uniti (445→443 note), 1 correttamente lasciato separato (due canali Slack Accounting×FPA distinti per periodo). Due cluster sono stati bloccati inizialmente dal classificatore di permessi del harness (cancellazione file non esplicitamente autorizzata su file specifici) e completati solo dopo che l'utente li ha nominati esplicitamente.

## Deciso

- Dedupe detection tenuta come script separato e di sola lettura, non come regola nel quality gate: giudizio semantico e gate strutturale hanno logiche e costi diversi.
- Prima di fidarsi di qualunque similarità, verificare sempre che il vector store combaci esattamente con le note su disco (stessi ID) — altrimenti il risultato è silenziosamente incompleto.
- Le fusioni di note richiedono lettura completa e giudizio "duplicato vs complementare" (hub-vs-spoke, periodi diversi), non solo soglia di similarità: due dei 13 cluster analizzati sono stati scartati o gestiti diversamente proprio per questo controllo.
- Cancellazioni di note pre-esistenti restano un'azione che il harness blocca se non esplicitamente autorizzata sui file nominati: rispettato il blocco senza cercare vie traverse, chiesta conferma esplicita all'utente sui 2 cluster bloccati.

## Aperto

- Dedupe stuart-vault: valutare `concetto-zapp-test-performance-premium.md` e `concetto-bpo-automazione-contatti-corrieri-2026.md` in un prossimo giro di `dedupe_check.py` (segnalati come probabili duplicati ma lasciati fuori scope in questa sessione).
