# Skill: canon

Trasforma le fonti grezze in `sources/` in note atomiche nel vault.
Due fasi obbligatorie: **canon** (estrazione fatti) → **note atomiche** (costruzione grafo).

Invocala ogni volta che viene aggiunto nuovo materiale in `sources/`.

---

## Regole generali (applica sempre)

- **Nessun fatto inventato**: se non e' nella fonte, non esiste nel vault.
- **I numeri devono quadrare** tra loro: coerenza interna obbligatoria.
- **Wikilink solo a note esistenti**: verifica sempre in `llms.txt` prima di scrivere un link.
- Date in formato `YYYY-MM-DD`, mai relative.
- Italiano naturale, nessun m-dash.
- Il frontmatter `related` e' sempre un array inline con ogni wikilink quotato:
  `related: ["[[nota-a]]", "[[nota-b]]"]`
- Il campo `summary` va tra virgolette doppie se contiene `:`.
- Il primo tag e' sempre il nome della cartella in cui si trova la nota.

---

## Fase 1 — Costruzione del canon

**Scopo:** estrarre tutti i fatti duri dalla fonte e scriverli in un unico file di lavoro strutturato.

**Passi:**

1. Leggi tutti i file presenti in `sources/` non ancora processati.
2. Leggi `llms.txt` per conoscere le note gia' esistenti nel vault.
3. **Prima di scrivere**, presenta un piano in 5 righe:
   - Cosa hai trovato nella fonte.
   - Quali sezioni coprirai nel canon (es. identita', esperienze, competenze, ecc.).
   - Quante note atomiche stimi di creare e in quali cartelle.
   **Aspetta l'ok dell'utente prima di procedere.**
4. Dopo l'ok, scrivi il file canon:
   - **Percorso:** `workspace/canon_<nome-fonte>.md`
     dove `<nome-fonte>` e' il nome del file sorgente senza estensione (es. `canon_cv-franceschetti.md`).
   - Il canon e' un file di lavoro piatto, non una nota Obsidian: niente frontmatter YAML.
   - Struttura il contenuto in sezioni tematiche con tabelle dove utile.
   - Includi **tutti** i fatti rilevanti: non filtrare in questa fase.
5. Dopo aver scritto il canon, mostralo in sintesi (massimo 10 righe) e chiedi conferma prima di passare alla Fase 2.

---

## Fase 2 — Costruzione delle note atomiche

**Scopo:** trasformare il canon in note atomiche nelle cartelle del vault.

### Regole per ogni nota

- **Una sola idea per nota**, massimo 300 righe.
- **Frontmatter obbligatorio:**
  ```yaml
  ---
  title: "<Titolo leggibile>"
  summary: "<Una frase che descrive la nota>"
  tags: [<cartella>, <tag-secondario>]
  status: active
  created: <YYYY-MM-DD>
  updated: <YYYY-MM-DD>
  related: ["[[nota-a]]", "[[nota-b]]", "[[nota-c]]"]
  ---
  ```
- **Minimo 3 wikilink uscenti nel corpo** verso note non-index che esistono gia' (conta target unici, non ripetizioni).
  - ⚠️ I link nel frontmatter `related` **non contano**: devono essere nel testo del corpo.
  - Se la nota e' breve e i link non emergono naturalmente, aggiungi una sezione `## Vedi anche` alla fine con i link pertinenti.
  - Esempio: `[[self-franceschetti]] — [[area-fp-and-a]] — [[data-carriera-timeline]]`
- **Nome file con prefisso di dominio** coerente con la cartella:
  - `self/` → `self-<slug>`
  - `areas/` → `area-<slug>`
  - `entities/` → `entity-<slug>` (aziende, strumenti) | `persona-<slug>` (persone)
  - `concepts/` → `concetto-<slug>`
  - `data/` → `data-<slug>`
  - `docs/` → `doc-<slug>`
  - `projects/` → `progetto-<slug>`
  - `outputs/` → `output-<slug>`
  - `code/` → `code-<slug>`

### Ordine di costruzione (rispettalo)

1. **Hub prima** — note-mappa che collegano piu' entita' (es. nota identita' personale in `self/`).
2. **Dettaglio dopo** — ogni nota di dettaglio si collega al suo hub e ad almeno 2 note vicine.
3. **Mai link in avanti** — un wikilink punta solo a una nota gia' scritta in questa sessione o gia' esistente nel vault.

### Processo per ogni nota

1. Mostra la prima nota (sempre l'hub principale) prima di procedere con le altre.
   Aspetta conferma dell'utente.
2. Dopo l'ok, scrivi le note rimanenti nell'ordine corretto.
3. Dopo ogni cartella completata, aggiorna il relativo `index-<cartella>.md` aggiungendo
   una riga per ogni nota creata nel formato: `- [[nome-nota]] — descrizione breve`.

### Al termine

1. Rigenera `llms.txt` lanciando: `python3 generate_llms.py`
2. Conferma quante note sono state create e in quali cartelle.
3. Segnala eventuali fatti dalla fonte che non e' stato possibile mappare in nessuna cartella.
