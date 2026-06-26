---
title: "RAG (Retrieval-Augmented Generation)"
summary: "Tecnica AI che recupera solo i documenti semanticamente rilevanti per una query, invece di caricare tutto il knowledge base in contesto."
tags: [concepts, ai, tech]
status: active
created: 2026-06-18
updated: 2026-06-18
related: ["[[index-concepts]]", "[[concetto-company-brain]]", "[[self-obiettivi]]"]
---

# RAG — Retrieval-Augmented Generation

## Il problema che risolve

Caricare 22.000 note in un contesto LLM è impossibile per limiti tecnici e di qualità. RAG risolve questo: invece di caricare tutto, recupera solo le note rilevanti per la domanda specifica.

## Come funziona

```
Query utente
    ↓
Converti query in vettore (embedding)
    ↓
Trova le 10 note più vicine nel DB vettoriale
    ↓
Carica quelle 10 note nel contesto dell'LLM
    ↓
L'LLM risponde usando solo quelle note
```

Ogni nota viene convertita in un array numerico (es. 1.536 dimensioni) che cattura il suo significato semantico. Note simili hanno vettori vicini nello spazio — la ricerca trova i vicini più prossimi alla query.

## Componenti tecnici

| Componente | Cos'è | Esempi |
|---|---|---|
| Embedding model | Converte testo in vettori | OpenAI `text-embedding-3-small`, nomic-embed |
| Vector database | Archivia vettori e cerca per similarità | ChromaDB (locale), Qdrant, Pinecone |
| Query layer | Orchestra il flusso embedding → ricerca → risposta | Python diretto, LangChain, LlamaIndex |

## Costi indicativi

Embeddizzare 22.000 note con OpenAI `text-embedding-3-small`: circa 2–4 euro una tantum.
Le query successive costano frazioni di centesimo.

## RAG vs llms.txt (il sistema attuale del vault)

| | llms.txt flat | RAG |
|---|---|---|
| Note supportate comodamente | ~500 | 100.000+ |
| Setup | Nessuno | Script Python + DB |
| Qualità risposta | Alta (tutto in contesto) | Alta (solo il rilevante) |
| Costo | 0 | Frazioni di centesimo per query |

Sotto le 500 note, `llms.txt` è più semplice e sufficiente. Sopra quella soglia, RAG diventa necessario.

## Rilevanza per il Company Brain

Il [[concetto-company-brain]] usa RAG come layer di interrogazione della knowledge aziendale. È la tecnologia che rende possibile scalare da un vault personale a un sistema multi-utente su decine di migliaia di documenti.

## Vedi anche

[[concetto-company-brain]] — l'applicazione business del RAG
[[concetto-automazioni-ai-silo]] — il problema che il RAG aiuta a risolvere su scala
[[self-obiettivi]] — obiettivo di costruire un company brain come prodotto
