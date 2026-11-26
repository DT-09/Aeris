"""Transparent, deterministic calculations for compressed-air telemetry."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import math


@dataclass(frozen=True, slots=True)
class FlowPoint:
    """Observed and baseline flow at one instant, both in m3/s."""

    timestamp: datetime
    observed_m3_s: float
    baseline_m3_s: float
    valid: bool = True
    context_comparable: bool = True


@dataclass(frozen=True, slots=True)
class ExcessVolumeResult:
    """Integrated excess volume and the coverage supporting that estimate."""

    excess_volume_m3: float
    elapsed_seconds: float
    covered_seconds: float
    skipped_intervals: int

    @property
    def coverage_ratio(self) -> float:
        if self.elapsed_seconds == 0:
            return 0.0
        return self.covered_seconds / self.elapsed_seconds


def _validate_point(point: FlowPoint) -> None:
    if point.timestamp.tzinfo is None or point.timestamp.utcoffset() is None:
        raise ValueError("all timestamps must be timezone-aware")
    for name, value in (
        ("observed_m3_s", point.observed_m3_s),
        ("baseline_m3_s", point.baseline_m3_s),
    ):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be numeric")
        if not math.isfinite(float(value)) or value < 0:
            raise ValueError(f"{name} must be finite and non-negative")


def estimate_excess_volume(
    points: list[FlowPoint] | tuple[FlowPoint, ...],
    *,
    max_gap_seconds: float = 120.0,
) -> ExcessVolumeResult:
    """Integrate positive observed-minus-baseline flow using trapezoids.

    An interval contributes only when both endpoints are valid and their
    operating contexts are comparable. Intervals longer than max_gap_seconds
    are excluded rather than bridged. Flow is in m3/s; result is in m3.

    This is an excess-consumption estimate, not proof of a leak or its cause.
    """
    if isinstance(max_gap_seconds, bool) or not math.isfinite(max_gap_seconds):
        raise ValueError("max_gap_seconds must be finite and positive")
    if max_gap_seconds <= 0:
        raise ValueError("max_gap_seconds must be finite and positive")

    for point in points:
        _validate_point(point)

    for previous, current in zip(points, points[1:]):
        if current.timestamp <= previous.timestamp:
            raise ValueError("points must be strictly increasing by timestamp")

    elapsed = 0.0
    covered = 0.0
    excess_volume = 0.0
    skipped = 0

    for previous, current in zip(points, points[1:]):
        duration = (current.timestamp - previous.timestamp).total_seconds()
        elapsed += duration

        interval_usable = (
            duration <= max_gap_seconds
            and previous.valid
            and current.valid
            and previous.context_comparable
            and current.context_comparable
        )
        if not interval_usable:
            skipped += 1
            continue

        previous_excess = max(0.0, previous.observed_m3_s - previous.baseline_m3_s)
        current_excess = max(0.0, current.observed_m3_s - current.baseline_m3_s)
        excess_volume += (previous_excess + current_excess) * 0.5 * duration
        covered += duration

    return ExcessVolumeResult(
        excess_volume_m3=excess_volume,
        elapsed_seconds=elapsed,
        covered_seconds=covered,
        skipped_intervals=skipped,
    )
