---
name: stuart-mbr-next-steps-followup
description: Draft Slack check-in messages to the owners of last month's MBR "next steps", ahead of the upcoming Monthly Business Review. Reads the most recent "next steps" recap Francesco posted in #monthly_business_review, groups items by owner, and creates Slack drafts (never sends) for Francesco to review. Use this skill whenever Francesco asks to "chase updates on next steps", "follow up on MBR next steps", "ask owners for updates before the MBR", or any variant of the recurring monthly ritual of pinging next-step owners before the next MBR. Do NOT use for the next-steps recap message itself (that's a separate manual write-up) — this skill only drafts the follow-up chase messages to owners.
---

# Stuart MBR Next Steps Follow-up

Every month, ahead of the Monthly Business Review, Francesco chases the owners of last month's "next steps" for a status update. This skill finds the most recent next-steps recap, splits it by owner, and drafts (not sends) one Slack message per owner.

## Step 1 — Find the source message

1. Find the channel: `slack_search_channels` query "monthly business review" (it's a private channel, `#monthly_business_review`).
2. Find the latest next-steps recap: `slack_search_public_and_private` query `next steps in:#monthly_business_review`, sort by timestamp. Look for the message **from Francesco** that itemizes numbered next steps with Sponsor/Owner lines (not the "MBR deck is ready" announcement, not a one-off reply) — this is the most recent MBR's recap, posted a few weeks earlier.
3. Read any thread replies on that message — owners sometimes clarify or split a point in the thread (e.g. "I incorporated this into point 9"). Use the corrected version if one exists.

## Step 2 — Parse and assign one primary recipient per item

Each item has the shape: number, title, Sponsor (exec, usually not the doer), Owner(s) (the actual doer(s)), a context sentence, and a "Next step: ..." line.

**Recipient rule:** the primary recipient is the **first-listed Owner, excluding Francesco**.
- If Francesco is the only owner, or the item is clearly his own to handle (e.g. co-owner alongside one other person and he's already dealt with it) — **skip it**, no message needed. Confirm with Francesco if unsure rather than guessing.
- Sponsors are cc-level context, not recipients — don't message a sponsor unless they're also the owner.

## Step 3 — Group items by recipient before drafting

**Slack allows only one draft per DM/channel at a time.** If the same person is the primary recipient on multiple items, combine them into a single message — don't try to send separate drafts to the same person (the second call will hit `draft_already_exists` semantics or silently overwrite the first).

Before drafting to two people who are tightly coupled on several items (e.g. a sponsor who is also personally the owner on other items, working closely with another owner), check whether Francesco already has an existing group DM with them — search `slack_search_public_and_private` for a distinctive keyword from their recent conversation, filtered to `channel_types: mpim`. **Group DMs cannot be created via the Slack tools available** — only drafted into if one already exists. If none exists, ask Francesco: send two separate individual messages, or point you to the group DM.

## Step 4 — Compose each message

Always include the **full next step**, not a paraphrase: title (as a heading), the original context sentence, and the literal "Next step: ..." line. Summarizing loses detail owners need to act on.

Template per item:
```
N. *Title* · Sponsor: X · Owner: Y, Z
<context sentence, verbatim from the recap>
Next step: <next-step sentence, verbatim from the recap>
```

Wrap with a short greeting and closing ask, e.g.:
```
Hey <Name(s)> — ahead of Thursday's MBR, quick check-in on the next step(s) from last month:

<item block(s)>

Would be great to get a quick update on each before Thursday. Thanks!
```

## Step 5 — Create drafts, never send

Use `slack_send_message_draft` (channel_id = the person's DM id, or the group DM id). **Never use `slack_send_message`** for this — Francesco reviews and sends each one himself.

There is no way to attach a screenshot/image to a Slack draft via these tools (text/markdown only) — if Francesco asks for a visual recap alongside the messages, say so rather than attempting it, and offer a text recap instead.

After creating all drafts, list them for Francesco with a one-line reminder of which item(s) each covers, and note explicitly which items were skipped because he's the owner.

## Step 6 — If asked to verify sending

Francesco may later ask "did I actually send these". Check each target channel/group DM with `slack_read_channel` (default sort is newest-first) and confirm whether a message matching the draft content appears with today's date. Don't assume drafts were sent just because they exist — read the channel.

## Hard rules

1. Never paraphrase a next step — always carry over the verbatim context + "Next step:" line.
2. Never send directly — drafts only, Francesco sends.
3. Never assume a group DM can be created — only drafted into if it already exists; ask if unsure.
4. First-listed owner (excluding Francesco) is the default recipient — don't message sponsors, and don't message Francesco's own co-owned items unless he asks.
5. One message per recipient, even if that means bundling several next steps together.
