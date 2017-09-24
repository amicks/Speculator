import numpy as np
import pandas as pd
from speculator import market
import tensorflow as tf

class DeepNeuralNetwork(tf.estimator.DNNClassifier):
    def __init__(self, features, targets, **kwargs):
        # Init model
        x_shape = len(features.train.columns) 
        feature_columns = [tf.feature_column.numeric_column(k) \
                           for k in features.train.columns]
        super().__init__(feature_columns=feature_columns,
                         hidden_units=[10, 20, 10],
                         n_classes=len(market.TARGET_CODES))

        # Set axes
        self.features = features
        self.targets = targets

        # Train model
        self.train_input_fn = self.get_input_fn(features.train, targets.train,
                                                batch_size=128,
                                                queue_capacity=1000,
                                                shuffle=False,
                                                num_threads=1,
                                                num_epochs=None)
        self.train(input_fn=self.train_input_fn, steps=2000)

        self.test_input_fn = self.get_input_fn(features.test, targets.test,
                                               batch_size=128,
                                               queue_capacity=1000,
                                               shuffle=False,
                                               num_threads=1,
                                               num_epochs=1)

        accuracy_score = self.evaluate(input_fn=test_input_fn)['accuracy']
        print(accuracy_score)

    def get_input_fn(self, x, y, **kwargs):
        return tf.estimator.inputs.pandas_input_fn(x=x, y=y, **kwargs)

    def predict(
