from speculator.features import rsi
from speculator.utils import poloniex
from speculator.utils import date
import sys

def get_rsi_poloniex(year=None, month=None, day=None,
                     direction='last', unit='day', count=14,
                     period=86400, currency_pair='USDT_BTC'):
    if year or month or day:
        if not year:
            year = 2017
        if not month:
            month = 1
        if not day:
            day = 1
        cur_delorean = date.date_to_delorean(year, month, day)
    else:
        # Market never 'closed' because it's still open
        # -> add 1 to the count to get another date
        count += 1
        cur_delorean = date.now_delorean()
    
    cur_epoch = int(cur_delorean.epoch)
    prev_epoch = date.shift_epoch(cur_delorean, direction, unit, count) 

    json = poloniex.chart_json(prev_epoch, cur_epoch, period, currency_pair)
    changes = poloniex.get_gains_losses(poloniex.parse_changes(json))
    return rsi.rs_idx(changes['gains'], changes['losses'])
    
def main():
    print(get_rsi_poloniex(unit='day', count=3))

if __name__=='__main__':
    sys.exit(main())
