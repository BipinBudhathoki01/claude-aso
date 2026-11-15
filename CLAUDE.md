# CLAUDE.md — Claude AEO Workspace Memory

## Hard Store Constraints (Enforce on Every Edit)

### Google Play Store
- **Title**: max 30 chars (highest ranking weight; ban promotional superlatives like "#1", "Best", "Top").
- **Short Description**: max 80 chars (above-the-fold conversion hook + keyword indexing).
- **Full Description**: max 4000 chars (indexed semantically; use relevant keywords naturally; no fixed density target is established).
- **What's New**: max 500 chars.
- **Android Vitals Bad Behavior Thresholds**: User-perceived Crash Rate <= **1.09%**, ANR Rate <= **0.47%**.
- **Review Replies**: <= 350 chars recommended; never incentivize rating changes.

### Apple App Store
- **Name**: max 30 chars.
- **Subtitle**: max 30 chars.
- **Keyword Field**: max 100 chars, comma-separated with **zero spaces after commas** (`a,b,c`).
- **Zero-Duplication Rule**: Never repeat words across Name, Subtitle, and Keywords.
- **Promotional Text**: max 170 chars (editable without binary review; not indexed).
- **Description**: max 4000 chars (not indexed by Apple Search; optimize for human conversion + LLM GEO).
