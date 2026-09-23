"""Controller for governed payroll country packs."""

import json

import frappe
from frappe.model.document import Document

from cyteerp_payroll_ai.core.countries import get_country


class PayrollCountryPack(Document):
	def autoname(self):
		self.name = self.country_code.strip().upper()

	def validate(self):
		country = get_country(self.country_code)
		self.country_code = country.code
		self.country_name = country.name
		self.region = country.region
		if not self.currency:
			self.currency = country.currency

		for fieldname in ("rules_json", "golden_tests_json"):
			value = self.get(fieldname)
			if value:
				try:
					json.loads(value)
				except (TypeError, ValueError):
					frappe.throw(f"{self.meta.get_label(fieldname)} must be valid JSON.")

		if self.status == "Production":
			required = {
				"rule_set_version": self.rule_set_version,
				"effective_from": self.effective_from,
				"compliance_owner": self.compliance_owner,
				"source_authority": self.source_authority,
				"source_reference": self.source_reference,
				"rules_json": self.rules_json,
				"golden_tests_json": self.golden_tests_json,
			}
			missing = [label.replace("_", " ").title() for label, value in required.items() if not value]
			if missing:
				frappe.throw("Production country packs require: " + ", ".join(missing))
			if not self.enabled:
				frappe.throw("A Production country pack must be enabled.")
