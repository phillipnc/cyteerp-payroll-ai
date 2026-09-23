"""Explainable payroll-quality checks."""

from decimal import Decimal
from typing import Any


def _decimal(value: Any) -> Decimal:
	return Decimal(str(value or 0))


def detect_anomalies(current: dict[str, Any], previous: dict[str, Any] | None = None) -> list[dict[str, Any]]:
	"""Return deterministic findings suitable for a review queue."""
	findings: list[dict[str, Any]] = []
	gross = _decimal(current.get("gross_earnings"))
	net = _decimal(current.get("net_pay"))
	tax = _decimal(current.get("tax"))

	if gross < 0:
		findings.append({"code": "negative_gross", "severity": "high", "message": "Gross earnings are negative."})
	if net < 0:
		findings.append({"code": "negative_net", "severity": "high", "message": "Net pay is negative."})
	if tax < 0:
		findings.append({"code": "negative_tax", "severity": "high", "message": "Tax is negative."})
	if gross and tax > gross:
		findings.append(
			{"code": "tax_exceeds_gross", "severity": "high", "message": "Tax exceeds gross earnings."}
		)
	if not current.get("employee_id"):
		findings.append(
			{"code": "missing_employee_id", "severity": "medium", "message": "Employee ID is missing."}
		)
	if previous:
		previous_gross = _decimal(previous.get("gross_earnings"))
		if previous_gross and abs(gross - previous_gross) / abs(previous_gross) >= Decimal("0.30"):
			findings.append(
				{
					"code": "gross_change_over_30_percent",
					"severity": "medium",
					"message": "Gross earnings changed by 30% or more from the previous period.",
					"previous": str(previous_gross),
					"current": str(gross),
				}
			)
	return findings
