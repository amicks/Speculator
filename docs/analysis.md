# Analysis Module
This module provides a way to take some requested market data from today to a previous date, and feed it into a machine learning interface, such as the Random Forest classifier.

## Market Class
Market takes a market symbol and previous date and, through a series a parsing, converts it into an interface ready for machine learning.

## Random Forest Class
RandomForest takes the prepared data from Market, creates a classifier, trains it, and predicts the test set.  Some results, such as the accuracy, confusion matrix, and feature importance are readily available.  Others can be accessed through the 'classifier' attribute, which is an instance of a sklearn RandomForestClassifier.  If further analysis is desired, it can easily be calculated through the given data.

### Dependencies:
* [scikit-learn](http://scikit-learn.org/stable/install.html), ` pip install scikit-learn `
* [pandas](https://pandas.pydata.org/pandas-docs/stable/install.html), ` pip install pandas `
