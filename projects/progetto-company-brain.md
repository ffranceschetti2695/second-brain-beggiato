---
title: "Progetto — Company Brain"
summary: "Costruire e vendere company brain aziendali: architettura, roadmap e piano verso il primo cliente pilota."
tags: [projects, ai, business, company-brain]
status: active
created: 2026-06-18
updated: 2026-07-07
related: ["[[area-ai-business]]", "[[concetto-company-brain]]", "[[concetto-rag]]", "[[concetto-automazioni-ai-silo]]", "[[doc-modelli-monetizzazione-ai]]"]
---

# Progetto — Company Brain

## Il personal brain come prototipo

Questo vault è già la versione artigianale del prodotto. Scalare significa sostituire ogni componente manuale con uno automatizzato.

| Personal Brain (ora) | Company Brain (scalato) |
|---|---|
| Depositi PDF in `sources/` | Pipeline automatica da API |
| `/canon` (Claude legge) | Claude API in batch |
| Note `.md` nel vault | Note `.md` + vector DB |
| `llms.txt` caricato in contesto | RAG: solo le note rilevanti |
| Tu fai domande a Claude | Automazioni + chatbot interno |

## Architettura tecnica

```
[FONTI AZIENDALI]
Confluence · Notion · Slack · Drive · Email · CRM
        ↓
[INGESTION PIPELINE]  ← il cuore del business
Connettori API → chunking → Claude API → note atomiche .md
        ↓
[STORAGE DOPPIO]
vault/ (leggibile da umani)  +  ChromaDB/Qdrant (interrogabile da AI)
        ↓
[QUERY LAYER]
Domanda → embedding → top-10 note → Claude → risposta
        ↓
[AUTOMAZIONI]
Onboarding bot · Supporto decisioni · Report automatici · Alert
```

L'ingestion non è un'operazione una tantum — è un loop che gira in background (es. ogni notte), recupera i nuovi documenti dalle fonti, li trasforma in note atomiche via Claude API, aggiorna vault e vector DB, e rigenera l'indice.

## Vantaggio competitivo

Il RAG è commodity — chiunque può fare `pip install chromadb`. Il valore è in due cose difficili:

1. **Qualità delle note atomiche** — trasformare raw data (es. thread Slack di 300 msg) in note strutturate con frontmatter corretto e wikilink coerenti. È la skill `/canon` applicata a fonti aziendali. Richiede prompt engineering sofisticato.
2. **Workflow di onboarding del cliente** — capire quali fonti contano, strutturare la tassonomia delle note per quella specifica azienda, identificare le automazioni ad alto valore immediato. Questa è consulenza, non solo tech. È dove entra il background FP&A.

## Stato stuart-brain (dogfood su Stuart, aggiornato 2026-07-07)

Il brain di Stuart è operativo in `~/Desktop/company-brain-app/stuart-vault/`.

| Fonte | Stato | Note create |
|---|---|---|
| Slack (canali + DM 1:1 + group DM leadership + war room) | Fatto | ~350+ |
| Confluence STRAT | Fatto | 9 (OKR 2026 completi) |
| Confluence DATA | Fatto | 11 (schema DWH, metriche) |
| Confluence GO+PROP | Fatto | 15 (ops + commerciale) |
| Confluence TOM | Fatto | 28 (filtro 90gg + keyword strategia/decisione, da 504 → 40 candidate) |
| Google Drive | Fatto (parziale) | 13 (FC6, MBR, H2 Plan, Mutares) — transcript Meet bloccati da Google ("ineligible for generative AI contexts") |
| Gmail Notes by Gemini | Fatto | 44 (77 email, lookback 365gg, log di dedup manuale in `doc-gmail-notes-gemini-ingestion-log`) |
| DWH snapshot | Fatto | 1 nota (Volume/GM mensile gen-giu 2026 per mercato via Superset MCP, `metrics_core.delivery_finance`; query in `connectors/dwh.py` corretta contro lo schema reale, era fittizia) |

**Totale attuale: 461 note atomiche + ChromaDB operativo.**

## Roadmap

| Step | Cosa fare | Stato |
|---|---|---|
| **1 — Personal brain** | Continuare a costruire il vault personale. | In corso |
| **2 — ChromaDB + pipeline** | Pipeline ingestion + ChromaDB locale. | Fatto |
| **3 — Stuart-brain** | Dogfood su Stuart: Slack + Confluence + Drive + Gmail + DWH. | Fatto (tutte le fonti coperte, solo Google Meet transcript bloccato lato Google) |
| **4 — Primo cliente pilota** | Azienda piccola (5–20 persone), fonti limitate. | Da fare |
| **5 — Scala** | Sistematizzare connettori, automatizzare pipeline, vendere. | Futuro |

## Aperto

- Vector DB (ChromaDB) su stuart-vault: disallineato (318/466 note indicizzate, ID stale dopo un rename di massa) e probabilmente superfluo sotto la soglia delle 500 note (vedi [[concetto-rag]]). Deciso 2026-07-07 di rimandare la re-indicizzazione a quando il prodotto sarà pronto per un vero test di scala, e nel frattempo lasciare `.chroma` così com'è (nessun danno, solo inutilizzato).
- Google Meet transcript: bloccati a livello Google, da rivalutare con approccio alternativo.
- Gmail Notes by Gemini: nessun connector/stato di dedup automatico, solo log manuale — da sistematizzare per ingestion incrementali future.
- DWH: nessuna credenziale Superset REST in `.env`, quindi il refresh resta manuale via MCP in sessione — da valutare uno scheduler quando si passa al primo cliente pilota.
- Media/bassa severità emerse dal coherence check 2026-07-07 (non ancora risolte): refuso anno FC3 lock date, vintage RPO Carrefour FR non esplicito tra FC3/FC6, buco operativo su Fnac (solo 1 nota, zero traccia Slack), 4 note quasi-duplicate sul ramp-down BPO organico.

## Note sul primo cliente pilota

- Dimensione ideale: 5–20 persone (fonti limitate, decisioni veloci, alto impatto visibile)
- Stack preferibile: Notion + Google Drive (API ben documentate, curva di apprendimento bassa)
- Obiettivo del pilota: imparare il workflow di onboarding, non fare profitto
- Profilo cliente: fondatore o COO di startup che già usa Notion come knowledge base

## Vedi anche

[[concetto-company-brain]] — [[area-ai-business]] — [[concetto-rag]] — [[doc-modelli-monetizzazione-ai]]
