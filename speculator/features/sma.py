from speculator.utils import date, poloniex, stats

"""
Simple Moving Average:
Average closing price over a period
SMA = avg(closes) = sum(closes) / len(closes)
"""

def eval_algorithm(closes):
    return stats.avg(closes)

def get_poloniex(year, month, day, unit, count, period, currency_pair):
    epochs = date.get_end_start_epochs(year, month, day, 'last', unit, count)
    json = poloniex.chart_json(epochs['shifted'], 
        epochs['initial'], period, currency_pair)[0]
    return from_poloniex(json)

def from_poloniex(json):
    closes = [date['close'] for date in json]
    return eval_algorithm(closes)
