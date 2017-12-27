<p align="center">
  <img src="https://i.imgur.com/AmrHhZV.png" width="425" height="200">
</p>

<div align="center">

[![travis build](https://img.shields.io/travis/amicks/Speculator.svg)](://travis-ci.org/amicks/Speculator)
![python version](https://img.shields.io/pypi/pyversions/Speculator.svg)
[![license](https://img.shields.io/pypi/l/Speculator.svg)](https://github.com/amicks/Speculator/blob/master/LICENSE)
[![tag](https://img.shields.io/github/tag/amicks/speculator.svg)](https://github.com/amicks/Speculator/archive/0.1.tar.gz)
![status](https://img.shields.io/pypi/status/Speculator.svg)

</div>

<br/>

Speculator is an API for predicting the price trend of cryptocurrencies like Bitcoin and Ethereum.

Normal markets will also be added in future updates.

## Getting Started
Using Python: `python main.py`

Using Public REST API:
``` bash
python api.py
curl http://localhost:5000/api/public/predict
```

For a full list of SQLALCHEMY\_DATABASE\_URI formats, see [SQLAlchemy's docs](http://flask-sqlalchemy.pocoo.org/2.3/config/) under "Connection URI Format".

**Prediction Example:**
<p>
  <img src="https://i.imgur.com/c6JdDWt.png" width="700" height="180">
</p>

Use the `--help` flag for a complete list of optional arguments.
###### Note: A website for a friendly user experience is in development

### Dependencies
Make sure these packages are installed before running Speculator:
``` bash
pip3 install delorean requests numpy tensorflow scikit-learn pandas flask flask-caching flask-restful flask-sqlalchemy psycopg2 webargs
```

### API
#### Web RESTful API
Just start the Flask server then make requests:

``` bash
python api.py
curl http://localhost:5000/api/public/predict -X GET
```

If you want to access the private API, simply make the DB connection an environment variable:
```
export SQLALCHEMY_DATABASE_URI='postgresql://username:password@host:port/db'
```

Private API access with a DB is enabled by default in api/\_\_init\_\_.py
Set `ENABLE_DB = False` to disable this.

##### Resources/Routes

---

**GET: `/api/private/market/?<int:id>`**
Retrieves market data from *required* id

**PUT: `/api/private/market/?<int:id>&<float:low>&<float:high>&<float:close>&<float:volume>`**
Creates market data from *required* id and *optional* keyword arguments of low, high and close prices, and volume.

**POST: `/api/private/market/?<int:id>&<float:low>&<float:high>&<float:close>&<float:volume>`**
Updates market data from *required* id and *optional* keyword arguments of low, high and close prices, and volume.
A value of -1 clears the attribute.

**DELETE: `/api/private/market/?<int:id>`**
Deletes market data from *required* id

---

**GET: `/api/public/predict/?<bool:use_db>&<str:model_type>&<str:symbol>&<str:unit>&<int:count>&<int:period>&<int:partition>&<int:delta>&<int:seed>&<int:trees>&<int:jobs>&<DelimitedList<str>:longs>`**
Gets prediction of the next trend, including probabilities of various outcomes and test set accuracy.

All arguments are optional.

- use_db: Enables the use of DB market data from the private API
  - note: When True, arguments for automatic gathering of data will be disabled (like unit)
  - default: False
- model_type: Machine learning model to train
  - default: 'random_forest'
  - valid values: 'random_forest', 'rf', 'deep_neural_network', or 'dnn'
- symbol: Currency to predict
  - default: 'USDT_BTC'
  - valid values: Symbols/Conversions are available via [Poloniex](https://poloniex.com/exchange)
- unit: Duration to predict from
  - default: 'month'
  - valid values: second, minute, hour, day, week, month, year
- count: `units` to predict from
  - default: 6
- period: Seconds for each chart candlestick
  - default: 86400
  - valid values: 300, 900, 1800, 7200, 14400, 86400
- partition: Market dates for each feature
  - note: A K-day RSI would need a partition of K
  - default: 14
- delta: Size of price neutral zone
  - note: Distinguishes between bearish/neutral/bullish trends
  - default: 25
- seed: Produces consistent results for ML models
  - note: When omitted (seed is None), values are inconsistent and not reproducible
  - default: None
- trees: Trees for the Random Forest model
  - note: Higher values (~65) are typically more accurate
  - default: 10
- jobs: CPU threads to use
  - default: 1
- longs: Uses long duration features
  - note: A K-day RSI would also include a 2K-day RSI (*long RSI*)
  - default: []

---

I plan to start a server for anyone to access this without starting their own Flask server, but with only public access.
Starting this on your own server with authentication for users (private access) will allow you to PUT/POST/DELETE your own market data and analyze that instead of the default.
This is currently in development and will be extended in the future.

#### Python Package
Speculator is available as a package on PyPi.
```
pip3 install speculator
```

If you want to use or thoroughly understand Speculator's API, I recommend checking out the [docs](docs/), which features a fully documented example.

### Project Structure
```
LICENSE
README.md

docs
    \_ CONTRIBUTING.md
    \_ analysis.md
    \_ example.md
    \_ example.py
    \_ utils.md

speculator
    \_ api.py
    \_ main.py
    \_ market.py
    \_ features
                \_ obv.py
                \_ rsi.py
                \_ sma.py
                \_ so.py
    \_ models
             \_ deep_neural_network.py
             \_ random_forest.py
    \_ tests
            \_ integration
                          \_ test_poloniex.py
            \_ unit
                   \_ test_date.py
                   \_ test_poloniex.py
                   \_ test_obv.py
                   \_ test_rsi.py
                   \_ test_sma.py
                   \_ test_so.py
                   \_ test_stats.py
    \_ utils
            \_ date.py
            \_ poloniex.py
            \_ stats.py
```

## Contact for Feedback, Questions, or Issues
Feel free to send me a message on Reddit at [/u/shneap](https://www.reddit.com/message/compose?to=shneap).  I am happy to hear any concerns, good or bad, in order to progress the development of this project.

### Contributing
Please read the detailed [contributing doc](docs/CONTRIBUTING.md).

### Disclaimer
Speculator is not to be used as financial advice or a guide for any financial investments.
