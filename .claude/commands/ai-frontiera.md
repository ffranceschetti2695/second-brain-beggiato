---
description: Daily AI digest — YouTube, X e Anthropic con sommari da transcript e log in journal
allowed-tools:
  - Read
  - Write
  - WebFetch
  - WebSearch
---

Sei un assistente che aggrega contenuti AI giornalieri. Esegui i passi qui sotto **in ordine**, senza saltarne nessuno.

## Argomenti

- `$ARGUMENTS` può contenere `--reset` (azzera seen) e/o `--giorni N` (finestra temporale, default 2)
- Esempio: `/ai-frontiera --giorni 7`

---

## Passo 1 — Leggi la configurazione

Leggi il file `.claude/commands/ai-frontiera-config.json` nel vault.
Leggi il file `.claude/commands/ai-frontiera-seen.json` nel vault (se non esiste, usa `{}`).

Se gli argomenti contengono `--reset`, sovrascrivi `ai-frontiera-seen.json` con `{}` e prosegui.

Estrai la finestra temporale: se `--giorni N` è presente usa N, altrimenti usa `finestra_ore` dal config diviso 24 (default 2 giorni).

---

## Passo 2 — Risolvi channel ID mancanti

Per ogni canale YouTube nel config con `"channel_id": null`:
- Fai una WebSearch: `{name} YouTube channel ID "UC"`
- Estrai l'ID nel formato `UCxxxxxxxx`
- Tienilo in memoria per questo run (non scrivere il file config)

---

## Passo 3 — Fetch YouTube RSS + transcript

Per ogni canale YouTube con `"active": true` (o senza campo active):

**3a. RSS feed:**
- URL: `https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}`
- Fai WebFetch sull'URL
- Estrai tutti gli `<entry>` con `<published>` nella finestra temporale
- Per ogni entry prendi: `<yt:videoId>`, `<title>`, `<published>`, `<link href>`, `<media:description>`
- Filtra gli ID già presenti in seen.json

**3b. Transcript (per ogni video nuovo trovato):**
- URL: `https://youtubetranscript.com/?server_vid={videoId}`
- Fai WebFetch su quell'URL
- Estrai il testo grezzo del transcript
- Se il fetch fallisce o il transcript è vuoto: usa la `<media:description>` dal feed RSS come fallback
- Se anche quella è vuota: usa solo il titolo

**3c. Sintetizza (per ogni video):**
Basandoti sul transcript (o fallback), produci:
- **Sommario**: 120-150 parole in italiano, narrativo, che spiega cosa viene mostrato/insegnato nel video. Circa 1 minuto di lettura.
- **Key message**: una frase secca sull'idea centrale
- **Bottom line**: perché è rilevante per chi vuole monetizzare AI

Se il fetch RSS fallisce: annota il canale come "non raggiungibile" e continua.

---

## Passo 4 — Fetch X/Twitter via Nitter RSS

Per ogni handle in `twitter_handles`:
- Prova prima: `https://nitter.net/{handle}/rss`
- Se fallisce: prova `https://nitter.privacydev.net/{handle}/rss`
- Se entrambi falliscono: annota come "non raggiungibile"
- Estrai i post con data nella finestra temporale
- Per ogni post: prendi id/link, testo completo, data
- Filtra gli ID già in seen.json

---

## Passo 5 — Fetch Anthropic News

- WebFetch su `https://www.anthropic.com/news`
- Estrai titoli, date e link degli articoli nella finestra temporale
- Se la data non è visibile, includi i 3 articoli più recenti

---

## Passo 6 — Produci l'output in chat

Se non ci sono contenuti nuovi scrivi:
> Nessun contenuto nuovo nelle ultime {N*24}h. Usa `--reset` per rivedere tutto o `--giorni N` per allargare la finestra.

Altrimenti produci questo output direttamente in chat:

---

## AI Frontiera — {data odierna YYYY-MM-DD}
*Finestra: ultime {N*24}h | Fetched: {ora attuale}*

### 📌 Overview generale
[2-3 frasi sul tono del momento: cosa sta succedendo nel panorama AI, quali temi emergono. In italiano.]

---

### 🎥 YouTube — Nuovi video
[Per ogni video trovato:]

**{Nome canale}** · {data pubblicazione}
[{Titolo video}]({URL})

{Sommario 120-150 parole basato sul transcript}

> **Key message:** {una frase}
> **Bottom line:** {perché è rilevante per monetizzare AI}

[Se nessun video: "Nessun video nuovo in questa finestra temporale."]

---

### 🐦 X / Twitter — Post rilevanti
[Per ogni post trovato:]

**@{handle}** · {data}
[→ link]({URL tweet})
> {testo completo del post o riassunto thread}

[Se nessun post: "Nessun post nuovo o Nitter non raggiungibile."]

---

### 📰 Anthropic — News & blog
[Per ogni articolo trovato:]

**[{Titolo}]({URL})** · {data}
> {1-2 righe di sommario}

[Se nessun articolo: "Nessun articolo nuovo."]

---

*Fonti non raggiungibili: {lista o "nessuna"}*

---

## Passo 7 — Aggiorna seen.json

Per ogni contenuto mostrato costruisci un oggetto con questi campi:
- `date`: data di pubblicazione (YYYY-MM-DD)
- `seen_on`: data di oggi (YYYY-MM-DD)
- `type`: `"youtube"` | `"twitter"` | `"anthropic"`
- `source`: nome canale / handle / `"Anthropic"`
- `title`: titolo o testo troncato
- `url`: link diretto
- `summary`: il sommario completo (solo youtube)
- `key_message`: (youtube e anthropic)
- `bottom_line`: (solo youtube)

Leggi `ai-frontiera-seen.json`, aggiungi le nuove voci, riscrivi il file.

---

## Passo 8 — Aggiorna il journal

Leggi il file `workspace/journal/ai-frontiera-log.md` (se non esiste, crealo con intestazione: `# AI Frontiera — Log\n\n`).

Prependi in cima al contenuto esistente (dopo l'intestazione) una nuova voce con questo formato:

```markdown
---

## {data odierna YYYY-MM-DD}

**Overview:** {le stesse 2-3 frasi dell'overview generale}

### Video
{Per ogni video: "- **[{titolo}]({url})** ({fonte}) — {key message}"}

### Post X
{Per ogni post: "- **@{handle}** — {testo troncato a 100 char} [→]({url})"}

### Anthropic
{Per ogni articolo: "- **[{titolo}]({url})** — {sommario breve}"}

```

Scrivi il file aggiornato in `workspace/journal/ai-frontiera-log.md`.
