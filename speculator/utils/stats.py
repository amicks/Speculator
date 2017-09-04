"""
Various math functions used throughout Speculator
"""

def avg(vals, count=None):
    """
    nums: Values to calculate average from
        type: list of ints/floats
    count: Number of units of time that the data was collected through
        type: int

    return: Average of values throughout a count
        type: float
    """ 
    sum = 0
    for v in vals:
        sum += v
    if count is None:
        count = len(vals)
    return float(sum) / count

