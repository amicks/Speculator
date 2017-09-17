import argparse
from datetime import datetime as dt
from speculator import analysis
from speculator.features import rsi
from speculator.features import so
from speculator.features import sma
from speculator.utils import date
from speculator.utils import poloniex

def get_args():
    today = dt.now()
    parser = argparse.ArgumentParser(
                        description='Get market statistics from Poloniex.com')
    parser.add_argument('-y', '--year', default=today.year,
                        type=int, help='Initial year')
    parser.add_argument('-m', '--month', default=today.month,
                        type=int, help='Initial month')
    parser.add_argument('-d', '--day', default=today.day,
                        type=int, help='Initial day')
    parser.add_argument('-u', '--unit', default='day',
                        help='second, minute, hour, day, week, month, year')
    parser.add_argument('-c', '--count', default=14, type=int,
                        help=('Number of "units" to go back '
                              '(behind the set date/now)'))
    parser.add_argument('-p', '--period', default=86400, type=int,
                        help=('Number of seconds for each candlestick: '
                              '300, 900, 1800, 7200, 14400, 86400 only valid'))
    parser.add_argument('-s', '--symbol', default='USDT_BTC',
                        help='Currency pairs, ex: USDT_BTC')
    return parser.parse_args()

def main():
    args = get_args()
    rf = analysis.RandomForest(seed=0)
    rf.fit_data(random_state=rf.seed)
    rf.predict_test_set()
    print(rf.accuracy())
    print(rf.confusion_matrix())
    print(rf.feature_importances())

if __name__=='__main__':
    raise SystemExit(main())
