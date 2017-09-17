from datetime import datetime as dt
from delorean import Delorean

def date_to_delorean(year, month, day):
    """ Converts date arguments to a Delorean instance in UTC
    
    Args:
        year: int between 1 and 9999.
        month: int between 1 and 12.
        day: int between 1 and 31.

    Returns:
        Delorean instance in UTC of date.
    """
    return Delorean(datetime=dt(year, month, day), timezone='UTC')

def date_to_epoch(year, month, day):
    """ Converts a date to epoch in UTC

    Args:
        year: int between 1 and 9999.
        month: int between 1 and 12.
        day: int between 1 and 31.

    Returns:
        Int epoch in UTC from date.
    """
    return int(date_to_delorean(year, month, day).epoch)

def now_delorean():
    """ Returns the current time as a Delorean instance in UTC """
    return Delorean(timezone='UTC')

def shift_epoch(delorean, direction, unit, count):
    """ Gets the resulting epoch after a time shift of a Delorean
    
    Args:
        delorean: Delorean datetime instance to shift from.
        direction: String to shift time forwards or backwards.
            Valid values: 'last', 'next'.
        unit: String of time period unit for count argument.
            What unit in direction should be shifted?
            Valid values: 'hour', 'day', 'week', 'month', 'year'.
        count: Int of units.
            How many units to shift in direction?

    Returns:
        Int epoch in UTC from a shifted Delorean
    """
    return int(delorean._shift_date(direction, unit, count).epoch)

def generate_epochs(delorean, direction, unit, count):
    """ Generates epochs from a shifted Delorean instance
    
    Args:
        delorean: Delorean datetime instance to shift from.
        direction: String to shift time forwards or backwards.
            Valid values: 'last', 'next'.
        unit: String of time period unit for count argument.
            What unit in direction should be shifted?
            Valid values: 'hour', 'day', 'week', 'month', 'year'.
        count: Int of units.
            How many units to shift in direction?

    Returns:
        Generator of count int epochs in UTC from a shifted Delorean
    """
    for shift in range(count):
        yield int(delorean._shift_date(direction, unit, shift).epoch)

def get_end_start_epochs(year, month, day, direction, unit, count):
    """ Gets epoch from a start date and epoch from a shifted date

    Args:
        year: Int between 1 and 9999.
        month: Int between 1 and 12.
        day: Int between 1 and 31.
        direction: String to shift time forwards or backwards.
            Valid values: 'last', 'next'.
        unit: String of time period unit for count argument.
            How far back to check historical market data.
            Valid values: 'hour', 'day', 'week', 'month', 'year'.
        count: Int of units.
            How far back to check historical market data?

    Returns:
        Dict of int epochs in UTC with keys 'initial' and 'shifted'
    """
    if year or month or day: # Date is specified
        if not year:
            year = 2017
        if not month:
            month = 1
        if not day:
            day = 1
        initial_delorean = date_to_delorean(year, month, day)
    else: # Date is not specified, get current date
        count += 1 # Get another date because market is still open
        initial_delorean = now_delorean()
    
    initial_epoch = int(initial_delorean.epoch)
    shifted_epoch = shift_epoch(initial_delorean, direction, unit, count)
    return { 'initial': initial_epoch, 'shifted': shifted_epoch }

