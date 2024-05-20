import unittest
from utils import parse_bank_name


class TestParseBankNameMethod(unittest.TestCase):
    def test_url(self):
        url = "https://kursdollar.org/bank/bi.php"
        self.assertEqual(parse_bank_name(url), 'bi')

    def test_url_with_param(self):
        url_param = "https://kursdollar.org/bank/bi.php?v_range=01/01/2024-05/31/2024"
        self.assertEqual(parse_bank_name(url_param), 'bi')


if __name__ == '__main__':
    unittest.main()
