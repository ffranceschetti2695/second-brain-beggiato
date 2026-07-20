---
title: "Claude Code subscription vs Anthropic API billing"
summary: "Claude Code (abbonamento) e Anthropic API (SDK Python) sono due prodotti con billing separato: usare l'SDK consuma crediti API indipendentemente dall'abbonamento."
tags: [concepts, ai, tooling]
status: active
created: 2026-07-04
updated: 2026-07-04
related: ["[[concetto-company-brain]]", "[[area-ai-business]]"]
---

# Claude Code subscription vs Anthropic API billing

## Il concetto

Ci sono due modi di usare Claude che sembrano simili ma hanno billing completamente separato:

| Prodotto | Come si usa | Billing |
|---|---|---|
| **Claude Code** | CLI/IDE extension, questa conversazione, Agent spawned in sessione | Abbonamento mensile fisso |
| **Anthropic API** | `import anthropic` → `client.messages.create(...)` nel codice Python | A consumo (token in/out) |

## Perché importa

Una pipeline Python che chiama `anthropic.Anthropic().messages.create(...)` **non usa i token del tuo abbonamento Claude Code**. Usa crediti API separati, che si esauriscono. L'abbonamento Claude Code non copre le chiamate SDK fatte da script esterni.

## Come sfruttare l'abbonamento

Per canonizzare documenti senza consumare crediti API, la soluzione è fare il lavoro dentro la sessione Claude Code:

1. Fetch dei dati grezzi via curl/HTTP (zero costo)
2. Passare il contenuto agli Agent spawned nella sessione (usa i token dell'abbonamento)
3. Gli Agent scrivono le note direttamente nel vault

Questo è più lento della pipeline automatica ma non costa nulla in più rispetto all'abbonamento già pagato.

## Quando usare cosa

- **In-session Agent** → canonizzazione one-shot, prototipi, ingestion manuale (come il stuart-brain)
- **Anthropic API** → pipeline automatica notturna in produzione, quando il costo per token è giustificato dal volume e dall'automazione

## Vedi anche

[[concetto-company-brain]] — [[area-ai-business]] — [[concetto-speed-to-lead-stack]]
