# Skill: performance

Costruisce lo scostamento mensile **Actual vs FC3** di Stuart (Volume, GR, GM) come bridge a 7 barre, partendo dal DWH e dalla baseline FC3.

**TRIGGER:**
Invoca questa skill quando l'utente dice "performance mensile", "slide performance", "bridge del mese", "scostamento actual vs FC3", "company performance", "waterfall del mese" o qualsiasi richiesta di costruire i bridge di performance di Stuart.

---

## Regole generali (applica sempre)

- Date in formato `YYYY-MM-DD`, mai relative.
- Fonte actuals = **DWH**, sempre. Mai i valori della sheet dashboard.
- Italiano naturale, nessun m-dash.
- Non inventare numeri: ogni cifra arriva dal DWH o dalla baseline FC3. Se un dato manca, fermati e chiedi.

---

## Materiali di riferimento (leggi prima di tutto)

All'avvio leggi questi file del vault, in quest'ordine:

1. `docs/doc-flusso-performance-mensile.md` — la procedura completa.
2. `code/code-query-actuals-dwh.md` — la query SQL canonica.
3. `docs/doc-dwh-finance-schema.md` — schema tabelle DWH.
4. `data/data-stuart-segmentazione-clienti.md` — mapping gruppo -> barra.
5. `data/data-fc3-baseline-2026.md` — baseline FC3 e logica delle 7 barre.

---

## Passi

1. **Chiedi il mese di lavoro** se non e' gia' indicato (es. "maggio 2026"). Calcola `month_end_date` = ultimo giorno del mese (`YYYY-MM-31`/`30`/`28`).

2. **Lancia la query actuals.** Prendi l'SQL da `code/code-query-actuals-dwh.md`, sostituisci `month_end_date` sul mese richiesto, e eseguila via MCP `superset-mcp_4_Execute_SQL_query` (sostituisci i newline con spazi nella chiamata). Se l'MCP non e' connesso, dillo e fermati.

3. **Applica il mapping.** Collassa `client_forecast_group_adj` nelle 7 barre (Tesco, UK Top, FR Top, PL Top, Mid-Market, SMB, Pipeline ENT) seguendo `data-stuart-segmentazione-clienti`. Negli actuals la Pipeline ENT e' 0.

4. **Check di quadratura (obbligatorio).** Verifica che il **volume totale** Actual coincida con il riferimento noto del mese. Se non quadra, **fermati**: il problema e' nel grouping o nel mese, non nei dati. Riporta lo scarto e chiedi.

5. **Leggi la baseline FC3** del mese (colonna del mese da `data-fc3-baseline-2026`; per mesi non congelati chiedi l'export FC3). Ricorda lo split pipeline (ENT a se', SMB dentro SMB, MM dentro MM) e l'estrazione di Intermarche verso FR Top.

6. **Costruisci i 3 bridge** (Volume, GR, GM). Per ciascuno: barra iniziale FC3, delta per barra (Actual - FC3), barra finale Actual. La somma dei delta deve quadrare (check = 0). Mostra ogni bridge come tabella: barra, FC3, Actual, delta.

7. **Narrativa.** Aggiungi 3-4 righe: driver principali del miss/beat, ranking dei segmenti per impatto, eventuale effetto [[concetto-additional-rpo]] sulla barra PL Top.

8. **Output.** Presenta i 3 bridge + la narrativa in chat. Poi **chiedi** se salvare il risultato in `outputs/` o aggiornare la colonna del mese in `data-fc3-baseline-2026`. Non scrivere file senza ok.

---

## Caveat noti

- **PL AmRest/JET**: GR e GM divergono dalla dashboard per additional RPO (scarto variabile, non fisso). Si usano i valori DWH; la barra PL Top assorbe lo scostamento. Il Volume non e' mai impattato.
- **Versione FC3**: scarto noto su Tesco GM tra dashboard ed export marzo. Per i valori FC3 dashboard usa i numeri dashboard.
- **Limite MCP**: la query Superset tronca a 10.000 righe; l'aggregato sta sotto.
