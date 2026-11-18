# Worked competitor research report

This is a fictional walkthrough. App names, the discovery response, storefront observations,
and measurements below are synthetic. No live store lookup or position measurement was made.

## Discovery and selection

The fictional target, Oriel Study Clock Demo, has focus sessions and scheduled breaks. Its
first screenshot shows the home screen without explaining either feature. We simulate an
Apple Search API response for `study timer` in the US English storefront at
2026-11-15 14:00 UTC. The positions below refer only to rows of that response.

| Evidence | Candidate | API result order | Relevance | Visible listing difference | Organic position |
| --- | --- | ---: | --- | --- | --- |
| E1 | Saffron Sundial Example | 1 | Relevant: timed study sessions | First screenshot identifies both the session and the break | Unknown |
| E2 | Dapple Finch Demo | 2 | Relevant: focus and session history | Subtitle describes tracking completed sessions | Unknown |
| E3 | Marble Pantry Timer Example | 3 | Excluded: kitchen timers | Listing describes cooking intervals | Unknown |
| E4 | Oriel Study Clock Demo | Not in this sample | Target | First screenshot has no session or break caption | Unknown |

**Observed in the scenario:** two candidates serve the study intent. The target already
supports timed sessions and breaks but does not explain that benefit on its first screenshot.
**Hypothesis:** making that benefit easier to spot could improve listing conversion.
**Unknown:** the target's search position, query volume, and all competitors' installs and
conversion. An app missing from this limited response may still appear in store search.

## Actions and validation

| Priority | Evidence | Proposed change | Effort and validation |
| --- | --- | --- | --- |
| 1 | E1, E4 | Add a readable caption about the session and break to the first screenshot | Low. Verify the caption at phone size, then compare product-page conversion in an eligible screenshot experiment. Keep the remaining assets and metadata the same. |
| 2 | E2, E4 | Consider the subtitle **Focus sessions and breaks** (25 / 30 characters) for a later metadata change | Low. Verify that both features are available, run the offline metadata lint, and compare the same query and storefront before and after the change. Record any concurrent releases or campaigns. |

Before changing anything, collect comparable, dated store captures for the target and the two
relevant candidates. Record query, storefront, language, device, signed-in state and whether a
placement is sponsored. If captures are unavailable, keep position unknown. A product-page
experiment addresses conversion. A separate before-and-after visibility comparison is
observational and cannot attribute a change to the subtitle by itself.

[Back to competitor research](../docs/COMPETITOR_RESEARCH.md)
