from speculator.utils import date
from speculator.utils import poloniex
from speculator.utils import stats

"""
Simple Moving Average:
Average closing price over a period
SMA = avg(closes) = sum(closes) / len(closes)
"""

def eval_algorithm(closes):
    """ Evaluates the SMA algorithm
    
    Args:
        closes: List of price closes.

    Returns:
        Float average of closes.
    """
    return stats.avg(closes)

def get_poloniex(*args):
    """ Gets SMA of a currency pair from Poloniex.com exchange

    Returns:
        Float average of closes.
    """
    return from_poloniex(poloniex.get_json_shift(*args))

def from_poloniex(json):
    """ Gets SMA from a JSON of market data
    
    Args:
        json: List of dates where each entry is a dict of raw market data.
    
    Returns:
        Float average of closes.
    """
    closes = [date['close'] for date in json]
    return eval_algorithm(closes)
