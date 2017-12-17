from speculator.features.RSI import RSI
import unittest

class RSITest(unittest.TestCase):
    def test_eval_rs(self):
        gains = [0.07, 0.73, 0.51, 0.28, 0.34, 0.43, 0.25, 0.15, 0.68, 0.24]
        losses = [0.23, 0.53, 0.18, 0.40]
        self.assertAlmostEqual(RSI.eval_rs(gains, losses), 2.746, places=3)

    def test_eval_algorithm(self):
        gains = [0.07, 0.73, 0.51, 0.28, 0.34, 0.43, 0.25, 0.15, 0.68, 0.24]
        losses = [0.23, 0.53, 0.18, 0.40]
        self.assertAlmostEqual(RSI.eval_algorithm(gains, losses),
                               73.307, places=3)
