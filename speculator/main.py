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

    m = analysis.Market('USDT_BTC')

    # Create two DataFrames, short and long partition times
    ptn_short = 14
    ptn_long = 28
    df_short = m.dataframe(ptn_short)
    df_long = m.dataframe(ptn_long)
    
    # Update column names to avoid conflicts
    df_long.columns = ['long_{0}'.format(c) for c in df_long.columns]

    # Merge the two DataFrames
    df = pd.concat([df_short[14:].reset_index(drop=True), df_long], axis=1)

    # Feed the DataFrame to a Random Forest Classifier
    rf = analysis.RandomForest(df, random_state=SEED, oob_score=True)
    rf.set_training_targets(25)
    rf.split_sets(random_state=SEED)
    rf.train()
    
    # Get the predictions and accuracies
    pred = rf.predict(rf.axes['features']['test'])
    print('Accuracy Score: {0:.3f}%'.format(
           100 * accuracy_score(rf.axes['targets']['test'], pred)))
    print('OOB: {0:.3f}%'.format(100 * rf.oob_score_))
    print('\nConfusion Matrix:')
    print(rf.confusion_matrix(rf.axes['targets']['test'], pred))
    print('\nFeature Importance:')
    print(rf.feature_importances())

if __name__=='__main__':
    SEED = 1
    raise SystemExit(main())
