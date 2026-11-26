"""Run an end-to-end synthetic AERIS measurement-to-finding demonstration."""
from __future__ import annotations
from datetime import datetime, timezone
import argparse
import json

from .analytics import FlowPoint
from .findings import detect_sustained_excess
from .simulator import generate_flow_events
from .telemetry import TelemetryEvent


def run_demo(scenario: str = "sustained_excess") -> dict[str, object]:
    events = generate_flow_events(
        start=datetime(2026, 11, 26, 8, 0, tzinfo=timezone.utc),
        count=120, interval_seconds=30, scenario=scenario, seed=19,
    )
    parsed = [TelemetryEvent.from_mapping(event) for event in events]
    points = [
        FlowPoint(
            timestamp=event.event_time_utc,
            observed_m3_s=event.value,
            baseline_m3_s=0.010,
        )
        for event in parsed
    ]
    findings = detect_sustained_excess(
        points, threshold_m3_s=0.005,
        minimum_duration_seconds=300, max_gap_seconds=60,
    )
    return {
        "data_provenance": "synthetic",
        "scenario": scenario,
        "events_processed": len(parsed),
        "finding_count": len(findings),
        "findings": [
            {
                "rule_id": item.rule_id,
                "classification": item.classification,
                "start_utc": item.start.isoformat(),
                "end_utc": item.end.isoformat(),
                "duration_seconds": item.duration_seconds,
                "mean_excess_m3_s": round(item.mean_excess_m3_s, 8),
                "peak_excess_m3_s": round(item.peak_excess_m3_s, 8),
                "estimated_excess_volume_m3": round(item.estimated_excess_volume_m3, 8),
                "interval_count": item.interval_count,
            }
            for item in findings
        ],
        "interpretation": "Investigation signal only; not proof of a leak or root cause.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the AERIS synthetic demonstration")
    parser.add_argument("--scenario", choices=("normal", "idle_loss", "sustained_excess"),
                        default="sustained_excess")
    args = parser.parse_args()
    print(json.dumps(run_demo(args.scenario), indent=2))


if __name__ == "__main__":
    main()
