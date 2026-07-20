# Istruzioni per Claude

## ⚠️ HARD CONSTRAINT — LINGUA DI RISPOSTA (leggi per prima cosa, sempre)

**Rispondi SEMPRE nella stessa lingua dell'ULTIMO messaggio di Francesco.** Nessuna eccezione, nessun default all'italiano.

- Questo vale **anche e soprattutto subito dopo aver invocato una skill o un tool** (es. `journal`, `daily-recap`, qualsiasi skill), il cui contenuto/output interno può essere in italiano indipendentemente dalla lingua della conversazione.
- Prima di scrivere la PRIMA parola della tua risposta finale, controlla: "in che lingua è scritto l'ultimo messaggio di Francesco?" e rispondi in quella lingua, punto. Ignora la lingua delle note del vault, degli skill file, dei log, o dei tuoi messaggi precedenti.
- Se l'ultimo messaggio è in inglese → rispondi in inglese. Se è in italiano → rispondi in italiano. Nessun'altra euristica prevale su questa.

Questa regola è già stata patchata una volta (2026-07-13) e continua a essere violata dopo l'uso di skill: trattala come la massima priorità di stile, non come una nota tra le altre.

---

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

**Soglia per creare una nota**: solo se aggiunge conoscenza statica genuina — un concetto, una regola, una struttura, un meccanismo. Non creare note per tabelle di dati numerici riestraibili dal DWH o da un file Excel (es. ratei mensili, split percentuali, serie storiche): quelli non aggiungono knowledge e si riderivano dalla fonte. Il test: "Se non avessi questa nota, perderei una comprensione che non posso recuperare altrove?" Se no, non crearla.

**Eccezione**: quando Francesco chiede esplicitamente di ricordare i piani di forecast/budget (BP, FC3, FC6, ecc.), crea la nota con i dati numerici anche se sono tabelle — quei piani sono snapshot temporali che non si riderivano facilmente.

1. Una nota = **un concetto** (atomica). Collega ad altre note con `[[wikilink]]` liberamente, usando solo nomi di note che esistono (verifica in `llms.txt`).
2. **Aggiorna l'`index-*.md` della cartella** (una riga: `[[nome-nota]] — gancio`).
3. **Rigenera l'indice AI**: `python3 generate_llms.py`. **Non editare `llms.txt` a mano** (è derivato dai frontmatter).

## Sessioni

A inizio sessione ("inizia sessione" / "buongiorno") e a fine ("chiudi sessione" / "fine giornata") usa la skill `journal`.

## Stile

- **Lingua: rispondi sempre nella lingua in cui Francesco ha scritto il messaggio corrente**, indipendentemente dalla lingua delle note del vault, di skill/tool intermedi, o dei messaggi precedenti nella stessa sessione. Se scrive in inglese, rispondi in inglese; se in italiano, rispondi in italiano. Questa regola vale anche subito dopo l'esecuzione di una skill (es. `journal`) che internamente produce output o log in italiano: la risposta finale all'utente deve comunque essere nella lingua del suo ultimo messaggio.
- Quando scrivi in italiano: niente m-dash, date sempre assolute in formato `YYYY-MM-DD` (mai relative).
- Quando scrivi in inglese: usa le convenzioni naturali inglesi (comunque niente m-dash, date assolute).
