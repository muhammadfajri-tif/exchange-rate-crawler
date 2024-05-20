import unittest
from utils import parse_price_rate

class TestParsePriceRateMethod(unittest.TestCase):
    def test_rate_no_diff(self):
        diff = "15.200,00"
        self.assertEqual(parse_price_rate(diff), "15200.00")

    def test_rate_no_diff_yen(self):
        diff_yen = "105,00"
        self.assertEqual(parse_price_rate(diff_yen), "105.00")

    def test_rate_invalid_price(self):
        diff = "69.420,,,,"
        self.assertIsNone(parse_price_rate(diff))

    def test_rate_invalid_price_dots(self):
        diff = "1...30"
        self.assertIsNone(parse_price_rate(diff))

    def test_rate_null(self):
        diff = ""
        self.assertIsNone(parse_price_rate(diff))

    def test_rate_random_string(self):
        diff = "this is random string"
        self.assertIsNone(parse_price_rate(diff))

    def test_rate_random_string_with_special_chars(self):
        diff = "this is, random string."
        self.assertIsNone(parse_price_rate(diff))

if __name__ == '__main__':
    unittest.main()
