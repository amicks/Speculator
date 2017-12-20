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

If you want to access the private API, simply make the DB connection an environment variable:
```
export SQLALCHEMY_DATABASE_URI='postgresql://username:password@host:port/db'
```

For a full list of SQLALCHEMY_DATABASE_URI formats, see [SQLAlchemy's docs](http://flask-sqlalchemy.pocoo.org/2.3/config/) under "Connection URI Format".

**Prediction Example:**
<p>
  <img src="https://i.imgur.com/c6JdDWt.png" width="700" height="180">
</p>

Use the `--help` flag for a complete list of optional arguments.
###### Note: A website for a friendly user experience is in development

### Dependencies
Make sure these packages are installed before running Speculator:
``` bash
pip3 install delorean requests numpy tensorflow scikit-learn pandas flask flask-cache flask-restful flask-sqlalchemy psycopg2 webargs
```

### API
#### Web RESTful API
Just start the Flask server then make requests:

``` bash
python api.py
curl http://localhost:5000/api/public/predict -X GET
```

For a list of valid arguments in the URL, please check back tomorrow (12/20/17).

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
