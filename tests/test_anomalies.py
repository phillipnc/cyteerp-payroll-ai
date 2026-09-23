import unittest

from cyteerp_payroll_ai.core.anomalies import detect_anomalies


class AnomalyTests(unittest.TestCase):
	def test_detects_negative_net_and_large_change(self):
		findings = detect_anomalies(
			{"employee_id": "EMP-001", "gross_earnings": "500", "net_pay": "-10", "tax": "20"},
			{"gross_earnings": "1000"},
		)
		codes = {finding["code"] for finding in findings}
		self.assertIn("negative_net", codes)
		self.assertIn("gross_change_over_30_percent", codes)

	def test_missing_employee_id(self):
		findings = detect_anomalies({"gross_earnings": "100", "net_pay": "100", "tax": "0"})
		self.assertEqual(findings[0]["code"], "missing_employee_id")
