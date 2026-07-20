---
title: "Schema DWH Finance (Stuart)"
summary: "Le tabelle del DWH Stuart usate per gli actuals di performance: granularita', colonne chiave, conversione FX e caveat."
tags: [docs, stuart, dwh, sql, reference]
status: active
created: 2026-06-25
updated: 2026-07-02
related: ["[[code-query-actuals-dwh]]", "[[doc-flusso-performance-mensile]]", "[[entity-stuart]]", "[[concetto-additional-rpo]]"]
---

# Schema DWH Finance

Tabelle del data warehouse di [[entity-stuart]] (Redshift, accesse via Superset SQL Lab / MCP) usate per estrarre gli actuals delle slide di performance. Riferimento per scrivere nuove query oltre a [[code-query-actuals-dwh]].

## `metrics_core.delivery_finance`

Tabella dei fatti: una riga per consegna (package) con economics. Granularita': package x giorno.

| Colonna | Significato |
|---|---|
| `package_date` | Data della consegna (base per il mese: `date_trunc('month', ...)`) |
| `country_name` | Mercato: UK, FR, PL, IT |
| `parent_client_id` / `parent_client_name` | Cliente parent (chiave di join e di grouping) |
| `is_invoiced` | Flag fatturato. **Filtrare sempre `= TRUE`** per gli actuals |
| `stuart_proposition` | Linea prodotto (Instant / Scheduled; da normalizzare) |
| `gross_revenue` / `gross_margin` | Ricavo e margine in **valuta locale** |
| `base_earnings`, `multiplier_earnings`, `other_earnings`, `bmg_earnings` | Componenti del ricavo corriere |
| `subcontractor_costs`, `contractor_penalties`, `employee_costs`, `total_costs` | Componenti di costo |
| `currency_conversion_rate` | Tasso per convertire in EUR |

**Conversione EUR:** ogni importo va diviso per `currency_conversion_rate` (`importo / nullif(currency_conversion_rate, 0)`). Questo e' il punto in cui nasce la divergenza con la dashboard su PL: vedi [[concetto-additional-rpo]].

## `mart_finance.inputs_client_grouping`

Tabella di mapping: assegna ogni cliente a segmento, tier, forecast group e status per anno. Granularita': cliente x geography x year (con possibili duplicati, da deduplicare via `ROW_NUMBER`).

| Colonna | Significato |
|---|---|
| `year` | Anno di validita' del mapping (join su anno del `package_date`) |
| `parent_client_id` | Chiave di join verso `delivery_finance` |
| `geography` | Mercato (join verso `country_name`) |
| `active_client_tier` | Tier interno del cliente |
| `client_forecast_group` | Gruppo di forecast (base del `client_forecast_group_adj`) |
| `client_status` | Existing / New (poi forzato a Churned per i gruppi churned) |
| `client_cohort_year` | Anno di acquisizione |

## Tabelle di forecast/budget (gsheets)

Usate per estrarre i piani mensili FC3/FC6/BP26 per paese (FR/PL/UK).

### `gsheets.raw_global_gm_projections_fc3__2026`

FC3 2026: una riga per (country, month, variable). Variabili principali: `Delivery Fee`, `Service Fee`, `VAT Commission`, `Gross Revenues`, `Total Costs`, `Gross Margin`, `Base Earnings`, `Incentive Earnings`, `Volume`.

### `gsheets.raw_global_gm_projections__2026`

BP26 e versioni successive. Filtrare su `version = 'BP26'` per il piano annuale. Contiene `Volume` mensile per paese — usato come denominatore per calcolare i tassi impliciti di coupon.

### Nota sui ratei FC3 vs FC6

FC6 non separa DF/SF per FR né Base/Incentive per paese: entrambe le decomposizioni vanno ricalcolate applicando i ratei FC3 ai totali FC6.

## Regole d'uso

- **Join** su `parent_client_id` + `country_name`/`geography` + anno.
- **Dedup** del grouping con `ROW_NUMBER() OVER (PARTITION BY parent_client_id, geography, year ...)` e `rn = 1`.
- **Mese**: `month_end_date = dateadd(day, -1, dateadd(month, 1, date_trunc('month', package_date)))` = ultimo giorno del mese.
- **Limite MCP**: la tool Superset tronca a 10.000 righe; il grouping aggregato sta ampiamente sotto.
