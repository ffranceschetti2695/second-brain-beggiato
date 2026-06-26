---
title: "Sessione 2026-06-18-c"
summary: "Esplorazione Company Brain, creazione nota di progetto nel vault e primo RAG funzionante con ChromaDB."
tags: [workspace, type/session]
status: done
created: 2026-06-18
updated: 2026-06-18
related: ["[[progetto-company-brain]]", "[[area-ai-business]]", "[[concetto-company-brain]]", "[[concetto-rag]]", "[[doc-modelli-monetizzazione-ai]]"]
---

## Fatto

Sessione Socratica sul progetto Company Brain: chiarita l'architettura tecnica (ingestion pipeline, storage doppio vault + ChromaDB, query layer), il vantaggio competitivo (qualità note atomiche + onboarding consulenziale), e la sequenza commerciale corretta (retainer come punto d'ingresso, prodottizzazione come punto di arrivo). Creata `projects/progetto-company-brain.md` con architettura completa e roadmap in 5 step. Aggiornati `index-projects.md`, `area-ai-business.md` e `llms.txt`. Costruito il primo prototipo RAG funzionante: cartella `company-brain-rag/` sul Desktop con `ingest.py`, `query.py` e `requirements.txt`. 45 note del vault indicizzate in ChromaDB locale con embedding `all-MiniLM-L6-v2`. Due query di test riuscite.

## Deciso

- Stuart non è il primo cliente pilota: troppo grande (IP, complessità) ma il domain knowledge acquisito lì è un asset competitivo da usare con player più piccoli.
- Il modello di riferimento è prodottizzazione, ma il punto d'ingresso commerciale è il retainer su un primo cliente reale.
- Embedding locale (`sentence-transformers`) invece di OpenAI per il prototipo: gratis, nessuna API key aggiuntiva, meccanica identica.

## Aperto

- Aumentare il limite di caratteri per note lunghe in `query.py` (attualmente tronca a 1500 char)
- Aggiungere ingestion da fonte esterna reale (Notion API o Google Drive)
- Definire e trovare il primo cliente pilota (5–20 persone, Notion + Drive come stack)
