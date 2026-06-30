# Skill: journal

Gestisce la memoria dinamica del Personal Brain. Quattro comandi:
`inizia sessione` | `buongiorno` | `chiudi sessione` | `fine giornata`.

**TRIGGER OBBLIGATORIO — NON NEGOZIABILE:**
Se l'utente dice "inizia sessione", "inizio sessione", "iniziamo una nuova sessione", "nuova sessione", "iniziamo la sessione" o "buongiorno", devi invocare questa skill con il tool `Skill` **PRIMA di qualsiasi altra azione o risposta**. Non puoi rispondere, non puoi leggere file, non puoi fare nulla prima di aver invocato la skill. Questo non è opzionale. Non ci sono eccezioni.

Qualsiasi frase che segnali l'inizio di una sessione di lavoro — anche se formulata in modo diverso da quelle elencate — deve triggerare questa skill immediatamente.

---

## Regole generali (applica sempre)

- Date in formato `YYYY-MM-DD`, mai relative.
- Usa solo [[wikilink]] a note che esistono gia' nel vault (verifica in `llms.txt`).
- Non inventare entita': se non c'e' niente da agganciare, chiedi all'utente a cosa collegare la nota.
- Italiano naturale, nessun m-dash.
- Il frontmatter `related` e' sempre un array inline con ogni wikilink quotato:
  `related: ["[[nota-a]]", "[[nota-b]]"]`
- Il campo `summary` va tra virgolette doppie se contiene `:`.

---

## Comando: `inizia sessione` (alias: `buongiorno`)

**Scopo:** briefing di inizio sessione. Non scrivere nulla nel vault.

**Passi:**

1. Leggi `llms.txt` per avere la mappa aggiornata delle entita'.
2. Leggi l'ultima nota in `workspace/journal/sessions/` (quella col nome data piu' recente).
   Se non esiste nessuna sessione, leggi `workspace/journal/daily/` per l'ultima nota daily.
   Se non esiste neppure quella, di' che e' la prima sessione registrata.
3. Rispondi con un **briefing strutturato in due sezioni**, leggendo la sezione "## Aperto" dell'ultima nota:

   **Stuart**
   - I prossimi step lavorativi confermati dall'utente alla chiusura della sessione precedente.
   - Se la sezione Aperto non ha sottosezione Stuart, deduci dal contesto.

   **Progetto AI / Monetizzazione**
   - I prossimi step del progetto company brain / AI confermati dall'utente alla chiusura.
   - Se la sezione Aperto non ha sottosezione AI, deduci dal contesto.

   Niente inferenze extra, niente suggerimenti non richiesti. Riporta solo cio' che e' scritto nell'Aperto.
4. Non creare file. Non chiedere conferma. Solo il briefing.

---

## Comando: `chiudi sessione`

**Scopo:** scrivere la nota di sessione per la sessione corrente.

**Passi:**

1. Guarda la conversazione corrente e deduci cosa e' stato fatto in questa sessione.
2. In un unico messaggio, presenta:
   - La sintesi in 3 righe di cosa abbiamo fatto (non chiedere conferma su questa parte).
   - Subito sotto, la bozza della sezione **## Aperto** strutturata in due workstream:
   ```
   ## Aperto

   ### Stuart
   - <prossimo step lavorativo Stuart, se presente>

   ### Progetto AI / Monetizzazione
   - <prossimo step progetto company brain / AI, se presente>
   ```
   Poi chiedi esplicitamente: "Questi sono i prossimi passi che ti mostrero' all'inizio della prossima sessione. Vanno bene o vuoi aggiungere, togliere o riformulare qualcosa?"
   Aspetta la risposta e applica le modifiche richieste. Non chiedere una seconda conferma.
3. Scrivi il file con l'Aperto confermato:
   - **Percorso:** `workspace/journal/sessions/sessione-<YYYY-MM-DD>.md`
     dove `<YYYY-MM-DD>` e' la data di oggi.
   - Se esiste gia' un file con quel nome (piu' sessioni nello stesso giorno),
     aggiungi un suffisso: `sessione-<YYYY-MM-DD>-b.md`, `sessione-<YYYY-MM-DD>-c.md`, ecc.
5. **Frontmatter:**
   ```yaml
   ---
   title: "Sessione <YYYY-MM-DD>"
   summary: "<Una frase su cosa abbiamo fatto>"
   tags: [workspace, type/session]
   status: done
   created: <YYYY-MM-DD>
   updated: <YYYY-MM-DD>
   related: ["[[<entita-1>]]", "[[<entita-2>]]"]
   ---
   ```
   Il campo `related` deve contenere [[wikilink]] alle note toccate durante la sessione.
   Sceglile da `llms.txt`. Se non riesci a identificarne nessuna, chiedi all'utente.
6. **Corpo:**
   ```
   ## Fatto
   <Cosa abbiamo concluso.>

   ## Deciso
   <Le scelte prese e il perche'.>

   ## Aperto

   ### Stuart
   - <prossimi step Stuart confermati dall'utente>

   ### Progetto AI / Monetizzazione
   - <prossimi step AI/monetizzazione confermati dall'utente>
   ```
7. Dopo aver scritto, conferma il percorso del file creato.

---

## Comando: `fine giornata`

**Scopo:** scrivere il daily che fonde tutte le sessioni del giorno.

**Passi:**

1. Leggi **tutte** le note `workspace/journal/sessions/sessione-<data-di-oggi>*.md`.
2. **Prima di scrivere**, di' in 3 righe cosa hai capito che e' successo oggi in totale.
   Aspetta l'ok dell'utente.
3. Dopo l'ok, scrivi il file:
   - **Percorso:** `workspace/journal/daily/<YYYY-MM-DD>.md`
4. **Frontmatter:**
   ```yaml
   ---
   title: "Daily <YYYY-MM-DD>"
   summary: "<Una frase: il filo conduttore della giornata>"
   tags: [workspace, type/daily]
   status: done
   created: <YYYY-MM-DD>
   updated: <YYYY-MM-DD>
   related: ["[[sessione-<YYYY-MM-DD>]]", "[[<entita-principale-1>]]", "[[<entita-principale-2>]]"]
   ---
   ```
   Il `related` include i [[wikilink]] a tutte le sessioni del giorno + le entita' statiche principali toccate.
5. **Corpo:**
   ```
   ## Fatto
   <Sintesi della giornata: cosa e' stato concluso. Fondi le sessioni senza ripeterle riga per riga.>

   ## Deciso
   <Le scelte prese durante la giornata e il loro perche'.>

   ## Aperto
   <Tutto cio' che resta in sospeso all'uscita dalla giornata.>

   ## Sessioni
   - [[sessione-<YYYY-MM-DD>]]
   - [[sessione-<YYYY-MM-DD>-b]]   ← solo se esistono sessioni aggiuntive
   ```
6. Dopo aver scritto, conferma il percorso del file creato.

---

## Template di riferimento

I template riusabili sono in:
- `workspace/journal/_templates/template-sessione.md`
- `workspace/journal/_templates/template-daily.md`
