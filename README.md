# Claude AEO

Open-source app store optimization inside the AI agent you already use.

[![Checks](https://github.com/BipinBudhathoki01/claude-aeo/actions/workflows/ci.yml/badge.svg)](https://github.com/BipinBudhathoki01/claude-aeo/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/BipinBudhathoki01/claude-aeo)](https://github.com/BipinBudhathoki01/claude-aeo/releases)

[Quick start](#quick-start) · [Agents](#meet-the-agents) · [Commands](#commands) · [Examples](#see-the-output) · [FAQ](#faq) · [Contribute](#contribute)

Audit Google Play and Apple App Store listings, find wasted keyword space, review stability metrics, organize user feedback, and prepare a measurable improvement plan.

**13 specialist agents · 15 specialist skills + 1 hub · 17 command intents · 8 Python helpers**

Claude Code uses your configured Claude model. Codex uses your configured model. Other compatible agents can read the same skill files. No mandatory model API key, Gemini dependency, web app, or hosted service. Your host runtime's normal billing, permissions, and data handling apply.

## What it does

- **Listing checks:** supplied character budgets, keyword redundancy, release copy, and store-specific recommendations.
- **Reviews:** model-assisted issue clustering and reply drafts, plus local CSV rating/version summaries.
- **Discovery:** keyword intent, competitor positioning, localization, and AI citation-readiness checklists.
- **Conversion:** screenshot briefs, monetization feedback, and experiment plans with explicit assumptions.
- **Policy and quality:** source-backed claim review and checks against supplied Android vitals.
- **Reports:** reproducible Markdown/JSON metadata reports and before/after listing comparisons.

This is an early community release. The helpers are tested; model judgment and runtime behavior need real-world validation. Recommendations require human review. No ranking gains, store approval, or AI citations are guaranteed.

## Quick start

### Claude Code plugin

Run inside Claude Code:

```text
/plugin marketplace add BipinBudhathoki01/claude-aeo
/plugin install app-store-aeo@claude-aeo-marketplace
```

Then ask the plugin hub:

```text
/app-store-aeo:aeo audit /absolute/path/to/listing.json
```

The plugin ID is `app-store-aeo`; the repository is `claude-aeo`. This avoids Claude's reserved third-party plugin-name prefix.

### Codex

Clone the pack:

```sh
git clone https://github.com/BipinBudhathoki01/claude-aeo.git
cd claude-aeo
```

Install on macOS/Linux:

```sh
bash install.sh codex
```

Or Windows PowerShell:

```powershell
./install.ps1 -Runtime codex
```

Restart Codex, invoke `$claude-aeo`, and ask it to audit your listing file. The full pack installs to `~/.codex/skills/claude-aeo`, respecting `CODEX_HOME` when set. It inherits the model configured in Codex.

### Claude Code manual installation

From the cloned repository, run `bash install.sh claude` or `./install.ps1 -Runtime claude`, restart Claude Code, and use `/aeo`. The complete pack installs to `~/.claude/skills/aeo`.

### Cursor and other agents

Open the cloned directory in your agent and ask it to read `SKILL.md`. Keep the complete pack together. Native discovery, slash commands, and delegation vary by runtime; equivalent plain-language requests work without those features.

Both installers refuse to overwrite an existing destination. Back up custom changes before deliberately replacing an installation. See [troubleshooting](docs/TROUBLESHOOTING.md).

## Meet the agents

These are specialist instruction files, not 13 separately hosted models. The host controls model choice, tool access, and concurrency. Only relevant specialists are needed for a task.

| Agent | Role | Command intent |
| --- | --- | --- |
| [`aeo-playstore`](agents/aeo-playstore.md) | Google Play metadata reviewer | `aeo playstore` |
| [`aeo-appstore`](agents/aeo-appstore.md) | Apple metadata and keywords reviewer | `aeo appstore` |
| [`aeo-reviews`](agents/aeo-reviews.md) | Review themes and reply drafts | `aeo reviews` |
| [`aeo-keywords`](agents/aeo-keywords.md) | Keyword intent strategist | `aeo keywords` |
| [`aeo-vitals`](agents/aeo-vitals.md) | Stability metrics reviewer | `aeo vitals` |
| [`aeo-geo`](agents/aeo-geo.md) | AI discovery readiness reviewer | `aeo geo` |
| [`aeo-screenshots`](agents/aeo-screenshots.md) | Screenshot conversion reviewer | `aeo screenshots` |
| [`aeo-competitor`](agents/aeo-competitor.md) | Competitor positioning analyst | `aeo competitor` |
| [`aeo-localization`](agents/aeo-localization.md) | Locale and language strategist | `aeo localization` |
| [`aeo-monetization`](agents/aeo-monetization.md) | Paywall feedback reviewer | `aeo monetization` |
| [`aeo-policy`](agents/aeo-policy.md) | Source-backed store policy reviewer | `aeo policy` |
| [`aeo-experiments`](agents/aeo-experiments.md) | Experiment planner | `aeo experiments` |
| [`aeo-reporting`](agents/aeo-reporting.md) | Metadata reports and revision comparisons | `aeo report`, `aeo compare` |

The 15 specialist skills add release-note and FLOW workflows alongside these roles. One hub routes requests. A full audit can delegate relevant checks when the runtime supports agents; otherwise it applies the same checklists sequentially. It must report only work actually performed.

## Commands

These are agent request intents. In the Claude plugin, append the intent after `/app-store-aeo:aeo`; in a manual Claude install, use `/aeo`; in Codex invoke `$claude-aeo` and ask in plain language. Terminal helpers appear in the next section.

| Intent and input | Output |
| --- | --- |
| `aeo audit listing.json` | Prioritized cross-store findings and evidence gaps |
| `aeo playstore listing.json` | Play listing recommendations and character counts |
| `aeo appstore listing.json` | Apple listing and keyword recommendations |
| `aeo reviews reviews.csv` | Rating summary, model-generated themes, reply drafts |
| `aeo keywords seed-list` | Intent and placement hypotheses |
| `aeo vitals listing.json` | Supplied metric threshold checks |
| `aeo geo app-url` | Citation-readiness and structured-data review |
| `aeo screenshots asset-directory` | Asset review when image tools are available; otherwise a brief |
| `aeo competitor app-ids` | Evidence-backed comparison; public Apple lookup helpers available |
| `aeo localization listing.json` | Locale priorities and localized copy drafts |
| `aeo monetization reviews.csv` | Paywall friction and positioning review |
| `aeo release-notes listing.json` | Release-note drafts |
| `aeo flow listing.json` | Staged optimization plan |
| `aeo policy listing.json` | Policy-risk table with sources and confidence |
| `aeo experiments listing.json` | Test brief, feasibility, assumptions, and guardrails |
| `aeo report listing.json` | Offline Markdown/JSON metadata report |
| `aeo compare before.json after.json` | Changed fields, budgets, introduced/resolved findings |

[Full command reference](docs/COMMANDS.md) · [Routing map](data/commands.json)

## See the output

Try the helpers without any AI account. Python 3.10+ is required; no third-party Python packages are needed.

```sh
python scripts/aeo_lint.py examples/listing.json
python scripts/audit_report.py examples/listing.json --format markdown
python scripts/audit_report.py examples/listing.json --format json
python scripts/listing_diff.py before.json after.json
python scripts/review_summary.py examples/reviews.csv
```

The included sample produces these real character budgets:

| Field | Used / limit |
| --- | --- |
| Play title | 25 / 30 |
| Play short description | 67 / 80 |
| Apple name | 12 / 30 |
| Apple subtitle | 28 / 30 |
| Apple keywords | 39 / 100 |

[View the generated sample report](examples/audit-report.md) · [Sample listing](examples/listing.json) · [Sample reviews](examples/reviews.csv)

The review CSV sample contains 3 synthetic reviews, with an average rating of 3.667 and one 1–2 star review. The helper aggregates data; theme and sentiment interpretation belongs to the user's model. Reports check supplied fields only, not full submission readiness.

Other helpers:

```sh
python scripts/ab_test_planner.py 28 10 1500 90
python scripts/launch_checklist.py 2026-12-01
python scripts/fetch_appstore.py 324684580 us
python scripts/competitor_gap.py "focus timer"
```

The final two access Apple's public iTunes APIs. The sample-size calculator is a rough planning estimate, not a significance test. See [data formats](docs/DATA_FORMATS.md) and [store sources](docs/SOURCES.md).

## How it works

```mermaid
flowchart LR
    Input[Listing JSON / reviews / assets] --> Host[Your existing AI runtime]
    Host --> Hub[AEO hub]
    Hub --> Checks[Local Python checks]
    Hub --> Specialists[Relevant specialist checklists]
    Checks --> Report[Evidence and draft action plan]
    Specialists --> Report
    Report --> Review[Your review and decision]
```

[Architecture](docs/ARCHITECTURE.md) · [Changelog](CHANGELOG.md)

## FAQ

**Is it free?** The pack is MIT licensed. Your AI runtime, model subscription, or provider may charge for use. Offline helpers do not call a model.

**Does it choose Claude, Codex, or another model?** Your runtime chooses. The pack does not force a model or add an AI provider dependency.

**Does it connect to my store account?** No. Authenticated Play Console and App Store Connect connectors are future extension ideas. Public Apple lookup is included. No automatic listing publication, review posting, or experiment creation is included.

**Does it collect data?** Local validation and reporting helpers make no network requests. The Apple helpers send supplied IDs or search terms to Apple. The host agent may send your input to its configured model provider. Redact private data before sharing reports.

**Can all agents run at once?** Only if the host supports it, permits it, and has capacity. The pack supports sequential fallback and makes no fixed parallelism or runtime promises.

**What has been tested?** There are 23 automated tests for helpers, invalid inputs, routing, installer behavior, and metadata boundaries. CI covers Windows/Linux with Python 3.10/3.13. Plugin validation also runs locally; real model output quality remains a separate review task.

## Contribute

Help with real-world runtime testing, source-backed policy updates, useful audit examples, localization, or future read-only store connectors.

- [Report a bug or suggest a feature](https://github.com/BipinBudhathoki01/claude-aeo/issues)
- [Discuss workflows](https://github.com/BipinBudhathoki01/claude-aeo/discussions)
- Read [contribution guidance](CONTRIBUTING.md), [community conduct](CODE_OF_CONDUCT.md), and [security reporting](SECURITY.md).

```sh
python -m unittest discover -s tests -v
```

MIT licensed. Independent project maintained by [Bipin Budhathoki](https://github.com/BipinBudhathoki01) and contributors; not affiliated with Anthropic, OpenAI, Google, or Apple.
