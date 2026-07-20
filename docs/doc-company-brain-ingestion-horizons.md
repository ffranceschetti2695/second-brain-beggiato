---
title: "Company Brain — Orizzonti temporali di ingestion per fonte"
summary: "Lookback configurati per ogni fonte del stuart-brain: Confluence per spazio, Slack da definire, Drive e DWH da fare."
tags: [docs, ai, company-brain]
status: active
created: 2026-07-06
updated: 2026-07-07
related: ["[[progetto-company-brain]]", "[[concetto-rag]]", "[[doc-dwh-finance-schema]]"]
---

# Company Brain — Orizzonti temporali di ingestion

Questa nota centralizza i lookback decisi per ciascuna fonte del [[progetto-company-brain]] (stuart-brain). L'obiettivo è avere signal/noise alto: documenti troppo vecchi diventano rumore.

## Confluence

| Spazio | Lookback | Stato | Note |
|---|---|---|---|
| STRAT | 18 mesi | Fatto | OKR, strategia, board deck |
| GO | 12 mesi | Fatto | Ops commerciale, go-to-market |
| PROP | 6 mesi | Fatto | Proposal, commerciale attivo |
| DATA | 6 mesi | Fatto | Schema DWH, metriche, data team |
| TOM | 90 giorni + filtro keyword decisionale | Fatto (2026-07-07) | 504 file totali filtrati a 40 (recency+keyword), 28 note atomiche dopo dedup, 5 file scartati (template vuoti/status thin) |

## Slack

Lookback non ancora formalizzato in modo uniforme. Nella sessione 2026-07-01 sono stati estratti 21 canali/DM senza un orizzonte temporale esplicito — la profondità dipendeva da quanto l'MCP restituiva per canale. Per i group DM leadership (2026-07-07) si è usato 90 giorni, coerente con la convenzione TOM/Drive.

Canali estratti (run 2026-07-01):
- Canali privati: FC6, finance, strategia Mutares, FR task force
- DM diretti: Sonia Gastelum, Ricardo Amorim, Mateo Noceti, Dimitrij Phoursa, Mark Jones, Antoine Wiecek, Gaspard RC

Group DM leadership ingeriti (2026-07-07, lookback 90gg):
- C0B6B1926G4 — Ricardo, Sonia, Dimitrij, Francesco (FR Task Force + SLO UK)
- C0B3CKX6FCY — + Cornelia Raportaru (financial update pre-weekend, pre-MBR)
- C0B6QTY1M9R — Mark Jones, Ricardo, Luxsanan Ramanusam, Dimitrij, Francesco (UK war room)
- C0A723ELQEA — Cornelia, Sonia, Francesco (MBR next steps, escalation ladder)

Canali già ingeriti in sessione 2026-07-07: `#operations`, `#revenue`, `#monthly_business_review`, `#uk_ops-commercial` (`C3EL24P6E`, 90gg — canale ad altissimo volume di status quotidiano, solo 1 framework durevole estratto: RAG store Tesco), `#uk-summer-war-room` (`C0B7ZKTG6BU`, 90gg — log settimanale strutturato, alto signal, hub dedicato creato).

Nessun canale noto ancora mancante da questa lista iniziale.

**Da decidere**: lookback standard Slack per i canali già ingeriti nel run 2026-07-01 (ipotesi: 6 mesi per canali strategici, 3 mesi per canali operativi) — tutte le ingestion successive (group DM leadership, uk_ops-commercial, uk-summer-war-room) hanno adottato 90 giorni.

## Google Drive

Nessun orizzonte definito. Ancora da fare. Fonti target: transcript Meet, FC/MBR report deck.

**Da decidere**: lookback ragionevole (ipotesi: 12 mesi per MBR/FC deck, 6 mesi per transcript Meet).

## Gmail (Notes by Gemini)

| Lookback | Stato | Note |
|---|---|---|
| 365 giorni (2025-07-07 → 2026-07-07), tutte le email | Fatto (2026-07-07) | 77 email "Notes by Gemini" (gemini-notes@google.com) ingerite senza filtro, canonizzate in 44 note atomiche nel stuart-vault |

Le serie ricorrenti (Weekly Operations & Sustainability, Pre-weekend CPO Governance, Global Revenue Bi-Weekly, Monthly Business Review) sono state raccolte in note-hub con log cronologico invece di una nota per istanza, per evitare duplicazione. I meeting one-off (FC3/FC6 review cycle, 1:1, iniziative strategiche) hanno note atomiche individuali. Raw source dei singoli email in `stuart-vault/sources/gmail/`.

## DWH (BigQuery)

Nessun orizzonte definito. Ancora da fare. Obiettivo: snapshot settimanale delle tabelle FP&A chiave (766/378 volume/GM).

**Da decidere**: finestra rolling (ipotesi: 24 mesi di storico per trend, refresh settimanale).

## Principio generale

Il lookback dovrebbe riflettere il ciclo di vita del contenuto:
- Strategia/OKR: 12–18 mesi (cambiano ogni anno)
- Ops attiva: 3–6 mesi (si evolve rapidamente)
- Dati finanziari: 24 mesi (serve storico per trend)
- Handbook/TOM: 90 giorni + filtro — il vecchio diventa obsoleto senza avvisare

## Vedi anche

[[progetto-company-brain]] — [[concetto-rag]] — [[doc-dwh-finance-schema]]
