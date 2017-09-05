from speculator.features.algorithms import rsi as rsi_alg
from speculator.utils import date
from speculator.utils import poloniex

def rsi_poloniex(year=None, month=None, day=None,
                     unit='day', count=14,
                     period=86400, currency_pair='USDT_BTC'):
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
    epochs = date.get_end_start_epochs(year, month, day, 'last', unit, count)
    json = poloniex.chart_json(epochs['shifted'],
                               epochs['initial'], period, currency_pair)
    changes = poloniex.get_gains_losses(poloniex.parse_changes(json))
    return rsi_alg.rs_idx(changes['gains'], changes['losses'])

