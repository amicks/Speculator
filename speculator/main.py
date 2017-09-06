from speculator.features import rsi, so, sma
import argparse

def get_args():
    parser = argparse.ArgumentParser(
        description='Get market statistics from Poloniex.com')
    parser.add_argument('-y', '--year', default=2017, type=int, help='Initial year')
    parser.add_argument('-m', '--month', default=1, type=int, help='Initial month')
    parser.add_argument('-d', '--day', default=1, type=int, help='Initial day')
    parser.add_argument('-u', '--unit', default='day',
        help='second, minute, hour, day, week, month, year')
    parser.add_argument('-c', '--count', default=3, type=int,
        help='Number of "units" to go back (behind the set date/now)')
    parser.add_argument('-p', '--period', default=7200, type=int,
        help='Number of seconds for each candlestick: ' \
        '300, 900, 1800, 7200, 14400, 86400 only valid')
    parser.add_argument('-s', '--symbol', default='USDT_BTC',
        help='Currency pairs, ex: USDT_BTC')
    return parser.parse_args()

def main():
    args = get_args()
    print('Relative Strength Index:')
    print(rsi.get_poloniex(args.year, args.month, args.day,
        args.unit, args.count, args.period, args.symbol))

    print('Stochastic Oscillator:')
    print(so.get_poloniex(args.year, args.month, args.day,
        args.unit, args.count, args.period, args.symbol))

    print('Simple Moving Average:')
    print(sma.get_poloniex(args.year, args.month, args.day,
        args.unit, args.count, args.period, args.symbol))

if __name__=='__main__':
    raise SystemExit(main())
