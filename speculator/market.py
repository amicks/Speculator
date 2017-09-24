from collections import namedtuple
from datetime import datetime as dt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from speculator.features import rsi
from speculator.features import sma
from speculator.features import so
import speculator.models.random_forest as rf
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

    def __init__(self, symbol='USDT_BTC', unit='month', count=6, period=86400):
        """ Inits market class of symbol with data going back count units """
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

    def features(self, partition=1):
        """ Parses market data JSON for technical analysis indicators

        Args:
            partition: Int of how many dates to take into consideration
                when evaluating technical analysis indicators.

        Returns:
            Pandas DataFrame instance with columns as numpy.float32 features.
        """
        data = []
        for offset in range(len(self.json) - partition):
            json = self.json[offset : offset + partition]
            data.append(eval_features(json))
        return pd.DataFrame(data=data, dtype=np.float32)

def targets(x, delta=10):
    """ Sets target market trend for a date

    Args:
        x: Pandas DataFrame of market features
        delta: Positive number defining a price buffer between what is
            classified as a bullish/bearish market for the training set.
            delta is equivalent to the total size of the neutral price zone.
            delta / 2 is equivalent to either the positive or negative
            threshold of the neutral price zone.

    Returns:
        Pandas Series of numpy int8 market trend targets
    """
    data = [] # Keep track of targets
    for row, _ in x.iterrows():
        if row == x.shape[0] - 1: # Can't predict yet, done.
            break

        # Get closing prices
        curr_close = x.close[row]
        next_close = x.close[row + 1]
        high_close = next_close + (delta / 2) # Pos. neutral zone threshold
        low_close = next_close - (delta / 2)  # Neg. neutral zone threshold

        # Get target
        if curr_close < low_close:
            target = TARGET_CODES['bearish']
        elif curr_close > high_close:
            target = TARGET_CODES['bullish']
        else:
            target = TARGET_CODES['neutral']
        data.append(target)

    return pd.Series(data=data, dtype=np.int8, name='target')

def eval_features(json):
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

def setup_model(x, y, model_type='random_forest', seed=None, **kwargs):
    """ Initializes a machine learning model

    Args:
        x: Pandas DataFrame, X axis of features
        y: Pandas Series, Y axis of targets
        model_type: Machine Learning model to use
            Valid values: 'random_forest'
        seed: Random state to use when splitting sets and creating the model
        **kwargs: Scikit Learn's RandomForestClassifier kwargs
    
    Returns:
        Trained model instance of model_type
    """
    sets = namedtuple('Datasets', ['train', 'test'])
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=seed)
    x = sets(x_train, x_test)
    y = sets(y_train, y_test)

    if model_type == 'random_forest':
        model = rf.RandomForest(x, y, random_state=seed, **kwargs)
    else:
        raise ValueError('Invalid model type kwarg')
    return model

