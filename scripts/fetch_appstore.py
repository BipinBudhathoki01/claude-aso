#!/usr/bin/env python3
"""Fetch live Apple App Store metadata via iTunes Lookup API."""
import json
import sys
import urllib.request
import urllib.parse


def fetch(app_id: str, country: str = "us") -> dict:
    query = urllib.parse.urlencode({"id": app_id, "country": country})
    url = f"https://itunes.apple.com/lookup?{query}"
    with urllib.request.urlopen(url, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if not data.get("results"):
        raise SystemExit(f"No app found for id={app_id}")
    item = data["results"][0]
    return {
        "iosAppId": str(item.get("trackId", app_id)),
        "iosBundleId": item.get("bundleId", ""),
        "iosName": item.get("trackName", ""),
        "developerName": item.get("artistName", ""),
        "category": item.get("primaryGenreName", ""),
        "iosDescription": item.get("description", ""),
        "iosWhatsNew": item.get("releaseNotes", ""),
        "iosRating": item.get("averageUserRating", 0),
        "iosReviewCount": item.get("userRatingCount", 0),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/fetch_appstore.py <app-id> [country]")
        sys.exit(1)
    cid = sys.argv[1]
    cc = sys.argv[2] if len(sys.argv) > 2 else "us"
    print(json.dumps(fetch(cid, cc), indent=2))
