"""Frappe API endpoints for Payroll AI."""

from decimal import Decimal
from typing import Any

from cyteerp_payroll_ai.core.anomalies import detect_anomalies as _detect_anomalies
from cyteerp_payroll_ai.core.countries import country_catalog, get_country
from cyteerp_payroll_ai.core.explain import explain_result
from cyteerp_payroll_ai.core.models import Component, PayrollInput, TaxBand
from cyteerp_payroll_ai.core.rules import calculate_payroll as _calculate_payroll

try:
	import frappe
except ImportError:  # pragma: no cover - exercised only outside a bench
	frappe = None


def _whitelist(function):
	return frappe.whitelist()(function) if frappe else function


def _json(payload: Any) -> dict[str, Any]:
	if isinstance(payload, str):
		import json

		return json.loads(payload)
	return payload


def _component_rows(rows: list[dict[str, Any]] | None) -> tuple[Component, ...]:
	return tuple(
		Component(code=str(row["code"]), amount=Decimal(str(row["amount"])), taxable=bool(row.get("taxable", True)))
		for row in (rows or [])
	)


@_whitelist
def get_supported_countries() -> list[dict]:
	return country_catalog()


@_whitelist
def calculate_payroll(payload: dict | str) -> dict[str, Any]:
	data = _json(payload)
	country = get_country(data["country"])
	bands = tuple(
		TaxBand(
			up_to=Decimal(str(item["up_to"])) if item.get("up_to") is not None else None,
			rate=Decimal(str(item["rate"])),
		)
		for item in data.get("tax_bands", [])
	)
	result = _calculate_payroll(
		PayrollInput(
			country=country.code,
			rule_set=data["rule_set"],
			currency=data.get("currency", country.currency),
			gross_earnings=Decimal(str(data["gross_earnings"])),
			taxable_earnings=(
				Decimal(str(data["taxable_earnings"])) if data.get("taxable_earnings") is not None else None
			),
			tax_bands=bands,
			tax_relief=Decimal(str(data.get("tax_relief", 0))),
			employee_deductions=_component_rows(data.get("employee_deductions")),
			employer_contributions=_component_rows(data.get("employer_contributions")),
			employee_id=data.get("employee_id"),
			employee_name=data.get("employee_name"),
			period=data.get("period"),
		)
	)
	return result.as_dict()


@_whitelist
def explain_payslip(result: dict | str, employee_name: str | None = None) -> dict[str, Any]:
	return explain_result(_json(result), employee_name=employee_name)


@_whitelist
def detect_anomalies(current: dict | str, previous: dict | str | None = None) -> list[dict[str, Any]]:
	return _detect_anomalies(_json(current), _json(previous) if previous else None)
