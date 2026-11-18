#!/usr/bin/env bash
set -euo pipefail
runtime="${1:-claude}"
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
case "$runtime" in
  claude) default_root="${HOME}/.claude/skills"; name="aso" ;;
  codex) default_root="${CODEX_HOME:-${HOME}/.codex}/skills"; name="claude-aso" ;;
  *) echo "Usage: bash install.sh [claude|codex] [destination-skills-directory]" >&2; exit 2 ;;
esac
destination_root="${2:-$default_root}"
target="${destination_root}/${name}"
if [ -e "$target" ]; then
  echo "Destination already exists: $target. Back it up or remove it before reinstalling." >&2
  exit 1
fi
mkdir -p "$target"
for entry in SKILL.md CLAUDE.md AGENTS.md LICENSE requirements-google-play.txt skills agents data scripts templates extensions docs examples; do
  cp -R "${script_dir}/${entry}" "$target/"
done
if [ "$runtime" = "claude" ]; then
  cp "${script_dir}/skills/aso/SKILL.md" "$target/SKILL.md"
fi
echo "Installed to $target. Restart your AI runtime to discover the skill."
