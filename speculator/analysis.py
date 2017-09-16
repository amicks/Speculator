from speculator.features import rsi, sma, so
from speculator.utils import date, poloniex

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix as conf_mtrx

from datetime import datetime as dt
import pandas as pd
import numpy as np
np.random.seed(0)
pd.options.display.width=150

class Market(object):
    def __init__(self, symbol='USDT_BTC', unit='month', count=6, period=86400,
                 partition=14, delta=25, update=True):

        self.direction = 'last'
        self.symbol = symbol 
        self.update = update

        self.json = self.load_json(unit, count, period)
        self.feature_dataset = self.load_historical_features(partition)
        self.feature_names = [n for n, _ in self.feature_dataset[0].items()]
        self.target_names = {'bearish': -1, 'neutral': 0, 'bullish': 1}
        self.set_training_targets(delta)

    def load_json(self, unit='month', count=6, period=86400):
        """
        Gets chart data from some previous date to the current date
        """
        today = dt.now()
        epochs = date.get_end_start_epochs(today.year, today.month, today.day,
            self.direction, unit, count)
        json, url = poloniex.chart_json(epochs['shifted'],
            epochs['initial'], period, self.symbol)
        if self.update:
            self.json, self.url = json, url
        return json

    def load_historical_features(self, partition=14):
        data = []
        for offset, _ in enumerate(self.json[partition * 2:]):
            short = self.json[partition + offset : (partition * 2) + offset]
            long = self.json[partition : (partition * 2) + offset]
            data.append(feature_data(short, long))
        if self.update:
            self.feature_dataset = data
        return data

    def set_training_targets(self, delta=25):
        for d, features in enumerate(self.feature_dataset[:-1]):
            next_features = self.feature_dataset[d + 1]
            high_close = next_features['close'] + (delta / 2)
            low_close  = next_features['close'] - (delta / 2)

            if features['close'] < low_close:
                features['target'] = self.target_names['bearish']
            elif features['close'] > high_close:
                features['target'] = self.target_names['bullish']
            else:
                features['target'] = self.target_names['neutral']

class RandomForest(Market):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Ignore last entry in dataset, no target to predict
        self.df = pd.DataFrame(self.feature_dataset[:-1])

        # Set axes: features (x) to target market trend (y)
        self.axes = {'features': {'all': self.df.drop('target', axis=1)},
                     'target':  {'all': self.df['target']}}

        # Create training and test samples
        self.load_axis_sets()
        
    def load_axis_sets(self):
        x = self.axes['features']
        y = self.axes['target']
        sets = train_test_split(x['all'], y['all'], random_state=0)
        x['train'], x['test'], y['train'], y['test'] = sets

    def fit_data(self, **kwargs):
        self.classifier = RandomForestClassifier(**kwargs)
        self.classifier.fit(self.axes['features']['train'],
                            self.axes['target']['train'])
        return self.classifier

    def predict_test_set(self):
        self.axes['target']['prediction'] = self.classifier.predict(
                                       self.axes['features']['test'])

    def accuracy(self):
        return accuracy_score(self.axes['target']['test'],
                              self.axes['target']['prediction'])

    def confusion_matrix(self):
        return pd.DataFrame(conf_mtrx(self.axes['target']['test'],
                                      self.axes['target']['prediction']),
                            index=['(A) %s' % k for k in self.target_names.keys()],
                            columns=['(P) %s' % k for k in self.target_names.keys()])

    def feature_importances(self):
        return list(zip(self.feature_names,
                        self.classifier.feature_importances_))

def feature_data(short_json, long_json):
    """
    Gets tech. analysis features from json
    
    short_json: Market data for a shorter period
        type: JSON
    long_json: Market data for a longer period, usually 2X of shorter
               Start date is earlier, but end date is the same
        type: JSON
    
    return: Feature values
        type: Dict of floats
    """
    return {'close'    : short_json[-1]['close'],
            'long_sma' : sma.from_poloniex(long_json),
            'short_sma': sma.from_poloniex(short_json),
            'rsi'      : rsi.from_poloniex(short_json),
            'so'       : so.from_poloniex(short_json)} 

# Set Axes for data, relate x (all data features) to y (target values)
# Get training and test sets for both
# Train Random Forest model to training sets
# Get predictions, test accuracy
# Get confusion matrix
# Get feature importance

rf = RandomForest()
rf.fit_data()
rf.predict_test_set()
print(rf.accuracy())
print(rf.confusion_matrix())
print(rf.feature_importances())
