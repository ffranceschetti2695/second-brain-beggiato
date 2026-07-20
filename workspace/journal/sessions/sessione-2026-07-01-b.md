---
title: "Sessione 2026-07-01-b"
summary: "Costruita la company-brain-app (pipeline ingestion Claude API + ChromaDB), spostata fuori dal vault; ricognizione MCP Stuart per il stuart-brain; corretto Giovanni Beggiato."
tags: [workspace, type/session]
status: done
created: 2026-07-01
updated: 2026-07-01
related: ["[[progetto-company-brain]]", "[[entity-stuart]]", "[[area-ai-business]]", "[[area-fp-and-a]]"]
---

## Fatto

- **Costruita la `company-brain-app`**: pipeline di ingestion che automatizza il flusso `/canon`. Componenti: connettori (`connectors/` con `local_folder` funzionante + `notion` pronto), `canonizer.py` (Claude API, modello `claude-opus-4-8`, due fasi canon→note atomiche strutturate), `vault_writer.py` (frontmatter conforme alle regole del vault), `vector_store.py` (ChromaDB locale, embedding `all-MiniLM-L6-v2`), `state.py` (ingestion incrementale), `llms_generator.py`, `pipeline.py` (orchestratore CLI).
- **Copre step 2 (ChromaDB) + step 3 (ingestion) della roadmap** di [[progetto-company-brain]].
- **Vault target parametrico** (`--vault`): la pipeline scrive nel brain del cliente, non nel personale. Testata end-to-end su un `demo-vault` isolato (12 note generate dal trascritto di Giovanni Beggiato + ricerca semantica funzionante).
- **Spostata l'app FUORI dal vault**: ora vive in `~/Desktop/company-brain-app/` (non più dentro Personal Brain). `.gitignore` del brain ripristinato.
- **Corretto "Joe/Gio" → Giovanni Beggiato** in tutte le note testuali del brain; salvata memoria dedicata.
- **Ricognizione MCP su Stuart** (dominio Ops/FP&A/reporting) per il futuro `stuart-brain`:
  - **Drive**: working set finance vivo (GM OPS Tracker, FP&A Ancillaries, FC6 GM Analysis, Consolidated P&L, MBR/GM decks).
  - **Confluence** (`stuart-team.atlassian.net`): Financial Data Pipeline (handbook BP/FC, FP&A), SteerCo Revenue↔BPO Ops mensili (spazio TOM), OKR 1.2 GM €4.3m, Automation Opportunities for Courier Ops Tasks. Rumore da scartare: post-mortem "Consuming lag" vuoti.
  - **Data warehouse** (Superset MCP): dataset FP&A chiave = `reporting_finance.global_gm_performance__monthly` (id 766) + `metrics_core.delivery_finance` (id 378) + Delivery Incentive Detail (1648, CPO).
  - **Slack**: canali chiave = **#operations** (`C041W0BD7U0`, financial update settimanale vs FC3), **#uk_ops-commercial** (`C3EL24P6E`), **#uk-summer-war-room** (`C0B7ZKTG6BU`), + group DM leadership (Ricardo Amorim, Sonia Gastelum, Dimitrij, Mark Jones, Luxs).

## Deciso

- **Stuart = palestra e proof, NON l'asset da vendere.** Si dogfooda il company brain su Stuart per imparare il workflow di onboarding; il prodotto vendibile è l'IP generica (motore + connettori + playbook), mai i dati Stuart. Primo cliente pagante ideale resta piccolo (5–20 persone), non Stuart.
- **Il codice sta fuori dal vault**; le note generate vanno in un vault target separato.
- **Copertura completa di Slack = lavoro del connettore, non della lettura manuale in chat** (la mia ricognizione era un campione parziale, keyword+UK biased: NON è overview completa).
- Modello di canonizzazione: `claude-opus-4-8` con adaptive thinking, structured outputs con fallback JSON per SDK vecchi.

## Aperto

### Stuart

- Il brain deve nascere dall'**ossatura operativa reale**, che vive su Slack + riunioni (non nei doc, spesso datati). Costruire il **connettore Slack** che tira le storie intere dei canali chiave (#operations, #uk_ops-commercial, #uk-summer-war-room, DM leadership) + FR/PL, non solo UK.
- **Leggere i transcript delle riunioni Google.** Link di esempio fornito da Francesco (da provare in nuova chat): `https://docs.google.com/document/d/1GgYk_x53fMG8RmS-nOcbtEV3I33dtxDSB34qUH47dYQ/edit` — capire la convenzione di naming/cartella dei transcript per ingerirli tutti. (Tool Drive `read_file_content` già disponibile.)
- Minare il file da ~54k caratteri della prima ricerca Slack (salvato nei tool-results) via subagent.

### Progetto AI / Monetizzazione

- **Costruire il `stuart-brain`** dalla fetta-nucleo (Slack #operations + war room + DM leve + Financial Data Pipeline Confluence + dataset FP&A 766/378 DWH): io leggo via MCP → scrivo in `stuart-vault/sources/` → lancio la pipeline → note + vector store. Vault in `~/Desktop/company-brain-app/stuart-vault/`.
- Testare un'**automazione sopra il brain**: candidata naturale = il Financial Update settimanale (l'agente lo redige col contesto del brain).
- Miglioramenti pipeline: **embedding multilingue** (la ricerca in italiano con all-MiniLM è mediocre); promuovere il connettore Slack/Confluence/DWH da MCP-in-sessione a codice reale.
- Eventuale **interfaccia visiva** (chat/dashboard sopra il vector store) — non ancora costruita.
