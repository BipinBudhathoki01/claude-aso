# Claude Code and Codex agent orchestration

Claude ASO is a portable set of focused ASO instructions, not a hosted agent service. The hub uses the model already selected by Claude Code or Codex. Native delegation creates focused agent contexts; it does not add a model provider or guarantee separate model capacity.

## Claude Code

Install the Claude ASO plugin using the README's marketplace instructions. The plugin's `agents/` directory contains Claude Code subagent definitions. During `aso audit`, the hub chooses only roles relevant to supplied evidence and delegates independent checks when native subagents are available. Use `aso offline-audit` to run the dedicated local-only workflow; it applies checklists sequentially and its agent definition has no web-fetch tool.

The manual Claude skill installer places the pack under `~/.claude/skills/aso`. In that setup, the hub falls back to sequential specialist checklists unless the user separately configures native agents. For native Claude subagents, the plugin installation is the supported path.

## Codex

Run `bash install.sh codex` or `./install.ps1 -Runtime codex`. The skill installs under `$CODEX_HOME/skills/claude-aso` (default `~/.codex/skills/claude-aso`); custom specialist TOML profiles install under `$CODEX_HOME/agents`. Existing files with the same names are preserved and reported instead of overwritten.

Codex profiles omit `model` and provider settings, so spawned agents inherit the active Codex model and permissions. Instruct the hub to use relevant roles such as `aso_playstore`, `aso_appstore`, `aso_reviews`, or `aso_vitals`. Codex only delegates when multi-agent support is enabled in the user's runtime and project is trusted. If those profiles are not loaded or delegation is unavailable, the hub applies the same Markdown specialist checklists sequentially.

## Shared audit contract

The coordinator sends each role its evidence, exact question, and the format in [`templates/agent-audit-result.md`](../templates/agent-audit-result.md). Each role returns findings, unknowns, hypotheses, actions, and checks performed. The coordinator deduplicates results, retains evidence references, and reports only work that ran.

## Offline data mode

Run `aso offline-audit <local files>` to restrict evidence gathering to supplied files and bundled repository references. The route must not use WebFetch/search, public store APIs, the Google Play Reporting API, or authenticated integrations. It may run local helpers for metadata, review CSVs, listing comparisons, and Play Console exports. It must not run `scripts/play_vitals.py`, which makes a Google API request.

Offline mode describes data collection, not inference. Claude Code or Codex may send prompts to its configured hosted model. Codex sandbox and network permissions remain controlled by the user's local configuration; repository instructions cannot override them.

This repository's automated checks validate route references and Codex TOML syntax, but cannot prove agent discovery or delegation in a user's freshly restarted Claude Code or Codex runtime. Record such runtime compatibility separately with the version, OS, install path, invocation, and observed delegation or fallback.
