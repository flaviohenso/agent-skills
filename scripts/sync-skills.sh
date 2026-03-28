#!/usr/bin/env bash
# Sincroniza todas as skills deste repositório para o diretório da CLI alvo.
# Uso:
#   ./scripts/sync-skills.sh cursor
#   ./scripts/sync-skills.sh gemini
#   ./scripts/sync-skills.sh claude [DIR_PROJETO]   # default: pwd

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-}"
DEST_BASE=""

case "$TARGET" in
  cursor)
    DEST_BASE="${HOME}/.cursor/skills"
    ;;
  gemini)
    DEST_BASE="${HOME}/.gemini/skills"
    ;;
  claude)
    PROJ="${2:-$PWD}"
    DEST_BASE="${PROJ}/.claude/skills"
    ;;
  *)
    echo "Uso: $0 cursor|gemini|claude [DIR_PROJETO_para_claude]" >&2
    exit 1
    ;;
esac

mkdir -p "$DEST_BASE"

shopt -s globstar nullglob
count=0
for skill_md in "$ROOT"/*/**/SKILL.md; do
  dir=$(dirname "$skill_md")
  rel="${dir#$ROOT/}"
  case "$rel" in
    _templates/*|docs/*|scripts/*|.github/*)
      continue
      ;;
  esac
  # skill folder = basename of directory containing SKILL.md
  name=$(basename "$dir")
  if [[ "$name" == "skill-template" ]]; then
    continue
  fi
  dest="$DEST_BASE/$name"
  rm -rf "$dest"
  cp -a "$dir" "$dest"
  echo "-> $dest"
  count=$((count + 1))
done

echo "Sincronizadas $count skills em $DEST_BASE"
