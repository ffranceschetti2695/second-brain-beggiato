---
title: "Company Brain — manuale tecnico dell'app di ingestion"
summary: "Riferimento tecnico completo di company-brain-app: stack, pipeline, connettori, strumenti di manutenzione, dedotto dal codice sorgente."
tags: [outputs, ai, company-brain, tech-stack]
status: active
created: 2026-07-08
updated: 2026-07-08
related: ["[[output-company-brain-retrospettiva]]", "[[progetto-company-brain]]", "[[concetto-company-brain]]", "[[doc-company-brain-ingestion-horizons]]"]
---

# Company Brain — manuale tecnico

Manuale di riferimento dell'app `company-brain-app` (in `~/Desktop/company-brain-app/`, fuori dal vault). Dove [[output-company-brain-retrospettiva]] spiega il *perché* delle decisioni, questo documento spiega il *come funziona oggi*, dedotto leggendo il codice. Usalo per ricordare velocemente lo stack e la logica di ingestion, o come base tecnica per una demo.

## Tech stack

| Livello | Scelta | Perché (dedotto dal codice) |
|---|---|---|
| Linguaggio | Python 3, nessun framework web | Script CLI orchestrati da `pipeline.py`, nessuna dipendenza da server |
| LLM canonizzazione | Anthropic API, modello `claude-sonnet-4-6` (`config.py`) | Rapporto qualità/costo migliore di Opus per canonizzare testo strutturato (Slack, Confluence) su volumi alti |
| Vector DB | ChromaDB (`chromadb`), `PersistentClient` per-vault in `<vault>/.chroma` | Locale, zero infrastruttura da gestire, si porta dietro col vault |
| Embedding | Default ChromaDB `all-MiniLM-L6-v2`, locale e offline dopo il primo download | Nessuna API esterna a pagamento per gli embedding |
| Validazione dati | Pydantic (`BaseModel`) per lo schema delle note atomiche | Garantisce che l'output del LLM rispetti sempre la stessa forma prima di toccare il filesystem |
| Config/secrets | `python-dotenv`, `.env` nella cartella dell'app | `ANTHROPIC_API_KEY` e credenziali dei connettori lette da ambiente o `.env` |
| Storage delle note | File `.md` con frontmatter YAML, stesso schema del Personal Brain | Il vault resta leggibile da umani anche senza l'app |

Dipendenze minime sempre installate: `anthropic`, `chromadb`, `python-dotenv`. Le dipendenze dei singoli connettori (`slack-sdk`, `atlassian-python-api`, `notion-client`, `google-api-python-client`, `pypdf`, `python-docx`) sono commentate in `requirements.txt` e vanno installate solo quando serve quella fonte — tenere la pipeline "leggera" di default.

## Architettura della pipeline

```
connector.fetch()                    →  RawDocument (source_id, title, content, origin, url, metadata)
        ↓
state.is_unchanged()  →  se invariato (hash content), skip
        ↓
Canonizer.canonize()
   fase 1: phase1_canon()             →  canon: fatti grezzi in markdown piatto
   fase 2: phase2_notes()             →  CanonResult: lista di AtomicNote validate (Pydantic)
        ↓
workspace_log.save_canon()           →  salva il canon come traccia di audit
        ↓
vault_writer.write_notes()           →  scrive i .md nel vault target, con frontmatter e wikilink filtrati
        ↓
vector_store.upsert_notes()          →  embedding + indicizzazione in ChromaDB
        ↓
state.mark_processed()               →  aggiorna lo stato incrementale
        ↓
llms_generator.generate()            →  rigenera llms.txt da zero (solo a fine run, se ci sono note nuove)
```

Tutto orchestrato da `pipeline.py`, unico entry point CLI. Non esistono altri modi per far girare l'ingestion end-to-end.

### RawDocument: il contratto tra fonte e pipeline

Ogni connettore, qualunque sia la fonte, restituisce una lista di `RawDocument` (`connectors/base.py`):

```
source_id   identificatore stabile nella fonte (es. "slack:C0B123", "confluence:98765")
title       titolo leggibile
content     testo grezzo completo
origin      da dove arriva ("slack", "confluence", "drive", "dwh", "notion", "local:...")
url         URL canonico, se esiste
metadata    dict libero (channel_id, space_key, mime_type, ecc.)
content_hash  sha256 del content, troncato a 16 char — usato per l'ingestion incrementale
```

Questo disaccoppiamento è il punto di estensione del prodotto: aggiungere una fonte nuova = scrivere una sottoclasse di `Connector` con un metodo `fetch()`, registrarla in `connectors/__init__.py`. Nient'altro nella pipeline cambia.

### Canonizer: le due fasi (il cuore del business)

`canonizer.py` automatizza a due chiamate LLM il flusso manuale della skill `/canon`:

1. **Fase 1 — canon** (`phase1_canon`): un prompt di sistema (`CANON_SYSTEM`) chiede di estrarre *tutti* i fatti duri dalla fonte in un documento piatto, senza filtrare, senza inventare nulla, numeri coerenti tra loro, date sempre `YYYY-MM-DD`, niente em-dash. Output: testo markdown, nessun frontmatter.
2. **Fase 2 — note atomiche** (`phase2_notes`): dato il canon più l'elenco delle note già esistenti nel vault (`existing_keys`), un secondo prompt (`NOTES_SYSTEM`) costruisce una lista di `AtomicNote` con vincoli hard:
   - una sola idea per nota, massimo ~300 righe
   - nome file col prefisso di dominio corretto per la cartella
   - almeno 3 collegamenti in stile wikilink (doppie parentesi quadre) distinti **nel corpo** (non nel frontmatter), verso note esistenti o create nello stesso batch — mai verso note inventate
   - ordine concettuale: prima le note-hub, poi il dettaglio

L'output è validato con **structured output nativo** (`client.messages.parse` + `output_format=CanonResult`) se l'SDK lo supporta; altrimenti fallback a JSON nel testo, estratto con `_extract_json` e validato via `CanonResult.model_validate_json`. In entrambi i casi il risultato è sempre un oggetto Pydantic tipizzato prima di toccare il filesystem — la pipeline non scrive mai testo LLM non validato.

Le chiamate usano `messages.stream` con `thinking={"type": "adaptive"}`; se l'SDK è troppo vecchio per il parametro (`TypeError`), ripiega senza adaptive thinking.

### Vault writer: dove le regole del frontmatter diventano codice

`vault_writer.py` applica meccanicamente le regole frontmatter del vault (le stesse descritte in `CLAUDE.md` del Personal Brain):
- `related`: array YAML inline, ogni wikilink quotato singolarmente (`_build_frontmatter`)
- `summary`: sempre tra virgolette doppie, con escape (`_yaml_quote`)
- `tags`: il primo tag è sempre il nome della cartella
- filename: normalizzato col prefisso corretto se il LLM non l'ha già messo (`_normalize_filename`)

Punto di sicurezza importante: **i wikilink validi** per una nota sono solo `existing_keys` (note già nel vault) più le chiavi dello stesso batch di scrittura. Qualsiasi `related` che punti fuori da questo insieme viene scartato silenziosamente in fase di scrittura frontmatter (niente nodi fantasma nel grafo), e i wikilink nel corpo che non risolvono vengono segnalati come `dangling` nel log di run (ma non bloccano la scrittura).

### Vector store e stato incrementale

- `vector_store.py`: un `PersistentClient` ChromaDB per vault, collection unica `vault_notes`, spazio cosine. L'`id` di ogni entry è il `filename` della nota — un `upsert` su una nota rinominata o riscritta sovrascrive l'entry invece di duplicarla.
- `state.py`: `<vault>/.ingestion_state.json`, mappa `source_id → {hash, notes}`. `is_unchanged()` confronta l'hash prima di rilanciare il canonizer — è quello che rende sicuro far girare la pipeline in loop (es. ogni notte) senza ri-processare tutto ogni volta.

## Schema del vault (comune a qualsiasi brain target)

Definito in `config.py`, condiviso da app e Personal Brain:

| Cartella | Prefisso filename |
|---|---|
| `self` | `self-` |
| `areas` | `area-` |
| `projects` | `progetto-` |
| `concepts` | `concetto-` |
| `docs` | `doc-` |
| `entities` | `entity-` oppure `persona-` |
| `data` | `data-` |
| `code` | `code-` |
| `outputs` | `output-` |

Ogni vault target ha, dentro di sé: `.chroma/` (vector store), `.ingestion_state.json` (stato incrementale), `llms.txt` (indice-porta). Questo rende il brain autocontenuto: spostando la cartella del vault ci si porta dietro l'intero cervello, app esclusa.

## I connettori: uno per fonte, tutti con la stessa interfaccia

| Connettore | Credenziali | Cosa filtra | Lookback default |
|---|---|---|---|
| `local` | nessuna | estensioni `.md/.txt/.markdown`, esclude file `index-*` | tutto ciò che c'è nella cartella |
| `notion` | `NOTION_TOKEN` (+ opz. `NOTION_DATABASE_ID`) | nessuno, salvo integrazione condivisa solo su pagine/DB scelti | tutto l'accessibile |
| `slack` | `SLACK_BOT_TOKEN` (bot OAuth) | esclude canali per keyword (`random`, `hiring`, `engineering`, `dev-`, `it-`, `infra`, ecc.) e canali con meno di `min_messages` (default 5) messaggi nel periodo | 180 giorni |
| `confluence` | `CONFLUENCE_URL/EMAIL/TOKEN` (token API personale, non admin) | esclude spazi per keyword (`engineering`, `hr`, `legal`, `devops`, ecc.) a meno che non si passi `space_keys` esplicito; scarta pagine con meno di 100 caratteri | 365 giorni |
| `drive` | `GOOGLE_SERVICE_ACCOUNT_JSON` (o MCP Drive in sessione) | include solo file il cui nome contiene keyword finanziarie/strategiche (`FC`, `MBR`, `budget`, `transcript`, `board`, `war room`, ecc.); supporta Google Doc, Sheet, PDF, DOCX | 365 giorni |
| `dwh` | `SUPERSET_URL/USER/PASS` | nessun filtro contenuto: query SQL fissa su `metrics_core.delivery_finance` | ultimi 6 mesi (query fissa in `DATASETS[0]["sql"]`) |
| `dwh-mcp` | nessuna (legge un JSON già estratto via MCP Superset in sessione) | — | dipende dal JSON fornito |

Dettagli operativi degni di nota:

- **Slack**: pagina tutti i canali pubblici/privati/mpim accessibili al bot, mappa gli utenti (`_get_user_map`) per rendere leggibili i messaggi, espande solo i thread con più di 3 reply (non tutti, per contenere il volume), rispetta il rate limit Tier 3 di Slack con `time.sleep(0.5)` tra le chiamate paginate.
- **Confluence**: conversione HTML→testo fatta a mano con regex (`_html_to_text`), zero dipendenze esterne per il parsing; il filtro temporale usa `version.when` della pagina, non la data di creazione.
- **Drive**: l'estrazione testo dipende dal mime type (`SUPPORTED_MIME_TYPES`) — Google Doc esportato come testo semplice, Sheet come CSV, PDF via `pypdf`, DOCX via `python-docx` (entrambe opzionali, con messaggio di errore esplicito se mancanti).
- **DWH**: il connettore "vero" (`DWHConnector`) fa login diretto su Superset via REST e produce **un solo** `RawDocument` a run, con tutte le sezioni/dataset concatenate in un unico markdown con tabelle. Nella pratica finora si è usato `DWHMcpConnector`, che salta l'autenticazione REST e legge un JSON già estratto manualmente via MCP Superset in sessione — nessuna credenziale Superset è mai stata messa in `.env`.
- **Notion**: unico connettore pensato esplicitamente per il primo cliente pilota (profilo fondatore/COO che usa Notion), copre i tipi di blocco più comuni (heading, liste, quote, code) in `_block_to_text`, estendibile per callout/toggle/tabelle quando servirà.
- **`fetch_confluence.py`**: script satellite separato dal connettore standard — scarica le pagine Confluence come file `.md` grezzi dentro `stuart-vault/sources/confluence/<SPAZIO>/`, con lookback specifico per spazio hardcoded (`STRAT` 540gg, `GO`/`TOM` 365gg, `PROP`/`DATA` 180gg). È il percorso realmente usato per Stuart: prima scarico su disco con questo script, poi canonizzazione tramite agenti Claude Code in sessione (non tramite `canonizer.py` via API), per usare i token dell'abbonamento invece dell'API a consumo.

## Strumenti di manutenzione del vault

Non fanno parte del flusso di ingestion in sé, ma tengono il "cervello" in salute mentre cresce:

- **`quality_gate.py`** — 6 regole strutturali su tutte le note (esclude `sources/`, `workspace/`, `_showcase/`): frontmatter completo (R1), corpo ≤300 righe (R2), almeno 3 wikilink in uscita validi (R3), zero link rotti (R4), zero note orfane senza link in entrata (R5), grafo connesso in un'unica componente via BFS (R6). Parametrico su `--vault`, promosso da strumento manuale a permanente.
- **`dedupe_check.py`** — trova coppie di note semanticamente troppo simili (cosine similarity ≥0.90 di default) usando gli embedding già in ChromaDB. Prima di confrontare, verifica che gli ID su disco coincidano esattamente con quelli nel vector store: se c'è disallineamento **si rifiuta di produrre un report parziale** e indica di rilanciare `reindex.py`. Solo lettura: non unisce né cancella nulla, produce un elenco di candidati da rivedere a mano.
- **`reindex.py`** — ricostruisce il vector store da zero leggendo le note su disco (frontmatter + corpo), senza chiamare l'API Claude né toccare i `.md`. È la riparazione standard dopo un rename di massa, un bug di una versione precedente della pipeline, o una migrazione di vault.
- **`workspace_log.py`** — l'equivalente automatico della skill `/canon` manuale: salva il canon di ogni fonte in `workspace/canon/canon_<slug>.md` (sovrascritto solo se il content_hash cambia) e appende ogni run in un log leggibile `workspace/journal/ingestion-log.md`, con note scritte, warning e fatti non mappati.
- **`llms_generator.py`** — rigenera `<vault>/llms.txt` da zero leggendo solo `title` e `summary` dal frontmatter di ogni nota, raggruppate per cartella. Gira automaticamente a fine pipeline se sono state scritte note nuove.

## Cheat sheet comandi

```bash
# Anteprima: canonizza ma non scrive nulla nel vault
python3 pipeline.py --dry-run

# Ingestion reale nel vault-demo di default
python3 pipeline.py

# Ingestion su un vault cliente, da una cartella locale di export
python3 pipeline.py --vault /percorso/brain-cliente --source /export/fonti-cliente

# Da Notion
python3 pipeline.py --vault /percorso/brain-cliente --connector notion --source <DATABASE_ID>

# Da Confluence, solo alcuni spazi
python3 pipeline.py --vault stuart-vault --connector confluence --spaces STRAT,DATA

# Ricerca semantica nel vector store (non fa ingestion)
python3 pipeline.py --vault stuart-vault --query "modelli di monetizzazione AI"

# Riprocessa anche documenti invariati (forza)
python3 pipeline.py --vault stuart-vault --force

# Manutenzione
python3 quality_gate.py --vault stuart-vault
python3 dedupe_check.py --vault stuart-vault --threshold 0.90
python3 reindex.py --vault stuart-vault
```

## Cosa NON fa (limiti attuali, dedotti dal codice)

- Nessuno scheduler incluso: il "loop ogni notte" descritto nell'architettura concettuale è un cron/GitHub Action da montare fuori dall'app, la pipeline stessa è stateless tra un'esecuzione e l'altra (solo `state.py` persiste).
- `DWHConnector` (via REST Superset) non è mai stato usato in produzione: il percorso reale è `DWHMcpConnector` con JSON estratto a mano via MCP in sessione — non c'è ancora un refresh automatico del DWH.
- Nessun merge automatico dei duplicati trovati da `dedupe_check.py`: la decisione resta sempre umana, per design.
- Nessuna gestione multi-tenant nell'app stessa: isolamento tra clienti è delegato interamente al parametro `--vault` (vault diversi = cartelle diverse), non c'è un livello di autenticazione o permessi nell'app.

## Vedi anche

[[progetto-company-brain]] — [[concetto-company-brain]] — [[doc-company-brain-ingestion-horizons]]
