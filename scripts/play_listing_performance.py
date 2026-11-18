#!/usr/bin/env python3
"""Summarize a Google Play Console store-listing performance CSV export."""
import argparse
import csv
from datetime import date
import json
from pathlib import Path
import re
import sys


DATE_HEADERS = {"date"}
VISITOR_HEADERS = {"store listing visitors", "visitors"}
CTR_HEADERS = {"click-through rate", "store listing click-through rate", "ctr"}
CONVERSION_HEADERS = {"store listing conversion rate", "conversion rate"}


def _percent(value: str, line: int) -> float:
    raw = value.strip()
    if not raw:
        raise ValueError(f"Rate is empty near record {line}")
    explicit_percent = raw.endswith("%")
    number_text = raw[:-1].strip() if explicit_percent else raw
    try:
        number = float(number_text)
    except ValueError:
        raise ValueError(f"Rate must be numeric or a percentage near record {line}") from None
    if not 0 <= number <= 100:
        raise ValueError(f"Rate must be between 0 and 100 percent near record {line}")
    # Play exports have used decimal fractions (0.12) while UI exports can
    # show percentage values (12). An explicit percent sign is always percent.
    return number if explicit_percent or number > 1 else number * 100


def summarize(path: Path) -> dict:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        if not reader.fieldnames:
            raise ValueError("CSV must include a header row")
        normalized = [name.strip().casefold() for name in reader.fieldnames]
        if len(normalized) != len(set(normalized)):
            raise ValueError("CSV has duplicate column names")
        date_field = next((name for name in reader.fieldnames if name.strip().casefold() in DATE_HEADERS), None)
        visitors_field = next((name for name in reader.fieldnames if name.strip().casefold() in VISITOR_HEADERS), None)
        ctr_field = next((name for name in reader.fieldnames if name.strip().casefold() in CTR_HEADERS), None)
        conversion_field = next((name for name in reader.fieldnames if name.strip().casefold() in CONVERSION_HEADERS), None)
        rate_field = ctr_field or conversion_field
        if not date_field or not visitors_field or not rate_field:
            raise ValueError("CSV needs Date, Store listing visitors, and Click-through rate or Store listing conversion rate columns")

        reserved = {date_field, visitors_field, rate_field}
        rows = []
        for line, row in enumerate(reader, 2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"Malformed CSV row near record {line}")
            try:
                day = date.fromisoformat(row[date_field].strip())
            except ValueError:
                raise ValueError(f"Date must use YYYY-MM-DD format near record {line}") from None
            visitors_text = row[visitors_field].strip()
            if not re.fullmatch(r"(?:\d+|\d{1,3}(?:,\d{3})+)", visitors_text):
                raise ValueError(f"Store listing visitors must be a non-negative integer near record {line}") from None
            visitors = int(visitors_text.replace(",", ""))
            if visitors < 0:
                raise ValueError(f"Store listing visitors must be a non-negative integer near record {line}")
            dimensions = {name: value.strip() for name, value in row.items() if name not in reserved and value.strip()}
            rows.append({
                "date": day.isoformat(),
                "visitors": visitors,
                "rate_percent": round(_percent(row[rate_field], line), 4),
                "dimensions": dimensions,
            })

    rows.sort(key=lambda item: (item["date"], sorted(item["dimensions"].items())))
    metric = "click_through_rate" if ctr_field else "store_listing_conversion_rate"
    date_counts = {}
    for row in rows:
        date_counts[row["date"]] = date_counts.get(row["date"], 0) + 1
    one_row_per_day = all(count == 1 for count in date_counts.values())
    dimension_names = {key for row in rows for key in row["dimensions"]}
    dimensions_stay_fixed = all(len({row["dimensions"].get(key) for row in rows}) <= 1 for key in dimension_names)
    summary = None
    notes = ["Data comes from the supplied Play Console CSV; it is not a Google API response."]
    if rows and one_row_per_day and dimensions_stay_fixed:
        visitor_total = sum(row["visitors"] for row in rows)
        weighted_rate = (sum(row["visitors"] * row["rate_percent"] for row in rows) / visitor_total
                         if visitor_total else None)
        summary = {
            "visitors": visitor_total,
            "visitor_weighted_rate_percent": round(weighted_rate, 4) if weighted_rate is not None else None,
            "first_day": rows[0]["date"],
            "last_day": rows[-1]["date"],
            "daily_visitor_change": rows[-1]["visitors"] - rows[0]["visitors"] if len(rows) > 1 else None,
            "daily_rate_change_percentage_points": round(rows[-1]["rate_percent"] - rows[0]["rate_percent"], 4) if len(rows) > 1 else None,
        }
    elif rows:
        notes.append("Totals and date-to-date deltas are omitted because the export has multiple rows per date or dimensions that vary over time; this avoids double-counting or comparing unlike segments.")
    return {
        "scope": "Supplied Google Play Console listing export only; trends do not prove which listing change caused a difference.",
        "metric": metric,
        "rows": rows,
        "summary": summary,
        "notes": notes,
    }


def markdown(report: dict) -> str:
    lines = ["# Google Play listing performance", "", report["scope"], "", f"Metric: `{report['metric']}`", ""]
    if report["summary"]:
        summary = report["summary"]
        lines += [f"- Visitors in export: {summary['visitors']}",
                  f"- Visitor-weighted rate: {summary['visitor_weighted_rate_percent']}%" if summary["visitor_weighted_rate_percent"] is not None else "- Visitor-weighted rate: unknown",
                  f"- Date range: {summary['first_day']} to {summary['last_day']}"]
        if summary["daily_visitor_change"] is not None:
            lines += [f"- First-to-last daily visitor change: {summary['daily_visitor_change']}",
                      f"- First-to-last daily rate change: {summary['daily_rate_change_percentage_points']} percentage points"]
        lines.append("")
    lines += ["| Date | Visitors | Rate (%) | Dimensions |", "| --- | ---: | ---: | --- |"]
    for row in report["rows"]:
        dimensions = ", ".join(f"{key}: {value}" for key, value in sorted(row["dimensions"].items())) or "—"
        cell = lambda value: str(value).replace("|", "\\|").replace("\n", " ").replace("<", "&lt;").replace(">", "&gt;")
        lines.append(f"| {row['date']} | {row['visitors']} | {row['rate_percent']} | {cell(dimensions)} |")
    for note in report["notes"]:
        lines += ["", f"Note: {note}"]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()
    try:
        report = summarize(args.csv)
    except (OSError, ValueError, csv.Error) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    output = json.dumps(report, indent=2) if args.format == "json" else markdown(report)
    print(output, end="\n" if args.format == "json" else "")
    return 0


if __name__ == "__main__":
    sys.exit(main())
