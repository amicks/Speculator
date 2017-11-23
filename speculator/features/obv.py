from speculator.utils import poloniex
"""
On Balance Volume:
OBV = OBV_prev + v
    such that,
        v = volume  if close >  close_prev
        v = 0       if close == close_prev
        v = -volume if close <  close_prev
"""

def eval_algorithm(curr, prev):
    """ Evaluates OBV

    Args:
        curr: Dict of current volume and close
        prev: Dict of previous OBV and close
    
    Returns:
        Float of OBV 
    """
    if curr['close'] > prev['close']:
        v = curr['volume']
    elif curr['close'] < prev['close']:
        v = curr['volume'] * -1
    else:
        v = 0
    return prev['obv'] + v

def get_poloniex(*args):
    """ Gets OBV of a currency pair from Poloniex.com exchange

    Returns:
        Float of OBV
    """
    return from_poloniex(poloniex.get_json_shift(*args))

def from_poloniex(json):
    """ Gets OBV from a JSON of market data

    Args:
        json: List of dates where each entry is a dict of raw market data.

    Returns:
        Float of OBV
    """
    closes = poloniex.get_attribute(json, 'close')
    volumes = poloniex.get_attribute(json, 'volume')
    for date, _ in enumerate(json):
        if date == 0:
            obv = 0
            continue
        curr = {'close': closes[date], 'volume': volumes[date]}
        prev = {'close': closes[date - 1], 'obv': obv}
        obv = eval_algorithm(curr, prev)
    return obv

