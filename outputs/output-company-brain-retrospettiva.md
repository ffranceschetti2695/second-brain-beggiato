---
title: "Company Brain — retrospettiva e logiche del prodotto"
summary: "Sintesi ragionata di tutto il lavoro fatto sul Company Brain: perché esiste, come è fatto, quali decisioni sono state prese e come si sono evolute nel tempo."
tags: [outputs, ai, company-brain, business]
status: active
created: 2026-07-08
updated: 2026-07-08
related: ["[[progetto-company-brain]]", "[[concetto-company-brain]]", "[[doc-company-brain-ingestion-horizons]]", "[[concetto-rag]]"]
---

# Company Brain — retrospettiva e logiche del prodotto

Questo documento serve a due cose: fissare in un posto solo il ragionamento dietro al prodotto (perché è fatto così e non altrimenti) e fare da base per demo a potenziali clienti. Non ripete l'architettura già descritta in [[progetto-company-brain]] e nel README dell'app — qui ci sono il *perché* delle scelte e la loro evoluzione nel tempo.

## L'idea in una frase

Una Company Brain è una knowledge base aziendale strutturata che sostituisce il lavoro manuale di "spiegare il contesto ad ogni automazione" con una base condivisa unica, leggibile sia da umani sia da AI. Il vault Personal Brain di Francesco è la versione artigianale del prodotto; `company-brain-app` è la sua automazione. Dettagli in [[concetto-company-brain]].

## Perché questo e non un altro prodotto AI

Deciso il 2026-06-18: il RAG (retrieval + vector DB) è commodity, replicabile in un weekend con `pip install chromadb`. Il vantaggio competitivo reale sta in due cose difficili da copiare:

1. **Qualità delle note atomiche** — trasformare dati grezzi (thread Slack da 300 messaggi, PDF Confluence, transcript meeting) in note strutturate, deduplicate, collegate correttamente. Non è un problema di infrastruttura, è prompt engineering + giudizio editoriale.
2. **Workflow di onboarding del cliente** — capire quali fonti contano davvero per un'azienda specifica, che tassonomia dare alle note, quali automazioni costruirci sopra. Qui entra il background FP&A di Francesco: è consulenza, non solo tech, ed è raro trovarla in profili puramente tecnici.

Di conseguenza, il primo passo commerciale resta la vendita/il retainer tradizionale — la Company Brain non sostituisce l'acquisizione cliente, cambia cosa si costruisce *dopo* averlo acquisito.

## Perché Stuart è la palestra e non il prodotto

Decisione fondante del 2026-07-01, mai messa in discussione dopo: si costruisce il brain **su Stuart** (dogfooding reale, dati veri, problemi veri) ma **il prodotto in vendita è l'IP generica** — motore di ingestion, connettori, playbook di onboarding — mai i dati Stuart. Stuart non è nemmeno il primo cliente pilota candidato (troppo grande e complesso per un pilota); il domain knowledge accumulato lì (FP&A, ops last-mile) diventa però un asset riusabile per vendere a player più piccoli e simili nel settore. Profilo del primo cliente pagante ideale: 5-20 persone, stack Notion + Google Drive (API semplici, curva di apprendimento bassa), obiettivo del pilota è imparare il workflow di onboarding, non fare profitto subito.

## Architettura: perché ogni pezzo esiste

La pipeline (`connector → canonizer → vault_writer → vector_store → llms_generator`, orchestrata da `pipeline.py`) non è nata tutta insieme. È cresciuta per problemi reali incontrati durante il dogfooding su Stuart, in questo ordine:

| Componente | Nato quando | Problema che risolve |
|---|---|---|
| `canonizer.py` | 2026-07-01 | Cuore del business: automatizza la trasformazione raw→note che prima si faceva a mano con la skill `/canon`. Due chiamate Claude (estrazione canon → note atomiche con wikilink), fallback JSON/Pydantic se l'SDK non supporta `output_format` nativo. |
| `vault_writer.py` / `vector_store.py` | 2026-07-01 | Scrivere le note nel vault *target* (mai cablato su un brain specifico) e indicizzarle in ChromaDB locale, dentro il vault stesso — così il cervello resta autocontenuto e portabile a un cliente. |
| `workspace_log.py` | 2026-07-01 (stessa ondata) | Senza tracciabilità, un'ingestion automatica in loop notturno diventa un black box. Salva il canon per fonte (`workspace/canon/<slug>.md`, sovrascritto solo se il contenuto cambia) + log append-only in `workspace/journal/ingestion-log.md` — audit trail di cosa è stato ingerito e quando. |
| `quality_gate.py` | Esisteva già manuale dal 2026-06-15, promosso a strumento permanente parametrico il 2026-07-07 | Con centinaia di note da fonti diverse, il grafo di wikilink si degrada silenziosamente (note orfane, link rotti, frontmatter incompleto). Sei regole strutturali + BFS per verificare che il grafo resti connesso e navigabile. |
| `dedupe_check.py` | Dopo `vector_store.py` | Fonti diverse (Slack + Confluence + Gmail) raccontano spesso lo stesso fatto. Usa cosine similarity ≥0.90 sugli embedding per segnalare duplicati concettuali cross-fonte. Non unisce mai da solo — si rifiuta persino di produrre un report se disco e indice ChromaDB sono disallineati, e in quel caso indica `reindex.py` come riparazione. |
| `reindex.py` | Insieme a `dedupe_check.py` | Ricostruisce il vector store da disco senza richiamare l'API né toccare i `.md` — riparazione standard dopo bug, rename di massa o migrazioni. |

Decisioni di design trasversali (dal README, confermate nel tempo):
- **Vault target parametrico** (`--vault`): è ciò che rende l'app vendibile — la punti sul brain del cliente, non è cablata su Stuart.
- **Wikilink sicuri**: il canonizer riceve l'elenco delle note esistenti e può linkare solo quelle (più il batch corrente); il writer filtra comunque i `related` per non creare nodi fantasma.
- **Embedding locale** (`all-MiniLM-L6-v2`): nessuna API esterna per gli embedding, scelto già nel prototipo del 2026-06-18 per evitare dipendenza da chiavi OpenAI.

## L'evoluzione del modello Claude usato

Non è stata una scelta fissa, ha seguito l'esperienza reale:
- **2026-07-01**: si parte con `claude-opus-4-8` con adaptive thinking — la qualità delle note è il differenziatore, non si risparmia sul modello.
- **2026-07-01 (poco dopo, dogfood su Slack)**: si passa a **Sonnet** — Opus si è rivelato troppo costoso su fonti grandi (centinaia di messaggi Slack), e il rapporto qualità/costo di Sonnet è risultato migliore per quel volume.
- **2026-07-06**: per la canonizzazione di Confluence si preferiscono **3 agenti Claude Code eseguiti in sessione** (che consumano i token dell'abbonamento) invece della pipeline via API Anthropic a pagamento — cambio di canale pratico, non di modello, per motivi di costo durante il dogfooding.

Lezione: il modello/canale giusto dipende dal volume e dal contesto della fonte, non è un parametro fissato una volta per tutte nell'architettura.

## Decisioni su cosa ingerire (e cosa no)

Non tutte le fonti sono state trattate allo stesso modo — ogni fonte ha richiesto una decisione esplicita su segnale/rumore:

- **Confluence TOM**: 504 file totali, troppo rumoroso da ingerire integralmente → filtro per recency (90 giorni) + keyword decisionale, sceso a 40 candidate, poi 28 note dopo dedup.
- **Slack canali ad alto volume** (es. `#uk_ops-commercial`): si estrae solo framework/decisione durevole, non lo status quotidiano — un canale può produrre anche una sola nota utile su centinaia di messaggi.
- **Gmail "Notes by Gemini"**: scelta opposta, ingest **senza filtro** su tutto il lookback (365 giorni) — qui la logica è che le note atomiche deduplicano da sole in fase di canonizzazione, e il volume è comunque basso (77 email).
- **xCel Bespoke** (2026-06-26): esclusa esplicitamente dal tracking permanente — usata più come caso negativo per capire cosa *non* va ingerito che come fonte reale.

Principio generale (fissato in [[doc-company-brain-ingestion-horizons]]): il lookback riflette il ciclo di vita del contenuto — strategia/OKR 12-18 mesi, ops attiva 3-6 mesi, dati finanziari 24 mesi, handbook/TOM 90 giorni perché diventa obsoleto senza avvisare.

## Problemi reali e come sono stati risolti

Vale la pena tenerne traccia perché sono il tipo di frizione che si ripresenterà identica con un cliente vero:

- **Query DWH fittizia**: `connectors/dwh.py` interrogava colonne che non esistevano nello schema reale. Riscritta contro `metrics_core.delivery_finance`, validata via Superset MCP e cross-validata contro la baseline FC3. Per lo snapshot si è accettata una semplificazione (RPO/CPO aggregati su `parent_client_name` senza il dedup di `client_forecast_group_adj` usato nel forecast) — accettabile solo perché è uno snapshot descrittivo, non andrebbe bene per un vero forecast.
- **Rename di massa che rompe i wikilink**: un rename di 318 file ha lasciato un suffisso "-md" duplicato più l'estensione `.md` dentro i wikilink — oltre 3.000 riferimenti da correggere. Lezione operativa: dopo un rename di massa, verificare subito i wikilink prima di considerare la migrazione conclusa.
- **Vector store disallineato dopo il rename** (318/466 note indicizzate, ID stale): invece di re-indicizzare subito, si è deciso di rimandare — sotto la soglia delle 500 note (vedi [[concetto-rag]]) `llms.txt` è sufficiente e il vector DB non aggiunge valore proporzionale al costo di manutenzione. `reindex.py` resta pronto per quando servirà davvero un test di scala.
- **Google Meet transcript irraggiungibili**: bloccati lato Google ("ineligible for generative AI contexts") e comunque vivono nel Drive dell'organizzatore del meeting, non in quello di chi lo ha solo partecipato — limite esterno, non risolvibile lato nostro con l'approccio Drive MCP attuale.
- **Gmail MCP di claude.ai non legge le email**: risolto passando a un Gmail MCP locale con OAuth su un progetto GCP personale (Stuart blocca la creazione di progetti GCP standard sull'account aziendale).
- **Incoerenze cross-fonte scoperte dal coherence check** (es. rito "Pre-weekend CPO Governance" dichiarato chiuso ad aprile ma in realtà proseguito a giugno nei DM): quando la fonte non basta a decidere quale versione sia vera, si lascia la discrepanza esplicita nella nota invece di risolverla arbitrariamente. È una scelta editoriale precisa: meglio un'incertezza dichiarata che un falso consenso.

## Stato attuale (dogfood su Stuart, 2026-07-07)

| Fonte | Stato | Note |
|---|---|---|
| Slack (canali + DM + group DM leadership + war room) | Fatto | ~350+ |
| Confluence (STRAT, DATA, GO, PROP, TOM) | Fatto | 63 |
| Google Drive | Fatto (parziale, Meet bloccati) | 13 |
| Gmail Notes by Gemini | Fatto | 44 |
| DWH (Superset MCP) | Fatto | 1 snapshot |

Totale: 461 note atomiche + ChromaDB (non riallineato, in pausa deliberata). Roadmap: fasi 1-3 (personal brain, pipeline, dogfood Stuart) completate; fase 4 (primo cliente pilota) ancora da avviare; fase 5 (scala) futura.

## Cosa resta aperto

- Formalizzare un lookback Slack uniforme per i canali ingeriti nella prima ondata (2026-07-01), oggi senza un orizzonte esplicito.
- Sistematizzare la dedup Gmail (oggi solo log manuale, nessun connector/state file dedicato).
- Valutare credenziali Superset REST per rendere il refresh DWH schedulabile invece che manuale in sessione.
- Alcuni finding minori del coherence check del 2026-07-07 non ancora risolti (refuso data lock FC3, vintage RPO Carrefour FR non esplicito, buco Fnac, quasi-duplicati ramp-down BPO).

## Come usarlo in una demo cliente

Il valore da mostrare non è "abbiamo un chatbot che risponde", è il prima/dopo: centinaia di thread Slack, pagine Confluence ed email sparse diventano un grafo di note atomiche interrogabile e navigabile in minuti, con tracciabilità di ogni fonte e un sistema di qualità (quality gate + dedupe) che tiene il grafo pulito mentre cresce. La storia di Stuart è la controprova pratica: non è un demo giocattolo, è stato fatto su un'azienda operativa vera, con i problemi veri che una vendita reale porterebbe (fonti disomogenee, permessi, dati sporchi, query DWH da correggere sul campo).
