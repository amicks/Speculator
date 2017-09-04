import unittest
from speculator import main

class GetRSIPoloniexTest(unittest.TestCase):
    def test_get_rsi_poloniex(self):
        rsi = main.get_rsi_poloniex(year=2017, month=1, day=1, unit='day', count=3) 
        self.assertAlmostEqual(rsi, 71.888274, places=4)

