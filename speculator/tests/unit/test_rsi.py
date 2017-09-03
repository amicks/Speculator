import unittest
import speculator.algos.rsi as RSI

class RSITest(unittest.TestCase):
    def test_avg(self):
        nums = [0.24, 0.62, 0.15, 0.83, 0.12345] 
        self.assertEqual(RSI.avg(nums), 0.39269)

        nums = [0.24, 0.62, 0.15, 0.83, 0.12345] 
        self.assertEqual(RSI.avg(nums, period=8), 0.24543125)

    def test_rs(self):
        gains = [0.07, 0.73, 0.51, 0.28, 0.34, 0.43, 0.25, 0.15, 0.68, 0.24]
        losses = [0.23, 0.53, 0.18, 0.40]
        self.assertAlmostEqual(RSI.rs(gains, losses), 2.746, places=3)

    def test_rs_idx(self):
        gains = [0.07, 0.73, 0.51, 0.28, 0.34, 0.43, 0.25, 0.15, 0.68, 0.24]
        losses = [0.23, 0.53, 0.18, 0.40]
        self.assertAlmostEqual(RSI.rs_idx(gains, losses), 73.307, places=3)
        
