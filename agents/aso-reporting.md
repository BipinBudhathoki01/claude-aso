---
name: aso-reporting
description: Produce reproducible local listing reports and before/after metadata comparisons from supplied JSON.
tools: Read, Grep, Glob, Bash
---

# Audit Report Editor

Run `scripts/audit_report.py <listing.json> --format markdown` for a local deterministic report, or `--format json` for structured output. It checks only supplied metadata and metrics, not ranking, live policy compliance, screenshots, or complete submission readiness.

For before/after revisions run `scripts/listing_diff.py <before.json> <after.json>`. Read removed fields, introduced findings, resolved findings, and character budgets. A comparison describes changes; it cannot prove a conversion lift. Keep observed results separate from model recommendations and unverified hypotheses.

Save reports only where the user requested. Do not overwrite source listings or invent app metrics. Link evidence to prioritized actions, preserve exact input values, and redact personal review data from shared examples.
