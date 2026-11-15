#!/usr/bin/env python3
"""Check supplied store metadata; exit 1 for critical issues, 2 for bad input."""
import json
import math
import re
import sys
from pathlib import Path

LIMITS = json.loads((Path(__file__).resolve().parents[1] / "data/store-limits.json").read_text(encoding="utf-8"))
FIELDS = {
    "playTitle": ("playStore", "titleMax"),
    "playShortDescription": ("playStore", "shortDescriptionMax"),
    "playFullDescription": ("playStore", "fullDescriptionMax"),
    "playWhatsNew": ("playStore", "whatsNewMax"),
    "iosName": ("appStore", "nameMax"),
    "iosSubtitle": ("appStore", "subtitleMax"),
    "iosKeywords": ("appStore", "keywordsMax"),
    "iosPromotionalText": ("appStore", "promotionalTextMax"),
    "iosDescription": ("appStore", "descriptionMax"),
    "iosWhatsNew": ("appStore", "whatsNewMax"),
}


def lint_listing(data: dict) -> list[dict]:
    if not isinstance(data, dict):
        raise ValueError("Listing must be a JSON object")
    issues = []
    for field, (store, key) in FIELDS.items():
        if field not in data:
            continue
        value = data[field]
        if not isinstance(value, str):
            raise ValueError(f"{field} must be a string")
        limit = LIMITS[store][key]
        if len(value) > limit or (field in ("playTitle", "iosName") and not value.strip()):
            issues.append({"store": store.lower(), "severity": "CRITICAL", "msg": f"{field} length {len(value)}/{limit}"})
    if not any(field in data for field in FIELDS):
        raise ValueError("Provide at least one supported listing field")

    thresholds = LIMITS["playStore"]["vitalsThresholds"]
    for field, key in (("playCrashRatePct", "crashRateMaxPct"), ("playAnrRatePct", "anrRateMaxPct")):
        if field not in data:
            if any(name.startswith("play") for name in data):
                issues.append({"store": "playstore", "severity": "WARNING", "msg": f"{field} not supplied; stability is unknown"})
            continue
        raw = data[field]
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not math.isfinite(raw) or not 0 <= raw <= 100:
            raise ValueError(f"{field} must be a finite percentage between 0 and 100")
        if raw >= thresholds[key]:
            issues.append({"store": "playstore", "severity": "CRITICAL", "msg": f"{field} {raw}% meets/exceeds {thresholds[key]}% bad-behavior threshold"})

    keywords = data.get("iosKeywords", "")
    if re.search(r",\s+", keywords):
        issues.append({"store": "appstore", "severity": "WARNING", "msg": "Remove spaces after commas in iosKeywords."})
    headers = set(re.findall(r"[^\W_]+", f"{data.get('iosName', '')} {data.get('iosSubtitle', '')}".casefold()))
    seen = set()
    duplicates = set()
    for token in re.findall(r"[^\W_]+", keywords.casefold()):
        if token in headers or token in seen:
            duplicates.add(token)
        seen.add(token)
    if duplicates:
        issues.append({"store": "appstore", "severity": "WARNING", "msg": "Redundant keyword words: " + ", ".join(sorted(duplicates))})
    return issues


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/aso_lint.py <listing.json>", file=sys.stderr)
        return 2
    try:
        payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8-sig"))
        findings = lint_listing(payload)
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps({"issue_count": len(findings), "issues": findings}, indent=2))
    return 1 if any(item["severity"] == "CRITICAL" for item in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
