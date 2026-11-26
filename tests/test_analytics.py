import unittest
from datetime import datetime, timedelta, timezone

from aeris_core.analytics import FlowPoint, estimate_excess_volume


T0 = datetime(2026, 11, 26, 10, 0, tzinfo=timezone.utc)


class ExcessVolumeTests(unittest.TestCase):
    def test_integrates_constant_excess_flow(self):
        points = [
            FlowPoint(T0, 0.020, 0.010),
            FlowPoint(T0 + timedelta(seconds=60), 0.020, 0.010),
        ]
        result = estimate_excess_volume(points)
        self.assertAlmostEqual(result.excess_volume_m3, 0.6)
        self.assertAlmostEqual(result.coverage_ratio, 1.0)

    def test_trapezoidal_integration(self):
        points = [
            FlowPoint(T0, 0.020, 0.010),
            FlowPoint(T0 + timedelta(seconds=60), 0.030, 0.010),
        ]
        result = estimate_excess_volume(points)
        self.assertAlmostEqual(result.excess_volume_m3, 0.9)

    def test_negative_deviation_is_not_counted_as_excess(self):
        points = [
            FlowPoint(T0, 0.005, 0.010),
            FlowPoint(T0 + timedelta(seconds=60), 0.005, 0.010),
        ]
        result = estimate_excess_volume(points)
        self.assertEqual(result.excess_volume_m3, 0.0)

    def test_skips_invalid_interval(self):
        points = [
            FlowPoint(T0, 0.020, 0.010),
            FlowPoint(T0 + timedelta(seconds=60), 0.020, 0.010, valid=False),
        ]
        result = estimate_excess_volume(points)
        self.assertEqual(result.excess_volume_m3, 0.0)
        self.assertEqual(result.skipped_intervals, 1)
        self.assertEqual(result.covered_seconds, 0.0)

    def test_skips_non_comparable_context(self):
        points = [
            FlowPoint(T0, 0.020, 0.010),
            FlowPoint(T0 + timedelta(seconds=60), 0.020, 0.010, context_comparable=False),
        ]
        result = estimate_excess_volume(points)
        self.assertEqual(result.covered_seconds, 0.0)

    def test_skips_large_gap(self):
        points = [
            FlowPoint(T0, 0.020, 0.010),
            FlowPoint(T0 + timedelta(seconds=600), 0.020, 0.010),
        ]
        result = estimate_excess_volume(points, max_gap_seconds=120)
        self.assertEqual(result.excess_volume_m3, 0.0)
        self.assertEqual(result.skipped_intervals, 1)

    def test_rejects_non_monotonic_timestamps(self):
        points = [
            FlowPoint(T0, 0.020, 0.010),
            FlowPoint(T0, 0.020, 0.010),
        ]
        with self.assertRaises(ValueError):
            estimate_excess_volume(points)

    def test_rejects_naive_timestamp(self):
        points = [
            FlowPoint(datetime(2026, 11, 26, 10, 0), 0.020, 0.010),
            FlowPoint(T0 + timedelta(seconds=60), 0.020, 0.010),
        ]
        with self.assertRaises(ValueError):
            estimate_excess_volume(points)


if __name__ == "__main__":
    unittest.main()
