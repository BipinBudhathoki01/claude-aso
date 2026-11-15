#!/usr/bin/env python3
"""Statistical A/B test sample size & duration estimator for Play Store & App Store."""
import json
import math
import sys


def calculate_sample_size(baseline_pct: float, mde_pct: float, daily_visitors: int, confidence: int = 90) -> dict:
    p1 = min(max(baseline_pct / 100.0, 0.01), 0.90)
    p2 = min(p1 * (1.0 + max(mde_pct / 100.0, 0.01)), 0.99)
    z_alpha = {95: 1.96, 90: 1.645, 80: 1.282}.get(confidence, 1.645)
    z_beta = 0.842
    p_bar = (p1 + p2) / 2.0
    num = (z_alpha * math.sqrt(2 * p_bar * (1 - p_bar)) + z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    per_variant = max(100, math.ceil(num / max((p2 - p1) ** 2, 1e-7)))
    total = per_variant * 2
    days = math.ceil(total / max(50, daily_visitors))
    return {
        "perVariant": per_variant,
        "totalVisitors": total,
        "estimatedDays": days,
        "targetConversionPct": round(p2 * 100, 2),
    }


if __name__ == "__main__":
    base = float(sys.argv[1]) if len(sys.argv) > 1 else 28.0
    mde = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
    daily = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
    conf = int(sys.argv[4]) if len(sys.argv) > 4 else 90
    print(json.dumps(calculate_sample_size(base, mde, daily, conf), indent=2))
