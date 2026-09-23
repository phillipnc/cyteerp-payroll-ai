"""Typed, framework-independent models used by the payroll engine."""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any


@dataclass(frozen=True)
class TaxBand:
	"""Progressive tax band with an optional upper bound."""

	up_to: Decimal | None
	rate: Decimal


@dataclass(frozen=True)
class Component:
	code: str
	amount: Decimal
	taxable: bool = True


@dataclass(frozen=True)
class PayrollInput:
	country: str
	rule_set: str
	currency: str
	gross_earnings: Decimal
	taxable_earnings: Decimal | None = None
	tax_bands: tuple[TaxBand, ...] = ()
	tax_relief: Decimal = Decimal("0")
	employee_deductions: tuple[Component, ...] = ()
	employer_contributions: tuple[Component, ...] = ()
	employee_id: str | None = None
	employee_name: str | None = None
	period: str | None = None


@dataclass(frozen=True)
class PayrollResult:
	country: str
	rule_set: str
	currency: str
	gross_earnings: Decimal
	taxable_earnings: Decimal
	tax: Decimal
	employee_deductions: Decimal
	net_pay: Decimal
	employer_contributions: Decimal
	employer_cost: Decimal
	employee_id: str | None = None
	employee_name: str | None = None
	period: str | None = None
	trace: tuple[str, ...] = field(default_factory=tuple)

	def as_dict(self) -> dict[str, Any]:
		return {
			"country": self.country,
			"rule_set": self.rule_set,
			"currency": self.currency,
			"gross_earnings": str(self.gross_earnings),
			"taxable_earnings": str(self.taxable_earnings),
			"tax": str(self.tax),
			"employee_deductions": str(self.employee_deductions),
			"net_pay": str(self.net_pay),
			"employer_contributions": str(self.employer_contributions),
			"employer_cost": str(self.employer_cost),
			"employee_id": self.employee_id,
			"employee_name": self.employee_name,
			"period": self.period,
			"trace": list(self.trace),
		}
