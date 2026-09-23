"""Controller for Payroll AI Settings."""

import frappe
from frappe.model.document import Document


class PayrollAISettings(Document):
	def validate(self):
		if self.ai_provider == "OpenAI-compatible" and not self.ai_endpoint:
			frappe.throw("AI Endpoint is required for an OpenAI-compatible provider.")
		if self.ai_provider == "Deterministic only":
			self.send_payroll_data_externally = 0
		self.require_human_review = 1
