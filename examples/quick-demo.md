# Reproduce the local demo

All input is fictional. The animation in the README is a styled rendering of actual helper output, not a store screenshot or a claim of ranking improvement.

## Before

```sh
python scripts/aso_lint.py examples/listing-before.json
```

Expected exit: 1. Findings:

- CRITICAL: `playTitle length 49/30`
- WARNING: `Redundant keyword words: focus, study, timer`

The Play title is `Focus Garden: Study Timer and Daily Habit Tracker` (49 / 30 characters). The Apple keyword string is `focus,timer,focus,study` (23 / 100 characters), which wastes space repeating words in the name/subtitle and itself.

## After

```sh
python scripts/aso_lint.py examples/listing.json
```

Expected exit: 0. Output: `issue_count: 0`, `issues: []`.

The corrected Play title is `Focus Garden: Study Timer` (25 / 30 characters). The Apple keyword string is `pomodoro,concentration,revision,routine` (39 / 100 characters).

## Inspect the changes and report

```sh
python scripts/listing_diff.py examples/listing-before.json examples/listing.json
python scripts/listing_diff.py examples/listing-before.json examples/listing.json --format markdown
python scripts/audit_report.py examples/listing.json --format markdown
```

All other fields and supplied sample vitals are unchanged. The result demonstrates metadata validation, not complete submission readiness. Use your AI runtime to review positioning, screenshots, policy evidence, and experiment ideas separately.
