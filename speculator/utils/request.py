import requests
from speculator.utils import date

def poloniex_chart_json(currency_pair='USDT_BTC',
                        start_epoch=date.shift_epoch(
                                date.now_delorean(),
                                'last', 'day', 14),
                        end_epoch=int(date.now_delorean().epoch), 
                        period=86400):
    """
    Requests cryptocurrency chart data from Poloniex.com
    """
    url = 'https://poloniex.com/public?command=returnChartData&' \
          'currencyPair={0}&start={1}&end={2}&period={3}'.format(
           currency_pair, start_epoch, end_epoch, period) 
    print(url)
    json = requests.get(url).json()
    print json
             
poloniex_chart_json()
