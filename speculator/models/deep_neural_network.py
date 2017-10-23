import numpy as np
import pandas as pd
from speculator import market
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)

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

    def accuracy(self, x, y):
        input_fn = self.get_input_fn(x, y)
        return self.evaluate(input_fn)['accuracy']

    def _predict_trends(self, x, y=None):
        input_fn = self.get_input_fn(x, y=y)
        # TF returns a dict generator, convert to list
        preds = list(self.predict(input_fn=input_fn))
        return [int(p['class_ids'][0]) for p in preds]
        
    def _predict_logs(self, x, y=None):
        input_fn = self.get_input_fn(x, y=y)
        # TF returns a dict generator, convert to list
        preds = list(self.predict(input_fn=input_fn))
        return [list(p['logits']) for p in preds]

    def _predict_probas(self, x, y=None):
        input_fn = self.get_input_fn(x, y=y)
        # TF returns a dict generator, convert to list
        preds = list(self.predict(input_fn=input_fn))
        return [list(p['probabilities']) for p in preds]
