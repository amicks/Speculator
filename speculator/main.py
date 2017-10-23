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

def predict(model_type, x, y=None):
    if model_type == 'random_forest' or model_type == 'rf':
        pass
    elif model_type == 'deep_neural_network' or model_type == 'dnn':
        pass

def main():
    args = get_args()

    m = market.Market(symbol=args.symbol, unit=args.unit,
                      count=args.count, period=args.period)
    x = m.features(partition=args.partition)
    if args.long is not None:
        # Create long features DataFrame
        x_long = m.features(partition=2 * args.partition)

        # Remove features not specified by args.long
        unwanted_features = [f for f in x.columns if f not in args.long]
        x_long = x_long.drop(unwanted_features, axis=1)
        
        # Prefix long columns with 'long_' to fix naming conflicts
        x_long.columns = ['long_{0}'.format(f) for f in x_long.columns]

        # Merge the two DataFrames
        skip = args.partition
        x = pd.concat([x[skip:].reset_index(drop=True), x_long], axis=1)

    y = market.targets(x, delta=args.delta)
    x = x.drop(['close'], axis=1)
    model = market.setup_model(x[:-1], y,
                               model_type=args.model.lower(),
                               seed=args.seed,
                               n_estimators=args.trees,
                               n_jobs=args.jobs)

    next_date = x.tail(1) # Remember the entry we didn't train?  Predict it.
    if type(model) is models.deep_neural_network.DeepNeuralNetwork:
        trend = market.target_code_to_name(model._predict_trends(next_date)[0])
        acc = model.accuracy(model.features.test, model.targets.test)
        probas = model._predict_probas(next_date)
        logs = model._predict_logs(next_date)
        pred_test = model._predict_trends(model.features.test)
        print(trend)
        print(probas)
        print(logs)
        print(acc)
    elif type(model) is models.random_forest.RandomForest:
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
        trend = market.target_code_to_name(model.predict(next_date)[0])
        print('Trend: {0}'.format(trend))
        if args.proba:
            print('Probability: {0}'.format(model.predict_proba(next_date)))
        if args.proba_log:
            print('Log Probability: {0}'.format(model.predict_log_proba(next_date)))

if __name__=='__main__':
    raise SystemExit(main())
