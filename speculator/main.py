from speculator.features import rsi
from speculator.utils import poloniex
from speculator.utils import date
import sys

def get_rsi_poloniex(direction='last', unit='day', count=14, period=86400, currency_pair='USDT_BTC'):
    now_delorean = date.now_delorean()
    now_epoch = int(now_delorean.epoch)
    prev_epoch = date.shift_epoch(now_delorean, direction, unit, count + 1) # +1 for initial date
    print('prev_epoch: {0}'.format(prev_epoch))
    print('now_epoch: {0}'.format(now_epoch))

    json = poloniex.chart_json(prev_epoch, now_epoch, period, currency_pair)
    changes = poloniex.get_gains_losses(poloniex.parse_changes(json))
    return rsi.rs_idx(changes['gains'], changes['losses'])
    
def main():
    print(get_rsi_poloniex(unit='day', count=3))

if __name__=='__main__':
    sys.exit(main())
