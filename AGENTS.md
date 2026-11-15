# AGENTS.md — Universal Agent Instructions for Claude ASO

This repository provides a cross-runtime App Store Optimization (ASO) and optional AI discovery (GEO) guidance agent toolkit.

## Execution Order
1. Read `data/store-limits.json` for exact platform character limits and Android Vitals thresholds.
2. Run `python3 scripts/aso_lint.py <listing.json>` before proposing copy edits.
3. Consult `skills/aso-*/SKILL.md` and `agents/aso-*.md` for domain-specific audit checklists.
4. Always output `char_count / max_limit` alongside every proposed title, subtitle, short description, and keyword string.
