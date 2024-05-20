import unittest
from utils import parse_price_rate

class TestParsePriceRateMethod(unittest.TestCase):
    def test_rate_no_diff(self):
        diff = "15.200,00"
        self.assertEqual(parse_price_rate(diff), "15200.00")

    def test_rate_no_diff_yen(self):
        diff_yen = "105,00"
        self.assertEqual(parse_price_rate(diff_yen), "105.00")

    def test_rate_null(self):
        diff = ""
        self.assertIsNone(parse_price_rate(diff))

if __name__ == '__main__':
    unittest.main()
