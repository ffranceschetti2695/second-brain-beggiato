---
title: "Query Actuals DWH (Performance Stuart)"
summary: "Query SQL canonica per estrarre gli actuals mensili (Volume, GR, GM) dal DWH Stuart, con grouping cliente gia' applicato."
tags: [code, stuart, sql, dwh, reporting]
status: active
created: 2026-06-25
updated: 2026-06-25
related: ["[[doc-dwh-finance-schema]]", "[[doc-flusso-performance-mensile]]", "[[data-stuart-segmentazione-clienti]]", "[[entity-stuart]]"]
---

# Query Actuals DWH

Query canonica degli **actuals** per le slide di performance mensili di [[entity-stuart]]. Gira su Redshift via Superset (MCP `superset-mcp_4_Execute_SQL_query`). Restituisce, per il mese richiesto, le metriche [[concetto-rpo-cpo-slo]] aggregate per `client_forecast_group_adj` x country x status x proposition. Schema delle tabelle in [[doc-dwh-finance-schema]].

> Validata 2026-06-25: Volume coincide al 100% con la dashboard; GR/GM divergono solo su PL per [[concetto-additional-rpo]]. Si usano sempre i valori DWH.

## Logica

- **`client_grouping` (CTE):** dedup di `mart_finance.inputs_client_grouping` con `ROW_NUMBER` per `parent_client_id x geography x year` (tiene una riga per cliente/anno).
- **`df_enriched` (CTE):** join con `metrics_core.delivery_finance` su `parent_client_id + country_name + year`. Applica:
  - `client_forecast_group_adj`: estrae Intermarche e SYSTEME-U, mappa i tier in MM, classifica i churned per paese.
  - `client_status_adj`: forza "Churned" sui gruppi churned.
  - `stuart_proposition`: normalizza in Instant / Scheduled.
  - Conversione in EUR: ogni importo `/ nullif(currency_conversion_rate, 0)`.
- **Filtro:** `is_invoiced = TRUE`.
- **Per il mese:** filtrare `month_end_date = '<YYYY-MM-31>'` (ultimo giorno del mese) oppure rimuovere il filtro per tutti i mesi.

## SQL

```sql
with client_grouping as (
    select year, parent_client_id, client_cohort_year,
           active_client_tier as internal_tier,
           client_forecast_group, client_status, geography as country
    from (
        select year, parent_client_id, client_cohort_year, active_client_tier,
               client_forecast_group, client_status, geography,
               ROW_NUMBER() OVER (
                   PARTITION BY parent_client_id, geography, year
                   ORDER BY active_client_tier, client_forecast_group
               ) as rn
        from mart_finance.inputs_client_grouping
    )
    where rn = 1
),
df_enriched as (
    select
        dateadd(day, -1, dateadd(month, 1, date_trunc('month', df.package_date)))::date as month_end_date,
        df.country_name, df.parent_client_id, df.parent_client_name,
        cg.client_cohort_year, cg.internal_tier, cg.client_forecast_group, cg.client_status,
        case
            when cg.client_forecast_group = 'Intermarché - FR' or df.parent_client_name ilike 'Intermarch%' then 'Intermarché - FR'
            when cg.client_forecast_group = 'SYSTEME-U - FR' or df.parent_client_name ilike 'SYSTEME-U%' then 'SYSTEME-U - FR'
            when cg.client_forecast_group in ('FR Existing Tier 3', 'FR Existing Tier 4', 'Interflora - FR') then 'FR - Existing MM'
            when cg.client_forecast_group in ('UK Existing Tier 3', 'UK Existing Tier 4', 'Papa John''s - UK') then 'UK - Existing MM'
            when cg.client_forecast_group in ('PL Existing Tier 3', 'PL Existing Tier 4') then 'PL - Existing MM'
            when cg.client_forecast_group in ('FR New Tier 3', 'FR New Tier 4') then 'FR - New MM'
            when cg.client_forecast_group in ('UK New Tier 3', 'UK New Tier 4') then 'UK - New MM'
            when cg.client_forecast_group in ('PL New Tier 3', 'PL New Tier 4') then 'PL - New MM'
            when cg.client_forecast_group in ('Apple - GL', 'Coop Food - UK', 'Just Eat - UK', 'Getir - UK', 'Sainsbury''s - UK') then 'UK - Churned'
            when cg.client_forecast_group in ('Epicery - FR', 'O''Tacos - FR', 'Just Eat - FR', 'Burger King - FR', 'Mcdonald''s - FR') then 'FR - Churned'
            when cg.client_forecast_group in ('Dominos - PL') then 'PL - Churned'
            when df.country_name = 'IT' then 'IT - Churned'
            else cg.client_forecast_group
        end as client_forecast_group_adj,
        case
            when case
                when cg.client_forecast_group in ('Apple - GL', 'Coop Food - UK', 'Just Eat - UK', 'Getir - UK', 'Sainsbury''s - UK') then 'UK - Churned'
                when cg.client_forecast_group in ('Epicery - FR', 'O''Tacos - FR', 'Just Eat - FR', 'Burger King - FR', 'Mcdonald''s - FR') then 'FR - Churned'
                when cg.client_forecast_group in ('Dominos - PL') then 'PL - Churned'
                when df.country_name = 'IT' then 'IT - Churned'
                else cg.client_forecast_group
            end in ('UK - Churned', 'FR - Churned', 'PL - Churned', 'IT - Churned')
            then 'Churned'
            else cg.client_status
        end as client_status_adj,
        case
            when df.stuart_proposition is null or trim(df.stuart_proposition) = '' then 'Instant'
            when df.stuart_proposition ilike '%sched%' then 'Scheduled'
            when df.stuart_proposition ilike '%instant%' then 'Instant'
            else df.stuart_proposition
        end as stuart_proposition,
        df.is_invoiced,
        df.base_earnings / nullif(df.currency_conversion_rate, 0) as base_earnings_eur,
        df.multiplier_earnings / nullif(df.currency_conversion_rate, 0) as multiplier_earnings_eur,
        df.other_earnings / nullif(df.currency_conversion_rate, 0) as other_earnings_eur,
        df.bmg_earnings / nullif(df.currency_conversion_rate, 0) as bmg_earnings_eur,
        df.subcontractor_costs / nullif(df.currency_conversion_rate, 0) as subcontractor_costs_eur,
        df.contractor_penalties / nullif(df.currency_conversion_rate, 0) as contractor_penalties_eur,
        df.employee_costs / nullif(df.currency_conversion_rate, 0) as employee_costs_eur,
        df.total_costs / nullif(df.currency_conversion_rate, 0) as total_costs_eur,
        df.gross_revenue / nullif(df.currency_conversion_rate, 0) as gr_eur,
        df.gross_margin / nullif(df.currency_conversion_rate, 0) as gm_eur
    from metrics_core.delivery_finance df
    left join client_grouping cg
        on df.parent_client_id = cg.parent_client_id
        and df.country_name = cg.country
        and EXTRACT(YEAR FROM df.package_date) = cg.year
)
select
    month_end_date, country_name, client_forecast_group_adj, client_status_adj,
    sum(case when is_invoiced then 1 else 0 end) as total_invoiced_volume,
    sum(base_earnings_eur) as base_earnings,
    sum(multiplier_earnings_eur) as multiplier_earnings,
    sum(other_earnings_eur) as other_earnings,
    sum(bmg_earnings_eur) as bmg_earnings,
    sum(subcontractor_costs_eur) as subcontractor_costs,
    sum(contractor_penalties_eur) as contractor_penalties,
    sum(employee_costs_eur) as employee_costs,
    sum(total_costs_eur) as total_costs,
    sum(gr_eur) as gr_eur,
    sum(gm_eur) as gm_eur,
    stuart_proposition, is_invoiced
from df_enriched
where is_invoiced = TRUE
  and month_end_date = '2026-05-31'   -- <- cambiare mese qui
group by month_end_date, country_name, client_forecast_group_adj, client_status_adj, is_invoiced, stuart_proposition
order by 1, 2, 3;
```

## Controllo di quadratura

Dopo l'estrazione, il **volume totale** deve coincidere con la dashboard all'unita' (a maggio 2026: 696.055, di cui Tesco 437.532). Se il volume non torna, il problema e' nel grouping o nel mese, non nei dati.
