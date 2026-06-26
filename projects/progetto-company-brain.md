---
title: "Progetto — Company Brain"
summary: "Costruire e vendere company brain aziendali: architettura, roadmap e piano verso il primo cliente pilota."
tags: [projects, ai, business, company-brain]
status: active
created: 2026-06-18
updated: 2026-06-18
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

## Roadmap

| Step | Cosa fare | Stato |
|---|---|---|
| **1 — Personal brain** | Continuare a costruire il vault personale. Ogni nota insegna cosa funziona e cosa no. | In corso |
| **2 — ChromaDB locale** | Aggiungere ChromaDB al vault. Scrivere uno script che embeddizza le note esistenti. Imparare il RAG dall'interno. | Da fare |
| **3 — Script ingestion** | Script di ingestion da una fonte reale (Notion API o Google Drive). | Da fare |
| **4 — Primo cliente pilota** | Azienda piccola (5–20 persone), fonti limitate (Notion + Drive). Costruire il brain da zero. Imparare il workflow di onboarding. | Da fare |
| **5 — Scala** | Sistematizzare i connettori, automatizzare la pipeline, vendere il servizio. | Futuro |

## Note sul primo cliente pilota

- Dimensione ideale: 5–20 persone (fonti limitate, decisioni veloci, alto impatto visibile)
- Stack preferibile: Notion + Google Drive (API ben documentate, curva di apprendimento bassa)
- Obiettivo del pilota: imparare il workflow di onboarding, non fare profitto
- Profilo cliente: fondatore o COO di startup che già usa Notion come knowledge base

## Vedi anche

[[concetto-company-brain]] — [[area-ai-business]] — [[concetto-rag]] — [[doc-modelli-monetizzazione-ai]]
