# Contributing to Speculator
Speculator is still very early in development, but as of 09/16/17, most foundational components are implemented.
A few technical analysis features have been calculated from Poloniex API's market data.  These features have been fed into a RandomForest classifier to predict a test set's market trend towards bearish, bullish, or neutral behavior.
There is still much more to add to the project, regardless of your experience level, and as such, this is a learning experience for every contributor.
There are simple and extremely complex technical analysis indicators.  More machine learning classification models should also be implemented.  A presentable display, whether by interactive GUI or plots, will eventually be needed.  The code must conform to the style guide.  A full list of planned features is in the roadmap below.  If anyone has ideas that would further the development of this project, do not hesitate to implement them and submit a pull request.

### Style Guide
The style guide should be followed as closely as possible, but use your best judgement on fringe scenarios.  However, detailed docstrings and naming conventions must be followed.
The [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) is being used as of 09/16/17.
All code should be updated to reflect this, but if anything does not conform, feel free to contribute.

### Testing
Every function in the features and utils packages are unit tested.  Only after successfully passing unit tests, should these functions be incorporated with other unit tested functions.  The result will be integration tested.  These tests must pass.  This requirement ensures a higher probability of success as a whole, and in the case of failure, helps pinpoint the root when debugging.

#### Running Unit/Integration Tests
```
cd $SPECULATOR_PATH/speculator/tests
python -m unittest discover
```
This test must run successfully with zero errors before pushing to master.

#### Travis-CI
Every pull request is checked through Travis-CI before being merged, validating functionality across all systems and eliminating any special local configurations.

### Roadmap
Date | Task | Status 
---  | ---  | ---
09.03.17 | Relative Strength Index (RSI) & Stochastic Oscillator (SO) algorithms | Done
09.04.17 | RSI and SO implementations with Poloniex | Done
09.05.17 | Simple Moving Average (SMA) algorithm & implementation | Done
10.01.17 | Random Forest implementation | Done
10.15.17 | Deep Neural Network implementation | Done
11.07.17 | On Balance Volume (OBV) algorithm | 
11.15.17 | On Balance Volume (OBV) implementation | 
12.15.17 | Website in JavaScript with React/Redux for easy GUI | In Progress
01.01.18 | Project release 1.0 | 
ongoing  | Add implementation for other exchanges (traditional & cryptos) | 

### Todo:
* Implement other machine learning models to be used with the same dataset, compare results.  Possible models include Support Vector Machines, Neural Networks, and Naive Bayes classifier.
* Add more technical analysis indicators that not only focus on market momentum and buy/sell signals.  Possible types of indicators include volatility of the market and on balance volume.

### Final Note:
The natural volatility in the current state of cryptocurrency markets from pump-and-dumps, fear of missing out, and network effects make it much harder to predict the future price when compared to traditional markets.
Therefore, it is important to not tunnel-vision on standard features and models, and consciously select which features and models provide the best benefit to Speculator. 
