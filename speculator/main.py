import argparse
from datetime import datetime as dt
import pandas as pd
from speculator import market
from speculator import models

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
    parser.add_argument('-l', '--long', nargs='*',
                        help=('List of features to enable longer calculations. '
                              'Example "--long rsi": 14 day RSI -> 28 day RSI'))
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
    assert args.partition > 0, 'The data must be partitioned!'

    m = market.Market(symbol=args.symbol, unit=args.unit,
                      count=args.count, period=args.period)
    features = m.features(partition=args.partition)
    if args.long is not None:
        features = m.set_long_features(features,
                                       columns_to_set=args.long,
                                       partition=args.partition)

    targets = market.targets(features, delta=args.delta)
    features = features.drop(['close'], axis=1)

    model = market.setup_model(features[:-1], targets,
                               model_type=args.model.lower(),
                               seed=args.seed,
                               n_estimators=args.trees,
                               n_jobs=args.jobs)

    next_date = features.tail(1) # Remember the entry we didn't train?  Predict it.

    # TODO: Reimplement display of confusion matrix and feature importances
    acc = model.accuracy(model.features.test, model.targets.test)
    print('Test Set Accuracy: {0:.3f}%'.format(100 * acc))

    trends = model._predict_trends(next_date)
    print('Predicted Trend: {0}'.format(market.target_code_to_name(trends[0])))

    if args.proba:
        probas = model._predict_probas(next_date)
        print('Probability: {0}'.format(probas[0]))
    if args.proba_log:
        logs = model._predict_logs(next_date)
        print('Log Probability: {0}'.format(logs[0]))

if __name__=='__main__':
    raise SystemExit(main())
