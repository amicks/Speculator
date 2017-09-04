import unittest
from speculator.utils import date

class DateTest(unittest.TestCase):
    def test_generate_epochs(self):
        delorean = date.date_to_delorean(2000, 1, 1)
        epochs = date.generate_epochs(delorean, 'last', 'day', 3)
        
        expected_epochs = [946684800, 946598400, 946512000]
        self.assertEqual(epochs, expected_epochs) 
        
