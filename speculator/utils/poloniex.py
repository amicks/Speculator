import logging
import requests
from speculator.utils import date

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def json_to_url(json, symbol):
    """ Converts a JSON to a URL by the Poloniex API 

    Args:
        json: JSON data as a list of dict dates, where the keys are
            the raw market statistics.
        symbol: String of currency pair, like a ticker symbol.

    Returns:
        String URL to Poloniex API representing the given JSON.
    """
    start = json[0]['date']
    end = json[-1]['date']
    diff = end - start

    # Get period by a ratio from calculated period to valid periods
    # Ratio closest to 1 is the period
    # Valid values: 300, 900, 1800, 7200, 14400, 86400
    periods = [300, 900, 1800, 7200, 14400, 86400]

    diffs = {}
    for p in periods:
        diffs[p] = abs(1 - (p / (diff / len(json)))) # Get ratio

    period = min(diffs, key=diffs.get) # Find closest period
    
    url = ('https://poloniex.com/public?command'
           '=returnChartData&currencyPair={0}&start={1}'
           '&end={2}&period={3}').format(symbol, start, end, period) 
    return url

def chart_json(start, end, period, symbol):
    """ Requests chart data from Poloniex API
    
    Args:
        start: Int epoch date to START getting market stats from.
            Note that this epoch is FURTHER from the current date.
        end: Int epoch date to STOP getting market stats from.
            Note that this epoch is CLOSER to the current date.
        period: Int defining width of each chart candlestick in seconds.
            Valid values: 300, 900, 1800, 7200, 14400, 86400
        symbol: String of currency pair, like a ticker symbol.

    Returns:
        Tuple of (JSON data, URL to JSON).
        JSON data as a list of dict dates, where the keys are
        the raw market statistics.
        String URL to Poloniex API representing the given JSON.
    """
    url = ('https://poloniex.com/public?command'
           '=returnChartData&currencyPair={0}&start={1}'
           '&end={2}&period={3}').format(symbol, start, end, period) 
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
    """ Gets price changes from JSON

    Args:
        json: JSON data as a list of dict dates, where the keys are
            the raw market statistics.

    Returns:
        List of floats of price changes between entries in JSON.
    """
    changes = []
    dates = len(json)
    for date in range(1, dates): 
        last_close = json[date - 1]['close']
        now_close  = json[date]['close']
        changes.append(now_close - last_close)
    logger.debug('Market Changes (from JSON):\n{0}'.format(changes))
    return changes

def get_gains_losses(changes):
    """ Categorizes changes into gains and losses

    Args:
        changes: List of floats of price changes between entries in JSON.

    Returns:
        Dict of changes with keys 'gains' and 'losses'.
        All values are positive.
    """
    res = {'gains': [], 'losses': []}
    for change in changes:
        if change > 0:
            res['gains'].append(change)
        else:
            res['losses'].append(change * -1)
    logger.debug('Gains: {0}'.format(res['gains']))
    logger.debug('Losses: {0}'.format(res['losses']))
    return res

def get_attribute(json, attr):
    """ Gets the values of an attribute from JSON

    Args:
        json: JSON data as a list of dict dates, where the keys are
            the raw market statistics.
        attr: String of attribute in JSON file to collect.

    Returns:
        List of values of specified attribute from JSON
    """
    res = [json[entry][attr] for entry, _ in enumerate(json)]
    logger.debug('{0}s (from JSON):\n{1}'.format(attr, res))
    return res

def get_json_shift(year, month, day, unit, count, period, symbol):
    """ Gets JSON from Poloniex.com exchange

    Args:
        year: Int between 1 and 9999.
        month: Int between 1 and 12.
        day: Int between 1 and 31.
        unit: String of time period unit for count argument.
            How far back to check historical market data.
            Valid values: 'hour', 'day', 'week', 'month', 'year'
        count: Int of units.
            How far back to check historical market data.
        period: Int defining width of each chart candlestick in seconds.
        symbol: String of currency pair, like a ticker symbol.

    Returns: JSON, list of dates where each entry is a dict of raw market data.
    """
    epochs = date.get_end_start_epochs(year, month, day, 'last', unit, count)
    return chart_json(epochs['shifted'], epochs['initial'],
                      period, symbol)[0]

