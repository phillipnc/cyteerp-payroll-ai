"""Provider boundary for optional external language-model explanations."""

from dataclasses import dataclass
from typing import Any, Protocol


class PayrollAIProvider(Protocol):
	def explain(self, result: dict[str, Any], question: str | None = None) -> str:
		"""Return an explanation for a payroll result."""


@dataclass(frozen=True)
class DeterministicProvider:
	"""Default provider; safe for installations with no external AI configured."""

	def explain(self, result: dict[str, Any], question: str | None = None) -> str:
		currency = result.get("currency", "")
		return (
			f"Net pay is {result.get('net_pay', '0.00')} {currency}; "
			f"tax is {result.get('tax', '0.00')} {currency}. "
			"See the calculation trace for the approved rule-set steps."
		)
