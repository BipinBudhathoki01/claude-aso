#!/usr/bin/env python3
"""Aggregate a normalized review CSV locally without exporting review text."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import sys


def summarize(path: Path) -> dict:
    ratings = Counter()
    versions = Counter()
    stores = Counter()
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        if not reader.fieldnames or not {"rating", "body"} <= set(reader.fieldnames):
            raise ValueError("CSV requires rating and body columns; optional: version, store")
        for line, row in enumerate(reader, 2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"Malformed CSV row near record {line}")
            try:
                rating = int(row["rating"])
            except ValueError:
                raise ValueError(f"Rating must be an integer from 1 to 5 near record {line}") from None
            if not 1 <= rating <= 5:
                raise ValueError(f"Rating must be from 1 to 5 near record {line}")
            ratings[rating] += 1
            versions[row.get("version", "").strip() or "unspecified"] += 1
            stores[row.get("store", "").strip() or "unspecified"] += 1
    total = sum(ratings.values())
    return {
        "scope": "Counts from supplied CSV only; no sentiment inference or population estimate.",
        "total_reviews": total,
        "average_rating": round(sum(r * count for r, count in ratings.items()) / total, 3) if total else None,
        "low_rating_count": ratings[1] + ratings[2],
        "rating_counts": {str(r): ratings[r] for r in range(1, 6)},
        "version_counts": dict(sorted(versions.items())), "store_counts": dict(sorted(stores.items())),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    args = parser.parse_args()
    try:
        report = summarize(args.csv)
    except (OSError, ValueError, csv.Error) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
