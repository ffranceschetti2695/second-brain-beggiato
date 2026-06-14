#!/usr/bin/env python3
"""
Aurora Cervello — Quality Gate
Audits all atomic notes against 6 rules.
Usage: python quality_gate.py
"""

import os
import re
import sys
from collections import defaultdict, deque

VAULT = os.path.dirname(os.path.abspath(__file__))
AUDIT_SKIP = {"sources", "workspace"}
REQUIRED_FM_FIELDS = {"title", "summary", "tags", "status", "created", "updated"}


def parse_note(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    lines = content.split("\n")

    fm_fields = set()
    body_start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                body_start = i + 1
                break
            m = re.match(r"^(\w+)\s*:", lines[i])
            if m:
                fm_fields.add(m.group(1))

    body_lines = lines[body_start:]
    body_text = "\n".join(body_lines)
    return fm_fields, body_lines, body_text, content


def extract_wikilinks(text):
    """Return set of unique wikilink targets (lowercase, no .md, no path prefix)."""
    raw = re.findall(r"\[\[([^\]]+)\]\]", text)
    result = set()
    for link in raw:
        link = link.split("|")[0].split("#")[0].strip()
        if "/" in link:
            link = link.split("/")[-1]
        if link:
            result.add(link.lower())
    return result


def collect_all_notes(vault):
    """All .md files in the vault (for link resolution). Returns {key: path}."""
    notes = {}
    for folder in os.listdir(vault):
        if folder.startswith("."):
            continue
        fp = os.path.join(vault, folder)
        if not os.path.isdir(fp):
            continue
        for fname in os.listdir(fp):
            if fname.endswith(".md"):
                notes[fname[:-3].lower()] = os.path.join(fp, fname)
    return notes


def collect_audit_notes(vault):
    """Notes to audit (excludes sources, workspace, hidden). Returns {key: (path, folder)}."""
    notes = {}
    for folder in os.listdir(vault):
        if folder in AUDIT_SKIP or folder.startswith("."):
            continue
        fp = os.path.join(vault, folder)
        if not os.path.isdir(fp):
            continue
        for fname in os.listdir(fp):
            if fname.endswith(".md"):
                notes[fname[:-3].lower()] = (os.path.join(fp, fname), folder)
    return notes


def is_index(key):
    return key.startswith("index-")


def main():
    all_notes = collect_all_notes(VAULT)
    audit_notes = collect_audit_notes(VAULT)

    if not audit_notes:
        print("Nessuna nota trovata da auditare.")
        sys.exit(0)

    # Parse all audit notes
    parsed = {}
    for key, (path, folder) in audit_notes.items():
        fm_fields, body_lines, body_text, full_text = parse_note(path)
        parsed[key] = {
            "fm_fields": fm_fields,
            "body_lines": body_lines,
            "body_links": extract_wikilinks(body_text),
            "all_links": extract_wikilinks(full_text),
            "folder": folder,
            "path": path,
        }

    errors = {}

    # ── R1: Frontmatter completo ─────────────────────────────────
    r1 = []
    for key in sorted(parsed):
        missing = REQUIRED_FM_FIELDS - parsed[key]["fm_fields"]
        if missing:
            r1.append(f"  {key}: mancano → {sorted(missing)}")
    if r1:
        errors["R1 — Frontmatter incompleto"] = r1

    # ── R2: Corpo ≤ 300 righe ────────────────────────────────────
    r2 = []
    for key in sorted(parsed):
        n = len(parsed[key]["body_lines"])
        if n > 300:
            r2.append(f"  {key}: {n} righe")
    if r2:
        errors["R2 — Corpo > 300 righe"] = r2

    # ── R3 & R4: wikilink in uscita ──────────────────────────────
    r3, r4 = [], []
    for key in sorted(parsed):
        d = parsed[key]

        # R3 — almeno 3 link in uscita verso note reali non-index (solo body)
        valid_out = {
            t for t in d["body_links"]
            if t in all_notes and not is_index(t)
        }
        if not is_index(key) and len(valid_out) < 3:
            detail = f" → {sorted(valid_out)}" if valid_out else ""
            r3.append(f"  {key}: {len(valid_out)}/3 link validi{detail}")

        # R4 — zero link rotti (body + frontmatter)
        broken = sorted(t for t in d["all_links"] if t not in all_notes)
        if broken:
            r4.append(f"  {key}: {broken}")

    if r3:
        errors["R3 — Meno di 3 wikilink in uscita validi"] = r3
    if r4:
        errors["R4 — Link rotti"] = r4

    # ── R5: Zero orfani ──────────────────────────────────────────
    incoming = defaultdict(set)
    for key, d in parsed.items():
        for target in d["body_links"]:
            if target in parsed:
                incoming[target].add(key)

    r5 = []
    for key in sorted(parsed):
        if is_index(key):
            continue
        if not incoming.get(key):
            r5.append(f"  {key}")
    if r5:
        errors["R5 — Note orfane (0 link in entrata)"] = r5

    # ── R6: Unica componente connessa ────────────────────────────
    adj = defaultdict(set)
    for key, d in parsed.items():
        for target in d["body_links"]:
            if target in parsed:
                adj[key].add(target)
                adj[target].add(key)

    all_keys = set(parsed)
    start = next(iter(all_keys))
    visited = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        for nb in adj[node]:
            if nb not in visited:
                queue.append(nb)

    isolated = sorted(all_keys - visited)
    if isolated:
        errors["R6 — Grafo non connesso"] = [
            f"  {len(isolated)} nodi isolati: {isolated}"
        ]

    # ── Output ───────────────────────────────────────────────────
    if not errors:
        print("OK, 0 errori")
    else:
        total = sum(len(v) for v in errors.values())
        print(f"Trovati {total} problemi in {len(errors)} regole:\n")
        for rule, items in errors.items():
            print("─" * 60)
            print(f"{rule}  ({len(items)} note)")
            for item in items:
                print(item)
        print("\n" + "─" * 60)
        print(f"Totale: {total} problemi su {len(audit_notes)} note auditate")


if __name__ == "__main__":
    main()
