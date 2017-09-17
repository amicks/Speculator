from datetime import datetime as dt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix as conf_mtrx
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
        TARGET_NAMES: Enum-like object, dict with a key-value 1:1 mapping,
            representing the possible target market trends.
        seed: Int random state seed used to split data sets.
        symbol: String of currency pair, like a ticker symbol.
        update: Bool whether to update attributes upon class function calls.
        json: JSON data as a list of dict dates, where the keys are
            the raw market statistics.
        feature_dataset: Feature data as a list of dict dates, where
            the keys are the evaluated technical analysis indicators.
        feature_names: List of features in feature_dataset.
        df: Pandas DataFrame instance of feature_dataset.  The last value is
            excluded because it is the current date's features, which does
            not have any target.
        axes: A dict of the feature axis (x) target axis (y) datasets.
            Each axis is also a dict, where the keys are the set of data
            (all data, training, test, prediction), and the value of each is
            its corresponding DataFrame. Example:
            {'features':
                {'all': DataFrame},
                {'train': DataFrame},
                {'test': DataFrame},
                {'prediction': DataFrame}
             'target': ...
            }
    """

    TARGET_NAMES = {'bearish': -1, 'neutral': 0, 'bullish': 1}

    def __init__(self, symbol='USDT_BTC', unit='month', count=6, period=86400,
                 partition=14, delta=25, update=True, seed=None):
        """ Inits market class with data going back count units
        
        Args:
            symbol: String of currency pair, like a ticker symbol.
            unit: String of time period unit for count argument.
                How far back to check historical market data.
                valid values: 'hour', 'day', 'week', 'month', 'year'
            count: Int of units.
                How far back to check historical market data.
            period: Int defining width of each chart candlestick in seconds.
            partition: Int of how many dates to take into consideration
                when evaluating technical analysis indicators.
            delta: Positive number defining a price buffer between what is
                classified as a bullish/bearish market for the training set.
                (2 * delta) is equivalent to the size of the neutral market,
                where no trend is seen.
            update: Bool whether to update attributes upon class function calls.
            seed: Int random state seed used to split data sets.
        """

        self.symbol = symbol 
        self.update = update
        self.seed = seed

        # Get market data set
        self.json = self.load_json(unit, count, period)
        self.feature_dataset = self.load_historical_features(partition)
        self.feature_names = [n for n, _ in self.feature_dataset[0].items()]
        self.set_training_targets(delta)

        # Ignore last entry in dataset, no target to predict
        self.df = pd.DataFrame(self.feature_dataset[:-1])

        # Set axes: features (x) to target market trend (y)
        self.axes = {'features': {'all': self.df.drop('target', axis=1)},
                     'target':  {'all': self.df['target']}}

        # Create training and test sets
        self.load_axis_sets(seed=self.seed)


    # Get chart data from some previous date to the current date
    def load_json(self, unit='month', count=6, period=86400):
        """ Gets market chart data from today to a previous date

        Args:
            unit: String of time period unit for count argument.
                How far back to check historical market data.
                valid values: 'hour', 'day', 'week', 'month', 'year'
            count: Int of units.
                How far back to check historical market data.
            period: Int defining width of each chart candlestick in seconds.

        Returns:
            List of dates where each entry is a dict of raw market data.
        """

        today = dt.now()
        DIRECTION = 'last'
        epochs = date.get_end_start_epochs(today.year, today.month, today.day,
            DIRECTION, unit, count)
        json, url = poloniex.chart_json(epochs['shifted'],
            epochs['initial'], period, self.symbol)
        if self.update:
            self.json, self.url = json, url
        return json

    def load_historical_features(self, partition=14):
        """ Parses market data JSON for technical analysis indicators

        Args:
            partition: Int of how many dates to take into consideration
                when evaluating technical analysis indicators.

        Returns:
            List of dicts of features
        """
        data = []
        for offset, _ in enumerate(self.json[partition * 2:]):
            short = self.json[partition + offset : (partition * 2) + offset]
            long = self.json[partition : (partition * 2) + offset]
            data.append(feature_data(short, long))
        if self.update:
            self.feature_dataset = data
        return data

    def set_training_targets(self, delta=25):
        """ Sets target market trend for a date

        Args:
            delta: Positive number defining a price buffer between what is
                classified as a bullish/bearish market for the training set.
                (2 * delta) is equivalent to the size of the neutral market,
                where no trend is seen.
        """

        for d, features in enumerate(self.feature_dataset[:-1]):
            next_features = self.feature_dataset[d + 1]
            high_close = next_features['close'] + (delta / 2)
            low_close  = next_features['close'] - (delta / 2)

            if features['close'] < low_close:
                features['target'] = self.TARGET_NAMES['bearish']
            elif features['close'] > high_close:
                features['target'] = self.TARGET_NAMES['bullish']
            else:
                features['target'] = self.TARGET_NAMES['neutral']
        
    def load_axis_sets(self, seed=None):
        """ Creates training and test sets for x and y axes

        Args:
            seed: Int random state seed used to split data sets.
        """
        
        x = self.axes['features']
        y = self.axes['target']
        sets = train_test_split(x['all'], y['all'], random_state=seed)
        x['train'], x['test'], y['train'], y['test'] = sets


class RandomForest(Market):
    """ Feeds a Market instance to a Random Forest classifier

    Attributes:
        classifier: Sklearn Random Forest Classifier Instance
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fit_data(self, **kwargs):
        """ Fit Random Forest model to training sets """
        self.classifier = RandomForestClassifier(**kwargs)
        self.classifier.fit(self.axes['features']['train'],
                            self.axes['target']['train'])
        return self.classifier

    def predict_test_set(self):
        """ Get prediction of test set from a trained classifier """
        self.axes['target']['prediction'] = self.classifier.predict(
                                                self.axes['features']['test'])

    def accuracy(self):
        """ Return accuracy score of prediction to the test set """
        return accuracy_score(self.axes['target']['test'],
                              self.axes['target']['prediction'])

    def confusion_matrix(self):
        """ Return crosstab DataFrame of test to prediction sets """
        return pd.crosstab(self.axes['target']['test'],
                           self.axes['target']['prediction'],
                           rownames=['(A)'], colnames=['(P)'])

    def feature_importances(self):
        """ Return list of features and their importance in classification """
        return list(zip(self.feature_names,
                        self.classifier.feature_importances_))

def feature_data(short_json, long_json):
    """ Gets technical analysis features from market data JSONs
    
    Args:
        short_json: Market data JSON for a shorter period
        long_json: Market data JSON for a longer period, usually 2X of shorter
    
    Returns:
        Dict of market features and their values
    """
    return {'close'    : short_json[-1]['close'],
            'long_sma' : sma.from_poloniex(long_json),
            'short_sma': sma.from_poloniex(short_json),
            'rsi'      : rsi.from_poloniex(short_json),
            'so'       : so.from_poloniex(short_json)} 

def main():
    rf = RandomForest(seed=0)
    rf.fit_data(random_state=rf.seed)
    rf.predict_test_set()
    print(rf.accuracy())
    print(rf.confusion_matrix())
    print(rf.feature_importances())

if __name__=='__main__':
    pd.options.display.width=150
    main()
