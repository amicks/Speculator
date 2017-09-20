import argparse
from datetime import datetime as dt
import pandas as pd
from sklearn.metrics import accuracy_score
from speculator import analysis
from speculator.features import rsi
from speculator.features import so
from speculator.features import sma
from speculator.utils import date
from speculator.utils import poloniex

"""
Predicts the next market trend based on the markets history
"""

def get_args():
    today = dt.now()
    parser = argparse.ArgumentParser(
                        description='Predict the next crypto market trend.')
    parser.add_argument('-u', '--unit', default='month',
                        help=('Time unit to go back: '
                              'second, minute, hour, day, week, month, year'))
    parser.add_argument('-c', '--count', default=6, type=int,
                        help=('Number of "units" to go back '
                              '(behind the set date/now)'))
    parser.add_argument('-pd', '--period', default=86400, type=int,
                        help=('Number of seconds for each candlestick: '
                              '300, 900, 1800, 7200, 14400, 86400 only valid'))
    parser.add_argument('-pn', '--partition', default=14, type=int,
                        help=('Number of candlesticks per '
                              'technical analysis calculation'))
    parser.add_argument('-sy', '--symbol', default='USDT_BTC',
                        help=('Currency pair, symbol, or ticker, from Poloniex'
                              'Examples: USDT_BTC, ETH_ZRX, BTC_XRP'))
    parser.add_argument('-sd', '--seed', default=None, type=int,
                        help=('Random state seed to be used when generating '
                              'the Random Forest and training/test sets'))
    parser.add_argument('-l', '--long', default=False, action='store_true',
                        help=('Enable longer feature calculations.  Example: '
                              'A 14 day SMA would also include a 28 day SMA'))
    parser.add_argument('-d', '--delta', default=25, type=int,
                        help=('Price buffer in the neutral zone before'
                              'classifying a trend as bullish or bearish'))
    parser.add_argument('-t', '--trees', default=10, type=int,
                        help=('Number of trees (estimators) to generate in '
                              'the Random Forest, higher is usually better'))
    parser.add_argument('-j', '--jobs', default=1, type=int,
                        help=('Number of jobs (CPUs for multithreading) when '
                              'processing model fits and predictions'))
    parser.add_argument('--proba', default=False, action='store_true',
                        help='Display probabilities of the predicted trend')
    parser.add_argument('--proba_log', default=False, action='store_true',
                        help=('Display logarithmic probabilities of the '
                              'predicted trend'))
    return parser.parse_args()

def main():
    args = get_args()

    m = analysis.Market(args.symbol, unit=args.unit,
                        count=args.count, period=args.period)
    rf = analysis.setup_model(m, args.partition, args.delta, args.long,
                              n_jobs=args.jobs, n_estimators=args.trees,
                              random_state=args.seed)
    
    print('###################')
    print('# TEST SET        #')
    print('###################')
    # Get the prediction
    pred_test = rf.predict(rf.axes['features']['test'])

    # Get statistics about model and prediction
    print('Accuracy Score: {0:.3f}%'.format(
           100 * accuracy_score(rf.axes['targets']['test'], pred_test)))
    print('\nConfusion Matrix:')
    print(rf.confusion_matrix(rf.axes['targets']['test'], pred_test))
    print(analysis.TARGET_CODES)
    print('\nFeature Importance:')
    print(rf.feature_importances())

    print()
    print('###################')
    print('# PREDICTED TREND #')
    print('###################')
    pred_today = rf.predict_next_trend(proba=args.proba, log=args.proba_log)
    print('Trend: {0}'.format(analysis.target_code_to_name(pred_today['pred'])))
    if args.proba:
        print('Probabilities: {0}'.format(pred_today['proba']))
    if args.proba_log:
        print('Log Probabilities: {0}'.format(pred_today['log']))

if __name__=='__main__':
    raise SystemExit(main())
