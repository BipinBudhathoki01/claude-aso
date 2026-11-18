# Google Play performance data

This pack supports two different Play Console data sources. Keep their metrics clearly labeled:

1. **Listing performance exports** report store listing visitors and a listing rate. Google documents the Store listing performance and Statistics pages as exportable in Play Console. Export a CSV from the relevant report, then run:

   ```sh
   python scripts/play_listing_performance.py path/to/export.csv --format markdown
   ```

   The importer accepts `Date`, `Store listing visitors`, and either `Click-through rate` or the legacy `Store listing conversion rate`. Decimal rates from 0 to 1 are interpreted as fractions (`0.12` = 12%); a trailing `%` or a numeric value above 1 is interpreted as a percentage. It keeps segmented rows separate and omits totals when multiple rows share a date, avoiding accidental double-counting. The summary is descriptive and does not establish why a metric changed.

2. **Android vitals from the Google Play Developer Reporting API** report app-quality data such as crash and ANR rates. This API does not supply store listing visitors or listing conversion/CTR. To use it:

   - Create a Google Cloud project and enable the [Google Play Developer Reporting API](https://developers.google.com/play/developer/reporting/overview).
   - Create a service account, then grant it the minimum required Play Console reporting permission for the app.
   - Keep the service-account JSON outside the repository and set `GOOGLE_APPLICATION_CREDENTIALS` to its local path.
   - Install the optional client authentication dependency: `python -m pip install -r requirements-google-play.txt`.
   - Query daily crash and ANR rates:

     ```sh
     python scripts/play_vitals.py --package com.example.app --start 2026-11-01 --end 2026-11-07
     ```

The API helper uses Google Application Default Credentials with the read-only `playdeveloperreporting` OAuth scope. Daily points use Google's documented `America/Los_Angeles` time zone. Credentials and API responses stay on the user's machine; neither helper publishes data or changes a Play listing.

The included [`play-listing-performance.csv`](../examples/play-listing-performance.csv) is synthetic data for demonstration. See [Google's listing performance report guide](https://support.google.com/googleplay/android-developer/answer/9859173) and [metric query reference](https://developers.google.com/play/developer/reporting/metricset-queries) for current platform details.
