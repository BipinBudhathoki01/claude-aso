#!/usr/bin/env python3
"""Search live App Store competitors via official iTunes Search API."""
import json
import sys
import urllib.parse
import urllib.request


def search_competitors(term: str, country: str = "us", limit: int = 6) -> list[dict]:
    qs = urllib.parse.urlencode({"term": term, "entity": "software", "country": country, "limit": limit})
    url = f"https://itunes.apple.com/search?{qs}"
    with urllib.request.urlopen(url, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    results = []
    for item in data.get("results", []):
        results.append({
            "appId": str(item.get("trackId", "")),
            "appName": item.get("trackName", ""),
            "developer": item.get("artistName", ""),
            "rating": item.get("averageUserRating", 0),
            "ratingCount": item.get("userRatingCount", 0),
            "genre": item.get("primaryGenreName", ""),
            "price": item.get("formattedPrice", "Free"),
        })
    return results


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "pomodoro timer"
    print(json.dumps(search_competitors(query), indent=2))
