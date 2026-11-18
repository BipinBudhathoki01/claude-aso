# Command reference

The command map in `data/commands.json` routes natural-language intents to skill files and optional specialist definitions. These are not terminal executables. Plugin invocation: `/app-store-aso:aso <intent>`. Manual Claude: `/aso <intent>`. Codex: invoke `$claude-aso`, then describe the intent.

| Intent | Input | Action |
| --- | --- | --- |
| audit | Listing JSON and optional supporting evidence | Cross-store audit and prioritized plan |
| playstore | Listing JSON | Google Play metadata review |
| appstore | Listing JSON or Apple app ID | Apple metadata review; public lookup when requested |
| reviews | Normalized CSV | Local rating summary, then model-assisted themes and reply drafts |
| keywords | Supplied keywords and listing | Intent and placement hypotheses |
| vitals | Listing JSON with measured percentages | Local threshold checks; missing metrics remain unknown |
| geo | App website URL or supplied page | AI discovery-readiness review, subject to host tools |
| screenshots | Supplied assets | Visual review when supported, otherwise an asset brief |
| competitor-lookup | Target ID/package, queries, storefront, optional rank screenshots/exports | Discover rivals, separate position evidence from API order, and propose measurable actions |
| competitor | App IDs or supplied competitor data | Positioning review without invented rank/volume metrics |
| localization | Listing and target locales | Adapt copy with per-field character counts |
| monetization | Supplied reviews and paywall evidence | Friction review |
| release-notes | Verified changes | Release copy drafts |
| flow | Listing and supporting evidence | Staged audit and experimentation workflow |
| policy | Listing and app behavior evidence | Source-backed policy risks; no approval guarantee |
| experiments | Store, supported surface, traffic and baseline | Test brief and sample-size estimate with assumptions |
| report | Listing JSON | `python scripts/audit_report.py listing.json --format markdown` or `--format json` |
| compare | Before and after listing JSON | `python scripts/listing_diff.py before.json after.json --format markdown` (or `--format json`) |

All workflows preserve the user's configured model. No command authorizes automatic store mutation. See [data formats](DATA_FORMATS.md) and [sources](SOURCES.md).

For Google Play data, see [Play Console performance exports and Android vitals API setup](GOOGLE_PLAY_DATA.md). Listing-performance metrics come from a Play Console CSV export; the optional Reporting API helper returns Android vitals only.
