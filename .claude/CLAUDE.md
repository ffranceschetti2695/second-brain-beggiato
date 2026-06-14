# Istruzioni per Claude

Questa è una cartella di vault Obsidian. Quando ricevi una domanda:

1. **Parti sempre dai file markdown presenti in questa cartella** — leggi prima i file rilevanti, poi rispondi.
2. Non cercare informazioni su strumenti esterni (Slack, Confluence, ecc.) a meno che io non lo chieda esplicitamente.
3. Se la risposta è nei file del vault, forniscila direttamente senza chiedere chiarimenti.

## Regole frontmatter per le note Obsidian

Quando crei note con frontmatter YAML, rispetta sempre queste regole (testate e verificate):

- **`related`**: array YAML inline con ogni wikilink quotato individualmente — `related: ["[[nota-a]]", "[[nota-b]]", "[[nota-c]]"]`
  - ❌ Non usare una stringa quotata unica: `related: "[[a]],[[b]]"` → crea nodi fantasma nel grafo
  - ❌ Non usare plain text senza parentesi: `related: [nota-a, nota-b]` → non navigabile
- **`summary`**: tra virgolette doppie se il testo contiene `:` — `summary: "Testo: con due punti"`
- **`tags`**: il primo tag è sempre il nome della cartella in cui si trova la nota
