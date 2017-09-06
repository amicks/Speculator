from speculator.utils import date, poloniex

"""
Stochastic Oscillator:
%K = 100 * (C - L(t)) / (H14 - L(t))
    such that,
        C = Current closing Price
        L(t) = Lowest Low over some duration t
        H(t) = Highest High over some duration t
          * t is usually 14 days

%K follows the speed/momentum of a price in a market
"""

def eval_algorithm(closing, low, high):
    return 100 * (closing - low) / (high - low)

def get_poloniex(year, month, day, unit, count, period, currency_pair):
    epochs = date.get_end_start_epochs(year, month, day, 'last', unit, count)
    json   = poloniex.chart_json(epochs['shifted'], 
                                 epochs['initial'], period, currency_pair)
    close  = json[-1]['close'] # Latest closing price
    low    = min(poloniex.get_attribute(json, 'low')) # Lowest low
    high   = max(poloniex.get_attribute(json, 'high')) # Highest high
    return eval_algorithm(close, low, high)

