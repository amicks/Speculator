from pandas import crosstab
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

class RandomForest(RandomForestClassifier):
    """ Random Forest Classifier using a DataFrame from a Market instance

    Attributes:
        features: Pandas DataFrame, X axis of features
        targets: Pandas Series, Y axis of targets
    
    All other attributes and functions are defined
    within Scikit Learn's RandomForestClassifier class.
    """
    def __init__(self, features, targets, **kwargs):
        """ Inits a Random Forest Classifier with a market attribute

        Args:
            **kwargs: Scikit Learn's RandomForestClassifier kwargs
        """
        # Init model
        super().__init__(**kwargs)

        # Set axes
        self.features = features
        self.targets = targets

        # Train model
        self.fit(features.train, targets.train)

    def feature_importances(self):
        """ Return list of features and their importance in classification """
        feature_names = [feature for feature in self.features.train]
        return list(zip(feature_names, self.feature_importances_))

    def confusion_matrix(self, actual, preds):
        """ Confusion matrix of actual set to predicted set """
        return crosstab(actual, preds, rownames=['(A)'], colnames=['(P)'])

    def accuracy(self, actual, preds):
        """ Accuracy score of actual set to predicted set """
        return accuracy_score(actual, preds)

