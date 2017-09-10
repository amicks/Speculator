from speculator.features import rsi, so, sma
from speculator.utils import date, poloniex
from datetime import datetime as dt
import argparse

from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

def get_args():
    today = dt.now()
    parser = argparse.ArgumentParser(
        description='Get market statistics from Poloniex.com')
    parser.add_argument('-y', '--year', default=today.year, type=int, help='Initial year')
    parser.add_argument('-m', '--month', default=today.month, type=int, help='Initial month')
    parser.add_argument('-d', '--day', default=today.day, type=int, help='Initial day')
    parser.add_argument('-u', '--unit', default='day',
        help='second, minute, hour, day, week, month, year')
    parser.add_argument('-c', '--count', default=14, type=int,
        help='Number of "units" to go back (behind the set date/now)')
    parser.add_argument('-p', '--period', default=86400, type=int,
        help='Number of seconds for each candlestick: ' \
        '300, 900, 1800, 7200, 14400, 86400 only valid')
    parser.add_argument('-s', '--symbol', default='USDT_BTC',
        help='Currency pairs, ex: USDT_BTC')
    return parser.parse_args()

def main():
    args = get_args()

    epochs = date.get_end_start_epochs(args.year, args.month, args.day,
        'last', args.unit, args.count)
    chart = poloniex.chart_json(epochs['shifted'], 
        epochs['initial'], args.period, args.symbol)
    json, url = chart[0], chart[1]

    print('Relative Strength Index:')
    print(rsi.from_poloniex(json))

    print('Stochastic Oscillator:')
    print(so.from_poloniex(json))

    print('Simple Moving Average:')
    print(sma.from_poloniex(json))

    

if __name__=='__main__':
    raise SystemExit(main())
