from flask import Flask, request
from flask_cache import Cache
from flask_restful import Resource, Api, reqparse
from speculator import market
from webargs import fields
from webargs.flaskparser import use_kwargs

app = Flask(__name__)
api = Api(app)

# TODO: Add private API with Redis
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

@api.resource('/api/public/predict')
class predict(Resource):
    """ Predict the next price of a symbol like USDT_BTC """
    # TODO: Add private POST/PUT/DELETE methods

    @use_kwargs({
        'model': fields.Str(missing='rf'),
        'symbol': fields.Str(missing='USDT_BTC'),
        'unit': fields.Str(missing='month'),
        'count': fields.Int(missing=6),
        'period': fields.Integer(missing=86400),
        'partition': fields.Integer(missing=14),
        'delta': fields.Integer(missing=25),
        'seed': fields.Integer(missing=None),
        'trees': fields.Integer(missing=10),
        'jobs': fields.Integer(missing=1),
        'longs': fields.DelimitedList(fields.Str(), missing=[])
    })
    @cache.memoize(3600)
    def get(self, model, symbol, unit, count, period,
            partition, delta, seed, trees, jobs, longs):
        m = market.Market(symbol=symbol, unit=unit,
                          count=count, period=period)

        features = m.set_features(partition=partition)
        features = m.set_long_features(features,
                                       columns_to_set=longs,
                                       partition=partition)

        targets = market.set_targets(features, delta=delta)
        features = features.drop(['close'], axis=1)

        model = market.setup_model(features[:-1], targets,
                                   model_type=model.lower(),
                                   seed=seed,
                                   n_estimators=trees,
                                   n_jobs=jobs)

        next_date = features.tail(1) # Remember the entry we didn't train?  Predict it.

        trend = market.target_code_to_name(model._predict_trends(next_date)[0])
        accuracy = model.accuracy(model.features.test, model.targets.test)
        proba = model._predict_probas(next_date)
        proba_log = model._predict_logs(next_date) # Logarithmic scale

        return {
            "trend": trend,
            "test_set_accuracy": "{0:.3f}%".format(100 * accuracy),
            "probabilities": {
                market.target_code_to_name(code): p for code, p in enumerate(proba[0])
            }
        }

if __name__ == '__main__':
    app.run(debug=True)
