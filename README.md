<p align="center">
  <img src="https://i.cubeupload.com/xjoofj.png" width="425" height="200">
</p>

[![travis build](https://img.shields.io/travis/AllstonMickey/Speculator.svg)](://travis-ci.org/AllstonMickey/Speculator)
![python version](https://img.shields.io/pypi/pyversions/Speculator.svg)
[![license](https://img.shields.io/pypi/l/Speculator.svg)](https://github.com/AllstonMickey/Speculator/blob/master/LICENSE)
[![tag](https://img.shields.io/github/tag/allstonmickey/speculator.svg)](https://github.com/AllstonMickey/Speculator/archive/0.1.tar.gz)
![status](https://img.shields.io/pypi/status/Speculator.svg)

Speculator predicts the market trend for cryptocurrencies, including Bitcoin, Ethereum, and many more.

Currently, prices are being taken from Poloniex, a crypto asset exchange.
Therefore, all tickers on Poloniex are able to be used in Speculator.  
Normal markets will also be added in future updates.

## How to get started
``` bash
git clone https://github.com/AllstonMickey/Speculator.git
cd Speculator/speculator
python main.py
```
Yes, it is _that_ easy.

This will display the next predicted market trend of USDT to Bitcoin.

Use the `--help` flag for a complete list of optional arguments.

**Example usage with arguments:**
<p align="center">
  <img src="http://i.cubeupload.com/WMiNJC.png">
</p>

A GUI will be designed to make this more user friendly, for both argument selection and results of the prediction.

### API
Speculator is available on PyPi as of 09/24/17.
```
pip3 install speculator
```

If you want to use or thoroughly understand Speculator's API, I recommend checking out the [examples package](speculator/examples/) and the [docs](docs/)

### Project Structure
`docs/` Documentation overview for packages, modules, and others.

`speculator/`  Project source files.

`speculator/main.py`  Main file to run Speculator with arguments.  Predicts the next trend of a ticker like USDT to BTC.

`speculator/market.py`  Module with market technical analysis features and their setup to a machine learning model.

`speculator/models/` Package of machine learning models.

`speculator/examples/`  Package of python script examples of Speculator's API and their related documentation/walkthrough/how-to. **This is important to understand Speculator's API**

`speculator/features/`  Package of market technical analysis indicators.

`speculator/utils/` Package with modules for basic functions like getting market data from an API or converting dates to epochs.

### Dependencies
Make sure these packages are installed before running Speculator:
* [Delorean](http://delorean.readthedocs.io/en/latest/install.html), `pip3 install delorean`
* [requests](http://docs.python-requests.org/en/latest/user/install/#install) `pip3 install requests`
* [NumPy](https://www.scipy.org/install.html), `pip3 install numpy`
* [scikit-learn](http://scikit-learn.org/stable/install.html), `pip3 install scikit-learn`
* [pandas](https://pandas.pydata.org/pandas-docs/stable/install.html), `pip3 install pandas`

Or just use a one-liner:
``` bash
pip3 install delorean requests numpy scikit-learn pandas
```

## Contact for Feedback, Questions, or Issues
Feel free to send me a message on Reddit at [/u/shneap](https://www.reddit.com/message/compose?to=shneap).  I am happy to hear any concerns, good or bad, in order to progress the development of this project.


### Contributing
Please read the detailed [contributing doc](docs/CONTRIBUTING.md).

## Basis
Part of this project is focused on an implementation of the research paper ["Predicting the direction of stock market prices using random forest"](https://arxiv.org/pdf/1605.00003.pdf), by Luckyson Khaidem, Snehanshu Saha, and Sudeepa Roy Dey.  I hope to gain insights into the accuracy of market technical analysis combined with modern machine learning methods.
This tool should not be used as financial advice, but serve merely as offering a display of technical analysis which may offer another perspective on any investments.
