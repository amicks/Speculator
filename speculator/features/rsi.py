from speculator.utils import date
from speculator.utils import poloniex
from speculator.utils import stats

"""
Relative Strength Index:
RSI = 100 - (100 / (1 + RS))
    such that,
        RS = avg(t-period gain) / avg(t-period loss)
"""

def eval_algorithm(gains, losses):
    """ Evaluates the RSI algorithm
    
    Args:
        gains: List of price gains.
        losses: List of prices losses.

    Returns:
        Float between 0 and 100, momentum indicator
        of a market measuring the speed and change of price movements.
    """
    return 100 - (100 / (1 + eval_rs(gains, losses)))

def eval_rs(gains, losses):
    """ Evaluates the RS variable in RSI algorithm

    Args:
        gains: List of price gains.
        losses: List of prices losses.

    Returns:
        Float of average gains over average losses.
    """
    # Number of days that the data was collected through
    count = len(gains) + len(losses)

    avg_gains = stats.avg(gains, count=count) if gains else 1
    avg_losses = stats.avg(losses,count=count) if losses else 1
    

    try:
        return avg_gains / avg_losses
    except ZeroDivisionError: # No losses
        return avg_gains

def get_poloniex(*args):
    """ Gets RSI of a currency pair from Poloniex.com exchange

    Returns:
        Float between 0 and 100, momentum indicator
        of a market measuring the speed and change of price movements.
    """
    return from_poloniex(poloniex.get_json_shift(*args))

def from_poloniex(json):
    """ Gets RSI from a JSON of market data
    
    Args:
        json: List of dates where each entry is a dict of raw market data.
    
    Returns:
        Float between 0 and 100, momentum indicator
        of a market measuring the speed and change of price movements.
    """
    changes = poloniex.get_gains_losses(poloniex.parse_changes(json))
    return eval_algorithm(changes['gains'], changes['losses'])
