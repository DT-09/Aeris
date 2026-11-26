import unittest
from datetime import datetime, timedelta, timezone
from aeris_core.analytics import FlowPoint
from aeris_core.findings import detect_sustained_excess

T0 = datetime(2026, 11, 26, tzinfo=timezone.utc)


class FindingTests(unittest.TestCase):
    def test_detects_sustained_excess_and_reports_evidence(self):
        points = [FlowPoint(T0 + timedelta(seconds=s), f, 0.010)
                  for s, f in [(0, .010), (30, .020), (60, .020), (90, .020)]]
        result = detect_sustained_excess(points, threshold_m3_s=.005,
                                         minimum_duration_seconds=60)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].duration_seconds, 90)
        self.assertEqual(result[0].interval_count, 3)
        self.assertAlmostEqual(result[0].estimated_excess_volume_m3, .75)
        self.assertEqual(result[0].classification, "observation")

    def test_short_spike_is_not_emitted(self):
        points = [FlowPoint(T0, .010, .010),
                  FlowPoint(T0 + timedelta(seconds=30), .030, .010),
                  FlowPoint(T0 + timedelta(seconds=60), .010, .010)]
        self.assertEqual(detect_sustained_excess(
            points, threshold_m3_s=.005, minimum_duration_seconds=60), [])

    def test_invalid_interval_breaks_run(self):
        points = [FlowPoint(T0, .020, .010),
                  FlowPoint(T0 + timedelta(seconds=30), .020, .010, valid=False),
                  FlowPoint(T0 + timedelta(seconds=60), .020, .010)]
        self.assertEqual(detect_sustained_excess(
            points, threshold_m3_s=.005, minimum_duration_seconds=30), [])

    def test_rejects_invalid_threshold(self):
        with self.assertRaises(ValueError):
            detect_sustained_excess([FlowPoint(T0, .02, .01)],
                                    threshold_m3_s=0, minimum_duration_seconds=30)


if __name__ == "__main__":
    unittest.main()
