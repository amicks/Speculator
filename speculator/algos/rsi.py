"""
Relative Strength Index:
RSI = 100 - (100 / (1 + RS))
    such that,
        RS = avg(t-period gain) / avg(t-period loss)
"""
def rs_idx(gains, losses):
    """
    rs: avg(period gain) / avg(period loss)
        type: float
    
    return: Momentum indicator of a market measuring
            the speed and change of price movements.
        type: float
    """
    return 100 - (100 / (1 + rs(gains, losses)))

def rs(gains, losses):
    """
    gains: Market price gains throughout a period
        type: list of floats

    losses: Market price losses throughout a period
        type: list of floats

    return: Momentum indicator of a market measuring
            the speed and change of price movements
        type: float
    """
    # Number of days that the data was collected through
    period = len(gains) + len(losses)

    return avg(gains, period=period) / avg(losses, period=period)

def avg(vals, period=None):
    """
    nums: Values to calculate average from
        type: list of ints/floats
    
    period: Number of days that the data was collected through
        type: int

    return: Average of values throughout a period
        type: int/float
    """ 
    sum = 0
    for v in vals:
        sum += v
    if period is None:
        period = len(vals)
    return sum / period
