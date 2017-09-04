import requests

def chart_json(start_epoch, end_epoch, period, currency_pair):
    """
    Requests cryptocurrency chart data from Poloniex.com

    start_epoch: Date to start getting market stats from
        type: int
    end_epoch: Date to stop getting market stats from
        type: int
    period: Candlestick period in seconds.
            Valid values: 300, 900, 1800, 7200, 14400, 86400
        type: int
    currency_pair: Currency symbols to compare
        type: string
    
    return: JSON of requested data from Poloniex exchange
        type: JSON (list of dict dates)
    """
    url = 'https://poloniex.com/public?command=returnChartData&' \
          'currencyPair={0}&start={1}&end={2}&period={3}'.format(
           currency_pair, start_epoch, end_epoch, period) 
    json = requests.get(url).json()
    return json

def parse_changes(json):
    """
    json: Poloniex JSON response
        type: JSON (list of dict dates)

    return: Closing price changes
        type: list of floats
    """
    dates = len(json)
    if dates <= 1:
        return None
    changes = []
    for date in range(1, dates): # second, minute, hour, day, week, month, year...
        last_close = json[date - 1]['close']
        now_close  = json[date]['close']
        changes.append(now_close - last_close)
    return changes

def get_gains_losses(changes):
    """
    Categorizes changes into gains/losses

    changes: Closing price changes
        type: list of floats

    return: Gains and losses of changes
        type: Dict of list gains/losses
    """
    res = { 'gains': [], 'losses': [] }
    for change in changes:
        if change > 0:
            res['gains'].append(change)
        else:
            res['losses'].append(change * -1)
    return res

