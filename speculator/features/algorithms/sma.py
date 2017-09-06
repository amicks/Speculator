import speculator.utils as utils

"""
Simple Moving Average:
Average closing price over a period
SMA = avg(closes) = sum(closes) / len(closes)
"""

def eval_algorithm(closes):
    return utils.stats.avg(closes)

def get_poloniex(year, month, day, unit, count, period, currency_pair):
    epochs = utils.date.get_end_start_epochs(year, month, day, 'last', unit, count)
    json = utils.poloniex.chart_json(epochs['shifted'], 
                               epochs['initial'], period, currency_pair)
    closes = [date['close'] for date in json]
    return eval_algorithm(closes)

