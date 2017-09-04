import unittest
from speculator.utils import math

class MathTest(unittest.TestCase):
    def test_avg(self):
        nums = [0.24, 0.62, 0.15, 0.83, 0.12345] 
        self.assertEqual(math.avg(nums), 0.39269)

        nums = [0.24, 0.62, 0.15, 0.83, 0.12345] 
        self.assertEqual(math.avg(nums, period=8), 0.24543125)
