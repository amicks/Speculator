Speculator [![travis build](https://img.shields.io/travis/AllstonMickey/Speculator.svg)](://travis-ci.org/AllstonMickey/Speculator)
==========
<p align="center">
  <img src="https://i.cubeupload.com/sfy2x2.png">
</p>

Speculator predicts the next 'closing' price for cryptocurrencies, including Bitcoin, Ethereum, and many more.

Currently, prices are being taken from Poloniex, a crypto asset exchange.
Therefore, all tickers on Poloniex are able to be used in Speculator.  
Normal markets will also be added in future updates.

## Getting Started
```
python main.py
```
*Yes, it is _that_ easy!*

This will display the next predicted closing price of a ticker.
*default:* USDT to Bitcoin

Use the `--help` flag for a complete list of optional arguments.

### Dependencies
* [Delorean](http://delorean.readthedocs.io/en/latest/install.html), ` pip install delorean `
* [scikit-learn](http://scikit-learn.org/stable/install.html), ` pip install scikit-learn `
* [pandas](https://pandas.pydata.org/pandas-docs/stable/install.html), ` pip install pandas `

### Contributing
Please read the detailed [contributing doc](docs/CONTRIBUTING.md).

## Basis
Part of this project is focused on an implementation of the research paper ["Predicting the direction of stock market prices using random forest"](https://arxiv.org/pdf/1605.00003.pdf), by Luckyson Khaidem, Snehanshu Saha, and Sudeepa Roy Dey.  I hope to gain insights into the accuracy of market technical analysis combined with modern machine learning methods.
This tool should not be used as financial advice, but serve merely as offering a display of technical analysis which may offer another perspective on any investments.
