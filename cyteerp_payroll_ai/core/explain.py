"""Deterministic explanation helpers used by the optional AI provider."""

from typing import Any


def explain_result(result: dict[str, Any], employee_name: str | None = None) -> dict[str, Any]:
	"""Create a plain-language explanation without sending payroll data externally."""
	name = employee_name or "The employee"
	currency = result.get("currency", "")
	tax = result.get("tax", "0.00")
	net_pay = result.get("net_pay", "0.00")
	trace = result.get("trace", [])
	summary = f"{name}'s net pay is {net_pay} {currency}. Tax calculated is {tax} {currency}."
	return {
		"summary": summary,
		"calculation_trace": trace,
		"rule_set": result.get("rule_set"),
		"country": result.get("country"),
		"human_review_required": True,
		"disclaimer": "This explanation describes the supplied calculation; it is not legal advice.",
	}
