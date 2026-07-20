# Skill: journal

Manages the Personal Brain's dynamic memory. Four commands:
`start session` | `good morning` | `close session` | `end of day`.

**MANDATORY TRIGGER — NON-NEGOTIABLE:**
If the user says "inizia sessione", "inizio sessione", "iniziamo una nuova sessione", "nuova sessione", "iniziamo la sessione", "buongiorno", "start session", "let's start a session", "new session", or "good morning", you must invoke this skill with the `Skill` tool **BEFORE any other action or response**. You cannot answer, cannot read files, cannot do anything before invoking the skill. This is not optional. There are no exceptions.

Any phrase that signals the start of a work session, even if phrased differently from the ones listed, must trigger this skill immediately.

---

## General rules (always apply)

- Dates in `YYYY-MM-DD` format, never relative.
- Use only [[wikilinks]] to notes that already exist in the vault (check in `llms.txt`).
- Do not invent entities: if there is nothing to link to, ask the user what to attach the note to.
- Natural Italian, no em dash (this is the vault's content-writing convention, independent of the language of this chat).
- The `related` frontmatter is always an inline array with each wikilink individually quoted:
  `related: ["[[note-a]]", "[[note-b]]"]`
- The `summary` field goes in double quotes if it contains a `:`.

---

## Command: `start session` (alias: `good morning`)

**Purpose:** session-start briefing. Do not write anything to the vault.

**Steps:**

1. Read `llms.txt` for the up-to-date map of entities.
2. Read `workspace/journal/open-items.md` — it is the source of truth for open steps.
   If the file doesn't exist, read the latest note in `workspace/journal/sessions/` as a fallback.
3. Reply with a **briefing per workstream**, reporting the items exactly as written in the file, grouped by section (Stuart, AI / Company Brain, Finance Dashboard, AI Frontiera, Vault / Tooling).
   No extra inference, no unsolicited suggestions.
4. Reply in the language the user wrote their session-start message in.
5. Do not create files. Do not ask for confirmation. Just the briefing.

---

## Command: `close session`

**Purpose:** write the session note for the current session.

**Steps (ONE confirmation in the whole flow, not two):**

1. Look at the current conversation and infer what was done in this session, and what new open steps emerged (only the new ones, not all open items).
2. Read `workspace/journal/open-items.md`. Autonomously infer, from the conversation context, what should be **Removed** (items completed in this session) and what should be **Added** (the new steps from point 1) — don't ask the user to list them, propose them yourself.
3. In a **single message** present everything together, without splitting into multiple rounds:
   - The 3-line summary of what we did.
   - **Removing** / **Adding** (if there's nothing to change, just write "no changes to open items" and skip the rest of this point).
   - The **full updated list** of open items per workstream (only if there are changes to review; if there are none, no need to repeat it).
   - Close with a single question only if there's something to review: "Confirm, or should I change something?" — if no changes are proposed, ask no question, go straight to step 4.
4. Wait for the reply (if a question was asked) and apply everything in one shot, including updating `open-items.md` (`updated` field = today's date). Do not ask for a second confirmation on any detail: if the user corrects something, apply the correction and move on, don't ask "confirm?" a second time.
5. Write the file with the confirmed Open items:
   - **Path:** `workspace/journal/sessions/sessione-<YYYY-MM-DD>.md`
     where `<YYYY-MM-DD>` is today's date. (Keep the Italian filename stem `sessione-` — this matches the existing files in the vault, do not rename to `session-`.)
   - If a file with that name already exists (multiple sessions on the same day),
     add a suffix: `sessione-<YYYY-MM-DD>-b.md`, `sessione-<YYYY-MM-DD>-c.md`, etc.
6. **Frontmatter:**
   ```yaml
   ---
   title: "Sessione <YYYY-MM-DD>"
   summary: "<One sentence on what we did>"
   tags: [workspace, type/session]
   status: done
   created: <YYYY-MM-DD>
   updated: <YYYY-MM-DD>
   related: ["[[<entity-1>]]", "[[<entity-2>]]"]
   ---
   ```
   The `related` field must contain [[wikilinks]] to the notes touched during the session.
   Pick them from `llms.txt`. If you can't identify any, ask the user.
7. **Body** (keep these Italian section headers — `Fatto`/`Deciso`/`Aperto` — to match the vault's existing convention):
   ```
   ## Fatto
   <What we concluded.>

   ## Deciso
   <The choices made and why.>

   ## Aperto
   <new steps that emerged in this session, confirmed by the user — only the new ones>
   ```
8. After writing, confirm the path of the file created.

---

## Command: `end of day`

**Purpose:** write the daily note that merges all of the day's sessions.

**Steps:**

1. Read **all** `workspace/journal/sessions/sessione-<today's-date>*.md` notes.
2. **Before writing**, state in 3 lines what you understood happened today overall.
   Wait for the user's ok.
3. After the ok, write the file:
   - **Path:** `workspace/journal/daily/<YYYY-MM-DD>.md`
4. **Frontmatter:**
   ```yaml
   ---
   title: "Daily <YYYY-MM-DD>"
   summary: "<One sentence: the day's throughline>"
   tags: [workspace, type/daily]
   status: done
   created: <YYYY-MM-DD>
   updated: <YYYY-MM-DD>
   related: ["[[sessione-<YYYY-MM-DD>]]", "[[<main-entity-1>]]", "[[<main-entity-2>]]"]
   ---
   ```
   The `related` field includes [[wikilinks]] to all of the day's sessions plus the main static entities touched.
5. **Body** (keep these Italian section headers, same reason as above):
   ```
   ## Fatto
   <Summary of the day: what was concluded. Merge the sessions without repeating them line by line.>

   ## Deciso
   <The choices made during the day and their reasoning.>

   ## Aperto
   <Everything left pending at the end of the day.>

   ## Sessioni
   - [[sessione-<YYYY-MM-DD>]]
   - [[sessione-<YYYY-MM-DD>-b]]   ← only if additional sessions exist
   ```
6. After writing, confirm the path of the file created.

---

## Reference templates

The reusable templates are in:
- `workspace/journal/_templates/template-sessione.md`
- `workspace/journal/_templates/template-daily.md`
