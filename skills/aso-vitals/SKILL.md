---
name: aso-vitals
description: Audit Crash Rate (<=1.09%) and ANR Rate (<=0.47%) before running ASO copy experiments.
---

# Skill: Store Vitals & Technical Health
Never ship keyword optimization alone if Android Vitals breaches bad-behavior thresholds.

When a user has Google Play Developer Reporting API access, they can run `scripts/play_vitals.py` for dated crash and ANR data. Treat API data as vitals only; store listing visitors, clicks, and CTR must come from a supplied Play Console export. Keep date range, timezone, dimensions, and missing data visible in the report.
