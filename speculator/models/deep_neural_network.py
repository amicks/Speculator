import numpy as np
import pandas as pd
from speculator import market
import tensorflow as tf

class DeepNeuralNetwork(tf.estimator.DNNClassifier):
    def __init__(self, features, targets, **kwargs):
        feature_columns = [tf.feature_column.numeric_column(k) \
                           for k in features.train.columns]
        super().__init__(feature_columns=feature_columns,
                         hidden_units=[10, 20, 10],
                         n_classes=len(market.TARGET_CODES))

        # Set axes
        self.features = features
        self.targets = targets

        # Train model
        self.fit(features.train, y=targets.train)

    def fit(self, x, y=None):
        input_fn = self.get_input_fn(x,
                                     y=y,
                                     batch_size=128,
                                     queue_capacity=1000,
                                     shuffle=True,
                                     num_threads=1,
                                     num_epochs=None)
        self.train(input_fn=input_fn, steps=2000)

    def get_input_fn(self, x, y=None, shuffle=True, **kwargs):
        return tf.estimator.inputs.pandas_input_fn(x,
                                                   y=y,
                                                   shuffle=shuffle,
                                                   **kwargs)

    def accuracy(self):
        input_fn = self.get_input_fn(self.features.test, y=self.targets.test)
        return self.evaluate(input_fn)

    def _predict(self, x, y=None):
        input_fn = self.get_input_fn(x, y=y)
        # TF returns a dict generator, convert to list
        pred = list(self.predict(input_fn=input_fn))

        # Interested in classes key, convert "b'$trend'" value to int
        return [int(p['classes'][0]) for p in pred]
        

