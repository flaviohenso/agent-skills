#!/usr/bin/env python3
"""Gera SKILL_INDEX.md a partir de todos os SKILL.md (exceto _templates)."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end].strip()
    body = text[end + 4 :].lstrip("\n")
    meta: dict[str, str] = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, rest = m.group(1), m.group(2).strip()
        if rest in (">-", ">", "|"):
            i += 1
            chunks: list[str] = []
            while i < len(lines) and (
                lines[i].startswith(" ") or lines[i].strip() == ""
            ):
                chunks.append(lines[i].strip())
                i += 1
            meta[key] = " ".join(x for x in chunks if x)
            continue
        if (rest.startswith('"') and rest.endswith('"')) or (
            rest.startswith("'") and rest.endswith("'")
        ):
            rest = rest[1:-1]
        meta[key] = rest
        i += 1
    return meta, body


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    rows: list[tuple[str, str, str, Path]] = []

    for skill_md in sorted(root.glob("**/SKILL.md")):
        rel = skill_md.relative_to(root)
        parts = rel.parts
        if parts[0].startswith(".") or parts[0] in ("_templates", "docs", "scripts"):
            continue
        if parts[0] == ".github":
            continue
        text = skill_md.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)
        name = meta.get("name", "")
        desc = meta.get("description", "").replace("\n", " ").strip()
        if not name:
            name = skill_md.parent.name
        category = parts[0] if len(parts) > 1 else "(raiz)"
        rows.append((category, name, desc, skill_md.parent))

    lines = [
        "# Índice de skills",
        "",
        "Gerado por `scripts/generate_skill_index.py`. Não edite à mão — regenere após alterar skills.",
        "",
        "| Categoria | Skill | Descrição | Caminho |",
        "|-----------|-------|-----------|---------|",
    ]
    for category, name, desc, folder in sorted(rows, key=lambda r: (r[0], r[1])):
        rel = folder.relative_to(root)
        lines.append(f"| {category} | `{name}` | {desc} | `{rel}/` |")

    out = root / "SKILL_INDEX.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Escrito {out} ({len(rows)} skills)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
