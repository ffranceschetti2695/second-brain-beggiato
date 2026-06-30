# Istruzioni per Claude

Questa è una cartella di vault Obsidian. Quando ricevi una domanda:

1. **Parti sempre dai file markdown presenti in questa cartella** — leggi prima i file rilevanti, poi rispondi.
2. Non cercare informazioni su strumenti esterni (Slack, Confluence, ecc.) a meno che io non lo chieda esplicitamente.
3. Se la risposta è nei file del vault, forniscila direttamente senza chiedere chiarimenti.

## Struttura e navigazione del vault

- **Per orientarti parti da `llms.txt`** (indice derivato: title + summary di ogni nota) e dagli `index-*.md` (uno per cartella). La mappa delle cartelle è in `index-personal-brain.md`.
- Cartelle: `self/` (identità), `areas/` (aree vita/lavoro), `entities/` (persone, aziende, strumenti), `concepts/` (glossario), `projects/` (progetti attivi), `data/` (dati e metriche), `docs/` (procedure e riferimenti), `code/` (snippet), `outputs/` (deliverable), `sources/` (materiale grezzo), `workspace/` (scratch + journal).
- Le note vivono solo nel vault. Il **codice dei progetti software sta fuori** (es. `~/Projects/ops-dashboard`) ed è tracciato da una nota in `projects/`.
- Workflow di ingestione: `sources/` (grezzo) → riconciliazione in `workspace/canon` (skill `canon`) → note atomiche nelle cartelle.

## Regole frontmatter per le note Obsidian

Quando crei note con frontmatter YAML, rispetta sempre queste regole (testate e verificate):

- **`related`**: array YAML inline con ogni wikilink quotato individualmente — `related: ["[[nota-a]]", "[[nota-b]]", "[[nota-c]]"]`
  - ❌ Non usare una stringa quotata unica: `related: "[[a]],[[b]]"` → crea nodi fantasma nel grafo
  - ❌ Non usare plain text senza parentesi: `related: [nota-a, nota-b]` → non navigabile
- **`summary`**: tra virgolette doppie se il testo contiene `:` — `summary: "Testo: con due punti"`
- **`tags`**: il primo tag è sempre il nome della cartella in cui si trova la nota
- **Campi standard** di ogni nota: `title`, `summary`, `tags`, `status`, `created`, `updated`, `related`.

## Quando crei, modifichi o elimini una nota

1. Una nota = **un concetto** (atomica). Collega ad altre note con `[[wikilink]]` liberamente, usando solo nomi di note che esistono (verifica in `llms.txt`).
2. **Aggiorna l'`index-*.md` della cartella** (una riga: `[[nome-nota]] — gancio`).
3. **Rigenera l'indice AI**: `python3 generate_llms.py`. **Non editare `llms.txt` a mano** (è derivato dai frontmatter).

## Sessioni

A inizio sessione ("inizia sessione" / "buongiorno") e a fine ("chiudi sessione" / "fine giornata") usa la skill `journal`.

## Stile

Italiano naturale, niente m-dash, date sempre assolute in formato `YYYY-MM-DD` (mai relative).
