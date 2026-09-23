"""Install hooks for safe, non-statutory catalogue seed data."""


def after_install() -> None:
	"""Create disabled scaffold records for the 54-country catalogue."""
	import frappe

	from cyteerp_payroll_ai.core.countries import COUNTRIES

	for country in COUNTRIES:
		if frappe.db.exists("Payroll Country Pack", country.code):
			continue
		doc = frappe.new_doc("Payroll Country Pack")
		doc.country_code = country.code
		doc.country_name = country.name
		doc.currency = country.currency
		doc.region = country.region
		doc.status = "Scaffold"
		doc.enabled = 0
		doc.insert(ignore_permissions=True)
