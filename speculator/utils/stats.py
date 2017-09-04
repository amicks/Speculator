"""
Various math functions used throughout Speculator
"""

def avg(vals, period=None):
    """
    nums: Values to calculate average from
        type: list of ints/floats
    
    period: Number of days that the data was collected through
        type: int

    return: Average of values throughout a period
        type: float
    """ 
    sum = 0
    for v in vals:
        sum += v
    if period is None:
        period = len(vals)
    return float(sum) / period
