"""Canonical telemetry envelope and strict validation.

Canonical units:
- pressure_pa: pascals
- flow_m3_s: cubic metres per second

This module validates data shape and basic physical plausibility. It does not
calibrate sensors or prove that a measurement is accurate.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import math
from typing import Any, Mapping


class TelemetryValidationError(ValueError):
    """Raised when a telemetry event violates the canonical contract."""


def _parse_aware_datetime(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise TelemetryValidationError(f"{field} must be a non-empty ISO-8601 string")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise TelemetryValidationError(f"{field} is not a valid ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise TelemetryValidationError(f"{field} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _required_text(payload: Mapping[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise TelemetryValidationError(f"{field} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True, slots=True)
class TelemetryEvent:
    schema_version: int
    event_id: str
    device_id: str
    site_id: str
    asset_id: str
    channel_id: str
    event_time_utc: datetime
    received_time_utc: datetime
    sequence_number: int
    metric: str
    value: float
    unit: str
    quality_flags: tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "TelemetryEvent":
        if not isinstance(payload, Mapping):
            raise TelemetryValidationError("event must be a mapping")

        schema_version = payload.get("schema_version")
        if type(schema_version) is not int or schema_version != 1:
            raise TelemetryValidationError("schema_version must be integer 1")

        sequence_number = payload.get("sequence_number")
        if type(sequence_number) is not int or sequence_number < 0:
            raise TelemetryValidationError("sequence_number must be a non-negative integer")

        metric = _required_text(payload, "metric")
        expected_units = {
            "pressure_pa": "Pa",
            "flow_m3_s": "m3/s",
        }
        if metric not in expected_units:
            raise TelemetryValidationError(f"unsupported metric: {metric}")

        unit = _required_text(payload, "unit")
        if unit != expected_units[metric]:
            raise TelemetryValidationError(
                f"{metric} requires canonical unit {expected_units[metric]}"
            )

        raw_value = payload.get("value")
        if isinstance(raw_value, bool) or not isinstance(raw_value, (int, float)):
            raise TelemetryValidationError("value must be a finite number")
        value = float(raw_value)
        if not math.isfinite(value):
            raise TelemetryValidationError("value must be a finite number")
        if value < 0 or (metric == "pressure_pa" and value == 0):
            raise TelemetryValidationError("value is outside the permitted physical domain")

        raw_flags = payload.get("quality_flags", ())
        if not isinstance(raw_flags, (list, tuple)) or any(
            not isinstance(flag, str) or not flag.strip() for flag in raw_flags
        ):
            raise TelemetryValidationError("quality_flags must be a list of non-empty strings")

        return cls(
            schema_version=schema_version,
            event_id=_required_text(payload, "event_id"),
            device_id=_required_text(payload, "device_id"),
            site_id=_required_text(payload, "site_id"),
            asset_id=_required_text(payload, "asset_id"),
            channel_id=_required_text(payload, "channel_id"),
            event_time_utc=_parse_aware_datetime(payload.get("event_time_utc"), "event_time_utc"),
            received_time_utc=_parse_aware_datetime(
                payload.get("received_time_utc"), "received_time_utc"
            ),
            sequence_number=sequence_number,
            metric=metric,
            value=value,
            unit=unit,
            quality_flags=tuple(flag.strip() for flag in raw_flags),
        )
