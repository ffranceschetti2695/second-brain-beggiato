---
name: stuart-financial-update-weekly
description: Generate Stuart's weekly Financial Update — the Friday "pre-weekend check" Slack post that goes to the C-level operations channel covering UK, FR and PL. Reads the GM OPS Tracker spreadsheet, pulls the in-progress week's volume/RPO/CPO/GM split and the month-to-date landing per market, and composes the message in the exact structure with figures framed vs BP'26. Use this skill whenever Francesco asks for a "financial update", "weekly financial update", "Friday financial update", "pre-weekend check", "weekly Ops update", or any variant asking for the recurring Friday Slack post on weekly GM impact and monthly landing. Also use proactively when Francesco mentions it's Friday and he needs to draft the weekend-check message, or when he says "do the same as last week" in the context of weekly ops communications. Do NOT use for monthly scorecards (use stuart-monthly-ops-scorecard or stuart-monthly-revenue-scorecard) or MBR recaps (use stuart-exec-summary).
---

# Stuart Weekly Financial Update

Produces the Friday "pre-weekend check" Slack post sent to Stuart's C-level operations channel. Audience: ExCo + Ops leadership — finance-literate, scan-only, want the bottom line up top with a clean three-way split and the monthly landing per market. Exactly three lines are bold: the title, the "Weekly — ..." header, and the "Monthly landing — ..." header. Everything else is plain text, with a bulleted ("•") list for the per-market monthly breakdown. Confirmed against Francesco's actual sent messages in #operations (most recently 2026-06-26).

**Bold syntax depends on the layer**: when composing the message string passed into the Slack MCP tools (`slack_send_message`, `slack_send_message_draft`), use standard markdown `**double asterisks**` — those tools parse standard markdown and convert it to Slack's native mrkdwn on send/draft. Single asterisks (`*text*`) in that same tool call render as *italics*, not bold — confirmed by testing (2026-07-17). The single-asterisk form is what Slack's own mrkdwn looks like once already rendered/stored (e.g. what you see reading raw text back via `slack_search_public`), but it is NOT what to type into these tool calls.

## When this triggers

Typical phrasings:
- "Do the weekly financial update"
- "Draft the Friday update / pre-weekend check"
- "Weekly financial update for this week"
- "Weekly Ops update vs BP"
- Francesco says "same as last week" in a Friday/weekly context

**Always confirm two inputs with Francesco before drafting — do not start reading the tracker until both are confirmed:**

1. **Focus week** — propose the in-progress ISO week as the default (e.g. "W26, Jun 22-28") and ask him to confirm or override.
2. **Comparison base** — propose FC3 as the default and ask him to confirm or override (common alternatives: BP'26, FC2).

Use the `ask_user_input_v0` elicitation tool with two separate questions, or ask both in a single message and wait for the answer.

## Inputs & defaults

| Input | Default | Notes |
|---|---|---|
| Focus week | Current ISO week, **confirmed by Francesco** | The Weekly tab usually shows it as a "Forecast" column |
| Source file | `Claude.ia \| GM - OPS Tracker` (fileId `1DWTP4_1GyjzGxPhOBzBZE-3tsWaKwKHadMLaJsHZrkc`) | This is the IMPORTRANGE mirror of the DLP-flagged original. Always remind Francesco it's the IMPORTRANGE version when reading. |
| Markets | UK, FR, PL | In this order |
| Comparison base | **FC3** (confirm with Francesco — common alternatives: BP'26, FC2) | Used in the header: "(all figures vs FC3)" or whichever base is confirmed |

## The orchestration flow

Do NOT use `read_file_content` directly — it only returns the Weekly tab and silently omits the Monthly tab, making the monthly landing paragraph impossible to produce. Do NOT load the base64 XLSX blob into the main context — it is hundreds of thousands of tokens and will saturate the window.

**Instead: spawn a single subagent that handles the entire data extraction.** The subagent absorbs the base64 cost; the main context receives only a compact JSON with the ~20 values needed.

### Step 1 — Spawn the data-extraction subagent

Launch a subagent with this exact task:

> Download the file with fileId `1DWTP4_1GyjzGxPhOBzBZE-3tsWaKwKHadMLaJsHZrkc` as XLSX (exportMimeType `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`). Decode the base64 response and save to a temp path. Then run Python with openpyxl to extract the following values and return them as a JSON object — nothing else, no prose:
>
> From tab "GM Tracker - Weekly", focus-week column (locate by matching row 10 = ISO week number `<W26>`, or row 9 = Monday `<2026-06-22>`):
> - weekly.global.gm_impact (row 37)
> - weekly.global.rpo_effect (row 33)
> - weekly.global.cpo_effect (row 34)
> - weekly.global.vol_effect (row 36)
> - weekly.uk.delta_vol (row 54), weekly.uk.gm_impact (row 78), weekly.uk.rpo_effect (row 74), weekly.uk.cpo_effect (row 75), weekly.uk.vol_effect (row 77)
> - weekly.fr.delta_vol (row 95), weekly.fr.gm_impact (row 119), weekly.fr.rpo_effect (row 115), weekly.fr.cpo_effect (row 116), weekly.fr.vol_effect (row 118)
> - weekly.pl.delta_vol (row 136), weekly.pl.gm_impact (row 160), weekly.pl.rpo_effect (row 156), weekly.pl.cpo_effect (row 157), weekly.pl.vol_effect (row 159)
>
> From tab "GM Tracker - Monthly", LEFT block only (cols 8-11):
> - monthly.tracked_month (row 6, col 3 — the end-of-month date)
> - monthly.global.delta_vol (row 9, col 11 — packages, integer)
> - monthly.uk.delta_vol (row 9, col 8), monthly.fr.delta_vol (row 9, col 9), monthly.pl.delta_vol (row 9, col 10)
> - monthly.global.gm_impact (row 33, col 11)
> - monthly.uk.gm_impact (row 33, col 8), monthly.uk.rpo_effect (row 37, col 8), monthly.uk.cpo_effect (row 38, col 8), monthly.uk.vol_effect (row 40, col 8)
> - monthly.fr.gm_impact (row 33, col 9), monthly.fr.rpo_effect (row 37, col 9), monthly.fr.cpo_effect (row 38, col 9), monthly.fr.vol_effect (row 40, col 9)
> - monthly.pl.gm_impact (row 33, col 10), monthly.pl.rpo_effect (row 37, col 10), monthly.pl.cpo_effect (row 38, col 10), monthly.pl.vol_effect (row 40, col 10)

Substitute the actual focus week number and Monday date before dispatching. Wait for the subagent to return the JSON before proceeding.

The workbook has four tabs; the two that matter are:
- **GM Tracker - Weekly** — weekly view, weeks laid out left-to-right as columns
- **GM Tracker - Monthly** — current-month landing, two side-by-side blocks (only the LEFT block is reliable, see Step 3)

### Step 2 — Read the focus week from "GM Tracker - Weekly"

Locate the focus-week column by matching row 10 (the week-number row) to the current ISO week, or by matching row 9 (begin-of-week date) to the Monday of the current ISO week. Confirm via row 7 — it usually shows "Forecast" for the in-progress week.

The Weekly tab is structured as four vertical blocks. Row offsets are stable:

| Block | Header row | Volume rows | RPO rows | CPO rows | GM split rows | GM Impact row |
|---|---|---|---|---|---|---|
| Global | 9 | 11 (Target), 12 (Actual), 13 (Delta) | 15-17 | 19-21 | 33 (GM RPO rate effect), 34 (GM CPO rate effect), 35 (GM rate effect), 36 (GM volume effect) | **37** |
| UK | 50 | 52, 53, 54 | 56-58 | 60-62 | 74, 75, 76, 77 | **78** |
| FR | 91 | 93, 94, 95 | 97-99 | 101-103 | 115, 116, 117, 118 | **119** |
| PL | 132 | 134, 135, 136 | 138-140 | 142-144 | 156, 157, 158, 159 | **160** |

For the focus-week column, pull these values for each market:
- **Delta Volume** (in packages)
- **GM RPO Rate effect** (€)
- **GM CPO Rate effect** (€)
- **GM Volume effect** (€)
- **GM Impact** (€) — this is the headline

The Global GM Impact (row 37) is the **headline weekly figure** in the message.

### Step 3 — Read the monthly landing from "GM Tracker - Monthly"

**Critical**: The Monthly tab has TWO blocks side-by-side, both labelled "Landing Forecast (Monthly)" in row 3. Only the LEFT block is reliable.

| Block | Cols | Status |
|---|---|---|
| Left | C/F headers, values in cols 8 (UK), 9 (FR), 10 (PL), 11 (Global) | ✅ Reliable — matches the sum of weekly GM Impact across all weeks of the focus month in the Weekly tab |
| Right | Headers at col 14, values in cols 16 (UK), 17 (FR), 18 (PL), 19 (Global) | ❌ Broken formulas — do NOT use |

Pull row 33 ("GM Impact") from the LEFT block — these are the per-market landing figures vs BP'26 for the month the tab is currently tracking.

**Month coherence check (mandatory):** the focus week and the Monthly tab must refer to the same calendar month. The Monthly tab's tracked month is shown in row 6, col 3 (an end-of-month date, e.g. `2026-04-30` for April, `2026-05-31` for May). The focus month is the month containing the Monday of the focus week (row 9 of the Weekly tab for the focus column).

- If they match → proceed with the values pulled.
- If they differ → **stop and tell Francesco**. The Monthly tab uses IMPORTRANGE and rolls forward when the source workbook updates; a mismatch means either the source hasn't rolled over yet, or Francesco is asking for a week in a different month than the tab is currently showing. Either way, the figures will be wrong if you proceed. Don't guess.

Sanity check (after coherence check passes): sum the focus-month weekly GM Impacts from the Weekly tab and confirm they match the Monthly tab's left block within rounding. If they diverge, flag it and stop.

### Step 4 — Compose the message

Use this exact structure. Bold ONLY the three lines below (title, weekly header, monthly header) — when composing the string for `slack_send_message`/`slack_send_message_draft`, write them with standard markdown `**double asterisks**` (the tool converts to Slack's native bold on post/draft). Everything else (figures, market names, body sentences) stays plain, unbolded text. Bullet points ("•", not "-" or "*") for the monthly per-market breakdown. One emoji in the title (`:moneybag:`). Slack does not support underline — use bold for emphasis instead. **No narrative attribution.**

```
:moneybag: **Financial Update — Pre-weekend check (all figures vs [comparison base])**

**Weekly — W[XX] ([Mon DD–DD])**
Lower volumes than target in [markets] (missing c.a X.Xk packages vs [base] — UK ~X.Xk, FR ~X.Xk, PL ~X.Xk). Higher RPO in [markets] vs [base]. [Markets] running CPO overspends vs [base].
Overall this week we aim to have a [positive/negative] GM impact of [+/-]€X.Xk vs [base] (+€X.Xk due to higher RPO, -€X.Xk due to CPO overspend and -€X.Xk due to missed volumes).

**Monthly landing — [Month]**
At current pace we aim to [meet / beat by €X.Xk / miss by c.a €X.Xk] the monthly GM target vs [base].
• UK [+/-]€X.Xk ([data-grounded explanation])
• FR [+/-]€X.Xk ([data-grounded explanation])
• PL [+/-]€X.Xk ([data-grounded explanation])

Any questions please let me know. Thanks.
```

For the per-market monthly explanation, ground every clause in the tracker numbers, never in narrative. Examples of acceptable phrases:
- "(RPO above BP)" — when RPO rate effect is a material positive contributor
- "(volumes above BP)" — when volume effect is a material positive contributor
- "(CPO favourable)" — when CPO is a material positive contributor (i.e. underspend)
- "(c.a Xk packages missed)" — when volume effect is materially negative
- "(CPO overspend)" — when CPO is materially negative
- "(RPO below BP)" — when RPO is materially negative

Examples of phrases to avoid:
- "driven by the Tesco RFP amendment" — narrative attribution
- "on strong volume delivery" — narrative ("strong" is editorial)
- Any client name, campaign name, RFP name, or business event

### Picking what to include in each market's monthly explanation

For each market, pull its three monthly components from the **GM Tracker - Monthly** tab LEFT block:
- `GM RPO Rate effect` — row 37
- `GM CPO Rate effect` — row 38
- `GM Volume Effect` — row 40
(UK col 8, FR col 9, PL col 10.)

A component is **material** if its absolute value is **≥ €3,000**. Material positives list: every component above +€3k. Material negatives list: every component below -€3k.

Composition rules:

1. **If the market's GM Impact ≥ 0 (ahead of BP)**: list all material positives with "&". If material negatives exist, append ", offsetting [negatives joined with &]". Example: RPO +€275k (material+), CPO -€84k (material-), Vol -€112k (material-) → "RPO above BP, offsetting c.a 87k packages missed & CPO overspend".
2. **If the market's GM Impact < 0 (behind BP)**: list all material negatives with "&". If material positives exist, append ", partly offset by [positives joined with &]". Example: RPO +€42k (material+), CPO -€44k (material-), Vol -€85k (material-) → "c.a 26k packages missed & CPO overspend, partly offset by RPO above BP".
3. **If everything is below the materiality threshold**: write "(roughly on BP)".

### Stylistic dedup (apply after composing each market's explanation)

When two phrases share the same "above BP" or "below BP" suffix, collapse them:

| Raw composition | Polished |
|---|---|
| "RPO above BP & volumes above BP" | "RPO & volumes above BP" |
| "RPO below BP & volumes below BP" | "RPO & volumes below BP" |
| "RPO above BP & CPO favourable" | (leave as-is — different suffixes) |
| "c.a 87k packages missed & CPO overspend" | (leave as-is — different suffixes) |

For volume miss callouts, use the per-market **focus-month** Δ vol sum (sum of `Delta Volume` row across all weekly columns whose begin-of-week falls in the focus month), NOT the focus week's value.

### Volume sentence threshold

For the **volume sentence** (paragraph 1), only quantify a market's volume gap if `|Δ Volume| ≥ 1,000` packages for the focus week. Below that, write the market as "on BP".

Sign-off line is fixed: "Any questions please let me know. Thanks." (no exclamation, no emoji).

## Hard rules

These have caused real errors in past attempts — do not violate.

1. **Title line must read** `:moneybag: **Financial Update — Pre-weekend check (all figures vs [base])**` (double-asterisk markdown as typed into the Slack tool call) — em dash before "Pre-weekend", parenthetical kept. Don't drop the emoji, the bold, or the parenthetical.
2. **Always include the monthly landing paragraph** with per-market UK/FR/PL breakdown. The weekly headline alone is incomplete.
3. **Read the spreadsheet as XLSX, not as natural-language**. The natural-language render merges tabs and produces wrong figures.
4. **Use the LEFT block of the Monthly tab only** (cols 8-11). The right block (cols 16-19) is broken.
5. **Focus week and Monthly tab must agree on the calendar month.** Compare the Monthly tab's row 6 col 3 date to the focus week's begin-of-week month. If they don't match, stop and tell Francesco — never proceed with a stale month.
6. **Never invent the weekly GM headline from incomplete forecast data**. If row 37 (Global GM Impact) for the focus week is empty or 0, stop and ask Francesco for the figures.
7. **Three-way decomposition must reconcile** to the headline (RPO + CPO + volume = GM Impact, ± rounding). If it doesn't, re-check the rows you pulled.
8. **Frame every figure vs the confirmed comparison base** (FC3 by default). No raw actuals, no week-on-week comparisons.
9. **Always remind Francesco at the start** that you're reading the "Claude.ia IMPORTRANGE version" of the tracker.
10. **Do not paste a numbered breakdown of source rows** at the bottom unless Francesco asks. The deliverable is the message, not the audit trail.

## Tone and format

- Bold (`**double asterisks**` in the tool call — NOT single asterisks, which render as italics) only the title, the "Weekly — ..." header, and the "Monthly landing — ..." header. Plain prose elsewhere; bullets ("•") for the monthly per-market list.
- **All € figures use one decimal** (€X.Yk format throughout the message — weekly headline and monthly figures alike).
- Weekly GM headline: **round half-down (truncate the second decimal)**. So -€4,154 → -€4.1k (not -€4.2k). In Python: `int(abs(v)/100)/10` then attach the sign.
- All other € figures: standard half-up to one decimal. So €81,561 → €81.6k, €146,679 → €146.7k.
- Volume figures: one decimal (e.g. ~10.9k, ~2.9k). Round to nearest 0.1k packages.
- "c.a" (standard spelling — not "ca." or "approx.").
- "vs BP'26" (apostrophe before 26, no space).
- Use "&" not "and" between market codes.
- Sign off exactly: "Any questions please let me know. Thanks."

## Computing per-market values for the message

**Weekly volume miss** (for the volume sentence): use the focus-week column directly — `Delta Volume` rows 54 (UK), 95 (FR), 136 (PL).

**Monthly volume miss per market** (for the monthly landing paragraph): pull directly from the Monthly tab LEFT block, row 9 (cols 8/9/10 for UK/FR/PL). Do NOT sum weekly columns — the Monthly tab already has the cumulative figure.

## Step 5 — Preview and push to Slack

1. **Always show the formatted message in chat first** as a preview.
2. **Wait for explicit approval** from Francesco ("sì", "ok", "send it", "vai", or equivalent) before pushing.
3. Once approved, send to `#operations` (channel ID: `C041W0BD7U0`) using the Slack `send_message` tool.
4. Return the message link after sending.

## Quick worked example (W17 / Apr 20-26, 2026)

> :moneybag: **Financial Update — Pre-weekend check (all figures vs BP'26)**
>
> **Weekly — W17 (Apr 20–26)**
> Lower volumes than target in the UK & FR (missing c.a 31k packages vs BP'26 — UK ~24k, FR ~7k). PL on BP. Higher RPO in UK & FR vs BP'26. UK & FR running CPO overspends vs BP'26.
> Overall this week we aim to have a negative GM impact of -€4.1k vs BP'26 (+€79k due to higher RPO, -€30k due to CPO overspend and -€54k due to missed volumes).
>
> **Monthly landing — April**
> At current pace we aim to beat the monthly GM target by c.a €7k vs BP'26.
> • UK +€79k (RPO above BP, offsetting c.a 87k packages missed & CPO overspend)
> • FR -€87k (c.a 26k packages missed & CPO overspend, partly offset by RPO above BP)
> • PL +€15k (RPO & volumes above BP)
>
> Any questions please let me know. Thanks.

Source values for the example above:
- Weekly tab col 33 (W17 forecast): GM Impact -€4,154; RPO rate effect +€79,171; CPO rate effect -€29,605; Volume effect -€53,720
- Weekly tab col 33 volume deltas: UK -24,314; FR -6,943; PL +651 (below 1k threshold → "PL on BP")
- Monthly tab row 33 LEFT block: UK +€78,960; FR -€86,717; PL +€14,888; Global +€7,131
- Monthly components: UK (RPO +€275k, CPO -€84k, Vol -€112k); FR (RPO +€42k, CPO -€44k, Vol -€85k); PL (RPO +€11k, CPO +€0k, Vol +€4k)
- April Δ vol per market: UK -86,927 → ~87k; FR -26,327 → ~26k; PL +2,397 → ~2k
