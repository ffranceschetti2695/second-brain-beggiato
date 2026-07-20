---
description: Cross-source lookup for anything about Stuart — checks the Stuart Brain vault first, then Slack, then Google Drive, in that order. Triggers on natural asks to find/check/look up status, info, or documents about a Stuart topic (a client, a deal, a decision, a number). Do NOT auto-invoke — when a message looks like this kind of lookup, ask Francesco first ("Want me to run the Stuart lookup skill for this?") and only proceed once he confirms.
allowed-tools:
  - Bash
  - Read
  - Grep
  - mcp__claude_ai_Slack__slack_search_public_and_private
  - mcp__claude_ai_Slack__slack_search_public
  - mcp__claude_ai_Slack__slack_search_channels
  - mcp__claude_ai_Slack__slack_read_channel
  - mcp__claude_ai_Slack__slack_read_thread
  - mcp__claude_ai_Google_Drive__search_files
  - mcp__claude_ai_Google_Drive__read_file_content
  - mcp__claude_ai_Google_Drive__download_file_content
  - mcp__claude_ai_Google_Drive__get_file_metadata
---

You are helping Francesco find information about Stuart by searching, in order, the Stuart Brain vault, Slack, and Google Drive.

## Trigger and confirmation gate

This skill is triggered by `/stuart-lookup <topic>` or by natural phrases where Francesco is trying to find/check/look up something about Stuart — e.g. "what's the status of X", "do we have anything on Y", "find the latest on Z", "check if there's history on...".

**Never auto-invoke.** When a message reads like this kind of lookup but doesn't explicitly call `/stuart-lookup`, ask first: "Want me to run the Stuart lookup skill for this?" (or a natural equivalent in the language of Francesco's message). Only run the steps below after he confirms. If he explicitly types `/stuart-lookup`, that itself is the confirmation — proceed directly.

Reply in the same language as Francesco's current message — never default to Italian, regardless of the language of vault notes, Slack messages, or Drive documents encountered along the way. This follows the global language-mirroring rule in CLAUDE.md.

## Step 1 — Stuart Brain vault (always first)

The vault lives at `~/Desktop/company-brain-app/stuart-vault/` and is a separate, already-synthesized knowledge base (Slack, Confluence, Drive, Gmail, DWH all ingested into atomic notes) — not the Obsidian Personal Brain vault this project's CLAUDE.md otherwise refers to.

Start with `llms.txt` or `index-stuart-vault.md` in that folder to orient, then grep/read the relevant notes (`concepts/`, `data/`, `docs/`, `entities/`, `sources/`). This is the fastest path to an answer since it's already curated — check it before anything else, every time.

Note its known gaps before trusting silence as an answer: Google Meet transcripts aren't ingested (blocked by Google), and Slack/Confluence/Gmail ingestion has a lag (as of the last full pass, Slack coverage ran through early July 2026) — so a "not found" here doesn't rule out the info existing, only that it isn't captured yet.

## Step 2 — Slack (if the vault doesn't fully answer it, or freshness matters)

Move to Slack when the vault has nothing, is incomplete, or the topic is likely to have moved since the vault's last ingestion (recent decisions, live negotiations, anything from the last few weeks).

Use `slack_search_channels` first if you need to find the right channel by name, then `slack_search_public_and_private` for message/file content (ask before falling back to `slack_search_public` only — private+public search needs no extra consent per the tool, but treat it as the default since Francesco's relevant channels are often private). Use `slack_read_channel` / `slack_read_thread` to pull surrounding context when a hit is part of a larger discussion.

## Step 3 — Google Drive (for the source documents themselves)

Move to Drive when Francesco needs an actual file (a deck, a report, a spreadsheet) rather than just the facts from it, or when Slack and the vault only gave partial/indirect confirmation and a primary document would settle it.

Use `search_files` with a structured query (title/fullText/modifiedTime as needed), then `read_file_content` for a quick text read or `download_file_content` when the actual file needs to be saved.

## Step 4 — Synthesize

Don't dump raw search results. Give Francesco a direct answer, and note which source(s) it came from (e.g. "per the vault..." / "per a July 9 Slack thread..." / "per the June Mutares deck..."), especially when sources disagree or one is more current than another. Keep it short and to the point — no meta-narrative about the search process itself unless something material was missing or contradictory.
