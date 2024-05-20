import unittest
from utils import parse_rate

class TestParseRateMethod(unittest.TestCase):
    def test_rate_negative_diff(self):
        diff = "15.800,00 (-25,00)"
        self.assertEqual(parse_rate(diff), ("15800.00", -25.0))

    def test_rate_negative_diff_yen(self):
        diff_yen = "101,00 (-2,00)"
        self.assertEqual(parse_rate(diff_yen), ("101.00", -2.0))
    
    def test_rate_negative_diff_float(self):
        diff = "15.800,00 (-4,20)"
        self.assertEqual(parse_rate(diff), ("15800.00", -4.20))
        
    def test_rate_positive_diff(self):
        diff = "10.313,00 (+8,00)"
        self.assertEqual(parse_rate(diff), ("10313.00", 8.0))

    def test_rate_positive_diff_yen(self):
        diff_yen = "103,00 (+2,00)"
        self.assertEqual(parse_rate(diff_yen), ("103.00", 2.0))

    def test_rate_positive_diff_float(self):
        diff = "10.313,00 (+8,69)"
        self.assertEqual(parse_rate(diff), ("10313.00", 8.69))

    def test_rate_no_diff(self):
        diff = "15.200,00"
        self.assertEqual(parse_rate(diff), ("15200.00", 0))

    def test_rate_no_diff_yen(self):
        diff_yen = "105,00"
        self.assertEqual(parse_rate(diff_yen), ("105.00", 0))

if __name__ == '__main__':
    unittest.main()
