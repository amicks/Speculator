from speculator.features import rsi, sma, so
from speculator.utils import date, poloniex
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime as dt
import pandas as pd
import numpy as np
np.random.seed(0)
pd.options.display.width=150

"""
def double_chart_duration(url):
    Gets chart data with double the duration

    url: URL to original chart JSON data
        type: string

    return: JSON, URL tuple of a chart
    # Parse URL into a dictionary.  First item is poloniex.com, ignore.
    vals = dict(field.split('=') for field in url.split('&')[1:])
    epoch_diff = int(vals['end']) - int(vals['start'])
    vals['start'] = str(int(vals['start']) - epoch_diff)
    return poloniex.chart_json(**vals)
"""

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

def set_training_targets(data, delta=0):
    for d, features in enumerate(data[:-1]):
        next_features = data[d + 1]
        high_close = next_features['close'] + (delta / 2)
        low_close  = next_features['close'] - (delta / 2)
        if features['close'] < low_close:
            features['target'] = 'rise'
        elif features['close'] > high_close:
            features['target'] = 'fall'
        else:
            features['target'] = 'neutral'
    return data

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
   
vals = load_historical_features('USDT_BTC', 14)
for k, v in enumerate(set_training_targets(vals)):
    print(k, v)
