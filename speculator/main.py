from speculator.features import rsi, so, sma
from speculator.utils import date, poloniex
from datetime import datetime as dt
import argparse

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

def double_chart_duration(url):
    """ 
    Gets chart data with double the duration

    url: URL to original chart JSON data
        type: string

    return: JSON, URL tuple of a chart
    """
    # Parse URL into a dictionary.  First item is poloniex.com, ignore.
    vals = dict(field.split('=') for field in url.split('&')[1:])
    epoch_diff = int(vals['end']) - int(vals['start'])
    vals['start'] = str(int(vals['start']) - epoch_diff)
    return poloniex.chart_json(**vals)

def get_training_data(json, url):
    eval_sma = sma.from_poloniex(json)
    print('Short SMA: {0}'.format(eval_sma))

    # Long term SMA (double the time from previous SMA evaluation)
    eval_sma_2t = sma.from_poloniex(double_chart_duration(url)[0]) 
    print('Long SMA: {0}'.format(eval_sma_2t))

    eval_rsi = rsi.from_poloniex(json)
    print('RSI: {0}'.format(eval_rsi))

    eval_so = so.from_poloniex(json)
    print('SO: {0}'.format(eval_so))

def main():
    args = get_args()

    epochs = date.get_end_start_epochs(args.year, args.month, args.day,
        'last', args.unit, args.count)
    chart = poloniex.chart_json(epochs['shifted'], 
        epochs['initial'], args.period, args.symbol)
    get_training_data(*chart)
    

if __name__=='__main__':
    raise SystemExit(main())
