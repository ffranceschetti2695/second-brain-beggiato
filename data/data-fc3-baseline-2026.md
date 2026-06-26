---
title: "FC3 Baseline 2026 (Stuart)"
summary: "Baseline forecast FC3 (export marzo 2026) a livello cliente per il flusso slide mensile: struttura, segmenti e colonna maggio dettagliata."
tags: [data, type/reference, stuart, fc3]
status: active
created: 2026-06-25
updated: 2026-06-25
related: ["[[entity-stuart]]", "[[concetto-rpo-cpo-slo]]", "[[progetto-france-task-force]]"]
---

# FC3 Baseline 2026

Baseline di forecast usata come pietra di paragone nelle slide di Company Performance mensili di [[entity-stuart]] (Actual vs FC3), scomposte tramite il [[concetto-bridge-waterfall]]. Le metriche seguono la logica [[concetto-rpo-cpo-slo]] (Volume, GR, GM, RPO, CPO).

## Fonte canonica

- **File:** `Revenue to GM - FC3 - March 2026 - Export to DWH`
- **Granularità:** cliente × mese (Jan–Dec 2026), metriche: Volume, Gross Revenue, RPO, Total Costs, CPO, GM, GM-del.
- **Uso nel flusso:** ogni mese il processo rilegge la colonna del mese corrente da questa fonte. Questa nota congela la colonna di maggio (mese di lavoro attuale) + la struttura; per gli altri mesi si ripesca dalla fonte.

## Totali FC3 maggio 2026 (controllo)

| KPI | FC3 maggio |
|---|---|
| Volume | 756,105 |
| Gross Revenue | €4,443,217 |
| GM | €1,069,957 |
| GM% | 24.1% |

## Struttura clienti / segmenti

- **Tesco** (UK, standalone)
- **UK Top Accounts:** Zapp, Pizza Hut, Iceland (+ TradeKart, marginale)
- **FR Top Accounts:** Carrefour, Sushi Shop, Franprix, SYSTEME-U (+ Côté Sushi = 0)
- **PL Top Accounts:** AmRest, Just Eat (JET) — (JET-DE = 0)
- **Mid-Market:** UK/FR/PL — Existing + New MM
- **SMB:** UK/FR/PL — Existing + New SMB
- **Pipeline:** suddivisa in **ENT Pipeline**, **SMB Pipeline**, **MM Pipeline** (per area UK/FR/PL e Global)

> ⚠️ Grouping definitivo dei bridge = da tab "Graphs" della Stuart Metrics Dashboard (Step 2). La struttura sopra è quella della fonte FC3, non necessariamente identica alle barre del waterfall.

## FC3 maggio 2026 — livello cliente (Volume / GR / GM)

### UK
| Cliente | Volume | Gross Revenue | GM |
|---|---|---|---|
| Tesco | 474,459 | €2,341,386 | €366,313 |
| Zapp | 55,969 | €459,505 | €145,819 |
| Pizza Hut | 4,429 | €26,928 | €8,760 |
| Iceland | 7,529 | €69,342 | €23,666 |
| TradeKart | 443 | €4,496 | €1,435 |
| UK Existing MM | 13,457 | €115,730 | €37,128 |
| UK New MM | 1,058 | €8,316 | €2,676 |
| UK Existing SMB | 2,239 | €25,108 | €7,992 |
| UK New SMB | 808 | €10,895 | €3,453 |

### FR
| Cliente | Volume | Gross Revenue | GM |
|---|---|---|---|
| Carrefour | 17,186 | €167,183 | €46,022 |
| Sushi Shop | 16,000 | €99,083 | €29,483 |
| Côté Sushi | 0 | €0 | €0 |
| Franprix | 2,500 | €23,750 | €6,750 |
| SYSTEME-U | 900 | €9,450 | €279 |
| FR Existing MM | 18,170 | €173,771 | €69,592 |
| FR New MM | 858 | €6,385 | €1,932 |
| FR Existing SMB | 16,367 | €237,051 | €106,115 |
| FR New SMB | 3,329 | €54,154 | €22,495 |

### PL
| Cliente | Volume | Gross Revenue | GM |
|---|---|---|---|
| AmRest | 71,300 | €311,268 | €104,900 |
| Just Eat (JET) | 38,010 | €180,548 | €42,331 |
| PL Existing MM | 300 | €1,350 | €464 |
| PL Existing SMB | 368 | €1,518 | €264 |
| PL New SMB | 51 | €199 | €26 |

### Pipeline (Global)
| Voce | Volume | Gross Revenue | GM |
|---|---|---|---|
| ENT Pipeline | 2,000 | €18,140 | €8,300 |
| SMB Pipeline | 8,375 | €97,661 | €33,763 |
| MM Pipeline | 0 | €0 | €0 |
| **Totale Pipeline** | **10,375** | **€115,801** | **€42,063** |

Ripartizione pipeline per area (maggio): UK €28,171 GR (ENT €18,140 + SMB €10,031); FR €87,630 GR (tutto SMB Pipeline); PL €0 (parte da giugno).

---

## Logica di grouping dei bridge (validata 2026-06-25 contro le formule del tab Graphs)

Il waterfall ha **7 barre**. Membership e regole, dedotte e verificate riga per riga dalle formule (`SUMPRODUCT` su Topline Figures) e dai tre bridge ufficiali:

| Barra | Membership |
|---|---|
| Tesco | Tesco |
| UK Top Accounts | Zapp + Pizza Hut + Iceland |
| FR Top Accounts | Carrefour + Sushi Shop + **Intermarché** + SYSTEME-U |
| PL Top Accounts | AmRest + Just Eat |
| Mid-Market | UK MM (+TradeKart) · FR MM (+Franprix +Côté **−Intermarché**) · PL MM |
| SMB | UK SMB · FR SMB · PL SMB |
| Pipeline ENT | **solo ENT Pipeline** |

**Regole chiave (non ovvie):**
1. **Pipeline split.** La barra "Pipeline ENT" contiene SOLO la ENT Pipeline. La **SMB Pipeline va dentro SMB**, la **MM Pipeline va dentro Mid-Market** (meccanismo `−Pipeline!C18 / −Pipeline!D18` che le rimette nei rispettivi segmenti). A maggio: SMB Pipeline €97,661 GR è il grosso del miss SMB; MM Pipeline = 0.
2. **TradeKart → UK Mid-Market** (hardcoded nella formula UK MM).
3. **Franprix + Côté Sushi → FR Mid-Market.**
4. **Intermarché è "bundled" dentro FR Existing MM** nel dato sorgente: viene estratto verso FR Top Accounts e nettato da FR MM (`−F41`). Valori FC3 di Intermarché estratti per quadratura: **Volume 1.170 · GR €12.271 · GM €1.170**. (FR Existing MM "puro" GR ≈ €155.500.)
5. **Fonti:** Actuals = **query DWH** (`metrics_core.delivery_finance`, vedi sezione "Actuals — fonte canonica DWH" sotto); baseline confronto = **FC3** (sostituisce la colonna Budget/BP).

> ⚠️ **Scostamento di versione FC3 noto:** il bridge ufficiale GM parte da FC3 GM totale **€1.068.978**, mentre questo export (marzo) riporta **€1.069.957** — differenza €979 tutta su Tesco GM (dashboard €365.334 vs export €366.313). Per il deck usare i valori della **dashboard**.

## Actuals — fonte canonica DWH (validata 2026-06-25)

Gli **actuals si rileggono sempre dal DWH** via query su `metrics_core.delivery_finance` (join con `mart_finance.inputs_client_grouping`, dedup `ROW_NUMBER` per parent_client × country × year, filtro `is_invoiced = TRUE`). La query restituisce per mese: `client_forecast_group_adj` × country × status × proposition con Volume / GR / GM in EUR. **Non si usano più i valori della sheet dashboard**: il DWH è la fonte unica e ripetibile.

**Validazione maggio 2026 vs tab Graphs della dashboard:**
- **Volume**: 16/16 gruppi identici all'unità (totale 696.055). Il grouping è confermato al 100%.
- **GR/GM**: 14/16 gruppi identici all'euro. Divergono solo **PL AmRest** e **PL JET** (ricavo convertito in EUR diverso = *additional RPO* lato dashboard). Lo scarto **non è fisso** (a maggio netto −€4.944 su GR/GM, ma varia ogni mese): si usano sempre i valori **DWH**.

**Mapping `client_forecast_group_adj` → barra del waterfall** (lato actuals):

| Gruppo DWH | Barra |
|---|---|
| Tesco - UK | Tesco |
| Zapp / Pizza Hut / Iceland - UK | UK Top Accounts |
| Carrefour / Sushi Shop / Intermarché / SYSTEME-U - FR | FR Top Accounts |
| AmRest / Just Eat (JET) - PL | PL Top Accounts |
| UK MM (+TradeKart) · FR MM (+Franprix +Côté) · PL MM · Churned | Mid-Market |
| UK SMB · FR SMB · PL SMB | SMB |
| (pipeline: 0 negli actuals) | Pipeline ENT |

> Côté Sushi, Franprix, TradeKart, Carrefour: nel grouping DWH le prime due confluiscono in FR MM e TradeKart in UK MM già a monte; Carrefour resta `Client_FR Carrefour` (→ FR Top). Le voci `*-Churned` cadono dentro MM del rispettivo paese.

## Bridge maggio 2026 verificati (Actual DWH − FC3) — output canonico

> Actuals = DWH. Volume coincide con la dashboard; su GR/GM la barra **PL Top** assorbe l'additional RPO (~€5k a maggio), quindi differisce leggermente dal waterfall dashboard.

**Volume (k):** FC3 756 → Actual 696 (−60). Tesco −37 · SMB −5,8 · PL Top −4,7 · MM −4,1 · UK Top −3,9 · FR Top −2,6 · Pipeline ENT −2,0.

**GR (€k):** FC3 4.443 → Actual 4.281 (−162). Tesco +72 · UK Top −24 · FR Top −40 · PL Top −20 · MM −64 · SMB −68 · Pipeline ENT −18.

**GM (€k):** FC3 1.069 → Actual 899 (−170). Tesco −25 · UK Top −37 · FR Top −30 · PL Top ≈0 · MM −33 · SMB −37 · Pipeline ENT −8.

Storia del mese vs FC3: miss diffuso (GR −3,7%, GM −16%), guidato da **SMB** e **Mid-Market** (non-materializzazione pipeline SMB + Franprix/MM sotto piano) e da margine eroso; **Tesco** unico forte positivo su GR.
