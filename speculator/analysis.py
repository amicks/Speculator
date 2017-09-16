from speculator.features import rsi, sma, so
from speculator.utils import date, poloniex

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

from datetime import datetime as dt
import pandas as pd
import numpy as np
np.random.seed(0)
pd.options.display.width=150

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

def load_json(symbol):
    """
    Gets features data from today to 6 months ago
    """
    today = dt.now()
    DIRECTION = 'last'
    UNIT = 'month'
    COUNT = 6
    PERIOD = 86400 # seconds in 1 day
    epochs = date.get_end_start_epochs(today.year, today.month, today.day,
        'last', 'month', 6)
    return poloniex.chart_json(epochs['shifted'],
        epochs['initial'], PERIOD, symbol)

def load_historical_features(symbol, shift):
    # Split given 6 month JSON into 14 day shifts
    # Get features for each period
    data = []
    json = load_json(symbol)[0]
    for k, v in enumerate(json[shift * 2:]):
        short = json[shift + k : (shift * 2) + k]
        long = json[k : (shift * 2) + k]
        data.append(feature_data(short, long))
    return data

def set_training_targets(data, delta=0):
    for d, features in enumerate(data[:-1]):
        next_features = data[d + 1]
        high_close = next_features['close'] + (delta / 2)
        low_close  = next_features['close'] - (delta / 2)
        if features['close'] < low_close:
            features['target'] = 1
            #features['target'] = 'rise'
        elif features['close'] > high_close:
            features['target'] = -1
            #features['target'] = 'fall'
        else:
            features['target'] = 0
            #features['target'] = 'neutral'

dataset = load_historical_features('USDT_BTC', 14)
set_training_targets(dataset, delta=50)

df = pd.DataFrame(dataset[:-1]) # Ignore last day, no target to predict
features = [f for f in df.columns if f is not 'target'] # Get features being used

# Set Axes for data, relate x (all data features) to y (target values)
# Get training and test sets for both
x = df.drop('target', axis=1).drop('close', axis=1) # Dataset with unknown target
y = df['target'] # Target values
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)

# Train Random Forest model to training sets
rfc = RandomForestClassifier(n_jobs=2, random_state=0)
rfc.fit(x_train, y_train)

# Get predictions, test accuracy
y_pred = rfc.predict(x_test)
print(accuracy_score(y_test, y_pred))

# Get confusion matrix
print(pd.DataFrame(confusion_matrix(y_test, y_pred),
                   index=['Actual Fall', 'Actual Neutral', 'Actual Rise'],
                   columns=['Pred. Fall', 'Pred. Neutral', 'Pred. Rise']))

# Get feature importance
print(list(zip(features, rfc.feature_importances_)))

