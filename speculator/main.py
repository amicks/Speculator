import argparse
from datetime import datetime as dt
import pandas as pd
from sklearn.metrics import accuracy_score
from speculator import market
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
    parser.add_argument('-m', '--model', default='random_forest',
                        help=('Machine learning model to use on market data'))
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

    m = market.Market(symbol=args.symbol, unit=args.unit,
                      count=args.count, period=args.period)
    x = m.features(partition=args.partition)
    y = market.targets(x, delta=args.delta)
    model = market.setup_model(x[:-1], y,
                               model_type=args.model,
                               seed=args.seed,
                               n_estimators=args.trees,
                               n_jobs=args.jobs)

    # Predict the target test set from the features test set
    pred = model.predict(model.features.test)

    # Get accuracies
    ftr_imps = model.feature_importances()
    conf_mx = model.confusion_matrix(model.targets.test, pred)
    acc = model.accuracy(model.targets.test, pred)

    # Display accuracies
    print('##################')
    print('# TEST SET       #')
    print('##################')
    print('Accuracy: {0:.3f}%'.format(100 * acc))
    print('\nConfusion Matrix:')
    print(conf_mx)
    print(market.TARGET_CODES)
    print('\nFeature Importance:')
    for ftr, imp in ftr_imps:
        print('  {0}: {1:.3f}%'.format(ftr, 100 * imp))

    print()

    # Display prediction and probabilities for the next trend
    print('##################')
    print('# PREDICTED NEXT #')
    print('##################')
    next_date = x.tail(1) # Remember the entry we didn't train?  Predict it.
    trend = market.target_code_to_name(model.predict(next_date)[0])
    print('Trend: {0}'.format(trend))
    if args.proba:
        print('Probability: {0}'.format(model.predict_proba(next_date)))
    if args.proba_log:
        print('Log Probability: {0}'.format(model.predict_log_proba(next_date)))

if __name__=='__main__':
    raise SystemExit(main())
