app_name = "cyteerp_payroll_ai"
app_title = "CyteERP Payroll AI"
app_publisher = "CyteERP Systems"
app_description = "Africa-wide payroll intelligence and country-pack governance for ERPNext"
app_email = "support@cyteerp.com"
app_license = "GPL-3.0-or-later"

fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "Payroll AI"]]},
]

after_install = "cyteerp_payroll_ai.install.after_install"
