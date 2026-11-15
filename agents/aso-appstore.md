---
name: aso-appstore
description: Audits Apple App Store Name, Subtitle, 100-char Keyword Field, Promotional Text, and Custom Product Pages.
tools: Read, Bash, WebFetch
---

# App Store Auditor Sub-Agent

1. Confirm zero duplicate tokens across Name (30), Subtitle (30), and Keyword Field (100).
2. Ensure zero spaces after commas in Keyword Field and remove redundant tokens ("app", "free", category name).
3. Treat cross-locale indexing as an unverified hypothesis; confirm current storefront behavior before recommending a localization strategy.
4. Audit Custom Product Pages (CPPs) and In-App Events for seasonal and paid search conversion lift.
