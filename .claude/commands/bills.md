---
description: Monthly recurring-bill tracker — pulls rent, gym, phone, electricity, gas and water bills from the gmail-account2 inbox, appends to a history CSV, and prints a category-by-month pivot table
allowed-tools:
  - Bash
  - Read
  - Write
  - mcp__gmail-account2__search_emails
  - mcp__gmail-account2__read_email
---

You are producing a monthly recurring-bill report for Francesco. Execute the steps below **in order**.

## Trigger

This skill is triggered by `/bills` or natural phrases like "run the bills skill", "update my bills", "how much am I paying in bills".

Reply in the same language as Francesco's current/latest message — never default to Italian, and ignore the language of this skill file or of email content. This follows the global language-mirroring rule in CLAUDE.md.

## Data model

History lives in `~/Documents/Bank Accounts/bills-history.csv`, one row per bill, columns:
`date,category,amount,period_start,period_end,period_days,month,notes`

`category` is one of: `rent`, `electricity`, `gas`, `water`, `movistar`, `fitness_park`.
`month` is `YYYY-MM` (the calendar month the bill/charge landed in — cash basis, not the consumption period).
`amount` can be blank if a figure was genuinely unrecoverable — never guess a number, leave it blank and explain why in `notes`.

## Step 1 — Determine current month and read existing history

Use Bash to get today's date. Compute `CURRENT_MONTH` as `YYYY-MM`.

Read `~/Documents/Bank Accounts/bills-history.csv`. If it doesn't exist, create it with just the header row and treat every "last date" below as absent (search from the earliest date you have data for, e.g. 2026/1/1).

**Important — search from last-known data, not from the start of the current month.** If `/bills` doesn't get run every single month, a "since start of this month" search would silently skip any month with no run at all. Instead, for each source below, find the most recent `date` already in the CSV for that category (or category pair for Endesa) and search `after:<that date>`. This guarantees any gap — one skipped month or six — gets backfilled in a single run, since Gmail search naturally returns everything after that date up to now, however many invoices that is.

## Step 2 — Fixed costs (rent, gym)

Rent (€1,340, paid on the 1st) and Fitness Park (€27/month, weekly auto-debit) are fixed constants — no email exists for rent, and the gym amount doesn't need re-verification against a PDF each month.

Find the most recent `month` value already recorded for `rent` (same for `fitness_park` — they should always move together, but check independently in case one somehow got out of sync). Starting from the month *after* that (or from the earliest month with any data in the CSV, if there's no rent/fitness_park row at all yet), append one row for **every** calendar month up to and including `CURRENT_MONTH` that doesn't already have one:
- `<1st of that month>,rent,1340.00,,,,<that month>,fixed monthly assumption`
- `<1st of that month>,fitness_park,27.00,,,,<that month>,fixed weekly auto-debit`

This backfills any skipped months in one pass rather than only ever adding the current one.

## Step 3 — Movistar (phone)

Find the most recent `date` recorded for `movistar` in the CSV. Search `mcp__gmail-account2__search_emails` with query `from:email.movistar.es "factura" after:<that date, YYYY/M/D>` (or `after:2026/1/1` if there's no prior Movistar row at all).

For each result not already in the CSV (match on invoice date), `read_email` and extract the "Total a pagar" figure (plain text, e.g. "40,00 €"). Append a row: `date,movistar,amount,,,,<month of that invoice date>,`.

If no new invoice is found, leave it out — don't invent a row. Movistar bills ~monthly around the 21st-23rd, so finding nothing new for the current month before that date each month is expected, not an error.

## Step 4 — Aigües de Barcelona (water)

Find the most recent `date` recorded for `water` in the CSV. Search `from:info.aiguesdebarcelona.cat "NUEVA FACTURA" after:<that date>` (or `after:2026/1/1` if none yet).

For each new result, `read_email` and extract the "Importe:" line (plain text, e.g. "73,71 €") and the "Fecha de emision de la factura" date. Append: `date,water,amount,,,,<month of that invoice date>,invoice dated <date>, consumo <X> m3`.

Water bills bimonthly — most searches will turn up nothing new. That's expected, not an error.

## Step 5 — Endesa (electricity + gas) — image OCR required

Find the most recent `date` recorded across *both* `electricity` and `gas` rows in the CSV (use the older of the two, so neither utility's next bill gets missed). Search `from:factura.endesaclientes.com after:<that date>` (or `after:2026/1/1` if neither has any rows yet).

For each new result not already in the CSV (match on the `Ref.` in the subject):
1. `read_email` to get the HTML body.
2. Determine electricity ("factura de luz") vs gas ("factura de gas") from the body text.
3. Extract the `Período del X al Y` and `Factura de N días` plain-text lines.
4. Find the `<img>` tag whose `src` starts with `https://www.endesaclientes.com/neolapi-b2c-avisos-rest/invoices/graficaBillConcepts?` — this renders a donut chart containing the € total as pixels, not text.
5. Download it: `curl -sL "<url>" -o /tmp/endesa_<id>.png` (or the session scratchpad dir if `/tmp` isn't writable).
6. Use the Read tool to view the downloaded PNG and read the € figure printed in the center of the donut (large font, e.g. "41,56€", with a "X,XX€ de coste medio diario" caption below).
7. If the image comes back blank/unreadable after one retry, do NOT guess — append the row with `amount` blank and a note: `"amount unrecoverable - chart image blank/unreadable"`.

Append: `date,electricity|gas,amount,period_start,period_end,period_days,CURRENT_MONTH,ref <Ref>`.

Also flag (but handle the same way) any invoice whose `Ref.` starts with `P26COR` or similar — these are correction/regularization docs, not normal consumption bills. Note this in the `notes` column so it's visible in the report, but still include it in the totals (it's real money moving).

## Step 6 — Save history

Write the updated CSV back to `~/Documents/Bank Accounts/bills-history.csv`, preserving all prior rows plus any newly appended ones. Never delete or overwrite existing rows — only append.

## Step 7 — Build and print the pivot table

Read the full CSV to build the report — never re-fetch Gmail for months already in the CSV, that's the whole point of persisting history (keeps token usage low: only the current month gets searched live, everything before it is a pure CSV read).

**7a — Quick summary table first.** Four rows, columns = each `YYYY-MM` present in the data:
- `Bills` = sum of `electricity + gas + water + movistar` for that month (everything variable/invoice-based)
- `Rent` = the `rent` row for that month
- `Fitness Park` = the `fitness_park` row for that month
- `TOTAL` = `Bills + Rent + Fitness Park`

This `TOTAL` row must equal that month's `TOTAL` in the detailed table below (7b) exactly — if it doesn't, there's a bug, so double check the arithmetic before printing. Print this table before the detailed one.

**7b — Detailed pivot table.** Rows = category, columns = each `YYYY-MM` present in the data (chronological), plus two average columns.

**Row order (fixed, don't resort):** `rent`, `electricity`, `gas`, `water`, `movistar`, `fitness_park`, then a `TOTAL` row.

For each category row, sum all amounts landing in that month (there can be multiple electricity rows in one month — sum them; a blank/unrecoverable amount contributes 0 to the sum but must NOT be silently absorbed into the total — call it out in the flagged list below the table, not with an inline symbol in the table itself. Keep the table clean, no emoji/warning markers in cells.)

**Two average columns:**
- **Avg incl. €0 months** — sum of all amounts for that category ÷ number of calendar months shown (including months with no bill).
- **Avg, bill-months only** — sum ÷ number of months that actually had at least one bill for that category.

For `rent` and `fitness_park` these two columns are identical (every month has one). Explicitly note in the output that the "bill-months only" average is not a monthly budget figure for bimonthly categories (gas, water) — it answers "how big is a typical bill", not "what do I pay per month."

The current/most-recent month is often partial (bills not yet issued for categories that haven't billed yet this cycle) — label its column "(partial)" and don't include it in either average.

Print the table in chat only. Don't write it to a separate file or create a vault note — this is numeric data that's fully recoverable from the CSV, not standalone knowledge (per this vault's note-creation threshold).

Flag clearly, right after the detailed table:
- Any row/cell with an unrecoverable amount
- Any correction/regularization doc included in the totals
- Which categories are still pending for the partial current month

## Step 8 — Short commentary

Close with a brief (3-5 sentence) read on the most recently *complete* month (not the partial current one): how it compares to the running average (over/under, by how much), any notable trajectory across the visible months (e.g. bimonthly bills landing together causing a spike), and a forward-looking flag if there's a seasonal reason to expect a change (e.g. summer AC usage pushing electricity up, winter heating pushing gas up). Keep this grounded in the actual numbers in the table, not generic advice.
