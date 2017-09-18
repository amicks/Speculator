from datetime import datetime as dt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from speculator.features import rsi
from speculator.features import sma
from speculator.features import so
from speculator.utils import date
from speculator.utils import poloniex


class Market(object):
    """ Evaluates TA indicators of a market
    
    Gets data from a market and then calculates technical analysis features.
    It also prepares this data to be fed into machine learning interfaces
    by creating a pandas DataFrame, and generating training/test sets
    for features (x-axis) and the target market trend (y-axis).

    Attributes:
        symbol: String of currency pair, like a ticker symbol.
        unit: String of time period unit for count argument.
            How far back to check historical market data.
            valid values: 'hour', 'day', 'week', 'month', 'year'
        count: Int of units.
            How far back to check historical market data.
        period: Int defining width of each chart candlestick in seconds.
            Valid values: 300, 900, 1800, 7200, 14400, 86400.
        json: JSON data as a list of dict dates, where the keys are
            the raw market statistics.
    """

    def __init__(self, symbol, unit='month', count=6, period=86400):
        """ Inits market class with data going back count units
        
        Args:
            symbol: String of currency pair, like a ticker symbol.
            unit: String of time period unit for count argument.
                How far back to check historical market data.
                valid values: 'hour', 'day', 'week', 'month', 'year'
            count: Int of units.
                How far back to check historical market data.
            period: Int defining width of each chart candlestick in seconds.
                Valid values: 300, 900, 1800, 7200, 14400, 86400.
        """
        self.symbol = symbol 
        self.unit = unit
        self.count = count
        self.period = period
        self.load_json()

    def load_json(self):
        """ Gets market chart data from today to a previous date """
        today = dt.now()
        DIRECTION = 'last'
        epochs = date.get_end_start_epochs(today.year, today.month, today.day,
                                           DIRECTION, self.unit, self.count)
        self.json = poloniex.chart_json(epochs['shifted'], epochs['initial'],
                                        self.period, self.symbol)[0]

    def dataframe(self, partition):
        """ Parses market data JSON for technical analysis indicators

        Args:
            partition: Int of how many dates to take into consideration
                when evaluating technical analysis indicators.

        Returns:
            Pandas DataFrame instance with columns as features.
        """
        data = []
        for offset in range(len(self.json) - partition):
            json = self.json[offset : offset + partition]
            data.append(get_features(json))
        return pd.DataFrame(data)


class RandomForest(RandomForestClassifier):
    """ Random Forest Classifier using a DataFrame from a Market instance

    Attributes:
        market: DataFrame instance from Market instance (Market().dataframe())
        axes: A dict of the feature axis (x) target axis (y) datasets.
            Each axis is also a dict, where the keys are the set of data
            (all data, training, test, prediction), and the value of each is
            its corresponding DataFrame. Example:
            {'features':
                {'train': DataFrame},
                {'test': DataFrame},
             'target':
                {'train': DataFrame},
                {'test': DataFrame},
            }
            This is only available after splitting the DataFrame into
            training and test sets.
    
    All other attributes and functions are defined
    within sklearn's RandomForestClassifier class.
    """

    def __init__(self, market, **kwargs):
        """ Inits a Random Forest Classifier with a market attribute

        Args:
            market: Pandas DataFrame with columns as market features,
                and rows as dates or entries.  The first row is the
                earliest date and the last row is closer to the present.
        """
        super().__init__(**kwargs)
        self.market = market

    def set_training_targets(self, delta):
        """ Sets target market trend for a date

        Args:
            delta: Positive number defining a price buffer between what is
                classified as a bullish/bearish market for the training set.
                (2 * delta) is equivalent to the size of the neutral market,
                where no trend is seen.
        """
        TARGET_NAMES = {'bearish': -1, 'neutral': 0, 'bullish': 1}
        targets = [] # Keep track of targets
        for row, _ in self.market.iterrows():
            if row == self.market.shape[0] - 1: # Can't predict yet, done.
                break

            # Get closing prices
            curr_close = self.market.close[row]
            next_close = self.market.close[row + 1]
            high_close = next_close + (delta / 2) # Pos. neutral zone threshold
            low_close = next_close - (delta / 2)  # Neg. neutral zone threshold

            # Get target
            if curr_close < low_close:
                target = TARGET_NAMES['bearish']
            elif curr_close > high_close:
                target = TARGET_NAMES['bullish']
            else:
                target = TARGET_NAMES['neutral']
            targets.append(target)

        # Convert targets to DF and merge with the self.market DF
        df = pd.DataFrame(targets, columns=['target']) 
        self.market = pd.concat([self.market, df], axis=1)

    def split_sets(self, random_state=None):
        """ Creates training and test sets for x and y axes

        Args:
            random_state: Int seed used to split data sets.
        """
        # Get features and targets into two separate DataFrames
        # Ignore the last row because it cannot be predicted without training
        features = self.market.drop('target', axis=1)[:-1]
        targets = self.market.target[:-1]

        # Create axes of training and test sets
        sets = train_test_split(features, targets, random_state=random_state)
        self.axes = {'features': {}, 'targets': {}} # Initialize dicts
        (self.axes['features']['train'], self.axes['features']['test'],
         self.axes['targets']['train'], self.axes['targets']['test']) = sets

    def train(self):
        """ Fit Random Forest model to training sets """
        self.fit(self.axes['features']['train'], self.axes['targets']['train'])

    def confusion_matrix(self, test, prediction):
        """ Return crosstab DataFrame of test to prediction sets """
        return pd.crosstab(test, prediction, rownames=['(A)'], colnames=['(P)'])

    def feature_importances(self):
        """ Return list of features and their importance in classification """
        feature_names = [name for name in self.market]
        return list(zip(feature_names, self.feature_importances_))

def get_features(json):
    """ Gets technical analysis features from market data JSONs
    
    Args:
        json: JSON data as a list of dict dates, where the keys are
            the raw market statistics.
    
    Returns:
        Dict of market features and their values
    """
    return {'close'    : json[-1]['close'],
            'sma'      : sma.from_poloniex(json),
            'rsi'      : rsi.from_poloniex(json),
            'so'       : so.from_poloniex(json)} 

def main():
    m = Market('USDT_BTC')

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
    rf = RandomForest(df, random_state=SEED, oob_score=True)
    rf.set_training_targets(25)
    rf.split_sets(random_state=SEED)
    rf.train()
    
    # Get the predictions and accuracies
    pred = rf.predict(rf.axes['features']['test'])
    print('Accuracy Score: {0:.3f}%'.format(
           100 * accuracy_score(rf.axes['targets']['test'], pred)))
    print('OOB: {0:.3f}%'.format(100 * rf.oob_score_))
    print('\nConfusion Matrix:')
    print(pd.crosstab(rf.axes['targets']['test'], pred,
                      rownames=['(A)'], colnames=['(P)']))
    print('\nFeature Importance:')
    print(rf.feature_importances())

if __name__=='__main__':
    SEED = 1
    pd.options.display.width=150
    raise SYstemExit(main())
