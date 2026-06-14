#!/usr/bin/env python3
"""
Aurora Cervello — Generatore showcase.md
Fotografia del vault per demo. DERIVATO: rigenera con python3 generate_showcase.py
"""

import os
import re
from collections import defaultdict, deque
from datetime import date

VAULT = os.path.dirname(os.path.abspath(__file__))
FOLDERS = ["self", "areas", "projects", "concepts", "docs", "entities", "data", "code", "outputs"]
OUTPUT = os.path.join(VAULT, "_showcase", "showcase.md")


def parse_note(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    lines = content.split("\n")
    fm = {}
    body_start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                body_start = i + 1
                break
            m = re.match(r"^(\w+)\s*:\s*(.*)", lines[i])
            if m:
                fm[m.group(1)] = m.group(2).strip().strip('"')
    body = "\n".join(lines[body_start:])
    links = set()
    for raw in re.findall(r"\[\[([^\]]+)\]\]", body):
        t = raw.split("|")[0].split("#")[0].strip()
        if "/" in t:
            t = t.split("/")[-1]
        if t:
            links.add(t.lower())
    return fm.get("title", ""), fm.get("summary", ""), links


def collect_notes():
    notes = {}  # key → (path, folder, title, summary, links)
    for folder in FOLDERS:
        fp = os.path.join(VAULT, folder)
        if not os.path.isdir(fp):
            continue
        for fname in sorted(os.listdir(fp)):
            if not fname.endswith(".md"):
                continue
            key = fname[:-3].lower()
            path = os.path.join(fp, fname)
            title, summary, links = parse_note(path)
            notes[key] = (path, folder, title, summary, links)
    return notes


def connected_components(notes):
    adj = defaultdict(set)
    for key, (_, _, _, _, links) in notes.items():
        for target in links:
            if target in notes:
                adj[key].add(target)
                adj[target].add(key)
    visited = set()
    components = 0
    for start in notes:
        if start in visited:
            continue
        components += 1
        queue = deque([start])
        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            for nb in adj[node]:
                if nb not in visited:
                    queue.append(nb)
    return components


def main():
    notes = collect_notes()

    # Stats
    total_notes = len(notes)
    total_links = sum(
        len([t for t in data[4] if t in notes])
        for data in notes.values()
    )
    components = connected_components(notes)

    # Notes per folder
    per_folder = defaultdict(list)
    for key, (_, folder, title, summary, _) in notes.items():
        per_folder[folder].append((key, title))

    # Hub summaries (index-* notes)
    hubs = {
        folder: next(
            ((key, summary) for key, (_, f, _, summary, _) in notes.items()
             if f == folder and key.startswith("index-")),
            None
        )
        for folder in FOLDERS
    }

    today = date.today().strftime("%Y-%m-%d")

    out = []
    out.append("---")
    out.append("title: Aurora Cervello — Showcase")
    out.append(f'summary: "Fotografia del vault Aurora Sistemi al {today}: {total_notes} note, {total_links} wikilink, {components} componente connessa."')
    out.append("tags: [self, showcase, demo]")
    out.append("status: active")
    out.append(f"created: {today}")
    out.append(f"updated: {today}")
    out.append('related: ["[[self-identita-aurora]]", "[[index-self]]"]')
    out.append("---")
    out.append("")
    out.append("# Aurora Cervello — Showcase")
    out.append("")
    out.append(f"> Fotografia generata il **{today}**. DERIVATA: rigenera con `python3 generate_showcase.py`.")
    out.append("")
    out.append("## Metriche del vault")
    out.append("")
    out.append("| Metrica | Valore |")
    out.append("|---|---|")
    out.append(f"| Note totali | **{total_notes}** |")
    out.append(f"| Wikilink totali | **{total_links}** |")
    out.append(f"| Componenti connesse | **{components}** {"✅ grafo unico" if components == 1 else "⚠️ isole rilevate"} |")
    out.append(f"| Cartelle attive | **{len([f for f in FOLDERS if per_folder.get(f)])}** |")
    out.append("")
    out.append("## Note per cartella")
    out.append("")
    out.append("| Cartella | Note |")
    out.append("|---|---|")
    for folder in FOLDERS:
        count = len(per_folder.get(folder, []))
        if count:
            out.append(f"| {folder}/ | {count} |")
    out.append(f"| **Totale** | **{total_notes}** |")
    out.append("")
    out.append("## Hub per cartella")
    out.append("")
    out.append("Ogni cartella ha un nodo indice che aggrega tutte le sue note.")
    out.append("")
    for folder in FOLDERS:
        hub = hubs.get(folder)
        if hub:
            key, summary = hub
            out.append(f"**[[{key}]]** ({folder}/) — {summary}")
        else:
            out.append(f"**{folder}/** — nessun hub trovato")
        out.append("")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    print(f"showcase.md generato: {total_notes} note, {total_links} wikilink, {components} componente connessa.")


if __name__ == "__main__":
    main()
