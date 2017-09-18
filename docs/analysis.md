# Analysis Module
This module provides a way to take some requested market data from today to a previous date, and feed it into a machine learning interface, such as the Random Forest classifier.

## Market Class
Market takes a market symbol and previous date and, through a series of parsing, converts it into a Pandas Dataframe.  This results in an easy-to-use interface ready for machine learning.

## Random Forest Class
RandomForest takes the prepared data from Market, creates a classifier, trains it.  Most useful attributes and functions are inherited through [sklearn's RandomForestClassifier class](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html).  If further analysis is desired, it can easily be calculated through the given data.

### Dependencies:
* [scikit-learn](http://scikit-learn.org/stable/install.html), ` pip install scikit-learn `
* [pandas](https://pandas.pydata.org/pandas-docs/stable/install.html), ` pip install pandas `
