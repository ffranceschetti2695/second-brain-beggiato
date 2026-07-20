---
name: stuart-mbr-next-steps-recap
description: Build the "next steps" recap message for the Monthly Business Review, from the meeting transcript/notes PDF Francesco downloads after each MBR, and draft it (never send) in #monthly_business_review in Francesco's usual format. Use whenever Francesco asks to "create the MBR next steps", "write up next steps from the last MBR", "draft the next steps recap", or any variant of turning the post-MBR transcript into the numbered Sponsor/Owner/Next-step message he posts after every session. Do NOT use for chasing owners for updates on an existing recap (that's stuart-mbr-next-steps-followup) — this skill produces the original recap message from a fresh meeting.
---

# Stuart MBR Next Steps Recap

After each Monthly Business Review, Francesco writes up a numbered "next steps" recap and posts it in `#monthly_business_review`, to be reviewed at the top of the following MBR. This skill builds that message from the meeting transcript and drafts it in Slack for his review.

## Step 0 — Check references first

1. `docs/doc-mbr-next-steps-followup.md` documents the sibling skill (`stuart-mbr-next-steps-followup`) that chases owners on an *existing* recap — read it for context on the overall monthly cadence, but it is not the format reference for this skill.
2. The actual format reference is **Francesco's own past recap messages in Slack** (Step 2 below) — always pull 2-3 recent examples before writing a new one, don't rely on memory of the format since it evolves (e.g. the sponsor/owner convention changed between the April and May 2026 recaps).

## Step 1 — Find the source transcript

The source is the most recently downloaded meeting notes/transcript PDF, typically in `~/Downloads`, titled something like `Monthly Business Review - Materials in Description - <date> - Notes by Gemini.pdf` or similar auto-generated meeting-notes export. Find it with `ls -lt ~/Downloads/*.pdf | head` and confirm the date matches the MBR Francesco just had — ask if more than one plausible candidate exists.

These are Gemini/auto-generated notes, not a verbatim transcript. Expect:
- Speaker labels sometimes anonymized or garbled (e.g. "Meeting Room UK" instead of a real name, a name misspelled like "Franchesca" for Francesco).
- A "Next steps" checklist section — this is the primary source, extracted by the notetaker itself.
- A "Decisions" section split into "Aligned" and "Needs Further Discussion" — items in "Needs Further Discussion" are often worth carrying into the recap as an open next step, since they're explicitly unresolved.
- A "Details" narrative section — use it to add context sentences and to resolve ambiguous next-step items, not as a source of new items.

## Step 2 — Learn the current format from Slack

1. Find the channel: `slack_search_channels` query "monthly business review" (private channel, `#monthly_business_review`).
2. Pull the last 2-3 recap messages: `slack_search_public_and_private` query `next steps in:#monthly_business_review`, sort by timestamp. Look for messages **from Francesco** that itemize numbered next steps with Sponsor/Owner lines (not the "deck is ready" announcements).
3. Match the current structure: opening greeting + reminder that this is iterative and people should flag anything missing/unclear/wrong, categories (they vary — e.g. Organisational / Strategic-Business / Presentation / AI — pick categories that fit the actual content, don't force last month's categories if they don't apply), then per item:
   ```
   N. *Title* · Sponsor: X · Owner: Y, Z
   <context sentence>
   Next step: <next-step sentence>
   ```
4. Match the closing CC line style (tags the exec-level sponsors/regulars, not every owner).

## Step 3 — Filter to what's actually executable and trackable

Not everything in the transcript's "Next steps" checklist belongs in the recap. Include an item only if it has a concrete owner and a concrete deliverable that can be checked off at the next MBR. Drop:
- Purely administrative/meta items about the MBR process itself (e.g. "share these next steps by Monday" — that's Francesco posting this very message).
- Internal onboarding/culture items with no measurable outcome (e.g. "brief the new joiner").
- Vague "communicate updates" items with no specific ask.

When unsure whether an item is trackable or just noise, ask Francesco rather than silently dropping or silently including it — list it separately as "considered but excluded, let me know if you want it back in."

## Step 4 — Resolve names to real Slack identities

Transcript names are frequently a first name, a nickname, or a garbled/anonymized label. Before drafting:
1. Use `slack_search_users` to resolve each name to a real user (title/email help disambiguate common first names).
2. If a name can't be resolved (unknown nickname, client-side contact, garbled label like "CL" or a name with no Slack match), **do not guess-tag them** — leave them as plain text and flag explicitly to Francesco that this name needs manual confirmation before sending.
3. Cross-check role plausibility against context (e.g. a name mentioned alongside Poland volume data should resolve to someone with a Poland-facing title) — don't pick the first search result blindly if multiple people share a first name.

## Step 5 — Draft, never send

Use `slack_send_message_draft` on the `#monthly_business_review` channel ID — never `slack_send_message`. Francesco reviews and sends it himself, same rule as the follow-up skill.

Always open the draft with Francesco's standard framing (adapt wording slightly to match the two-three most recent examples pulled in Step 2, but the substance is constant):
```
Hello <!here>,

Below are the next steps coming from the previous MBR. As always, these will be reviewed at the beginning of the next MBR.
Please let me know if anything is unclear, if something is missing, or if you disagree with any of the points - this is an iterative process and the goal is to build on this together.

Thanks!

CC. <sponsor/exec mentions>
```

Tag every resolved person with real Slack mention syntax `<@USER_ID|Display Name>` — plain-text names don't notify anyone, which defeats the point of the recap.

## Step 6 — Report back

After creating the draft, give Francesco:
1. The channel link to review it.
2. A one-line list of what changed vs. a straight transcript dump (items dropped as noise, items merged, owners corrected).
3. An explicit callout of any name that couldn't be resolved to a Slack identity, so he can add the tag manually or correct it before sending.

## Hard rules

1. Never send directly — draft only, Francesco sends.
2. Never invent or guess-resolve an ambiguous name to a Slack tag — flag it instead.
3. Pull the format from recent real Slack messages each time, don't assume last month's category labels still apply.
4. Only include items with a concrete owner and a checkable deliverable — flag borderline items rather than silently including or excluding them.
5. Carry over context + "Next step:" content faithfully; don't paraphrase away the specifics an owner needs to act on.
