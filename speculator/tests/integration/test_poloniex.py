from speculator.features import obv
from speculator.features import rsi
from speculator.features import sma
from speculator.features import so
from speculator.utils import date
from speculator.utils import poloniex
import unittest
        
# https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start=1483228800&end=1483315200&period=86400

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

EXPECTED_CHANGES = ([EXPECTED_RESPONSE[1]['close'] -
                     EXPECTED_RESPONSE[0]['close']])

YEAR          = 2017
MONTH         = 1
DAY           = 1
UNIT          = 'day'
COUNT         = 3
PERIOD        = 86400
SYMBOL        = 'USDT_BTC'
EPOCH1        = 1483228800 # 01/01/2017, 00:00 epoch
EPOCH2        = 1483315200 # 01/02/2017, 00:00 epoch
HTTP_RESPONSE = poloniex.chart_json(EPOCH1, EPOCH2, PERIOD, SYMBOL)[0]

class PoloniexIntegrationTest(unittest.TestCase):
    def test_parse_changes(self):
        self.assertEqual(poloniex.parse_changes(HTTP_RESPONSE),
                         EXPECTED_CHANGES) 

    def test_get_gains_losses(self):
        res = {'gains': [g for g in EXPECTED_CHANGES if g >= 0],
               'losses': [l for l in EXPECTED_CHANGES if l < 0]}
        self.assertEqual(poloniex.get_gains_losses(
                         poloniex.parse_changes(HTTP_RESPONSE)), res)

    def test_get_attribute(self):
        res = [attribute['quoteVolume'] for attribute in HTTP_RESPONSE]
        attr = 'quoteVolume'
        self.assertEqual(poloniex.get_attribute(HTTP_RESPONSE, attr), res) 

    def test_get_rsi_poloniex(self):
        eval_rsi = rsi.get_poloniex(YEAR, MONTH, DAY,
                                    UNIT, COUNT, PERIOD, SYMBOL) 
        self.assertAlmostEqual(eval_rsi, 71.888274, places=4)

    def test_get_stoch_osc_poloniex(self):
        eval_so = so.get_poloniex(YEAR, MONTH, DAY,
                                  UNIT, COUNT, PERIOD, SYMBOL)
        self.assertAlmostEqual(eval_so, 88.9532721773, places=4)

    def test_get_sma_poloniex(self):
        eval_sma = sma.get_poloniex(YEAR, MONTH, DAY,
                                    UNIT, COUNT, PERIOD, SYMBOL)
        self.assertAlmostEqual(eval_sma, 974.808582, places=4)

    def test_get_obv_poloniex(self):
        eval_obv = obv.get_poloniex(YEAR, MONTH, DAY,
                                    UNIT, COUNT, PERIOD, SYMBOL)
        self.assertAlmostEqual(eval_obv, 78590.3475, places=4)
