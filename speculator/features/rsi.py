from speculator.utils import date, poloniex, stats

"""
Relative Strength Index:
RSI = 100 - (100 / (1 + RS))
    such that,
        RS = avg(t-period gain) / avg(t-period loss)
"""

def eval_algorithm(gains, losses):
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

def get_poloniex(year, month, day, unit, count, period, currency_pair):
    """
    Gets RSI of a currency pair from Poloniex.com exchange
year: 1 <= year <= 9999, Poloniex market on year
        type: integer
    month: 1 <= month <= 12, Poloniex market on month
        type: integer
    day: 1 <= day <= 31, Poloniex market on day
        type: integer
    direction: 'last' (move backwards in time) or
               'next' (move forwards in time)
        type: string
    unit: 'day', 'week', 'month', 'year' (Poloniex doesn't accept smaller times)
        type: string
    num_shifts: Number of shifts by unit in direction
        type: integer
    period: Candlestick period in seconds.
            Valid values: 300, 900, 1800, 7200, 14400, 86400
        type: int
    
    currency_pair: Currency symbols to compare
        type: string

    return: Momentum indicator of a market measuring
            the speed and change of price movements
        type: float
    """
    epochs  = date.get_end_start_epochs(year, month, day, 'last', unit, count)
    json    = poloniex.chart_json(epochs['shifted'],
                                  epochs['initial'], period, currency_pair)
    changes = poloniex.get_gains_losses(poloniex.parse_changes(json))
    return eval_algorithm(changes['gains'], changes['losses'])

