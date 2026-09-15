import unittest

from ec.demos.apm_sprint0 import apm_observation, run
from ec.intelligence.advisory import assess_order_delay_risk


class APMSprint0AdvisoryTests(unittest.TestCase):
    def test_detects_material_delay_risk(self):
        assessment = assess_order_delay_risk(apm_observation())
        self.assertEqual(assessment.severity, "critical")
        self.assertIn("2 days beyond", assessment.diagnosis)
        self.assertIn("$280,000", assessment.diagnosis)
        self.assertIn("+8.4%", assessment.expected_impact)
        self.assertEqual(assessment.confidence, 0.93)

    def test_output_is_explicitly_advisory_not_execution(self):
        result = run()
        self.assertEqual(result["status"], "ADVISORY_ONLY")
        assessment = result["assessment"]
        self.assertIn("Do not execute automatically", assessment["recommendation"])
        self.assertIn("authorized human/policy", assessment["authority_notice"])
        self.assertIn("EVO", assessment["authority_notice"])

    def test_evidence_is_visible_and_sourced(self):
        result = run()
        evidence = result["assessment"]["evidence"]
        self.assertGreaterEqual(len(evidence), 6)
        self.assertTrue(all(item["source"] for item in evidence))
        labels = {item["label"] for item in evidence}
        self.assertIn("Customer promise date", labels)
        self.assertIn("Current supplier ETA", labels)
        self.assertIn("Revenue at risk", labels)


if __name__ == "__main__":
    unittest.main()
