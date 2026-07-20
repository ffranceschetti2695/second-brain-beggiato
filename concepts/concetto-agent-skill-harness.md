---
title: "Agent, Skill e Harness: tre livelli distinti in Claude Code"
summary: "Skill = procedura che modifica il mio comportamento; Agent = sub-istanza delegata con contesto isolato; Harness = l'infrastruttura (CLI/SDK) che rende possibili entrambi."
tags: [concepts, ai, tooling]
status: active
created: 2026-07-07
updated: 2026-07-07
related: ["[[concetto-claude-code-vs-api-billing]]", "[[concetto-company-brain]]"]
---

# Agent, Skill e Harness: tre livelli distinti in Claude Code

## Il concetto

Tre termini spesso confusi perché coesistono nello stesso ambiente, ma vivono a livelli diversi:

| Livello | Cos'è | Esempio |
|---|---|---|
| **Skill** | Istruzioni pacchettizzate (markdown + risorse) che dicono a Claude *come* affrontare un compito specifico. Non gira in autonomia: carica nel contesto di Claude e ne cambia il comportamento per quel turno | `journal`, `systematic-debugging`, `agent-debates` |
| **Agent** | Istanza separata del modello, con contesto e tool propri, spawnata per un compito autonomo e delimitato. Gira indipendentemente e ritorna un risultato, senza condividere la cronologia della conversazione a meno che non gliela si passi esplicitamente | `Explore`, `general-purpose`, agenti spawnati da una skill |
| **Harness** | L'infrastruttura che ospita tutto: CLI/SDK, sistema di permessi, CLAUDE.md, hook, memoria persistente. Rende possibile invocare skill e spawnare agent | Claude Code stesso |

Analogia: harness = l'ufficio e i suoi sistemi, skill = una procedura/checklist sulla scrivania, agent = un collega a cui si delega un sotto-compito.

## Skill e Agent possono comporsi

Una skill può prescrivere lo spawn di uno o più agent come parte della sua esecuzione. Esempi concreti:

- `agent-debates` — spawna agent con posizioni avversariali che discutono su round multipli
- `deep-research` — fan-out di agent di ricerca in parallelo, poi sintesi
- `code-review` — agent separati per dimensione di review, poi verifica adversariale dei finding

La skill è la ricetta, l'agent è il cuoco delegato: la skill non è un agent, ma può orchestrarne.

## "Agentic" è un concetto più ampio

Nel senso generale, "agentic" descrive qualunque workflow in cui il modello incatena autonomamente ragionamento e tool call verso un obiettivo (es. leggere un'email, decidere, rispondere). In questo senso ampio, Claude è sempre "un agente" quando usa tool per conto dell'utente — indipendentemente dal fatto che spawni o meno un Agent in senso tecnico (harness).

La distinzione stretta (Agent come sub-istanza con contesto isolato) è un caso specifico di quel concetto più ampio, usato quando conviene isolare il contesto o parallelizzare, non l'unico modo di essere "agentic".

## Vedi anche

[[concetto-claude-code-vs-api-billing]] — [[concetto-company-brain]] — [[progetto-company-brain]]
