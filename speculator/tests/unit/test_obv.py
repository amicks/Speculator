from speculator.features.OBV import OBV
import unittest

class OBVTest(unittest.TestCase):
    def test_eval_algorithm_case1(self):
        # Case 1: close > close_prev, return obv + volume
        curr = {'close': 5, 'volume': 1}
        prev = {'close': 4, 'obv': 2}
        self.assertEqual(OBV.eval_algorithm(curr, prev), 3)

    def test_eval_algorithm_case2(self):
        # Case 2: close == close_prev, return obv
        curr = {'close': 5, 'volume': 1}
        prev = {'close': 5, 'obv': 2}
        self.assertEqual(OBV.eval_algorithm(curr, prev), 2)

    def test_eval_algorithm_case3(self):
        # Case 3: close < close_prev, return obv - volume
        curr = {'close': 5, 'volume': 1}
        prev = {'close': 6, 'obv': 2}
        self.assertEqual(OBV.eval_algorithm(curr, prev), 1)
