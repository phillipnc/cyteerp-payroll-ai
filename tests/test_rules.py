import unittest
from decimal import Decimal

from cyteerp_payroll_ai.core.models import Component, PayrollInput, TaxBand
from cyteerp_payroll_ai.core.rules import calculate_payroll, progressive_tax


class RulesTests(unittest.TestCase):
	def test_progressive_tax(self):
		tax, trace = progressive_tax(
			Decimal("10000"),
			(
				TaxBand(Decimal("3000"), Decimal("0")),
				TaxBand(Decimal("8000"), Decimal("0.20")),
				TaxBand(None, Decimal("0.30")),
			),
		)
		self.assertEqual(tax, Decimal("1600.00"))
		self.assertEqual(len(trace), 3)

	def test_calculation_trace_and_net_pay(self):
		result = calculate_payroll(
			PayrollInput(
				country="ZM",
				rule_set="test-2026",
				currency="ZMW",
				gross_earnings=Decimal("18500"),
				tax_bands=(
					TaxBand(Decimal("3000"), Decimal("0")),
					TaxBand(Decimal("8000"), Decimal("0.20")),
					TaxBand(None, Decimal("0.30")),
				),
				employee_deductions=(Component("pension", Decimal("500")),),
				employer_contributions=(Component("napsa", Decimal("500")),),
			)
		)
		self.assertEqual(result.tax, Decimal("4150.00"))
		self.assertEqual(result.net_pay, Decimal("13850.00"))
		self.assertEqual(result.employer_cost, Decimal("19000.00"))
		self.assertTrue(any("Band 3" in line for line in result.trace))

	def test_empty_bands_are_safe_and_explicit(self):
		result = calculate_payroll(
			PayrollInput(country="KE", rule_set="unconfigured", currency="KES", gross_earnings=100)
		)
		self.assertEqual(result.tax, Decimal("0.00"))
		self.assertTrue(any("No approved tax bands" in line for line in result.trace))
