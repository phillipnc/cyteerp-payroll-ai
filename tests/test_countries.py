import unittest

from cyteerp_payroll_ai.core.countries import COUNTRIES, country_catalog, get_country


class CountryCatalogueTests(unittest.TestCase):
	def test_catalogue_has_54_countries(self):
		self.assertEqual(len(COUNTRIES), 54)
		self.assertEqual(len({country.code for country in COUNTRIES}), 54)
		self.assertEqual(len(country_catalog()), 54)

	def test_zimbabwe_metadata(self):
		country = get_country("zw")
		self.assertEqual(country.currency, "USD")
		self.assertEqual(country.region, "Southern Africa")

	def test_unknown_country_is_rejected(self):
		with self.assertRaises(ValueError):
			get_country("XX")
