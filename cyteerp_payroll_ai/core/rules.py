"""Deterministic payroll calculation primitives."""

from decimal import ROUND_HALF_UP, Decimal

from .models import PayrollInput, PayrollResult, TaxBand

CENT = Decimal("0.01")


def money(value: Decimal | int | float | str) -> Decimal:
	"""Normalise a value to two decimal places using payroll rounding."""
	return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)


def progressive_tax(taxable_income: Decimal, bands: tuple[TaxBand, ...]) -> tuple[Decimal, list[str]]:
	"""Calculate tax from ordered bands and return an auditable trace."""
	income = max(Decimal("0"), taxable_income)
	if not bands:
		return Decimal("0.00"), ["No approved tax bands supplied; tax calculated as 0.00."]

	tax = Decimal("0")
	lower = Decimal("0")
	trace: list[str] = []
	for index, band in enumerate(bands, start=1):
		if band.rate < 0 or band.rate > 1:
			raise ValueError(f"Tax band {index} rate must be between 0 and 1.")
		upper = band.up_to
		if upper is not None and upper < lower:
			raise ValueError(f"Tax band {index} upper bound is below the previous band.")
		band_income = max(Decimal("0"), (upper if upper is not None else income) - lower)
		band_income = min(band_income, max(Decimal("0"), income - lower))
		band_tax = band_income * band.rate
		tax += band_tax
		trace.append(
			f"Band {index}: {money(band_income)} at {band.rate * 100}% = {money(band_tax)}."
		)
		lower = upper if upper is not None else income
		if lower >= income:
			break
	return money(tax), trace


def calculate_payroll(payload: PayrollInput) -> PayrollResult:
	"""Calculate a gross-to-net result without importing Frappe or an LLM."""
	gross = money(payload.gross_earnings)
	taxable = money(payload.taxable_earnings if payload.taxable_earnings is not None else gross)
	relief = money(payload.tax_relief)
	tax_base = max(Decimal("0.00"), taxable - relief)
	tax, tax_trace = progressive_tax(tax_base, payload.tax_bands)
	employee_deductions = money(sum((money(item.amount) for item in payload.employee_deductions), Decimal("0")))
	employer_contributions = money(
		sum((money(item.amount) for item in payload.employer_contributions), Decimal("0"))
	)
	net_pay = money(gross - tax - employee_deductions)
	employer_cost = money(gross + employer_contributions)
	trace = [
		f"Gross earnings: {gross} {payload.currency}.",
		f"Taxable earnings: {taxable} {payload.currency}.",
		f"Tax relief: {relief} {payload.currency}; taxable base: {tax_base} {payload.currency}.",
		*tax_trace,
		f"Employee deductions excluding tax: {employee_deductions} {payload.currency}.",
		f"Net pay: {net_pay} {payload.currency}.",
		f"Employer contributions: {employer_contributions} {payload.currency}.",
	]
	return PayrollResult(
		country=payload.country.upper(),
		rule_set=payload.rule_set,
		currency=payload.currency.upper(),
		gross_earnings=gross,
		taxable_earnings=taxable,
		tax=tax,
		employee_deductions=money(tax + employee_deductions),
		net_pay=net_pay,
		employer_contributions=employer_contributions,
		employer_cost=employer_cost,
		employee_id=payload.employee_id,
		employee_name=payload.employee_name,
		period=payload.period,
		trace=tuple(trace),
	)
