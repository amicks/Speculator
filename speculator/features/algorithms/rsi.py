from speculator.utils import stats

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
    return 100 - (100 / (1 + eval_rs(gains, losses)))

def eval_rs(gains, losses):
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
    count = len(gains) + len(losses)
    return stats.avg(gains, count=count) / stats.avg(losses, count=count)

