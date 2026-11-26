import unittest
from datetime import datetime, timezone
from aeris_core.simulator import generate_flow_events
from aeris_core.telemetry import TelemetryEvent


class SimulatorTests(unittest.TestCase):
    def test_generation_is_deterministic(self):
        args = dict(start=datetime(2026, 11, 26, tzinfo=timezone.utc), count=12)
        self.assertEqual(generate_flow_events(**args), generate_flow_events(**args))

    def test_events_satisfy_contract_and_are_marked_synthetic(self):
        events = generate_flow_events(start=datetime(2026, 11, 26, tzinfo=timezone.utc), count=8)
        self.assertEqual(len(events), 8)
        for event in events:
            self.assertIn("synthetic", TelemetryEvent.from_mapping(event).quality_flags)

    def test_dropout_and_duplicate_controls(self):
        start = datetime(2026, 11, 26, tzinfo=timezone.utc)
        self.assertEqual(len(generate_flow_events(start=start, count=10, dropout_every=3)), 7)
        events = generate_flow_events(start=start, count=6, duplicate_every=2)
        self.assertEqual(len(events), 9)
        self.assertEqual(events[1]["event_id"], events[2]["event_id"])

    def test_rejects_naive_start(self):
        with self.assertRaises(ValueError):
            generate_flow_events(start=datetime(2026, 11, 26))


if __name__ == "__main__":
    unittest.main()
