# Claude AEO

[![Checks](https://github.com/BipinBudhathoki01/claude-aeo/actions/workflows/ci.yml/badge.svg)](https://github.com/BipinBudhathoki01/claude-aeo/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An open-source skill pack for Google Play and Apple App Store optimization: listing audits, keyword planning, review reply drafts, screenshots, release planning, and AI discovery readiness.

**Use the AI runtime you already have.** This pack contains Markdown instructions and Python helpers, not a hosted AI service or web app. Claude Code uses your configured Claude model; Codex uses your configured model. Other agents can read the same files. No Gemini dependency, additional model API key, or Node.js installation is required. Your runtime's normal subscription, usage limits, permissions, and data handling still apply.

This is an initial community release. Helpers are tested; end-to-end model behavior varies by runtime. Store integrations are documented extension ideas, not working authenticated connectors. The pack drafts recommendations; it does not publish listings or post reviews.

## Install

Clone the repository:

```sh
git clone https://github.com/BipinBudhathoki01/claude-aeo.git
cd claude-aeo
```

### Claude Code

Inside Claude Code:

```text
/plugin marketplace add BipinBudhathoki01/claude-aeo
/plugin install app-store-aeo@claude-aeo-marketplace
```

Use `/app-store-aeo:aeo` for the plugin hub. For manual installation, use `bash install.sh claude` on macOS/Linux or `./install.ps1 -Runtime claude` in PowerShell, restart Claude Code, and use `/aeo`.

### Codex

```sh
bash install.sh codex
```

On Windows PowerShell:

```powershell
./install.ps1 -Runtime codex
```

The installer copies the complete pack into `~/.codex/skills/claude-aeo` (or `$CODEX_HOME/skills/claude-aeo` when configured). Restart Codex, invoke `$claude-aeo`, and ask it to audit your listing. The installer stops if the destination exists; back it up or remove it deliberately before reinstalling.

### Other agents, including Cursor

Open this cloned folder in your agent and ask it to read `SKILL.md` and audit `examples/listing.json`. Keep the whole directory together so scripts, data, and specialist instructions remain available. Native slash commands and parallel agent support depend on your runtime; plain-language requests work without those features.

## Try it

Python 3.10+ is needed only for helpers. No third-party Python dependencies.

```sh
python scripts/aeo_lint.py examples/listing.json
python scripts/ab_test_planner.py 28 10 1500 90
python scripts/launch_checklist.py 2026-12-01
python scripts/fetch_appstore.py 324684580 us
python scripts/competitor_gap.py "focus timer"
```

The last two commands access Apple's public iTunes APIs. The linter exits with code 1 for critical findings and 2 for invalid input. Missing vitals produce a warning rather than an invented healthy metric. The A/B calculator is a planning estimate, not proof of significance.

Example request:

> Read SKILL.md. Audit examples/listing.json for both stores. Run the linter, show character counts for proposed copy, distinguish measured facts from hypotheses, and save a prioritized action plan. Do not publish changes.

## Capabilities

| Request | Purpose |
| --- | --- |
| `aeo audit` | Cross-store audit and prioritized plan |
| `aeo playstore` / `aeo appstore` | Store-specific copy and metadata review |
| `aeo reviews` | Review clustering and reply drafts |
| `aeo keywords` / `aeo competitor` | Keyword and positioning hypotheses |
| `aeo vitals` | Supplied stability metrics and threshold checks |
| `aeo screenshots` / `aeo geo` | Conversion assets and AI discovery readiness |
| `aeo monetization` / `aeo release-notes` | Paywall feedback and release copy |
| `aeo flow` | A staged optimization workflow |

See [commands](docs/COMMANDS.md), [architecture](docs/ARCHITECTURE.md), and [store references](docs/SOURCES.md). Specialists run in parallel only when the agent supports delegation; otherwise apply the checklists sequentially. No ranking improvements or AI citations are guaranteed.

## Contribute

Issues and pull requests are welcome. Useful contributions include evidence-backed store rules, tests, localization guidance, and runtime compatibility fixes. Read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

```sh
python -m unittest discover -s tests -v
```

Never commit credentials, private console exports, or personal review data. See [SECURITY.md](SECURITY.md) for private reporting. MIT licensed; see [LICENSE](LICENSE). Independent project; not affiliated with Anthropic, OpenAI, Google, or Apple.
