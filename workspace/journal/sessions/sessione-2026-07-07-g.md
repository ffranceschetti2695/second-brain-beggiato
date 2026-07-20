---
title: "Sessione 2026-07-07-g"
summary: "Quality gate e coherence check completi sullo stuart-brain: bug fix strutturale, collegamento di tutte le note sotto-soglia, remediation dei finding critici e demo Obsidian/ChromaDB"
tags: [workspace, type/session]
status: done
created: 2026-07-07
updated: 2026-07-07
related: ["[[progetto-company-brain]]"]
---

## Fatto

Eseguito un quality gate strutturale sullo stuart-vault (466 note): trovato e corretto un bug sistemico di filename (suffisso "-md" duplicato, 318 file rinominati) e di wikilink (estensione ".md" scritta dentro le parentesi), con oltre 3.000 riferimenti incrociati aggiornati di conseguenza. Eseguito un coherence check mirato su 6 temi cross-fonte (OKR 2026, FC6, DWH vs baseline FC3, clienti chiave, governance/cadenze, BPO ramp-down): trovati 4 finding ad alta severità (OKR2 declassato ma non aggiornato nel framework, headcount CNX India in contraddizione diretta Confluence/Slack, hub Weekly Operations non allineato alla correzione già fatta su Pre-weekend, stato Waitrose ambiguo tra "Closed Won" e trial aperto), tutti verificati con le fonti primarie e risolti nelle note. Un secondo giro dedicato al pattern "hub dichiara chiuso qualcosa proseguito altrove" non ha trovato altre istanze oltre alle due già note.

Collegate tutte le 79 note sotto-soglia (R3, meno di 3 wikilink in uscita) e le 29 note orfane (R5, zero link in entrata) tramite 4 batch di lavoro paralleli per cluster tematico (BPO/automazioni, clienti Francia, UK ops/Tesco, OKR/DWH/finance-FP&A). Il quality gate finale è sceso da 163 a 9 problemi residui, tutti eccezioni attese (index senza frontmatter completo, 4 link a note mai create).

Fatta una demo: ripulito il grafo Obsidian dello stuart-vault (rimossa una cartella-scarto di un vault Obsidian creato per errore, filtrato `sources/` dal grafo per escludere i 777 file grezzi pre-canonizzazione, aggiunti color group per cartella). Testata la query semantica ChromaDB (`pipeline.py --query`): funzionante ma il vector store è disallineato (318/466 note, ID stale dopo il rename). Discusso e deciso di non re-indicizzare ora: sotto la soglia delle 500 note (vedi [[concetto-rag]]) l'indice `llms.txt` è sufficiente, la re-indicizzazione va fatta solo quando serve un vero test di scala.

Reso `quality_gate.py` uno strumento permanente di `company-brain-app` (prima era solo una copia adattata al volo), con supporto `--vault` per riusarlo su qualunque vault gestito dall'app.

## Deciso

- Priorità di lavoro: prima consolidare la qualità strutturale sullo stuart-brain esistente (fatto in questa sessione), poi valutare la scalata a un vero DB vettoriale solo quando il prodotto sarà pronto per un test di scala reale.
- `.chroma` nello stuart-vault resta così com'è (disallineato, inutilizzato) finché non si decide di re-indicizzare: nessun danno a lasciarlo, non vale la pena mantenerlo sincronizzato sotto la soglia delle 500 note.
- `quality_gate.py` diventa parte permanente della toolchain di `company-brain-app`, da rilanciare dopo ogni batch di ingestion.
- Le correzioni ai 4 finding critici del coherence check sono state applicate direttamente (non solo segnalate): dove la fonte non bastava a decidere con certezza (es. discrepanza baseline 15 vs 14 agenti CNX India, percentuale di copertura Waitrose), la discrepanza è stata lasciata esplicita nella nota invece di essere risolta arbitrariamente.

## Aperto

- Vector DB (ChromaDB) stuart-vault: disallineato, re-indicizzazione rimandata a un test di scala futuro
- Coherence check: risolvere i finding media/bassa severità rimasti — refuso anno FC3 lock date, vintage RPO Carrefour FR (FC3 vs FC6) non esplicito, buco operativo su Fnac (zero traccia Slack), 4 note quasi-duplicate ramp-down BPO organico
