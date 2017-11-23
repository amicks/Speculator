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

