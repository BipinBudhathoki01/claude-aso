# Input and output formats

## Listing JSON

Use a JSON object like `examples/listing.json`. Supported text keys are `playTitle`, `playShortDescription`, `playFullDescription`, `playWhatsNew`, `iosName`, `iosSubtitle`, `iosKeywords`, `iosPromotionalText`, `iosDescription`, and `iosWhatsNew`. Limits come from `data/store-limits.json`.

Partial listings are accepted. Reports explicitly list missing text fields. Missing metrics are unknown, not assumed healthy. Supply `playCrashRatePct` and `playAnrRatePct` as numeric percentages, for example `0.4` for 0.4%, not `0.004`. Counts use Unicode code points; the store console is the final validator.

`aso_lint.py` exits 0 for no critical findings, 1 for critical findings, and 2 for invalid input. Report, comparison, and review-summary helpers exit 0 when a report was generated, even if it includes findings, and 2 for invalid input. Inspect their structured results; report generation is not a release gate.

`listing_diff.py` reports added, modified, and removed fields, the exact before/after values, character counts where applicable, introduced/resolved lint findings, and all remaining findings. Resolved findings can result from removing a field; inspect removals before concluding the new listing is better. Comparisons include source text: redact private data before sharing.

## Review CSV

Normalize exports to UTF-8 CSV with a header. UTF-8 BOM and quoted multiline fields are accepted. Required columns: `rating` (integer 1–5) and `body`. Optional columns: `version`, `store`. Other columns are ignored. No store-native CSV schema is assumed.

```csv
rating,body,version,store
5,"A clear timer for study sessions.",1.2.0,playstore
2,"Timer stopped when the screen locked.",1.2.0,playstore
```

The helper reports sample count, mean rating, 1–2 star count, and counts by rating/version/store. Empty exports return zero counts and a null average. Invalid ratings or malformed rows stop with an error. Review bodies are not included in the aggregate output. The sample is not necessarily representative of the app's full user base.

No topic detection or sentiment inference is performed by the CSV helper. Ask your existing AI runtime to interpret the supplied text separately when needed.
