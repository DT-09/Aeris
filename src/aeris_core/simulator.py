"""Deterministic synthetic telemetry for development and acceptance tests."""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
import random


def generate_flow_events(*, start: datetime, count: int = 120,
                         interval_seconds: int = 30, scenario: str = "normal",
                         seed: int = 7, dropout_every: int | None = None,
                         duplicate_every: int | None = None,
                         delay_every: int | None = None) -> list[dict[str, object]]:
    """Generate explicitly synthetic compressed-air flow events."""
    if start.tzinfo is None or start.utcoffset() is None:
        raise ValueError("start must be timezone-aware")
    if type(count) is not int or count < 2:
        raise ValueError("count must be an integer of at least 2")
    if type(interval_seconds) is not int or interval_seconds <= 0:
        raise ValueError("interval_seconds must be a positive integer")
    if scenario not in ("normal", "idle_loss", "sustained_excess"):
        raise ValueError("unsupported scenario")
    for name, cadence in (("dropout_every", dropout_every),
                          ("duplicate_every", duplicate_every),
                          ("delay_every", delay_every)):
        if cadence is not None and (type(cadence) is not int or cadence < 1):
            raise ValueError(f"{name} must be a positive integer or None")

    rng = random.Random(seed)
    start = start.astimezone(timezone.utc)
    events = []
    first, last = count // 3, (2 * count) // 3
    for index in range(count):
        if dropout_every and (index + 1) % dropout_every == 0:
            continue
        baseline = 0.010
        excess = 0.0
        if first <= index < last and scenario in ("idle_loss", "sustained_excess"):
            excess = 0.006 if scenario == "idle_loss" else 0.012
        observed = max(0.0, baseline + excess + rng.uniform(-0.0002, 0.0002))
        event_time = start + timedelta(seconds=index * interval_seconds)
        receive_time = event_time + timedelta(seconds=interval_seconds)
        if delay_every and (index + 1) % delay_every == 0:
            receive_time += timedelta(minutes=5)
        event = {
            "schema_version": 1, "event_id": f"sim-flow-{index:06d}",
            "device_id": "sim-device-01", "site_id": "sim-site-01",
            "asset_id": "sim-compressed-air-header", "channel_id": "sim-flow-main",
            "event_time_utc": event_time.isoformat(),
            "received_time_utc": receive_time.isoformat(),
            "sequence_number": index, "metric": "flow_m3_s",
            "value": round(observed, 8), "unit": "m3/s",
            "quality_flags": ["synthetic"],
        }
        events.append(event)
        if duplicate_every and (index + 1) % duplicate_every == 0:
            duplicate = dict(event)
            duplicate["quality_flags"] = ["synthetic", "transport_duplicate"]
            events.append(duplicate)
    return events
