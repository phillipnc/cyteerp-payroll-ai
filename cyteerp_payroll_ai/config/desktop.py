from frappe import _


def get_data():
	return [
		{
			"module_name": "Payroll AI",
			"type": "module",
			"label": _("Payroll AI"),
			"color": "green",
			"icon": "octicon octicon-shield",
			"link": "List/Payroll AI Settings",
			"link_type": "List",
			"onboard_present": 0,
		}
	]
