import unittest
from speculator.utils import poloniex
        
# https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start=1483228800&end=1483272000&period=86400

EXPECTED_RESPONSE = [{'close': 999.36463982,
                      'date': 1483228800,
                      'high': 1008.54999326,
                      'low': 957.02,
                      'open': 965.00000055,
                      'quoteVolume': 1207.33863593,
                      'volume': 1196868.2615889,
                      'weightedAverage': 991.32772361},
                     {'close': 1019.00000076,
                      'date': 1483315200,
                      'high': 1034.32896003,
                      'low': 994.00000044,
                      'open': 999.92218873,
                      'quoteVolume': 1818.58703006,
                      'volume': 1847781.3863449,
                      'weightedAverage': 1016.0533182}]

EXPECTED_CHANGES = [EXPECTED_RESPONSE[1]['close'] - EXPECTED_RESPONSE[0]['close']]

class PoloniexTest(unittest.TestCase):
    def test_chart_json(self):
        ny_midnight   = 1483228800 # 01/01/2017, 00:00
        ny_noon       = 1483315200 # 01/02/2017, 00:00
        period        = 86400
        currency_pair = 'USDT_BTC'
        http_response = poloniex.chart_json(ny_midnight, ny_noon, period, currency_pair)
        self.assertEqual(http_response, EXPECTED_RESPONSE)

    def test_parse_changes(self):
        self.assertEqual(poloniex.parse_changes(EXPECTED_RESPONSE), EXPECTED_CHANGES)

    def test_get_gains_losses(self):
        res = {'gains': [g for g in EXPECTED_CHANGES if g >= 0],
               'losses': [l for l in EXPECTED_CHANGES if l < 0]}
        self.assertEqual(poloniex.get_gains_losses(EXPECTED_CHANGES), res)

