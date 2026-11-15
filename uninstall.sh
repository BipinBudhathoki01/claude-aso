#!/usr/bin/env bash
set -euo pipefail
echo 'Remove only the directory created by the installer after backing up custom changes:'
echo 'Claude Code: ~/.claude/skills/aeo'
echo 'Codex: ${CODEX_HOME:-~/.codex}/skills/claude-aeo'
echo 'For plugin installation use /plugin uninstall app-store-aeo@claude-aeo-marketplace.'
echo 'No files were removed.'
