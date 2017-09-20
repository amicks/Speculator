Speculator [![travis build](https://img.shields.io/travis/AllstonMickey/Speculator.svg)](://travis-ci.org/AllstonMickey/Speculator)
==========
<p align="center">
  <img src="https://i.cubeupload.com/eAerFa.png">
</p>

Speculator predicts the market trend for cryptocurrencies, including Bitcoin, Ethereum, and many more.

Currently, prices are being taken from Poloniex, a crypto asset exchange.
Therefore, all tickers on Poloniex are able to be used in Speculator.  
Normal markets will also be added in future updates.

## How to get started
```
git clone https://github.com/AllstonMickey/Speculator.git
cd Speculator/speculator
python main.py
```
Yes, it is _that_ easy.

This will display the next predicted market trend of USDT to Bitcoin.

Use the `--help` flag for a complete list of optional arguments.

**Example usage with arguments:**
<p align="center">
  <img src="https://i.cubeupload.com/c1Plfp.png">
</p>

A GUI will be designed to make this more user friendly, for both argument selection and results of the prediction.


### Project Structure
_docs/_  Documentation overview for packages, modules, and others.
_speculator/_  Project source files.
_speculator/main.py_  Main file to run Speculator with arguments.  Predicts the next trend of a ticker like USDT to BTC.
_speculator/analysis.py_  Module with market technical analysis features and their application to a machine learning model.
_speculator/features/_  Package of market technical analysis features
_speculator/utils/_ Package with modules for basic functions like getting market data from an API or converting dates to epochs.

### Dependencies
Make sure these packages are installed before running Speculator:
* [Delorean](http://delorean.readthedocs.io/en/latest/install.html), ` pip install delorean `
* [scikit-learn](http://scikit-learn.org/stable/install.html), ` pip install scikit-learn `
* [pandas](https://pandas.pydata.org/pandas-docs/stable/install.html), ` pip install pandas `

## Contact for Feedback, Questions, or Issues
Feel free to send me a message on Reddit at [/u/shneap](https://www.reddit.com/message/compose?to=shneap).  I am happy to hear any concerns, good or bad, in order to progress the development of this project.


### Contributing
Please read the detailed [contributing doc](docs/CONTRIBUTING.md).

## Basis
Part of this project is focused on an implementation of the research paper ["Predicting the direction of stock market prices using random forest"](https://arxiv.org/pdf/1605.00003.pdf), by Luckyson Khaidem, Snehanshu Saha, and Sudeepa Roy Dey.  I hope to gain insights into the accuracy of market technical analysis combined with modern machine learning methods.
This tool should not be used as financial advice, but serve merely as offering a display of technical analysis which may offer another perspective on any investments.
