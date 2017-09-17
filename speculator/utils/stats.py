"""
Various math functions used throughout Speculator
"""

def avg(vals, count=None):
    """ Returns the average value

    Args:
        vals: List of numbers to calculate average from.
        count: Int of total count that vals was part of.

    Returns:
        Float average value throughout a count.
    """ 
    sum = 0
    for v in vals:
        sum += v
    if count is None:
        count = len(vals)
    return float(sum) / count

