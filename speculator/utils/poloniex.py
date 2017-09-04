import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.debug(' HTTP Request URL:\n{0}'.format(url))
    json = requests.get(url).json()
    logger.debug(' JSON:\n{0}'.format(json))
    return json

def parse_changes(json):
    """
    json: Poloniex JSON response
        type: JSON (list of dict dates)

    return: Closing price changes
        type: list of floats
    """
    if 'error' in json:
        logger.error(' Invalid parameters in URL for HTTP response')
        raise SystemExit
    elif all(val == 0 for val in json[0]):
        logger.error(' Bad HTTP response.  Time unit too short?')
        raise SystemExit

    dates = len(json)
    if dates <= 1: # time to short
        logger.error(' Not enough dates to calculate changes')
        raise SystemExit
    
    changes = []
    for date in range(1, dates): # second, minute, hour, day, week, month, year...
        last_close = json[date - 1]['close']
        now_close  = json[date]['close']
        changes.append(now_close - last_close)
    logger.debug('Market Changes (from JSON):\n{0}'.format(changes))
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
    logger.debug(' Gains:\n{0}\nLosses:\n{1}'.format(res['gains'], res['losses']))
    return res

