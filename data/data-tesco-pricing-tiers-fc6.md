---
title: "Tesco — Nuovo sistema di pricing tier (RFP FC6)"
summary: "Tabella dei nuovi tier RPO Tesco post-RFP (confermati, in vigore da luglio 2026), con la vecchia tabella tier 2023-2025 che sostituiscono"
tags: [data, type/reference, tesco, pricing]
status: active
created: 2026-07-13
updated: 2026-07-13
related: ["[[entity-stuart]]", "[[persona-mark-jones]]", "[[concetto-rpo-cpo-slo]]", "[[concetto-additional-rpo]]", "[[data-fc3-baseline-2026]]"]
---

# Tesco — Nuovo sistema di pricing tier (RFP FC6)

Nuovi tier RPO per [[entity-stuart]] su Tesco, usciti dalla RFP conclusa a maggio 2026 e confermati come contract net rates. Documentati nella Confluence "FC6/RFP Tesco Strategy Document" (spazio TOM, autore [[persona-mark-jones]], ultimo aggiornamento 2026-05-22): https://stuart-team.atlassian.net/wiki/spaces/TOM/pages/6982270978/FC6+RFP+Tesco+Strategy+Document

Rollout annunciato in Slack (#uk_ops-commercial) da Damián Kinderknecht il 2026-07-01: "nuove tariffe implementate da oggi", con soglie riconvertite da mensili a settimanali (÷ ~4,345 settimane/mese).

## Tabella tier (soglie mensili, tariffa netta)

| Volume mensile | Tariffa lorda | Tariffa netta (dopo breakage e marketing) |
|---|---|---|
| ≤ 400.000 ordini | £4,75 | **£4,68** (−£0,07 breakage) |
| 400.001 – 430.000 ordini | £4,50 | **£4,43** (−£0,07 breakage; marketing non ancora attivato) |
| Oltre 430.000 ordini | £4,50 | **£4,40** (−£0,07 breakage, −£0,03 marketing) |
| Oltre 500.000 ordini | £4,40 | £4,30 (non applicabile ai volumi attuali) |

Soglie equivalenti settimanali (usate nel rollout Slack): ~92.061 (£4,68) · ~98.965 (£4,43) · ~115.075 (£4,40).

Questi tier alimentano il modello di margine lordo FC6 (€1.437k) confrontato contro il benchmark FC3 (€1.039k) nel documento.

## Sostituisce: tabella tier 2023-2025 (superata)

Fonte precedente: Confluence "[Active] 2023-2025 SLAs & Pricing - Tesco" (spazio sales/Commercial, autore Haeri Yoon, ultimo aggiornamento 2025-04-01) — non aggiornata da prima del rollout RFP, quindi ormai stale: https://stuart-team.atlassian.net/wiki/spaces/sales/pages/4084596740/Active+2023-2025+SLAs+Pricing+-+Tesco

| Tier | Soglia volume (pacchi consegnati/settimana) | Sconto su totale pacchi |
|---|---|---|
| 1 | ≤ 30.000 | £0,00 |
| 2 | 30.001 – 40.000 | £0,10 |
| 3 | 40.001 – 50.000 | £0,20 |
| 4 | 50.001 – 70.000 | £0,30 |
| 5 | 70.001 – 90.000 | £0,40 |
| 6 | ≥ 90.001 | £0,50 |

Sconti non cumulabili tra tier; valutati in parallelo alla Stuart Pool Density Rebate (£0,40/pacco se un pool raggiunge ≥270 pacchi consegnati/settimana). Pricing update di marzo 2025: tariffa media finale £4,75 se ≥85.000 pacchi/settimana, altrimenti £4,85.

> ⚠️ Una nota interna ("Tesco Pricing Reporting", Confluence, giugno 2026) segnalava che il back office stava ancora usando la griglia tariffaria del 2024, prima del rollout dei nuovi tier — da verificare se l'allineamento è completo.

## Vedi anche

[[concetto-rpo-cpo-slo]] — [[concetto-additional-rpo]] — [[data-fc3-baseline-2026]]
