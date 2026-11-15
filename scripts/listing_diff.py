#!/usr/bin/env python3
"""Compare supplied listings and identify introduced or resolved lint findings."""
import argparse
import json
from pathlib import Path
import sys

from aso_lint import FIELDS, LIMITS, lint_listing


def compare(before: dict, after: dict) -> dict:
    old_findings, new_findings = lint_listing(before), lint_listing(after)
    changes = []
    for field in sorted(before.keys() | after.keys()):
        if field in before and field in after and before[field] == after[field]:
            continue
        row = {"field": field, "change": "added" if field not in before else "removed" if field not in after else "modified",
               "before": before.get(field), "after": after.get(field)}
        if field in FIELDS:
            store, key = FIELDS[field]
            row["limit"] = LIMITS[store][key]
            row["before_count"] = len(before[field]) if field in before else None
            row["after_count"] = len(after[field]) if field in after else None
        changes.append(row)
    return {
        "scope": "Supplied file comparison only; changes do not establish conversion or ranking lift.",
        "changes": changes,
        "introduced_findings": [f for f in new_findings if f not in old_findings],
        "resolved_findings": [f for f in old_findings if f not in new_findings],
        "after_findings": new_findings,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    args = parser.parse_args()
    try:
        report = compare(*(json.loads(p.read_text(encoding="utf-8-sig")) for p in [args.before, args.after]))
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
