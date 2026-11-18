# Troubleshooting

- **Skill not visible:** restart the runtime. For Codex confirm `SKILL.md`, `scripts/`, and `data/` are together under `$CODEX_HOME/skills/claude-aso` or `~/.codex/skills/claude-aso`. For manual Claude use `~/.claude/skills/aso`.
- **Plugin command not found:** plugin ID is `app-store-aso`; use `/app-store-aso:aso`. Repository and marketplace names differ from the plugin ID.
- **Codex ASO agents not offered:** restart Codex, confirm the profiles exist under `$CODEX_HOME/agents` (default `~/.codex/agents`), and trust the project if Codex requests it. The installer preserves same-named custom profiles. If multi-agent support is unavailable, ask `$claude-aso` to apply the specialists sequentially.
- **Need a local-only audit:** invoke `aso offline-audit` and provide local evidence files. This avoids live data lookups, but Claude/Codex may still send prompts to the model provider configured in the host runtime.
- **Installer destination already exists:** back up custom changes, then deliberately replace the old installation. The installer refuses to overwrite it automatically.
- **PowerShell execution policy blocks the installer:** inspect it first. If you choose to run it, use a process-scoped invocation such as `powershell -ExecutionPolicy Bypass -File ./install.ps1 -Runtime codex`.
- **Python command not found:** install Python 3.10+. Use `python3` on systems where `python` is unavailable.
- **Helper cannot find data:** copy the complete pack rather than isolated Python files. Scripts resolve constraints relative to their installed location.
- **CSV columns differ:** normalize your export to `rating,body,version,store`; only rating and body are required.
- **No delegation or image inspection:** use sequential checklists or an asset brief. Do not report unsupported tools as executed.
- **No browsing:** use supplied evidence and dated sources, clearly noting that current policy or listing data was not verified live.
- **Optional icon/root context warnings in Claude validation:** these do not block the local plugin. The hub reads the bundled rule/source files explicitly. A marketplace catalog icon is future polish.

Use `bash uninstall.sh` to print removal guidance. It does not delete files automatically. For installed plugins, use `/plugin uninstall app-store-aso@claude-aso-marketplace`.
