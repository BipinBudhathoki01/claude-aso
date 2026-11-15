#!/usr/bin/env python3
"""Generate dated launch timeline milestones for Play Store & App Store submissions."""
from datetime import datetime, timedelta
import json
import sys


def build_timeline(launch_date_str: str) -> list[dict]:
    launch = datetime.strptime(launch_date_str, "%Y-%m-%d")
    offsets = [
        (-14, "Metadata & Keyword Freeze (Play 30/80/4000, iOS 30/30/100)"),
        (-10, "Visual Assets & First-3-Frame Screenshots QA"),
        (-7, "Closed Testing Android Vitals Gate (Crash <= 1.09%, ANR <= 0.47%)"),
        (-4, "Submit iOS App Review (with Demo Account) & Play Production Track"),
        (0, "Launch Day: Publish Promotional Text, In-App Event & Social Links"),
        (7, "T+7 Review Triage + Launch First PPO / Store Listing Experiment"),
    ]
    return [
        {"date": (launch + timedelta(days=d)).strftime("%Y-%m-%d"), "offsetDays": d, "milestone": label}
        for d, label in offsets
    ]


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else datetime.utcnow().strftime("%Y-%m-%d")
    print(json.dumps(build_timeline(target), indent=2))
