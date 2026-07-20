---
description: Rebuild the monthly Budget Plan CSV view (RPO/CPO/GM del, Volume, GM, GR, Total Costs, EBITDA, Contribution Margin by FR/UK/PL/Global) blending BP26, FC3 and the latest FC forecast, ready to paste into the tracker sheet
allowed-tools:
  - Bash
  - Read
  - Write
---

You are rebuilding Francesco's monthly Budget Plan view as a CSV he can paste straight into Google Sheets. This skill is triggered by `/budget-plan-view` or phrases like "rebuild the budget plan view", "update the budget plan CSV with the latest FC", "same as last time but with FC7/FC8/...".

Note: the source sheet's own title cell literally reads "Budget FC9 - BP26" — that's just this view's internal label inside the tracker file (unrelated to which FC cycle is actually being blended in), so don't read meaning into the "FC9" part or repeat it back to Francesco as if it were the forecast cycle in use. Refer to this as "the Budget Plan view" everywhere else.

## What this view is

A monthly (Jan-Dec) table blending three vintages of the same P&L metrics:
- **Jan-Apr**: `BP26` (the original 2026 budget, doesn't change)
- **A middle stretch**: `FC3` (an older forecast snapshot, baseline for months not yet covered by a newer FC file)
- **From a cutover month onward**: the **latest FC cycle** Francesco has downloaded (FC6, FC7, FC8...), which should replace FC3 for those months

The source of truth for the BP26/FC3 base is the **`Plan` sheet** inside `OPS - GM Tracker*.xlsx` (any file matching that name pattern in `~/Downloads/`) — its row 3 tags each month `BP26` or `FC3`. Never hand-derive BP26/FC3 numbers from other sheets; this Plan sheet is the canonical layout and column order.

The source of truth for the latest FC replacement data is the **`Revenue to GM - FC<N> - <Month> <Year>.xlsx`** file in `~/Downloads/` — pick whichever has the **highest N** and the most recent download timestamp if several exist. Its filename tells you the cutover: `FC<N> - <Month> <Year>` means actuals/baseline run through `<Month> <Year>`, so the FC data should replace FC3 starting the **month after** that (e.g. "FC6 - June 2026" → replace from July onward).

## Step 1 — Locate the files

```
ls -lt ~/Downloads | grep -i "GM Tracker"
ls -lt ~/Downloads | grep -i "Revenue to GM"
```

Pick the most recent GM Tracker file and the highest-numbered/most recent Revenue to GM FC file. If several FC files are equally recent, ask Francesco which one to use rather than guessing.

## Step 2 — Read the Plan sheet (BP26/FC3 base)

Open `OPS - GM Tracker*.xlsx` with openpyxl (`data_only=True`), sheet `Plan`. Columns H:S = Jan-Dec 2026. Row 2 = month-end dates, row 3 = period tag (`BP26`/`FC3`) per column.

Row map (confirmed against the screenshot Francesco provided — don't re-derive, just re-read in case row numbers shift after edits, by searching for the label in column B/C):

| Rows | Market | Metric |
|---|---|---|
| 4-6 | FR | RPO, CPO, GM del |
| 7-9 | UK | RPO, CPO, GM del |
| 10-12 | PL | RPO, CPO, GM del |
| 14-16 | "no DE" / Global | RPO, CPO, GM del |
| 18-20 | FR, UK, PL | Volume |
| 22 | GLOBAL | Volume |
| 24-26 | FR, UK, PL | GM |
| 28 | GLOBAL | GM |
| 30-32 | FR, UK, PL | GR |
| 34-36 | FR, UK, PL | Total Costs |
| 38 | GLOBAL | GR |
| 40 | GLOBAL | EBITDA |
| 42 | GLOBAL | Contribution Margin |

Note: in the Plan sheet, **CPO is stored as a positive number** (magnitude, not signed cost) — keep that convention in the output.

## Step 3 — Read the FC<N> file for the cutover months

Open the `Revenue to GM - FC<N>...xlsx` file, sheets `FR - Revenue to GM Figures`, `UK - Revenue to GM Figures`, `PL - Revenue to GM Figures`, and `Topline Figures - Global`. In each country sheet, the `Country View` block (rows ~9-15, one row per Client Name = country) holds, in this exact order: Volume, Gross Revenue, RPO, Total Costs, CPO, GM, GM-del — columns Jan-Dec run left to right starting right after the "Variable Name" column. `Topline Figures - Global` has the same 7 metrics as standalone rows (Volume, Gross Revenue, RPO, Total Costs, CPO, GM, GM-del) already summed across markets — use it directly for the Global rows and for the "no DE" Global RPO/CPO/GM del rows (they're the same numbers, since this file has no DE market yet).

**Sign fix**: this file stores **CPO as negative** — take `abs()` before writing it out, to match the Plan sheet's positive convention. Total Costs stays negative in both sources (no fix needed there).

**No EBITDA / Contribution Margin in the FC file** — those two GLOBAL rows have no FC<N> equivalent. Leave them as FC3 for the cutover months and say so explicitly in your reply; don't invent a number.

## Step 4 — Blend and determine the cutover column

From the FC filename, compute the cutover month (month after the file's `<Month> <Year>`). For columns before the cutover, keep the Plan sheet value and its original BP26/FC3 tag. From the cutover month onward, replace the value with the FC<N> figure (from Step 3) and tag that column `FC<N>` in the period row.

## Step 5 — Write the CSV in the exact copy-paste layout

Two label columns (`Market`, `Metric`), then one column per month. Round all values to 2 decimals. Match this exact row/blank-row structure (confirmed against Francesco's screenshot — preserve every blank row, they matter for how it pastes into the sheet). Title the first cell "Budget Plan" (not the source sheet's internal "Budget FC9 - BP26" label):

```
Budget Plan,,Jan 26,Feb 26,...,Dec 26
,,BP26,BP26,BP26,BP26,FC3,FC3,FC<N>,FC<N>,FC<N>,FC<N>,FC<N>,FC<N>
<blank row>
FR,RPO,...
FR,CPO,...
FR,GM del,...
UK,RPO,...
UK,CPO,...
UK,GM del,...
PL,RPO,...
PL,CPO,...
PL,GM del,...
<blank row>
DE,Global RPO,...
DE,Global CPO,...
DE,Global GM del,...
<blank row>
FR,Volume,...
UK,Volume,...
PL,Volume,...
<blank row>
GLOBAL,Volume,...
<blank row>
FR,GM,...
UK,GM,...
PL,GM,...
<blank row>
GLOBAL,GM,...
<blank row>
FR,GR,...
UK,GR,...
PL,GR,...
<blank row>
FR,Total Costs,...
UK,Total Costs,...
PL,Total Costs,...
<blank row>
GLOBAL,GR,...
<blank row>
GLOBAL,EBITDA,...
<blank row>
GLOBAL,Contribution Margin,...
```

Save it to `~/Desktop/budget-plan-monthly-<year>.csv` (don't put it in the vault's `data/` folder — per this vault's note-creation rules, this is a re-derivable numeric table, not standalone knowledge, so it stays a plain file outside the vault).

## Step 6 — Report back

Tell Francesco: which GM Tracker and FC<N> files you used, the cutover month, that CPO sign was normalized, and that EBITDA/Contribution Margin remain FC3 (no FC<N> source exists for them). Reply in the language of his latest message.
