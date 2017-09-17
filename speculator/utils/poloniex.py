import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def json_to_url(json, currencyPair):
    start = json[0]['date']
    end = json[-1]['date']
    diff = end - start

    # Get period by a ratio from calculated period to valid periods
    # Ratio closest to 1 is the period
    # Valid values: 300, 900, 1800, 7200, 14400, 86400
    periods = [300, 900, 1800, 7200, 14400, 86400]
    diffs = { p: abs(1 - (p / (diff / len(json)))) for p in periods }
    period = min(diffs, key=diffs.get)
    
    url = 'https://poloniex.com/public?command=returnChartData&' \
          'currencyPair={0}&start={1}&end={2}&period={3}'.format(
           currencyPair, start, end, period) 
    return url

def chart_json(start, end, period, currencyPair):
    """
    Requests cryptocurrency chart data from Poloniex.com

    start_epoch: Date to start getting market stats from
        * FURTHER from current date
        type: int
    end_epoch: Date to stop getting market stats from
        * CLOSER to current date
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
           currencyPair, start, end, period) 
    logger.debug(' HTTP Request URL:\n{0}'.format(url))
    json = requests.get(url).json()
    logger.debug(' JSON:\n{0}'.format(json))

    if 'error' in json:
        logger.error(' Invalid parameters in URL for HTTP response')
        raise SystemExit
    elif all(val == 0 for val in json[0]):
        logger.error(' Bad HTTP response.  Time unit too short?')
        raise SystemExit
    elif len(json) < 1: # time to short
        logger.error(' Not enough dates to calculate changes')
        raise SystemExit

    return json, url

def parse_changes(json):
    """
    json: Poloniex JSON response
        type: JSON (list of dict dates)

    return: Closing price changes
        type: list of floats
    """
    changes = []
    dates = len(json)
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

def get_attribute(json, attr):
    """
    json: Poloniex JSON response
        type: JSON (list of dict dates)
    attr: Attribute in JSON file to collect

    return: Closing price changes
        type: list of floats
    """
    res = []
    dates = len(json)
    for date in range(dates): # second, minute, hour, day, week, month, year...
        res.append(json[date][attr])
    logger.debug('{0}s (from JSON):\n{1}'.format(attr, res))
    return res

