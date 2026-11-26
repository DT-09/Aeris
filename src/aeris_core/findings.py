"""Explainable rules that convert flow observations into reviewable findings."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
import math
from .analytics import FlowPoint, _validate_point


@dataclass(frozen=True, slots=True)
class ExcessFlowFinding:
    start: datetime
    end: datetime
    duration_seconds: float
    mean_excess_m3_s: float
    peak_excess_m3_s: float
    estimated_excess_volume_m3: float
    interval_count: int
    rule_id: str = "sustained-excess-flow-v1"
    classification: str = "observation"


def detect_sustained_excess(points: list[FlowPoint] | tuple[FlowPoint, ...], *,
                            threshold_m3_s: float,
                            minimum_duration_seconds: float,
                            max_gap_seconds: float = 120.0) -> list[ExcessFlowFinding]:
    """Find contiguous intervals above threshold; never infer a root cause."""
    for name, value in (("threshold_m3_s", threshold_m3_s),
                        ("minimum_duration_seconds", minimum_duration_seconds),
                        ("max_gap_seconds", max_gap_seconds)):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be numeric")
        if not math.isfinite(float(value)) or value <= 0:
            raise ValueError(f"{name} must be finite and positive")
    for point in points:
        _validate_point(point)
    for left, right in zip(points, points[1:]):
        if right.timestamp <= left.timestamp:
            raise ValueError("points must be strictly increasing by timestamp")

    findings = []
    run = []

    def flush():
        nonlocal run
        if not run:
            return
        duration = sum(item[2] for item in run)
        if duration >= minimum_duration_seconds:
            findings.append(ExcessFlowFinding(
                start=run[0][0].timestamp, end=run[-1][1].timestamp,
                duration_seconds=duration,
                mean_excess_m3_s=sum(item[3] * item[2] for item in run) / duration,
                peak_excess_m3_s=max(item[4] for item in run),
                estimated_excess_volume_m3=sum(item[3] * item[2] for item in run),
                interval_count=len(run),
            ))
        run = []

    for left, right in zip(points, points[1:]):
        duration = (right.timestamp - left.timestamp).total_seconds()
        usable = (duration <= max_gap_seconds and left.valid and right.valid
                  and left.context_comparable and right.context_comparable)
        if not usable:
            flush()
            continue
        a = max(0.0, left.observed_m3_s - left.baseline_m3_s)
        b = max(0.0, right.observed_m3_s - right.baseline_m3_s)
        mean, peak = (a + b) / 2.0, max(a, b)
        if mean >= threshold_m3_s:
            run.append((left, right, duration, mean, peak))
        else:
            flush()
    flush()
    return findings
