from speculator.features.algorithms import stoch_osc as so_alg
from speculator.utils import date
from speculator.utils import poloniex

def so_poloniex(year=None, month=None, day=None,
                           unit='day', count=14,
                           period=86400, currency_pair='USDT_BTC'):
    epochs = date.get_end_start_epochs(year, month, day, 'last', unit, count)
    json = poloniex.chart_json(epochs['shifted'], 
                               epochs['initial'], period, currency_pair)
    close = json[-1]['close'] # Latest closing price
    low   = min(poloniex.get_attribute(json, 'low')) # Lowest low
    high  = max(poloniex.get_attribute(json, 'high')) # Highest high
    return so_alg.stochastic_oscillator(close, low, high)

