---
description: Recap of Slack and Gmail from yesterday to now, with a per-message breakdown and flagged action items
allowed-tools:
  - Bash
  - mcp__claude_ai_Slack__slack_search_public_and_private
  - mcp__claude_ai_Slack__slack_read_thread
  - mcp__claude_ai_Gmail__search_threads
  - mcp__claude_ai_Gmail__get_thread
  - mcp__gmail-account2__search_emails
  - mcp__gmail-account2__read_email
---

You are an assistant producing the daily recap of Slack, work Gmail, and personal Gmail. Execute the steps below **in order**, without skipping any.

## Trigger

This skill is triggered by `/daily-recap` or natural phrases like "what did I miss", "give me yesterday's recap", "recap from yesterday to now", "cosa mi sono perso", "dammi il recap di ieri".

Reply in the same language as Francesco's current/latest message in the conversation — never default to Italian, and ignore the language of this skill file, of tool output, or of earlier messages in the session. This follows the global language-mirroring rule in CLAUDE.md.

## Step 1 — Compute the time window

Use Bash to compute:
- `YESTERDAY` = yesterday's date in `YYYY-MM-DD` format, for display in the recap header only
- `YESTERDAY_TS` = Unix timestamp (seconds) of yesterday at 00:00 local time

The window is: from yesterday 00:00 to now. No upper bound is needed — omitting `before` automatically captures everything up to the current moment.

**Do not use the `after:YYYY-MM-DD` text modifier in the query string** — it has been observed to be exclusive of that calendar day (it skipped the entirety of yesterday in a past run, silently dropping a whole day of messages including a substantive DM thread). Always pass `YESTERDAY_TS` via the tool's dedicated `after` parameter (Unix timestamp, documented as inclusive) instead.

## Step 2 — Fetch Slack

**Never surface customer-care/support-ticket channels** — channels like `#*customercare*`, `#support-*`, `#cnxwh_global`, `#cnx_cs_*`, `#*-help`, or any channel dominated by the "Stuart CS" bot handling individual rider/delivery tickets. These are high-volume, low-signal operational chatter (single delivery delays, PIN issues, rider assignment) that burn tokens without ever containing anything Francesco needs to see. Exclude them from the query itself with `-in:#channel-name` modifiers so they're never fetched, not just filtered after the fact. Build the exclusion list from channels you've seen flagged this way in past runs, plus any channel whose name matches the patterns above.

Call `slack_search_public_and_private` with:
- `query`: `-in:#zapp-customercare-stuart-connect -in:#cnxwh_global -in:#support-pl-pysznepl -in:#support-uk-justeat_for_business` (just the exclusions — no date modifier in the query text; extend this list with any other CS/support-ticket channel encountered)
- `after`: `YESTERDAY_TS` (the dedicated timestamp parameter, not the query string)
- `channel_types`: leave the default (`public_channel,private_channel,mpim,im` — covers channels, DMs, and group DMs)
- `include_bots`: `false`
- `sort`: `timestamp`, `sort_dir`: `asc`
- `limit`: `20` per call

**Paginate exhaustively**: keep calling with the returned `cursor` until the response has no more pages (no `cursor` returned, or pagination_info says there are no more). Do not stop after a fixed number of pages — the goal is full coverage of every channel, DM, and group DM Francesco is a member of, not a sample. If the result set is very large, it's fine to stop paginating once messages are clearly outside the time window, but never stop just because "enough" pages have been fetched.

If a page still surfaces an obvious CS-ticket channel not yet on the exclusion list (recognizable by the "Stuart CS" bot handling a single delivery/rider issue), skip reading its thread context and don't add it to the breakdown — just note it under noise and add it to the exclusion list for the next query in this same run.

For each message found, keep: source channel/DM, author, text, timestamp, permalink.

If a message is part of a thread and the context isn't clear from the text alone, use `slack_read_thread` to retrieve context before summarizing.

If the call fails, note "Slack unreachable" and continue with Gmail.

## Step 3 — Fetch work Gmail

Call `mcp__claude_ai_Gmail__search_threads` (the `claude_ai_Gmail` connector — this is Francesco's work inbox) with:
- `query`: `after:{YESTERDAY with slashes, e.g. 2026/07/13} in:inbox category:primary`
- `pageSize`: `50`

For each thread with a subject/snippet that isn't clearly enough to summarize, call `get_thread` to get the full body.

If the call fails, note "Work Gmail unreachable" and continue. Note: a separate, unrelated server (`mcp__gmail__*`) has previously failed here with `invalid_grant` — don't use it; `claude_ai_Gmail` is the one that works for the work inbox.

## Step 3b — Fetch personal Gmail

Call `mcp__gmail-account2__search_emails` (a distinct connector for Francesco's personal inbox, also used by the `bills` skill) with:
- `query`: `after:{YESTERDAY with slashes, e.g. 2026/07/13} in:inbox category:primary`
- `maxResults`: `50`

For each email in the results, call `mcp__gmail-account2__read_email` to get sender, subject, body, date.

If the call fails, note "Personal Gmail unreachable" and continue.

## Step 4 — Filter out noise

From the collected Slack, work Gmail, and personal Gmail lists, separate:
- **Relevant**: messages/emails from real people with content that requires reading or action, OR content with business signal (see Step 5b) even if no action is needed. For personal email, "business signal" won't usually apply — treat anything requiring a reply/decision/action, or genuinely noteworthy personal news, as relevant instead.
- **Noise**: automated notifications, digests, calendar invites, bots, mailing lists/newsletters, receipts/confirmations with nothing to act on — this applies to both inboxes.

Noise doesn't go into the detailed breakdown, but should be counted per source (e.g. "12 automated Slack notifications, 5 work newsletters, 8 personal promo emails ignored").

## Step 5 — Flag action items

For each relevant item, assess whether it seems to require a reply, a decision, or an action from Francesco (direct question, approval request, deadline, etc.). If so, mark it with ⚠️ at the start of the line.

## Step 5b — Flag business signal

Independently of whether an action is needed, assess whether the item carries business signal: anything conceptual or with an impact on the business — country/market performance, commercial developments (deals, churn, pricing, clients), competitive moves, ops issues, strategic shifts — even a minor or indirect one.

If it does, score it 1-10 for business impact (10 = major, e.g. a market-moving deal or a material performance miss; 1 = marginal, barely worth a mention) and tag the line with 🔥{score}. Skip the tag entirely for items with no business signal — don't force a score onto routine coordination messages.

An item can carry both ⚠️ and 🔥 at once (e.g. a decision request that also signals a commercial shift) — combine them on the same line, don't split into separate sections.

## Step 6 — Produce the output in chat

Don't save anything to disk. Produce only this output in chat:

---

## Recap — {YESTERDAY} → today {current time}

### Overview
[2-3 sentences: what happened overall, general tone, whether anything is urgent]

### 💬 Slack
[For each channel/DM with relevant messages, group like this:]

**{#channel or "DM with {name}"}**
- [⚠️ if action needed][ 🔥{score} if business signal] **{author}** — {one-line summary of the message or thread} → [link]({permalink})

[If no relevant messages: "No relevant messages in this window."]

### 📧 Work Gmail
[For each relevant email:]

- [⚠️ if action needed][ 🔥{score} if business signal] **{sender}** — *{subject}* — {one-line summary}

[If no relevant emails: "No relevant emails in this window."]

### 📬 Personal Gmail
[For each relevant email:]

- [⚠️ if action needed] **{sender}** — *{subject}* — {one-line summary}

[If no relevant emails: "No relevant emails in this window."]

---

*Noise ignored: {N} automated Slack notifications, {N} work newsletters/notifications, {N} personal promo/newsletter emails*
*Unreachable: {list or "none"}*

---

If there's no relevant content in either source, simply write:
> No relevant messages or emails from yesterday to now.
