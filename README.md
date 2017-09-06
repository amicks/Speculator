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
Date | Task | Status 
---  | ---  | ---
09.03.17 | Relative Strength Index (RSI) & Stochastic Oscillator (SO) algorithms | Done
09.04.17 | RSI and SO implementations with Poloniex | Done
09.05.17 | Simple Moving Average (SMA) algorithm & implementation | Done
09.06.17 | Exponential Moving Average (EMA) algorithm & implementation |
09.08.17 | Moving Average Convergence Divergence (MACD) algorithm | 
09.10.17 | Moving Average Convergence Divergence (MACD) implementation | 
09.12.17 | Price Rate of Change (PROC) algorithm | 
09.15.17 | Price Rate of Change (PROC) implementation | 
09.17.17 | On Balance Volume (OBV) algorithm | 
09.20.17 | On Balance Volume (OBV) implementation | 
10.01.17 | Random Forest implementation | 
10.15.17 | GUI | 
10.20.17 | Project release 1.0 | 
10.28.17 | Add implementation for other exchanges (traditional & cryptos) | 

#### Misc. Todo
* Add Style Guide and Contributor doc for contributors
* Update docs when each task on the roadmap is completed, do NOT wait until the project is over!
* Integration/Unit test each functionality before pushing/merging code to master
* Implement other machine learning algorithms with the same dataset, compare results
