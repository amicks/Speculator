from speculator.features import rsi
from speculator.utils import poloniex
from speculator.utils import date
import sys

def get_rsi_poloniex(year=None, month=None, day=None,
                     direction='last', unit='day', count=14,
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
    if year or month or day: # Date is specified
        if not year:
            year = 2017
        if not month:
            month = 1
        if not day:
            day = 1
        cur_delorean = date.date_to_delorean(year, month, day)
    else: # Date is not specified, get current date
        count += 1 # Get another date because market is still open
        direction = 'last' # Can't get future prices, must go back
        cur_delorean = date.now_delorean()
    
    cur_epoch = int(cur_delorean.epoch)
    prev_epoch = date.shift_epoch(cur_delorean, direction, unit, count) 

    json = poloniex.chart_json(prev_epoch, cur_epoch, period, currency_pair)
    changes = poloniex.get_gains_losses(poloniex.parse_changes(json))
    return rsi.rs_idx(changes['gains'], changes['losses'])
    
def main():
    print(get_rsi_poloniex(unit='day', count=3, currency_pair='USDT_BTC'))

if __name__=='__main__':
    sys.exit(main())
