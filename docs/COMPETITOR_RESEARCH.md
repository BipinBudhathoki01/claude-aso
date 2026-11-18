# Competitor lookup and ranking research

Use `aso competitor-lookup` to discover relevant rivals and decide what to improve. Use `aso competitor` for a deeper teardown of already-selected rivals. Both use your AI runtime's configured model.

The [fictional worked report](../examples/competitor-research-report.md) shows how to turn a discovery sample into actions and validation checks.

## Live Apple discovery

```sh
python scripts/competitor_lookup.py --term "study timer" --term "focus planner" --country np --target-id 1234567890 --limit 6
```

Replace the fictional target ID `1234567890` with your own app ID before running. The read-only helper uses Apple's public Search/Lookup APIs. It emits JSON with target metadata, candidate listings, source URLs, storefront, capture time, title-word overlap, disclosed ratings/counts, version dates, price labels, and available screenshot URLs. It flags same-publisher results for manual review. Missing values remain null. Up to five distinct queries and one optional target lookup are made per invocation; avoid repeated bulk polling.

`api_result_order` is the order in the API response. It is **not verified App Store organic rank**. The report deliberately sets `ranking_status` to `not_measured`. A target absent from the limited result sample is not necessarily unranked. API metadata does not include private keywords, keyword volume, conversion, or downloads. Pricing labels do not disclose the full subscription/paywall experience.

Exit codes: 0 for successful discovery, 1 for a partial/failed network or target lookup (inspect `errors`), 2 for invalid input. Do not silently interpret failed searches as empty markets. An app's presence in the API does not establish competitive relevance; the agent must inspect it.

## Google Play and actual position evidence

Google Play research uses host browsing tools or supplied screenshots/provider exports. No automatic Play ranking connector is included. If a search page is unavailable, continue with known listing URLs and mark position as unknown.

Record these fields for every measured position:

| Field | Required context |
| --- | --- |
| Store / app ID | Apple or Google Play, exact numeric ID/package |
| Query | Exact search text |
| Country / locale | Matching storefront and language |
| Position | Observed position and whether paid or organic |
| Time | Capture date/time with timezone |
| Device/context | Device, signed-in state if known, filters, personalization limitations |
| Method/source | Store search screenshot or provider export, linked file/URL |

Store observations are contextual samples. Provider ranks remain provider-reported measurements. Do not combine different countries, queries, dates, paid placements, or methods into a claimed trend. Never infer the causal reasons for a ranking from public metadata alone.

## Expected action plan

The agent should connect each recommendation to evidence, a plausible mechanism, effort, and a validation metric:

| Evidence | Possible action | Validation |
| --- | --- | --- |
| A relevant rival explains a supported feature more clearly | Draft clearer benefit copy for our listing | Validate budgets; test conversion with an eligible platform experiment |
| Verified review complaints mention a need our product genuinely solves | Explain that capability in copy/screenshots | Inspect assets and compare conversion; do not fabricate reviews |
| Relevant rivals have materially more ratings in the same storefront | Review our compliant review-request flow | Measure request completion and rating quality; never incentivize ratings |
| Supplied position captures show a query visibility gap | Improve truthful metadata relevance for that intent | Repeat comparable captures and track acquisition/conversion; no promised lift |

These are examples, not findings about any named app. Keyword difficulty, ranking mechanisms, and expected gains remain hypotheses unless independently supported. Copy drafts require the target listing and `aso_lint.py` validation, with character counts. Do not copy competitor branding or claim affiliations.

API reference: [Apple Search API](https://performance-partners.apple.com/search-api), checked 2026-11-15. See [store sources](SOURCES.md) for metadata guidance.
