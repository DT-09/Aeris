import unittest
from aeris_core.demo import run_demo


class EndToEndDemoTests(unittest.TestCase):
    def test_sustained_excess_scenario_emits_finding(self):
        result = run_demo("sustained_excess")
        self.assertEqual(result["data_provenance"], "synthetic")
        self.assertEqual(result["events_processed"], 120)
        self.assertGreater(result["finding_count"], 0)
        self.assertEqual(result["findings"][0]["classification"], "observation")

    def test_normal_scenario_emits_no_finding(self):
        result = run_demo("normal")
        self.assertEqual(result["finding_count"], 0)

    def test_idle_loss_scenario_emits_finding(self):
        result = run_demo("idle_loss")
        self.assertGreater(result["finding_count"], 0)


if __name__ == "__main__":
    unittest.main()
