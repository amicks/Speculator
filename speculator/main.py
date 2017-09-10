from speculator.features import rsi, so, sma
from speculator.utils import date, poloniex
from datetime import datetime as dt
import argparse

def get_args():
    today = dt.now()
    parser = argparse.ArgumentParser(
        description='Get market statistics from Poloniex.com')
    parser.add_argument('-y', '--year', default=today.year, type=int, help='Initial year')
    parser.add_argument('-m', '--month', default=today.month, type=int, help='Initial month')
    parser.add_argument('-d', '--day', default=today.day, type=int, help='Initial day')
    parser.add_argument('-u', '--unit', default='day',
        help='second, minute, hour, day, week, month, year')
    parser.add_argument('-c', '--count', default=14, type=int,
        help='Number of "units" to go back (behind the set date/now)')
    parser.add_argument('-p', '--period', default=86400, type=int,
        help='Number of seconds for each candlestick: ' \
        '300, 900, 1800, 7200, 14400, 86400 only valid')
    parser.add_argument('-s', '--symbol', default='USDT_BTC',
        help='Currency pairs, ex: USDT_BTC')
    return parser.parse_args()

def main():
    args = get_args()

    epochs = date.get_end_start_epochs(args.year, args.month, args.day,
        'last', args.unit, args.count)
    json = poloniex.chart_json(epochs['shifted'], 
        epochs['initial'], args.period, args.symbol)

    print('Relative Strength Index:')
    print(rsi.from_poloniex(json))
    #print(rsi.get_poloniex(args.year, args.month, args.day,
    #    args.unit, args.count, args.period, args.symbol))

    print('Stochastic Oscillator:')
    print(so.from_poloniex(json))
    #print(so.get_poloniex(args.year, args.month, args.day,
    #    args.unit, args.count, args.period, args.symbol))

    print('Simple Moving Average:')
    print(sma.from_poloniex(json))
    #print(sma.get_poloniex(args.year, args.month, args.day,
    #    args.unit, args.count, args.period, args.symbol))

    

if __name__=='__main__':
    raise SystemExit(main())
