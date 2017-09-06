import unittest
from speculator.features import sma

class SMATest(unittest.TestCase):
    def test_eval_algorithm(self):
        closes = [11, 12, 13, 14, 15, 16, 17]
        self.assertEqual(sma.eval_algorithm(closes), 14)

