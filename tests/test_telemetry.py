import unittest

from aeris_core.telemetry import TelemetryEvent, TelemetryValidationError


def valid_payload():
    return {
        "schema_version": 1,
        "event_id": "evt-001",
        "device_id": "device-01",
        "site_id": "site-01",
        "asset_id": "compressor-room-main",
        "channel_id": "flow-main",
        "event_time_utc": "2026-11-26T10:00:00Z",
        "received_time_utc": "2026-11-26T10:00:01+00:00",
        "sequence_number": 1,
        "metric": "flow_m3_s",
        "value": 0.012,
        "unit": "m3/s",
        "quality_flags": [],
    }


class TelemetryContractTests(unittest.TestCase):
    def test_valid_event_is_parsed(self):
        event = TelemetryEvent.from_mapping(valid_payload())
        self.assertEqual(event.event_id, "evt-001")
        self.assertEqual(event.value, 0.012)
        self.assertEqual(event.event_time_utc.utcoffset().total_seconds(), 0)

    def test_rejects_unit_mismatch(self):
        payload = valid_payload()
        payload["unit"] = "L/min"
        with self.assertRaises(TelemetryValidationError):
            TelemetryEvent.from_mapping(payload)

    def test_normalizes_offset_timestamp_to_utc(self):
        payload = valid_payload()
        payload["event_time_utc"] = "2026-11-26T15:30:00+05:30"
        event = TelemetryEvent.from_mapping(payload)
        self.assertEqual(event.event_time_utc.isoformat(), "2026-11-26T10:00:00+00:00")

    def test_rejects_non_finite_value(self):
        for invalid in (float("nan"), float("inf"), float("-inf")):
            payload = valid_payload()
            payload["value"] = invalid
            with self.subTest(value=invalid):
                with self.assertRaises(TelemetryValidationError):
                    TelemetryEvent.from_mapping(payload)

    def test_rejects_timezone_naive_timestamp(self):
        payload = valid_payload()
        payload["event_time_utc"] = "2026-11-26T10:00:00"
        with self.assertRaises(TelemetryValidationError):
            TelemetryEvent.from_mapping(payload)

    def test_rejects_boolean_as_numeric_value(self):
        payload = valid_payload()
        payload["value"] = True
        with self.assertRaises(TelemetryValidationError):
            TelemetryEvent.from_mapping(payload)

    def test_rejects_negative_flow(self):
        payload = valid_payload()
        payload["value"] = -0.1
        with self.assertRaises(TelemetryValidationError):
            TelemetryEvent.from_mapping(payload)

    def test_rejects_unknown_schema_version(self):
        payload = valid_payload()
        payload["schema_version"] = 2
        with self.assertRaises(TelemetryValidationError):
            TelemetryEvent.from_mapping(payload)


if __name__ == "__main__":
    unittest.main()
