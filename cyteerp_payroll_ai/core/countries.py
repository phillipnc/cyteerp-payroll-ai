"""Africa-wide country catalogue and country-pack readiness metadata."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Country:
	code: str
	name: str
	currency: str
	region: str
	languages: tuple[str, ...]
	status: str = "scaffold"

	def as_dict(self) -> dict:
		return asdict(self)


COUNTRIES: tuple[Country, ...] = (
	Country("DZ", "Algeria", "DZD", "North Africa", ("ar", "fr")),
	Country("AO", "Angola", "AOA", "Central Africa", ("pt",)),
	Country("BJ", "Benin", "XOF", "West Africa", ("fr",)),
	Country("BW", "Botswana", "BWP", "Southern Africa", ("en",)),
	Country("BF", "Burkina Faso", "XOF", "West Africa", ("fr",)),
	Country("BI", "Burundi", "BIF", "East Africa", ("fr", "rn")),
	Country("CV", "Cabo Verde", "CVE", "West Africa", ("pt",)),
	Country("CM", "Cameroon", "XAF", "Central Africa", ("fr", "en")),
	Country("CF", "Central African Republic", "XAF", "Central Africa", ("fr",)),
	Country("TD", "Chad", "XAF", "Central Africa", ("fr", "ar")),
	Country("KM", "Comoros", "KMF", "East Africa", ("fr", "ar")),
	Country("CG", "Congo", "XAF", "Central Africa", ("fr",)),
	Country("CD", "Democratic Republic of the Congo", "CDF", "Central Africa", ("fr",)),
	Country("CI", "Côte d'Ivoire", "XOF", "West Africa", ("fr",)),
	Country("DJ", "Djibouti", "DJF", "East Africa", ("fr", "ar")),
	Country("EG", "Egypt", "EGP", "North Africa", ("ar",)),
	Country("GQ", "Equatorial Guinea", "XAF", "Central Africa", ("es", "fr")),
	Country("ER", "Eritrea", "ERN", "East Africa", ("ar", "en", "ti")),
	Country("SZ", "Eswatini", "SZL", "Southern Africa", ("en", "ss")),
	Country("ET", "Ethiopia", "ETB", "East Africa", ("am", "en")),
	Country("GA", "Gabon", "XAF", "Central Africa", ("fr",)),
	Country("GM", "The Gambia", "GMD", "West Africa", ("en",)),
	Country("GH", "Ghana", "GHS", "West Africa", ("en",)),
	Country("GN", "Guinea", "GNF", "West Africa", ("fr",)),
	Country("GW", "Guinea-Bissau", "XOF", "West Africa", ("pt",)),
	Country("KE", "Kenya", "KES", "East Africa", ("en", "sw")),
	Country("LS", "Lesotho", "LSL", "Southern Africa", ("en", "st")),
	Country("LR", "Liberia", "LRD", "West Africa", ("en",)),
	Country("LY", "Libya", "LYD", "North Africa", ("ar",)),
	Country("MG", "Madagascar", "MGA", "East Africa", ("fr", "mg")),
	Country("MW", "Malawi", "MWK", "Southern Africa", ("en", "ny")),
	Country("ML", "Mali", "XOF", "West Africa", ("fr",)),
	Country("MR", "Mauritania", "MRU", "North Africa", ("ar", "fr")),
	Country("MU", "Mauritius", "MUR", "East Africa", ("en", "fr")),
	Country("MA", "Morocco", "MAD", "North Africa", ("ar", "fr")),
	Country("MZ", "Mozambique", "MZN", "Southern Africa", ("pt",)),
	Country("NA", "Namibia", "NAD", "Southern Africa", ("en",)),
	Country("NE", "Niger", "XOF", "West Africa", ("fr",)),
	Country("NG", "Nigeria", "NGN", "West Africa", ("en",)),
	Country("RW", "Rwanda", "RWF", "East Africa", ("en", "fr", "rw")),
	Country("ST", "São Tomé and Príncipe", "STN", "Central Africa", ("pt",)),
	Country("SN", "Senegal", "XOF", "West Africa", ("fr",)),
	Country("SC", "Seychelles", "SCR", "East Africa", ("en", "fr")),
	Country("SL", "Sierra Leone", "SLE", "West Africa", ("en",)),
	Country("SO", "Somalia", "SOS", "East Africa", ("so", "ar")),
	Country("ZA", "South Africa", "ZAR", "Southern Africa", ("en",)),
	Country("SS", "South Sudan", "SSP", "East Africa", ("en",)),
	Country("SD", "Sudan", "SDG", "North Africa", ("ar", "en")),
	Country("TZ", "Tanzania", "TZS", "East Africa", ("sw", "en")),
	Country("TG", "Togo", "XOF", "West Africa", ("fr",)),
	Country("TN", "Tunisia", "TND", "North Africa", ("ar", "fr")),
	Country("UG", "Uganda", "UGX", "East Africa", ("en", "sw")),
	Country("ZM", "Zambia", "ZMW", "Southern Africa", ("en",)),
	Country("ZW", "Zimbabwe", "USD", "Southern Africa", ("en",)),
)

COUNTRY_INDEX = {country.code: country for country in COUNTRIES}


def get_country(code: str) -> Country:
	"""Return a country by ISO alpha-2 code, normalising user input."""
	normalised = code.strip().upper()
	try:
		return COUNTRY_INDEX[normalised]
	except KeyError as exc:
		raise ValueError(f"Unsupported African country code: {code}") from exc


def country_catalog() -> list[dict]:
	return [country.as_dict() for country in COUNTRIES]
