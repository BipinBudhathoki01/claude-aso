#!/usr/bin/env python3
"""Create offline metadata reports; no model or network access required."""
import argparse
import json
from pathlib import Path
import sys

from aso_lint import FIELDS, LIMITS, lint_listing


def build_report(listing: dict) -> dict:
    findings = lint_listing(listing)
    budgets = []
    for field, (store, key) in FIELDS.items():
        if field in listing:
            limit = LIMITS[store][key]
            budgets.append({"field": field, "count": len(listing[field]), "limit": limit,
                            "remaining": limit - len(listing[field])})
    return {
        "scope": "Offline checks of supplied metadata only; no ranking or policy approval assessment.",
        "status": "critical_findings" if any(f["severity"] == "CRITICAL" for f in findings)
                  else "warnings" if findings else "no_findings_in_supplied_fields",
        "budgets": budgets,
        "missing_fields": [field for field in FIELDS if field not in listing],
        "findings": findings,
    }


def markdown(report: dict) -> str:
    def cell(value):
        return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ").replace("<", "&lt;").replace(">", "&gt;")
    lines = ["# Listing metadata report", "", report["scope"], "", f"Status: `{report['status']}`", "",
             "| Field | Characters | Remaining |", "| --- | --- | --- |"]
    for row in report["budgets"]:
        lines.append(f"| {row['field']} | {row['count']} / {row['limit']} | {row['remaining']} |")
    lines += ["", "## Findings", ""]
    lines += [f"- **{f['severity']}** ({f['store']}): {cell(f['msg'])}" for f in report["findings"]] or ["No findings in supplied fields."]
    if report["missing_fields"]:
        lines += ["", "Fields not supplied: " + ", ".join(report["missing_fields"])]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("listing", type=Path)
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()
    try:
        report = build_report(json.loads(args.listing.read_text(encoding="utf-8-sig")))
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2) if args.format == "json" else markdown(report), end="\n" if args.format == "json" else "")
    return 0


if __name__ == "__main__":
    sys.exit(main())
