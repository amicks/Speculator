import unittest
from speculator.features.algorithms.stoch_osc import stochastic_oscillator

class StochOscAlgTest(unittest.TestCase):
    def test_stochastic_oscillator(self):
        closing = 127.29
        low     = 124.56
        high    = 128.43
        self.assertAlmostEqual(stochastic_oscillator(closing, low, high),
                               70.54, places=2)

