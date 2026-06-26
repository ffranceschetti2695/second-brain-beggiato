#!/usr/bin/env python3
"""
Personal Brain — Generatore llms.txt
Legge i frontmatter di tutte le note atomiche del vault e riscrive llms.txt da zero.
Usage: python3 generate_llms.py
"""

import os
import re

VAULT = os.path.dirname(os.path.abspath(__file__))
FOLDERS = ["self", "areas", "projects", "concepts", "docs", "entities", "data", "code", "outputs"]
OUTPUT = os.path.join(VAULT, "llms.txt")


def get_frontmatter(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    lines = content.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, None
    fm = {}
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            break
        m = re.match(r"^(\w+)\s*:\s*(.*)", lines[i])
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"')
    return fm.get("title"), fm.get("summary")


def main():
    lines = [
        "# Personal Brain — llms.txt",
        "# Indice-porta per AI. DERIVATO: non modificare a mano.",
        "# Rigenera con: python3 generate_llms.py",
        "# Fonte: frontmatter (title + summary) di ogni nota atomica del vault.",
        "",
    ]

    total = 0
    for folder in FOLDERS:
        fp = os.path.join(VAULT, folder)
        if not os.path.isdir(fp):
            continue

        files = sorted(f for f in os.listdir(fp) if f.endswith(".md"))
        if not files:
            continue

        lines.append("---")
        lines.append(f"## {folder}/")
        lines.append("")

        for fname in files:
            title, summary = get_frontmatter(os.path.join(fp, fname))
            key = fname[:-3]
            if summary:
                lines.append(f"- [[{key}]] — {summary}")
            elif title:
                lines.append(f"- [[{key}]] — {title}")
            else:
                lines.append(f"- [[{key}]]")
            total += 1

        lines.append("")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"llms.txt rigenerato: {total} note in {len(FOLDERS)} cartelle.")


if __name__ == "__main__":
    main()
