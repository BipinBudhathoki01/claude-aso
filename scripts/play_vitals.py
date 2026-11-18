#!/usr/bin/env python3
"""Fetch crash and ANR trends from the Google Play Developer Reporting API."""
import argparse
from datetime import date
import json
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SCOPE = "https://www.googleapis.com/auth/playdeveloperreporting"
BASE_URL = "https://playdeveloperreporting.googleapis.com/v1beta1"
PACKAGE_RE = re.compile(r"^[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)+$")


def query_metric(access_token: str, package: str, metric_set: str, metric_names: list[str],
                 start: date, end: date, opener=urlopen) -> list[dict]:
    url = f"{BASE_URL}/apps/{package}/{metric_set}:query"
    body = json.dumps({
        "timelineSpec": {
            "aggregationPeriod": "DAILY",
            "startTime": {"year": start.year, "month": start.month, "day": start.day, "timeZone": "America/Los_Angeles"},
            "endTime": {"year": end.year, "month": end.month, "day": end.day, "timeZone": "America/Los_Angeles"},
        },
        "metrics": metric_names,
        "pageSize": 1000,
    }).encode("utf-8")
    rows = []
    page_token = None
    while True:
        payload = json.loads(body)
        if page_token:
            payload["pageToken"] = page_token
        request = Request(url, data=json.dumps(payload).encode("utf-8"), headers={
            "Authorization": f"Bearer {access_token}", "Content-Type": "application/json",
        }, method="POST")
        try:
            with opener(request, timeout=30) as response:
                result = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ValueError(f"Google Play Reporting API returned HTTP {exc.code}: {detail[:1000]}") from None
        except URLError as exc:
            raise ValueError(f"Could not reach Google Play Reporting API: {exc.reason}") from None
        rows.extend(result.get("rows", []))
        page_token = result.get("nextPageToken")
        if not page_token:
            break
    return rows


def fetch_vitals(access_token: str, package: str, start: date, end: date, opener=urlopen) -> dict:
    if not PACKAGE_RE.fullmatch(package):
        raise ValueError("Package name must look like com.example.app")
    if end < start:
        raise ValueError("End date must be on or after start date")
    return {
        "scope": "Google Play Developer Reporting API Android vitals only; this API result does not include store-listing visitors or conversion rate.",
        "package_name": package,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "timezone": "America/Los_Angeles",
        "crash_rate_rows": query_metric(access_token, package, "crashRateMetricSet", ["crashRate", "distinctUsers"], start, end, opener),
        "anr_rate_rows": query_metric(access_token, package, "anrRateMetricSet", ["anrRate", "distinctUsers"], start, end, opener),
    }


def _access_token() -> str:
    try:
        import google.auth
        from google.auth.exceptions import GoogleAuthError
        from google.auth.transport.requests import Request as GoogleAuthRequest
    except ImportError:
        raise ValueError("Install optional dependencies with: python -m pip install -r requirements-google-play.txt") from None
    try:
        credentials, _ = google.auth.default(scopes=[SCOPE])
        credentials.refresh(GoogleAuthRequest())
    except GoogleAuthError as exc:
        raise ValueError(f"Google authentication failed: {exc}") from None
    if not credentials.token:
        raise ValueError("Google credentials did not provide an access token")
    return credentials.token


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", required=True, help="App package name, for example com.example.app")
    parser.add_argument("--start", required=True, type=date.fromisoformat, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", required=True, type=date.fromisoformat, help="End date (YYYY-MM-DD)")
    args = parser.parse_args()
    try:
        report = fetch_vitals(_access_token(), args.package, args.start, args.end)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
