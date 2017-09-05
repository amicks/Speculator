# Speculator [![travis build](https://img.shields.io/travis/AllstonMickey/Speculator.svg?style=flat-square)](://travis-ci.org/AllstonMickey/Speculator)
This project aims to predict future stock prices using popular algorithms from machine learning and finance.

Currently, prices are being taken from Poloniex, a Bitcoin/cryptocurrency asset exchange.  Normal markets will also be added in future updates.

### Basis
Part of this project is focused on an implementation of the research paper ["Predicting the direction of stock market prices using random forest"](https://arxiv.org/pdf/1605.00003.pdf), by Luckyson Khaidem, Snehanshu Saha, and Sudeepa Roy Dey.  I hope to gain insights into the accuracy of market technical analysis combined with modern machine learning methods.
This tool should not be used as financial advice, but serve merely as offering a display of technical analysis which may offer another perspective on any investments.

### Getting Started
The project is not ready for use at this time.  Still in development.
However, feel free to commit and contribute to the development.
A style guide is not yet written, but in the meantime, you can get a gyst of the style through the existing codebase.

### Testing
Please read the [testing doc](docs/testing.md).

### Roadmap
#### September, 2017
Date | Task
---  | ---
_5th_ | Williams %R algorithm
_6th_ | Williams %R implementation
_8th_ |  Moving Average Convergence Divergence (MACD) algorithm
_10th_ | Moving Average Convergence Divergence (MACD) implementation
_12th_ | Price Rate of Change (PROC) algorithm
_15th_ | Price Rate of Change (PROC) implementation
_17th_ | On Balance Volume (OBV) algorithm
_20th_ | On Balance Volume (OBV) implementation
#### October, 2017
Date | Task
---  | ---
_1st_ | Random Forest implementation
_15th_ | GUI
_20th_ | Project release 1.0
_28th_ | Add implementation for other exchanges (traditional & cryptos)

#### Misc. Todo
* Update docs when each task on the roadmap is completed, do NOT wait until the project is over!
* Integration/Unit test each functionality before pushing/merging code to master
* Implement other machine learning algorithms with the same dataset, compare results
