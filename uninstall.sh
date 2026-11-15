#!/usr/bin/env bash
set -euo pipefail
echo 'Remove only the directory created by the installer after backing up custom changes:'
echo 'Claude Code: ~/.claude/skills/aso'
echo 'Codex: ${CODEX_HOME:-~/.codex}/skills/claude-aso'
echo 'For plugin installation use /plugin uninstall app-store-aso@claude-aso-marketplace.'
echo 'No files were removed.'
