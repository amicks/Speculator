import unittest
from speculator.features import so

class SOTest(unittest.TestCase):
    def test_eval_algorithm(self):
        closing = 127.29
        low     = 124.56
        high    = 128.43
        self.assertAlmostEqual(
            so.eval_algorithm(closing, low, high), 70.54, places=2)

