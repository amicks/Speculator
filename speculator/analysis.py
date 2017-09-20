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

#Enum-like object with 1:1 mapping.  Converts a readable
# market trend like 'bearish' to an int that is easier to parse.
TARGET_CODES = {'bearish': -1, 'neutral': 0, 'bullish': 1}

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
            **kwargs: Arguments for scikit-learn's RandomForestClassifier
        """
        super().__init__(**kwargs)
        self.market = market

    def set_training_targets(self, delta):
        """ Sets target market trend for a date

        Args:
            delta: Positive number defining a price buffer between what is
                classified as a bullish/bearish market for the training set.
                delta is equivalent to the total size of the neutral price zone.
                delta / 2 is equivalent to either the positive or negative
                threshold of the neutral price zone.
        """
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
                target = TARGET_CODES['bearish']
            elif curr_close > high_close:
                target = TARGET_CODES['bullish']
            else:
                target = TARGET_CODES['neutral']
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
        
    def predict_next_trend(self, proba=False, log=False):
        """ Predicts the next market trend

        *** RandomForest must be trained! ***

        Returns:
            List of predicted classes.
            Index 0: Trend
            Index 1: Probability
            Index 2: Log Probability
        """
        # The date to predict is the last row in the dataframe
        # Target was set to None when we trained the model, so drop it.
        today = self.market.tail(1).drop('target', axis=1)

        preds = [self.predict(today)[0]]
        if proba:
            preds.append(self.predict_proba(today))
        if log:
            preds.append(self.predict_log_proba(today))
        return preds


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

def setup_model(market, partition, delta, use_long, **kwargs):
    """ Converts a market to a trained Random Forest

    Args:
        market: Market instance to feed to Random Forest
        partition: Int of how many dates to take into consideration
            when evaluating technical analysis indicators.
        delta: Positive number defining a price buffer between what is
            classified as a bullish/bearish market for the training set.
            delta is equivalent to the total size of the neutral price zone.
            delta / 2 is equivalent to either the positive or negative
            threshold of the neutral price zone.
        use_long: Bool, includes features from a longer partition in
            addition to the normal partition size.  Example:
            A 14 day SMA would also include a 28 day SMA if use_long is True.
        **kwargs: Arguments for scikit-learn's RandomForestClassifier
    """
    df = market.dataframe(partition)

    if use_long:
        # Create longer dataframe, update column names to avoid conflicts
        df_long = market.dataframe(partition * 2)
        df_long.columns = ['long_{0}'.format(c) for c in df_long.columns]

        # Merge the two DataFrames
        skip = partition
        df = pd.concat([df[skip:].reset_index(drop=True), df_long], axis=1)
    
    # Feed the DataFrame to a Random Forest Classifier
    rf = RandomForest(df, **kwargs)
    rf.set_training_targets(delta)
    rf.split_sets(random_state=SEED)
    rf.train()
    return rf

def target_code_to_name(code):
    """ Converts an int target code to a target name
    
    Since self.TARGET_CODES is a 1:1 mapping, perform a reverse lookup
    to get the more readable name.

    Args:
        code: Value from self.TARGET_CODES

    Returns:
        String target name corresponding to the given code.
    """
    TARGET_NAMES = {v: k for k, v in TARGET_CODES.items()}
    return TARGET_NAMES[code]

def main():
    m = Market(SYMBOL)
    rf = setup_model(m, PARTITION, DELTA, USE_LONG,
                     random_state=SEED, oob_score=False)
    
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
    print(TARGET_CODES)
    print('\nFeature Importance:')
    print(rf.feature_importances())

    print()
    print('###################')
    print('# PREDICTED TREND #')
    print('###################')
    pred_today = rf.predict_next_trend(proba=True, log=True)
    print('Trend: {0}'.format(target_code_to_name(pred_today[0])))
    print('Probabilities: {0}'.format(pred_today[1]))
    print('Log Probabilities: {0}'.format(pred_today[2]))

if __name__=='__main__':
    PARTITION = 14
    DELTA = 25
    USE_LONG = True
    SYMBOL = 'USDT_BTC'
    SEED = 2
    pd.options.display.width=150
    raise SystemExit(main())
